#!/usr/bin/env python3
# Python wizard for interactive file conversion

# Import local files
import src.utils as utils
import src.spectral as spectral
import src.cross as cross
import src.phys as phys
import src.ptf as ptf
import src.netcdf as netcdf
import os
import glob
import numpy as np
import time


def main():

    # ------------ PARAMETERS ------------
    source = "exomol"         # Source database 
    vols = ["H2O"]   # List of gases
    alias = "Snowline"          # Alias for this spectral file
    UV = False               # Includes the UV range wavenumbers and cross-sections
    nband = 32              # Number of wavenumber bands
    drops = True            # Include water droplet scattering?
    method = 3              # Band selection method
    numax = 10000.0        # Clip to this maximum wavenumber [cm-1]
    numin = 10.0             # Clip to this minimum wavenumber [cm-1]
    dnu   = 1.0             # Downsample to this wavenumber resolution [cm-1]
    preNC = False           # Use pre-existing netCDF files in output/ if they are found

    xaxis = 'wavenumber'    # Plotting axis: wavelength [nm] or wavenumber [cm-1]
    lim = [None, None]      # Limits for the x-axis, example: if xaxis = wavenumber: [None, 100000], if xaxis = wavelength: [None, 1000], the whole spectra: [None, None]


    # Target pressures [bar] and temperatures [K] for the spectral file
    tgt_p = np.logspace(-3.5, 4.0, num=22, endpoint=True)
    tgt_t = np.array([
        25.0,
        *np.arange(100, 500, 25.0),
        *np.arange(500, 1000, 50.0),
        *np.arange(1000, 4100, 100.0),
        4500, 5000.0
    ], dtype=np.float64)

    # ------------ EXECUTION -------------
    # Check volatile names
    for i in range(len(vols)):
        safe = phys.chemsafe(vols[i])
        if safe is None:
            raise Exception("Invalid gas '%s'"%vols[i])
        vols[i] = safe

    # ===========
    # Check paths
    for v in vols:
        formula_path = os.path.join(utils.dirs[source], v.strip()+"/")
        if not os.path.exists(formula_path):
            raise Exception("Could not find folder '%s'" % formula_path)


    # ===========
    # Remove content of output folder under this alias (optionally including netCDFs)
    for f in glob.glob(utils.dirs["output"]+"/%s*"%alias):
        remove = [".log", ".sf", ".sf_k", ".sh", ".dat", ".chk", ".chk_k", ".sct", "_map", "_lbl"]
        if not preNC:
            remove.append(".nc")
        for p in remove:
            if p in f:
                utils.rmsafe(f)


    # ===========
    # Print params
    print("Parameters")
    print("    source: %s"%source)
    print("    alias:  %s"%alias)
    print("    vols:   %s"%utils.get_arr_as_str(vols))
    print("    nvols:  %d"%len(vols))
    print("    nband:  %d"%nband)
    print("    numin, numax, dnu : %.1f, %g, %.2f cm-1"%(numin, numax, dnu))
    print("    tgt_p:  %s"%utils.get_arr_as_str(tgt_p))
    print("    tgt_t:  %s"%utils.get_arr_as_str(tgt_t))
    print(" ")


    # ===========
    # Test each volatile for its numin, numax, pmin, pmax, tmin, tmax
    print("Verifying domain of input data")
    if source == "dace":
        if np.amin(tgt_p) < 1.0e-8:
            raise Exception("Requested pressures exceed DACE domain (p < 1.0e-8 bar)")
        if np.amax(tgt_p) > 1.0e3:
            raise Exception("Requested pressures exceed DACE domain (p > 1.0e3 bar)")

    #     check files directly
    dat_numin, dat_numax = np.inf, -np.inf
    dat_tmin, dat_tmax = np.inf, -np.inf
    for v in vols:
        print("    checking %s"%v)
        #     read first file
        formula_path = os.path.join(utils.dirs[source], v+"/")
        temp_xc = cross.xsec(v, source, ptf.list_files(source, v)[0])
        temp_xc.read(UV=UV, numin=numin, numax=numax, dnu=dnu)
        temp_xc.plot("wavelength", [None,None], show=False)

        #     get numin, numax
        vol_numin = np.amin(temp_xc.get_nu())
        vol_numax = np.amax(temp_xc.get_nu())
        dat_numin = min(dat_numin, vol_numin)
        dat_numax = max(dat_numax, vol_numax)
        print("        numin, numax = %.1f, %.1f cm-1"%(vol_numin, vol_numax))

        #     get tmin, tmax
        _,at,_ = ptf.list_all_ptf(source, v)
        dat_tmin = min(dat_tmin, np.amin(at))
        dat_tmax = max(dat_tmax, np.amax(at))

    #     check temperature range
    if np.amin(tgt_t) < dat_tmin:
        raise Exception("Requested temperatures exceed data domain (t < %g K)"%dat_tmin)
    if np.amax(tgt_t) > dat_tmax:
        raise Exception("Requested temperatures exceed data domain (t > %g K)"%dat_tmax)

    #     set new nu range
    numin = max(numin, dat_numin)
    numax = min(numax, dat_numax)
    print("    numin, numax set to %.1f, %.1f cm-1 \n"%(numin, numax)) # Set the nu limits to encompass all volatile nus (least restrictive)

    # ===========
    # Determine flattened p,t grid using last of the absorbers
    arr_p, arr_t  = ptf.best_pt(source, vols[-1], tgt_p, tgt_t)

    # Ensure pressure grid is ascending and unique
    # if not utils.is_ascending(arr_p):
    #     raise Exception("Pressure grid is not strictly ascending!")
    # if not utils.is_unique(arr_p):
    #     raise Exception("Pressure grid is not unique (contains repeated values)!")

    # ===========
    # Get nu array for required range and resolution (also using last absorber)
    nu_arr = cross.xsec(vols[-1], source, 
                            ptf.list_files(source, vols[-1])[0]).read(UV, numin=numin, numax=numax, dnu=dnu).get_nu()

    # ===========
    # Determine bands
    band_edges = spectral.best_bands(nu_arr, method, nband)

    # ===========
    # Write skeleton file and PT grids
    spectral.create_skeleton(alias, arr_p, arr_t, vols, band_edges)


    # ===========
    # Write netCDFs containing absorption spectra
    nc_paths = {}
    dnu_last = 1.000
    for iv,v in enumerate(vols):
        # For this volatile...

        # Determine output path
        ncp = os.path.join(utils.dirs["output"] , alias+"_"+v+".nc")
        nc_paths[v] = ncp
        if os.path.exists(ncp) and preNC:
            print("WARNING: Using pre-existing netCDF file for %s lbl absorption. Any configuration mismatch here will lead to issues."%v)
            continue

        # Get numin, numax for this volatile
        formula_path = ptf.get_formula_path(source, v)
        temp_xc = cross.xsec(v, source, ptf.list_files(source, v)[0])
        temp_xc.parse_name()
        
        # Map files, finding the closest p,t point to each target p,t point
        vol_p, vol_t, vol_f = ptf.map_ptf(source, v, arr_p, arr_t)

        # Write these p,t,f to csv file for reference
        ptf.write_csv(alias, v, vol_p, vol_t, vol_f)

        # Write netCDF from BIN files
        dnu_this = netcdf.write_ncdf_from_grid(UV, ncp, v, source, arr_p, arr_t, vol_f, dnu=dnu, numin=numin, numax=numax)

        # Check resolution
        if (iv > 0) and (not np.isclose(dnu_last, dnu_this)):
            raise Exception("Wavenumber resolutions differ between volatiles (%g != %g)" % (dnu_last, dnu_this))
        else:
            dnu_last = dnu_this


    # ===========
    # Calculate k-coefficients from netCDF
    for i,f1 in enumerate(vols):
        spectral.calc_kcoeff_lbl(alias, f1, nc_paths[f1])
        for f2 in vols[i:]:
            spectral.calc_kcoeff_cia(alias, f1, f2, dnu_last)


    # ===========
    # Calculate water droplet properties
    if drops and ("H2O" in vols):
        spectral.calc_waterdroplets(alias)


    # ===========
    # Assemble final spectral file
    spectral.assemble(alias, vols)

    # ------------------------------------
    return


if __name__ == "__main__":
    utils.checkenv()
    start = time.perf_counter()
    print("Hello\n")
    main()
    end = time.perf_counter()
    elapsed = (end-start)
    print('Time elapsed: ', elapsed//3600, 'hours', "%.2f"%((elapsed%3600)//60), 'minutes.')
    print("Goodbye")
    exit(0)
