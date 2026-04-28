---
title: "Grids"
nav_order: 2
parent: "Numerics and Tools"
layout: default
render_with_liquid: false
---

andres working on this one 
## Grids

Several kinds of finite element grids are implemented in JOREK. Some
grids are used for the determination of the equilibrium only and are not
aligned to the magnetic flux surfaces. These initial grids are (names of
subroutines given):

-   `grid_bezier_square`: Rectangular grid in R- and Z-directions
-   `grid_polar_bezier`: Polar grid with an adjustable boundary shape.
    Refer to Figure \[fig:grid_polar\] and Figure \[fig:grid_xpoint\]
    (grey). This is usually the default choice as initial grid.
-   `grid_bezier_square_polar`: Combination of both, i.e., a square grid
    inside and a polar grid around it.

As soon as the equilibrium has been determined, a finite element mesh
can be generated that is aligned to the equilibrium magnetic flux
surfaces. For this purpose, two grid generation routines are available:

-   `grid_flux_surface`: Two sides of the elements are aligned to the
    flux surfaces of a tokamak configuration without X-point.
-   `grid_xpoint`: The elements are aligned to the flux surfaces of an
    X-point configuration with a single lower X-point (see
    Figure \[fig:grid_xpoint\], red).

In Figure \[fig:grid_xpoint\], two finite element grids are shown. The
grey mesh is of `grid_polar_bezier` type and used for the equilibrium
determination only (initial grid). The flux-surface aligned grid for
X-point geometry (`grid_xpoint`) that is successively used for the
time-integration of the MHD-equations is shown in red.

![grid_polar.png](/wiki/grid_polar.png)

The numbering of the nodes in polar and flux surface grids (black
numbers), the numbering of the nodes within an element (red numbers) and
the directions of the element-local coordinates \$s\$ and \$t\$ are
shown.

![grid_xpoint.png](/wiki/grid_xpoint.png)

The initial grid (`grid_polar_bezier`, grey) and the flux surface
aligned grid (`grid_xpoint`, red) are shown. Both have a significantly
higher resolution in real applications. Specifically, the routine
`grid_xpoint` fails for too coarse initial grids.

## Tutorials

Here is a tutorial for the construction of basic X-point grids, double
X-point grids, and wall-extended grids:

-   [Grad-Shafranov Tutorial](GS_tutorial)
-   [X-point Grid Construction](Xgrid_tutorial)
-   [Double X-point Grid Construction](DXgrid_tutorial)
-   [Wall-extended Grid Construction](Wallgrid_tutorial)
-   [Alternative wall-extended Grid Construction](Wallgrid_tutorial2)
-   [Gn-continuous Grid Construction](Gn_grid_tutorial)
