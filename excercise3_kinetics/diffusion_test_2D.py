import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import convolve2d

from matplotlib import pyplot as plt
from matplotlib import animation as animation

# constants
SHAPE = (256,256)
FRAMES = 500
T_MAX = 50

conc0 = np.zeros(SHAPE, dtype=float)
conc0[120:137,120:137] = 1.

def D_conc(t, conc):
    # TODO: handle the edges
    conc = np.reshape(conc, SHAPE)
    filt = [[0,1,0],[1,-4,1],[0,1,0]]
    Dconc = convolve2d(conc, filt, mode='same')
    return Dconc.flatten()

# solve differential equation
solution = solve_ivp(D_conc, [0,T_MAX], conc0.flatten(), t_eval=np.linspace(0,T_MAX,FRAMES), max_step=1, method="BDF")

solution = np.reshape(solution.y,[*SHAPE,FRAMES]).transpose([2,0,1])

# animate result
fig, ax = plt.subplots()

img = ax.imshow(solution[0])

def animate(i):
    img.set_array(solution[i])  # update the data.
    return img,


ani = animation.FuncAnimation(fig, animate, frames=range(FRAMES), interval=50, blit=True, save_count=50)

plt.show()