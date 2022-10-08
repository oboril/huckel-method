# Automatic processing of Gaussian output
This collection of scripts helps to extract data from Gaussian .out files, graph the data and estimate vibrational frequencies.  
The script were specifically made to work with H2O and H2S.
## Extracting the data from .out files
The data can be parsed from .out files using the `parse.py` script.
```
Usage:
python parse.py [input folder] [output file] [optional flags --full --quotes]

Parameters:
[input folder]: folder containing the .out files
[output file]: the file where the data will be saved (in .csv format)
--full : include file names and quotes in the csv file
--quotes : saves only the quotes (in alphabetical order without duplicates)
```
By default, the saved file contains three columns:
`energy [hartree], bond length [Angstroem], angle [degrees]`

Example output:
```
C:\excercise2_gaussian>python parse.py data/H2Ooutfiles data/H2O.csv
INFO:root:Discovered 2275 .out files
INFO:root:Saving data to 'H2O_test.csv'
INFO:root:File saved, program exited successfuly
```
The `data/H2O.csv` file contains:
```
energy;distance;angle
-75.776261847;0.7000;100.0
-75.7771837999;0.7000;101.0
-75.778034029;0.7000;102.0
...
```

## Processing the data
The script `calculate_frequencies.py` uses the data to find the equilibrium geometry, vibrational frequencies, and classical limits. It can be also used to plot the energy potential.
```
Usage:
python calculate_frequencies.py [input file] [--graph, optional]

Parameters:
[input file]: the .csv file containing energies, bond lengths and angles
--graph : if this flag is used, a 3D graph of the potential energy will be shown
```

Example output:
```
C:\excercise2_gaussian>python calculate_frequencies.py data/H2S.csv --graph
Datapoint with minimum energy:
Energy [hartree]    r [Angstroem]       angle [degrees]     
-398.6756280320     1.350               94.0

Fitting the harmonic potential...
INFO:root:Fitting harmonic potential using 20 data points
INFO:root:Fitting harmonic potential using 80 data points
INFO:root:Fitting harmonic potential using 60 data points
INFO:root:Fitting harmonic potential using 57 data points
INFO:root:Fitting harmonic potential using 57 data points

Equilibrium geometry:
Energy [hartree]    r [Angstroem]       angle [degrees]
-398.6759644244     1.332               94.0

Frequencies:
Symm. stretch [cm-1]          Bending [cm-1]
2710.6                        1296.5

Classical limits:
Symm. stretch [Angstroem]     Bending [degree]
0.079                         9.81

INFO:root:Program terminated successfuly.
```

Example graph:  
![Example graph of the potential energy](example_graph.png?raw=true "Title")

# The math behind frequency estimation
To estimate the bivrational frequencies, the potential energy around minimum is fitted to the harmonic potential:

$$E=E_0+\frac{1}{2}k_r(r-\bar{r})^2+\frac{1}{2}k_\theta(\theta-\bar{\theta})^2$$

The wavelengths can be then estimated from the force constants $k_r$ and $k_\theta$ as follows:

$$\tilde{\nu} = \frac{1}{2\pi\tilde{c}} \sqrt{\frac{k_r}{{\mu}_r}}$$

$$\tilde{\nu} = \frac{1}{2\pi\tilde{c}} \sqrt{\frac{k_\theta}{{\bar{r}}^2{\mu}_\theta}}$$

The effective masses are taken to be $\mu_r=2.0\text{ amu}$ and $\mu_\theta=0.5\text{ amu}$ as recommended in the handout.