---
title: "JET"
nav_order: 2
parent: "Machines"
layout: default
render_with_liquid: false
---

# Information relevant for simulating JET

## Direction of plasma current and toroidal field

Standard operation in JET is with $I_p$ and $B_t$ both running clockwise when looking from the top. In JOREK, since $\mathbf{B} = \nabla\psi\times \nabla\phi + F~\nabla\phi$ and $\phi$ also runs clockwise, this means that one should have $\psi_{axis}>\psi_{bnd}$.


## From EFIT to JOREK

Equilibrium data reconstructed by EFIT may be converted into JOREK input data by using [eqdsk2jorek.f90](eqdsk2jorek.f90).

**Note:** The sign convention for $\psi$ in EFIT (at least at JET) is opposite to the one in JOREK, i.e. a standard JET equilibrium has $\psi_{axis}^{EFIT}<\psi_{bnd}^{EFIT}$. As a consequence, we use $\psi_{JOREK}=-\psi_{EFIT}$ and $ff'_{JOREK}=-ff'_{EFIT}$.

## MGI and SPI relevant information

[Slides](assets/jet/seminar_20150917_sjach.pdf) from S. Jachmich which contain information on **MGI experiments** and show the position of the various Disruption Mitigation Valves (DMVs).

The **SPI system** installed in 2019 replaces DMV1. Its toroidal position, in JOREK coordinates, is therefore $\phi=6.08$, considering that $\phi=0$ corresponds to the middle of Octant 1. Some information on the SPI system can be found in these [slides](assets/jet/baylor_spi_jet_tsdw_2017.pdf) from L. Baylor.

## Synthetic diagnostics

- [KB5 bolometer](jet_synthetic_KB5_bolometer)

## JET ELM tutorial

Follow the JET ELM tutorial here: [JET ELM tutorial](jet_tutorial).