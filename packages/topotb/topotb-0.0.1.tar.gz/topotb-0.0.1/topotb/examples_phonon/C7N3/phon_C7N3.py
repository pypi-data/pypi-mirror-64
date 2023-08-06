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
from irreps_phonopy import *

from plot_structure import *


from pprint import pprint

class primitive():
    def __init__(self, model_sym, model_phon):
        self.model_sym = model_sym
        self.model_phon = model_phon
        self.dataset = model_sym.analyzer.get_symmetry_dataset()
    
    def get_cell(self):
        return self.model_sym.structure.lattice.matrix
    
    def get_number_of_atoms(self):
        return self.model_phon.total_num_atom_prim
    
    def get_scaled_positions(self):
        return self.model_phon.direct_coord_prim
        

if __name__ == "__main__":
    multiple =[2,2,1]
    q_path2 = [[0, 0, 0], [0.5,0.0,0.0], [-0.3333, 0.6667, 0.0], [0, 0, 0]]
    q_spacing = 20
    name = 'C7N3'
    
    orbs = sr.WANNIER_ORBITALS['p']
    orbs_fin = [orbs[1],orbs[2],orbs[0]]
    print(orbs_fin)
    
    spinor = False
#    if not ('x' in orbs_fin and 'y' in orbs_fin and 'z' in orbs_fin):
#           raise RuntimeError ("The orbitals of phonon must be ['x', 'y', 'z'] and your orbitals are {0}".format(orbs_fin)) 

    filename = 'POSCAR'
    flags = ['-i','POSCAR']
    #plot_str_poscar(filename)
    # Here we use the dict to represent the calculated k-points
    #kpoints = {'GM':[0,0,0],'K':[1.0/3.0,1.0/3.0,0],'M':[0.5,0,0]}
    kpoints = {'GM':[0,0,0],'K':[1.0/3.0,1.0/3.0,0],'M':[0.5,0,0]}
    kpt_label = list(kpoints.keys())
    #print(list(kpoints.keys()))
    sitesym = SiteSymmetry(filename, orbs_fin, spinor, kpoints) 

#    print(np.shape(sitesym.sitesym))
#    print(sitesym.sitesym[1])
#    print(np.array(sitesym.rep_site[1]))
#    sys.exit()
#    sitesym.get_irreps(kpoints)
    phonon_model = phonopy_TB(multiple)
    sitesym.get_irreps_phonon(kpoints, phonon_model)
    #pprint(sitesym.rep_spg[1][0])
    #print(sitesym.dataset['std_lattice'])
#    prim = primitive(sitesym, phonon_model)
#    for iq in range(len(kpoints)):
#        (eig_val,eig_vec)=phonon_model.solve_one_phonon(kpoints[kpt_label[iq]],eig_vectors=True)
#        #pprint(eig_vec.T[0])
#    
#        dynamical_matrix = phonon_model.construct_dynamical_matrix_q(kpoints[kpt_label[iq]])
#    
#        irreps = IrReps(dynamical_matrix,prim,kpoints[kpt_label[iq]])
#
#        irreps.run()
#        grmat = irreps.get_ground_matrices()
#
#        #pprint(grmat)
#        vec = irreps.get_eigenvectors()
#        #gr_mat = irreps.get_ground_matrices()
#        
#       # pprint(vec[0])
#        irreps.show(show_irreps=False)
#        #irreps._write_yaml(False)
#        sys.exit()
        
#    pprint(phonon_model.direct_coord_prim)
#    pprint(sitesym.structure)
#    
#    
#    sitesym.get_irreps_phonon(kpoints, phonon_model)
#    phonon_model.get_phonon_band(name, q_path2, q_spacing)