#!/usr/bin/env python3 
# Interpolate nu,k values for a series of p,t points from the DACE database

import src.utils as utils
import src.dace as dace
import numpy as np

def main():
    # --- PARAMETERS ---
    isotopologue = '14N2'
    linelist = 'WCCRMT'
    linelist_version = 1.0

    p_arr = np.logspace(-6, 3, 80)
    t_arr = np.linspace(60.0, 2900.0, 40) - 5.0

    outdir = utils.dirs["dace"] + "/N2_INTERP/"
    # -------------------



    # --- EXECUTION ---
    dace.download(isotopologue, linelist, linelist_version, p_arr, t_arr, outdir)
    # -----------------
    return 

if __name__ == "__main__":
    print("Hello")
    main()
    print("Goodbye")
    exit(0)