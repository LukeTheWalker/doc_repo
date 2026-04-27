---
title: "31128-7-base-case-for-Alex"
nav_exclude: true
parent: "Equilibria"
layout: default
render_with_liquid: false
---

<!-- #TODO_BY_HAOWEI -->
<!-- The missing attachments need to be downloaded from: https://jorek.eu/aug/doku.php?id=31128-7-base-case-for-alex -->

# 31128ed7 base case for Alex

- **Aim:** Simulations for AUG with diamagnetic drift (`tauIC=7e-3`)

- see also [http://www2.ipp.mpg.de/~mhoelzl/augelm/](http://www2.ipp.mpg.de/~mhoelzl/augelm/)
  - Remark: R0=LR; R1=; R2=HR; R3=HR2

- [trunk-for-31128ed7dia.tar.bz2](assets/asdex_upgrade/trunk-for-31128ed7dia.tar.bz2)
- [31128ed7-dia-basecase.tar.bz2](assets/asdex_upgrade/31128ed7-dia-basecase.tar.bz2)

```text
n_flux    = 81
n_open    = 17
n_private = 9
```

| resol | `n_tht` | `n_leg` | compute nodes |
| ----- | ------- | ------- | ------------- |
| R0    | 91      | 9       |               |
| R1    | 128     | 13      |               |
| R2    | 181     | 18      |               |
| R3    | 256     | 25      | around 8      |

- tstep=1.d0 until saturation; then reduce as necessary

- **Resolution scan**: R0...R3 with n=4,6,8,12,16
- **tauIC scan**: R3 single harmonic n=4,6,8,12,16 at tauIC=0,3.5e-3,7e-3
- **Large simulations**:
  - Start with n=0...12 with R2 and R3