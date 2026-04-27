---
title: "Stellarator Reduced MHD"
nav_order: 3
parent: "Base Fluid Models"
grand_parent: "Physics Models"
layout: default
render_with_liquid: false
---

# The Stellarator Reduced MHD Model

The JOREK stellarator model (reduced MHD) features two distinct models:

1. **Model 180** does not evolve the plasma in time but only calculates the **initial conditions** from VMEC/GVEC.
2. **Model 183** actually **evolves the plasma in time** (keeping the same hard-coded compiling parameters as model 180).

The models include some hard-coded switches, such as the inclusion of the parallel velocity $v_{\parallel}$.

A detailed description of the original JOREK stellarator model implementations can be found in the following literature:

1. N. Nikulsin. [Models and methods for nonlinear magnetohydrodynamic simulations of stellarators](https://mediatum.ub.tum.de/?id=1624218) (2021), PhD thesis, TUM.
2. R. Ramasamy [Equilibrium and initial value problem simulation studies of nonlinear magnetohydrodynamics in stellarators](https://mediatum.ub.tum.de/?id=1686004) (2022), PhD thesis, TUM. Here, particulary Ch. 7 is important. 
3. N. Nikulsin et al. [JOREK3D: An extension of the JOREK nonlinear MHD code to stellarators](https://doi.org/10.1063/5.0087104), Physics of Plasmas 29.6 (2022). 
4. R. Ramasamy et al. [Nonlinear MHD modeling of soft beta limits in W7-AS](https://doi.org/10.1088/1741-4326/ad56a1), Nucl. Fusion 64 086030 (2024).

## The GVEC import

*TO DO*

## The stellarator model equations 

*TO DO*