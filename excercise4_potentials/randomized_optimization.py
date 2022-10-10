# This script attempts to find global minimum by iteratively finding local minimum and randomizing the coordinates
# Rus using: python randomized_optimization.py [potential] [number of particles] [iterations] [output file]

import numpy as np
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
if ITERATIONS < 1:
    print(f"ERROR: The number of iterations must be at least 1, not {ITERATIONS}")
    exit()

FILENAME = argv[4]
if not FILENAME.endswith(".xyz"):
    print(f"ERROR: the output file must be .xyz, not {FILENAME}")
    print("Use: python randomized_optimization.py [potential] [number of particles] [iterations] [output file]")
    exit()

# INITIALIZE VARIABLES

# Amplitudes used for randomization
RANDOMIZATION = np.linspace(2.,0.,ITERATIONS)

# Initialize position of all particles randomly in a 8x8x8 box around origin
POS0 = np.random.rand(N_PARTICLES*3-6)*8-4

energy_fun = lambda vec: utils.get_energy(vec, POTENTIAL)

# RUN THE OPTIMIZATION

print("Minimizing energy...")
start = datetime.now()

pos0 = POS0
best_energy = np.inf
best_vec = pos0
for i, rnd in enumerate(RANDOMIZATION):
    solution = minimize(energy_fun, pos0, tol=1e-5)
    if not solution.success:
        print("WARNING: Solution did not converge, skipping this iteration")
        print(solution.message)

        pos0 = best_vec + np.random.randn(len(solution.x))*rnd
        continue
    energy = energy_fun(solution.x)
    if energy < best_energy:
        best_energy = energy
        best_vec = solution.x

    print(f"Iter {i}: E = {energy_fun(best_vec)}")
    pos0 = best_vec + np.random.randn(len(solution.x))*rnd

print(f"Minimization ended in {datetime.now()-start}")

# PRINT AND SAVE THE RESULTS

energy = energy_fun(best_vec)

print(f"Minimum energy = {energy:0.4f}")

print("Distance matrix:")
print(utils.distance_matrix_to_str(best_vec))

utils.save_coordinates(best_vec, FILENAME, f"Optimized solution, E = {energy:0.4f}")
print(f"Coordinates saved to {FILENAME}")