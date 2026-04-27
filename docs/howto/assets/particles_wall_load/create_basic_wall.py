"""
Generate basic wall model for jorek namelist
========================================================
Creates 3D CAD wall model from the edges of the jorek computational grid.
"""

import numpy as np
import h5py
 
wall2d = np.genfromtxt("jorek_namelist",
                       dtype       = 'U',
                       delimiter   = ',',
                       skip_header = 113,
                       max_rows    = 371-114)
 
r = np.array([float(x.split("=")[-1]) for x in wall2d[:,0]])
z = np.array([float(x.split("=")[-1]) for x in wall2d[:,1]])
 
nr = r.size
nphi = 360
 
nodes = np.zeros(( nphi*(nr-1)*2*9, ))
for p in range(nphi):
    for i in range(r.size-1):
        idx  = p * (nr-1) * 2 * 9 + i * 2 * 9
        phi1 = p     * 2*np.pi / nphi
        phi2 = (p+1) * 2*np.pi / nphi
 
        x1 = r[i]   * np.cos(phi1)
        x2 = r[i]   * np.cos(phi2)
        x3 = r[i+1] * np.cos(phi1)
        y1 = r[i]   * np.sin(phi1)
        y2 = r[i]   * np.sin(phi2)
        y3 = r[i+1] * np.sin(phi1)
        z1 = z[i]
        z2 = z[i]
        z3 = z[i+1]
        nodes[idx:idx+9] = [x1, y1, z1, x2, y2, z2, x3, y3, z3]
 
        x1 = r[i+1] * np.cos(phi2)
        x2 = r[i+1] * np.cos(phi1)
        x3 = r[i]   * np.cos(phi2)
        y1 = r[i+1] * np.sin(phi2)
        y2 = r[i+1] * np.sin(phi1)
        y3 = r[i]   * np.sin(phi2)
        z1 = z[i+1]
        z2 = z[i+1]
        z3 = z[i]
        nodes[idx+9:idx+18] = [x1, y1, z1, x2, y2, z2, x3, y3, z3]
 
ntriangle = nphi*(nr-1)*2
with h5py.File('wall2d.h5','w') as h5:
    h5.create_dataset("ntriangle",  (1,),              data=ntriangle, dtype='i4')
    h5.create_dataset("nodes",      (ntriangle*3*3,),  data=nodes,     dtype='f8')
 
import matplotlib.pyplot as plt
plt.plot(r,z,color='red')
plt.scatter(np.sqrt(nodes[0::3]**2 + nodes[1::3]**2 ), nodes[2::3], 1)
plt.gca().set_aspect('equal', 'box')
 
plt.show()
