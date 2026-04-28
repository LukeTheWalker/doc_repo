---
title: "Neutrals and Impurities"
nav_order: 7
parent: "Kinetic Particle Module"
layout: default
render_with_liquid: false
---

# Kinetic Neutrals and Impurities
The kinetic neutral and/or impurity extension of JOREK can be used to simulate the plasma Scrape-Off Layer (SOL) in a higher fidelity manner than the base MHD model or fluid neutral and impurity models.

* [Coupling Scheme](../neutrals_and_impurities/ncs_ics_coupling_scheme.md)
* [Implemented Atomic Processes](../neutrals_and_impurities/ncs_ics_atomic_processes.md)
  * [Neutral-Neutral Collisions](../neutrals_and_impurities/neutral_neutral_collisions.md)
  * [Impurity Collisions](../neutrals_and_impurities/impurity_collisions.md)
* [Plasma-Wall Interactions](../neutrals_and_impurities/particle_wall_interactions.md)
* [Gas Puffing](../neutrals_and_impurities/gas_puffing.md)
* [Tutorial](../neutrals_and_impurities/tutorial.md)

For more details please take a look at kinetic_main.f90 and mod_particle_evolution.f90,  or contact [Máté](mate.szuecs@ipp.mpg.de) or [Daniel](D.Maris@differ.nl|Daniel).

## Publications and References
* Liang, Y. C., et al. "JOREK simulations of the X-point radiator formation and its movement in ASDEX Upgrade." arXiv preprint arXiv:2602.08614 (2026).
* Szücs, M. (2024). Modeling detachment and burn-through in small edge localized mode regimes using the nonlinear magnetohydrodynamic code JOREK. Master Thesis, Technische Universität München, München.
* Maris, D. "Time-dependent Scrape-Off Layer simulations with JOREK for detachment control." (2024). MSc Thesis, Eindhoven University of Technology.
* Korving, S. Q. (2024). MHD Simulations of Neutral and Impurity Transport in ELM-controlled Plasmas: with application to ITER. [Phd Thesis 1 (Research TU/e / Graduation TU/e), Applied Physics and Science Education]. Eindhoven University of Technology.
* Korving, S. Q., et al. "Simulation of neoclassical heavy impurity transport in ASDEX Upgrade with applied 3D magnetic fields using the nonlinear MHD code JOREK." Physics of Plasmas 31.5 (2024).
* Korving, S. Q., et al. "Development of the neutral model in the nonlinear MHD code JOREK: Application to E× B drifts in ITER PFPO-1 plasmas." Physics of Plasmas 30.4 (2023).
* Van Vugt, D. C., et al. "Kinetic modeling of ELM-induced tungsten transport in a tokamak plasma." Physics of Plasmas 26.4 (2019).
* van Vugt, D. C. (2019). Nonlinear coupled MHD-kinetic particle simulations of heavy impurities in tokamak plasmas. [Phd Thesis 1 (Research TU/e / Graduation TU/e), Applied Physics and Science Education]. Technische Universiteit Eindhoven.