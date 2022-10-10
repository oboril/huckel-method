# Excercise 4: Exploring Potential Energy surfaces
This folder contains two different scripts which attempt to find the global energetic minimum of multiparticle system.

Use:
```
python randomized_optimization.py [potential] [number of particles] [iterations] [output file]
    [potential] - what potential to use, available are: lennard-jones, morse-1, morse-2
    [number of particles] - number of particles in the system, all are assumed to be identical
    [iterations] - number of randomizations to perform, recommended value is 5-20
    [output file] - .xyz file where the optimized coordinates will be saved
```

```
python simulated_annealing.py [potential] [number of particles] [iterations] [output file]
    [potential] - what potential to use, available are: lennard-jones, morse-1, morse-2
    [number of particles] - number of particles in the system, all are assumed to be identical
    [iterations] - number of iterations to perform, recommended value is 100 000 - 1 000 000
    [output file] - .xyz file where the optimized coordinates will be saved
```

## The approach
Because the multiparticle systems contain numerous local minima, algorithms such as gradient descent are not suitable for finding the global minimum. The search space is too large to explore systematically, and so stochactic optimization algorithms must be used.

### Redundant coordinates
To simplify the problem, it is possible to remove 6 degrees of freedom (which would correspond to cluster translation and rotation). Let's say that the location of each particle is $(x_i,y_i,z_i)$.
Without loss of generality, the coordinates $x_1, y_1, z_1, x_2, y_2, x_3$ can be set to 0.

### Randomized optimization
The script `randomized_optimization.py` repeatedly finds a local minimum and randomly pertubes the coordinates. This approach is more likely to find the global solution than a single optimization, but it is not very reliable when there are local minima with similar energies to the global minimum.

Example output:
```
C:\excercise4_potentials>python randomized_optimization.py lennard-jones 7 10 output.xyz      
Minimizing energy...
Iter 0: E = -3.8832650136422986
Iter 1: E = -3.8832650136422986
Iter 2: E = -4.126346042001279
WARNING: Solution did not converge, skipping this iteration
Desired error not necessarily achieved due to precision loss.
Iter 4: E = -4.126346042001279
Iter 5: E = -4.126346042001279
Iter 6: E = -4.126346042001279
Iter 7: E = -4.126346042001279
Iter 8: E = -4.126346042001279
Iter 9: E = -4.126346042001279
Minimization ended in 0:00:03.677972
Minimum energy = -4.1263
Distance matrix:
0.0000 1.1152 1.1152 1.1152 1.1152 1.1477 1.1152
1.1152 0.0000 1.8188 1.1241 1.1241 1.1152 1.8188
1.1152 1.8188 0.0000 1.1241 1.8188 1.1152 1.1241
1.1152 1.1241 1.1241 0.0000 1.8188 1.1152 1.8188
1.1152 1.1241 1.8188 1.8188 0.0000 1.1152 1.1241
1.1477 1.1152 1.1152 1.1152 1.1152 0.0000 1.1152
1.1152 1.8188 1.1241 1.8188 1.1241 1.1152 0.0000
Coordinates saved to output.xyz
```

### Simulated annealing
This approach is well known for its asymptotic convergence to the global minimum, as well as for its computational inefficiency. From my experiments, 1M iterations are usually enough to converge to the global minimum, but the calculation takes 2-3 minutes.

Example output:
```
C:\excercise4_potentials>python simulated_annealing.py lennard-jones 7 1000000 output.xyz
Minimizing energy...
Minimization ended in 0:02:18.295457
Minimum energy = -4.1263
Distance matrix:
0.0000 1.1477 1.1152 1.1152 1.1152 1.1152 1.1152
1.1477 0.0000 1.1152 1.1152 1.1152 1.1152 1.1152
1.1152 1.1152 0.0000 1.8188 1.8188 1.1241 1.1241
1.1152 1.1152 1.8188 0.0000 1.1241 1.8188 1.1241
1.1152 1.1152 1.8188 1.1241 0.0000 1.1241 1.8188
1.1152 1.1152 1.1241 1.8188 1.1241 0.0000 1.8188
1.1152 1.1152 1.1241 1.1241 1.8188 1.8188 0.0000
Coordinates saved to output.xyz
```

# Results


| # particles   | shape  | E(Lennard-Jones)  | E(Morse 1) | E(Morse 2) |
| ------------- |-------------| -----| -----| ----- |
| 3 | triangle                 | -0.7500 | 0.0000 | 0.0000 |
| 4 | tetrahedron              | -1.5000 | 0.0000 | 0.0000 |
| 5 | trigonal bipyramid       | -2.2760 | 0.1477 | 0.4567 |
| 6 | octahedron               | -3.1780 | 0.2818 | 0.8664 |
| 7 | pentagonal bipyramid     | -4.1263 | 0.6718 | 2.1732 |