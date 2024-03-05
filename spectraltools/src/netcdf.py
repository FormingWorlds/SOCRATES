# Tools for writing netcdf files

import numpy as np
from netCDF4 import Dataset
import os

import src.utils as utils
import src.cross as cross

def write_ncdf_from_grid(nc_path:str, formula:str, source:str, p_points:np.ndarray, t_points:np.ndarray, f_points:list):
    """Write netCDF file containing P, T, nu, and cross-section data.

    Parameters
    ----------
    nc_path : str
        Output file path
    formula : str
        Chemical formula for absorber
    source : str
        Name of source database
    p_points : np.ndarray
        Sorted pressure values [bar]
    t_points : np.ndarray 
        Sorted temperature values [K]
    f_points : list
        List of file paths mapping to the p,t values 

    Returns
    -------
    str
        Path to resultant netCDF file.
    """

    # Check input is valid 
    len_p = len(p_points)
    len_t = len(t_points)
    if len_p != len_t:
        raise Exception("Pressure and Temperature points have different lengths (%d,%d)"%(len_p,len_t))
    if not utils.is_ascending(p_points):
        print(utils.get_arr_as_str(p_points))
        raise Exception("Pressure array is not strictly ascending") 

    # Open file
    print("Writing netCDF for '%s' from '%s'..."%(formula,source))
    utils.rmsafe(nc_path)
    ds = Dataset(nc_path, "w", format="NETCDF4")

    # Read first xsec to get nu array
    x_first = cross.xsec(formula, source, f_points[0])
    x_first.read()
    nu_arr = x_first.get_nu() * 100.0  # convert cm-1 to m-1
    print("    nu_min , nu_max = %.2f , %.2f cm-1" % (x_first.numin,x_first.numax))

    # Create dimensions
    print("    define dimensions")
    
    len_nu = len(nu_arr)
    dim_nu = ds.createDimension("nu",      len_nu)
    dim_pt = ds.createDimension("pt_pair", len_p)

    # Create variables
    print("    define variables")
    var_p = ds.createVariable("p_calc","f4",("pt_pair",))
    var_p.title = "pressure"
    var_p.long_name = "pressure"
    var_p.units = "Pa"

    var_t = ds.createVariable("t_calc","f4",("pt_pair",))
    var_t.title = "temperature"
    var_t.long_name = "temperature"
    var_t.units = "K"

    var_nu = ds.createVariable("nu","f4",("nu",))
    var_nu.title = "wavenumber"
    var_nu.long_name = "wavenumber"
    var_nu.units = "m-1"
    var_nu.step = float(nu_arr[1]-nu_arr[0])

    var_xc = ds.createVariable("kabs","f4",("pt_pair","nu",))
    var_xc.title = "absorption"
    var_xc.long_name = "absorption"
    var_xc.units = "m2 kg-1"


    # Write p,t,nu
    print("    write p, t, nu")
    var_p[:]  = p_points * 1.0e5  # convert bar to Pa
    var_t[:]  = t_points
    var_nu[:] = nu_arr

    # Read and write cross-sections (2D)
    print("    write cross-section data")
    counter = 0
    modprint = max(int(len_p*0.1), 1)
    for i in range(len_p):  # for each p,t point
        counter = i+1
        if counter % modprint == 0:
            print("    point %5d of %5d   (%5.1f%%)" % (counter,len_p, 100.0*(counter/len_p)))

        # Read file at this p,t
        this_xsec = cross.xsec(formula, source, f_points[i])
        this_xsec.read()
        var_xc[i,:] = this_xsec.arr_k / 10.0  # convert cm2/g to m2/kg
        del this_xsec

    print("    done writing to '%s'" % nc_path)
    # Finish up
    ds.close()
    return nc_path

def read_netcdf_pt(fpath:str):
    """Read p,t values from netCDF file

    Parameters
    ----------
    fpath : str
        Path to netCDF file

    Returns
    -------
    np.ndarray
        Sorted pressure values [bar]
    np.ndarray 
        Sorted temperature values [K]
    """

    ds = Dataset(fpath, "r", format="NETCDF4")

    arr_p  = np.array(ds.variables["p_calc"][:] ) * 1.0e-5  # pa to bar
    arr_t  = np.array(ds.variables["t_calc"][:] )

    ds.close()

    return arr_p, arr_t

def read_netcdf_point(fpath:str, idx:int):
    """Read netCDF cross-section data at a specific index

    Parameters
    ----------
    fpath : str
        Path to netCDF file
    idx : int
        Index of point

    Returns
    -------
    np.ndarray
        Wavenumber array [cm-1]
    np.ndarray
        Cross-section array [cm2/g]
    """

    ds = Dataset(fpath, "r", format="NETCDF4")

    arr_nu = np.array(ds.variables["nu"][:]) / 100.0   # m-1 to cm-1
    arr_k  = np.array(ds.variables["kabs"][idx][:]) * 10.0  # m2/kg to cm2/g

    ds.close()

    return arr_nu, arr_k

