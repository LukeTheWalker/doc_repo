"""
W7-A Divertor Grid Modification at gvec2jorek.dat Level
========================================================
Modifies gvec2jorek.dat to create a divertor-indented grid by:
1. Moving boundary nodes inward (tanh smoothing)
2. Proportionally scaling interior nodes
3. Recomputing ALL derivatives using PchipInterpolator
4. Keeping field values at original grid indices (model180 recomputes equilibrium)
5. Converting back to Fourier modes and writing new gvec2jorek.dat

Key improvement over modify_grid_proper.py (H5-level approach):
- Derivatives are COMPUTED FROM new geometry, not inherited from old one
- Model180 sees a geometrically consistent grid and computes proper chi_correction
- Eliminates the 10mm convergence cliff from stale handle vectors

Pipeline: gvec2jorek_indented.dat --> model180 --> jorek000001.h5 --> model183

Usage:
    python modify_gvec2jorek_divertor.py --depth 10
    python modify_gvec2jorek_divertor.py --depth 15 --output gvec2jorek_15mm.dat
    python modify_gvec2jorek_divertor.py --depth 10 15 20 30   # batch mode

Author: Elias Waagaard (elwa)
Date: February 2026
"""

import numpy as np
import sys
import argparse
import time
from pathlib import Path
from scipy.interpolate import PchipInterpolator, make_interp_spline
import helper_gvec2jorek as h

# ============================================================================
# CONFIGURATION
# ============================================================================
CONFIG = {
    'input_file': 'gvec2jorek.dat',
    'output_dir': '.',

    # W7-A grid
    'n_flux': 41,
    'n_tht': 48,
    'nfp': 5,
    'n_planes_fourier': 64,

    # W7-A geometry
    'R0': 1.99,
    'field_period_deg': 72.0,  # 360/5

    # Divertor parameters (to be changed)
    'div_theta_center': 0.0,      # outboard midplane [deg]
    'div_theta_width': 30.0,      # half-width in theta [deg]
    'div_phi_center': 36.0,       # middle of field period [deg]
    'div_phi_width': 20.0,        # half-width in phi [deg]
    'div_ellipticity': 1.5,       # Z elongation
    'tanh_smooth_width': 10.0,    # smoothing width [deg]
}

ALL_NAMES = [
    'R', 'R_s', 'R_t', 'R_st',
    'Z', 'Z_s', 'Z_t', 'Z_st',
    'P', 'P_s', 'P_t', 'P_st',
    'A_R', 'A_R_s', 'A_R_t', 'A_R_st',
    'A_Z', 'A_Z_s', 'A_Z_t', 'A_Z_st',
    'A_phi', 'A_phi_s', 'A_phi_t', 'A_phi_st',
    'B_R', 'B_R_s', 'B_R_t', 'B_R_st',
    'B_Z', 'B_Z_s', 'B_Z_t', 'B_Z_st',
    'B_phi', 'B_phi_s', 'B_phi_t', 'B_phi_st',
    'J_R', 'J_R_s', 'J_R_t', 'J_R_st',
    'J_Z', 'J_Z_s', 'J_Z_t', 'J_Z_st',
    'J_phi', 'J_phi_s', 'J_phi_t', 'J_phi_st',
]

POSITION_NAMES = ['R', 'R_s', 'R_t', 'R_st', 'Z', 'Z_s', 'Z_t', 'Z_st']

FIELD_SETS = [
    ('P', 'P_s', 'P_t', 'P_st'),
    ('A_R', 'A_R_s', 'A_R_t', 'A_R_st'),
    ('A_Z', 'A_Z_s', 'A_Z_t', 'A_Z_st'),
    ('A_phi', 'A_phi_s', 'A_phi_t', 'A_phi_st'),
    ('B_R', 'B_R_s', 'B_R_t', 'B_R_st'),
    ('B_Z', 'B_Z_s', 'B_Z_t', 'B_Z_st'),
    ('B_phi', 'B_phi_s', 'B_phi_t', 'B_phi_st'),
    ('J_R', 'J_R_s', 'J_R_t', 'J_R_st'),
    ('J_Z', 'J_Z_s', 'J_Z_t', 'J_Z_st'),
    ('J_phi', 'J_phi_s', 'J_phi_t', 'J_phi_st'),
]


# ============================================================================
# GVEC FILE I/O
# ============================================================================

def read_gvec_file(filepath, n_tht, n_flux):
    """Read complete GVEC file."""
    data = {}
    metadata = {}
    with open(filepath, 'r') as f:
        for line in f:
            if '##<<' in line and 'number of grid' in line:
                break
        line = f.readline()
        n_rad, n_theta, n_phi = map(int, line.strip().split())
        metadata['n_rad'] = n_rad
        metadata['n_theta'] = n_theta
        metadata['n_phi'] = n_phi
        if n_rad != n_flux or n_theta != n_tht:
            raise ValueError(f"Grid mismatch: file ({n_rad},{n_theta}) vs "
                             f"expected ({n_flux},{n_tht})")

        for line in f:
            if '##<<' in line and 'global' in line:
                break
        line = f.readline()
        params = list(map(int, line.strip().split()))
        metadata['coord_type'] = params[0]
        metadata['nfp'] = params[1]
        metadata['asym'] = params[2]
        metadata['m_max'] = params[3]
        metadata['n_max'] = params[4]
        metadata['n_modes'] = params[5]
        metadata['global_line'] = line.strip()

        for line in f:
            if '##<<' in line and 'Variable' in line:
                break
        for name in ALL_NAMES:
            data[name] = h.read_gvec_data(f, n_tht, n_flux, metadata['n_modes'])

    print(f"  Read {len(data)} fields, grid {n_flux}x{n_tht}, "
          f"nfp={metadata['nfp']}, n_modes={metadata['n_modes']}")
    return data, metadata


def write_gvec(outfile, infile, data_new, n_flux, n_tht, metadata):
    """Write modified GVEC file, copying header from original."""
    with open(outfile, 'w') as out:
        with open(infile, 'r') as inp:
            for line in inp:
                if '##<<' in line and 'number of grid' in line:
                    out.write(line)
                    break
                out.write(line)
            inp.readline()  # skip old grid line
            out.write(f"{n_flux:8d}{n_tht:8d}{metadata['n_phi']:8d}\n")
            line = inp.readline()
            out.write(line)
            line = inp.readline()
            out.write(line)
            inp.readline()  # skip old format line
        for name in ALL_NAMES:
            h.write_gvec_data(out, data_new[name], name)
    print(f"  Written: {outfile}")
    print(f"  Size: {Path(outfile).stat().st_size / 1e6:.1f} MB")


# ============================================================================
# DIVERTOR GEOMETRY
# ============================================================================

def tanh_smooth(x, center, width, smooth_width):
    """Smooth envelope: 1 inside [center-width, center+width], 0 outside."""
    left = 0.5 * (1 + np.tanh((x - (center - width)) / smooth_width))
    right = 0.5 * (1 - np.tanh((x - (center + width)) / smooth_width))
    return left * right


def compute_indentation(R, Z, phi_deg, depth_mm, cfg):
    """Compute radial indentation (in meters) for each node.

    Args:
        R, Z: arrays of node positions
        phi_deg: toroidal angle in degrees
        depth_mm: maximum indentation depth in mm
        cfg: configuration dict

    Returns:
        delta_r: radial indentation (positive = inward), same shape as R
    """
    depth = depth_mm / 1000.0  # mm -> m
    R0 = cfg['R0']
    theta_deg = np.degrees(np.arctan2(Z, R - R0))

    theta_factor = tanh_smooth(theta_deg, cfg['div_theta_center'],
                               cfg['div_theta_width'], cfg['tanh_smooth_width'])

    phi_mod = phi_deg % cfg['field_period_deg']
    phi_factor = tanh_smooth(phi_mod, cfg['div_phi_center'],
                             cfg['div_phi_width'], cfg['tanh_smooth_width'])

    theta_rad = np.radians(theta_deg)
    ellipse_factor = np.sqrt(np.cos(theta_rad)**2 +
                             (np.sin(theta_rad) / cfg['div_ellipticity'])**2)

    return depth * theta_factor * phi_factor / ellipse_factor


# ============================================================================
# DERIVATIVE COMPUTATION
# ============================================================================

def recompute_derivatives(data_real, n_flux, n_tht, i_plane, coord_names=None):
    """Recompute _s, _t, _st derivatives for ALL radial layers using
    PchipInterpolator on the actual node positions.

    This is the key improvement: derivatives are computed FROM the new positions,
    not inherited from the old geometry.
    """
    if coord_names is None:
        coord_names = ['R', 'Z']

    tht = np.linspace(0, 2 * np.pi, n_tht, endpoint=False)
    rad = np.linspace(0, 1, n_flux, endpoint=True)

    for coord in coord_names:
        nodes = data_real[coord][:, :, i_plane]  # (n_tht, n_flux)

        # Theta derivatives: periodic spline through each radial ring
        for irad in range(n_flux):
            ring = nodes[:, irad]
            ring_closed = np.append(ring, ring[0])
            tht_closed = np.append(tht, 2 * np.pi)
            spline = PchipInterpolator(tht_closed, ring_closed)
            data_real[f'{coord}_t'][:, irad, i_plane] = spline.derivative()(tht)

        # Radial derivatives: spline through each poloidal column
        for itht in range(n_tht):
            col = nodes[itht, :]
            spline = PchipInterpolator(rad, col)
            data_real[f'{coord}_s'][itht, :, i_plane] = spline.derivative()(rad)

        # Cross derivatives: differentiate _t in radial direction
        for itht in range(n_tht):
            col_t = data_real[f'{coord}_t'][itht, :, i_plane]
            spline = PchipInterpolator(rad, col_t)
            data_real[f'{coord}_st'][itht, :, i_plane] = spline.derivative()(rad)


def recompute_field_derivatives(data_real, n_flux, n_tht, i_plane, field_sets):
    """Recompute derivatives for field quantities to be consistent with
    the new grid spacing (even though field VALUES stay at original indices,
    their radial/poloidal derivatives need updating because the s- and t-spacing
    represents different physical distances on the modified grid).
    """
    tht = np.linspace(0, 2 * np.pi, n_tht, endpoint=False)
    rad = np.linspace(0, 1, n_flux, endpoint=True)

    for (val_name, s_name, t_name, st_name) in field_sets:
        nodes = data_real[val_name][:, :, i_plane]

        # Theta derivatives
        for irad in range(n_flux):
            ring = nodes[:, irad]
            ring_closed = np.append(ring, ring[0])
            tht_closed = np.append(tht, 2 * np.pi)
            spline = PchipInterpolator(tht_closed, ring_closed)
            data_real[t_name][:, irad, i_plane] = spline.derivative()(tht)

        # Radial derivatives
        for itht in range(n_tht):
            col = nodes[itht, :]
            spline = PchipInterpolator(rad, col)
            data_real[s_name][itht, :, i_plane] = spline.derivative()(rad)

        # Cross derivatives
        for itht in range(n_tht):
            col_t = data_real[t_name][itht, :, i_plane]
            spline = PchipInterpolator(rad, col_t)
            data_real[st_name][itht, :, i_plane] = spline.derivative()(rad)


# ============================================================================
# MAIN MODIFICATION LOGIC
# ============================================================================

def modify_grid_divertor(data, metadata, depth_mm, cfg):
    """Modify gvec2jorek.dat grid with divertor indentation.

    Returns modified data dict (Fourier modes) and real-space data.
    """
    n_flux = cfg['n_flux']
    n_tht = cfg['n_tht']
    nfp = cfg['nfp']
    n_modes = metadata['n_modes']
    n_planes = cfg['n_planes_fourier']

    phi = np.linspace(0, 2 * np.pi / nfp, n_planes, endpoint=False)
    phi_deg = np.degrees(phi)

    # Convert ALL data to real space for modification
    print("  Converting to real space...")
    data_real = {}
    for name in ALL_NAMES:
        data_real[name] = h.evaluate_data_full(data[name], phi, nfp)

    # --- Modify positions ---
    print(f"  Applying divertor indentation: depth = {depth_mm} mm")
    R0 = cfg['R0']
    max_indent = 0.0

    for i_plane in range(n_planes):
        R_bnd = data_real['R'][:, -1, i_plane]
        Z_bnd = data_real['Z'][:, -1, i_plane]

        # Compute indentation at boundary
        delta_r = compute_indentation(R_bnd, Z_bnd, phi_deg[i_plane],
                                      depth_mm, cfg)
        max_indent = max(max_indent, np.max(delta_r))

        # Radial direction from axis to each boundary node
        R_axis = np.mean(data_real['R'][:, 0, i_plane])
        Z_axis = np.mean(data_real['Z'][:, 0, i_plane])

        dR_bnd = R_bnd - R_axis
        dZ_bnd = Z_bnd - Z_axis
        r_bnd = np.sqrt(dR_bnd**2 + dZ_bnd**2)

        # Unit radial direction
        eR = dR_bnd / r_bnd
        eZ = dZ_bnd / r_bnd

        # Move boundary inward
        R_bnd_new = R_bnd - delta_r * eR
        Z_bnd_new = Z_bnd - delta_r * eZ

        # Proportional scaling of ALL interior layers
        for irad in range(n_flux):
            frac = irad / (n_flux - 1)  # 0 at axis, 1 at boundary
            R_old = data_real['R'][:, irad, i_plane]
            Z_old = data_real['Z'][:, irad, i_plane]

            # Scale: axis stays fixed, boundary gets full indentation
            data_real['R'][:, irad, i_plane] = R_old - frac * delta_r * eR
            data_real['Z'][:, irad, i_plane] = Z_old - frac * delta_r * eZ

    print(f"  Max indentation: {max_indent*1000:.2f} mm")

    # --- Recompute position derivatives ---
    print("  Recomputing position derivatives (PchipInterpolator)...")
    t0 = time.time()
    for i_plane in range(n_planes):
        recompute_derivatives(data_real, n_flux, n_tht, i_plane, ['R', 'Z'])

        # Check Jacobian
        xjac = (data_real['R_s'][:, :, i_plane] * data_real['Z_t'][:, :, i_plane] -
                data_real['R_t'][:, :, i_plane] * data_real['Z_s'][:, :, i_plane])
        n_neg = np.sum(xjac <= 0)
        if n_neg > 0 and i_plane % 8 == 0:
            print(f"    Plane {i_plane}: {n_neg} negative Jacobian points")
        if i_plane % 16 == 0:
            print(f"    Plane {i_plane}/{n_planes}: "
                  f"Jac_min={np.min(xjac):.3e}, Jac_max={np.max(xjac):.3e}")
    t_pos = time.time() - t0
    print(f"  Position derivatives: {t_pos:.1f}s")

    # --- Recompute field derivatives ---
    # Field VALUES stay at original grid indices (they represent the same
    # flux surfaces, just at slightly different physical positions).
    # Model180 will recompute the equilibrium anyway.
    # But derivatives need updating because the grid spacing changed.
    print("  Recomputing field derivatives...")
    t0 = time.time()
    for i_plane in range(n_planes):
        recompute_field_derivatives(data_real, n_flux, n_tht, i_plane, FIELD_SETS)
    t_field = time.time() - t0
    print(f"  Field derivatives: {t_field:.1f}s")

    # --- Convert back to Fourier modes ---
    print("  Converting to Fourier modes...")
    data_new = {}
    for name in ALL_NAMES:
        data_new[name] = h.calculate_modes_full(data_real[name], phi, n_modes, nfp)

    # --- Verification ---
    print("\n  Verification at phi=0:")
    phi0 = np.array([0.0])
    for name in ['R', 'Z']:
        vals = h.evaluate_data_full(data_new[name], phi0, nfp)
        vals_orig = h.evaluate_data_full(data[name], phi0, nfp)
        print(f"    {name}: axis orig={vals_orig[0,0,0]:.6f} new={vals[0,0,0]:.6f}, "
              f"bnd orig={vals_orig[0,-1,0]:.6f} new={vals[0,-1,0]:.6f}")

    # Jacobian check from modes
    R_s = h.evaluate_data_full(data_new['R_s'], phi0, nfp)[:, :, 0]
    Z_s = h.evaluate_data_full(data_new['Z_s'], phi0, nfp)[:, :, 0]
    R_t = h.evaluate_data_full(data_new['R_t'], phi0, nfp)[:, :, 0]
    Z_t = h.evaluate_data_full(data_new['Z_t'], phi0, nfp)[:, :, 0]
    jac = R_s * Z_t - R_t * Z_s
    print(f"    Jacobian: min={np.min(jac):.3e}, max={np.max(jac):.3e}, "
          f"n_neg={np.sum(jac <= 0)}")

    # Max displacement
    R_new = h.evaluate_data_full(data_new['R'], phi0, nfp)[:, :, 0]
    Z_new = h.evaluate_data_full(data_new['Z'], phi0, nfp)[:, :, 0]
    R_orig = h.evaluate_data_full(data['R'], phi0, nfp)[:, :, 0]
    Z_orig = h.evaluate_data_full(data['Z'], phi0, nfp)[:, :, 0]
    disp = np.sqrt((R_new - R_orig)**2 + (Z_new - Z_orig)**2)
    print(f"    Max displacement: {np.max(disp)*1000:.2f} mm")

    return data_new, data_real


# ============================================================================
# MAIN
# ============================================================================

def main(depths_mm, cfg):
    """Run divertor indentation for one or more depths."""
    print("=" * 70)
    print("W7-A Divertor Grid Modification (gvec2jorek level)")
    print("=" * 70)

    # Read input once
    print(f"\nReading: {cfg['input_file']}")
    data, metadata = read_gvec_file(cfg['input_file'], cfg['n_tht'], cfg['n_flux'])

    for depth in depths_mm:
        print(f"\n{'='*70}")
        print(f"Processing depth = {depth} mm")
        print(f"{'='*70}")

        output_file = cfg.get('output_file', None)
        if output_file is None:
            output_file = str(Path(cfg['output_dir']) /
                              f"gvec2jorek_divertor_{depth}mm.dat")

        t0 = time.time()
        data_new, data_real = modify_grid_divertor(data, metadata, depth, cfg)
        dt = time.time() - t0

        print(f"\n  Writing: {output_file}")
        write_gvec(output_file, cfg['input_file'], data_new,
                   cfg['n_flux'], cfg['n_tht'], metadata)
        print(f"  Total time: {dt:.1f}s")

    print("\nDone.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Modify W7-A gvec2jorek.dat with divertor indentation')
    parser.add_argument('--depth', type=float, nargs='+', required=True,
                        help='Indentation depth(s) in mm (e.g., 10 15 20 30)')
    parser.add_argument('--output', type=str, default=None,
                        help='Output file path (only for single depth)')
    args = parser.parse_args()

    cfg = CONFIG.copy()
    if args.output is not None:
        if len(args.depth) > 1:
            raise ValueError("--output only valid for single depth")
        cfg['output_file'] = args.output

    main(args.depth, cfg)
