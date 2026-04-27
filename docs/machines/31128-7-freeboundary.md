---
title: "Freeboundary Equilibrium with JOREK"
nav_exclude: true
parent: "Equilibria"
layout: default
render_with_liquid: false
---

<!-- #TODO_BY_HAOWEI -->
<!-- The missing attachments need to be downloaded from: https://jorek.eu/aug/doku.php?id=31128-7-freeboundary -->

# Input for a freeboundary equilibrium of micdu/eqb/31128/ed7 with JOREK

- Coil currents (extracted with shot_kk program by ers; see ~mhoelzl/shot_kk_2014/31128-2.4s/):

```text
coil       current [MA t]
IV1o        0.59079802
IV1u        1.47550797
IV2o       -0.40878099
IV2u       -1.08130205
IV3o       -0.11582000
IV3u       -0.11954700
ICoIo      -0.00274200
ICoIu      -0.00008600
Ipslon     -0.00048700
Ipslun      0.00222000
IHO2od      1.03397000
IHO2ud      1.67137802
IOH        -8.31900024
```

- Coil information:
  - Coil geometry (provided by ers): [aug-polcoils-ers.tar.gz](assets/asdex_upgrade/aug-polcoils-ers.tar.gz)
  - [Representation of the pf coils used in Cliste](aug-pf-coils-cliste) (from Mike Dunne)
  - Coils responsible for position control (Mike Dunne via e-mail): *Simple answer: the V2O and V2U coils do the main work of position control. More in depth answer: the V2 coiuls are used as standard to feed back on Raus and Zsquad (quadratic regression on the current center) during the flattop. During ramp up, it's usually the FP regression of R_current and z_current. In addition, in discharge 31128, there was also feedback on the strikelines by the V1U and OH2U coils. *
- Starting point -- ELM stable case with fixed boundary equilibrium: [31128-7-freebound-starting-point.tar.gz](assets/asdex_upgrade/31128-7-freebound-starting-point.tar.gz)
  - Data for comparison of the free boundary equilibrium: [31128-7-cliste-comparison-data.tar.gz](assets/asdex_upgrade/31128-7-cliste-comparison-data.tar.gz)
  - [R_bound,Z_bound,Psi_bound](assets/asdex_upgrade/31128-7-psibound.txt) different from what we used for the fixed boundary (to avoid coils inside the JOREK domain); see ~mhoelzl/liste2jorek/micdu-eqb-31128-ed7-2.4s/
- [starwall-response.dat.tar.gz](assets/asdex_upgrade/starwall-response.dat.tar.gz) -- for the input provided by jarsuch

## Repeating the old ITER case to verify the code is not broken

- Old data by M. Hoelzl:
  - [iter-freebound-case.tar.gz](assets/asdex_upgrade/iter-freebound-case.tar.gz)
  - [iter-freebound-beta0.tar.gz](assets/asdex_upgrade/iter-freebound-beta0.tar.gz) (even simpler case with beta=0)
  - **ITER X-point case:** [2016-03_repeat_vde-xpoint.tar.gz](assets/asdex_upgrade/2016-03_repeat_vde-xpoint.tar.gz) -- [starwall-response.dat.tar.bz2](http://www2.ipp.mpg.de/~mhoelzl/download/starwall-response.dat.tar.bz2)