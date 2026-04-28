---
title: "Neutral neutral collisions"
nav_order: 8
parent: "Neutrals and Impurities"
layout: default
render_with_liquid: false
---

## Neutral neutral collisions ##

If you are running JOREK with particles, and you are using kinetic neutrals, then you might want to consider using neutral neutral collisions. This is important for the physics in regimes where the neutral neutral collisions happen on the same timescales or faster than neutral plasma interactions (e.g. charge exchange). This is usually only the case in colder areas of the domain such as where gas is puffed, in the private flux region, and in the divertor under detached conditions. If you doubt whether it is important for you, you could switch it on in a test case, see at what timescales collisions take place, and compare that to the other processes affecting the neutrals.

### Namelist input ###
To switch on neutral self collisions within a species, you need to set the flag %use_kin_neutral_coll = .true. for the neutral group you want to do collisions for, and specify the collisional parameters %neutral_coll_dTw (explained below). For instance, when your neutrals are a Deuterium species, you set something like:
```fortran90
part_group_configs(1)%id              = "D01"
part_group_configs(1)%Z               = -2
part_group_configs(1)%mass            = 2.01410178
part_group_configs(1)%coupling_scheme = 'ncs'
part_group_configs(1)%n_particles     = 1e4
part_group_configs(1)%type            = 'particle_kinetic_leapfrog'

part_group_configs(1)%use_kin_neutral_coll = .true.
part_group_configs(1)%neutral_coll_dTw     = 2.d-10, 273, 0.68
```
#### The collisional parameters %neutral\_coll\_dTw ####
The collisions are modeled with binary collisions between super particles, where the collisional cross section and its temperature dependence are determined from the variable hard sphere (VHS) model, which requires reference diameter d\_ref (m), reference temperatrue T\_ref (K) and viscosity index ω (-). These three values are the d, T and w of the %neutral\_coll\_dTw input parameter required from the user. They represent the physical collisional properties of the gas, and must be given to the code from outside sources.

In [G. A. Bird, Gas Dynamics and the Direct Simulation of Gas Flows, Appendix A](https://doi.org/10.1093/oso/9780198561958.005.0001) in tables A1 (for ω) and A2 (for diameter d<sub>ref</sub>) we can find the collisional parameters for H<sub>2</sub>, He, Ne, Ar, N<sub>2</sub> etc (both tables are for T<sub>ref</sub>=0°C=273K). However, there are no known values for specific isotopes or for radicals, so we have to approximate values for H/D/D<sub>2</sub>/T/T<sub>2</sub>. (If you know of better values, please discuss and share that knowledge.)

Since elastic collisions are dependent on the size of inter particle interactions, which are based on electromagnetic repulsion forces between the electrons and ions of both particles, we can assume that the number of neutrons does not influence the chance that a particle collides, and thus the VHS parameters are the same for isotopes. (Note that in the collisional mechanics particle weights play a role, so there the neutrons are important, and are also taken into account.) This leaves us with H<sub>2</sub>/D<sub>2</sub>/T<sub>2</sub> , for which we can use the H<sub>2</sub> parameters, and H/D/T  for which we need to approximate the parameters.

We can take the viscosity index ω<sub>H</sub>≈ ω<sub>He</sub>= ω<sub>Ne</sub>=0.66 given that these low Z mono-atomic gases have the same value it is reasonable that radical hydrogen will be in that range too. This choice also corresponds reasonably well with the value for ω<sub>D</sub>=0.68 chosen in  [S. Varoutis et al. Fus. Engin. Design 121 (2017) 13–21](https://doi.org/10.1016/j.fusengdes.2017.05.108), however it is not so clear to me how they arrived at this value from the source they cite as in their source neither radicals nor isotopes are mentioned (and the value they chose for ω<sub>D<sub>2</sub></sub>=0.73 is quite different from ω<sub>H<sub>2</sub></sub>=0.67 in the table of Bird).

The reference diameter can be approximated with the van der Waals radius r<sub>w</sub> (the length scale of a different particle particle interaction) times a correction factor based on the difference between van der Waals radius and d<sub>ref</sub> in He: d<sub>ref,H</sub> ≈ r<sub>w,H</sub>  (d<sub>ref,He</sub>/ r<sub>w,He</sub>) = 1.2 ・10<sup>-10</sup>・2.33・10<sup>-10</sup>/(1.4・10<sup>-10</sup>) ≈ 2.0・10<sup>-10</sup>m.

_Table with example parameters for dTw (H/D/T comes from the calculation above, the others come from the table from Bird). Note that impurity species have their own collisional operators which depend on their charge, so you likely won’t need the values for He, Ne, N<sub>2</sub> and Ar unless you want to simulate unionized neutral gas._
| Species | d<sub>ref</sub> (m) | T<sub>ref</sub> (K) | ω (-) |
|---------|---------------------|---------------------|-------|
| H/D/T | 2.0・10<sup>-10</sup> | 273 | 0.66 | 
| H<sub>2</sub>/D<sub>2</sub>/T<sub>2</sub> | 2.92・10<sup>-10</sup> | 273 | 0.67 |
| He | 2.33・10<sup>-10</sup> | 273 | 0.66 |
| Ne | 2.77・10<sup>-10</sup> | 273 | 0.66 |
| N<sub>2</sub> | 4.17・10<sup>-10</sup> | 273 | 0.74 |
| Ar | 4.17・10<sup>-10</sup> | 273 | 0.81 |

### How the code works ###
Detailed information on why this neutral neutral collision (NNC) algorithm was chosen, how it is exactly implemented (including all equations), and how it was verified can be found at git: [NNC implementation pdf](https://git.iter.org/rest/api/1.0/projects/STAB/repos/jorek/attachments/1327). What follows is a brief summary of the main components.

**Overview of the collisional algorithm:**
  * The collisions are run separately per neutral species.
  * _For each neutral species:_ particles are sorted per element.
  * _For each element:_ particles are sorted into collisional bins.  
  * _For each bin:_ the number of pairs to be tried for collision is determined (see NTC below). 
  * _For each pair:_ two random particles in the bin are drawn to form the pair. The real collisional chance of the pair is determined from P\_real=n sigma v\_r dt, where n is the sampled background density, sigma is the collisional cross section (determined from the variable hard sphere model), v\_r is the relative velocity and dt the timestep. The chance that is rolled against (P\_try) is rescaled to get the correct collisional frequency (see NTC below).
  * _For colliding pairs:_ the final velocity is determined from collisional mechanics (given two random impact parameters). Because we use variable weights, in theory the heavier superparticle (i.e. representing more atoms) would need to be split up into a colliding and a non-colliding part, but for now the code doesn't do that but instead gives the heavier particle the final velocity direction as if it had the same weight as the lighter particle, but scale its magnitude in order to keep energy balance. This breaks momentum balance (although momentum is still conserved in a statistical sense), but ensures the correct diffusive behaviour.

**NTC algorithm:**
NTC stands for no time counter and it is a widely used method to speed up direct simulation monte carlo collisions. Instead of trying for N/2 pairs with chance P\_real, we try for N\_try = N/2 * P\_max pairs with chance P\_try = P\_real/P\_max, as for convergence it is required that P\_max << 1 (to avoid the chance of having multiple collisions in one timestep), so this saves computational time while keeping the correct collisional frequency.

**On correctness:** 
It was verified that the correct diffusion coefficient of a gas chamber can be reproduced to within a few % relative error (with some ifs and buts, which are explained in the attached document, but the short of it is that the algorithm does what it should, the gas chamber scenario has been committed as particles/examples /test\_neutral\_neutral\_collision.f90, with example input in particles/examples/namelist/test\_neutral\_neutral\_collision\_input\_example).

**Limitations:** 
  * Currently only self-collisions within a species are implemented. When molecular interactions will be added, this framework needs to be expanded to also simulate the cross-collisions between molecular and radical hydrogen isotopes.
  * In kinetic\_main, the timestep for the neutral collisions calls is the fluid timestep, which might be a bit large for the neutral collisions depending on your application. In the worst case, you would need to lower the fluid timestep to resolve the neutral collisions well. In the future it is the idea to make the timing of different particle processes more flexible so that also multiple collision events can happen between each fluid timestep.


### Running the code ###
Running the NNC algorithm for a single species is about 5x faster than a single particle timestep for that species, and that ratio holds up to 10^7 particles (and probably above too, although this hasn’t been checked), so including the collisions should not slow you down too much, if your timestep was small enough to capture the collisions.

While the code runs, there will be some output generated for the self collisions of each species. This will look something like the following:
```
====================================================================================================
Neutral self collision
====================================================================================================
--- self collisions of species D01 ---
max (pa in elm/pa in bin/P_real/min tau) =    5193      78    4.29584E-01    2.32784E-08
P_max_elm rescale values (min/max)     3.95184E-01    5.76109E-01
WARNING: P_try>1 for          2 out of     219884 collision attempts during this timestep
diagnostics (P_real av/tau av/sigma av/pairs tried/pairs coll/weight coll/#P_try>1/#P_try<0/sum V_c/d av/av angle frac) =    1.83505E-01    5.44944E-08    6.36173E-20    2.19884E+05    1.83948E+05    9.01038E+24    2.00000E+00    0.00000E+00    2.51378E+03    1.41712E-10    8.19442E-01
Neutral self collision complete in (min/mean/max)    0.0653   0.0665   0.0677 s
```

#### What output to keep an eye on: ####
For the algorithm to work well, we need both P\_try<1 (as otherwise our NTC algorithm rescaling is missing collisions that should have happened) and P\_real<<1 (as otherwise our assumption that particle collides at most once during a timestep is inaccurate meaning we are missing collisions). If either P\_try>1 or P\_max>1 (which means that P\_real>1 last timestep, and next timestep some particles will be tried more than once) you will get a warning message. In the above example there was a warning for P\_try>1, which often happens at the first few timesteps of simulations as the rescaling value P\_max still needs to be determined accurately.


The main diagnostics to keep an eye on are the **P\_max\_elm (max)** (second line) (as a rule of thumb, maybe don’t let it go above 50%) and the average **P\_real** (diagnostic line) (as a rule of thumb, don’t let it go above 20%) as when either of them is big, this means that the timestep is a bit large for the collisions. If you need to lower your fluid timestep, you can use the **min tau** (first line) and **av tau** (diagnostics) to guide you in the new choice for the timestep.


#### Details of logfile output: ####
In the diagnostic output, the first two line tells as about the extremes of last timestep, we have: the maximum number of particles in an element **pa in elm**, the maximum number of particles in a collisional bin **pa in bin**, the maximum **P\_real**, the minimum collision time tau (=timestep/P\_real) **min tau**. On the second line we have the **min**imum and **max**imum P\_max in the domain (P\_max is tracked per grid element rather than globally).

The diagnostic line tells us about domain averages/values, so first we have the **av**erage **P\_real**, then the **av**erage **tau**, then the **av**erage collisional cross-section **sigma**, then the number of **pairs** that were **tried** for collision, the number of **pairs** that **coll**ided, the **weight** (# real particles) that **coll**ided, the number (**#**) of pairs with **P\_try>1** (this should be negligible and preferably 0), the number (**#**) of pairs with **P\_try<0** (should also be small and preferably 0, but due to negative projected densities this might be nonzero, but in any case in regions with negative projected densities, the real neutral density would be small and thus collisions are negligible), a sanity check on the **sum** of the collisional cell volumes **V\_c** (this is equal to the domain volume only if there are neutrals in every grid element, which for normal fusion simulations is not true in the core), the average distance between two super particles **d av** (which ideally should be smaller than the distance travelled between two collisions i.e. v*tau, as otherwise momentum and energy transport is overestimated, but given that the neutrals are not big channels anyway, in practice this overestimation happens a lot and can be ignored), and lastly the average scattering angle fraction (average of scattering angle/90° of all collided pair) **av angle frac** which tells us something about the whether the collisions are large angle collisions (~1) or small angle collisions (<<1) (since the collisions are elastic neutral collisions, we are expecting large angle collisions, so if this fraction is smaller than 0.7 or so, there might be something strange going on in the simulation, such as that most particles that collide have aligned velocities, maybe due to some neutral gas flow effect).


