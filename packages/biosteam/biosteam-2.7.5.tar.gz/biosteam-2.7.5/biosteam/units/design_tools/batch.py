# -*- coding: utf-8 -*-
"""
General functional algorithms for batch design.
"""

__all__ = ('size_batch',)

def size_batch(F_vol, tau_reaction, tau_turnaround, N_reactors, V_wf) -> dict:
    """
    Solve for batch reactor volume, cycle time, and loading time.
    
    Parameters
    ----------
    F_vol : float
        Volumetric flow rate.
    tau_reaction : float
        Reaction time.
    tau_turnaround : float
        Turnaround time.
    N_reactors : int
        Number of reactors.
    V_wf : float
        Fraction of working volume.
    
    Returns
    -------
    dict
        * 'Reactor volume': float
        * 'Batch time': float
        * 'Cycle time': float
        * 'Loading time': float
       
    Notes
    -----
    Units of measure may vary so long as they are consistent.
        
    """
    # Cycle time assuming no down time.
    tau_cycle = tau_reaction + tau_turnaround
    
    # Total volume of all reactors.
    V_T = F_vol * tau_cycle / (1 - 1 / N_reactors)
    
    # Volume of an individual reactor
    V_i = V_T/N_reactors
    
    # Time required to load a reactor
    tau_loading = V_i/F_vol
    
    # Total batch time
    tau_batch = tau_cycle + tau_loading
    
    # Account for excess volume
    V_i /= V_wf 
    
    return {'Reactor volume': V_i,
            'Batch time': tau_batch,
            'Cycle time': tau_cycle,
            'Loading time': tau_loading}
        
        