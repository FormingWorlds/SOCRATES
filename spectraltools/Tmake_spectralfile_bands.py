#!/usr/bin/env python3
# Make spectral files with the same absorbers but different numbers of bands,
# packaging each one into its own zip archive. Absorbers, alias and all other
# settings are taken from the parameters in Tmake_spectralfile.py

# Import local files
import src.utils as utils
import Tmake_spectralfile
import Tpackage_spectralfile
import logging
import os
import time
import argparse

log = logging.getLogger("fwl."+__name__)

# Main function
def main(nbands:list, target:str, overwrite:bool):
    target = os.path.abspath(target)

    # Runs share the same alias, so each one clears the output of the previous
    # run. Pre-existing netCDFs are kept if preNC=True, since they do not
    # depend on the number of bands.
    zpaths = []
    for nband in nbands:

        # Make spectral file, with its own log
        logfile = utils.setup_logger("Tmake_spectralfile")
        log.info("Spectral Tools Wizard (version %s)", utils.__version__)
        log.info("Making spectral file with nband=%d", nband)
        start = time.perf_counter()
        alias = Tmake_spectralfile.main(nband=nband)
        elapsed = time.perf_counter()-start
        log.info("Time elapsed: %d hours %.2f minutes.", elapsed//3600, (elapsed%3600)//60)

        # Copy this run's log into output folder, so that it is packaged
        out_logfile = utils.move_log_to_output(logfile, alias=alias)
        log.info("Copied log file to '%s'", out_logfile)

        # Package into <target>/<alias>/<nband>/<alias>.zip
        utils.setup_logger("Tpackage_spectralfile")
        ztarget = os.path.join(target, alias, "%d"%nband)
        Tpackage_spectralfile.main(alias, ztarget, overwrite)
        zpaths.append(os.path.join(ztarget, alias+".zip"))

    log.info("")
    log.info("Wrote %d zip files", len(zpaths))
    for z in zpaths:
        log.info("    %s", z)


# Run main function
if __name__ == "__main__":
    utils.checkenv()

    parser = argparse.ArgumentParser(description='Make and zip spectral files with different numbers of bands')
    parser.add_argument('target', type=str, nargs='?', default='.',
                        help='Folder in which to write <alias>/<nband>/<alias>.zip (default: current directory)')
    parser.add_argument('--nband', type=int, nargs='+', default=[16, 32, 64, 128, 256, 2048],
                        help='Numbers of bands to make')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing zip files')
    args = parser.parse_args()

    main(args.nband, args.target, args.overwrite)


# End of file
