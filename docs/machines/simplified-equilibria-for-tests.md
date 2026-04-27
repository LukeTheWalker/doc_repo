---
title: "Simplified Equilibria for Tests"
nav_exclude: true
parent: "Equilibria"
layout: default
render_with_liquid: false
---
<!-- #TODO_BY_HAOWEI -->
<!-- The missing attachments need to be downloaded from: https://jorek.eu/aug/doku.php?id=simplified_equilibria_for_tests -->

# Simplified Equilibria for Tests

## Tearing mode test case in large aspect ratio ("intear")

- R0=10m, a=1m (circular cross-section)
- This should be sufficient to specify the test case:

```text
rho  = const = 1
T    = 0.0497 - 0.0393 * PsiN
Btor = F0/R with F0=10
PsiN = a1*r + a2*r^2 + (1-a1-a2)*r^3 mit a1=-0.062829 und a2=1.84896
q    = 1.71001 + 0.64087 PsiN + 1.81974 PsiN^2 - 2.49093 PsiN^3 + 2.29412 PsiN^4
Psi_axis = -0.20266
Psi_bnd  = 0
n0   = 6*10^19 m^-3
rho0 = 2*10^-7 kg/m^3 -> sqrt(mu0 rho0)=5e-7 is the JOREK time normalization
```

- In cylinder approximation use: `Btor = 1` and `R = 10`
- For the normalization of rho and T see [here](../physics/normalization)
- Details we need to agree about when comparing in detail: eta, visco, ZK_par, ZK_perp, D_perp, ...

## Internal Kink equilibrium for Isabel

- [jorek-input-aug-like-fixed-boundary-equilibrium-for-isabel-with-q0-larger-than-1.tar.gz](assets/asdex_upgrade/jorek-input-aug-like-fixed-boundary-equilibrium-for-isabel-with-q0-larger-than-1.tar.gz)
- [current_profile_for_isabel.dat.tar.gz](assets/asdex_upgrade/current_profile_for_isabel.dat.tar.gz)
- [rminor_profile_for_isabel.dat.tar.gz](assets/asdex_upgrade/rminor_profile_for_isabel.dat.tar.gz)