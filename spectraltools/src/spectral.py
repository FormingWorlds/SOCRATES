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
        2 = logspace, but using a single band to cover the longest wavelengths \n

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

    # Validate
    if len(nu_arr) < 2:
        raise Exception("Wavenumber array is too short")
    if not utils.is_ascending(nu_arr):
        raise Exception("Wavenumber array is not strictly ascending")
    if nband < 1:
        raise Exception("There must be at least one band")
    if nband > len(nu_arr)-2:
        raise Exception("Too many bands! (%d requested)"%nband)
    
    # Check range
    numin = max(nu_arr[0], floor)
    numax = nu_arr[-1]
    lognumin = np.log10(numin)
    lognumax = np.log10(numax)

    # Simple case
    if nband == 1:
        return [numin, numax]
    
    # Other cases ...

    vlong_cutoff = 100.0 # [cm-1] Value where the "very long wavelengths" region starts.
    if (numin > vlong_cutoff) and (method == 2):
        method = 1 
    
    nedges = nband+1
    match method:
        case 0:
            bands = np.linspace(numin, numax, nedges)
        case 1: 
            bands = np.logspace(lognumin, lognumax, nedges)
        case 2:
            bands = np.array([numin, vlong_cutoff])
            bands = np.append(bands, np.logspace(np.log10(vlong_cutoff) , lognumax , nedges-1 )[1:])
        case _:
            raise Exception("Invalid band selection method (%d)"%method)

    # Ensure that the band edges exist in the nu_arr
    bands_out = []
    for be in bands:
        bands_out.append(utils.get_closest(be, nu_arr))
    bands_out = np.array(bands_out)

    if not utils.is_unique(bands_out):
        print(utils.get_arr_as_str(bands_out))
        raise Exception("Best band edges are not unique! Try a different method, or increase the resolution")
    if not utils.is_ascending(bands_out):
        print(utils.get_arr_as_str(bands_out))
        raise Exception("Best band edges are ascending! Try a different method, or increase the resolution")

    # print("Best bands: " + utils.get_arr_as_str(bands_out))
    return bands_out



def create_skeleton(alias:str, p_points:np.ndarray, t_points:np.ndarray, volatile_list:list, band_edges:list):
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

    T_grid = t_points
    P_grid = p_points * 1.0e5  # bar to Pa
    
    print("    T_grid [K]  (n=%d): "%len(T_grid) + utils.get_arr_as_str(T_grid))
    print("    P_grid [Pa] (n=%d): "%len(P_grid) + utils.get_arr_as_str(P_grid))

    # Generate P-T files to be read by Ccorr script
    pt_lbl_file = open(pt_lbl, "w+")
    pt_lbl_file.write('*PTVAL' + '\n')
    for prs in np.unique(P_grid):
        line = ""
        line += "%.5e"%prs 
        for t in np.unique(T_grid):
            line +=" %.5e"%t 
        line += "\n" 
        pt_lbl_file.write(line)
    pt_lbl_file.write('*END' + '\n')
    pt_lbl_file.close()
    
    T_grid_as_str = str(" ").join(["%.2f"%t for t in T_grid])
    pt_cia_file = open(pt_cia, "w+")
    pt_cia_file.write('*PTVAL' + '\n')
    pt_cia_file.write(T_grid_as_str + '\n')
    pt_cia_file.write('*END' + '\n')
    pt_cia_file.close()

    # Open file to produce bash script
    f = open(exec_file_name, "w+")

    # Write skeleton spectral file using prep_spec utility
    f.write('prep_spec <<EOF'+ '\n')
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
        f.write("%.2f %.2f \n"%(band_edges[i], band_edges[i-1]))

    # Set absorbers in each band to zero for now
    f.write("0*%d\n"%nband)

    # Set continua in each band to zero for now
    f.write("0*%d\n"%nband)

    # Exclude no regions
    f.write("n \n")

    # Close prep_spec
    f.write("-1 \n")
    f.write("EOF \n")
    f.write(" \n ")
    f.close()
    os.chmod(exec_file_name,0o777)

    logfile = os.path.join(utils.dirs["output"], "%s_skel.log"%alias); utils.rmsafe(logfile)
    with open(logfile,'w') as hdl:
        sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
    sp.check_returncode()

    time.sleep(1.0)
    print("    done")
    return skel_path

def calc_kcoeff_lbl(alias:str, formula:str, nc_xsc_path:str, nband:int):
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
    max_path = 1.0e4
    tol_type = 'b'

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
        case 'n': f.write(" -n 4")          # Use this many k-terms
        case 't': f.write(" -t 1.0e-2")     # Calculate k-terms needed to keep RMS error in the transmission below this value
        case 'b': f.write(" -b 5.0e-4")     # Calculate k-terms according to where absorption scaling peaks, keeping the maximum transmission error below this value

    f.write(" -s %s"%skel_path)         # (Input) Path to skeleton spectral file (used to provide the spectral bands - will not be overwritten)
    f.write(" +p")                      # Planckian Weighting
    f.write(" -lk")                     # A look-up table will be used for the pressure/temperature scaling
    f.write(" -o %s"%kcoeff_path)       # Output file, holding the correlated-k terms for each pressure/temperature
    f.write(" -m %s"%monitor_path)      # (Output) Pathname of monitoring file.
    f.write(" -L %s"%nc_xsc_path)       # (Input) Pathname of input netCDF file containing the absorption coefficients for each pressure/temperature pair
    f.write(" -sm %s"%mapping_path)     # (Output) Mapping from wavenumber- to g-space and corresponding k-term weights
    f.write(" \n ")
    
    f.close()
    os.chmod(exec_file_name,0o777)

    print("    start")
    with open(logging_path,'w') as hdl:  # execute using script so that the exact command is stored for posterity
        sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
    sp.check_returncode()

    time.sleep(1.0)
    print("    done")
    return kcoeff_path

def calc_kcoeff_cia(alias:str, formula_A:str, formula_B:str, nband:int):
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
    nc_xsc_path : str
        Input netCDF file containing cross-section data for range of p,t,nu
    nband : int
        Number of bands (THIS MUST MATCH THE SKELETON FILE)

    """

    # Parameters
    max_path = 1.0e4
    tol_type = 't' 
    dnu = 0.1           # Frequency increment [m-1]
    nproc = 20          # Number of processes
    nu_cutoff = 2500.0  # Line cutoff [m-1]

    # Re-order pair and check if valid
    p_in = [formula_A.strip(),formula_B.strip()]
    is_valid = False
    for p_check in utils.cia_pairs:
        # Is valid
        if p_in == p_check:
            pair = p_in
            is_valid = True
            break 
        # Is valid, but swapped
        if [p_in[1], p_in[0]] == p_check:
            pair = [p_in[1], p_in[0]]
            is_valid = True
            break
    if not is_valid:
        raise Exception("Invalid CIA pairing " + str(p_in))
    
    pair_ids = [utils.absorber_id[p] for p in pair]
    pair_str = "%s-%s"%(pair[0],pair[1])
    both_water = bool( (pair[0]=="H2O") and (pair[1]=="H2O"))
    print("Calculating k-coefficients for '%s' CIA for '%s'..."%(pair_str, alias))

    # Setup file (read) paths
    pt_cia       = os.path.join(utils.dirs["output"], "%s_pt_cia.dat"%alias)
    skel_path    = os.path.join(utils.dirs["output"], alias+"_skel.sf")
    check_files = [skel_path, pt_cia]
    
    if both_water:
        lbl_path   = os.path.join(utils.dirs["output"],"%s_H2O_lbl.sf_k"%alias)
        mt_ckd_296 = os.path.join( utils.dirs["cia"] , "mt_ckd_v3.0_s296")
        mt_ckd_260 = os.path.join( utils.dirs["cia"] , "mt_ckd_v3.0_s260")
        check_files.extend([lbl_path, mt_ckd_260, mt_ckd_296])
    else:
        db_cia = os.path.join(utils.dirs["cia"], pair_str+".cia")
        check_files.extend([db_cia])
        
    for f in check_files:
        if not os.path.exists(f):
            raise Exception("File not found: '%s'"%f)

    # Setup file (write) paths
    kcoeff_path  = os.path.join(utils.dirs["output"],"%s_%s_cia.sf_k"%(alias,pair_str)); utils.rmsafe(kcoeff_path)
    monitor_path = os.path.join(utils.dirs["output"],"%s_%s_mon.log"%(alias, pair_str)); utils.rmsafe(monitor_path)
    mapping_path = os.path.join(utils.dirs["output"],"%s_%s_map.nc"% (alias, pair_str)); utils.rmsafe(mapping_path)
    logging_path = os.path.join(utils.dirs["output"],"%s_%s.log"%    (alias, pair_str)); utils.rmsafe(logging_path)
 
    # Open executable file for writing
    exec_file_name = os.path.join(utils.dirs["output"],"%s_make_%s.sh"%(alias,pair_str)); utils.rmsafe(exec_file_name)
    f = open(exec_file_name, 'w+')

    #    Handle water self-broadening as a special case
    if both_water:
        f.write("Ccorr_k")
        f.write(" -F %s"%pt_cia)
        f.write(" -R 1 %d"%nband) 
        f.write(" -c %.3f"%nu_cutoff)
        f.write(" -i %.3f"%dnu)
        f.write(" -ct %d %d %.3e"%(pair_ids[0], pair_ids[1], max_path))

        match tol_type:
            case 'n': f.write(" -n 4")          # Use this many k-terms
            case 't': f.write(" -t 1.0e-3")     # Calculate k-terms needed to keep RMS error in the transmission below this value
            case 'b': f.write(" -b 5.0e-4")     # Calculate k-terms according to where absorption scaling peaks, keeping the maximum transmission error below this value

        f.write(" -e %s %s"%(mt_ckd_296, mt_ckd_260))
        f.write(" -k")
        f.write(" -s %s"%skel_path)
        f.write(" +p")
        f.write(" -lk")
        f.write(" -o %s"%kcoeff_path)
        f.write(" -m %s"%monitor_path)
        f.write(" -L %s"%mapping_path)
        f.write(" -lw %s"%lbl_path) 
        f.write(" \n ")

    #    All other cases
    else:
        db_cia = os.path.join(utils.dirs["cia"], pair_str+".cia")

        f.write("Ccorr_k")
        f.write(" -F %s"%pt_cia)
        f.write(" -CIA %s"%db_cia)
        f.write(" -R 1 %d"%nband)
        f.write(" -i %.3f"%dnu)
        f.write(" -ct %d %d %.3e"%(pair_ids[0], pair_ids[1], max_path))

        match tol_type:
            case 'n': f.write(" -n 4")       
            case 't': f.write(" -t 1.0e-2")  
            case 'b': f.write(" -b 5.0e-4")  

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
    with open(logging_path,'w') as hdl:  # execute using script so that the exact command is stored for posterity
        sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
    sp.check_returncode()

    time.sleep(1.0)
    print("    done")
    return kcoeff_path


def assemble(alias:str, volatile_list:list):



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
    # 5                         #     ?
    # $sp_dir/fit_lw_drop5      #     ?
    # 1.50000E-06 5.00000E-05   #     ?
    # 11                        # add aerosol parameters in each band
    # $sp_dir/sulphuric_lw.avg  #     ?
    # 12                        # add ice crystal parameters in each band
    # 8                         #     ?
    # $sp_dir/fit_lw_ice8       #     ?
    # -1                        # done
    # EOF
    #
    # </EXAMPLE>

    # Parameters
    planck_npoints = 2000
    planck_range   = (200.0, 4000.0)

    # Check that files exist
    skel_path   = os.path.join(utils.dirs["output"], alias+"_skel.sf")
    for f in [skel_path]:
        if not os.path.exists(f):
            raise Exception("File not found: '%s'"%f)

    # Write script
    print("Assembling final spectral file for '%s'..."%alias)
    spec_path = os.path.join(utils.dirs["output"], alias+"_final.sf"); utils.rmsafe(spec_path)
    logging_path   = os.path.join(utils.dirs["output"],"%s_final.log"%    alias); utils.rmsafe(logging_path)
    exec_file_name = os.path.join(utils.dirs["output"],"%s_make_final.sh"%alias); utils.rmsafe(exec_file_name)
    f = open(exec_file_name,'w+')

    #    point to input/output spectral files
    f.write('prep_spec <<EOF'+ '\n')
    f.write(skel_path + '\n')
    f.write('n \n')
    f.write('%s \n' % spec_path)

    #    add thermal emission
    f.write('6 \n')
    f.write('n      \n')
    f.write('t      \n')
    f.write('%.2f %.2f \n'%planck_range)
    f.write('%d    \n'%planck_npoints)

    #    add line absorption
    for i,v in enumerate(volatile_list):
        lbl_path = os.path.join(utils.dirs["output"], "%s_%s_lbl.sf_k"%(alias, v))
        f.write('5 \n')
        if i > 0:
            f.write('y \n')
        f.write('%s \n'%lbl_path)

    #    add CIA 

    #    add droplets
        
    #    add aerosols
        
    #    add ice

    #    done
    f.write('-1'+ '\n')
    f.write('EOF'+ '\n')
    f.close()
    os.chmod(exec_file_name,0o777)

    # Execute script
    print("    start")
    with open(logging_path,'w') as hdl:
        sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
    sp.check_returncode()

    print("    done")

