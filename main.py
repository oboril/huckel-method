import sys
import logging
logging.basicConfig(level=logging.INFO)

import numpy as np
from numpy import linalg as la

import huckel_matrix as hm
from parse_input import parse_user_input

def calc_platonic_solid(n_atoms, optimized):
    if optimized:
        logging.warning("There is no optimization for this structure")
    H = hm.platonic_solid(n_atoms)
    eigvals, eigvects = la.eigh(H)

    print_results(-eigvals)

def calc_cyclic_polyene(n_atoms, optimized):
    if optimized:
        logging.info("Using general solution to obtain energies")

        k = np.arange(n_atoms, dtype=float)
        energies = -2*np.cos(2*np.pi*k/n_atoms)

        print_results(energies)
    else:
        H = hm.cyclic_polyene(n_atoms)
        eigvals, eigvects = la.eigh(H)

        print_results(-eigvals)
    

def calc_linear_polyene(n_atoms, optimized):
    if optimized:
        logging.info("Using general solution to obtain energies")
        
        k = np.arange(n_atoms, dtype=float)
        energies = -2*np.cos((k+1)*np.pi/(n_atoms+1))

        print_results(energies)
    else:
        H = hm.linear_polyene(n_atoms)
        eigvals, eigvects = la.eigh(H)

        print_results(-eigvals)
    

def print_results(raw_energies):
    """Calculates the degeneracies and prints the result table"""
    # Detect degeneracies
    raw_energies = np.sort(raw_energies)
    energies = [raw_energies[0]]
    degeneracies = [0]
    for e in raw_energies:
        if abs(e-energies[-1]) < 1e-5:
            degeneracies[-1] += 1
        else:
            energies.append(e)
            degeneracies.append(1)
    
    # Print output
    form = "{:<6} {:<8} {:>10.3f}"
    form_head = "{:<6} {:<8} {:>10}"
    print(form_head.format("N", "Degen.", "Energy"))
    for i, (e,d) in list(enumerate(zip(energies, degeneracies)))[::-1]:
        print(form.format(i+1, d, e))

if __name__ == '__main__':
    # Parse the arguments from console
    structure, n_atoms, flags = parse_user_input()


    optimized = ("optimized" in flags)
    
    if structure == "no_calc":
        # No calculation has been submitted
        logging.warning("Exiting without performing any calculation")
    else:
        # Call the relevant function
        if structure == "platonic":
            calc_platonic_solid(n_atoms, optimized)
        elif structure == "linear_polyene":
            calc_linear_polyene(n_atoms, optimized)
        elif structure == "cyclic_polyene":
            calc_cyclic_polyene(n_atoms, optimized)

        logging.info("Program has finished successfuly")

