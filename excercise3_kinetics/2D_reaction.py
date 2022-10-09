import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import convolve2d

from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib.colors import ListedColormap

from datetime import datetime

from PIL import Image

# custom colormap
orange = np.array([207, 112, 64])/255
blue = np.array([167, 115, 250])/255
x = np.linspace(0,1,255)
colors = [orange*(1-i)+blue*(i) for i in x]
colormap = ListedColormap(colors)

SHAPE = (2,512,512)
y0 = np.zeros(SHAPE, dtype=float)
y0[0] = 1.
y0[1] = 1.

noise = Image.fromarray((np.random.rand(12,12)*255).astype(np.uint8), 'L').resize(SHAPE[1:], Image.BICUBIC)
noise = np.array(noise, dtype=float)/255
noise = noise**4

#plt.imshow(noise)
#plt.axis('off')
#plt.tight_layout()
#plt.show()

y0[1] = 0.3+0.7*noise

#y1 = np.arange(SHAPE[-1])
#y1, y2 = np.meshgrid(y1,y1)
#y0[0] += 0.2*np.sin(0.8*y1)*np.cos(0.2*y2)
#y0[0] += 0.3*np.sin(0.04*y1)*np.sin(0.1*y2)
#y0[0] *= (np.exp(-(y1-80)**2/20)*np.exp(-(y2-80)**2/20) + np.exp(-(y1-30)**2/10)*np.exp(-(y2-50)**2/20))
#y0[1] += convolve2d(np.random.randn(*SHAPE[1:])*0.01, np.array([[1,2,1],[2,4,2],[1,2,1]])/16, mode='same')
#
#plt.imshow(y0[0])
#plt.show()

def dy(t, y):
    alpha=0.5
    beta=-0.2
    gamma=0.1
    delta=-0.2

    y = np.reshape(y, SHAPE)

    a,b = y

    da = a*alpha + a*b*beta
    db = a*b*gamma + b*delta

    filt = [[0,1,0],[1,-4,1],[0,1,0]]
    peri = np.zeros(SHAPE[1:])
    peri[0,:] += 1.
    peri[:,1] += 1.
    peri[-1,:] += 1.
    peri[:,-1] += 1.

    K = 3e-3

    diff_da = convolve2d(a,filt,mode="same")*K
    diff_db = convolve2d(a,filt,mode="same")*K

    diff_da += peri*a*K
    diff_db += peri*b*K

    return np.array([da+diff_da, db+diff_db]).flatten()


T_MAX = 2000
FRAMES = 2000

print("Solving equations...")
start = datetime.now()
solution = solve_ivp(dy, (0,T_MAX), y0.flatten(), t_eval=np.linspace(0,T_MAX,FRAMES), method='DOP853', rtol=1e-5, atol=1e-5, first_step=1e-2)
print("Finished in", datetime.now()-start)
print("Solved!")
print(solution.message)

#reshape
solution = np.reshape(solution.y,[*SHAPE,FRAMES]).transpose([3,0,1,2])

solution = solution[:,1]

# animate result
fig, ax = plt.subplots(figsize=(6,6))

img = ax.imshow(solution[0], vmin=0, vmax=7, cmap=colormap)
time_text = ax.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)

plt.axis('off')
plt.tight_layout()

fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
ax.margins(0,0)

def animate(i):
    img.set_array(solution[i])  # update the data.
    time_text.set_text(f'Frame: {i+1}')
    return img, time_text


ani = animation.FuncAnimation(fig, animate, frames=range(FRAMES), interval=50, blit=True, save_count=50)

print("Saving the animation")
FFwriter = animation.FFMpegWriter(fps=20)
ani.save('animation2.mp4', writer = FFwriter)
print("Animation saved")

plt.show()