# This scripts simulates 2D diffusion in a closed square container
# Run using: python diffusion_2D.py

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import convolve2d

from matplotlib import pyplot as plt
from matplotlib import animation as animation

from datetime import datetime

# Define the simulation constants
SHAPE = (256,256)
TIME = np.linspace(0,200,200)

# Define the initial state
conc0 = np.zeros(SHAPE, dtype=float)
conc0[100:150,100:180] = 1.

# Define the differential equations
def D_conc(t, conc):
    # Reshape the array to correct shape
    conc = np.reshape(conc, SHAPE)

    # Apply the convolution to get derivative
    filt = [[0,1,0],[1,-4,1],[0,1,0]]
    Dconc = convolve2d(conc, filt, mode='same')

    # Handle the edges
    edges = np.zeros(SHAPE)
    edges[0,:]+=1
    edges[:,0]+=1
    edges[-1,:]+=1
    edges[:,-1]+=1
    Dconc += edges*conc

    # return the flattened array with derivatives
    return Dconc.flatten()

# Solve the differential equation
print("Solving equations...")
start = datetime.now()

solution = solve_ivp(D_conc, [TIME[0],TIME[-1]], conc0.flatten(), t_eval=TIME, max_step=1, method="DOP853")

print("Finished in", datetime.now()-start)
print(solution.message)

# Reshape the solution to [t,x,y]
solution = np.reshape(solution.y,[*SHAPE,len(TIME)]).transpose([2,0,1])

# Animate the result
fig, ax = plt.subplots()

img = ax.imshow(solution[0], vmin=0, vmax=1, cmap='hot')
time_text = ax.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes, color='white')
fig.colorbar(img)

def animate(i):
    """Updates the data for each animation frame"""
    img.set_array(solution[i])
    time_text.set_text(f"Time: {TIME[i]:0.0f}")
    return img, time_text


ani = animation.FuncAnimation(fig, animate, frames=len(TIME), interval=50, blit=True, save_count=50)

plt.show()