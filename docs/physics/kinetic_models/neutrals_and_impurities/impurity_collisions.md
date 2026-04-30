---
title: "Impurity Collisions"
nav_order: 8
parent: "Neutrals and Impurities"
layout: default
render_with_liquid: false
---

# Impurity collisions
Currently, charged impurities can collide with background plasma ions using two types of the so-called Homma collision operator.
To use these type of impurity collisions set `use_kin_bg_collisions=.t.` and choose `kin_bg_coll_type`, which is Homma 2020 by defualt.

## Homma 2012
Published in [*Y. Homma, 2012 JCP*], builds on the Monte Carlo Binary Collision Model (BCM) [*T. Takizuka, H. Abe, 1977 JCP*], and adds the contribution of the thermal force by choosing a background plasma ion velocity from a distorted Maxwell distribution under the temperature gradient.
To use this operator, set `kin_bg_coll_type=Homma2013`.

## Homma 2020
Improves the previous model by adding a heat-flux limiter, since the Spitzer-Haerm formula used for the sampled heat-flux is known to be overestimated in low collisionality regimes [*Y. Homma, 2020 Nucl. Fusion*].

To use this operator, set `kin_bg_coll_type=Homma2020`.

The heat-flux limiter can be adjusted with the `homma2020_alpha` parameter, default and recommended value is 1.5 [Fundamenski 2005].