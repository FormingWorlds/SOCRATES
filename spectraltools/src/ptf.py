import logging
import numpy as np
import os

import src.exocross as exocross
import src.dace as dace
import src.cross as cross
import src.hitran as hitran
import src.utils as utils

log = logging.getLogger("fwl."+__name__)


def list_files(source:str, formula:str, quiet=True):
    match source:
        case "dace":
            return dace.list_files(formula)
        case "exocross":
            return exocross.list_files(formula, quiet=quiet)
        case "hitran":
            return hitran.list_files(formula)
        case _:
            raise Exception("Invalid source '%s'"% source)
        
# Get formula path
def get_formula_path(source:str, formula:str):
    match source:
        case "dace":
            return dace.get_formula_path(formula)
        case "hitran":
            return hitran.get_formula_path(formula)
        case "exocross":
            return exocross.get_formula_path(formula)
        case _:
            raise Exception("Invalid source '%s'"% source)

# Get the first available file for a formula, raising a clear error if none exist
def first_file(source:str, formula:str):
    files = list_files(source, formula, quiet=True)
    if len(files) == 0:
        raise Exception("No cross-section files found for '%s' with '%s' - check data directory" % (formula, source))
    return files[0]

# List the p,t values across all BIN files (f) in the directory
def list_all_ptf(source:str, formula:str, allow_itp:bool=True, quiet=True):
    files = list_files(source, formula, quiet=quiet)

    all_p = []
    all_t = []
    all_f = []
    for f in files:
        if ("Itp" in f) and (not allow_itp):
            continue
        x = cross.xsec("", source, f)
        x.parse_name()
        all_p.append(x.p)
        all_t.append(x.t)
        all_f.append(f)
    return all_p, all_t, all_f

def best_pt(source:str, formula:str, p_targets:list, t_targets:list, allow_itp:bool=True):
    """
    Find the best pressure and temperature points for a given source and formula.

    This is a flattened grid.

    Parameters
    ----------
    source : str
        Source of the data (e.g. "dace", "exocross")
    formula : str
        Formula of the volatile (e.g. "H2O")
    p_targets : list
        Target pressure values [bar]
    t_targets : list
        Target temperature values [K]   

    Returns
    -------
    np.ndarray
        pressures [bar]
    np.ndarray 
        temperatures [K]
    """

    # Get all points
    all_p, all_t, all_f = list_all_ptf(source, formula, allow_itp=allow_itp)
    all_n = len(all_f)
    log.info("    found %d files", all_n)

    # Check limits
    want_n = len(p_targets) * len(t_targets)
    if want_n == 0:
        want_n = all_n
    log.info("    want %d files", want_n)
    if want_n >= 2000:
        raise Exception("SOCRATES does not support more than 2000 PT points")

    # Unique P,T values
    unique_p = np.unique(all_p)
    unique_t = np.unique(all_t)

    if len(unique_p) * len(unique_t) != all_n:
        raise Exception("Files are not unique or the p,t grid is not rectilinear")

    # Find best temperatures
    log.info("    finding best temperatures")
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
    log.info("    finding best pressures")
    selected_p = []
    if (len(p_targets) >= len(unique_p)) or (len(p_targets) == 0):
        selected_p = unique_p[:]
    else:
        use_p = []
        search_p = list(unique_p[:])
        for p in p_targets:
            i = utils.get_closest_idx(np.log10(p), np.log10(search_p))
            selected_p.append(search_p[i])
            search_p.pop(i)
    
    # Flatten p,t points (ensure ascending order)
    use_t = []
    use_p = []
    for p in sorted(selected_p):
        for t in sorted(selected_t):
            use_t.append(t)
            use_p.append(p)

    log.info("    %d t points selected", len(use_t))
    log.info("    %d p points selected", len(use_p))

    use_t = np.array(use_t, dtype=float)
    use_p = np.array(use_p, dtype=float)

    return use_p, use_t

def find_closest_file(source:str, formula:str, target_p:float, target_t:float,
                      quiet=True):
    """
    Find the closest file to the given pressure and temperature points.

    Parameters
    ----------
    source : str
        Source of the data (e.g. "dace", "exocross")
    formula : str
        Formula of the volatile (e.g. "H2O")
    target_p : float
        Target pressure [bar]
    target_t : float
        Target temperature [K]

    Returns
    -------
    str
        Path to the closest file
    """

    match source:
        case "dace":
            import src.dace as dace
            close_path = dace.find_bin_close(formula, float(target_p), float(target_t), quiet=quiet)
        case "hitran":
            import src.hitran as hitran
            close_path = hitran.find_xsc_close(formula, float(target_p), float(target_t), quiet=quiet)
        case "exocross":
            import src.exocross as exocross
            close_path = exocross.find_xsec_close(formula, float(target_p), float(target_t), quiet=quiet)
        case _:
            raise Exception(f"Invalid source {source}")
    
    return close_path

def map_ptf(source:str, formula:str, p_targets:list, t_targets:list, allow_itp:bool=True):
    """Map p,t points covered by source files within a given directory.

    The p,t arrays will be sorted in ascending order, pressure first. 
    They do not need to have the same length, but must be 1D.
    Also returns the file paths, for them to be read fully later.

    Parameters
    ----------
    source : str
        Source of the data (e.g. "dace", "exocross")
    formula : str
        Formula of the volatile (e.g. "H2O")
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

    log.info("Mapping p,t points to cross-section files for '%s' from '%s'", formula, source)

    # get files for this formula
    _, _, all_f = list_all_ptf(source, formula, allow_itp=allow_itp)
    all_n = len(all_f)
    log.info("    found %d files", all_n)

    # Map to files
    atol = 1.0e-5
    use_n = len(t_targets)
    if use_n >= 100:
        modprint = int(use_n * 0.1)
    else:
        modprint = 1

    use_f = []
    use_t = []
    use_p = []
    for j in range(use_n):
        if (j+1)%modprint == 0:
            log.info("      %: " + "%d"%((j+1)/use_n *100.0))

        # find closest p,t point for this formula
        f = find_closest_file(source, formula, p_targets[j], t_targets[j])
        use_f.append(f)

        # get p,t from file name
        x = cross.xsec("", source, f)
        x.parse_name()
        use_p.append(x.p)
        use_t.append(x.t)
    use_f = np.array(use_f, dtype=str)

    # Get total size on disk (to warn user)
    size = 0.0
    for f in use_f:
        size += os.path.getsize(f)
    size *= 1.0e-9

    # Result
    log.info("    %d files mapped, totalling %.2f GB", use_n, size)
    log.info("    done")
    return use_p, use_t, use_f


def write_csv(alias:str, v:str, p:list, t:list, f:list):
    """Write p,t,f to csv file for reference.

    Parameters
    ----------
    alias : str
        Alias for the spectral file
    v : str
        Formula of the volatile
    p : list
        List of pressures [bar]
    t : list
        List of temperatures [K]
    f : list
        List of file paths
    """

    path = os.path.join(utils.dirs["output"], "%s_%s_ptf.csv"%(alias, v))

    with open(path, "w") as f_out:
        f_out.write("p/bar,t/K,file\n")
        for i in range(len(p)):
            f_out.write("%g,%g,%s\n"%(p[i], t[i], f[i]))
