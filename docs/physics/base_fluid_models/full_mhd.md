---
title: "Tokamak Full MHD"
nav_order: 2
parent: "Base Fluid Models"
grand_parent: "Physics Models"
layout: default
render_with_liquid: false
---

# JOREK Full MHD Model

Refer also to the [models](./base_fluid_models.md), [coordinates](../coordinates.md), [notation](../notation.md), and [normalization](../normalization.md) pages.

The full MHD model in JOREK was originally implemented by [J.W. Haverkort et al., J. Comput. Phys. 316, 281–302 (2016)](https://doi.org/10.1016/j.jcp.2016.04.007), which describes the visco-resistive MHD equations, the Weyl gauge formulation, the finite-element weak-form discretization, and benchmarks against the internal kink mode, tearing mode, and ballooning mode. The model was subsequently extended with diamagnetic rotation, neoclassical friction, neutral-beam injection sources, and Mach-1/sheath boundary conditions in [S.J.P. Pamela et al., Phys. Plasmas 27, 102510 (2020)](https://doi.org/10.1063/5.0018208).

Unlike the [reduced MHD](./reduced_mhd.md) model, which assumes the toroidal magnetic field is constant in time and the perpendicular velocity is approximately poloidal, the full MHD model evolves **all three components** of the magnetic vector potential $\mathbf{A}$ and the velocity field $\mathbf{v}$ without these simplifying assumptions. This allows the full MHD model to capture physics that reduced MHD cannot, such as:

- Parallel magnetic field fluctuations ($\delta B_\parallel$)
- Fast magneto-sonic waves
- Finite-$\beta$ effects on internal kink modes
- More accurate modeling of spherical tokamak instabilities

The available full MHD models are summarized below (see also the [models overview](./base_fluid_models.md)):

| Model | $A_3$ | $A_R$ | $A_Z$ | $V_R$ | $V_Z$ | $V_\phi$ | $\rho$ | $T$ | $T_i$ | $T_e$ | $\rho_n$ | $\rho_{\text{imp}}$ |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **model710** | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | | | | |
| **model711** | 1 | 2 | 3 | 4 | 5 | 6 | 7 | | 8 | 9 | | |
| **model712** | 1 | 2 | 3 | 4 | 5 | 6 | 7 | | 8 | 9 | 10 | |
| **model750** | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |

## Magnetic Field

In order to ensure that the magnetic field satisfies Gauss's law $\nabla\cdot\mathbf{B}=0$ exactly, the magnetic field is defined as

$$\begin{equation}
  \mathbf{B} = \frac{F}{R}\,\mathbf{e}_\phi + \nabla\times\mathbf{A}
\end{equation}$$

where $\mathbf{A}$ is the magnetic vector potential and $F = F(\psi)$ is a **toroidally axisymmetric equilibrium function**, defined to satisfy the initial Grad–Shafranov equilibrium ($\psi$ is the poloidal magnetic flux). $F$ is **constant in time**, and thus the evolution of the toroidal magnetic field is determined by $\mathbf{A}$ alone.

**Note:** This differs from the reduced MHD definition of $B_\phi = F_0/R$, where $F_0$ is constant both in space and time. In the full MHD formulation, $F(\psi)$ may vary radially, encoding the equilibrium toroidal field profile, but is fixed in time.

The formulation ensures $\nabla\cdot\mathbf{B}=0$ exactly, without any approximation, since $\nabla\cdot\mathbf{B}$ involves derivatives of $\mathbf{A}$ only up to second order, which are well defined in the bi-cubic finite elements used by JOREK.

## Variable Decomposition

The magnetic vector potential, velocity field, and magnetic field are decomposed along the cylindrical basis vectors $(\mathbf{e}_R, \mathbf{e}_Z, \mathbf{e}_\phi)$:

$$\begin{align}
  \mathbf{A} &= A_R\,\mathbf{e}_R + A_Z\,\mathbf{e}_Z + \frac{1}{R}A_3\,\mathbf{e}_\phi \\[4pt]
  \mathbf{v} &= V_R\,\mathbf{e}_R + V_Z\,\mathbf{e}_Z + V_\phi\,\mathbf{e}_\phi \\[4pt]
  \mathbf{B} &= B_R\,\mathbf{e}_R + B_Z\,\mathbf{e}_Z + B_\phi\,\mathbf{e}_\phi
\end{align}$$

The variables $A_R$, $A_Z$, $V_R$, $V_Z$, $V_\phi$, $B_R$, $B_Z$, $B_\phi$ denote the **physical cylindrical components** (projections onto the normalized basis vectors $\mathbf{e}_R$, $\mathbf{e}_Z$, $\mathbf{e}_\phi$). The physical toroidal component of $\mathbf{A}$ is therefore $A_\phi^{\text{phys}} = A_3/R$.

This gives a direct mapping to the reduced-MHD formulation:

$$\begin{equation*}
  \psi \equiv R^2\,\mathbf{A}\cdot\nabla\phi = R\,A_\phi^{\text{phys}}
\end{equation*}$$

The toroidal velocity $V_\phi$ and magnetic field $B_\phi$ are stored directly as physical components, i.e. $\mathbf{v}\cdot\mathbf{e}_\phi = V_\phi$ and $\mathbf{B}\cdot\mathbf{e}_\phi = B_\phi$, without any metric factor.

If an external electric field is applied (e.g., via a loop-voltage boundary condition), $A_3$ undergoes a rigid temporal shift in the axisymmetric equilibrium, while the normalized flux $\psi_N = (\psi - \psi_{\text{axis}})/(\psi_{\text{bnd}} - \psi_{\text{axis}})$ remains stationary.

### Projection Strategy

The **induction equation** is projected along the vectors $(\mathbf{e}_R, \mathbf{e}_Z, \mathbf{e}_\phi)$.

The **momentum equation** is projected along the vectors $(\mathbf{e}_R, \mathbf{e}_Z, \mathbf{B})$. As noted in the original paper, this choice of projection is **essential for numerical stability**: by removing the $\mathbf{J}\times\mathbf{B}$ term from the equation for $V_\parallel$, the $\mathbf{B}$-projection removes unnecessary fast magneto-sonic wave components that would otherwise pollute the solution.

## Choice of Gauge

The starting point is Ohm's law combined with Faraday's law $\partial_t\mathbf{B} = -\nabla\times\mathbf{E}$. Writing $\mathbf{B} = \nabla\times\mathbf{A}$ and $\mathbf{E} = -\mathbf{v}\times\mathbf{B} + \eta\mathbf{J}$, uncurling Faraday's law gives

$$\begin{equation}
  \frac{\partial\mathbf{A}}{\partial t} = \mathbf{v}\times\mathbf{B} - \eta\mathbf{J} - \nabla\Phi
\end{equation}$$

where $\Phi$ is the electric potential. The curl operator annihilates the gradient $\nabla\Phi$, so the information about $\Phi$ is lost in the curl operation and a choice of gauge is necessary.

Since the magnetic and electric fields are invariant under the gauge transformation $\mathbf{A}' = \mathbf{A} + \nabla W$, $\Phi' = \Phi - \partial_t W$ (for any scalar function $W$), the full MHD model adopts **Weyl's gauge**: the gauge-transformed potential is set to zero ($\Phi' = 0$), which implies that the original electric potential satisfies

$$\begin{equation}
  \Phi = \partial_t W
\end{equation}$$

This simplifies the induction equation to $\partial_t\mathbf{A}' = \mathbf{v}\times\mathbf{B} - \eta\mathbf{J}$ (dropping the prime). In practice, if an external electric field is applied to the plasma, the magnetic vector potential will shift in time (even in the stationary equilibrium state).

## Governing Equations

The full system of extended MHD equations, including diffusion, sources, and rotation effects, is as follows.

### Induction Equation

$$\begin{equation}
  \frac{\partial\mathbf{A}}{\partial t} = \mathbf{v}\times\mathbf{B}
    + \frac{m_i}{2e\rho}\nabla_\parallel p
    - \eta\,\bigl(\mathbf{J} - \mathbf{S}_J\bigr)
\end{equation}$$

where $\eta$ is the resistivity, $\mathbf{J} = \nabla\times\mathbf{B}$ is the current density, and the second term on the RHS represents the **diamagnetic contribution** (with $m_i$ and $e$ being the ion mass and charge). The current source $\mathbf{S}_J$ has the dimensions of a current density and keeps the current profile steady for long simulations; it also includes the bootstrap current source, which evolves as a function of the pressure gradient.

In the weak-form implementation, the resistive term $-\eta\,\mathbf{J}$ is integrated by parts to avoid second-order derivatives of $\mathbf{A}$, which would otherwise introduce noise from fast magneto-sonic waves. A detailed derivation of the integration by parts for each cylindrical component is given on the [weak-form resistive term page](./full_mhd_eta_terms.md).

The diamagnetic term is obtained using standard drift ordering, assuming $p_e \approx p/2$ for a single-temperature model (710), and neglecting the perpendicular force balance $m_i(\mathbf{J}\times\mathbf{B} - \nabla_\perp p)/(e\rho)$ (i.e., Hall effects).

In the implementation described by Pamela et al., the diamagnetic terms are neglected in the $A_R$ and $A_Z$ equations for numerical stability, while the dominant toroidal component is retained.

### Momentum Equation

$$\begin{equation}
  \rho\frac{\partial\mathbf{v}}{\partial t}
    = - \rho\bigl(\mathbf{v} + \mathbf{v}_i^*\bigr)\cdot\nabla\mathbf{v} + \mathbf{J}\times\mathbf{B} - \nabla p
    + \mu\nabla^2\bigl(\mathbf{v} - \mathbf{S}_{\mathrm{NBI}}\bigr)
    + \nabla\cdot\mathbf{P}_{\mathrm{neo}}
    - C_\rho\mathbf{v}
\end{equation}$$

where:

- $\mathbf{v}_i^*$ is the **ion diamagnetic velocity** (see [below](#diamagnetic-and-neoclassical-effects))
- $\mu$ is the viscosity (with Spitzer-like temperature dependence $\mu = \mu_0 T^{-3/2}$)
- $\mathbf{S}_{\mathrm{NBI}}$ represents the neutral-beam-injection velocity source profile
- $\mathbf{P}_{\mathrm{neo}}$ is the neoclassical poloidal friction tensor (see [below](#diamagnetic-and-neoclassical-effects))
- $-C_\rho\,\mathbf{v}$ accounts for the diffusion and source terms from the continuity equation carried into the momentum equation, with $C_\rho = \nabla\cdot(D_\perp\nabla_\perp\rho + D_\parallel\nabla_\parallel\rho) + S_\rho$

### Continuity Equation

$$\begin{equation}
  \frac{\partial\rho}{\partial t}
    = -\nabla\cdot\bigl(\rho(\mathbf{v} + \mathbf{v}_i^*)\bigr)
    + \nabla\cdot\bigl(D_\perp\nabla_\perp\rho + D_\parallel\nabla_\parallel\rho\bigr)
    + S_\rho
\end{equation}$$

where $D_\perp$ and $D_\parallel$ are the perpendicular and parallel particle diffusion coefficients, and $S_\rho$ is a particle source (e.g., to model pellet injection or to balance diffusive losses).

### Energy Equation

$$\begin{equation}
  \frac{\partial p}{\partial t}
    = -\mathbf{v}\cdot\nabla p
    - \gamma p\,\nabla\cdot\mathbf{v}
    + \nabla\cdot\bigl(\kappa_\perp\nabla_\perp T + \kappa_\parallel\nabla_\parallel T\bigr)
    + S_T
\end{equation}$$

where $\gamma = 5/3$ (monatomic gas), $\kappa_\perp$ and $\kappa_\parallel$ are the perpendicular and parallel thermal conductivities, and $S_T$ is a heating source. The total pressure is $p = \rho T$.

The parallel thermal conductivity follows the Braginskii model: $\kappa_\parallel = \kappa_0 T^{5/2}$, where $\kappa_0$ has well-defined physical amplitudes for ion and electron temperatures. Since the single-temperature models (model710) only include one temperature, $\kappa_0$ is typically chosen as the average of the ion and electron coefficients.

### Parallel and Perpendicular Gradient Operators

$$\begin{align}
  \nabla_\parallel &= \frac{1}{B^2}\,\mathbf{B}\,\mathbf{B}\cdot\nabla \\[4pt]
  \nabla_\perp &= \nabla - \nabla_\parallel
\end{align}$$

## Diamagnetic and Neoclassical Effects

### Ion Diamagnetic Velocity

$$\begin{equation}
  \mathbf{v}_i^* = \frac{m_i}{2e\rho B^2}\,\mathbf{B}\times\nabla p
\end{equation}$$

Note the factor $2$ in the denominator comes from the assumption that, with a single total temperature $T$, the ion pressure is $p_i \approx p/2$.

### Neoclassical Poloidal Friction

$$\begin{align}
  \nabla\cdot\mathbf{P}_{\mathrm{neo}} &= \mu_{\mathrm{neo}}\,\rho\,\frac{B^2}{B_\theta^2}\,(v_\theta - v_{\mathrm{neo}})\,\mathbf{e}_\theta \\[4pt]
  v_{\mathrm{neo}} &= -\frac{\kappa_i m_i}{2e B_\theta}\,(\nabla T\times\mathbf{B})\cdot\mathbf{e}_\theta
\end{align}$$

where $\mathbf{e}_\theta = \mathbf{B}_\theta / |\mathbf{B}_\theta|$ is the unit vector along the poloidal magnetic field $\mathbf{B}_\theta = B_R\mathbf{e}_R + B_Z\mathbf{e}_Z$, $\mu_{\mathrm{neo}}$ is the neoclassical friction coefficient, $\kappa_i$ is the neoclassical heat diffusivity, and $v_\theta$ is the poloidal velocity $v_\theta = (\mathbf{v} + \mathbf{v}_i^*)\cdot\mathbf{e}_\theta$.

### Gyro-viscous Cancellation

The diamagnetic effects are implemented taking into account the **gyro-viscous cancellation** and the **gyro-viscous heat-flux cancellation**, which eliminate several diamagnetic terms in the momentum and energy equations. This cancellation assumes a constant magnetic field (the common simplified form), not the full form involving the magnetization velocity.

## Diffusion Coefficients and Sources

Both the resistivity and viscosity have a Spitzer-like dependence on temperature:

$$\begin{equation}
  \eta = \eta_0\,T^{-3/2}, \qquad \mu = \mu_0\,T^{-3/2}
\end{equation}$$

where $\eta_0$ and $\mu_0$ are the values on the magnetic axis.

Radial profiles for the perpendicular diffusion coefficients $D_\perp$ and $\kappa_\perp$ can be used to mimic cross-field kinetic turbulent transport, which is important for H-mode scenarios where transport is strongly reduced in the pedestal region. Two approaches are available for maintaining background profiles:

1. **Constant flux**: $D_\perp(\psi) \propto (\partial\rho/\partial\psi)^{-1}$ so that a spatially constant source sustains the profile.
2. **Arbitrary profile**: the particle source $S_\rho$ must be spatially adapted to compensate for radially varying diffusive losses.

At present, numerical (hyper-) diffusion is **not needed** in the full MHD model, even for strongly non-linear cases.

## Boundary Conditions

Two types of boundary conditions are used:

| Boundary type | Conditions |
| --- | --- |
| **Flux-surface aligned** | Dirichlet (all variables fixed in time); can be relaxed for density and temperature |
| **Intersecting field lines** | Dirichlet for $\mathbf{A}$; Neumann (free outflow) for density; Mach-1 and sheath boundary conditions for velocity and temperature |

The **Mach-1 boundary condition** for velocity:

$$\begin{equation}
  v_\parallel = \mathbf{v}\cdot\hat{\mathbf{b}} = \pm c_s = \pm\sqrt{\gamma T}
\end{equation}$$

The **sheath boundary condition** for temperature:

$$\begin{equation}
  n T\,v_\parallel + \kappa_\parallel\nabla_\parallel T
    = \gamma_{\mathrm{sh}}\,n T\,v_\parallel
\end{equation}$$

Equivalently, $\kappa_\parallel\nabla_\parallel T = (\gamma_{\mathrm{sh}} - 1)\rho T\,v_\parallel$, where $\gamma_{\mathrm{sh}}$ is the ion sheath transmission factor, typically between 4.5 and 10.0.

## Normalization

The equations are normalized using two constants: vacuum permeability $\mu_0$ and central density $\rho_0$. This is similar to the Alfvén time normalization: for a deuterium plasma with central particle density $n_0 \approx 6 \times 10^{19}\,\mathrm{m}^{-3}$, a normalized time unit corresponds to approximately $0.5\,\mu\mathrm{s}$.

This is a **pseudo-normalization**: not all variables are dimensionless in the final formulation. In particular, the **magnetic field is not normalized**.

## Comparison with Reduced MHD

| Aspect | Reduced MHD | Full MHD |
| --- | --- | --- |
| Magnetic field evolution | $\psi$ only (poloidal flux) | $A_R$, $A_Z$, $A_3$ (full vector potential) |
| Toroidal field $B_\phi$ | Fixed ($F_0/R$) | Evolves via $A_R$, $A_Z$ |
| Velocity | $u$ (stream function) + $v_\parallel$ | $V_R$, $V_Z$, $V_\phi$ |
| $\nabla\cdot\mathbf{B}=0$ | Satisfied analytically | Satisfied exactly via vector potential |
| Parallel field fluctuations | Not captured | Captured ($\delta B_\parallel$) |
| Fast magneto-sonic waves | Removed | Partially present (filtered by $\mathbf{B}$-projection) |
| Finite-$\beta$ kink modes | Deviates at finite $\beta$ | Accurate |

## References

1. J.W. Haverkort, H.J. de Blank, G.T.A. Huysmans, J. Pratt, B. Koren, *Implementation of the full viscoresistive magnetohydrodynamic equations in a nonlinear finite element code*, [J. Comput. Phys. 316, 281–302 (2016)](https://doi.org/10.1016/j.jcp.2016.04.007).
2. S.J.P. Pamela, A. Bhole, G.T.A. Huijsmans, et al., *Extended full-MHD simulation of non-linear instabilities in tokamak plasmas*, [Phys. Plasmas 27, 102510 (2020)](https://doi.org/10.1063/5.0018208).
3. E. Franck et al., [Part I: Document on two-fluid and single-fluid MHD](./assets/hierarchymhd.pdf).
4. E. Franck et al., [Part II: Document on reduced MHD](./assets/reduced_mhd.pdf).
