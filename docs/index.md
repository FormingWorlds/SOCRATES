---
title: SOCRATES
hide: 
  - toc
  - navigation
---

<div style="padding-left: 1em; padding-right : 1em" markdown = 1>

# SOCRATES

<p class="subtitle">Suite Of Community RAdiative Transfer codes based on Edwards and Slingo</p>

SOCRATES is a high-performance radiative transfer code for computing fluxes, heating rates, and radiances in planetary atmospheres. Its primary development and maintenance is lead by the UK Met Office. SOCRATES is applied as the radiative transfer core of the [PROTEUS framework](https://proteus-framework.org/PROTEUS/), called by the radiative-convective atmosphere model [AGNI](https://www.h-nicholls.space/AGNI/).

!!! info "PROTEUS framework"
    This documentation describes SOCRATES as integrated into the PROTEUS framework for exoplanet atmosphere modelling. The original Met Office repository can be found [here](https://github.com/MetOffice/socrates).

## Overview

SOCRATES solves the radiative transfer equation in a plane-parallel atmosphere, computing monochromatic and broad-band radiative quantities across the shortwave and longwave spectral regions. Its primary solver is the two-stream radiation code, driven by spectral files: pre-computed data files that encode absorption data, optical properties for gases, clouds, aerosols, and scattering. In PROTEUS, there are spectral files available created specifically for exoplanet applications, covering a wide range of atmospheric compositions.

Installation steps are available in the tutorials page:

- [Installation](How-to/installation.md)


The official documentation PDFs can be found online:

 - [Technical guide](Reference/documentation_pdfs.md#technical-guide)
 - [User guide](Reference/documentation_pdfs.md#user-guide)


## Citation

Please cite these papers if you use SOCRATES:

- Edwards, J. M. and Slingo, A. (1996):  [10.1002/qj.49712253107](https://doi.org/10.1002/qj.49712253107)
- Manners, J. (2024):  [10.1063/5.0185476](https://doi.org/10.1063/5.0185476)

</div>