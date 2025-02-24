import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ParticleSystem:
    def __init__(self, num_particles, dt, boundary, G, damping, trail_length):
        self.num_particles = num_particles
        self.dt = dt
        self.boundary = boundary
        self.G = G
        self.damping = damping
        self.epsilon = 0.1
        self.trail_length = trail_length
        self.positions = np.random.uniform(-boundary / 2, boundary / 2, (num_particles, 2))
        self.velocities = np.random.uniform(-1, 1, (num_particles, 2))
        self.trails = np.repeat(self.positions[:, None, :], trail_length, axis=1)

    def update(self, t):
        a1 = np.array([8 * np.cos(t * 0.5), 6 * np.sin(t * 0.5)])
        a2 = np.array([-8 * np.cos(t * 0.5), -6 * np.sin(t * 0.5)])
        d1 = a1 - self.positions
        d2 = a2 - self.positions
        dist1 = np.sum(d1 ** 2, axis=1) + self.epsilon
        dist2 = np.sum(d2 ** 2, axis=1) + self.epsilon
        f1 = self.G * d1 / dist1[:, None]
        f2 = -self.G * d2 / dist2[:, None]  # repulsive force from second attractor
        force = f1 + f2

        self.velocities += force * self.dt
        self.positions += self.velocities * self.dt

        for i in range(2):
            mask = self.positions[:, i] < -self.boundary
            self.positions[mask, i] = -self.boundary
            self.velocities[mask, i] *= -1
            mask = self.positions[:, i] > self.boundary
            self.positions[mask, i] = self.boundary
            self.velocities[mask, i] *= -1

        self.velocities *= self.damping
        self.trails[:, :-1, :] = self.trails[:, 1:, :]
        self.trails[:, -1, :] = self.positions
        return a1, a2, self.positions, self.velocities, self.trails

def main():
    np.random.seed(42)
    num_particles = 300
    dt = 0.05
    boundary = 20
    G = 50
    damping = 0.99
    trail_length = 20
    ps = ParticleSystem(num_particles, dt, boundary, G, damping, trail_length)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8))
    scat = ax.scatter(ps.positions[:, 0], ps.positions[:, 1], s=10, c='cyan',
                      edgecolors='none', alpha=0.8, cmap='viridis')
    a1_plot, = ax.plot([], [], 'yo', markersize=10)
    a2_plot, = ax.plot([], [], 'mo', markersize=10)

    trail_lines = []
    for i in range(num_particles):
        line, = ax.plot(ps.trails[i, :, 0], ps.trails[i, :, 1],
                        lw=1, color='white', alpha=0.3)
        trail_lines.append(line)

    u = np.linspace(0, 2 * np.pi, 400)
    lissajous_line, = ax.plot(10 * np.sin(3 * u), 10 * np.sin(4 * u),
                              color='magenta', lw=2, alpha=0.5)

    time_text = ax.text(-boundary + 1, boundary - 2, '', color='white', fontsize=12)

    ax.set_xlim(-boundary, boundary)
    ax.set_ylim(-boundary, boundary)
    ax.set_aspect('equal')
    ax.axis('off')

    def animate(frame):
        t = frame * dt
        a1, a2, positions, velocities, trails = ps.update(t)
        scat.set_offsets(positions)
        speed = np.linalg.norm(velocities, axis=1)
        scat.set_array(speed)

        a1_plot.set_data([a1[0]], [a1[1]])
        a2_plot.set_data([a2[0]], [a2[1]])
        for i, line in enumerate(trail_lines):
            line.set_data(trails[i, :, 0], trails[i, :, 1])

        x_liss = 10 * np.sin(3 * u + t * 0.5)
        y_liss = 10 * np.sin(4 * u)
        lissajous_line.set_data(x_liss, y_liss)

        time_text.set_text(f"Time = {t:.2f}")
        return [scat, a1_plot, a2_plot, lissajous_line, time_text] + trail_lines

    anim = FuncAnimation(fig, animate, frames=1000, interval=30, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
