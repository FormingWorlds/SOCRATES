# Spectral files

SOCRATES takes all of its spectrally dependent data from a **spectral file** supplied at run time, rather than from the code itself. The spectral file sets the bands and their limits, the gaseous absorbers and their k-terms in each band, continuum absorption, Rayleigh scattering, the data for the thermal source function, and the optical properties of clouds and aerosols. The choice of spectral file therefore fixes the spectral resolution and which absorbers and processes the radiation calculation can include.

[Spectral files](../Explanations/spectral_files.md) explains what spectral files are and what they contain, and [Building spectral files](../Explanations/spectraltools_pipeline.md) describes how the PROTEUS files are made with [`spectraltools`](https://github.com/FormingWorlds/SOCRATES/tree/main/spectraltools).

Two sets of spectral files are described in this reference:

- [PROTEUS spectral files](proteus_spectral_file_reference.md): files made for exoplanet and planetary atmospheres within the PROTEUS framework, identified by a codename and a band count and downloaded from Zenodo. Each one is a pair of files: `<Codename>.sf` and the k-coefficient lookup tables `<Codename>.sf_k`.
- [Met Office spectral files](spectral_file_reference.md): the standard files distributed with SOCRATES, developed for Earth atmosphere modelling in the Unified Model.

[Validation](spectral_file_validation.md) shows how the Generation III PROTEUS files reproduce the runaway greenhouse limit, and how their results change with the number of bands.
