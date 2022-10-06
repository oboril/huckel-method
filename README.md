# Hückel method
This script calculates the Huckel energies for selected compounds.

The Huckel method is described here:
https://en.wikipedia.org/wiki/H%C3%BCckel_method

In this script, \alpha=0 and \beta=-1.

## Use
To calculate the Huckel energies for specified pi-system, run:
  python main.py [structure] [number of atoms, optional]
The possible structures are:
  linear_polyene, platonic, cyclic_polyene, tetrahedron, octahedron, cube, icosahedron, dodecahedron, fullerene60
Flags:
  -h --help       Displays this message
  -o --optimized  Use general solution for linear and cyclic polyenes instead of solving eigenvalues
Example inputs:
  - python main.py cyclic_polyene 6
  - python main.py cube
  - python main.py platonic 4
  - python main.py fullerene60
The output energies are relative to the atom energies, and are not scaled (alpha=0, beta=-1).

## Requirements
Python 3 (I'm using Python 3.10)  
numpy  
logging  
unittest