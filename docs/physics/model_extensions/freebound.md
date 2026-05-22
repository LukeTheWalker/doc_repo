---
title: "Free Boundary Extension (STARWALL, CARIDDI)"
nav_order: 1
parent: "Model Extensions"
grand_parent: "Physics Models"
layout: default
render_with_liquid: false
---

In order to take into account the effects of the vacuum, conductive structures and external case, JOREK can be coupled to EM-wall codes (STARWALL and CARIDDI).
This is done by the so-called vacuum-casing principle, which allows to only prescribe the boundary conditions at the computational boundary of JOREK and requires mutual interaction matrices of the external structures.
Due to this, the other codes only need to be run once before the start of the JOREK simualtion.
More information can be found in the references.
The following documentation describes how to set up the simulations and which tools are available for the free-boundary extension.