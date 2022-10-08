# Some physical constants
from scipy.constants import N_A, h, c, Rydberg
amu = 1e-3/N_A
hartree = Rydberg*h*c*2


import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import logging
import sys
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
    """Finds the datapoint with lowest energy"""
    minimum = np.argmin(data["energies"])
    min_dist, min_angl = np.unravel_index(minimum, data["energies"].shape)

    return data["distances"][min_dist], data["angles"][min_angl], data["energies"][min_dist, min_angl]

def harmonic_potential(dist_angl, E_min, k_r, k_theta, r_min, theta_min):
    """The harmonic approximation of the potential energy"""
    dist, angl = dist_angl

    # Calculate the energy
    E = E_min + 0.5*k_r*(dist - r_min)**2 + 0.5*k_theta*(angl-theta_min)**2

    return E


def fit_potential_around_minimum(data, delta_dist, delta_angl, min_dist=None, min_angl=None):
    """
    Fits the data within (delta_dist, delta_angl) from the potential minimum to the harmonic potential
    """

    # Use the datapoint with minimal energy as estimate of the equilibrium geometry if not provided
    min_dist_rough, min_angl_rough, min_energy_rough = find_min_energy(data)
    if min_dist is None:
        min_dist = min_dist_rough
    if min_angl is None:
        min_angl = min_angl_rough

    # Filter the data around the energy minimum
    filtered = data["raw"]
    filtered = filtered[np.abs(filtered[:,1]-min_dist) <= delta_dist]
    filtered = filtered[np.abs(filtered[:,2]-min_angl) <= delta_angl]

    logging.info(f"Fitting harmonic potential using {len(filtered)} data points")

    p0 = [min_energy_rough,1,1e-5,min_dist,min_angl] # estimate of the parameters
    params, covar = curve_fit(harmonic_potential, filtered[:,1:].T, filtered[:,0], p0=p0)

    return params

def calculate_frequencies(k_r, k_theta, r_mean, mu_r=2.0, mu_theta=0.5):
    """Calculates the wavenumbers from force constants and mean bond length"""

    # convert everything to SI units and radians
    mu_r *= amu # from amu to kg
    mu_theta *= amu # from amu to kg

    r_mean *= 1e-10 # from Angstroem to m

    k_r *= 1e20*hartree # from hartree/Angstroem^2 to J/m^2
    k_theta *= (180/np.pi)**2*hartree # from hartree/degree^2 to J/radian^2

    # calculate wavenumbers [in cm-1]
    nu_r = 1/(2*np.pi*c)*np.sqrt(k_r/mu_r) * 1e-2
    nu_theta = 1/(2*np.pi*c)*np.sqrt(k_theta/(r_mean**2*mu_theta)) * 1e-2
    
    return nu_r, nu_theta, k_r, k_theta

def estimate_classical_limits(nu_r, nu_theta, k_r, k_theta):
    """Estimates the classical limit of change in angle/distance during vibration"""

    # Calculate the classical limits
    dr_max = np.sqrt(h*c*nu_r*1e2/k_r)
    dtheta_max = np.sqrt(h*c*nu_theta*1e2/k_theta)

    # Convert to Angstroem and degrees
    dr_max *= 1e10
    dtheta_max *= 180/np.pi

    return dr_max, dtheta_max

def estimate_frequencies_with_estimated_limits(iters=5):
    """
    Estimates the frequencies (in cm-1).
    
    The datapoints which are used to fit the harmonic potential are iteratively chosen according to classical limits.

    Returns the frequencies (cm-1), the potential energy minimum (energy [hartree], r_min [A], theta_min [deg]), classical limits (in SI and radians)
    """
    limits = (0.1, 2.)
    min_loc = find_min_energy(data)[:2]

    for i in range(iters):
        params = fit_potential_around_minimum(data, *limits, *min_loc)
        min_loc = params[3:5]

        freqs = calculate_frequencies(*params[1:4])

        limits = estimate_classical_limits(*freqs)

        if limits[0] < 0.06:
            limits[0] = 0.06
        if limits[1] < 1.1:
            limits[1] = 1.1
    
    return freqs[:2], params[[0,3,4]], limits

def plot_3D(data, filename):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    dist, angl = np.meshgrid(data["distances"], data["angles"])

    surf = ax.plot_surface(dist, angl, data["energies"].T, cmap="coolwarm",
                           linewidth=0, antialiased=True)

    ax.set_title(filename)
    ax.set_xlabel("r [A]")
    ax.set_ylabel("angle [degree]")
    ax.set_zlabel("E [hartree]")
    plt.show()


if __name__ == "__main__":

    # Parse console input
    if len(sys.argv) < 2:
        logging.error("You must specify the file with data")
        logging.info("Run the script as: python calculate_frequencies.py [filename] [--graph, optional]")
        exit(0)

    graph = False
    if "--graph" in sys.argv:
        graph = True

    # Load the data
    filename = sys.argv[1]
    try:
        data = load_data(filename)
    except Exception as ex:
        logging.error(f"Could not load the data from '{filename}'\n{ex}")

    # Fit the harmonic potential and estimate frequencies
    min_point = find_min_energy(data)
    print("Datapoint with minimum energy:")
    print("{:<20}{:<20}{:<20}".format("Energy [hartree]","r [Angstroem]","angle [degrees]"))
    print("{:<20.10f}{:<20.03f}{:<20.1f}".format(min_point[2],min_point[0],min_point[1]))

    print()
    print("Fitting the harmonic potential...")

    freqs, minimum, limits = estimate_frequencies_with_estimated_limits()
    print()

    print("Equilibrium geometry:")
    print("{:<20}{:<20}{:<20}".format("Energy [hartree]","r [Angstroem]","angle [degrees]"))
    print("{:<20.10f}{:<20.03f}{:<20.1f}".format(*minimum))
    print()

    print("Frequencies:")
    print("{:<30}{:<30}".format("Symm. stretch [cm-1]","Bending [cm-1]"))
    print("{:<30.1f}{:<30.1f}".format(*freqs))
    print()

    print("Classical limits:")
    print("{:<30}{:<30}".format("Symm. stretch [Angstroem]","Bending [degree]"))
    print("{:<30.3f}{:<30.2f}".format(*limits))
    print()

    if graph:
        plot_3D(data, filename)

    logging.info("Program terminated successfuly.")