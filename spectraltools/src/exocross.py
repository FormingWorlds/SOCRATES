# Tools for handling exocross 'xsec' files

import logging
from glob import glob
import os

import src.cross as cross
import src.utils as utils

log = logging.getLogger("fwl."+__name__)

linelists = ["ExoMol", "ExoAtom", "HITRAN", "HITEMP"]

def get_formula_path(formula:str, quiet=True):

    directory = os.path.join(utils.dirs["exocross"])

    # exocross derived from various linelists - use the first one found, in
    # priority order, but warn if more than one exists so the choice is visible
    found = []
    for s in linelists:
        dir = os.path.join(directory, formula, s)
        if os.path.exists(dir):
            found.append((s, dir))

    if len(found) == 0:
        raise Exception("Formula '%s' not found in ExoCross directory! Check chem_dict in phys.py" % formula)

    if len(found) > 1 and not quiet:
        log.warning("    multiple ExoCross linelists found for '%s'; using '%s'", formula, found[0][0])

    return found[0][1]


# List ExoCross xsec files in directory
def list_files(formula:str, quiet=False) -> list:
    directory = get_formula_path(formula, quiet=quiet)
    files = glob(directory+"/*.xsec*")
    if len(files) == 0:
        log.warning("No xsec files found in '%s'", directory)
    return [os.path.abspath(f) for f in files]

def find_xsec_close(formula:str, p_aim:float, t_aim:float, quiet=True) -> str:
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

    files = list_files(formula, quiet=True)
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
    if not quiet:
        log.info("Found xsec file (p=%.2e bar, t=%.2f K) with distance = %.3f%%", p, t, d)

    return files[i]
