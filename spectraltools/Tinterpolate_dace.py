#!/usr/bin/env python3
# Interpolate nu,k values for a series of p,t points from the DACE database

import src.utils as utils
import src.dace as dace
import numpy as np

def main():
    # --- PARAMETERS ---

    # Intended target pressures [bar]
    p_arr = np.logspace(-6, 3, 5)

    # Intended target temperatures [K]
    t_arr = np.linspace(60.0, 2900.0, 5) - 5.0
    t_arr = np.append(t_arr, [75.0, 100.0])

    # Uncomment one of the blocks below or write your own
    #isotopologue = '1H2-16O'
    #linelist = 'POKAZATEL'
    #linelist_version = 2.0
    #t_lims = (50.0, 2900.0)
    #outdir = utils.dirs["dace"] + "/H2O/"

    #isotopologue = '1H2'
    #linelist = 'RACPPK'
    #linelist_version = 1.0
    #t_lims = (50.0, 4500.0)
    #outdir = utils.dirs["dace"] + "/H2/"

    #isotopologue = '12C-16O'
    #linelist = 'HITEMP2019'
    #linelist_version = 1.0
    #t_lims = (50.0, 8900.0)
    #outdir = utils.dirs["dace"] + "/CO/"

    #isotopologue = '12C-16O2'
    #linelist = 'UCL-4000'
    #linelist_version = 1.0
    #t_lims = (50.0, 4500.0)
    #outdir = utils.dirs["dace"] + "/CO2/"

    #isotopologue = '12C-1H4'
    #linelist = 'YT34to10'
    #linelist_version = 1.0
    #t_lims = (50.0, 2900.0)
    #outdir = utils.dirs["dace"] + "/CH4/"

    isotopologue = '14N2'
    linelist = 'WCCRMT'
    linelist_version = 1.0
    t_lims = (600.0, 4500.0)
    outdir = utils.dirs["dace"] + "/N2/"

    # isotopologue = '16O2'
    # linelist = 'HITRAN2020'
    # linelist_version = 1.0
    # t_lims = (50.0, 4500.0)
    # outdir = utils.dirs["dace"] + "/O2/"

    # isotopologue = '16O3'
    # linelist = 'HITRAN2020'
    # linelist_version = 1.0
    # t_lims = (50.0, 3500.0)
    # outdir = utils.dirs["dace"] + "/O3/"

    # isotopologue = '14N2-16O'
    # linelist = 'HITEMP2019'
    # linelist_version = 1.0
    # t_lims = (50.0, 4500.0)
    # outdir = utils.dirs["dace"] + "/N2O/"

    # isotopologue = '14N-1H3'
    # linelist = 'CoYuTe'
    # linelist_version = 2.0
    # t_lims = (50.0, 1900.0)
    # outdir = utils.dirs["dace"] + "/NH3/"

    # isotopologue = '16O-1H'
    # linelist = 'HITEMP2020'
    # linelist_version = 1.0
    # t_lims = (50.0, 8900.0)
    # outdir = utils.dirs["dace"] + "/OH/"

    # isotopologue = '1H2-32S'
    # linelist = 'AYT2'
    # linelist_version = 2.0
    # t_lims = (50.0, 2900.0)
    # outdir = utils.dirs["dace"] + "/H2S/"

    # isotopologue = '1H-12C-14N'
    # linelist = 'Harris'
    # linelist_version = 2.0
    # t_lims = (50.0, 2900.0)
    # outdir = utils.dirs["dace"] + "/HCN/"

    # isotopologue = '32S-16O2'
    # linelist = 'ExoAmes'
    # linelist_version = 2.0
    # t_lims = (50.0, 1900.0)
    # outdir = utils.dirs["dace"] + "/SO2/"

    # -------------------
    # Na, NaO, Fe, FeO, FeH, K, SiO, SiO2, PH3, provided already by SOCRATES

    # isotopologue = ''
    # linelist = ''
    # linelist_version = .0
    # t_lims = (50.0, 8900.0)
    # outdir = utils.dirs["dace"] + "//"


    # --- EXECUTION ---

    # Print
    print("Target pressures [K]:      " + str(p_arr))
    print("Target temperatures [bar]: " + str(t_arr))
    print(" ")

    # Check requests against database temperature limits
    t_req = []; t_drp = []
    for t in t_arr:
        if t_lims[0] <= t <= t_lims[1]:
            t_req.append(t)  # requested temperatures
        else:
            t_drp.append(t)  # dropped temperatures
    print('run')
    # Download files
    dace.download(isotopologue, linelist, linelist_version, p_arr, t_req, outdir)

    # Extend grid to temperatures outside of database range (if required)
    dace.extend(outdir, t_drp)

    # -----------------
    return

if __name__ == "__main__":
    print("Hello")
    main()
    print("Goodbye")
    exit(0)
