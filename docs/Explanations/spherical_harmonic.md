# Spherical harmonic radiance code

!!! note
    This overview is based on the technical guide by James Manners, John M. Edwards, Peter Hill & Jean-Claude Thelen (Met Office, 2017), which can be found [here](../Reference/documentation_pdfs.md#technical-guide).  It is under Crown Copyright. 

## Overview

The spherical harmonic radiance code solves the monochromatic radiative transfer equation for **radiances** rather than integrated fluxes, expanding the angular dependence of the radiation field in spherical harmonics. This provides greater angular resolution than the two-stream approach, at higher computational cost, and is particularly suited to applications requiring accurate radiance fields (e.g. remote sensing simulations).

The monochromatic equation of transfer is:

$$(n \cdot \nabla) I(\mathbf{x}, n) = -(k^{(s)} + k^{(a)}) I(\mathbf{x}, n) + \frac{k^{(s)}}{4\pi} \int_\Omega I(\mathbf{x}, n') P(n', n)\, d\omega_{n'} + j(\mathbf{x}, n)$$

where $I$ is the radiance, $k^{(s)}$ and $k^{(a)}$ are the scattering and absorption coefficients, $P(n', n)$ is the phase function, and $j$ is the emission source term.

The phase function is expanded in Legendre polynomials:

$$P(n', n) = \sum_{l=0}^\infty (2l+1) g_l P_l(n' \cdot n)$$

and may be $\delta$-rescaled using the standard prescription $k^{(s)} \to (1-f)k^{(s)}$ before further treatment.

---

## Fundamentals of solving for radiances

Assuming a **plane-parallel atmosphere**, the radiance field is expanded in spherical harmonics $Y_l^m(n)$:

$$I(\mathbf{x}, n) = \sum_{l=0}^\infty \sum_{m=-l}^{l} I_{lm}(\mathbf{x}) Y_l^m(n) + I_\odot \delta(n' - n_\odot)$$

where the direct solar beam $I_\odot$ is kept separate. Using the orthogonality of the $Y_l^m$ and introducing optical depth $\tau$ and single-scattering albedo $\omega = k^{(s)} / (k^{(s)} + k^{(a)})$, the equation of transfer reduces to a coupled system:

$$c^+_{l-1,m} \frac{dI_{l-1,m}}{d\tau} + c^-_{l+1,m} \frac{dI_{l+1,m}}{d\tau} = s_l I_{lm}(\tau) - s_0 \sqrt{4\pi} B(\tau) \delta_{l0}\delta_{m0} - \omega g_l Y_l^{m*}(n_\odot) I_\odot(\tau)$$

where $s_l = 1 - \omega g_l$ and the Clebsch–Gordan coefficients are:

$$c^+_{lm} = \sqrt{\frac{(l+1-m)(l+1+m)}{(2l+1)(2l+3)}}, \qquad c^-_{lm} = \sqrt{\frac{(l-m)(l+m)}{(2l-1)(2l+1)}}$$

The atmosphere is divided into $N$ homogeneous layers with optical thicknesses $\tau_i$, $i = 1, \ldots, N$. The full solution in each layer is the sum of a **complementary function** and a **particular integral**.

---

## The complementary function

The complementary function consists of exponentials $H_{lm}(\mu) e^{\tau/\mu}$ for $\mu \in \mathbb{R}$. For fixed azimuthal order $m$, the permissible values of $\mu$ are defined by an eigenvalue problem. Truncating the spherical harmonic expansion at odd order $L$, the recurrence relations:

$$c^-_{m+1,m} H_{m+1,m} = s_m \mu H_{mm}$$

$$c^+_{l-1,m} H_{l-1,m} + c^-_{l+1,m} H_{l+1,m} = s_l \mu H_{lm}, \quad m < l < L'$$

$$c^+_{L'-1,m} H_{L'-1,m} = s_{L'} \mu H_{L'm}$$

where $L' = L$ if $m$ is even and $L' = L+1$ if $m$ is odd. Defining $K_{lm} = \sqrt{s_l} H_{lm}$, this becomes a symmetric tridiagonal eigenvalue problem:

$$\sum_l C_{ql} K_{lm} = \mu K_{lm}$$

with non-zero entries $C_{l-1,l} = c^+_{l-1,m}/\sqrt{s_l s_{l-1}}$.

**Numerical stability:** For $|\mu| > 1$ the recurrence has growing solutions triggered by rounding errors. The recurrence is therefore always applied in the direction of **decreasing** $l$. When scattering is nearly conservative, intermediate terms can overflow; the recurrence is recast in $H'_{lm} = \sigma^{-l} H_{lm}$ where $\sigma = 1/\max(1, 2\mu^{-1})$ to prevent this.

**Halving the eigenproblem:** Since eigenvalues come in $\pm\mu_k$ pairs, the even and odd components of the eigenvector decouple, halving the size of the matrix to be diagonalised. The eigenvalues of the reduced matrix have diagonal elements $d_j = E^2_{2j-1} + E^2_{2j}$ and sub-diagonal elements $e_j = E_{2j-2} E_{2j-1}$.

The complementary function in the $i$-th layer is written using only negative exponentials to avoid overflow:

$$I_{lm}(\tau) = \sum_k H^-_{lmk} e^{-\tau/\mu_k} + \sum_k H^+_{lmk} e^{-(\tau_i - \tau)/\mu_k}$$

**Conservative scattering** ($\omega \to 1$) causes the matrix $C$ to become singular for $m = 0$. This is handled by artificially reducing $\omega$ slightly to avoid ill-conditioning.

---

## Particular integrals

### Thermal radiation

In the infra-red, the equation of transfer is reformulated in terms of **differential radiances** $I' = I - B$. For a Planckian source varying **linearly** across a layer:

$$I_{i,10} = \frac{1}{s_{1i}} \sqrt{\frac{4\pi}{3}} \frac{\Delta B_i}{\tau_i}$$

with $I_{i,lm} = 0$ otherwise, where $\Delta B_i$ is the difference in the Planck function across layer $i$.

For **quadratic** variation of the Planckian:

$$I_{i,10} = \frac{1}{s_{1i}} \sqrt{\frac{4\pi}{3}} \frac{\Delta B_i}{\tau_i} - \frac{2}{s_{1i}} \sqrt{\frac{4\pi}{3}} \frac{\Delta^2 B_i}{\tau_i^2} \tau$$

$$I_{i,00} = -\frac{2 c^-_{1,0}}{s_{0i} s_{1i}} \sqrt{\frac{4\pi}{3}} \frac{\Delta^2 B_i}{\tau_i^2}, \qquad I_{i,20} = -\frac{2 c^+_{1,0}}{s_{2i} s_{1i}} \sqrt{\frac{4\pi}{3}} \frac{\Delta^2 B_i}{\tau_i^2}$$

**Small optical depths** cause ill-conditioning. This is resolved by adding to the particular integral a solution of the homogeneous system that exhibits the same singularity as $\tau \to 0$:

$$I_{l0} = q_0 s_1 \sum_k V_{kl} V_{k1} \left\{ (-1)^l e^{-\tau/\mu_k} - e^{-(\tau_i - \tau)/\mu_k} \right\}$$

where $V_{kl} = K_{klm}/\sqrt{s_l}$ and the coefficients $u^\pm_k = \mp q_0 s_1 V_{k1}$ are determined by matching the singularity structure.

### Solar particular integral

Using the convention $\mu_0 = -\cos\theta_\odot$, the direct solar beam in layer $i$ is:

$$I_{\odot i}(\tau) = I_\odot(\Delta_{i-1}) e^{-\tau/\mu_0}$$

A particular integral of the form $I_{ilm}(\tau) = Z_{ilm} e^{-\tau/\mu_0}$ is sought, giving the recurrence:

$$c^+_{l-1,m} Z_{i,l-1,m} + c^-_{l+1,m} Z_{i,l+1,m} = -\mu_0 s_{li} Z_{ilm} + \mu_0 I_\odot(\Delta_{i-1}) \omega_i g_{li} Y_l^{m*}(n_\odot)$$

with solution:

$$Z_{ilm} = -I_\odot(\Delta_{i-1}) Y_l^{m*}(n_\odot) + \gamma V_{ilm}(\mu_0)$$

where $\gamma = I_\odot(\Delta_{i-1}) Y_{L'+1}^{m*}(n_\odot) / V_{i,L'+1,m}(\mu_0)$ enforces the truncation condition, and $V(\mu_0)$ satisfies the associated homogeneous recurrence.

**Ill-conditioning** arises when $\mu_0$ approaches an eigenvalue $\mu_k$. This is removed by subtracting a weighted multiple of the corresponding eigensolution, applied smoothly via a weighting that depends on the separation $|\mu_0 - \mu_k|$ rather than an if-test.

---

## Boundary conditions

### Interior boundaries

Continuity of the radiance field at each interior level requires:

$$I_{i,lm}(\tau_i) = I_{i+1,lm}(0), \quad 1 \leq i \leq N, \quad \forall\, l, m$$

### Upper boundary

At the top of the atmosphere, the downward radiance is specified as $I(n) = I^{(0)}(n)$ for $n \in \Omega^-$. Since the full boundary condition cannot be imposed in a truncated system, **Marshak's conditions** [^cite-Marshak] are used — the inner product of the residual with odd-parity harmonics is set to zero:

$$\sum_l \kappa_{ll'm} (I_{lm} - I^{(0)}_{lm}) = 0$$

where:

$$\kappa_{ll'm} = \int_{\Omega^-} Y_l^m(n) Y_l^{m*}(n)\, d\omega_n$$

For $l + l'$ even, $\kappa_{ll'm} = \frac{1}{2} \delta_{ll'}$. For $l + l'$ odd, $\kappa_{ll'm}$ is evaluated analytically using associated Legendre polynomial identities:

$$\Upsilon^m_l(0) = -\sqrt{\frac{2l+1}{2l-3} \cdot \frac{l+m-1}{l+m} \cdot \frac{l-m-1}{l-m}}\, \Upsilon^m_{l-2}(0)$$

### Surface boundary conditions

The surface is characterised by a **bidirectional reflectance distribution function (BRDF)** $\gamma_r(n, n')$, so that:

$$I(n) = \int_{\Omega^-} \gamma_r(n, n') I(n') (n' \cdot {-\hat{e}_z})\, d\omega_{n'}, \quad n \in \Omega^+$$

For a Lambertian surface, $\gamma_r = \alpha/\pi$ where $\alpha$ is the albedo.

The BRDF is expanded in a double spherical harmonic series:

$$\gamma_r(n, n') = \sum_{l,m} \sum_{l',m'} \Gamma_{lml'm'} Y_l^m(n) Y_l^{m'*}(n')$$

Imposing rotational symmetry, reflectional symmetry, reciprocity ($\gamma_r(n,n') = \gamma_r(n',n)$), and the reality of $\gamma_r$ reduces the coefficients to real, symmetric quantities $\Psi_{ll'm}$ with $\Psi_{ll'-m} = \Psi_{ll'm}$.

The full surface boundary condition including thermal emission is:

$$I(n) = \int_{\Omega^-} \gamma_r(n, n') \left[ I(n') + I_\odot \delta(n' - n_\odot) - B^* \right] (n' \cdot {-\hat{e}_z})\, d\omega_{n'} + B^*$$

where $B^*$ is the isotropic Planckian radiance at the surface temperature, arising from Kirchhoff's law.

After applying Marshak's procedure and expanding, the boundary condition becomes:

$$\sum_\lambda I_{\lambda M} \left[ (-1)^\lambda \kappa_{L\lambda M} + \sum_j \rho_j \Phi_{jL\lambda M} \right] = I_\odot \mu_\odot \sum_j \rho_j \sum_{l'} Y_L^{M*}(n_\odot) \Xi_{jLl'M} + B^* \delta_{0M} \left[ \sqrt{4\pi} \kappa_{L00} + \sum_j \rho_j \Lambda_{jL} \right]$$

where $\Xi$, $\Phi$, and $\Lambda$ are precomputed geometric coupling matrices that depend only on the BRDF expansion coefficients $\rho_j$ and the $\kappa_{ll'm}$ integrals.

#### The BRDF of the ocean surface

The ocean surface BRDF is not available from a single direct reference [^cite-Mobley94]. The radiance code itself is used to compute the radiance within the ocean, with special upper boundary conditions to handle refraction. Key optical properties:

**Rayleigh scattering in water:**

$$k^{(s)}_w(\lambda) = K_R (\lambda_0/\lambda)^{4.32}$$

where $\lambda_0 = 550\,\text{nm}$, $K_R = 0.93$ (pure water) or $1.21$ (sea water).

**Particulate scattering** [^cite-Petzold72] is related to chlorophyll concentration $C$ (mg m$^{-3}$):

$$k^{(s)}_P = \left(\frac{550}{\lambda[\text{nm}]}\right)^{0.3} C^{0.62}$$

**Absorption** [^cite-Morel91] [^cite-PS81]:

$$k^{(a)} = \left( k^{(a)}_w(\lambda) + 0.66\, a^{*\prime}_c(\lambda)\, C^{0.65} \right) \left[ 1 + 0.2 \exp(-0.014(\lambda[\text{nm}] - 440)) \right]$$

**Refraction at the surface** follows Snell's law ($\sin\theta_i = n\sin\theta_t$, $n \approx 1.34$), with the Fresnel reflection coefficient for unpolarised light:

$$r_{aw} = \frac{1}{2} \left[ \left(\frac{\sin(\theta_i - \theta_t)}{\sin(\theta_i + \theta_t)}\right)^2 + \left(\frac{\tan(\theta_i - \theta_t)}{\tan(\theta_i + \theta_t)}\right)^2 \right]$$

Total internal reflection occurs for upward rays beyond the critical angle ($r_{wa} = 1$). The boundary condition in the ocean is:

$$I(n) = r_{wa} I(n_r) + (1 - r_{aw}) n^2 I_a(n_a), \quad n \in \Omega^-$$

---

## Numerical implementation

Since $I \in \mathbb{R}$, coefficients satisfy $I_{l,-m} = (-1)^m I_{lm}^*$, so only $m \geq 0$ need be stored. The complex $e^{im\phi}$ dependence factors out as $I_{lm} = C_{lm} e^{-im\phi_\odot}$, and the full radiance field reduces to:

$$I_{lm} Y_l^m + I_{l,-m} Y_l^{-m} = 2 C_{lm} \Upsilon^m_l \cos m(\phi - \phi_\odot)$$

reducing storage requirements by roughly a factor of two compared to a naive complex implementation.

---

## Increasing the speed of computation

### The source function (TMS) technique

Computing radiances by spherical harmonics alone converges slowly because high orders are needed to represent singly scattered radiation. The **TMS method** [^cite-NT88] separates single and multiple scattering: the full (unrescaled) phase function is used for single scattering, while the rescaled truncated phase function handles multiple scattering.

The diffuse radiance equation under rescaling becomes:

$$\mu \frac{dI}{d\hat{\tau}} = I - \frac{\hat{\omega}}{4\pi} \int_\Omega \hat{I}_T \hat{P}\, d\omega'_n - \frac{\hat{\omega}}{4\pi(1-f)} \int_\Omega I_\odot P\, d\omega'_n$$

The algorithm proceeds as follows:

1. Solve the rescaled, truncated equation using spherical harmonics to obtain $\hat{I}_T$ and $\hat{I}_\odot$.
2. Integrate along a ray using $\hat{I}_T$ as the source function for multiply scattered radiation.
3. Compute the unrescaled single-scattering contribution from the true solar beam $I_\odot$ separately.

The final integration along a ray between optical depths $\hat{\Delta}^-$ and $\hat{\Delta}^+$ gives:

$$I(n, \hat{\Delta}^+) = I(n, \hat{\Delta}^-) e^{(\hat{\Delta}^+/\mu - \hat{\Delta}^-/\mu)} + \sum_{i \in \mathcal{I}} \sum_{(l,m) \in T} \hat{\omega}_i \hat{g}_{li} Y_l^m(n) A_{ilm} + \sum_{i \in \mathcal{I}} \sum_{l \in F_L} \frac{2l+1}{4\pi} \hat{\omega}_i \hat{g}_{li} P_l(n_\odot \cdot n) B_i$$

where $A_{ilm}$ and $B_i$ are layer contributions evaluated by integrating exponential terms analytically.

### Ill-conditioning near eigenvalue crossings

When $\mu \to \tilde{\mu}$ (an eigenvalue or $\mu_0$), geometric factors of the form $\tilde{\mu}/(\tilde{\mu} - \mu)$ become ill-conditioned. This is regularised using a perturbation $\eta$:

$$\eta = \frac{\varepsilon}{(\tilde{\mu} - \mu) + \text{sgn}(\tilde{\mu} - \mu)\sqrt{\varepsilon}}$$

where $\varepsilon$ is machine epsilon, so that:

$$G \approx \tilde{\mu} \left(1 - \frac{\eta\hat{\tau}}{\mu\tilde{\mu}}\right) \frac{e^{-s_n + \hat{\tau}/\tilde{\mu}} - e^{-s_f}}{\tilde{\mu} - \mu + \eta}$$

This introduces errors of $O(\sqrt{\varepsilon})$ only in a neighbourhood of the singularity.

---

## Fast solution of the linear equations

A more efficient algorithm for the core linear system — not yet fully implemented — reduces the dominant operation count from $O(18N^3 L)$ (banded solver with partial pivoting) to $O(6N^3 L)$.

### Block structure

For fixed azimuthal order $m$, retaining $2N$ polar orders, the amplitudes at the top and bottom of each layer are assembled into a block matrix system. Collecting alternate (even/odd) eigenvector components as $W_{sk}$ and $U_{sk}$ respectively, the orthogonality relations give:

$$\sum_s \rho_s W_{sk} W_{sk'} = \delta_{kk'}, \qquad \sum_s \sigma_s U_{sk} U_{sk'} = \delta_{kk'}$$

Marshak's condition at the top boundary becomes a block equation involving the matrix $M_{sp} = \tilde{M}_{2s+1-m,\, 2p-m}$.

### Forward recurrence

After block Gaussian elimination, the system reduces to a recurrence of the form:

$$Z_n = C_n - D_n X_{n-1}$$

$$Y_n = (Z_n^{-1} - A_n)^{-1}$$

$$X_n = -Y_n B_n$$

where the matrices $A_n$, $B_n$, $C_n$, $D_n$ are related to the eigenvector blocks and layer transmission factors $\theta_k = e^{-\bar{\tau}/\mu_k}$.

Key simplifications arise from the relations $R = P^{-1}$, $S = Q^{-1}$, and:

$$P = \text{diag}(\mu_{11}^{-1}, \ldots, \mu_{N1}^{-1})\, S^T\, \text{diag}(\mu_{12}, \ldots, \mu_{N2})$$

which reduce the cost of computing $P$ and $R$ from $O(4N^3)$ to $O(4N^2)$ multiplications.

### Back substitution

After forward elimination, back substitution proceeds as:

$$u^+_n = x_n - A_n u^-_{n+1} - B_n u^+_{n+1}$$

$$u^-_n = z_n - X_n x_n$$

Only matrices $A$, $B$, $X$ need be retained at each level, reducing memory by a factor of three relative to the banded solver.

---

[^cite-Marshak]: R. E. Marshak, *Note on the spherical harmonic method as applied to the Milne problem for a sphere*, Phys. Rev., 71:443–446, 1947.
[^cite-Mobley94]: C. D. Mobley, *Light and Water*, Academic Press, first edition, 1994.
[^cite-Petzold72]: T. J. Petzold, *Volume scattering functions for selected ocean waters*, Technical Report SIO Ref. 72-78, Scripps Institution of Oceanography, La Jolla, 1972.
[^cite-Morel91]: A. Morel, *Light and marine photosynthesis: a spectral model with geochemical and climatological implications*, Prog. Oceanogr., 26:263, 1991.
[^cite-PS81]: L. Prieur and S. Sathyendranath, *An optical classification of coastal and oceanic waters based on the specific spectral absorption curves of phytoplankton pigments, dissolved organic matter, and other particulate materials*, Limnol. Oceanogr., 26(4):671–689, 1981.
[^cite-NT88]: T. Nakajima and M. Tanaka, *Algorithms for radiative intensity calculations in moderately thick atmospheres using a truncation approximation*, J. Quant. Spectrosc. Radiat. Transfer, 40:51–69, 1988.
[^cite-Roujean92]: J.-L. Roujean, M. Leroy, and P.-Y. Deschamps, *A bidirectional reflectance model of the Earth's surface for the correction of remote sensing data*, J. Geophys. Res., 97:20455–20468, 1992.
[^cite-Benassi84]: M. Benassi, R. D. M. Garcia, A. H. Karp, and C. E. Siewert, *A high-order spherical harmonics solution to the standard problem in radiative transfer*, Astrophys. J., 280:853–864, 1984.
