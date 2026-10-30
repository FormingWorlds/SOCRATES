# Validation of spectral files

This page tests the Generation III [PROTEUS spectral files](proteus_spectral_file_reference.md) in three ways: whether they reproduce the radiation limit of a runaway greenhouse atmosphere, how much the outgoing longwave radiation (OLR) changes with the number of bands, and how they compare with a line-by-line calculation. It covers Snowline, Breezehome and Volenfell.

The calculations were made with [AGNI](https://www.h-nicholls.space/AGNI/) version 1.14.0, which calls SOCRATES for the radiative transfer. They use the two-stream solver with equivalent extinction for overlapping gases, include continuum absorption, and leave out Rayleigh scattering, clouds and stellar radiation. The temperature profiles are prescribed rather than solved for, as described in each section. The scripts that make these calculations and figures are in [`misc/validation/spectral_files`](https://github.com/nichollsh/AGNI/tree/main/misc/validation/spectral_files) in the AGNI repository.

---

## Runaway greenhouse

A pure-steam atmosphere above a water ocean has an upper limit on its OLR ([Komabayasi 1967](https://doi.org/10.2151/jmsj1965.45.1_137); [Ingersoll 1969](https://doi.org/10.1175/1520-0469%281969%29026%3C1191:TRGAHO%3E2.0.CO;2)). As the surface warms, the atmosphere becomes optically thick, and its emission comes from the upper part of the atmosphere, where the temperature follows the saturation curve of H<sub>2</sub>O. The OLR then stays almost constant as the surface warms further: this is the radiation limit of the runaway greenhouse ([Kasting 1988](https://doi.org/10.1016/0019-1035%2888%2990116-9); [Nakajima et al. 1992](https://doi.org/10.1175/1520-0469%281992%29049%3C2256:ASOTGE%3E2.0.CO;2)). Once the surface is hot enough (above about 1700 K in these calculations), the hot lower atmosphere emits at shorter wavelengths, where H<sub>2</sub>O absorbs less, and the OLR rises again (e.g. [Goldblatt et al. 2013](https://doi.org/10.1038/ngeo1892); [Hamano et al. 2015](https://doi.org/10.1088/0004-637X/806/2/216)).

**Set-up.** The atmosphere is pure H<sub>2</sub>O with an inventory of 270 bar. Below the critical temperature, the surface pressure is the saturation vapour pressure if that is smaller than 270 bar, with the rest of the water taken to be in the ocean. The temperature follows a dry adiabat from the surface, replaced by the saturation curve wherever the adiabat would be supersaturated, up to 10<sup>−5</sup> bar on 100 levels. The gas is ideal with constant heat capacity, and the gravity is 9.81 m s<sup>−2</sup>. The surface temperature runs from 200 K to 2500 K in steps of 25 K. The set-up follows the [canonical runaway notebook](https://github.com/nichollsh/AGNI/blob/main/docs/notebooks/01_canonical-runaway.ipynb) in AGNI.

<figure markdown="span">
  ![OLR of a pure-steam atmosphere against surface temperature, for Snowline at five band counts and four published models](../assets/validation/runaway_light.png#only-light)
  ![OLR of a pure-steam atmosphere against surface temperature, for Snowline at five band counts and four published models](../assets/validation/runaway_dark.png#only-dark)
  <figcaption>OLR of a pure-steam atmosphere against surface temperature. Left: the runaway limit, on a linear scale. Right: the full range, on a logarithmic scale. The published curves were digitised from figures in those papers (see below).</figcaption>
</figure>

OLR in W m<sup>−2</sup> at selected surface temperatures:

| Source | 400 K | 1000 K | 1500 K | 2000 K | 2200 K |
|--------|-------|--------|--------|--------|--------|
| Snowline, 32 bands | 294 | 292 | 292 | 419 | 891 |
| Snowline, 64 bands | 295 | 293 | 293 | 342 | 558 |
| Snowline, 128 bands | 295 | 293 | 293 | 406 | 822 |
| Snowline, 256 bands | 295 | 294 | 294 | 448 | 990 |
| Snowline, 2048 bands | 295 | 294 | 294 | 500 | 1190 |
| [Goldblatt et al. (2013)](https://doi.org/10.1038/ngeo1892) | 283 | 281 | 280 | | |
| [Kopparapu et al. (2013)](https://doi.org/10.1088/0004-637X/765/2/131) | 290 | 294 | 294 | 306 | |
| [Hamano et al. (2015)](https://doi.org/10.1088/0004-637X/806/2/216) | | | 279 | 303 | 417 |
| [Selsis et al. (2023)](https://doi.org/10.1038/s41586-023-06258-3) | | 276 | 274 | 336 | 604 |

- Snowline gives a runaway limit of 292–296 W m<sup>−2</sup> for surface temperatures between 300 K and 1500 K, at every band count. Breezehome has the same bands and H<sub>2</sub>O data as Snowline, and gives the same OLR.
- This agrees with Kopparapu et al. (2013) to within 2 %, and is 4–7 % higher than Goldblatt et al. (2013), Hamano et al. (2015) and Selsis et al. (2023). These models differ from each other and from this set-up in their opacity data and assumptions, so exact agreement is not expected.
- Above about 1700 K the OLR depends strongly on the number of bands, and does not change monotonically with it. At 2200 K it ranges from 558 W m<sup>−2</sup> with 64 bands to 1190 W m<sup>−2</sup> with 2048 bands. At this temperature every band count except 64 gives a higher OLR than Hamano et al. (2015) and Selsis et al. (2023).

The Goldblatt et al. (2013), Kopparapu et al. (2013) and Hamano et al. (2015) curves were digitised from Fig. 12a of Hamano et al. (2015), and the Selsis et al. (2023) curve from their Fig. 2 (convective profiles). The data are in [`res/literature_data/runaway`](https://github.com/nichollsh/AGNI/tree/main/res/literature_data/runaway) in the AGNI repository.

---

## Number of bands

Each Generation III family is available with 32, 64, 128, 256 and 2048 bands. Here the OLR from the files with fewer bands is compared with the 2048-band file of the same family, which resolves the spectrum most finely. No line-by-line calculation was made, so this shows how consistent the band counts are with each other, not how accurate the 2048-band files are.

**Set-up.** The temperature follows a dry adiabat from the surface up to an isothermal stratosphere at one third of the surface temperature (one half for Volenfell), up to 10<sup>−5</sup> bar on 40 levels. The composition is fixed and the same at all heights. The compositions are illustrative, not the result of a chemistry calculation:

| Family | Composition (mole fractions) | Surface pressures | Surface temperatures |
|--------|------------------------------|-------------------|----------------------|
| Snowline | H<sub>2</sub>O | 1 and 100 bar | 700, 1500 and 2500 K |
| Breezehome | H<sub>2</sub>O 0.5, CO<sub>2</sub> 0.3, CO 0.05, O<sub>2</sub> 0.05, SO<sub>2</sub> 0.05, OCS 0.03, S<sub>2</sub> 0.02 | 1 and 100 bar | 700, 1500 and 2500 K |
| Volenfell | O<sub>2</sub> 0.30, Na 0.30, SiO 0.20, Fe 0.10, MgO 0.05, K 0.03, CO 0.0195, TiO 0.0005 | 0.1 and 10 bar | 2000, 3000 and 4000 K |

<figure markdown="span">
  ![Difference in OLR from the 2048-band file against the number of bands, for Snowline, Breezehome and Volenfell](../assets/validation/bands_light.png#only-light)
  ![Difference in OLR from the 2048-band file against the number of bands, for Snowline, Breezehome and Volenfell](../assets/validation/bands_dark.png#only-dark)
  <figcaption>Difference in OLR from the 2048-band file of the same family, against the number of bands. Top: the lower surface pressure. Bottom: the higher surface pressure.</figcaption>
</figure>

- At 100 bar with surface temperatures of 700 K and 1500 K, every band count agrees with the 2048-band file to within 0.6 %. These atmospheres are optically thick, and the OLR is set by the isothermal stratosphere.
- In the other cases, the files with fewer bands differ more. With 32 bands, the OLR is 40 % higher for Breezehome at 1 bar and 700 K, and 15 % lower for Volenfell at 0.1 bar and 2000 K.
- With 256 bands, the OLR is within 5 % of the 2048-band file for Snowline, within 6 % for Breezehome and within 8 % for Volenfell, in every case.
- The differences do not always shrink as the number of bands grows. At 100 bar and 2500 K, the 64-band files of Snowline and Breezehome differ more (−13 % and −14 %) than the 32-band files (−5 % and −11 %).

<figure markdown="span">
  ![Outgoing flux against wavelength for Breezehome with 32, 256 and 2048 bands](../assets/validation/spectrum_light.png#only-light)
  ![Outgoing flux against wavelength for Breezehome with 32, 256 and 2048 bands](../assets/validation/spectrum_dark.png#only-dark)
  <figcaption>Outgoing flux in each band for Breezehome with 32, 256 and 2048 bands, for the seven-gas composition at 1 bar and a surface temperature of 1500 K. The OLR is 16.6 % higher with 32 bands and 5.2 % higher with 256 bands than with 2048 bands.</figcaption>
</figure>

---

## Line-by-line comparison

AGNI can also calculate the outgoing flux line by line with the [Reference Forward Model](https://eodg.atm.ox.ac.uk/RFM/) (RFM; [Dudhia 2017](https://doi.org/10.1016/j.jqsrt.2016.06.018)). Here the RFM is run on the same atmosphere as Breezehome, using the HITRAN lines of H<sub>2</sub>O and CO<sub>2</sub> between 4000 and 5000 cm<sup>−1</sup> (2.0–2.5 µm) that AGNI downloads with `get_data.sh parfiles` ([Zenodo record](https://zenodo.org/records/15806626)).

**Set-up.** The atmosphere is 70 % H<sub>2</sub>O and 30 % CO<sub>2</sub> at 1 bar, with a surface temperature of 700 K, and the same type of profile as in [Number of bands](#number-of-bands). Continua are left out of both calculations, so only line absorption is compared. The RFM radiance is calculated every 0.002 cm<sup>−1</sup> at a secant of 1.66 and multiplied by π to give a flux; 1.66 is the diffusivity factor of the two-stream scheme that AGNI uses in the longwave. The RFM needs line data a little beyond each end of the range it calculates, so it covers 4026–4973 cm<sup>−1</sup>, and only the bands that lie within this range are compared. None of the 32-band file's bands do.

The two calculations do not use the same line data: Breezehome uses the ExoMol POKAZATEL (H<sub>2</sub>O) and Dozen (CO<sub>2</sub>) line lists, computed with PyExoCross, while the RFM uses HITRAN with its own line shapes and cut-off. The comparison therefore tests the line data and the k-term fits together.

<figure markdown="span">
  ![Outgoing flux between 4000 and 5000 cm⁻¹ from the RFM and from Breezehome, with the difference in each band](../assets/validation/lbl_light.png#only-light)
  ![Outgoing flux between 4000 and 5000 cm⁻¹ from the RFM and from Breezehome, with the difference in each band](../assets/validation/lbl_dark.png#only-dark)
  <figcaption>Top: outgoing flux from the RFM and from Breezehome with 256 and 2048 bands. Bottom: difference of each Breezehome band from the RFM flux integrated over the same band.</figcaption>
</figure>

- Over the 71 bands of the 2048-band file that lie in this range, Breezehome gives 5.5 % more outgoing flux than the RFM (11.66 against 11.05 W m<sup>−2</sup>). With 256 bands (8 bands in the range) it gives 3.1 % more.
- Between 4300 and 4700 cm<sup>−1</sup>, which carries 89 % of the flux, the 2048-band file agrees with the RFM to within −13 % to +25 % in each band. Larger differences occur at both ends, where the band-mean flux falls to 1/330 (below 4300 cm<sup>−1</sup>) and 1/15 000 (above 4700 cm<sup>−1</sup>) of its peak: up to +160 % between 4026 and 4300 cm<sup>−1</sup>, and down to −87 % above 4700 cm<sup>−1</sup>. These bands carry 8 % and 2 % of the flux.
- The 64- and 128-band files give 38 % and 26 % more flux than the RFM over their bands, in line with the band-count comparison above, where fewer bands give a higher OLR for Breezehome at 1 bar and 700 K.
- The RFM band fluxes change by less than 0.4 % when its step is increased from 0.002 to 0.01 cm<sup>−1</sup>.

---

## References

- Dudhia, A. 2017, Journal of Quantitative Spectroscopy and Radiative Transfer 186, 243, [doi:10.1016/j.jqsrt.2016.06.018](https://doi.org/10.1016/j.jqsrt.2016.06.018).
- Goldblatt, C., Robinson, T. D., Zahnle, K. J. & Crisp, D. 2013, Nature Geoscience 6, 661, [doi:10.1038/ngeo1892](https://doi.org/10.1038/ngeo1892).
- Hamano, K., Kawahara, H., Abe, Y., Onishi, M. & Hashimoto, G. L. 2015, ApJ 806, 216, [doi:10.1088/0004-637X/806/2/216](https://doi.org/10.1088/0004-637X/806/2/216).
- Ingersoll, A. P. 1969, Journal of the Atmospheric Sciences 26, 1191, [doi:10.1175/1520-0469(1969)026<1191:TRGAHO>2.0.CO;2](https://doi.org/10.1175/1520-0469%281969%29026%3C1191:TRGAHO%3E2.0.CO;2).
- Kasting, J. F. 1988, Icarus 74, 472, [doi:10.1016/0019-1035(88)90116-9](https://doi.org/10.1016/0019-1035%2888%2990116-9).
- Komabayasi, M. 1967, Journal of the Meteorological Society of Japan 45, 137, [doi:10.2151/jmsj1965.45.1_137](https://doi.org/10.2151/jmsj1965.45.1_137).
- Kopparapu, R. K., et al. 2013, ApJ 765, 131, [doi:10.1088/0004-637X/765/2/131](https://doi.org/10.1088/0004-637X/765/2/131).
- Nakajima, S., Hayashi, Y.-Y. & Abe, Y. 1992, Journal of the Atmospheric Sciences 49, 2256, [doi:10.1175/1520-0469(1992)049<2256:ASOTGE>2.0.CO;2](https://doi.org/10.1175/1520-0469%281992%29049%3C2256:ASOTGE%3E2.0.CO;2).
- Selsis, F., Leconte, J., Turbet, M., Chaverot, G. & Bolmont, É. 2023, Nature 620, 287, [doi:10.1038/s41586-023-06258-3](https://doi.org/10.1038/s41586-023-06258-3).
