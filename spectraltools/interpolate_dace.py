#!/usr/bin/env python3 
# Interpolate nu,k values for a series of p,t points

import src.utils as utils
import src.dace as dace

def main():
    isotopologue = '1H2-16O'
    linelist = 'POKAZATEL'
    linelist_version = 2.0
    pressure = 1.0
    temperature = 300.0
    dace.download(isotopologue, linelist, linelist_version, pressure, temperature)

if __name__ == "__main__":
    main()
    exit(0)