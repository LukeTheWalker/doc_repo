---
title: "ADAS Atomic Data"
nav_order: 4
parent: "Impurities"
grand_parent: "Model Extensions"
layout: default
render_with_liquid: false
---
## Brief overview

In JOREK models (like 500, 501, 502, 565, 600 etc) that involve processes such as ionization, recombination, line-radiation, Bremsstrahlung, recombination radiation, the corresponding rate-coefficients are often taken from Atomic Data and Analysis Structure (ADAS) database. The coefficients are given in ASCII text files for different elements, which one can in principle download from the OPEN-ADAS webpage [https://open.adas.ac.uk/](https://open.adas.ac.uk/).
For convenience, the files corresponding to commonly used elements like Hydrogen, Neon, Argon etc are pre-downloaded and can be found [here](https://www.jorek.eu/wiki/lib/exe/fetch.php?media=adas_data.tar.gz). While running JOREK, if you want to use ADAS coefficients, then the path to the folder containing these files must be provided in the input/namelist file, using the input parameter `adas_dir`.

## Naming convention

We use the [ADF11 Iso-nuclear master files](http://open.adas.ac.uk/adf11). This dataset contains the following coefficients: (Coefficients unavailable for W have been marked with `()`)

| Symbol | Ionisation state from electron-ion collisions |
|--------|-----------------------------------------------|
| ACD    | Effective recombination coefficients          |
| SCD    | Effective ionisation coefficients             |
| (QCD)  | (Cross-coupling coefficients)                 |
| (XCD)  | (Parent cross-coupling coefficients)          |

| Symbol | ionisation state from hydrogen-ion collisions    |
|--------|---------------------------------------------------|
| (CCD)  | (Charge exchange effective recombination coefficients) |

| Symbol | Radiation emission from electron-ion collisions |
|--------|-------------------------------------------------|
| PLT    | Line power driven by excitation of ions         |
| PRB    | Continuum and line power driven by recombination and Bremsstrahlung of dominant ions |
| (PLS)  | (Line power from selected transitions of dominant ions) |

| Symbol | Radiation emission from hydrogen-ion collisions |
|--------|-------------------------------------------------|
| (PRC)  | (Line power due to charge transfer from thermal neutral hydrogen to dominant ions) |

For simulating W impurities in fusion plasmas we would need ACD, SCD, CCD. To estimate the radiation losses, we would also need PLT, PRB.

CCD is not in the dataset for W, so we will do without for now.

The filenames follow a simple format:

| type | filename       | units  |
|------|----------------|--------|
| ACD  | acd50_w.dat    | cm3s-1 |
| SCD  | scd50_w.dat    | cm3s-1 |
| PLT  | plt50_w.dat    | Wcm3   |
| PRB  | prb50_w.dat    | Wcm3   |

all metastable unresolved.

## Parametrization using the coefficients

All the coefficients are pure functions of free-electron density and electron temperature. At the moment the coefficients are valid for electron densities up to
  * $2\times 10^{21} m^{-3}$ for Hydrogen
  * $3\times 10^{21} m^{-3}$ for Neon, Argon ?
Data is available for extended density range (upto 1e24 m^-3 for Deuterium) but these are not yet used in JOREK.

The parametrization (functional dependence) of rates on the coefficients are as follow,

---To be filled---

## Data format in the ADAS files

Note that the raw ADAS data is structured that all recombining data (ACD & PRB) are recombining FROM Z = 1 to N, while all ionizing data (SCD & PLT) are ionizing TO Z = 1 to N. To avoid an off-by-one error, we shifted the raw data by one index in mod_openadas.f90 when reading the raw ADAS data.

The file format can also be seen in more detail on the [Open-ADAS site](http://open.adas.ac.uk/man/appxa-11.pdf).

  * per ionisation level
    * per temperature (in log10, eV)
      * per density (in log10, cm^-3)
        * log10 of Generalized collisional radiative coefficient (ACD, SCD, PLT, PRB)

## Getting ionization rates from the above data

  * The ionization coefficients are given for z = 1..n_Z as ionizing to the level z.
  * The recombination coefficients are given for z = 1..n_Z as recombining from the level z

  * ionization rate to z in a volume = SCD(z, Te) * n_e * n_z
  * ionization rate to z for an atom (1/s) = SCD(z, Te) * n_e
  * probability of an atom ionizing in a specific time = SCD(z, Te) * n_e * dt which is only valid for small probabilities

The same calculation as above holds for the recombination rate, and the LT/RB power per atom

## Interpolation in coefficients

The coefficients are interpolated linearly in log10 of Te and ne. This could be replaced with higher-order splines for instance.

## Checking the radiation power function and its components

A quick way to check the radiation power function and its components is to use the radiation_function_diagno program, which output the aforementioned data for a set of hard-coded parameters and impurity species. 

Another way is to check the automatically generated charge_distribution.dat file, which contains the Coronal Equilibrium charge state distribution for a range of electron temperatures, as well as the total radiation power function.

## Data

You can also download the data from below
  * **[Data currently used in JOREK](https://www.jorek.eu/wiki/lib/exe/fetch.php?media=adas_data.tar.gz)**
  * **[Data with extended density (available only for Hydrogen)](https://www.jorek.eu/wiki/lib/exe/fetch.php?media=files.tar.gz)**

## Contact persons

In case of questions, you might try contacting someone from the below list. Each of them has different levels of exposure to ADAS/JOREK, so not everyone might be able to answer every question that you have.
  * Martin O'Mullane (one of the main developers of ADAS, not a JOREK user), email: martin.omullane@strath.ac.uk
  * Di Hu, email: hudi2@buaa.edu.cn
  * Sven Korving, email: Sven.Korving@iter.org
  * Fabian Wieschollek, email: fawie@ipp.mpg.de
  * Vinodh Bandaru, email: vkb@ipp.mpg.de
  * Máté Szűcs, email: mate.szuecs@ipp.mpg.de
