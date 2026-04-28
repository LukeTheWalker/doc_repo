---
title: "JOREK-STARWALL"
nav_order: 22
render_with_liquid: false
parent: "Physics Models"
---

# JOREK-STARWALL

*The coupling of JOREK with the vacuum code STARWALL, allows to simulate the **electro-magnetic interaction of the plasma with conducting structures via eddy currents**. An extension of this model to include **Halo currents** is currently in preparation.*

- **[Tutorial on how to run JOREK-STARWALL](freebound.md)** by examples (5/2017)
- **[Frequently Asked Questions (FAQs)](jorek-starwall-faqs.md)**

- **[Derivation of Lagrangian and Response Matrices](starwall-derivation.md)**
- [JOREK-STARWALL Workshop, Garching (5/2017)](2017-05-jorek-starwall-workshop.md)

- **[Scripts and extra tools for free-broundary](freeboundary-scripts.md)**
## References

*When using JOREK-STARWALL, please cite the two references shown in bold print*

- **P. Merkel, E. Strumberger. *Linear MHD stability studies with the STARWALL code.* arXiv:1508.04911 (2015) [Link](http://arxiv.org/abs/1508.04911)**
- **Hoelzl M., et al, *Coupling the JOREK and STARWALL Codes for Non-linear Resistive-wall Simulations.* Journal of Physics: Conference Series, 401, 012010 (2012) [Link](http://dx.doi.org/10.1088/1742-6596/401/1/012010)**
- Merkel P and Sempf M 2006 Proc. 21st IAEA Fusion Energy Conf. (Chengdu, China) TH/P3-8 [Link](http://www-naweb.iaea.org/napc/physics/FEC/FEC2006/papers/th_p3-8.pdf)
- P. Merkel. Resistive Wall Stability STARWALL-JOREK. Unpublished report (2010).![PDF](jor_star2.pdf)
- Hoelzl M., Huijsmans G.T.A., Merkel P., Atanasiu C., Lackner K., Nardon E., Aleynikova K., Liu F., Strumberger E., McAdams R., Chapman I., Fil A. Non-Linear Simulations of MHD Instabilities in Tokamaks Including Eddy Current Effects and Perspectives for the Extension to Halo Currents. Journal of Physics: Conference Series 561, 012011 (2014) [PDF](http://www2.ipp.mpg.de/~mhoelzl/2014-09-varenna-mhoelzl-paper.pdf)
- Zakharov L., Atanasiu C., Lackner K., Hoelzl M., Strumberger E. Electromagnetic Thin Wall Model for Simulations of Plasma Wall Touching Kink and Vertical Modes. Journal of Plasma Physics 81, 515810610 (2015) [PDF](http://www2.ipp.mpg.de/~mhoelzl/2015-12_Zakharov_J_Plasma_Phys.pdf)
- S. Mochalskyy, M. Hoelzl, R. Hatzky. Parallelization of JOREK-STARWALL for non-linear MHD simulations including resistive walls (Report of the EUROfusion High Level Support Team Projects JORSTAR/JORSTAR2). arXiv:1609.07441 (02/2018) [PDF](http://www2.ipp.mpg.de/~mhoelzl/2018-02-Mochalskyy-arXiv.pdf)
- Artola F.J., Huijsmans G.T.A., Hoelzl M., Beyer P., Loarte A., Gribov Y. Non-linear magnetohydrodynamic simulations of Edge Localised Modes triggering via vertical oscillations. Nuclear Fusion 58, 096018 (2018). [PDF](http://www2.ipp.mpg.de/~mhoelzl/2018-Artola-NF.pdf)
- Artola Such F.J., PhD thesis, Univ. Aix-Marseille (2018)

## Additional Information

- The **normalization of the wall resistivity** can be found in the [JOREK normalization table](normalization.md)
- Some remarks on [real_space2bezier.f90](real_space2bezier.f90.md) by G. Huijsmans
- [publications_on_vdes_in_asdex_upgrade](publications_on_vdes_in_asdex_upgrade.md)
- Old version of vacuum_response.f90 with input/output routines for sequential and MPI I/O: ![](2017-11-vacuum_response.f90.tar.gz)
