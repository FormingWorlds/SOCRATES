# General utilities 

import os

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
    
# Named directories
dirs = {"tools":os.path.join(os.path.abspath(os.environ["RAD_DIR"]), "spectraltools/")}
dirs["output"] = os.path.join(dirs["tools"] , "output/" )
dirs["data"] = os.path.join(dirs["tools"]   , "data/" )
dirs["dace"] = os.path.join(dirs["data"]    , "dace/" )
dirs["hitran"] = os.path.join(dirs["data"]  , "hitran/" )
dirs["exomol"] = os.path.join(dirs["data"]  , "exomol/" )

# Check if output folder exists
def check_output_exists():
    return os.path.exists( dirs["output"]  )

# Sanitise source string
def sourcesafe(source:str):
    safe = source.strip().lower()
    if safe not in ["dace", "hitran", "exomol"]:
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
