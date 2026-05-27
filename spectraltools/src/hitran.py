# Tools for processing HITRAN files

# Import system libraries
from glob import glob
import os

# Import files
import src.cross as cross
import src.utils as utils

def get_formula_path(formula:str):
    directory = os.path.join(utils.dirs["hitran"], formula)
    if not os.path.exists(directory):
        raise Exception("Formula '%s' not found in HITRAN directory! Check chem_dict in phys.py" % formula)
    return directory

# List HITRAN xsc files in directory
def list_files(formula:str) -> list:
    directory = get_formula_path(formula)
    files = glob(directory+"/*.xsc")
    if len(files) == 0:
        print("WARNING: No xsc files found in '%s'"%directory)
    return [os.path.abspath(f) for f in files]

def find_xsc_close(formula:str, p_aim:float, t_aim:float) -> str:
    """Search for HITRAN xsc file.

    Finds the HITRAN xsc file in the directory which most closely matches the target p,t values.

    Parameters
    ----------
    formula : str
        Formula name (e.g. "H2O")
    p_aim : float
        Target pressure [bar]
    t_aim : float
        Target temperature [K]

    Returns
    -------
    str
        Absolute path to best xsc file
    """

    if (p_aim < 0) or (t_aim < 0):
        raise Exception("Target pressure and temperature must be positive values")

    directory = get_formula_path(formula)
    files = list_files(formula)
    count = len(files)
    if count == 0:
        raise Exception("Could not find any xsc files in '%s'" % directory)
    
    p_arr = []  # pressure
    t_arr = []  # temperature
    for f in files:
        temp = cross.xsec("", "hitran", f)
        temp.read(UV=False)
        p_arr.append(temp.p)
        t_arr.append(temp.t)

    i,d,p,t = utils.find_pt_close(p_arr, t_arr, p_aim, t_aim)
    print("Found xsc file with distance = %.3f%%" % d)

    return files[i]