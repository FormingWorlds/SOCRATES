# Tools for writing netcdf files

import numpy as np
from netCDF4 import Dataset
import os

import common.utils as utils
import common.cross as cross

def write_ncdf(formula:str, source:str, p_points:np.ndarray, t_points:np.ndarray, f_points:list):
    """Write netCDF file containing P, T, nu, and cross-section data.

    Parameters
    ----------
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

    # Open file
    ds_path = os.path.join( utils.dirs["output"] , "x_%s.nc"%formula)
    print("Writing netCDF for '%s'..."%formula)
    utils.rmsafe(ds_path)
    ds = Dataset(ds_path, "w", format="NETCDF4")

    # Read first xsec to get nu array
    x_first = cross.xsec(formula, source, f_points[0])
    x_first.read()
    nu_arr = x_first.arr_nu * 100.0  # convert cm-1 to m-1
    print("    nu_min = %.2f cm-1" % x_first.numin)
    print("    nu_max = %.2f cm-1" % x_first.numax)

    # Create dimensions
    print("    define dimensions")
    len_pt = len(p_points)
    len_nu = len(nu_arr)
    dim_nu = ds.createDimension("nu",      len_nu)
    dim_pt = ds.createDimension("pt_pair", len_pt)

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
    modprint = 10
    counter = 0
    for i in range(len_pt):  # for each p,t point
        counter = i+1
        if counter % modprint == 0:
            print("    point %5d of %5d   (%5.1f%%)" % (counter,len_pt, 100.0*(counter/len_pt)))

        # Read file at this p,t
        this_xsec = cross.xsec(formula, source, f_points[i])
        this_xsec.read()
        var_xc[i,:] = this_xsec.arr_k * 10.0  # convert cm2/g to m2/kg
        del this_xsec

    print("    done writing to '%s'" % ds_path)
    # Finish up
    ds.close()
    return ds_path


    