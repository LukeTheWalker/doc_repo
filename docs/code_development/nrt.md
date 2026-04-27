---
title: "Regression Tests"
nav_order: 2
parent: "Code Development"
layout: default
render_with_liquid: false
---

# Regression Testing

***Regression testing aims at detecting problems that are accidentally introduced into the code.** A regression test makes sure that a selected set of code results does not change after a commit pushed on the repository.*

- **The tests run automatically on the ITER git system after each commit** -- see column "Builds" in the [ITER Stash system](https://git.iter.org/projects/STAB/repos/jorek/branches). This makes sure that we immediately know when a commit "broke something in the code".
- It is also easy to run the tests locally yourself as described below.

## How do the tests work?

To reduce the execution time, the code is typically **restarted in the non-linear phase of a simulation and executed for a single time step**. After this short run, the resulting `nodes%values` are compared for absolute differences to a reference result. The comparison is done via HDF5 tools. Other kinds of test cases (e.g., free boundary equilibrium) exist as well.

- The `run_test.sh` script allows to run test cases.
- If a test is successful, the script will return error code 0, otherwise a non-zero value (often with an exit status equal to 1). This return code indicates to the "Bamboo" software on the ITER platform that a test was not successful.
- Additionally, at the end of the output, you will find a line similar to `Test 'tearing_circ_303' passed.`. This message is useful for the user to know whether the test was successful.

## How to run the tests as a user?

### Preparation steps

The normal preparation is necessary for working with JOREK:

- Obtain the code from the github/ITER git repository (see [here](../howto/first_steps))
- Create a Makefile.inc file for the machine you are using. Examples can be found in the folder Make.inc/ (see also [compiling](../compiling/cat_compiling))
- Load the required modules, for instance `module load intel impi fftw hdf5`. Scripts are available for this purpose for some machines, e.g., for Helios: `source reg_tests/job_scripts/helios/env.sh`
- **Add the directory where the HDF5 library is located to your Makefile.inc (see [HDF5-Tools](../numerics/hdf5tools.md))**

Finally you need to obtain data for running the regression tests:

- Obtain the restart files required for the tests: `reg_tests/get_all_data.sh`. In case the machine you are using does not have access to the ITER git repository and/or to jorek.eu directly, please [follow these instructions](nrt-preparation-with-rsync).

### Run a single test case interactively

- Note that **`reg_tests/run_test.sh -h`** will print the list of possible command line options.
- List all available test cases (name plus short explanation):

```text
reg_tests/run_test.sh -l
```

- If you have access to a machine that can run mpi jobs interactively, just run one test case with the following command (compilation + execution will occur):

```text
reg_tests/run_test.sh -j 8 tear_circ_303
```

- It is also possible to split compilation and execution into two commands:

```text
reg_tests/run_test.sh -p -j 8 tear_circ_303  # compile the binaries required
reg_tests/run_test.sh -n tear_circ_303       # run without compiling
```

### Run a single test case via a job script

- Compile the jorek executables for the test case (the -p flag specifies that the simulation will not run, only the compilation will be perfomed):

```text
reg_tests/run_test.sh -p -j 8 tear_circ_303
```

- Put the following command into your job script and submit it

```text
reg_tests/run_test.sh -k -n tear_circ_303
```

- For some machines, a batch script is already prepared in `reg_tests/job_scripts`

### Carry out several test cases at once

- All test cases can be executed all at once with these commands

```text
cd reg_tests
compile_all.sh
run_all.sh
```

- All test cases can be submitted as batch jobs via

```text
cd reg_tests
compile_all.sh
launch_all.sh
```

- Note, that you have to set environment variables, e.g., `export JOREK_HOST=helios` and `export BATCHCOMMAND=sbatch` for the `launch_all.sh` script. You can also equivalently source the following file: reg_tests/job_scripts/helios/env.sh

## How to create new test cases?

- Create a directory in `reg_tests/testcases`, e.g. `verynew_333`
- Put an input file named `input` into `reg_tests/testcases/verynew_333`
- Copy (from another existing test case) a `settings.sh` file into `verynew_333` and modify it to match your needs
- Launch the initial run that generates the `begin.h5` and `end.h5` files

```text
reg_tests/run test.sh -i verynew_333
```

- Send the restart files (`begin.h5`  and `end.h5`) to the web store on jorek.eu. Indeed, reference restart files are stored on a web site `http://jorek.eu/dav_nrt` to prevent the git repository to get too big.

```text
cd reg_tests/testcases/
./send_testcase_data.sh verynew_333
cd -
```

- Note that for some cases, not only the `begin.h5` and `end.h5` files need to be sent to jorek.eu for storage, but also additional files (e.g., STARWALL response for free boundary cases, or RMP field files)
- You have finished. You may also add verynew_333 in git repository to share the test:

```text
cd reg_tests/testcases/
rm verynew_333/*.h5 verynew_333/*.tar* verynew_333/jorek_model*
git add verynew_333
# note, you may need to add more files depending on the case!
git commit -m "Adding the verynew_333 test case"
git push
```

## How do the non-regression scripts work ?

What do the scripts perform when typing `jorek/reg_tests/run_test.sh -k tear_circ_199` ?

- Compile. Three executables are generated and stored in `reg_tests/testcases/tear_circ_199`:

```text
jorek_model199_3, rst_bin2hdf5, rst_hdf52bin
```

- Create directory to run the test, then needed files are copied into this directory. Example of a temporary directory name: `reg_tests/tmp13027`
- Go to this temporary directory to run the test
- Convert the reference HDF5 file `begin.h5` into `jorek_restart.rst`
- Launching the scenario stored into `reg_tests/testcases/tear_circ_199/settings.sh`
- Convert the final state `jorek_restart.rst` into `jorek_restart.h5`
- Compare the final state `jorek restart.h5` against reference file `end.h5` and print `Test passed` if everything  is fine

## How to update a test case?

For instance after a bug fix, a test case might need to be updated since the code results changed:

- Launch the test case from scratch with `-i` option (i.e. we do not want to restart from `begin.h5`)

```text
reg_tests/run_test.sh -i tear_circ_199
```

- In case of success, `begin.h5` and `end.h5` are stored into `reg_tests/testcases/tear_circ_199` overwriting older files
- Then, it is required to update the restart files on the web site `http://jorek.eu/dav_nrt` with the command

```text
cd reg_tests/testcases/
./send_testcase_data.sh tear_circ_199
cd -
```

- Then, after you have run this, the `.version` file in your test directory will contain the latest version name of your test. You need to commit and push this to the git server, otherwise the tests on the ITER will not know about your latest versione, e.g.:

```text
git add reg_tests/testcases/tear_circ_303/.version
git commit -m "Updating regression test tear_circ_303 due to changes XYZ."
git push
```

- A set of job scripts that can be used on supercomputers are stored in `reg_tests/job_scripts/`. This can help you to run a full case in order to update the restart files.

## How to refresh locally stored restart files?

Before retrieving the new files, you need to remove previous files. The commands are:

```text
reg_tests/cleanup.sh
reg_tests/get_all_data.sh
```

## Automated non-regression testing

- Test are running in "Bamboo" on the ITER platform, see [here](https://ci.iter.org/browse/STAB-JOREK)