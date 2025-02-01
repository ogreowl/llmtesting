import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

plt.style.use('dark_background')
num_nodes = 50
nodes = []
for i in range(num_nodes):
    t = random.randint(1000, 2000)
    pos = np.random.rand(2) * 10
    nodes.append({'id': i, 'time': t, 'pos': pos})
nodes.sort(key=lambda n: n['time'])
for i, node in enumerate(nodes):
    node['id'] = i

edges = []
for i in range(1, num_nodes):
    base = random.randint(0, i - 1)
    edges.append({'source': nodes[base]['id'], 'target': nodes[i]['id'], 'time': nodes[i]['time']})
    for j in range(i):
        if j != base and random.random() < 0.35:
            edges.append({'source': nodes[j]['id'], 'target': nodes[i]['id'], 'time': nodes[i]['time']})

start_year = nodes[0]['time']
end_year = nodes[-1]['time'] + 150
frames = 500
times = np.linspace(start_year, end_year, frames)
growth_duration = 40
ripple_period = 50

cmap = plt.cm.inferno
norm = plt.Normalize(start_year, end_year)
for node in nodes:
    node['color'] = cmap(norm(node['time']))

fig, ax = plt.subplots(figsize=(8, 8))

def dynamic_background(t):
    x = np.linspace(0, 10, 300)
    y = np.linspace(0, 10, 300)
    X, Y = np.meshgrid(x, y)
    phase = (t - start_year) / (end_year - start_year) * 2 * np.pi
    return np.sin(3 * X + phase) * np.cos(3 * Y - phase)

def update(frame):
    t = times[frame]
    ax.clear()
    zoom = 1 + 0.5 * np.sin(frame / 50)
    mid = 5
    lim = 5 * zoom
    ax.set_xlim(mid - lim, mid + lim)
    ax.set_ylim(mid - lim, mid + lim)
    bg = dynamic_background(t)
    ax.imshow(bg, extent=[0, 10, 0, 10], origin='lower', cmap='cool', alpha=0.15, zorder=0)
    ax.axis('off')
    
    for edge in edges:
        if t < edge['time']:
            continue
        dt = t - edge['time']
        frac = min(dt / growth_duration, 1)
        s = nodes[edge['source']]['pos']
        d = nodes[edge['target']]['pos']
        ax.plot([s[0], s[0] + frac * (d[0] - s[0])],
                [s[1], s[1] + frac * (d[1] - s[1])],
                color='cyan', linewidth=2, alpha=0.7)
        particle_frac = (dt % growth_duration) / growth_duration
        p_x = s[0] + particle_frac * (d[0] - s[0])
        p_y = s[1] + particle_frac * (d[1] - s[1])
        ax.scatter(p_x, p_y, s=30, color='white', alpha=0.9, zorder=3)
    
    for node in nodes:
        if t < node['time']:
            continue
        ax.scatter(node['pos'][0], node['pos'][1], s=150, color=node['color'],
                   edgecolors='white', linewidths=1.2, zorder=4)
        age = t - node['time']
        ripple_phase = (age % ripple_period) / ripple_period
        ripple_radius = 0.5 + 2 * ripple_phase
        circle = plt.Circle(node['pos'], ripple_radius, color=node['color'],
                            fill=False, lw=2, alpha=1 - ripple_phase, zorder=2)
        ax.add_patch(circle)
    
    ax.text(0.5, 0.95, f'Year: {int(t)}', transform=ax.transAxes,
            ha='center', va='center', fontsize=20, color='w')

ani = animation.FuncAnimation(fig, update, frames=frames, interval=50)
plt.show()
