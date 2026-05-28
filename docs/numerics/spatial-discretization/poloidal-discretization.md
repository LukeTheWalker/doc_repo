---
title: "Poloidal discretization"
nav_order: 3
parent: "Spatial Discretization"
layout: default
render_with_liquid: false
---


# Polodial discretization

JOREK uses isoparametric $G_m$-continuous Bezier finite elements for spatial discretization on the poloidal plane $RZ$. Instead of using control points as "direct" degrees of freedom, a different formulation, called *nodal formulation* (see [here](#bezier-finite-element-nodal-representation)), is used, which greatly facilitate imposing $G_m$-continuity across multiple finite elements. What isoparametric and $G_m$-continuous (with $m\in \mathbb{N}$) mean will be explained soon.

For an overview of Bezier curves, Bezier surfaces and how to pass from these to the concept of Bezier finite elements see the [Introduction to bezier surfaces](introduction-to-bezier.md)

We use the parameters $s,t\in [0,1]$ as local coordinates of a Bezier finite element, so the discretization on a single Bezier finite element of degree $n$ reads as

$$
X_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{n}\sum_{j=0}^{n} \mathbf{P}_{ij} B_i^n(s)B_j^n(t) \tag{3}
$$

with $B_i^n$ and $B_j^n$ Bernstein polynomials and $P_{ij}$ control points of the surface.

As explained in the following section, Equation $(3)$ is rewritten in a more convenient way, that is:

$$
X_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{u}^{ij} b_i(s,t)
$$

### Bezier finite element nodal representation
In JOREK a particular formulation of the Bezier finite elements is used, called nodal representation.  
A node is an interpolation point. On a Bezier surface, independently of the polynomial order chosen, the interpolation points are always $4$.  
With nodal representation we mean that the degrees of freedom (the control points) are associated to a node, an interpolation point, instead to an element. Furthermore, control points are divided into groups, based on which node they are auxiliary to (basically, which node they are close to, see illustration in next paragraph), and then are rewritten as the node they are associated to plus some vectors (which are the new degrees of freedom): $\mathbf{P}\_{ij} = \mathbf{P}\_{00} + \sum_l c_l \vec{u}^l$.

When the degree $n$ is odd, each group has $(n+1)^2/4$ points. The nodal representation is not defined in JOREK for $n$ even.  
The vectors used to construct all auxiliary control points of a node $\mathbf{P}\_{00}$ form a vectorial basis local to the node.

In the following of this section we provide an example with bi-cubic Bezier finite element, which is the most used finite element in JOREK. 
Next we discuss about the **generalized nodal representation** to any polynomial order, not only bi-cubic, that is implemented in JOREK and we
show that $G_m$ continuity is simpler to be imposed on such a representation.
Finally we provide an insight on why this particular formulation is chosen and is meaningful.

#### Nodal representation of bi-cubic Bezier finite element
This formulation is based on the following work: [O. Czarny, G. Huysmans, J.Comput.Phys 227, 7423 (2008)](https://www.sciencedirect.com/science/article/pii/S0021999108002118).

With bi-cubic Bezier finite element the Bernstein polynomials' basis is a cartesian product of the cubic Bernstein polynomials' basis. 

The control points are divided in 4 groups as shown in the following illustration with 4 different colors:

$$
\begin{matrix}
\color{red}{30}      &&& \color{red}{31}      &&& \color{green}{32}      &&& \color{green}{33} \\
\color{red}{\times} &&& \color{red}{\bullet} &&& \color{green}{\bullet} &&& \color{green}{\times} \\ \\
\color{red}{20}      &&& \color{red}{21}      &&& \color{green}{22}      &&& \color{green}{23} \\
\color{red}{\bullet} &&& \color{red}{\bullet} &&& \color{green}{\bullet} &&& \color{green}{\bullet} \\ \\
10      &&& 11      &&& \color{blue}{12}      &&& \color{blue}{13} \\
\bullet &&& \bullet &&& \color{blue}{\bullet} &&& \color{blue}{\bullet} \\ \\
00      &&& 01      &&& \color{blue}{02}      &&& \color{blue}{03} \\
\times &&& \bullet &&& \color{blue}{\bullet} &&& \color{blue}{\times} \\ \\
\end{matrix}
$$

Where the $\times$ indicate a node (an interpolation point) and $\bullet$ non-interpolating control points

Then for each group $i$ the vectors $p_i, v_i, u_i$ and $w_i$ are introduced along with 
certain pre-defined quantities $h_{u,i}$ and $h_{v,i}$

$$
\begin{align}
\mathbf{P}_{0,0} &= p_1 \
\mathbf{P}_{0,1} &= p_1 + v_1\, h_{v,1} \\
\mathbf{P}_{1,0} &= p_1 + u_1\, h_{u,1} \\
\mathbf{P}_{1,1} &= P_{0,1} + P_{1,0} - p_1 + w_1\, h_{w,1} \\ \\
\mathbf{P}_{3,0} &= p_2 \\
\mathbf{P}_{3,1} &= p_2 + v_2\, h_{v,2} \\
\mathbf{P}_{2,0} &= p_2 + u_2\, h_{u,2} \\
\mathbf{P}_{2,1} &= P_{3,1} + P_{2,0} - p_2 + w_2\, h_{w,2} \\ \\
\mathbf{P}_{3,3} &= p_3 \\
\mathbf{P}_{3,2} &= p_3 + v_3\, h_{v,3} \\
\mathbf{P}_{2,3} &= p_3 + u_3\, h_{u,3} \\
\mathbf{P}_{2,2} &= P_{2,3} + P_{3,2} - p_3 + w_3\, h_{w,3} \\ \\
\mathbf{P}_{0,3} &= p_4 \\
\mathbf{P}_{0,2} &= p_4 + v_4\, h_{v,4} \\
\mathbf{P}_{1,3} &= p_4 + u_4\, h_{u,4} \\
\mathbf{P}_{1,2} &= P_{0,2} + P_{1,3} - p_4 + w_4\, h_{w,4}
\end{align}
\tag{4}
$$

In particular, when patching together multiple Bezier finite elements, except for special points (grid axis and x point) or the boundary, each node will be shared by $4$ elements. 
Instead of viewing the _amount of DoF per element_ we look at the _amount of DoF per node_. So instead of the previous illustration, which is useful only to introduce the division of DoF in groups, the following one, centered on one node $\mathbf{P}\_{00}$ where 4 finite elements are glued together, reflects better the formalism used:

$$
\begin{matrix}
\text{-11}      &&& \text{01}      &&& \text{11}      \\ 
\bullet &&& \bullet &&& \bullet  \\ 
\text{-10}      &&& \text{00}      &&& \text{10}      \\ 
\bullet &&& \times &&& \bullet  \\ 
\text{-11} &&& \text{0-1}      &&& \text{1-1}      \\ 
\bullet &&& \bullet &&& \bullet  \\ 
\end{matrix}
$$

In the above illustration, $G_0$ continuity is assumed, indeed the 4 "glued" finite elements share the same control points on the edges (and hence the same edges).

We call $\xi_{11}$ the finite element on the top right of $P_{00}$, $\xi_{-11}$ the one on the top left, $\xi_{-1-1}$ the one on the bottom left and $\xi_{1-1}$ the one on the bottom right.



#### Generalized nodal representation of Bezier finite element
The work [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub) generalizes what has been shown in the previous paragraph for bi-cubic elements to any degree $n$ and always imposing $G_m$ continuity with $m=(n-1)/2$.
Instead of using $p_i,u_i,v_i,w_i$ vectors, the notation is $u_{ij}$ and $h_{u,i}$ are replaced with $h^{ij}$ For example, in the bi-cubic case we have $u_{i0}:=p_i, u_{i1}:=u_i, ...$. 
Then the generalized formulation, only for group of node $\mathbf{P}_{00}$, reads as follows:

$$
\mathbf{P}_{ij} = h^{ij}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{kl} \tag{5}
$$

with $0\leq i,j \leq (n+1)/2$

Technically this formulation is only for the element of 1 of the 4 glued patches sharing $\mathbf{P}\_{00}$, that is for element $\xi_{11}$.
See [Appendix A](#appendix-a-full-generic-nodal-formulation) to see the formulation also for $\xi_{-1-1}$, $\xi_{-11}$, $\xi_{1-1}$.


#### <u>Imposing the continuity on generalized nodal representation</u>
$G_m$ continuity on the shared nodes is obtained by imposing the following constrains.

$\forall j, \ \ h^{-ij}$ is constrained by:
$$
h^{-ij} = 
\begin{cases}
-\alpha h^{ij} & \text{for } i = 1 \text{ and } \alpha > 0 \\
h^{ij} & for i \neq 1
\end{cases} \tag{6a}
$$

$\forall i, \ \ h^{i-j}$ is constrained by:

$$
h^{i-j} = 
\begin{cases}
-\beta h^{ij} & \text{for } j = 1 \text{ and } \beta > 0 \\
h^{ij} & for j \neq 1
\end{cases} \tag{6b}
$$

where negative indexes are used to indicate sizes of elements $\xi_{-11}$ or $\xi_{1-1}$ or $\xi_{-1-1}$. For example $h^{-21}$ would belong to $\xi_{-11}$ ("first negative, second positive").

See [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub) for the derivation.

#### <u>Brief intuition on the formulation</u>
As demonstrated in Corollary 1 of [S. Pamela et al. J. Comput. Phys. 464, 111101 (2022)](https://www.sciencedirect.com/science/article/pii/S0021999122001632?via%3Dihub), in the particular nodal formulation used, the vectors $u^{ij}$ are **equal** in direction and sign (but not absolute value) with the **derivative** 

$$
\frac{\partial^{i+j} \mathbf{P}}{\partial^{i} s \partial^{j} t}(s=0,t=0)
$$

This is extremely helpful, for instance, when building the mesh, since derivatives of $R$ and $Z$ are used to obtain a flux aligned grid.

### Finite element basis with nodal formulation
Nodal formulation, as shown in the previous paragraph, refers to associating the degrees of freedom (the control points) to a node instead of an element.
Furthermore, control points are rewritten as the node they are associated to plus some vectors (which are the new degrees of freedom). 
This change in the representation of degrees of freedom (from control point to vectors local to one node) implies that formulation $(3)$ has to change and in particular the basis $\{B_i^n(s)B_j^n(t) \}_{i,n=0\dots n}$, associated to the control points, needs to be substituted by a basis associated to vectors $\vec{u}^{ij}$. 
This is obtained by rewriting $(5)$ such that on the right-hand side no $\mathbb{P}\_{xy}$ appears, so that each $\mathbb{P}\_{ij}$ depends uniquely on $h^{xy}$ and $\vec{u}^{xy}$, then substituting this result in $(3)$ and grouping on $\vec{u}^{ij}$. 

The new formulation for an element $K$ reads:

$$
X_{\text{pol}}^{(K)} = \sum_{i=0}^{\text{n_vertices}} \sum_{j=0}^{\text{n_degrees}} h^{ij}\vec{u}^{ij} b_{ij}^n(s,t) \tag{7}
$$

In the cubic case the following basis is obtained:
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
\tag{8}
$$



### True degrees of freedom, sizes and separation of geometrical coordinates from physical variables
When using Bezier surfaces of degree $n$ and with $\mathbf{P} \in \mathbb{R}^{d}$, each vertex has a basis of $\left(\frac{n+1}{2}\right)^2$ vectors (ex: with $n=3$, 4 vectors). 
Theoretically every entry of $\vec{u}^{ij}$ is a degree of freedom , so the total number of theoretical degrees of freedom is $d$ times the number of vectors.

However spatial coordinates $R$ and $Z$, corrisponding to the first two entries of $\vec{u}^{ij}$, are **fixed** when **building the mesh**. 
So the true number of degrees of freedom is
$$
N_{\text{dof}} = (d-2)\left(\frac{n+1}{2}\right)^2
$$

When building the mesh also the values of the sizes $h^{ij}$ are determined. 

This difference between the use of Bezier curves for geometrical coordinates and for physical coordinates implies that it makes sense to have two separate formulations:

$$
X_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{u}^{ij} b_{ij}(s,t)
$$

and

$$
\begin{pmatrix} R \\ Z
\end{pmatrix}
_\text{pol}^{(K)}(s,t) = \sum_{i=0}^{N_\text{vert}-1} \sum_{j=0}^{\text{dof_per_vertex}} h^{ij} \vec{v}^{ij} b_{ij}(s,t)
$$

Note that $h^{ij}$ and $b_{ij}$ are the same for both formulations! A formulation that has the same basis $\{b_{ij}}$ for both geometical and physical variables is called **isoparametric**.


## Appendix A: full generic nodal formulation
The generic nodal formulation introduced in a [previous paragraph](#generalized-nodal-representation-of-bezier-finite-element) expresses only the control points of element $\xi_{11}$. To represent control points of elements $\xi_{-1-1}$, $\xi_{-11}$, $\xi_{1-1}$, the formulation is basically the same but negative index must be handled. It is fundamental to note that sizes ($h^{ij}$) will vary (they are element-dependent) but the basis vectors $\vec{u}^ij$ will be the same across all 4 elements. 

Formulation for $\xi_{11}$ (same as [previous paragraph](#generalized-nodal-representation-of-bezier-finite-element)):
$$
\mathbf{P}_{ij} = h^{ij}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{kl}
$$ 
with $0\leq i,j \leq (n+1)/2$

Formulation for $\xi_{-11}$:
$$
\mathbf{P}_{-ij} = h^{-ij}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{-kl}
$$ 
with $0\leq i,j \leq (n+1)/2$

Formulation for $\xi_{-1-1}$:
$$
\mathbf{P}_{-i-j} = h^{-i-j}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{-k-l}
$$ 
with $0\leq i,j \leq (n+1)/2$

Formulation for $\xi_{1-1}$:
$$
\mathbf{P}_{i-j} = h^{i-j}\vec{u}^{ij} + \sum_{k=0}^i\sum_{l=0}^j (-1)^{1+i+j+k+l}(1-\delta_{ki}\delta_{lj}) 
\begin{pmatrix}
i \\ k
\end{pmatrix}
\begin{pmatrix}
j \\ l
\end{pmatrix}
\mathbf{P}_{k-l}
$$ 
with $0\leq i,j \leq (n+1)/2$