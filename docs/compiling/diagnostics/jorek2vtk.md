---
title: "jorek2vtk"
nav_order: 33
render_with_liquid: false
parent: "General"
---

This program converts a JOREK restart file to vtk format. Usage:
   ./jorek2vtk < input
where `input` is the JOREK namelist input file.

If a file called `vtk.nml` exists, it will be used to set some parameters of the vtk export. An annotated example of `vtk.nml` is given here

<code fortran vtk.nml>
&vtk_params
  nsub                   = 5       ! Number of subdivisions of cubic finite elements into linear pieces
  i_tor                  = -1      ! If i_tor > 0, only this mode will be included in the vtk file...
  i_plane                = 1       ! ... otherwise, all modes are summed up at toroidal plane i_plane
  without_n0_mode        = .false. ! If true, do not include the n=0 mode (i_tor=1)
  SI_units               = .false. ! when true, write variables in SI units
  include_fluxes         = .false. ! include energy and density fluxes (or not)
  include_neo            = .false. ! include neoclassical and more terms (or not)
  include_magnetic_field = .false. ! include vector of magnetic field (or not)
  include_velocity_field = .false. ! include vector of velocity field (or not)
  include_bootstrap      = .false. ! include bootstrap current and averaged current
  include_psi_norm       = .false. ! include normalized flux
  include_Jpol           = .false. ! include poloidal currents
/
</code>

# jorek2vtk_3d

The program **jorek2vtk_3d** allows to convert the file `jorek_restart.rst` into a three-dimensional .vtk file that can be plotted, using e.g. Visit or Paraview.
  jorek2vtk_3d < input

If present, a `vtk.nml` file is read which needs to look different to the one used by `jorek2vtk`:

<code fortran vtk.nml>
&vtk_params
  nsub                   = 5       ! Number of subdivisions of cubic finite elements into linear pieces
  without_n0_mode        = .false. ! If true, do not include the n=0 mode (i_tor=1)
  n_toroidal             = 200     ! Write out data at this number of toroidal positions
/
</code>

# convert2vtk.sh

If a larger number of restart files needs to be converted, the script convert2vtk.sh might be helpful. It allows to convert a certain range of restart files (option `-only min-max`). The script creates the `vtk.nml` file for you automatically in the background and also allows to convert several restart files in parallel.

It is possible to
- Set the parameters `nsub,i_tor`, and `i_plane` directly via command-line options `-nsub`,`-i_tor` and `-i_plane`.
- or to create the vtk.nml file manually (if the options `-nsub`,`-i_tor`, or `-i_plane` are provided the manually created vtk.nml file will be ignored)
- Option `-j 8` allows to run in parallel using eight threads
- **Run convert2vtk.sh -h for detailed information**

Some examples:
- Conversion with default parameters, using the jorek2vtk program, put vtk-files into folder `vtk_iplane1/`

    convert2vtk.sh jorek2vtk input

- Conversion for different toroidal planes, put results into folder `vtk_iplane2/...`

    convert2vtk.sh -i_plane 2-7 jorek2vtk input

- Conversion of the restart files for timesteps 280 and 300 to 320, include only the $n\neq0$ toroidal modes, put the results into folder `vtk_no0_iplane1/...`

    convert2vtk.sh -no0 -only 280,300-320 jorek2vtk input

- Conversion with default parameters to 3d vtk files, output in folder `vtk3d/`

    convert2vtk.sh jorek2vtk_3d input

Run the script with option "`-h`" for usage information.
