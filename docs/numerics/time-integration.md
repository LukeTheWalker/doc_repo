---
title: "Time Integration"
nav_order: 3
parent: "Numerics and Tools"
layout: default
render_with_liquid: false
---

# Time integration 

The time-integration of a set of equations of the form 

$$
\frac{\partial \mathbf{A(u)}}{\partial t} = \mathbf{B}(\mathbf{u},t) \tag{1}
$$

can be discretized by the general form  (refer to Beam80 and Hirsch91, Chapter 11.1)

$$
(1+\xi) \, \mathbf{A}^{n+1} - (1+2\xi) \, \mathbf{A}^{n} + \xi \, \mathbf{A}^{n-1}
= \Delta t \left[
\theta \, \mathbf{B}^{n+1}
+ (1 - \theta - \phi) \, \mathbf{B}^{n}
- \phi \, \mathbf{B}^{n-1}
\right] \tag{2}

$$

which guarantees second-order accuracy, if $\phi+\theta-\xi = 1/2$. Superscripts like $\mathbf{B}^n$ indicate at which timestep the corresponding expression is evalued.

The linearization 

$$
\mathbf{H}^{n+1} \approx \mathbf{H}^n + \left[ \frac{\partial \mathbf{H}}{\partial \mathbf{u}} \right]^n \cdot \, \delta \mathbf{u}^n \tag{3}
$$

where $\mathbf{H} = \mathbf{A}$ or $\mathbf{H} = \mathbf{B}$, which is described in Reference Hirsch91, Chapter 11.3, allows to rewrite Equation (2) in the following way, where $\phi = 0$ has been chosen.

$$
\begin{split}
  (1+\xi)\left[\mathbf{A}^n+\left(\frac{\partial \mathbf{A}}{\partial \mathbf{u}}\right)^n\delta\mathbf{u}^n\right]
    -(1+\xi)\mathbf{A}^n-\xi\mathbf{A}^n+\xi\mathbf{A}^{n-1} \\
    =\Delta t\left[\theta\left(\mathbf{B}^n+\left(\frac{\partial \mathbf{B}}{\partial \mathbf{u}}\right)^n\delta\mathbf{u}^n\right)
      +(1-\theta)\mathbf{B}^n\right] \tag{4}
\end{split}
$$

Here, 

$$
  \delta\mathbf{u}^n \equiv \mathbf{u}^{n+1}-\mathbf{u}^n \tag{5}
$$

After some simplifications, and using the backward linearization

$$
  \mathbf{H}^{n-1}\approx \mathbf{H}^n-\left[\frac{\partial \mathbf{H}}{\partial \mathbf{u}}\right]^n\cdot\delta\mathbf{u}^{n-1}, \tag{6}
$$

one obtains

$$
  \boxed{
    \left[(1+\xi)\left(\frac {\partial \mathbf{A}}{\partial \mathbf{u}}\right)^n-\Delta t\theta\left(\frac{\partial \mathbf{B}}{\partial \mathbf{u}}\right)^n\right]\delta\mathbf{u}^n
      =\Delta t\mathbf{B}^n+\xi\left(\frac{\partial \mathbf{A}}{\partial \mathbf{u}}\right)^n\delta\mathbf{u}^{n-1}
  }, \tag{7}
$$

which is the time-integration scheme implemented in JOREK. Certain parameter choices correspond to well-known time integration methods as listed in Table 1. The parameter $\xi$ is denoted ''zeta'' in the code.

| $\theta$ | $\xi$ | Method | input parameter `time_evol_scheme` |
|----------|------|--------|------------------------------------|
| 1/2 | 0 | **Crank-Nicolson scheme (default)** | `"Crank-Nicholson"` |
| 1 | 1/2 | **BDF2 (Gears) scheme** | `"Gears"` |
| 1 | 0 | Implicit Euler scheme (usually not used) | `"implicit Euler"` |

Explicitly, the terms $(\partial\mathbf{A}/\partial{\mathbf{u}})\cdot\delta\mathbf{u}$ and $(\partial\mathbf{B}/\partial{\mathbf{u}})\cdot\delta\mathbf{u}$ lead to the following transformations of expressions: 

$$
\begin{aligned}
  g                             &~~\rightarrow~~ \delta g               \\
  g^2                           &~~\rightarrow~~ 2\;g\;\delta g         \\
  g\;h                          &~~\rightarrow~~ g\;\delta h+h\;\delta g\\
  \frac{\partial g}{\partial x}                 &~~\rightarrow~~ \frac{\partial (\delta g)}{\partial x} \\
  \left(\frac{\partial g}{\partial x}\right)^2  &~~\rightarrow~~ 2\;\frac{\partial g}{\partial x}\;\frac{\partial (\delta g)}{\partial x}
\end{aligned} \tag{8}
$$

Here, $g$ and $h$ denote arbitrary variables and $x$ an arbitrary coordinate. For instance, $\partial j/\partial\phi$ turns into $\partial(\delta j)/\partial\phi$.

## Generalized equations

Consider a set of equations of the form

$$
\sum_i a_i(\mathbf{u},t)\frac{\partial \mathbf{A}_i( \partial\mathbf{u})}{t} = \mathbf{B}(\mathbf{u},t), \tag{9}
$$

where the $a_i$'s can in general be spatial differential operators. A discretization similar to (2) (with $\phi=0$) can be derived for such equations.

Consider first the explicit (forward) and implicit (backward) Euler schemes. In both cases, the time derivative $\partial\mathbf{A}/\partial t$ is replaced by the difference quotient $(\mathbf{A}^{n+1}-\mathbf{A}^n)/\Delta t$, with everything else being evaluated at time step $n$ for explicit Euler and time step $n+1$ for implicit Euler:

$$
\begin{aligned}
&\text{Explicit:}\qquad &&\sum_i a_i^n (\mathbf{A}_i^{n+1}-\mathbf{A}_i^n) = \Delta t\mathbf{B}^n, \\
&\text{Implicit:}\qquad &&\sum_i a_i^{n+1} (\mathbf{A}_i^{n+1}-\mathbf{A}_i^n) = \Delta t\mathbf{B}^{n+1}.
\end{aligned} \tag{10}
$$

The Crank-Nicolson scheme is simply an average of the two Euler schemes:

$$
\sum_i (\frac{1}{2}a_i^{n+1}+\frac{1}{2}a_i^n)(\mathbf{A}_i^{n+1}-\mathbf{A}_i^n) = \Delta t(\frac{1}{2}\mathbf{B}^{n+1}+\frac{1}{2}\mathbf{B}^n). \tag{11}
$$

On the other hand, the BDF2 scheme derives a second order approximation for the time derivative at time step $n+1$ by Taylor expanding $\mathbf{A}_i^n$ and $\mathbf{A}_i^{n-1}$ around $\mathbf{A}_i^{n+1}$:

$$
\mathbf{A}_i^n = \mathbf{A}_i^{n+1} - \Delta t\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} + \frac{(\Delta t)^2}{2}\left(\frac{\partial^2\mathbf{A}_i}{\partial t^2}\right)^{n+1} + ... \\
\mathbf{A}_i^{n-1} = \mathbf{A}_i^{n+1} - 2\Delta t\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} + 2(\Delta t)^2\left(\frac {\partial^2 \mathbf{A}_i}{\partial t^2}\right)^{n+1} + ... \tag{12}
$$

Solving both of the above expressions for the first order time derivative, one obtains

$$
\begin{aligned}
&(*)\qquad &&\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} = \frac{\mathbf{A}_i^{n+1}-\mathbf{A}_i^n+\frac{1}{2}\Delta t\left(\frac{\partial^2 \mathbf{A}_i}{\partial t^2}\right)^{n+1}}{\Delta t}, \\
&(**)\qquad &&\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} = \frac{\mathbf{A}_i^{n+1}-\mathbf{A}_i^{n-1}+2\Delta t\left(\frac{\partial^2 \mathbf{A}_i}{\partial t^2}\right)^{n+1}}{2\Delta t}.
\end{aligned} \tag{13}
$$

It follows that

$$
\left(\frac{\partial \mathbf{A}_i}{\partial t}\right)^{n+1} = a(*)+b(**) = \frac{(a+\frac{1}{2}b)\mathbf{A}_i^{n+1}-a\mathbf{A}_i^n-\frac{1}{2}b\mathbf{A}_i^{n-1}+(\frac{1}{2}a+b)\Delta t\left(\frac{\partial^2 \mathbf{A}_i}{\partial t^2}\right)^{n+1}}{\Delta t}, \tag{14}
$$

where $a+b=1$. To obtain second order accuracy, the condition $\frac{1}{2}a+b=0$ is imposed, resulting in $a=2$ and $b=-1$. Evaluating equation (9) at time step $n+1$ and substituting in the second order approximation for $\partial\mathbf{A}/\partial t$ at time step $n+1$, the BDF2 scheme is obtained:

$$
\sum_i a_i^{n+1} (\frac{3}{2}\mathbf{A}_i^{n+1}-2\mathbf{A}_i^n+\frac{1}{2}\mathbf{A}_i^{n-1}) = \Delta t\mathbf{B}^{n+1}. \tag{15}
$$

Generalizing equations (10), (11) and (15), one can write:

$$
\sum_i [\theta a_i^{n+1} + (1-\theta)a_i^n][(1+\xi)\mathbf{A}_i^{n+1} - (1+2\xi)\mathbf{A}_i^n + \xi\mathbf{A}_i^{n-1}] = \Delta t[\theta\mathbf{B}^{n+1} + (1-\theta)\mathbf{B}^n]. \tag{16}
$$

By plugging in the corresponding values for $\theta$ and $\xi$ from Table 1, the Crank-Nicolson, BDF2 and implicit Euler schemes can be recovered from equation (16).)

### References
  * **[Beam80]** Beam, R.M. and Warming, R.F. Alternating direction implicit methods for parabolic equations with a mixed derivative. SIAM Journal on Scientific and Statistical Computing, 1(1), 131 (1980). ISSN 01965204. [[http://dx.doi.org/10.1137/0901007|doi:10.1137/0901007]]
  * **[Hirsch91]**: Hirsch, C. Numerical computation of internal and external flows. Volume 1: Fundamentals of Numerical Discretization. J. Wiley, Chichester (1991). ISBN 9780471923855.


