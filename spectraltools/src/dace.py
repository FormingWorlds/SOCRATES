# Tools for processing DACE files

# Import system libraries
from glob import glob
import numpy as np
import os
from scipy.spatial import KDTree

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

    files = list_files(directory)

    # Targets?
    use_all = (len(p_targets) == 0) or (len(t_targets) == 0)

    # Record all P,T points
    all_p = []
    all_t = []
    all_f = []
    for f in files:
        x = cross.xsec("", "dace", f)
        x.parse_binname()
        all_p.append(x.p)
        all_t.append(x.t)
        all_f.append(f)
    all_n = len(all_f)

    # Unique P,T values
    unique_p = sorted(list(set(all_p)))
    unique_t = sorted(list(set(all_t)))

    if use_all:
        print("    use_all = True")
        # Store all points
        use_p = all_p[:] 
        use_t = all_t[:] 
    else:
        print("    use_all = False")
        
        # Setup KD tree for search
        X = np.array([np.log10(all_p), all_t]).T
        tree = KDTree(X, leafsize=100, copy_data=True)

        # Setup points to search by
        tgt_p = []
        tgt_t = []
        for p in p_targets:
            for t in t_targets:
                tgt_p.append(p)
                tgt_t.append(t)

        # Perform search
        Q = np.array([np.log10(tgt_p), tgt_t]).T
        best_d, best_i = tree.query(Q)
        use_p = np.array(all_p, dtype=float)[best_i]
        use_t = np.array(all_t, dtype=float)[best_i]

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
                        out_p.append(p)
                        out_t.append(t)
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

