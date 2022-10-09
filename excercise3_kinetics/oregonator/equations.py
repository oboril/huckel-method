# This file contains the definition of the differential equations and the initial state
# The ln(concentrations) is calculated to make the solution numerically stable

import numpy as np

# Rate constants
ln_k1 = np.log(1.34)
ln_k2 = np.log(1.6e9)
ln_k3 = np.log(8e3)
ln_k4 = np.log(4e7)
ln_k5 = np.log(1)

# Initial concentrations
initial_concs = np.log([0.06, 0.06, 1e-50, 1e-50, 10**(-9.8), 10**(-6.52), 10**(-7.32)])

# Names of the variables
variables = "A B P Q X Y Z".split()

# Definition of the differential equations
def conc_changes(t, concs):
    ln_A, ln_B, ln_P, ln_Q, ln_X, ln_Y, ln_Z = concs

    ln_r1 = ln_k1 + ln_A + ln_Y
    ln_r2 = ln_k2 + ln_X + ln_Y
    ln_r3 = ln_k3 + ln_B + ln_X
    ln_r4 = ln_k4 + ln_X*2
    ln_r5 = ln_k5 + ln_Z

    d_ln_A = -np.exp(ln_r1-ln_A)
    d_ln_B = -np.exp(ln_r3-ln_B)
    d_ln_P = np.exp(ln_r1-ln_P)+np.exp(ln_r2-ln_P)
    d_ln_Q = np.exp(ln_r4-ln_Q)
    d_ln_X = np.exp(ln_r1-ln_X)-np.exp(ln_r2-ln_X)+np.exp(ln_r3-ln_X)-2*np.exp(ln_r4-ln_X)
    d_ln_Y = -np.exp(ln_r1-ln_Y)-np.exp(ln_r2-ln_Y)+np.exp(ln_r5-ln_Y)
    d_ln_Z = np.exp(ln_r3-ln_Z)-np.exp(ln_r5-ln_Z)

    return [d_ln_A, d_ln_B, d_ln_P, d_ln_Q, d_ln_X, d_ln_Y, d_ln_Z]

