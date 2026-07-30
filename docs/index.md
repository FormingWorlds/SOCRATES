# SOCRATES

<p class="subtitle">Suite Of Community RAdiative Transfer codes based on Edwards and Slingo</p>

[![License](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://github.com/FormingWorlds/SOCRATES/blob/main/LICENCE)
[![Docs](https://img.shields.io/github/actions/workflow/status/FormingWorlds/SOCRATES/docs.yaml?branch=main&label=Docs)](https://proteus-framework.org/SOCRATES/)

**SOCRATES** is the radiative transfer core of the [PROTEUS](https://proteus-framework.org/PROTEUS) coupled atmosphere-interior evolution framework, called by the radiative-convective atmosphere model [AGNI](https://www.h-nicholls.space/AGNI/). It is a high-performance code for computing fluxes, heating rates, and radiances in planetary atmospheres; its primary development and maintenance is led by the UK Met Office.


!!! info "PROTEUS framework"
    This documentation describes SOCRATES as integrated into the PROTEUS framework for exoplanet atmosphere modelling. The original Met Office repository can be found [here](https://github.com/MetOffice/socrates).

## Overview

SOCRATES solves the radiative transfer equation in a plane-parallel atmosphere, computing monochromatic and broad-band radiative quantities across the shortwave and longwave spectral regions. Its primary solver is the two-stream radiation code, driven by spectral files: pre-computed data files that encode absorption data, optical properties for gases, clouds, aerosols, and scattering. In PROTEUS, there are spectral files available created specifically for exoplanet applications, covering a wide range of atmospheric compositions.

The **official documentation PDFs** can be found [here](Reference/documentation_pdfs.md).

## Get started

<div class="grid cards" markdown>

-   :material-download: **Install SOCRATES**

    Set up SOCRATES with the guided
    installer.

    [Installation guide](How-to/installation.md){ .md-button .md-button--primary }

-   :material-school: **New to SOCRATES?**

    Start with the first-run tutorial.

    [First-run tutorial](Tutorials/first_run.md){ .md-button .md-button--primary }

-   :material-earth: **Understand the model**

    Understand the physics behind SOCRATES. 

    [Model overview](Explanations/overview.md){ .md-button .md-button--primary}

</div>

Need the full picture? See the [get started guide](getting_started.md).

## Citation and credit

If you make use of SOCRATES, please reference the scientific manuscripts
outlined in the [Bibliography](Reference/publications.md), state the code
version used, and include an acknowledgement. 

## License

SOCRATES is released under the [BSD 3-Clause Licence](https://github.com/FormingWorlds/SOCRATES/blob/main/LICENCE).

!!! info "Licenses across the PROTEUS framework"
    Different components within the PROTEUS framework carry different licenses. Please find information about the use of licenses within the PROTEUS framework on the website's [license page](https://proteus-framework.org/license/).

