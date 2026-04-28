---
title: "Known issues"
nav_order: 7
parent: "Kinetic Particle Module"
layout: default
render_with_liquid: false
---

# Known issues regarding simulations with kinetic particles
  * Segmentation fault/memory error: private arrays in OpenMP parallel regions are stored on the stack, we can easily run into memory issues if we use many particles, have a fine grid and/or use large ntor. Try increasing the stack size by adding the following to your jobscript:
    ```
    ulimit -s unlimited
    export OMP_STACKSIZE="500M"
    ```
    The exact stack size changes from case to case, here we set it to 500 Mb, try out a few values.

    If this doesn't help and you still get segmentation faults, try removing feedback_rhs from the reduction clause in the particle evolution OMP do loop, declare it shared and perform atomic updates anytime feedback_rhs is updated, such as:
    ```
    !$omp atomic update
    feedback_rhs() = ...
    ```
  * `particles` in `!$omp shared()` lists can cause issues with certain compilers. To fix, `sim` should be in the shared list and particles should not. 
  * Memory leak. If your simulation stops after multiple hours without apparent reason, without a helpful error message in the error file, this might be caused by a memory leak. (On ITER SDCC with intel compilers the message for instance only says `srun: error: 98dci4-clu-3098: task 6: Killed`. This usually happens when something is done with the FE matrix like a projection or factorisation, because that is the moment a lot of data is used). Please discuss this so that we can try to find the origin and solve it for everyone. 
  * Computational speed: it seems that unused particles can still eat up significant computational time when n_particles << particles in use (especially when the greatest common divisor is small (e.g. gcd=1), see [kinetic timestepping](./timestepping.md)), so try to avoid unnecessarily large part_group_configs(i)%n_particles
