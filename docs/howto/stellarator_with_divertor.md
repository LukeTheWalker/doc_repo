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

*TO DO: briefly link to the stellarator_setup.md*, where the gvec --> gvec2jorek.dat --> jorek model 180 --> jorek000000.h5 and jorek000001.h5 (where the latter is used as jorek_restart.h5 for model 183) --> jorek model 183. 

*TO DO: write about USE_EXT_FIELD* flag to load vacuum field.

To realistically capture divertor physics, **sheath boundary conditions** (SBC) are necessary to capture the dynamics close to the first wall when open magnetic field intersect the boundary. The well-established main physics formulae, already implemented in the JOREK tokamak model and in other divertor physics codes, state that for flux surfaces intersecting boundaries with angle $\alpha$, we have:

1. **The Bohm criterion**: $$v_{\parallel} \geq \pm c_s f(\alpha), \quad \text{where  }\alpha = \arcsin \bigg(\frac{|\hat{n} \cdot \textbf{B}|}{\textbf{B}|} \bigg), \text{  typically with smoothing  $ f(\alpha) = \tanh(\alpha/\alpha_0)$ ,   e.g. $\alpha_0 = 5$ deg}$$


2. **Particle flux** at sheath entrance: $$\Gamma_n = n \cdot v_{\parallel}$$

3. **Heat flux** (simplest case with single $T$): $$q = \gamma \cdot k T_e \Gamma_n$$

More physics details on SBC and their implementation can be found in P.C Stangeby (2000), CRC Press, and M. Hoelzl et al., Nucl. Fusion 61, 065001 (2021).

<img src="assets/stellarator_with_divertor/sheath_boundary_conditions_incidence_angle.png" alt="Alt text" width="250">



## Simplistic case: W7-A with artificial divertor

The first minimum viable stellarator divertor grid example features an artificial divertor indentation in the stellarator Wendelstein 7-A:

<img src="assets/stellarator_with_divertor/W7-A_divertor_illustrated.png" alt="Alt text" width="700">

*TO DO: add actual (simple) formula describing this indentation for the (most extreme) 50 mm indentation case*

*TO do: describe very briefly and concisely how Bezier elemnents are handled, and the derivatives (where cubic splines, where PCHIP interpolation).*

*TO do: describe very briefly in some Python snippets the bare minimum and key ingredients from runs/015_bezier_surface_construction/phase15_conformal_divertor/modify_gvec2jorek_divertor.py, and which the input ingredients are (for example relating to the stellarator_setup.md*

<img src="assets//stellarator_with_divertor/boundary_toroidal_5panel_divertor_50.0mm.png" alt="Alt text" width="700">

## W7-X divertor grids

### Grid construction

#### Harmonic mapping

*To do: very concise description of harmonic mapping and why it is relevant for stellarator grids, citing Robert Babin et al 2025 Plasma Phys. Control. Fusion 67 035005*

*To do: describe the harmonic mapping part in runs/019_w7x_half_beta_island_divertor/step20_w7x_bean_scaling/extend_grid_harmonic.py*

#### Divertor moulding

*To do: describe the moulding part in runs/019_w7x_half_beta_island_divertor/step20_w7x_bean_scaling/extend_grid_harmonic.py*

<img src="assets//stellarator_with_divertor/w7x_divertor_grid_5panel.png" alt="Alt text" width="700">