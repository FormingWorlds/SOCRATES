#!/usr/bin/env python3
# Package a completed spectral file and its associated files into a zip archive

# Import local files
import src.utils as utils
import logging
import os
import glob
import zipfile
import argparse

log = logging.getLogger("fwl."+__name__)

# Main function
def main(alias:str, target:str, overwrite:bool):
    out = os.path.abspath(utils.dirs["output"])

    # Required files: the spectral file and its k-table
    required = [os.path.join(out, alias+".sf"),
                os.path.join(out, alias+".sf_k")]
    for f in required:
        if not os.path.isfile(f):
            raise FileNotFoundError("Required file '%s' not found. Has the run for '%s' completed?" % (f, alias))

    # Optional files: logs, checksums and plots for this alias
    extra = sorted(
                glob.glob(os.path.join(out, alias+"*.log")) +
                glob.glob(os.path.join(out, alias+"*.chk*")) +
                glob.glob(os.path.join(out, alias+"*.pdf"))
                         )

    # Backup of the generating script, which holds the run settings. Stored in
    # the zip as '<alias>_Tmake_spectralfile.py'. This is the script as it is
    # now, which may differ from what was used if it was edited after the run.
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tmake_spectralfile.py")
    if os.path.isfile(script):
        if os.path.getmtime(script) > os.path.getmtime(required[0]):
            log.warning("Tmake_spectralfile.py is newer than '%s'; its settings may not match this spectral file", required[0])
    else:
        log.warning("Cannot find '%s'; not backing up settings", script)
        script = None

    files = required + extra
    log.info("Packaging %d files for '%s'", len(files), alias)

    # Target folder
    target = os.path.abspath(target)
    os.makedirs(target, exist_ok=True)
    zpath = os.path.join(target, alias+".zip")
    if os.path.exists(zpath) and not overwrite:
        raise FileExistsError("'%s' already exists (use --overwrite)" % zpath)

    # Write archive, with files placed loose in the root of the zip
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            log.info("    adding '%s'", os.path.basename(f))
            zf.write(f, arcname=os.path.basename(f))
        if script is not None:
            log.info("    adding settings backup '%s_Tmake_spectralfile.py'", alias)
            zf.write(script, arcname=alias+"_Tmake_spectralfile.py")

    # Verify archive integrity and contents
    with zipfile.ZipFile(zpath, "r") as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError("Corrupt entry '%s' in '%s'" % (bad, zpath))
        names = set(zf.namelist())
    expected = {os.path.basename(f) for f in files}
    if script is not None:
        expected.add(alias+"_Tmake_spectralfile.py")
    missing = expected - names
    if missing:
        raise RuntimeError("Archive is missing entries: %s" % sorted(missing))

    log.info("Wrote '%s'", zpath)


# Run main function
if __name__ == "__main__":
    utils.setup_logger("Tpackage_spectralfile")

    parser = argparse.ArgumentParser(description='Zip a spectral file with its k-table, logs, plots and settings')
    parser.add_argument('alias',  type=str, help='Alias used for spectral file generation')
    parser.add_argument('target', type=str, nargs='?', default='.',
                        help='Folder in which to write <alias>.zip (default: current directory)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing zip file')
    args = parser.parse_args()

    main(args.alias, args.target, args.overwrite)


# End of file
