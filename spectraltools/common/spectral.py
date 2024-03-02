# Tools for handling socrates spectral files

import numpy as np
import os, subprocess
import common.utils as utils

def create_skeleton(spfile:str, p_points:np.ndarray, t_points:np.ndarray, volatile_list:list, numin:float, numax:float, dnu:float):

    print("Creating skeleton spectral file")
    utils.rmsafe(spfile)
 
    # Sanitise bands
    numin = max(numin, 1.0)
    band_limits = np.arange(numin, numax+dnu, dnu)
    nband = len(band_limits)-1
    print("    number of bands: %d"%nband)

    # Sanitise volatiles 
    volatile_list_unique = list(set(volatile_list))
    volatile_list = []
    for v in volatile_list_unique:
        v = str(v).strip()
        if v not in list(utils.absorber_id.keys()):
            raise Exception("Volatile %s is not supported by SOCRATES"%v)
        volatile_list.append(v)
    nvols = len(volatile_list)
    print("    included volatiles: " + str(" ").join(volatile_list))

    # P-T grids for LbL and CIA data
    pt_lbl = os.path.join(utils.dirs["output"], "pt_grid_lbl.dat"); utils.rmsafe(pt_lbl)
    pt_cia = os.path.join(utils.dirs["output"], "pt_grid_cia.dat"); utils.rmsafe(pt_cia)

    # File name of bash execution script to be written
    exec_file_name = os.path.join(utils.dirs["output"],"recent_sp_skel.sh")
    utils.rmsafe(exec_file_name)

    T_grid = t_points
    P_grid = p_points * 1.0e5  # bar to Pa
    
    print("    T_grid [K]  (n=%d): "%len(T_grid) + " " + str(T_grid))
    print("    P_grid [Pa] (n=%d): "%len(P_grid) + " " + str(P_grid))

    # Generate P-T files to be read by Ccorr script
    pt_lbl_file = open(pt_lbl, "w+")
    pt_lbl_file.write('*PTVAL' + '\n')
    for prs in P_grid:
        line = ""
        line += "%.5e"%prs 
        for t in T_grid:
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
    f.write(spfile + '\n')

    # Set number of bands
    f.write("%d \n"%nband)

    # Set total number of absorbers 
    # (both LbL- and CIA-only ones, count all uncommented, individual molecules below)
    f.write("%d \n"%nvols)
    print("    number of volatiles: %d"%nvols)
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

    # Set bands by range
    f.write('r'+ '\n')
    f.write("c %.2f %.2f %.2f \n"%(numin, numax, dnu))

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

    logfile = os.path.join(utils.dirs["output"], "recent_sp_skel.log"); utils.rmsafe(logfile)
    with open(logfile,'w') as hdl:
        sp = subprocess.run(["bash",exec_file_name], stdout=hdl, stderr=hdl)

