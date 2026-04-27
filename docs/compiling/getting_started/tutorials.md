---
title: "Tutorials"
nav_order: 1
parent: "Getting Started"
grand_parent: "Compiling and Running"
layout: default
render_with_liquid: false
---

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

## Configuring and compiling JOREK

In order to compile JOREK, first of all you need to prepare the `Makefile.inc` configuration file for compiling JOREK. This file contains the hard-coded parameters and needs to be adapted for the specific machine were the code is going to be run.

The `Makefile.inc` file needs is placed into the main folder of the JOREK repository you have cloned (where you also find the `jorek2_main.f90` file). You can have a look in the `Make.in` subfolder to see if there is a `Makefile.inc` file already setup for your specific machine, and copy it into the `Makefile.inc` file in the main folder.

The most important **hard-coded parameters** that need to be setup in the `Makefile.inc` file are:

| Name     | Description   | Reasonable values |
|----------|---------------|-------------------|
| `model`  | physics model | 600, 710          |
| `n_tor ` | number of toroidal harmonics (counting sine and cosine separately!) | 1, 3, 5, 7, 9, …         |
| `n_period ` | toroidal periodicity | 1, 2, 3, 4, …         |
| `n_plane ` | number of toroidal planes for real-space representation | at leat `2*(n_tor-1)`       |
