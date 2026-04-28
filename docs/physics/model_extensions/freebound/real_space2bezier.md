---
title: "real_space2bezier (Guido's notes)"
nav_order: 1
parent: "Free-boundary references"
grand_parent: "Free Boundary Extension (STARWALL, CARIDDI)"
layout: default
render_with_liquid: false
---


**Source:** `real_space2bezier.f90` (STARWALL)

> **Note:** To be adapted to include the scale factors!

## Overview

As JOREK works with Bézier finite elements and STARWALL with a set of discrete points, a conversion is needed from points representation to the Bézier representation (and vice versa).

## Bézier Representation

The Bézier representation is defined as:

$$f(s) = \sum_{i=1}^{2} \sum_{j=1}^{N} \alpha_{ij} H_{ij}(s)$$

where:
- $i$ numbers the basis functions (2 basis functions per element)
- $j$ numbers the nodes
- $\alpha_{ij}$ are the Bézier coefficients to be determined
- $H_{ij}(s)$ are the Bézier basis functions

The target function $g(s)$ is given on $N_g$ discrete points.

## Least Squares Fit

The Bézier coefficients $\alpha_{ij}$ are calculated using a least squares fit by minimizing:

$$W = \int \left( f(s) - g(s) \right)^2 ds$$

Setting $\frac{\partial W}{\partial \alpha_{ij}} = 0$, we obtain:

$$\int H_{kl}(s) \sum_{i=1}^{2} \sum_{j=1}^{N} \alpha_{ij} H_{ij}(s) \, ds = \int H_{kl}(s) g(s) \, ds$$

This yields a system of linear equations with coefficients:

$$A_{kl,ij} = \int H_{kl}(s) H_{ij}(s) \, ds$$

## Elemental Matrix Contributions

For a single element, integrating from $s=0$ to $1$:

$$A_{elm} = \frac{1}{140} \begin{pmatrix}
52 & 22 & 18 & -13 \\
22 & 12 & 13 & -9 \\
18 & 13 & 52 & -22 \\
-13 & -9 & -22 & 12
\end{pmatrix}$$

### Regular Periodic Boundaries

For a regular periodic boundary without corners, elemental matrices are assembled to form repeated identical blocks:

$$\frac{1}{140} \begin{pmatrix}
18 & 13 & 104 & 0 & 18 & -13 \\
-13 & -9 & 0 & 24 & 13 & -9
\end{pmatrix}$$

### Boundaries with Corners

Boundaries with corners require special treatment. At a corner node:
- The node has 3 degrees of freedom
- Elements sharing a corner have the same coefficient for the first Bézier function
- The second function (representing the derivative) is independent on the left and right
- This creates a discontinuity in the derivative along the boundary

## Discussion Points

- **Integration consistency:** Why integrate the Bézier basis functions exactly when the integral over $g(s)$ is computed discretely? Should both sides of the equation use the same integration accuracy?
- **Quadrature rule improvement:** STARWALL currently uses equidistantly spaced points (typically 10) inside each boundary element. For better least-square approximation accuracy, consider using 4 Gaussian points per element with 4th-order Gaussian integration instead of 2nd-order trapezoidal integration.

*To be continued...*
