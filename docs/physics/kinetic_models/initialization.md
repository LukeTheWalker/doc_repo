# Kinetic particle initialization 

With initialization we mean what the particles get as original distribution before the simulation with kinetic_main starts. Initialization can be done in 3 ways, either nothing is initialized, the particles are initialized from a restart file, or the particles are initialized according to some initial distribution.

# No initialization 
Simply set restart_particles=.f. in the namelist, and set nothing for part_group_configs(...)%init_function and %init_pdf. This means that at the start of the simulation with kinetic_main, there will be no simulated particles yet. This is for instance useful for doing neutrals simulations which will be puffed/generated through (wall) recombination automatically during the simulation. 

# Restarting the particles 
To restart the particles from a file, set restart_particles=.t. During initialization, kinetic_main will automatically look for a part_restart.h5 file in the simulation folder and load all the groups from that file directly into the simulation. To do this, you need the corresponding groups in your namelist input file as well. This means you need to have entries in your namelist input with the same %id, %Z, %mass and %type as before the groups before restart, but you can vary each group's %n_particles (although at the moment you can only increase it, not decrease it).

If you want to do your new simulation with more or less part_groups than are present in the restart_file, it is advised to specify your intention by setting the namelist input "part_groups_in_use" to the list of IDs that you want to use in your new simulation (e.g. `part_groups_in_use = "D01" "N01"`). If you want to drop groups from the part_restart.h5 file, you **have** to specify "part_groups_in_use". You will get messages in your output file stating which groups have been loaded and which groups have been dropped.

The part_restart.h5 files are generated automatically at the end of each successful simulation with kinetic_main, and every 500 jorek steps, an intermediate "interim_part_restart.h5" file will be generated (that overwrites a previous interim restart file if that exists, to save on disk space as these restart files can be GBs of data). 

# Initialize the particles according to a given distribution 

!!! Add initializers here (@James)
