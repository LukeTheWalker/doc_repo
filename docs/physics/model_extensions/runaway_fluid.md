---
title: "REs — Fluid Model"
nav_order: 1
parent: "Runaway Electrons"
grand_parent: "Model Extensions"
layout: default
render_with_liquid: false
---


# RE fluid model
## Brief overview
The RE fluid model considers REs as a fluid species that is separate from the main ions, impurities, neutrals, and electrons. A few points to note:

- Implemented only within model-600.
- At the moment, implemented to work only with the single temperature model and coronal equilibrium for impurities.
- Only the RE number density is tracked/evolved. RE momentum and pitch angle are not evolved (this can only be done in the [kinetic version](../kinetic_models/runaway_electrons/runaway_electrons.md)).
- Physical RE sources implemented:
  - Compton scattering
  - Tritium decay
  - Avalanche (secondary)
- Effect of partially-ionized impurities are taken into account while computing the RE sources. See more information in the reference list below.
- It is also possible to choose artificial RE seeds such as a Gaussian seed, scaled-down J profile, etc., via the input file.
- RE parallel advection and diffusion are not mutually exclusive. Both can co-exist, which is advantageous in certain instances for numerical stability.

## Compiling

To include RE fluid in a simulation, you should simply set the flag as follows before compiling:

```bash
./util/config.sh with_refluid=.true.
```

## Input parameters

The following are the input parameters relevant to the RE fluid model:

| Variable                  | Meaning                                           | Options or comments                                                                 |
|---------------------------|---------------------------------------------------|------------------------------------------------------------------------------------|
| `re_initialize`           | Option to initialize artificial RE seed           | 1: Spatially Gaussian RE seed; 2: RE seed is a scaled-down J-profile; any other value implies no artificial RE seed |
| `initial_re_current_fraction` | `J_re_seed = f * J (at t=0)`                   | Real value between 0 to 1. Used only when `re_initialize=2`.                       |
| `re_gauss_fact`           | Scaling factor for Gauss-seed                     | Real value. Used only when `re_initialize=1`.                                      |
| `re_gauss_origin`         | Origin for Gauss-seed in units of `Psi_norm`      | Real value between 0 to 1. Used only when `re_initialize=1`.                       |
| `re_gauss_width`          | Width of Gauss seed in units of `Psi_norm`        | Real value. Used only when `re_initialize=1`.                                      |
| `re_trit_seed`            | Tritium seed                                      | `.t.` or `.f.`                                                                     |
| `re_compt_seed`           | Compton seed                                      | `.t.` or `.f.`                                                                     |
| `re_sec_source`           | Avalanche source                                  | `.t.` or `.f.`                                                                     |
| `psinorm_aval_threshold`  | Upper bound of `psi_norm` beyond which RE avalanche is set to zero | For numerical convenience in certain rare instances. Real value.                  |
| `vpar_re_sign`            | Direction of RE parallel motion                   | `+1` for counter-clockwise `Ip` or `-1` for clockwise `Ip` (e.g., `+1` for AUG, DTT, etc., and `-1` for JET, ITER, etc.). |
| `re_adv_fact`             | Fraction of speed-of-light used for RE parallel advection | Real value less than or equal to 1.                                               |
| `Dre_par`                 | RE parallel diffusivity                           | Real value.                                                                        |
| `Dre_iso`                 | RE isotropic (a.k.a. 'perpendicular') diffusivity | Real value.                                                                        |
| `Dre_num`                 | RE hyperdiffusivity                               | Real value.                                                                        |
| `gamma_rel`               | Relativistic gamma assuming monoenergetic REs     | Real value. Required even if not used immediately.                                 |

## References

More details and model description can be found from the following:
| | | 
|---|---|
| Initial Publication of RE fluid model and GO benchmark. See Appendix for normalization | Bandaru, V., Hoelzl, M., Artola, F.J., Papp, G., Huijsmans, G.T.A., 2019. Physical Review E 99, 63317. [10.1103/PhysRevE.99.063317](https://doi.org/10.1103/PhysRevE.99.063317)
|Further improvements in the model including partial screenting|V. Bandaru, M. Hoelzl, F. J. Artola, O. Vallhagen, M. Lehnen, JOREK Team; Runaway electron fluid model extension in JOREK and ITER relevant benchmarks. Phys. Plasmas 1 August 2024; 31 (8): 082503. [10.1063/5.0213962](https://doi.org/10.1063/5.0213962)|

## Tutorial

- See the [Tutorial](../../howto/refluid-tutorial.md) for a first simulation of RE generation.
