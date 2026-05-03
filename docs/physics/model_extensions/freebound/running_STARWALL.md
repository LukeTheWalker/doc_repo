---
title: "Running and setting up STARWALL"
nav_order: 4
parent: "Free Boundary Extension (STARWALL, CARIDDI)"
grand_parent: "Model Extensions"
layout: default
render_with_liquid: false
---

This page intends to explain how to compile, setup and run the STARWALL code for free-boundary simulations in JOREK.

## Getting the source code
Clone the code, currently at the ITER bitbucket server

```bash
git clone --branch develop ssh://git@git.iter.org/stab/starwall.git starwall/
```

## Compiling
To compile you need a FORTRAN compiler with MPI and also the [**MKL**](https://en.wikipedia.org/wiki/Math_Kernel_Library) library that includes SCaLAPACK. First you need to set up a configuration file for your machine and name it as `config.in` in the main directory. For example, for ITER, go to the STARWALL folder and do

```bash
cp configs/config.iter config.in
```
and be sure that the MKL modules are well linked

```bash
MKL_HOME=$(MKLROOT)
LAPACK_LIB = $(MKL_HOME)/lib/intel64/libmkl_sequential.a -Wl,--start-group  $(MKL_HOME)/lib/intel64/libmkl_intel_lp64.a $(MKL_HOME)/lib/intel64/libmkl_sequential.a $(MKL_HOME)/lib/intel64/libmkl_core.a $(MKL_HOME)/lib/intel64/libmkl_scalapack_lp64.a   $(MKL_HOME)/lib/intel64/libmkl_blacs_intelmpi_lp64.a    -Wl,--end-group -lpthread

LIB = $(LAPACK_LIB)
```
To compile simply do

```bash
make clean 
make
```
The executable to run is
```bash
./starwall/o_3d/STARWALL_JOREK_Linux
```

## Running

Create a run folder for STARWALL wherever you find convenient (e.g. `run_starwall`)

### Getting the boundary.txt file
1. Run JOREK with `freeboundary=.t.` in the input file. JOREK will stop and the **boundary.txt** file with the geometry of the coupling surface will appear in the folder.
2. Copy **boundary.txt** to the `run_starwall` folder.

### Create a STARWALL input file
Choose whatever name you prefer (e.g. `input_starwall`). See the following example for ITER, **the input parameters** are explained [here](#parameter-overview)
```bash
&PARAMS
  ! Calculate response matrix for:
  !   0=no wall, 1=ideal wall, 2=resistive wall
  i_response = 2,
  
  ! Number of toroidal modes
  n_harm     = 1,

  ! Toroidal mode numbers n_tor(i) for i=1...n_harm
  n_tor      = 0
  
  ! Number of toroidal grid points for real space representation
  nv         = 32,
  
  ! B_par is computed on a surface shifted by delta into the vacuum domain
  ! (numerical parameter: leave unchanged)
  delta      = 0.001,
  
  ! Number of grid points per boundary element
  n_points   = 10,
  
  ! Number of unconnected wall components
  ! (CURRENTLY UNUSED)
  nwall      = 1,
  
  ! Representation of the wall:
  !   1=Fourier series, 2=triangles, 3=triangles+index fu.
  iwall      = 1,

  ! PF coils file
  pol_coil_file  = 'polcoils_iter.nml'
    
  ! Passive components file
  diag_coil_file = 'passive_components.nml'
  
/

&PARAMS_WALL
  ! eta_thin,wall in SI units [Ohm]
  eta_thin_w = 1.33e-05
  
  ! Wall grid points in poloidal direction
  nwu        = 60,
  
  ! Wall grid points in toroidal direction
  nwv        = 60,
  
  ! Number of Fourier harmonics
  mn_w       = 8,
  
  ! Modes characterizing the wall shape (data taken from ../wall/descur/input/out_vmec_test)
  n_w  =          0,         0,         0,         0,         0,         0,         0,         0,
  m_w  =          0,         1,         2,         3,         4,         5,         6,         7,
  rc_w =  5.7387E+0, 2.8230E+0, 4.3479E-1,-1.0796E-1, 8.9448E-2, 1.2628E-2, 1.2445E-3, 2.9309E-2,
  rs_w =  0.0000E+0, 3.6590E-2, 5.1754E-2, 6.4473E-2, 5.7993E-2, 1.8204E-2,-1.4235E-2,-1.4031E-2,
  zc_w =  7.9184E-2, 3.6590E-2, 7.4851E-2, 3.4342E-2, 1.2247E-2,-1.2918E-2,-2.1155E-2,-7.0774E-3,
  zs_w =  0.0000E+0, 5.1906E+0,-2.2917E-1, 7.2744E-3,-2.3149E-2,-3.0743E-3, 1.6155E-4,-7.0349E-3,
/
```

### Submitting the job
**STARWALL is a MPI only code**, there is no OpenMP being used. Therefore, in your job file, you must set the following parameters before running
```bash
  #SBATCH --ntasks-per-node= Number of cpus per node of your machine
  #SBATCH --cpus-per-task  =1
  
  export OMP_NUM_THREADS=1
```
Then the command to run STARWALL is simply

```bash
  mpirun STARWALL_JOREK_Linux input_starwall > output_starwall
```
Depending on the size of your problem and the number of cpus that you use it may take from minutes to several hours. For ITER demanding simulations, it may take about 8 hours with 4-8 compute nodes. 

Right at the start of the run, STARWALL produces the “wall.vtk” that you can plot with visit or paraview to visualize the geometry of the wall that you have specified in the input file. You can see the output information from STARWALL in output_starwall. 

Finally, the response file should appear in your running folder

```bash
  ./starwall-response.dat
```
which you will need to copy or link to the JOREK directory.

## Parameter setup

### Parameter overview

| Input Parameter | Explanation |
|---|---|
| `n_harm` | Number of toroidal harmonics, see [Select modes and harmonics](#select-modes-and-harmonics) |
| `n_tor` | Toroidal mode numbers to be included, see [Select modes and harmonics](#select-modes-and-harmonics) |
| `nv` | Number of toroidal grid points representing the plasma in STARWALL |

Usually no need to change the following ones:

| Input Parameter | Explanation |
|---|---|
| `i_response` | 2 -- don't touch |
| `delta` | 0.001 -- don't touch |
| `n_points` | 10 -- don't touch |
| `nwall` | 1 -- don't touch for simple walls |

Additionally, for a **simple closed wall** represented by Fourier harmonics (see [Setting up a simple wall](#setting-up-a-simple-wall) for details):

| Input Parameter | Explanation |
|---|---|
| `eta_thin_w` | Thin wall resistivity, see [Wall and coil resistivities](#wall-and-coil-resistivities) |
| `nwu` | Number of poloidal points to represent the simple wall |
| `nwv` | Number of toroidal points to represent the simple wall |
| `mn_w` | Number of harmonics to describe the simple wall geometry |
| `n_w(*)` | Toroidal mode number of the harmonics describing the simple wall geometry |
| `m_w(*)` | Poloidal mode number of the harmonics describing the simple wall geometry |
| `rc_w(*)` | Cosine harmonics for R describing the simple wall geometry |
| `rs_w(*)` | Sine harmonics for R describing the simple wall geometry |
| `zc_w(*)` | Cosine harmonics for Z describing the simple wall geometry |
| `zs_w(*)` | Sine harmonics for Z describing the simple wall geometry |

Additionally when including **coils** (see [Include coils](#include-coils) for details):

| Input Parameter | Explanation |
|---|---|
| `pol_coil_file` | File name, axisymmetric coils for free boundary equilibrium, vertical feedback etc |
| `rmp_coil_file` | File name, non-axisymmetric active coils |
| `diag_coil_file` | File name, coils of arbitrary geometry used as virtual diagnostics |
| `voltage_coil_file` | File name (not working yet) |



### Setting up a simple wall

The following example sets up a wall with the geometry $R=10+1.2\cos(\theta)$ and $Z=1.2\sin(\theta)$ which is represented by 32 poloidal and 32 toroidal points (i.e., 2×32×32=2048 triangles):

```fortran
&PARAMS_WALL
  nwu        = 32,
  nwv        = 32,
  mn_w       = 2,
  eta_thin_w = 1.e-6,
  n_w(1)=0, m_w(1)=0, rc_w(1)=10.0, rs_w(1)=0., zc_w(1)=0., zs_w(1)=0.0,
  n_w(2)=0, m_w(2)=1, rc_w(2)= 1.2, rs_w(2)=0., zc_w(2)=0., zs_w(2)=1.2,
/
```

For the parameter `eta_thin_w`, refer to [How to set up wall and coil resistivities?](#how-to-set-up-wall-and-coil-resistivities).

### Select modes and harmonics

`n_harm` denotes the number of harmonics, and `n_tor` lists the corresponding toroidal mode numbers. A few examples:

| Toroidal mode numbers | `n_harm` | `n_tor` |
|---|---|---|
| 0 | 1 | 0 |
| 0,1,2 | 3 | 0,1,2 |
| 4,8 | 2 | 4,8 |

Search in the JOREK logfile for the following section which reports harmonics taken into account in the response:

```
-----------------------------------------------------------------------------
STARWALL RESPONSE INFORMATION:
-----------------------------------------------------------------------------
...
i_tor                   = 2 (n=1 cos), 3 (n=1 sin)
-----------------------------------------------------------------------------
```

**Note:**
* Modes present in JOREK, but not present in the STARWALL response will be treated with ideal wall boundary conditions.
* For modes present in STARWALL but not included in JOREK, the vacuum response will be ignored.

### How to set up wall and coil resistivities?

Wall and coil resistivities are set up **in STARWALL** as explained below. The JOREK parameter `wall_resistivity_fact` allows scaling both wall and coil resistivities at the same time.

#### Wall

The wall resistivity is set up in STARWALL by the parameter `eta_thin_w`. From the material property $\eta_{wall,SI}$ [Ω·m] and the wall thickness $d_{wall}$ [m], you can calculate the "thin wall resistivity" as:

$$\eta_{thin,SI}=\frac{\eta_{wall,SI}}{d_{wall}} \text{ [Ω]}$$

Set `eta_thin_w` to this SI value.

#### Coils

For the coils, the input parameter `resist` refers to the resistance of the coil in Ohm (if the coil has more than one turn, this value refers to all turns combined). The corresponding $\eta_{thin,norm}$ is calculated automatically from it.

### Include coils
Coils need to be added in STARWALL via additional coil files. The names of these files are specified in the main STARWALL input file via the following parameters:

| Input Parameter | Explanation |
|---|---|
| `pol_coil_file` | File name, axisymmetric coils for free boundary equilibrium, vertical feedback, etc. |
| `rmp_coil_file` | File name, non-axisymmetric active coils |
| `diag_coil_file` | File name, coils of arbitrary geometry used as virtual diagnostics |
| `voltage_coil_file` | File name (not working yet) |

Some example coil files can be found in the STARWALL repository in the folder `coil_inputs/`. Each coil file contains two sections.

**The first section** only contains general information about the coil set:

```fortran
&coil_set_nml
  description = 'short plain text description of this coil set'
  ncoil       = 1  ! number of coils in the set
/
```

**The second section** contains the details about the coil properties:

```fortran
&coils_nml
  ...
/
```

Here the properties of each coil are specified as described in the following sections.

#### General fields for each coil independent of the type

```fortran
coil(1)%name            ! name of the coil
coil(1)%coil_type       ! can be axisym_thick, axisym_fila, general_thin (see below)
coil(1)%resist          ! resistance of the coil in Ohm
```

Depending on the `coil_type`, additional information needs to be provided as explained below.

#### Axisymmetric coils with dR and dZ extent (`coil_type=axisym_thick`)

```fortran
coil(1)%R               ! Position in R (center of coil)
coil(1)%Z               ! Position in Z (center of coil)
coil(1)%dR              ! Full width in R
coil(1)%dZ              ! Full width in Z
coil(1)%nbands_R        ! Discretize coil by triangle bands in R direction
coil(1)%nbands_Z        ! Discretize coil by triangle bands in Z direction
coil(1)%ntorpts         ! Number of toroidal points
coil(1)%nturns          ! Number of turns for the coil
```

**Update (25.04.2022):** It is now possible to specify coil bands at different radial and vertical positions to represent current loops of the same electric circuit, for example. The number of parts is given by `nparts_coil`. Each part has values for R, Z, dR, and dZ. Each part can be subdivided into several bands in R and Z directions as before. The old input files are backwards compatible.

**Input with new options:**

```fortran
coil(1)%nparts_coil      ! Number of coil parts N
coil(1)%R(N)             ! Position in R (center of coil)
coil(1)%Z(N)             ! Position in Z (center of coil)
coil(1)%dR(N)            ! Full width in R
coil(1)%dZ(N)            ! Full width in Z
coil(1)%nbands_R         ! Discretize coil by triangle bands in R direction
coil(1)%nbands_Z         ! Discretize coil by triangle bands in Z direction
coil(1)%ntorpts          ! Number of toroidal points
coil(1)%n_thick_turns(N) ! Number of turns per coil part
```

#### Axisymmetric coils specified by filaments (`coil_type=axisym_fila`)

```fortran
coil(1)%n_fila          ! Number of filaments for the coil
coil(1)%n_fila_turns    ! Number of turns in each filament
coil(1)%width           ! "Width" of the coil
coil(1)%R_fila          ! R-position of each filament
coil(1)%Z_fila          ! Z-position of each filament
coil(1)%ntorpts         ! Number of toroidal points
```

#### 3D coil specified by a list of points (`coil_type=general_thin`)

```fortran
coil(1)%n_pts           ! Number of points along the coil
coil(1)%width           ! "Width" of the coil
coil(1)%xpts            ! x-Position of each point along the coil
coil(1)%ypts            ! y-Position of each point along the coil
coil(1)%zpts            ! z-Position of each point along the coil
coil(1)%nturns          ! Number of turns for the coil
coil(1)%dir3d(n_pts*3)  ! OPTIONAL: for each point, give the direction of the band.
                        ! The norm corresponds to the coil width.
                        ! The order is dx1, dy1, dz1, ..., dxN, dyN, dzN
```

