# Tools for handling socrates spectral files

import numpy as np
import os, subprocess, time
import src.utils as utils

def best_bands(nu_arr:np.ndarray, method:int, nband:int, floor=1.0) -> np.ndarray:
    """Choose the best band edges.

    Given all the available nu values, calculates the 'best' band edges for a given method. \n
    Methods:    
        0 = linspace   \n 
        1 = logspace   \n
        2 = logspace, using a single band to cover long WL \n
        3 = logspace, using a few linear-spaced bands to cover long WL \n
        4 = piecewise band density (linspace - logspace - logspace) \n
        9 = match legacy spectral file (IN THIS CASE nband MUST BE SET TO 318)

    Parameters
    ----------
    nu_arr : np.ndarray
        Wavenumber array [cm-1]
    method : int
        Selection method
    nband : int 
        Required number of bands
    floor : float
        Restrict nu to be larger than this value

    Returns
    -------
    np.ndarray
        Band edges, ascending [cm-1]
    """

    print("Finding best bands (method=%d)..."%method)

    # Validate
    if len(nu_arr) < 2:
        raise Exception("Wavenumber array is too short")
    if not utils.is_ascending(nu_arr):
        raise Exception("Wavenumber array is not strictly ascending")
    if nband < 1:
        raise Exception("There must be at least one band")
    if nband > len(nu_arr)-2:
        raise Exception("Too many bands! (%d requested)"%nband)
    if (method == 9) and (nband != 318):
        raise Exception("When method=9 (legacy), you must set nband=318")
    
    # Check range
    numin = max(nu_arr[1], floor)
    numax = nu_arr[-2]
    lognumin = np.log10(numin)
    lognumax = np.log10(numax)

    # Simple case
    if nband == 1:
        return [numin, numax]
    
    # Other cases ...
    if (nband == 2) and (method > 2):
        method = 2

    shrt_cutoff = 1.7e4  # [cm-1] Value where the "short wavelength" region starts.
    if (numax < shrt_cutoff) and (method == 4):
        method = 3
    
    long_cutoff = 200.0 # [cm-1] Value where the "long wavelength" region starts.
    if (numin > long_cutoff) and (method in [2,3]):
        method = 1 
    
    # Get target bands
    nedges = nband+1
    match method:
        case 0:
            bands = np.linspace(numin, numax, nedges)
        case 1: 
            bands = np.logspace(lognumin, lognumax, nedges)
        case 2:
            bands = np.array([numin, long_cutoff])
            bands = np.append(bands, np.logspace(np.log10(long_cutoff) , lognumax , nedges-1 )[1:])
        case 3: 
            len_lin = int(nedges*0.15)
            bands = np.linspace(numin, long_cutoff, len_lin+1)[:-1]
            bands = np.append(bands, np.logspace(np.log10(long_cutoff), lognumax, nedges-len_lin))
        case 4:
            len1 = int( max(nedges*0.15, 2) )
            len3 = int( max(nedges*0.07, 2) )
            len2 = nedges-len1-len3
            bands = np.linspace(numin, long_cutoff, len1+1)[:-1]
            bands = np.append(bands, np.logspace(np.log10(long_cutoff), np.log10(shrt_cutoff), len2+1)[:-1])
            bands = np.append(bands, np.logspace(np.log10(shrt_cutoff), lognumax, len3))
        
        case 9:
            bands = np.concatenate((np.arange(0.0,3000,25),np.arange(3000,11000,50),np.arange(11000,30500,500))) 
            bands[0] = 1.0
            numin = bands[0]
            numax = bands[-1]
        case _:
            raise Exception("Invalid band selection method (%d)"%method)

    # For each target band, find closest nu value
    bands_out = []
    dist_last = 9e99
    set_band = 0
    for i,nu in enumerate(nu_arr):      # iterate over all nu
        dist = abs(nu-bands[set_band])  # distance between this nu and target band edge
        if dist > dist_last:            # further from the edge than before => were closest to it during the previous iter
            bands_out.append(nu_arr[i-1])  # store band edge
            set_band += 1                  # target nu set to next edge
            dist_last = 9e99
            if set_band > 1:
                print("    band %3d : %.2f - %.2f cm-1     %.2f - %.2f nm" 
                      % (set_band-1, bands_out[-2], bands_out[-1], utils.wn2wl(bands_out[-2]), utils.wn2wl(bands_out[-1]))
                      )
        else:
            dist_last = dist
        if (method==9) and (set_band == nband+1):
            break
    bands_out = np.array(bands_out)

    suggest = "Try a different method, choose fewer bands, or increase the source resolution"
    if not utils.is_unique(bands_out):
        raise Exception("Best band edges are not unique! "+suggest)
    if not utils.is_ascending(bands_out):
        raise Exception("Best band edges are not ascending! "+suggest)

    print("    done\n")
    return bands_out


def get_cia_pair(fA:str, fB:str):
    """Get the valid CIA pairing.

    If the two absorber names fA,fB form a valid CIA pair, returns that pair as 
    as list with two elements. Otherwise returns an empty list.

    Parameters
    ----------
    fA : str
        formula A
    fB : str
        formula B

    Returns
    -------
    list
        CIA pairing
    """

    p_in  = [fA,fB]
    for p_check in utils.cia_pairs:  # For each possible pairing
        # Is valid
        if p_in == p_check:
            return p_in
        # Is valid, but swapped
        if [p_in[1], p_in[0]] == p_check:
            return [p_in[1], p_in[0]]
    return []

def create_skeleton(alias:str, p_points:np.ndarray, t_points:np.ndarray, volatile_list:list, band_edges:list, dry:bool=False):
    """Create skeleton spectral file.

    Creates a spectral file with meta-data. Does not calculate k-terms or other physical properties.

    Parameters
    ----------
    alias : str
        alias of spectral file
    p_points : np.ndarray
        Pressure values [bar]
    t_points : np.ndarray
        Temperature values [K]
    volatile_list : list 
        List of absorber names
    band_edges : list 
        List of band edges (length = nbands+1) [cm-1]
    
    dry : bool
        Dry run?

    Returns
    -------
    str
        Path to skeleton spectral file
    """

    print("Creating skeleton spectral file '%s'"%alias)
    skel_path = os.path.join(utils.dirs["output"], alias+"_skel.sf")
    utils.rmsafe(skel_path)
 
    # Sanitise bands
    if not utils.is_ascending(band_edges):
        raise Exception("Band edges must be strictly ascending")
    numin = band_edges[0]
    numax = band_edges[-1]
    nband = len(band_edges)-1
    print("    number of bands: %d"%nband)
    print("    numin , numax: %.2f , %.2f cm-1"%(numin, numax))

    # Sanitise volatiles 
    volatile_list_unique = list(set(volatile_list))
    volatile_list = []
    for v in volatile_list_unique:
        v = str(v).strip()
        if v not in list(utils.absorber_id.keys()):
            raise Exception("Volatile %s is not supported by SOCRATES"%v)
        volatile_list.append(v)
    nvols = len(volatile_list)
    print("    included volatiles (n=%d): "%len(volatile_list) + utils.get_arr_as_str(volatile_list))

    # P-T grids for LbL and CIA data
    pt_lbl = os.path.join(utils.dirs["output"], "%s_pt_lbl.dat"%alias); utils.rmsafe(pt_lbl)
    pt_cia = os.path.join(utils.dirs["output"], "%s_pt_cia.dat"%alias); utils.rmsafe(pt_cia)

    # File name of bash execution script to be written
    exec_file_name = os.path.join(utils.dirs["output"],"%s_make_skel.sh"%alias)
    utils.rmsafe(exec_file_name)

    p_write = np.round(p_points * 1.0e5, 3)  
    t_write = np.round(t_points, 3)
    
    print("    number of p,t points: %d"%len(t_write))
    print("    unique p values [Pa]: "+ utils.get_arr_as_str(np.unique(p_write)))
    print("    unique t values [K] : "+ utils.get_arr_as_str(np.unique(t_write)))

    # Generate P-T files to be read by Ccorr_k script
    pt_lbl_file = open(pt_lbl, "w+")
    pt_lbl_file.write('*PTVAL' + '\n')
    for prs in np.unique(p_write):
        line = ""
        line += "%.4f"%prs 
        for t in np.unique(t_write):
            line +=" %.4f"%t 
        line += "\n" 
        pt_lbl_file.write(line)
    pt_lbl_file.write('*END' + '\n')
    pt_lbl_file.close()
    
    ref_pres_cia = utils.get_closest(1.0e5, p_write) # set reference pressure to ~1 bar
    pt_cia_file = open(pt_cia, "w+")
    pt_cia_file.write('*PTVAL \n')
    line = "%.4f"%ref_pres_cia 
    for t in np.unique(t_write):
        line +=" %.4f"%t 
    pt_cia_file.write(line + " \n")
    pt_cia_file.write('*END \n')
    pt_cia_file.close()

    # Open file to produce bash script
    f = open(exec_file_name, "w+")

    # Write skeleton spectral file using prep_spec utility
    f.write('prep_spec <<EOF\n')
    f.write(skel_path + '\n')

    # Set number of bands
    f.write("%d \n"%nband)

    # Set total number of absorbers 
    # (both LbL- and CIA-only ones, count all uncommented, individual molecules below)
    f.write("%d \n"%nvols)
    abs_ids = []
    for v in volatile_list:
        absid = utils.absorber_id[v]
        abs_ids.append(absid)
        f.write(absid +" \n")

    # Count total number of continua (self and foreign)
    active_pairs = []
    for i,p in enumerate(utils.cia_pairs):
        if ((p[0] in volatile_list) and (p[1] in volatile_list)) or (  (p[1] in volatile_list) and  (p[0] in volatile_list) ):
            active_pairs.append(i)
    f.write("%d \n"%len(active_pairs))
    print("    number of continua: %d"%len(active_pairs))

    # Set CIA pairs
    for i in active_pairs:
        p = utils.cia_pairs[i]
        f.write("%s %s \n"%(utils.absorber_id[p[0]],utils.absorber_id[p[1]]))

    # Set number of aerosols
    f.write("0 \n")

    # Set bands manually (in reverse order, since they'll be converted to wavelength)
    f.write("c \n")
    for i in range(nband,0,-1):
        f.write("%.3f %.3f \n"%(band_edges[i], band_edges[i-1]))
    # for i in range(nband):
    #     f.write("%.3f %.3f \n"%(band_edges[i], band_edges[i+1]))

    # Set absorbers in each band to zero for now
    f.write("0*%d\n"%nband)

    # Set continua in each band to zero for now
    f.write("0*%d\n"%nband)

    # Exclude no regions
    f.write("n \n")

    # Close prep_spec
    f.write("-1 \n")
    f.write("EOF\n")
    f.write(" \n ")
    f.close()
    os.chmod(exec_file_name,0o777)

    logfile = os.path.join(utils.dirs["output"], "%s_skel.log"%alias); utils.rmsafe(logfile)
    if not dry:
        with open(logfile,'w') as hdl:
            sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
        sp.check_returncode()

    time.sleep(1.0)
    print("    done writing to '%s' \n"%skel_path)
    return skel_path

def calc_kcoeff_lbl(alias:str, formula:str, nc_xsc_path:str, nband:int,  dry:bool=False):
    """Calculate k-coefficients for line absorption

    Takes netCDF file containing cross-sections as input. Outputs k-terms at given p,t points and bands specified in the skeleton file

    Parameters
    ----------
    alias : str
        Alias of spectral file
    formula : str
        Formula of absorber
    nc_xsc_path : str
        Input netCDF file containing cross-section data for range of p,t,nu
    nband : int
        Number of bands (THIS MUST MATCH THE SKELETON FILE)

    dry : bool
        Dry run?

    Returns 
    ----------
    str
        Path to file containing the new k-coefficients
    """

    # <EXAMPLE>
    # 
    # Ccorr_k -F ${GAS_DATA_DIR}/${PT_FILE} \
    #   -R 1 400 -l 1 ${COL_MASS_K_H2O} -b 5.0e-4 \
    #   -s $skelfile +p -lk \
    #   -o $sp_dir/h2o_lwf_l -m $sp_dir/h2o_lwf_lm \
    #   -L $H2O_LBL_LWF \
    #   -sm $sp_dir/h2o_lwf_l_map.nc \
    #    > $sp_dir/h2o_lwf_log
    #
    # </EXAMPLE>

    print("Calculating k-coefficients for '%s' line absorption for '%s'..."%(formula, alias))

    # Parameters
    max_path = 1.0e1
    tol_type = 't'
    nproc = 20

    # Check that files exist
    skel_path   = os.path.join(utils.dirs["output"], alias+"_skel.sf")
    pt_lbl      = os.path.join(utils.dirs["output"], "%s_pt_lbl.dat"%alias)
    for f in [nc_xsc_path, skel_path, pt_lbl]:
        if not os.path.exists(f):
            raise Exception("File not found: '%s'"%f)
        
    formula = formula.strip()
    absid = utils.absorber_id[formula]

    kcoeff_path  = os.path.join(utils.dirs["output"],"%s_%s_lbl.sf_k"%(alias,formula)); utils.rmsafe(kcoeff_path)
    monitor_path = os.path.join(utils.dirs["output"],"%s_%s_mon.log"%(alias,formula)); utils.rmsafe(monitor_path)
    mapping_path = os.path.join(utils.dirs["output"],"%s_%s_map.nc"% (alias,formula)); utils.rmsafe(mapping_path)
    logging_path = os.path.join(utils.dirs["output"],"%s_%s.log"%    (alias,formula)); utils.rmsafe(logging_path)

    # Open executable file for writing
    exec_file_name = os.path.join(utils.dirs["output"],"%s_make_%s.sh"%(alias,formula)); utils.rmsafe(exec_file_name)
    f = open(exec_file_name, 'w+')

    f.write("Ccorr_k")
    f.write(" -F %s"%pt_lbl)                  # (Input) Pathname of file containing pressures and temperatures at which to calculate coefficients. 
    f.write(" -R 1 %d"%nband)                 # The range of spectral bands to be used 
    f.write(" -l %s %.3e"%(absid, max_path))  # Generate line absorption data. gas is the type number (identifier) of the gas to be considered. max−path is the maximum absorptive pathlength (kg/m2) for the gas

    match tol_type:
        case 'n': f.write(" -n 20")         # Use this many k-terms
        case 't': f.write(" -t 1.0e-3")     # Calculate k-terms needed to keep RMS error in the transmission below this value
        case 'b': f.write(" -b 1.0e-2")     # Calculate k-terms according to where absorption scaling peaks, keeping the maximum transmission error below this value

    f.write(" -s %s"%skel_path)         # (Input) Path to skeleton spectral file (used to provide the spectral bands - will not be overwritten)
    f.write(" +p")                      # Planckian Weighting
    f.write(" -lk")                     # A look-up table will be used for the pressure/temperature scaling
    f.write(" -k")                      # Adjust for continuua
    f.write(" -o %s"%kcoeff_path)       # Output file, holding the correlated-k terms for each pressure/temperature
    f.write(" -m %s"%monitor_path)      # (Output) Pathname of monitoring file.
    f.write(" -L %s"%nc_xsc_path)       # (Input) Pathname of input netCDF file containing the absorption coefficients for each pressure/temperature pair
    f.write(" -sm %s"%mapping_path)     # (Output) Mapping from wavenumber- to g-space and corresponding k-term weights
    f.write(" -np %s"%nproc)            # Doesn't seem to work for LbL calculation
    f.write(" \n ")
    
    f.close()
    os.chmod(exec_file_name,0o777)

    # Run
    print("    start")
    if not dry:
        with open(logging_path,'w') as hdl:  # execute using script so that the exact command is stored for posterity
            print("    please wait...")
            sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
        sp.check_returncode()

    time.sleep(1.0)
    print("    done writing to '%s'\n"%kcoeff_path)

    # Check logfile
    with open(logging_path,'r') as hdl:
        if "Execution ends" not in str(hdl.read()):
            print("-------------------------------------------")
            print("WARNING: An error may have occurred! Check logfile.")
            print("-------------------------------------------")

    return kcoeff_path

def calc_kcoeff_cia(alias:str, formula_A:str, formula_B:str, dnu:float, dry:bool=False):
    """Calculate k-coefficients for continuum absorption

    Takes netCDF file containing cross-sections as input. Outputs k-terms at the required p,t,nu ranges.

    Parameters
    ----------
    alias : str
        Alias of spectral file
    formula_A : str
        Formula of absorber A
    formula_B : str
        Formula of absorber B
    dnu : float
        Wavenumber integration step [m-1]. MUST MATCH LBL FILE.

    dry : bool
        Dry run?

    Returns 
    ----------
    str
        Path to file containing the new k-coefficients
    """

    # Parameters
    max_path = 1.0e1
    tol_type = 'b' 
    nproc = 30          # Number of processes
    nu_cutoff = 2500.0  # Line cutoff [m-1]

    # Re-order pair and check if valid
    p_in = [formula_A.strip(),formula_B.strip()]
    pair = get_cia_pair(p_in[0], p_in[1])
    if len(pair) == 0:
        return
    
    pair_ids = [utils.absorber_id[p] for p in pair]
    pair_str = "%s-%s"%(pair[0],pair[1])
    both_water = bool( (pair[0]=="H2O") and (pair[1]=="H2O"))
    print("Calculating k-coefficients for '%s' CIA for '%s'..."%(pair_str, alias))

    # Setup file (read) paths
    pt_cia       = os.path.join(utils.dirs["output"], "%s_pt_cia.dat"%alias)
    skel_path    = os.path.join(utils.dirs["output"], alias+"_skel.sf")
    check_files = [skel_path, pt_cia]
    
    if both_water:
        lbl_map_path  = os.path.join(utils.dirs["output"],"%s_H2O_map.nc"% alias)
        mt_ckd_296    = os.path.join( utils.dirs["socrates"], "data", "continua", "mt_ckd3p2_s296")
        mt_ckd_260    = os.path.join( utils.dirs["socrates"], "data", "continua", "mt_ckd3p2_s260")
        check_files.extend([lbl_map_path, mt_ckd_260, mt_ckd_296])
    else:
        db_cia = os.path.join(utils.dirs["cia"], pair_str+".cia")
        check_files.extend([db_cia])
        
    for f in check_files:
        if not os.path.exists(f):
            raise Exception("File not found: '%s'"%f)
    
    # Read skeleton file for bands...
    with open(skel_path,'r') as hdl:
        lines = hdl.readlines()
    nband = int(  str(lines[2]).split("=")[1].strip()  )
    band_edgesm = []
    block_idx:int = -999999999
    for l in lines:
        # We want block 1 data
        if "Band        Lower limit         Upper limit" in l:
            block_idx = 0 
        if (block_idx > 0) and ("*END" in l):
            break 
        
        # Read bands
        if (block_idx > 0):
            s = [float(ss.strip()) for ss in l.split()[1:]]
            # First edge
            if block_idx == 1:
                band_edgesm.append(s[0])  # Note that these are in units of [metres]
            # Upper edges
            band_edgesm.append(s[1])  # [metres]

        # Block index 
        block_idx += 1

    # Band range
    iband = [1, nband]

    # Setup file (write) paths
    kcoeff_path    = os.path.join(utils.dirs["output"],"%s_%s_cia.sf_k"%(alias,pair_str)); utils.rmsafe(kcoeff_path)
    monitor_path   = os.path.join(utils.dirs["output"],"%s_%s_mon.log"%(alias, pair_str)); utils.rmsafe(monitor_path)
    mapping_path   = os.path.join(utils.dirs["output"],"%s_%s_map.nc"% (alias, pair_str)); utils.rmsafe(mapping_path)
    logging_path   = os.path.join(utils.dirs["output"],"%s_%s.log"%    (alias, pair_str)); utils.rmsafe(logging_path)
 
    # Open executable file for writing
    exec_file_name = os.path.join(utils.dirs["output"],"%s_make_%s.sh"%(alias,pair_str)); utils.rmsafe(exec_file_name)
    f = open(exec_file_name, 'w+')

    #    Handle water self-broadening as a special case
    if both_water:

        # Limit band range for MT_CKD case
        ckd_bands = []  # list of allowed bands
        ckd_wlrange = [ 500.50e-9 , 0.01 ]  # Domain for MT_CKD, in metres
        for i in range(0,nband):
            b_lo = band_edgesm[i]      # short WL edge
            b_hi = band_edgesm[i+1]    # long WL edge
            if (ckd_wlrange[0] < b_lo) and (ckd_wlrange[1] > b_hi):  # if this band is entirely within MT_CKD's domain
                ckd_bands.append(i+1)

        iband = [ min(ckd_bands) , max(ckd_bands)] 
        iband_revrev = [ nband-iband[1]+1 , nband-iband[0]+1 ]  # doubly reversed (so it is printed the same as best_bands)

        print("    Using MT_CKD with band limits: " + str(iband_revrev))

        f.write("Ccorr_k")
        f.write(" -F %s"%pt_cia)
        f.write(" -R %d %d"%(iband[0], iband[1])) 
        f.write(" -c %.3f"%nu_cutoff)
        f.write(" -i %.3f"%dnu)
        f.write(" -ct %s %s %.3e"%(pair_ids[0], pair_ids[1], max_path))

        match tol_type:
            case 'n': f.write(" -n 10")         # Use this many k-terms
            case 't': f.write(" -t 1.0e-3")     # Calculate k-terms needed to keep RMS error in the transmission below this value
            case 'b': f.write(" -b 1.0e-3")     # Calculate k-terms according to where absorption scaling peaks, keeping the maximum transmission error below this value

        f.write(" -e %s %s"%(mt_ckd_296, mt_ckd_260))
        f.write(" -s %s"%skel_path)
        f.write(" +p")
        f.write(" -lk")
        f.write(" -o %s"%kcoeff_path)
        f.write(" -m %s"%monitor_path)
        f.write(" -L %s"%mapping_path)
        f.write(" -lm %s"%lbl_map_path) 
        f.write(" -np %s"%nproc) 
        f.write(" \n ")

        #   Ccorr_k -F $CONT_PT_FILE \
        # -R 1 400 -i 0.1 -ct 1 1 ${COL_H2OC} -t 5.0e-4 \
        # -e $CONT_H2O_S296 $CONT_H2O_S260 \
        # -s $skelfile +p -lk \
        # -o $sp_dir/h2o-h2o_lw_c -m $sp_dir/h2o-h2o_lw_cm \
        # -L $sp_dir/h2o-h2o_lw_clbl.nc \
        # -lw $sp_dir/h2o_lwf_l_map.nc \
        # > $sp_dir/h2o-h2o_lw_clog

    #    All other cases
    else:
        db_cia = os.path.join(utils.dirs["cia"], pair_str+".cia")

        print("    Using HITRAN CIA database")

        f.write("Ccorr_k")
        f.write(" -F %s"%pt_cia)
        f.write(" -CIA %s"%db_cia)
        f.write(" -R %d %d"%(iband[0], iband[1])) 
        f.write(" -i %.3f"%dnu)
        f.write(" -ct %s %s %.3e"%(pair_ids[0], pair_ids[1], max_path))

        match tol_type:
            case 'n': f.write(" -n 4")       
            case 't': f.write(" -t 1.0e-3")  
            case 'b': f.write(" -b 1.0e-3")  

        f.write(" -s %s"%skel_path)
        f.write(" +p")
        f.write(" -lk")
        f.write(" -o %s"%kcoeff_path)
        f.write(" -m %s"%monitor_path)
        f.write(" -L %s"%mapping_path)
        f.write(" -np %d"%nproc)
        f.write(" \n ")

    f.close()
    os.chmod(exec_file_name,0o777)

    print("    start")
    if not dry:
        with open(logging_path,'w') as hdl:  # execute using script so that the exact command is stored for posterity
            print("    please wait...")
            sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
        sp.check_returncode()

    time.sleep(1.0)
    print("    done writing to '%s'\n"%kcoeff_path)

    # Check logfile
    with open(logging_path,'r') as hdl:
        if "Execution ends" not in str(hdl.read()):
            print("-------------------------------------------")
            print("WARNING: An error may have occurred! Check logfile.")
            print("-------------------------------------------")

    return kcoeff_path


def calc_waterdroplets(alias:str, dry:bool=False):
    """Calculate water droplet scattering properties.

    Adapted from the SOCRATES tutorial and other code written by Ryan Boukrouche.

    Parameters
    ----------
    alias : str
        Alias of spectral file
    dry : bool
        Dry run?

    Returns 
    ----------
    str
        Path to scattering properties fit
    """

    # Parameters
    weighting_temperature = 250.0

    # Check that input files exist
    skel_path    = os.path.join(utils.dirs["output"], alias+"_skel.sf")
    drop_data    = os.path.join(utils.dirs["socrates"], "data", "cloud", "scatter_drop_type5")
    check_files = [skel_path]
    for f in check_files:
        if not os.path.exists(f):
            raise Exception("File not found: '%s'"%f)
        
    print("Calculating water droplet optical properties for '%s'..."%alias)
        
    # Output paths
    fit_path       = os.path.join(utils.dirs["output"],"%s_droplet.sct"%     alias); utils.rmsafe(fit_path)
    monitor_path   = os.path.join(utils.dirs["output"],"%s_droplet_mon.log"% alias); utils.rmsafe(monitor_path)
    logging_path   = os.path.join(utils.dirs["output"],"%s_droplet.log"%     alias); utils.rmsafe(logging_path)
    exec_file_name = os.path.join(utils.dirs["output"],"%s_make_droplet.sh"% alias); utils.rmsafe(exec_file_name)

    # Write command
    f = open(exec_file_name, 'w+')

    f.write("Cscatter_average ")
    f.write(" -s %s"%skel_path) # Skeleton spectral file
    f.write(" -P 1")            # Moments to be calculated
    f.write(" -t")              # Method for thick averaging
    f.write(" -p %.2f"%weighting_temperature)               # Planckian weighting, temperature [K]
    f.write(" -f 5 %s %s 1.e3"%(fit_path,monitor_path))     # Fit type (pade=5), output fit file, monitor file, density of material [kg m-3]
    f.write(" %s"%drop_data)    # (Input) Droplet scattering data
    f.write(" \n")

    f.close()
    os.chmod(exec_file_name,0o777)

    print("    start")
    if not dry:
        with open(logging_path,'w') as hdl:  # execute using script so that the exact command is stored for posterity
            print("    please wait...")
            sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
        sp.check_returncode()

    time.sleep(1.0)
    print("    done writing to '%s'\n"%fit_path)

    return fit_path


def assemble(alias:str, volatile_list:list, dry:bool=False):
    """Assemble final spectral file.

    Parameters
    ----------
    alias : str
        Alias of spectral file
    volatile_list : str
        List of volatiles

    dry : bool
        Dry run?

    Returns 
    ----------
    str
        Path to file
    """


    # <EXAMPLE>
    # 
    # echo 'Constructing spectral file'
    # prep_spec << EOF > ${specfile}_log 2>&1
    # $skelfile                 # skeleton file
    # n                         # don't overwrite
    # $specfile                 # output file
    # 6                         # add thermal emission
    # n                         #     no filter
    # t                         #     tabulated planck function
    # 60 540                    #     table range
    # 500                       #     table npoints
    # 5                         # add k-terms
    # $sp_dir/h2o_lwf_l         #     path to esft data
    # 5                         # add k-terms
    # y                         #     append
    # $sp_dir/co2_lw_l          #     path to esft data
    # 5                         # add k-terms
    # y                         #     append
    # $sp_dir/so2_lw_l          #     path to esft data
    # 19                        # add CIA 
    # $sp_dir/h2o-h2o_lw_c      #     path to esft data
    # 19                        # add CIA
    # y                         #     append
    # $sp_dir/co2-co2_lw_c      #     path to esft data
    # 10                        # add droplet parameters in each band.
    # 5                         #     droplet type
    # $sp_dir/fit_lw_drop5      #     path to fit file
    # 1.50000E-06 5.00000E-05   #     droplet parameters
    # 11                        # add aerosol parameters in each band
    # $sp_dir/sulphuric_lw.avg  #     ?
    # 12                        # add ice crystal parameters in each band
    # 8                         #     ?
    # $sp_dir/fit_lw_ice8       #     ?
    # -1                        # done
    # EOF
    #
    # </EXAMPLE>

    success = True

    # Check that files exist
    skel_path   = os.path.join(utils.dirs["output"], alias+"_skel.sf")
    for f in [skel_path]:
        if not os.path.exists(f):
            raise Exception("File not found: '%s'"%f)

    # Write script
    print("Assembling final spectral file for '%s'..."%alias)
    spec_path = os.path.join(utils.dirs["output"], alias+".sf"); utils.rmsafe(spec_path)
    logging_path   = os.path.join(utils.dirs["output"],"%s_final.log"%    alias); utils.rmsafe(logging_path)
    exec_file_name = os.path.join(utils.dirs["output"],"%s_make_final.sh"%alias); utils.rmsafe(exec_file_name)
    f = open(exec_file_name,'w+')

    #    point to input/output spectral files
    f.write("prep_spec <<EOF\n")
    f.write(skel_path + "\n")
    f.write("n \n")
    f.write("%s \n" % spec_path)

    #    add line absorption
    print("    line absorption: ", end='')
    for i,v in enumerate(volatile_list):
        print(v+" ", end='')
        lbl_path = os.path.join(utils.dirs["output"], "%s_%s_lbl.sf_k"%(alias, v))
        f.write("5 \n")
        if i > 0:
            f.write("y \n")
        f.write("%s \n"%lbl_path)
    print("")

    #    add CIA 
    print("    CIA: ", end='')
    cia_count = 0
    for i,p in enumerate(utils.cia_pairs):
        if ((p[0] in volatile_list) and (p[1] in volatile_list)) or (  (p[1] in volatile_list) and  (p[0] in volatile_list) ):
            pair_str = p[0]+"-"+p[1]
            print(pair_str+" ", end='')

            f.write("19 \n")
            if cia_count > 0:
                f.write("y \n")

            cia_path = os.path.join(utils.dirs["output"],"%s_%s_cia.sf_k"%(alias,pair_str))
            f.write("%s \n"%cia_path)

            cia_count += 1
    if cia_count == 0:
        print("(none)")
    else:
        print("")

    #    add water droplets
    print("    water droplets: ", end='')
    droplet_path = os.path.join(utils.dirs["output"],"%s_droplet.sct"%alias)
    if os.path.exists(droplet_path):
        
        f.write("10 \n")                        # Block 10
        f.write("5 \n")                         # Droplet type
        f.write("%s \n"%droplet_path)           # Fit data  
        f.write("1.50000E-06 5.00000E-05 \n")   # Pade fits

        print("scattering properties included")
    else:
        print("(none)")
        
    #    add aerosols
    print("    aerosols: ", end='')
    print("(none)")
        
    #    add ice
    print("    ice: ", end='')
    print("(none)")

    #    done
    f.write("-1 \n")
    f.write("EOF\n")
    f.write(" \n ")
    f.close()
    os.chmod(exec_file_name,0o777)

    # Execute script
    print("    start")
    if not dry:
        with open(logging_path,'w') as hdl:
            print("    please wait...")
            sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
        sp.check_returncode()

    print("    done writing to '%s' \n"%spec_path)


    # Check for NaN values
    with open(spec_path,'r') as hdl:
        if "NaN" in hdl.read():
            success = False
            print("-------------------------------------------")
            print("WARNING: Spectral file contains NaN values!")
            print("-------------------------------------------")

    # Calculate checksum
    if success:
        # spectral file
        chk_path = os.path.join(utils.dirs["output"], alias+".chk"); utils.rmsafe(chk_path)
        with open(chk_path,'w') as hdl:
            hdl.write("%s \n" % utils.checksum(spec_path))

        # lookup table
        chk_path = os.path.join(utils.dirs["output"], alias+".chk_k"); utils.rmsafe(chk_path)
        with open(chk_path,'w') as hdl:
            hdl.write("%s \n" % utils.checksum(spec_path+"_k"))

    return spec_path

