The following table contains information about spectral files that can be downloaded through Zenodo (https://zenodo.org/communities/proteus_framework/records?q=&f=subject%3Aspectral_files&l=list&p=1&s=10&sort=newest).

| Codename   | Bands | Absorbers              | Continua                 | UV      | Tolerance | Sources | NaN-clean | SOCRATES | Date       | Platform    | Creator          | Notes                |
|------------|-------|------------------------|--------------------------|---------|-----------|---------|-----------|----------|------------|-------------|------------------|---------------------|
| Legacy     |  318  | H2O, CO2, O3, N2O, CO, CH4, O2, NO, SO2, NO2, NH3, HNO3, N2, H2, He, OCS | CO2, CH4, O2, N2, H2, He |No      | 1.00E-02  | HITRAN  | TRUE      | 2002     | 2021       | Linux Intel | Tim Lichtenberg   | Legacy spectral file used in Lichtenberg+2021 |
| Oak        |  318  | H2O                    | H2O                      | No      | 1.00E-02  | HITRAN  | TRUE      | 2306     | 2023-07-10 | Linux Intel | Harrison Nicholls | Water-only spectral file from HITRAN. To be used for benchmarking. |
| Idwal      |  318  | H2O                    | H2O                      | No      | 1.00E-02  | HITRAN  | FALSE     | 2211     | 2023-07-11 | Linux Intel | Harrison Nicholls | Made redundant by Oak. They only differ by SOCRATES version. |
| Balmora    |  318  | H2O                    | H2O                      | No      | 1.00E-02  | HITRAN  | FALSE     | 2306     | 2023-07-19 | Mac ARM     | Tim Lichtenberg   | Made redundant by Oak. They only differ by creation platform. |
| Triangle   |  318  | H2O, H2, CO2           | H2O, H2, CO2             | No      | 1.00E-02  | HITRAN  | TRUE      | 2306     | 2023-07-11 | Linux Intel | Harrison Nicholls | Test |
| Mallard    |  318  | H2O, H2, CO2, CO, CH4, O2, N2, He | H2O, CO2, CH4, O2, N2, H2, He | No      | 1.00E-02  | HITRAN  | TRUE      | 2306     | 2023-07-13 | Linux Intel | Harrison Nicholls | HITRAN file with useful opacities |
| Reach      |  318  | H2O, CO2, O3, N2O, CO, CH4, O2, NO, SO2, NO2, NH3, HNO3, N2, H2, He, OCS | H2O, CO2, CH4, O2, N2, H2, He | No      | 1.00E-02  | HITRAN  | TRUE      |  2306     | 2023-07-19 | Linux Intel | Harrison Nicholls | Same as above but with more opacities |
| Vivec      |  318  | H2O, CO2, O3, N2O, CO, CH4, O2, NO, SO2, NO2, NH3, HNO3, N2, H2, He, OCS | H2O, CO2, CH4, O2, N2, H2, He | No      | 1.00E-02  | HITRAN  | FALSE     | 2306     | 2023-07-25 | Mac Intel   | Tim Lichtenberg   | Same as above, but compiled on MacOS |
| Alduin     |  318  | H2O                    | H2O                      | No      | 1.00E-02  | EXOMOL  | TRUE      | 2306     |            | Linux Intel | Ryan Boukrouche   | Script exists to generate this file, but it is not currently available |
| Kynesgrove |  318  | O2                     | O2-O2                    | No      | 5.00E-04  | DACE    | TRUE      | 2403     | 2024-03-14 | Linux Intel | Harrison Nicholls | Created for validation of DACE xsec data against SOCRATES' own LbL calculations used in Mallard. |
| Frostflow  |  4096 | H2O                    | H2O                      | No      | 5.00E-03  | DACE    | TRUE      | 2403     | 2024-03-20 | Linux Intel | Harrison Nicholls | Very high resolution. Intended for benchmarking. |
| Frostflow  |  256  | ^                      | ^                        | ^       | ^         | ^       | ^         | ^        | ^          | ^           | ^                 | High resolution. |
| Frostflow  |  48   | ^                      | ^                        | ^       | ^         | ^       | ^         | ^        | ^          | ^           | ^                 | Medium resolution. |
| Frostflow  |  16   | ^                      | ^                        | ^       | ^         | ^       | ^         | ^        | ^          | ^           | ^                 | Low resolution. Intended for debugging. |
| Dayspring  |  4096 | H2O, H2, CO2, CO, CH4, N2 | H2O-H2O, H2-CH4, H2-H2, N2-H2, N2-N2, N2-H2O, CO2-CO2, CO2-H2, CO2-CH4 | No      | 1.00E-02  | DACE    |  TRUE      | 2403     | 2024-04-30 | Linux Intel | Harrison Nicholls | Very high resolution. Intended for benchmarking. |
| Dayspring  |  256  | ^                      | ^                        | ^       | ^         | ^       | ^         | ^        | ^          | ^           | ^                 | High resolution. |
| Dayspring  |  48   | ^                      | ^                        | ^       | ^         | ^       | ^         | ^        | ^          | ^           | ^                 | Medium resolution. |
| Dayspring  |  16   | ^                      | ^                        | ^       | ^         | ^       | ^         | ^        | ^          | ^           | ^                 | Low resolution. Intended for debugging. |
| Honeyside  |  4096 | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S | H2O-H2O, H2-CH4, H2-H2, H2-N2, N2-N2, N2-H2O, CO2-CO2, CO2-H2, CO2-CH4 | No      | 1.00E-02  | DACE    | TRUE      | 2403     | 2024-07-07 | Linux Intel | Harrison Nicholls | Very high resolution. Intended for benchmarking. |
| Honeyside  |  256  | ^                      | ^                        | ^       | ^         | ^       | ^         | ^        | ^          | ^           | ^                 | High resolution. |
| Honeyside  |  48   | ^                      | ^                        | ^       | ^         | ^       | ^         | ^        | ^          | ^           | ^                 | Medium resolution. |
| Honeyside  |  16   | ^                      | ^                        | ^       | ^         | ^       | ^         | ^        | ^          | ^           | ^                 | Low resolution. Intended for debugging. |
| Rocks      |  256  | O2, SiO, SiO2          | O2-O2                    | No      | ?         | DACE    | TRUE      | 2407.2   | 2025-05-15 | Linux Intel | Alex McGinty      | High resolution file used for comparison with JWST observations of rock-vapour atmospheres. |
| Rocks      |  128  | H2, H2O, O2, SiO, SiO2 | H2O-H2O, H2-H2, O2-O2    | ^       | ?         | ^       | ^         | ^        | ^          | ^           | Alex McGinty      | Rock vapours and key volatiles. |
| Rocks      |  64   | H2, H2O, O2, SiO, SiO2 | H2O-H2O, H2-H2, O2-O2    | ^       | ?         | ^       | ^         | ^        | ^          | ^           | Alex McGinty      | Rock vapours and key volatiles (low resolution). |
| Winterfell | 4096  | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S, O2 | H2O-H2O, H2-CH4, H2-H2, H2-N2, N2-N2, N2-H2O, CO2-CO2, CO2-H2, CO2-CH4 | CO2, H2O, H2S, N2, N2O, NH3, O3, SO2 | ?|DACE, MPI| TRUE      | 2407.2   | 2026-01-12 | Linux Intel | Bruna Fena        | Honeyside but with UV included for some molecules. Very high-resolution. |
| Winterfell | 256   | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S, O2 | ^       | ^       | ?|^        | ^         | ^        | ^          | ^           | ^                 | High resolution.   |
| Winterfell | 48    | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S, O2 | ^       | ^       | ?|^        | ^         | ^        | ^          | ^           | ^                 | Medium resolution. |
| Winterfell | 16    | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S, O2 | ^       | ^       | ?|^        | ^         | ^        | ^          | ^           | ^                 | Low-resolution.    |
| Dragonstone| 4096  | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S     | H2O-H2O, H2-CH4, H2-H2, H2-N2, N2-N2, N2-H2O, CO2-CO2, CO2-H2, CO2-CH4 | CO2, H2O, H2S, N2, N2O, NH3, O3, SO2 | ?|DACE, MPI| TRUE      | 2407.2   | 2026-01-12 | Linux Intel | Bruna Fena        | Same as Lighthouse but no O2 included. Very high-resolution. |
| Dragonstone  | 256   | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S     | ^       | ^       | ?|^        | ^         | ^        | ^          | ^           | ^                 | High resolution.   |
| Dragonstone  | 48    | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S     | ^       | ^       | ?|^        | ^         | ^        | ^          | ^           | ^                 | Medium resolution. |
| Dragonstone  | 16    | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S     | ^       | ^       | ?|^        | ^         | ^        | ^          | ^           | ^                 | Low-resolution.    |
| Sunspear   | 4096  | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S, O2 | H2O-H2O, H2-CH4, H2-H2, H2-N2, N2-N2, N2-H2O, CO2-CO2, CO2-H2, CO2-CH4 | CO2, SO2, H2S | ?|DACE, MPI| TRUE      | 2407.2   | 2026-01-12 | Linux Intel | Bruna Fena        | To simulate Ranjan and Sasselov (2016), only CO2, SO2 and H2S have UV values. Very high-resolution. |
| Sunspear   | 256   | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S, O2 | ^       | ^       | ?|^        | ^         | ^        | ^          | ^           | ^                 | High resolution.   |
| Sunspear   | 48    | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S, O2 | ^       | ^       | ?|^        | ^         | ^        | ^          | ^           | ^                 | Medium resolution. |
| Sunspear   | 16    | H2O, H2, CO2, CO, CH4, N2, NH3, SO2, N2O, O3, HCN, H2S, O2 | ^       | ^       | ?|^        | ^         | ^        | ^          | ^           | ^                 | Low-resolution.    |


The files for the UV were taken from the MPI-Mainz UV/VIS Spectral Atlas:
CO2: Archer et al. (2013); Cook et al. (1966); Kuo et al. (2004); Gallagher et al. (1988); Shaw et al. (1995); Shemansky (1972); Venot, O. et al. (2018).
H2O: Gürtler et al. (1977); J.B. Burkholder; S.P. Sander; J. Abbatt; J.R. Barker; R.E. Huie; C.E. Kolb; M.J. Kurylo; V.L. Orkin and Wine (2015); Ranjan et al. (2020).
H2S: Feng et al. (1999); Grosch et al. (2015); Wu and Chen (1998).
N2: Souza and Srivastava (1994).
N2O: Johnston and Graham (1974).
NH3: Burton et al. (1993); Limão-Vieira et al. (2019).
O3: Mason et al. (1996); Molina and Molina (1986); Serdyuchenko et al. (2014).
SO2: Golomb et al. (1962); Olive (2015).
