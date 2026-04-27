"""
Example script for two-step harmonic-mapping + divertor moulding for W7-X grid extension.

Step 1 (harmonic mapping): per phi plane, map LCFS -> conformal envelope
(uniformly scaled LCFS). pybie2d Laplace-Dirichlet solve gives smooth,
positive-Jacobian intermediate shells.

Step 2 (divertor moulding): compute displacement field from ray-intersection
with divertor targets, then proportionally rescale ALL extension shells
inward (scale_field). Preserves monotonicity and positive Jacobians.
"""

import logging
import numpy as np
import sys
import time
from pathlib import Path
from scipy.interpolate import CubicSpline, PchipInterpolator, make_interp_spline
import helper_gvec2jorek as h
logging.basicConfig(level=logging.WARNING)  # suppress pybie2d info spam

# ============================================================================
# CONFIGURATION and PARAMETERS
# ============================================================================

# TO DO: add actual link to files when become available

INPUT_FILE = Path("gvec2jorek.dat") # input gvec2jorek file with interpolated B_vac field (from w7x_mgrid2bvac.py)
OUTPUT_DIR = Path(__file__).parent # where output plots will be produced
DIV_DIR = Path("WALL_DIV") # w7-x divertor files (Kisslinger format) from EMC3-Lite universal

N_FLUX = 41           # original W7-X GVEC shells
N_EXT = 12            # extension layers
N_THT = 48
NFP = 5
N_PLANES = 64         # phi planes for Fourier decomposition

# Step 1: Conformal envelope (harmonic mapping target)
# Additive (not proportional), like rays out from LCFS: W7-X r_lcfs varies 0.3-1.8m
CONFORMAL_EXT_M = 0.150   # 150mm additive envelope (uniform at all theta)

# Step 2: Divertor moulding (post-harmonic indentation)
DIVERTOR_MARGIN_M = 0.005 # 5mm margin inside divertor targets
DIVERTOR_SMOOTH_DEG = 25.0  # cosine taper at theta cluster edges [deg]
PHI_TAPER_DEG = 15.0      # cosine taper at phi edges of divertor range [deg]
SCALE_MIN = 0.05          # minimum extension-width fraction (prevents collapse)
SCALE_MAX = 3.0           # maximum extension-width fraction (limits push-out)
MOULD_FRAC = 1.0          # moulding fraction (1.0 = full, 0.5 = half indent)
N_FINE = 720              # fine theta grid for ray tracing

# Harmonic mapping
N_BND_PTS = 512           # boundary discretization for pybie2d
NEWTON_TOL = 1e-8         # Newton convergence tolerance
NEWTON_MAX_ITER = 80      # max Newton iterations
GRID_NXY = 1000           # pybie2d grid resolution (NxN)

# Divertor files
PERIOD_DEG = 72.0
FLIP_DIVERTOR_PHI = True
PHI_MATCH_TOL_DEG = 2.5

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
# GVEC FILE I/O (reuse from extend_grid_scale_rescale.py)
# ============================================================================

def read_gvec_file(filepath, n_tht, n_flux):
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
            raise ValueError(f"Grid mismatch: ({n_rad},{n_theta}) vs ({n_flux},{n_tht})")
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
        metadata['n_phi'] = 2 * params[4]
        for line in f:
            if '##<<' in line and 'Variable' in line:
                break
        for name in ALL_NAMES:
            data[name] = h.read_gvec_data(f, n_tht, n_flux, metadata['n_modes'])
    print(f"  Read {filepath.name}: {n_flux}x{n_tht}, "
          f"nfp={metadata['nfp']}, n_modes={metadata['n_modes']}")
    return data, metadata


def write_gvec_file(outfile, infile, data, n_flux_out, n_tht, metadata):
    with open(outfile, 'w') as out:
        with open(str(infile), 'r') as inp:
            for line in inp:
                if '##<<' in line and 'number of grid' in line:
                    out.write(line)
                    break
                out.write(line)
            inp.readline()
            out.write(f"{n_flux_out:8d}{n_tht:8d}{metadata['n_phi']:8d}\n")
            line = inp.readline()
            out.write(line)
            line = inp.readline()
            out.write(line)
            inp.readline()
        for name in ALL_NAMES:
            h.write_gvec_data(out, data[name], name)
    print(f"  Written: {outfile} ({Path(outfile).stat().st_size / 1e6:.1f} MB)")


# ============================================================================
# DIVERTOR GEOMETRY
# ============================================================================

def read_kisslinger_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    header = lines[1].split()
    n_phi_k = int(header[0])
    n_r = int(header[1])
    slices = []
    idx = 2
    for _ in range(n_phi_k):
        phi_deg = float(lines[idx].strip())
        idx += 1
        pts = []
        for _ in range(n_r):
            v = lines[idx].split()
            pts.append((float(v[0]) / 100.0, float(v[1]) / 100.0))
            idx += 1
        slices.append((phi_deg, pts))
    return slices


def load_all_divertors():
    fnames = ['div_hor_upper_0_1.5', 'div_hor_upper_1.5_19', 'div_ver_upper',
              'div_hor_lower_0_15', 'div_hor_lower_15_28']
    raw = {}
    for fn in fnames:
        fp = DIV_DIR / fn
        if fp.exists():
            raw[fn] = read_kisslinger_file(fp)
            print(f"  Loaded {fn}: {len(raw[fn])} phi slices")
    divs = {}
    for group_name, file_list in [
        ('upper_hor', ['div_hor_upper_0_1.5', 'div_hor_upper_1.5_19']),
        ('lower_hor', ['div_hor_lower_0_15', 'div_hor_lower_15_28']),
        ('upper_ver', ['div_ver_upper']),
    ]:
        merged = {}
        for fn in file_list:
            if fn in raw:
                for phi, pts in raw[fn]:
                    merged[phi] = pts
        if merged:
            divs[group_name] = sorted(merged.items())
    return divs


def get_divertor_segments_at_phi(divertors, target_phi_deg):
    segments = []
    for fname, slices in divertors.items():
        best_dphi = PHI_MATCH_TOL_DEG + 1
        best_match = None
        for phi_emc3, points in slices:
            phi_j = (PERIOD_DEG - phi_emc3) % PERIOD_DEG if FLIP_DIVERTOR_PHI \
                else phi_emc3 % PERIOD_DEG
            dphi = abs(phi_j - target_phi_deg)
            if dphi > PERIOD_DEG / 2:
                dphi = PERIOD_DEG - dphi
            if dphi < best_dphi:
                best_dphi = dphi
                best_match = (points, False)
            phi_sym = (PERIOD_DEG - phi_j) % PERIOD_DEG
            if abs(phi_sym - phi_j) > 1.0:
                dphi_sym = abs(phi_sym - target_phi_deg)
                if dphi_sym > PERIOD_DEG / 2:
                    dphi_sym = PERIOD_DEG - dphi_sym
                if dphi_sym < best_dphi:
                    best_dphi = dphi_sym
                    best_match = (points, True)
        if best_match is not None and best_dphi <= PHI_MATCH_TOL_DEG:
            pts, z_flip = best_match
            for i in range(len(pts) - 1):
                R1, Z1 = pts[i]
                R2, Z2 = pts[i + 1]
                if z_flip:
                    Z1, Z2 = -Z1, -Z2
                segments.append((R1, Z1, R2, Z2))
    return segments


# ============================================================================
# RAY INTERSECTION
# ============================================================================

def ray_segment_intersection(R_axis, Z_axis, theta_rad, R1, Z1, R2, Z2):
    dir_R = np.cos(theta_rad)
    dir_Z = np.sin(theta_rad)
    dR_seg = R2 - R1
    dZ_seg = Z2 - Z1
    det = dir_R * (-dZ_seg) - dir_Z * (-dR_seg)
    if abs(det) < 1e-20:
        return None
    dR0 = R1 - R_axis
    dZ0 = Z1 - Z_axis
    t = (dR0 * (-dZ_seg) - dZ0 * (-dR_seg)) / det
    s = (dR0 * (-dir_Z) - dZ0 * (-dir_R)) / det
    if t > 0 and -0.05 <= s <= 1.05:
        return t
    return None


# ============================================================================
# TARGET BOUNDARY CONSTRUCTION
# ============================================================================

def construct_target_boundary(R_lcfs, Z_lcfs, R_axis, Z_axis,
                              phi_deg_label=""):
    """Construct conformal envelope: LCFS + additive offset at all angles.

    No divertor consideration here -- divertor following is handled by
    the moulding step AFTER harmonic mapping.

    Returns: R_target(N_THT), Z_target(N_THT)
    """
    dR = R_lcfs - R_axis
    dZ = Z_lcfs - Z_axis
    r_lcfs = np.sqrt(dR**2 + dZ**2)
    angle = np.arctan2(dZ, dR)

    r_target = r_lcfs + CONFORMAL_EXT_M

    R_target = R_axis + r_target * np.cos(angle)
    Z_target = Z_axis + r_target * np.sin(angle)

    return R_target, Z_target


# ============================================================================
# DIVERTOR MOULDING (Step 2: post-harmonic indentation, from run 016)
# ============================================================================

def compute_scale_at_phi(R_lcfs, Z_lcfs, R_outer, Z_outer, segments,
                         margin_m=DIVERTOR_MARGIN_M,
                         smooth_deg=DIVERTOR_SMOOTH_DEG):
    """Compute per-node scale field using LCFS-outward-direction rays.

    Instead of shooting rays from the magnetic axis (which fails at the bean
    indentation where divertors are at smaller polar radius than the LCFS),
    shoots rays from each LCFS point in the harmonic extension direction
    (LCFS -> conformal outer shell). This correctly handles concave regions.

    Returns: scale (n_theta,) - scale factor for extension width.
             scale < 1: pull toward divertor (inside conformal)
             scale > 1: push toward divertor (beyond conformal)
    """
    from scipy.interpolate import CubicSpline

    n_theta = len(R_lcfs)
    scale = np.ones(n_theta)
    if not segments:
        return scale

    n_fine = N_FINE
    theta_coarse = np.linspace(0, 2 * np.pi, n_theta, endpoint=False)
    theta_fine = np.linspace(0, 2 * np.pi, n_fine, endpoint=False)

    # Interpolate LCFS and outer boundary to fine grid (close loop for periodic)
    theta_closed = np.append(theta_coarse, 2 * np.pi)
    cs_Rl = CubicSpline(theta_closed, np.append(R_lcfs, R_lcfs[0]),
                         bc_type='periodic')
    cs_Zl = CubicSpline(theta_closed, np.append(Z_lcfs, Z_lcfs[0]),
                         bc_type='periodic')
    cs_Ro = CubicSpline(theta_closed, np.append(R_outer, R_outer[0]),
                         bc_type='periodic')
    cs_Zo = CubicSpline(theta_closed, np.append(Z_outer, Z_outer[0]),
                         bc_type='periodic')

    R_lc_f = cs_Rl(theta_fine)
    Z_lc_f = cs_Zl(theta_fine)
    R_out_f = cs_Ro(theta_fine)
    Z_out_f = cs_Zo(theta_fine)

    # Extension direction at each fine point (LCFS -> outer)
    dR_f = R_out_f - R_lc_f
    dZ_f = Z_out_f - Z_lc_f
    ext_len_f = np.sqrt(dR_f**2 + dZ_f**2)
    ext_angle_f = np.arctan2(dZ_f, dR_f)

    # Ray-trace from LCFS in extension direction on fine grid
    d_div_fine = np.full(n_fine, np.nan)
    for i in range(n_fine):
        if ext_len_f[i] < 1e-8:
            continue
        best_t = None
        for R1, Z1, R2, Z2 in segments:
            t = ray_segment_intersection(
                R_lc_f[i], Z_lc_f[i], ext_angle_f[i], R1, Z1, R2, Z2)
            if t is not None and t > 0:
                if best_t is None or t < best_t:
                    best_t = t
        if best_t is not None:
            d_div_fine[i] = best_t  # distance from LCFS to divertor

    has_div = ~np.isnan(d_div_fine)
    if not np.any(has_div):
        return scale

    # Cluster detection on fine grid
    div_indices = np.where(has_div)[0]
    gap_threshold = int(np.ceil(5.0 / (360.0 / n_fine)))
    clusters = []
    c_start = div_indices[0]
    for i in range(1, len(div_indices)):
        if div_indices[i] - div_indices[i - 1] > gap_threshold:
            clusters.append((c_start, div_indices[i - 1]))
            c_start = div_indices[i]
    clusters.append((c_start, div_indices[-1]))

    # Theta taper on fine grid
    f_theta_fine = np.zeros(n_fine)
    smooth_idx = max(1, int(np.ceil(smooth_deg / (360.0 / n_fine))))
    for cs, ce in clusters:
        if cs <= ce:
            f_theta_fine[cs:ce + 1] = 1.0
        else:
            f_theta_fine[cs:] = 1.0
            f_theta_fine[:ce + 1] = 1.0
        for i in range(1, smooth_idx + 1):
            idx = (cs - i) % n_fine
            frac = i / smooth_idx
            f_theta_fine[idx] = max(f_theta_fine[idx],
                                    0.5 * (1 + np.cos(np.pi * frac)))
        for i in range(1, smooth_idx + 1):
            idx = (ce + i) % n_fine
            frac = i / smooth_idx
            f_theta_fine[idx] = max(f_theta_fine[idx],
                                    0.5 * (1 + np.cos(np.pi * frac)))

    # Compute raw scale on fine grid (scale = (d_div + margin) / ext_len)
    raw_scale_fine = np.ones(n_fine)
    for i in range(n_fine):
        if ext_len_f[i] < 1e-8:
            continue
        if has_div[i]:
            raw_scale_fine[i] = (d_div_fine[i] + margin_m) / ext_len_f[i]
        elif f_theta_fine[i] > 1e-6:
            # Interpolate from nearest divertor hits
            left_i = right_i = None
            for d in range(1, n_fine // 2):
                if left_i is None and has_div[(i - d) % n_fine]:
                    left_i = (i - d) % n_fine
                if right_i is None and has_div[(i + d) % n_fine]:
                    right_i = (i + d) % n_fine
                if left_i is not None and right_i is not None:
                    break
            if left_i is not None and right_i is not None:
                d_l = min(abs(i - left_i), n_fine - abs(i - left_i))
                d_r = min(abs(i - right_i), n_fine - abs(i - right_i))
                w_l = d_r / (d_l + d_r)
                w_r = d_l / (d_l + d_r)
                d_interp = w_l * d_div_fine[left_i] + w_r * d_div_fine[right_i]
                l_interp = w_l * ext_len_f[left_i] + w_r * ext_len_f[right_i]
                if l_interp > 1e-8:
                    raw_scale_fine[i] = (d_interp + margin_m) / l_interp
            elif left_i is not None:
                raw_scale_fine[i] = (d_div_fine[left_i] + margin_m) / ext_len_f[left_i]
            elif right_i is not None:
                raw_scale_fine[i] = (d_div_fine[right_i] + margin_m) / ext_len_f[right_i]

    raw_scale_fine = np.clip(raw_scale_fine, SCALE_MIN, SCALE_MAX)

    # Map fine grid to coarse boundary nodes: blend scale with taper
    for ith in range(n_theta):
        fine_idx = int(np.round(theta_coarse[ith] / (2 * np.pi)
                                * n_fine)) % n_fine
        f_th = f_theta_fine[fine_idx]
        scale[ith] = 1.0 + f_th * (raw_scale_fine[fine_idx] - 1.0)

    return scale


def compute_scale_field(data_real, n_flux, n_flux_orig, divertors, phi_deg):
    """Compute full scale field (theta x phi) with toroidal cosine tapers.

    Uses LCFS-outward-direction rays for correct bean-indent handling.
    """
    n_theta = N_THT
    n_phi = len(phi_deg)
    i_lcfs = n_flux_orig - 1
    scale_field = np.ones((n_theta, n_phi), dtype=float)

    phi_has_data = np.zeros(n_phi, dtype=bool)
    for iphi in range(n_phi):
        segments = get_divertor_segments_at_phi(divertors, phi_deg[iphi])
        if segments:
            phi_has_data[iphi] = True

    if not np.any(phi_has_data):
        print("  WARNING: No divertor data found at any phi!")
        return scale_field

    phi_data_indices = np.where(phi_has_data)[0]
    phi_idx_min = phi_data_indices[0]
    phi_idx_max = phi_data_indices[-1]
    print(f"  Divertor phi range: {phi_deg[phi_idx_min]:.1f} - "
          f"{phi_deg[phi_idx_max]:.1f} deg")

    for iphi in range(n_phi):
        phi_j = phi_deg[iphi]

        # Phi taper
        if iphi < phi_idx_min:
            dphi = phi_deg[phi_idx_min] - phi_j
            if dphi > PHI_TAPER_DEG:
                continue
            f_phi = 0.5 * (1 + np.cos(np.pi * dphi / PHI_TAPER_DEG))
        elif iphi > phi_idx_max:
            dphi = phi_j - phi_deg[phi_idx_max]
            if dphi > PHI_TAPER_DEG:
                continue
            f_phi = 0.5 * (1 + np.cos(np.pi * dphi / PHI_TAPER_DEG))
        else:
            f_phi = 1.0

        segments = get_divertor_segments_at_phi(divertors, phi_j)

        R_lc = data_real['R'][:, i_lcfs, iphi]
        Z_lc = data_real['Z'][:, i_lcfs, iphi]
        R_out = data_real['R'][:, -1, iphi]
        Z_out = data_real['Z'][:, -1, iphi]

        per_phi_scale = compute_scale_at_phi(R_lc, Z_lc, R_out, Z_out, segments)

        # Apply phi taper: blend between 1.0 and per_phi_scale
        scale_field[:, iphi] = 1.0 + f_phi * (per_phi_scale - 1.0)

    return scale_field


def apply_scale_field(data_real, scale_field, n_flux, n_flux_orig, scale_frac):
    """Apply scale field to extension shells using LCFS-based direction.

    For each (theta, phi), scales the extension vector (LCFS -> shell)
    proportionally. Preserves radial monotonicity.
    """
    n_theta = N_THT
    n_phi = scale_field.shape[1]
    i_lcfs = n_flux_orig - 1
    max_disp = 0.0

    for iphi in range(n_phi):
        for ith in range(n_theta):
            raw_scale = scale_field[ith, iphi]
            # Blend with scale_frac (mould_frac)
            scale = 1.0 + scale_frac * (raw_scale - 1.0)
            if abs(scale - 1.0) < 1e-8:
                continue

            R_lc = data_real['R'][ith, i_lcfs, iphi]
            Z_lc = data_real['Z'][ith, i_lcfs, iphi]

            # Track displacement for reporting
            R_old = data_real['R'][ith, -1, iphi]
            Z_old = data_real['Z'][ith, -1, iphi]

            for irad in range(n_flux_orig, n_flux):
                R_i = data_real['R'][ith, irad, iphi]
                Z_i = data_real['Z'][ith, irad, iphi]
                dR = R_i - R_lc
                dZ = Z_i - Z_lc
                data_real['R'][ith, irad, iphi] = R_lc + dR * scale
                data_real['Z'][ith, irad, iphi] = Z_lc + dZ * scale

            R_new = data_real['R'][ith, -1, iphi]
            Z_new = data_real['Z'][ith, -1, iphi]
            disp = np.sqrt((R_new - R_old)**2 + (Z_new - Z_old)**2)
            max_disp = max(max_disp, disp)

    active = scale_field != 1.0
    if np.any(active):
        # Compute effective scale after scale_frac blending
        eff = 1.0 + scale_frac * (scale_field - 1.0)
        sc_active = eff[scale_field != 1.0]
        sc_min = sc_active.min()
        sc_max = sc_active.max()
    else:
        sc_min = sc_max = 1.0
    print(f"    Max displacement: {max_disp * 1000:.1f} mm")
    print(f"    Scale range: {sc_min:.3f} - {sc_max:.3f}")
    return scale_field


def enforce_coverage(data_real, n_flux, n_flux_orig, divertors, phi_deg,
                     margin_m=DIVERTOR_MARGIN_M, n_nearest=5):
    """Post-moulding coverage enforcement: push boundary nodes to envelop
    all divertor targets that are NOT inside the boundary polygon.

    Uses Cartesian closest-point approach (no polar coordinates).
    Projects uncovered divertor points onto the extension direction of each
    nearby boundary node and pushes outward if needed.
    """
    from matplotlib.path import Path as MplPath

    n_theta = N_THT
    i_lcfs = n_flux_orig - 1
    total_pushed = 0

    for iphi in range(len(phi_deg)):
        segments = get_divertor_segments_at_phi(divertors, phi_deg[iphi])
        if not segments:
            continue

        R_bnd = data_real['R'][:, -1, iphi].copy()
        Z_bnd = data_real['Z'][:, -1, iphi].copy()
        R_lc = data_real['R'][:, i_lcfs, iphi]
        Z_lc = data_real['Z'][:, i_lcfs, iphi]

        poly = MplPath(np.column_stack([np.append(R_bnd, R_bnd[0]),
                                        np.append(Z_bnd, Z_bnd[0])]))

        uncovered = []
        for R1, Z1, R2, Z2 in segments:
            for k in range(21):
                t = k / 20
                Rp = R1 + t * (R2 - R1)
                Zp = Z1 + t * (Z2 - Z1)
                if not poly.contains_point((Rp, Zp)):
                    uncovered.append((Rp, Zp))

        if not uncovered:
            continue

        # Compute max required push per boundary node
        push_factor = np.ones(n_theta)
        for Rp, Zp in uncovered:
            dists = np.sqrt((R_bnd - Rp)**2 + (Z_bnd - Zp)**2)
            nearest_idx = np.argsort(dists)[:n_nearest]

            for idx in nearest_idx:
                ext_R = R_bnd[idx] - R_lc[idx]
                ext_Z = Z_bnd[idx] - Z_lc[idx]
                ext_len = np.sqrt(ext_R**2 + ext_Z**2)
                if ext_len < 1e-8:
                    continue
                # Project uncovered point onto extension direction
                dp_R = Rp - R_lc[idx]
                dp_Z = Zp - Z_lc[idx]
                d_along = (dp_R * ext_R + dp_Z * ext_Z) / ext_len
                required = d_along + margin_m
                if required > ext_len:
                    factor = min(required / ext_len, SCALE_MAX)
                    push_factor[idx] = max(push_factor[idx], factor)
                    total_pushed += 1

        # Apply push to extension shells
        for ith in range(n_theta):
            if push_factor[ith] <= 1.0 + 1e-8:
                continue
            for irad in range(n_flux_orig, n_flux):
                dR = data_real['R'][ith, irad, iphi] - R_lc[ith]
                dZ = data_real['Z'][ith, irad, iphi] - Z_lc[ith]
                data_real['R'][ith, irad, iphi] = R_lc[ith] + dR * push_factor[ith]
                data_real['Z'][ith, irad, iphi] = Z_lc[ith] + dZ * push_factor[ith]

    print(f"    Coverage enforcement: {total_pushed} pushes across all phi planes")
    return total_pushed


# ============================================================================
# HARMONIC MAPPING (Laplace-Dirichlet via pybie2d)
# ============================================================================

def harmonic_ring_mapping(R_inner, Z_inner, R_outer, Z_outer, n_ext, n_tht,
                          phi_label=""):
    """Create n_ext smooth intermediate shells between inner and outer curves
    using harmonic mapping (Laplace-Dirichlet BVP).

    Returns: R_shells(n_tht, n_ext), Z_shells(n_tht, n_ext)
             shells are indexed from just past inner to just before outer
    """
    from pybie2d.boundaries.global_smooth_boundary.global_smooth_boundary import (
        Global_Smooth_Boundary as GSB)
    from pybie2d.boundaries.collection import BoundaryCollection
    from pybie2d.grid import Grid, PointSet
    from pybie2d.solvers.laplace_dirichlet import (
        LaplaceDirichletSolver, Laplace_Layer_Apply)
    from pybie2d.boundaries.global_smooth_boundary.laplace_close_quad import (
        Compensated_Laplace_Apply)
    from scipy.interpolate import griddata

    N = N_BND_PTS
    tau = np.linspace(0, 2 * np.pi, N, endpoint=False)

    # Create periodic splines for inner and outer curves (n_tht -> N)
    tht_gvec = np.linspace(0, 2 * np.pi, n_tht, endpoint=False)
    tht_closed = np.append(tht_gvec, 2 * np.pi)

    Ri_c = np.append(R_inner, R_inner[0])
    Zi_c = np.append(Z_inner, Z_inner[0])
    Ro_c = np.append(R_outer, R_outer[0])
    Zo_c = np.append(Z_outer, Z_outer[0])

    inner_spl = make_interp_spline(tht_closed,
                                   np.column_stack((Ri_c, Zi_c)),
                                   k=5, bc_type='periodic')
    outer_spl = make_interp_spline(tht_closed,
                                   np.column_stack((Ro_c, Zo_c)),
                                   k=5, bc_type='periodic')

    # pybie2d boundaries
    inner_pts = inner_spl(tau)
    outer_pts = outer_spl(tau)
    boundary_i = GSB(inner_pts[:, 0], inner_pts[:, 1])
    boundary_o = GSB(outer_pts[:, 0], outer_pts[:, 1])

    boundaryc = BoundaryCollection()
    boundaryc.add([boundary_o, boundary_i], ["i", "e"])
    boundaryc.amass_information()

    # Scale factor: inner boundary maps to circle of radius=scale
    scale = N_FLUX / (N_FLUX + N_EXT) * 0.5

    # Boundary conditions: map to circles in (xi, eta) space
    h_xi_i = np.cos(boundary_i.t)
    h_et_i = np.sin(boundary_i.t)
    h_xi_o = np.cos(boundary_o.t)
    h_et_o = np.sin(boundary_o.t)
    h_xi_b = np.concatenate([h_xi_o, scale * h_xi_i])
    h_et_b = np.concatenate([h_et_o, scale * h_et_i])

    # Solve Laplace BVP
    solver = LaplaceDirichletSolver(boundaryc, solve_type="formed",
                                    check_close=True)
    d_xi = solver.solve(h_xi_b)
    d_et = solver.solve(h_et_b)

    # Evaluate forward map on a grid to build initial guesses
    import map2disc
    bbox, bbox_border = map2disc.core.get_bounding_box(boundary_o)
    Nxy = GRID_NXY
    full_grid = Grid(bbox[0, :], Nxy, bbox[1, :], Nxy)
    int_i, ext_i = boundary_i.find_interior_points(full_grid)
    int_o, ext_o = boundary_o.find_interior_points(full_grid)
    grid_b = Grid(bbox[0, :], Nxy, bbox[1, :], Nxy,
                  mask=full_grid.reshape(ext_i & int_o))

    def eval_dipole(bnd, tgt, dip, gradient=False):
        """Evaluate dipole with close-point correction.
        Follows Orin's evaluate_dipole pattern from run_map2ring.py."""
        charge = dip * bnd.SLP_vector
        evals = Laplace_Layer_Apply(bnd, tgt, charge=charge, dipstr=dip,
                                    gradient=gradient)
        for b, (boundary, side) in enumerate(
                zip(bnd.boundaries, bnd.sides)):
            side_str = str(side)
            distance = boundary.tolerance_to_distance(1e-6)
            close_mask = tgt.find_near_points(boundary, distance)
            if np.sum(close_mask) == 0:
                continue
            close_target = PointSet(tgt.x[close_mask], tgt.y[close_mask])
            boundary.add_module("Laplace_Close_Quad")
            dip_single = dip[slice(*bnd.get_inds(b))]
            eval_single = Laplace_Layer_Apply(
                boundary, close_target, dipstr=dip_single, gradient=gradient)
            corrected = Compensated_Laplace_Apply(
                boundary, close_target, side_str, dip_single,
                do_DLP=True, do_SLP=False, gradient=gradient)
            if gradient:
                evals[0][close_mask] += corrected[0] - eval_single[0]
                evals[1][close_mask] += corrected[1] - eval_single[1]
                evals[2][close_mask] += corrected[2] - eval_single[2]
            else:
                evals[close_mask] += corrected - eval_single
        return evals

    xi_grid = eval_dipole(boundaryc, grid_b, d_xi)
    et_grid = eval_dipole(boundaryc, grid_b, d_et)

    # Target points in ring: desired rho and theta
    rho_vals = np.linspace(scale, 1.0, n_ext + 2)[1:-1]  # n_ext shells
    theta_vals = np.linspace(0, 2 * np.pi, n_tht, endpoint=False)

    target_xi = rho_vals[:, None] * np.cos(theta_vals)
    target_et = rho_vals[:, None] * np.sin(theta_vals)
    target_flat_xi = target_xi.flatten()
    target_flat_et = target_et.flatten()

    # Initial guesses via griddata
    # grid_b.x/y are already 1D arrays of only the masked (ring) points
    xieta_grid = np.stack([xi_grid, et_grid], axis=1)
    z_grid = grid_b.x + 1j * grid_b.y
    z_guess = griddata(xieta_grid, z_grid,
                       (target_flat_xi, target_flat_et), method="linear")
    # Fall back to nearest for any NaN (outside convex hull)
    bad = np.isnan(z_guess)
    if bad.any():
        z_nearest = griddata(xieta_grid, z_grid,
                             (target_flat_xi[bad], target_flat_et[bad]),
                             method="nearest")
        z_guess[bad] = z_nearest
    xy_guess = np.stack([z_guess.real, z_guess.imag], axis=1)

    # Newton refinement with damping and clamping
    target_arr = np.stack([target_flat_xi, target_flat_et], axis=1
                          ).reshape((-1, 2, 1))
    xy = xy_guess.copy()
    active = np.ones(xy.shape[0], dtype=bool)

    # Compute bounding box for clamping
    R_min = min(R_inner.min(), R_outer.min()) - 0.1
    R_max = max(R_inner.max(), R_outer.max()) + 0.1
    Z_min = min(Z_inner.min(), Z_outer.min()) - 0.1
    Z_max = max(Z_inner.max(), Z_outer.max()) + 0.1

    for iteration in range(NEWTON_MAX_ITER):
        # Clamp active points to bounding box
        xy[active, 0] = np.clip(xy[active, 0], R_min, R_max)
        xy[active, 1] = np.clip(xy[active, 1], Z_min, Z_max)

        pts = PointSet(x=xy[active, 0], y=xy[active, 1])
        xi_v, xi_dx, xi_dy = eval_dipole(boundaryc, pts, d_xi, gradient=True)
        et_v, et_dx, et_dy = eval_dipole(boundaryc, pts, d_et, gradient=True)
        xieta = np.stack([xi_v, et_v], axis=1).reshape((-1, 2, 1))
        residual = xieta - target_arr[active, ...]
        jac = np.stack([np.stack([xi_dx, xi_dy], 1),
                        np.stack([et_dx, et_dy], 1)], 1)

        # Damped Newton step
        try:
            step = np.linalg.solve(jac, residual).squeeze()
        except np.linalg.LinAlgError:
            break
        # Limit step size to 0.1m
        step_norm = np.sqrt(step[:, 0]**2 + step[:, 1]**2) if step.ndim == 2 \
            else np.sqrt(step[0]**2 + step[1]**2)
        if step.ndim == 2:
            too_large = step_norm > 0.1
            if too_large.any():
                step[too_large] *= 0.1 / step_norm[too_large, None]
        xy[active, :] -= step if step.ndim == 2 else step[None, :]

        active[active] = ((np.abs(residual[:, 0, 0]) > NEWTON_TOL) |
                          (np.abs(residual[:, 1, 0]) > NEWTON_TOL))
        if not active.any():
            break

    n_converged = xy.shape[0] - active.sum()
    if active.any():
        print(f"    WARNING: {active.sum()} Newton pts did not converge "
              f"({phi_label}) -- using linear fallback for these")
        # For unconverged points, use linear interpolation
        R_lin, Z_lin = linear_ring_fill(R_inner, Z_inner, R_outer, Z_outer,
                                        n_ext, n_tht)
        # Map flat indices back to (irad, itht)
        active_idx = np.where(active)[0]
        for idx in active_idx:
            irad = idx // n_tht
            itht = idx % n_tht
            xy[idx, 0] = R_lin[irad, itht]
            xy[idx, 1] = Z_lin[irad, itht]

    R_shells = xy[:, 0].reshape(n_ext, n_tht)
    Z_shells = xy[:, 1].reshape(n_ext, n_tht)

    return R_shells, Z_shells


# ============================================================================
# FALLBACK: LINEAR INTERPOLATION (for planes where pybie2d fails)
# ============================================================================

def linear_ring_fill(R_inner, Z_inner, R_outer, Z_outer, n_ext, n_tht):
    """Linear radial interpolation between inner and outer curves."""
    R_shells = np.zeros((n_ext, n_tht))
    Z_shells = np.zeros((n_ext, n_tht))
    for irad in range(n_ext):
        t = (irad + 1) / (n_ext + 1)
        R_shells[irad, :] = R_inner + t * (R_outer - R_inner)
        Z_shells[irad, :] = Z_inner + t * (Z_outer - Z_inner)
    return R_shells, Z_shells


# ============================================================================
# DERIVATIVE COMPUTATION
# ============================================================================

def compute_all_derivatives(data_real, n_total, n_tht, i_plane):
    """Recompute R,Z derivatives for entire grid.
    CubicSpline (C2, periodic) in theta, CubicSpline in radial."""
    tht = np.linspace(0, 2 * np.pi, n_tht, endpoint=False)
    rad = np.linspace(0, 1, n_total, endpoint=True)
    tht_closed = np.append(tht, 2 * np.pi)
    i_lcfs = N_FLUX - 1

    for coord in ['R', 'Z']:
        nodes = data_real[coord][:, :, i_plane]

        # Theta derivatives: CubicSpline (periodic) for all shells
        for irad in range(n_total):
            ring = nodes[:, irad]
            ring_c = np.append(ring, ring[0])
            spline = CubicSpline(tht_closed, ring_c, bc_type='periodic')
            data_real[f'{coord}_t'][:, irad, i_plane] = spline(tht, 1)

        # Radial derivatives: CubicSpline for interior, Pchip for extension
        for itht in range(n_tht):
            col = nodes[itht, :]
            # Interior: CubicSpline (C2)
            spline_in = CubicSpline(rad[:i_lcfs + 1], col[:i_lcfs + 1])
            data_real[f'{coord}_s'][itht, :i_lcfs + 1, i_plane] = \
                spline_in(rad[:i_lcfs + 1], 1)
            # Extension: Pchip (monotone, prevents overshoot)
            spline_ext = PchipInterpolator(rad[i_lcfs:], col[i_lcfs:])
            data_real[f'{coord}_s'][itht, i_lcfs:, i_plane] = \
                spline_ext.derivative()(rad[i_lcfs:])

        # Cross derivatives: d/ds of d/dt
        for itht in range(n_tht):
            col_t = data_real[f'{coord}_t'][itht, :, i_plane]
            spline_in = CubicSpline(rad[:i_lcfs + 1], col_t[:i_lcfs + 1])
            data_real[f'{coord}_st'][itht, :i_lcfs + 1, i_plane] = \
                spline_in(rad[:i_lcfs + 1], 1)
            spline_ext = CubicSpline(rad[i_lcfs:], col_t[i_lcfs:])
            data_real[f'{coord}_st'][itht, i_lcfs:, i_plane] = \
                spline_ext(rad[i_lcfs:], 1)


def compute_field_derivatives(data_real, n_total, n_tht, i_plane):
    """Recompute P,A,B,J derivatives with PchipInterpolator."""
    tht = np.linspace(0, 2 * np.pi, n_tht, endpoint=False)
    rad = np.linspace(0, 1, n_total, endpoint=True)
    tht_closed = np.append(tht, 2 * np.pi)

    for (val_name, s_name, t_name, st_name) in FIELD_SETS:
        nodes = data_real[val_name][:, :, i_plane]
        for irad in range(n_total):
            ring = nodes[:, irad]
            ring_c = np.append(ring, ring[0])
            spline = PchipInterpolator(tht_closed, ring_c)
            data_real[t_name][:, irad, i_plane] = spline.derivative()(tht)
        for itht in range(n_tht):
            col = nodes[itht, :]
            spline = PchipInterpolator(rad, col)
            data_real[s_name][itht, :, i_plane] = spline.derivative()(rad)
        for itht in range(n_tht):
            col_t = data_real[t_name][itht, :, i_plane]
            spline = PchipInterpolator(rad, col_t)
            data_real[st_name][itht, :, i_plane] = spline.derivative()(rad)


# ============================================================================
# COVERAGE CHECK
# ============================================================================

def check_coverage(R_bnd, Z_bnd, segments):
    """Check what fraction of divertor sample points lie inside boundary."""
    from matplotlib.path import Path as MplPath
    if not segments:
        return None, None
    poly = MplPath(np.column_stack([np.append(R_bnd, R_bnd[0]),
                                    np.append(Z_bnd, Z_bnd[0])]))
    n_samp = 20
    n_inside = 0
    n_total = 0
    max_gap = 0.0
    for R1, Z1, R2, Z2 in segments:
        for k in range(n_samp + 1):
            t = k / n_samp
            Rp = R1 + t * (R2 - R1)
            Zp = Z1 + t * (Z2 - Z1)
            n_total += 1
            if poly.contains_point((Rp, Zp)):
                n_inside += 1
            else:
                d = np.min(np.sqrt((Rp - R_bnd)**2 + (Zp - Z_bnd)**2)) * 1000
                max_gap = max(max_gap, d)
    pct = n_inside / n_total * 100 if n_total > 0 else 0
    return pct, max_gap


# ============================================================================
# PER-PHI DIAGNOSTIC PLOT
# ============================================================================

def plot_phi_diagnostic(R_lcfs, Z_lcfs, R_target, Z_target, R_shells, Z_shells,
                        segments, phi_deg, kappa, output_dir, jac_ext=None,
                        prefix='harmonic_'):
    """Generate a single-panel geometry plot for one phi plane."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    sys.path.insert(0, str(Path('/tokp/work/elwa/analysis')))
    import plot_settings as ps

    fig, ax = plt.subplots(1, 1, figsize=(8, 8), constrained_layout=True)
    cr = lambda a: np.append(a, a[0])

    n_ext = R_shells.shape[0] if R_shells is not None else 0
    if R_shells is not None:
        for irad in range(n_ext):
            ax.plot(cr(R_shells[irad, :]), cr(Z_shells[irad, :]),
                    color='firebrick', alpha=0.4, lw=0.6)
    ax.plot(cr(R_lcfs), cr(Z_lcfs), 'steelblue', lw=2.0, label='LCFS')
    ax.plot(cr(R_target), cr(Z_target), 'firebrick', lw=2.0, label='Moulded')
    for R1, Z1, R2, Z2 in segments:
        ax.plot([R1, R2], [Z1, Z2], 'k-', lw=2.5)
    ax.set_xlabel('R [m]')
    ax.set_ylabel('Z [m]')
    ax.set_aspect('equal')
    ax.legend(fontsize=9, loc='lower left')
    ax.set_title(f'$\\phi$ = {phi_deg:.0f}$^\\circ$', fontsize=13)

    outpath = output_dir / f'{prefix}phi{phi_deg:05.1f}.png'
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=120)
    plt.close(fig)
    return outpath


# ============================================================================
# MAIN
# ============================================================================

def main():
    n_total = N_FLUX + N_EXT
    output_file = OUTPUT_DIR / f"gvec2jorek_harmonic_{N_EXT}.dat"
    plots_dir = OUTPUT_DIR / 'plots'
    plots_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("W7-X Two-Step Grid Extension: Harmonic Mapping + Divertor Moulding")
    print("=" * 70)
    print(f"  n_flux={N_FLUX}, n_ext={N_EXT}, n_total={n_total}")
    print(f"  Step 1: Conformal envelope = LCFS + {CONFORMAL_EXT_M*1000:.0f}mm (additive)")
    print(f"  Step 2: Divertor moulding: margin={DIVERTOR_MARGIN_M*1000:.0f}mm, "
          f"taper={DIVERTOR_SMOOTH_DEG:.0f}deg, scale_min={SCALE_MIN}")
    print(f"  pybie2d: N_bnd={N_BND_PTS}, grid={GRID_NXY}x{GRID_NXY}")

    # Read input
    print(f"\nReading: {INPUT_FILE}")
    data, metadata = read_gvec_file(INPUT_FILE, N_THT, N_FLUX)
    nfp = metadata['nfp']
    n_modes = metadata['n_modes']

    # Load divertors
    print("\nLoading divertor targets:")
    divertors = load_all_divertors()

    # Phi planes
    phi_rad = np.linspace(0, 2 * np.pi / nfp, N_PLANES, endpoint=False)
    phi_deg = np.degrees(phi_rad)

    # Evaluate LCFS positions at all phi planes
    print("\nEvaluating LCFS at all phi planes...")
    R_all_orig = h.evaluate_data_full(data['R'], phi_rad, nfp)  # (N_THT, N_FLUX, N_PLANES)
    Z_all_orig = h.evaluate_data_full(data['Z'], phi_rad, nfp)

    # Initialize extended real-space arrays
    data_real = {}
    for name in POSITION_NAMES:
        data_real[name] = np.zeros((N_THT, n_total, N_PLANES))
    data_real['R'][:, :N_FLUX, :] = R_all_orig
    data_real['Z'][:, :N_FLUX, :] = Z_all_orig

    # Process each phi plane (Step 1: harmonic mapping to conformal envelope)
    print(f"\nStep 1: Harmonic mapping ({N_PLANES} phi planes)...")
    t_start = time.time()
    stats = []
    use_harmonic = True

    for iphi in range(N_PLANES):
        R_lcfs = R_all_orig[:, N_FLUX - 1, iphi]
        Z_lcfs = Z_all_orig[:, N_FLUX - 1, iphi]
        R_axis = np.mean(R_all_orig[:, 0, iphi])
        Z_axis = np.mean(Z_all_orig[:, 0, iphi])

        # Elongation
        dR_ext = R_lcfs.max() - R_lcfs.min()
        dZ_ext = Z_lcfs.max() - Z_lcfs.min()
        kappa = max(dZ_ext / dR_ext, 1.0) if dR_ext > 1e-10 else 1.0

        # Step 1: Construct conformal envelope (no divertors)
        R_target, Z_target = construct_target_boundary(
            R_lcfs, Z_lcfs, R_axis, Z_axis,
            phi_deg_label=f"phi={phi_deg[iphi]:.1f}")

        data_real['R'][:, -1, iphi] = R_target
        data_real['Z'][:, -1, iphi] = Z_target

        # Fill ring with harmonic mapping (or linear fallback)
        try:
            if use_harmonic:
                R_shells, Z_shells = harmonic_ring_mapping(
                    R_lcfs, Z_lcfs, R_target, Z_target,
                    N_EXT, N_THT, phi_label=f"phi={phi_deg[iphi]:.1f}")
            else:
                R_shells, Z_shells = linear_ring_fill(
                    R_lcfs, Z_lcfs, R_target, Z_target, N_EXT, N_THT)
        except Exception as e:
            print(f"    WARNING: harmonic mapping failed at phi={phi_deg[iphi]:.1f}: "
                  f"{e} -- using linear fallback")
            R_shells, Z_shells = linear_ring_fill(
                R_lcfs, Z_lcfs, R_target, Z_target, N_EXT, N_THT)

        # Store shells (R_shells is [n_ext, n_tht])
        for irad in range(N_EXT):
            data_real['R'][:, N_FLUX + irad, iphi] = R_shells[irad, :]
            data_real['Z'][:, N_FLUX + irad, iphi] = Z_shells[irad, :]

        ext_w = np.sqrt((R_target - R_lcfs)**2 + (Z_target - Z_lcfs)**2)
        stat = {
            'phi': phi_deg[iphi], 'kappa': kappa,
            'ext_min': ext_w.min() * 1000, 'ext_max': ext_w.max() * 1000,
        }
        stats.append(stat)

        if iphi % 8 == 0:
            print(f"  phi={phi_deg[iphi]:5.1f}: kappa={kappa:.2f}, "
                  f"ext={ext_w.min()*1000:.0f}-{ext_w.max()*1000:.0f}mm")

    t_total = time.time() - t_start
    print(f"  Step 1 complete: {t_total:.1f}s")

    # ---- Step 2: Divertor moulding ----
    print(f"\nStep 2: Divertor moulding (mould_frac={MOULD_FRAC:.2f})...")
    t0 = time.time()
    scale_field = compute_scale_field(
        data_real, n_total, N_FLUX, divertors, phi_deg)
    print(f"  Scale field: {time.time() - t0:.1f}s")

    t0 = time.time()
    apply_scale_field(data_real, scale_field, n_total, N_FLUX, MOULD_FRAC)
    print(f"  Moulding applied: {time.time() - t0:.1f}s")

    # ---- Recompute derivatives after moulding ----
    print("\n  Recomputing position derivatives (hybrid CubicSpline/Pchip)...")
    t0 = time.time()
    n_neg_total_real = 0
    for iphi in range(N_PLANES):
        compute_all_derivatives(data_real, n_total, N_THT, iphi)
        xjac = (data_real['R_s'][:, :, iphi] *
                data_real['Z_t'][:, :, iphi] -
                data_real['R_t'][:, :, iphi] *
                data_real['Z_s'][:, :, iphi])
        n_neg = np.sum(xjac[:, N_FLUX - 1:] <= 0)
        n_neg_total_real += n_neg
        if iphi % 16 == 0:
            print(f"    phi={phi_deg[iphi]:5.1f}: Jac_min={np.min(xjac):.3e}, "
                  f"n_neg={n_neg}")
    print(f"  Derivatives: {time.time() - t0:.1f}s, "
          f"total n_neg (real space)={n_neg_total_real}")

    # Generate per-phi diagnostic plots (after moulding)
    # Summary plots go to plots/, all-phi plots go to plots/all_phi/
    all_phi_dir = OUTPUT_DIR / 'plots' / 'all_phi'
    all_phi_dir.mkdir(parents=True, exist_ok=True)
    diag_phi_targets = [0, 9, 18, 27, 36, 45, 54, 63]
    diag_phi_idx = [int(np.round(p / (PERIOD_DEG / N_PLANES)))
                    for p in diag_phi_targets]
    diag_phi_idx = [i for i in diag_phi_idx if i < N_PLANES]  # safety
    for iphi in range(N_PLANES):
        R_lcfs = data_real['R'][:, N_FLUX - 1, iphi]
        Z_lcfs = data_real['Z'][:, N_FLUX - 1, iphi]
        R_target = data_real['R'][:, -1, iphi]
        Z_target = data_real['Z'][:, -1, iphi]
        R_shells = data_real['R'][:, N_FLUX:-1, iphi].T  # (n_ext-1, n_tht)
        Z_shells = data_real['Z'][:, N_FLUX:-1, iphi].T
        segments = get_divertor_segments_at_phi(divertors, phi_deg[iphi])
        dR_ext = R_lcfs.max() - R_lcfs.min()
        dZ_ext = Z_lcfs.max() - Z_lcfs.min()
        kappa = max(dZ_ext / dR_ext, 1.0) if dR_ext > 0 else 1.0
        xjac = (data_real['R_s'][:, :, iphi] *
                data_real['Z_t'][:, :, iphi] -
                data_real['R_t'][:, :, iphi] *
                data_real['Z_s'][:, :, iphi])
        # All-phi plots go to all_phi/ subfolder
        plot_phi_diagnostic(R_lcfs, Z_lcfs, R_target, Z_target,
                            R_shells, Z_shells, segments, phi_deg[iphi],
                            kappa, all_phi_dir, jac_ext=xjac[:, N_FLUX - 1:],
                            prefix='')
        # Summary plots (selected phi) go to plots/ (top level)
        if iphi in diag_phi_idx:
            plot_phi_diagnostic(R_lcfs, Z_lcfs, R_target, Z_target,
                                R_shells, Z_shells, segments, phi_deg[iphi],
                                kappa, OUTPUT_DIR / 'plots',
                                jac_ext=xjac[:, N_FLUX - 1:])

    # s_factor rescaling for interior derivatives
    s_old = 1.0 / (N_FLUX - 1)
    s_new = 1.0 / (n_total - 1)
    ratio = s_old / s_new
    print(f"  s_factor rescaling: {s_old:.6f} -> {s_new:.6f}, ratio={ratio:.4f}")
    for name in ['R_s', 'R_st', 'Z_s', 'Z_st']:
        data_real[name][:, :N_FLUX - 1, :] *= ratio

    # Physical fields: copy LCFS value, zero s-derivatives
    print("\n  Extending physical fields...")
    data_ext = {}
    for name in ALL_NAMES:
        data_ext[name] = np.zeros((N_THT, n_total, n_modes))
        data_ext[name][:, :N_FLUX, :] = data[name]

    phys_value = ['P', 'P_t', 'J_R', 'J_R_t', 'J_Z', 'J_Z_t',
                  'J_phi', 'J_phi_t']
    phys_zero = ['P_s', 'P_st', 'J_R_s', 'J_R_st', 'J_Z_s', 'J_Z_st',
                 'J_phi_s', 'J_phi_st']
    for name in phys_value:
        for irad in range(N_EXT):
            data_ext[name][:, N_FLUX + irad, :] = data[name][:, N_FLUX - 1, :]
    for name in phys_zero:
        data_ext[name][:, N_FLUX:, :] = 0.0

    # Evaluate field quantities in real space for derivative computation
    print("  Evaluating fields in real space for derivative computation...")
    field_names = [n for n in ALL_NAMES if n not in POSITION_NAMES]
    for name in field_names:
        arr = h.evaluate_data_full(data_ext[name], phi_rad, nfp)
        data_real[name] = arr

    print("  Recomputing field derivatives...")
    t0 = time.time()
    for iphi in range(N_PLANES):
        compute_field_derivatives(data_real, n_total, N_THT, iphi)
    print(f"  Field derivatives: {time.time() - t0:.1f}s")

    # Convert all to Fourier modes
    print("\n  Converting to Fourier modes...")
    t0 = time.time()
    data_out = {}
    i_lcfs = N_FLUX - 1
    for name in ALL_NAMES:
        data_out[name] = np.zeros((N_THT, n_total, n_modes))
        # Interior: preserve original GVEC modes
        data_out[name][:, :i_lcfs, :] = data[name][:, :i_lcfs, :]
        # LCFS + extension: from real space
        data_out[name][:, i_lcfs:, :] = h.calculate_modes_full(
            data_real[name][:, i_lcfs:, :], phi_rad, n_modes, nfp)

    # Interior s-derivatives: preserve rescaled original modes
    for name in ['R_s', 'R_st', 'Z_s', 'Z_st']:
        data_out[name][:, :i_lcfs, :] = data[name][:, :i_lcfs, :] * ratio

    print(f"  Fourier conversion: {time.time() - t0:.1f}s")

    # Final Jacobian check from modes
    print("\n  Final Jacobian check (from Fourier modes, all phi):")
    R_s_all = h.evaluate_data_full(data_out['R_s'], phi_rad, nfp)
    Z_s_all = h.evaluate_data_full(data_out['Z_s'], phi_rad, nfp)
    R_t_all = h.evaluate_data_full(data_out['R_t'], phi_rad, nfp)
    Z_t_all = h.evaluate_data_full(data_out['Z_t'], phi_rad, nfp)
    jac_all = R_s_all * Z_t_all - R_t_all * Z_s_all
    n_neg_total = np.sum(jac_all <= 0)
    n_neg_ext = np.sum(jac_all[:, N_FLUX:, :] <= 0)
    print(f"    Total: min={np.min(jac_all):.3e}, n_neg={n_neg_total}")
    print(f"    Extension: min={np.min(jac_all[:, N_FLUX:, :]):.3e}, "
          f"n_neg={n_neg_ext}")

    # Write output
    print(f"\n  Writing: {output_file}")
    write_gvec_file(output_file, INPUT_FILE, data_out, n_total, N_THT, metadata)

    # Coverage check
    print("\n  Divertor coverage:")
    print(f"  {'phi_J':>6} {'coverage':>9} {'max_gap':>9}")
    for phi_check in [0, 4.5, 9, 13.5, 18, 27, 36, 54, 58.5, 63, 67.5]:
        phi_chk_rad = np.array([np.radians(phi_check)])
        R_chk = h.evaluate_data_full(data_out['R'], phi_chk_rad, nfp)[:, :, 0]
        Z_chk = h.evaluate_data_full(data_out['Z'], phi_chk_rad, nfp)[:, :, 0]
        segs = get_divertor_segments_at_phi(divertors, phi_check)
        pct, gap = check_coverage(R_chk[:, -1], Z_chk[:, -1], segs)
        if pct is not None:
            print(f"  {phi_check:6.1f} {pct:8.1f}% {gap:8.1f}mm")
        else:
            print(f"  {phi_check:6.1f}  no div data")

    # Summary
    print(f"\n  Summary:")
    print(f"    Total negative Jacobians (real space): {n_neg_total_real}")
    print(f"    Total negative Jacobians (Fourier modes): {n_neg_total}")
    print(f"    Extension Jac min (modes): {np.min(jac_all[:, N_FLUX:, :]):.3e}")

    # 5-panel summary plot
    print("\n  Generating summary plots...")
    plot_5panel_summary(data_out, metadata, divertors, phi_deg, OUTPUT_DIR)

    print("\nDone.")


# ============================================================================
# SUMMARY PLOTS
# ============================================================================

def plot_5panel_summary(data_out, metadata, divertors, phi_deg, output_dir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    sys.path.insert(0, str(Path('/tokp/work/elwa/analysis')))
    import plot_settings as ps

    phi_show = [0, 18, 36, 54, 66]
    nfp = metadata['nfp']
    cr = lambda a: np.append(a, a[0])

    fig, axes = plt.subplots(1, len(phi_show), figsize=(4 * len(phi_show), 5),
                             sharey=True, constrained_layout=True)

    for ax_idx, phi_target in enumerate(phi_show):
        ax = axes[ax_idx]
        phi_rad = np.array([np.radians(phi_target)])
        R_all = h.evaluate_data_full(data_out['R'], phi_rad, nfp)[:, :, 0]
        Z_all = h.evaluate_data_full(data_out['Z'], phi_rad, nfp)[:, :, 0]

        # Extension shells (moulded)
        for irad in range(N_FLUX, N_FLUX + N_EXT):
            R_ring = cr(R_all[:, irad])
            Z_ring = cr(Z_all[:, irad])
            ax.plot(R_ring, Z_ring, color='firebrick', alpha=0.4, lw=0.6)

        # LCFS
        R_lcfs = R_all[:, N_FLUX - 1]
        Z_lcfs = Z_all[:, N_FLUX - 1]
        ax.plot(cr(R_lcfs), cr(Z_lcfs), color='steelblue', lw=2.0,
                label='LCFS')

        # Conformal envelope (dashed reference)
        R_axis = np.mean(R_all[:, 0])
        Z_axis = np.mean(Z_all[:, 0])
        dR_cf = R_lcfs - R_axis
        dZ_cf = Z_lcfs - Z_axis
        r_cf = np.sqrt(dR_cf**2 + dZ_cf**2) + CONFORMAL_EXT_M
        angle_cf = np.arctan2(dZ_cf, dR_cf)
        R_conf = R_axis + r_cf * np.cos(angle_cf)
        Z_conf = Z_axis + r_cf * np.sin(angle_cf)
        ax.plot(cr(R_conf), cr(Z_conf), color='silver', lw=1.5, ls='--',
                label='Conformal' if ax_idx == 0 else None)

        # Moulded boundary
        ax.plot(cr(R_all[:, -1]), cr(Z_all[:, -1]),
                color='firebrick', lw=2.0, label='Moulded')

        # Divertor targets
        segments = get_divertor_segments_at_phi(divertors, phi_target)
        for i_seg, (R1, Z1, R2, Z2) in enumerate(segments):
            ax.plot([R1, R2], [Z1, Z2], color='forestgreen', lw=2.5,
                    label='Divertor' if (ax_idx == 0 and i_seg == 0) else None)

        ax.set_title(f'$\\phi$ = {phi_target}$^\\circ$', fontsize=11)
        ax.set_xlabel('R [m]')
        if ax_idx == 0:
            ax.set_ylabel('Z [m]')
        if ax_idx == 1:
            ax.legend(fontsize=7, loc='upper left')
        ax.set_aspect('equal')

    fig.suptitle('W7-X Harmonic + Moulding: Conformal envelope (dashed grey) '
                 'vs Moulded boundary (red) vs Divertor targets (green)',
                 fontsize=11)
    outpath = output_dir / 'plots' / 'harmonic_5panel.png'
    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"  Plot: {outpath}")



if __name__ == '__main__':
    main()
