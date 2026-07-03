# Standard spectral files

!!! note
    The spectral files described here are the **standard Met Office files** distributed with SOCRATES, originally developed for use in the Unified Model (UM) and associated climate configurations. They are described in detail in the technical guide by James Manners, John M. Edwards, Peter Hill & Jean-Claude Thelen (Met Office, 2017), found [here](documentation_pdfs.md#technical-guide). 

---

## Overview

Standard spectral files are provided for four major model configurations, each with separate shortwave (SW) and longwave (LW) files. Files with names beginning `sp_` are readable text format for use with UM version ≥ 8.6 or the offline code; files beginning `spec3a_` are namelist format for UM version ≤ 8.5.

| Configuration | SW file | LW file(s) |
|---|---|---|
| Global Atmosphere 7 | `sp_sw_ga7` | `sp_lw_ga7` |
| Global Atmosphere 3 | `sp_sw_ga3_0` | `sp_lw_ga3_0`, `sp_lw_ga3_1` |
| HadGEM2 | `spec3a_sw_hadgem1_5o_rlfx` | `spec3a_lw_hadgem1_5C` |
| HadGEM1 | `spec3a_sw_hadgem1_3` | `spec3a_lw_hadgem1_3` |

Older files for HadCM3, HadAM4, and the mesoscale model are also distributed; see the technical guide for their full descriptions.

---

## Global Atmosphere Configuration 7

### `sp_sw_ga7`

Sections are identical to `sp_sw_ga3_0` except for changes to the spectral bands, solar spectrum (including Rayleigh coefficients), and gaseous absorption.

**Spectral bands:**

| Band | Wavelength (nm) |
|---|---|
| 1 | 200 – 320 |
| 2 | 320 – 505 |
| 3 | 505 – 690 |
| 4 | 690 – 1190 |
| 5 | 1190 – 2380 |
| 6 | 2380 – 10000 |

The six bands are identical to `sp_sw_ga3_0` except that the combined bands 2 and 3 are now properly split into two true bands at 505 nm.

**Solar spectrum:** "Lean 12", a mean over 2000–2011 from the SPARC/SOLARIS group recommendation [^cite-Lean00], with associated updates to Rayleigh scattering coefficients.

**Gaseous absorption:** Newly derived for all gases using HITRAN 2012 [^cite-HITRAN] and the CAVIAR water vapour continuum. Absorption coefficients are scaled via a look-up table of 59 pressures × 5 temperatures, based on a mid-latitude summer profile. Total of **41 major gas k-terms**.

Gases included: H$_2$O, O$_3$, CO$_2$, O$_2$, N$_2$O, CH$_4$, SO$_2$ (experimental), OCS (experimental).

Ozone cross-sections from Serdyuchenko et al. [^cite-Serd14] and Gorshelev et al. [^cite-Gors14] for UV/visible; Brion–Daumont–Malicet for the far UV. In band 1, one k-term per 20 nm sub-interval (200–320 nm); in band 2, sub-intervals at 320–400 nm and 400–505 nm to allow the incoming solar flux to be supplied on finer wavelength bands for solar spectral variability experiments.

---

### `sp_lw_ga7`

Sections are identical to `sp_lw_ga3_0` except for changes to gaseous absorption and thermal emission.

**Spectral bands:**

| Band | Wavenumber (cm⁻¹) | Wavelength (µm) |
|---|---|---|
| 1 | 1 – 400 | 25 – 10000 |
| 2 | 400 – 550 | 18.18 – 25 |
| 3 | 550 – 590 and 750 – 800 | 12.5 – 13.33 and 16.95 – 18.18 |
| 4 | 590 – 750 | 13.33 – 16.95 |
| 5 | 800 – 990 and 1120 – 1200 | 8.33 – 8.93 and 10.10 – 12.5 |
| 6 | 990 – 1120 | 8.93 – 10.10 |
| 7 | 1200 – 1330 | 7.52 – 8.33 |
| 8 | 1330 – 1500 | 6.67 – 7.52 |
| 9 | 1500 – 2995 | 3.34 – 6.67 |

Bands 3 and 5 are split bands (see [Spectral files: split bands](../Explanations/spectral_files.md#split-bands-block-14)).

**Gaseous absorption:** Newly derived for all gases (except CO$_2$ in band 4) using HITRAN 2012 and CAVIAR. Total of **81 major gas k-terms**.

Greenhouse gases included: H$_2$O, CO$_2$, O$_3$, N$_2$O, CH$_4$, CFC-11, CFC-12, CFC-113, HCFC-22, HFC-134a, SO$_2$ (experimental), OCS (experimental).

The improved representation of CO$_2$ in the window region (more minor gas k-terms in bands 5 and 6) provides a better forcing response to increases in CO$_2$ (tested up to ×32 present-day). The new method of hybrid scattering may be used with this spectral file: 27 of the major gas k-terms (where their nominal optical depth is less than 10 in a mid-latitude summer atmosphere) use the full scattering solver; the remaining 54 (optical depth > 10) use a cheaper non-scattering solver.

**Thermal emission:** Planck function fitted by a quartic polynomial over 160–330 K. This increases the lower bound of the fit from 150 K used with `sp_lw_ga3_0` and slightly improves the fit over the important temperature range for the Earth's atmosphere.

---

## Global Atmosphere Configuration 3

### `sp_sw_ga3_0`

Sections are identical to `spec3a_sw_hadgem1_5o_rlfx` except for changes to the solar spectrum (including Rayleigh coefficients), gaseous absorption, aerosols, and ice crystals.

**Spectral bands:** Identical to `sp_sw_ga7` except bands 2 and 3 are not true spectral bands, they share the combined range 320–690 nm and only the sum of fluxes in these two bands is physically meaningful.

**Solar spectrum:** Lean (2000, updated) [^cite-Lean00], based on satellite observations at wavelengths shorter than 735 nm with the Kurucz spectrum [^cite-Kurucz95] at longer wavelengths, meaned over the last two solar cycles (1983–2004).

**Gaseous absorption:** Revised O$_3$ k-terms in bands 1–3 for improved ozone heating rate calculations and to better incorporate solar variability [^cite-Zhong08]. The UV band is divided into six narrow sub-bands, each with a single ozone k-term.

Gases included: H$_2$O, O$_3$, CO$_2$, O$_2$.

**Aerosols:** Addition of four aerosol species: fresh and aged OCFF (organic carbon fossil fuel), delta aerosol, and nitrate aerosol. The optical properties of the six divisions of mineral dust have been revised using refractive indices from Balkanski et al. [^cite-Balk07], making mineral dust less absorbing in the SW and more absorbing in the LW.

**Ice crystals:** A new parametrisation (type 9) based on observed particle size distributions and an ensemble model of ice crystal type and orientation. Optical properties are linked directly to temperature and ice water content with no intermediate dependence on ice crystal size.

---

### `sp_lw_ga3_0`

Used for climate configurations where a more accurate treatment of the stratosphere is required. Sections are identical to `spec3a_lw_hadgem1_5C` except for changes to gaseous absorption, thermal emission, aerosols, and ice crystals.

**Spectral bands:** Identical to `sp_lw_ga7` (nine bands; bands 3 and 5 split).

**Gaseous absorption:** New k-terms for CO$_2$ (band 4) and O$_3$ (band 6) [^cite-ZhongH00], increasing the total number of k-terms by 14 relative to `spec3a_lw_hadgem1_5C` to allow a more accurate treatment of stratospheric absorption.

Greenhouse gases: H$_2$O, CO$_2$, O$_3$, N$_2$O, CH$_4$, CFC-11, CFC-12, CFC-113, HCFC-22, HFC-134a.

**Thermal emission:** Quartic fit over 150–330 K. The previous fit (180–330 K in `spec3a_lw_hadgem1_5C`) could give negative emission at very cold temperatures sometimes seen at the top of the model.

**Aerosols and ice crystals:** Same additions as `sp_sw_ga3_0`.

---

### `sp_lw_ga3_1`

Used for forecast configurations where speed of computation and a more accurate treatment of the troposphere are required. Sections are identical to `spec3a_lw_hadgem1_5C` except for changes to aerosols and ice crystals, the same additions as `sp_sw_ga3_0`, with the extra CO$_2$ and O$_3$ k-terms of `sp_lw_ga3_0` not included.

---

## HadGEM2

### `spec3a_sw_hadgem1_5o_rlfx`

Used in the HadGEM2-A model and the global forecast model from PS20. All sections are identical to `spec3a_sw_hadgem1_3` except for changes to aerosols and Rayleigh scattering.

**Rayleigh scattering:** Rayleigh scattering coefficients in `spec3a_sw_hadgem1_3` were found to be in error by approximately 20% due to a bug in the generating code [^cite-Haywood08]. These are corrected here.

**Aerosols:** Mie scattering calculations have provided optical properties for seven additional aerosols: six size bins of mineral dust and one mode of biogenic aerosol from terpene emissions. Parametrisations of Aitken sulphate, fresh biomass (mode 1), and aged biomass (mode 2) have also been updated. Biogenic aerosols are hygroscopic.

---

### `spec3a_lw_hadgem1_5C`

Used in the HadGEM2-A model and the global forecast model from PS20. All sections are identical to `spec3a_lw_hadgem1_3` except for changes to aerosols.

**Aerosols:** Same additions as `spec3a_sw_hadgem1_5o_rlfx`.

**Block 15 (new):** Contains specific absorption and scattering coefficients of each aerosol mode at six wavelengths (0.38, 0.44, 0.55, 0.67, 0.87, 1.02 µm), used by the model to compute aerosol optical depth. In contrast to block 11, these coefficients are monochromatic. Hygroscopic aerosols have relative-humidity-dependent coefficients.

---

## HadGEM1

### `spec3a_sw_hadgem1_3`

**Spectral bands:** Six bands; bands 2 and 3 share the range 320–690 nm (not true bands).

**Solar spectrum:** Kurucz (1995) [^cite-Kurucz95].

**Gaseous absorption:** H$_2$O (with CKD 2.4 continuum [^cite-CKD]), O$_3$, CO$_2$, O$_2$. Foreign continuum combined with line data and fitted as one entity; self-broadened continuum represented explicitly. Spectroscopic data from HITRAN 2000 [^cite-HITRAN] with published corrections, augmented by theoretical weak lines.

**Aerosols:** Five standard climatological aerosols [^cite-Cusack98], plus two sulphate modes (Aitken and accumulation), two black carbon modes (fresh and aged), two sea-salt modes (film and jet), two biomass smoke modes (fresh and aged), and six mineral dust size bins.

**Cloud droplets:** Four types available (2, 3, 4, 5), based on size distributions from Rockel et al. [^cite-Rockel91] with effective radii 1.5–50 µm. Types 2 and 3 use linear fits (Slingo & Schrecker [^cite-SS82]); types 4 and 5 use Padé approximants. Type 4 corresponds to thin averaging and type 5 to thick averaging; **type 5 preferred** for both convective and large-scale clouds.

**Ice crystals:** Types 2 and 3 (spherical analogy, thin/thick averaging); type 7 (planar polycrystals, anomalous diffraction approximation [^cite-Krist99] [^cite-Krist00], fit in terms of mean maximum dimension $\bar{D}_l$); type 8 (ice aggregates [^cite-Edwards07], fit in terms of effective dimension $D_e$). **Type 2 recommended** for large-scale cloud; **type 3 for convective cloud**.

---

### `spec3a_lw_hadgem1_3`

**Spectral bands:** Nine bands; bands 3 and 5 are split.

**Thermal emission:** Quartic fit over 180–330 K.

**Gaseous absorption:** H$_2$O, O$_3$, CO$_2$, N$_2$O, CH$_4$, CFC-11, CFC-12, CFC-113, HCFC-22, HFC-125, HFC-134a. Spectroscopic data from HITRAN 92 for most gases; CKD 2.4 continuum for water vapour [^cite-CKD]. Halocarbon cross-sections from K. Shine (pers. comm.).

**Cloud droplets and ice crystals:** As per `spec3a_sw_hadgem1_3`. Only type 1 droplet data initially available for LW; types 4 and 5 (Padé fits) now recommended.

---

[^cite-Lean00]: J. Lean, *Evolution of the sun's spectral irradiance since the Maunder minimum*, Geophys. Res. Lett., 27:2425–2428, 2000.
[^cite-Kurucz95]: R. L. Kurucz, CD-ROM 23, Harvard Smithsonian Center for Astrophysics, 1995.
[^cite-HITRAN]: L. S. Rothman et al., *The HITRAN molecular spectroscopic database*, J. Quant. Spectrosc. Radiat. Transfer, various editions (2000, 2012).
[^cite-Serd14]: A. Serdyuchenko, V. Gorshelev, M. Weber, W. Chehade, and J. P. Burrows, *High spectral resolution ozone absorption cross-sections — Part 2: Temperature dependence*, Atmos. Meas. Tech., 7:625–636, 2014.
[^cite-Gors14]: V. Gorshelev, A. Serdyuchenko, M. Weber, W. Chehade, and J. P. Burrows, *High spectral resolution ozone absorption cross-sections — Part 1: Measurements, data analysis and comparison with previous measurements around 293 K*, Atmos. Meas. Tech., 7:609–624, 2014.
[^cite-Zhong08]: W. Zhong, S. M. Osprey, L. J. Gray, and J. D. Haigh, *Influence of the prescribed solar spectrum on calculations of atmospheric temperature*, Geophys. Res. Lett., 35(L22813), 2008.
[^cite-ZhongH00]: W. Zhong and J. D. Haigh, *An efficient and accurate correlated-k parametrization of infrared radiative transfer for troposphere–stratosphere–mesosphere GCMs*, Atmos. Sci. Lett., 1(2):125–135, 2000.
[^cite-Balk07]: Y. Balkanski, M. Schulz, T. Claquin, and S. Guibert, *Reevaluation of mineral aerosol radiative forcings suggests a better agreement with satellite and AERONET data*, Atmos. Chem. Phys., 7:81–95, 2007.
[^cite-Haywood08]: J. Haywood et al., *Identification/impact/rectification of a bug in radiation code preprocessing and spectral files*, Met Office Technical Report, 2008.
[^cite-CKD]: S. A. Clough, F. X. Kneizys, and R. W. Davies, *Line shape and the water vapor continuum*, Atmos. Res., 23:229–241, 1989.
[^cite-Cusack98]: S. Cusack, A. Slingo, J. M. Edwards, and M. Wild, *The radiative impact of a simple aerosol climatology on the Hadley Centre atmospheric GCM*, Q. J. Roy. Meteorol. Soc., 124:2517–2526, 1998.
[^cite-Rockel91]: B. Rockel, E. Raschke, and B. Weyres, *A parametrization of broad band radiative transfer properties of water, ice and mixed clouds*, Beiträge Phys. Atmosph., 64:1–12, 1991.
[^cite-SS82]: A. Slingo and H. M. Schrecker, *On the shortwave radiative properties of stratiform water clouds*, Q. J. R. Meteorol. Soc., 108:407–426, 1982.
[^cite-Krist99]: J. E. Kristjánsson, J. M. Edwards, and D. L. Mitchell, *A new parameterization scheme for the optical properties of ice crystals for use in general circulation models*, Phys. Chem. Earth (B), 24:231–236, 1999.
[^cite-Krist00]: J. E. Kristjánsson, J. M. Edwards, and D. L. Mitchell, *The impact of a new scheme for the optical properties of ice crystals on the climates of two GCMs*, J. Geophys. Res., 105:10063–10079, 2000.
[^cite-Edwards07]: J. M. Edwards, S. Havemann, J.-C. Thelen, and A. J. Baran, *A new parametrization for the radiative properties of ice crystals: Comparison with existing schemes and impact in a GCM*, J. Atmos. Res., 83:19–35, 2007.
