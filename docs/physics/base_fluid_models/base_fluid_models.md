---
title: "Base Fluid Models"
nav_order: 5
parent: "Physics Models"
has_children: true
nav_fold: true
layout: default
render_with_liquid: false
---

Andres working on this now

# JOREK Physics Models

^ Model ^ Description ^^ Variables ^^^^^^^^^^
^ ::: ^ ::: ^^ 1 ^ 2 ^ 3 ^ 4 ^ 5 ^ 6 ^ 7 ^ 8 ^ 9 ^ 10 ^
| [[model199]] | [[Reduced MHD]] | No parallel flows | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | | | | |
| [[model303/333]] | :::         | Parallel flows | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | $v_{||}$ | | | |
| [[model305]] | :::         | ECCD 1 current model | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | $v_{||}$ | $J_{ECCD}$ | | |
| [[model306]] | :::         | ECCD 2 current model | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | $v_{||}$ | $J_{EC1}$ | $J_{EC2}$ | |
| [[model400]] | :::         | Parallel flows; separate $T_e$ and $T_i$ | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T_i$ | $v_{||}$ | $T_e$ | | |
| [[model500/501/555]] | :::         | Parallel flows and neutral/impurity density | $\psi$ | $u$ | $j$ | $\omega$ | $\rho$ | $T$ | $v_{||}$ | $\rho_{n/imp}$ | | |
| [[model600]] | :::         | Combines the above models, using switches to select with or w/o parallel flow, separate $T_e$ and $T_i$, neutrals, impurities, ... | | | | | | | | | | |
| [[model710]] | [[Full MHD]]    | | $A_3$ | $A_R$ | $A_Z$ | $u_R$ | $u_Z$ | $u_\phi$ | $\rho$ | $T$ | | |
| [[model711]] | [[Full MHD]]    | | $A_3$ | $A_R$ | $A_Z$ | $u_R$ | $u_Z$ | $u_\phi$ | $\rho$ | $Ti$ | $Te$ | |
| [[model712]] | [[Full MHD]]    | | $A_3$ | $A_R$ | $A_Z$ | $u_R$ | $u_Z$ | $u_\phi$ | $\rho$ | $Ti$ | $Te$ | $\rho_n$ |

Refer also to the page about [Notation Conventions](../notation.md).

## Derivations by Emmanuel Franck et al. 

  * {{ ::hierarchymhd.pdf |Part I: Document on two-fluid and single-fluid MHD}}
  * {{ ::reduced_mhd.pdf |Part II: Document on reduced MHD}}