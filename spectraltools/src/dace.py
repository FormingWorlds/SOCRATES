# Tools for processing DACE files

# Import system libraries
from glob import glob
import numpy as np
import os

# Import files
import src.cross as cross
import src.utils as utils

# List DACE bin files in directory
def list_files(directory:str) -> list:
    files = glob(directory+"/"+"Out*.bin")
    if len(files) == 0:
        print("WARNING: No bin files found in '%s'"%directory)
    return [os.path.abspath(f) for f in files]

def find_bin_close(directory:str, p_aim:float, t_aim:float, quiet=False) -> str:
    """Search for DACE bin file.

    Finds the DACE bin file in the directory which most closely matches the target p,t values.

    Parameters
    ----------
    directory : str
        Directory containing bin files
    p_aim : float
        Target pressure [bar]
    t_aim : float
        Target temperature [K]

    Returns
    -------
    list
        List of ranked closest bin files (length=rank)
    """

    if (p_aim < 0) or (t_aim < 0):
        raise Exception("Target pressure and temperature must be positive values")

    files = list_files(directory)
    count = len(files)
    if count == 0:
        raise Exception("Could not find any bin files in '%s'" % directory)
    
    # Read all files
    p_arr = []  # pressure
    t_arr = []  # temperature
    for f in files:
        temp = cross.xsec("", "dace", f)
        temp.parse_binname()
        p_arr.append(temp.p)
        t_arr.append(temp.t)

    # Find bin
    i,d,p,t = utils.find_pt_close(p_arr, t_arr, p_aim, t_aim)
    if not quiet:
        print("Found bin file with distance = %.3f%%  :  p=%.2e bar, t=%.2f K" % (d,p,t))

    return files[i]

# List the p,t values across all BIN files (f) in the directory
def list_all_ptf(directory:str):
    files = list_files(directory)

    all_p = []
    all_t = []
    all_f = []
    for f in files:
        x = cross.xsec("", "dace", f)
        x.parse_binname()
        all_p.append(x.p)
        all_t.append(x.t)
        all_f.append(f)
    return all_p, all_t, all_f


def get_pt(directory:str, p_targets:list=[], t_targets:list=[]):
    """Get p,t points covered by DACE bin files within a given directory.

    The p,t arrays will be sorted in ascending order, pressure first.
    Also returns the file paths, for them to be read fully later.

    Parameters
    ----------
    directory : str
        Directory containing bin files

    Returns
    -------
    np.ndarray
        pressures [bar]
    np.ndarray 
        temperatures [K]
    list 
        file paths which map to these p,t values
    """

    print("Mapping p,t points")

    all_p, all_t, all_f = list_all_ptf(directory)
    all_n = len(all_f)

    # Unique P,T values
    unique_p = sorted(list(set(all_p)))
    unique_t = sorted(list(set(all_t)))

    # Find best temperatures
    selected_t = []
    if (len(t_targets) >= len(unique_t)) or (len(t_targets) == 0):
        selected_t = unique_t[:]
    else:
        use_t = []
        search_t = unique_t[:]
        for t in t_targets:
            i = utils.get_closest_idx(t, search_t)
            selected_t.append(search_t[i])
            search_t.pop(i)

    # Find best pressures
    selected_p = []
    if (len(p_targets) >= len(unique_p)) or (len(p_targets) == 0):
        selected_p = unique_p[:]
    else:
        use_p = []
        search_p = unique_p[:]
        for p in p_targets:
            i = utils.get_closest_idx(p, search_p)
            selected_p.append(search_p[i])
            search_p.pop(i)
    
    # Flatten p,t points
    use_t = []
    use_p = []
    for p in selected_p:
        for t in selected_t:
            use_t.append(t)
            use_p.append(p)

    use_t = np.array(use_t, dtype=float)
    use_p = np.array(use_p, dtype=float)

    use_n = len(use_p)

    # Sort points into the correct p,t order, dropping duplicates
    out_p = []
    out_t = []
    for p in unique_p:     #  for all unique p
        for t in unique_t: #  for all unique t
            for i in range(use_n):  # for all selected points
                if np.isclose(use_p[i], p) and np.isclose(use_t[i], t): # select this point?

                    # Check if duplicate
                    duplicate = False 
                    for j in range(len(out_p)):
                        if (p == out_p[j]) and (t == out_t[j]):
                            duplicate = True
                            break
                    
                    # Add to output array (if not a duplicate)
                    if not duplicate:
                        out_p.append(use_p[i])
                        out_t.append(use_t[i])
                        break 

    # Warn on dropped values
    out_n = len(out_p)
    lost = abs(out_n - use_n)
    if lost > 0:
        print("WARNING: Duplicate values dropped from p,t grid (dropped count = %d)"%lost)

    # Map to files
    atol = 1.0e-8
    out_f = []
    
    for i in range(all_n):
        p = all_p[i]
        t = all_t[i]
        for j in range(out_n):
            if np.isclose(out_p[j], p, atol=atol) and np.isclose(out_t[j], t, atol=atol):
                out_f.append(all_f[i])
                break 

    if (len(out_p) != len(out_t)) or (len(out_p) != len(out_f)):
        raise Exception("Mapping failed!")
    
    # Get total size on disk (to warn user)
    size = 0.0
    for f in out_f:
        size += os.path.getsize(f)
    size *= 1.0e-9
    
    # Result
    print("    %d files mapped, totalling %g GB" % (out_n, size))
    print("    done\n")
    return np.array(out_p, dtype=float), np.array(out_t, dtype=float), out_f

