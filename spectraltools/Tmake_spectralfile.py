#!/usr/bin/env python3 
# Python wizard for interactive file conversion

# Import local files 
import src.utils as utils
import src.spectral as spectral
import src.dace as dace
import src.cross as cross
import src.netcdf as netcdf
import os, glob
import numpy as np

def main():

    # ------------ PARAMETERS ------------
    formula = "H2O"
    source = "dace"
    vols = [formula]
    alias = "demo"
    nband = 400
    method = 4     # band selection method
    numax = 3e4+2   # clip to this maximum wavenumber [cm-1]
    numin = 1.0    # clip to this minimum wavenumber [cm-1]
    dnu   = 0.0    # downsample to this wavenumber resolution [cm-1]

    # tgt_p = np.logspace(-7, 3, 26)
    # tgt_t = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0, 2250.0, 2500.0, 2750.0, 3000.0]

    tgt_p = tgt_t = []

    # ------------------------------------




   
    # ------------ EXECUTION -------------
    # Check paths
    formula_path = os.path.join(utils.dirs[source], formula.strip()+"/")
    if not os.path.exists(formula_path):
        raise Exception("Could not find folder '%s'" % formula_path)
    for f in glob.glob(utils.dirs["output"]+"/%s*"%alias):
        os.remove(f)

    # Determine p,t grid 
    arr_p, arr_t, arr_f = dace.get_pt(formula_path, tgt_p , tgt_t)

    # Get nu grid
    temp_xc = cross.xsec(formula, source, dace.list_files(formula_path)[0])
    temp_xc.read(numin=numin, numax=numax, dnu=dnu)

    # Determine bands 
    band_edges = spectral.best_bands(temp_xc.get_nu(), method, nband)

    # Write skeleton file
    spectral.create_skeleton(alias, arr_p, arr_t, vols, band_edges)

    # Write netCDF containing absorption spectra
    nc_paths = {}
    dnu_last = -1
    for v in vols:
        # For this volatile...
        ncp = os.path.join(utils.dirs["output"] , alias+"_"+formula+".nc")
        dnu = netcdf.write_ncdf_from_grid(ncp, formula, source, arr_p, arr_t, arr_f, dnu=dnu, numin=numin, numax=numax)
        nc_paths[v] = ncp

        # Check resolution
        if (dnu_last > 0) and not np.isclose(dnu_last, dnu):
            raise Exception("Wavenumber resolutions differ between volatiles (%g != %g)" % (dnu_last, dnu))
        dnu_last = dnu

    # Calculate k-coefficients from netCDF 
    for i,f1 in enumerate(vols):
        # Get path of lbl netCDF file
        ncp = nc_paths[f1]
        spectral.calc_kcoeff_lbl(alias, f1, ncp, nband)
        for f2 in vols[i:]: 
            spectral.calc_kcoeff_cia(alias, f1, f2, band_edges, dnu)

    # Assemble final spectral file
    spectral.assemble(alias, vols)
    # ------------------------------------
    return 
    

if __name__ == "__main__":
    print("Hello\n")
    main()
    print("Goodbye")
    exit(0)
