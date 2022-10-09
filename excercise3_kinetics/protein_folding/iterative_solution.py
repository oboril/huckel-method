# This script finds the equilibrium concentrations of the species by numerically solving the kinetics equations
# Run as: python iterative_solution.py

import numpy as np
from scipy.integrate import solve_ivp

from matplotlib import pyplot as plt

import constants as const

# Constants
T_MAX = 1e6
INITIAL_CONC = [0., 1., 0.]
UREA_CONCENTRATIONS = np.linspace(0,10,100)

def get_rate_constants(urea_conc):
    """Calculates the rate constants at given urea concentration"""
    kf_R15 = const.rate_const["kf_R15"]*np.exp(const.urea_coeff["kf_R15"]*urea_conc)
    ku_R15 = const.rate_const["ku_R15"]*np.exp(const.urea_coeff["ku_R15"]*urea_conc)
    kf_R16 = const.rate_const["kf_R16"]*np.exp(const.urea_coeff["kf_R16"]*urea_conc)
    ku_R16 = const.rate_const["ku_R16"]*np.exp(const.urea_coeff["ku_R16"]*urea_conc)
    return kf_R15, ku_R15, kf_R16, ku_R16

# Define the differential equations
def d_conc(t, y, rate_constants):
    """Returns the derivatives of the concentrations"""
    kf_R15, ku_R15, kf_R16, ku_R16 = rate_constants
    D, I, N = y

    dD = -D*kf_R15 + I*ku_R15
    dN = -N*ku_R16 + I*kf_R16
    dI = - dD - dN

    return [dD, dI, dN]

if __name__ == "__main__":
    print("Solving the equations...")
    results = np.zeros([len(UREA_CONCENTRATIONS), 3])
    for i, conc in enumerate(UREA_CONCENTRATIONS):
        # Get the rate constants
        rate_constants = get_rate_constants(conc)
        fun = lambda t,y: d_conc(t,y, rate_constants)

        # Solve the kinetic equations
        solution = solve_ivp(fun, [0,T_MAX], INITIAL_CONC, method='LSODA', t_eval=[T_MAX])
        if not solution.success:
            print(f"ERROR: The integration did not converge (urea concentration = {conc:0.2f} M)")
            exit()
        # Save the solution
        eq = solution.y[:,0]
        results[i] = eq

    print("Equations solved")

    # Extract the concentrations
    D, I, N = results.T

    # Plot the result
    plt.plot(UREA_CONCENTRATIONS, D, label="D")
    plt.plot(UREA_CONCENTRATIONS, I, label="I")
    plt.plot(UREA_CONCENTRATIONS, N, label="N")

    plt.xlabel("Urea concentration [M]")
    plt.ylabel("Fractional composition")

    plt.legend()
    plt.show()
