import numpy as np
import pandas as pd


class HTM_CELL():
    
    """
    
    """
    
    def __init__(self, M=None, N=None, n_dendrites=None, n_synapses=None, 
                 nmda_th=None, perm_th=None, perm_init=None):
        
        """
        
        """
        
        self.M = M # number of cells per minicolumn
        self.N = N # number of minicolumns
        
        self.n_dendrites = n_dendrites # number of dendritic segments on a single cell
        self.n_synapses = n_synapses # total number of CONNECTED synapses on a single dendritic segment
        
        self.nmda_th = nmda_th
        self.perm_th = perm_th
        self.perm_init = perm_init
        
        # list containing the matrices of potential synapses (permanence values) for each dendrite
        # of the HTM cell
        self.dendrites = [np.random.normal(loc=self.perm_init, scale=0.01, size=[self.M, self.N])
                          for i in range(self.n_dendrites)] # is a list of 32 MxN matrices
        
        return
        
        
    def get_connected_synapses(self):
        """
        For getting the connected synapses on all the dendrites of the cell.
        
        Returns
        -------
        A Boolean array of size (n_dendrites, M, N)

        """
        
        connected_synapses = np.array(self.dendrites > self.perm_th) # is a list of 32 MxN binary matrices
        
        return connected_synapses
        
    
    def max_overlap_dendrite(self):
        
        return
        
        
    def cell_output(self):
        
        return
        
        
    def cell_predict(self):
        
        return
        
        