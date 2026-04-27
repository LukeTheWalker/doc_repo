---
title: "MGI/Disruptions"
nav_exclude: true
parent: "ASDEX Upgrade JOREK Wiki"
layout: default
render_with_liquid: false
---

<!-- #TODO_BY_HAOWEI -->
<!-- The missing attachments need to be downloaded from: https://jorek.eu/aug/doku.php?id=mgi_disruptions -->

# MGI and Disruption Simulations for ASDEX Upgrade

## General

- [Presentations with first preliminary simulations by Eric](assets/asdex_upgrade/discussion_jorek_aug_d2_mgi_modelling_060815.pptx)
- [Information on AUG Experiments (G. Pautasso)](assets/asdex_upgrade/gap_notes_22-3-16.pdf)

## Based on Equilibrium micdu/eqb/30444/1/1.95

JOREK input for this equilibrium. **Note** that this includes a modified grid_xpoint.f90 file for the grid generation.

- [micdu_eqb_30444_ed1_1.95s_jorek-input_v0.tar.gz](assets/asdex_upgrade/micdu_eqb_30444_ed1_1.95s_jorek-input_v0.tar.gz) -- starting point, not all parameters parameters optimized

### Important Parameters

#### Equilibrium Specific

$$
\begin{align*}
  n_0&=5.77\cdot10^{19}m^{-3} \\
  \rho_0&=1.93\cdot10^{-7}kg m^{-3} \\
  T_{e,0}&=2.4keV \\
  \sqrt{\mu_0\rho_0}&= 4.92\cdot10^{-7}~~~\text{(units omitted)} \\
  \sqrt{\mu_0/\rho_0}&= 2.55~~~\text{(units omitted)} \\
  \eta_{\perp,0}&=1.97\cdot1.65\cdot10^{-9}\frac{ln\Lambda}{\left(T_e[keV]\right)^{3/2}}\Omega m=1.3\cdot10^{-8}\Omega m=5\cdot10^{-9}~~~\text{(JOREK units)} \\
  	au_{IC}&=5\cdot10^{-3}~~~\text{(JOREK units)}
\end{align*}
$$

#### For Deuterium MGI

- Changes required in `models/model500/mgi_module.f90` compared to svn revision 1411 for modeling Deuterium MGI:

```text
mnum = 4.0d0      ! line 174
kst  = 1.40d0     ! line 176
```

- **NOTE:** `P_Dmv` needs to be multiplied by two in the input file to account for $D_2$ molecules versus $D$ atoms

## Virtual Diagnostics

### Interferometry

- Lines of sight in the experiment

```text
DCN (DCN Interferometer) #33299 2s
H-0 (Line of sight)
 From R= 1.053m, z= 0.211m, phi=303.400
 To   R= 2.249m, z=-0.023m, phi=305.000
H-1 (Line of sight)
 From R= 1.006m, z= 0.145m, phi=303.800
 To   R= 2.166m, z= 0.153m, phi=303.800
H-2 (Line of sight)
 From R= 1.007m, z= 0.315m, phi=303.800
 To   R= 2.170m, z= 0.324m, phi=303.800
H-4 (Line of sight)
 From R= 1.129m, z= 1.057m, phi=303.800
 To   R= 2.167m, z= 0.153m, phi=303.800
H-5 (Line of sight)
 From R= 1.095m, z= 0.803m, phi=303.800
 To   R= 2.171m, z= 0.443m, phi=303.800

COO (CO2 Interferometer) #33299 2s
V-1 CO2 (Line of sight)
 From R= 1.785m, z=-1.200m, phi=303.400
 To   R= 1.785m, z= 1.200m, phi=303.400
V-2 CO2 (Line of sight)
 From R= 1.200m, z=-1.200m, phi=303.400
 To   R= 1.200m, z= 1.200m, phi=303.400
```

- Data from experiment with circular plasma: [ne_32006.tar](assets/asdex_upgrade/ne_32006.tar)

#### Virtual Diagnositics

Put the following into a file `postproc_script` and run `./jorek2_postproc < ./postproc_script`. You may have to adapt the name of the namelist file in the script.

```text
namelist input2

si-units

for step 0 to 9999 do  
  expressions rho
  int_along_pol_line    1.785  -1.2  1.785  1.2  0.52
  int_along_pol_line    1.200  -1.2  1.200  1.2  0.52
  int_along_pol_line    2.135  -1.2  2.135  1.2  0.52

  expressions t
  point 1.5  0. 0.
done
```

## Corrections to be done in the code

- In models/model500/mgi_source.f90, correct the code so that the time of the start of the gas deposition be t_mgi (presently it is OK for JET but not for ASDEX-U [for which the injection starts slightly BEFORE t_mgi!])
  - Temporary solution for ASDEX-U: set L_tube = 0. in the input file
- Move certain hard-coded parameters relative to the MGI to the input file: mnum (mass number of the gas), kst (ratio of specific heats of the gas). Perhaps the best is to have one parameter in the input file which gives the type of gas: D2, Ar, ...