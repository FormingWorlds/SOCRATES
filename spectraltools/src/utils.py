# General utilities

import os
import numpy as np
import hashlib

# Check that SOCRATES is setup
if "RAD_DIR" not in os.environ.keys() or (os.environ["RAD_DIR"] is None):
    raise Exception("Cannot find SOCRATES! Refer to README.md")

# Named directories
dirs = {"socrates":os.path.abspath(os.environ["RAD_DIR"])}
dirs["tools"]  = os.path.join(dirs["socrates"], "spectraltools/")
dirs["output"] = os.path.join(dirs["tools"] , "output/" )
dirs["data"]   = os.path.join(dirs["tools"]   , "data/" )
dirs["dace"]   = os.path.join(dirs["data"]    , "dace/" )
dirs["hitran"] = os.path.join(dirs["data"]  , "hitran/" )
dirs["exomol"] = os.path.join(dirs["data"]  , "exomol/" )
dirs["cia"]    = os.path.join(dirs["data"]     , "cia/" )
dirs["moleculesUV"]    = os.path.join(dirs["tools"]     , "moleculesUV/" )

if not os.path.exists(dirs["output"]):
    raise Exception("Output folder '%s' not found"%dirs["output"])

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
        if not arr[i] > arr[i-1]:
            return False
    return True

# Check if array is unique (no repeated values)
def is_unique(arr):
   flat = np.array(arr).flatten()
   return bool( len(np.unique(flat)) == len(flat) )

# Convert all of the values in an array into one long string
def get_arr_as_str(arr):
    if type(arr[0]) is float:
        return " ".join(["%g"%v for v in arr])
    elif type(arr[0]) is int:
        return " ".join(["%d"%v for v in arr])
    else:
        return " ".join([str(v) for v in arr])

# Get item in 'arr' that is numerically closest to 'value'
def get_closest(value, arr):
    return arr[np.argmin(np.abs(np.array(arr)-value))]

# Get index of item in 'arr' that is numerically closest to 'value'
def get_closest_idx(value, arr):
    return np.argmin(np.abs(np.array(arr)-value))

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

# Calculate the checksum of a file using the BLAKE2b algorithm
def checksum(filename:str):
    # Adapted from https://stackoverflow.com/a/1131238
    with open(filename, "rb") as f:
        file_hash = hashlib.blake2b()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

# Check that the environment is configured
def checkenv():
    from shutil import which
    if which("prep_spec") is not None:
        return True
    else:
        raise EnvironmentError("Cannot find SOCRATES executables. Have you sourced set_rad_env?")

gas_list = []
gas_list_pcf = os.path.join(dirs["socrates"], "src", "radiance_core", "gas_list_pcf.F90")
with open(gas_list_pcf, "r") as f:
    gas_list_raw = f.readlines()
read_start = False
for line in gas_list_raw:
    # beginning of list of gases
    if "PARAMETER :: header_gas(npd_gases)" in line:
        if read_start:
            raise Exception("Unexpected start of gas list in '%s'"%gas_list_pcf)
        read_start = True
        continue

    # end of list of gases
    if read_start and line.endswith("/)\n"):
        read_start = False
        break

    # middle of list of gases
    if read_start:
        line_splt = line.strip().replace(" ","").replace("'","").replace("&","").split(',')
        gas_list.extend([s for s in line_splt if len(s) > 0])

absorber_id = {}
for i,g in enumerate(gas_list):
    absorber_id[g] = "%d"%(i+1)

# List of valid continuum combinations in SOCRATES/HITRAN
cia_pairs = [
    ["H2O","H2O"],
    ["H2","CH4"],
    ["H2","H2"],
    ["H2","H"],
    ["H2","He"],
    ["He","H"],
    ["N2","H2"],
    ["N2","He"],
    ["N2","N2"],
    ["N2","H2O"],
    ["O2","CO2"],
    # ["O2","N2"],      # this one shows some strange behaviour
    ["O2","O2"],
    ["CO2","CO2"],
    ["CO2","H2"],
    ["CO2","He"],
    ["CO2","CH4"],
    ["CO2","Ar"],
    ["CH4","He"]
]
