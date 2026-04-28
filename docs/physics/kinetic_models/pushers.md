---
title: "Particle pushers"
nav_order: 7
parent: "Kinetic Particle Module"
layout: default
render_with_liquid: false
---

# Available particle pushers:

- Boris (See G.L. Delzanno, E. Camporeale / JCP 253 (2013) 259-277) :
    - `boris_all_initial_half_step_backwards_RZPhi(particle, mass, fields, time, timestep)`
    - `boris_push_cylindrical(particle, mass, E, B, timestep)`
- Runge Kutta (C. Sommariva et al., Nucl. Fusion 58 (2018) 016043)
    - `runge_kutta_fixed_dt_relativistic_particle_push_jorek(fields,time,timestep,mass,particle)`
    - `runge_kutta_fixed_dt_gc_push_jorek_radreact(fields,t,dt,mass,particle)`
- Volume preserving scheme (see  R. Zhang et al., Phys. Plasmas 22 (2015) 044501, C. Sommariva et al., Nucl. Fusion 58 (2018) 016043)
    - `volume_preserving_push_jorek(particle,fields,mass,time,timestep,ifail)`
    - `volume_preserving_radiation_push_jorek(particle,fields,mass,time,timestep,ifail)`

For more information on the pushers that can be used for runaway electrons and inlcuding the effect of Coulomb collisions into the pushing, please see [Runaway electron physics in the particle tracer](runaway_electrons/runaway_electron_pushers.md). 