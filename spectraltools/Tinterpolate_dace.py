#!/usr/bin/env python3 
# Interpolate nu,k values for a series of p,t points from the DACE database

import src.utils as utils
import src.dace as dace
import numpy as np

def main():
    # --- PARAMETERS ---
    p_arr = np.logspace(-6, 3, 80)
    t_arr = np.linspace(60.0, 2900.0, 40) - 5.0
    t_arr = np.append(t_arr, [75.0, 100.0])


    # Uncomment one of the blocks below or write your own

    isotopologue = '1H2-16O'
    linelist = 'POKAZATEL'
    linelist_version = 2.0
    outdir = utils.dirs["dace"] + "/H2O_INTERP/"

    # isotopologue = '1H2'
    # linelist = 'RACPPK'
    # linelist_version = 1.0
    # outdir = utils.dirs["dace"] + "/H2_INTERP/"

    # isotopologue = '12C-16O'
    # linelist = 'HITEMP2019'
    # linelist_version = 1.0
    # outdir = utils.dirs["dace"] + "/CO_INTERP/"

    # isotopologue = '12C-16O2'
    # linelist = 'UCL-4000'
    # linelist_version = 1.0
    # outdir = utils.dirs["dace"] + "/CO2_INTERP/"

    # isotopologue = '12C-1H4'
    # linelist = 'YT34to10'
    # linelist_version = 1.0
    # outdir = utils.dirs["dace"] + "/CH4_INTERP/"

    # isotopologue = '14N2'
    # linelist = 'WCCRMT'
    # linelist_version = 1.0
    # outdir = utils.dirs["dace"] + "/N2_INTERP/"

    # isotopologue = '16O2'
    # linelist = 'HITRAN2020'
    # linelist_version = 1.0
    # outdir = utils.dirs["dace"] + "/O2_INTERP/"

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