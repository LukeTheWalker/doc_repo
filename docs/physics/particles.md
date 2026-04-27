---
title: "Kinetic Particle Module"
nav_order: 6
parent: "Physics Models"
layout: default
render_with_liquid: false
---

Hannes working on this one now. 


<!-- ====== Particles ====== -->

# Particles
Think page is a hub for the kinetic framework with links to all subpages. This kinetics wiki is still being written, so this is work in progress.

## Introduction
* [Introduction to the kinetic framework](particles/particle_introduction.md) Read this first before you read any other link on this page.


## Introductions to the available particle species
  * [[Neutrals and impurities]]
  * [[Runaway electrons]]
  * [[Energetic ions]]

## Known issues
  * [[particles:Issues]]: See currently known issues and how to solve/avoid them.

## Details on different aspects of the kinetics
  * [[particles:coupling schemes]] How to couple your kinetic particles to the plasma (or not).
  * [[particles:initialization]] How to choose the initial distribution of your particles.
  * [[particles:wall_actions]] How to choose the boundary conditions for your particles.

## Numerics details
  * [[Particle types]] Which additional variables each particle type has.
  * [[Pushers]] (Incomplete) overview of available pushers.

## Available diagnostics and post-processors:

  * [[Particle Fast Camera]] Post-processor generating synthetic images from JOREK MHD and particle simulations
  * [[particles poincare]] for REs
  * [[particles phase space]] for FPs

## Work in progress

  * PRs for RE and FP into kinetic main
  * PR for 2 temperature compatibility
  * compatibility with full MHD

## Wanted (but not started)

  * Generalisation of initialisers
  * Flexible combination of coupling scheme, pusher and particle type
  * Add "off" coupling scheme to have no coupling to the plasma at all and a static plasma

## People actively developing kinetic_main 
  * Máté Szűcs, [[mate.szuecs@ipp.mpg.de]]
  * Daniël Maris, [[D.Maris@differ.nl]]
  * Andrés Cathey, [[andres.cathey@ipp.mpg.de]]
  * James Carpenter, [[james.s.carpenter@durham.ac.uk]]

See also the [[kinetics coordination]] page, the [[kinetic users]] page, and the [[wp-kinetics|working group page where you can subscribe to the mailing list]] 

## Old information

Link to old information from before kinetic applications were brought together as kinetic_main: [[particles:old_kinetics]]




