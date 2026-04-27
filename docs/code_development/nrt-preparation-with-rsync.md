---
title: "NRT preparation with rsync"
parent: "Regression Tests"
layout: default
render_with_liquid: false
---

# Preparation of the nrt tests in case the machine you are using does not have access to the ITER git repository and to jorek.eu

- Get the code from the repository with git on a machine where outward ssh connection is available

```text
$ git clone ssh://git.iter.org/stab/jorek.git jorek_git
$ git checkout nrt
```

- Download the reference test cases (restart files) from the jorek.eu web site 

```text
$ jorek_git/non_regression_tests/get_all_data.sh
```

- Transfer the directory to the machine you are using for the tests (example: Helios)

```text
$ rsync -av --progress jorek_git USER@helios.iferc-csc.org:
$ ssh USER@helios.iferc-csc.org
$ cd jorek_git
```
