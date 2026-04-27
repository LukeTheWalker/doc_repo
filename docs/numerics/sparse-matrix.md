---
title: "Sparse Matrix Format"
nav_order: 5
parent: "Numerics and Tools"
layout: default
render_with_liquid: false
---

# Sparse Matrix Format

THIS SECTION REMAINS UNDER DEVELOPEMENT

The central data structure for all linear algebra in JOREK is `type_SP_MATRIX`,
defined in `datatypes/mod_sparse_matrix.f90`.
The **primary storage format is block coordinate (BCOO)**: non-zero entries are
stored as a flat list of dense $b \times b$ blocks in an arbitrary order,
sharing the same `irn`/`jcn`/`val` arrays at the scalar level.  A block-CSR
view (`iblockptr`) is derived from the BCOO data on demand for the iterative
solver and GPU paths.

---

## Block Structure and Degrees of Freedom

Let $N_\text{nodes}$ be the total number of finite-element nodes.
The global matrix dimension is

$$n_\text{global} = N_\text{nodes} \times b, \qquad
b = n_\text{var} \times n_\text{tor}$$

where $n_\text{var}$ is the number of MHD variables and $n_\text{tor}$ is the
number of retained toroidal Fourier modes (cosine and sine combined).
The product $b$ is stored in `a_mat%block_size`.

A **block row** $i$ corresponds to node $i$.  It has one $b \times b$ nonzero
block for each node $j$ that is coupled to node $i$ through the finite-element
stencil.  The number of nonzero blocks in block row $i$ is `ijA_size(i)`; the
maximum over all block rows is `maxsize`.

### DOF ordering and index mapping

The scalar row (or column) index of degree of freedom
(node $i$, variable $v$, toroidal component $t$) is

$$\text{idx}(i,\,v,\,t) \;=\; (i-1)\,b \;+\; (v-1)\,n_\text{tor} \;+\; t$$

Variable varies slowly (stride $n_\text{tor}$), toroidal mode varies fastest
(stride 1).  The following diagram shows the layout for a small example
($N = 3$ nodes, $n_\text{var} = 2$, $n_\text{tor} = 2$, $b = 4$):

```
 ←──────────── node 1 ────────────→  ←──── node 2 ────→  ←──── node 3 ────→
 ┌──── var 1 ────┬──── var 2 ────┐   ┌──── var 1 ────┬────  ···
 │  m₁  │  m₂  │  m₁  │  m₂  │   │      m₁  │  m₂  │   ···
 │   1  │   2  │   3  │   4  │   │       5  │   6   │   ···
 └───────────────────────────────┘  └─────────────────     ···
```

The same ordering applies to rows and columns.  A $b \times b$ block
$B(i,j)$ therefore decomposes into $n_\text{var} \times n_\text{var}$
sub-blocks of size $n_\text{tor} \times n_\text{tor}$, one per
variable-coupling pair:

```
 Block B(node i, node j)               columns: DOFs of node j

           ← var 1 →   ← var 2 →   ···   ← var n_var →
         ┌───────────┬───────────┬─────┬───────────┐
 var 1   │  Bψψ      │  Bψu      │     │  BψT      │  ← rows: DOFs
         ├───────────┼───────────┼─────┼───────────┤     of node i
 var 2   │  Buψ      │  Buu      │     │  BuT      │
         ├───────────┼───────────┼─────┼───────────┤
         │           │           │...  │           │
         ├───────────┼───────────┼─────┼───────────┤
 var Nv  │  BTψ      │  BTu      │     │  BTT      │
         └───────────┴───────────┴─────┴───────────┘

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

### MPI distribution

Each MPI rank owns a contiguous range of block rows
`my_ind_min` … `my_ind_max`.  The local scalar row count is
`nr = my_ind_size × b`.

| Field | Description |
| --- | --- |
| `ng` | Global scalar dimension $n_\text{global}$ |
| `nr`, `nc` | Locally owned scalar rows / columns |
| `nnz` | Locally owned scalar non-zeros |
| `my_ind_min`, `my_ind_max` | Block-row range owned by this rank (inclusive) |
| `my_ind_size` | `my_ind_max - my_ind_min + 1` |
| `index_min(:)`, `index_max(:)` | Block-row ranges of every MPI rank (size `ncpu`) |
| `comm` | MPI communicator over which the matrix is distributed |
| `row_distributed` | `.true.` when rows are partitioned (standard for the transient system) |
| `col_distributed` | `.true.` when columns are partitioned (PaStiX path) |
| `reduced` | `.true.` when the matrix is replicated on all ranks |

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
 iblockptr:   1           3                  6     8
              │           │                  │     │
              ▼           ▼                  ▼     ▼
 flat list: [ B(1,1) B(1,2) | B(2,1) B(2,2) B(2,3) | B(3,2) B(3,3) ]
              └─ brow 1 ──┘   └──────── brow 2 ────────┘  └─ brow 3 ─┘
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
    i_glob   = (i - 1)*b² + 1               ! first scalar entry of block i
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

### Scalar CSR (for direct solvers and GPU)

A separate scalar CSR conversion is performed by `convert_sorting()` when
required (e.g. PaStiX, or the GPU matvec path).  This routine:

1. Sorts `jcn` and `val` within each scalar row into ascending column order.
2. Overwrites `irn(1:nr+1)` **in-place** with the resulting scalar CSR row
   pointers (computed internally as a local array and then copied in).

After this call `irn` no longer holds row indices — its first `nr+1` entries
are now scalar CSR row pointers.  The remaining entries of `irn` past `nr+1`
are stale and should not be read.  Note that `a_mat%iptr` is a separate array
pointer that is **not** set by `convert_sorting`; callers that need the row
pointer under the `iptr` name must copy or alias it explicitly.