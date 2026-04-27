---
title: "Tutorials"
nav_order: 1
parent: "Getting Started"
grand_parent: "Compiling and Running"
layout: default
render_with_liquid: false
---

*This page is a stub — content to be added.*

# Running JOREK for the first time

This tutorial will show you how to run your first small JOREK simulations. It will help you to configure and compile libraries, main code, and diagnostics, run interactively and via a batch system. You will also learn how to use first simple diagnostics. Basic Linux knowledge is required and you should have access to a cluster to run the examples yourself. Please refer to the specific documentation pages for the mostly used HPC systems.

## Preparation of the environment

On most machines, the `module` command is used to make the required software (e.g. compilers and libraries) available. Typically, JOREK is compiler with the Intel compiler and MPI/OpenMP libraries for best efficiency, but can be also compiled e.g. with the GNU compilers and libraries.

You can put the `module` commands in your `.bashrc` file in the home directory, so that the required software is loaded automatically at login. Typical `module` commands will look like this:

    module purge
    module load git
    module load intel-oneapi-mpi/
    module load intel-oneapi-compilers
    module load intel-oneapi-mkl/2024.0.0--intel-oneapi-mpi--2021.12.1
    module load hdf5/1.14.3--intel-oneapi-mpi--2021.12.1--oneapi--2024.1.0

Other useful commands: Use `module avail` to check for available modules, `module list` to see what you have already loaded, `module unload` to unload a specific module, `module purge` to unload all modules.

## Getting the JOREK code

You need to get an account on one of the platforms where the JOREK code is hosted and clone the repository of the code using git.

This is an example using the ITER platform:

     git clone ssh://git@git.iter.org/stab/jorek.git

