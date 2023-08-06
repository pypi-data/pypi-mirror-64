# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 10:29:07 2020

@author: zhoup
"""
import sys
import numpy as np

sys.path.append(r'E:\BaiduNetdiskDownload\pytopo_tb\project\project\topotb')

from phon_wav import phonopy_TB
from sitesym1 import SiteSymmetry
import symmetry_representation as sr

from pprint import pprint

if __name__ == "__main__":
    multiple =[2,2,1]
    q_path2 = [[0, 0, 0], [0.5,0.0,0.0], [-0.3333, 0.6667, 0.0], [0, 0, 0]]
    q_spacing = 20
    name = 'CrI3'
    
    orbs = sr.WANNIER_ORBITALS['p']
    orbs_fin = [orbs[1],orbs[2],orbs[0]]
    print(orbs_fin)
    
    spinor = False
#    if not ('x' in orbs_fin and 'y' in orbs_fin and 'z' in orbs_fin):
#           raise RuntimeError ("The orbitals of phonon must be ['x', 'y', 'z'] and your orbitals are {0}".format(orbs_fin)) 


    filename = 'POSCAR'
    # Here we use the dict to represent the calculated k-points
    kpoints = {'GM':[0,0,0],'K':[1.0/3.0,1.0/3.0,0],'M':[0.5,0,0]}
    sitesym = SiteSymmetry(filename, orbs_fin, spinor, kpoints) 
    print(sitesym.monolayer)

#    print(np.shape(sitesym.sitesym))
#    print(sitesym.sitesym[1])
#    print(np.array(sitesym.rep_site[1]))
#    sys.exit()
#    sitesym.get_irreps(kpoints)
    phonon_model = phonopy_TB(multiple)
    sitesym.get_irreps_phonon(kpoints, phonon_model)