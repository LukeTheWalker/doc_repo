---
title: "Impurities — Marker Model"
nav_order: 2
parent: "Impurities"
grand_parent: "Model Extensions"
layout: default
render_with_liquid: false
---

## Using marker particles for mixed impurity SPI modelling

This page illustrates some basic steps and tips on using the collisional-radiative non-equilibrium impurity treatment via marker particles for mixed pellet simulations. Implementation of the method was published in [D Hu et al 2021 Plasma Phys. Control. Fusion 63 125003](https://iopscience.iop.org/article/10.1088/1741-4326/acc8e9/meta).

### 1. Code version (to be updated)

As of 2024.11, we recommend using model 600 of branch [IMAS-4606](https://git.iter.org/projects/STAB/repos/jorek/commits?until=refs%2Fheads%2FIMAS-4606-add-non-equilibrium-radiation-terms-in-model600-mod_elt_matrix_fft.f90-but-based-on-the&merges=include#), whereas model 502 of branch [feature/SPImodel502_w_marker](https://git.iter.org/projects/STAB/repos/jorek/commits?until=refs%2Fheads%2Ffeature%2FSPImodel502_w_marker&merges=include#) has also been largely used.

**Note:** The option of `with_impurities=.t.` and `with_neutrals=.t.` of model 600 of the IMAS-4606 branch is not supposed to be used yet - debugging is still on-going. See details in this [pull request](https://git.iter.org/projects/STAB/repos/jorek/pull-requests/891/overview).

Note that the option `with_vpar` must be activated.  

### 2. Compiling (two steps)

- Compile JOREK as one usually does for simulations without marker particles.
- Compile markers: `marker_spi_source.f90` stored in `/particles/examples`. Note that `USE -MUMPS` should be set to 1 in the Makefile.inc before compilation as projecting markers requires MUMPS. (Don't confuse this with those in the JOREK namelist though: `use_mumps`, `use_pastix` and `use_strumpack` in the JOREK input file refer to the solver used for the fluid time stepping, nothing to do with the marker particle setup).

### 3. Running simulations

Note that `EXPORT OMP_STACKSIZE` would need to be set to a larger value (for example 50M) for using with markers without running into memory issues (when restarting). 

**WARNING**: There are intel compiler versions (e.g. 2021.10.0) that have a bug that blocks marker simulations! This comes due to the use of select types inside omp loops. This is supposed to have been fixed in newer compiler versions...

#### New parameters in the JOREK namelist:

- `use_marker`: to use marker particles or not
- `restart_particles`: similar to `restart`, but for markers 
- `n_particles`: (maximum) number of marker particles used in the simulation. As mentioned in Di's PPCF paper above, a good rule of thumb is that one marker particle represents 10^{14} real particles.
- `tstep_particles`: time step (in SI unit) for pushing marker particles, this should be sufficiently smaller than the fluid time step, see Di's paper.
- Filters need to be applied to smooth out the particle projection and ensure numerical stability. A good start could be:

    - filter_perp = 1.d-4
    - filter_hyper = 1.d-8
    - filter_par = 5.d-1
    - filter_perp_n0 = 1.d-4
    - filter_hyper_n0 = 1.d-8
    - filter_par_n0 = 5.d-1


- `diff_diffusive_flux`: if set to `.true.`, this option turns on an additional term in the marker particle pusher that is proportional to the gradient of rho_imp, therefore it mimics the density diffusion and helps the consistent evolution of aux05 and rho_imp.

#### Steps to run a simulation with marker particles:

- Deactivate the above parameters and run a standard JOREK simulation without markers for some (say ~50) time steps (use your standard `srun jorek_modelxxx` in the jobscript)
- Restart the simulation with `use_marker = .t.` but `restart_particles = .f.` as there are no particles in the simulation yet. Don't forget to use `srun marker_spi_source` in the jobscript. 
- After the defined run time, restart the simulation again but this time with `restart_particles = .t.` as well to be able to load the stored particle information. Don't forget to copy the latest particle restart file into `part_restart.h5` (similar to the jorek restart file)

### 4. Diagnostics

Most of the standard JOREK diagnostics should be applicable to the marker simulations when using the branch [IMAS-4606](https://git.iter.org/projects/STAB/repos/jorek/commits?until=refs%2Fheads%2FIMAS-4606-add-non-equilibrium-radiation-terms-in-model600-mod_elt_matrix_fft.f90-but-based-on-the&merges=include#). 

Some tips:
- For `jorek2vtk` or `convert2vtk.sh`, one needs to include the option `-proj projections` when using the command. Extra fields like `aux01` and `aux05` will be generated in the obtained vtk files, for example when viewing using Paraview. These correspond to the ionization power density (`aux01`), radiation power density (`aux02`), effective charge of impurities (`aux03`), mean charge of impurity species (`aux04`) and impurity number density (`aux05`), respectively, as described in Di's paper. 
- Sanity check to make sure the parameter setup is reasonable: compare the projections and the fluid fields, which should have very similar structures. Useful Python scripts by Weikang (to be added).
- Additional sanity check: run the marker program with the hardcoded `CE_marker` flag set to true. In this way the CE approximation is used for markers instead of the CR treatment. The result should be comparable with fluid simulations using the CE approximation, as discussed in the paper by Di.
- The `aux01`-`aux05` variables are also available as expressions for `jorek2_postproc`.
- The aux variables must be multiplied by normalization factors to be converted to physical units (for example, with the purpose of the quantitative comparison with their fluid counterparts). The normalization factors are printed at the beginning of the log from `marker_spi_source`. In particular, the normalization factor for the radiation power density (`aux02`) is `E_norm / t_norm`, and the normalization factor for the impurity number density (`aux05`) is `N_norm`.
*This page is a stub — content to be added.*
