---
title: "Introduction to spatial discretization"
nav_order: 3
parent: "Spatial Discretization"
layout: default
render_with_liquid: false
---
# WARNING: still work in progress
Giacomo is working on this

# Introduction to spatial Discretization in JOREK

The discretization of JOREK is well described in the papers [O. Czarny, G. Huysmans, J.Comput.Phys 227, 7423 (2008)](https://www.sciencedirect.com/science/article/pii/S0021999108002118) and [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub). Here we present a summary of the most important aspects and the code implementation.

As extensively explained [here](/docs/physics/coordinates.html), JOREK uses the cylindrical coordinates $(R,Z,\phi)$. The discretization on the poloidal plane (variables $R$ and $Z$) is discretized using 2D Bezier finite elements, discussed in the [following section](#2d-bezier-finite-elements-in-the-poloidal-plane) whereas the discretization along the toroidal direction (variable $\phi$) is performed with a truncated real Fourier series, as explained in [this section](#real-fourier-series-in-toroidal-direction).

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
$G_m$ continuous Bezier finite elements of order $p$ are used to discretize the poloidal plane RZ.  
Each Bezier finite element is a Bezier surface with $p^2$ control points, of which $4$ interpolation points.

A Bezier surface is defined as

$$
\mathbf{X}(s,t) = \sum_{i=0}^{n} \sum_{j=0}^{n} \mathbf{P}_{ij}B_i^n(s) B_j^n(s)  \tag{3}
$$

where $\mathbf{P}_{ij}$ are the control points and $B_i^n$ and $B_j^n$ are the so-called Bernstein polynomials, defined as:

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


### Nodal degrees of freedom
Instead of looking at the degrees of freedom (i.e. control points) for each finite element (i.e. each Bezier surface), degrees of freedom are assigned to the interpolation points (called _nodes_, which are $4$ for each face). A particular formulation is then chosen, where the control points assigned to one node are expressed as a linear combination of certain vectors local to the node. This vectors are chosen such that they coincide with the $\partial_s^i\partial_t^j \mathbf{X}$ evaluated in the node. 

With bicubic Bezier finite elements, for example, the nodal representation at a generic node $\mathbf{P}_{00}$ is:

$$
\begin{align}
\mathbf{P}_{0,0} &= \vec{u}^{00} \\
\mathbf{P}_{0,1} &= \vec{u}^{00} + \vec{u}^{01}\, h_{01} \\
\mathbf{P}_{1,0} &= \vec{u}^{00} + \vec{u}^{10}\, h_{10} \\
\mathbf{P}_{1,1} &= \mathbf{P}_{0,1} + \mathbf{P}_{1,0} - \vec{u}^{00} + \vec{u}^{11}\, h_{11} \\ 
\end{align}
$$

For a general Bezier surface of degree $n$, the formulation reads as:
$$
\mathbf{P}_{ij} = h^{ij}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{kl} \tag{4}
$$

with $0\leq i,j \leq (n+1)/2$

### $G_m$ continuity
The nodal formulation makes easier imposing $G_m$ continuity.  
In JOREK, most nodes are shared by $4$ finite elements, except for the boundary and few special points (x points and grid axis, which are treated differently). Let $\xi_{11}$, $\xi_{-11}$, $\xi_{-1-1}$, $\xi_{1-1}$ be the $4$ finite elements sharing one node $\mathbf{P}_{00}$, as in the following figure:
 
ADD FIGURE HERE

and let every of this elements have a formulation as $(4)$ but with $h^{ij}$ and $\mathbf{P}_{kl}$ that are unique for each element (see appendix A of [Poloidal discretization](poloidal-discretization.md)), then $G_m$ continuity is imposed with the following costraints:

$\forall j, \ \ h^{-ij}$ is constrained by:
$$
h^{-ij} = 
\begin{cases}
-\alpha h^{ij} & \text{for } i = 1 \text{ and } \alpha > 0 \\
h^{ij} & for i \neq 1
\end{cases} \tag{5a}
$$

$\forall i, \ \ h^{i-j}$ is constrained by:

$$
h^{i-j} = 
\begin{cases}
-\beta h^{ij} & \text{for } j = 1 \text{ and } \beta > 0 \\
h^{ij} & for j \neq 1
\end{cases} \tag{5b}
$$

where the $-$ signs on the indices identify the $\xi_{xy}$ element.

### Nodal formulation
With the formalism introduced in $(4)$, when substituted in $(3)$, a new formulation of the finite element, called nodal formulation, is obtained:
$$
\mathbf{X}_{\text{pol}}^{(K)} = \sum_{i=0}^{\text{n_vertices}} \sum_{j=0}^{\text{n_degrees}} h^{ij}\vec{u}^{ij} b_{ij}^n(s,t) \tag{6}
$$

The new basis functions $b_{ij}$ are simply obtained by gathering all the terms with $\vec{u}^{ij}$. An example of such basis for the bicubic case is given in the [Poloidal discretization page](poloidal-discretization.md)

### Decoupling geometrical variables and physical variables
Until now, vector $\mathbf{X}$ had both the geometrical variables and phyisical variables. However, the two formulations are decoupled in two analogous but separate formulations. Why this? Because they have different toroidal discretization!

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

Toroidal discretization is applied both to the physical variables both to the coordinate variables. As the two formulations are distinct in the poloidal case, as well here are separate. The difference lies in how many elements of the Fourier series are used in the two discretizations.

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
X_{\nu}(s_{i_G},t_{j_G},\phi_{p}) &= \sum_{k = 1}^{N_{vert}}\sum_{j = 1}^{N_{ord}}\sum_{l = 1}^{N_{tor}} \mathrm{nodes}(i)\text{\%}\mathrm{values}(1,j,\nu) \\
&\qquad \cdot \mathrm{H}(k,j,i_G,j_G) \cdot \mathrm{element}\text{\%}\mathrm{size}(k,j) \cdot \mathrm{HZ}(1,p)
\end{align}
\tag{9}
$$

### Gaussian points
For the heavy part, that is the integration, precomputed values of basis functions $b_{ij}$ at gaussian points are used. 
These values are computed by the `initialize_basis()` function in `basis_at_gaussian.f90`, called at the start up fo the code.

### Using high order finite elements
When using high order finite elements ($n\geq 7$), basis functions files and their evaluation at gaussian points has to be calculated before compiling the code. To do this, `tools/util/generate_codes_for_norder_gt_7.py` must be invoked. At the beginning of the file there are some parameters to be set, such as `n_order`.
