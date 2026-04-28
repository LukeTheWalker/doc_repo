---
title: "Jorek2_connection2"
nav_order: 22
render_with_liquid: false
parent: "General"
---

## Jorek2_connection2

This diagnostic produces a poincare plot of the magnetic field geometry. Run it as
   jorek2_connection2 < intear

It uses the file jorek_restart.rst to load the simulation state.
Output is generated in the files 
- connection_new.vtk contains the poincare plot
- strikes_coordinates.txt contains the coordinates where a fieldline strikes the wall
- strikes_values.txt contains the corresponding values of physical parameters
- strikes.vtk is the combination of the two above

### Program settings
If a file connecvtk.nml exists that is read in to set the following parameters:
   &connecvtk_params
     psi_theta = .true. ! Set to true to look in the psi-theta coordinate system, false for RZ
     n_turns = 100 ! Number of toroidal turns to follow a fieldline
     n_phi = 200 ! Number of steps per toroidal turn
     ns = 1 ! Number of starting points within one element
     nt = 1 ! Number of starting points within one element
     element_start_percent = 0.25 ! Skip the inner 25% of elements
   /

### Running in parallel
This tool can take a long time, so it is convenient to run this in parallel. Here is a qsub example
  #!/bin/sh
  #PBS -N connection2
  #PBS -V
  #PBS -l walltime="1:59:00"
  #PBS -l nodes=1:ppn=12
  #PBS -o connection.log
  #PBS -e connection.err
  mpiexec -verbose -np 12 jorek2_connection2 < intear
