# Tools for handling exocross 'xsec' files

from glob import glob 
import os

import src.cross as cross
import src.utils as utils

linelists = ["ExoMol", "ExoAtom", "HITRAN", "HITEMP"]

def get_formula_path(formula:str):

    directory = os.path.join(utils.dirs["exocross"])

    # exocross derived from various linelists
    for s in linelists:
        dir = os.path.join(directory, formula, s)
        if os.path.exists(dir):
            return dir

    raise Exception("Formula '%s' not found in ExoCross directory! Check chem_dict in phys.py" % formula)


# List ExoCross xsec files in directory
def list_files(formula:str) -> list:
    directory = get_formula_path(formula)
    files = glob(directory+"/*.xsec*")
    if len(files) == 0:
        print("WARNING: No xsec files found in '%s'"%directory)
    return [os.path.abspath(f) for f in files]

def find_xsec_close(formula:str, p_aim:float, t_aim:float) -> str:
    """Search for ExoCross xsec file.

    Finds the ExoCross xsec file in the directory which most closely matches the target p,t values.

    Parameters
    ----------
    directory : str
        Directory containing xsec files
    p_aim : float
        Target pressure [bar]
    t_aim : float
        Target temperature [K]

    Returns
    -------
    str
        Absolute path to best xsec file
    """

    if (p_aim < 0) or (t_aim < 0):
        raise Exception("Target pressure and temperature must be positive values")
    
    directory = get_formula_path(formula)

    files = list_files(formula)
    count = len(files)
    if count == 0:
        raise Exception("Could not find any xsec files in '%s'" % directory)
    
    p_arr = []  # pressure
    t_arr = []  # temperature
    for f in files:
        temp = cross.xsec("", "exocross", f)
        temp.parse_name()
        p_arr.append(temp.p)
        t_arr.append(temp.t)

    i,d,p,t = utils.find_pt_close(p_arr, t_arr, p_aim, t_aim)
    print("Found xsec file with distance = %.3f%%" % d)

    return files[i]
