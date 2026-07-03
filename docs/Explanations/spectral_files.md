# Spectral files

!!! info "Based on technical guide"
    This overview is based on the SOCRATES technical guide by James Manners, John M. Edwards, Peter Hill & Jean-Claude Thelen (Met Office, 2017), which can be found [here](../Reference/documentation_pdfs.md#technical-guide). It is under Crown Copyright.

## Overview

Atmospheric radiative transfer spans an enormous range of frequencies, across which gaseous absorption coefficients vary by many orders of magnitude. The approach adopted in SOCRATES, and in general circulation models (GCMs) broadly, is to divide the solar or infra-red spectral region into a number of **bands**, across which all radiative quantities except gaseous absorption coefficients may be treated as uniform. More bands give more accuracy, but at greater computational cost; the appropriate balance depends on the application.

A key design choice in SOCRATES is that the frequency discretisation is not fixed in the code itself. Instead, it is set by an external file supplied at runtime: the **spectral file**. This separates the physical parametrisation data from the radiation solver, making the code flexible and easy to update. A spectral file generated for one version of SOCRATES remains compatible with future versions (though not necessarily the reverse, as new functionality may add new data blocks).

---

## Role of the spectral file

The spectral file serves as the single source of truth for all spectrally dependent data used by the radiation code. This includes:

- The number and limits of spectral bands
- The gaseous absorbers active in each band and their absorption data
- Rayleigh scattering coefficients
- Planck function polynomial fits (longwave only)
- Parametrisations for the single-scattering properties of cloud droplets, ice crystals, and aerosols
- Continuum absorption coefficients

Because parametrisations that require spectrally dependent data can only be selected if such data are present in the spectral file, **the choice of spectral file determines which physical parametrisations are available** at runtime. Spectral files should therefore be selected with care to match the intended configuration.

!!! warning "Modidying spectral files"
    Generating or modifying spectral files requires detailed knowledge of radiative transfer. Standard files are provided for common configurations; users should not modify these unless they have the necessary expertise.

---

## Spectral bands

The spectral region is divided into bands within which all radiative quantities (except gaseous absorption coefficients) are treated as frequency-independent. The total flux is the sum of partial fluxes over bands (see [Two-stream radiation code](two_stream.md#spectral-integration)).

In some shortwave spectral files, certain bands share the same wavelength limits. These are **not true spectral bands**: they represent a computational splitting for efficiency, and only the sum of fluxes across such paired bands is physically meaningful. The excluded sub-ranges are specified in block 14 (see below).

---

## Block structure

The spectral file is organised into numbered **blocks**, each corresponding to a different category of physical data. The flag `l_present(i)` is set to `.TRUE.` if block `i` is present; not all blocks are required for all calculations.

| Block | Contents | Notes |
|---|---|---|
| 0 | Number and identities of gaseous and aerosol species | Gases indexed by type number from `gas_list_pcf`; aerosols from `rad_pcf` |
| 1 | Spectral band limits (wavelengths in metres) | Some bands may share limits, see split bands below |
| 2 | Fraction of solar spectrum in each band | Shortwave only |
| 3 | Rayleigh scattering coefficients | Shortwave only |
| 4 | List of gaseous absorbers active in each band | First gas listed must be the primary absorber |
| 5 | k-distribution fits to gaseous transmissions | Includes scaling functions or look-up tables |
| 6 | Polynomial fit to the Planck function in each band | Longwave only |
| 7 | *(Obsolete, not present in current files)* | — |
| 8 | List of continuum absorbers in each band | Primarily self- and foreign-broadened water vapour continua |
| 9 | Continuum absorption coefficients | — |
| 10 | Single-scattering parametrisations for cloud droplets | May contain multiple types; valid size range recorded |
| 11 | Aerosol optical properties | Selection varies by file; hygroscopic aerosols include humidity dependence via look-up table |
| 12 | Single-scattering parametrisations for ice crystals | May contain multiple types; valid size range recorded |
| 13 | Heuristic Doppler broadening adjustments | Longwave only; obsolescent, will move to block 5 |
| 14 | Band exclusions (split bands) | Defines sub-ranges excluded from a band's limits |
| 15 | Monochromatic aerosol absorption/scattering coefficients | At specific wavelengths, for aerosol optical depth diagnostics |

### Gaseous absorption (block 5)

Gaseous absorption data are stored as **k-distribution** fits. For each active gas in each band, absorption coefficients are either:

- **Scaled** from a reference value using a pressure- and temperature-dependent scaling function (two functional forms are supported; see [Two-stream radiation code](two_stream.md#gaseous-absorption)), or
- **Interpolated** directly from a look-up table of coefficients at a grid of pressures and temperatures, now the preferred approach.

The first gas listed in block 4 for each band is the **primary absorber**; minor gases may be treated via the equivalent extinction approximation rather than full random overlap.

### Cloud and ice parametrisations (blocks 10 and 12)

Blocks 10 and 12 may contain data for **multiple types** of droplet or ice crystal parametrisation within a single file. The term *type* is deliberately flexible; different types may represent:

- Different assumed size distributions
- Different spectral averaging methods (thin or thick averaging)
- Different crystal shapes (for ice)
- Different fitting functions (linear, Padé approximants, polynomial)

Type numbers are supplied at runtime and must be chosen to match the spectral file in use. The minimum and maximum particle sizes for which each parametrisation is valid are recorded alongside the coefficients.

### Split bands (block 14)

In some files, a band's wavelength limits in block 1 encompass a wider range than is actually used, with a sub-range **excluded** by listing it in block 14. For example, if band 5 spans 8–12 µm but band 6 spans 10–11 µm and is excluded from band 5, then band 5 effectively covers 8–10 µm and 11–12 µm. Split bands are used purely for computational efficiency and are transparent to the solver.

---

## Naming conventions

Although not formally required, a consistent naming convention is used for standard files:

| Prefix | Format | Description |
|---|---|---|
| `sp_sw_` | Text | Shortwave file, UM version ≥ 8.6 or offline code |
| `sp_lw_` | Text | Longwave file, UM version ≥ 8.6 or offline code |
| `spec3a_sw_` | Namelist | Shortwave file, UM version ≤ 8.5 |
| `spec3a_lw_` | Namelist | Longwave file, UM version ≤ 8.5 |

When new functionality is added to a file without changing existing results, the **filename is unchanged**. When existing data are modified (changing results), a **new filename** is introduced so that older configurations remain reproducible.

Two utility programs handle format conversion between namelist and text formats: `nml_spec` (text → namelist) and `spec_nml` (namelist → text).

---

## Generating and modifying spectral files

Spectral files are generated using the **pre-processing suite** of the offline Edwards–Slingo radiation code. Generation requires expertise in radiative transfer.

When a new requirement arises (e.g. adding a new absorbing gas, updating continuum data, or incorporating a new aerosol type), users should contact the radiation group rather than modifying files independently. Aerosol optical property data in particular are generated in consultation with aerosol modelling specialists.

!!! note
    Standard spectral files for common configurations are provided in the SOCRATES repository. A reference description of these files is given in the [reference section](../Reference/spectral_file_reference.md).
