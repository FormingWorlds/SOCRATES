# PROTEUS spectral files

!!! note
    The spectral files described here have been generated specifically for use within the PROTEUS framework, covering atmospheric compositions relevant to exoplanet and planetary science applications. They are distinct from the [standard Met Office spectral files](spectral_files_reference.md) distributed with SOCRATES for Earth atmosphere modelling.

---

## Overview

Each spectral file is identified by a codename and a band count; several codenames are available at multiple resolutions. All files are in the standard SOCRATES spectral file format.

Spectroscopic data sources are abbreviated as follows: **HITRAN** – [HITRAN database](https://hitran.org/); **EXOMOL** — [ExoMol database](https://www.exomol.com/); **DACE** — [DACE opacity database](https://dace.unige.ch/opacityDatabase/).

---

## Spectral file table
 
| Codename | Bands | Absorbers | Continua | Tolerance | Source | NaN-clean | SOCRATES | Date | Platform | Creator | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Legacy | 318 | CO₂, CH₄, O₂, N₂, H₂, He | — | 1.00E-02 | HITRAN | Yes | 2002 | 2021 | Linux Intel | Tim Lichtenberg | Legacy spectral file used in Lichtenberg+2021 |
| Oak | 318 | H₂O | H₂O | 1.00E-02 | HITRAN | Yes | 2306 | 2023-07-10 | Linux Intel | Harrison Nicholls | Water-only spectral file from HITRAN. To be used for benchmarking. |
| Idwal | 318 | H₂O | H₂O | 1.00E-02 | HITRAN | No | 2211 | 2023-07-11 | Linux Intel | Harrison Nicholls | Made redundant by Oak. They only differ by SOCRATES version. |
| Balmora | 318 | H₂O | H₂O | 1.00E-02 | HITRAN | No | 2306 | 2023-07-19 | Mac ARM | Tim Lichtenberg | Made redundant by Oak. They only differ by creation platform. |
| Triangle | 318 | H₂O, H₂, CO₂ | H₂O, H₂, CO₂ | 1.00E-02 | HITRAN | Yes | 2306 | 2023-07-11 | Linux Intel | Harrison Nicholls | Test |
| Mallard | 318 | H₂O, H₂, CO₂, CO, CH₄, O₂, N₂, He | H₂O, CO₂, CH₄, O₂, N₂, H₂, He | 1.00E-02 | HITRAN | Yes | 2306 | 2023-07-13 | Linux Intel | Harrison Nicholls | HITRAN file with useful opacities |
| Reach | 318 | H₂O, CO₂, O₃, N₂O, CO, CH₄, O₂, NO, SO₂, NO₂, NH₃, HNO₃, N₂, H₂, He, OCS | H₂O, CO₂, CH₄, O₂, N₂, H₂, He | 1.00E-02 | HITRAN | Yes | 2306 | 2023-07-19 | Linux Intel | Harrison Nicholls | Same as above but with more opacities. Script exists to generate this file, but it is not currently available. |
| Vivec | 318 | H₂O, CO₂, O₃, N₂O, CO, CH₄, O₂, NO, SO₂, NO₂, NH₃, HNO₃, N₂, H₂, He, OCS | H₂O, CO₂, CH₄, O₂, N₂, H₂, He | 1.00E-02 | HITRAN | No | 2306 | 2023-07-25 | Mac Intel | Tim Lichtenberg | Same as above, but compiled on MacOS |
| Alduin | 432 | H₂O | H₂O | 1.00E-02 | EXOMOL | Yes | 2306 | — | Linux Intel | Ryan Boukrouche | — |
| Kynesgrove | 318 | O₂ | O₂-O₂ | 5.00E-04 | DACE | Yes | 2403 | 2024-03-14 | Linux Intel | Harrison Nicholls | Created for validation of DACE xsec data against SOCRATES' own LbL calculations used in Mallard. |
| Frostflow | 4096 | H₂O | H₂O | 5.00E-03 | DACE | Yes | 2403 | 2024-03-20 | Linux Intel | Harrison Nicholls | Very high resolution. Intended for benchmarking. |
| Frostflow | 256 | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | High resolution. |
| Frostflow | 48 | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | Medium resolution. |
| Frostflow | 16 | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | Low resolution. Intended for debugging. |
| Dayspring | 4096 | H₂O, H₂, CO₂, CO, CH₄, N₂ | H₂O-H₂O, H₂-CH₄, H₂-H₂, H₂-N₂, N₂-N₂, N₂-H₂O, CO₂-CO₂, CO₂-H₂, CO₂-CH₄ | 1.00E-02 | DACE | Yes | 2403 | 2024-04-30 | Linux Intel | Harrison Nicholls | Very high resolution. Intended for benchmarking. |
| Dayspring | 256 | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | High resolution. |
| Dayspring | 48 | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | Medium resolution. |
| Dayspring | 16 | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | Low resolution. Intended for debugging. |
| Honeyside | 4096 | H₂O, H₂, CO₂, CO, CH₄, N₂, NH₃, SO₂, N₂O, O₃, HCN, H₂S | H₂O-H₂O, H₂-CH₄, H₂-H₂, H₂-N₂, N₂-N₂, N₂-H₂O, CO₂-CO₂, CO₂-H₂, CO₂-CH₄ | 1.00E-02 | DACE | Yes | 2403 | 2024-07-07 | Linux Intel | Harrison Nicholls | Very high resolution. Intended for benchmarking. |
| Honeyside | 256 | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | High resolution. |
| Honeyside | 48 | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | Medium resolution. |
| Honeyside | 16 | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | ^ | Low resolution. Intended for debugging. |
| Rocks | 256 | O₂, SiO, SiO₂ | O₂-O₂ | — | DACE | Yes | 2407.2 | 2025-05-15 | Linux Intel | Alex McGinty | — |
| Rocks | 128 | H₂, H₂O, O₂, SiO, SiO₂ | H₂O-H₂O, H₂-H₂, O₂-O₂ | — | DACE | Yes | 2407.02 | 2025-05-15 | Linux Intel | Alex McGinty | Rock vapours and key volatiles. High resolution file used for comparison with JWST observations of rock-vapour atmospheres. |
| Rocks | 64 | H₂, H₂O, O₂, SiO, SiO₂ | H₂O-H₂O, H₂-H₂, O₂-O₂ | — | DACE | Yes | 2407.02 | 2025-05-15 | Linux Intel | Alex McGinty | Rock vapours and key volatiles (low resolution). |

---

## Choosing a spectral file

The appropriate spectral file depends on the atmospheric composition being modelled and the required spectral resolution:

- For **benchmarking or comparison with observations**, use a high- or very-high-resolution configuration (256–4096 bands).
- For **debugging**, use a low resolution spectral file with 16 bands.
- For **water-dominated atmospheres**, Frostflow or Oak are appropriate depending on the required resolution and data source.
- For **mixed volatile atmospheres** (H₂O, CO₂, CH₄, H₂, N₂ and more), Honeyside is the most complete option.
- For **rock-vapour atmospheres** (relevant to magma ocean planets), use the Rocks files which include SiO and SiO₂ opacity.