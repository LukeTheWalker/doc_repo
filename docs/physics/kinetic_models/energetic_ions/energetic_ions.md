---
title: "Energetic Ion"
nav_order: 7
parent: "Kinetic Particle Module"
layout: default
render_with_liquid: false
---

# Energetic ions

A species of suprathermal ions can be included in JOREK via the kinetic particle framework. To simulate the interaction of energetic particles (EPs) with MHD modes a hybrid kinetic-MHD model is used [1]. The plasma is split into a bulk part, which is treated with an MHD model, and the energetic particles, which are treated kinetically. More details about the JOREK implementation and applications can be found in [2].

## Full-f

JOREK uses a full-f formulation for the EPs. Their distribution function is modeled by $N_\mathrm{p}$ marker particles:

$$
    f(\mathbf{r}, \mathbf{v}, t) = \sum_{i=1}^{N_\mathrm{p}} w_i \, \delta(\mathbf{r}-\mathbf{r}_i(t)) \, \delta(\mathbf{v}-\mathbf{v}_i(t))
$$

The markers are evolved in time with one of the available pushers e.g. the Boris pusher. 

## Coupling scheme

The coupling between EPs and bulk MHD fluid is provided by a pressure coupling scheme. The EP pressure tensor $\boldsymbol{P}_\mathrm{h}$ enters the momentum balance equation according to

$$
  \rho \frac{\partial \mathbf{u}}{\partial t}=-\rho \mathbf{u} \cdot \nabla \mathbf{u}+\mathbf{J} \times \mathbf{B}-\nabla p +  \left[ \nabla\cdot\underline{\boldsymbol{P}_\mathrm{h}}\right]_\perp
$$

Instead of the full tensor, usually the CGL form 

$$
  \underline{\boldsymbol{P}}_\mathrm{h} =  \left[  P_{\parallel} \mathbf{b}\mathbf{b} + P_{\perp}\left( \underline{1}-\mathbf{b}\mathbf{b} \right)  \right]
$$

is used with components

$$
  P_\parallel = m \int \mathrm{d}^3 \mathbf{v} \ f(\mathbf{r}, \mathbf{v}, t) v_\parallel^2
$$

$$
  P_\perp = \frac{m}{2} \int \mathrm{d}^3 \mathbf{v} \ f(\mathbf{r}, \mathbf{v}, t) v_\perp^2
$$

In reduced MHD, it is possible to switch to a scalar pressure for the EPs by setting `use_pcs_full = .false.` and `use_pcs = .true.` In the full MHD models, only the CGL form is implemented and always switched on by `use_pcs = .true.`

The pressure tensor is provided by the six components

$$
  \boldsymbol{P}_\mathrm{h}^{RR}, \ \boldsymbol{P}_\mathrm{h}^{ZZ}, \ \boldsymbol{P}_\mathrm{h}^{\phi\phi} \ \boldsymbol{P}_\mathrm{h}^{\phi\phi}, \ \boldsymbol{P}_\mathrm{h}^{RZ}, \ \boldsymbol{P}_\mathrm{h}^{R\phi}, \ \boldsymbol{P}_\mathrm{h}^{Z\phi}
$$

which are then used in the MHD system of equations in `mod_elt_matrix_fft`. 

## Example

An example use case can be found in `particles/examples/tae_phase_space_project.f90` with the input in `namelist/model307/itpa(_eq)` or `namelist/model710/itpa_full(_eq)`. 

First equilibrium, then particles. 



## Diagnostics

phase space projections

projections very flexible

## Initialization of energetic particles

### Consistency with the MHD equilibrium



### Importing a fast particle experimental distribuion





# Old wiki articles:

Importing fast particle experimental distribution function

Projections on arbitrary coordinates (particles_phase_space)

## References:
[1] W. Park et al., Phys. Fluids B 4, 2033 (1992).

[2] T. Bogaarts et al., Phys. plasmas 29, 122501 (2022).






