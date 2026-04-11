# Integration into the PROTEUS framework

!!! note
    This page describes how SOCRATES is integrated into [AGNI](https://www.h-nicholls.space/AGNI/dev/), the radiative-convective atmosphere model of the [PROTEUS framework](https://proteus-framework.org/PROTEUS/). For full details of the AGNI model, including its convection, condensation, and chemistry schemes, see the [AGNI model description](https://www.h-nicholls.space/AGNI/dev/explanation/model/).

## The PROTEUS framework

PROTEUS is a coupled framework for modelling the formation and evolution of rocky planet atmospheres. It integrates a suite of specialist modules covering interior dynamics, atmospheric chemistry, escape, and climate. AGNI is the main atmospheric structure and climate module within this framework, responsible for computing the radiative-convective equilibrium temperature structure of the atmosphere at each timestep of a PROTEUS simulation.

## AGNI and radiative transfer

AGNI models a planetary atmosphere as a single 1D column, split into levels defined logarithmically in pressure space between the surface and the top of the atmosphere. AGNI nominally simulates radiative transfer using SOCRATES, which solves the radiative transfer equation using a two-stream solution. At each step of the solver loop, AGNI passes cell-centre temperatures, pressures, geometric heights, and gas mixing ratios to SOCRATES, which returns upward and downward spectral fluxes at all cell edges for both the shortwave and longwave components.

---

## Technical integration

AGNI is written in Julia while SOCRATES is written in Fortran. SOCRATES is accessed via a Julia interface originally written by Stuart Daines, with the SOCRATES binaries included directly in the precompiled AGNI code, which significantly improves performance. For aerosols, AGNI generates band-averaged optical properties files at runtime using `scatter_average_90`, then inserts these into the runtime spectral file using `prep_spec`, alongside the stellar spectrum and Rayleigh scattering terms.

---

## Opacity and absorption

Opacity is handled using the **correlated-k approximation**, with either random overlap or equivalent extinction used to account for overlapping absorption in mixtures of gases. The key data sources are:

- **Gas absorption cross-sections**: taken from [DACE](https://dace.unige.ch/opacityDatabase/)
- **Water vapour continuum**: estimated using the MT_CKD model
- **Other continua**: derived from HITRAN
- **Rayleigh scattering**, water cloud radiative properties, and aerosol parametrisations are also included

The spectral files used within PROTEUS have been generated specifically for exoplanet and planetary science applications, covering atmospheric compositions relevant to rocky planet evolution including H₂O, CO₂, CH₄, H₂, He, CO, N₂, NH₃, SO₂, and rock vapour species (SiO, SiO₂). Multiple spectral resolutions are available, from low-resolution files suitable for coupled PROTEUS runs to high-resolution files for benchmarking and comparison with observations such as JWST.

---

## Surface boundary conditions

Surface reflectivity can be modelled as a greybody with an albedo from 0 to 1. Alternatively, the surface can be modelled using empirical reflectance data that varies with wavelength. The file can tabulate any one of: spherical reflectance, hemispherical emissivity, or single scattering albedo.

---

## Validation

AGNI includes an interface to the [Reference Forward Model (RFM)](https://eodg.atm.ox.ac.uk/RFM/), which provides a straightforward way to validate and benchmark SOCRATES radiative transfer calculations independently.