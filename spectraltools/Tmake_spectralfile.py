#!/usr/bin/env python3 
# Python wizard for interactive file conversion

# Import local files 
import src.utils as utils
import src.spectral as spectral
import src.dace as dace
import src.cross as cross
import src.phys as phys
import src.netcdf as netcdf
import os, glob
import numpy as np

def main():

    # ------------ PARAMETERS ------------
    source = "dace"             # Source database (DO NOT CHANGE)
    vols = ["H2O"]              # List of volatile absorbers
    alias = "Falkreath"         # Alias for this spectral file
    nband = 100                 # Number of wavenumber bands
    drops = False  # include water droplet scattering?
    method = 3     # band selection method
    numax = 3.5e4  # clip to this maximum wavenumber [cm-1]
    numin = 1.0    # clip to this minimum wavenumber [cm-1]
    dnu   = 0.0    # downsample to this wavenumber resolution [cm-1]
    preNC = True   # use pre-existing netCDF files in output/ if they are found

    # tgt_p = tgt_t = []

    tgt_p = np.logspace(-6, 3, 80)
    # tgt_t = np.append( [60.0, 100.0, 150.0, 200.0] , np.linspace(250.0, 2900.0, 20)  ) - 5.0
    tgt_t = np.linspace(105.0, 2900.0, 20) - 5.0

    # ------------------------------------




   
    # ------------ EXECUTION -------------
    # Check volatile names
    for i in range(len(vols)):
        vols[i] = phys.chemsafe(vols[i])


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
    print("    nband:  %d"%nband)
    print("    numin, numax, dnu = %.1f, %g, %.2f cm-1"%(numin, numax, dnu))
    print(" ")


    # ===========
    # Test each volatile for its numin, numax, pmin, pmax, tmin, tmax
    print("Verifying domain of input data")
    #     pressure grids are always the same
    if np.amin(tgt_p) < 1.0e-8:
        raise Exception("Requested pressures exceed data domain (p < 1.0e-8 bar)")
    if np.amax(tgt_p) > 1.0e3:
        raise Exception("Requested pressures exceed data domain (p > 1.0e3 bar)")

    #     check files directly
    dat_numin, dat_numax = np.inf, -np.inf
    dat_tmin, dat_tmax = np.inf, -np.inf
    for v in vols:
        print("    checking %s"%v)
        #     read first file
        formula_path = os.path.join(utils.dirs[source], v.strip()+"/")
        temp_xc = cross.xsec(v, source, dace.list_files(formula_path)[0])
        temp_xc.read(numin=numin, numax=numax, dnu=dnu)

        #     get numin, numax
        dat_numin = min(dat_numin, np.amin(temp_xc.get_nu()))
        dat_numax = max(dat_numax, np.amax(temp_xc.get_nu()))

        #     get tmin, tmax 
        _,at,_ = dace.list_all_ptf(formula_path)
        dat_tmin = min(dat_tmin, np.amin(at))
        dat_tmax = max(dat_tmax, np.amax(at))

    #     check temperature range
    if np.amin(tgt_t) < dat_tmin:
        raise Exception("Requested temperatures exceed data domain (t < %g K)"%dat_tmin)
    if np.amax(tgt_t) < dat_tmax:
        raise Exception("Requested temperatures exceed data domain (t > %g K)"%dat_tmax)

    #     set new nu range
    numin = max(numin, dat_numin)
    numax = min(numax, dat_numax)
    print("    numin, numax set to %.1f, %.1f cm-1 \n"%(numin, numax)) # Set the nu limits to encompass all volatile nus (least restrictive)


    # ===========
    # Determine p,t grid using one of the absorbers
    arr_p, arr_t, arr_f = dace.map_ptf(formula_path, tgt_p , tgt_t)


    # ===========
    # Get nu array for required range and resolution
    formula_path = os.path.join(utils.dirs[source], vols[0].strip()+"/")
    nu_arr = cross.xsec(vols[0], source, dace.list_files(formula_path)[0]).read(numin=numin, numax=numax, dnu=dnu).get_nu()


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

        # Output path
        ncp = os.path.join(utils.dirs["output"] , alias+"_"+v+".nc")
        nc_paths[v] = ncp
        if os.path.exists(ncp) and preNC:
            print("WARNING: Using pre-existing netCDF file for %s lbl absorption. Any configuration mismatch here will lead to issues."%v)
            continue 

        # Get files for this volatile using the p,t,f map from vols[0]
        files = []
        if iv > 0:
            for f in arr_f: 
                # Try simply substituting volatile name
                ftry = str(f).replace(vols[0], v)
                if os.path.exists(ftry):
                    files.append(ftry)
                    continue 

                # Try also substituting "out"<->"itp" 
                if "Itp" in ftry:
                    ftry = ftry.replace("Itp", "Out")
                else:
                    ftry = ftry.replace("Out", "Itp")
                if os.path.exists(ftry):
                    files.append(ftry)
                    continue 

                raise Exception("Could not find bin file for '%s' corresponding to '%s'"%(v,f))

            if (len(files) != len(arr_f)):
                raise Exception("Could not map '%s' files to '%s' files" % (v, vols[0]))
        else:
            files = arr_f

        # Write netCDF from BIN files
        dnu_this = netcdf.write_ncdf_from_grid(ncp, v, source, arr_p, arr_t, files, dnu=dnu, numin=numin, numax=numax)

        # Check resolution
        if (iv > 0) and (not np.isclose(dnu_last, dnu_this)):
            raise Exception("Wavenumber resolutions differ between volatiles (%g != %g)" % (dnu_last, dnu_this))
        else:
            dnu_last = dnu_this


    # ===========
    # Calculate k-coefficients from netCDF 
    for i,f1 in enumerate(vols):
        spectral.calc_kcoeff_lbl(alias, f1, nc_paths[f1], nband)
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
    print("Hello\n")
    main()
    print("Goodbye")
    exit(0)
