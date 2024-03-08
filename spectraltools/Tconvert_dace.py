#!/usr/bin/env python3 
# Convert DACE bin files to a NetCDF file

# Import local files 
import src.dace as dace
import src.utils as utils
import src.netcdf as netcdf

import sys, os

# Main function
def main(formula:str):

    print("Processing DACE bin files for %s"%formula)

    formula_path = os.path.join(utils.dirs["dace"], formula.strip()+"/")
    if not os.path.exists(formula_path):
        raise Exception("Could not find folder '%s'" % formula_path)

    arr_p, arr_t, arr_f = dace.get_pt(formula_path)
    nc_path = os.path.join(utils.dirs["output"] , formula+"_dace.nc")
    netcdf.write_ncdf_from_grid(nc_path, formula, "dace", arr_p, arr_t, arr_f)
    
    # dace_test = cross.xsec(formula, bin_path)
    # dace_test.readbin()
    # dace_test.plot(units=0)


# Run main function
if __name__ == "__main__":

    if not utils.check_output_exists():
        print("ERROR: Output folder does not exist - refer to README.md for more information")
        exit(1)

    args = sys.argv
    main(args[1])
    exit(0)


# End of file
