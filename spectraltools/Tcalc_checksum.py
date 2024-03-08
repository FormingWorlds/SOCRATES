#!/usr/bin/env python3 
# Calculate the checksum of a file, for verifying spectral file or data integrity

import sys, os
import src.utils as utils

def main(fpath:str):
    c = utils.checksum(fpath)
    print(c)

if __name__ == "__main__":
    f = sys.argv[1]
    f = os.path.abspath(f)
    main(f)
    exit(0)