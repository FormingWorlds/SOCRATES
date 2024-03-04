# General utilities 

import os
import numpy as np

# Named directories
dirs = {"tools":os.path.join(os.path.abspath(os.environ["RAD_DIR"]), "spectraltools/")}
dirs["output"] = os.path.join(dirs["tools"] , "output/" )
dirs["data"] = os.path.join(dirs["tools"]   , "data/" )
dirs["dace"] = os.path.join(dirs["data"]    , "dace/" )
dirs["hitran"] = os.path.join(dirs["data"]  , "hitran/" )
dirs["exomol"] = os.path.join(dirs["data"]  , "exomol/" )


# Convert wavenumber [cm-1] to wavelength [nm]
def wn2wl(wn:float) -> float:
    if wn == 0:
        return float("inf")
    else:
        return 10000000.0 / wn

# Convert wavelength [nm] to wavenumber [cm-1]
def wl2wn(wl:float) -> float:
    if wl == 0:
        return float("inf")
    else:
        return 10000000.0 / wl
    
# Check iterable is strictly ascending
def is_ascending(arr):
    l = len(arr)
    if l < 2:
        return True
    for i in range(1,l):
        if not arr[i] >= arr[i-1]:
            return False 
    return True

# Check if array is unique (no repeated values)
def is_unique(arr):
   return bool( len(np.unique(arr)) == len(arr) )

# Convert all of the values in an array into one long string
def get_arr_as_str(arr):
    if type(arr[0]) == float:
        return " ".join(["%g"%v for v in arr])
    elif type(arr[0]) == int:
        return " ".join(["%d"%v for v in arr])
    else:
        return " ".join([str(v) for v in arr])

# Get item in 'arr' that is numerically closest to 'value'
def get_closest(value, arr):
    return arr[np.argmin(np.abs(np.array(arr)-value))]

    
# Find the closest point in a p,t grid, returning its index, distance, p, t.
def find_pt_close(arr_p, arr_t, target_p, target_t):
    target_p = max(1.0e-9, target_p)
    target_t = max(1.0e-9, target_t)
    nvals = len(arr_p)
    dists = []
    for i in range(nvals):
        dists.append(100.0 * ( ( (arr_p[i]-target_p)/target_p)**2.0 + (  (arr_t[i]-target_t)/target_t  )**2.0   )**0.5)
    iclose = np.argmin(dists)
    dclose = dists[iclose]
    return iclose, dclose, arr_p[iclose], arr_t[iclose]
    
# Check if output folder exists
def check_output_exists():
    return os.path.exists( dirs["output"]  )

# Sanitise source string
def sourcesafe(source:str):
    safe = source.strip().lower()
    if safe not in ["dace", "hitran", "exomol", "direct"]:
        raise Exception("Invalid source '%s'"% source)
    return safe

# Safely remove a file
def rmsafe(file:str):
    if file in ["","."]:
        print("WARNING: an attempt was made to remove the current working directory!")
        return
    if os.path.exists(file):
        os.remove(file)

# Map absorber names to their IDs (see SOCRATES user guide p.71)
absorber_id = {
    "H2O" :'1' ,  
    "CO2" :'2' ,  
    "O3"  :'3' , 
    "N2O" :'4' ,  
    "CO"  :'5' , 
    "CH4" :'6' ,  
    "O2"  :'7' , 
    "NO"  :'8' , 
    "SO2" :'9' ,  
    "NO2" :'10',  
    "NH3" :'11',  
    "HNO3":'12',  
    "N2"  :'13', 
    "H2"  :'23', 
    "He"  :'24', 
    "OCS" :'25'
}
