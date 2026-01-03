# SpectralFile tools

This subdirectory is not part of the original SOCRATES repository. It is distributed under the 3-Clause BSD License.

### Overview

Computing k-coefficients from a line-list is very expensive because there can be a large number of transitions for a single molecule. To speed this up, it is useful to split the process into two steps:
1. Calculating cross-sections from a line-list (at line resolution).
2. Calculating k-coefficients from the cross-sections (at a lower resolution).

Step 1 is by far the slowest, so it is helpful to use pre-computed opacities. These tools aim to generalise the creation of SpectralFiles from pre-computed opacity tables by converting them into a common netCDF format. These netCDF files can then be read by SOCRATES when generating SpectralFiles with the required properties.

**You will need to download the source cross-sections yourself**. For a given database (`db`) and absorber (`ab`), the files should be placed in the directory `data/db/ab/`. All output files will be written to `output/`, which **you will also need to create yourself** or create a symbolic link called `output` which points to another extant location. The tools are primarily targeted at parsing cross-sections from DACE, with other databases partially supported for comparison purposes. It is recommended that you download cross-sections using the `Tinterpolate_dace.py` tool, and then generate spectral files using `Tmake_spectralfile.py`.

These tools all operate by storing the spectral absorption cross-section (versus wavenumber) of an absorber (at a given temperature and pressure) in an `xsec` Python object. This is defined in `src/cross.py`. The various sources can be loaded into this object, and then written as a netCDF, plotted, or otherwise manipulated as required.

**Ultraviolet range**. It is possible to enable the option that takes into consideration the ultraviolet range in the making of the spectral files (`Tmake_spectralfile.py` enable UV = True). **You will need to upload the cross-sections and wavenumbers (same file) for each molecule yourself**. The folder should be named as moleculesUV. It's required to have a resolution of 0.01cm-1 in order to match the resolution socrates uses. If you are using DACE files for longer wavelengths, make sure that your ultraviolet files end where DACE starts (if there is not enough data, negligible values can be used).

**Plotting**. For every molecule, a plot is created with wavelength in the x-axis and cross-section in the y-axis. It can be changed by modifying the xaxis (`Tmake_spectralfile.py`).

### Content

| Tool                     | Description   |
|--------------------------|---------------|
| `Tmake_spectralfile.py`  | Generate a spectral file for the specified absorbers and wavenumber/pressure/temperature range |
| `Tconvert_dace.py`       | Convert DACE binary files into the netCDF format for the specified absorber   |
| `Tdownload_cia.py`       | Download CIA databases from the HITRAN website into `data/cia/` |
| `Tplot_absorption.py`    | Plot absorption cross-section versus wavenumber  |
| `Tcalc_checksum.py`      | Calculate the BLAKE2b checksum of a file in order to verify its integrity  |
| `Tinterpolate_dace.py`   | Download interpolated cross-sections from DACE at the requested pressure/temperature values  |
| `Tclean_output.py`       | Clean output directory, retaining netCDF files for future use (use --help for info)  |


### Requirements

* SOCRATES
   - Must have been compiled
   - Executables have been added to your `PATH` variable using `. ./set_rad_env`
* Python (version >= 3.11) and the following libraries
   - numpy
   - netcdf4
   - glob
   - shutil
   - requests
   - hashlib
   - matplotlib
   - dace-query
   - h5py

### Online sources
* DACE (https://dace.unige.ch/opacityDatabase/)
* ExoMol (https://exomol.com/data/data-types/xsec/)
* HITRAN (https://hitran.org/xsc/)
* HITRAN CIA (https://hitran.org/cia/)
* MT_CKD H2O (https://github.com/AER-RC/MT_CKD_H2O)

