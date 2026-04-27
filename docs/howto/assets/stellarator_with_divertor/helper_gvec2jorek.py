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
