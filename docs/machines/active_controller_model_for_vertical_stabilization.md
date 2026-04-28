---
title: "Active controller model for vertical stabilization"
parent: "ASDEX Upgrade"
layout: default
render_with_liquid: false
---

# Active controller model for vertical stabilization

A PID controller was added to JOREK to enable active stabilization in free-boundary simulations including $n=0$.

## Fundamentals


It acts on specific coils based on the vertical axis position and its evolution in the simulation according to:

$$
\begin{align}
\Delta I &=  K_\text{P}\,e(t) + K_\text{D} \frac{\mathrm{d} e(t)}{\mathrm{d} t} + K_\text{I} \int_{t_0}^{t} e(t)
\end{align}
$$

where $e=Z(t)-Z_\text{ref}(t)$ is the deviation from the reference value and $K_\text{P}$, $K_\text{I}$, $K_\text{D}$ are the proportional, integral and derivative gains.

## Implementation in JOREK

The equation above is discretized and built into the `coil_current_source` routine in `vacuum/vacuum_response.dat` after the current profile of the PF coils is interpolated. There, it has the following form:

$$
\begin{align}
\mathrm{d}Z_\text{err} &= Z_\text{axis}(t_n) - Z_\text{ref}(t_n)\\
\mathrm{d}Z_\text{der} &= \frac{Z_\text{axis}(t_n) - Z_\text{axis}(t_{n-1})}{\Delta t}\\
\mathrm{d}Z_\text{integral} +&= \left(Z_\text{axis}(t_n) - Z_\text{ref}(t_{n})\right)\Delta t \\\\
\Delta I &=   K_\text{P}\,\mathrm{d}Z_\text{err} + K_\text{D}\,\mathrm{d}Z_\text{der}   + K_\text{I} \,\mathrm{d}Z_\text{integral}\\
I(i) &=  I(i) + \mathrm{vert\_FB\_amp\_ts}(i)\,\Delta I  
\end{align}
$$

It has the following features with the parameters listed in the table below:

- Activate the controller after a certain time `start_VFB_ts`
- Use a constant reference value or an input profile
- Specify the tact time, a periodic interval after which the controller acts
- Set coil current limits for each coil individually
- Set an amplification factor for each coil individually to distribute the action

The controller is only activated if the amplification factors are specified and if the start time is exceeded.

## Parameters

| Parameter | Comment | Typical values |
| --- | --- | --- |
| `vert_FB_gain(1)` | proportional gain $K_\text{P}$ | `1.e0` (case dependent) |
| `vert_FB_gain(2)` | derivative gain $K_\text{D}$ | `1.e0` |
| `vert_FB_gain(3)` | integral gain $K_\text{I}$ | `1.e0` |
| `start_VFB_ts` [$t_{\text{JOREK}}$] | start time of vertical feedback | `-` |
| `vert_FB_amp_ts` | gain amplification factor for individual coils | $>0$ for upper, $<0$ for lower coils |
| `I_coils_max` [A] | maximum allowed current in the PF coil | case specific |
| `vert_FB_tact` [$t_{\text{JOREK}}$] | apply VFB only periodically | optional |
| `Z_ref_ts(t)` | time trace of reference axis position | case specific |
| `vert_pos_file` [$t_{\text{JOREK}}$ \| m] | input file for time dependent axis position | - |


## How to specify the input profile

The position can be specified by either:

- an input profile file (`vert_pos_file`)
  - the time is given in [$t_{\text{JOREK}}$]
  - the vertical position in [m]
  - when the simulation is longer than specified by the profile, the last value of the profile is used as the reference.
- the input parameter `Z_axis_ref` also used for the free boundary equilibrium
- if none of this is specified, the initial or restart value of the axis is used

## Tuning
The optimal gains can vary from case to case, depending on the equilibrium parameters and the use case.

Normally, the axis oscillates during the first time steps when the controller is active.
This oscillation can be used to adjust the gains. Otherwise, a sudden variation in the target value (a step response) can be used to improve the settings. 

The tuning can be performed in three steps:

- Increase $K_\text{P}$ with the other gains at 0 until the oscillation amplitude is low and the overshoot is small in the case of a step response. If $K_\text{P}$ is too high, the response will overshoot and the system becomes unstable.
- Increase $K_\text{D}$ to reduce the oscillations.
- Increase $K_\text{I}$ if there is an error in steady state. (I have not seen a big effect of this so far, and the error was usually very low with only $K_\text{P}$ and $K_\text{D}$ gains.)



