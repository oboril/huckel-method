# This script uses the reaction rate constants to get the exact fraction of species at different urea concentrations
# Run using: python exact_solution.py

import numpy as np
from matplotlib import pyplot as plt

import constants as cons

def get_equilibrium_constants(urea_conc):
    """Calculates the two equilibrium constants at given urea concentration"""

    K_R15 = cons.rate_const["kf_R15"]*np.exp(cons.urea_coeff["kf_R15"]*urea_conc)
    K_R15 /= cons.rate_const["ku_R15"]*np.exp(cons.urea_coeff["ku_R15"]*urea_conc)

    K_R16 = cons.rate_const["kf_R16"]*np.exp(cons.urea_coeff["kf_R16"]*urea_conc)
    K_R16 /= cons.rate_const["ku_R16"]*np.exp(cons.urea_coeff["ku_R16"]*urea_conc)

    return K_R15, K_R16

def get_fractional_composition(urea_conc):
    """Calculates the fractional composition at given urea concentration"""
    
    K_R15, K_R16 = get_equilibrium_constants(urea_conc)

    D = 1/(1+K_R15+K_R15*K_R16)
    I = D*K_R15
    N = I*K_R16

    return D, I, N

if __name__=="__main__":
    urea_conc = np.linspace(0,10,100)
    D, I, N = get_fractional_composition(urea_conc)

    plt.plot(urea_conc, D, label="D")
    plt.plot(urea_conc, I, label="I")
    plt.plot(urea_conc, N, label="N")

    plt.xlabel("Urea concentration [M]")
    plt.ylabel("Fractional composition")

    plt.legend()
    plt.show()
