---
title: "Weak-Form Resistive Term in Full MHD"
nav_order: 16
parent: "Base Fluid Models"
grand_parent: "Physics Models"
layout: default
render_with_liquid: false
---

# Weak-Form Integration of the Resistive Term in Full MHD
# Introduction

This wiki explains how the resistive terms are integrated by parts in Full-MHD. The main reason for doing this is that it avoids 2nd order derivatives, which are noisy and numerically unstable due to fast-waves in Full-MHD.

The main issue with this is that, in principle, integration by parts comes with boundary terms, implemented in `mod_boundary_matrix_open.f90`, and these can be ignored as long as the variables in question, `AR`, `AZ`, and `A3`, are fixed at the boundary, i.e. Dirichlet boundary conditions. However, this is not the correct thing to do in Full-MHD, because `AR` and `AZ` should in principle remain free. Hence, we attempt to give a derivation of all terms here.

---

# Resistive term in weak form

The resistive term is described in the induction equation as

$$
\begin{aligned}
\partial_{t} \vec{A} &= \vec{v}\times\vec{B} - \eta\vec{J}, \\
\vec{B} &= B^R\vec{e}_R + B^Z\vec{e}_Z + B^{\phi}\vec{e}_{\phi}, \\
\vec{J} &= \nabla\times\vec{B} \\
&= \vec{e}_R \frac{1}{R} \left(RB^{\phi}_Z - B^Z_{\phi}\right)
+\vec{e}_Z \frac{1}{R} \left(B^R_{\phi} - RB^{\phi}_R - B^{\phi}\right)
+\vec{e}_{\phi} \left(B^Z_R - B^R_Z\right), \\
\vec{A} &= A^R\vec{e}_R + A^Z\vec{e}_Z + A^3\nabla\phi .
\end{aligned}
$$

Note that in JOREK, $\vec{B}$, like the velocity $\vec{u}$, is expressed with its physical component $B^{\phi}\vec{e}_{\phi}$, whereas the magnetic potential $\vec{A}$ is expressed with its geometrical component

$$
A^3\nabla\phi = \vec{e}_{\phi}\frac{A^3}{R},
$$

such that there is a correspondence between the $A^3$ of Full-MHD and the $\psi$ of reduced-MHD.

The above expression for $\vec{J}$ can be rearranged and expressed with divergence terms, which will make the integration by parts clearer later on. First, note that for a vector like $\vec{B}$, expressed with the physical toroidal component $B^{\phi}\vec{e}_{\phi}$, we have

$$
\nabla\cdot\vec{B}
=
\frac{1}{R}\partial_R \left(RB^R\right)

+ \partial_Z B^Z
+ \frac{1}{R}\partial_{\phi}B^{\phi}.
  $$

Therefore,

$$
\begin{aligned}
\vec{J} &= \vec{e}_R J^R + \vec{e}_Z J^Z + \vec{e}_{\phi}J^{\phi}, \\
J^R
&= \frac{1}{R} \left(RB^{\phi}_Z - B^Z_{\phi}\right)
= \nabla\cdot\left(B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}\right), \\
J^Z
&= \frac{1}{R} \left(B^R_{\phi} - RB^{\phi}_R - B^{\phi}\right)
= \nabla\cdot\left(B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R\right), \\
J^{\phi}
&= B^Z_R - B^R_Z
= R \nabla\cdot\left(\frac{1}{R}B^Z\vec{e}_R - \frac{1}{R}B^R\vec{e}_Z\right).
\end{aligned}
$$

Therefore, in weak form, with the test function $V$, and integrating over the volume $\Omega$, bounded by the surface $\xi$, the resistive term gives

$$
\begin{aligned}
\int_{\Omega} - V\eta\vec{J} d\Omega
&=
\int_{\Omega} - V\eta
\left(
J^R\vec{e}_R
+ J^Z\vec{e}_Z
+ J^{\phi}\vec{e}_{\phi}
\right)
d\Omega .
\end{aligned}
$$

---

# Integration by parts

We now proceed to integrate by parts each term from the projection along the three vectors $\vec{e}_R$, $\vec{e}_Z$, and $\vec{e}_{\phi}$. On the domain boundary $\xi$, we define the normal vector as

$$
\vec{n} = n^R\vec{e}_R + n^Z\vec{e}_Z .
$$

In JOREK, since the boundary of our domain is toroidally axisymmetric, although this may not be true for stellarator cases, it follows that

$$
\vec{n}\cdot\vec{e}_{\phi} = 0 .
$$

---

## Integration of the $\vec{e}_R$ term

$$
\begin{aligned}
&\int_{\Omega} - V\eta J^R d\Omega\\
&=
\int_{\Omega}

- V\eta
  \nabla\cdot
  \left(
  B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}
  \right)
  d\Omega \\
  &=
  \int_{\Omega}
- \nabla\cdot
  \left[
  V\eta
  \left(
  B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}
  \right)
  \right]
  d\Omega \\
  &\quad

+ \int_{\Omega}
  \nabla(V\eta)
  \cdot
  \left(
  B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}
  \right)
  d\Omega \\
  &=
  \int_{\xi}

- V\eta
  \left(
  B^{\phi}\vec{e}_Z - B^Z\vec{e}_{\phi}
  \right)
  \cdot \vec{n} d\xi \\
  &\quad

+ \int_{\Omega}
  \left[
  B^{\phi} \left(V_Z\eta + V\eta_Z\right)

  - \frac{1}{R} B^Z \left(V_{\phi}\eta + V\eta_{\phi}\right)
    \right]
    d\Omega \\
    &=
    \int_{\xi}

- V\eta B^{\phi}n^Z
  d\xi \\
  &\quad

+ \int_{\Omega}
  \left[
  B^{\phi} \left(V_Z\eta + V\eta_Z\right)

  - \frac{1}{R} B^Z \left(V_{\phi}\eta + V\eta_{\phi}\right)
    \right]
    d\Omega .
    \end{aligned}
    $$

Thus, in `mod_elt_matrix_fft.f90`, the RHS term needed is

```fortran
+ v * (eta_Z*Bp - eta_p*BZ/R)
+ eta * (v_Z*Bp - v_p*BZ/R)
```

while in `mod_boundary_matrix_open.f90`, the RHS term needed is

```fortran
- v * eta * Bp * normal(2)
```

---

## Integration of the $\vec{e}_Z$ term

$$
\begin{aligned}
&\int_{\Omega} - V\eta J^Z d\Omega\\
&=
\int_{\Omega}

- V\eta
  \nabla\cdot
  \left(
  B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R
  \right)
  d\Omega \\
  &=
  \int_{\Omega}
- \nabla\cdot
  \left[
  V\eta
  \left(
  B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R
  \right)
  \right]
  d\Omega \\
  &\quad

+ \int_{\Omega}
  \nabla(V\eta)
  \cdot
  \left(
  B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R
  \right)
  d\Omega \\
  &=
  \int_{\xi}

- V\eta
  \left(
  B^R\vec{e}_{\phi} - B^{\phi}\vec{e}_R
  \right)
  \cdot \vec{n}
   d\xi \\
  &\quad

+ \int_{\Omega}
  \left[
  \frac{1}{R} B^R \left(V_{\phi}\eta + V\eta_{\phi}\right)

  - B^{\phi} \left(V_R\eta + V\eta_R\right)
    \right]
    d\Omega \\
    &=
    \int_{\xi}
+ V\eta B^{\phi}n^R
  d\xi \\
  &\quad
+ \int_{\Omega}
  \left[
  \frac{1}{R} B^R \left(V_{\phi}\eta + V\eta_{\phi}\right)

  - B^{\phi} \left(V_R\eta + V\eta_R\right)
    \right]
    d\Omega .
    \end{aligned}
    $$

Thus, in `mod_elt_matrix_fft.f90`, the RHS term needed is

```fortran
+ v * (eta_p*BR/R - eta_R*Bp)
+ eta * (v_p*BR/R - v_R*Bp)
```

while in `mod_boundary_matrix_open.f90`, the RHS term needed is

```fortran
+ v * eta * Bp * normal(1)
```

---

## Integration of the $R\vec{e}_{\phi}$ term

Remember that the projection for the toroidal equation includes a factor $R$, so that the time-derivative term of $A^3$, i.e. $\psi$, reads as $\partial_t A^3$ in the code, instead of $\frac{1}{R}\partial_t A^3$, since

$$
\begin{aligned}
&\int_{\Omega} - V\eta J^{\phi} d\Omega\\
&=
\int_{\Omega}

- V\eta R^2
  \nabla\cdot
  \left(
  \frac{1}{R}B^Z\vec{e}_R

  - \frac{1}{R}B^R\vec{e}_Z
    \right)
    d\Omega \\
    &=
    \int_{\Omega}
- \nabla\cdot
  \left[
  V\eta R^2
  \left(
  \frac{1}{R}B^Z\vec{e}_R

  - \frac{1}{R}B^R\vec{e}_Z
    \right)
    \right]
    d\Omega \\
    &\quad

+ \int_{\Omega}
  \nabla(V\eta R^2)
  \cdot
  \left(
  \frac{1}{R}B^Z\vec{e}_R

  - \frac{1}{R}B^R\vec{e}_Z
    \right)
    d\Omega \\
    &=
    \int_{\xi}

- V\eta R
  \left(
  B^Z\vec{e}_R - B^R\vec{e}_Z
  \right)
  \cdot \vec{n}
   d\xi \\
  &\quad

+ \int_{\Omega}
  \left[
  B^Z
  \left(
  V_R\eta R + V\eta_R R + 2V\eta
  \right)

  - RB^R
    \left(
    V_Z\eta + V\eta_Z
    \right)
    \right]
    d\Omega \\
    &=
    \int_{\xi}
+ V\eta R
  \left(
  B^Z n^R - B^R n^Z
  \right)
   d\xi \\
  &\quad
+ \int_{\Omega}
  \left[
  B^Z
  \left(
  V_R\eta R + V\eta_R R + 2V\eta
  \right)

  - RB^R
    \left(
    V_Z\eta + V\eta_Z
    \right)
    \right]
    d\Omega .
    \end{aligned}
    $$

Finally, for clarity, we describe the RHS terms that are needed in JOREK, remembering that the $d\Omega$ volume integrand contains a factor $R$.

Thus, in `mod_elt_matrix_fft.f90`, the RHS term needed is

```fortran
+ v * R * (eta_R*BZ - eta_Z*BR)
+ eta * (2*v + R*v_R)*BZ
- eta * R * v_Z*BR
```

while in `mod_boundary_matrix_open.f90`, the RHS term needed is

```fortran
+ v * eta * R * BZ * normal(1)
- v * eta * R * BR * normal(2)
```

In practice, this term can be ignored because $A^3$ is fixed on the boundary. However, maybe these terms will need to be included for free-boundary cases.
