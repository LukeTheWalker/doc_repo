---
title: "Introduction to the kinetic framework"
nav_order: 7
parent: "Kinetic Particle Module"
layout: default
render_with_liquid: false
---

## Introduction to the kinetic framework

Kinetic simulations make use of test particles (also sometimes called tracer particles, superparticles, or marker particles, although there are nuances in meaning) which represent the underlying distribution function of the real particles (for example individual atoms) to be simulated. This is in contrast to fluid simulations, where the real particles (for instance the plasma ions and electrons) are represented by quantities on a grid (such as density and temperature). Rather than using deterministic equations to evolve the plasma state (in a fluid solver), the kinetic particles are updated by sampling random interaction outcomes from the statistical distribution of the interaction. That's why this type of simulation is often called a Monte Carlo simulation because of the randomness in Monte Carlo casino's.

The kinetic extension in JOREK is a flexible framework including options for kinetic neutrals, impurities, runaway electrons and energetic particles, with different schemes to set up 2 way coupling with the MHD fluid. The kinetic extension runs from the kinetic_main program, which is the kinetics extension equivalent of jorek_model600 (which is compiled from jorek2_main.f90). With kinetic_main, the choices of the simulation setup can be made directly from the namelist input file (the details of which will be explained on this page and subpages).

Currently the kinetics extension lives in a separate branch called "kinetic_develop". There is an ongoing effort to pull together the capability of many separate example programs into "kinetic_main", so that the separate example files are not necessary anymore (once this is done, kinetic_develop will be merged into develop).

To use kinetic_main, you first need to compile. Make sure that your hard coded settings are correct (`./util/config.sh`) and are compatible with kinetic_main (currently, kinetic_main is compatible with with_vpar and with_TiTe, but not with with_neutrals and with_impurities as it assumes you will do those kinetically. Furthermore everything should be compatible with 2D and 3D so you can choose any normal combination of n_tor, n_plane and n_period. If you don't know what this is about, please see [running jorek for the first time](../../howto/running_jorek_for_the_first_time.md)). Then, simply run the following command in your jorek folder to compile kinetic_main:

```bash
  make kinetic_main
```

To run kinetic_main, you need an initial base MHD jorek_restart.h5 file, such as can be made by running jorek_model600 with restart=.f. (for more information on running the fluid model, see [running jorek for the first time](../../howto/running_jorek_for_the_first_time.md), be sure to use model600 though). kinetic_main will automatically load in jorek_restart.h5 from the folder in which it is run (or throw an error if it doesn't exist).

Furthermore, depending on your application you might need additional files in your simulation folder such a wall.txt (for grid_to_wall=.true. if you don't use patches), or files like acd12_h.dat (which contain rate coefficients for kinetic neutral/impurity reactions with the plasma), or files like y_DD.dat (which contain Eckstein coefficients which describe rates for wall interactions such as sputtering).

Furthermore, you need a namelist input file which contains input for both the MHD plasma and the kinetic particles you are including (which will be explained shortly).

With the right files in your simulation folder, you can simply run like:

```bash
  kinetic_main < namelist
```

### Kinetic namelist input basics 

The kinetic species in kinetic_main are governed from the input file using "part_group_configs". All particles in a group will represent the same underlying species (e.g. W impurities, or runaway electrons), but each test particle will have it's own position, weight and velocity/momentum/energy (depending on the type of particle) etc.

To add a particle group (i.e. a kinetic species), set it's defining variables accordingly (these apply for all individual particles from this group:)

| Variable | meaning |
| - | - |
| %id | 3 letter unique ID for this particle group (the rest of the code and the output file will refer to this group by this ID. The id is required and must be unique) |
| %Z | atomic mass number (integer, -1 for e, -2 for D, -3 for T) |
| %mass | mass of the particle group (in AMU) |
| %coupling_scheme | a three letter code which specifies how this group is coupled to the MHD plasma, see [[coupling_schemes | coupling schemes]] |
| %n_particles | the maximum number of simulated test particles this group can have (can be specified as real number like 1e6 for convenience) |
| %type | the particle type defines both which variables the particle has (such as charge q, velocity, energy, momentum, magnetic moment etc.) and how the particle is pushed by a pusher to propagate to its new position after a timestep |

Then depending on the type of particle and the coupling, you might want to specify additional flags that describe which interactions with the plasma to simulate etc. See more on the linked pages from [particles](../particles.md) in the section "Available coupling types and tutorials".
