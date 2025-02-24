
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_zlim(-2, 2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

num_particles = 100
particles = np.random.rand(num_particles, 3) * 2 - 1
particles[:, 0] *= 4
particles[:, 1] *= 4
particles[:, 2] *= 0.5

num_stars = 200
stars = np.random.uniform(-10, 10, (num_stars, 3))


def dynamic_surface(t):
    R = np.sqrt(X**2 + Y**2)
    return np.sin(R - t)


def dynamic_curve(t):
    phi = np.linspace(0, 2 * np.pi, 300)
    x_curve = 3 * np.cos(phi + t)
    y_curve = 3 * np.sin(phi + t)
    z_curve = np.sin(3 * phi + t)
    return x_curve, y_curve, z_curve


def dynamic_curve2(t):
    phi = np.linspace(0, 2 * np.pi, 200)
    x_curve = 2 * np.cos(2 * phi + t)
    y_curve = 2 * np.sin(3 * phi + t)
    z_curve = np.cos(4 * phi + t)
    return x_curve, y_curve, z_curve


def dynamic_spiral(t):
    phi = np.linspace(0, 4 * np.pi, 400)
    x_spiral = 2 * np.cos(phi + t)
    y_spiral = 2 * np.sin(phi + t)
    z_spiral = np.linspace(-1, 1, 400)
    return x_spiral, y_spiral, z_spiral


def draw_cube(t):
    vertices = np.array([[-1, -1, -1],
                         [ 1, -1, -1],
                         [ 1,  1, -1],
                         [-1,  1, -1],
                         [-1, -1,  1],
                         [ 1, -1,  1],
                         [ 1,  1,  1],
                         [-1,  1,  1]])
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),
             (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    R = np.array([[np.cos(t), -np.sin(t), 0],
                  [np.sin(t),  np.cos(t), 0],
                  [0,          0,         1]])
    rotated_vertices = vertices.dot(R.T)
    for edge in edges:
        pts = rotated_vertices[list(edge), :]
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color='orange', lw=1)


def update(frame):
    ax.clear()
    t = frame / 10.0
    ax.scatter(stars[:, 0], stars[:, 1], stars[:, 2], color='white', s=5, alpha=0.2)
    Z = dynamic_surface(t)
    ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.7, rstride=2, cstride=2, linewidth=0)
    x_curve, y_curve, z_curve = dynamic_curve(t)
    ax.plot(x_curve, y_curve, z_curve, color='black', lw=2)
    x_curve2, y_curve2, z_curve2 = dynamic_curve2(t)
    ax.plot(x_curve2, y_curve2, z_curve2, color='white', lw=1.5, linestyle='--')
    x_spiral, y_spiral, z_spiral = dynamic_spiral(t)
    ax.plot(x_spiral, y_spiral, z_spiral, color='magenta', lw=1)
    draw_cube(t)
    theta = t
    R_mat = np.array([[np.cos(theta), -np.sin(theta), 0],
                      [np.sin(theta),  np.cos(theta), 0],
                      [0,              0,             1]])
    rotated = particles.dot(R_mat.T)
    ax.scatter(rotated[:, 0], rotated[:, 1], rotated[:, 2], color='cyan', s=20)
    ax.scatter([0], [0], [0], color='yellow', s=100)
    ax.view_init(elev=30, azim=t * 20)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-2, 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_facecolor('xkcd:black')
    fig.patch.set_facecolor('xkcd:midnight blue')
    ax.set_title("3D Dynamic Visualization", color='white', fontsize=16)
    ax.text2D(0.05, 0.95, f"Time: {t:.2f}", transform=ax.transAxes, color='white', fontsize=12)
    return ax,


anim = FuncAnimation(fig, update, frames=300, interval=50, blit=False)


def on_key(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)


fig.canvas.mpl_connect('key_press_event', on_key)

fig.text(0.5, 0.01, 'Press "q" to quit', ha='center', color='white', fontsize=10)


def extra_info():
    print("3D Dynamic Visualization running. Press 'q' to quit.")
    print("Enjoy the show!")


extra_info()

if __name__ == '__main__':
    plt.show()
