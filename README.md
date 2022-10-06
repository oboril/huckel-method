# Hückel method
This script calculates the Huckel energies for selected compounds.
The Huckel method is described here:
https://en.wikipedia.org/wiki/H%C3%BCckel_method

In this script:  
$\left<\Psi_i\middle|\hat{H}\middle|\Psi_i\right>=H_{i,i}=\alpha=0$  
$\left<\Psi_i\middle|\hat{H}\middle|\Psi_j\right>=H_{i,j}=\beta=-1 \quad (i\ne j)$  
$\left<\Psi_i\middle|\Psi_i\right>=S_{i,i}=1$  
$\left<\Psi_i\middle|\Psi_j\right>=S_{i,j}=0 \quad (i\ne j)$  


## Use
To calculate the Huckel energies for specified &pi;-system, run:  
```
python main.py [structure] [number of atoms, optional] [flags, optional]
```  
The possible structures are:  
```
linear_polyene, platonic, cyclic_polyene, tetrahedron, octahedron, cube, icosahedron, dodecahedron, fullerene60
```  
Flags:  
```
    -h --help       Displays this message  
    -o --optimized  Use general solution for linear and cyclic polyenes instead of solving eigenvalues
```
Example inputs:  
```
python main.py cyclic_polyene 6
python main.py cube
python main.py platonic 4
python main.py fullerene60
```
The output energies are relative to the atom energies, and are not scaled (alpha=0, beta=-1).

## Requirements
Python 3 (I'm using Python 3.10)  
 * numpy  
 * logging  
 * unittest

## Example output
```
C:\huckel-method> python main.py cyclic_polyene 6 --optimized
INFO:root:Using general solution to obtain energies
N      Degen.       Energy
4      1             2.000
3      2             1.000
2      2            -1.000
1      1            -2.000
INFO:root:Program has finished successfuly
```

```
C:\huckel-method> python main.py fullerene60                 
N      Degen.       Energy
15     3             2.618
14     4             2.562
13     4             2.000
12     5             1.618
11     3             1.438
10     5             1.303
9      3             0.382
8      3             0.139
7      5            -0.618
6      9            -1.000
5      4            -1.562
4      3            -1.820
3      5            -2.303
2      3            -2.757
1      1            -3.000
INFO:root:Program has finished successfuly
```