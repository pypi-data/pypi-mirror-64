# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:07:03 2020

@author: Administrator
"""

from mayavi import mlab
from tvtk.api import tvtk
import numpy as np

import matplotlib
matplotlib.use('Agg')
from pythtb import * # import TB model class
import pymatgen as mg
import pymatgen.symmetry.analyzer
from pymatgen import Structure
import numpy as np
import pylab as pl

import sys

def plot_cell(cell):
    p = tvtk.PolyData()
    p.points = [[0.0,0.0,0.0],[1.0,0.0,0,0]]
    poly = []
    ids = list(cell.point_ids)
    for i in range(cell.number_of_faces):
        poly.append([ids.index(x) for x in cell.get_face(i).point_ids])
    p.polys = poly
    mlab.pipeline.surface(p, opacity = 0.3)





def make_points_array(x, y, z):
    return np.c_[x.ravel(), y.ravel(), z.ravel()]
    
if __name__ == "__main__": 
    strfile = 'graphene.cif'
    structure = Structure.from_file(strfile)    
    analyzer1 = mg.symmetry.analyzer.SpacegroupAnalyzer(structure,symprec=0.0001,angle_tolerance=2)
    str_data = analyzer1.get_symmetry_dataset()
    
    # make two dimensional tight-binding graphene model
    pos  = str_data['std_positions']
    print(pos)
    x = []; y = []; z = [];
    for p in pos:
        x.append(p[0])
        y.append(p[1])
        z.append(p[2])
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    print(x,y,z)
    scalars = np.array([1,1])
    
    mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))
    mlab.clf()
    
    latt = np.array([[0,0,0],[1,1,1],[0,0,0]])
    l = mlab.plot3d(lattx, latty, lattz,  tube_radius=0.025, colormap='Spectral')
    
    pts = mlab.points3d(x, y, z, scalars, scale_factor=0.15, resolution=10)
    connections = [[0,1]]
    pts.mlab_source.dataset.lines = np.array(connections)
    
    # Use a tube fiter to plot tubes on the link, varying the radius with the
    # scalar value
    tube = mlab.pipeline.tube(pts, tube_radius=0.0015)
    tube.filter.radius_factor = 0.01
    tube.filter.vary_radius = 'vary_radius_by_scalar'
    mlab.pipeline.surface(tube, color=(0.8, 0.8, 0))
   # mlab.view(49, 31.5, 52.8, (4.2, 37.3, 20.6))

    mlab.show()