import numpy as np
from scipy.integrate import solve_ivp


from matplotlib import pyplot as plt
from matplotlib import animation as animation

# solve differential equation
def D_conc(t, conc):
    filt = [1,-2,1]
    return np.convolve(conc, filt, mode='same')

x = np.linspace(0,10)
conc0 = np.where((x>5)&(x<5.5), 1, 0)

solution = solve_ivp(D_conc, [0,50], conc0, t_eval=np.linspace(0,50,200), max_step=1, method="Radau")

print(dir(solution))

integrals = np.sum(solution.y, axis=0)
plt.plot(integrals)
plt.show()


# animate result

fig, ax = plt.subplots()

line, = ax.plot(x, conc0)

def animate(i):
    line.set_ydata(solution.y[:,i])  # update the data.
    return line,


ani = animation.FuncAnimation(fig, animate, frames=range(200), interval=50, blit=True, save_count=50)

plt.show()