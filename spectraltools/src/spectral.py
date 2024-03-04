# Tools for handling socrates spectral files

import numpy as np
import os, subprocess
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
    

def create_skeleton(name:str, p_points:np.ndarray, t_points:np.ndarray, volatile_list:list, band_edges:list):
    """Create skeleton spectral file.

    Creates a spectral file with meta-data. Does not calculate k-terms or other physical properties.

    Parameters
    ----------
    name : str
        Name of spectral file
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

    print("Creating skeleton spectral file '%s'"%name)
    skel_path = os.path.join(utils.dirs["output"], name+"_skel.sf")
    utils.rmsafe(skel_path)
 
    # Sanitise bands
    if not utils.is_ascending(band_edges):
        raise Exception("Band edges must be strictly ascending")
    numin = band_edges[0]
    numax = band_edges[-1]
    nband = len(band_edges)-1
    print("    number of bands: %d"%nband)
    print("    numin, numax: %.2f , %.2f cm-1"%(numin, numax))

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
    pt_lbl = os.path.join(utils.dirs["output"], "%s_pt_lbl.dat"%name); utils.rmsafe(pt_lbl)
    pt_cia = os.path.join(utils.dirs["output"], "%s_pt_cia.dat"%name); utils.rmsafe(pt_cia)

    # File name of bash execution script to be written
    exec_file_name = os.path.join(utils.dirs["output"],"%s_make_skel.sh"%name)
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
    pt_cia_file.write('*PTVAL' + '\n')  # CHECK THIS??
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

    # Count total number of "continua"
    # (count number of participating CIA pairs [self+foreign])
    counter_continua = 0
    if "H2O" in volatile_list:
        counter_continua += 1
    if "CO2" in volatile_list:
        counter_continua += 1
    if "CH4" in volatile_list:
        counter_continua += 1
    if "O2" in volatile_list:
        counter_continua += 1
    if "N2" in volatile_list:
        counter_continua += 1
    if "H2" in volatile_list:
        counter_continua += 1
    if ("CO2" in volatile_list) and ("CH4" in volatile_list):
        counter_continua += 1
    if ("CO2" in volatile_list) and ("H2" in volatile_list):
        counter_continua += 1
    if ("CO2" in volatile_list) and ("He" in volatile_list):
        counter_continua += 1
    if ("CH4" in volatile_list) and ("He" in volatile_list):
        counter_continua += 1
    if ("O2" in volatile_list) and ("CO2" in volatile_list):
        counter_continua += 1
    if ("O2" in volatile_list) and ("N2" in volatile_list):
        counter_continua += 1
    if ("N2" in volatile_list) and ("H2O" in volatile_list):
        counter_continua += 1
    if ("N2" in volatile_list) and ("CH4" in volatile_list):
        counter_continua += 1
    if ("N2" in volatile_list) and ("H2" in volatile_list):
        counter_continua += 1
    if ("N2" in volatile_list) and ("He" in volatile_list):
        counter_continua += 1
    if ("H2" in volatile_list) and ("CH4" in volatile_list):
        counter_continua += 1
    if ("H2" in volatile_list) and ("He" in volatile_list):
        counter_continua += 1
    f.write(str(counter_continua) + '\n')
    print("    number of continua:", counter_continua)

    ### Set CIA pairs
    ##   Self:
    # H2O-H2O
    if "H2O" in volatile_list:
        f.write('1'  + ' ')  # H2O-
        f.write('1'  + '\n')  # -H2O
    # CO2-CO2
    if "CO2" in volatile_list:
        f.write('2'  + ' ')  # CO2-
        f.write('2'  + '\n')  # -CO2
    # CH4-CH4
    if "CH4" in volatile_list:
        f.write('6'  + ' ')  # CH4-
        f.write('6'  + '\n')  # -CH4
    # O2-O2
    if "O2" in volatile_list:
        f.write('7'  + ' ')  # O2-
        f.write('7'  + '\n')  # -O2
    # N2-N2
    if "N2" in volatile_list:
        f.write('13' + ' ')  # N2-
        f.write('13' + '\n')  # -N2
    # H2-H2
    if "H2" in volatile_list:
        f.write('23' + ' ')  # H2-
        f.write('23' + '\n')  # -H2

    ##   Foreign:
    # CO2-CH4
    if ("CO2" in volatile_list) and ("CH4" in volatile_list):
        f.write('2'  + ' ')  # CO2-
        f.write('6'  + '\n')  # -CH4
    # CO2-H2
    if ("CO2" in volatile_list) and ("H2" in volatile_list):
        f.write('2'  + ' ')  # CO2-
        f.write('23' + '\n')  # -H2
    # CO2-He
    if ("CO2" in volatile_list) and ("He" in volatile_list):
        f.write('2'  + ' ')  # CO2-
        f.write('24' + '\n')  # -He
    # CH4-He
    if ("CH4" in volatile_list) and ("He" in volatile_list):
        f.write('6'  + ' ')  # CH4-
        f.write('24' + '\n')  # -He
    # O2-CO2
    if ("O2" in volatile_list) and ("CO2" in volatile_list):
        f.write('7'  + ' ')  # O2-
        f.write('2'  + '\n')  # -CO2
    # O2-N2
    if ("O2" in volatile_list) and ("N2" in volatile_list):
        f.write('7'  + ' ')  # O2-
        f.write('13' + '\n')  # -N2
    # N2-H2O
    if ("N2" in volatile_list) and ("H2O" in volatile_list):
        f.write('13' + ' ')  # N2-
        f.write('1'  + '\n')  # -H2O
    # N2-CH4
    if ("N2" in volatile_list) and ("CH4" in volatile_list):
        f.write('13' + ' ')  # N2-
        f.write('6'  + '\n')  # -CH4
    # N2-H2
    if ("N2" in volatile_list) and ("H2" in volatile_list):
        f.write('13' + ' ')  # N2-
        f.write('23' + '\n')  # -H2
    # N2-He
    if ("N2" in volatile_list) and ("He" in volatile_list):
        f.write('13' + ' ')  # N2-
        f.write('24' + '\n')  # -He
    # H2-CH4
    if ("H2" in volatile_list) and ("CH4" in volatile_list):
        f.write('23' + ' ')  # H2-
        f.write('6'  + '\n')  # -CH4
    # H2-He
    if ("H2" in volatile_list) and ("He" in volatile_list):
        f.write('23' + ' ')  # H2-
        f.write('24' + '\n')  # -He

    # Set number of aerosols
    f.write('0'+ '\n')

    # Set bands manually (in reverse order, since they'll be converted to wavelength)
    f.write('c'+ '\n')
    for i in range(nband,-1,-1):
        f.write("%.2f %.2f \n"%(band_edges[i], band_edges[i-1]))

    # Set absorbers in each band to zero for now
    f.write("0*%d\n"%nband)

    # Set continua in each band to zero for now
    f.write("0*%d\n"%nband)

    # Exclude no regions
    f.write('n'+ '\n')

    # Close prep_spec
    f.write('-1'+ '\n')
    f.write('EOF'+ '\n')
    f.close()
    os.chmod(exec_file_name,0o777)

    logfile = os.path.join(utils.dirs["output"], "%s_skel.log"%name); utils.rmsafe(logfile)
    with open(logfile,'w') as hdl:
        sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
    sp.check_returncode()

    print("    done")
    return skel_path

def calc_kcoeff(name:str, formula:str, nc_xsc_path:str, nband:int):

    print("Calculating k-coefficients for '%s' in '%s'..."%(formula, name))

    # Parameters
    max_path = 1.0e4
    tol_type = 'b'

    # Check that files exist
    skel_path   = os.path.join(utils.dirs["output"], name+"_skel.sf")
    pt_lbl      = os.path.join(utils.dirs["output"], "%s_pt_lbl.dat"%name)
    pt_cia      = os.path.join(utils.dirs["output"], "%s_pt_cia.dat"%name)
    for f in [nc_xsc_path, skel_path, pt_lbl, pt_cia]:
        if not os.path.exists(f):
            raise Exception("File not found: '%s'"%f)
        
    formula = formula.strip()

    kcoeff_path  = os.path.join(utils.dirs["output"],"%s_%s_kco.sfk"%(name,formula)); utils.rmsafe(kcoeff_path)
    monitor_path = os.path.join(utils.dirs["output"],"%s_%s_mon.log"%(name,formula)); utils.rmsafe(monitor_path)
    mapping_path = os.path.join(utils.dirs["output"],"%s_%s_map.nc"% (name,formula)); utils.rmsafe(mapping_path)
    logging_path = os.path.join(utils.dirs["output"],"%s_%s.log"%    (name,formula)); utils.rmsafe(logging_path)

    # Open executable file for writing
    exec_file_name = os.path.join(utils.dirs["output"],"make_sfk_%s_%s.sh"%(name,formula)); utils.rmsafe(exec_file_name)
    f = open(exec_file_name, 'w+')

    f.write("Ccorr_k")
    f.write(" -F %s"%pt_lbl)       # (Input) Pathname of file containing pressures and temperatures at which to calculate coefficients. 
    f.write(" -R 1 %d"%nband)       # The range of spectral bands to be used 
    f.write(" -l 1 %.3e"%max_path)  # Generate line absorption data. gas is the type number (identifier) of the gas to be considered. max−path is the maximum absorptive pathlength (kg/m2) for the gas

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
    
    f.close()
    os.chmod(exec_file_name,0o777)

    print("    start")
    with open(logging_path,'w') as hdl:
        sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)
    sp.check_returncode()

    print("    done")

    # Ccorr_k -F ${GAS_DATA_DIR}/${PT_FILE} \
    #   -R 1 400 -l 1 ${COL_MASS_K_H2O} -b 5.0e-4 \
    #   -s $skelfile +p -lk \
    #   -o $sp_dir/h2o_lwf_l -m $sp_dir/h2o_lwf_lm \
    #   -L $H2O_LBL_LWF \
    #   -sm $sp_dir/h2o_lwf_l_map.nc \
    #    > $sp_dir/h2o_lwf_log

