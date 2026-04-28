---
title: "Interactive Diagnostic Tool jorek2_postproc"
nav_order: 30
render_with_liquid: false
parent: "General"
---

**The diagnostic program jorek2_postproc is a very flexible diagnostic tool that can be used interactively or using small scripts**. Just some examples:
- Support for **"arbitrary" physical expressions** and for JOREK as well as **SI units**!
- This is possible by building on top of the [new_diag diagnostic framework](new_diag.md). You can find the [list of currently available expressions here](new_diag_expressions.md) and easily [implement your own expressions](new_diag.md#implement_own_expressions).
- Toroidally averaged **midplane profiles** of expressions.
- Expressions at a **fixed point versus time**.
- Expressions **along a line**.
- **Expressions averaged toroidally and poloidally within a fluxsurface**. This refers to a flux surface of the axisymmetric field component.
- Write out the separatrix.
- ...
- For the impatient: [All available postprocessing commands](jorek2_postproc-interactive_help.md)

## How You Get Started Using JOREK2_POSTPROC

- The program is compiled by:

  ```
  make jorek2_postproc
  ```

- It can be executed in two different ways, **interactively or with a script**. The syntax of the postprocessing commands (as described a bit later) is exactly the same, no matter if you run jorek2_postproc interactively or with a script.

  ```
  ./jorek2_postproc                     # Interactive usage
  ./jorek2_postproc < postproc_script   # Run with a script

  # IMPORTANT: jorek2_postproc < namelist will not work!!!
  ```

**For your first steps, I recommend that you run jorek2_postproc interactively.** When you call it, it will print the following example to get you started:

    namelist input               # Read namelist input file
    set units 0                  # Select JOREK units
    for step 100 to 200 do       # Do the following for severl time steps:
  
      expressions Psi_N T rho      # Select physical expressions
      mark_coords 1                # Mark first expression as coordinate
      set surfaces 200             # Number of flux surfaces
      average                      # Toroidal and poloidal average
  
      expressions R rho T Psi Er   # Select expressions
      mark_coords 1                # Mark first expression as coordinate
      set linepoints 200           # Number of points along a line
      midplane                     # Midplane profiles
    done

You may call "help" interactively in jorek2_postproc to get a **list of available postprocessing commands** and "help <command>" to get details on the usage of the respective command ([also printed here](jorek2_postproc-interactive_help.md)). Some things that you are used to from the Linux command line (like arrow left, arrow up, ...) do not work since this would be too hard to implement in Fortran.

**Now let's go through the example step by step:**
- First of all, jorek2_postproc is case-sensitive. So upper/lower-case spelling makes a difference!
- When you run jorek2_postproc, you need to tell it first where it can find the **namelist input file** by calling "namelist <input-file>".
- **The "set" command** allows to modify postprocessing settings. Type only "set" to see what settings are currently active. With "set units 0", you select JOREK units while "set units 1" selects SI-units.
- **The "for" loop** allows to perform postprocessing commands on several time steps when it is called like "for step <mmm> to <nnn> do". The alternative is to use "for step <mmm>" to run a postprocessing command on a single time step only.
- **The "expressions" command** selects physical expressions for the following commands. By calling it without parameters, a table of all available expressions is printed.
- **The "mark_coords" command** marks the first <n> expressions as coordinate expressions. This is important only in some cases to prevent applying a Fourier filter to coordinate expressions, for instance.
- We already saw the "set" command. With "set surfaces <nnn>" you tell jorek2_postproc to use <nnn> flux surfaces, for instance when searching for flux surfaces in the average command.
- **The "average" command** calculates toroidally and poloidally averaged values of the expressions you have selected and writes them into the subfolder "postproc/" (where all output of jorek2_postproc goes). The created file will have a name like "exprs_averaged_s00000..00200.dat" (s00000..00200 refers to time steps 0 to 200) and be of the following structure. So, there is one block per time step (separated by two blank lines) and one column per expression. Which expressions and which time steps are found in the file can be seen from the comment lines starting with "#".

  ```
  # Psi_N                  T                      rho                    
  # time step #000000
    4.999715655219729E-03  9.959956938522579E-07  1.000000000000000E+00
    1.746722551182135E-02  9.861224023020603E-07  1.000000000000000E+00
    2.993458959824115E-02  9.762490723795582E-07  1.000000000000000E+00
    [...]
    9.650534434178093E-01  2.356386773060824E-07  1.000000000000000E+00
    9.775056886630850E-01  2.257639579034879E-07  1.000000000000000E+00
    9.899724831959084E-01  2.158894554271154E-07  1.000000000000000E+00


  # Psi_N                  T                      rho                    
  # time step #000010
    4.999706691999141E-03  9.914456977332929E-07  9.999997693726987E-01
    1.746723404945607E-02  9.816293849844919E-07  9.999997737975996E-01
    2.993460806567594E-02  9.718130407060454E-07  9.999997782497250E-01
    [...]
    9.650534493133450E-01  2.354816596878166E-07  1.000000112501098E+00
    9.775056427694649E-01  2.256638515538048E-07  1.000000050973303E+00
    9.899725366052402E-01  2.158452819825082E-07  1.000000003052590E+00
  ```

- We have seen the "expressions" and "mark_coords" commands before. We are selecting "R" as coordinate here, as this makes most sense for plotting midplane profiles.
- The "set" command is used here to set "linepoints" to 200. This is the number of points used along straight lines (commands midplane, pol_line, tor_line ...).
- **The "midplane" command** outputs the selected expressions on the midplane (Z-position of the axis) from the inner to the outer boundary of the computational domain. The resulting file will have a name like "exprs_midplane_s00000..00200.dat" and a structure like:

  ```
  # R                      rho                    T                    
  # time step #000000
    9.000995954629104E+00  1.000000000000000E+00  2.088679680492613E-07
    9.011036151551821E+00  9.999999999999999E-01  2.183437850223690E-07
    9.021076352219909E+00  1.000000000000000E+00  2.279205893935197E-07
    [...]
    1.097891466885171E+01  1.000000000000000E+00  2.300010150576124E-07
    1.098895486678414E+01  1.000000000000000E+00  2.194434044859602E-07
    1.099899506494068E+01  9.999999999999999E-01  2.089761709280904E-07


  # R                      rho                    T                    
  # time step #000010
    9.000995951802391E+00  9.999999838209058E-01  2.088647778045389E-07
    9.011036148721947E+00  9.999998644571847E-01  2.183020724393824E-07
    9.021076349386879E+00  9.999998118499164E-01  2.278309314804877E-07
    [...]
    1.097891466540316E+01  1.000000185342449E+00  2.298513344962954E-07
    1.098895486333243E+01  1.000000139458445E+00  2.193607599267047E-07
    1.099899506148581E+01  1.000000017316645E+00  2.089681590296227E-07

  [...]
  ```

## Running With Scripts

Running jorek2_postproc with your own script is easy. Write the commands into the script just as you would do it in interactive mode. You can run jorek2_postproc with your script then from the command line:
  ./jorek2_postproc < your_script

You can add comments to your script after the "#" symbol. The getting started example shown above can directly be used as a script, for instance.

The scripts can be quite powerful as you may apply them to several simulations without modifications (you might have to adapt details like the namelist input file).

## Interactive Help

**The list of available postprocessing commands** can be shown directly in jorek2_postproc when you are running in interactive mode:
  help

You can get additional information for each command by typing:
  help <command>

**[You can find the information of the interactive help also on this page](jorek2_postproc-interactive_help.md)**.

## Plotting The Ascii Output With Gnuplot

I'm not giving an introduction to Gnuplot here. A lot of this stuff can be found [here](http://www.gnuplot.info/help.html), for instance. Just the most essential things:

So what you do is call gnuplot
  gnuplot

Then you may do the following:
- Remember that each expression is written out as a separate column. Thus, to plot the third expression (e.g., T) versus the first one (e.g., R) you would do the following:

  plot 'exprs_midplane_s00000.dat' using 1:3 with lines

- If you have output data for several time steps ("for step 0 to 200 do"), your file will contain one block per time step (separated by two blank lines, each). To plot the third expression versus the first one for all blocks (all time steps), you simply call:

  plot 'exprs_midplane_s00000..00200.dat' using 1:3 with lines

- To plot a single time step of such a file, for instance the sixth one in your ascii file, you have to select a block (numbering starts at zero here!) with "index":

  plot 'exprs_midplane_s00000..00200.dat' index 5 using 1:3 with lines

- To compare two different time points, for instance blocks 1 and 50:

  ```
  plot 'exprs_midplane_s00000..00200.dat' index 0  using 1:3 with lines, \
       'exprs_midplane_s00000..00200.dat' index 49 using 1:3 with lines
  ```

- With a recent gnuplot version, you can even plot blocks 15 to 50 easily:

  plot for [i=14:49] 'exprs_midplane_s00000..00200.dat' index i using 1:3 with lines
## Implementation

jorek2_postproc is implemented in the subfolder `postproc/`. There are the following Fortran source files:

| Source file | Description |
| --- | --- |
| jorek2_postproc.f90 | Main program |
| mod_exec_commands.f90 | Main module containing the commands |
| mod_convert_character.f90 | Auxilliary module for conversion between int/float and character strings |
| mod_parse_commands.f90 | Auxilliary module to split the user input into commands and arguments |
| mod_postproc_help.f90 | Auxilliary module containing the interactive help texts |
| mod_settings.f90 | Auxilliary module implementing the infrastructure for the "set" command |

Many postprocessing commands are built using the [new_diag](new_diag.md) framework which is responsible for evaluating arbitrary expressions at arbitrary positions. If you want to implement new physical expressions, you will have to do that in the new_diag framework documented [here](new_diag.md).

### Adding Your Own Postprocessing Commands

- **Create a subroutine in mod_exec_commands.f90 for your command**. Add clear comments! Implement similar to existing commands!
- **Add your command to mod_postproc_help:**
  - Add to the list of help topics at the top
  - Create a help topic with clear usage information
- Add your command to the two **select case structures in the routine exec_command of mod_exec_commands.f90**


### Known problems

Trying to run jorek2_postproc compiled with n_plane=1 will not be possible to use the **"average" command**. The error 

  forrtl: severe (174): SIGSEGV, segmentation fault occurred

will appear and nothing will be written to the ./postproc folder.
