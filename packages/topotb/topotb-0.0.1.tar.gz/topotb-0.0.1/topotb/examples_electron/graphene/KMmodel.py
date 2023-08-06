# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 23:53:43 2020

@author: zhoup
"""

import sys
sys.path.append(r'C:\Users\zhoup\Desktop\project\topotb')

import numpy as np
from sitesym1 import SiteSymmetry
import symmetry_representation as sr
from pythtb import *
from plot_band_tb import *
from plot_structure import plot_str_cif
from model_examples import km_model

if __name__ == '__main__':
    filename = 'graphenekm.cif'
    #plot_str_cif(filename)
    orbs=sr.WANNIER_ORBITALS['p']
    orbs_fin = [orbs[0]]
    print(orbs_fin)
    spinor = True
    #list the degeneracy of bands
    # Here we use the dict to represent the calculated k-points
    kpoints = {'GM':[0.0,0,0]}
    #print(list(kpoints.keys()))
    my_model = km_model(False,filename)
    my_model.display()
    #sys.exit()
    sitesym = SiteSymmetry(filename, orbs_fin, spinor, kpoints)
    #plot_band_tb_hexagonal(my_model, 'graphenen_band.pdf')
    #print(sitesym.monolayer)
    #sys.exit()
    
    #irreps = sitesym.get_irreps(kpoints)
    

   # plot_band_tb_hexagonal(my_model, 'graphenen_band.pdf')
    sitesym.get_irreps_tb(kpoints, my_model)
    sitesym.display_symmetry_info()