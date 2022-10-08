import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import logging
logging.basicConfig(level=logging.INFO)

def load_data(filename):
    """
    Loads the csv [energy, distance, angle] and parses the energies into 2D array [distance,angle]
    """
    # Load the data
    data = np.genfromtxt(filename, delimiter=";", skip_header=1)

    # Preprocess and reshape into 2D
    distances = np.unique(data[:,1])
    angles = np.unique(data[:,2])

    energies = data[:,0][np.lexsort((data[:,1], data[:,2]))]
    energies = energies.reshape([len(angles),len(distances)]).T

    result = {"distances": distances, "angles": angles, "energies": energies, "raw": data}

    return result

def find_min_energy(data):
    minimum = np.argmin(data["energies"])
    min_dist, min_angl = np.unravel_index(minimum, data["energies"].shape)

    return data["distances"][min_dist], data["angles"][min_angl]

def plot_3D(data):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    dist, angl = np.meshgrid(data["distances"], data["angles"])

    surf = ax.plot_surface(dist, angl, data["energies"].T, cmap="coolwarm",
                           linewidth=0, antialiased=True)
    plt.show()

def quadratic_2D(dist_angl, a,b,c,d,e,f):
    dist, angl = dist_angl
    return a + b*dist + c*angl + d*dist*angl + e*dist**2 + f*angl**2

def quadratic_2D_min(params):
    """Returns the minimum of the 2D quadratic function [distance, angle, energy]"""
    a,b,c,d,e,f = params
    min_angle = (b*d - 2*e*c)/(4*e*f - d**2)
    min_distance = - (b + d*min_angle)/(2*e)
    min_energy = quadratic_2D([min_distance, min_angle],*params)

    return min_distance, min_angle, min_energy

def quadratic_2D_hessian(params):
    """Returns the hessian of the 2D quadratic function, the order of derivatives is [distance, angle]"""
    a,b,c,d,e,f = params
    dDD = 2*e
    dAA = 2*f
    dAD = d
    hess = np.array([[dDD,dAD],[dAD,dAA]])

    return hess

def fit_quadratic_around_minimum(data, delta_dist, delta_angl):
    """
    Uses data around the minimum in the range (+- delta_dist, +- delta_angl) to fit 2nd degree 2D polynomial.
    E = a + b*D + c*A + d*D*A + e*D*D + f*A*A (where E is energy, D is distance, A is angle)
    """

    min_dist, min_angl = find_min_energy(data)

    filtered = data["raw"]
    filtered = filtered[np.abs(filtered[:,1]-min_dist) <= delta_dist]
    filtered = filtered[np.abs(filtered[:,2]-min_angl) <= delta_angl]

    logging.info(f"Fitting 2D quadratic function using {len(filtered)} data points")

    params, covar = curve_fit(quadratic_2D, filtered[:,1:].T, filtered[:,0])

    return params

data = load_data("data/H2O.csv")

min_dist, min_angl = find_min_energy(data)
print(min_dist, min_angl)

params = fit_quadratic_around_minimum(data, 0.1,3)
print(quadratic_2D([min_dist, min_angl],*params))

print(quadratic_2D_min(params))