# Physical model description

!!! note
    This overview is based on the SOCRATES technical guide by James Manners, John M. Edwards, Peter Hill & Jean-Claude Thelen (Met Office, 2017), which can be found [here](https://github.com/FormingWorlds/SOCRATES/tree/main/docs/techguide). It is under Crown Copyright. 

## What is SOCRATES?

SOCRATES (Suite Of Community RAdiative Transfer codes based on Edwards and Slingo) is a flexible radiative transfer code developed at the Met Office. It computes **radiative fluxes and heating rates** throughout an atmospheric column, and is designed to serve a wide range of applications; from weather prediction to climate modelling and exoplanet atmosphere research.

The code is structured around two core radiation solvers, supported by spectral files that encode the frequency discretisation and optical property data, and a well-defined interface to any calling model.

---

## Structure of the physical model

### Radiation solvers

SOCRATES provides two complementary approaches to solving the radiative transfer equation:

#### [Two-stream radiation code](two_stream.md)

The two-stream code is the primary solver for computing broad-band radiative fluxes and heating rates efficiently. It represents the angular dependence of the radiation field with just two streams — an upward and a downward diffuse flux — together with a direct solar beam in the shortwave. The key steps are:

1. The spectrum is divided into **bands**, each further subdivided into quasi-monochromatic regions using a k-distribution method.
2. Within each region, layer **transmission and reflection coefficients** are derived from the single-scattering properties (optical depth $\tau$, single-scattering albedo $\omega$, asymmetry parameter $g$).
3. A **two-stream approximation** (Eddington, PIFM, discrete ordinates, or hemispheric mean) is selected to close the system.
4. **$\delta$-rescaling** corrects for strong forward scattering.
5. The resulting linear system is solved by an efficient recurrence based on Gaussian elimination.

The code handles gaseous absorption (including overlapping gases and continua), aerosols, Rayleigh scattering, water droplets, and ice crystals. Cloud overlap is treated via random, maximum-random, or exponential-random schemes, with the Monte Carlo Independent Column Approximation (McICA) available for sub-grid cloud variability.

#### [Spherical harmonic radiance code](spherical_harmonic.md)

The spherical harmonic code solves for the full angular radiance field by expanding $I(\mathbf{x}, n)$ in spherical harmonics $Y_l^m(n)$. This provides greater angular resolution than the two-stream approach, at higher computational cost, and is suited to applications requiring accurate radiances (e.g. remote sensing simulations). Key features include:

- A **complementary function** built from eigensolutions of a symmetric tridiagonal system, with careful numerical stabilisation for conservative scattering and large optical depths.
- **Particular integrals** for thermal emission (linear and quadratic Planckian variation) and the direct solar beam, with regularisation for small optical depths.
- **Marshak boundary conditions** at the top of atmosphere, and a full **BRDF surface boundary condition**, including an ocean surface model with Fresnel reflection, Snell's law refraction, and particulate/absorption parametrisations.
- The **TMS source function technique** [^cite-NT88] to accelerate convergence by separating single and multiple scattering.
- A fast block-recurrence linear solver that reduces the dominant operation count from $O(18N^3 L)$ to $O(6N^3 L)$.

### [Spectral files](../spectral_files.md)

Both solvers rely on **spectral files**: external, user-supplied files that define the frequency discretisation and store all spectrally dependent optical property data. This includes:

- Band limits and solar fractions
- k-distribution fits for gaseous absorption
- Rayleigh scattering coefficients
- Planck function polynomial fits
- Parametrisations for cloud droplets, ice crystals, and aerosols

The separation of spectral data from the radiation code itself makes SOCRATES highly flexible: a spectral file generated for one version of the code remains compatible with future versions, and new gases, aerosols, or parametrisations can be added without modifying the solver.

### [Interface to the calling model](../interface.md)

SOCRATES is designed to be embedded in any atmospheric model through a clean, well-defined interface. All inputs and outputs are wrapped into eight structured types, `control`, `dimen`, `spectrum`, `atm`, `cld`, `aer`, `bound`, and `radout`, passed to the core routine `radiance_calc`. This design keeps the radiation code self-contained and straightforward to couple to new models.

---

## Choosing a solver

| | Two-stream | Spherical harmonic |
|---|---|---|
| **Primary output** | Fluxes, heating rates | Radiances |
| **Angular resolution** | Low (2 streams) | High (up to order $L$) |
| **Computational cost** | Low | High |
| **Typical use** | GCMs, NWP, climate runs | Remote sensing, offline studies |
| **Cloud treatment** | Single column or McICA | Single column |
| **Surface BRDF** | Albedo ($\alpha_s$, $\alpha_d$) | Full BRDF expansion |

For most atmospheric modelling applications the **two-stream code** is the appropriate choice. The **spherical harmonic code** is used where accurate radiance fields are needed.

[^cite-NT88]: T. Nakajima and M. Tanaka, *Algorithms for radiative intensity calculations in moderately thick atmospheres using a truncation approximation*, J. Quant. Spectrosc. Radiat. Transfer, 40:51–69, 1988.