---
title: "Pitagora-CPU"
nav_order: 2
parent: "Systems"
grand_parent: "Getting Started"
layout: default
render_with_liquid: false
---

# Running JOREK on Pitagora CPU partition hosted by CINECA

## Getting Access

- Account Creation via `[`https://userdb.hpc.cineca.it/`](https://userdb.hpc.cineca.it/)` - Create New User
- Then fill out the HPC-Related information and upload your scanned ID/passport
- Contact the respective PI to add you to the project

## README

- E-Mail Address of CINECA Helpdesk: superc@cineca.it
- The present project related to the TSVV-F is called: **FUPA2_REDISMHD**`  
- Documentation: `[`https://docs.hpc.cineca.it/hpc/pitagora.html#pitagora-card`](https://docs.hpc.cineca.it/hpc/pitagora.html#pitagora-card)`

## Login

` ssh -Y <user>@login.pitagora.cineca.it`

which establishes a connection to one of the available login nodes. You
can also indicate explicitly the login nodes:

` login01-ext.pitagora.cineca.it`  
` login02-ext.pitagora.cineca.it`  
` login03-ext.pitagora.cineca.it`  
` login04-ext.pitagora.cineca.it`  
` login05-ext.pitagora.cineca.it`  
` login06-ext.pitagora.cineca.it`

Login nodes with odd number (01,03,05) are similar to the CPU partition
of the compute nodes: 2 × AMD EPYC 9745
(https://www.amd.com/en/products/processors/server/epyc/9005-series/amd-epyc-9745.html),
128 cores total, 768 GiB DDR5 RAM.

Login nodes with even number (02,04,06) match the compute nodes with
GPU: 2 × Intel Xeon Gold 6548Y+
(https://www.intel.com/content/www/us/en/products/sku/237564/intel-xeon-gold-6548y-processor-60m-cache-2-50-ghz/specifications.html),
32 cores total, 512 GiB DDR5 RAM, 1 × NVIDIA H100 NVL GPU
(https://www.nvidia.com/en-us/data-center/h100/).

Compile your code on the correct login if you want it to be executed on
a specific compute node partition.

## Software Available

As usual *module avail/load/list/show* allows to access the available
software.

Some non-preinstalled softwares (gnuplot, paraview, visit) are available
at /pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/.

To use the gnuplot, set:
`export PATH=/pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/gnuplot/bin:$PATH`

The visit and paraview (copied from Viper) work well on Intel CPU nodes
(login02/04/06), but fail to start on AMD CPU nodes (login01/03/05).

The visit can be enabled by:
`export PATH=/pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/mpcdf/soft/RHEL_9/packages/x86_64/visit/3.4.2/bin:$PATH`
The paraview can be enabled by two steps:
`export PATH=/pitagora_work/FUPA1_MHD/JOREK_LIBRARIES/mpcdf/soft/RHEL_9/packages/x86_64/paraview/5.11.2/bin:$PATH alias paraview='paraview --mesa' # to disable hardware rendering, as H100 is only for computing`