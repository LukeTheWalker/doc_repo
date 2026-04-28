---
title: "Run with Sheath Heat-Flux BC"
nav_order: 6
parent: "Physics Options"
grand_parent: "Howto"
layout: default
render_with_liquid: false
---
## Running with sheath boundary conditions for the heat-flux

### Heat flux definition
The total plasma heat flux is composed of three main terms, representing conduction of thermal energy, convection of thermal energy and convection of kinetic energy. In a single temperature MHD model, the equation in the non-normalized form is
$$
\mathbf{Q} = -(\kappa_{\perp}\nabla_{\perp}+\kappa_{\parallel}\nabla_{\parallel})  T   +  \frac{\gamma}{\gamma-1}n_e k_B  T (\mathbf{v}_\perp +\mathbf{v}_\parallel) + \frac{\rho}{2}v^2 (\mathbf{v}_\perp +\mathbf{v}_\parallel)
$$
to derive such expression see  [Goedbloed, Principles of MHD, vol I, section 4.3.2., 2008 digital print].



### Single temperature models (303/333/500/600)

By default, the temperature is fixed in the boundary (Dirichlet B.C.). Instead, you can impose the normal heat-flux to the boundary as:
$$
\mathbf{Q}\cdot\mathbf{n} = \gamma_{sh} n_e k_B T_e \mathbf{v_\parallel}\cdot\mathbf{n}
$$
This expression is given by "P. Stangeby, *The plasma boundary of magnetic fusion devices*, (2000)" in chapter 2 equation 2.94. Typical values of $\gamma_{sh}$ are 7-8 for $T_e = T_i$.

To include this boundary condition, let's say for boundary type `i`, you has to set
```text
bc_natural_open = .t.      ! sheath boundary conditions enabled
gamma_stangeby  = 8.d0     ! The Stangeby gamma_sh
bcs(i)%dirichlet%T = .f.   ! Switch off the Dirichlet condition
bcs(i)%natural%T   = .t.   ! Switch on the natural condition
```
For more information on how to set boundary conditions and noundary type see [choose boundary conditions](./choose_boundary_conditions.md).

## Two temperature models (400/502/600)
In this case, each temperature equation has a separate $\gamma_{sh}$, and the setup is

```text
bc_natural_open = .t.      ! sheath boundary conditions enabled

! ions
gamma_i_stangeby    = 3.0d0 ! The Stangeby gamma_sh for ions
bcs(i)%dirichlet%Ti = .f.   ! Switch off the Dirichlet condition
bcs(i)%natural%Ti   = .t.   ! Switch on the natural condition

! electrons
gamma_e_stangeby    = 5.0d0 ! The Stangeby gamma_sh for electrons
bcs(i)%dirichlet%Te = .f.   ! Switch off the Dirichlet condition
bcs(i)%natural%Te   = .t.   ! Switch on the natural condition
```
For more information on how to set boundary conditions and noundary type see [choose boundary conditions](./choose_boundary_conditions.md).

### Treatment at grazing angles


As shown in the Stangeby equation at the top of the page, the heat flux vanishes in situations where $\mathbf{v}\cdot\mathbf{n}=0$. These situations may occur when magnetic field lines are totally parallel to the wall (grazing angles). In those cases, artificial energy accumulation may occur, which is unphysical. For that, you can use a minimum heat flux, which will is purely diffusive and it is chosen as

$$
\mathbf{Q}\cdot\mathbf{n}|_{min} = \gamma_{sh} n_e k_B  T_e c_s \sin (\theta_{min}) 
$$

where the sound speed $c_s$ is calculated using directly the temperature (not $v_\parallel$). Note that now the total heat flux has a new extra contribution due to this minimum heat flux

$$
\mathbf{Q}\cdot\mathbf{n} = \gamma_{sh} n_e k_B  T_e \mathbf{v}_\parallel\cdot\mathbf{n} +\mathbf{Q}\cdot\mathbf{n}|_{min}
$$

You can select the value of $\theta_{min}$ from the JOREK input file, setting

    min_sheath_angle = 1  ! Example of 1 degree (not in radians!)

**IMPORTANT**: In order to be able to calculate these fluxes, your grid resolution or $\kappa_\perp$ must be sufficiently large to resolve the numerical gradients imposed by the boundary condition. Note also that by default, this treatment is also applied to the particle flux

$$
\mathbf{\Gamma}\cdot\mathbf{n} = n_i \mathbf{v}_\parallel\cdot\mathbf{n} +\mathbf{\Gamma}\cdot\mathbf{n}|_{min}
$$

where

$$
\mathbf{\Gamma}\cdot\mathbf{n}|_{min} =  n_i c_s \sin (\theta_{min}) = -D \nabla n_i\cdot\mathbf{n}
$$

This approach was used in the paper below

[1] [F J Artola et al 2021 Plasma Phys. Control. Fusion 63 064004](https://iopscience.iop.org/article/10.1088/1361-6587/abf620)

