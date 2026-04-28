---
title: "Kinetic timestepping"
nav_order: 7
parent: "Kinetic Particle Module"
layout: default
render_with_liquid: false
---

# Kinetic timestepping

In the kinetic application of JOREK, there are multiple numerical timescales. Besides the MHD fluid timestep (tstep or tstep_n in the input namelist, in JOREK normalised units), there is the particle timestep tstep_particles (in seconds). In general, the particle timestep must be chosen based on the physical processes that are being modelled. This means that the particle timestep for kinetic runaway electrons will be far smaller (order 10^-12 s) compared to the particle timestep of kinetic neutral (order 10^-7 s). 

In kinetic main, there is at the moment only a single timestep for all kinetic species, as there haven't been a lot of developments for integrated neutrals/impurities with fast particles/runaway electrons yet.

## Intermediate timescale

However, besides these two fundamental timescales for coupled simulations (fluid and particle timescales), certain simulations benefit from having intermediate timescales. This has been implemented in kinetic_main in the form of an inner particle loop in which actions depending only on the particles can happen more frequently than the fluid timestep. It is coded such that each particle-particle action can take it's own frequency, while all still synchronising to the particle timesteps and to the fluid timesteps. This is done by setting how many (integer) particle timesteps you want the action to happen through the %(...)each_nstep_part like variables in the namelist.
In the backend, the greatest common divisors (gdc's) and least common multiple (lcm) of all of these %(...)each_nstep_part variables are calculated automatically, and from this the inner particle loop in kinetic_main is set up. The particle evolution happens each inner particle loop call, for an amount of steps equal to the global gcd (rather than 1, to save on computational time and output file cluttering). Particle-particle interactions only happens as often as they are required (which is determined from their own stored %each_nstep_particles).
This means backwards compatibility is preserved when the %each_nstep_part variables are not set. However, the reg tests were still broken because the neutral neutral collisions (NNC) now use their own projection, as the jorek_feedback projection comes too late since the NNC were moved into the inner particle loop for if you want to do more than 1 neutral collision per fluid timestep. It was checked that all commits before and after this change passed the reg test, and it was checked that in the limit of small timestep, the neutral density projection for the NNC visually corresponds with the neutral density projection from the aux_nodes list in paraview.
The default value for the gcd, lcm and each_nstep_part variables is -9999991, and it is interpreted as meaning that action should happen only once per fluid timestep. (The reason this default is chosen is that it is the negative of a big prime number, so the gcd and lcm of it with almost any other number will give very strange and thus debuggable answers if it somehow ends up in a place it shouldn't)
The particle actions currently implemented to work with this intermediate timescale are the [wall_actions](./neutrals_and_impurities/particle_wall_interactions.md), [neutral neutral collisions](./neutrals_and_impurities/neutral_neutral_collisions.md) and work is in progress for the runaway electron large angle collisions and runaway electron resampling.
The output file will print some information at before entering the inner particle loop and at the beginning of each step in the inner particle loop.

### An example

Let's see how this works in practice. Suppose you have a deuterium plasma with deuterium neutrals and the following settings:
```fortran90
tstep_n=30
tstep_particles    = 5.d-7
central_density = 0.425558
...
part_group_configs(1)%ncoll_each_nstep_part=10
part_group_configs(1)%wall_act_each_nstep_part=2
```
This gives `sqrt(mu0*rho0)       =   2.0501E-07`, so the fluid timestep in SI units would then be $6.15\cdot10^{-6}$s. Since we want to do the wall actions each 2 particle steps, and the neutral self collisions each 10 particle steps, we need to do a multiple of 10 particle steps each fluid step. The gcd of 2 and 10 is 2, the lcm of 2 and 10 is 10. But we can fit more than 10 particle steps into one fluid timestep, and we don't want to make our effective partice timestep bigger than the given particle timestep in the input, so instead we will make it smaller so that we can accomodate 20 step, i.e. 2 blocks of 10 steps. Now we have our inner particle loop set up, we will take steps of 2 particle steps, and then we do the actions after the requested amount of particle steps. This is all determined by the program automatically, and the results can be seen in the output just before the inner particle loop starts:

```
====================================================================================================
  Starting inner particle loop
====================================================================================================
 sim%time                   :   1.553451140746281E-002
 tstep_fluid_si             :   6.150231147637786E-006
 aim tstep_particles        :   5.000000000000000E-007
 used tstep_part_adj        :   3.075115573818893E-007
 nstep_inner_loop           :           20
 lcm, n_lcm_blocks          :           10           2
 gcd, inner_stepsize        :            2           2
 n_part*dt_part - dt_fluid  :   0.000000000000000E+000
====================================================================================================
  Starting inner particle loop iteration getting us to istep_inner_loop=     2 out of     20          
====================================================================================================
====================================================================================================
  Particle evolution loop
====================================================================================================
 ---------- Evolving particle group: D01 ----------
...
```

### How to choose your %(...)each_nstep_part variables

If the lcm is a lot bigger than tstep_particles/tstep_fluid_si, then you will take very small particle steps without that really being necessary. It will throw a warning for this but you are responsible for using reasonable %(...)each_nstep_part variables. In general this means avoiding (co-)primes, e.g. don't use 15 and 7, because you will end up with an lcm of 105, meaning your tstep_particles will likely be unnecessarily small to fit 105 particle timesteps into one fluid timestep, and gcd of 1, meaning a lot of computation time is wasted on loading/unloading particles and the output file is cluttered. Rather, try to use multiples of eachother, in this case rather than 7 and 15, use 5 and 15, which has gcd=5, lcm=15. Also avoid large %(...)each_nstep_part altogether if tstep_particle/tstep_fluid_si is small. Just leave the %(...)each_nstep_part blank if you only want to do that action once every fluid timestep (it will then be done on the last inner particle loop step, and not be taken into account in the lcm/gcd calculations).