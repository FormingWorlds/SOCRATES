# Tools for processing DACE files

# Import system libraries
from glob import glob
import numpy as np
import os, sys

# Import files
import src.cross as cross
import src.utils as utils

# Download interpolated file from dace
def download(isotopologue:str, linelist:str, linelist_version:float, p_arr, t_arr, outdir:str):

    from dace_query.opacity import Molecule
    import h5py, struct, subprocess, glob

    tmpdir = "/tmp/dace/"
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)
    for e in ["tar", "hdf5", "bin", "ref"]:
        for f in glob.glob(tmpdir+"*."+e):
            utils.rmsafe(f)

    len_p = len(p_arr)
    max_p = 1.0e3
    min_p = 1.0e-8
    if (np.amax(p_arr) > max_p) or (np.amin(p_arr) < min_p):
        raise Exception("Pressure target exceeds the valid range of (%g,%g)"%(min_p,max_p))
    max_t = np.inf
    min_t = 50.0
    if (np.amax(t_arr) > max_t) or (np.amin(t_arr) < min_t):
        raise Exception("Temperature target exceeds the valid range of (%g,%g)"%(min_t,max_t))

    print("Total requests: %d" % (len(p_arr)*len(t_arr)))

    # For all p,t
    for ip,p in enumerate(sorted(p_arr)):
        t_req = []
        p_req = []
        for t in sorted(t_arr):
            t_req.append(t)
            p_req.append(p)
        npts = len(t_req)
        print("\np[%d/%d] : requesting %d points"%(ip,len_p,npts))

        # Download file
        tarnme = "temp.tar"
        tarpath = os.path.join(tmpdir, tarnme)
        utils.rmsafe(tarpath)
        Molecule.interpolate(isotopologue, linelist, round(linelist_version,1), t_req, p_req, output_directory=tmpdir, output_filename=tarnme)
        
        # Untar the file
        print("Untarring file")
        oldcwd = os.getcwd()
        os.chdir(tmpdir)
        sp = subprocess.run(["tar","-xvf",tarpath,"--strip-components=1"], stdout=subprocess.DEVNULL)
        os.chdir(oldcwd)
        
        # Read hdf5 file 
        print("Converting to bin files")
        hdf5path = glob.glob(tmpdir+"/*.hdf5")[0]
        with h5py.File(hdf5path,'r+') as hf:
            # Get the dataset
            dso = hf["opacity"]
            for i,key in enumerate(list(dso.keys())):
                j = i+1
                print("    point %4d of %4d  (%5.2f%%)"%(j, npts, 100.0*j/npts))
                ds = dso[key]

                # Read k
                k_arr = ds[:]
                numax = len(k_arr) * 100.0
                numin = 0.0

                # Read p,t
                p = ds.attrs["pressure"]
                t = ds.attrs["temperature"]

                # Write pressure as string 
                pstr = ""
                logp = np.log10(p) * 100.0
                if logp < 0.0:
                    pstr += "n"
                else:
                    pstr += "p"
                pstr += "%03d"%abs(logp)

                # Write bin file
                binnme  = "Itp"
                binnme += "_%05d" % numin 
                binnme += "_%05d" % (numax/1e4)
                binnme += "_%05d" % t
                binnme += "_%s"   % pstr
                binnme += ".bin"
                binpath = os.path.join(outdir, binnme)
                utils.rmsafe(binpath)
                with open(binpath, "wb") as hdl:
                    for i in range(0,len(k_arr),4):
                        vals = [k_arr[i],k_arr[i+1],k_arr[i+2],k_arr[i+3]]
                        hdl.write(struct.pack('4f', *vals))  # 4 bytes at a time (Float32)
        print("\n")

    return outdir


# List DACE bin and itp files in directory
def list_files(directory:str) -> list:
    files = list(glob(directory+"/"+"Out*.bin"))
    files.extend(list(glob(directory+"/"+"Itp*.bin")))
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

def get_pt(directory:str, p_targets:list=[], t_targets:list=[], allow_itp:bool=True):
    """Get p,t points covered by DACE bin files within a given directory.

    The p,t arrays will be sorted in ascending order, pressure first. 
    They do not need to have the same length, but must be 1D.
    Also returns the file paths, for them to be read fully later.

    Parameters
    ----------
    directory : str
        Directory containing bin files
    p_targets : list
        Target pressure values [bar]
    t_targets : list
        Target temperature values [K]
    allow_itp : bool
        Use bin files which were generated by interpolation?

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

