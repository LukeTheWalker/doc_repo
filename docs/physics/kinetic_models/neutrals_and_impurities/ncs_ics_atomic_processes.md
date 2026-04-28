# Atomic physics
Currently the following atomic physics processes are modeled, usually using coefficients from OpenADAS ([[adas|Brief overview]]):

**Neutrals:**
  * *Line radiation*: energy sink for background plasma.
  * *Ionization*: kinetic neutral -> background fluid ion.
  * *Recombination*: background fluid ion -> kinetic neutral.
  * *Charge-exchange*: modeled here as elastic collision between a background fluid- and kinetic ion, changes particle velocity and contributes to parallel momentum coupling term.
  * [Neutral neutral collisions](../../howto/neutral_neutral_collisions.md)

**Impurities:**
  * *Radiation*: including line radiation, Bremsstrahlung and contribution from recombination.
  * *Ionization*: increases charge state by one.
  * *Recombination*: decreases charge state by one.
  * *Collisions*: currently binary collisions with the background plasma ions, resulting in neoclassical effects.