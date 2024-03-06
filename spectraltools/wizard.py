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
    print("Wizard says hello\n")

    formula = "H2O"
    source = "dace"
    vols = [formula]
    alias = "demo"
    nband = 360
    numax = 2e99   # clip to this maximum wavenumber [cm-1]
    numin = 1.0    # clip to this minimum wavenumber [cm-1]
    dnu   = 0.0    # downsample to this wavenumber resolution [cm-1]

    formula_path = os.path.join(utils.dirs[source], formula.strip()+"/")
    if not os.path.exists(formula_path):
        raise Exception("Could not find folder '%s'" % formula_path)
    
    for f in glob.glob(utils.dirs["output"]+"/%s*"%alias):
        os.remove(f)

    # Get P,T grid
    tgt_p = np.logspace(-5, 3, 15)
    tgt_t = [100.0,  250.0,  500.0,  750.0,  900.0,  1000.0,  1200.0,  1400.0,  1600.0,  1800.0,  2000.0,  2250.0,  2500.0,  2750.0,  3000.0,  3500.0,  4000.0]
    arr_p, arr_t, arr_f = dace.get_pt(formula_path, tgt_p , tgt_t)

    # Get nu grid + write skeleton
    temp_xc = cross.xsec(formula, source, dace.list_files(formula_path)[0])
    temp_xc.read(numin=numin, numax=numax, dnu=dnu)
    band_edges = spectral.best_bands(temp_xc.get_nu(), 2, nband)
    spectral.create_skeleton(alias, arr_p, arr_t, vols, band_edges)

    # Write netCDF containing absorption spectra
    nc_path = os.path.join(utils.dirs["output"] , alias+"_"+formula+".nc")
    _, dnu = netcdf.write_ncdf_from_grid(nc_path, formula, source, arr_p, arr_t, arr_f, dnu=dnu, numin=numin, numax=numax)

    # Calculate k-coefficients from netCDF 
    for i,f1 in enumerate(vols):
        spectral.calc_kcoeff_lbl(alias, f1, nc_path, nband)
        for f2 in vols[i:]:
            spectral.calc_kcoeff_cia(alias, f1, f2, band_edges, dnu)

    # Assemble final spectral file
    spectral.assemble(alias, vols)

    print("Goodbye")

if __name__ == "__main__":
    main()
    exit(0)
