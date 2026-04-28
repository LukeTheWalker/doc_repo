---
title: "Kinetic Runaway Electrons"
nav_order: 7
parent: "Kinetic Particle Module"
layout: default
render_with_liquid: false
---

# Runaway Electrons
For getting started with REs, refer to [run jorek with runaway electrons](./)
# Coupling Scheme 
The coupling scheme used in JOREK is a pressure coupling scheme. However, the current arising from runaways is also needed for this scheme. There are therefore 3 coupling parameters: the parallel and perpendicular RE pressure, and the RE current.

$$
\mathbf{J}_{\text{r}} = q\int \mathbf{v}f_{\text{r}} d^3\mathbf{v}
$$

$$
\mathcal{P}_{\text{r},\perp} = \frac{m}{2}\int \gamma_{\text{L}}v^2_{\perp}f_{\text{r}}d^3\mathbf{v}
$$

$$
\mathcal{P}_{\text{r},\parallel} = m \int \gamma_{\text{L}}v^2_{\parallel}f_{\text{r}}d^3\mathbf{v}
$$

The subscript r refers to REs, $$q$$ is the electron charge, $m$ the electron mass, $\mathbf{v}$ the electron velocity, $f_{\text{r}}$ the RE distribution function, $v_{\perp}$ and $v_{\parallel}$ the perpendicular and parallel components of electron velocity respectively, and $\gamma_{\text{L}}$ is the Lorentz factor. In simulations, these quantities are calculated, then projected onto the JOREK FE grid for use in relevant MHD equations. The influence of RE's in the MHD equations appear in the momentum equation and in the current ($\mathbf{J}\rightarrow(\mathbf{J}-\mathbf{J}_{\text{r}})$, where $\mathbf{J}$ refers to the bulk MHD current). The momentum equation is modified as follows :

$$
\rho\left(\frac{\partial \mathbf{V}}{\partial t} + \mathbf{V}\cdot\nabla\mathbf{V}\right) = -\nabla p + \mathbf{J}\times\mathbf{B} -\left(\mathcal{P}_{\text{r},\parallel}-\mathcal{P}_{\text{r},\perp} \right)\boldsymbol{\kappa} - \nabla\mathcal{P}_{\text{r},\perp} + \nabla \cdot \boldsymbol{\tau}
$$

Note that in this equation, $\mathbf{J}$ is not including the RE current. This is because the pressure related terms are derived from $\mathbf{J}_{\text{r}}\times\mathbf{B}$. For more details, see the papers below.

The derivation of the RE coupling scheme can be found in *V. Bandaru et al. Phys. Plasmas 2023* (https://doi.org/10.1063/5.0165240).

The implementation of the model in JOREK, along with simulations of a RE beam termination in JET can be found in *H. Bergström et al. Plasma Phys. Control. Fusion 2025* (https://doi.org/10.1088/1361-6587/adaee7) 

# Non kinetic_main implementation 
There are several other RE related physics (such as radiation forces, and collisions) that are implemented in JOREK, but not yet in the kinetic_main. See [particles_runaways](./runaway_electron_pushers.md) and the example executables mentioned within for more details. Note that care should be taken when using the example executables (especially if in the kinetic_develop branch) as some functionality may be incompatible with the newer kinetic_main framework.
