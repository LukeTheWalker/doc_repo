---
title: "Spatial Discretization"
nav_order: 1
parent: "Numerics and Tools"
layout: default
render_with_liquid: false
---

# Spatial Discretization in JOREK

The discretization of JOREK is well described in the papers [O. Czarny, G. Huysmans, J.Comput.Phys 227, 7423 (2008)](https://www.sciencedirect.com/science/article/pii/S0021999108002118) and [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub). Here we present a summary of the most important aspects and the code implementation.

As extensively explained [here](http://localhost:4000/doc_repo/docs/physics/coordinates.html), JOREK uses the cylindrical coordinates $(R,Z,\phi)$. The discretization on the poloidal plane (variables $R$ and $Z$) is discretized using 2D Bezier finite elements, discussed the [following section](#2d-bezier-finite-elements-in-the-poloidal-plane) whereas the discretization along the toroidal direction (variable $\phi$) is performed with a truncated real Fourier series, as explained in [this section](#real-fourier-series-in-toroidal-direction).

## 2D Bezier finite elements in the poloidal plane

JOREK uses isoparametric Gm-continuous Bezier finite elements for spatial discretization on the poloidal plane $RZ$. Instead of using control points as "direct" degrees of freedom, a different formulation, called *nodal formulation* (see [here](#bezier-finite-element-nodal-representation)), is used, which greatly facilitate imposing Gm-continuity across multiple finite elements. What isoparametric and Gm-continuous (with $m\in \mathbb{N}$) means will be explained soon.

### Brief introduction on Bezier curves and Bezier surfaces

We start with a brief overview of Bezier curves and then move from this background to the particular formalism used in JOREK.

#### <u>Bezier curves</u>

Bezier curves are parametric curves $\mathbf{P}(t)$ which are controlled by a set of points, intuitively called *control points*.
The parameter $t$ is in the range $[0,1]$.
The first and the last points, namely $\mathbf{P}\_0$ and $\mathbf{P}\_{n - 1}$ on the sequence of control points are interpolation points, that is $\mathbf{P}(0) = \mathbf{P}\_0$ and $\mathbf{P}(1) = \mathbf{P}\_1$.
The influence of the control points on the shape of the curve is determined by the a base $\{B_0(t), \dots, B_n(t)\}$, called *Bernstein polynomials*. Point `i` is associated to the polynomial $\mathbf{P}\_i$, indeed the mathematical expression of the Bezier curve is

$$
\mathbf{P}(t) = \sum_{i = 0}^{n}\mathbf{P}_iB_i(t)
$$

Bernstein polynomial are defined by the following formula:

$$B_{i}^{n}(s) = \frac{n!}{i!(n - i)!} s^{i}(1 - s)^{n - i}\qquad i = 0\ldots n$$

Bernstein polynomials' basis is fundamental in the Bezier finite element framework. In JOREK, it is **not** the basis local to the single finite element, but the latter is derived from the Bernstein basis. More on this in the section [Bezier finite element nodal representation](#bezier-finite-element-nodal-representation).

When referring to Bezier curves of degree $n$ we mean that we have $n + 1$ points and $n + 1$ polynomials of degree $n$.

> **Intuition on Bezier curves**: Bezier curves were invented by the French engineer Pierre Bézier and the intuitive way of building them is through the [de Casteljau's algorithm](https://en.wikipedia.org/wiki/De_Casteljau%27s_algorithm). You can see Bezier curves as Linear intERPolation (in graphics vocabulary, LERP) applied recursively. First, you linearly interpolate with parameter `t` every two consecutivive control points, so you generate `n` points. Then you do the same with this new "derived" control point, again with parameter `t`, until you reach only one point. This is $\mathbf{P}(t)$ The following image depicts what just described:
> 
> <img src="assets/spatial-discretization/bezier_curve.png" width="500">

> **Important note on dimensionality**: It is important to underline that points $\mathbf{P}_i$ can belong to a space $\mathbb{R}^m$ with **any** $m$, given that $m > 1$. Bezier curves are generally though with $\mathbf{P}_i \in \mathbb{R}^2$ but it my be as well $\mathbf{P}_i \in \mathbb{R}^{100}$! Indeed in JOREK the smallest space is $\mathbb{R}^8$ since at least $6$ variables are used.

#### <u>Bezier surfaces</u>

Bezier surfaces can be viewed as the tensor product of Bezier curves. The basis has now the following form:

$$\{B_{i}(s)B_{j}(t)\}_{i = 0\ldots n,j = 0\ldots n}$$

and to each polynomial there is the corrspective $\mathbf{P}_{i,j}$ element. The Bezier surface then writes:

$$\mathbf{P}(s,t) = \sum_{i = 0}^{n}\sum_{j = 0}^{n}B_{i}^{n}(s)B_{j}^{n}(t)$$

<img src="assets/spatial-discretization/bezier_surface.png" width="500">

### From Bezier surfaces to Bezier finite elements

In JOREK Bezier surfaces are used for the discretization on the poloidal plane. The points $\mathbf{P}_i$ has as first two coordinates the domain coordinates $R$ and $Z$, whereas the remaining $6+$ coordinates correspond to the variables (functions) of interest (see [here](http://localhost:4000/doc_repo/docs/physics/base_fluid_models/base_fluid_models.html) for the list of variables used).

In its most elementary version a Bezier finite element is nothing but a Bezier surface and the *degrees of freedom* are the points $\mathbf{P}_i$. To be precise, each entry of a point $\mathbf{P}_i \in \mathbb{R}^m$ is a degree of freedom, so the total number of degrees of freedom is $n \cdot m$.

The formulation gets more complex when patching together multiple finite elements to create the global representation. Indeed constraints on the continuity

### Bezier finite element nodal representation

### The following is still to be adapted

Two-dimensional third-order Bernstein polynomials $B_{i,j}^{3}(s,t)$ defined by

$$
B_{i,j}^{3}(s,t) = B_{i}^{3}(s)B_{j}^{3}(t)\qquad i,j = 0\ldots 3 \tag{1}
$$

with

$$
B_{i}^{3}(s) = \frac{3!}{i!(3 - i)!} s^{i}(1 - s)^{3 - i} \tag{2}
$$

are used for the discretization in the poloidal plane. The coordinates $s = 0\ldots 1$ and $t = 0\ldots 1$ form the element-local coordinate system. A quantity $X$ which may be a coordinate or a physical variable $(R,Z,\Psi,T,\ldots$; iso-parametric discretization) can be expressed by

$$
X(s,t) = \sum_{i = 0}^{3}P_{i,j}B_{i,j}^{3}(s,t). \tag{3}
$$

As first order continuity of the finite elements is demanded, not all combinations of control points $P_{i,j}$ are valid. Effectively, four free parameters $p_k$, $u_k$, $v_k$, and $w_k$ remain per node $k$ and quantity $X$ of the element. The control points $P_{i,j}$ can be reconstructed from these free parameters as given in the following. Nodes $k = 1\ldots 4$ correspond to the positions $(i,j) = (0,0)$, $(3,0)$, $(3,3)$, and $(0,3)$.

$$
\begin{array}{r l}
P_{0,0} &= p_1 \\
P_{0,1} &= p_1 + v_1\, d_{v,1} \\
P_{1,0} &= p_1 + u_1\, d_{u,1} \\
P_{1,1} &= P_{0,1} + P_{1,0} - p_1 + w_1\, d_{u,1}\, d_{v,1} \\
P_{3,0} &= p_2 \\
P_{3,1} &= p_2 + v_2\, d_{v,2} \\
P_{2,0} &= p_2 + u_2\, d_{u,2} \\
P_{2,1} &= P_{3,1} + P_{2,0} - p_2 + w_2\, d_{u,2}\, d_{v,2} \\
P_{3,3} &= p_3 \\
P_{3,2} &= p_3 + v_3\, d_{v,3} \\
P_{2,3} &= p_3 + u_3\, d_{u,3} \\
P_{2,2} &= P_{2,3} + P_{3,2} - p_3 + w_3\, d_{u,3}\, d_{v,3} \\
P_{0,3} &= p_4 \\
P_{0,2} &= p_4 + v_4\, d_{v,4} \\
P_{1,3} &= p_4 + u_4\, d_{u,4} \\
P_{1,2} &= P_{0,2} + P_{1,3} - p_4 + w_4\, d_{u,4}\, d_{v,4}
\end{array}
\tag{4}
$$

Here, the $d_{u,k}$ and $d_{v,k}$ are measures for the distances of the control points from the element nodes. These are element properties, i.e., for a node that belongs to several elements, the value of $d_{u,k}$ depends on the element considered. In JOREK, they are represented by

$$
\begin{align}
&\texttt{element%size(k,1)} \rightarrow 1  \\
&\texttt{element%size(k,2)} \rightarrow d_{u,k} \\
&\texttt{element%size(k,3)} \rightarrow d_{v,k} \\
&\texttt{element%size(k,4)} \rightarrow d_{u,k} d_{v,k} 
\end{align}
$$

## Projecting on the bezier elements

The distribution $X(s,t)$ of quantity $X$ within a certain element can be expressed by Equation $(3)$. Inserting Equations $(1)$-$(2)$ and Equation $(4)$ leads to the following expression

$$
X(s,t) = \sum_{k = 1}^{4} \tilde{p}_k(s,t) \tag{5}
$$

with the contributions

$$
\tilde{p}_k = b_{k,1}\, p_k + b_{k,2}\, u_k\, d_{u,k} + b_{k,3}\, v_k\, d_{v,k} + b_{k,4}\, w_k\, d_{u,k}\, d_{v,k} \tag{6}
$$

associated to the four nodes. Here,

$$
\begin{array}{r l}
b_{1,1} &= (1 - s)^{2} (1 - t)^{2} (1 + 2 s) (1 + 2 t) \\
b_{1,2} &= 3 (1 - s)^{2} (1 - t)^{2} s (1 + 2 t) \\
b_{1,3} &= 3 (1 - s)^{2} (1 - t)^{2} (1 + 2 s) t \\
b_{1,4} &= 9 (1 - s)^{2} (1 - t)^{2} s t \\
b_{2,1} &= s^{2} (1 - t)^{2} (3 - 2 s) (1 + 2 t) \\
b_{2,2} &= 3 s^{2} (1 - t)^{2} (1 - s) (1 + 2 t) \\
b_{2,3} &= 3 s^{2} (1 - t)^{2} (3 - 2 s) t \\
b_{2,4} &= 9 s^{2} (1 - t)^{2} (1 - s) t \\
b_{3,1} &= s^{2} t^{2} (3 - 2 s) (3 - 2 t) \\
b_{3,2} &= 3 s^{2} t^{2} (1 - s) (3 - 2 t) \\
b_{3,3} &= 3 s^{2} t^{2} (3 - 2 s) (1 - t) \\
b_{3,4} &= 9 s^{2} t^{2} (1 - s) (1 - t) \\
b_{4,1} &= (1 - s)^{2} t^{2} (1 + 2 s) (3 - 2 t) \\
b_{4,2} &= 3 (1 - s)^{2} t^{2} s (3 - 2 t) \\
b_{4,3} &= 3 (1 - s)^{2} t^{2} (1 + 2 s) (1 - t) \\
b_{4,4} &= 9 (1 - s)^{2} t^{2} s (1 - t) .
\end{array}
\tag{7}
$$

In JOREK, the quantities $b_{k,j}$ are required at the position of the Gaussian points with indices $(i_G, j_G)$. They are denoted

$\texttt{H(k,j,i_G,j_G)} b_{k,j}$ at Gaussian point $(i_G,j_G) \tag{8}$ 

and are initialized in the subroutine ''basisfunctions2''.

## Notation in the code

The degrees of freedom of each node corresponding to the $l$-th toroidal harmonic of the $\nu$-th physical quantity are denoted in the following way in the code:

$$
\begin{align}
&\texttt{node%values(l,1,\nu)} \rightarrow p_k  \\
&\texttt{node%values(l,2,\nu)} \rightarrow u_k  \\
&\texttt{node%values(l,3,\nu)} \rightarrow v_k  \\
&\texttt{node%values(l,4,\nu)} \rightarrow w_k 
\end{align}
$$

The degrees of freedom of the coordinates $R$ ($\mu = 1$) and $Z$ ($\mu = 2$) are called,

$$
\begin{align}
 &\texttt{node%x(1,\mu)} \rightarrow p_k  \\
 &\texttt{node%x(2,\mu)} \rightarrow u_k  \\
 &\texttt{node%x(3,\mu)} \rightarrow v_k  \\
 &\texttt{node%x(4,\mu)} \rightarrow w_k 
\end{align}
$$

For all $\nu = 1\ldots N_{var}$ and $i_G, j_G = 1\ldots N_{Gauss}$ and $p = 1\ldots N_{plane}$, the variable values at a given Gaussian point $(s_{i_G}, t_{j_G})$ at the toroidal position $\phi_p$ in a given finite element can be expressed by

$$
\begin{aligned}
X_{\nu}(s_{i_G},t_{j_G},\phi_{p}) &= \sum_{k = 1}^{N_{vert}}\sum_{j = 1}^{N_{ord}}\sum_{l = 1}^{N_{tor}} \mathrm{nodes}(i)\%\mathrm{values}(1,j,\nu) \\
&\qquad \cdot \mathrm{H}(k,j,i_G,j_G) \cdot \mathrm{element}\%\mathrm{size}(k,j) \cdot \mathrm{HZ}(1,p),
\end{aligned}
\tag{9}
$$

where `i=element%vertex(k)`. Here, $N_{var}$ denotes the number of physical variables, $N_{Gauss} = 4$ the number of Gaussian points used for Gauss quadrature in $s$ and $t$ directions each, $N_{plane} = 2(N_{tor} - 1)$ the number of toroidal planes located at $\phi_{p} = 2\pi (p - 1) / N_{plane}$, $N_{vert} = 4$ the number of vertices in each element, $N_{ord} = 4$ the number of degrees of freedom per vertex, and $N_{tor}$ the number of different toroidal Fourier modes. The quantity ''HZ(l,p)'' corresponds to the value of the $l$-th Fourier mode at the toroidal position $\phi_{p}$ and is denoted $Z_{l}(\phi_{p})$ in the following. The table below lists which Fourier modes correspond to the different mode indices $l$.

| l | 1 | 2 | 3 | 4 | 5 | ... |
|---|---|---|---|---|---|---|
| $Z_l(\phi_p) \equiv$ `HZ`(l,p) | 1 | $\cos \phi_p$ | $\sin \phi_p$ | $\cos 2\phi_p$ | $\sin 2\phi_p$ | ... |

## Real Fourier series in toroidal direction

* For the toroidal direction, a real Fourier series ($\cos$, $\sin$) is used:

| JOREK harmonic | Toroidal mode number | Toroidal basis function |
|--|--|--|
| 1 | 0 | 1 |
| 2 | n_period | cos(n_period*phi) |
| 3 | n_period | sin(n_period*phi) |
| 4 | 2*n_period | cos(2*n_period*phi) |
| 5 | 2*n_period | sin(2*n_period*phi) |
| ... | ... | ... |
| n_tor-1 | (n_tor-1)/2*n_period | cos((n_tor-1)/2*n_period*phi) |
| n_tor | (n_tor-1)/2*n_period | sin((n_tor-1)/2*n_period*phi) |

* The **hard-coded_parameters** `n_tor` and `n_period` are used to select the harmonics included in the simulation.
  * `n_tor`: Total number of real Fourier modes (odd integer number)
  * `n_period`: Toroidal periodicity (positive integer number)
* The **maximum toroidal mode number** included in a simulation is `n_max=(n_tor-1)/2*n_period`.
* A **sufficient number of toroidal planes** is required to avoid aliasing. The minimal requirement is typically `n_plane >= 2 * n_tor`. It is always a good idea to scan `n_plane` for a simulation to ensure convergence. `n_plane` must be a power of 2, if FFTW is not used. If FFTW is used (see [here](http://localhost:4000/doc_repo/docs/compiling/cat_compiling.html) for more), `n_plane` can be an arbitrary positive integer number, but not for all values FFTW is similarly efficient.