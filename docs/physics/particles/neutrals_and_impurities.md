---
title: "Neutrals and Impurities"
nav_order: 7
parent: "Kinetic Particle Module"
layout: default
render_with_liquid: false
---

## Kinetic Neutrals and Impurities 
For a tutorial on how to run with kinetic neutrals and impurities please refer to: [ run with kinetic neutrals and impurities](../../howto/ncs_ics_tutorial.md).

### Atomic physics
Currently the following atomic physics processes are modeled, usually using coefficients from OpenADAS ([[adas|Brief overview]]):

**Neutrals:**
  * *Line radiation*: energy sink for background plasma.
  * *Ionization*: kinetic neutral -> background fluid ion.
  * *Recombination*: background fluid ion -> kinetic neutral.
  * *Charge-exchange*: modeled here as elastic collision between a background fluid- and kinetic ion, changes particle velocity and contributes to parallel momentum coupling term.
  * [[particles:neutral_neutral_collisions|Neutral neutral collisions]]
**Impurities:**
  * *Radiation*: including line radiation, Bremsstrahlung and contribution from recombination.
  * *Ionization*: increases charge state by one.
  * *Recombination*: decreases charge state by one.
  * *Collisions*: currently binary collisions with the background plasma ions, resulting in neoclassical effects.

For more details please refer to *S. Q. Korving et al. PoP 2023* and *PoP 2024*, take a look at kinetic_main.f90 and mod_particle_evolution.f90,  or contact [Máté](mate.szuecs@ipp.mpg.de) or [Daniel](D.Maris@differ.nl|Daniel).


### Coupling scheme

The derivation and implementation of the (kinetic) neutral model for JOREK is described in [*S. Q. Korving et al. PoP 2023*](https://doi.org/10.1063/5.0135318).

For the neutral (ncs) and impurity (ics) coupling scheme, sources and sinks for particles are projected for the density, momentum, and energy equations. However, as the JOREK form of the equations is different than the typical Euler form of the equations, the source terms need to be corrected. The sources are corrected as follows:

$`\left( \frac{\partial \rho}{\partial t}\right) = S_\rho`$

$` \rho \left( \frac{\partial v}{\partial t}\right) = \vec{S}_v = \vec{S}_{\rho v}-\vec{v}S_\rho`$

$`\left( \frac{\partial \rho T}{\partial t}\right) = S_T = (\gamma -1)\left( S_E - \vec{v}\cdot \vec{S}_{\rho v} + \frac{1}{2} v^2 S_\rho \right) `$,

Where $`S_E`$, $`\vec{S}_{\rho v}`$ and $`S_\rho`$ are the physical source terms.

### Overview of source terms

| Reaction | $`S_\rho`$   | $`\vec{S}_{\rho v}`$  | $`\vec{S}_{v}`$ | $`S_{E,i}`$ | $`S_{Ti}`$ | $`S_{E,e}`$ | $`S_{Te}`$ |
| - | - | - | - | - | - | - | - |
| *n* Ion| $`m_i \Gamma_{ion}`$ | $`m_i \Gamma_{ion} \vec{v}_n`$ | $`m_i \Gamma_{ion} (\vec{v}_n - \vec{v}_n)`$ | $`\Gamma_{ion} ( \frac{m_i}{m_n}\frac{T_n}{\gamma-1} + \frac{1}{2} m_i v_n^2)`$ | $`\Gamma_{ion} ( T_n + \frac{1}{2} m_i (\vec{v}_n-\vec{v}_i)^2)`$ | $`-\Gamma_{ion} \|E_{Bind}\|`$ | $`-\Gamma_{ion} \|E_{Bind}\|`$ |
| *n* rec | $`-m_i \Gamma_{rec}`$ | $`-m_i \Gamma_{rec} \vec{v}_i`$ | - | $`-\Gamma_{rec}( \frac{T_i}{\gamma-1}+\frac{1}{2} m_i v_i^2 )`$| $`-\Gamma_{rec} T_i`$ | $`-\Gamma_{rec} \frac{T_e}{\gamma-1}`$ | $`-(L_{PRB}-S_{rec}\|E_{bind}\|)n_e n_i`$ |
| *n* CX | - | $`w_p (v_n^{old} - (N_{rng} \sqrt{\frac{T_i}{m_i}}+v_{drift}))`$ | idem | $`\frac{1}{2} w_p ((v_n^{old})^2-(v_n^{new})^2)`$ | $`S_E^{CX} - v \cdot S_v^{CX}`$ | | |
| *Imp* ion/rec | - | - | - | - | - | $`-w_p \|E_{bind}\|`$ |  $`-(\gamma-1)w_p \|E_{bind}\|`$ |
| *Imp* rad | - | - | - | - | - | $`-n_e w_p (PLT + PRB -S_{rec}\|E_{bind}\|)\delta t`$ | $`-(\gamma-1)n_e w_p (PLT + PRB -S_{rec}\|E_{bind}\|)\delta t`$ |
| *Imp* coll | - | $`w_p m_{imp}(v_{old}-v_{new})`$| idem | $`\frac{1}{2} w_p m_{imp}(v_{old}^2-v_{new}^2)`$ | $`(\gamma - 1)\frac{1}{2} w_p m_{imp}(v_{old}^2-v_{new}^2)`$ | | |

Note 1, the terms including ($`T + \frac{1}{2} m_i (\vec{v}_a-\vec{v}_b)^2`$) is a fluid picture, where the macroscopic drift velocity can be slpit from the random microscopic velocity resulting in the temperature. For the particle picture, it is just the kinetic energy.

Note 2, there is a difference between a radiation rate, and cooling rate. The energy sink for the plasma is the cooling rate. Not all radiation is couling the plasma, e.g. the dielectric cascade in i-e recombination