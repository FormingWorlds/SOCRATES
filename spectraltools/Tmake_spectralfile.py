#!/usr/bin/env python3
# Python wizard for interactive file conversion

# Import local files
import src.utils as utils
import src.spectral as spectral
import src.cross as cross
import src.phys as phys
import src.ptf as ptf
import src.netcdf as netcdf
import logging
import os
import glob
import numpy as np
import time

log = logging.getLogger("fwl."+__name__)


def main():

    log.info("    SOCRATES directory: %s", utils.dirs["socrates"])
    log.info("    SOCRATES version: %s", utils.socratesver())
    log.info("    SOCRATES git hash: %s", utils.git_hash())

    # Water
    # vols = ["H2O" ]   # List of gases
    # alias = "Snowline"          # Alias for this spectral file

    # Rock vapours
    # vols = ["CO", "O2", "SiO", "TiO", "MgO", "Na", "K", "Fe"]   # List of gases
    # alias = "Volenfell"          # Alias for this spectral file

    # Oxidised volatiles
    # vols = ["H2O", "CO2", "CO", "O2", "SO2", "OCS", "S2" ]   # List of gases
    # alias = "Breezehome"          # Alias for this spectral file

    # Reduced volatiles
    # vols = ["H2", "CO", "CH4", "SH", "S2", "H2S", "N2", "NH3" ]   # List of gases
    # alias = "Cliffshade"          # Alias for this spectral file

    # Combined volatiles
    # vols = ["H2O", "H2", "CO2", "CO", "O2", "O3", "CH4", "SO2", "OCS", "SH", "S2", "H2S", "N2", "NH3", "HCN"]
    # alias = "Proudspire"

    # Hot jupiters
    # vols = ["H2O", "H2", "CO2", "CO", "SiO", "TiO", "VO", "MgO", "Na", "K", "Fe"]
    # alias  = "Skyborn"

    # Vapours + volatiles (small)
    # vols = ["H2O", "H2", "CO2", "CO", "O2", "CH4", "SO2", "NH3", "SiO",	"TiO", "Na", "K"]
    # alias = "Atmora"

    # Vapours + volatiles (large)
    # vols = ["H2O", "H2", "CO2", "CO", "O2", "O3", "CH4", "SO2", "OCS", "SH", "S2", "H2S", "N2", "NH3", "HCN", "SiO", "TiO", "MgO", "Na", "K", "Fe"]
    # alias = "Sovngarde"

    # ------------ PARAMETERS ------------
    source = "exocross"         # Source database
    vol_source = {"VO":"dace", "CH4":"dace"}   # Per-gas overrides of source database
    vols = ["H2O" ]   # List of gases
    alias = "Snowline"          # Alias for this spectral file
    UV = False               # Includes the UV range wavenumbers and cross-sections
    nband = 128              # Number of wavenumber bands
    drops = True            # Include water droplet scattering?
    method = 3              # Band selection method
    numax = 50000.0        # Clip to this maximum wavenumber [cm-1]
    numin = 10.0             # Clip to this minimum wavenumber [cm-1]
    dnu   = 0.025             # Downsample to this wavenumber resolution [cm-1]
    preNC = True           # Use pre-existing netCDF files in output/ if they are found

    # band selection methods (wavenumber space):
    # 0 = linspace   \n
    # 1 = logspace   \n
    # 2 = linspace, using a single band to cover long WL \n
    # 3 = logspace, using a few linear-spaced bands to cover long WL \n
    # 4 = piecewise density (linspace - logspace - logspace) \n
    # 5 = selected by density of the planck function at given temperatures \n
    # 9 = match legacy spectral file (IN THIS CASE nband MUST BE SET TO 318)


    xaxis = 'wavenumber'    # Plotting axis: wavelength [nm] or wavenumber [cm-1]
    lim = [100.0, numax]      # Limits for the x-axis, example: if xaxis = wavenumber: [None, 100000], if xaxis = wavelength: [None, 1000], the whole spectra: [None, None]

    # Target pressures [bar]
    tgt_p = [
        -5.0, -4.0,
        *np.arange(-3.5, 4.5, 0.5)
    ]
    tgt_p = np.array([utils.round_float_sigfigs(10**p, 1) for p in tgt_p], dtype=np.float64)

    # Target temperatures [K]
    tgt_t = np.array([
        25.0,
        *np.arange(100, 350, 25.0),
        *np.arange(350, 1000, 50.0),
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

    # Source database for each volatile
    vol_source = {phys.chemsafe(k):utils.sourcesafe(s) for k,s in vol_source.items()}
    srcs = {v:vol_source.get(v, source) for v in vols}

    # Reference volatile for p,t grid and band edges: last one using the default source
    vref = ([v for v in vols if srcs[v] == source] or vols)[-1]

    # ===========
    # Check paths
    for v in vols:
        formula_path = os.path.join(utils.dirs[srcs[v]], v.strip()+"/")
        if not os.path.exists(formula_path):
            raise Exception("Could not find folder '%s'" % formula_path)


    # ===========
    # Remove content of output folder under this alias (optionally including netCDFs)
    for f in glob.glob(utils.dirs["output"]+"/%s*"%alias):
        remove = [".log", ".sf", ".sf_k", ".sh", ".dat", ".chk", ".chk_k",
                  ".sct", "_map", "_lbl", ".pdf", ".png", ".csv", "_map.nc"]
        if not preNC:
            remove.append(".nc")
        for p in remove:
            if p in f:
                utils.rmsafe(f)


    # ===========
    # Print params
    log.info("")
    log.info("Parameters")
    log.info("    source:   %s", source)
    log.info("    gases:    (N=%d)", len(vols))
    for v in vols:
        log.info("          %6s from %s", v, srcs[v])
    log.info("    alias:    %s", alias)
    log.info("    nband:    %d", nband)
    log.info("    numin, numax, dnu : %.3f, %.3f, %.3f cm-1", numin, numax, dnu)
    log.info("    method:   %d", method)
    log.info("    masspath: %.2e kg/m2", spectral.CCORRK_MAXPATH)
    log.info("    UV:       %s", str(UV))
    log.info("    preNC:    %s", str(preNC))
    log.info("    n_tp:     %d", len(tgt_p)*len(tgt_t))
    log.info("    tgt_p:    %s", utils.get_arr_as_str(tgt_p, fmt=r"%.2e", sep=','))
    log.info("    tgt_t:    %s", utils.get_arr_as_str(tgt_t, fmt=r"%.2f", sep=','))
    log.info("    drops:    %s", str(drops))


    # ===========
    # Test each volatile for its numin, numax, pmin, pmax, tmin, tmax
    log.info("")
    log.info("Verifying domain of input data")
    #     check files directly
    dat_numin, dat_numax = np.inf, -np.inf
    dat_tmin, dat_tmax = np.inf, -np.inf
    dat_pmin, dat_pmax = np.inf, -np.inf
    for v in vols:
        log.info("    checking %s", v)
        #     read first file
        formula_path = os.path.join(utils.dirs[srcs[v]], v+"/")
        temp_xc = cross.xsec(v, srcs[v], ptf.first_file(srcs[v], v))
        temp_xc.read(UV=UV, numin=numin, numax=numax, dnu=dnu)
        temp_xc.plot([None,None],
                     show=False, quiet=True,
                     alias=alias+"_", pad_xlim=5e3)

        #     get numin, numax
        vol_numin = np.amin(temp_xc.get_nu())
        vol_numax = np.amax(temp_xc.get_nu())
        dat_numin = min(dat_numin, vol_numin)
        dat_numax = max(dat_numax, vol_numax)
        log.info("        numin, numax = %.1f, %.1f cm-1", vol_numin, vol_numax)

        #     get pmin, pmax, tmin, tmax
        ap,at,_ = ptf.list_all_ptf(srcs[v], v, quiet=False)
        dat_tmin = min(dat_tmin, np.amin(at))
        dat_tmax = max(dat_tmax, np.amax(at))
        dat_pmin = min(dat_pmin, np.amin(ap))
        dat_pmax = max(dat_pmax, np.amax(ap))

        #     warn if this volatile will be clamped to its nearest p,t point
        rtol = 1.0e-2
        p_out = tgt_p[(tgt_p < np.amin(ap)*(1-rtol)) | (tgt_p > np.amax(ap)*(1+rtol))]
        t_out = tgt_t[(tgt_t < np.amin(at)*(1-rtol)) | (tgt_t > np.amax(at)*(1+rtol))]
        if len(p_out) > 0:
            log.warning("    %s data spans p = [%.2e, %.2e] bar; using nearest for p = %s bar",
                        v, np.amin(ap), np.amax(ap), utils.get_arr_as_str(p_out, fmt=r"%.2e", sep=','))
        if len(t_out) > 0:
            log.warning("    %s data spans t = [%.2f, %.2f] K; using nearest for t = %s K",
                        v, np.amin(at), np.amax(at), utils.get_arr_as_str(t_out, fmt=r"%.2f", sep=','))

    #     check temperature and pressure range
    if np.amin(tgt_t) < dat_tmin:
        raise Exception("Requested temperatures exceed data domain (t < %.2f K)"%dat_tmin)
    if np.amax(tgt_t) > dat_tmax:
        raise Exception("Requested temperatures exceed data domain (t > %.2f K)"%dat_tmax)
    if np.amin(tgt_p) < dat_pmin*(1-rtol):
        raise Exception("Requested pressures exceed data domain (p < %.2e bar)"%dat_pmin)
    if np.amax(tgt_p) > dat_pmax*(1+rtol):
        raise Exception("Requested pressures exceed data domain (p > %.2e bar)"%dat_pmax)

    #     set new nu range
    numin = max(numin, dat_numin)
    numax = min(numax, dat_numax)
    log.info("    numin, numax set to %.1f, %.1f cm-1", numin, numax) # Set the nu limits to encompass all volatile nus (least restrictive)

    # ===========
    # Determine flattened p,t grid using reference absorber
    log.info("Using %s as reference for p,t grid and band edges", vref)
    arr_p, arr_t  = ptf.best_pt(srcs[vref], vref, tgt_p, tgt_t)

    # Ensure pressure grid is ascending and unique
    # if not utils.is_ascending(arr_p):
    #     raise Exception("Pressure grid is not strictly ascending!")
    # if not utils.is_unique(arr_p):
    #     raise Exception("Pressure grid is not unique (contains repeated values)!")

    # ===========
    # Get nu array for required range and resolution (first file from reference absorber)
    nu_file = ptf.first_file(srcs[vref], vref)
    nu_samp = cross.xsec(vref, srcs[vref], nu_file)
    nu_arr = nu_samp.read().get_nu()

    # ===========
    # Determine bands
    log.info("")
    band_edges = spectral.best_bands(nu_arr, method, nband, alias=alias+"_")

    # ===========
    # Write skeleton file and PT grids
    log.info("")
    spectral.create_skeleton(alias, arr_p, arr_t, vols, band_edges)


    # ===========
    # Write netCDFs containing absorption spectra
    log.info("")
    nc_paths = {}
    dnu_last = None
    for iv,v in enumerate(vols):
        # For this volatile...

        # Determine output path
        ncp = os.path.join(utils.dirs["output"] , alias+"_"+v+".nc")
        nc_paths[v] = ncp

        # Get numin, numax for this volatile
        formula_path = ptf.get_formula_path(srcs[v], v)
        temp_xc = cross.xsec(v, srcs[v], ptf.first_file(srcs[v], v))
        temp_xc.read()
        temp_xc.plot([numin, numax], show=False, quiet=False,
                     band_edges=band_edges,
                     alias=alias+"_", pad_xlim=5e3)
        numin_v = max(numin, np.amin(temp_xc.get_nu()))
        numax_v = min(numax, np.amax(temp_xc.get_nu()))

        # Can skip PTF mapping?
        if os.path.exists(ncp) and preNC:
            log.warning("Using pre-existing netCDF file for %s lbl absorption"%v)
            log.warning("    Configuration mismatch here will lead to issues")

            # Resolution of the existing file, in [m-1]
            nu_pre = netcdf.read_netcdf_nu(ncp)
            dnu_this = float(nu_pre[1]-nu_pre[0]) * 100.0
            log.info("    Wavenumber resolution of pre-existing file: %g m-1"%dnu_this)

        else:
            # Map files, finding the closest p,t point to each target p,t point
            vol_p, vol_t, vol_f = ptf.map_ptf(srcs[v], v, arr_p, arr_t)

            # Write these p,t,f to csv file for reference
            ptf.write_csv(alias, v, vol_p, vol_t, vol_f)

            # Write netCDF from source files
            dnu_this = netcdf.write_ncdf_from_grid(UV, ncp, v, srcs[v],
                                                   arr_p, arr_t, vol_f,
                                                   dnu=dnu, numin=numin_v, numax=numax_v)

        # Check resolution
        if (dnu_last is not None) and (not np.isclose(dnu_last, dnu_this)):
            raise Exception("Wavenumber resolutions differ between volatiles (%g != %g)" % (dnu_last, dnu_this))
        else:
            dnu_last = dnu_this

    if dnu_last is None:
        raise Exception("Could not determine wavenumber resolution of netCDF files")


    # ===========
    # Calculate k-coefficients from netCDF
    log.info("")
    for i,f1 in enumerate(vols):
        spectral.calc_kcoeff_lbl(alias, f1, nc_paths[f1])
        for f2 in vols[i:]:
            spectral.calc_kcoeff_cia(alias, f1, f2, dnu_last)


    # ===========
    # Calculate water droplet properties
    log.info("")
    if drops and ("H2O" in vols):
        spectral.calc_waterdroplets(alias)


    # ===========
    # Assemble final spectral file
    log.info("")
    spectral.assemble(alias, vols)

    # ------------------------------------
    return alias


if __name__ == "__main__":
    logfile = utils.setup_logger("Tmake_spectralfile")
    utils.checkenv()
    start = time.perf_counter()
    log.info("Spectral Tools Wizard (version %s)", utils.__version__)
    alias = main()
    end = time.perf_counter()
    elapsed = (end-start)
    log.info("Time elapsed: %d hours %.2f minutes.", elapsed//3600, (elapsed%3600)//60)

    # Copy this run's log into output folder
    out_logfile = utils.move_log_to_output(logfile, alias=alias)
    log.info("Copied log file to '%s'", out_logfile)

    log.info("Goodbye")
    exit(0)
