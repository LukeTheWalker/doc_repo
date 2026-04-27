---
title: "Spatial Discretization"
nav_order: 1
parent: "Numerics and Tools"
layout: default
render_with_liquid: false
---

====== Spatial Discretization in JOREK ======

The discretization of JOREK is well described in the paper [[https://www.sciencedirect.com/science/article/pii/S0021999108002118|O. Czarny, G. Huysmans, J.Comput.Phys 227, 7423 (2008)]].

==== 2D Bezier finite elements in the poloidal plane ====

Two-dimensional third-order Bernstein polynomials $B_{i,j}^3(s,t)$ defined by
\begin{equation}\label{eq:BezierA}
  B_{i,j}^3(s,t)=B_i^3(s)\;B_j^3(t)\hspace{20mm}i,\;j\;=\;0\;\dots\;3,
\end{equation}
with
\begin{equation}\label{eq:BezierB}
  B_i^3(s)=\frac{3!}{i!(3-i)!}\;s^i (1-s)^{3-i}
\end{equation}
are used for the discretization in the poloidal plane. The
coordinates $s=0\dots1$ and $t=0\dots1$ form the element-local coordinate system. A
quantity $X$ which may be a coordinate or a physical variable
($R$, $Z$, $\Psi$, $T$, ...; iso-parametric discretization) can be expressed by
\begin{equation}\label{eq:Bezier1}
  X(s,t) = \sum_{i=0}^3 P_{i,j}\;B_{i,j}^3(s,t).
\end{equation}
As first order continuity of the finite elements is demanded, not all combinations
of control points $P_{i,j}$ are valid.
Effectively, four free parameters $p_k$, $u_k$, $v_k$, and $w_k$
remain per node $k$ and quantity $X$ of the element. The control points
$P_{i,j}$ can be reconstructed from these free parameters as given in the following.
Nodes $k=1\dots4$ correspond
to the positions $(i,j)=(0,0)$, $(3,0)$, $(3,3)$, and $(0,3)$.

\begin{equation}\begin{split}
  P_{0,0} &= p_1  \\
  P_{0,1} &= p_1 + v_1\;d_{v,1}  \\
  P_{1,0} &= p_1 + u_1\;d_{u,1}  \\
  P_{1,1} &= P_{0,1} + P_{1,0} - p_1 + w_1\;d_{u,1}\;d_{v,1} \\
  P_{3,0} &= p_2  \\
  P_{3,1} &= p_2 + v_2\;d_{v,2}  \\
  P_{2,0} &= p_2 + u_2\;d_{u,2}  \\
  P_{2,1} &= P_{3,1} + P_{2,0} - p_2 + w_2\;d_{u,2}\;d_{v,2} \\
  P_{3,3} &= p_3  \\
  P_{3,2} &= p_3 + v_3\;d_{v,3}  \\
  P_{2,3} &= p_3 + u_3\;d_{u,3}  \\
  P_{2,2} &= P_{2,3} + P_{3,2} - p_3 + w_3\;d_{u,3}\;d_{v,3} \\
  P_{0,3} &= p_4  \\
  P_{0,2} &= p_4 + v_4\;d_{v,4}  \\
  P_{1,3} &= p_4 + u_4\;d_{u,4}  \\
  P_{1,2} &= P_{0,2} + P_{1,3} - p_4 + w_4\;d_{u,4}\;d_{v,4}
\end{split}\label{eq:controlpts}\end{equation}

Here, the $d_{u,k}$ and $d_{v,k}$ are measures for the distances of the
control points from the element nodes. These are element properties, i.e.,
for a node that belongs to several elements, the value of $d_{u,k}$ depends
on the element considered. In JOREK, they are represented by
\begin{align*}
  \texttt{element%size(k,1)} &~~\rightarrow ~~1                \\
  \texttt{element%size(k,2)} &~~\rightarrow ~~d_{u,k}          \\
  \texttt{element%size(k,3)} &~~\rightarrow ~~d_{v,k}          \\
  \texttt{element%size(k,4)} &~~\rightarrow ~~d_{u,k}\;d_{v,k}.
\end{align*}

=== Projecting on the bezier elements ===
The distribution $X(s,t)$ of quantity $X$ within a certain element can be expressed
by Equation~\eqref{eq:Bezier1}. Inserting Equations \eqref{eq:BezierA}--\eqref{eq:BezierB} and
Equation \eqref{eq:controlpts} leads to the following
expression
\begin{equation}
  X(s,t) = \sum_{k=1}^4 \tilde{p}_k(s,t)
\end{equation}
with the contributions
\begin{equation}
  \tilde{p}_k = b_{k,1}\;p_k + b_{k,2}\;u_k\;d_{u,k} + b_{k,3}\;v_k\;d_{v,k} + b_{k,4}\;w_k\;d_{u,k}\;d_{v,k}
\end{equation}
associated to the four nodes. Here,
\begin{equation}\begin{split}
  b_{1,1}&= (1-s)^2\;(1-t)^2\;(1+2s)\;(1+2t)  \\
  b_{1,2}&=3(1-s)^2\;(1-t)^2\;s\;(1+2t)  \\
  b_{1,3}&=3(1-s)^2\;(1-t)^2\;(1+2s)\;t  \\
  b_{1,4}&=9(1-s)^2\;(1-t)^2\;s\;t \\
  b_{2,1}&= s^2\;(1-t)^2\;(3-2s)\;(1+2t)  \\
  b_{2,2}&=3s^2\;(1-t)^2\;(1-s)\;(1+2t)  \\
  b_{2,3}&=3s^2\;(1-t)^2\;(3-2s)\;t  \\
  b_{2,4}&=9s^2\;(1-t)^2\;(1-s)\;t \\
  b_{3,1}&= s^2\;t^2\;(3-2s)\;(3-2t)  \\
  b_{3,2}&=3s^2\;t^2\;(1-s)\;(3-2t)  \\
  b_{3,3}&=3s^2\;t^2\;(3-2s)\;(1-t)  \\
  b_{3,4}&=9s^2\;t^2\;(1-s)\;(1-t) \\
  b_{4,1}&= (1-s)^2\;t^2\;(1+2s)\;(3-2t)  \\
  b_{4,2}&=3(1-s)^2\;t^2\;s\;(3-2t)  \\
  b_{4,3}&=3(1-s)^2\;t^2\;(1+2s)\;(1-t)  \\
  b_{4,4}&=9(1-s)^2\;t^2\;s\;(1-t).
\end{split}\end{equation}

In JOREK, the quantities $b_{k,j}$ are required at the position of the Gaussian points
with indices $(i_G,j_G)$. They are denoted
\begin{equation}
  \texttt{H(k,j,$i_G$,$j_G$)} ~~\rightarrow ~~b_{k,j}~\text{at Gaussian point}~(i_G,j_G)
\end{equation}
and are initialized in the subroutine ''basisfunctions2''.

=== Notation in the code ===
The degrees of freedom of each node corresponding to the $l$-th toroidal harmonic of the
$\nu$-th physical quantity are denoted in the following way in the code:
\begin{align*}
  \texttt{node%values(l,1,}\nu\texttt{)} &~~ \rightarrow ~~p_k \\
  \texttt{node%values(l,2,}\nu\texttt{)} &~~ \rightarrow ~~u_k \\
  \texttt{node%values(l,3,}\nu\texttt{)} &~~ \rightarrow ~~v_k \\
  \texttt{node%values(l,4,}\nu\texttt{)} &~~ \rightarrow ~~w_k.
\end{align*}

The degrees of freedom of the coordinates $R$
($\mu=1$) and $Z$ ($\mu=2$) are called,
\begin{align*}
  \texttt{node%x(1,}\mu\texttt{)} &~~\rightarrow ~~p_k \\
  \texttt{node%x(2,}\mu\texttt{)} &~~\rightarrow ~~u_k \\
  \texttt{node%x(3,}\mu\texttt{)} &~~\rightarrow ~~v_k \\
  \texttt{node%x(4,}\mu\texttt{)} &~~\rightarrow ~~w_k.
\end{align*}


For all $\nu=1\dots N_{var}$ and $i_G,j_G=1\dots N_{Gauss}$ and $p=1\dots N_{plane}$, the
variable values at a given Gaussian point $(s_{i_G},t_{j_G})$ at the toroidal
position $\phi_p$ in a given finite element can be expressed by
\begin{equation}
\begin{split}
  X_\nu(s_{i_G},t_{j_G},\phi_p)=\sum_{k=1}^{N_{vert}}\sum_{j=1}^{N_{ord}}\sum_{l=1}^{N_{tor}}~
    &\texttt{nodes(i)%values(l,j,}\nu\texttt{)}    \\
    &\cdot\texttt{H(k,}j,i_G,j_G\texttt{)}
    \cdot\texttt{element%size(k,j)}
    \cdot\texttt{HZ(l,p)},
\end{split}
\end{equation}

where ''i=element%vertex(k)''. Here, $N_{var}$ denotes the number of physical variables,
$N_{Gauss}=4$ the number of Gaussian points used for Gauss quadrature in $s$ and $t$ directions
each, $N_{plane}=2(N_{tor}-1)$ the number of toroidal planes located at
$\phi_p=2\pi(p-1)/N_{plane}$, $N_{vert}=4$ the number of vertices in each element, $N_{ord}=4$
the number of degrees of freedom per vertex, and $N_{tor}$ the number of different toroidal
Fourier modes. The quantity ''HZ(l,p)'' corresponds to the value of the $l$-th Fourier
mode at the toroidal position $\phi_p$ and is denoted $Z_l(\phi_p)$ in the following.
The table below lists which Fourier modes
correspond to the different mode indices $l$.

^ l ^ 1 ^ 2 ^ 3 ^ 4 ^ 5 ^ ... ^
| $Z_l(\phi_p)\equiv\texttt{HZ(l,p)}$ | 1 | $\cos\phi_p$ | $\sin\phi_p$ | $\cos2\phi_p$ | $\sin2\phi_p$ | ... |


==== Real Fourier series in toroidal direction ====

  * For the toroidal direction, a real Fourier series (cos, sin) is used:

^ JOREK harmonic ^ Toroidal mode number ^ Toroidal basis function ^
| 1                      | 0                    | 1                       |
| 2                      | n_period             | cos(n_period*phi) |
| 3                      | n_period             | sin(n_period*phi) |
| 4                      | 2*n_period             | cos(2*n_period*phi) |
| 5                      | 2*n_period             | sin(2*n_period*phi) |
| ...                    | ...                  | ...               |
| n_tor-1                | (n_tor-1)/2*n_period | cos((n_tor-1)/2*n_period*phi) |
| n_tor                  | (n_tor-1)/2*n_period | sin((n_tor-1)/2*n_period*phi) |

  * The [[hard-coded_parameters]] ''n_tor'' and ''n_period'' are used to select the harmonics included in the simulation.
    * ''n_tor'': Total number of real Fourier modes (odd integer number)
    * ''n_period'': Toroidal periodicity (positive integer number)
  * The **maximum toroidal mode number** included in a simulation is ''n_max=(n_tor-1)/2*n_period''.
  * A **sufficient number of toroidal planes** is required to avoid aliasing. The minimal requirement is typically ''n_plane >= 2 * n_tor''. It is always a good idea to scan ''n_plane'' for a simulation to ensure convergence. ''n_plane'' must be a power of 2, if FFTW is not used. If FFTW is used (see [[compiling|the information about compiling]]) ''n_plane'' can be an arbitrary positive integer number, but not for all values FFTW is similarly efficient.
