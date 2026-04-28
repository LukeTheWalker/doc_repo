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
...