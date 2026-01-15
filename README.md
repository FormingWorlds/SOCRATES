
# Socrates - Suite Of Community RAdiative Transfer codes based on Edwards and Slingo

## Contributing Guidelines

Welcome!

The following links are here to help set clear expectations for everyone
contributing to this project. By working together under a shared understanding,
we can continuously improve the project while creating a friendly, inclusive
space for all contributors.

### Contributors Licence Agreement

Please see the
[Momentum Contributors Licence Agreement](https://github.com/MetOffice/Momentum/blob/main/CLA.md)

Agreement of the CLA can be shown by adding yourself to the CONTRIBUTORS file
alongside this one, and is a requirement for contributing to this project.

### Code of Conduct

Please be aware of and follow the
[Momentum Code of Coduct](https://github.com/MetOffice/Momentum/blob/main/docs/CODE_OF_CONDUCT.md)

### Working Practices

This project is managed as part of the Simulation Systems group of repositories.

Please follow the Simulation Systems
[Working Practices.](https://metoffice.github.io/simulation-systems/index.html)

Questions are encouraged in the Simulation Systems
[Discussions.](https://github.com/MetOffice/simulation-systems/discussions)

Please be aware of and follow the Simulation Systems
[AI Policy.](https://metoffice.github.io/simulation-systems/FurtherDetails/ai.html)

## Contents
0. Licence
1. What's included?
2. Compiling the source code externally
3. Running the code
4. Tested compilers
5. Contributors
6. Adding a new gas


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

`docs/` contain the user guide and technical guide for the Socrates code.

`spectraltools/` contains new addons to the code which allow for streamlined and flexible creation of spectral files from precomputed cross-sections.

### 2) Compiling the source code externally

The following commands can be run to build the suite and setup your path to the executables and man pages:

1. `./configure`   
2. `./build_code`             
3. `source ./set_rad_env`      

### 3) Running the code

Once you have set your path to the man pages (see section 2/3) you can find up-to-date instructions for running the following routines:

Two-stream and spherical harmonics radiance codes using netCDF or text CDL input files:

* `man Cl_run_cdf`
* `man Cl_run_cdl`

A Mie scattering code for determining optical properties of aerosol and cloud particles:

* `man Cscatter`

A correlated-k code for the calculation of gaseous absorption coefficients for the spectral files either directly from HITRAN .par or .xsc databases or line-by-line absorption coefficients in a netCDF input file:

For external users it should only be necessary to edit the file
make/Mk_cmd to allow compilation of the code on your system. FORTCOMP
and LINK can be changed to your local Fortran compiler. To use the netCDF
routines you must also change INCCDF_PATH and LIBCDF_PATH to point to
your local netCDF installation.

The following commands can then be run to build the suite and setup
your path to the executables and man pages:

`./build_code`\
`. ./set_rad_env`

See previous section for building individual routines.

### Compilation of scripts in sbin

There are a small number of utilities in sbin/ which are written
in C and require compilation. A Makefile has been provided:

`cd $RAD_SCRIPT`\
`make`

### Running the code

Once you have set your path to the man pages (see section 2/3) you can
find up-to-date instructions for running the following routines:

Two-stream and spherical harmonics radiance codes using netCDF or
text CDL input files:

`man Cl_run_cdf`\
`man Cl_run_cdl`

A Mie scattering code for determining optical properties of aerosol
and cloud particles:

`man Cscatter`

A correlated-k code for the calculation of gaseous absorption
coefficients for the spectral files either directly from HITRAN
.par or .xsc databases or line-by-line absorption coefficients in
a netCDF input file:

`man Ccorr_k`

Auxillary routines for format conversion, interpolation etc:

`man Ccdf2cdl`\
`man Ccdl2cdf`\
`man Cinterp`

These scripts are a command line interface to interactive routines in the `bin/` directory. These routines may be run directly if desired (eg. l_run_cdf).

It is very useful to study the examples/ directory for common usage of the code.


### 4) Tested compilers

The full suite has been tested with the following compilers:
* Intel ifort 17.0.7    
* GNU gfortran 9.4.0


## Adding a new gas

This has to be done manually and will require editing a lot of files. The easiest thing to 
do is to search for the gas "ho2no2" across all files and copy what you see. Always add
new gases to the end of the existing lists. This will require changing function calls, 
various hardcoded arrays and variables. You should expect to edit these files:
* `julia/src/SOCRATES_C.f90`
* `julia/src/SOCRATES.jl`
* `spectraltools/src/phys.py`
* `spectraltools/src/utils.py`
* `src/interface_core/socrates_set_spectrum.F90`
* `src/modules_gen/input_head_pcf.f90`
* `src/radiance_core/def_control.F90`
* `src/radiance_core/gas_list_pcf.F90`


## References
* [1]  https://code.metoffice.gov.uk/trac/socrates
* [2]  https://doi.org/10.1002/qj.49712253107
* [3]  https://doi.org/10.1051/0004-6361/201323169
* [4]  https://doi.org/10.5194/gmd-16-5601-2023
