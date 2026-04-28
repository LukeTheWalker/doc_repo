---
title: "Introduction to the particle wall_actions"
nav_order: 8
parent: "Neutrals and Impurities"
layout: default
render_with_liquid: false
---

## Introduction to particle wall\_actions ##

At the wall, there are a variety of things that could happen that influence the kinetic particles in your simulation. The plasma might for instance recombine into neutrals and simultaneously sputter tungsten, kinetic impurities species might neutralize and re-enter the domain with a different velocity, and tungsten might self sputter. In the backend (found at particles/mod\_particle\_wall\_interaction.f90) all of these interactions at the wall are handled through wall\_action objects which contain the information about the type of interaction, the origin species (what goes into the wall) and the target species (what comes out of the wall). Every wall\_action object only handles one interaction to keep the code modular. Currently the wall\_action %types that are implemented are: "reflection", which handles neutrals/impurities neutralising on the wall and re-entering the plasma with a different energy (but the same weight), "self sputter", which handles kinetic wall impurities which self sputter on the wall, "fluid sputter", which handles the sputtering done by the plasma, "wall recomb", which handles the plasma recombining at the wall into kinetic neutral particles, and "pump", which handles pumping surfaces. For the moment the implemented types focus on kinetic neutrals and impurities, but should boundary conditions be necessary for other types of particles, this framework could be extended to include them (e.g. diagnosing the wall loads from REs, or dealing with the exhaust of fusion He particles).

To give the user full flexibility on what interactions to use for the simulation, the wall\_actions can be set from the namelist through the wall action config object (wall\_act\_configs). One species can do multiple things at the wall so it might be necessary to specify multiple wall\_actions through their configs per origin species.

For each wall\_act\_config object the following options can be specified:
| wall\_act\_configs(i)% | option meaning |
|----------------------|----------------|
| type                 | one of the types (such as "wall recomb") mentioned above |
| target\_group\_id      | the %id of the target group (leave blank for self interaction types such as "self sputter") |
| weight\_factor        | optional factor to scale the resulting weight which is useful in more complicated scenario's |
| only\_in\_polygon      | set .true. if you only want to do this action in the polygon defined by poly\_R, poly\_Z (default .false.)|
| poly\_R               | R coordinates of polygon (only relevant if only\_in\_polygon=.true.). Define the polygon in order in the R,Z plane (point 1 connects to 2, connects to 3 etc.) |
| poly\_Z               | Z coordinates of polygon (only relevant if only\_in\_polygon=.true.) |
| nametag              | optional, for distinguishing this wall\_action in the output file compared to similar wall\_actions |
| supers\_num\_wall      | to set the number of created super particles |
| supers\_weight\_wall   | to set the weight of each individual created super particle |
| supers\_ratio\_wall    | to set the ratio of created super particles this action over the species total (%n\_particles) |

At the moment, only\_in\_polygon only works for the particle interactions ("reflection", "self sputter" and "pump"), and is likely mostly used for "pump" type wall\_actions. It works by only selecting those particles which got lost with last known location in the given polygon (before they left the domain). The last known location must have been within a boundary element (otherwise the particle is lost altogether and an error will be thrown), so to catch all particles reaching the boundary you want to select, make sure to include the depth of the boundary elements inside your polygon. 

Set the nametag option to an understandable name of the polygon (e.g. "outer\_target"), especially if you use multiple instances of the same action type and target in different polygons (if you have multiple pump surfaces for example).

At most one of the supers\_...\_wall options should be set, and they must all be left blank for %types that don't produce super particles (such as "reflection" or "self sputter"). If the %type creates particles and no super\_...\_wall is set, then the default is the supers\_ratio\_wall scheme with a ratio of 5.d-4

To set the interactions of the MHD fluid with the wall (which creates kinetic particles), it is necessary to set up fluid\_configs objects. If you run a simple plasma, you usually only need 1 fluid\_config, but you might want to treat the single MHD fluid as a combination of different species at the wall (e.g. a D+T plasma with trace N). For each fluid\_configs(i) (with i=1,2,...) the following options can be specified:

| fluid\_configs(i)%   | option meaning |
|---------------------|----------------|
| Z                   | the atomic number of the species (or -2 for D, -3 for T) (this option is always required) |
| density\_fraction    | the fraction of the MHD fluid density represented by this species (the sum of fluid\_configs(:)%density\_fraction must be 1) |
| wall\_act\_configs(:) | the corresponding wall\_action configs of this species |

Note that if you only specify one species, you can leave the %density\_fraction blank as it will be assumed equal to 1.

In the backend all wall\_actions will be generated from these wall\_act\_configs, and they will be grouped based on their types and targets. Self interaction type (like "self sputter" and "reflection") wall\_actions will be run after the particle stepper, while the other types will be run before the stepper as they generate new particles. 

If you specified multiple wall\_actions for the same species in the same area (such as a local "pump" action on top of a global "self sputter" action), only one interaction will be done for any given particle upon hitting the wall. The  "pump" action is hardcoded to take precedence over "self sputter" and "reflection". E.g. if you set both a "pump" action and a "self sputter" action in the same area (for example because the "pump" is local with only\_in\_polygon=.t., and the "self sputter" is the default global), only the "pump" action will happen in that area.

More complicated scenario's: avoid specifying other overlapping actions (e.g. 2 overlapping local "pump"s, or overlapping "reflection" and "self sputter". It will do the first applicable "pump" action or else the first applicable "reflection" or "self sputter" action that you specified, but that is all way more confusing than just making sure the polygons don't overlap. There is no check for this.). If you somehow want to pump everywhere except a local area where you want "reflection" or "self sputter", then just define a polygon that excludes the part where you don't want pumping for the "pump" action.

The "fluid sputter" types are grouped per target species and the creation scheme of the first "fluid sputter" type is used for the group rather than for that individual sputter action as this means the weight of the generated W is more homogeneous. (E.g. in a D plasma with trace N; the $D^+ \rightarrow W$ fluid sputtering generates the same weight W superparticles as the $N^+ \rightarrow W$ fluid sputtering.)

You can specify particle wall\_actions to happen more often than once every _fluid_ timestep (each n-th _particle_ step) through `part_group_configs(i)wall_act_each_nstep_part`. This is useful when a large fraction of your particles hit the wall during a single fluid timestep. See also [kinetic timestepping](../timestepping.md)

### Practical example to showcase the functionality ###

Suppose you want to have a kinetic particle simulation with neutrals and you want the neutrals to reflect off the wall when they hit the wall. As normal you first specify your neutral species:

```fortran90
part_group_configs(1)%id              = "D01"
part_group_configs(1)%Z               = -2
part_group_configs(1)%mass            = 2.01410178
part_group_configs(1)%coupling_scheme = 'ncs'
part_group_configs(1)%n_particles     = 1e4
part_group_configs(1)%type            = 'particle_kinetic_leapfrog'
```

With your origin species set up, you can set the wall action for this species:

```fortran90
part_group_configs(1)%wall_act_configs(1)%type = "reflection"
```

In the backend the new velocities are determined using an Eckstein formula of which the coefficients must be specified in files in the simulation folder (for "reflection" and "wall recomb" it will determine whether there was thermal desorption or fast reflection based on these coefficients. For deuterium-deuterium reactions it looks for the files y\_DD.dat and ye\_DD.dat, examples of which can be found in the reg\_tests/testcases/particle\_imp\_xpoint\_600). Because the reflection type necessarily means that the target species is the origin species, there is no need to specify the target species explicitly, and because there are no new superparticles created in this interaction, there is no need to set the supers\_...\_wall options.
 
If you now want to have a non-fully saturated wall (or effectively a global pumping at the wall), you could set the %weight\_factor to something smaller than 1 to simulate partial absorption of neutrals into the wall:

```fortran90
part_group_configs(1)%wall_act_configs(1)%weight_factor=0.98d0
```

Now you also might want to simulate a pump duct. You can do this by setting a "pump" action for a specific polygon (for example in the private flux region), setting weight\_factor < 1 (so that the absorption coefficient at the pump surface is 1-weight\_factor, to get a realistic absorption coefficient, refer to [Kukushkin et al. 2017](https://doi.org/10.1016/j.jnucmat.2007.01.094) equation 2) and defining the polygon in which the boundary is a pump surface (in this everything in the square with opposite corners of (R,Z)=(2.75,-1.4) and (3.2,-1.7)):

```fortran90
  part_group_configs(1)%wall_act_configs(2)%type="pump"
  part_group_configs(1)%wall_act_configs(2)%weight_factor=0.7d0
  part_group_configs(1)%wall_act_configs(2)%only_in_polygon=.t.
  part_group_configs(1)%wall_act_configs(2)%poly_R= 2.75,3.2,3.2,2.75
  part_group_configs(1)%wall_act_configs(2)%poly_Z= -1.4,-1.4,-1.7,-1.7  
  part_group_configs(1)%wall_act_configs(2)%nametag="PFR"
```

Okay, so with this setup pumping will be done with an absorption factor of (100%-70%=)30% in the defined polygon (because the "pump" action takes precedence over other particle particle actions, and only one particle particle action is executed per particle). Outside the polygon (everywhere else), particles will be reflected (thermal desorption or fast reflection) off the wall with absorption of (100%-98%=)2% to simulate a non fully saturated wall.

Suppose your neutrals dominate the divertor area, and thus they also hit the wall a lot, then you want to do your wall_actions for this paricle group more often than once every _fluid_ timestep. If that is the case, you can set the wall actions to be done every n integer _particle_ timesteps (in this case every 2 particle timesteps)

```fortran90
part_group_configs(1)wall_act_each_nstep_part  = 2
```

Good, that is the neutrals settled. Now suppose you want to investigate the first plasma after boronization in a scenario where the tungsten divertor is still partially covered by the boron, and you are interested in the tungsten transport in this case (I don't know why, but hey, you do you). So you add a second kinetic species of tungsten impurities:

```fortran90
part_group_configs(2)%id              = 'W01'
part_group_configs(2)%Z               = 74
part_group_configs(2)%mass            = 183.84
part_group_configs(2)%coupling_scheme = 'ics'
part_group_configs(2)%n_particles     = 1e4
part_group_configs(2)%type            = 'particle_kinetic_leapfrog'
```

Suppose there's 20% B and 80% W on the wall surface, and you ignore boron entering the plasma so you want a "reflection" type on the boron but a "self sputter" type on the tungsten. You then set

```fortran90
part_group_configs(2)%wall_act_configs(1)%type          = "reflection"
part_group_configs(2)%wall_act_configs(1)%weight_factor = 0.2d0
part_group_configs(2)%wall_act_configs(2)%type          = "self sputter"
part_group_configs(2)%wall_act_configs(2)%weight_factor = 0.8d0
```

Okay, on the particle side everything is set up, but now you want to specify how the MHD fluid should behave at the wall. Suppose you have a deuterium plasma with a trace of nitrogen (for the purpose of sputtering). You want the deuterium to wall recombine into kinetic neutral deuterium, you want the deuterium to sputter tungsten, and you want the nitrogen to sputter tungsten. So you set the fluid configs and their wall actions:

```fortran90
fluid_configs(1)%Z                = -2
fluid_configs(1)%density_fraction = 0.99d0
fluid_configs(1)%wall_act_configs(1)%type               = "wall recomb"
fluid_configs(1)%wall_act_configs(1)%target_group_id    = "D01"
fluid_configs(1)%wall_act_configs(1)%supers_weight_wall = 1.d16

fluid_configs(1)%wall_act_configs(2)%type               = "fluid sputter"
fluid_configs(1)%wall_act_configs(2)%target_group_id    = "W01"
fluid_configs(1)%wall_act_configs(2)%weight_factor      = 0.8d0
fluid_configs(1)%wall_act_configs(2)%supers_num_wall    = 10

fluid_configs(2)%Z                = 7
fluid_configs(2)%density_fraction = 0.01d0
fluid_configs(2)%wall_act_configs(1)%type               = "fluid sputter"
fluid_configs(2)%wall_act_configs(1)%target_group_id    = "W01"
fluid_configs(2)%wall_act_configs(1)%weight_factor      = 0.8d0
```

Note that %supers\_num\_wall is only set for the first "fluid sputter" as that sets it for the wall\_action group that does "fluid sputter" into "W01". We still use 80% of the "fluid sputter" because we have the 20% boron still. In this example case there is a slight inconsistency at the wall and in the rest of the plasma because the above fluid\_configs are only taken into account at the wall. For kinetic deuterium neutrals that ionise into the MHD plasma, then only 99% of that ionised weight will wall recombine back into deuterium at the wall (because the density\_fraction of the deuterium in the plasma is set to 0.99d0). You could compensate for this artificial particle loss by setting %weight\_factor of the "wall recomb" action to 1/0.99 = 1.010101010101d0. Essentially these kind of inconsistencies come from the fact that we have a single MHD fluid, but we then want to separate that single species into different components at the wall because trace impurities are very important for sputtering.