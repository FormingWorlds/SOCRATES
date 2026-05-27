# Tools for processing DACE files

# Import system libraries
import numpy as np
import os
import glob

# Import files
import src.cross as cross
import src.utils as utils
import src.phys as phys

def get_formula_path(formula:str):
    path = os.path.join(utils.dirs["dace"], formula+"/")
    if not os.path.exists(path):
        raise Exception("Formula '%s' not found in DACE directory! Check chem_dict in phys.py" % formula)
    return path

# List DACE bin and itp files in directory
def list_files(formula:str) -> list:
    directory = get_formula_path(formula)
    files = list(glob.glob(directory+"/"+"Out*.bin"))
    files.extend(list(glob.glob(directory+"/"+"Itp*.bin")))
    if len(files) == 0:
        print("WARNING: No bin files found in '%s'"%directory)
    return [os.path.abspath(f) for f in files]

def find_bin_close(formula:str, p_aim:float, t_aim:float, quiet=False) -> str:
    """Search for DACE bin file.

    Finds the DACE bin file in the directory which most closely matches the target p,t values.

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
    list
        List of ranked closest bin files (length=rank)
    """

    if (p_aim < 0) or (t_aim < 0):
        raise Exception("Target pressure and temperature must be positive values")

    directory = get_formula_path(formula)
    files = list_files(formula)
    count = len(files)
    if count == 0:
        raise Exception("No bin files found in '%s'"%directory)
    
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


# Download interpolated file from dace
def download(isotopologue:str, linelist:str, linelist_version:float, p_arr, t_arr, outdir:str):

    from dace_query.opacity import Molecule
    import h5py
    import struct
    import subprocess

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

    # For all p
    for ip,p in enumerate(sorted(p_arr)):
        t_req = []
        p_req = []
        for t in sorted(t_arr): # For all t
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

        # Write database/reference info to file
        if ip == 0:
            infpath = os.path.join(outdir, "info.txt"); utils.rmsafe(infpath)

            refpath = glob.glob(tmpdir+"/*.ref")
            if len(refpath) > 0:
                refpath = refpath[0]
                with open(refpath, 'r') as hdl:
                    reflines = hdl.readlines()
            else:
                reflines = ["[No literature references found]\n"]

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

# Extend data to temperatures outside of the range provided by the database.
# def extend(outdir:str, t_extend):

    # Extends temperature range by simply copying and renaming the nearest 
    # valid temperature point. E.g. if 3000 K were requested but the database 
    # only extends to 2900 K, then the 2900 K point would be duplicated and 
    # re-labelled as 3000 K. This can be thought of nearest-neighbour
    # extrapolation, which avoids making extra assumptions about the physics.
    # This extrapolation is performed for all pressures, which assumes that the 
    # p/t grid is rectangular.

    # Required?
    # if len(t_extend) < 1:
    #     return outdir    

    # # Get current points
    # all_p, all_t, all_f =  ptf.list_all_ptf("dace", "H2O")
    # all_n = len(all_t)

    # # For all extended points...
    # for t_req in t_extend:

    #     print("Extending grid to %.1f K"%t_req)

    #     # Find nearest temperature for which we have data
    #     t_close = utils.get_closest(t_req, all_t)

    #     # Find all source points at this temperature
    #     t_src = []
    #     p_src = []
    #     f_src = []
    #     for i in range(all_n):
    #         if abs(all_t[i] - t_close) < 1.0e-10:
    #             t_src.append(all_t[i])
    #             p_src.append(all_p[i])
    #             f_src.append(all_f[i])

    #     # Check that the number of files is correct 
    #     n_src = len(t_src)
    #     n_unq = len(np.unique(all_p))
    #     if n_src != n_unq:
    #         print("WARNING: File count mismatch when extending temperature range (%d != %d)"%(n_src, n_unq))

    #     # Copy and rename these points with new temperature value 
    #     n_cpy = 0
    #     for i in range(len(t_src)):
    #         # get path 
    #         path_src = os.path.abspath(f_src[i])
    #         part_fol = path_src.split("/")[:-1]  # folders
    #         part_nme = path_src.split("/")[-1]   # file 

    #         # change temperature
    #         split_nme = list(part_nme.split("_")) # split file name 
    #         split_nme[3] = "%05d"%t_req

    #         # new file path
    #         path_new = "/".join(part_fol)
    #         path_new += "/"
    #         path_new += "_".join(split_nme)
    #         path_new = os.path.abspath(path_new)

    #         # copy file
    #         shutil.copyfile(path_src, path_new)
    #         n_cpy += 1

    #     print("    copied %d files"%n_cpy)

    # return outdir

