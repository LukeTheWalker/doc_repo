---
title: "Run Stellarator Model with Divertor Region"
nav_order: 2
parent: "Stellarator"
grand_parent: "Howto"
layout: default
render_with_liquid: false
---

# Running Stellarator with Divertor Region

Unlike tokamak models, JOREK does not have a built-in equilibrium solver for stellarator but uses an ideal MHD equilibrium solver from GVEC, assuming nested flux surfaces. The main limitation with this approach has been that  

## Simplistic case: W7-A with artificial divertor

