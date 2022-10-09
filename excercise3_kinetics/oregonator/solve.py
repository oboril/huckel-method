# This script calculates the numerical solution to the oregonator equations specified in equations.py
# Run using: python solve.py

# The concentrations as their logarithm to make the integration more stable

import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt
from datetime import datetime

import equations as eq

# Specify the timepoints
TIME = np.linspace(0,300,1500)

# Solve the equations
print("Solving equations...")
start = datetime.now()

solution = solve_ivp(eq.conc_changes, (TIME[0],TIME[-1]), eq.initial_concs, t_eval=TIME, method='BDF', vectorized=True, rtol=1e-3, atol=1e-3)

print("Finished in", datetime.now()-start)
print(solution.message)

# Check the integration was successful
if not solution.success:
    print("ERROR: The integration was not successful")
    exit()

# Convert the concentrations from ln(conc) to conc
solution = np.exp(solution.y)

# Plot the results
for i in range(len(solution)):
    plt.semilogy(TIME, solution[i], '-' if i%2==0 else '--', label=eq.variables[i])

plt.ylim([10e-14, 1])

plt.xlabel("Time [s]")
plt.ylabel("Concentration [M]")

plt.legend()
plt.show()