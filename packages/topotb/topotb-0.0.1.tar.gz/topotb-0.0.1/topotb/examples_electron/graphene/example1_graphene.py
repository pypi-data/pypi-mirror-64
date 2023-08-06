# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 09:13:26 2020

@author: Administrator
"""
import sys
sys.path.append(r'C:\Users\zhoup\Desktop\project\topotb')

import numpy as np
from topotb.site_symmetry import SiteSymmetry
import symmetry_representation as sr
from pythtb import *
from topotb.plot_band_tb import *
from topotb.plot_structure import plot_str_cif
from topotb.topotb_help import topotb_help


if __name__ == '__main__':
    filename = 'graphene.cif'
    #topotb_help()
    #plot_str_cif(filename)
    orbs=sr.WANNIER_ORBITALS['p']
    orbs_fin = [orbs[0]]
    print(orbs_fin)
    spinor = False
    #list the degeneracy of bands
    # Here we use the dict to represent the calculated k-points
    kpoints = {'GM':[0.00000,0,0]}
    #print(list(kpoints.keys()))
    sitesym = SiteSymmetry(filename, orbs_fin, spinor, kpoints)
    #print(sitesym.monolayer)
    #sys.exit()
    
    #irreps = sitesym.get_irreps(kpoints)
    
    latt  = sitesym.structure.lattice.matrix
    pos = []
    for isite in sitesym.structure:
        pos.append(isite.frac_coords)
    #print(sitesym.structure.as_dict())
    if spinor:
        my_model=tb_model(3,3,latt,pos, nspin = 2)
    else:
        my_model=tb_model(3,3,latt,pos)

    # set model parameters
    delta=0.0
    t=-1.0
    
    # set on-site energies
    my_model.set_onsite([-delta,delta])
    # set hoppings (one for each connected pair of orbitals)
    # (amplitude, i, j, [lattice vector to cell containing j])
    my_model.set_hop(t, 0, 1, [ 0, 0, 0])
    my_model.set_hop(t, 0, 1, [ -1, 0, 0])
    my_model.set_hop(t, 0, 1, [ 0, 1, 0])
   # plot_band_tb_hexagonal(my_model, 'graphenen_band.pdf')
    sitesym.get_irreps_tb(kpoints, my_model)
    sitesym.display_symmetry_info()
