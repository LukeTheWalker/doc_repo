---
title: "Assess Particle Wall Loads with Particle Tracker"
nav_order: 2
parent: "Kinetic Particles"
grand_parent: "Howto"
layout: default
render_with_liquid: false
---

# Assess Particle Wall Loads with the Particle Tracker
**Note:**
  * The wall collision check has been implemented fully only for relativistic particle and relativistic guiding center modes. For other modes the algorithm still exists but you can't get a full output without implementing how the particle energy is evaluated in the export routine (so this is a simple thing to do).
  * You'll need a triangular mesh that represents PFCs to use this module. If you don't have one, use the script `assets/particles_wall_load/create_basic_wall.py` to generate a simple wall mesh from the edges of the JOREK computational grid.
  * More details is provided in the {{ ::internship_report_with_chapters.pdf |internship report}} of Miko Skyllas.



## Input

The input consists of a simple HDF5 file that has two datasets: **ntriangle** indicating number of wall elements (triangles) and **nodes** which is an array of triangle nodes in a format [x1_1, y1_1, z1_1, x2_1, y2_1, z2_1,x3_1, y3_1, z3_1, x1_2, y1_2, z1_2, ...], where the last index is triangle ID.

An easy way to construct the wall input is e.g. by reading the data (usually in stl or vtk format) with pyvista, and converting it to desired format.

At present wall models for a few tokamaks in the format taken by JOREK exist: ITER, ASDEX Upgrade, EU-DEMO. These are available on the TOK cluster under /shares/users/public/visv.


The wall mesh has to be included in the run folder.

## Running a simulation with wall collision checks


The implementation of the module can be found in particles/mod_wall_collision.f90. To use this module in a particle simulation, begin by initializing the wall data.

``` fortran
type(octree_triangle) :: octree ! The struct containing the wall data.
call mod_wall_collision_init('wall.h5', octree, max_depth)
```

To check wall collisions at each time step, use (inside the simulation loop)
``` fortran
call mod_wall_collision_check(p, q, octree, wall_id, wall_pos)
```

where p is the marker position at the beginning of the time step (in cylindrical coordinates) and q at the end of the time step. The subroutine returns id of the wall element that was hit (zero otherwise) and the impact point as p + t * (q - p) where parameter t is determined by the collision check. The wall element id corresponds to the position of the element in the input file.

Free resources with
``` fortran
call mod_wall_collision_free(octree)
```

The data can then be exported with
``` fortran
call mod_wall_collision_export(sim, file)
```

Note that this assumes that (for lost markers) you have stored the data as i_elm = (-1) * wall_id. The minus sign is there just to notify that the marker is lost.

An example script can be found in particles/examples/example_wallload.f90

## Description of the algorithm

The algorithm is relatively simple. At each time-step, the line segment between the marker new and old positions is used to perform ray-tracing with respect to wall triangles using Möller-Trumbore algorithm. To optimize the process, ray tracing is only performed against triangles that are in close proximity. This is accomplished by recursively dividing the volume into eight quadrants, and only checking collisions against those triangles that are inside the same volume(s) as the marker new or old position. This octree is built upon initialization, and it's effectiveness can be seen in the following plot (for simulations max_depth=6 is recommended):

<img src="assets/particles_wall_load/octree_convergence.png" alt="Alt text" width="250">


## Output and post-processing

For the output the module creates a HDF5 file that contains:
  * IDs (i.e. index in the original input array starting from 1) of the wetted elements.
  * Particle load (prt/m^2) on each wetted triangle. The particle load is counted as sum(weight) / area of the element, where sum is over all particles that hit the element.
  * Heat load (J/m^2) on each wetted triangle. The heat load is counted as sum( particle weight * particle energy) / area of the element.


The post-processing script is util/plot_wallload.py that will output the wetted area, and maximum particle and heat loads. The script requires wall input, wall loads and optionally also the particle restart file. The script also visualizes the losses (note that the default settings are for ITER):

<img src="assets/particles_wall_load/particle_losses.png" alt="Alt text" width="250">
<img src="assets/particles_wall_load/3D_wall_load.png" alt="Alt text" width="195">

**Left**: Scatter plot of marker final positions. **Right** Loads on the 3D wall mesh.

<img src="assets/particles_wall_load/3D_wall_load_mean.png" alt="Alt text" width="250">
<img src="assets/particles_wall_load/wall_load_histogram.png" alt="Alt text" width="240">

**Left** Load pattern on the wall. Note that these losses are projected on the blue curve shown in the first figure, so this figure does not show exact losses or their distribution but just the general pattern. **Right** Histogram showing area affected at least by the given heat load.

Optionally, one can also output the particle restart file, where i_elm indicates the end state of the given marker (>0 confined, =0 was lost but did not hit wall, < 0 triangle ID (multiplied with -1 to indicate the marker was lost) where this marker was lost).

Another possibility is to output a particle output file into a format compatible with the FIREWALL code. This is then an HDF5 file which contains a group called "groups" with a subgroup called "001" (particle species type), which in turn contains the following (where only the needed quantities for FIREWALL are listed):
* i_elm: array containing the wall ids of the triangle hit by the respective markers.
* t_loss: array containing the time of impact of the markers with the wall.
* v: matrix containing the momentum vector at the time of impact for the markers.
* weight: array containing the physical particle count for each marker. 

The output from FIREWALL for the ITER case would then look like:

<img src="assets/particles_wall_load/3D_FIREWALL.png" alt="Alt text" width="200">
<img src="assets/particles_wall_load/toroidal_FIREWALL.png" alt="Alt text" width="245">

**Left** Surface temperatures on the 3D wall model. **Right** Toroidal projection of the surface temperatures.

