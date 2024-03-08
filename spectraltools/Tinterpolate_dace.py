#!/usr/bin/env python3 
# Interpolate nu,k values for a series of p,t points

import src.utils as utils
import src.dace as dace
import numpy as np

def main():
    # --- PARAMETERS
    isotopologue = '1H2-16O'
    linelist = 'POKAZATEL'
    linelist_version = 2.0

    p_arr = np.logspace(-6, 3, 80)
    t_arr = np.linspace(60.0, 2900.0, 40) - 5.0

    outdir = utils.dirs["dace"] + "/H2O_INTERP/"

    # --- EXECUTION
    dace.download(isotopologue, linelist, linelist_version, p_arr, t_arr, outdir)
    return 

if __name__ == "__main__":
    print("Hello")
    main()
    print("Goodbye")
    exit(0)