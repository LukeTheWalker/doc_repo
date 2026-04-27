---
title: "Random-Number Generators"
nav_order: 6
parent: "Numerics and Tools"
layout: default
render_with_liquid: false
---

# Random number generators in JOREK

For the JOREK-particles extension many random numbers are required, for example in the particle initialization routines.
To get acceptable speed, parallelisation and accuracy, we need a high-quality random number generator.
This we find in the [PCG](http://www.pcg-random.org/) family of pseudo-random number generators, which is both extremely fast and of high quality.

## Why not use the Fortran built-in RNG?

The Fortran intrinsic `random_number` has several limitations that make it unsuitable for JOREK's use case. 
The builtin random-number generators in Fortran are compiler-dependent and often of low quality. Furthermore they are not thread-safe and cannot be used in OpenMP parallel regions without external locking.
Additionally they do not offer strided sampling and jump-ahead to specific values.
Those attributes are very useful when generating related sets of random numbers on different MPI tasks.

## Usage

Please consider the following example in a serial context (only one OpenMP thread):

```fortran
  use mod_pcg32_rng
  use mod_random_seed
  real*8 :: rans(7)
  type(pcg32_rng) :: rng ! or class(type_rng), allocatable :: rng ! and allocate(pcg32_rng::rng)
  call rng%initialize(n_dims=7, seed=random_seed(), n_streams=1, i_stream=1, ierr=ifail)
  ! create 7 random numbers per call on 1 thread selecting the first stream
  
  call rng%next(rans)
```

**Parameters for `rng%initialize`:**

| Parameter | Description |
|---|---|
| `n_dims` | Number of random values produced per call to `next`. |
| `seed` | Integer seed for the generator. See the [Seeding section](#seeding). |
| `n_streams` | Total number of independent streams being initialised (across all threads and ranks). |
| `i_stream` | Index of the stream assigned to this instance, in the range `[1, n_streams]`. |
| `ierr` | Returns 0 on success, non-zero on failure.  |

### OpenMP parallel context

In parallel we define a number of streams of random numbers, where each thread selects one stream.
The following OpenMP example is adapted from `particles/examples/W_sputtering_rad_coll.f90`:

```fortran
  type(pcg32_rng), dimension(:), allocatable :: rng
  real*8 :: ran(6)
  integer :: n_stream, i_rng, i, j
  
  seed = random_seed()
  n_stream = 1
  !$ n_stream = omp_get_max_threads()
  allocate(rng(n_stream))
  do i=1,n_stream
    call rng(i)%initialize(6, seed, n_stream, i)
  end do
  
  !$omp parallel default(private), shared(rng)
  i_rng = 1
  !$ i_rng = omp_get_thread_num()+1
  
  !$omp do
  do j=1,size(particles,1)
    call rng(i_rng)%next(ran)
  end do
  !$omp end do
  !$omp end parallel
```

To use this with a hybrid MPI-OpenMP architecture we need to calculate the stream number and index across the processors.
This can be done easily with a few MPI calls combined with the above example.

### Sobol' sequence QRNG

The `sobseq` qrng has some properties which need to be treated with care.

#### Output stream correlation

The strength of the Sobol' sequence is the correlation in the output stream, but this causes some problems too.
For instance in the first stream of the sobseq generator every even number is > 0.5.
This has consequences for rejection sampling in parallel, where we use the strided generator to provide multiple streams. It is very important to try an equal number of samples on every thread, instead of looking for an equal number of accepted proposals.

#### Strided generation

Due to the strided implementation of the `sobseq` generator it can only accept a number of streams which is a power of 2.

#### Seeding

The Sobol' series has no possibility of seeding with any number. The `seed` parameter is ignored in calls to `rng%initialize`.

## Implementation

To simplify adoption in JOREK and the testing of different generators I have created an interface for random-number generators in `tools/mod_rng.f90`.
This is at present implemented by two different generators:

- pcg32 (`tools/mod_pcg32_rng.f90` using `tools/mod_pcg32.f90` and `tools/pcg_basic.c`)
- Sobol sequence (`tools/mod_sobseq_rng.f90` using `tools/mod_sobseq.f90`)

### Interface

An implementation of the RNG interface must provide the following routines:

- `initialize(rng, n_dims, seed, n_streams, i_stream, ierr)`
- `next(rng, out)`
- `jump_ahead(rng, delta)`

whose names should be self-explanatory.

## Seeding

I have also provided a module to create seed numbers for the generator, from `/dev/urandom` or by xor-ing the time and current process pid in `tools/mod_random_seed.f90`.