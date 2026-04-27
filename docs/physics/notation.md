---
title: "Notation Conventions"
nav_order: 1
parent: "Physics Models"
layout: default
render_with_liquid: false
---

# Notation Conventions

## General

| Symbol(s) | Description |
| --- | --- |
| S   | Scalars are printed in regular font | 
| $\mathbf{V}$ | Vectors are printed bold |
| $V_1, V_2, V_3$ | Co-variant components of vector $\mathbf{V}$ (cylindrical coordinates unless stated differently) |
| $V^1, V^2, V^3$ | Contra-variant components of vector $\mathbf{V}$ (cylindrical coordinates unless stated differently) |
| $V_R, V_Z, V_\phi$ | Physical cylindrical components (i.e., corresponding to normalized basis vectors) | 
| $\mathbf{T}, T_{\alpha \beta}, T^{\alpha \beta}$ | Tensors are printed bold, Tensor components in regular font | 

Einstein summation convention applies, i.e., $a_i b^i \equiv \sum_i a_i b^i$.

## Coordinate Related Symbols

| Symbol(s) | Description |
| --- | --- |
| $x, y, z$ | Cartesian Coordinates [(1)](#footnotes) |
| $R, Z, \phi$ | Cylindrical Coordinates |
| $u^1\equiv R, u^2\equiv Z, u^3\equiv\phi$ | Cylindrical Coordinates |
| $\mathbf{a}_1, \mathbf{a}_2, \mathbf{a}_3$ | Co-variant basis vectors (not unit vectors; cylindrical coordinates unless stated differently) |
| $\mathbf{a}^1, \mathbf{a}^2, \mathbf{a}^3$ | Contra-variant basis vectors (not unit vectors; cylindrical coordinates unless stated differently) |
| $\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3$ | Normalized co-variant basis vectors (cylindrical coordinates unless stated differently) [(2)](#footnotes) |
| $\mathbf{e}^1, \mathbf{e}^2, \mathbf{e}^3$ | Normalized contra-variant basis vectors (cylindrical coordinates unless stated differently) [(2)](#footnotes) |
| $g_{ij}, g^{ij}$ | Co- and contra-variant metric tensor components |
| $g$ | Determinant of co-variant metric tensor $g=\textrm{det}(\mathbf{g}_{ij})$ |
| $J$ | Jacobian ($J^2=g$) |
| $\partial_\alpha U\equiv\partial U / \partial u^\alpha$ | Short notation for derivatives (e.g., $\partial_1 U\equiv\partial U/\partial R$) |

Refer also to the page about [Coordinates](coordinates).

## Physical Quantities

| Symbol(s) | Description |
| --- | --- |
| $\psi$ | Poloidal Flux |
| $\psi_N$ | Normalized Poloidal Flux $\psi_N=(\psi - \psi_\text{axis})/(\psi_\text{bnd}-\psi_\text{axis})$ |
| $\mathbf{B}$ | Magnetic Field Vector |
| $\mathbf{b}$ | Normalized Magnetic Field Vector $\mathbf{b}=\mathbf{B}/\vert B\vert$ |
| ... | ... |

Refer also to the page about [Models](base_fluid_models/base_fluid_models.md).

## Footnotes
  - In element_matrix routines, x and y are frequently used as synonyms for R and Z which must not be confused with the Cartesian coordinates. 
  - Normalized co- and contra-variant basis vectors are of course identical in the cylindrical coordinate system.