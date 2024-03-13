# Tools for processing DACE files

# Import system libraries
import numpy as np
import os, glob

# Import files
import src.cross as cross
import src.utils as utils
import src.phys as phys

# Download interpolated file from dace
def download(isotopologue:str, linelist:str, linelist_version:float, p_arr, t_arr, outdir:str):

    from dace_query.opacity import Molecule
    import h5py, struct, subprocess

    # Validate p,t
    len_p = len(p_arr)
    max_p = 1.0e3
    min_p = 1.0e-8
    if (np.amax(p_arr) > max_p) or (np.amin(p_arr) < min_p):
        raise Exception("Pressure target exceeds the valid range of (%g,%g)"%(min_p,max_p))
    max_t = np.inf
    min_t = 50.0
    if (np.amax(t_arr) > max_t) or (np.amin(t_arr) < min_t):
        raise Exception("Temperature target exceeds the valid range of (%g,%g)"%(min_t,max_t))
    
    # Validate name
    formula = phys.iso_to_formula(isotopologue)
    phys.chemsafe(formula)  # will raise error if formula is invalid

    # Tidy files
    tmpdir = "/tmp/dacedownload_%s/"%formula
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)
    for e in ["tar", "hdf5", "bin", "ref"]:
        for f in glob.glob(tmpdir+"*."+e):
            utils.rmsafe(f)

    print("")
    print("Downloading %s (%s) from DACE"%(formula,isotopologue))
    print("Linelist: %s (v%.1f)"%(linelist,linelist_version))
    print("Total requests: %d" % (len(p_arr)*len(t_arr)))

    # Output folder
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # For all p,t
    for ip,p in enumerate(sorted(p_arr)):
        t_req = []
        p_req = []
        for t in sorted(t_arr):
            t_req.append(t)
            p_req.append(p)
        npts = len(t_req)
        print("\np[%d/%d] : requesting %d points"%(ip+1,len_p,npts))

        # Download file
        tarnme = formula+".tar"
        tarpath = os.path.join(tmpdir, tarnme)
        utils.rmsafe(tarpath)
        Molecule.interpolate(isotopologue, linelist, round(linelist_version,1), t_req, p_req, output_directory=tmpdir, output_filename=tarnme)

        # Check file
        if not os.path.exists(tarpath):
            raise Exception("File not found at '%s'"%tarpath)
        
        # Untar the file
        print("Untarring file")
        oldcwd = os.getcwd()
        os.chdir(tmpdir)
        sp = subprocess.run(["tar","-xvf",tarpath,"--strip-components=1"], stdout=subprocess.DEVNULL)
        os.chdir(oldcwd)

        # Copy ref file
        if ip == 0:
            refpath = glob.glob(tmpdir+"/*.ref")[0]
            infpath = os.path.join(outdir, "info.txt")
            utils.rmsafe(infpath)
            if os.path.exists(refpath):
                with open(refpath, 'r') as hdl:
                    reflines = hdl.readlines()
            else:
                reflines = "[No literature references found]\n"
            with open(infpath, 'w') as hdl:
                hdl.write(isotopologue + "\n")
                hdl.write(formula + "\n")
                hdl.write(linelist + " version " +  str(linelist_version) + "\n\n")

                hdl.write("Requested pressures [bar]: " + utils.get_arr_as_str(p_arr) + "\n")
                hdl.write("Requested tempreatures [K]: " + utils.get_arr_as_str(t_arr) + "\n\n")

                for l in reflines:
                    hdl.write(l)
                hdl.write("\n")
        
        # Read hdf5 file 
        print("Converting to bin files")
        hdf5path = glob.glob(tmpdir+"/*.hdf5")[0]
        with h5py.File(hdf5path,'r+') as hf:
            # Get the dataset
            dso = hf["opacity"]
            for i,key in enumerate(list(dso.keys())):
                j = i+1
                print("    point %4d of %4d  (%5.1f%%)"%(j, npts, 100.0*j/npts))
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
    files = list(glob.glob(directory+"/"+"Out*.bin"))
    files.extend(list(glob.glob(directory+"/"+"Itp*.bin")))
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
        return []
    
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
def list_all_ptf(directory:str, allow_itp:bool=True):
    files = list_files(directory)

    all_p = []
    all_t = []
    all_f = []
    for f in files:
        if ("Itp" in f) and (not allow_itp):
            continue
        x = cross.xsec("", "dace", f)
        x.parse_binname()
        all_p.append(x.p)
        all_t.append(x.t)
        all_f.append(f)
    return all_p, all_t, all_f

def map_ptf(directory:str, p_targets:list=[], t_targets:list=[], allow_itp:bool=True):
    """Map p,t points covered by DACE bin files within a given directory.

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

    # Get all points
    all_p, all_t, all_f = list_all_ptf(directory, allow_itp=allow_itp)
    all_n = len(all_f)
    print("    found %d files"%all_n)
    
    # Check limits
    want_n = len(p_targets) * len(t_targets)
    if want_n == 0:
        want_n = all_n
    print("    want %d files"%want_n)
    if want_n >= 2000:
        raise Exception("SOCRATES does not support more than 2000 PT points")

    # Unique P,T values
    unique_p = np.unique(all_p)
    unique_t = np.unique(all_t)

    if len(unique_p) * len(unique_t) != all_n:
        raise Exception("Files are not unique or the p,t grid is not rectilinear")

    # Find best temperatures
    print("    finding best temperatures")
    selected_t = []
    if (len(t_targets) >= len(unique_t)) or (len(t_targets) == 0):
        selected_t = unique_t[:]
    else:
        use_t = []
        search_t = list(unique_t[:])
        for t in t_targets:
            i = utils.get_closest_idx(t, search_t)
            selected_t.append(search_t[i])
            search_t.pop(i)

    # Find best pressures
    print("    finding best pressures")
    selected_p = []
    if (len(p_targets) >= len(unique_p)) or (len(p_targets) == 0):
        selected_p = unique_p[:]
    else:
        use_p = []
        search_p = list(unique_p[:])
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

    # Map to files
    print("    mapping to files")
    atol = 1.0e-5
    use_n = len(use_p)
    modprint = int(use_n * 0.1)
    
    print("     %: ", end='')
    use_f = []
    for j in range(use_n):
        if (j+1)%modprint == 0:
            print("%d " %( (j+1)/use_n *100.0), end='', flush=True)

        for i in range(all_n):
            p = all_p[i]
            t = all_t[i]
            if np.isclose(use_p[j], p, atol=atol) and np.isclose(use_t[j], t, atol=atol):
                use_f.append(all_f[i])
                break 
    print(" ")
    use_f = np.array(use_f, dtype=str)

    # Check if things don't line up
    if (len(use_p) != len(use_t)):
        raise Exception("Mapping failed (p vs t), (%d vs %d)"%(len(use_p), len(use_t)))
    if (len(use_p) != len(use_f)):
        raise Exception("Mapping failed (p/t vs f) , (%d vs %d)"%(len(use_p), len(use_f)))
    
    # Get total size on disk (to warn user)
    size = 0.0
    for f in use_f:
        size += os.path.getsize(f)
    size *= 1.0e-9
    
    # Result
    print("    %d files mapped, totalling %g GB" % (use_n, size))
    print("    done\n")
    return use_p, use_t, use_f

