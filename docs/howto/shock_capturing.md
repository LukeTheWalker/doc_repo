---
title: "Use Shock Capturing Features"
nav_order: 5
parent: "Numerics and Stabilization"
grand_parent: "Howto"
layout: default
render_with_liquid: false
---

How to use shock capturing stabilization
----------------------------------------

The shock capturing stabilization terms should be used if numerical oscillations are seen in presence of a shock/discontinuity, leading to numerical stability problems. Currently shock capturing is not included into all branches of JOREK. Only model600 and model750 include them.

The technique includes the detection of a discontinuity and the addition of the numerical stabilization locally, near a discontinuity and in the parallel direction. The shock detection is based on the pressure gradient.

In practice, the stabilization is added at each time step by updating visco_T, visco_par, D_perp, ZK_perp, Dn0 and D_perp_imp with the stabilization coefficients if the shock-capturing-scheme switch **use_sc** is set to .true. . The amount of the shock capturing stabilization can be controlled from the input file using following parameters: 

  * Viscosities
    * visco_sc_num  
    * visco_par_sc_num
  * Diffusivities 
    * D_par_sc_num     
    * D_perp_sc_num 
    * D_par_imp_sc_num
    * D_perp_imp_sc_num
  * Single Temperature
    * ZK_par_sc_num 
    * ZK_perp_sc_num
  * Two Temperature  
    * ZK_i_par_sc_num
    * ZK_i_perp_sc_num 
    * ZK_e_par_sc_num
    * ZK_e_perp_sc_num
  * Neutrals
    * Dn_p_sc_num      
    * Dn_pol_sc_num
  * Impurities
    * D_par_imp_sc_num
    * D_perp_imp_sc_num 

By default, above parameters are set to zero. The stabilization can be used only in selected MHD variables in which shocks/discontinuities are seen. Typically, for any MHD variable, parallel and perpendicular parameters may be set to equal value, for example, D_par_sc_num = 10 and D_perp_sc_num = 10, in the input file. Such a choice will add stabilization isotropically. If the value 10 does not suffice, try increasing it to 20 and so on. For the neutral density equation 'Dn_p_sc_num' and 'Dn_pol_sc_num' control the stabilization in the phi (parallel) direction and poloidal plane respectively. 

There exists the possibilty to extend the shock capturing to visco_par_par and also include visco_par_par_sc_num. This has been tried, but showed no significant improvement for the considered pellet expansion case.

  * **add_sources_in_sc:**
The stabilization scheme may be 'upgraded' by setting the logical variable 'add_sources_in_sc' = .t. in the input file. It is set to .false. by default. Setting 'add_sources_in_sc' = .t. increases the strength of the stabilization near the location of the sources. This treatment may be needed if sources are strong.

  * **An example:**
An example of isotropic shock-capturing stabilization parameters to be used for a simulation with single temperature and with impurities: 

```
use_sc = .t. 
add_sources_in_sc = .t. 
visco_par_sc_num = 10 
visco_sc_num = 10 
D_par_sc_num = 10
D_perp_imp_sc_num = 10 
ZK_par_sc_num = 10 
ZK_perp_sc_num = 10 
D_par_imp_sc_num = 10 
D_perp_imp_sc_num = 10 
```


 ### Few Remarks: 

1. To add 'isotropic' stabilization in a variable, corresponding parallel and perpendicular parameters should be equal. I suggest to start with this simple but effective 'isotropic' scheme. 

2. The parallel direction refers to the direction of the magnetic field. To use 'anisotropic' stabilization (more in the parallel direction), use higher values for par_sc_num parameter than perp_sc_num, for example: ZK_par_sc_num = 100 and ZK_perp_sc_num = 1. 

3. Unfortunately, setting optimum values of shock-capturing parameters requires will take some experience. To my experience with SPI simulations with full MHD, par_sc_num = perp_sc_num = 10 seems a good choice of parameters. However, they can be different for different grids and problems.  

4. Please note that the shock-capturing stabilization scheme does not affect the induction, current and vorticity equations and hence there are no corresponding numerical parameters.

For the details please see  [shock_capturing.pdf](assets/shock_capturing/bv_stabilization.pdf)


