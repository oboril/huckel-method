# This script simulates simplified equations describing the Belousov-Zabotinsky reaction
# Run using: python belousov_zabotinsky_reaction.py [output_file_name.mp4] [resolution] [duration]

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import convolve2d

from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib.colors import ListedColormap

from datetime import datetime

from PIL import Image

from sys import argv

# Parse the input arguments
if len(argv) != 4:
    print("ERROR: Incorrect number of arguments")
    print("Run this script using: python belousov_zabotinsky_reaction.py [output_file_name.mp4] [resolution] [duration]")
    exit()

FILENAME = argv[1]
if not FILENAME.endswith(".mp4"):
    print("ERROR: The output file must be .mp4")
    print("Run this script using: python belousov_zabotinsky_reaction.py [output_file_name.mp4] [resolution] [duration]")
    exit()

try:
    RESOLUTION = int(argv[2])
except Exception as ex:
    print(f"ERROR: Could not parse {argv[2]} to an integer")
    print("Run this script using: python belousov_zabotinsky_reaction.py [output_file_name.mp4] [resolution] [duration]")
    exit()

try:
    DURATION = int(argv[3])
except Exception as ex:
    print(f"ERROR: Could not parse {argv[3]} to an integer")
    print("Run this script using: python belousov_zabotinsky_reaction.py [output_file_name.mp4] [resolution] [duration]")
    exit()

# Custom colormap
orange = np.array([207, 112, 64])/255
blue = np.array([167, 115, 250])/255
x = np.linspace(0,1,255)
colors = [orange*(1-i)+blue*(i) for i in x]
colormap = ListedColormap(colors)

# Define the initial conditions
SHAPE = (2,RESOLUTION,RESOLUTION)
y0 = np.zeros(SHAPE, dtype=float)
y0[0] = 1.
y0[1] = 1.
TIME = np.arange(DURATION)

# Random noise used to initialize the concentrations
noise = Image.fromarray((np.random.rand(RESOLUTION//30,RESOLUTION//30)*255).astype(np.uint8), 'L').resize(SHAPE[1:], Image.Resampling.BICUBIC)
noise = np.array(noise, dtype=float)/255
noise = noise**4

y0[1] = 0.3+0.7*noise


# Definition of the differential equations
def dy(t, y):
    # Constants
    alpha=0.5
    beta=-0.2
    gamma=0.1
    delta=-0.2

    # Reshape the array to [compound, x, y]
    y = np.reshape(y, SHAPE)
    
    a,b = y # Getting the individual compounds

    # Calculate the derivatives due to reaction
    da = a*alpha + a*b*beta
    db = a*b*gamma + b*delta

    # Calculate the derivatives due to diffusion
    filt = [[0,1,0],[1,-4,1],[0,1,0]]

    diff_da = convolve2d(a,filt,mode="same")
    diff_db = convolve2d(a,filt,mode="same")

    # Handle the edges
    peri = np.zeros(SHAPE[1:])
    peri[0,:] += 1.
    peri[:,1] += 1.
    peri[-1,:] += 1.
    peri[:,-1] += 1.

    diff_da += peri*a
    diff_db += peri*b

    # Return the combined derivatives. The derivative due to diffusion is scaled (larger scale = faster diffusion)
    K = 3e-3
    return np.array([da+diff_da*K, db+diff_db*K]).flatten()

# Solve the equations 
print("Solving equations...")
start = datetime.now()

solution = solve_ivp(dy, (0,DURATION), y0.flatten(), t_eval=TIME, method='DOP853', rtol=1e-5, atol=1e-5, first_step=1e-2)

print("Finished in", datetime.now()-start)
print(solution.message)

# Check that the integration converged
if not solution.success:
    print("ERROR: integration did not converge")
    exit()

# Reshape the solution to [t, compound, x, y]
solution = np.reshape(solution.y,[*SHAPE,DURATION]).transpose([3,0,1,2])

# Only the second compound is used for visualization
solution = solution[:,1]

# Animate the result
fig, ax = plt.subplots(figsize=(6,6))

img = ax.imshow(solution[0], vmin=0, vmax=7, cmap=colormap)
time_text = ax.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)

# Remove white spaces around the figure
plt.axis('off')
plt.tight_layout()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
ax.margins(0,0)

def animate(i):
    img.set_array(solution[i])
    time_text.set_text(f'Frame: {i+1}')
    return img, time_text

ani = animation.FuncAnimation(fig, animate, frames=range(DURATION), interval=50, blit=True, save_count=50)

print("Saving the animation...")
FFwriter = animation.FFMpegWriter(fps=20)
ani.save(FILENAME, writer = FFwriter)
print("Animation saved")

plt.show()