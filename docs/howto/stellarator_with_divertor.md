---
title: "Run Stellarator Model with Divertor Region"
nav_order: 2
parent: "Stellarator"
grand_parent: "Howto"
layout: default
render_with_liquid: false
---

# Running Stellarator with Divertor Region

Unlike tokamak models, JOREK does not have a built-in equilibrium solver for stellarator but uses an ideal MHD equilibrium solver from GVEC, assuming nested flux surfaces. Historically, this meant that the simulation domain has been limited to the Last Closed Flux Surface (LCFS). To go beyond the LCFS, one typically either needs:

1. Dommaschk potentials 
2. Vacuum field $\nabla \chi$ from coils

For further conceptual details, see the [stellarator](stellarator.md) page. This page illustrates the minimal building blocks to get started with creating and running simulations with stellarator grids with divertors. 

*TO DO: write about USE_EXT_FIELD* flag to load vacuum field.

To realistically capture divertor physics, **sheath boundary conditions** are necessary to capture the dynamics close to the first wall when open magnetic field intersect the boundary. The well-established main physics formulae, already implemented in the JOREK tokamak model and in other divertor physics codes, state that for flux surfaces intersecting boundaries with angle $\alpha$, we have:

1. **The Bohm criterion**: $$v_{\parallel} \geq \pm c_s f(\alpha), \quad \text{where  }\alpha = \arcsin \bigg(\frac{|\hat{n} \cdot \textbf{B}|}{\textbf{B}|} \bigg), \text{  typically with smoothing  $ f(\alpha) = \tanh(\alpha/\alpha_0)$ ,   e.g. $\alpha_0 = 5$ deg}$$


2. **Particle flux** at sheath entrance: $$\Gamma_n = n \cdot v_{\parallel}$$

3. **Heat flux** (simplest case with single $T$): $$q = \gamma \cdot k T_e \Gamma_n$$

<img src="assets/stellarator_with_divertor/sheath_boundary_conditions_incidence_angle.png" alt="Alt text" width="250">



## Simplistic case: W7-A with artificial divertor

The first 

<img src="assets/stellarator_with_divertor/W7-A_divertor_illustrated.png" alt="Alt text" width="800">

