# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 18:43:39 2019

@author: yoelr
"""
from . import Facility
from ..decorators import cost

__all__ = ('ProcessWaterCenter',)

@cost('Makeup water flow rate', 'Makeup water pump',
      CE=551, kW=20*0.7457, cost=6864, S=155564, n=0.8, BM=3.1)
@cost('Process water flow rate', 'Process water pump',
      CE=551, kW=75*0.7457, cost=15292, S=518924, n=0.8, BM=3.1)
@cost('Process water flow rate', 'Tank',
      CE=522, cost=250e3, S=451555, n=0.7, BM=1.7)
class ProcessWaterCenter(Facility):
    """
    Create a ProcessWaterCenter object that takes care of balancing the amount
    of make-up water required for the process. The capital cost and power
    are based on the flow rate of process and make-up water as in [1]_.
    
    Parameters
    ----------
    ins : stream sequence
        [0] Recycle water.
        
        [1] Make-up water.
    outs : stream
        Process water.
    update_recycled_process_water : callable, optional
        Function to update recycled water (ins[0]).
    
    References
    ----------
    .. [1] Humbird, D., Davis, R., Tao, L., Kinchin, C., Hsu, D., Aden, A.,
        Dudgeon, D. (2011). Process Design and Economics for Biochemical 
        Conversion of Lignocellulosic Biomass to Ethanol: Dilute-Acid 
        Pretreatment and Enzymatic Hydrolysis of Corn Stover
        (No. NREL/TP-5100-47764, 1013269). https://doi.org/10.2172/1013269
    
    """
    network_priority = 2
    _N_ins = 2
    _N_outs = 1
    _units = {'Makeup water flow rate': 'kg/hr',
              'Process water flow rate': 'kg/hr'}
    def __init__(self, ID='', ins=None, outs=(), update_recycled_process_water=None):
        Facility.__init__(self, ID, ins, outs)
        self.update_recycled_process_water = update_recycled_process_water
    
    def _assert_compatible_property_package(self): pass
    
    def _run(self):
        if self.update_recycled_process_water: self.update_recycled_process_water()
        s_recycle, s_makeup = self._ins
        s_process, = self.outs
        process_water = s_process.F_mol
        recycle_water = s_recycle.F_mol
        process_loss = process_water - recycle_water
        makeup_water = process_loss if process_loss > 0 else 0
        s_makeup.imol['7732-18-5'] = makeup_water
        Design = self.design_results
        Design['Process water flow rate'] = process_water * 18.015
        Design['Makeup water flow rate'] = makeup_water * 18.015
        
        