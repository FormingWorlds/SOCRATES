
# SOCRATES
**S**uite **O**f **C**ommunity **RA**diative **T**ransfer codes based on **E**dwards and **S**lingo.     

Rehosted from the original Met Office source [1] with modifications by Harrison Nicholls.

### Contents
0. Licence
1. What's included?
2. [Omitted in this redistribution of the code]
3. Compiling the source code externally
4. Compilation of scripts in sbin
5. Running the code
6. Tested compilers
7. Contributors


--------------------------------

### 0) BSD 3-Clause licence

(C) Crown copyright Met Office. All rights reserved.    
For further details please refer to the file COPYRIGHT.txt which you should have received as part of this distribution.


### 1) What's included?

`src/` contains the source code in Fortran 95 (.f90) and a few remaining in Fortran 77 (.f).

`make/` contains the Makefile which then accesses the various `Mk_*` files.

`sbin/` contains scripts that can be used to run the fortran routines.

`man/` contains man pages for scripts in sbin/. For example, running `man Cl_run_cdf` will give options for that script. 

`examples/` and `data/` provide test input for the radiation code. See the CONTENTS in each directory under `examples/` for instructions.

`idl/` and `python/` contain scripts to generate atmospheric profiles etc in netCDF format to be used as input for the radiation code (`l_run_cdf`).

`docs/` contain the user guide and technical guide for the ES code.

`spectraltools/` contains new addons to the code which allow for streamlined and flexible creation of spectral files from precomputed cross-sections.

### 3) Compiling the source code externally

The following commands can be run to build the suite and setup your path to the executables and man pages:

1. `./configure`   
2. `./build_code`             
3. `source ./set_rad_env`      


### 4) Compilation of scripts in sbin

There are a small number of utilities in `sbin/` which are written in C and require compilation. A Makefile has been provided:

1. `cd $RAD_SCRIPT`
2. `make`


### 5) Running the code

Once you have set your path to the man pages (see section 2/3) you can find up-to-date instructions for running the following routines:

Two-stream and spherical harmonics radiance codes using netCDF or text CDL input files:

* `man Cl_run_cdf`
* `man Cl_run_cdl`

A Mie scattering code for determining optical properties of aerosol and cloud particles:

* `man Cscatter`

A correlated-k code for the calculation of gaseous absorption coefficients for the spectral files either directly from HITRAN .par or .xsc databases or line-by-line absorption coefficients in a netCDF input file:

* `man Ccorr_k`

Auxillary routines for format conversion, interpolation etc:

* `man Ccdf2cdl`
* `man Ccdl2cdf`
* `man Cinterp`

These scripts are a command line interface to interactive routines in the `bin/` directory. These routines may be run directly if desired (eg. l_run_cdf).

It is very useful to study the examples/ directory for common usage of the code.


### 6) Tested compilers

The full suite has been tested with the following compilers:
* Intel ifort 17.0.7    
* GCC gfortran 9.4.0

### 7) Contributors

Significant contributors include:
* J. Edwards
* A. Slingo
* J. Manners

### 8) Adding a new gas

This has to be done manually and will require editing a lot of files. The easiest thing to 
do is to search for the gas "ho2no2" across all files and copy what you see. Always add
new gases to the end of the existing lists. This will require changing function calls and 
various hardcoded arrays and variable names. You should expect to change these files:
* `julia/src/SOCRATES_C.f90`
* `julia/src/SOCRATES.jl`
* `spectraltools/src/phys.py`
* `spectraltools/src/utils.py`
* `src/interface_core/socrates_set_spectrum.F90`
* `src/modules_gen/input_head_pcf.f90`
* `src/radiance_core/def_control.F90`
* `src/radiance_core/gas_list_pcf.F90`


### References
* [1]  https://code.metoffice.gov.uk/trac/socrates
* [2]  https://doi.org/10.1002/qj.49712253107
* [3]  https://doi.org/10.1051/0004-6361/201323169
* [4]  https://doi.org/10.5194/gmd-16-5601-2023
