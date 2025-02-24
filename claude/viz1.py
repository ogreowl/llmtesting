import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Set up the figure with high resolution and quality
plt.rcParams['figure.figsize'] = [12, 10]
plt.rcParams['figure.dpi'] = 100
plt.style.use('dark_background')

# Create the figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Generate data for a complex 3D shape - a combination of multiple equations
theta = np.linspace(0, 2 * np.pi, 100)
z = np.linspace(-2, 2, 100)
theta, z = np.meshgrid(theta, z)

# Create a spiral torus
r = 1 + 0.3 * np.sin(5 * theta) + 0.2 * np.cos(3 * z)
x = r * np.sin(theta)
y = r * np.cos(theta)

# Create colormap based on the values
colors = np.zeros(z.shape)
for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        # Complex coloring based on position and radius
        colors[i, j] = 0.5 * np.sin(5 * theta[i, j]) + 0.5 * np.cos(3 * z[i, j]) + r[i, j]

# Plot the surface with a custom colormap
surf = ax.plot_surface(x, y, z, facecolors=cm.plasma(colors/np.max(colors)), 
                      antialiased=True, alpha=0.7)

# Add additional elements - scattered points to represent particles
num_particles = 300
particle_positions = np.random.rand(num_particles, 3) * 4 - 2
particle_colors = cm.cool(np.linspace(0, 1, num_particles))
ax.scatter(particle_positions[:, 0], particle_positions[:, 1], particle_positions[:, 2], 
           c=particle_colors, s=10, alpha=0.8)

# Add flow lines for visual complexity
line_count = 16
for i in range(line_count):
    # Create curved lines emanating from the center
    phi = 2 * np.pi * i / line_count
    radius = np.linspace(0, 2, 100)
    spiral_z = np.linspace(-1.5, 1.5, 100) * np.sin(phi * 2)
    line_x = radius * np.cos(phi + radius)
    line_y = radius * np.sin(phi + radius)
    ax.plot(line_x, line_y, spiral_z, color=cm.winter(i/line_count), linewidth=1.5, alpha=0.6)

# Add a central glowing sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
sphere_x = 0.5 * np.cos(u) * np.sin(v)
sphere_y = 0.5 * np.sin(u) * np.sin(v)
sphere_z = 0.5 * np.cos(v)
ax.plot_surface(sphere_x, sphere_y, sphere_z, color='yellow', alpha=0.3)

# Add vector field arrows for additional complexity
arrow_x, arrow_y, arrow_z = np.mgrid[-2:2:8j, -2:2:8j, -2:2:8j]
u = np.sin(arrow_y) * np.cos(arrow_z)
v = np.sin(arrow_x) * np.cos(arrow_z)
w = np.sin(arrow_x) * np.cos(arrow_y)
ax.quiver(arrow_x, arrow_y, arrow_z, u, v, w, length=0.3, normalize=True, color='cyan', alpha=0.4)

# Set view angle and labels
ax.view_init(elev=30, azim=45)
ax.set_xlabel('X Dimension', fontsize=12)
ax.set_ylabel('Y Dimension', fontsize=12)
ax.set_zlabel('Z Dimension', fontsize=12)
ax.set_title('Complex 3D Visualization with Matplotlib', fontsize=16, pad=20)

# Remove gridlines and background for cleaner look
ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Animation function to rotate the view
def animate(frame):
    ax.view_init(elev=30, azim=frame)
    return fig,

# Create animation - rotate 360 degrees
ani = FuncAnimation(fig, animate, frames=np.arange(0, 360, 2), interval=50, blit=True)

# Save the animation (requires ffmpeg or imagemagick)
# ani.save('complex_3d_visualization.gif', writer='pillow', fps=20, dpi=100)

# Show the static plot
plt.tight_layout()
plt.show()