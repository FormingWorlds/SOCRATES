# PROTEUS spectral files

!!! note
    The spectral files described here have been generated specifically for use within the PROTEUS framework, covering atmospheric compositions relevant to exoplanet and planetary science applications. They are distinct from the [standard Met Office spectral files](spectral_file_reference.md) distributed with SOCRATES for Earth atmosphere modelling.

---

## Spectral file summary table

Each spectral file is identified by a codename and a band count; several codenames are available at multiple resolutions. All files are in the standard SOCRATES spectral file format. The Generation III files are made with the [`spectraltools`](https://github.com/FormingWorlds/SOCRATES/tree/main/spectraltools) scripts in this repository; [Building spectral files](../Explanations/spectraltools_pipeline.md) describes how.

A quick reference, with one row per codename. Click a codename for its details and data sources, or a band count for its record in the [PROTEUS Zenodo community](https://zenodo.org/communities/proteus_framework). Band counts without a link have no Zenodo record yet.

### Generation III

| Codename | Purpose | Bands | Gases |
|----------|---------|-------|-------|
| [Snowline](#snowline) | Water | 2048, 256, 128, 64, 32 | H<sub>2</sub>O |
| [Breezehome](#breezehome) | Oxidised volatiles | 2048, 256, 128, 64, 32 | H<sub>2</sub>O, CO<sub>2</sub>, CO, O<sub>2</sub>, SO<sub>2</sub>, OCS, S<sub>2</sub> |
| [Cliffshade](#cliffshade) | Reduced volatiles | 2048, 256, 128, 64, 32 | H<sub>2</sub>, CO, CH<sub>4</sub>, S<sub>2</sub>, H<sub>2</sub>S, N<sub>2</sub>, NH<sub>3</sub> |
| [Volenfell](#volenfell) | Rock vapours | 2048, 256, 128, 64, 32 | CO, O<sub>2</sub>, SiO, TiO, MgO, Na, K, Fe |
| [Proudspire](#proudspire) | Combined volatiles | 2048, 256, 128, 64, 32 | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, O<sub>2</sub>, O<sub>3</sub>, CH<sub>4</sub>, SO<sub>2</sub>, OCS, S<sub>2</sub>, H<sub>2</sub>S, N<sub>2</sub>, NH<sub>3</sub>, HCN |
| [Skyborn](#skyborn) | Hot Jupiters | 2048, 256, 128, 64, 32 | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, SiO, TiO, VO, MgO, Na, K, Fe |
| [Atmora](#atmora) | Rock vapours and volatiles (smaller set) | 2048, 256, 128, 64, 32 | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, O<sub>2</sub>, CH<sub>4</sub>, SO<sub>2</sub>, S<sub>2</sub>, H<sub>2</sub>S, NH<sub>3</sub>, SiO, TiO, Na, K |
| [Sovngarde](#sovngarde) | Rock vapours and volatiles (larger set) | 2048, 256, 128, 64, 32 | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, O<sub>2</sub>, O<sub>3</sub>, CH<sub>4</sub>, SO<sub>2</sub>, OCS, S<sub>2</sub>, H<sub>2</sub>S, N<sub>2</sub>, NH<sub>3</sub>, HCN, SiO, TiO, MgO, Na, K, Fe |

### Generation II

| Codename | Purpose | Bands | Gases |
|----------|---------|-------|-------|
| [Kynesgrove](#kynesgrove) | Validation of DACE O<sub>2</sub> cross-sections against SOCRATES line-by-line calculations | [318](https://zenodo.org/records/23190125 "Kynesgrove 318 on Zenodo") | O<sub>2</sub> |
| [Frostflow](#frostflow) | Water-dominated atmospheres (DACE) | [4096](https://zenodo.org/records/15799776 "Frostflow 4096 on Zenodo"), [256](https://zenodo.org/records/15799754 "Frostflow 256 on Zenodo"), [48](https://zenodo.org/records/15696415 "Frostflow 48 on Zenodo"), [16](https://zenodo.org/records/15799743 "Frostflow 16 on Zenodo") | H<sub>2</sub>O |
| [Dayspring](#dayspring) | Mixed volatiles, smaller set than Honeyside (DACE) | [4096](https://zenodo.org/records/15799495 "Dayspring 4096 on Zenodo"), [256](https://zenodo.org/records/15799474 "Dayspring 256 on Zenodo"), [48](https://zenodo.org/records/15721749 "Dayspring 48 on Zenodo"), [16](https://zenodo.org/records/15799318 "Dayspring 16 on Zenodo") | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub> |
| [Honeyside](#honeyside) | Mixed volatiles; suggested for magma-ocean planets (DACE) | [4096](https://zenodo.org/records/15696457 "Honeyside 4096 on Zenodo"), [256](https://zenodo.org/records/15799731 "Honeyside 256 on Zenodo"), [48](https://zenodo.org/records/15799652 "Honeyside 48 on Zenodo"), [16](https://zenodo.org/records/15799607 "Honeyside 16 on Zenodo") | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub>, NH<sub>3</sub>, SO<sub>2</sub>, N<sub>2</sub>O, O<sub>3</sub>, HCN, H<sub>2</sub>S |
| [Rocks](#rocks) | Rock-vapour atmospheres, for comparison with JWST observations | [256](https://zenodo.org/records/15806423 "Rocks 256 on Zenodo"), [128](https://zenodo.org/records/15806401 "Rocks 128 on Zenodo"), [64](https://zenodo.org/records/15806381 "Rocks 64 on Zenodo") | H<sub>2</sub>, H<sub>2</sub>O, O<sub>2</sub>, SiO, SiO<sub>2</sub> (the 256-band file has only O<sub>2</sub>, SiO and SiO<sub>2</sub>) |
| [Winterfell](#winterfell) | As Honeyside, with UV cross-sections | [4096](https://zenodo.org/records/18402082 "Winterfell 4096 on Zenodo"), [256](https://zenodo.org/records/18402159 "Winterfell 256 on Zenodo"), [48](https://zenodo.org/records/18402184 "Winterfell 48 on Zenodo"), [16](https://zenodo.org/records/18402217 "Winterfell 16 on Zenodo") | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub>, NH<sub>3</sub>, SO<sub>2</sub>, N<sub>2</sub>O, O<sub>3</sub>, HCN, H<sub>2</sub>S, O<sub>2</sub> |
| [Dragonstone](#dragonstone) | As Winterfell, without O<sub>2</sub> | [4096](https://zenodo.org/records/18922546 "Dragonstone 4096 on Zenodo"), [256](https://zenodo.org/records/18910878 "Dragonstone 256 on Zenodo"), [48](https://zenodo.org/records/18922528 "Dragonstone 48 on Zenodo"), [16](https://zenodo.org/records/18922335 "Dragonstone 16 on Zenodo") | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub>, NH<sub>3</sub>, SO<sub>2</sub>, N<sub>2</sub>O, O<sub>3</sub>, HCN, H<sub>2</sub>S |
| [Sunspear](#sunspear) | Reproducing Ranjan & Sasselov (2016): UV for CO<sub>2</sub>, SO<sub>2</sub> and H<sub>2</sub>S only | 4096, 256, 48, 16 | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub>, NH<sub>3</sub>, SO<sub>2</sub>, N<sub>2</sub>O, O<sub>3</sub>, HCN, H<sub>2</sub>S, O<sub>2</sub> |

### Generation I

| Codename | Purpose | Bands | Gases |
|----------|---------|-------|-------|
| [Legacy](#legacy) | Legacy file used in Lichtenberg et al. (2021) | [318](https://zenodo.org/records/15806343 "Legacy 318 on Zenodo") | H<sub>2</sub>O, CO<sub>2</sub>, O<sub>3</sub>, N<sub>2</sub>O, CO, CH<sub>4</sub>, O<sub>2</sub>, NO, SO<sub>2</sub>, NO<sub>2</sub>, NH<sub>3</sub>, HNO<sub>3</sub>, N<sub>2</sub>, H<sub>2</sub>, He, OCS |
| [Oak](#oak) | Water only (HITRAN), for benchmarking | [318](https://zenodo.org/records/15743843 "Oak 318 on Zenodo") | H<sub>2</sub>O |
| [Idwal](#idwal) | Superseded by Oak (older SOCRATES version) | 318 | H<sub>2</sub>O |
| [Balmora](#balmora) | Superseded by Oak (built on macOS) | 318 | H<sub>2</sub>O |
| [Triangle](#triangle) | Test file | 318 | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub> |
| [Mallard](#mallard) | Common opacities from HITRAN | [318](https://zenodo.org/records/23190131 "Mallard 318 on Zenodo") | H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, O<sub>2</sub>, N<sub>2</sub>, He |
| [Reach](#reach) | As Mallard, with more opacities | [318](https://zenodo.org/records/23190144 "Reach 318 on Zenodo") | H<sub>2</sub>O, CO<sub>2</sub>, O<sub>3</sub>, N<sub>2</sub>O, CO, CH<sub>4</sub>, O<sub>2</sub>, NO, SO<sub>2</sub>, NO<sub>2</sub>, NH<sub>3</sub>, HNO<sub>3</sub>, N<sub>2</sub>, H<sub>2</sub>, He, OCS |
| [Vivec](#vivec) | As Reach, built on macOS | 318 | H<sub>2</sub>O, CO<sub>2</sub>, O<sub>3</sub>, N<sub>2</sub>O, CO, CH<sub>4</sub>, O<sub>2</sub>, NO, SO<sub>2</sub>, NO<sub>2</sub>, NH<sub>3</sub>, HNO<sub>3</sub>, N<sub>2</sub>, H<sub>2</sub>, He, OCS |

---

## Choosing a spectral file

The appropriate spectral file depends on the atmospheric composition being modelled and the required spectral resolution:

- For **benchmarking or comparison with observations**, use a high- or very-high-resolution configuration (256–4096 bands).
- For **debugging**, use a low resolution spectral file with 16 bands.
- For **water-dominated atmospheres**, Frostflow or Oak are appropriate depending on the required resolution and data source.
- For **mixed volatile atmospheres** (H<sub>2</sub>O, CO<sub>2</sub>, CH<sub>4</sub>, H<sub>2</sub>, N<sub>2</sub> and more), Honeyside is the most complete option.
- For **rock-vapour atmospheres** (relevant to magma ocean planets), use the Rocks files which include SiO and SiO<sub>2</sub> opacity.
- The Generation III files are organised by composition: **Snowline** for water, **Breezehome** for oxidised volatiles, **Cliffshade** for reduced volatiles, **Volenfell** for rock vapours, **Proudspire** for combined volatiles, **Skyborn** for hot Jupiters, and **Atmora** and **Sovngarde** for rock vapours with volatiles (a smaller and a larger set of gases). Each has 32, 64, 128, 256 and 2048 bands.

---

## Spectral file details

One subsection per codename. **k-term tolerance** is the maximum RMS error in transmission allowed when choosing the number of k-terms (`Ccorr_k` option `-t` for Generation III). **Maximum absorber path** (Generation III) is the largest absorber amount for which `Ccorr_k` fits the k-terms to the line-by-line transmission (options `-l` for line absorption and `-ct` for continua); the build script sets 10³ kg m⁻² by default and 10 kg m⁻² for SiO, TiO, VO, MgO, Na, K and Fe (see [Building spectral files](../Explanations/spectraltools_pipeline.md)). The abbreviations used for data sources are listed under [Abbreviations](#abbreviations). A "?" marks a value that is not known.

### Legacy

- **Bands**: 318
- **Zenodo records**: [318](https://zenodo.org/records/15806343 "Legacy 318 on Zenodo")
- **Absorbers**: H<sub>2</sub>O, CO<sub>2</sub>, O<sub>3</sub>, N<sub>2</sub>O, CO, CH<sub>4</sub>, O<sub>2</sub>, NO, SO<sub>2</sub>, NO<sub>2</sub>, NH<sub>3</sub>, HNO<sub>3</sub>, N<sub>2</sub>, H<sub>2</sub>, He, OCS
- **Continua**: CO<sub>2</sub>, CH<sub>4</sub>, O<sub>2</sub>, N<sub>2</sub>, H<sub>2</sub>, He
- **UV cross-sections**: No
- **Sources**: HITRAN
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2002
- **Date**: 2021
- **Platform**: Linux Intel
- **Creator**: Tim Lichtenberg
- **Notes**: Legacy spectral file used in Lichtenberg+2021

### Oak

- **Bands**: 318
- **Zenodo records**: [318](https://zenodo.org/records/15743843 "Oak 318 on Zenodo")
- **Absorbers**: H<sub>2</sub>O
- **Continua**: H<sub>2</sub>O
- **UV cross-sections**: No
- **Sources**: HITRAN
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2306
- **Date**: 2023-07-10
- **Platform**: Linux Intel
- **Creator**: Harrison Nicholls
- **Notes**: Water-only spectral file from HITRAN. To be used for benchmarking.

### Idwal

- **Bands**: 318
- **Zenodo records**: no Zenodo record found
- **Absorbers**: H<sub>2</sub>O
- **Continua**: H<sub>2</sub>O
- **UV cross-sections**: No
- **Sources**: HITRAN
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2211
- **Date**: 2023-07-11
- **Platform**: Linux Intel
- **Creator**: Harrison Nicholls
- **Notes**: Made redundant by Oak. They only differ by SOCRATES version.

### Balmora

- **Bands**: 318
- **Zenodo records**: no Zenodo record found
- **Absorbers**: H<sub>2</sub>O
- **Continua**: H<sub>2</sub>O
- **UV cross-sections**: No
- **Sources**: HITRAN
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2306
- **Date**: 2023-07-19
- **Platform**: Mac ARM
- **Creator**: Tim Lichtenberg
- **Notes**: Made redundant by Oak. They only differ by creation platform.

### Triangle

- **Bands**: 318
- **Zenodo records**: no Zenodo record found
- **Absorbers**: H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>
- **Continua**: H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>
- **UV cross-sections**: No
- **Sources**: HITRAN
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2306
- **Date**: 2023-07-11
- **Platform**: Linux Intel
- **Creator**: Harrison Nicholls
- **Notes**: Test

### Mallard

- **Bands**: 318
- **Zenodo records**: [318](https://zenodo.org/records/23190131 "Mallard 318 on Zenodo")
- **Absorbers**: H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, O<sub>2</sub>, N<sub>2</sub>, He
- **Continua**: H<sub>2</sub>O, CO<sub>2</sub>, CH<sub>4</sub>, O<sub>2</sub>, N<sub>2</sub>, H<sub>2</sub>, He
- **UV cross-sections**: No
- **Sources**: HITRAN
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2306
- **Date**: 2023-07-13
- **Platform**: Linux Intel
- **Creator**: Harrison Nicholls
- **Notes**: HITRAN file with useful opacities

### Reach

- **Bands**: 318
- **Zenodo records**: [318](https://zenodo.org/records/23190144 "Reach 318 on Zenodo")
- **Absorbers**: H<sub>2</sub>O, CO<sub>2</sub>, O<sub>3</sub>, N<sub>2</sub>O, CO, CH<sub>4</sub>, O<sub>2</sub>, NO, SO<sub>2</sub>, NO<sub>2</sub>, NH<sub>3</sub>, HNO<sub>3</sub>, N<sub>2</sub>, H<sub>2</sub>, He, OCS
- **Continua**: H<sub>2</sub>O, CO<sub>2</sub>, CH<sub>4</sub>, O<sub>2</sub>, N<sub>2</sub>, H<sub>2</sub>, He
- **UV cross-sections**: No
- **Sources**: HITRAN
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2306
- **Date**: 2023-07-19
- **Platform**: Linux Intel
- **Creator**: Harrison Nicholls
- **Notes**: Same as above but with more opacities

### Vivec

- **Bands**: 318
- **Zenodo records**: no Zenodo record found
- **Absorbers**: H<sub>2</sub>O, CO<sub>2</sub>, O<sub>3</sub>, N<sub>2</sub>O, CO, CH<sub>4</sub>, O<sub>2</sub>, NO, SO<sub>2</sub>, NO<sub>2</sub>, NH<sub>3</sub>, HNO<sub>3</sub>, N<sub>2</sub>, H<sub>2</sub>, He, OCS
- **Continua**: H<sub>2</sub>O, CO<sub>2</sub>, CH<sub>4</sub>, O<sub>2</sub>, N<sub>2</sub>, H<sub>2</sub>, He
- **UV cross-sections**: No
- **Sources**: HITRAN
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2306
- **Date**: 2023-07-25
- **Platform**: Mac Intel
- **Creator**: Tim Lichtenberg
- **Notes**: Same as above, but compiled on MacOS

### Kynesgrove

- **Bands**: 318
- **Zenodo records**: [318](https://zenodo.org/records/23190125 "Kynesgrove 318 on Zenodo")
- **Absorbers**: O<sub>2</sub>
- **Continua**: O<sub>2</sub>-O<sub>2</sub>
- **UV cross-sections**: No
- **Sources**: DACE
- **k-term tolerance**: 5.00E-04
- **SOCRATES version**: 2403
- **Date**: 2024-03-14
- **Platform**: Linux Intel
- **Creator**: Harrison Nicholls
- **Notes**: Created for validation of DACE xsec data against SOCRATES' own LbL calculations used in Mallard.

### Frostflow

- **Bands**:
    - 4096: Very high resolution. Intended for benchmarking.
    - 256: High resolution.
    - 48: Medium resolution.
    - 16: Low resolution. Intended for debugging.
- **Zenodo records**: [4096](https://zenodo.org/records/15799776 "Frostflow 4096 on Zenodo"), [256](https://zenodo.org/records/15799754 "Frostflow 256 on Zenodo"), [48](https://zenodo.org/records/15696415 "Frostflow 48 on Zenodo"), [16](https://zenodo.org/records/15799743 "Frostflow 16 on Zenodo")
- **Absorbers**: H<sub>2</sub>O
- **Continua**: H<sub>2</sub>O
- **UV cross-sections**: No
- **Sources**: DACE
- **k-term tolerance**: 5.00E-03
- **SOCRATES version**: 2403
- **Date**: 2024-03-20
- **Platform**: Linux Intel
- **Creator**: Harrison Nicholls

### Dayspring

- **Bands**:
    - 4096: Very high resolution. Intended for benchmarking.
    - 256: High resolution.
    - 48: Medium resolution.
    - 16: Low resolution. Intended for debugging.
- **Zenodo records**: [4096](https://zenodo.org/records/15799495 "Dayspring 4096 on Zenodo"), [256](https://zenodo.org/records/15799474 "Dayspring 256 on Zenodo"), [48](https://zenodo.org/records/15721749 "Dayspring 48 on Zenodo"), [16](https://zenodo.org/records/15799318 "Dayspring 16 on Zenodo")
- **Absorbers**: H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub>
- **Continua**: H<sub>2</sub>O-H<sub>2</sub>O, H<sub>2</sub>-CH<sub>4</sub>, H<sub>2</sub>-H<sub>2</sub>, N<sub>2</sub>-H<sub>2</sub>, N<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-H<sub>2</sub>O, CO<sub>2</sub>-CO<sub>2</sub>, CO<sub>2</sub>-H<sub>2</sub>, CO<sub>2</sub>-CH<sub>4</sub>
- **UV cross-sections**: No
- **Sources**: DACE
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2403
- **Date**: 2024-04-30
- **Platform**: Linux Intel
- **Creator**: Harrison Nicholls

### Honeyside

- **Bands**:
    - 4096: Very high resolution. Intended for benchmarking.
    - 256: High resolution.
    - 48: Medium resolution.
    - 16: Low resolution. Intended for debugging.
- **Zenodo records**: [4096](https://zenodo.org/records/15696457 "Honeyside 4096 on Zenodo"), [256](https://zenodo.org/records/15799731 "Honeyside 256 on Zenodo"), [48](https://zenodo.org/records/15799652 "Honeyside 48 on Zenodo"), [16](https://zenodo.org/records/15799607 "Honeyside 16 on Zenodo")
- **Absorbers**: H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub>, NH<sub>3</sub>, SO<sub>2</sub>, N<sub>2</sub>O, O<sub>3</sub>, HCN, H<sub>2</sub>S
- **Continua**: H<sub>2</sub>O-H<sub>2</sub>O, H<sub>2</sub>-CH<sub>4</sub>, H<sub>2</sub>-H<sub>2</sub>, H<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-H<sub>2</sub>O, CO<sub>2</sub>-CO<sub>2</sub>, CO<sub>2</sub>-H<sub>2</sub>, CO<sub>2</sub>-CH<sub>4</sub>
- **UV cross-sections**: No
- **Sources**: DACE
- **k-term tolerance**: 1.00E-02
- **SOCRATES version**: 2403
- **Date**: 2024-07-07
- **Platform**: Linux Intel
- **Creator**: Harrison Nicholls

### Rocks

- **Bands**:
    - 256: High resolution file used for comparison with JWST observations of rock-vapour atmospheres.
    - 128: Rock vapours and key volatiles.
    - 64: Rock vapours and key volatiles (low resolution).
- **Zenodo records**: [256](https://zenodo.org/records/15806423 "Rocks 256 on Zenodo"), [128](https://zenodo.org/records/15806401 "Rocks 128 on Zenodo"), [64](https://zenodo.org/records/15806381 "Rocks 64 on Zenodo")
- **Absorbers**: 256 bands: O<sub>2</sub>, SiO, SiO<sub>2</sub>; 128 and 64 bands: H<sub>2</sub>, H<sub>2</sub>O, O<sub>2</sub>, SiO, SiO<sub>2</sub>
- **Continua**: 256 bands: O<sub>2</sub>-O<sub>2</sub>; 128 and 64 bands: H<sub>2</sub>O-H<sub>2</sub>O, H<sub>2</sub>-H<sub>2</sub>, O<sub>2</sub>-O<sub>2</sub>
- **UV cross-sections**: No
- **Sources**: DACE
- **k-term tolerance**: ?
- **SOCRATES version**: 2407.2
- **Date**: 2025-05-15
- **Platform**: Linux Intel
- **Creator**: Alex McGinty

### Winterfell

- **Bands**:
    - 4096: Honeyside but with UV included for some molecules. Very high-resolution.
    - 256: High resolution.
    - 48: Medium resolution.
    - 16: Low-resolution.
- **Zenodo records**: [4096](https://zenodo.org/records/18402082 "Winterfell 4096 on Zenodo"), [256](https://zenodo.org/records/18402159 "Winterfell 256 on Zenodo"), [48](https://zenodo.org/records/18402184 "Winterfell 48 on Zenodo"), [16](https://zenodo.org/records/18402217 "Winterfell 16 on Zenodo")
- **Absorbers**: H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub>, NH<sub>3</sub>, SO<sub>2</sub>, N<sub>2</sub>O, O<sub>3</sub>, HCN, H<sub>2</sub>S, O<sub>2</sub>
- **Continua**: H<sub>2</sub>O-H<sub>2</sub>O, H<sub>2</sub>-CH<sub>4</sub>, H<sub>2</sub>-H<sub>2</sub>, H<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-H<sub>2</sub>O, CO<sub>2</sub>-CO<sub>2</sub>, CO<sub>2</sub>-H<sub>2</sub>, CO<sub>2</sub>-CH<sub>4</sub>
- **UV cross-sections**: CO<sub>2</sub>, H<sub>2</sub>O, H<sub>2</sub>S, N<sub>2</sub>, N<sub>2</sub>O, NH<sub>3</sub>, O<sub>3</sub>, SO<sub>2</sub> (see [UV cross-sections](#uv-cross-sections))
- **Sources**: DACE, MPI
- **k-term tolerance**: ?
- **SOCRATES version**: 2407.2
- **Date**: 2026-01-12
- **Platform**: Linux Intel
- **Creator**: Bruna Fena

### Dragonstone

- **Bands**:
    - 4096: Same as Lighthouse but no O<sub>2</sub> included. Very high-resolution.
    - 256: High resolution.
    - 48: Medium resolution.
    - 16: Low-resolution.
- **Zenodo records**: [4096](https://zenodo.org/records/18922546 "Dragonstone 4096 on Zenodo"), [256](https://zenodo.org/records/18910878 "Dragonstone 256 on Zenodo"), [48](https://zenodo.org/records/18922528 "Dragonstone 48 on Zenodo"), [16](https://zenodo.org/records/18922335 "Dragonstone 16 on Zenodo")
- **Absorbers**: H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub>, NH<sub>3</sub>, SO<sub>2</sub>, N<sub>2</sub>O, O<sub>3</sub>, HCN, H<sub>2</sub>S
- **Continua**: H<sub>2</sub>O-H<sub>2</sub>O, H<sub>2</sub>-CH<sub>4</sub>, H<sub>2</sub>-H<sub>2</sub>, H<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-H<sub>2</sub>O, CO<sub>2</sub>-CO<sub>2</sub>, CO<sub>2</sub>-H<sub>2</sub>, CO<sub>2</sub>-CH<sub>4</sub>
- **UV cross-sections**: CO<sub>2</sub>, H<sub>2</sub>O, H<sub>2</sub>S, N<sub>2</sub>, N<sub>2</sub>O, NH<sub>3</sub>, O<sub>3</sub>, SO<sub>2</sub> (see [UV cross-sections](#uv-cross-sections))
- **Sources**: DACE, MPI
- **k-term tolerance**: ?
- **SOCRATES version**: 2407.2
- **Date**: 2026-01-12
- **Platform**: Linux Intel
- **Creator**: Bruna Fena

### Sunspear

- **Bands**:
    - 4096: To simulate Ranjan and Sasselov (2016), only CO<sub>2</sub>, SO<sub>2</sub> and H<sub>2</sub>S have UV values. Very high-resolution.
    - 256: High resolution.
    - 48: Medium resolution.
    - 16: Low-resolution.
- **Zenodo records**: no Zenodo record found
- **Absorbers**: H<sub>2</sub>O, H<sub>2</sub>, CO<sub>2</sub>, CO, CH<sub>4</sub>, N<sub>2</sub>, NH<sub>3</sub>, SO<sub>2</sub>, N<sub>2</sub>O, O<sub>3</sub>, HCN, H<sub>2</sub>S, O<sub>2</sub>
- **Continua**: H<sub>2</sub>O-H<sub>2</sub>O, H<sub>2</sub>-CH<sub>4</sub>, H<sub>2</sub>-H<sub>2</sub>, H<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-H<sub>2</sub>O, CO<sub>2</sub>-CO<sub>2</sub>, CO<sub>2</sub>-H<sub>2</sub>, CO<sub>2</sub>-CH<sub>4</sub>
- **UV cross-sections**: CO<sub>2</sub>, SO<sub>2</sub>, H<sub>2</sub>S (see [UV cross-sections](#uv-cross-sections))
- **Sources**: DACE, MPI
- **k-term tolerance**: ?
- **SOCRATES version**: 2407.2
- **Date**: 2026-01-12
- **Platform**: Linux Intel
- **Creator**: Bruna Fena

### Snowline

Water. Made with `spectraltools`; see [Building spectral files](../Explanations/spectraltools_pipeline.md).

- **Bands**:
    - 2048: Very high resolution. Intended for benchmarking.
    - 256: High resolution.
    - 128: Medium resolution.
    - 64: Low resolution.
    - 32: Low resolution.
- **Absorbers**: H<sub>2</sub>O
- **Continua**: H<sub>2</sub>O-H<sub>2</sub>O
- **UV cross-sections**: No
- **Sources**: EXOMOL, ExoCross, MT_CKD
- **k-term tolerance**: 5.00E-03
- **Maximum absorber path**: 10³ kg m⁻² (H<sub>2</sub>O); 10³ kg² m⁻⁵ for the continuum
- **SOCRATES version**: 2607.3
- **Date**: 2026-10-29
- **Platform**: Linux
- **Creator**: Harrison Nicholls
- Also contains water droplet scattering data (block 10).
- **References**: line list Polyansky et al. 2018; MT_CKD Mlawer et al. 2012, 2023. Also cite the ExoMol database references (Tennyson et al. 2024) and the ExoCross and PyExoCross references (Yurchenko et al. 2018; Zhang et al. 2024). Details and links are in [Opacity data and references](#opacity-data-and-references).

### Breezehome

Oxidised volatiles. Made with `spectraltools`; see [Building spectral files](../Explanations/spectraltools_pipeline.md).

- **Bands**:
    - 2048: Very high resolution. Intended for benchmarking.
    - 256: High resolution.
    - 128: Medium resolution.
    - 64: Low resolution.
    - 32: Low resolution.
- **Absorbers**: H<sub>2</sub>O, CO<sub>2</sub>, CO, O<sub>2</sub>, SO<sub>2</sub>, OCS, S<sub>2</sub>
- **Continua**: H<sub>2</sub>O-H<sub>2</sub>O, O<sub>2</sub>-CO<sub>2</sub>, O<sub>2</sub>-O<sub>2</sub>, CO<sub>2</sub>-CO<sub>2</sub>, CO<sub>2</sub>-H<sub>2</sub>O
- **UV cross-sections**: No
- **Sources**: EXOMOL, ExoCross, HITRAN CIA, MT_CKD
- **k-term tolerance**: 5.00E-03
- **Maximum absorber path**: 10³ kg m⁻² for every gas; 10³ kg² m⁻⁵ for the continua
- **SOCRATES version**: 2607.4
- **Date**: 2026-10-29
- **Platform**: Linux
- **Creator**: Harrison Nicholls
- Also contains water droplet scattering data (block 10).
- **References**: line lists Polyansky et al. 2018, Yurchenko et al. 2025, Tao et al. 2026, Somogyi et al. 2026, Underwood et al. 2016, Tóbiás et al. 2018, Owens et al. 2024, Gomez et al. 2024; the CIA references for O<sub>2</sub>-CO<sub>2</sub>, O<sub>2</sub>-O<sub>2</sub>, CO<sub>2</sub>-CO<sub>2</sub> and CO<sub>2</sub>-H<sub>2</sub>O; MT_CKD Mlawer et al. 2012, 2023. Also cite the ExoMol database references (Tennyson et al. 2024), the ExoCross and PyExoCross references (Yurchenko et al. 2018; Zhang et al. 2024) and the three HITRAN CIA overview papers. Details and links are in [Opacity data and references](#opacity-data-and-references).

### Cliffshade

Reduced volatiles. Made with `spectraltools`; see [Building spectral files](../Explanations/spectraltools_pipeline.md).

- **Bands**:
    - 2048: Very high resolution. Intended for benchmarking.
    - 256: High resolution.
    - 128: Medium resolution.
    - 64: Low resolution.
    - 32: Low resolution.
- **Absorbers**: H<sub>2</sub>, CO, CH<sub>4</sub>, S<sub>2</sub>, H<sub>2</sub>S, N<sub>2</sub>, NH<sub>3</sub>
- **Continua**: H<sub>2</sub>-CH<sub>4</sub>, H<sub>2</sub>-H<sub>2</sub>, N<sub>2</sub>-H<sub>2</sub>, N<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-CH<sub>4</sub>, CH<sub>4</sub>-CH<sub>4</sub>
- **UV cross-sections**: No
- **Sources**: EXOMOL, HITEMP, ExoCross, DACE, HITRAN CIA
- **k-term tolerance**: 5.00E-03
- **Maximum absorber path**: 10³ kg m⁻² for every gas; 10³ kg² m⁻⁵ for the continua
- **SOCRATES version**: 2607.4
- **Date**: 2026-10-29
- **Platform**: Linux
- **Creator**: Harrison Nicholls
- **References**: line lists Roueff et al. 2019 (paper and data set), Tao et al. 2026, Hargreaves et al. 2020, Gomez et al. 2024, Azzam et al. 2016, Chubb et al. 2018, Western et al. 2018, Western 2017, Shemansky 1969, Jans 2024, Coles et al. 2019, Al Derzi et al. 2015; DACE (Grimm & Heng 2015, Grimm et al. 2021, HELIOS-K); HITEMP (Rothman et al. 2010); the CIA references for H<sub>2</sub>-CH<sub>4</sub>, H<sub>2</sub>-H<sub>2</sub>, N<sub>2</sub>-H<sub>2</sub>, N<sub>2</sub>-N<sub>2</sub>, N<sub>2</sub>-CH<sub>4</sub> and CH<sub>4</sub>-CH<sub>4</sub>. Also cite the ExoMol database references (Tennyson et al. 2024), the ExoCross and PyExoCross references (Yurchenko et al. 2018; Zhang et al. 2024) and the three HITRAN CIA overview papers. Details and links are in [Opacity data and references](#opacity-data-and-references).

### Volenfell

Rock vapours. Made with `spectraltools`; see [Building spectral files](../Explanations/spectraltools_pipeline.md).

- **Bands**:
    - 2048: Very high resolution. Intended for benchmarking.
    - 256: High resolution.
    - 128: Medium resolution.
    - 64: Low resolution.
    - 32: Low resolution.
- **Absorbers**: CO, O<sub>2</sub>, SiO, TiO, MgO, Na, K, Fe
- **Continua**: O<sub>2</sub>-O<sub>2</sub>
- **UV cross-sections**: No
- **Sources**: EXOMOL, ExoAtom, ExoCross, HITRAN CIA
- **k-term tolerance**: 5.00E-03
- **Maximum absorber path**: 10³ kg m⁻² for CO and O<sub>2</sub>, 10 kg m⁻² for SiO, TiO, MgO, Na, K and Fe; 10³ kg² m⁻⁵ for the continuum
- **SOCRATES version**: 2607.4
- **Date**: 2026-10-29
- **Platform**: Linux
- **Creator**: Harrison Nicholls
- **References**: line lists Tao et al. 2026, Somogyi et al. 2026, Yurchenko et al. 2021, McKemmish et al. 2019, 2024, Li et al. 2019, Kramida et al. 2024; ExoAtom (Ni et al. 2026); the CIA references for O<sub>2</sub>-O<sub>2</sub>. Also cite the ExoMol database references (Tennyson et al. 2024), the ExoCross and PyExoCross references (Yurchenko et al. 2018; Zhang et al. 2024) and the three HITRAN CIA overview papers. Details and links are in [Opacity data and references](#opacity-data-and-references).

### Proudspire

Combined volatiles. Made with `spectraltools`; see [Building spectral files](../Explanations/spectraltools_pipeline.md).

- **Bands**: 2048, 256, 128, 64, 32
- **Gases (line list)**: H<sub>2</sub>O (POKAZATEL), H<sub>2</sub> (RACPPK), CO<sub>2</sub> (Dozen), CO (4thplus), O<sub>2</sub> (SWYT), O<sub>3</sub> (HITRAN2024), CH<sub>4</sub> (HITEMP2020), SO<sub>2</sub> (ExoAmes), OCS (OYT8), S<sub>2</sub> (Gomez), H<sub>2</sub>S (AYT2), N<sub>2</sub> (WCCRMT), NH<sub>3</sub> (CoYuTe), HCN (Harris)

### Skyborn

Hot Jupiters. Made with `spectraltools`; see [Building spectral files](../Explanations/spectraltools_pipeline.md).

- **Bands**: 2048, 256, 128, 64, 32
- **Gases (line list)**: H<sub>2</sub>O (POKAZATEL), H<sub>2</sub> (RACPPK), CO<sub>2</sub> (Dozen), CO (4thplus), SiO (SiOUVenIR), TiO (Toto), VO (VOMYT), MgO (LiTY), Na (NIST), K (NIST), Fe (NIST)

### Atmora

Rock vapours and volatiles (smaller set). Made with `spectraltools`; see [Building spectral files](../Explanations/spectraltools_pipeline.md).

- **Bands**: 2048, 256, 128, 64, 32
- **Gases (line list)**: H<sub>2</sub>O (POKAZATEL), H<sub>2</sub> (RACPPK), CO<sub>2</sub> (Dozen), CO (4thplus), O<sub>2</sub> (SWYT), CH<sub>4</sub> (HITEMP2020), SO<sub>2</sub> (ExoAmes), S<sub>2</sub> (Gomez), H<sub>2</sub>S (AYT2), NH<sub>3</sub> (CoYuTe), SiO (SiOUVenIR), TiO (Toto), Na (NIST), K (NIST)

The gas list for Atmora is taken from the planning sheet; the build script `spectraltools/Tmake_spectralfile.py` currently lists Atmora without S<sub>2</sub> and H<sub>2</sub>S.

### Sovngarde

Rock vapours and volatiles (larger set). Made with `spectraltools`; see [Building spectral files](../Explanations/spectraltools_pipeline.md).

- **Bands**: 2048, 256, 128, 64, 32
- **Gases (line list)**: H<sub>2</sub>O (POKAZATEL), H<sub>2</sub> (RACPPK), CO<sub>2</sub> (Dozen), CO (4thplus), O<sub>2</sub> (SWYT), O<sub>3</sub> (HITRAN2024), CH<sub>4</sub> (HITEMP2020), SO<sub>2</sub> (ExoAmes), OCS (OYT8), S<sub>2</sub> (Gomez), H<sub>2</sub>S (AYT2), N<sub>2</sub> (WCCRMT), NH<sub>3</sub> (CoYuTe), HCN (Harris), SiO (SiOUVenIR), TiO (Toto), MgO (LiTY), Na (NIST), K (NIST), Fe (NIST)

The line list for each gas is the same as in the [line opacity table](#line-opacities).

---

## Opacity data and references

This section lists the data used by the Generation III files, and the references to cite for them; each family's own list is in its subsection above. All references below are in the BibTeX file [proteus_spectral_file_references.bib](proteus_spectral_file_references.bib). They were taken from each data provider's recommended citation and checked against the Crossref or DataCite record (or against the provider's page where there is no DOI).

### Line opacities

PyExoCross cross-sections were computed from the line list with the line-wing cut-off given. DACE cross-sections were downloaded from DACE, which computes them with HELIOS-K; their cut-off is set by DACE and has not been checked.

| Species | Line list | Database and cross-sections | References |
|---------|-----------|-----------------------------|------------|
| H<sub>2</sub>O | POKAZATEL | ExoMol; PyExoCross, cut-off 25 cm⁻¹ | [Polyansky et al. 2018](https://doi.org/10.1093/mnras/sty1877) |
| H<sub>2</sub> | RACPPK | ExoMol; PyExoCross, cut-off 100 cm⁻¹ | [Roueff et al. 2019](https://doi.org/10.1051/0004-6361/201936249); data set [VizieR J/A+A/630/A58](https://doi.org/10.26093/cds/vizier.36300058) |
| CO<sub>2</sub> | Dozen | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Yurchenko et al. 2025](https://doi.org/10.1093/mnras/staf2135) |
| CO | 4thplus | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Tao et al. 2026](https://doi.org/10.1093/mnras/stag985) |
| O<sub>2</sub> | SWYT | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Somogyi et al. 2026](https://doi.org/10.1093/mnras/stag1279) |
| SO<sub>2</sub> | ExoAmes | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Underwood et al. 2016](https://doi.org/10.1093/mnras/stw849); [Tóbiás et al. 2018](https://doi.org/10.1016/j.jqsrt.2018.01.006) |
| OCS | OYT8 | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Owens et al. 2024](https://doi.org/10.1093/mnras/stae1110). ExoMol also lists a second paper, marked as submitted; it is not included here. |
| S<sub>2</sub> | Gomez | HITRAN-format line list hosted by ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Gomez et al. 2024](https://doi.org/10.1093/mnras/stae246) |
| H<sub>2</sub>S | AYT2 | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Azzam et al. 2016](https://doi.org/10.1093/mnras/stw1133); [Chubb et al. 2018](https://doi.org/10.1016/j.jqsrt.2018.07.012) |
| N<sub>2</sub> | WCCRMT | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Western et al. 2018](https://doi.org/10.1016/j.jqsrt.2018.07.017); [Western 2017](https://doi.org/10.1016/j.jqsrt.2016.04.010); [Shemansky 1969](https://doi.org/10.1063/1.1672058); [Jans 2024](https://doi.org/10.1016/j.jqsrt.2023.108809) |
| CH<sub>4</sub> | HITEMP2020 | HITEMP; cross-sections from DACE | [Hargreaves et al. 2020](https://doi.org/10.3847/1538-4365/ab7a1a) |
| NH<sub>3</sub> | CoYuTe | ExoMol; cross-sections from DACE | [Coles et al. 2019](https://doi.org/10.1093/mnras/stz2778); [Al Derzi et al. 2015](https://doi.org/10.1016/j.jqsrt.2015.03.034) |
| SiO | SiOUVenIR | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Yurchenko et al. 2021](https://doi.org/10.1093/mnras/stab3267) |
| TiO | Toto | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [McKemmish et al. 2019](https://doi.org/10.1093/mnras/stz1818); [McKemmish et al. 2024](https://doi.org/10.1093/rasti/rzae037) |
| MgO | LiTY | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Li et al. 2019](https://doi.org/10.1093/mnras/stz912) |
| Na, K, Fe | NIST (ExoAtom data set version 20240901) | ExoAtom; PyExoCross, cut-off 100 cm⁻¹ | [Kramida et al. 2024, NIST ASD](https://doi.org/10.18434/T4W30F); [Ni et al. 2026](https://doi.org/10.1093/rasti/rzaf065) |
| O<sub>3</sub> | HITRAN2024 | HITRAN; PyExoCross, cut-off 40 cm⁻¹ | [Gordon et al. 2026](https://doi.org/10.1016/j.jqsrt.2026.109807) |
| HCN | Harris | ExoMol; PyExoCross, cut-off 40 cm⁻¹ | [Harris et al. 2006](https://doi.org/10.1111/j.1365-2966.2005.09960.x); [Barber et al. 2014](https://doi.org/10.1093/mnras/stt2011) |
| VO | VOMYT | ExoMol; cross-sections from DACE | [McKemmish et al. 2016](https://doi.org/10.1093/mnras/stw1969) |

### Continua

HITRAN CIA files are from the HITRAN `main` folder, except CH<sub>4</sub>-CH<sub>4</sub> and CH<sub>4</sub>-Ar, which are only in the `alternate` folder. The HITRAN CIA overview papers should be cited alongside the original sources: [Terragni et al. 2025](https://doi.org/10.1016/j.jqsrt.2025.109631) (the reference that the HITRAN CIA page gives), [Karman et al. 2019](https://doi.org/10.1016/j.icarus.2019.02.034) and [Richard et al. 2012](https://doi.org/10.1016/j.jqsrt.2011.11.004).

| Pair | Data | Original references |
|------|------|---------------------|
| H<sub>2</sub>O-H<sub>2</sub>O | MT_CKD 4.3 self-continuum (`absco-ref_wv-mt-ckd4p3.nc`) | [Mlawer et al. 2012](https://doi.org/10.1098/rsta.2011.0295); [Mlawer et al. 2023](https://doi.org/10.1016/j.jqsrt.2023.108645) |
| H<sub>2</sub>-CH<sub>4</sub> | `H2-CH4_norm_2011.cia` | [Borysow & Frommhold 1986, ApJ 304](https://doi.org/10.1086/164221) |
| H<sub>2</sub>-H<sub>2</sub> | `H2-H2_2011.cia` | [Abel et al. 2011](https://doi.org/10.1021/jp109441f) |
| N<sub>2</sub>-H<sub>2</sub> | `N2-H2_2024.cia` | [Borysow & Frommhold 1986, ApJ 303](https://doi.org/10.1086/164096); [Wei et al. 2024](https://doi.org/10.1016/j.ijhydene.2024.10.318) |
| N<sub>2</sub>-N<sub>2</sub> | `N2-N2_2021.cia` | [Chistikov et al. 2019](https://doi.org/10.1063/1.5125756); [Baranov et al. 2005](https://doi.org/10.1016/j.jms.2005.06.008); [Lafferty et al. 1996](https://doi.org/10.1364/ao.35.005911); [Hartmann et al. 2017](https://doi.org/10.1002/2016jd025677) |
| N<sub>2</sub>-CH<sub>4</sub> | `N2-CH4_2024.cia` | [Finenko et al. 2022](https://doi.org/10.3847/1538-4365/ac36d3) |
| O<sub>2</sub>-CO<sub>2</sub> | `O2-CO2_2024.cia` | [Banerjee et al. 2019](https://doi.org/10.1039/c8cp06778c); [Vangvichith et al. 2009](https://doi.org/10.1016/j.jqsrt.2009.06.002) |
| O<sub>2</sub>-O<sub>2</sub> | `O2-O2_2024.cia` | [Baranov et al. 2005](https://doi.org/10.1016/j.jms.2005.06.008); [Mondelain et al. 2019](https://doi.org/10.1029/2018jd029317); [Kassi et al. 2021](https://doi.org/10.1029/2021jd034860); [Adkins et al. 2023](https://doi.org/10.1016/j.jqsrt.2023.108732); [Karman et al. 2018](https://doi.org/10.1038/s41557-018-0015-x); [Spiering & van der Zande 2012](https://doi.org/10.1039/c2cp40961e); [Tran et al. 2006](https://doi.org/10.1029/2005jd006869); [Spiering et al. 2011](https://doi.org/10.1039/c1cp20403c); [Thalman & Volkamer 2013](https://doi.org/10.1039/c3cp50968k); [Finkenzeller & Volkamer 2022](https://doi.org/10.1016/j.jqsrt.2021.108063) |
| CO<sub>2</sub>-CO<sub>2</sub> | `CO2-CO2_2024.cia` | [Gruszka & Borysow 1997](https://doi.org/10.1006/icar.1997.5773); [Baranov et al. 2004](https://doi.org/10.1016/j.jms.2004.04.010); [Terragni et al. 2025](https://doi.org/10.1016/j.jqsrt.2025.109595); [Baranov et al. 2003](https://doi.org/10.1007/978-94-010-0025-3_12); [Tran et al. 2024](https://doi.org/10.1016/j.icarus.2024.116265); [Baranov 2018](https://doi.org/10.1016/j.jms.2017.11.005) |
| CO<sub>2</sub>-H<sub>2</sub>O | `CO2-H2O_2024.cia` | [Fleurbaey et al. 2022](https://doi.org/10.1016/j.jqsrt.2022.108162) |
| CH<sub>4</sub>-CH<sub>4</sub> | `CH4-CH4_2011.cia` (alternate folder) | [Borysow & Frommhold 1987](https://doi.org/10.1086/165426) |
| N<sub>2</sub>-H<sub>2</sub>O | `N2-H2O_2018.cia` | [Hartmann et al. 2018](https://doi.org/10.1063/1.5019994) |
| O<sub>2</sub>-N<sub>2</sub> | `O2-N2_2024.cia` | [Thibault et al. 1997](https://doi.org/10.1364/ao.36.000563); [Orlando et al. 1991](https://doi.org/10.1029/91jd02042); [Menoux et al. 1993](https://doi.org/10.1364/ao.32.000263); [Baranov et al. 2005](https://doi.org/10.1016/j.jms.2005.06.008); [Lafferty et al. 1996](https://doi.org/10.1364/ao.35.005911); [Mondelain et al. 2019](https://doi.org/10.1029/2018jd029317); [Kassi et al. 2021](https://doi.org/10.1029/2021jd034860); [Adkins et al. 2023](https://doi.org/10.1016/j.jqsrt.2023.108732); [Tran et al. 2006](https://doi.org/10.1029/2005jd006869) |
| CO<sub>2</sub>-H<sub>2</sub> | `CO2-H2_2024.cia` | [Turbet et al. 2020](https://doi.org/10.1016/j.icarus.2020.113762) |
| CO<sub>2</sub>-CH<sub>4</sub> | `CO2-CH4_2024.cia` | [Fakhardji et al. 2022](https://doi.org/10.1016/j.jqsrt.2022.108148) |

### General references

- **ExoMol database**: [Tennyson et al. 2024](https://doi.org/10.1016/j.jqsrt.2024.109083) (most recent release) and [Tennyson et al. 2016](https://doi.org/10.1016/j.jms.2016.05.002); optionally the data-format update [Corey et al. 2026](https://doi.org/10.1093/rasti/rzag081). ExoMol asks users to cite the line list papers as well.
- **ExoCross and PyExoCross**: [Yurchenko et al. 2018](https://doi.org/10.1051/0004-6361/201732531) (ExoCross); [Zhang et al. 2024](https://doi.org/10.1093/rasti/rzae016) (PyExoCross).
- **ExoAtom**: [Ni et al. 2026](https://doi.org/10.1093/rasti/rzaf065).
- **DACE and HELIOS-K**: [Grimm & Heng 2015](https://doi.org/10.1088/0004-637x/808/2/182); [Grimm et al. 2021](https://doi.org/10.3847/1538-4365/abd773), which describes the database; the [HELIOS-K repository](https://github.com/exoclime/HELIOS-K).
- **HITRAN2024**: [Gordon et al. 2026](https://doi.org/10.1016/j.jqsrt.2026.109807).
- **HITEMP**: [Rothman et al. 2010](https://doi.org/10.1016/j.jqsrt.2010.05.001); for CH<sub>4</sub>, also [Hargreaves et al. 2020](https://doi.org/10.3847/1538-4365/ab7a1a).
- **NIST Atomic Spectra Database**: [Kramida et al. 2024](https://doi.org/10.18434/T4W30F) (version 5.12; add the access date).
- **MT_CKD**: [Mlawer et al. 2012](https://doi.org/10.1098/rsta.2011.0295) and [Mlawer et al. 2023](https://doi.org/10.1016/j.jqsrt.2023.108645); AER and HITRAN also list [Mlawer et al. 2019](https://doi.org/10.1029/2018jd029508), and AER lists [Delamere et al. 2010](https://doi.org/10.1029/2009jd012968), [Payne et al. 2011](https://doi.org/10.1109/tgrs.2010.2091416) and the [MT_CKD_H2O software](https://github.com/AER-RC/MT_CKD_H2O).

### Additional references for Proudspire, Skyborn, Atmora and Sovngarde

Proudspire, Skyborn, Atmora and Sovngarde also need: Gordon et al. 2026 (O<sub>3</sub>; Proudspire, Sovngarde), Harris et al. 2006 and Barber et al. 2014 (HCN; Proudspire, Sovngarde), McKemmish et al. 2016 (VO; Skyborn), and the CIA references for N<sub>2</sub>-H<sub>2</sub>O, O<sub>2</sub>-N<sub>2</sub>, CO<sub>2</sub>-H<sub>2</sub> and CO<sub>2</sub>-CH<sub>4</sub> where both gases of a pair are present.

### Caveats

- **CO<sub>2</sub>-H<sub>2</sub>O**: the HITRAN data cover only 296 K and 5700–6300 cm⁻¹. They are used at all temperatures.
- **N<sub>2</sub>-H<sub>2</sub>O**: the HITRAN data cover 250–350 K.
- **CH<sub>4</sub>-CH<sub>4</sub> and CH<sub>4</sub>-Ar** come from HITRAN's `alternate` folder, which the HITRAN CIA readme describes as holding either alternative data or data "not generally recommended due to large uncertainties". CH<sub>4</sub>-Ar is not applied in any file here, since none contains Ar.
- **DACE coverage**: the DACE data stop at 2500 K for CH<sub>4</sub> (HITEMP2020), 1900 K for NH<sub>3</sub> (CoYuTe) and 2900 K or 4500 K for VO (VOMYT versions 1.0 and 2.0), and at 10³ bar. The files' grid reaches 5000 K and 10⁴ bar, so at the missing points these gases use the nearest available point. The DACE line-list versions used are not recorded in the build logs.
- **NIST ASD version**: the ExoAtom NIST data set is dated 20240901, before ASD version 5.12 was released, so the data may come from an earlier ASD version. The BibTeX entry follows NIST's current (version 5.12) citation form.
- **MT_CKD** is defined for line absorption cut at 25 cm⁻¹ with the Lorentzian "pedestal" removed. The H<sub>2</sub>O cross-sections use a 25 cm⁻¹ cut-off; whether the pedestal was removed has not been checked.
- **Original sources**: HITRAN (for O<sub>3</sub>) and HITEMP (for CH<sub>4</sub>) also ask users to cite the original source of each parameter used. Those per-line sources are not listed here.

---

### UV cross-sections

The files for the UV were taken from the MPI-Mainz UV/VIS Spectral Atlas:

- CO<sub>2</sub>: Archer et al. (2013); Cook et al. (1966); Kuo et al. (2004); Gallagher et al. (1988); Shaw et al. (1995); Shemansky (1972); Venot, O. et al. (2018).
- H<sub>2</sub>O: Gürtler et al. (1977); J.B. Burkholder; S.P. Sander; J. Abbatt; J.R. Barker; R.E. Huie; C.E. Kolb; M.J. Kurylo; V.L. Orkin and Wine (2015); Ranjan et al. (2020).
- H<sub>2</sub>S: Feng et al. (1999); Grosch et al. (2015); Wu and Chen (1998).
- N<sub>2</sub>: Souza and Srivastava (1994).
- N<sub>2</sub>O: Johnston and Graham (1974).
- NH<sub>3</sub>: Burton et al. (1993); Limão-Vieira et al. (2019).
- O<sub>3</sub>: Mason et al. (1996); Molina and Molina (1986); Serdyuchenko et al. (2014).
- SO<sub>2</sub>: Golomb et al. (1962); Olive (2015).

---

## Abbreviations

The data sources in the [spectral file details](#spectral-file-details) are abbreviated as follows:

  * **HITRAN** – [HITRAN linelist](https://hitran.org/)
  * **EXOMOL** — [ExoMol linelist](https://www.exomol.com/)
  * **DACE** — [DACE opacity database](https://dace.unige.ch/opacityDatabase/): cross-sections computed with HELIOS-K from published line lists, including ExoMol, HITRAN and HITEMP line lists.
  * **ExoCross** — Cross-sections computed from line lists with ExoCross. The Generation III files used PyExoCross, the Python version of ExoCross.
  * **ExoAtom** — [ExoAtom](https://www.exomol.com/exoatom/) database of atomic line lists in ExoMol format; its NIST data set is used here.
  * **HITEMP** — [HITEMP](https://hitran.org/hitemp/) high-temperature line database.
  * **HITRAN CIA** — [HITRAN collision-induced absorption](https://hitran.org/cia/) data.
  * **MT_CKD** — [MT_CKD](https://github.com/AER-RC/MT_CKD_H2O) water vapour continuum model; version 4.3 (self-continuum only) in Generation III.
  * **MPI** — MPI-Mainz UV/VIS Spectral Atlas (UV cross-sections; see [UV cross-sections](#uv-cross-sections)).
