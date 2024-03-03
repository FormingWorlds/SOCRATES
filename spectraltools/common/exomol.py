# Tools for handling exomol files

from glob import glob 
import os

import common.cross as cross
import common.utils as utils

# List ExoMol sigma files in directory
def list_files(directory:str) -> list:
    files = glob(directory+"/*.sigma")
    if len(files) == 0:
        print("WARNING: No sigma files found in '%s'"%directory)
    return [os.path.abspath(f) for f in files]

def find_sigma_close(directory:str, p_aim:float, t_aim:float) -> str:
    """Search for ExoMol sigma file.

    Finds the ExoMol sigma file in the directory which most closely matches the target p,t values.

    Parameters
    ----------
    directory : str
        Directory containing sigma files
    p_aim : float
        Target pressure [bar]
    t_aim : float
        Target temperature [K]

    Returns
    -------
    str
        Absolute path to best sigma file
    """

    if (p_aim < 0) or (t_aim < 0):
        raise Exception("Target pressure and temperature must be positive values")

    files = list_files(directory)
    count = len(files)
    if count == 0:
        raise Exception("Could not find any sigma files in '%s'" % directory)
    
    print("WARNING: ExoMol spectra are calculated at zero pressure, so 'best' value will not be ideal")
    
    p_arr = []  # pressure
    t_arr = []  # temperature
    for f in files:
        temp = cross.xsec("", "exomol", f)
        temp.parse_sigmaname()
        p_arr.append(temp.p)
        t_arr.append(temp.t)

    i,d,p,t = utils.find_pt_close(p_arr, t_arr, p_aim, t_aim)
    print("Found sigma file with distance = %.3f%%" % d)

    return files[i]
