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
- **[Contributing to the Docs](docs/contributing.md)**

### Compiling and Running

- **[Getting started](docs/compiling/getting_started/learn_jorek.md)**
  - [Tutorials](docs/compiling/getting_started/tutorials.md)
  - [Compile](docs/compiling/getting_started/compiling.md) \| [Hard-Coded Parameters](docs/compiling/getting_started/hard-coded_parameters.md) \| [Preprocessor Flags](docs/compiling/getting_started/preprocessor.md)
  - [Run](docs/compiling/getting_started/running.md) \| [Leonardo-CPU](docs/compiling/getting_started/leonardo-cpu.md) \| [Pitagora-CPU](docs/compiling/getting_started/pitagora-cpu.md) \| [Pitagora-GPU](docs/compiling/getting_started/pitagora-gpu.md) \| [IPP Garching](docs/compiling/getting_started/run_at_ipp_garching.md) \| [ITER Cluster](docs/compiling/getting_started/iter_cluster.md) \| [EUROfusion Gateway](docs/compiling/getting_started/eurofusion_gateway.md) \| [TGCC-CEA](docs/compiling/getting_started/tgcc-cea.md) \| [MacOS](docs/compiling/getting_started/macos.md)
- **[List of Input Parameters](docs/compiling/input.md)**
- **[Diagnostics and Scripts](docs/compiling/diagnostics.md)**
  - [JOREK-IMAS](docs/compiling/diagnostics/jorek-imas.md)

### Code Development

- **[Development Workflow](docs/code_development/develop.md)**
- **[Regression Tests](docs/code_development/nrt.md)**

### Physics Models

- **[Notation Conventions](docs/physics/notation.md)**
- **[Normalization](docs/physics/normalization.md)**
- **[Vector Identities](docs/physics/vector-identities.md)**
- **[Coordinate Systems](docs/physics/coordinates.md)**
- **[Base Fluid Models](docs/physics/base_fluid_models/base_fluid_models.md)**
  - [Tokamak Reduced MHD](docs/physics/base_fluid_models/reduced_mhd.md)
  - [Tokamak Full MHD](docs/physics/base_fluid_models/full_mhd.md)
  - [Stellarator Reduced MHD](docs/physics/base_fluid_models/jorek3d.md)
- **[Kinetic Particle Module](docs/physics/particles.md)**
- **[Model Extensions](docs/physics/model_extensions/model_extensions.md)**
  - [Free Boundary Extension (STARWALL, CARIDDI)](docs/physics/model_extensions/freebound.md)
  - Impurities: [fluid model](docs/physics/model_extensions/impurities_fluid.md) \| [marker model](docs/physics/model_extensions/impurities_marker.md) \| [kinetic model](docs/physics/model_extensions/impurities_kinetic.md)
    - [ADAS Atomic Data](docs/physics/model_extensions/adas.md)
  - Neutrals: [fluid model](docs/physics/model_extensions/neutrals_fluid.md) \| [kinetic model](docs/physics/model_extensions/neutrals_kinetic.md)
  - REs: [fluid model](docs/physics/model_extensions/runaway_fluid.md) \| [kinetic model](docs/physics/model_extensions/runaway_kinetic.md)

### Numerics and Tools

- [Spatial Discretization](docs/numerics/spatial-discretization.md) \| [Grids](docs/numerics/grids.md)
- [Time Integration](docs/numerics/time-integration.md)
- [Element Matrix FFT](docs/numerics/element_matrix_fft.md)
- [Solver and Preconditioner](docs/numerics/solver.md) \| [Sparse Matrix Format](docs/numerics/sparse-matrix.md) 
- [Random-Number Generators](docs/numerics/rngs.md)
- [HDF5 Tools](docs/numerics/hdf5tools.md)

### Howto...

- Get started with **[JOREK](docs/howto/running_jorek_for_the_first_time.md)**, **[JOREK-STARWALL](docs/howto/running_jorek-starwall_for_the_first_time.md)**, **[JOREK-CARIDDI](docs/howto/running_jorek-cariddi_for_the_first_time.md)** and **[JOREK Diagnostics](docs/howto/introduction_to_jorek_diagnostics.md)**
- Set up a **[JOREK simulation grid](docs/howto/wallgrid_tutorial.md)**
- Convert EFIT equilibrium data into JOREK input with **[eqdsk2jorek](docs/howto/eqdsk2jorek.md)**
- Get **[D_perp and ZK_perp for stationary profiles](docs/howto/diffusion_coef.md)**
- Check **[energy conservation](docs/howto/energy_conservation.md)**
- Run with **[diamagnetic drift](docs/howto/diamag.md)** and **[neoclassical effects](docs/howto/neo.md)** and **[include diamagnetic drift in the viscosity term](docs/howto/wdia.md)**
- Run with **[Taylor-Galerkin Stabilization](docs/howto/tgnum.md)** and **[correct negative densities / temperatures](docs/howto/corr_neg.md)** (workaround)
- Run with **[RMPs](docs/howto/rmp.md)** (old boundary conditions, without STARWALL)
- Calculate **B** outside and inside the JOREK grid (**[jorek2_fields_xyz](docs/howto/jorek2_fields_xyz.md)**)
- Calculate the **[total wall forces](docs/howto/jorek2_wall_forces.md)** (needs JOREK-STARWALL)
- Run including **[Ohmic heating](docs/howto/ohmic_heating.md)**
- Run with **[Sheath heat-flux BC](docs/howto/sheath_heatflux_bc.md)**
- Run an **[MGI simulation](docs/howto/mgi_tutorial.md)** and an **[SPI simulation](docs/howto/spi_tutorial.md)**
- Set up **[Spitzer resistivity](docs/howto/spitzer_resistivity.md)** and anisotropic heat diffusion
- Create an **[X-point plasma from a limiter plasma](docs/howto/x-point_from_limiter.md)**
- Run with **[mode groups in preconditioner](docs/howto/mode_groups.md)**
- **[Choose boundary conditions](docs/howto/choose_boundary_conditions.md)**
- **[How to use shock capturing features](docs/howto/shock_capturing.md)**
- **[Run stellarator simulations](docs/howto/stellarator_setup.md)**
- **[Plot equation terms in VTK](docs/howto/plot_rhs_terms.md)**
- **[Use phase space projections](docs/howto/particles_phase_space.md)**
- **[Assess particle wall loads with the particle tracker](docs/howto/particles_wall_load.md)**
- **[Assess fluid loads on 3D walls with field line tracing](docs/howto/fluid_wall_load.md)**
- **[Generate Poincaré plots with the particle tracker](docs/howto/particles_poincare.md)**
- **[Runaway electron physics in the particle tracker](docs/howto/particles_runaways.md)**
- **[Use the controller module](docs/howto/using_controller_module.md)**
- Run with **[Non-linear time-stepping (Newton iterations)](docs/howto/inexact_newton_solver.md)**
- **[Reconstruct how namelist input parameters were changed](docs/howto/nml2h5.md)**
- **[Show time in Paraview plots](docs/howto/showing_time_in_paraview.md)**
- **[Variable MultiScale (VMS) Stabilization in full MHD model 750](docs/howto/vms.md)**
- Compile and run the **[Particle Fast Camera](docs/howto/particle_fast_camera.md)**
- **[Compress the response matrices](docs/howto/compress_response_matrices.md)** in the free-boundary and resistive wall extension
- **[Run the stellarator model with the divertor region](docs/howto/stellarator_with_divertor.md)**
- **[Run with kinetic neutrals and impurities](docs/howto/ncs_ics_tutorial.md)**
- Run particle simulations with **[neutral neutral collisions](docs/howto/neutral_neutral_collisions.md)**
- Activate the **[inward pinch term in the density equation](docs/howto/inward_pinch_term.md)**
- **[Computing parallel electric field $E_{\\vert\\vert}$ in JOREK](docs/howto/efield_in_jorek.md)**
- **[Helicity conservation](docs/howto/helicity_conservation.md)**

### Machines, Coordinates, Geometry, Synthetic Diagnostics, Reference Scenarios

- **[ITER](docs/machines/iter.md)**
- **[JET](docs/machines/jet.md)**
- **[ASDEX Upgrade](docs/machines/asdex_upgrade.md)**
