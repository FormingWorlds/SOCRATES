# Tools for batch processing files

# Import system libraries
from glob import glob
import numpy as np
import os, shutil

# Import files
import common.cross as cross
import common.utils as utils

# List DACE bin files in directory
def list_files(directory:str) -> list:
    files = glob(directory+"/"+"Out*.bin")
    if len(files) == 0:
        print("WARNING: No bin files found in '%s'"%directory)
    return [os.path.abspath(f) for f in files]

def find_bin_close(directory:str, p_aim:float, t_aim:float) -> str:
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
    d_arr = []  # distance from target
    for f in files:
        temp = cross.xsec("", "dace", f)
        temp.parse_binname()
        p_arr.append(temp.p)
        t_arr.append(temp.t)

        dist = 100.0 * ( ( (p_aim-temp.p)/temp.p )**2.0 + ( (t_aim-temp.t)/temp.t )**2.0 ) ** 0.5
        d_arr.append(dist)

    i_close = np.argmin(d_arr)
    print("Found BIN file with distance = %.3f%%" % d_arr[i_close])

    return files[i_close]

def find_grid(directory:str, p_list:list, t_list:list):
    """Get DACE files that are close to the given p,t values.

    Parameters
    ----------
    directory : str
        Directory containing bin files
    p_list : list
        Target pressures [bar]
    t_list : float
        Target temperatures [K]

    Returns
    -------
    list
        List of file paths
    """

    # Gather files
    files = []
    for p in p_list:
        for t in t_list:
            new = find_bin_close(directory, p, t)
            if new in files:
                print("This p,t grid would result in duplicate points")
                return
            else:
                files.append(new)
    return files

def get_pt(directory:str):
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

    # P,T points
    arr_p = []
    arr_t = []
    for f in files:
        x = cross.xsec("", "dace", f)
        x.parse_binname()
        arr_p.append(x.p)
        arr_t.append(x.t)

    # Unique P,T values
    unique_p = sorted(list(set(arr_p)))
    num_p = len(unique_p)  
    unique_t = sorted(list(set(arr_t)))
    num_t = len(unique_t)  

    # Sorted arrays
    sorted_p = []
    sorted_t = []
    sorted_f = []
    for p in unique_p:
        for t in unique_t:
            # store these p,t
            sorted_p.append(p)
            sorted_t.append(t)
            # record which file maps to this p,t pair
            for i,f in enumerate(files):
                if np.isclose(arr_p[i],p) and np.isclose(arr_t[i],t):
                    sorted_f.append(f)

    if (len(sorted_f) != len(sorted_p)) or (len(sorted_p) != len(sorted_t)):
        raise Exception("Mapping failed!")
    
    # Get total size on disk (to warn user)
    size = 0.0
    for f in  files:
        size += os.path.getsize(f)
    size *= 1.0e-9
    
    # Result
    print("    %d files found, totaling %.2f GB" % (len(sorted_p), size))
    return np.array(sorted_p, dtype=float), np.array(sorted_t, dtype=float), sorted_f



# Write xsc files and p,t grid to files in the given folder
def write_grid(outdir:str, form:str, binfiles:list, concat=True):

    nfiles = len(binfiles)

    print("Writing grid with %d points" % nfiles)

    # Check output dir
    if not os.path.exists(outdir):
        raise Exception("Cannot write xsc files (output folder does not exist)")

    # Expected output files
    tsvout = outdir+"/"+"%s_grid.tsv"%form
    totout = outdir+"/%s_grid.xsc"%form

    print("    removing old files")
    rmvout = [] 
    rmvout.extend(list(glob(outdir+"/%s.xsc"%form)))
    rmvout.extend([tsvout, totout])
    for r in rmvout:
        utils.rmsafe(r)

    xscdir = outdir
    if concat:
        xscdir = outdir + "/.xsctemp/"
        if os.path.isdir(xscdir):
            shutil.rmtree(xscdir)
        os.mkdir(xscdir)

    # Get data and write xsc files
    print("    please wait...")
    p_arr = []
    t_arr = []
    xscfiles = []
    wnmin = -1
    wnmax = -1
    modprint = 10
    pctlast  = -999.0
    for i in range(nfiles):
        x = cross.xsec(form, "dace", binfiles[i])
        x.readbin()
        wnmin = x.numin
        wnmax = x.numax
        t_arr.append(x.t)
        p_arr.append(x.p)
        xscfiles.append(x.writexsc(xscdir))
        thispct = i/float(nfiles-1)*100.0
        if (thispct > pctlast + modprint - 1.0e-9):
            pctlast = thispct
            print("    %3d%%" % thispct)

    wlmax = utils.wn2wl(wnmin)
    wlmin = utils.wn2wl(wnmax)

    print("    p_arr = %s bar" % str(p_arr))
    print("    t_arr = %s K"   % str(t_arr))
    print("    wlmin = %.3f nm\t\tnumax = %.3f cm-1"  % (wlmin, wnmax))
    print("    wlmax = %.3f nm\t\tnumin = %.3f cm-1"  % (wlmax, wnmin))

    # If concat: concatenate xsc files and then remove temp dir
    if concat:
        with open(totout, 'w') as totfile:
            for xfile in xscfiles:
                with open(xfile) as infile:
                    for line in infile:
                        totfile.write(line)
                totfile.write("\n")
        shutil.rmtree(xscdir)
        print("    wrote xsc data to the file '%s'" % totout)
    else:
        print("    wrote xsc data to files in '%s'" % outdir)

    # Write p,t file
    grid = np.array([p_arr,t_arr]).T
    np.savetxt(tsvout, grid, fmt="%1.3e", delimiter=" ", header="p/bar    T/K")

    print("    wrote p,t values to the file '%s'" % tsvout)
