#!/usr/bin/env python3
"""Upload PROTEUS spectral files to Zenodo as records of the PROTEUS community.

Each pair of codename and band count becomes one Zenodo record, titled
``spectral_files/<Codename>/<nband>``, which holds these loose files:

    <Codename>.sf, <Codename>.sf_k         spectral file and its k-coefficient file
    <Codename>.chk, <Codename>.chk_k       BLAKE2b checksums of the two files above
    <Codename>_Tmake_spectralfile_<timestamp>.log   generator log
    <Codename>_*.log                       logs of prep_spec, Ccorr_k and Cscatter_average,
                                           with their monitor logs, except the Cscatter_average
                                           monitor log <Codename>_droplet_mon.log (1.7 GB with
                                           2048 bands); empty logs are skipped
    <Codename>_Tmake_spectralfile.py       generator script (settings backup), only if
                                           its settings agree with the generator log

This layout follows the existing records (for example
https://zenodo.org/records/15799731): one record per codename and band count,
loose files, keyword "spectral_files", licence CC-BY-4.0, resource type
dataset, each record its own concept (no version chain). AGNI's
src/get_data.sh downloads <Codename>.sf and <Codename>.sf_k from a record by
file name, and fwl-io (used by PROTEUS) downloads every file of a record, so
the zip archive made by Tpackage_spectralfile.py is not uploaded: AGNI would
not find the files inside it, and fwl-io would download it in addition to the
loose files.

The files are read from

    ROOT/<Codename>/<nband>/

Sub-folders of ROOT whose names start with '_' or '.' (such as _old) are
ignored.

Steps
-----
1. Discover and check (always; offline). For each record: parse block 0 of the
   .sf (absorbers, continua, band count) and the generator log (SOCRATES
   version and git hash, spectraltools version, build time, gases with their
   sources and maximum mass paths, band-selection method, continua and their
   sources); check them against each other and against the folder
   name; compute MD5, BLAKE2b and CRC32 of each file in one pass; compare the
   BLAKE2b of .sf and .sf_k with the .chk and .chk_k files; compare each file
   with its copy in <Codename>.zip (size and CRC32) when the zip is present;
   refuse a .sf or .sf_k that contains "NaN", and a .sf_k that contains the
   netCDF fill value 9.969210E+36 (an input netCDF that was never filled) or any
   value above 1e30, reporting the gas or continuum index and the number of
   lines affected. The generator script is parsed
   (not run) and left out, with a warning, if its alias, gases, sources, mass
   paths or other settings differ from the log: Tpackage_spectralfile.py
   stores the Tmake_spectralfile.py present at packaging time, which may
   have been edited for another spectral file by then.
2. Dry run (the default). Print the records, their metadata, the files with
   sizes and checksums, and exit. No network request is made and no file is
   written.
3. --upload. List the user's depositions, then create one draft per record
   (or resume the draft with the same title), set its metadata (with the build
   date of the file as the publication date, and a request to reserve the
   record's DOI, which is logged), upload the files with a streamed PUT to the
   record's bucket, and compare the MD5 that Zenodo reports for each file with
   the local MD5. The run stops at the first mismatch or error. Nothing is
   published.
4. --upload --publish. As 3, then publish each verified draft. A published
   record can no longer be deleted by its owner.

At the end of an --upload run, a Markdown table of codename, band count, record
URL and DOI is printed for the documentation (docs/Reference/proteus_spectral_file_reference.md).

Safety defaults
---------------
* Dry run unless --upload is given; publishing needs --publish as well.
* The target is the sandbox (https://sandbox.zenodo.org) unless --production
  is given. Sandbox records use test DOIs and can be discarded, so a mistaken
  run there has no lasting effect.
* On production, the script asks for confirmation before it creates or changes
  drafts, and again before it publishes; --yes skips both questions.
* The access token is read only from the environment variable ZENODO_TOKEN
  (production) or ZENODO_SANDBOX_TOKEN (sandbox), and only when --upload is
  given. It is never printed or logged. It needs the scopes deposit:write and
  deposit:actions.

Resuming
--------
No state is kept between runs: Zenodo is the only record of what has been
uploaded. Each --upload run lists the user's depositions and matches them to
the records by title (spectral_files/<Codename>/<nband>), so a failed run can
be repeated with the same command: a draft with the same title is reused, files
already present with the correct MD5 are not uploaded again, and records
already published are skipped. Two drafts with the same title stop the run.

Community
---------
The record is added to the community through the "communities" field of the
deposit metadata, the route documented in Zenodo's developer documentation
(https://developers.zenodo.org/#deposit-metadata). The community curators may have to accept the
request; after publishing, the script reports whether the record lists the
community yet. The proteus_framework community exists only on production, so
on the sandbox no community is requested unless --community names one.

Examples
--------
    # dry run over every family and band count below ROOT
    python Tupload_zenodo.py ROOT

    # dry run for one record, printing the exact metadata JSON
    python Tupload_zenodo.py ROOT --family Snowline --nband 256 --show-json

    # test run on the sandbox: drafts and uploads, no publishing
    ZENODO_SANDBOX_TOKEN=... python Tupload_zenodo.py ROOT --nband 32 --upload \
        --creator "Family, Given" --orcid 0000-0000-0000-0000

    # production: drafts and uploads, then publish (asks for confirmation)
    ZENODO_TOKEN=... python Tupload_zenodo.py ROOT --production --upload --publish \
        --creator "Family, Given" --orcid 0000-0000-0000-0000
"""

# This script deliberately does not import src.utils: that module raises
# without RAD_DIR and spectraltools/output/, which an upload does not need.

from __future__ import annotations

import argparse
import ast
import datetime as dt
import math
import hashlib
import html
import json
import logging
import os
import re
import sys
import time
import zipfile
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

log = logging.getLogger("fwl.Tupload_zenodo")

# ---------------------------------------------------------------------------
# Conventions of the existing PROTEUS spectral-file records on Zenodo,
# read from https://zenodo.org/api/records?communities=proteus_framework&q=keywords:spectral_files
# ---------------------------------------------------------------------------

HOSTS = {"sandbox": "https://sandbox.zenodo.org", "production": "https://zenodo.org"}
TOKEN_VARS = {"sandbox": "ZENODO_SANDBOX_TOKEN", "production": "ZENODO_TOKEN"}

COMMUNITY = "proteus_framework"
KEYWORDS = ["spectral_files"]          # the community page filters on this subject
LICENSE = "cc-by-4.0"
UPLOAD_TYPE = "dataset"
ACCESS_RIGHT = "open"

DOCS_URL = "https://proteus-framework.org/SOCRATES/Reference/proteus_spectral_file_reference.html"
# Shown in the "Repository URL" field of the record. Zenodo keeps it as the custom field code:codeRepository,
# which its legacy API returns under metadata.custom; the deposit API is not documented to accept it, so the
# script checks that the draft keeps it.
REPO_URL = "https://github.com/FormingWorlds/SOCRATES"

# Zenodo developer documentation, legacy deposit API (still the documented
# REST API of Zenodo after its move to InvenioRDM):
#  - deposit metadata, including "communities": [{"identifier": ...}]:
COMMUNITY_DOC = "https://developers.zenodo.org/#deposit-metadata"
#  - bucket upload (streamed PUT to links.bucket, up to 50 GB per file):
BUCKET_DOC = "https://developers.zenodo.org/#quickstart-upload"
# The InvenioRDM review request (PUT /api/records/{id}/draft/review with type
# "community-submission", https://inveniordm.docs.cern.ch/reference/rest_api_reviews/)
# is not used: Zenodo's developer documentation lists its Communities API as
# "currently in testing" and does not document that route.

USER_AGENT = "SOCRATES-spectraltools-Tupload_zenodo/1.0"
CONNECT_TIMEOUT = 30.0  # seconds

SOURCE_NAMES = {"exocross": "ExoCross", "dace": "DACE", "hitran": "HITRAN",
                "exomol": "ExoMol", "direct": "direct"}

# Band-selection methods, as described in Tmake_spectralfile.py and
# src/spectral.py:best_bands.
BAND_METHODS = {
    0: "linearly spaced in wavenumber",
    1: "logarithmically spaced in wavenumber",
    2: "linearly spaced in wavenumber, with a single band covering long wavelengths",
    3: "logarithmically spaced in wavenumber, with a few linearly spaced bands covering long wavelengths",
    4: "piecewise density (linear, logarithmic, logarithmic)",
    5: "selected by the density of the Planck function at given temperatures",
    9: "matching the legacy 318-band spectral file",
}

_LOG_FORMAT = logging.Formatter(fmt="[%(asctime)s %(levelname)7s] %(message)s",
                                datefmt="%H:%M:%S")


class CheckError(Exception):
    """A local file is missing or inconsistent; nothing should be uploaded."""


class ZenodoError(RuntimeError):
    """A request to Zenodo failed or returned something unexpected."""


# ---------------------------------------------------------------------------
# Local files
# ---------------------------------------------------------------------------

@dataclass
class LocalFile:
    name: str
    path: Path
    size: int = 0
    md5: str = ""
    blake2b: str = ""
    crc32: int = 0
    nan_count: int = 0


@dataclass
class LogInfo:
    path: Path
    build_time: dt.datetime
    tools_version: str = ""
    socrates_version: str = ""
    git_hash: str = ""
    alias: str = ""
    nband: int = 0
    source: str = ""
    gases: list = field(default_factory=list)        # (formula, source, maxpath string)
    n_gases: int = 0
    numin: str = ""
    numax: str = ""
    dnu: str = ""
    method: int = -1
    masspath: str = ""
    uv: bool | None = None
    drops_param: bool | None = None
    n_tp: int = 0
    line_absorbers: list = field(default_factory=list)
    continua: list = field(default_factory=list)      # "A-B"
    continuum_sources: dict = field(default_factory=dict)
    droplets: bool | None = None


@dataclass
class Item:
    codename: str
    nband: int
    folder: Path
    files: list = field(default_factory=list)        # LocalFile, in upload order
    block0: dict = field(default_factory=dict)
    log: LogInfo | None = None
    excluded: list = field(default_factory=list)     # (file name, reason)
    zip_checked: bool = False
    metadata: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return f"{self.codename}/{self.nband}"

    @property
    def title(self) -> str:
        return f"spectral_files/{self.codename}/{self.nband}"

    @property
    def total_size(self) -> int:
        return sum(f.size for f in self.files)


def human_size(n: int) -> str:
    for unit in ("B", "KiB", "MiB", "GiB"):
        if n < 1024 or unit == "GiB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n} B"


def hash_file(lf: LocalFile, scan_nan: bool) -> None:
    """Fill size, MD5, BLAKE2b (as Tcalc_checksum.py), CRC32 and the NaN count, in one pass."""
    md5 = hashlib.md5()
    b2 = hashlib.blake2b()
    crc = 0
    size = 0
    nans = 0
    tail = b""
    with lf.path.open("rb") as f:
        while chunk := f.read(1 << 22):
            md5.update(chunk)
            b2.update(chunk)
            crc = zlib.crc32(chunk, crc)
            size += len(chunk)
            if scan_nan:
                # Fortran writes a NaN as "NaN"; keep two bytes across chunk edges
                buf = tail + chunk
                nans += buf.count(b"NaN")
                tail = buf[-2:]
    lf.size = size
    lf.md5 = md5.hexdigest()
    lf.blake2b = b2.hexdigest()
    lf.crc32 = crc & 0xFFFFFFFF
    lf.nan_count = nans


# ---------------------------------------------------------------------------
# Implausible values in the k-coefficient file
# ---------------------------------------------------------------------------

# netCDF default fill value for float (NC_FILL_FLOAT), written as 9.969210E+36 in a
# .sf_k when Ccorr_k reads a variable that was never filled.
FILL_VALUE = 9.969209968386869e36
# No valid entry of a .sf_k comes near this: in the files checked so far every value,
# the pressure grid included, stays below 1e11.
K_LIMIT = 1.0e30

# "*BLOCK: <name>" or "Band: <b>, gas|continuum: <i>" section headers of a .sf_k
_SFK_SECTION = re.compile(rb"^\*BLOCK:\s*([^\n]*?)\s*$|^Band:\s*(\d+),\s*(gas|continuum):\s*(\d+)", re.M)
# Cheap pre-filter for a value >= 1e30: exponent +30..+99, a three-digit exponent
# written without 'E' (Fortran), Infinity, or a field overflow written as asterisks
_SFK_BIG = re.compile(rb"[Ee]\+(?:3\d|[4-9]\d)|\d\+\d{3}|Infinity|\*{3,}")


def scan_large_values(path: Path) -> dict:
    """Find netCDF fill values and values above K_LIMIT in a .sf_k, by section.

    Returns {(block, kind, index): {"lines", "fill", "other", "bands"}}, where block
    is the .sf_k block name (e.g. "k-table", "continuum k-table"), kind is "gas" or
    "continuum", and index is the absorber or continuum index of block 0 of the .sf
    (kind "header" with index 0 for the lookup grid before the first section).
    """
    bad = {}
    cur = ("", "header", 0, 0)   # block, kind, index, band

    def _section(m, c):
        if m.group(1) is not None:
            return (m.group(1).decode(errors="replace"), "header", 0, 0)
        return (c[0], m.group(3).decode(), int(m.group(4)), int(m.group(2)))

    carry = b""
    with path.open("rb") as f:
        while True:
            chunk = f.read(1 << 24)
            buf = carry + chunk
            if not buf:
                break
            if chunk:                       # keep a partial last line for the next chunk
                cut = buf.rfind(b"\n") + 1
                if cut == 0:
                    carry = buf
                    continue
                buf, carry = buf[:cut], buf[cut:]
            else:
                carry = b""
            if not _SFK_BIG.search(buf):    # fast path: only track the section headers
                for m in _SFK_SECTION.finditer(buf):
                    cur = _section(m, cur)
            else:
                for line in buf.split(b"\n"):
                    m = _SFK_SECTION.match(line)
                    if m:
                        cur = _section(m, cur)
                        continue
                    if not _SFK_BIG.search(line):
                        continue
                    n_fill = n_other = 0
                    for tok in line.split():
                        try:
                            v = float(tok)
                        except ValueError:
                            v = math.inf
                        if math.isclose(v, FILL_VALUE, rel_tol=1e-6):
                            n_fill += 1
                        elif not v <= K_LIMIT:
                            n_other += 1
                    if n_fill or n_other:
                        rec = bad.setdefault(cur[:3], {"lines": 0, "fill": 0, "other": 0, "bands": set()})
                        rec["lines"] += 1
                        rec["fill"] += n_fill
                        rec["other"] += n_other
                        rec["bands"].add(cur[3])
            if not chunk:
                break
    return bad


def describe_large_values(bad: dict, b0: dict, nband: int) -> str:
    """One phrase per affected section, naming the gas or continuum from block 0."""
    parts = []
    for (block, kind, index), r in sorted(bad.items()):
        if kind == "gas" and 1 <= index <= len(b0["absorbers"]):
            what = f"gas {index} ({b0['absorbers'][index - 1]})"
        elif kind == "continuum" and 1 <= index <= len(b0["continua"]):
            what = f"continuum {index} ({b0['continua'][index - 1]})"
        else:
            what = f"{kind} {index}"
        vals = []
        if r["fill"]:
            vals.append(f"{r['fill']} netCDF fill values 9.969210E+36")
        if r["other"]:
            vals.append(f"{r['other']} other values above {K_LIMIT:.0e}")
        parts.append(f"'{block}' {what}: {r['lines']} lines in {len(r['bands'])} of {nband} bands "
                     f"({', '.join(vals)})")
    return "; ".join(parts)


# ---------------------------------------------------------------------------
# Spectral file block 0 and the SOCRATES gas list
# ---------------------------------------------------------------------------

def gas_list_path() -> Path:
    """Find gas_list_pcf.F90 in this SOCRATES tree, or below RAD_DIR."""
    rel = Path("src") / "radiance_core" / "gas_list_pcf.F90"
    candidates = [Path(__file__).resolve().parent.parent / rel]
    if os.environ.get("RAD_DIR"):
        candidates.append(Path(os.environ["RAD_DIR"]) / rel)
    for c in candidates:
        if c.is_file():
            return c
    raise CheckError("Cannot find gas_list_pcf.F90 (looked in: %s)"
                     % ", ".join(str(c) for c in candidates))


def read_gas_list(path: Path) -> tuple[list, list]:
    """Return the formulae (header_gas) and long names (name_absorb), indexed by identifier-1."""
    text = path.read_text()

    def _array(name: str) -> list:
        m = re.search(r"PARAMETER\s*::\s*%s\(npd_gases\)\s*=\s*\(/(.*?)/\)" % name, text, re.S)
        if m is None:
            raise CheckError(f"Cannot find {name} in {path}")
        return [s.strip() for s in re.findall(r"['\"]([^'\"]*)['\"]", m.group(1))]

    formulae, names = _array("header_gas"), _array("name_absorb")
    if len(formulae) != len(names) or not formulae:
        raise CheckError(f"header_gas and name_absorb differ in length in {path}")
    return formulae, names


def parse_block0(sf: Path, formulae: list, names: list) -> dict:
    """Read the band count, absorbers and continua from block 0 of a spectral file."""
    with sf.open("r", errors="replace") as f:
        first = f.readline()
        if not re.match(r"\*BLOCK:\s*TYPE\s*=\s*0\s*:", first):
            raise CheckError(f"{sf.name}: does not start with block 0")
        lines = []
        for line in f:
            if line.startswith("*END"):
                break
            lines.append(line.rstrip("\n"))
        else:
            raise CheckError(f"{sf.name}: block 0 has no *END")
    text = "\n".join(lines)

    def _int(pattern: str, default=None) -> int:
        m = re.search(pattern, text)
        if m is None:
            if default is None:
                raise CheckError(f"{sf.name}: block 0 lacks '{pattern}'")
            return default
        return int(m.group(1))

    nband = _int(r"Number of spectral bands\s*=\s*(\d+)")
    n_abs = _int(r"Total number of gaseous absorbers\s*=\s*(\d+)")
    n_cont = _int(r"Total number of generalised continua\s*=\s*(\d+)", default=0)

    absorbers, long_names = [], []
    i = next((k for k, l in enumerate(lines) if "Absorber(identifier and name)" in l), None)
    if n_abs and i is None:
        raise CheckError(f"{sf.name}: block 0 lacks the list of absorbers")
    for k in range(n_abs):
        m = re.match(r"\s*(\d+)\s+(\d+)\s+(\S.*?)\s*$", lines[i + 1 + k])
        if m is None or int(m.group(1)) != k + 1:
            raise CheckError(f"{sf.name}: cannot read absorber line '{lines[i + 1 + k]}'")
        ident, name = int(m.group(2)), m.group(3)
        if not 1 <= ident <= len(formulae):
            raise CheckError(f"{sf.name}: absorber identifier {ident} is not in the SOCRATES gas list")
        if names[ident - 1] != name:
            raise CheckError(f"{sf.name}: absorber {ident} is '{name}' in block 0 but "
                             f"'{names[ident - 1]}' in gas_list_pcf.F90")
        absorbers.append(formulae[ident - 1])
        long_names.append(name)

    continua = []
    if n_cont:
        j = next((k for k, l in enumerate(lines) if "Gas 1(index and name)" in l), None)
        if j is None:
            raise CheckError(f"{sf.name}: block 0 lacks the list of continua")
        for k in range(n_cont):
            line = lines[j + 1 + k]
            m = re.match(r"\s*(\d+)\s+(\d+)\s+(\S.*?)\s{2,}(\d+)\s+(\S.*?)\s*$", line)
            if m is None or int(m.group(1)) != k + 1:
                raise CheckError(f"{sf.name}: cannot read continuum line '{line}'")
            g1, g2 = int(m.group(2)), int(m.group(4))
            for g, name in ((g1, m.group(3)), (g2, m.group(5))):
                if not 1 <= g <= n_abs or long_names[g - 1] != name:
                    raise CheckError(f"{sf.name}: continuum line '{line}' does not match the absorbers")
            continua.append(f"{absorbers[g1 - 1]}-{absorbers[g2 - 1]}")

    return {"nband": nband, "absorbers": absorbers, "continua": continua}


# ---------------------------------------------------------------------------
# Generator log (written by Tmake_spectralfile.py)
# ---------------------------------------------------------------------------

def parse_log(path: Path) -> LogInfo:
    m = re.search(r"_Tmake_spectralfile_(\d{8}T\d{6})\.log$", path.name)
    if m is None:
        raise CheckError(f"{path.name}: no time stamp in the log name")
    info = LogInfo(path=path, build_time=dt.datetime.strptime(m.group(1), "%Y%m%dT%H%M%S"))

    current_cia = None
    for raw in path.read_text(errors="replace").splitlines():
        line = re.sub(r"^\[[^\]]*\]\s?", "", raw)  # drop "[hh:mm:ss LEVEL] "
        s = line.strip()
        if m := re.search(r"Spectral Tools Wizard \(version (\S+)\)", s):
            info.tools_version = m.group(1)
        elif m := re.match(r"SOCRATES version:\s*(\S+)", s):
            info.socrates_version = m.group(1)
        elif m := re.match(r"SOCRATES git hash:\s*(\S+)", s):
            info.git_hash = m.group(1)
        elif m := re.match(r"source:\s+(\S+)$", s):
            info.source = m.group(1)
        elif m := re.match(r"gases:\s+\(N=(\d+)\)", s):
            info.n_gases = int(m.group(1))
        elif m := re.match(r"(\S+) from (\S+)\s+maxpath\s+(\S+) kg/m2$", s):
            info.gases.append((m.group(1), m.group(2), m.group(3)))
        elif m := re.match(r"alias:\s+(\S+)$", s):
            info.alias = m.group(1)
        elif m := re.match(r"nband:\s+(\d+)$", s):
            info.nband = int(m.group(1))
        elif m := re.match(r"numin, numax, dnu\s*:\s*(\S+), (\S+), (\S+) cm-1", s):
            info.numin, info.numax, info.dnu = m.groups()
        elif m := re.match(r"method:\s+(\d+)$", s):
            info.method = int(m.group(1))
        elif m := re.match(r"masspath:\s+(\S+) kg/m2$", s):
            info.masspath = m.group(1)
        elif m := re.match(r"UV:\s+(True|False)$", s):
            info.uv = m.group(1) == "True"
        elif m := re.match(r"drops:\s+(True|False)$", s):
            info.drops_param = m.group(1) == "True"
        elif m := re.match(r"n_tp:\s+(\d+)$", s):
            info.n_tp = int(m.group(1))
        elif m := re.match(r"line absorption:\s*(.*)$", s):
            info.line_absorbers = [] if "(none)" in m.group(1) else m.group(1).split()
        elif m := re.match(r"CIA:\s*(.*)$", s):
            info.continua = [] if "(none)" in m.group(1) else m.group(1).split()
        elif m := re.match(r"water droplets:\s*(yes|no)$", s):
            info.droplets = m.group(1) == "yes"
        elif m := re.match(r"Calculating k-coefficients for '([^']+)' CIA", s):
            current_cia = m.group(1)
        elif current_cia and "Using HITRAN CIA database" in s:
            info.continuum_sources[current_cia] = "HITRAN CIA"
            current_cia = None
        elif current_cia and "MT_CKD" in s:
            info.continuum_sources[current_cia] = "MT_CKD"
            current_cia = None

    missing = [k for k, v in (("SOCRATES version", info.socrates_version),
                              ("SOCRATES git hash", info.git_hash),
                              ("alias", info.alias), ("nband", info.nband),
                              ("method", info.method >= 0), ("masspath", info.masspath),
                              ("gases", info.gases), ("line absorption", info.line_absorbers))
               if not v]
    if missing:
        raise CheckError(f"{path.name}: cannot find {', '.join(missing)} in the log")
    return info


# ---------------------------------------------------------------------------
# Generator script (backed up by Tpackage_spectralfile.py)
# ---------------------------------------------------------------------------

SCRIPT_SETTINGS = ("alias", "vols", "source", "vol_source", "method", "drops", "UV",
                   "numin", "numax", "dnu", "maxpath", "vol_maxpath")


def script_mismatches(path: Path, codename: str, info: LogInfo) -> list:
    """Compare the settings in a generator script with its log; return the differences.

    Tpackage_spectralfile.py stores the Tmake_spectralfile.py present at packaging
    time, which may have been edited for another spectral file since. The script is
    parsed, never run: each setting must have exactly one literal assignment (later
    derived reassignments such as 'numin = max(numin, ...)' are ignored).
    """
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError as exc:
        return [f"cannot parse ({exc})"]
    values = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id in SCRIPT_SETTINGS):
            try:
                values.setdefault(node.targets[0].id, []).append(ast.literal_eval(node.value))
            except ValueError:
                pass
    problems = [f"{k} has {len(values.get(k, []))} literal assignments"
                for k in SCRIPT_SETTINGS if len(values.get(k, [])) != 1]
    if problems:
        return problems
    s = {k: v[0] for k, v in values.items()}

    def close(a, b) -> bool:  # the log prints 3 significant figures
        return math.isclose(float(a), float(b), rel_tol=1e-2)

    if s["alias"] != codename:
        problems.append(f"alias '{s['alias']}'")
    if sorted(s["vols"]) != sorted(g for g, _, _ in info.gases):
        problems.append(f"gases {s['vols']}")
    else:
        for gas, src, path_str in info.gases:
            if s["vol_source"].get(gas, s["source"]).lower() != src.lower():
                problems.append(f"source of {gas}")
            if not close(s["vol_maxpath"].get(gas, s["maxpath"]), path_str):
                problems.append(f"maximum mass path of {gas}")
    if s["method"] != info.method:
        problems.append(f"method {s['method']}")
    if info.uv is not None and s["UV"] != info.uv:
        problems.append(f"UV {s['UV']}")
    if info.drops_param is not None and s["drops"] != info.drops_param:
        problems.append(f"drops {s['drops']}")
    if not close(s["maxpath"], info.masspath):
        problems.append(f"maxpath {s['maxpath']}")
    for key in ("numin", "numax", "dnu"):
        if getattr(info, key) and not close(s[key], getattr(info, key)):
            problems.append(f"{key} {s[key]}")
    return problems


# ---------------------------------------------------------------------------
# Discovery and checks
# ---------------------------------------------------------------------------

def discover(root: Path, families: list | None, nbands: list | None) -> list:
    """Return (codename, nband, folder) for every ROOT/<Codename>/<nband>/<Codename>.sf."""
    if not root.is_dir():
        raise CheckError(f"Root folder '{root}' does not exist")
    found = []
    for fam in sorted(p for p in root.iterdir() if p.is_dir()):
        if fam.name.startswith(("_", ".")):
            continue
        for nb in sorted((p for p in fam.iterdir() if p.is_dir() and p.name.isdigit()),
                         key=lambda p: int(p.name)):
            if (nb / f"{fam.name}.sf").is_file():
                found.append((fam.name, int(nb.name), nb))
    if families:
        known = sorted({c for c, _, _ in found})
        unknown = [f for f in families if f not in known]
        if unknown:
            raise CheckError(f"Unknown family {unknown}; found {known}")
        found = [x for x in found if x[0] in families]
    if nbands:
        known = sorted({n for _, n, _ in found})
        unknown = [n for n in nbands if n not in known]
        if unknown:
            raise CheckError(f"Band count {unknown} not found for the selected families; found {known}")
        found = [x for x in found if x[1] in nbands]
    if not found:
        raise CheckError(f"No spectral files found below '{root}'")
    return found


def build_item(codename: str, nband: int, folder: Path, formulae: list, names: list) -> Item:
    item = Item(codename=codename, nband=nband, folder=folder)

    # Files to upload, in a fixed order
    required = [f"{codename}.sf", f"{codename}.sf_k", f"{codename}.chk", f"{codename}.chk_k"]
    for name in required:
        if not (folder / name).is_file():
            raise CheckError(f"{item.key}: missing {name}")
    logs = sorted(folder.glob(f"{codename}_Tmake_spectralfile_*.log"))
    if len(logs) != 1:
        raise CheckError(f"{item.key}: expected one {codename}_Tmake_spectralfile_*.log, found {len(logs)}")
    item.log = info = parse_log(logs[0])
    names_up = required + [logs[0].name]

    # Every other log of the build (prep_spec, Ccorr_k and Cscatter_average, with their monitor logs), except
    # the Cscatter_average monitor log, which is far larger than the spectral file itself
    for path in sorted(folder.glob("*.log")):
        if path.name in names_up:
            continue
        if path.name == f"{codename}_droplet_mon.log":
            item.excluded.append((path.name, f"Cscatter_average monitor log, {human_size(path.stat().st_size)}"))
        elif path.stat().st_size == 0:
            item.excluded.append((path.name, "empty file"))
        else:
            names_up.append(path.name)

    # The generator script is uploaded only if its settings agree with the log
    script = folder / f"{codename}_Tmake_spectralfile.py"
    if script.is_file():
        problems = script_mismatches(script, codename, info)
        if problems:
            item.excluded.append((script.name, "settings differ from the log: " + ", ".join(problems)))
        else:
            names_up.append(script.name)
    else:
        item.excluded.append((script.name, "not found"))
    for name, why in item.excluded:
        log.warning("%s: not uploading %s (%s)", item.key, name, why)

    item.files = [LocalFile(name=n, path=folder / n) for n in names_up]
    for lf in item.files:
        hash_file(lf, scan_nan=lf.name in (f"{codename}.sf", f"{codename}.sf_k"))

    sf, sfk, chk, chkk = item.files[:4]

    # BLAKE2b against the .chk files
    for data, chkfile in ((sf, chk), (sfk, chkk)):
        stored = chkfile.path.read_text().strip()
        if stored != data.blake2b:
            raise CheckError(f"{item.key}: BLAKE2b of {data.name} does not match {chkfile.name}")

    # No NaN in the files to be distributed
    for lf in (sf, sfk):
        if lf.nan_count:
            raise CheckError(f"{item.key}: {lf.name} contains {lf.nan_count} 'NaN'")

    # Block 0 against the folder and the log
    item.block0 = parse_block0(sf.path, formulae, names)
    if item.block0["nband"] != nband:
        raise CheckError(f"{item.key}: block 0 has {item.block0['nband']} bands")

    # No unfilled netCDF variable and no absurd value in the k-coefficient file
    bad = scan_large_values(sfk.path)
    if bad:
        raise CheckError(f"{item.key}: {sfk.name} holds implausible values: "
                         + describe_large_values(bad, item.block0, nband))
    if info.nband != nband or info.alias != codename:
        raise CheckError(f"{item.key}: log is for alias '{info.alias}' with {info.nband} bands")
    if info.n_gases and info.n_gases != len(info.gases):
        raise CheckError(f"{item.key}: log lists N={info.n_gases} gases but {len(info.gases)} gas lines")
    if (sorted(item.block0["absorbers"]) != sorted(info.line_absorbers)
            or sorted(g[0] for g in info.gases) != sorted(info.line_absorbers)):
        raise CheckError(f"{item.key}: absorbers differ between block 0 {item.block0['absorbers']}, "
                         f"the log's gas list and its assembled list {info.line_absorbers}")

    def _pairs(lst):
        return sorted(tuple(sorted(p.split("-"))) for p in lst)
    if _pairs(item.block0["continua"]) != _pairs(info.continua):
        raise CheckError(f"{item.key}: continua differ between block 0 {item.block0['continua']} "
                         f"and the log {info.continua}")

    # Compare with the packaged zip (Tpackage_spectralfile.py), if present
    zpath = folder / f"{codename}.zip"
    if zpath.is_file():
        with zipfile.ZipFile(zpath) as zf:
            for lf in item.files:
                try:
                    zi = zf.getinfo(lf.name)
                except KeyError:
                    raise CheckError(f"{item.key}: {lf.name} is not in {zpath.name}") from None
                if zi.file_size != lf.size or zi.CRC != lf.crc32:
                    raise CheckError(f"{item.key}: {lf.name} differs from its copy in {zpath.name}")
        item.zip_checked = True
    return item


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

def display_name(name: str) -> str:
    """'Family, Given' -> 'Given Family'."""
    if ", " in name:
        family, given = name.split(", ", 1)
        return f"{given} {family}"
    return name


def source_name(src: str) -> str:
    return SOURCE_NAMES.get(src.lower(), src)


def describe_html(item: Item, creator_name: str) -> str:
    """Description in the style of the existing records, plus provenance from the log."""
    info, b0 = item.log, item.block0
    e = html.escape
    sf, sfk = item.files[0], item.files[1]

    sources = []
    for _, src, _ in info.gases:
        if source_name(src) not in sources:
            sources.append(source_name(src))
    paras = [
        f"SOCRATES spectral file fitted to {e(' and '.join(sources))} opacities, "
        f"created by {e(display_name(creator_name))}.",
        f"Bands: {b0['nband']}.",
        f"Line absorbers: {e(', '.join(b0['absorbers']))}.",
        "Continuum absorbers: " + (e(", ".join(b0["continua"])) if b0["continua"] else "none") + ".",
    ]
    if info.droplets is not None:
        paras.append("Water droplet scattering: " + ("included." if info.droplets else "not included."))
    if info.uv is not None:
        paras.append("Ultraviolet cross-sections: " + ("included." if info.uv else "not included."))

    gas_txt = "; ".join(f"{e(g)}: {e(source_name(s))}, maximum mass path {e(p)} kg/m2"
                        for g, s, p in info.gases)
    paras.append(f"Line absorption data: {gas_txt}.")
    if b0["continua"]:
        cont_txt = "; ".join(f"{e(c)}: {e(info.continuum_sources.get(c, 'source not stated in the log'))}"
                             for c in b0["continua"])
        paras.append(f"Continuum data: {cont_txt}.")

    method = BAND_METHODS.get(info.method)
    method_txt = f"{info.method}" + (f" ({e(method)})" if method else "")
    build = info.build_time.strftime("%Y-%m-%d %H:%M:%S")
    gen = (f"Generated with SOCRATES {e(info.socrates_version)} (git hash <code>{e(info.git_hash)}</code>)"
           + (f" and spectraltools {e(info.tools_version)}" if info.tools_version else "")
           + f", run started {build} (time stamp of the generator log). "
           f"Band-selection method {method_txt}; default maximum mass path {e(info.masspath)} kg/m2")
    if info.numin:
        gen += (f"; wavenumber range {e(info.numin)} to {e(info.numax)} cm-1, "
                f"sampled at {e(info.dnu)} cm-1")
    if info.n_tp:
        gen += f"; {info.n_tp} pressure-temperature points"
    paras.append(gen + ".")

    paras.append(f"BLAKE2b checksums (also in {e(sf.name.replace('.sf', '.chk'))} and "
                 f"{e(sfk.name.replace('.sf_k', '.chk_k'))}): "
                 f"{e(sf.name)} <code>{sf.blake2b}</code>; {e(sfk.name)} <code>{sfk.blake2b}</code>.")
    has_script = any(lf.name.endswith("_Tmake_spectralfile.py") for lf in item.files)
    programs = ["prep_spec", "Ccorr_k"] + (["Cscatter_average"] if any(
        lf.name.endswith("_droplet.log") for lf in item.files) else [])
    paras.append(f"Files: {e(sf.name)} and {e(sfk.name)} (spectral file and k-coefficients), "
                 "their checksums, the generator log, the logs of the SOCRATES programs run during the build "
                 f"({', '.join(programs[:-1])} and {programs[-1]})"
                 + (", and the generator script." if has_script else "."))
    paras.append(f'Documentation: <a href="{DOCS_URL}">PROTEUS spectral files reference</a> '
                 "in the SOCRATES documentation.")
    return "".join(f"<p>{p}</p>" for p in paras)


def html_to_text(s: str) -> list:
    s = s.replace("</p>", "\n")
    s = re.sub(r'<a href="([^"]*)">([^<]*)</a>', r"\2 (\1)", s)
    s = re.sub(r"<[^>]+>", "", s)
    return [html.unescape(x) for x in s.splitlines() if x.strip()]


def build_metadata(item: Item, creator: dict, community: str) -> dict:
    md = {
        "upload_type": UPLOAD_TYPE,
        "title": item.title,
        "creators": [creator],
        "description": describe_html(item, creator["name"]),
        "access_right": ACCESS_RIGHT,
        "license": LICENSE,
        "keywords": list(KEYWORDS),
        "version": item.log.build_time.strftime("%Y%m%dT%H%M%S"),
        # The date the spectral file was built (time stamp of the generator log)
        "publication_date": item.log.build_time.strftime("%Y-%m-%d"),
        # Reserve the record's DOI on the draft, so that it is known before publishing. Zenodo returns it in
        # metadata.prereserve_doi and registers it with DataCite only when the record is published.
        "prereserve_doi": True,
        "custom": {"code:codeRepository": REPO_URL},
    }
    if community:
        md["communities"] = [{"identifier": community}]
    return md


# ---------------------------------------------------------------------------
# Records found on Zenodo during this run
# ---------------------------------------------------------------------------

class Records:
    """What this run has found or done on Zenodo for each record, keyed '<Codename>/<nband>'. Nothing is
    written to disk: the next run finds the drafts and published records again by title."""

    def __init__(self):
        self.data = {}

    def get(self, key: str) -> dict | None:
        return self.data.get(key)

    def update(self, key: str, **values) -> None:
        self.data.setdefault(key, {}).update(values)


# ---------------------------------------------------------------------------
# Zenodo client (legacy deposit API)
# ---------------------------------------------------------------------------

class _UploadStream:
    """File reader with a length (so requests sends Content-Length) and progress logging."""

    def __init__(self, path: Path, size: int, name: str):
        self._f = path.open("rb")
        self._size = size
        self._name = name
        self._sent = 0
        self._next = 0.25

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        while chunk := self.read(1 << 20):
            yield chunk

    def read(self, n: int = -1) -> bytes:
        chunk = self._f.read(n)
        self._sent += len(chunk)
        if self._size and self._sent / self._size >= self._next:
            log.info("        %s: %3.0f%% sent", self._name, 100.0 * self._sent / self._size)
            while self._sent / self._size >= self._next:
                self._next += 0.25
        return chunk

    def close(self) -> None:
        self._f.close()


def _strip_md5(checksum) -> str:
    return str(checksum or "").removeprefix("md5:")


def _error_text(r) -> str:
    try:
        j = r.json()
        msg = j.get("message", "")
        errs = j.get("errors")
        return f"{msg} {json.dumps(errs)}" if errs else str(msg)
    except ValueError:
        return r.text[:500]


class ZenodoClient:
    def __init__(self, host: str, token: str, timeout: float):
        import requests  # only needed for network actions
        self._requests = requests
        self.host = host.rstrip("/")
        self.api = self.host + "/api"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}", "User-Agent": USER_AGENT})

    def _call(self, method: str, url: str, expect: tuple, retry: bool = True, **kw):
        kw.setdefault("timeout", (CONNECT_TIMEOUT, self.timeout))
        for attempt in (1, 2, 3):
            try:
                r = self.session.request(method, url, **kw)
            except self._requests.RequestException as exc:
                raise ZenodoError(f"{method} {url} failed: {type(exc).__name__}: {exc}") from None
            if r.status_code == 429 and retry and attempt < 3:
                wait = r.headers.get("Retry-After")
                try:
                    wait = float(wait)
                except (TypeError, ValueError):
                    reset = r.headers.get("X-RateLimit-Reset")
                    wait = float(reset) - time.time() if reset and reset.isdigit() else 60.0
                wait = min(max(wait, 1.0), 120.0)
                log.warning("Rate limited by Zenodo; waiting %.0f s", wait)
                time.sleep(wait)
                continue
            if r.status_code in (401, 403) and r.status_code not in expect:
                raise ZenodoError(f"{method} {url} returned HTTP {r.status_code}: {_error_text(r)} "
                                  f"(the token was not accepted: check that it was created on {self.host} "
                                  "with the scopes deposit:write and deposit:actions)")
            if r.status_code not in expect:
                raise ZenodoError(f"{method} {url} returned HTTP {r.status_code}: {_error_text(r)}")
            return r
        raise ZenodoError(f"{method} {url}: still rate limited after 3 attempts")

    def list_depositions(self, page_size: int = 25, max_pages: int = 200) -> list:
        # Zenodo refuses a page size above 25 for any request it does not count as authenticated
        # (HTTP 400), so pages of 25 are requested
        out = []
        for page in range(1, max_pages + 1):
            r = self._call("GET", f"{self.api}/deposit/depositions", (200,),
                           params={"size": page_size, "page": page})
            batch = r.json()
            out.extend(batch)
            if len(batch) < page_size:
                break
        else:
            raise ZenodoError(f"More than {page_size * max_pages} depositions; increase max_pages")
        return out

    def create(self) -> dict:
        # POST is not idempotent: never retried, so a lost response cannot create two drafts
        return self._call("POST", f"{self.api}/deposit/depositions", (201,), retry=False, json={}).json()

    def get(self, dep_id) -> dict:
        return self._call("GET", f"{self.api}/deposit/depositions/{dep_id}", (200,)).json()

    def set_metadata(self, dep_id, metadata: dict) -> dict:
        return self._call("PUT", f"{self.api}/deposit/depositions/{dep_id}", (200,),
                          json={"metadata": metadata}).json()

    def delete_file(self, dep_id, file_id) -> None:
        self._call("DELETE", f"{self.api}/deposit/depositions/{dep_id}/files/{file_id}", (204,))

    def upload(self, bucket: str, lf: LocalFile) -> dict:
        stream = _UploadStream(lf.path, lf.size, lf.name)
        try:
            r = self._call("PUT", f"{bucket}/{quote(lf.name)}", (200, 201), retry=False,
                           data=stream, headers={"Content-Type": "application/octet-stream"})
        finally:
            stream.close()
        return r.json()

    def publish(self, dep_id) -> dict:
        return self._call("POST", f"{self.api}/deposit/depositions/{dep_id}/actions/publish",
                          (202,), retry=False).json()

    def get_record(self, rec_id) -> dict | None:
        try:
            return self._call("GET", f"{self.api}/records/{rec_id}", (200,)).json()
        except ZenodoError as exc:
            log.warning("Could not read the published record: %s", exc)
            return None


def _remote_files(dep: dict) -> dict:
    out = {}
    for f in dep.get("files") or []:
        name = f.get("filename") or f.get("key")
        out[name] = {"id": f.get("id"), "md5": _strip_md5(f.get("checksum")),
                     "size": int(f.get("filesize", f.get("size", -1)))}
    return out


def sync_files(client: ZenodoClient, dep: dict, item: Item) -> dict:
    """Upload missing or differing files, verify every MD5, and return the deposition."""
    dep_id = dep["id"]
    bucket = (dep.get("links") or {}).get("bucket")
    if not bucket:
        raise ZenodoError(f"{item.key}: deposition {dep_id} has no bucket link")
    expected = {lf.name: lf for lf in item.files}
    remote = _remote_files(dep)
    extra = sorted(set(remote) - set(expected))
    if extra:
        raise ZenodoError(f"{item.key}: deposition {dep_id} holds unexpected files {extra}; "
                          "remove them on Zenodo, then run again")
    for lf in item.files:
        rf = remote.get(lf.name)
        if rf and rf["md5"] == lf.md5 and rf["size"] == lf.size:
            log.info("    %s: already uploaded, MD5 matches", lf.name)
            continue
        if rf:
            log.warning("    %s: remote copy differs (MD5 %s), deleting it", lf.name, rf["md5"])
            client.delete_file(dep_id, rf["id"])
        log.info("    %s: uploading %s", lf.name, human_size(lf.size))
        t0 = time.time()
        j = client.upload(bucket, lf)
        got_md5, got_size = _strip_md5(j.get("checksum")), j.get("size")
        if got_md5 != lf.md5 or (got_size is not None and int(got_size) != lf.size):
            raise ZenodoError(f"{item.key}: {lf.name} uploaded with MD5 {got_md5} and size {got_size}, "
                              f"expected {lf.md5} and {lf.size}. Stopping.")
        log.info("    %s: MD5 verified (%.0f s)", lf.name, time.time() - t0)

    # Independent check: list the deposition's files again
    dep = client.get(dep_id)
    remote = _remote_files(dep)
    if set(remote) != set(expected):
        raise ZenodoError(f"{item.key}: deposition {dep_id} lists {sorted(remote)}, "
                          f"expected {sorted(expected)}")
    for name, lf in expected.items():
        if remote[name]["md5"] != lf.md5:
            raise ZenodoError(f"{item.key}: {name} has MD5 {remote[name]['md5']} on Zenodo, "
                              f"expected {lf.md5}")
    return dep


def prepare_draft(client: ZenodoClient, records: Records, item: Item, existing: dict) -> bool:
    """Create the draft of one record, or resume the one with the same title, and upload its files.
    False if a record with this title is already published."""
    matches = existing.get(item.title, [])
    published = [d for d in matches if d.get("submitted")]
    drafts = [d for d in matches if not d.get("submitted")]
    if published:
        log.info("%s: already published (deposition %s); not creating another", item.key, published[0]["id"])
        _record_published(client, records, item, published[0])
        return False
    if len(drafts) > 1:
        raise ZenodoError(f"{item.key}: {len(drafts)} drafts titled '{item.title}' exist "
                          f"({[d['id'] for d in drafts]}); delete the extra ones on Zenodo first")
    if drafts:
        dep = drafts[0]
        log.info("%s: resuming draft %s", item.key, dep["id"])
    else:
        dep = client.create()
        log.info("%s: created draft %s", item.key, dep["id"])
    records.update(item.key, deposit_id=dep["id"], status="draft",
                   bucket=(dep.get("links") or {}).get("bucket"),
                   draft_url=(dep.get("links") or {}).get("html"))

    dep = client.set_metadata(dep["id"], item.metadata)
    log.info("%s: metadata set", item.key)
    kept = ((dep.get("metadata") or {}).get("custom") or {}).get("code:codeRepository")
    if kept != REPO_URL:
        log.warning("%s: Zenodo did not keep the repository URL (draft has %r); set it in the web form",
                    item.key, kept)
    dep = sync_files(client, dep, item)
    reserved = ((dep.get("metadata") or {}).get("prereserve_doi") or {}).get("doi")
    if reserved:
        log.info("%s: reserved DOI %s", item.key, reserved)
    else:
        log.warning("%s: Zenodo did not return a reserved DOI for draft %s", item.key, dep["id"])
    records.update(item.key, deposit_id=dep["id"], status="draft",
                   bucket=(dep.get("links") or {}).get("bucket"),
                   draft_url=(dep.get("links") or {}).get("html"),
                   reserved_doi=reserved)
    log.info("%s: draft complete, all files verified", item.key)
    return True


def _record_published(client: ZenodoClient, records: Records, item: Item, dep: dict) -> None:
    rec_id = dep.get("record_id") or dep.get("id")
    doi = dep.get("doi") or (dep.get("metadata") or {}).get("doi")
    reserved = (records.get(item.key) or {}).get("reserved_doi")
    if reserved and doi and doi.lower() != reserved.lower():
        log.warning("%s: published with DOI %s, not the reserved DOI %s", item.key, doi, reserved)
    url = (dep.get("links") or {}).get("record_html") or f"{client.host}/records/{rec_id}"
    records.update(item.key, deposit_id=dep.get("id"), record_id=rec_id, status="published",
                   record_url=url, doi=doi)


def publish_one(client: ZenodoClient, records: Records, item: Item, community: str) -> None:
    entry = records.get(item.key)
    dep_id = entry["deposit_id"]
    # Re-check the draft immediately before the irreversible step
    dep = client.get(dep_id)
    if dep.get("submitted"):
        _record_published(client, records, item, dep)
        return
    remote = _remote_files(dep)
    if {k: v["md5"] for k, v in remote.items()} != {lf.name: lf.md5 for lf in item.files}:
        raise ZenodoError(f"{item.key}: files of draft {dep_id} changed since upload; not publishing")
    title = dep.get("title") or (dep.get("metadata") or {}).get("title")
    if title != item.title:
        raise ZenodoError(f"{item.key}: draft {dep_id} is titled '{title}'; not publishing")
    dep = client.publish(dep_id)
    _record_published(client, records, item, dep)
    entry = records.get(item.key)
    log.info("%s: published %s (DOI %s)", item.key, entry["record_url"], entry.get("doi"))

    if community:
        rec = client.get_record(entry["record_id"])
        comms = [c.get("id") or c.get("identifier") for c in ((rec or {}).get("metadata") or {}).get("communities", [])]
        if community in comms:
            log.info("%s: record is in community '%s'", item.key, community)
            records.update(item.key, community=community, community_status="included")
        else:
            log.warning("%s: record does not list community '%s' yet; the request may await a curator",
                        item.key, community)
            records.update(item.key, community=community, community_status="pending or unknown")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_item(item: Item, show_json: bool) -> None:
    md = item.metadata
    p = print
    p(f"== {item.title}")
    p(f"   folder:      {item.folder}")
    c = md["creators"][0]
    p(f"   title:       {md['title']}")
    p(f"   version:     {md['version']}")
    p(f"   date:        {md['publication_date']} (publication date: build date of the file)")
    p(f"   DOI request: {'reserve on upload' if md.get('prereserve_doi') else 'none'}")
    p(f"   repository:  {(md.get('custom') or {}).get('code:codeRepository', '(none)')}")
    p(f"   creator:     {c['name']}; ORCID {c.get('orcid', '(none)')}; "
      f"affiliation {c.get('affiliation', '(none)')}")
    p(f"   type:        {md['upload_type']}; access {md['access_right']}; licence {md['license']}")
    p(f"   keywords:    {', '.join(md['keywords'])}")
    p(f"   communities: {', '.join(x['identifier'] for x in md.get('communities', [])) or '(none)'}")
    p("   description:")
    for line in html_to_text(md["description"]):
        p(f"     | {line}")
    p(f"   files ({len(item.files)}, {human_size(item.total_size)}):")
    w = max(len(lf.name) for lf in item.files)
    for lf in item.files:
        p(f"     {lf.name:<{w}}  {lf.size:>11d} B  md5 {lf.md5}")
    for name, why in item.excluded:
        p(f"   NOT uploaded: {name}: {why}")
    checks = ["block 0 = log (bands, absorbers, continua)", "BLAKE2b = .chk/.chk_k", "no NaN in .sf/.sf_k",
              f"no netCDF fill value or value > {K_LIMIT:.0e} in .sf_k"]
    checks.append("files = zip members (size, CRC32)" if item.zip_checked else "no zip to compare")
    p(f"   checks:      {'; '.join(checks)}")
    if show_json:
        p("   metadata JSON:")
        for line in json.dumps({"metadata": md}, indent=2).splitlines():
            p(f"     {line}")
    p("")


def print_table(items: list, records: Records) -> None:
    print("| Codename | Bands | Download | DOI |")
    print("|----------|-------|----------|-----|")
    for item in items:
        entry = records.get(item.key)
        if entry and entry.get("status") == "published":
            url = f"[{item.codename} {item.nband} on Zenodo]({entry.get('record_url', '')})"
            doi = entry.get("doi") or ""
        elif entry:
            url = f"(draft) {entry.get('draft_url') or entry.get('deposit_id')}"
            doi = f"{entry['reserved_doi']} (reserved)" if entry.get("reserved_doi") else ""
        else:
            url, doi = "(not uploaded)", ""
        print(f"| {item.codename} | {item.nband} | {url} | {doi} |")

    # Bands cells for the table in docs/Reference/proteus_spectral_file_reference.md, one row per codename,
    # with each published band count linked to its record
    print("")
    print("| Codename | Bands |")
    print("|----------|-------|")
    for codename in dict.fromkeys(item.codename for item in items):
        cells = []
        for item in sorted((i for i in items if i.codename == codename), key=lambda i: -i.nband):
            entry = records.get(item.key)
            if entry and entry.get("status") == "published":
                cells.append(f"[{item.nband}]({entry.get('record_url', '')} \"{codename} {item.nband} on Zenodo\")")
            else:
                cells.append(f"{item.nband}")
        print(f"| {codename} | {', '.join(cells)} |")


def confirm(question: str, answer: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        log.error("Confirmation needed but stdin is not a terminal; pass --yes to proceed")
        return False
    return input(f"{question} Type '{answer}' to continue: ").strip() == answer


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="Tupload_zenodo.py",
        description="Upload PROTEUS spectral files (one Zenodo record per codename and band count) "
                    "to Zenodo and the PROTEUS community. Without --upload this is a dry run that "
                    "makes no network request.",
        epilog=__doc__.split("Steps\n-----\n", 1)[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("root", type=Path,
                   help="folder holding <Codename>/<nband>/ sub-folders, e.g. .../nogit_new_spectralfiles")
    p.add_argument("--family", nargs="+", metavar="CODENAME",
                   help="only these families (default: every family found below ROOT)")
    p.add_argument("--nband", nargs="+", type=int, metavar="N",
                   help="only these band counts (default: every band count found)")
    tgt = p.add_mutually_exclusive_group()
    tgt.add_argument("--sandbox", dest="target", action="store_const", const="sandbox",
                     help="target %s with $%s (the default)" % (HOSTS["sandbox"], TOKEN_VARS["sandbox"]))
    tgt.add_argument("--production", dest="target", action="store_const", const="production",
                     help="target %s with $%s" % (HOSTS["production"], TOKEN_VARS["production"]))
    p.set_defaults(target="sandbox")
    p.add_argument("--upload", action="store_true",
                   help="create or resume drafts and upload the files (default: dry run)")
    p.add_argument("--publish", action="store_true",
                   help="publish the drafts after their files are verified; needs --upload. "
                        "A published record cannot be deleted")
    p.add_argument("--yes", action="store_true",
                   help="do not ask for confirmation before production actions")
    p.add_argument("--community", default=None,
                   help=f"community identifier (default: {COMMUNITY} on production, none on the sandbox, "
                        "where it does not exist); '' for none")
    p.add_argument("--creator", default=None,
                   help="creator as 'Family, Given' (required with --upload)")
    p.add_argument("--orcid", default="",
                   help="creator ORCID (default: none)")
    p.add_argument("--affiliation", default="",
                   help="creator affiliation (default: none)")
    p.add_argument("--timeout", type=float, default=900.0,
                   help="read timeout of each request in seconds (default: %(default)s)")
    p.add_argument("--show-json", action="store_true",
                   help="also print the metadata JSON that would be sent")
    args = p.parse_args(argv)
    if args.publish and not args.upload:
        p.error("--publish needs --upload (drafts are created or resumed and verified first)")
    if args.upload and not args.creator:
        p.error("--upload needs --creator")
    return args


def main(argv=None) -> int:
    args = parse_args(argv)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setFormatter(_LOG_FORMAT)
    root_logger.addHandler(console)

    host = HOSTS[args.target]
    community = args.community if args.community is not None else (
        COMMUNITY if args.target == "production" else "")
    creator = {"name": args.creator or "(not set; use --creator)"}
    if args.affiliation:
        creator["affiliation"] = args.affiliation
    if args.orcid:
        creator["orcid"] = args.orcid
    root = args.root.absolute()

    # 1. Discover and check (offline)
    try:
        formulae, names = read_gas_list(gas_list_path())
        found = discover(root, args.family, args.nband)
    except CheckError as exc:
        log.error("%s", exc)
        return 1
    log.info("Checking %d records below %s", len(found), root)
    items, errors = [], []
    for codename, nband, folder in found:
        try:
            item = build_item(codename, nband, folder, formulae, names)
            item.metadata = build_metadata(item, creator, community)
            items.append(item)
        except (CheckError, OSError, zipfile.BadZipFile) as exc:
            msg = str(exc)
            errors.append(msg if msg.startswith(f"{codename}/{nband}:") else f"{codename}/{nband}: {msg}")
    for e in errors:
        log.error("%s", e)
    if errors and (args.upload or not items):
        log.error("%d of %d records failed the checks; nothing done. Fix them, or leave them out "
                  "with --family/--nband", len(errors), len(found))
        return 1

    print("")
    for item in items:
        print_item(item, args.show_json)
    nfiles = sum(len(i.files) for i in items)
    total = sum(i.total_size for i in items)
    largest = max((lf for i in items for lf in i.files), key=lambda lf: lf.size)
    print(f"Target:  {host} ({args.target}); community: {community or '(none)'}")
    print(f"Records: {len(items)} passed the checks, {len(errors)} failed; files: {nfiles}; "
          f"total {human_size(total)} ({total} B); "
          f"largest file {human_size(largest.size)} ({largest.path.parent.parent.name}/"
          f"{largest.path.parent.name}/{largest.name})")
    if not args.creator:
        print("Note:    no creator set (use --creator; required with --upload)")
    if not args.affiliation:
        print("Note:    no creator affiliation set (use --affiliation to add one)")

    # 2. Dry run
    if not args.upload:
        print("\nDry run: no network request made and no file written. "
              "Use --upload to create drafts (sandbox unless --production).")
        if errors:
            print(f"\nFAILED the checks ({len(errors)} records; --upload refuses to run while "
                  "any selected record fails):")
            for e in errors:
                print(f"  - {e}")
            return 1
        return 0

    # 3. Network actions
    token = os.environ.get(TOKEN_VARS[args.target], "").strip()
    if not token:
        log.error("Set the environment variable %s to a Zenodo access token for %s "
                  "(scopes deposit:write and deposit:actions)", TOKEN_VARS[args.target], host)
        return 1
    if args.target == "production" and not confirm(
            f"\nThis will create or update {len(items)} draft records on {host} and upload "
            f"{human_size(total)}{' (publishing is asked separately)' if args.publish else ''}.",
            "yes", args.yes):
        log.info("Aborted; nothing done")
        return 1

    logfile = root / f"Tupload_zenodo_{args.target}_{dt.datetime.now():%Y%m%dT%H%M%S}.log"
    fh = logging.FileHandler(logfile, mode="w")
    fh.setFormatter(_LOG_FORMAT)
    root_logger.addHandler(fh)
    log.info("Logging to %s", logfile)

    client = ZenodoClient(host, token, args.timeout)
    del token
    status = 0
    ready = []
    records = Records()
    try:
        # Zenodo is the only record of earlier runs: drafts and published records are found by title
        existing = {}
        log.info("Listing your depositions to find drafts and records made earlier")
        for d in client.list_depositions():
            t = d.get("title") or (d.get("metadata") or {}).get("title")
            existing.setdefault(t, []).append(d)
        for item in items:
            if prepare_draft(client, records, item, existing):
                ready.append(item)

        if args.publish and ready:
            if args.target == "production" and not confirm(
                    f"\nPublish {len(ready)} records on {host}? Published records get a DOI and "
                    "cannot be deleted.", "publish", args.yes):
                log.info("Not publishing; the drafts stay as they are")
            else:
                for item in ready:
                    publish_one(client, records, item, community)
        elif ready:
            log.info("%d drafts ready; not published (use --publish)", len(ready))
    except ZenodoError as exc:
        log.error("%s", exc)
        log.error("Stopped. Run the same command again to resume: drafts are found again by title")
        status = 1
    except KeyboardInterrupt:
        log.error("Interrupted. Run the same command again to resume: drafts are found again by title")
        status = 1

    print("")
    print_table(items, records)
    return status


if __name__ == "__main__":
    sys.exit(main())
