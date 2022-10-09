# This script simulates 1D diffusion in closed finite space
# Run this using: python diffusion_1D.py
# First, integral of the concentration over time is shown (to show that the amount of material stays constant)
# Then, the animation of the diffusion is shown

import numpy as np
from scipy.integrate import solve_ivp

from matplotlib import pyplot as plt
from matplotlib import animation as animation

# Definition of the differential equations
def D_conc(t, conc):
    filt = [1,-2,1]
    d_conc = np.convolve(conc, filt, mode='same')

    # Handle the edges
    d_conc[0] += conc[0]
    d_conc[-1] += conc[-1]

    return d_conc

# Define the initial state
x = np.linspace(0,10,100)
conc0 = np.where((x>=3)&(x<=3.5), 1, 0)+np.where((x>=7)&(x<=7.5), 1, 0)

# Define the simulation timepoints
TIME = np.linspace(0,50,200)

# Solve the differential equation
solution = solve_ivp(D_conc, [TIME[0],TIME[-1]], conc0, t_eval=TIME, max_step=1, method="DOP853")

# Plot the integral over time to show that the total amount of the substance does not change
integrals = np.sum(solution.y, axis=0)
plt.plot(TIME, integrals)
plt.ylim(0,np.max(integrals)*1.1)
plt.xlabel("Time")
plt.ylabel("Integral over entire space")
plt.show()


# Animate the diffusion
fig, ax = plt.subplots()

line, = ax.plot(x, conc0)
time_text = ax.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)

ax.set_xlabel("1D space")
ax.set_ylabel("Concentration")

def animate(i):
    """Updates the data for each animation frame"""
    line.set_ydata(solution.y[:,i])
    time_text.set_text(f"Time: {TIME[i]:0.1f}")
    return line,time_text

ani = animation.FuncAnimation(fig, animate, frames=range(200), interval=50, blit=True, save_count=50)

plt.show()