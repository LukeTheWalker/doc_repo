"""
Minimal illustration of the divertor indentation function:

    delta_r(theta, phi) = d * f_theta(theta) * f_phi(phi)
                          / sqrt(cos^2(theta) + (sin(theta)/kappa)^2)

where f_theta, f_phi are smooth tanh envelopes and kappa is the elongation.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.rcParams.update(
    {
        "font.family": "serif",
    }
)


# example parameters (W7-A field period = 72 deg)
depth_mm      = 50.0    # d: max indentation depth [mm]
theta_center  = 0.0     # outboard midplane [deg]
theta_width   = 30.0    # half-width in theta [deg]
phi_center    = 36.0    # middle of field period [deg]
phi_width     = 20.0    # half-width in phi [deg]
kappa         = 1.5     # elongation
smooth_width  = 10.0    # tanh transition width [deg]
field_period  = 72.0    # one W7-A field period [deg]


# ============================================================================
# functions
def tanh_envelope(x, center, half_width, smooth):
    """Smooth top-hat: 1 inside [center-half_width, center+half_width], 0 outside."""
    left  = 0.5 * (1 + np.tanh((x - (center - half_width)) / smooth))
    right = 0.5 * (1 - np.tanh((x - (center + half_width)) / smooth))
    return left * right


def indentation(theta_deg, phi_deg):
    """Delta_r in mm."""
    f_theta = tanh_envelope(theta_deg, theta_center, theta_width, smooth_width)
    f_phi   = tanh_envelope(phi_deg,   phi_center,   phi_width,   smooth_width)
    t = np.radians(theta_deg)
    geom = np.sqrt(np.cos(t)**2 + (np.sin(t) / kappa)**2)
    return depth_mm * f_theta * f_phi / geom

# grid
theta = np.linspace(-180, 180, 361)
phi   = np.linspace(0, field_period, 145)
th, ph = np.meshgrid(theta, phi)
dr = indentation(th, ph)

# plot the grid
fig, ax = plt.subplots(figsize=(7, 3.7))
n_levels = 20
levels = np.linspace(0, dr.max(), n_levels + 1)
cf = ax.contourf(theta, phi, dr, levels=levels, cmap='Reds')
cbar = fig.colorbar(cf, ax=ax, pad=0.02)
cbar.set_label('Indentation [mm]', fontsize=11)

ax.axvline(theta_center, color='gray', lw=0.9, ls='--', alpha=0.8)
ax.axhline(phi_center,   color='gray', lw=0.9, ls='--', alpha=0.8)

ax.set_xlabel(r'$\theta$ [deg]', fontsize=11)
ax.set_ylabel(r'$\phi$ [deg]', fontsize=11)
ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.set_xlim(-180, 180)
ax.set_ylim(0, field_period)

fig.tight_layout()
outfile = 'w7a_divertor_indentation_example_map.png'
fig.savefig(outfile, dpi=150)
plt.show()
