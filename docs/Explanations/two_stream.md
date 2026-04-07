# Two-stream radiation code

!!! note
    This overview is taken from the technical guide by James Manners, John M. Edwards, Peter Hill & Jean-Claude Thelen  (Met Office, 2017), which can be found [here](https://github.com/FormingWorlds/SOCRATES/tree/main/docs/techguide). 

## Overview

The two-stream radiation code computes radiative fluxes throughout an atmospheric column, from which heating rates and related diagnostics are derived. The approach proceeds as follows:

1. The spectral region is divided into bands, each handled by a **spectral file** that encodes parametrizations and discretisation data.
2. Each band is subdivided into quasi-monochromatic regions, within which gaseous absorption coefficients are treated as fixed.
3. A **two-stream approximation** is applied in each quasi-monochromatic region, representing the radiance field with an upward diffuse flux, a downward diffuse flux, and (in the shortwave) a direct solar flux.
4. Partial fluxes are assembled into broad-band totals via weighted sums.

The spectral file is external and user-supplied, making the frequency discretisation flexible and decoupled from the radiation code itself. A spectral file generated for one version of the code remains compatible with future versions.

---

## Spectral integration

Let $F$ denote any flux (direct, diffuse, or net). The total flux is the sum over spectral bands:

$$F = \sum_j F_j^{(b)}$$

The flux in band $j$ is a weighted sum over quasi-monochromatic regions indexed $k$:

$$F_j^{(b)} = \sum_k w_k F_k^{(qm)}$$

where $w_k$ is the weight of the $k$-th region and $F_k^{(qm)}$ is the flux calculated for that region. The number of quasi-monochromatic calculations and their weights are determined by the **overlap treatment** for gaseous absorption and the data in the spectral file.

---

## Monochromatic flux calculation

The atmosphere is divided into **N homogeneous layers**, numbered 1 to N from the top. Boundaries (levels) are numbered 0 to N. The primary variables are:

| Region | Variables |
|---|---|
| Solar (shortwave) | Upward flux $U$, total downward flux $V$, direct solar flux $Z$ |
| Infra-red (longwave) | Upward and downward **differential** fluxes (actual flux minus $\pi B$), denoted $U$ and $V$ |

The net flux is $N = V - U$. Fluxes in a homogeneous-layer column obey the recurrence:

$$U_{i-1} = T_i U_i + R_i V_{i-1} + S_i^+$$

$$V_i = T_i V_{i-1} + R_i U_i + S_i^-$$

$$Z_i = T_{0i} Z_{i-1}$$

where $T$, $R$, and $T_0$ are the diffuse transmission, diffuse reflection, and direct transmission coefficients respectively.

**Boundary conditions:**

- *Top of atmosphere (solar):* $V_0 = Z_0 = \Phi_0 / \chi_0$, where $\Phi_0$ is the solar irradiance and $\chi_0$ is the secant of the solar zenith angle.
- *Top of atmosphere (IR):* $V_0 = 0$.
- *Surface (solar):* $U_N = \alpha_s Z_N + \alpha_d (V_N - Z_N)$, where $\alpha_s$ and $\alpha_d$ are the direct and diffuse surface albedos.
- *Surface (IR):* $U_N = \alpha_d V_N + \varepsilon^* \pi B^*$, where $\varepsilon^*$ is surface emissivity and $B^*$ is the Planckian function at the surface temperature.

**Source terms** $S^\pm$ arise from:

- *Solar:* Scattering of the direct beam into diffuse radiation.
- *IR:* Variations in the Planckian source function across the layer (linear or quadratic in the Unified Model to suppress grid-scale waves).

The Planckian function is fitted by a polynomial in temperature:

$$B = \sum_{k=0}^n \beta_k (\theta / \theta_R)^k$$

---

## Flux calculation: transmission and reflection coefficients

For a single layer (subscript $i$ dropped), the fundamental single-scattering properties are the **optical depth** $\tau$, **single-scattering albedo** $\omega$, and **asymmetry parameter** $g$.

These determine intermediate quantities $s$ and $d$ (see [Two-Stream Approximations](#two-stream-approximations) below), from which the layer coefficients are derived:

$$\lambda = \sqrt{sd}, \quad p = e^{-\lambda\tau}, \quad \Gamma = \frac{s - \lambda}{s + \lambda}$$

$$T = \frac{p(1 - \Gamma^2)}{1 - p^2\Gamma^2}, \quad R = \Gamma(1 - p^2) / (1 - p^2\Gamma^2)$$

Numerical care is required as these expressions become **indeterminate as $\tau \to 0$**: a small tolerance (square root of machine precision) is added to relevant terms, and asymptotic forms are used where appropriate.

---

## Two-stream approximations

The two-stream equations express diffuse fluxes $F^\pm$ in terms of two parameters $s$ and $d$ (where $s = \alpha_1 + \alpha_2$, $d = \alpha_1 - \alpha_2$). Several approximations are available:

| Approximation | $s$ | $d$ |
|---|---|---|
| **Eddington** | $\tfrac{3}{2}(1 - \omega g)$ | $2(1 - \omega)$ |
| **PIFM85** (Zdunkowski & Korb 1985) | $D - \tfrac{3}{2}\omega g$ | $D(1 - \omega)$, $D = 2$ (or $1.66$ in IR) |
| **Zdunkowski et al. 1980** | $2 - \tfrac{3}{2}\omega g - \tfrac{1}{2}\omega$ | $2(1 - \omega)$ |
| **Discrete ordinates** | $\sqrt{3}(1 - \omega g)$ | $\sqrt{3}(1 - \omega)$ |
| **Hemispheric mean** | $2(1 - \omega g)$ | $2(1 - \omega)$ |

---

## Delta-rescaling of single scattering properties

The crude angular representation in the two-stream equations introduces errors for strongly forward-scattering particles. The **$\delta$-rescaling** (Joseph et al. 1976) corrects this. A forward-scattering fraction $f = g^2$ is defined and the properties are transformed:

$$\tau \to \tau(1 - \omega f)$$

$$\omega \to \frac{\omega(1 - f)}{1 - \omega f}$$

$$g \to \frac{g - f}{1 - f}$$

---

## Single scattering properties by process

When multiple optical processes are active, their mass extinction and scattering coefficients are combined additively, with the asymmetry weighted by scattering coefficients:

$$k^{(e)} = \sum_j k_j^{(e)}, \quad k^{(s)} = \sum_j k_j^{(s)}, \quad g = \sum_j k_j^{(s)} g_j \Big/ \sum_j k_j^{(s)}$$

The optical depth and single-scattering albedo for a layer follow from:

$$\tau = k^{(e)} \Delta m, \quad \omega = k^{(s)} / k^{(e)}$$

where $\Delta m$ is the column mass.

### Gaseous absorption

For $M$ active gases in a band, the total gaseous mass extinction is:

$$k^{(e,g)} = \sum_j K_j^{(g)} q_j f_j(p, \theta)$$

where $K_j^{(g)}$ is a reference mass extinction coefficient, $q_j$ is the mixing ratio, and $f_j$ is a scaling function accounting for pressure and temperature variations.

**Scaling functions**: two forms are supported. The preferred form is:

$$f = \left(\frac{p + \Delta}{p_0 + \Delta}\right)^\alpha \left[1 + A\left(\frac{\theta - \theta_0}{\theta_0}\right) + B\left(\frac{\theta - \theta_0}{\theta_0}\right)^2\right]$$

where $\alpha$, $\Delta$, $A$, $B$ are fitted parameters ($\Delta$ represents Doppler broadening). Alternatively, coefficients may be interpolated directly from a **look-up table** in the spectral file (now the preferred method).

### Self-broadening of gases

When a gas has a volume mixing ratio close to unity, **self-broadening** from same-species collisions becomes important. The gas fraction (volume mixing ratio) is derived from mass mixing ratios, accounting for whether water vapour is included in the total density.

### Continuum absorption

Discrepancies far from line centres are represented by a **smoothly varying continuum**. The main continua are the **self-broadened** and **foreign-broadened** continua of water vapour:

$$k^{(e,c)} = K_f^{(c)} q_w f_f n_{b,f} + K_s^{(c)} q_w f_s n_{b,s}$$

where $q_w$ is the water vapour mixing ratio, $n_b$ is the molar density of the broadening species, and subscripts $f$ and $s$ denote foreign and self-broadened components. The implementation is based on the **CKD continuum model** (Clough et al. 1989). A more general continuum parametrisation also supports **collision-induced absorption (CIA)**.

### Aerosols

For each aerosol species in each band, extinctions are proportional to mass mixing ratio:

$$k^{(e,a)} = \sum_j K_j^{(e,a)} q_j, \quad k^{(s,a)} = \sum_j K_j^{(s,a)} q_j, \quad g^{(a)} = \sum_j K_j^{(s,a)} q_j g_j \Big/ k^{(s,a)}$$

There is no representation of size-distribution variation within the model. The **humidity dependence** of hygroscopic aerosol optical properties is handled via a look-up table in the spectral file.

### Rayleigh scattering

Represented by adding a **band-constant value** to the scattering and total extinctions. The asymmetry parameter for Rayleigh scattering is zero.

### Water droplets

Droplet properties depend on both mass mixing ratio $L$ and **effective radius** $r_e$. Three parametrisation forms are available:

**Slingo & Schrecker (1982):**
$$k^{(e)} = L(a + b/r_e), \quad k^{(s)} = k^{(e)}(1 - c - dr_e), \quad g = e + fr_e$$

**Ackerman & Stephens / Hu & Stamnes (1987/1993):**
$$k^{(e)} = L(a_1 r_e^{b_2} + c_1), \quad \ldots$$
*(More flexible but computationally expensive due to exponentials; rarely used in practice.)*

**Padé approximants** (recommended for wide size ranges):
$$k^{(e)} = L \cdot \frac{p_1 + p_2 r_e + p_3 r_e^2}{1 + p_4 r_e + p_5 r_e^2 + p_6 r_e^3}, \quad \ldots$$

### Ice crystals

Ice crystal parametrisation is more complex due to **irregular crystal shapes**. Several schemes are available:

| Scheme | Size Measure | Notes |
|---|---|---|
| Slingo & Schrecker analogy | Effective radius $r_e$ | Simplest; used in HadAM3 |
| Modified anomalous diffraction (Mitchell et al. 1996) | Mean max dimension $\bar{D}_l$ | Two quartic polynomials for small/large ranges |
| Fu (1996) / Fu et al. (1998) | Effective dimension $D_e$ | Proportional to volume/projected-area ratio |
| Baran et al. (2013) | Ice water content + temperature | Linked directly to GCM prognostic variables |
| Baran et al. (2014) | Ice water content only | No intermediate size variable |

The spectral file may contain data for multiple ice crystal types, selectable at runtime.

---

## Overlapping Gaseous Absorption

When multiple gases absorb in a band, their spectral lines may overlap. Full **random overlap** treatment is available but expensive. Faster approximations are provided:

### Equivalent extinction

An extension of the FESFT method (Ritter & Geleyn 1992). For minor gases, a single band-representative extinction coefficient is derived from a subsidiary calculation:

$$\bar{K} = \frac{\sum_r w_r K_r N_r}{\sum_r w_r N_r}$$

where $N_r$ is the net flux for the $r$-th k-term and $w_r$ is the corresponding weight. Variants using the **modulus of layer incident fluxes** are available for improved accuracy near temperature inversions.

In the solar region, minor gas direct transmissions are multiplicative and computed exactly; diffuse flux corrections use a grey equivalent extinction weighted by direct surface fluxes.

---

## Treatment of clouds

### Single column approach

A fractional cloud cover $W_i$ may be specified within each layer $i$, divided into $N_T$ types (stratiform water, stratiform ice, convective water, convective ice). Clouds are treated as **plane-parallel** with no three-dimensional effects.

The vertical overlapping of clouds is handled by coupling coefficients $u_{i,j,k}$ and $v_{i,j,k}$ that transfer fluxes between regions at layer boundaries, following a generalisation of Geleyn & Hollingsworth (1979).

Layers are decomposed into **regions** (clear, stratiform cloud, convective cloud), and fluxes within each region are assumed horizontally uniform.

### Cloud overlap schemes

Three assumptions are supported for computing the overlap area $Y_{i,j,k}$:

| Scheme | Description |
|---|---|
| **Random overlap** | $Y_{i,j,k} = X_{i,j} X_{i+1,k}$ |
| **Maximum-random overlap** | Similar regions are maximally overlapped; dissimilar ones randomly overlapped |
| **Exponential-random overlap** (Hogan & Illingworth 2000) | Combines random and maximum-random linearly via overlap coefficient $\alpha = \exp(-\delta p / p_0)$, where $\delta p$ is layer separation and $p_0$ is the decorrelation length |

Sub-grid scale cloud water content variability can be included by multiplying cloud water content by a **scaling factor**.

### Monte Carlo Independent Column Approximation (McICA)

McICA (Pincus et al. 2003) efficiently represents sub-grid cloud variability by sampling a different randomly chosen sub-column for each spectral integration point. Properties:

- Each sub-column layer is either overcast or cloud-free (no partial cloud).
- The resulting radiative profile is **unbiased** relative to a full ICA calculation but introduces **noise**.
- Sub-columns are generated by a stochastic cloud generator (Räisänen et al. 2004) using a **gamma distribution** for in-cloud water content.
- Fractional standard deviation may be set globally or parametrised from resolution and cloud properties (Hill et al. 2012, Boutle et al. 2013).
- McICA is currently available only when cloud is segregated by **phase** (not by type; no convection separation).

---

## Algorithmic details

### Algorithm overview

On entry to the radiation code:

1. Spectrally independent operations (cloud overlap, moist aerosol properties) are performed first.
2. Fluxes are computed band by band; broad-band fluxes are accumulated.
3. Within each band, single-scattering properties of non-gaseous species are computed (uniform across the band).
4. Gaseous overlap treatments generate sets of **pseudo-monochromatic calculations**.
5. In each pseudo-monochromatic calculation, the **linear two-stream equations are assembled and solved**.

### Solving the two-stream equations

The two-stream equations generate a banded linear system. Rather than applying a standard banded-matrix algorithm directly, a **set of algebraic recurrences** is constructed that follows Gaussian elimination while exploiting the pattern of zero entries. This minimises the operation count.

The algorithm proceeds in two stages:

**Forward sweep:** Relations of the form
$$U_{ij} = \sum_k \alpha_{i+1,jk} V_{ik} + G^+_{i+1,j}$$
are assembled upward from the surface boundary condition, progressively eliminating unknowns.

**Back substitution:** Once downward fluxes at each level are known, upward fluxes are recovered from the recurrence.

> **Technical note:** No pivoting is performed. Given that the single-scattering albedo $\omega$ is perturbed away from 1 to avoid rescaling singularities and that elimination begins at the surface with an albedo less than 1, pivoting is not required.

### Approximate scattering in the longwave

Full scattering is less critical in the longwave. An **iterative approximation** is used:

1. Assume the upward flux at each level is Planckian at the local temperature; set upward differential flux to zero and transmit downward from the top.
2. Knowing downward differential fluxes, compute upward fluxes working upward through the atmosphere.

This captures scattering effects on cloud emissivity but not the direct reflection of radiation from below a cloud. It significantly reduces execution time.

### Other fast algorithms

- **Ignoring LW scattering entirely:** Fastest option; flux equations reduce to pure transmission problems. Not recommended where clouds or dust cause significant LW scattering.
- **Hybrid scattering:** Different scattering treatments per k-term, specified in the spectral file. Restricts expensive full-scattering calculations to optically thin, scattering-important wavelengths. Gives significant speed improvements for small accuracy cost.

### The magnification factor

At grazing solar zenith angles, Earth's curvature causes the local zenith angle to increase along a ray path toward the Sun. A magnification factor could correct surface flux calculations, but would be inconsistent with column heating rate profiles (where the local zenith angle does not change with altitude). The code **omits the magnification factor**, prioritising accuracy of atmospheric heating rate profiles over surface flux accuracy at high zenith angles.

---

## References

| Topic | Reference |
|---|---|
| Two-stream core | Edwards & Slingo (1996), *Q. J. Roy. Meteorol. Soc.* |
| δ-rescaling | Joseph et al. (1976), *J. Atm. Sci.* |
| Water droplets (Slingo) | Slingo & Schrecker (1982), *Q. J. R. Meteorol. Soc.* |
| Water droplets (Padé) | Hu & Stamnes (1993), *J. Climate* |
| Ice crystals (anomalous diffraction) | Mitchell et al. (1996), *J. Atm. Sci.* |
| Ice crystals (aggregate) | Baran et al. (2001, 2013, 2014) |
| Equivalent extinction | Edwards (1996), *J. Atm. Sci.*; Ritter & Geleyn (1992) |
| Cloud overlap | Geleyn & Hollingsworth (1979); Hogan & Illingworth (2000) |
| McICA | Pincus et al. (2003), *J. Geophys. Res.* |
| Stochastic cloud generator | Räisänen et al. (2004), *Q. J. Roy. Meteorol. Soc.* |
| Water vapour continuum | Clough et al. (1989), *Atmos. Res.* |