---
title: "The ''new_diag'' framework"
nav_order: 10
render_with_liquid: false
parent: "Code Development"
---

- Implemented in `diagnostics/new_diag/`.
- Demonstration: `diagnostics/new_diag_demo.f90` (`make new_diag_demo`)

Allows, for instance, to do a Fourier analysis of arbitrary quantities like the pressure. Is used for some of the `jorek2_postproc` functionality.
## Available Expressions

- The easiest way to list available expressions is to run [jorek2_postproc](jorek2_postproc.md) interactively and call "expressions".
- [The list can also be found here](new_diag_expressions.md).

## Implement Own Expressions

This is actually very easy in most cases! You have to add the expression in the module `new_diag/mod_expressions.f90`:
- Add the expression to the `init_expr` routine close to the beginning of the file.
- Add the expression to the case-statement into subroutine `eval_expr` very close to the end of the file.
- Make sure that you use the `fact_time`, `fact_T`, etc variables appropriately such that your expression is calculated correctly both in JOREK normalized units ([normalization](normalization.md)) and SI units.
- If the necessary "ingredients" for your expression have not been calculated already in routine `eval_expr`, you will have to compute them at the correct places. Put [preprocessor directives](preprocessor.md) around model-specific quantities in order to avoid compilation problems for different models.
