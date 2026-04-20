---
title: "JOREK Wiki"
nav_order: 1
nav_exclude: true
layout: default
render_with_liquid: false
---

- **[JOREK Website](https://www.jorek.eu)** → [Send an e-mail](mailto:mhoelzl@ipp.mpg.de) if something is missing \| [Add to the gallery](https://www.jorek.eu)
- **[Information for New JOREK Users](docs/jorek_access.md)** \| **[Code License](docs/code_license.md)**
- **[Publication Rules](docs/publication_rules.md)** \| **[JOREK Logo](docs/jorek_logo.md)** \| **[jorek-preprint@jorek.eu](mailto:jorek-preprint@jorek.eu)**
- **[Frequently Asked Questions (FAQ)](docs/faq.md)**

### Compiling and Running

- **[Getting started](docs/learn_jorek.md)**
  - [Tutorials](docs/tutorials.md)
  - [Compile](docs/compiling.md) \| [Hard-Coded Parameters](docs/hard-coded_parameters.md) \| [Preprocessor Flags](docs/preprocessor.md)
  - [Run](docs/running.md) \| [Leonardo-CPU](docs/leonardo-cpu.md) \| [Pitagora-CPU](docs/pitagora-cpu.md) \| [Pitagora-GPU](docs/pitagora-gpu.md) \| [IPP Garching](docs/run_at_ipp_garching.md) \| [ITER Cluster](docs/iter_cluster.md) \| [EUROfusion Gateway](docs/eurofusion_gateway.md) \| [TGCC-CEA](docs/tgcc-cea.md) \| [MacOS](docs/macos.md)
- **[List of Input Parameters](docs/input.md)**
- **[Diagnostics and Scripts](docs/diagnostics.md)**
  - [JOREK-IMAS](docs/jorek-imas.md)

### Code Development

- **[Development Workflow](docs/develop.md)**
- **[Regression Tests](docs/nrt.md)**

### Physics Models

- **[Notation Conventions](docs/notation.md)**
- **[Normalization](docs/normalization.md)**
- **[Vector Identities](docs/vector-identities.md)**
- **[Coordinate Systems](docs/coordinates.md)**
- **[Base Fluid Models](docs/base_fluid_models.md)**
  - [Tokamak Reduced MHD](docs/reduced_mhd.md)
  - [Tokamak Full MHD](docs/full_mhd.md)
  - [Stellarator Reduced MHD](docs/jorek3d.md)
- **[Kinetic Particle Module](docs/particles.md)**
- **[Model Extensions](docs/model_extensions.md)**
  - [Free Boundary Extension (STARWALL, CARIDDI)](docs/freebound.md)
  - Impurities: [fluid model](docs/impurities_fluid.md) \| [marker model](docs/impurities_marker.md) \| [kinetic model](docs/impurities_kinetic.md)
    - [ADAS Atomic Data](docs/adas.md)
  - Neutrals: [fluid model](docs/neutrals_fluid.md) \| [kinetic model](docs/neutrals_kinetic.md)
  - REs: [fluid model](docs/runaway_fluid.md) \| [kinetic model](docs/runaway_kinetic.md)

### Numerics and Tools

- [Spatial Discretization](docs/spatial-discretization.md) \| [Grids](docs/grids.md)
- [Time Integration](docs/time-integration.md)
- [Element Matrix FFT](docs/element_matrix_fft.md)
- [Solver and Preconditioner](docs/solver.md)
- [Random-Number Generators](docs/rngs.md)
- [HDF5 Tools](docs/hdf5tools.md)

### Howto...

- Get started with **[JOREK](docs/running_jorek_for_the_first_time.md)**, **[JOREK-STARWALL](docs/running_jorek-starwall_for_the_first_time.md)**, **[JOREK-CARIDDI](docs/running_jorek-cariddi_for_the_first_time.md)** and **[JOREK Diagnostics](docs/introduction_to_jorek_diagnostics.md)**
- Set up a **[JOREK simulation grid](docs/wallgrid_tutorial.md)**
- Convert EFIT equilibrium data into JOREK input with **[eqdsk2jorek](docs/eqdsk2jorek.md)**
- Get **[D_perp and ZK_perp for stationary profiles](docs/diffusion_coef.md)**
- Check **[energy conservation](docs/energy_conservation.md)**
- Run with **[diamagnetic drift](docs/diamag.md)** and **[neoclassical effects](docs/neo.md)** and **[include diamagnetic drift in the viscosity term](docs/wdia.md)**
- Run with **[Taylor-Galerkin Stabilization](docs/tgnum.md)** and **[correct negative densities / temperatures](docs/corr_neg.md)** (workaround)
- Run with **[RMPs](docs/rmp.md)** (old boundary conditions, without STARWALL)
- Calculate **B** outside and inside the JOREK grid (**[jorek2_fields_xyz](docs/jorek2_fields_xyz.md)**)
- Calculate the **[total wall forces](docs/jorek2_wall_forces.md)** (needs JOREK-STARWALL)
- Run including **[Ohmic heating](docs/ohmic_heating.md)**
- Run with **[Sheath heat-flux BC](docs/sheath_heatflux_bc.md)**
- Run an **[MGI simulation](docs/mgi_tutorial.md)** and an **[SPI simulation](docs/spi_tutorial.md)**
- Set up **[Spitzer resistivity](docs/spitzer_resistivity.md)** and anisotropic heat diffusion
- Create an **[X-point plasma from a limiter plasma](docs/x-point_from_limiter.md)**
- Run with **[mode groups in preconditioner](docs/mode_groups.md)**
- **[Choose boundary conditions](docs/choose_boundary_conditions.md)**
- **[How to use shock capturing features](docs/shock_capturing.md)**
- **[Run stellarator simulations](docs/stellarator_setup.md)**
- **[Plot equation terms in VTK](docs/plot_rhs_terms.md)**
- **[Use phase space projections](docs/particles_phase_space.md)**
- **[Assess particle wall loads with the particle tracker](docs/particles_wall_load.md)**
- **[Assess fluid loads on 3D walls with field line tracing](docs/fluid_wall_load.md)**
- **[Generate Poincaré plots with the particle tracker](docs/particles_poincare.md)**
- **[Runaway electron physics in the particle tracker](docs/particles_runaways.md)**
- **[Use the controller module](docs/using_controller_module.md)**
- Run with **[Non-linear time-stepping (Newton iterations)](docs/inexact_newton_solver.md)**
- **[Reconstruct how namelist input parameters were changed](docs/nml2h5.md)**
- **[Show time in Paraview plots](docs/showing_time_in_paraview.md)**
- **[Variable MultiScale (VMS) Stabilization in full MHD model 750](docs/vms.md)**
- Compile and run the **[Particle Fast Camera](docs/particle_fast_camera.md)**
- **[Compress the response matrices](docs/compress_response_matrices.md)** in the free-boundary and resistive wall extension
- **[Run the stellarator model with the divertor region](docs/stellarator_with_divertor.md)**
- **[Run with kinetic neutrals and impurities](docs/ncs_ics_tutorial.md)**
- Run particle simulations with **[neutral neutral collisions](docs/neutral_neutral_collisions.md)**
- Activate the **[inward pinch term in the density equation](docs/inward_pinch_term.md)**
- **[Computing parallel electric field $E_{\\vert\\vert}$ in JOREK](docs/efield_in_jorek.md)**
- **[Helicity conservation](docs/helicity_conservation.md)**

### Machines, Coordinates, Geometry, Synthetic Diagnostics, Reference Scenarios

- **[ITER](docs/iter.md)**
- **[JET](docs/jet.md)**
- **[ASDEX Upgrade](docs/asdex_upgrade.md)**
