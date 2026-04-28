---
title: "Gas Puffing"
nav_order: 8
parent: "Neutrals and Impurities"
layout: default
render_with_liquid: false
---

## Gas Puffing ##

The gas injection system is coded in two parts: you can specify locations in your simulation domain using the valve object, after which you can puff from these valves for each part\_group\_configs by using the puff\_ctrl objects. 

### Setting up a valve ###
The valves are defined through the valves object from the namelist. You can specify at most n\_valves\_max = 20 valves. The options for each valve are:

| valves(i)%           | option meaning |
|----------------------|----------------|
| type                 | four character code for the valve type. At the moment a poloidal circular ('circ') and poloidal 4 point polygon ('poly') option are implemented |
| phi                  | toroidal angle of the valve (particles will be generated at this toroidal angle) |
| r\_valve              | radius of poloidal circular valve (type must be 'circ')|
| R\_valve\_loc          | R position of circular valve (type must be 'circ') |
| Z\_valve\_loc          | Z position of circular valve (type must be 'circ') |
| poly\_R               | 4 R vertices of a quadrangular valve (type must be 'poly') |
| poly\_Z               | 4 Z vertices of a quadrangular valve (type must be 'poly') |

If the valves%(i)%type='circ' you need to define a circular valve in the poloidal plane with r\_valve, R\_valve\_loc, Z\_valve\_loc. You can optionally specify a specific toroidal location phi at which the valve is located (if left unspecified, the particles puffed from this valve will be put at a random toroidal location).
If the valves%(i)%type='poly', you need to define a quadrangular valve by setting poly\_R and poly\_Z (both exactly 4 points) which defines a quadrangle with the following corners; top-left: (poly\_R(1),poly\_Z(1)), top-right: (poly\_R(2),poly\_Z(2)), bottom-left: (poly\_R(3),poly\_Z(3)), bottom-right: (poly\_R(4),poly\_Z(4)).

### Setting up the puffrates at a valve ###

With the valves defined, each neutral or impurity particle group can puff from each valve by setting the corresponding part\_group\_configs(j)%puff\_ctrl(i) object. Here part\_group\_configs(j)%puff\_ctrl(i) means the puff control object for valves(i) of species j (so setting a puffrate at part\_group\_configs(j)%puff\_ctrl(1) means puffing group j from the valve specified at valves(1)). The options for each puff\_ctrl object are:

| part\_group\_configs(j)%puff\_ctrl(i)% | option meaning |
|-------------------------------------|----------------|
| supers\_num\_puff                     | number of new superparticles initialised at each puff action |
| supers\_weight\_puff                  | aimed weight (no. real particles per superparticle) of the new superparticles initialised at each puff action |
| supers\_ratio\_puff                   | fraction of the total number of superparticles allocated for this group (i.e. part\_group\_configs(i)%n\_particles) to use for each puff action |
| times | array of time checkpoints (SI, in seconds) for which the puffing rate is specified (requires a defined puff\_ctrl(i)%rates of the same length) |
| rates | array of specified puff rates (atoms/second) at given time checkpoints (requires a defined puff\_ctrl(i)%times of the same length) |
| from\_file | filename of ASCII piecewise linear puffrate, with two columns: time in s, rate in atoms/s |

The supers\_...\_puff variables set how many super particles each puff action at this valve will create, similar to other particle creating actions such as for example those found in [Plasma-Wall Interactions](../neutrals_and_impurities/particle_wall_interactions.md). You can only set one of the super\_...\_puff variables. If you don't set any of the three, the supers\_ratio\_puff method will be used, with its default value being set by supers\_ratio\_puff\_default=$10^{-4}$ in mod\_particle\_puffing.f90

The actual puffrate over time is set by a piecewise linear function. This can either be specified from an ASCII file (with two columns, the first specifying the times and the last specyfing the rates at those times). In that case there is no limit on the amount of timepoints you use, so you have arbitrary time resolution in your puffrate. Alternatively, the puffrate can be specified directly from the input namelist if you don't need more that n\_puff\_segments\_max=20 timepoints. In that case, set the timepoints in "times" at which the corresponding puffrates are set in "rates". In either case (namelist or from file), it will use the first rate for t smaller than the first time defined, and after the last specified timepoint it will use the last specified rate, so if you want a constant puffrate over time, you would only have to set rates(1)=..., times(1)=0.

Note that you can puff a single particle group from as many or as few valves as you specified and you can individually control the rates and creation scheme at each valve.