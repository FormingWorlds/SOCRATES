#!/usr/bin/env python3
# Remove all files in output folder

# Import local files
import src.utils as utils
import logging
import os
import glob
import argparse
import time

log = logging.getLogger("fwl."+__name__)

# Main function
def main(alias:str, rm_netcdf:bool, dryrun:bool):
    # Inform
    log.info("Removing files for '%s'", alias)
    if rm_netcdf:
        log.info("(Will remove NetCDF files)")

    # In case user changes mind
    time.sleep(5.0)

    # Get files
    all_files = glob.glob(utils.dirs["output"]+"/"+alias+"*")
    net_files = glob.glob(utils.dirs["output"]+"/"+alias+"_*.nc")

    # Filter net_files (files to keep) 
    sav_files = []
    for f in net_files:
        skip_this=False 
        for c in ["-","cia","map","lbl"]:
            if c in f.split("/")[-1]:
                skip_this=True  
        if not skip_this:
            sav_files.append(f)

    # Get abspath 
    all_abs = [os.path.abspath(f) for f in all_files]
    net_abs = [os.path.abspath(f) for f in sav_files]

    # Delete files 
    for f in all_abs:
        if (f not in net_abs) or rm_netcdf:
            if dryrun:
                log.info("    dry run not removing '%s'", f)
            else:
                os.remove(f)

    log.info("Done")


# Run main function
if __name__ == "__main__":
    utils.setup_logger("Tclean_output")

    parser = argparse.ArgumentParser(description='Remove files in output folder')
    parser.add_argument('alias',    type=str, help='Alias used for spectral file generation')
    parser.add_argument('--netcdf', action='store_true', help='Also remove NetCDF files')
    parser.add_argument('--dry',    action='store_true', help='Dry run (do not remove files)')
    args = parser.parse_args()

    main(args.alias, args.netcdf, args.dry)


# End of file
