---
title: "cliste2jorek script"
parent: "ASDEX Upgrade"
layout: default
render_with_liquid: false
---

# cliste2jorek script

- cliste2jorek is a **Python script** which semi-automatically constructs the equilibrium-part of the JOREK input based on an ASDEX Upgrade equilibrium reconstruction of the CLISTE code. The equilibrium reconstruction must be based on measured kinetic profiles and have a high resolution (typically `micdu/eqb`). Mike Dunne is usually the contact person for these kind of equilibria.
- **Repository:** http://solps-mdsplus.aug.ipp.mpg.de/repos/CLISTE2JOREK/trunk
  - `svn checkout http://solps-mdsplus.aug.ipp.mpg.de/repos/CLISTE2JOREK/trunk <local-folder-for-cliste2jorek>`
  - (Contact Matthias Hoelzl or David Coster if you need access to this repository)
- An **example** can be found in the folder `example/` of the repository:
  - An ascii file with boundary points is required (`rz.dat` in the example).
  - An ascii file with the electron density profile is required (`ne.dat` in the example).
  - A standard input file is required of the following form:

```
micdu
eqb
28848
2
7.00
rz.dat
ne.dat
300
2000
```

- **How to run** the example?

```
ssh toki01.bc
cd <cliste2jorek-trunk>/example/
module load anaconda ### YOU ACTUALLY NEED TO LOAD A ANACONDA VERSION FOR PYTHON 2.X!
python ../cliste2jorek.py < input | tee logfile
```

- After running cliste2jorek, the `control.pdf` file will give a first impression about how good the fits worked which have been used to smooth profiles for JOREK. This typically needs user interaction, so you probably have to re-do at least some of the fits manually.
- The most important output is `jorek.nml` which contains information for the JOREK namelist input file, and the profiles `rho_fitted.dat`, `t_fitted.dat`, `ffp_fitted.dat`.
- The file `fluxsurf.dat` along with the information written out into the logfile allows to compare the equilibrium reconstruction of JOREK later on with the CLISTE equilibrium to be sure that everything worked fine.

## Access rights

In order to access the shot files you need to be part of the afs user group augd:aug_team or be assigned read rights from the owner of the particular folder (e.g. micdu).

