#!/usr/bin/env python3 
# Python wizard for interactive file conversion

# Import local files 
import common.spectral as spectral
import common.utils as utils
import common.dace as dace
import common.cross as cross
import os

def main():
    print("Wizard says hello")

    formula = "CO2"
    source = "dace"
    vols = [formula]
    spfile = utils.dirs["output"]+"sp_demo"

    formula_path = os.path.join(utils.dirs[source], formula.strip()+"/")
    if not os.path.exists(formula_path):
        raise Exception("Could not find folder '%s'" % formula_path)

    arr_p, arr_t, arr_f = dace.get_pt(formula_path)
    
    temp_xc = cross.xsec(formula, source, dace.list_files(formula_path)[0])
    temp_xc.read()
    numin = temp_xc.numin
    numax = temp_xc.numax
    dnu   = (numax-numin)/40.0

    spectral.create_skeleton(spfile, arr_p, arr_t, vols, numin, numax, dnu)

    print("Goodbye")

if __name__ == "__main__":
    main()
    exit(0)
