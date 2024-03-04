#!/usr/bin/env python3 
# Python wizard for interactive file conversion

# Import local files 
import src.utils as utils
import src.spectral as spectral
import src.dace as dace
import src.cross as cross
import src.netcdf as netcdf
import os
import numpy as np

def main():
    print("Wizard says hello")

    formula = "CO2"
    source = "dace"
    vols = [formula]
    alias = "demo"
    nband = 10

    formula_path = os.path.join(utils.dirs[source], formula.strip()+"/")
    if not os.path.exists(formula_path):
        raise Exception("Could not find folder '%s'" % formula_path)

    # Get P,T grid
    arr_p, arr_t, arr_f = dace.get_pt(formula_path, [0.1, 1.0, 10.0] , [100.0, 300.0, 500.0, 1000.0, 2000.0])

    # Get nu grid + write skeleton
    temp_xc = cross.xsec(formula, source, dace.list_files(formula_path)[0])
    temp_xc.read()
    band_edges = spectral.best_bands(temp_xc.get_nu(), 2, nband)
    spectral.create_skeleton(alias, arr_p, arr_t, vols, band_edges)

    # Write netCDF containing absorption spectra
    nc_path = os.path.join(utils.dirs["output"] , alias+"_"+formula+".nc")
    netcdf.write_ncdf_from_grid(nc_path, formula, source, arr_p, arr_t, arr_f)

    # Calculate k-coefficients from netCDF 
    spectral.calc_kcoeff_lbl(alias, formula, nc_path, nband)


    print("Goodbye")

if __name__ == "__main__":
    main()
    exit(0)
