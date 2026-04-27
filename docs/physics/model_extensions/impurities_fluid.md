---
title: "Impurities — Fluid Model"
nav_order: 1
parent: "Impurities"
grand_parent: "Model Extensions"
layout: default
render_with_liquid: false
---

# The impurity fluid model

These models contain a field (variable number 8 or var_rhoimp in the code) corresponding to the impurity density. This page applies to dedicated impurity models such as models 501/502, as well as thei modular general model 600.

Such models can be used for example for [SPI simulations](spi_tutorial) or [MGI simulations](mgi_tutorial).

## Models 501/502

**Important note:** At present, `tau_ic = 0.` should be set when using models 501/502, i.e. diamagnetic effects should not be included (they are not properly implemented).

### Definition of the variables

**Variable number 5:** In models 501/502, $\rho$ (variable number 5) is the **total** mass density, all species included (but neglecting the electron mass). That is:

\begin{aligned}
  \rho = \rho_i + \rho_{imp}
\end{aligned}

where $\rho_i$ is the main ion density and $\rho_{imp}$ is the impurity density, all charge states included.

**Pressure:** In models 501/502, the pressure that appears naturally in the energy and momentum equations is the **total** pressure $p$, all species included. In model 501, we assume that all species have a common temperature $T/2$. The pressure is therefore (with non-JOREK normalizations for the moment, to avoid confusions) $p=n_{tot}T/2$, where $n_{tot}$ is the total particle density: $n_{tot}=n_{i}+n_{e}+n_{imp}$. By quasi-neutrality we have $n_e=n_i+\langle Z \rangle_{imp}n_{imp}$. Therefore, $n_{tot}=2n_i+(\langle Z \rangle_{imp}+1)n_{imp}$. Now, $n_i=\rho_i/m_i$ and $n_{imp}=\rho_{imp}/m_{imp}$, so: $n_{tot}=[2\rho_i+\frac{(\langle Z \rangle_{imp}+1)m_i}{m_{imp}}\rho_{imp}]/m_i=[2\rho+(\frac{(\langle Z \rangle_{imp}+1)m_i}{m_{imp}}-2)\rho_{imp}]/m_i$. The pressure can therefore be expressed as (now in JOREK units):

\begin{aligned}
  p=(\rho+\alpha_{imp}\rho_{imp})T/m_{i}
\end{aligned}

where we define $\alpha_{imp} \equiv \frac{(\langle Z \rangle_{imp}+1)m_i}{2m_{imp}}-1$. Note that we will assume that $\langle Z \rangle_{imp}=\langle Z \rangle_{imp}(T)$, so that $\alpha_{imp}=\alpha_{imp}(T)$.

**Variable number 8:** In models 501/502, variable number 8 is $\rho_{imp}$, the impurity mass density, all charge states included.

### Normalizations

| Connection between SI and normalized units | | Description of the quantity / Comment |
|--------------------------------------------|------|----------------------------------------|
| $\rho_\mathrm{SI}~[\mathrm{kg/m^3}]$ | $=\rho\;\rho_0$ | Total mass density |
| $\rho_\mathrm{imp,SI}~[\mathrm{kg/m^3}]$ | $=\rho_\mathrm{imp}\;\rho_0$ | Impurity mass density |
| $n_\mathrm{i,SI}~[\mathrm{m^{-3}}]$ | $=(\rho - \rho_\mathrm{imp})\;n_0$ | Main ion number density |
| $n_\mathrm{imp,SI}~[\mathrm{m^{-3}}]$ | $=\rho_\mathrm{imp}\;n_0\;\mu_{imp}$ | Impurity number density |
| $n_\mathrm{e,SI}~[\mathrm{m^{-3}}]$ | $= n_\mathrm{i,SI}\;+\;\langle Z \rangle_{imp}\;n_\mathrm{imp,SI}$ | Electron number density |

**Having defined:**

| Symbol | Expression | Comment |
|--------|------------|---------|
| $n_0~[m^{-3}]$ | `central_density` $\cdot 10^{20}$ | `central_density` gets a default value in `preset_parameters.f90` and should be specified in the input file |
| $\rho_0~[kg\;m^{-3}]$ | `central_mass` $\cdot n_0 \cdot m_\text{AMU}$ | `central_mass` gets a default value in `preset_parameters.f90` and should be specified in the input file |
| $\mu_\mathrm{imp}~[1]$ | `m_i_over_m_imp` $ = m_\mathrm{i}/m_\mathrm{imp}$ | `m_i_over_m_imp` is defined by the impurity species. |

### Equations

<!--
- [Di's note](note501.pdf)
- [Di's note for model 502](note502.pdf)
- [Boniface's note](mgi_spi_premixed_modelingdiag.pdf)
-->

#### Vorticity equation (eq. 2)

The full MHD momentum equation reads:

\begin{aligned}
\rho (\partial_t + \mathbf{v} \cdot \nabla) \mathbf{v}  = \mathbf{j} \times \mathbf{B} - \nabla p + \nu \Delta \mathbf{v} - (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \mathbf{v} + S_{\rho_{imp}} \mathbf{v}_{imp}
\end{aligned}

where $\mathbf{v}_{imp}$ is the velocity of the impurities deposited by the $S_{\rho_{imp}}$ source term. Note the presence of the term $-(\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \mathbf{v}$ on the RHS. This term, which ensures momentum conservation, is not present in other JOREK models at the moment (21/08/18) but may be included in the future.

The reduced MHD vorticity equation is derived by applying the operator $\nabla\phi\cdot\nabla\times(R^2...)$ to the momentum equation. The result in the absence of the $-(\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \mathbf{v}$ term is presented [here](reduced_mhd). The $-(\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \mathbf{v}$ term yields an additional term $-\nabla \cdot \left[ R^2 (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \nabla_{pol} u \right] $ on the RHS of the vorticity equation (we neglect the contribution from $- (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) v_{||}\mathbf{B} $). In weak form, this term becomes $ \int - u^* \nabla \cdot \left[ R^2 (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \nabla_{pol} u \right] dV$ (where $u^*$ is the test function), which can be transformed into $ \int R^2 (\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) (\nabla u^* \cdot \nabla_{pol} u) dV $ via an integration by parts. In order to implement this term, it is necessary to develop $\nabla \cdot (\rho \mathbf{v})$, which is done [here](div_rho_v).

#### Definition of current (eq. 3)

This equation remains the same as in other JOREK [reduced MHD models](reduced_mhd):
\begin{aligned}
  j = \Delta^*\psi
\end{aligned}

#### Definition of vorticity (eq. 4)

This equation remains the same as in other JOREK [reduced MHD models](reduced_mhd):
\begin{aligned}
  \omega = \Delta_\text{pol} u
\end{aligned}

#### Global continuity equation (eq. 5)

The global continuity equation, i.e. the equation describing the evolution of the total mass density, reads:

\begin{aligned}
\partial_t \rho = - \nabla \cdot (\rho \mathbf{v}) + \nabla \cdot (D_i \nabla (\rho - \rho_{imp})) + \nabla \cdot (D_{imp} \nabla \rho_{imp}) + S_{\rho_i} + S_{\rho_{imp}}
\end{aligned}

One important aspect of the model for e.g. [SPI](spi_tutorial) or [MGI simulations](mgi_tutorial) is the volumetric source term $S_{\rho_{imp}}$ through which impurities are deposited. Some information on the parameterization of this term is given [here](particle_source_parameterization).

#### Pressure equation (eq. 6)

The pressure equation reads something like:

\begin{aligned}
\partial_t p = - \mathbf{v} \cdot \nabla p - \gamma p \nabla \cdot \mathbf{v} + Conduction + Joule - Radiation - Ionization
\end{aligned}

assuming that all species have the same ratio of heat capacities $\gamma$, which is the case if we consider mono-atomic impurities and main ions (which we plan to do). We recall that here $p=(\rho+\alpha_{imp}\rho_{imp})T$ (see above).

#### Parallel momentum equation (eq. 7)

The parallel momentum equation is obtained by applying $\mathbf{B} \cdot (...) $ to the full MHD momentum equation (written above, in the Vorticity equation section). The result in the absence of the $-(\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) \mathbf{v}$ term is presented [here](reduced_mhd). To implement the latter, the approximation $\mathbf{B} \cdot \mathbf{v} \approx B^2 v_{\parallel} \approx \frac{F_0^2}{R^2} v_{\parallel} $ is used, which intuitively seems to make sense in reduced MHD. In weak form, the parallel momentum equation therefore gets a RHS term $ \int -(\partial_t \rho + \nabla \cdot (\rho \mathbf{v})) B^2 v_{parallel} $. In order to implement this term, it is necessary to develop $\nabla \cdot (\rho \mathbf{v})$, which is done [here](div_rho_v).

#### Impurity continuity equation (eq. 8)

The impurity continuity equation, i.e. the equation describing the evolution of the impurity mass density (all charge states included), reads:

\begin{aligned}
\partial_t \rho_{imp} = - \nabla \cdot (\rho_{imp} \mathbf{v}) + \nabla \cdot (D_{imp} \nabla \rho_{imp}) + S_{\rho_{imp}}
\end{aligned}

As already mentioned above, one important aspect of the model for e.g. [SPI](spi_tutorial) or [MGI simulations](mgi_tutorial) is the volumetric source term $S_{\rho_{imp}}$ through which impurities are deposited. Some information on the parameterization of this term is given [here](particle_source_parameterization).

### Implementation of the equations

- [Global continuity equation](model_501_global_continuity)
- [Induction equation](model_501_induction)
- [Vorticity equation](model_501_vorticity)
- [Pressure equation](model_501_pressure_eq)
- [Parallel momentum equation](model_501_parallel_momentum)
- [Impurity continuity equation](model_501_impurity_continuity)
- **Note:** the equations for the definition of current and vorticity are the same as in other models

### Atomic coefficients

Atomic coefficients are taken from the [ADAS database](adas.md). The "baseline" version of models 501/502 assume coronal equilibrium, but a non-equilibrium has been implemented recently (see below).

### Non-equilibrium impurities

A particle based non-equilibrium model has been implemented in JOREK, compatible with 501/502 and 600.
See [The marker representation of collisional-radiative impurity model](impurities_marker.md).


