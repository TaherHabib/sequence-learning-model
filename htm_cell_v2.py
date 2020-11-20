import numpy as np
import pandas as pd

from ufuncs import dot_prod

class HTM_CELL():
    
    """
    
    """
    
    def __init__(self, cellsPerColumn=None, numColumns=None, 
                 maxDendritesPerCell=None, maxSynapsesPerDendrite=None, 
                 nmdaThreshold=None, permThreshold=None, permInit=None, permInit_sd=None):
        
        self.M = cellsPerColumn
        self.N = numColumns 

        self.maxDendritesPerCell = maxDendritesPerCell
        self.maxSynapsesPerDendrite = maxSynapsesPerDendrite # max. number of CONNECTED synapses on a 
                                                             # single dendritic segment.
        self.nmdaThreshold = nmdaThreshold
        self.permThreshold = permThreshold
        self.permInit = permInit
        self.permInit_sd = permInit_sd
        
        # list containing the (numpy array) MxN matrices of potential synapses (permanence values) for each dendrite
        # of the HTM cell; shape: (<maxDendritesPerCell>,M,N). There are NO dendrites initially.
        self.dendrites = [None for i in range(maxDendritesPerCell)]
        
        self.dutycycle = []
        
        return
    
    
    def get_cell_numDendrites(self):
        
        numDendrites = 0
        for dendrite in self.dendrites:
            if dendrite is None:
                continue
            else:
                numDendrites+=1
        
        return numDendrites
    
    
    def get_cell_numSynapsesOnDendrite(self, dendrite_idx=None):
        
        return np.count_nonzero(self.dendrites[dendrite_idx])
    
    
    def grow_cell_newDendrite(self, prev_winnerCells=None):
        
        newDendrite = np.array(np.random.normal(loc=self.permInit, scale=self.permInit_sd, size=[self.M, self.N]), 
                               dtype=np.float64)
        
        newDendrite = newDendrite*prev_winnerCells
        # 'newDendrite' will ONLY have connections (at permInit level) to 'presynaptic_WinnerCells'.
        # The rest will be all 0.0. Any dendrite will have atmost <maxSynapsesPerDendrite> synapses.
        
        newDendrite_idx = None
        
        # 'newDendrite' will be assigned to the first "non-NONE" index in self.dendrites array
        for i in range(self.maxDendritesPerCell):
            if self.dendrites[i] is None:
                newDendrite_idx = i
                break
            else:
                continue
            
        if newDendrite_idx is None:
            print('Cell Capacity is FULL! :(')
        
        else:
            self.dendrites[newDendrite_idx] = newDendrite

        return
    
    
    def grow_cell_newSynapsesOnDendrite(self, dendrite_idx=None, prev_winnerCells=None):
        
        newSynapsesCapacity = self.maxSynapsesPerDendrite - self.get_cell_numSynapsesOnDendrite(dendrite_idx)
        
        
        
        return
    
    
    def update_cell_dendritePermanences(self, dendrite_idx=None, prev_state=None):
        
        
        return
    
    
    def get_cell_connectedSynapses(self):
        """
        For getting the connected synapses on all the dendrites of the cell.
        
        """
        
        cell_connectedSynapses = []
        
        for dendrite in self.dendrites:
            if dendrite is None:
                cell_connectedSynapses.append(None)
            else:
                cell_connectedSynapses.append(dendrite>self.permThreshold)
        
        return np.array(cell_connectedSynapses, dtype=object) # numpy array of length <maxDendritesPerCell> of either 
                                                              # 'None' elements or MxN (numpy) boolean matrices.        
                    
    def get_cell_predicitivity(self, net_state=None):
        """
        Checks if the cell is in a predictive state, given the current 
        timestep's network activity.

        Parameters
        ----------
        net_state : binary array of shape (MxN). 
        Containing the activity of cell population from current time step.
    
        Returns
        -------
        None.

        """

        # 'dendritesSpikes' will be a list containing <maxDendritesPerCell> elements,
        # either 'None' if the dendrites have NO synapses; OR, a boolean value.
        dendritesSpikes = []        
        cell_predictivity = False
        predDendrites = None
        cell_connectedSynapses = self.get_cell_connectedSynapses() 
                
        for dendrite in cell_connectedSynapses:
            if dendrite is None:
                dendritesSpikes.append(None)
            else:
                # 'is_nmdaSpike' is a numpy boolean array of length 1, with either a True or False.
                is_nmdaSpike = dot_prod(net_state, dendrite)>self.nmdaThreshold
                dendritesSpikes.append(is_nmdaSpike[0])
            
        if any(dendritesSpikes):
            cell_predictivity = True
            predDendrites = np.where(dendritesSpikes)[0] # 1D numpy array of max. possible length 
                                                         # <maxDendritesPerCell>.
                                                        
        return cell_predictivity, predDendrites
    
     
    def get_cell_numUnusedDendrites(self):
        
        num_UnusedDendrites = 0
        
        for dendrite in self.dendrites:
            if dendrite is None:
                num_UnusedDendrites += 1
            else:
                continue
        
        return num_UnusedDendrites
    
    
    def get_cell_allDendrites(self):
        """
        For getting the permanence values of all synapses on all the dendrites 
        of the cell.
        
        """
        
        return np.array(self.dendrites, dtype=object)
    
    
    def update_cell_dutycycle(self, prev_state=None, prev_pred=None):
        
        
        return