import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 500
r_particles = np.random.uniform(0.1, 10, N)
theta_particles = np.random.uniform(0, 2*np.pi, N)
colors = np.random.rand(N)
x_particles = r_particles * np.cos(theta_particles)
y_particles = r_particles * np.sin(theta_particles)

fig, ax = plt.subplots(figsize=(8, 8))
scat = ax.scatter(x_particles, y_particles, c=colors, cmap='hsv', s=10, animated=True)
theta_line = np.linspace(0, 10*np.pi, 1000)
line, = ax.plot([], [], lw=2, color='white')
ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_facecolor('black')
fig.patch.set_facecolor('black')
ax.axis('off')

def update(frame):
    global theta_particles
    theta_particles += 0.02 / (r_particles + 0.1)
    x_particles = r_particles * np.cos(theta_particles)
    y_particles = r_particles * np.sin(theta_particles)
    scat.set_offsets(np.c_[x_particles, y_particles])
    
    t = frame / 10.0
    a, b, c = 0.2, 5, 10
    r_line = a * theta_line + b * np.sin(c * theta_line + t)
    x_line = r_line * np.cos(theta_line)
    y_line = r_line * np.sin(theta_line)
    line.set_data(x_line, y_line)
    return scat, line

ani = FuncAnimation(fig, update, frames=np.arange(0, 1000), interval=30, blit=True)
plt.show()
