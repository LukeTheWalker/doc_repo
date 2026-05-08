---
title: "Introduction to spatial discretization"
nav_order: 3
parent: "Spatial Discretization"
layout: default
render_with_liquid: false
---

# Introduction to spatial Discretization in JOREK

The discretization of JOREK is well described in the papers [O. Czarny, G. Huysmans, J.Comput.Phys 227, 7423 (2008)](https://www.sciencedirect.com/science/article/pii/S0021999108002118) and [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub). Here we present a summary of the most important aspects and the code implementation.

As extensively explained [here](/docs/physics/coordinates.html), JOREK uses the cylindrical coordinates $(R,Z,\phi)$. The discretization on the poloidal plane (variables $R$ and $Z$) is discretized using 2D Bezier finite elements, discussed in the [following section](#2d-bezier-finite-elements-in-the-poloidal-plane) whereas the discretization along the toroidal direction (variable $\phi$) is performed with a truncated real Fourier series, as explained in [this section](#toroidal-discretization-with-real-fourier-series).

On a finite element $K$, using a local coordinate system $s,t$ (see [Introduction to Bezier surfaces](introduction-to-bezier.md)), the two discretizations combined read as follows:

$$
\mathbf{X}^{(K)}(s,t,\phi) = \left(\sum_{l=1}^{N_\text{tor}} Z_l(\phi) \left (\sum_{i = 1}^{N_\text{vert}}\sum_{j = 1}^{\text{dof}} h^{ij} \vec{u}^{ijl} b_{i,j}(s,t)\right) \right ) \tag{1}
$$

with $\mathbf{X}$ the vector of variables (i.e. $\rho$, $T$, $u$, ...).
For the geometrical poloidal variables $R,Z$, there is a similar relation:

$$
\begin{pmatrix}
R \\
Z
\end{pmatrix}^{(K)}
(s,t,\phi) 
= \left(\sum_{l=1}^{N_{\text{coord_tor}}} Z_l(\phi) \left (\sum_{i = 1}^{N_{vert}}\sum_{j = 1}^{\text{dof}} h^{ij} \vec{v}^{ijl} b_{i,j}(s,t)\right) \right ) \tag{2}
$$

The inner parenthesis is the poloidal discretization, which uses the basis functions $b_{i,j}$, while $Z_l$ are the basis functions for the toroidal discretization.

Note that when building the mesh, all the degrees of freedom $\vec{v}^{ijl}$ in $(2)$ are fixed as well as $h^{ij}$ (for both $(2)$ and $(1)$).

### Parameters of the formulation
- $N_\text{tor}$, in the code `n_tor` and $N_\text{coord_tor}$, in the code `n_coord_tor`, are two parameters to be specified at compile time (see [this section](#toroidal-discretization-with-real-fourier-series))
- $N_\text{vert}$ is fixed to $4$ 
- $\text{dof}$ (`n_degrees`), that is the number of degrees of freedom for each vertex for each problem variable (ex: $T$), is determined by the polynomial degree `n_order` (user can choose it) with the following relation: `n_degrees = ((n_order+1)/2)^2`.

## 2D Bezier finite elements in the poloidal plane
$G_m$ continuous Bezier finite elements of order $n$ are used to discretize the poloidal plane RZ.  
Each Bezier finite element is a Bezier surface with $n^2$ control points, of which $4$ interpolation points.

A Bezier surface is defined as

$$
\mathbf{X}(s,t) = \sum_{i=0}^{n} \sum_{j=0}^{n} \mathbf{P}_{ij}B_i^n(s) B_j^n(s)  \tag{3}
$$

where $\mathbf{P}_{ij}$ are the control points and $B_i^n$ and $B_j^n$ are the Bernstein polynomials, defined as:

$$
B_i^n(s) = \frac{n!}{i!(n-i)!} s^i (1-s)^n-1
$$

It is important to note that in $(3)$, the vector $\mathbf{X}$ includes both geometrical variables ($R$ and $Z$) and physical variables (ex. $\Psi$, $\rho$, $T$, ...). So it writes:

$$
\mathbf{X} = 
\begin{pmatrix}
R \\
Z \\
\Psi \\
\rho \\
T \\
\vdots
\end{pmatrix}
$$

However, in practice, geometrical variables and physical variables are _decoupled_ in two separate formulations. More on this at [this paragraph](#decoupling-geometrical-variables-and-physical-variables).

A more in depth explanation on Bezier surfaces can be found in [Introduction to bezier surfaces](introduction-to-bezier.md).

### Nodal formulation
Tipically degrees of freedom (here the control points) are grouped for each face (here Bezier patch). In JOREK instead they are grouped by nodes. Each Bezier surfaces have $4$ interpolation points, which are called nodes. So this means that all other control points are assigned to one interpolation point.  
Indeed, as shown in [Introduction to bezier surfaces](introduction-to-bezier.md), each control point is connected with the deriative on one node. 

In JOREK for each node a local vectorial basis is defined and the control points associated to the node are expressed in function of this basis. 
For example, with bi-cubic Bezier surfaces, control points of node $\mathbf{P}\_{00}$ would be expressed as follows:

$$
\begin{align}
\mathbf{P}_{0,0} &= \vec{u}^{00} \\
\mathbf{P}_{0,1} &= \vec{u}^{00} + \vec{u}^{01}\, h_{01} \\
\mathbf{P}_{1,0} &= \vec{u}^{00} + \vec{u}^{10}\, h_{10} \\
\mathbf{P}_{1,1} &= \mathbf{P}_{0,1} + \mathbf{P}_{1,0} - \vec{u}^{00} + \vec{u}^{11}\, h_{11} \\ 
\end{align} \tag{4}
$$

where $h^{ij}$ are called _element sizes_ and are set during the mesh construction phase.

This formulation has the main advantage of making easier how $G_m$ continuity is imposed. When $4$ patches share a node $\mathbf{P}_{00}$, $G_m$ continuity is imposed by:
1. Sharing the local basis $\{\vec{u}^{ij}\}_{ij}$ among all $4$ patches.
2. Setting certain simple constraints on $h_{ij}$ (see [Poloidal discretization](poloidal-discretization.md))

Using $(4)$, which can be generalized to a Bezier curve of any order $n$ (see [Poloidal discretization](poloidal-discretization.md)), then $(3)$ can be rewritten as

$$
\mathbf{X}_{\text{pol}}^{(K)} = \sum_{i=0}^{\text{n_vertices}} \sum_{j=0}^{\text{n_degrees}} h^{ij}\vec{u}^{ij} b_{ij}^n(s,t) \tag{5}
$$

where $b_{ij}$ are the new basis functions, obtained by gathering together all the terms with $\vec{u}^{ij}$.


### Decoupling geometrical variables and physical variables
Until now, vector $\mathbf{X}$ had both the geometrical variables and phyisical variables. However, in practice the two formulations are decoupled in two analogous but separate formulations. Why this? Because they have different _toroidal_ discretization.

The two formulations read as

$$
\mathbf{X}_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{u}^{ij} b_{ij}(s,t)
$$

and

$$
\begin{pmatrix} R \\ Z
\end{pmatrix}
_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{v}^{ij} b_{ij}(s,t)
$$

where now $\mathbf{X}$ refers only to the physical variables.

Note that $h^{ij}$ are the **same**

## Toroidal discretization with real Fourier series

Toroidal discretization is applied both to the physical variables both to the coordinate variables. They are both discretized with the same approach, that is truncated real Fourier series, but using different parameters (number of harmonics included and periodicity of the harmonics, see after the table).

A real Fourier series ($\cos$, $\sin$) is used, as shown in the following table:

| JOREK harmonic | Toroidal mode number | Toroidal basis function |
|--|--|--|
| 1 | 0 | 1 |
| 2 | $n_\text{period}$ | $\cos(n_\text{period}\phi)$ |
| 3 | $n_\text{period}$ | $\sin(n_\text{period}\phi)$ |
| 4 | $2n_\text{period}$ | $\cos(2n_\text{period}\phi)$ |
| 5 | $2n_\text{period}$ | $\sin(2n_\text{period}\phi)$ |
| ... | ... | ... |
| n_$\text{tor}-1$ | $\frac{n_\text{tor}-1}{2} n_\text{period}$ | $\cos(\frac{n_\text{tor}-1}{2}n_\text{period}\phi)$ |
| n_$\text{tor}$ | $\frac{n_\text{tor}-1}{2} n_\text{period}$ | $\sin(\frac{n_\text{tor}-1}{2}n_\text{period}\phi)$ |

For the physical discretization, **hard-coded parameters** `n_tor` and `n_period` are used to select the harmonics included in the simulation:
  * `n_tor`: Total number of real Fourier modes (odd integer number)
  * `n_period`: Toroidal periodicity (positive integer number)

For the coordinate/geometrical discretization, `n_coord_tor` and `n_coord_period` are used in the same manner.

The **maximum toroidal mode number** included in a simulation is `n_max=(n_tor-1)/2*n_period`.  
A **sufficient number of toroidal planes** is required to avoid aliasing. The minimal requirement is typically `n_plane >= 2 * n_tor`. It is always a good idea to scan `n_plane` for a simulation to ensure convergence. `n_plane` must be a power of 2, if FFTW is not used. If FFTW is used (see [here](/docs/compiling/cat_compiling.md) for more), `n_plane` can be an arbitrary positive integer number, but not for all values FFTW is similarly efficient.

## Putting all together: toroidal and poloidal discretization
When the two discretizations are combined, the poloidal degrees of freedom are now replicated for each poloidal mode $l$. That is, the total number of degrees of freedom is

$$
N_{\text{dof}} = \text{n_tor} (d-2) \left( \frac{n+1}{2}\right)^2
$$

So the formulations $(1)$ and $(2)$ are obtained.


## Implementation in the code
There are 2 fundamental types: `type_node` and `type_element` (see `data_structure.f90`).

`type_node` contains the degrees of freedom $\vec{u}^{ij}$ (for physical variables) in `node%values` array and $\vec{v}^{ij}$ (for coordinates) in `node%x` array.

`type_element` contains the sizes $h^{ij}$ for each vertex.

Here are some examples showing how DoF and sizes are stored. 

Fixed a toroidal number $l \in [0, \text{n_tor}]$, physical degrees of freedom can be accessed as follows:

$$
\begin{align}
&\texttt{node\%values(l,1,1)} \rightarrow p_k  \\
&\texttt{node\%values(l,2,1)} \rightarrow u_k  \\
&\texttt{node\%values(l,3,1)} \rightarrow v_k  \\
&\texttt{node\%values(l,4,1)} \rightarrow w_k 
\end{align}
$$

the first index is the toroidal mode, the second index the degree of freedom and the third index the variable 

$$
\begin{align}
&\texttt{element\%size(k,1)} \rightarrow h^{00} := 1  \\
&\texttt{element\%size(k,2)} \rightarrow h^{10} \\
&\texttt{element\%size(k,3)} \rightarrow h^{01} \\
&\texttt{element\%size(k,4)} \rightarrow h^{11}
\end{align}
$$

$$
\begin{align}
 &\texttt{node\%x(1,\mu)} \rightarrow p_k  \\
 &\texttt{node\%x(2,\mu)} \rightarrow u_k  \\
 &\texttt{node\%x(3,\mu)} \rightarrow v_k  \\
 &\texttt{node\%x(4,\mu)} \rightarrow w_k 
\end{align}
$$

For all $\nu = 1\ldots N_{var}$ and $i_G, j_G = 1\ldots N_{Gauss}$ and $p = 1\ldots N_{plane}$, the variable values at a given Gaussian point $(s_{i_G}, t_{j_G})$ at the toroidal position $\phi_p$ in a given finite element can be expressed by

$$
\begin{align}
X_{\nu}(s_{i_G},t_{j_G},\phi_{p}) &= \sum_{k = 1}^{N_{vert}}\sum_{j = 1}^{N_{ord}}\sum_{l = 1}^{N_{tor}} \mathrm{nodes}(i)\text{\%}\mathrm{values}(l,j,\nu) \\
&\qquad \cdot \mathrm{H}(k,j,i_G,j_G) \cdot \mathrm{element}\text{\%}\mathrm{size}(k,j) \cdot \mathrm{HZ}(l,p)
\end{align}
\tag{9}
$$

Above notation is slightly different from $(1)$ and $(2)$. Indeed we have $H(k,j,i_g,j_g):=b_{kj}(s_{i_g}, t_{j_g})$ . Furthermore $HZ(l,p):=Z_l(\phi_p)$.

### Gaussian points
For the heavy part, that is the integration, precomputed values of basis functions $b_{ij}$ at gaussian points are used. 
These values are computed by the `initialize_basis()` function in `basis_at_gaussian.f90`, called at the start up fo the code.

### Using high order finite elements
When using high order finite elements ($n\geq 7$), basis functions files and their evaluation at gaussian points has to be calculated before compiling the code. To do this, `tools/util/generate_codes_for_norder_gt_7.py` must be invoked. At the beginning of the file there are some parameters to be set, such as `n_order`.

### Other routines
Other routines involving Bezier finite elements are the ones doing the mapping $(K, s,t) \rightarrow (R,Z)$ (`interp_RZP.f90`) and its reverse mapping (`find_RZ.f90`). $K$ is a finite element.

#### interp_RZP.f90
Simply uses expression $(2)$. Some overloads also provide up to second derivatives (also crossed) $\partial_s^i \partial_t^j R$ and $\partial_s^i \partial_t^j Z$. 

#### find_RZ.f90 
There is no general mapping $(R,Z) \rightarrow (s,t)$, because $(s,t)$ are coordinates local to each element $K$. In general there is no direct way to detect which is the element that contains $(R_\text{find},Z_\text{find})$, so a tree is built.  
Instead of iterating through all the elements to see which contains $(R_\text{find},Z_\text{find})$, elements are ordered into a quadtree (`mod_quadtree.f90`). See, for example the [quadtree wikipedia page](https://en.wikipedia.org/wiki/Quadtree) for an explanation of this data structure.  
This does not provide a single element as container of $(R_\text{find},Z_\text{find})$ but a few elements as _potential containers_.  

After having used the quadtree, for each of the remaining elements Newton method is used to solve the following system:
$$
\begin{cases}
R(s,t) = R_\text{find} \\
Z(s,t) = Z_\text{find}
\end{cases}
$$

For each of these elements Newton method is executed for 20 iterations, after which, if the point has not been found, another starting point is tried.  
Starting points used are hard coded in `find_RZ.f90` file.  
The first element in which convergence is reached (that is, the error is under a certain threshold), is returned, along with the found solutions `s` and `t`.

