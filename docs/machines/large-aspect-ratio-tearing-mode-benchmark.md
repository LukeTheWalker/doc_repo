---
title: "Large aspect ratio tearing mode benchmark"
nav_exclude: true
parent: "Equilibria"
layout: default
render_with_liquid: false
---

<!-- #TODO_BY_HAOWEI -->
<!-- The missing attachments need to be downloaded from: https://jorek.eu/aug/doku.php?id=large_aspect_ratio_tearing_mode_benchmark -->

# Large Aspect Ratio Tearing Mode Benchmark

- circular plasma
- `eta` is constant over the whole computational domain
- no `visco`
- density constant $7.24\cdot10^{19}m^{-3}$ (deuterium)
- For JOREK normalization:
  - $\rho_0=n_0\cdot m_D=7.24\cdot10^{19}m^{-3}\cdot3.34\cdot10^{-27}kg=2.42\cdot10^{-7}kg\,m^{-3}$
  - $\sqrt{\mu_0\rho_0}=5.5\cdot10^{-7}$
  - $\sqrt{\mu_0/\rho_0}=2.3$

## Aspect Ratio 10 Cases

### Beta ~ 0 Case

- Information from Erika (output of Cotrans): [tearcirc_ar10_beta0.tar.gz](assets/asdex_upgrade/tearcirc_ar10_beta0.tar.gz)
- Required for the run:
  - $R=10m$
  - $a=1m$
  - $\Psi_{axis}-\Psi_{bnd}=1.2495 Wb$
  - $F_{pol}=-1.2495\Psi_N$
    - $FF'=-1.2495\Psi_N$
  - $F_0\approx9.969$ i.e., $B_{tor}\approx1T$
  - [q-profile as a function of Psi_N](assets/asdex_upgrade/q_tearcirc_ar10_b0.dat.gz)
    - $q=1.8\dots4.09$

<!-- - Comparison of growth rates:

| eta | CASTOR3D | Q.Yu | JOREK | Flexi |
| --- | -------- | ---- | ----- | ----- |
|     |          |      |       |       | -->