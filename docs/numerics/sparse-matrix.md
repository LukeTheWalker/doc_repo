---
title: "Sparse Matrix Format"
nav_order: 5
parent: "Numerics and Tools"
layout: default
render_with_liquid: false
---

# Sparse Matrix Format

The central data structure for all linear algebra in JOREK is `type_SP_MATRIX`,
defined in `datatypes/mod_sparse_matrix.f90`.
The **primary storage format is block coordinate (BCOO)**: non-zero entries are
stored as a flat list of dense $b \times b$ blocks,
sharing the same `irn`/`jcn`/`val` arrays at the scalar level.  A block-CSR
view (`iblockptr`) is derived from the BCOO data on demand for the iterative
solver and GPU paths.

---

## Block Structure and Degrees of Freedom

JOREK uses bicubic Hermite finite elements.  Each physical mesh node carries
$n_\text{dof} = n_\text{dof,1D}^2$ Hermite DOF indices representing the function
value and its poloidal derivatives ($\partial_R$, $\partial_Z$,
$\partial_R\partial_Z$).  For the default cubic order (`n_order = 3`) this gives
$n_\text{dof} = 2^2 = 4$ Hermite DOF indices per physical node.  Each Hermite
DOF index occupies its own **block row** of size $b$ in the global matrix — so
"node $i$" in the matrix always refers to Hermite DOF index $i$, not a physical
mesh point.

The block size and global matrix dimension are

$$b = n_\text{var} \times n_\text{tor}, \qquad
n_\text{global} = N_\text{unique} \times b$$

where $n_\text{var}$ is the number of MHD variables, $n_\text{tor}$ is the number
of retained toroidal Fourier modes, and
$N_\text{unique}$ is the count of unique Hermite DOF indices.  The product $b$
is stored in `a_mat%block_size`.

**Axis sharing.** At the magnetic axis all $N_\text{axis}$ axis nodes share a
single function-value Hermite DOF index (global index 1).  Their derivative DOF
indices ($\partial_R$, $\partial_Z$, $\partial_R\partial_Z$) remain distinct per
node.  Compared to a grid without an axis this saves $N_\text{axis} - 1$ indices:

$$N_\text{unique}
  = N_\text{nodes} \times n_\text{dof} - (N_\text{axis} - 1)$$

where $N_\text{nodes}$ is the number of physical mesh nodes and
$N_\text{axis}$ is the number of axis nodes.  The code computes $N_\text{unique}$
implicitly as the maximum Hermite DOF index over all nodes:

```fortran
ng = max(node%index) * block_size  ! = N_unique * b
```

A **block row** $i$ corresponds to Hermite DOF index $i$.  It has one
$b \times b$ nonzero block for each Hermite DOF index $j$ that is coupled to $i$
through the finite-element stencil.  The number of nonzero blocks in block row
$i$ is `ijA_size(i)`; the maximum over all block rows is `maxsize`.

### DOF ordering and index mapping

The scalar row (or column) index of degree of freedom
(Hermite DOF index $i$, variable $v$, toroidal component $t$) is

$$\text{idx}(i,\,v,\,t) \;=\; (i-1)\,b \;+\; (v-1)\,n_\text{tor} \;+\; t$$

Variable varies slowly (stride $n_\text{tor}$), toroidal mode varies fastest
(stride 1).  The following diagram shows the layout for a small example
($N_\text{unique} = 3$, $n_\text{var} = 2$, $n_\text{tor} = 3$, $b = 6$):

```
 ┌───┬───┬───┬───┬───┬───┐     ┌───┬───┬───┬───┬───┬───┐     ···
 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │     │ 7 │ 8 │ 9 │10 │11 │12 │     ···
 ├───┴───┴───┼───┴───┴───┤     ├───┴───┴───┼───┴───┴───┤     ···
 │   var 1   │   var 2   │     │   var 1   │   var 2   │     ···
 ├───────────┴───────────┤     ├───────────┴───────────┤     ···
 │    Hermite DOF 1      │     │    Hermite DOF 2      │     ···
 ├───────────────────────┘     └───────────────────────┘
 │                       Node 1                              ···
 └──────────────────────────────────────────────────────
```

The same ordering applies to rows and columns.  A $b \times b$ block
$B(i,j)$ therefore decomposes into $n_\text{var} \times n_\text{var}$
sub-blocks of size $n_\text{tor} \times n_\text{tor}$, one per
variable-coupling pair:

```
 Block B(node i, node j)

           ← var 1 →   ← var 2 →   ···  ← var n_var →
         ┌───────────┬───────────┬─────┬────────────┐
 var 1   │    Bψψ    │    Bψu    │     │    BψT     │
         ├───────────┼───────────┼─────┼────────────┤
 var 2   │    Buψ    │    Buu    │     │    BuT     │
         ├───────────┼───────────┼─────┼────────────┤
 ...     │           │           │ ... │            │
         ├───────────┼───────────┼─────┼────────────┤
 var Nv  │    BTψ    │    BTu    │     │    BTT     │
         └───────────┴───────────┴─────┴────────────┘

 Each sub-block is n_tor × n_tor and encodes how one MHD variable at
 node i couples to one MHD variable at node j across all retained
 toroidal Fourier components.
```

---

## Primary Format: Block COO (BCOO)

### Scalar-level arrays

| Array | Size | Content |
| --- | --- | --- |
| `irn` | `nnz` | Global scalar row index of each scalar non-zero (1-based) |
| `jcn` | `nnz` | Global scalar column index of each scalar non-zero (1-based) |
| `val` | `nnz` | Value of each scalar non-zero |

Blocks are stored **contiguously** in these arrays: block $k$ (1-indexed)
occupies positions $(k-1)b^2 + 1$ through $k b^2$ in all three arrays.
Within a block the $b^2$ entries are laid out in **row-major order**
(local row varies slowly, local column varies fast):
entry $(r, c)$ of the block sits at offset $b(r-1) + c$ from the block start.
The ordering of blocks themselves is arbitrary (COO), though in practice the
assembly proceeds row-by-row so blocks of the same block row appear
consecutively.

### Block-level structure arrays

| Array | Size | Content |
| --- | --- | --- |
| `ijA_size` | `my_ind_size` | Number of nonzero blocks in block row $i$ |
| `irn_jcn` | `my_ind_size × maxsize` | `irn_jcn(i,k)` is the **block column index** of the $k$-th nonzero block of block row $i$ |
| `ijA_index` | `my_ind_size × maxsize` | `ijA_index(i,k)` is the **1-indexed scalar position in `val`** of the first entry of the $k$-th nonzero block of block row $i$ |

These three arrays provide a random-access view into the BCOO list without
requiring a sorted order.

### Status flags

| Flag | Set when |
| --- | --- |
| `bcsr_mapped` | `iblockptr` and `jcn_block` have been computed |
| `device_mapped` | Matrix arrays have been allocated on the GPU |
| `scaled` | Diagonal row/column scaling has been applied |
| `equilibrated` | Full equilibration scaling has been applied |

---

## Storage Layout: Worked Example

The following example uses **3 block rows, 3 block columns, b = 2**,
giving $n_\text{global} = 6$ and 7 nonzero blocks ($\text{nnz} = 7 \times 4 = 28$).

### 1 — Block-level sparsity pattern

```
         bcol 1   bcol 2   bcol 3
       ┌────────┬────────┬────────┐
brow 1 │ B(1,1) │ B(1,2) │        │
       ├────────┼────────┼────────┤
brow 2 │ B(2,1) │ B(2,2) │ B(2,3) │
       ├────────┼────────┼────────┤
brow 3 │        │ B(3,2) │ B(3,3) │
       └────────┴────────┴────────┘
```

### 2 — Flat BCOO: val / irn / jcn

Block $k$ occupies positions $(k-1)\,b^2+1$ through $k\,b^2$ in all three arrays.

```
 ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
 │ B(1,1)  │ B(1,2)  │ B(2,1)  │ B(2,2)  │ B(2,3)  │ B(3,2)  │ B(3,3)  │
 └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
    ^1         ^5        ^9        ^13       ^17       ^21       ^25
  block 1    block 2   block 3   block 4   block 5   block 6   block 7
```

Zooming into block 1 — B(1,1) stored **row-major** over its $b^2 = 4$ scalars:

```
 position in val:   1     2     3     4
 val:              a₁₁   a₁₂   a₂₁   a₂₂   (aᵢⱼ = entry at local row i, col j)
 irn:               1     1     2     2     (global scalar row)
 jcn:               1     2     1     2     (global scalar col)
```

### 3 — Block-structure arrays

`ijA_size`, `irn_jcn`, and `ijA_index` provide random-access into the flat
BCOO list without requiring a sorted order:

```
 brow │ ijA_size │  irn_jcn(brow, :)  │  ijA_index(brow, :)
──────┼──────────┼────────────────────┼─────────────────────
  1   │    2     │   1    2           │    1    5
  2   │    3     │   1    2    3      │    9   13   17
  3   │    2     │   2    3           │   21   25
```

`irn_jcn(i,k)` is the global block-node index of the coupled node (= block column number).
`ijA_index(i,k)` is the 1-indexed scalar position in `val` where that block starts —
e.g. `ijA_index(2,3) = 17` means B(2,3) starts at `val(17)`, so its entry
$(r,c)$ is at `val(17 + b*(r-1) + c - 1)`.

### 4 — Derived BCSR: iblockptr

After `set_block_csr_permutations`, `iblockptr` expresses the same BCOO data
as a CSR row pointer over blocks:

```
 iblockptr:   1               3                      6               8
              │               │                      │               │
              ▼               ▼                      ▼               ▼
 flat list: [ B(1,1) B(1,2) | B(2,1) B(2,2) B(2,3) | B(3,2) B(3,3) ]
              └─ brow 1 ──┘   └──── brow 2 ──────┘   └─ brow 3 ──┘
```

Block row $i$ owns flat-list positions `iblockptr(i)` … `iblockptr(i+1)−1`,
so the `bcsr_matv` inner loop can stride directly through `val` with a fixed
offset of $b^2$ per block.

---

## Derived Format: Block CSR (BCSR)

The BCSR view is computed lazily by
`set_block_csr_permutations()` in `matrix/sorting_module.f90`
the first time it is needed (flag `bcsr_mapped`).

### What the conversion does

`set_block_csr_permutations` iterates over the flat BCOO block list and
counts how many blocks belong to each block row:

```fortran
do i = 1, nnz_blocks
    i_glob   = (i - 1)*b*b + 1               ! first scalar entry of block i
    j        = (irn(i_glob) - offset)/b + 1  ! block row of block i
    jcn_block(i) = jcn(i_glob)/b + 1         ! block column of block i
    iblockptr(j+1) = iblockptr(j+1) + 1
end do
! prefix-sum iblockptr → CSR row pointers
```

Two new arrays are allocated and populated:

| Array | Size | Content |
| --- | --- | --- |
| `iblockptr` | `my_ind_size + 1` | Block CSR row pointer: block row $i$ owns blocks `iblockptr(i)` … `iblockptr(i+1)-1` |
| `jcn_block` | `nnz_blocks` | Block column index of block $j$ in BCSR enumeration |

The `val`, `irn`, and `jcn` arrays are **not reordered**; `iblockptr` simply
expresses the existing BCOO order as a CSR structure.  This is correct because
the prefix-sum construction assigns block-index ranges in sequential order, so
it only produces valid pointers when the flat BCOO list is already **sorted by
block row** — all blocks of row 1 before all blocks of row 2, and so on.
This ordering is guaranteed by the row-by-row finite-element assembly.

### Scalar CSR 

A separate scalar CSR conversion is performed by `convert_sorting()` when
required (e.g. PaStiX).  This routine:

1. Sorts `jcn` and `val` within each scalar row into ascending column order.
2. Overwrites `irn(1:nr+1)` **in-place** with the resulting scalar CSR row
   pointers (computed internally as a local array and then copied in).

After this call `irn` no longer holds row indices — its first `nr+1` entries
are now scalar CSR row pointers.  The remaining entries of `irn` past `nr+1`
are stale and should not be read.  Note that `a_mat%iptr` is a separate array
pointer that is **not** set by `convert_sorting`; callers that need the row
pointer under the `iptr` name must copy or alias it explicitly.

---

## MPI Distribution

The matrix is distributed across MPI ranks by **block rows**: each rank owns
a contiguous, non-overlapping range of block rows and stores all non-zero entries
that fall in those rows.  Column indices (`jcn`, `jcn_block`) are always global —
a local row can couple to any column in the full matrix, regardless of which rank
owns that column's rows.

### Partitioning

```text
rank 0       rank 1       rank 2         ...     rank P-1
┌──────────┐ ┌──────────┐ ┌──────────┐          ┌──────────┐
│ brow  1  │ │ brow K₀+1│ │ brow K₁+1│          │ brow K   │
│   ...    │ │   ...    │ │   ...    │    ...   │   ...    │
│ brow K₀  │ │ brow K₁  │ │ brow K₂  │          │ brow Nᵤ  │
└──────────┘ └──────────┘ └──────────┘          └──────────┘
 my_ind_min   my_ind_min   my_ind_min             my_ind_min
 = 1          = K₀+1       = K₁+1                = K+1
```

Each rank's range is `[my_ind_min, my_ind_max]` (1-based block-row indices).
The global directory arrays `index_min(1:ncpu)` and `index_max(1:ncpu)` let any
rank compute any other rank's range.

The local scalar row count and index offset follow directly:

$$n_r = \texttt{my_ind_size} \times b, \qquad
  \text{offset} = (\texttt{my_ind_min} - 1) \times b$$

where $b$ is the block size.  Global scalar row index $g$ maps to local scalar
row $g - \text{offset}$.

### Assembly

Assembly is purely local: each rank loops over its own element set and checks
whether a test-function block row falls within `[my_ind_min, my_ind_max]` before
adding a contribution.  No inter-rank communication is required during matrix
fill.

### Distribution Modes

| Field | Type | Meaning |
| --- | --- | --- |
| `ng` | integer | Global scalar dimension $n_\text{global}$ |
| `nr` | integer | Locally owned scalar rows (`my_ind_size × b`) |
| `nc` | integer | Locally owned scalar columns (= `ng` for row-distributed) |
| `nnz` | integer | Locally owned scalar non-zeros |
| `my_ind_min`, `my_ind_max` | integer | Inclusive block-row range of this rank |
| `my_ind_size` | integer | `my_ind_max − my_ind_min + 1` |
| `index_min(:)`, `index_max(:)` | integer(ncpu) | Block-row ranges of all ranks |
| `ncpu` | integer | Number of MPI ranks |
| `comm` | integer | MPI communicator |
| `row_distributed` | logical | `.true.` — rows partitioned (standard transient matrix) |
| `col_distributed` | logical | `.true.` — columns also partitioned (PaStiX path) |
| `reduced` | logical | `.true.` — full matrix replicated on all ranks |

The standard configuration for the global transient matrix is
`row_distributed = .true.`, `col_distributed = .false.`, `reduced = .false.`.

**`col_distributed`** is set for the PaStiX direct solver, which requires a
column-distributed CSR input.  After `convert_sorting()`, `irn` is overwritten
with scalar CSR row pointers and the column partition information is used to
determine the local column range.

**`reduced`** is used for matrices that must be available in full on every rank
(e.g. certain preconditioner sub-matrices).  In this mode `nnz` counts global
non-zeros and `irn`/`jcn`/`val` hold the complete matrix on every process.

---

## Format Used by Each Consumer

| Consumer | Format | Key arrays |
| --- | --- | --- |
| Direct assembly / FE routines | BCOO | `irn`, `jcn`, `val`, `ijA_size`, `irn_jcn`, `ijA_index` |
| Matrix–vector products (CPU) | BCSR | `iblockptr`, `jcn`, `val` |
| Matrix–vector products (GPU) | Scalar CSR | `iptr`/`irn`, `jcn`, `val` |
| MUMPS direct solve | Scalar COO (row-distributed) | `irn`, `jcn`, `val` |
| PaStiX direct solve | Scalar CSR (column-distributed) | `iptr`, `jcn`, `val` |
| STRUMPACK direct solve | Scalar COO | `irn`, `jcn`, `val` |
