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
  * [Neutrals and Impurities](particles/neutrals_and_impurities.md)
  * [Runaway Electrons](particles/runaway_electrons.md)
  * [Energetic Ions](particles/energetic_ions.md)

## Known issues
  * [Issues](particles/issues.md): See currently known issues and how to solve/avoid them.

## Details on different aspects of the kinetics
  * [Coupling schemes](particles/coupling_schemes.md): How to couple your kinetic particles to the plasma (or not).
  * [Initialization](particles/initialization.md): How to choose the initial distribution of your particles.
  * [Wall actions](particles/wall_actions.md): How to choose the boundary conditions for your particles.

## Numerics details
  * [Particle types](particles/particle_types.md): Which additional variables each particle type has.
  * [Pushers](particles/pushers.md) (Incomplete) overview of available pushers.

## Available diagnostics and post-processors:

  * [Particle fast camera](particles/particle_fast_camera.md): Post-processor generating synthetic images from JOREK MHD and particle simulations.
  * [Particles poincare](particles/particles_poincare.md) for REs.
  * [Particles phase space](particles/particles_phase_space.md): for FPs.

## Work in progress

  * PRs for RE and FP into kinetic main.
  * PR for 2 temperature compatibility.
  * Compatibility with full MHD.

## Wanted (but not started)

  * Generalisation of initialisers.
  * Flexible combination of coupling scheme, pusher and particle type.
  * Add "off" coupling scheme to have no coupling to the plasma at all and a static plasma.

## People actively developing kinetic_main 
  * Máté Szűcs, [[mate.szuecs@ipp.mpg.de]]
  * Daniël Maris, [[D.Maris@differ.nl]]
  * Andrés Cathey, [[andres.cathey@ipp.mpg.de]]
  * James Carpenter, [[james.s.carpenter@durham.ac.uk]]

See also the [kinetics coordination](particles/kinetics_coordination.md) page, the [kinetic users](particles/kinetic_users.md) page, and the [[wp-kinetics|working group page where you can subscribe to the mailing list]] 

## Old information

Link to old information from before kinetic applications were brought together as kinetic_main: [old_kinetics](particles/old_kinetics.md)




