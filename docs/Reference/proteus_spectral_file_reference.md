# PROTEUS spectral files

!!! note
    The spectral files described here have been generated specifically for use within the PROTEUS framework, covering atmospheric compositions relevant to exoplanet and planetary science applications. They are distinct from the [standard Met Office spectral files](spectral_file_reference.md) distributed with SOCRATES for Earth atmosphere modelling.

---

## Overview

Each spectral file is identified by a codename and a band count; several codenames are available at multiple resolutions. All files are in the standard SOCRATES spectral file format.

Spectroscopic data sources are abbreviated as follows: [**HITRAN**](https://hitran.org/), [**ExoMol**](https://www.exomol.com/), [**ExoAtom**](https://exomol.com/exoatom/), [**DACE**](https://dace.unige.ch/opacityDatabase/).

---

## Spectral file summary table
 
| Codename | Bands | Absorbers | Source | Notes |
|---|---|---|---|---|
| Legacy | 318 | CO$_2$, CH$_4$, O$_2$, N$_2$, H$_2$, He | HITRAN | Legacy file used in Lichtenberg et al. (2021) |
| Oak | 318 | H$_2$O | HITRAN | Water-only file from HITRAN; intended for benchmarking |
| Idwal | 318 | H$_2$O | HITRAN | Made redundant by Oak |
| Balmora | 318 | H$_2$O | HITRAN | Made redundant by Oak |
| Triangle | 318 | H$_2$O, H$_2$, CO$_2$ | HITRAN | Test file |
| Mallard | 318 | H$_2$O, H$_2$, CO$_2$, CO, CH$_4$, O$_2$, N$_2$, He | HITRAN | HITRAN file with useful opacities |
| Reach | 318 | H$_2$O, CO$_2$, O$_3$, N$_2$O, CO, CH$_4$, O$_2$, NO, SO$_2$, NO$_2$, NH$_3$, HNO$_3$, N$_2$, H$_2$, He, OCS | HITRAN | Same as Mallard but with more opacities |
| Vivec | 318 | H$_2$O, CO$_2$, O$_3$, N$_2$O, CO, CH$_4$, O$_2$, NO, SO$_2$, NO$_2$, NH$_3$, HNO$_3$, N$_2$, H$_2$, He, OCS | HITRAN | Same as Reach, compiled on macOS |
| Alduin | 432 | H$_2$O | EXOMOL | |
| Kynesgrove | 318 | O$_2$ | DACE | Validation of DACE cross-section data against SOCRATES line-by-line calculations |
| Frostflow | 16 / 48 / 256 / 4096 | H$_2$O | DACE | Multi-resolution; 4096 intended for benchmarking, 16 for debugging |
| Dayspring | 16 / 48 / 256 / 4096 | H$_2$O, H$_2$, CO$_2$, CO, CH$_4$, N$_2$ | DACE | Multi-resolution; 4096 intended for benchmarking, 16 for debugging |
| Honeyside | 16 / 48 / 256 / 4096 | H$_2$O, H$_2$, CO$_2$, CO, CH$_4$, N$_2$, NH$_3$, SO$_2$, N$_2$O, O$_3$, HCN, H$_2$S | DACE | Multi-resolution; 4096 intended for benchmarking, 16 for debugging |
| Rocks | 64 / 128 / 256 | H$_2$, H$_2$O, O$_2$, SiO, SiO$_2$ | DACE | Rock vapours and key volatiles; 128-band file for JWST comparison |
 
---
 
## Full metadata
 
??? info "Honeyside"
    | Bands | Tolerance | NaN-clean | SOCRATES | Date | Platform | Creator | Notes |
    |---|---|---|---|---|---|---|---|
    | 4096 | 1.00E-02 | Yes | 2403 | 2024-07-07 | Linux Intel | Harrison Nicholls | Very high resolution; intended for benchmarking |
    | 256 | ^ | ^ | ^ | ^ | ^ | ^ | High resolution |
    | 48 | ^ | ^ | ^ | ^ | ^ | ^ | Medium resolution |
    | 16 | ^ | ^ | ^ | ^ | ^ | ^ | Low resolution; intended for debugging |
 
    **Absorbers:** H$_2$O, H$_2$, CO$_2$, CO, CH$_4$, N$_2$, NH$_3$, SO$_2$, N$_2$O, O$_3$, HCN, H$_2$S  
    **Continua:** H$_2$O-H$_2$O, H$_2$-CH$_4$, H$_2$-H$_2$, H$_2$-N$_2$, N$_2$-N$_2$, N$_2$-H$_2$O, CO$_2$-CO$_2$, CO$_2$-H$_2$, CO$_2$-CH$_4$  
    **Source:** DACE
 
??? info "Rocks"
    | Bands | Absorbers | Continua | NaN-clean | SOCRATES | Date | Platform | Creator | Notes |
    |---|---|---|---|---|---|---|---|---|
    | 256 | O$_2$, SiO, SiO$_2$ | O$_2$-O$_2$ | Yes | 2407.2 | 2025-05-15 | Linux Intel | Alex McGinty | — |
    | 128 | H$_2$, H$_2$O, O$_2$, SiO, SiO$_2$ | H$_2$O-H$_2$O, H$_2$-H$_2$, O$_2$-O$_2$ | Yes | 2407.02 | 2025-05-15 | Linux Intel | Alex McGinty | Rock vapours and key volatiles. High resolution file for comparison with JWST observations of rock-vapour atmospheres |
    | 64 | H$_2$, H$_2$O, O$_2$, SiO, SiO$_2$ | H$_2$O-H$_2$O, H$_2$-H$_2$, O$_2$-O$_2$ | Yes | 2407.02 | 2025-05-15 | Linux Intel | Alex McGinty | Rock vapours and key volatiles (low resolution) |
 
    **Source:** DACE
 
??? info "Dayspring"
    | Bands | Tolerance | NaN-clean | SOCRATES | Date | Platform | Creator | Notes |
    |---|---|---|---|---|---|---|---|
    | 4096 | 1.00E-02 | Yes | 2403 | 2024-04-30 | Linux Intel | Harrison Nicholls | Very high resolution; intended for benchmarking |
    | 256 | ^ | ^ | ^ | ^ | ^ | ^ | High resolution |
    | 48 | ^ | ^ | ^ | ^ | ^ | ^ | Medium resolution |
    | 16 | ^ | ^ | ^ | ^ | ^ | ^ | Low resolution; intended for debugging |
 
    **Absorbers:** H$_2$O, H$_2$, CO$_2$, CO, CH$_4$, N$_2$  
    **Continua:** H$_2$O-H$_2$O, H$_2$-CH$_4$, H$_2$-H$_2$, H$_2$-N$_2$, N$_2$-N$_2$, N$_2$-H$_2$O, CO$_2$-CO$_2$, CO$_2$-H$_2$, CO$_2$-CH$_4$  
    **Source:** DACE
 
??? info "Frostflow"
    | Bands | Tolerance | NaN-clean | SOCRATES | Date | Platform | Creator | Notes |
    |---|---|---|---|---|---|---|---|
    | 4096 | 5.00E-03 | Yes | 2403 | 2024-03-20 | Linux Intel | Harrison Nicholls | Very high resolution; intended for benchmarking |
    | 256 | ^ | ^ | ^ | ^ | ^ | ^ | High resolution |
    | 48 | ^ | ^ | ^ | ^ | ^ | ^ | Medium resolution |
    | 16 | ^ | ^ | ^ | ^ | ^ | ^ | Low resolution; intended for debugging |
 
    **Absorbers:** H$_2$O  
    **Continua:** H$_2$O  
    **Source:** DACE
 
??? info "Kynesgrove"
    | Field | Value |
    |---|---|
    | Bands | 318 |
    | Absorbers | O$_2$ |
    | Continua | O$_2$-O$_2$ |
    | Tolerance | 5.00E-04 |
    | Source | DACE |
    | NaN-clean | Yes |
    | SOCRATES version | 2403 |
    | Date | 2024-03-14 |
    | Platform | Linux Intel |
    | Creator | Harrison Nicholls |
    | Notes | Created for validation of DACE cross-section data against SOCRATES' own line-by-line calculations used in Mallard |
 
??? info "Reach"
    | Field | Value |
    |---|---|
    | Bands | 318 |
    | Absorbers | H$_2$O, CO$_2$, O$_3$, N$_2$O, CO, CH$_4$, O$_2$, NO, SO$_2$, NO$_2$, NH$_3$, HNO$_3$, N$_2$, H$_2$, He, OCS |
    | Continua | H$_2$O, CO$_2$, CH$_4$, O$_2$, N$_2$, H$_2$, He |
    | Tolerance | 1.00E-02 |
    | Source | HITRAN |
    | NaN-clean | Yes |
    | SOCRATES version | 2306 |
    | Date | 2023-07-19 |
    | Platform | Linux Intel |
    | Creator | Harrison Nicholls |
    | Notes | Same as Mallard but with more opacities. Script exists to generate this file, but it is not currently available. |
 
??? info "Mallard"
    | Field | Value |
    |---|---|
    | Bands | 318 |
    | Absorbers | H$_2$O, H$_2$, CO$_2$, CO, CH$_4$, O$_2$, N$_2$, He |
    | Continua | H$_2$O, CO$_2$, CH$_4$, O$_2$, N$_2$, H$_2$, He |
    | Tolerance | 1.00E-02 |
    | Source | HITRAN |
    | NaN-clean | Yes |
    | SOCRATES version | 2306 |
    | Date | 2023-07-13 |
    | Platform | Linux Intel |
    | Creator | Harrison Nicholls |
    | Notes | HITRAN file with useful opacities |
 
??? info "Alduin"
    | Field | Value |
    |---|---|
    | Bands | 432 |
    | Absorbers | H$_2$O |
    | Continua | H$_2$O |
    | Tolerance | 1.00E-02 |
    | Source | EXOMOL |
    | NaN-clean | Yes |
    | SOCRATES version | 2306 |
    | Date | — |
    | Platform | Linux Intel |
    | Creator | Ryan Boukrouche |
    | Notes | — |
 
??? info "Oak"
    | Field | Value |
    |---|---|
    | Bands | 318 |
    | Absorbers | H$_2$O |
    | Continua | H$_2$O |
    | Tolerance | 1.00E-02 |
    | Source | HITRAN |
    | NaN-clean | Yes |
    | SOCRATES version | 2306 |
    | Date | 2023-07-10 |
    | Platform | Linux Intel |
    | Creator | Harrison Nicholls |
    | Notes | Water-only spectral file from HITRAN. To be used for benchmarking. |
 
??? info "Legacy"
    | Field | Value |
    |---|---|
    | Bands | 318 |
    | Absorbers | CO$_2$, CH$_4$, O$_2$, N$_2$, H$_2$, He |
    | Continua | — |
    | Tolerance | 1.00E-02 |
    | Source | HITRAN |
    | NaN-clean | Yes |
    | SOCRATES version | 2002 |
    | Date | 2021 |
    | Platform | Linux Intel |
    | Creator | Tim Lichtenberg |
    | Notes | Legacy spectral file used in Lichtenberg et al. (2021) |
 
??? info "Vivec"
    | Field | Value |
    |---|---|
    | Bands | 318 |
    | Absorbers | H$_2$O, CO$_2$, O$_3$, N$_2$O, CO, CH$_4$, O$_2$, NO, SO$_2$, NO$_2$, NH$_3$, HNO$_3$, N$_2$, H$_2$, He, OCS |
    | Continua | H$_2$O, CO$_2$, CH$_4$, O$_2$, N$_2$, H$_2$, He |
    | Tolerance | 1.00E-02 |
    | Source | HITRAN |
    | NaN-clean | No |
    | SOCRATES version | 2306 |
    | Date | 2023-07-25 |
    | Platform | Mac Intel |
    | Creator | Tim Lichtenberg |
    | Notes | Same as Reach, but compiled on macOS |
 
??? info "Triangle"
    | Field | Value |
    |---|---|
    | Bands | 318 |
    | Absorbers | H$_2$O, H$_2$, CO$_2$ |
    | Continua | H$_2$O, H$_2$, CO$_2$ |
    | Tolerance | 1.00E-02 |
    | Source | HITRAN |
    | NaN-clean | Yes |
    | SOCRATES version | 2306 |
    | Date | 2023-07-11 |
    | Platform | Linux Intel |
    | Creator | Harrison Nicholls |
    | Notes | Test |
 
??? info "Idwal"
    | Field | Value |
    |---|---|
    | Bands | 318 |
    | Absorbers | H$_2$O |
    | Continua | H$_2$O |
    | Tolerance | 1.00E-02 |
    | Source | HITRAN |
    | NaN-clean | No |
    | SOCRATES version | 2211 |
    | Date | 2023-07-11 |
    | Platform | Linux Intel |
    | Creator | Harrison Nicholls |
    | Notes | Made redundant by Oak. They only differ by SOCRATES version. |
 
??? info "Balmora"
    | Field | Value |
    |---|---|
    | Bands | 318 |
    | Absorbers | H$_2$O |
    | Continua | H$_2$O |
    | Tolerance | 1.00E-02 |
    | Source | HITRAN |
    | NaN-clean | No |
    | SOCRATES version | 2306 |
    | Date | 2023-07-19 |
    | Platform | Mac ARM |
    | Creator | Tim Lichtenberg |
    | Notes | Made redundant by Oak. They only differ by creation platform. |

---

## Choosing a spectral file

The appropriate spectral file depends on the atmospheric composition being modelled and the required spectral resolution:

- For **benchmarking or comparison with observations**, use a high- or very-high-resolution configuration (256–4096 bands).
- For **debugging**, use a low resolution spectral file with 16 bands.
- For **water-dominated atmospheres**, Frostflow or Oak are appropriate depending on the required resolution and data source.
- For **mixed volatile atmospheres** (H$_2$O, CO$_2$, CH$_4$, H$_2$, N$_2$ and more), Honeyside is the most complete option.
- For **rock-vapour atmospheres** (relevant to magma ocean planets), use the Rocks files which include SiO and SiO$_2$ opacity.