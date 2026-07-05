
# Socrates - Suite Of Community RAdiative Transfer codes based on Edwards and Slingo

<a href="https://github.com/FormingWorlds/SOCRATES/actions/workflows/docs.yaml"><img alt="Documentation" src="https://github.com/FormingWorlds/SOCRATES/actions/workflows/docs.yaml/badge.svg"></a>
<a href="https://github.com/FormingWorlds/SOCRATES/blob/main/LICENCE"><img alt="License: BSD-3-Clause" src="https://img.shields.io/badge/License-BSD--3--Clause-blue.svg"></a>

SOCRATES is a high-performance radiative transfer code for computing fluxes, heating rates, and radiances in planetary atmospheres. Its primary development and maintenance is lead by the UK Met Office. This fork of SOCRATES is applied as the radiative transfer core of the [PROTEUS framework](https://proteus-framework.org/PROTEUS/), called by the radiative-convective atmosphere model [AGNI](https://www.h-nicholls.space/AGNI/).

## Documentation

Please visit the [documentation website](https://proteus-framework.org/SOCRATES/) for installation instructions, a tutorial, reference information and a model overview. Additionally, the latest documentation PDFs built by GitHub Actions are available from the
[Build docs PDFs workflow artifacts](https://github.com/FormingWorlds/SOCRATES/actions/workflows/build-docs-pdf.yaml).

## What's included?

The Socrates package contains the following directories:
src/ make/ data/ examples/ idl/ python/ man/ sbin/ docs/

`src/` contains the source code in Fortran 2018 (.f90) and a few remaining
in fixed Fortran format (.f).

`make/` contains the Makefile which then accesses the various Mk_*
files.

`sbin/` contains scripts that can be used to run the fortran routines.

`man/` contains man pages for scripts in sbin/. For example, running
`man Cl_run_cdf` will give options for that script.

`examples/` and `data/` provide test input for the radiation code.
See the CONTENTS in each directory under examples/ for instructions.

`idl/` and `python/` contain scripts to generate atmospheric profiles etc
in netCDF format to be used as input for the radiation code (l_run_cdf).

`docs/` contain documentation, as well as the user guide and technical guide for the Socrates code.

## Standalone install

1. Clone SOCRATES from GitHub:
   ```bash
   git clone https://github.com/FormingWorlds/SOCRATES.git
   ```
2. Change into the new directory:
   ```bash
   cd SOCRATES
   ```
3. Configure the installation:
   ```bash
   ./configure
   ```
4. Compile the code:
   ```bash
   ./build_code
   ```

### Setting `RAD_DIR`

SOCRATES needs the location of its root directory, referred to as `RAD_DIR`, available as
an environment variable. Run the following commands from inside the SOCRATES directory.

To set this temporarily, for the current terminal session only:

```bash
export RAD_DIR=$(pwd)
```

To set this permanently:

**Bash**:
```bash
echo "export RAD_DIR=$(pwd)" >> ~/.bashrc
source ~/.bashrc
```

**Zsh**:

```bash
echo "export RAD_DIR=$(pwd)" >> ~/.zshrc
source ~/.zshrc
```

### Compilation of scripts in sbin

There are a small number of utilities in sbin/ which are written
in C and require compilation. A Makefile has been provided:

`cd $RAD_SCRIPT`\
`make`

## Running the code

Set up your path to the executables and man pages:

```
source $RAD_DIR/set_rad_env
```

Then find up-to-date instructions for running the following routines:

1. Two-stream and spherical harmonics radiance codes using netCDF or text CDL input files:

   `man Cl_run_cdf`\
   `man Cl_run_cdl`

2. A Mie scattering code for determining optical properties of aerosol and cloud particles:

   `man Cscatter`

3. A correlated-k code for the calculation of gaseous absorption coefficients for the spectral files either directly from HITRAN .par or .xsc databases or line-by-line absorption coefficients in a netCDF input file:

   `man Ccorr_k`

4. Auxillary routines for format conversion, interpolation etc:

   `man Ccdf2cdl`\
   `man Ccdl2cdf`\
   `man Cinterp`

These scripts are a command line interface to interactive routines in
the bin/ directory. These routines may be run directly if desired (eg.
l_run_cdf).

It is useful to study the examples/ directory for common usage
of the code, or follow the python-based [tutorial](https://proteus-framework.org/SOCRATES/Tutorials/first_run.html) on the documentation website.

## Tested compilers

The full suite has been tested with the following compilers:

Intel ifort 19\
GCC gfortran 12.2

To use these compilers within the Met Office run, respectively:\
`./build_code azure_ifort19`\
`./build_code azure_gfortran12`

On the Monsoon3 collaboration machine:\
`./build_code monsoon3_gfortran12`


## Adding a new gas

This has to be done manually and will require editing a lot of files. The easiest thing to do is to search for the gas "ho2no2" across all files and copy what you see. Always add new gases to the end of the existing lists. This will require changing function calls, various hardcoded arrays and variables. You should expect to edit these files:
* `julia/src/SOCRATES_C.f90`
* `julia/src/SOCRATES.jl`
* `spectraltools/src/phys.py`
* `spectraltools/src/utils.py`
* `src/interface_core/socrates_set_spectrum.F90`
* `src/modules_gen/input_head_pcf.f90`
* `src/modules_gen/refract_re_ccf.f90`
* `src/radiance_core/def_control.F90`
* `src/radiance_core/gas_list_pcf.F90`

You should also make sure to avoid the 'lazy' way to extend FORTRAN arrays where remaining values are filled in bulk, because the `generate_wrappers.jl` script will not be able to parse the FORTRAN source code.

## References

All references can be found in the [bibliography](https://proteus-framework.org/SOCRATES/Reference/publications.html) on the documentation website. 
