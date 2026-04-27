---
title: "Run with Taylor-Galerkin Stabilization"
nav_order: 1
parent: "Numerics and Stabilization"
grand_parent: "Howto"
layout: default
render_with_liquid: false
---

Taylor Galerkin Stabilization
=============================

  * Taylor Galerkin stabilization is currently implemented for the reduced MHD models 303, 333, 400, 500, 501 and 555.
  * At present, the diamagnetic velocity is not included in the stabilization terms (ongoing development).

How to use it?
=====================

  * To use the stabilization, set the input parameter (array) ''TGNUM'' in the JOREK input file to a reasonable value. The preset value is 0, so no stabilization. Depending on your application, you should ensure via a parameter scan, that the stabilization does not affect the linear growth rates significantly.
  * Recommended values to start from are:
  
```
  TGNUM = 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5
```

  * The ''TGNUM'' values are given per equation (some equations don't actually contain stabilization terms, see the implementation). The example above is therefore given for model303, as it contains seven variables. 
