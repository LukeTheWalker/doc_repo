---
title: "Equilibria"
nav_exclude: true
parent: "ASDEX Upgrade JOREK Wiki"
layout: default
render_with_liquid: false
---

<!-- #TODO_BY_HAOWEI -->
<!-- The missing attachments need to be downloaded from: https://jorek.eu/aug/doku.php?id=equilibria -->

# Equilibria

### cliste2jorek Script

- The [cliste2jorek script](cliste2jorek_script) extracts the equilibrium information of ASDEX Upgrade shotfiles for JOREK.

### Conversion of NEMEC Equilibria

- $J_{pol}$ from Cotrans mode0 (`xm_jpol_spol`) $\rightarrow$ calculate FF' from it as below, make fit to smooth
- $\Delta\Psi_\text{NEMEC}$ is $\Psi_{bnd}-\Psi_{axis}$ in NEMEC coordinates
- Nevermind signs...

$$
\begin{align}
F &= \frac{\mu_0}{2\pi}\; J_{pol} \\
\Psi_\text{JOREK} &= \frac{1}{2\pi}\;\Psi_\text{NEMEC} \\
F' &= \frac{\partial F}{\partial\Psi_\text{JOREK}} = \frac{\partial F}{\partial\Psi_N}\underbrace{\frac{\partial\Psi_N}{\partial\Psi_\text{JOREK}}}_{=1/(\Delta\Psi_\text{JOREK})} = \frac{2\pi}{\Delta\Psi_\text{NEMEC}}\;\frac{\partial F}{\partial\Psi_N} \\
FF' &= \frac{2\pi}{\Delta\Psi_\text{NEMEC}}\;\frac{\mu_0^2}{4\pi^2}J_{pol}\frac{\partial J_{pol}}{\partial\Psi_N} = \frac{\mu_0^2}{2\pi\Delta\Psi_\text{NEMEC}}\;J_{pol}\frac{\partial J_{pol}}{\partial\Psi_N}
\end{align}
$$

### Simplified Equilibria for Tests

- [Simplified Equilibria for Tests](simplified-equilibria-for-tests)
- [Large aspect ratio tearing mode benchmark](large-aspect-ratio-tearing-mode-benchmark)
- [Simplified X-point tearing mode test case](simplified-x-point-tearing-mode-test-case)

### micdu / eqb / 17686 / 4.4s / Edition 1  (QH-Mode in carbon times)

- [Equilibrium in put for JOREK](assets/asdex_upgrade/for-feng-17686.tar.bz2)

### micdu / eqb / 33353 / 1.5s / Edition 2

- Equilibrium for **QH-Mode simulations with Feng** (similar discharge to what is planned for QH-Mode experiments in 2017 AUG campaign)
- [Profiles from Eli](assets/asdex_upgrade/33353_profiles.tar.gz)
  - **Important:** $v_\text{tor} = \omega_\text{tor} \cdot R$, i.e., $\omega_\text{tor}$ is given in units $\text{rad}/s$.

### micdu / eqb / 33616 / 7.2s / Edition *

- [ELM synchronized profiles by Florian Laggner](assets/asdex_upgrade/aug_33616_elm-synchronized-profiles-laggner.tar.gz)

#### Edition 1

- Used for **comparison of ELM crash with Felician et al (Paper 2017)**
- Should be the equilibrium just before the ELM crash
- $q_0=1.08$, $I_\text{tor}=800 kA$, $n_{e,0}=7.5\cdot10^{19}m^{-3}$, deuterium
- Profiles from Mike: [33616-profiles.tar.gz](assets/asdex_upgrade/33616-profiles.tar.gz) versus $\rho_\text{pol}=\sqrt{\Psi_N}$
- JOREK normalization factors: $\sqrt{\mu_0\rho_0}=5.6\cdot10^{-7}$, $\sqrt{\mu_0/\rho_0}=2.2$
- See:
  - `/tokp/work/mhoelzl/data/2016-09-AUGELMs-33616`
    - CLISTE2JOREK: `/tokp/work/mhoelzl/data/2016-09-AUGELMs-33616/cliste2jorek/trunk/33616-7.2s-ed1`
  - `/ptmp1/scratch/mhoelzl/FROM-DRACO/data/2016-09-AUGELMs-33616/`
  - http://www2.ipp.mpg.de/~mhoelzl/augelm3/
- Case for Daan without any rotation based on `n0-8_dia_neo_par_JN333bs_higherchipar_e1e-7_CORRVTOR`: [33616-for-daan.tar.gz](assets/asdex_upgrade/33616-for-daan.tar.gz)

### midcu / eqb / 23221 / 4.7s / Edition 2

- ELM unstable without diamagnetic drift
- ELM unstable with diamagnetic drift

### midcu / eqb / 29342 / 4.25s / Edition 2

- ELM unstable without diamagnetic drift
- ELM stable with diamagnetic drift
- **[Input for JOREK including input profiles](assets/asdex_upgrade/jorek-input_micdu_eqb_29342_4.25s_ed2.tar.gz)**

### midcu / eqb / 31128 / 2.4s / Edition 5

All information about **experimental data of shot #31128** and other shots of the 2014 experimental campaign on ELM control by RMPs can be found here:
https://www.aug.ipp.mpg.de/augtwiki/bin/view/CWAC/ModelingData2014

- **[Input for JOREK including input profiles](assets/asdex_upgrade/input_files_aug_31128_2400ms_iteration5.tar.gz)**
  - Remark: To get the equilibrium converged, set amix=0.2 in poisson.f90
- ELM unstable without diamagnetic drift
- ELM stable with diamagnetic drift
- Used by Shimpei Futatani for pellet studies

### midcu / eqb / 31128 / 2.4s / Edition 6

- Same as Edition 5, but temperature pedestal increased by about 10 percent
- Input for Cliste2Jorek given in next section (Edition 7)
- **[Input for JOREK including input profiles](assets/asdex_upgrade/input_jorek_iteration6.tar.gz)**
- ELM ??? without diamagnetic drift
- ELM ??? with diamagnetic drift

### midcu / eqb / 31128 / 2.4s / Edition 7

- Same as Edition 5, but temperature pedestal increased by about 20 percent
- [Input for cliste2jorek](assets/asdex_upgrade/input_cliste.tar.gz)
- [Crude Output from cliste2jorek](assets/asdex_upgrade/output_cliste.tar.gz)
- [Output from cliste2jorek modified to be used as input in JOREK](assets/asdex_upgrade/output_cliste_modified_for_jorek_input.tar.gz)
- **[Input for JOREK including input profiles](assets/asdex_upgrade/input_jorek_aug_31128_magic_iteration9.tar.gz)**
- ELM unstable without diamagnetic drift
- ELM unstable with diamagnetic drift.
- [Plots](micdu-eqb-31128-2.4-7_plots)
- Trick used to make the equilibrium converge: define amix=0.2 in poisson.f90 (also used in edition #5.)
- [Input file with possibly sufficient resolution for n=8 available here](assets/asdex_upgrade/input_n8.tar.gz)
- Simulation run with svn/git version #1406. Numerically unstable at the center. Needs to find out what is wrong.
  - one hypothesis: qprofile may be slightly under 1 at the very center: [qprofile](assets/asdex_upgrade/qprofiles_plots.png). Needs to increase a bit qprofile at the center (by decreasing ffprime)?
    - [Modified ffprime profile such that q0>1](assets/asdex_upgrade/ffp_31128_7_2.tar.gz)
  - with 2 tricks, possible to suppress central instability:
    - add a 'buffer' with high resistivity, hyperresistivity, viscosity and hyperviscosity at the center (e.g. for psi_n<0.15). [Modif in element_matrix.f90](assets/asdex_upgrade/element_matrix.f90.tar.gz)
    - add a 'buffer' with zero perturbation at the center (e.g. for psi_n <0.01) [Modif in boundary_conditions.f90](assets/asdex_upgrade/boundary_conditions.f90.tar.gz)
- Other problem: large deviation between restart 0 and equilibrium flows + large SOL currents. Since density pedestal is moved inwards during flow establishment, use contracted density profile from the beginning may help reduce these currents. [Contracted density profile available here.](assets/asdex_upgrade/rho_fitted_contract_new.dat.tar.gz)
- [Scans of eta/visco/eta_num/visco_num/etc](31128-7-scans)
- [Freeboundary Equilibrium with JOREK](31128-7-freeboundary)
- [31128-7-base-case-for-Alex](31128-7-base-case-for-Alex)

[ffp-scans](ffp-scans)

[tau_IC scans](tauIC%20scans)

### micdu / eqb / 30701 / 3.19s / Edition 2

- H-Mode case potentially interesting for ELM simulations

### micdu / eqb / 30734 / 1.2s / Edition 3

- L-Mode case: NTM and RMP coils
- Note: $q_0<1$ should be avoided for the JOREK simulations
- [fitted-experimental-profiles_30734.tar.gz](assets/asdex_upgrade/fitted-experimental-profiles_30734.tar.gz)