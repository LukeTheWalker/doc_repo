---
title: "Element Matrix FFT"
nav_order: 4
parent: "Numerics and Tools"
layout: default
render_with_liquid: false
---

# Element Matrix Assembly

## Overview

`mod_elt_matrix_fft.f90` computes the contribution of a single finite element to the
global sparse matrix and right-hand side vector.  It is called once per element
inside the outer assembly loop in `matrix/construct_matrix_mod.f90`.

**Signature** (model-independent interface):

```fortran
subroutine element_matrix_fft(element, nodes, xpoint2, xcase2,           &
                R_axis, Z_axis, psi_axis, psi_bnd, R_xpoint, Z_xpoint,   &
                ELM, RHS, tid,                                           &
                ELM_p, ELM_n, ELM_k, ELM_kn, RHS_p, RHS_k,               &
                eq_g, eq_s, eq_t, eq_p, eq_ss, eq_st, eq_tt,             &
                delta_g, delta_s, delta_t,                               &
                i_tor_min, i_tor_max, aux_nodes, ELM_pnn, get_terms)
```


The geometry/physics arguments (`xpoint2`, `xcase2`, `R_axis`, …) are model-specific
inputs describing the equilibrium geometry and are passed through unchanged to the
weak-form evaluation.  `eq_g/s/t/p/ss/st/tt` and `delta_g/s/t` are pre-allocated
workspace arrays (size `n_plane × n_var × n_gauss × n_gauss`) for the field
synthesis; they are passed in from the outer assembly loop to avoid repeated
allocation.  `tid` is the OpenMP thread identifier.

**Outputs** — `ELM(DIM0, DIM0)` and `RHS(DIM0)`, where
`DIM0 = n_tor × n_vertex_max × n_degrees × n_var`.
These map directly to the dense $b \times b$ block in the global BCOO matrix; see
[Sparse Matrix Format](sparse-matrix.md) for the block layout.

**FFT workspace** — `ELM_p`, `ELM_n`, `ELM_k`, `ELM_kn`, `ELM_pnn`
(size `n_plane × DIM1 × DIM1`, `DIM1 = n_vertex_max × n_var × n_degrees`) and
`RHS_p`, `RHS_k` (size `n_plane × DIM1`) hold the per-plane Gauss sums used
during the FFT path.  They are declared in the caller and passed in so that the
storage is reused across elements without re-allocation.

---

## Representation of Fields

JOREK represents 3D fields as a Fourier series in the toroidal angle $\phi$:

$$f(R, Z, \phi) = \sum_{n=0}^{n_\text{tor}-1} f_n(R, Z) \cdot H_n(\phi)$$

The Fourier basis $H_n(\phi)$ consists of real-valued cosine and sine harmonics
stored consecutively:

```text
index in n_tor:   1      2        3        4        5      ...
                  n=0   n=n₁(c)  n=n₁(s)  n=n₂(c)  n=n₂(s) ...
```

Array `HZ(in, mp)` holds the value of the `in`-th harmonic at the `mp`-th
toroidal plane (one of `n_plane` equidistant angles spanning the periodic domain).
Array `mode(in)` stores the integer mode number associated with each harmonic
(0 for `in=1`, $n_1$ for `in=2,3`, etc.).

The poloidal direction uses bicubic Hermite basis functions $H_{i,j}(R,Z)$
(vertex $i$, Hermite DOF $j$).  The full 3D basis is the product
$H_{i,j}(R,Z) \times H_n(\phi)$.

---

## Computation Paths

The routine selects between two paths at runtime:

```fortran
if (i_tor_min == 1 .and. i_tor_max == n_tor) then
    use_fft = (n_tor >= n_tor_fft_thresh)   ! global matrix: FFT if many modes
else
    use_fft = .false.                        ! harmonic sub-matrix: always direct
end if
```

`n_tor_fft_thresh` is a namelist parameter (default 2); it also carries an
optional per-model override.

---

## Direct Harmonic Path (`use_fft = .false.`)

Used for small `n_tor` or when building individual harmonic sub-matrices for
the block-harmonic preconditioner.

```text
n_tor_start = i_tor_min,  n_tor_end = i_tor_max
HHZ = HZ          (actual Fourier values at each plane)
```

**Loop structure:**

```text
for (ms, mt)        — n_gauss² poloidal Gauss points
  for mp = 1..n_plane
    synthesise fields at (ms, mt, mp)                  [eq_g, eq_s, …]
    for im = i_tor_min..i_tor_max                      [test mode]
      compute test basis  v = H(i,j,ms,mt) × HZ(im,mp)
      for (k,l) in n_vertex × n_degrees                [trial DOF]
        for in = i_tor_min..i_tor_max                  [trial mode]
          compute trial basis ψ = H(k,l,ms,mt) × HZ(in,mp)
          evaluate weak form → amat
          ELM(row(im), col(in)) += w × amat            [direct scatter]
```

The toroidal integral is performed as an explicit sum over all $n_\text{plane}$
planes and all mode pairs $(im, in)$.  Cost per element:

$$\mathcal{O}\!\left(n_\text{gauss}^2 \times n_\text{plane} \times n_\text{tor}^2 \times n_\text{DOF}^2 \right)$$

where $n_\text{DOF} = n_\text{vertex} \times n_\text{degrees} \times n_\text{var}$.

---

## FFT Path (`use_fft = .true.`)

Used for the global monolithic matrix when `n_tor >= n_tor_fft_thresh`.

```text
n_tor_start = n_tor_end = 1       (mode loop runs once)
HHZ = 1.0                         (no Fourier factor during integration)
```

The algorithm has two phases.

### Phase 1 — Physical-Space Gauss Integration

```text
for (ms, mt)        — n_gauss² poloidal Gauss points
  for mp = 1..n_plane                                 [toroidal planes]
    synthesise fields at (ms, mt, mp)                  [eq_g, eq_s, …]
    compute test basis  v = H(i,j,ms,mt) × 1           [HHZ = 1]
    for (k,l) in n_vertex × n_degrees                  [trial DOF]
      compute trial basis ψ = H(k,l,ms,mt) × 1
      evaluate weak form:
        amat    → ELM_p(mp, trial_DOF, test_var) += w × amat
        amat_n  → ELM_n(mp, …)                  += w × amat_n
        amat_k  → ELM_k(mp, …)                  += w × amat_k
        amat_kn → ELM_kn(mp, …)                 += w × amat_kn
        amat_nn → ELM_pnn(mp, …)                += w × amat_nn
```

The five per-plane buffers separate contributions by how many toroidal
derivatives appear in the bilinear form:

| Buffer | Factor at scatter | Meaning |
| --- | --- | --- |
| `ELM_p` | $1$ | no toroidal derivative on either side |
| `ELM_n` | $\text{mode}(m)$ | $\partial_\phi$ on trial function |
| `ELM_k` | $\text{mode}(k)$ | $\partial_\phi$ on test function |
| `ELM_kn` | $\text{mode}(k)\cdot\text{mode}(m)$ | $\partial_\phi$ on both |
| `ELM_pnn` | $\text{mode}(m)^2$ | $\partial_\phi^2$ on trial function |

The split is necessary because $\partial_\phi H_n(\phi)$ changes the
cosine/sine type of the harmonic and introduces a factor of the mode number.

After Phase 1, each buffer holds, for every (test DOF, trial DOF) pair, a
real-valued signal sampled at `n_plane` equidistant toroidal angles.

### Phase 2 — FFT and Harmonic Scatter

For each (test DOF, trial DOF) pair and each buffer:

```text
in_fft = ELM_p[1:n_plane]
out_fft = r2c_FFT(in_fft)           ← dfftw_execute_dft_r2c  or  my_fft

for each (row mode k, col mode m):
    l = (k-1) + (m-1)    ← sum
    l = (k-1) - (m-1)    ← difference
    ELM[index_k, index_m] += ±Re/Im(out_fft[l+1]) × factor
```

The real-to-complex DFT is performed by one of two backends, selected at compile
time via the `USE_FFTW` preprocessor flag:

- **FFTW** (`USE_FFTW` defined, recommended) — calls
  `dfftw_execute_dft_r2c(fftw_plan, in_fft, out_fft)`.  The plan handle
  `fftw_plan` (stored in `phys_module`) is created once at startup with
  `dfftw_plan_dft_r2c_1d` for a transform of length `n_plane`.  FFTW
  \[[Frigo & Johnson, 2005](https://doi.org/10.1109/JPROC.2004.840301)\]
  automatically selects the most efficient algorithm for the given `n_plane`
  at plan-creation time; it is therefore advisable to choose `n_plane` as a
  product of small primes (powers of 2 are optimal).

- **Internal fallback** (`USE_FFTW` not defined) — calls `my_fft`, a simple
  DFT implementation included for portability.  It is $\mathcal{O}(n_\text{plane}^2)$
  and intended only for testing or platforms where FFTW is unavailable.

The mechanism follows from the product-to-sum identities for trigonometric
functions.  Denoting $\hat{f}_l = \text{DFT}(f)_l$ (with the r2c convention
$\text{Re}(\hat{f}_l) = \int f\cos(l\phi)\,\mathrm{d}\phi$,
$\text{Im}(\hat{f}_l) = -\int f\sin(l\phi)\,\mathrm{d}\phi$), the four
cosine/sine sub-entries of `ELM` at mode pair $(k, m)$ are:

$$\begin{aligned}
(\cos_k,\,\cos_m):\quad & +\operatorname{Re}(\hat{f}_{k+m}) + \operatorname{Re}(\hat{f}_{k-m}) \\
(\sin_k,\,\cos_m):\quad & -\operatorname{Im}(\hat{f}_{k+m}) - \operatorname{Im}(\hat{f}_{k-m}) \\
(\cos_k,\,\sin_m):\quad & -\operatorname{Im}(\hat{f}_{k+m}) + \operatorname{Im}(\hat{f}_{k-m}) \\
(\sin_k,\,\sin_m):\quad & -\operatorname{Re}(\hat{f}_{k+m}) + \operatorname{Re}(\hat{f}_{k-m})
\end{aligned}$$

In all four cases the same two FFT bins $l = (k-1) \pm (m-1)$ are read; the
only difference is which of Re or Im is used and with what sign.  The code
materialises these four additions for $l \ge 0$ and handles $l < 0$ via the
conjugate symmetry $\hat{f}_{-l} = \overline{\hat{f}_l}$ (which swaps the sign
of Im).  The five buffers contribute independently, each scaled by its
respective mode-number factor.

**Cost per element:**

$$\text{Phase 1: }\mathcal{O}\!\left(n_\text{gauss}^2 \times n_\text{plane} \times n_\text{DOF}^2\right)$$

$$\text{Phase 2: }\mathcal{O}\!\left(n_\text{tor}^2 \times n_\text{DOF}^2\right)$$

Since $n_\text{plane} \approx 2\,n_\text{tor}$, Phase 1 scales linearly in
$n_\text{tor}$ rather than quadratically, yielding a large saving for high mode
counts.

---

## Data-Flow Diagram

```text
 nodes (DOF values)
        │
        ▼
 ┌─────────────────────────────────┐
 │  Field synthesis  (eq_g/s/t/…)  │  n_plane × n_gauss² × n_var
 │  IFFT-like:                     │
 │  eq(mp,var,ms,mt) =             │
 │    Σ_{in,j} val × H × HZ(in,mp) │
 └───────────────┬─────────────────┘
                 │
        ┌────────┴────────┐
        │ direct path     │ FFT path
        │ (small n_tor)   │ (large n_tor)
        │                 │
        ▼                 ▼
 ELM directly      per-plane buffers
 at each           ELM_p / ELM_n
 mode pair         ELM_k / ELM_kn
 (k, m)            ELM_pnn
                       │
                       │  r2c FFT per (DOF pair, buffer)
                       ▼
                   out_fft[l]
                       │
                       │  scatter at l = (k-1) ± (m-1)
                       ▼
                  ELM[mode k, mode m]
```

---

## Source File Map

| File | Role |
| --- | --- |
| `models/model600/mod_elt_matrix_fft.f90` | Full physics, model 600 reference |
| `models/model*/mod_elt_matrix_fft.f90` | Per-model variants (same interface) |
| `models/phys_module.f90` | `HZ`, `mode`, `n_tor_fft_thresh`, `fftw_plan` |
| `gauss/basis_at_gaussian.f90` | Precomputed `H`, `H_s`, `H_t`, … at Gauss points |
| `models/mod_settings.f90` | Compile-time `n_plane`, `n_order`, `n_tor` |
| FFTW library | [fftw.org](https://www.fftw.org) — Frigo & Johnson, *Proc. IEEE* 93(2), 2005 |




