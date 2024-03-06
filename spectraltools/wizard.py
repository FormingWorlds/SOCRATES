#!/usr/bin/env python3 
# Python wizard for interactive file conversion

# Import local files 
import src.utils as utils
import src.spectral as spectral
import src.dace as dace
import src.cross as cross
import src.netcdf as netcdf
import os, glob

def main():
    print("Wizard says hello")

    formula = "H2O"
    source = "dace"
    vols = [formula]
    alias = "demo"
    nband = 10
    numax = 2e4   # clip to this maximum wavenumber [cm-1]
    numin = 1.0    # clip to this minimum wavenumber [cm-1]
    dnu   = 0.0    # downsample to this wavenumber resolution [cm-1]

    formula_path = os.path.join(utils.dirs[source], formula.strip()+"/")
    if not os.path.exists(formula_path):
        raise Exception("Could not find folder '%s'" % formula_path)
    
    for f in glob.glob(utils.dirs["output"]+"/%s*"%alias):
        os.remove(f)

    # Get P,T grid
    arr_p, arr_t, arr_f = dace.get_pt(formula_path, [0.01, 10.0, 100.0, 1000.0] , [100, 800, 2000.0])

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
