#!/usr/bin/env python3 
# Interpolate nu,k values for a series of p,t points

import src.utils as utils
import src.dace as dace
import numpy as np

def main():
    isotopologue = '1H2-16O'
    linelist = 'POKAZATEL'
    linelist_version = 2.0

    p_arr = [0.0010, 0.0022, 0.0047, 0.0100, 0.0219, 0.0468, 0.1000, 0.2188, 0.4677, 1.0000, 2.1878, 4.6774, 10.0000, 21.8776, 46.7735, 100.0000, 218.7762, 467.7351, 1000.0000, 2187.7616, 4677.3514, 10000.0000, 21877.6162, 46773.5141, 100000.0000, 213796.2090, 457088.1896, 1000000.0000, 2137962.0895, 4570881.8961, 10000000.0000, 21379620.8950, 45708818.9615, 100000000.0000]
    t_arr = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0, 2250.0, 2500.0]

    p_arr = np.array(p_arr) * 3.0
    t_arr = np.array(t_arr)

    outdir = utils.dirs["data"] + "/itp/"

    dace.download(isotopologue, linelist, linelist_version, p_arr, t_arr, outdir)
            


if __name__ == "__main__":
    main()
    exit(0)