---
title: "Diagnostics jorek2vtk_GaussVortTerms"
nav_order: 34
render_with_liquid: false
parent: "General"
---

This diagnostic calculates the different terms of the vorticity equation integrated in the Gaussian points and creates a VTK file where the different terms can be visualize in the poloidal plane. Also it calculates the volume or surface average of this terms. It can be applied to several time steps and therefore it provides the evolution of the different vorticity terms as a function of time. 

In the following we give the details about the compilation, the execution and the output files where the vorticity terms are stored. 

## Compilation

   make jorek2vtk_GaussVortTerms
 
The executable **jorek2vtk_GaussVortTerms** is created.

## Input files

The executable needs the following files:

- jorek_restart.rst (main jorek calculation data)

- the INPUT file used for the main jorek calculation

- **(OPTIONAL)** vtk_GaussVortTerms.nml (in this file: if **n_plane_local = n_plane** -> volume averaged calculation, if **n_plane_local = 1** -> surface averaged calculation; by **DEFAULT**: **n_plane_local = n_plane**)

## Execute

To execute for a **single time step** (for the current jorek_restart.rst):

   ./jorek2vtk_GaussVortTerms < INPUT_file

To run for **several time steps** use the bash script: **run_vtk_GaussTerms.sh**

**First check** the file **run_vtk_GaussTerms.sh** and **change** the INPUT file name on line 42. If you want to execute from the iteration 1000 to 3000 by steps of 20, run:

   ./run_vtk_GaussTerms.sh 1000 3000 20
 
## Output files

 Files created after the run (FOR A SINGLE TIME STEP):
- **Average_Terms_Voriticity_Gauss.dat** (Volume/surface averaged terms of the vorticity equation)

- **jorek_tmp.vtk**                      (vtk file, to be read with paraview or other)

- **Diff_Vort_Terms_in_Element.dat**     (Value of the different vorticity terms for all the elements calculated in   weak form WITH integration by parts AND noted with "_2" at the end if calculated WITHOUT integration by parts) 

 Files created after the run (FOR MULTIPLE TIME STEPS, using the script run_vtk_GaussTerms.sh):

- **Average_Terms_Voriticity_Gauss.dat**    (Volume/surface averaged terms of the vorticity equation)

- **Average_Terms_Voriticity_Gauss_IT.dat** (Volume/surface averaged terms of the vorticity equation **at different times/ITERATIONS**)

- **jorekGaussXXXXX.vtk**                   (vtk files at ITERATION XXXXX, to be read with paraview or other)

- **Diff_Vort_Terms_in_Element.dat**        (Value of the different vorticity terms for all the elements calculated in weak form WITH integration by parts and noted with "_2" at the end if calculated WITHOUT integration by parts, **JUST FOR THE LAST ITERATION CONSIDERED**)
