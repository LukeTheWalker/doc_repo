"""
Minimal helper functions for reading and writing gvec files for the divertor example, 
and evaluating the Fourier modes in real space.
"""

import numpy as np
import decimal

def read_gvec_data(in_gvec, n_theta, n_rad, n_modes):
    data=[]
    # Read gvec data up to the next variable.
    for line in in_gvec:
        if line.strip().startswith('##'):
            break
        data.extend(float(x) for x in line.strip().split())
    return np.array(data, dtype=float).reshape((n_theta, n_rad, n_modes), order='F')

def evaluate_data(mode_data, phi, nfp):
    """Given the fourier modes (mode_data), evaluate the value of the data in real space at a toroidal angle, phi.
    mode_data should be of shape (n_modes)."""
    n_modes = len(mode_data)
    n_max = int((n_modes-1)/2)
    sin_modes = np.arange(0, n_max)
    cos_modes = np.arange(n_max, n_modes)
    data_real = -np.sum(mode_data[sin_modes] * np.sin(nfp * (sin_modes+1) * phi)) + \
                np.sum(mode_data[cos_modes] * np.cos(nfp * (cos_modes - n_max) * phi))
    return data_real

def evaluate_data_full(mode_data, phi, nfp):
    """Given the fourier modes (mode_data), evaluate the value of the data in real space at a list of toroidal angles, phi.
    mode_data should be of shape (n_tht, n_flux, n_modes)."""
    _, _, n_modes = mode_data.shape; n_planes = len(phi)
    n_max = int((n_modes-1)/2)
    sin_mode_numbers = np.arange(1, n_max+1)
    cos_mode_numbers = np.arange(0, n_max+1)
    phi_reshaped = phi.reshape(n_planes,1)
    sin_values = np.sin(nfp*sin_mode_numbers*phi_reshaped)
    cos_values = np.cos(nfp*cos_mode_numbers*phi_reshaped)
    sin_mode_coefficients = mode_data[:,:,:n_max]
    cos_mode_coefficients = mode_data[:,:,n_max:n_modes]
    sin_sum = -np.einsum('ijk,lk->ijl', sin_mode_coefficients, sin_values)  # Negative as we use a RH coordinate system
    cos_sum = np.einsum('ijk,lk->ijl', cos_mode_coefficients, cos_values)
    return sin_sum + cos_sum

def write_gvec_data(out_gvec, data, name):
    out_gvec.write(f'##<< 2D scalar variable fourier modes (1:Ntheta,1:Ns), Variable name:  "{name}"\n')
    # Reorder the data for Fortran ordering
    # fortran_data = data[name].ravel(order='F')
    fortran_data = data.ravel(order='F')
    # Write it to the file, 6 numbers at a time
    for i in range(0, len(fortran_data), 6):
        line_data = fortran_data[i:i+6]
        strings = []
        for val in line_data:
            s = f"{val:23.15E}"
            if 'E' in s:
                # Split string into decimal and exponent parts
                parts = s.split('E')
                dec = decimal.Decimal(parts[0].strip())
                exp = int(parts[1])

                # Divide decimal part by 10 and add one to exponenet
                if dec != 0:
                    dec /= 10
                    exp += 1
                # Reformat for correct lengths:
                dec_formatted = f"{dec: .15f}"      # Strip to 
                exp_formatted = f"{exp:+03d}"
                str = f"{dec_formatted}E{exp_formatted}"
            strings.append(f"{str: >23}")
        line = " ".join(strings)
        out_gvec.write(line + "\n")


def calculate_modes(f, phi, n_modes, nfp):
    """Given the values of a function f at angles phi, calculate the sine and cosine modes up to n_modes."""
    n_planes = len(phi)
    n_max = int((n_modes - 1)/2)
    sin_modes = np.arange(0, n_max)
    cos_modes = np.arange(n_max, n_modes)
    modes = np.zeros(n_modes, dtype=float)
    for m in sin_modes:
        modes[m] = -(2/n_planes) * np.sum(f * np.sin(nfp * (m+1) * phi))
    for m in cos_modes:
        modes[m] = (2/n_planes) * np.sum(f * np.cos(nfp * (m - n_max) * phi))

    modes[int((n_modes-1)/2)] /= 2  # The m=0 cosine mode should be halved.
    return modes

def calculate_modes_full(data, phi, n_modes, nfp):
    """Given the values of some data with shape (n_tht, n_flux, n_planes),
        calculate the sine and cosine modes up to n_modes."""
    n_tht, n_flux, n_planes = data.shape
    n_max = int((n_modes - 1)/2)
    sin_mode_numbers = np.arange(1, n_max+1)
    cos_mode_numbers = np.arange(0, n_max+1)
    phi_reshaped = phi.reshape(n_planes,1)
    sin_values = np.sin(nfp*sin_mode_numbers*phi_reshaped)  # This is of shape (n_planes, n_max)
    cos_values = np.cos(nfp*cos_mode_numbers*phi_reshaped)  # These are of shape (n_planes, n_max+1)

    mode_data = np.zeros((n_tht, n_flux, n_modes), dtype=float)
    # x = np.einsum('ijk,kl->ijl', data, sin_values)
    mode_data[:,:,:n_max] = -(2/n_planes) * np.einsum('ijk,kl->ijl', data, sin_values)  # Negative as we use a RH coordinate system
    mode_data[:,:,n_max:] =  (2/n_planes) * np.einsum('ijk,kl->ijl', data, cos_values)
    mode_data[:,:,n_max] /= 2   # The m=0 mode should be halved (as you don't get the 2 at the front)
    return mode_data

def read_gvec_header(filepath):
    """Read gvec2jorek.dat header and return grid parameters."""
    with open(filepath) as f:
        # Skip comment lines to find grid params
        for line in f:
            line = line.strip()
            if line.startswith('##'):
                continue
            parts = line.split()
            n_rad, n_theta, n_phi = int(parts[0]), int(parts[1]), int(parts[2])
            break
        # Next non-comment line: global params
        for line in f:
            line = line.strip()
            if line.startswith('##'):
                continue
            parts = line.split()
            coord_type = int(parts[0])
            nfp = int(parts[1])
            asym = int(parts[2])
            m_max = int(parts[3])
            n_max = int(parts[4])
            n_modes = int(parts[5])
            sin_range = (int(parts[6]), int(parts[7]))
            cos_range = (int(parts[8]), int(parts[9]))
            break

    return {
        'n_rad': n_rad, 'n_theta': n_theta, 'n_phi': n_phi,
        'coord_type': coord_type, 'nfp': nfp, 'asym': asym,
        'm_max': m_max, 'n_max': n_max, 'n_modes': n_modes,
        'sin_range': sin_range, 'cos_range': cos_range,
    }

def read_gvec_blocks(filepath, n_theta, n_rad, n_modes):
    """Read all data blocks from gvec2jorek.dat.
    Returns dict of {name: array(n_theta, n_rad, n_modes)}."""
    blocks = {}
    block_names = []
    current_name = None
    data_lines = []

    with open(filepath) as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith('##<<'):
                # Save previous block if any
                if current_name is not None and data_lines:
                    values = []
                    for dl in data_lines:
                        values.extend(float(x) for x in dl.split())
                    arr = np.array(values, dtype=np.float64)
                    expected = n_theta * n_rad * n_modes
                    if len(arr) == expected:
                        blocks[current_name] = arr.reshape(
                            (n_theta, n_rad, n_modes), order='F')
                    block_names.append(current_name)
                    data_lines = []

                # Parse block name
                if 'Variable name:' in stripped:
                    name = stripped.split('"')[1]
                    current_name = name
                elif 'number of grid points' in stripped:
                    current_name = '_grid_params'
                elif 'global:' in stripped:
                    current_name = '_global_params'
                else:
                    current_name = stripped
                data_lines = []
            elif stripped.startswith('##'):
                continue  # Header comment
            else:
                if current_name is not None:
                    data_lines.append(stripped)

        # Save last block
        if current_name is not None and data_lines:
            values = []
            for dl in data_lines:
                values.extend(float(x) for x in dl.split())
            arr = np.array(values, dtype=np.float64)
            expected = n_theta * n_rad * n_modes
            if len(arr) == expected:
                blocks[current_name] = arr.reshape(
                    (n_theta, n_rad, n_modes), order='F')
            block_names.append(current_name)

    return blocks, block_names

def write_gvec_block(f, data, name):
    """Write one data block in gvec2jorek.dat format."""
    f.write(f'##<< 2D scalar variable fourier modes (1:Ntheta,1:Ns), Variable name:  "{name}"\n')
    flat = data.ravel(order='F')
    for i in range(0, len(flat), 6):
        chunk = flat[i:i+6]
        strings = []
        for val in chunk:
            s = f"{val:23.15E}"
            if 'E' in s:
                parts = s.split('E')
                dec = decimal.Decimal(parts[0].strip())
                exp = int(parts[1])
                if dec != 0:
                    dec /= 10
                    exp += 1
                dec_fmt = f"{dec: .15f}"
                exp_fmt = f"{exp:+03d}"
                s = f"{dec_fmt}E{exp_fmt}"
            strings.append(f"{s: >23}")
        f.write(" ".join(strings) + "\n")