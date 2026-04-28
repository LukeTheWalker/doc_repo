# Run with kinetic neutrals and impurities
This tutorial shows how to include kinetic neutrals and/or impurities in JOREK simulations. We assume that the user is already familiar with running standalone JOREK simulations, see [[running_jorek_for_the_first_time|Running JOREK for the first time]].

## 1. Executable and input files
At the moment, simulations are only possible on a branch called kinetic_develop (to be merged into develop). Checkout this branch, choose model600 in your Makefile.inc and compile kinetic_main with your preferred model settings. It has to be noted that the option with_vpar=.true. is needed to run with these particles. The model supports both one- and two-temperature settings and ntor=1 or higher, as well.

The reaction rates for the atomic physics processes are extracted from OpenADAS files, the ones required for this tutorial are found here:

A jorek restart files in the form of jorek_restart.h5 is needed to interpolate the background fields.

# 2. Including neutral particles
To include neutral particles of species deuterium, the following lines have to be added to your namelist:
```
restart_particles =.f.
tstep_particles = 5.d-7

deuterium_adas = .t.
```
where tstep_particles defines the particle step size (for each fluid step) in seconds and restart_particles is no particle restart file is available. Otherwise set to .t. and have a part_restart.h5 ready. Set deuterium_adas=.t. to X.

We define valves, and initialize our particles inside the valves defined by polygons or circles:
```
valves(1)%type = "poly"
valves(1)%poly_R = 3.86d0, 3.9d0, 3.86d0, 3.9d0
valves(1)%poly_Z = 0.1d0,  0.1d0,  0.0d0, 0.0d0
```
Next, the deuterium particle group is initialized with id (chosen freely), charge number, atomic mass, coupling scheme, the number of particles to be allocated and particle type:
```
! Deuterium Neutrals (D01)
part_group_configs(1)%id = "D01"
part_group_configs(1)%Z = -2                             ! JOREK convention charge number for kinetic D
part_group_configs(1)%mass = 2.01410174369812            ! atomic mass in AMU
part_group_configs(1)%coupling_scheme = "ncs"            ! Neutral Coupling Scheme
part_group_configs(1)%n_particles = 1e4
part_group_configs(1)%type = "particle_kinetic_leapfrog" ! only supported type for neutrals and impurities
part_group_configs(1)%atom_data_suffix = "12_h"          ! ending of corresponding adas .dat files
```

To choose which atomic physics to include:
```
part_group_configs(1)%use_kin_puffing = .t.
part_group_configs(1)%use_kin_cx = .t.
part_group_configs(1)%use_kin_ionisation = .t.
part_group_configs(1)%use_kin_recombination = .t.
part_group_configs(1)%use_kin_radiation = .t.
```

For the particle-wall interaction we choose reflection here:
```
part_group_configs(1)%wall_act_configs(1)%type = "reflection"
```

The background fluid interacts with the wall, too and can lead to new neutrals:
```
fluid_configs(1)%Z=-2
fluid_configs(1)%wall_act_configs(1)%type="wall recomb"
fluid_configs(1)%wall_act_configs(1)%target_group_id="D01"
fluid_configs(1)%wall_act_configs(1)%supers_num_wall=200
```

The puffing pattern/rate from the valve for D is set by:
```
part_group_configs(1)%puff_ctrl(1)%times = 0.
part_group_configs(1)%puff_ctrl(1)%rates = 1.d20 !< constant puffing rate
part_group_configs(1)%puff_ctrl(1)%supers_num_puff = 40
```

Now run like you would usually do with JOREK, but this time using kinetic_main. The files reuired for this tutorial can be found here:

Let's complicate things a bit and include neutral-neutral collisions with:
```
part_group_configs(1)%use_kin_neutral_coll   = .t.
part_group_configs(1)%neutral_coll_dTw = 2.d-10, 273, 0.66
```

# 3. Including impurities
In the following example, we will include nitrogen impurities (along with the previously described neutrals), seeded from the same valve as deuterium. Similarly to neutrals, in the namelist we set:
```
! Nitrogen Impurities (N01)
part_group_configs(2)%id = "N01"
part_group_configs(2)%Z = 7
part_group_configs(2)%mass = 14.0067396163940
part_group_configs(2)%coupling_scheme = "ics"
part_group_configs(2)%n_particles     = 1e4
part_group_configs(2)%type            = "particle_kinetic_leapfrog"

part_group_configs(2)%use_kin_puffing        = .t. 
part_group_configs(2)%use_kin_ionisation     = .t.
part_group_configs(2)%use_kin_radiation      = .t.
part_group_configs(2)%use_kin_bg_collisions  = .t.
part_group_configs(2)%atom_data_suffix = "96_n"
part_group_configs(2)%puff_ctrl(1)%times = 0     
part_group_configs(2)%puff_ctrl(1)%rates = 1.d19
part_group_configs(2)%puff_ctrl(1)%supers_num_puff = 20
```

Now we can run with both neutrals and impurities.

# 4. Tips and tricks
  * When other impurity species are needed, one has to change the parameters Z, mass, atom_data_suffix and have the corresponding ADAS files.
  * If the SOL is of interest it is recommended to enable grid_to_wall and set natural boundary conditions, using:
  * To include particle projections in vtks, use the flag -proj jorek, with convert2vtk.sh
  * Excessive radiation can lead to negative temperatures and numerical problems, make sure that you don't use unreasonable puffing rates, then look into one of the workarounds at [[corr_neg|The following functionality allows to "correct" negative densities or temperatures in order to avoid floating point exceptions]].