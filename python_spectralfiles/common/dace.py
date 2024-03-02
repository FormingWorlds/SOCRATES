# Tools for batch processing files

# Import system libraries
from glob import glob
import numpy as np
import os, shutil

# Import files
import common.cross as cross
import common.utils as utils


# List DACE bin files in dir
def list_files(dir:str) -> list:
    return list(glob(dir+"/"+"Out*.bin"))

def find_bin_close(dir:str, p_aim:float, t_aim:float) -> str:
    """Search for DACE bin file.

    Finds the DACE bin file in the directory which most closely matches the target p,t values.

    Parameters
    ----------
    dir : str
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

    files = list_files(dir)
    count = len(files)
    if count == 0:
        raise Exception("Could not find any bin files in '%s'" % dir)
    
    p_arr = []  # pressure
    t_arr = []  # temperature
    d_arr = []  # distance from target
    for f in files:
        temp = cross.xsec("", f)
        temp.parse_binname()
        p_arr.append(temp.p)
        t_arr.append(temp.t)

        dist = ( ( (p_aim-temp.p)/temp.p )**2.0 + ( (t_aim-temp.t)/temp.t )**2.0 ) ** 0.5
        d_arr.append(dist)

    i_close = np.argmin(d_arr)

    return files[i_close]

# Get DACE files that are close to the given p,t values
def get_grid(dir:str, p_list:list, t_list:list):

    # Gather files
    files = []
    for p in p_list:
        for t in t_list:
            new = find_bin_close(dir, p, t)
            if new in files:
                print("This p,t grid would result in duplicate points")
                return
            else:
                files.append(new)

    return files

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
        if os.path.exists(r):
            os.remove(r)

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
        x = cross.xsec(form, binfiles[i])
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
