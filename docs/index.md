# SOCRATES 

<p class="subtitle">Suite Of Community RAdiative Transfer codes based on Edwards and Slingo</p>

SOCRATES is a high-performance radiative transfer code for computing fluxes, heating rates, and radiances in planetary atmospheres. Originally developed and maintained by the UK Met Office, it is used as the correlated-k radiative transfer core of the [PROTEUS framework](https://proteus-framework.org/PROTEUS/), called by the radiative-convective atmosphere model [AGNI](https://www.h-nicholls.space/AGNI/dev/). 

!!! info "PROTEUS framework"
    This documentation describes SOCRATES as integrated into the PROTEUS framework for exoplanet atmosphere modelling. The original Met Office repository can be found [here](https://github.com/MetOffice/socrates).

---
## Overview

SOCRATES solves the radiative transfer equation in a plane-parallel atmosphere, computing monochromatic and broad-band radiative quantities across the shortwave and longwave spectral regions. Its primary solver is the two-stream radiation code, driven by **spectral files**: external files that encode the frequency discretisation, absorption data, and optical properties for gases, clouds, aerosols, and scattering. In PROTEUS, there are spectral files available created specifically for exoplanet applications, covering a wide range of atmospheric compositions including H₂O, CO₂, CH₄, H₂, He, CO, N₂, NH₃, SO₂, and rock vapour species.




---

## Citation

If you use SOCRATES as part of PROTEUS, please cite the original code description:

- Edwards, J. M. and Slingo, A. (1996): Studies with a flexible new radiation code. I: Choosing a configuration for a large-scale model. *Q. J. Roy. Meteorol. Soc.*, 122, 689–719.
