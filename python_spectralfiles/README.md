# Python SpectralFile tools

This subdirectory is not part of the original SOCRATES repository. It is distributed under the 3-Clause BSD License.


### Overview

Computing k-coefficients from a line-list is very slow, because there can be a very large number of lines for a single molecule. To speed this up, it's easier to split the process into two steps:
1. Calculating cross-sections from a line-list (at line resolution).    
2. Calculating k-coefficients from the cross-sections (at a lower resolution).    

Since step 1 is by far the slowest part, it is ideal to use pre-computed opacities. These tools aims to generalise the creation of SpectralFiles from pre-computed opacity tables by converting them into a common NetCDF format. These NetCDF files can then be read by SOCRATES for generating SpectralFiles with the required properties.

You will need to download the source cross-sections manually.

### Content

| Tool                  | Usage     |
|-----------------------|-----------|
| `dace2netcdf`         | Convert DACE binary files into a NetCDF format   | 
| `exomol2netcdf`       | Convert ExoMol sigma files into a NetCDF format  |
| `hitran2netcdf`       | Convert HITRAN xsc files into a NetCDF format    |
| `wizard`              | Interactive wizard for generating spectral files |


### Requirements

* SOCRATES
   - Must have been compiled
   - Executables have been added to your `PATH` using `set_rad_env`
* Python (version 3.12) and its libraries
   - numpy
   - matplotlib
   - netcdf4

### Online sources
* ExoMol (https://exomol.com/data/data-types/xsec/)
* DACE (https://dace.unige.ch/opacityDatabase/)
* HITRAN (https://hitran.org/xsc/)


