
# SOCRATES
**S**uite **O**f **C**ommunity **RA**diative **T**ransfer codes based on **E**dwards and **S**lingo.     

Rehosted from the original MetOffice source with modifications by Harrison Nicholls.

Contents:

0. Licence
1. What's included?
2. [Omitted in this redistribution of the code]
3. Compiling the source code externally
4. Compilation of scripts in sbin
5. Running the code
6. Tested compilers
7. Reporting bugs and receiving updates


### 0) BSD 3-Clause licence

(C) Crown copyright Met Office. All rights reserved.
For further details please refer to the file COPYRIGHT.txt
which you should have received as part of this distribution.


### 1) What's included?

You should have received this package as a tar file containing the
directories: src/ make/ data/ examples/ idl/ python/ man/ sbin/ docs/

src/ contains the source code in Fortran 95 (.f90) and a few remaining 
in Fortran 77 (.f).

make/ contains the Makefile which then accesses the various Mk_*
files.

sbin/ contains scripts that can be used to run the fortran routines.

man/ contains man pages for scripts in sbin/. For example, running
'man Cl_run_cdf' will give options for that script. 

examples/ and data/ provide test input for the radiation code. 
See the CONTENTS in each directory under examples/ for instructions.

idl/ and python/ contain scripts to generate atmospheric profiles etc
in netCDF format to be used as input for the radiation code (l_run_cdf).

docs/ contain the user guide and technical guide for the ES code.

### 3) Compiling the source code externally

For external users it should only be necessary to edit the file
make/Mk_cmd to allow compilation of the code on your system. FORTCOMP
and LINK can be changed to your local Fortran compiler. To use the netCDF
routines you must also change INCCDF_PATH and LIBCDF_PATH to point to
your local netCDF installation.

The following commands can then be run to build the suite and setup
your path to the executables and man pages:

`./build_code`
`ksh2bash.sh`
`. ./set_rad_env`

See section 2 for building individual routines.


### 4) Compilation of scripts in sbin

There are a small number of utilities in sbin/ which are written 
in C and require compilation. A Makefile has been provided:

`cd $RAD_SCRIPT`
`make`


### 5) Running the code

Once you have set your path to the man pages (see section 2/3) you can 
find up-to-date instructions for running the following routines:

Two-stream and spherical harmonics radiance codes using netCDF or
text CDL input files:

`man Cl_run_cdf`
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

`man Ccdf2cdl`
`man Ccdl2cdf`
`man Cinterp`

These scripts are a command line interface to interactive routines in
the bin/ directory. These routines may be run directly if desired (eg.
l_run_cdf).

It is very useful to study the examples/ directory for common usage
of the code.


### 6) Tested compilers

The full suite has been tested with the following compilers:

Intel ifort 17.0.7
GCC gfortran 8.1.0

To use these compilers within the Met Office run, respectively:
`./build_code ifort`
`./build_code gfortran`

