# Particle coupling schemes

As explained in the kinetics [introduction](./particle_introductions,md), each part_group_config needs a 3 letter code %coupling_scheme. This page gives a bit more detail on the different coupling schemes.

In the backend, the combination of chosen coupling schemes for all used part_group_configs will automatically create a certain number of variables that will be projected to the finite element grid to be fed into the fluid equations (mod_elt_matrix_fft) as sources/sinks. This quantifies the feedback to the plasma from the kinetic particles. The required coupling variables are determined in particles/mod_coupling_settings.f90 (assess_and_accumulate_variables), with the coupling variables themselves defined in particles/coupling_variables.f90

At the moment, kinetic_main assumes some coupling to the plasma, i.e. it is not possible to use kinetic_main while using a static background plasma or for tracer purposes. To do this, you need a dedicated program script, rather than kinetic_main.

The currently implemented coupling schemes are:

| coupling_scheme | description |
|-----------------|-------------|
| ncs | neutral coupling scheme, see [neutrals and impurities coupling scheme](./neutrals_and_impurities.md) |
| ics | impurity coupling scheme, see [neutrals and impurities coupling scheme](./neutrals_and_impurities.md) |
| rep | pressure coupling scheme for runaway electrons, see [runaways electrons](./runaways_electrons.md) |
| ccs | current coupling scheme for fast particles, see [energetic ions](./energetic_ions.md) |
| pcs | pressure coupling scheme for fast particles, see [energetic ions](./energetic_ions.md) |
| pcf | pressure coupling scheme, full tensor, for fast particles, see [energetic ions](./energetic_ions.md) |
