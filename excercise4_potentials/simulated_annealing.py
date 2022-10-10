# This script attempts to find the global minimum using simulated annealing
# Use as: python simulated_annealing.py [potential] [number of particles] [iterations] [output file]

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import minimize

import utils
import potentials

from sys import argv
from datetime import datetime

# PARSE THE USER INPUT
if len(argv) != 5:
    print("ERROR: Incorrect number of arguments")
    print("Use: python randomized_optimization.py [potential] [number of particles] [iterations] [output file]")
    exit()

if argv[1] in potentials.potentials:
    POTENTIAL = potentials.potentials[argv[1]]
else:
    print(f"ERROR: Unknown potential '{argv[1]}'")
    print("The possible potentials are:", ', '.join(potentials.potentials.keys()))
    exit()

try:
    N_PARTICLES = int(argv[2])
except:
    print(f"ERROR: Could not parse the number of particles '{argv[2]}'")
    print("Use: python randomized_optimization.py [potential] [number of particles] [iterations] [output file]")
    exit()
if N_PARTICLES < 3:
    print(f"ERROR: The number of particles must be at least 3, not {N_PARTICLES}")
    exit()

try:
    ITERATIONS = int(argv[3])
except:
    print(f"ERROR: Could not parse the number of iterations '{argv[3]}'")
    print("Use: python randomized_optimization.py [potential] [number of particles] [iterations] [output file]")
    exit()
if ITERATIONS < 100:
    print(f"ERROR: The number of iterations must be at least 100, not {ITERATIONS}")
    exit()

FILENAME = argv[4]
if not FILENAME.endswith(".xyz"):
    print(f"ERROR: the output file must be .xyz, not {FILENAME}")
    print("Use: python randomized_optimization.py [potential] [number of particles] [iterations] [output file]")
    exit()

# INITIALIZE VARIABLES
TIME = np.linspace(0,1,ITERATIONS)
TEMP = (1-TIME)*0.1+1e-7
RANDOMIZATION = TEMP*1.

# Initialize position of all particles randomly in a 8x8x8 box around origin
POS0 = np.random.rand(N_PARTICLES*3-6)*8-4

energy_fun = lambda vec: utils.get_energy(vec, POTENTIAL)

# RUN SIMULATED ANNEALING
print("Minimizing energy...")
start = datetime.now()

best_e = 999.
best_vec = POS0
curr_e = 999.
curr_vec = POS0
energies = []
iters = []
for i, (rnd, temp) in enumerate(zip(RANDOMIZATION, TEMP)):
    test_vec = curr_vec + np.random.randn(len(curr_vec))*rnd
    test_e = energy_fun(test_vec)

    if max(abs(test_vec) > 5.):# or test_e > 5.:
        continue
    
    if test_e < best_e:
        best_e = test_e
        best_vec = test_vec

    dE = test_e - curr_e
    if dE < 0:
        prob = 1
    else:
        prob = np.exp(-dE/temp)

    if prob >= np.random.rand():
        curr_e = test_e
        curr_vec = test_vec
        energies.append(curr_e)
        iters.append(i)

# Refine the result
solution = minimize(energy_fun, best_vec)
if not solution.success:
        print("WARNING: Solution did not converge")
        print(solution.message)
        exit()
    
best_vec = solution.x
best_e = energy_fun(best_vec)

print(f"Minimization ended in {datetime.now()-start}")



# PRINT AND SAVE THE RESULTS

print(f"Minimum energy = {best_e:0.4f}")

print("Distance matrix:")
print(utils.distance_matrix_to_str(best_vec))

utils.save_coordinates(best_vec, FILENAME, f"Optimized solution, E = {best_e:0.4f}")
print(f"Coordinates saved to {FILENAME}")

# Show the energy over iterations
plt.plot(iters, energies)
plt.show()