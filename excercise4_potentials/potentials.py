import numpy as np

def lennard_jones(r):
    """
    Returns the Lennard-Jones potential for the distance r.
    Assumes that all constants are 1, this can be corrected by calculating the potential as V = 4*e*lennard_jones(r/sigma).
    """
    r6 = r**6
    V = (1/r6**2) - (1/r6)
    return V

def morse(r, re):
    """
    Returns the Morse potential for the distance r and equilibrium distance re
    Assumes that all constants are 1, , this can be corrected by calculating the potential as V = D_e*(r*sigma, re*sigma).
    """
    V = (1-np.exp(-(r-re)))**2
    return V

potentials = {"lennard-jones": lennard_jones, "morse-1": lambda r: morse(r,1.), "morse-2": lambda r: morse(r,2.)}
