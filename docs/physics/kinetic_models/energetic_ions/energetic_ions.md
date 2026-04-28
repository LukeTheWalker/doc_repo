# Energetic ions

A species of suprathermal ions can be included in JOREK via the kinetic particle framework. To simulate the interaction of energetic particles (EPs) with MHD modes a hybrid kinetic-MHD model is used [1]. The plasma is split into a bulk part, which is treated with an MHD model, and the energetic particles, which are treated kinetically. More details about the JOREK implementation and applications can be found in [2].

## Full-f

JOREK uses a full-f formulation for the EPs. Their distribution function is modeled by $N_\mathrm{p}$ marker particles:

$$
    f(\mathbf{r}, \mathbf{v}, t) = \sum_{i=1}^{N_\mathrm{p}} w_i \, \delta(\mathbf{r}-\mathbf{r}_i(t)) \, \delta(\mathbf{v}-\mathbf{v}_i(t))
$$



## Coupling scheme

pressure coupling

CGL

6 variables



## Diagnostics

phase space projections

projections very flexible

## Initialization of energetic particles

### Consistency with the MHD equilibrium



### Importing a fast particle experimental distribuion





# Old wiki articles:

Importing fast particle experimental distribution function

Projections on arbitrary coordinates (particles_phase_space)

## References:
[1] W. Park et al., Phys. Fluids B 4, 2033 (1992).

[2] T. Bogaarts et al., Phys. plasmas 29, 122501 (2022).






