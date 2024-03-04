# Tools for processing DACE files

# Import system libraries
from glob import glob
import numpy as np
import os, shutil

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
    str
        Absolute path to best bin file
    """

    if (p_aim < 0) or (t_aim < 0):
        raise Exception("Target pressure and temperature must be positive values")

    files = list_files(directory)
    count = len(files)
    if count == 0:
        raise Exception("Could not find any bin files in '%s'" % directory)
    
    p_arr = []  # pressure
    t_arr = []  # temperature
    for f in files:
        temp = cross.xsec("", "dace", f)
        temp.parse_binname()
        p_arr.append(temp.p)
        t_arr.append(temp.t)

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

    # Get files
    files = list_files(directory)

    # Targets?
    use_all = (len(p_targets) == 0) or (len(t_targets) == 0)

    # P,T points
    arr_p = []
    arr_t = []
    arr_f = []
    if use_all:
        print("    use_all = True")
        for f in files:
            x = cross.xsec("", "dace", f)
            x.parse_binname()
            arr_p.append(x.p)
            arr_t.append(x.t)
            arr_f.append(f)
    else:
        print("    use_all = False")
        for p in p_targets:
            for t in t_targets:
                f = find_bin_close(directory, p, t, quiet=True)
                x = cross.xsec("", "dace", f)
                x.parse_binname()
                arr_p.append(x.p)
                arr_t.append(x.t)
                arr_f.append(f)

    # Unique P,T values
    unique_p = sorted(list(set(arr_p)))
    num_p = len(unique_p)  
    unique_t = sorted(list(set(arr_t)))
    num_t = len(unique_t)  

    # Sorted arrays
    sorted_p = []
    sorted_t = []
    sorted_f = []

    counter = 1
    num_pt = num_p * num_t
    modprint = int(num_pt*0.1)
    for p in unique_p:
        for t in unique_t:
            if counter % modprint == 0:
                print("    point %5d of %5d   (%5.1f%%)" % (counter,num_pt, 100.0*(counter/num_pt)))

            # store these p,t
            sorted_p.append(p)
            sorted_t.append(t)
            # record which file maps to this p,t pair
            for i,f in enumerate(arr_f):
                if np.isclose(arr_p[i],p) and np.isclose(arr_t[i],t):
                    sorted_f.append(f)

            counter += 1

    if (len(sorted_f) != len(sorted_p)) or (len(sorted_p) != len(sorted_t)):
        raise Exception("Mapping failed!")
    
    # Get total size on disk (to warn user)
    size = 0.0
    for f in sorted_f:
        size += os.path.getsize(f)
    size *= 1.0e-9
    
    # Result
    print("    %d files mapped, totaling %g GB" % (len(sorted_p), size))
    return np.array(sorted_p, dtype=float), np.array(sorted_t, dtype=float), sorted_f

