# General utilities

import os
import logging
import shutil
from datetime import datetime
import numpy as np
import hashlib

# Version
__version__ = "1.0.0"

log = logging.getLogger("fwl."+__name__)

# Check that SOCRATES is setup
if "RAD_DIR" not in os.environ.keys() or (os.environ["RAD_DIR"] is None):
    raise Exception("Cannot find SOCRATES! Refer to README.md")

# Named directories
dirs = {"socrates":os.path.abspath(os.environ["RAD_DIR"])}
dirs["tools"]  = os.path.join(dirs["socrates"], "spectraltools/")
dirs["output"] = os.path.join(dirs["tools"] , "output/" )
dirs["data"]   = os.path.join(dirs["tools"]   , "data/" )
dirs["dace"]   = os.path.join(dirs["data"]    , "dace/" )
dirs["hitran"] = os.path.join(dirs["data"]  , "hitran/" )
dirs["exomol"] = os.path.join(dirs["data"]  , "exomol/" )
dirs["exocross"]  = os.path.join(dirs["data"]  , "exocross/" )
dirs["cia"]    = os.path.join(dirs["data"]     , "cia/" )
dirs["moleculesUV"]    = os.path.join(dirs["tools"]     , "moleculesUV/" )

if not os.path.exists(dirs["output"]):
    raise Exception("Output folder '%s' not found"%dirs["output"])

# Convert wavenumber [cm-1] to wavelength [nm]
def wn2wl(x) -> float:

    x = np.array(x, float)
    near_zero = np.isclose(x, 0)
    x[near_zero] = np.inf
    x[~near_zero] = 10000000.0 / x[~near_zero]
    return x

# Convert wavelength [nm] to wavenumber [cm-1]
wl2wn = wn2wl  # Inverse function is the same, just swap input/output

# Check iterable is strictly ascending
def is_ascending(arr):
    l = len(arr)
    if l < 2:
        return True
    for i in range(1,l):
        if not arr[i] > arr[i-1]:
            return False
    return True

# Check if array is unique (no repeated values)
def is_unique(arr):
   flat = np.array(arr).flatten()
   return bool( len(np.unique(flat)) == len(flat) )

# Round float to n significant figures
def round_float_sigfigs(x, n):
    return np.round(x, -int(np.floor(np.sign(x) * np.log10(abs(x)))) + n)

# Convert all of the values in an array into one long string
def get_arr_as_str(arr, fmt=r"%g",sep=' '):
    if type(arr[0]) is float or type(arr[0]) is np.float64:
        return sep.join([fmt%v for v in arr])
    elif type(arr[0]) is int:
        return sep.join([fmt%v for v in arr])
    else:
        return sep.join([str(v) for v in arr])

# Get item in 'arr' that is numerically closest to 'value'
def get_closest(value, arr):
    return arr[np.argmin(np.abs(np.array(arr)-value))]

# Get index of item in 'arr' that is numerically closest to 'value'
def get_closest_idx(value, arr):
    return np.argmin(np.abs(np.array(arr)-value))

# Find the closest point in a p,t grid, returning its index, distance, p, t.
def find_pt_close(arr_p, arr_t, target_p, target_t):
    target_p = max(1.0e-9, target_p)
    target_t = max(1.0e-9, target_t)
    nvals = len(arr_p)
    dists = []

    for i in range(nvals):
        dists.append(100.0 * ( ( (arr_p[i]-target_p)/target_p)**2.0 + (  (arr_t[i]-target_t)/target_t  )**2.0   )**0.5)
    iclose = np.argmin(dists)
    dclose = dists[iclose]

    best_p = arr_p[iclose]
    best_t = arr_t[iclose]

    return iclose, dclose, best_p, best_t

# Check if output folder exists
def check_output_exists():
    return os.path.exists( dirs["output"]  )

# Sanitise source string
def sourcesafe(source:str):
    safe = source.strip().lower()
    if safe not in ["dace", "hitran", "exomol", "direct", "exocross"]:
        raise Exception("Invalid source '%s'"% source)
    return safe

# Safely remove a file
def rmsafe(file:str):
    if file in ["","."]:
        log.warning("an attempt was made to remove the current working directory!")
        return
    if os.path.exists(file):
        os.remove(file)


_LOG_FORMATTER = logging.Formatter(
    fmt="[%(asctime)s %(levelname)7s] %(message)s",
    datefmt="%H:%M:%S",
)



def setup_logger(name:str, date=True, level=logging.INFO) -> str:
    """Configure logging for a spectraltools entry-point script.

    Adds a console handler (plain, print-like formatting) and a file
    handler to the root logger, so that log records from every 'src.*'
    module (each using logging.getLogger(__name__)) are captured. The file
    handler writes a timestamped log to '<name>.log' in the current working
    directory.

    Parameters
    ----------
    name : str
        Name of the running script; used only to name the log file.
    date: bool
        If True, include timestamps in the log name.
    level : int
        Logging level for both handlers.

    Returns
    -------
    str
        Path to the log file created in the current working directory.
    """

    root = logging.getLogger()
    root.setLevel(level)

    # Drop any handlers from a previous call in this process
    for h in list(root.handlers):
        root.removeHandler(h)

    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(_LOG_FORMATTER)
    root.addHandler(console)

    if date:
        name = "%s_%s" % (name, datetime.now().strftime("%Y%m%dT%H%M%S"))
    logfile = os.path.join(os.getcwd(), "%s.log" % name)
    filehandler = logging.FileHandler(logfile, mode="w")
    filehandler.setLevel(level)
    filehandler.setFormatter(_LOG_FORMATTER)
    root.addHandler(filehandler)

    return logfile


def copy_log_to_output(logfile:str, alias:str=None) -> str:
    """Copy a log file (as created by setup_logger) into the output/ folder.

    Parameters
    ----------
    logfile : str
        Path to the log file, as returned by setup_log.
    alias : str
        If given, prefixed onto the destination filename (so the copy is
        matched, and cleaned up on a subsequent run, by the same
        '<alias>*' glob used elsewhere in the output folder).

    Returns
    -------
    str
        Path to the copied log file inside output/
    """

    for h in logging.getLogger().handlers:
        h.flush()

    name = os.path.basename(logfile)
    if alias:
        name = "%s_%s" % (alias, name)
    dest = os.path.join(dirs["output"], name)
    shutil.copy2(logfile, dest)
    return dest

# Calculate the checksum of a file using the BLAKE2b algorithm
def checksum(filename:str):
    # Adapted from https://stackoverflow.com/a/1131238
    with open(filename, "rb") as f:
        file_hash = hashlib.blake2b()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

# Check that the environment is configured
def checkenv():
    from shutil import which
    if which("prep_spec") is not None:
        return True
    else:
        raise EnvironmentError("Cannot find SOCRATES executables. Have you sourced set_rad_env?")
    
# Get socrates version from file
def socratesver():
    ver_file = os.path.join(dirs["socrates"], "version")
    if not os.path.exists(ver_file):
        raise Exception("Cannot find SOCRATES version file '%s'"%ver_file)
    with open(ver_file, "r") as f:
        ver = f.read().strip()
    return ver

gas_list = []
gas_list_pcf = os.path.join(dirs["socrates"], "src", "radiance_core", "gas_list_pcf.F90")
with open(gas_list_pcf, "r") as f:
    gas_list_raw = f.readlines()
read_start = False
for line in gas_list_raw:
    # beginning of list of gases
    if "PARAMETER :: header_gas(npd_gases)" in line:
        if read_start:
            raise Exception("Unexpected start of gas list in '%s'"%gas_list_pcf)
        read_start = True
        continue

    # end of list of gases
    if read_start and line.endswith("/)\n"):
        read_start = False
        break

    # middle of list of gases
    if read_start:
        line_splt = line.strip().replace(" ","").replace("'","").replace("&","").split(',')
        gas_list.extend([s for s in line_splt if len(s) > 0])

absorber_id = {}
for i,g in enumerate(gas_list):
    absorber_id[g] = "%d"%(i+1)

# List of valid continuum combinations in SOCRATES/HITRAN
cia_pairs = [
    ["H2", "CH4"],
    ["H2", "H2"],
    ["H2", "H"],
    ["H2", "He"],
    ["He", "H"],
    ["N2", "H2"],
    ["N2", "He"],
    ["N2", "N2"],
    ["N2", "H2O"],
    ["O2", "CO2"],
    # ["O2", "N2"], # shows strange behaviour
    ["O2", "O2"],
    ["CO2", "CO2"],
    ["CO2", "H2"],
    ["CO2", "He"],
    ["CO2", "CH4"],
    ["CO2", "Ar"],
    ["CH4", "He"],
    ["CH4", "Ar" ],
    ["CH4", "CH4"],
]
