#!/usr/bin/env python3 
# Convert DACE bin file to an xsc file

# Import local files 
import common.cross as cross
import common.dace as dace
import common.phys as phys

import os, sys

# Main function
def main(formula:str, pres, temp):

    dace_db = os.path.join( os.path.abspath(".") , "data" , "dace")
    formula_path =  os.path.join(dace_db, formula.strip())
    bin_path = dace.find_bin_close(formula_path, float(pres), float(temp))

    dace_test = cross.xsec(formula, "dace", bin_path)
    dace_test.readbin()
    dace_test.plot(units=0)


    # p_list = [1.0, 10.0, 100.0]
    # t_list = [100.0, 1500.0, 3000.0]

    # binfiles = batch.get_grid(d, p_list, t_list)
    # batch.write_grid(".", "H2O", binfiles, concat=True)

    # htrn_test = cross.xsec("CH3F", "hitran", hitran_db+"CH3F/CH3F_278.1K-760.0Torr_600.0-6500.0_0.11_N2_123_43.xsc")
    # htrn_test.readxsc()
    # htrn_test.plot(units=1)


# Run main function
if __name__ == "__main__":

    args = sys.argv
    if not (len(args) == 4):
        raise Exception("Invalid arguments")
    
    main(args[1], args[2], args[3])


# End of file
