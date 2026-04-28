---
title: "Particle types"
nav_order: 7
parent: "Kinetic Particle Module"
layout: default
render_with_liquid: false
---

# Particle types (see `particles/mod_particle_types.f90`)

The table below shows the different particle types and their variables. All particles have the variables corresponding to particle base with additional variable based on their type. 

| type      | variables      | units          | comment |
| --------- | -------------- | -------------- | ------- |
| particle base   | x(3)    | [m,m,rad]       | particle position in  (R,Z, phi) space |
|                 | st(2)   | [real*8]        | local finite element coordinates |
|                 | weight  | [real*4]        | weight of particle , total number of "real" particles = sum(weights)|
|                 | i_elm   | [integer]       | element number containing this particle|
|                 | i_life  | [integer]       | measures how often the particle has been reused"|
|                 | t_birth | [s]             | measures the birth time of the particle|
| _kinetic        | v(3)    | [m/s]           | velocity in S.I. units, in directions (R,Z,phi)|
|                 | q       | [e]       | charge |
| _kinetic_leapfrog| v(3)    | [m/s]     | velocity at **t = t(n-1/2)** , in directions (R,Z,phi)|
|                 | q       | [e]       | charge|
| _kinetic_relativistic| p(3) |[AMU m/s]| momentum **[X,Y,Z]**|
|                 | q       | [e] | charge|
|                 | q       | [e]       | charge|
| _gc             | E       | [eV]      | kinetic energy|
|                 | mu      | [eV]      | magnetic moment (sign determines direction of the parallel velocity)|
|                 | q       | [e]       | charge |
| _gc_relativistic| p(2) |[AMU m/s, AMU m<sup>2</sup>/(T*s<sup>2</sup>)]| 1: parallel momentum, 2: magnetic moment|
|                 | q | [e]| charge |

**Particle type conversion:**

(see `particles/pushers/mod_boris.f90` and `particles/pushers/mod_kinetic_relativistic.f90`)

  * `kinetic_leapfrog_to_gc(node_list, element_list, particle_in, E, B, mass, dt)`
  * `gc_to_kinetic_leapfrog(particle_in, node_list, element_list, chi, E, B, mass, dt)`
  * `kinetic_to_kinetic_leapfrog(particle_in, E, B, mass, dt)`
  * `kinetic_leapfrog_to_kinetic(particle_in, E, B, mass, dt)`
  * `kinetic_to_gc(node_list, element_list, particle_in, B, mass)` 
  * `gc_to_kinetic(node_list, element_list, particle_in, chi, B, mass)`
  * `relativistic_kinetic_to_particle(node_list,element_list,particle_in, particle_out,mass,B)`
  * `relativistic_kinetic_to_relativistic_gc(node_list,element_list, particle_in,mass,B)`
  * `relativistic_kinetic_to_gc(node_list,element_list,particle_in,mass,B)` 
  * `gc_to_relativistic_kinetic(node_list,element_list,particle_in,time,mass,chi,B)`
  
