---
title: "Physical Expressions Available"
nav_order: 11
render_with_liquid: false
parent: "Code Development"
---

The following physical expressions are currently available for model 303 in the [new_diag](new_diag.md) framework and in the [jorek2_postproc](jorek2_postproc.md) diagnostics. Available expressions may differ between models. The easiest for getting an up to date list is to compile `jorek2_postproc`, execute it interactively and call the command `expressions` which produces a complete list.

| Expression | Description |
| --- | --- |
| R | Cylindrical Coordinate R (== Major Radius) |
| Z | Cylindrical Coordinate Z |
| phi | Cylindrical Coordinate phi |
| theta | Poloidal Angle With Respect to Magnetic Axis |
| theta_star | Poloidal Straight Field Line Angle (for flux surfaces) |
| length | Length Along Poloidal Line (for poloidal lines) |
| r_minor | Minor Radius From A = r_minor**2 pi (for flux surfaces) |
| x | Cartesian Coordinate x |
| y | Cartesian Coordinate y |
| z | Cartesian Coordinate z (== Cylindrical Z) |
| Psi_N | Normalized Poloidal Magnetic Flux |
| xjac | 2D Jacobian in the Poloidal Plane |
| t | Simulation time |
| Psi | Poloidal Magnetic Flux |
| u | Velocity Stream Function |
| Phi | Electric Potential Phi |
| zj | Toroidal Current Density Multiplied by R |
| currdens | Physical Toroidal Current Density (== zj/R) |
| omega | Toroidal Vorticity Component |
| rho | Mass Density |
| T | Temperature (Electrons plus Ions) |
| vpar | Parallel Velocity (along magnetic field lines) |
| eta_T | Temperature Dependent Resistivity |
| visco_T | Temperature Dependent Viscosity |
| zkpar_T | Temperature Dependent Parallel Heat Diffusivity |
| dprof | Particle Diffusivity |
| zkprof | Perpendicular Heat Diffusivity |
| pres | Total Pressure |
| B_abs | Norm of the Magnetic Field Vector |
| Btor | Toroidal Magnetic Field Component |
| BR | Magnetic Field Component Along R |
| BZ | Vertical Magnetic Field Component |
| B_theta | Poloidal Magnetic Field Component |
| Er | Radial Electric Field |
| Vtheta_i | Ion Poloidal Velocity |
| Mach_par | Parallel Mach Number |
| Mach_pol | Poloidal Mach Number |
| V_sound | Sound Speed |
| V_neo | Neoclassical Velocity |
| Vperp_e | Electron Perpendicular Velocity |
| Vperp_i | Ion Perpendicular Velocity |
| V_ExB | ExB Velocity |
| Vstar_e | Electron Diamagnetic Velocity |
| Vstar_i | Ion Diamagnetic Velocity |
| ki_neo | Neoclassical Heat Diffusivity |
| mu_neo | Neoclassical Friction Coefficient |
| E_II | E_II (with 2 vertical bars) for RE acceleration |
| E_crit | E_crit for RE avalanching (Connor-Hastie) |
| E_dreicer | Electrical field for Dreicer RE primary source |
