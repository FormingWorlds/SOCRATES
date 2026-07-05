# First SOCRATES run

This tutorial walks through computing thermal (longwave) radiative fluxes through a simple
single-column water-vapour atmosphere. By the end you will have:

- downloaded a PROTEUS spectral file,
- prepared it for use with SOCRATES,
- assembled a minimal set of atmospheric input files,
- run SOCRATES, and
- understood the output.

**Prerequisites:** SOCRATES installed with `RAD_DIR` set and the `FWL_DATA` environment variable set (see [Installation](../How-to/installation.md)). Make sure you also have a [working Python environment](../How-to/installation.md#set-up-a-python-environment-optional) with the necessary dependencies. 

!!! note "Spectral file used in this tutorial"
    We use **Frostflow-256**, a water-vapour-only file with 256 spectral bands from the
    DACE opacity database. For quick debugging runs, a 16-band version is available on
    [Zenodo](https://zenodo.org/records/15799743). For production work, the [4096-band version](https://zenodo.org/records/15799776) provides the highest resolution.

---

## 1. Download the spectral file

PROTEUS spectral files are hosted on Zenodo. Each spectral file and band count is a
separate record. Download Frostflow at 256 bands
(Zenodo record [10.5281/zenodo.15799754](https://doi.org/10.5281/zenodo.15799754)):

```bash
mkdir -p $FWL_DATA/spectral_files/Frostflow/256
cd $FWL_DATA/spectral_files/Frostflow/256

wget "https://zenodo.org/records/15799754/files/Frostflow.sf?download=1"   -O Frostflow.sf
wget "https://zenodo.org/records/15799754/files/Frostflow.sf_k?download=1" -O Frostflow.sf_k
```

---

## 2. Create a working directory

```bash
mkdir -p socrates_tutorial/out
cd socrates_tutorial
```

---

## 3. Prepare the spectral file

The downloaded spectral file needs a thermal source function (Block 6) added before it
can be used for longwave calculations. Copy it into your working directory first, then
modify the local copy, leaving the original in `$FWL_DATA` untouched. While in `socrates_tutorial`:

```bash
cp $FWL_DATA/spectral_files/Frostflow/256/Frostflow.sf   Frostflow.sf
cp $FWL_DATA/spectral_files/Frostflow/256/Frostflow.sf_k Frostflow.sf_k
```

Source the SOCRATES environment to put `prep_spec` on your path:

```bash
source $RAD_DIR/set_rad_env
```

Now add Block 6 (thermal source function, tabulated over 100–4000 K at 250 temperature
points). This uses the `prep_spec` utility interactively:

```bash
printf "%s\n" \
  "Frostflow.sf" \
  "a" \
  "6" \
  "n" \
  "T" \
  "100 4000" \
  "250" \
  "-1" \
  | prep_spec
```

What each input does:

| Input | Prompt | Meaning |
|-------|--------|---------|
| `$HOME/socrates_tutorial/Frostflow.sf` | File name | Full path to the local copy |
| `a` | Append or new? | Append to existing file |
| `6` | Block type | Block 6: thermal source function |
| `n` | Filter required? | No |
| `T` | Table or polynomial? | Tabulate |
| `100 4000` | Temperature range (K) | Covers cold stratospheres to magma ocean surfaces |
| `250` | Number of temperature points | Standard resolution |
| `-1` | Next block | Write file and exit |

Set a shell variable pointing to the prepared spectral file:

```bash
SPECTRUM=Frostflow.sf
N_BANDS=256
```

---

## 4. Prepare the atmospheric input files

SOCRATES reads the atmospheric state from a set of netCDF files that share a common
**basename** and differ only by their suffix. Here we use the basename `atm`.

The atmosphere is divided into N homogeneous layers, bounded by N+1 levels. Layer
mid-point values go into most files; level-edge temperatures go into `.tl`.

We will set up a 10-layer hot steam atmosphere, the kind of conditions relevant to a
post-magma-ocean planet.

### 4.1 Install dependencies

If you have not yet installed the necessary Python dependencies:

```bash
pip install -r "$RAD_DIR/python/requirements.txt"
```

### 4.2 Write the input script

Save the following as `make_inputs.py` in `socrates_tutorial/`:

```python
import sys
import os
import numpy as np
import f90nml

# Import netCDF helpers from SOCRATES
sys.path.insert(0, os.path.join(os.environ['RAD_DIR'], 'python'))
from nctools import ncout_surf, ncout2d, ncout3d

BASENAME = "out/atm"

# --- Atmosphere structure ---
N_LAYERS = 10
p_surf = 1.0e7   # Pa  (100 bar)
p_top  = 1.0e2   # Pa  (1 mbar)
p_mid  = np.logspace(np.log10(p_surf), np.log10(p_top), N_LAYERS)

T_surf = 1500.0  # K
T_top  = 200.0   # K
t_mid  = np.linspace(T_surf, T_top, N_LAYERS)

# Level-edge values (N+1)
p_lev = np.concatenate([[p_surf * 1.05],
                         0.5 * (p_mid[:-1] + p_mid[1:]),
                         [p_top * 0.95]])
t_lev = np.interp(p_lev, p_mid[::-1], t_mid[::-1])[::-1]

# H2O mass mixing ratio: pure steam
h2o = np.ones(N_LAYERS)

# --- Write input files ---
ncout3d(f"{BASENAME}.t",  0, 0, p_mid, t_mid, 't',  longname="Temperature", units='K')
ncout3d(f"{BASENAME}.tl", 0, 0, p_lev, t_lev, 'tl', longname="Temperature", units='K')
ncout3d(f"{BASENAME}.p",  0, 0, p_mid, p_mid, 'p',  longname="Pressure",    units='Pa')
ncout3d(f"{BASENAME}.q",  0, 0, p_mid, h2o,   'q',  longname="q",           units='kg/kg')

ncout2d(f"{BASENAME}.tstar", 0, 0, T_surf, 'tstar', longname="Surface Temperature", units='K')
ncout2d(f"{BASENAME}.pstar", 0, 0, p_surf, 'pstar', longname="Surface Pressure",    units='Pa')
ncout_surf(f"{BASENAME}.surf", 0, 0, 1, 0.0)

# Planetary namelist — SOCRATES uses Earth defaults without this
nml = {
    'socrates_constants': {
        'planet_radius':  6.371e6,   # m
        'grav_acc':       9.81,      # m s-2
        'mol_weight_air': 0.018,     # kg mol-1  (pure H2O)
        'r_gas_dry':      462.0,     # J kg-1 K-1
        'cp_air_dry':     1996.0,    # J kg-1 K-1
    }
}
f90nml.write(nml, f"{BASENAME}.nml")

print("Input files written:")
for f in sorted(os.listdir("out")):
    if f.startswith("atm."):
        print(f"  out/{f}")
```

Run it:

```bash
python make_inputs.py
```

You should see eight files under `out/`: `out/atm.nml`, `out/atm.p`, `out/atm.pstar`, `out/atm.q`, `out/atm.surf`,
`out/atm.t`, `out/atm.tl`, `out/atm.tstar`.

---

## 5. Run SOCRATES

Run the longwave calculation, writing all output to the `out/` subdirectory:

```bash
Cl_run_cdf \
  -B out/atm \
  -s $SPECTRUM \
  -R 1 $N_BANDS \
  -ch $N_BANDS \
  -I \
  -g 2 \
  -C 5 \
  -u \
  -N out/atm.nml
```

| Option | Meaning |
|--------|---------|
| `-B out/atm` | Basename: output files written to `out/` with prefix `atm` |
| `-s $SPECTRUM` | Path to the prepared spectral file |
| `-R 1 $N_BANDS` | Use spectral bands 1 to N_BANDS |
| `-ch $N_BANDS` | Number of channels (must match `-R`) |
| `-I` | Solve for thermal (longwave) source |
| `-g 2` | Correlated-k gas overlap |
| `-C 5` | Cloud scheme 5 (clear-sky — no cloud input files needed) |
| `-u` | Write upward flux output files |
| `-N out/atm.nml` | Namelist file with planetary parameters |

If the run succeeds you will see a short diagnostic summary printed to the terminal.

---

## 6. Inspect the output

SOCRATES writes one netCDF output file per flux quantity under `out/`. These are NetCDF files, although their file extensions are different. Each file also contains the wavelengths of each spectral band, and the pressure grid used.

| File | Contents |
|------|----------|
| `out/atm.uflx` | Upward flux (W m$^{-2}$) |
| `out/atm.dflx` | Diffuse downward flux (W m$^{-2}$) |
| `out/atm.vflx` | Total downward flux (W m$^{-2}$) |
| `out/atm.nflx` | Net downward flux (W m$^{-2}$) |
| `out/atm.hrts` | Heating rates (K day$^{-1}$) |

Read and plot the upward flux profile by pasting the following code in `plot.py`:

```python
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np

# Open the NetCDF file
ds = nc.Dataset("out/atm.uflx")

# Read the spectral upward-longwave fluxes at each layer
spec_flux = ds.variables["uflx"][:, :, 0, 0]

# Sum over all spectral bands to get bolometric flux
bolo_flux = np.sum(spec_flux, axis=0)

# Read pressure grid
pres = ds.variables["plev"][:]

# close the file
ds.close()

# Make the plot of flux versus pressure (i.e. height)
plt.figure(dpi=300)
plt.plot(bolo_flux, pres / 1e5, "b-o")
plt.gca().invert_yaxis()
plt.yscale("log")
plt.xlabel(r"Upward flux (W m$^{-2}$)")
plt.ylabel("Pressure (bar)")
plt.title(r"Upward bolometric longwave flux, Frostflow-256, pure H$_2$O")
plt.tight_layout()
plt.savefig("out/flux_profile.pdf", bbox_inches="tight")

# Print the outgoing longwave radiation flux
olr = bolo_flux[0]
print(f"OLR: {olr:.1f} W/m^2")

plt.show()
```

Then:

```bash
python plot.py
```

The upward flux at the top of atmosphere is the **outgoing longwave radiation (OLR)**, 
the rate at which the atmosphere thermally emits radiation energy to space.

---

## 7. Next steps

- **Add more gases.** Supply `.co2`, `.n2` etc. files and use a multi-gas spectral file
  such as Dayspring or Honeyside.
- **Add a stellar source.** Run with `-S` instead of `-I`, supplying `.stoa`, `.szen`,
  and `.sazim` input files.
- **Change planetary parameters.** Edit `atm.nml` to set the correct gravity, radius,
  and molecular weight for your target planet.
- **Increase resolution.** The 4096-band Frostflow provides higher-resolution results.

For information on all available spectral files and their absorbers, see
[PROTEUS spectral files](../Reference/proteus_spectral_file_reference.md).