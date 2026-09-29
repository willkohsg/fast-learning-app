# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, math, os
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(S, exist_ok=True)

# --- Q11 sketch axes: 0 <= x <= 4pi, y from -1 to 7 -------------------
fig, ax = plt.subplots(figsize=(6.8, 4.3))
ax.set_xlim(-0.9, 4*math.pi + 0.9); ax.set_ylim(-3.4, 9.0)
ax.annotate("", xy=(4*math.pi + 0.8, 0), xytext=(-0.8, 0),
            arrowprops=dict(arrowstyle='->', lw=1.2, color='k'))
ax.annotate("", xy=(0, 8.7), xytext=(0, -3.1),
            arrowprops=dict(arrowstyle='->', lw=1.2, color='k'))
ax.text(4*math.pi + 0.95, 0, "x", fontsize=12, style='italic', va='center')
ax.text(0.18, 8.9, "y", fontsize=12, style='italic', ha='left')
ax.text(-0.25, -0.75, "0", fontsize=11, ha='right')
for xv, lab in [(math.pi, r"$\pi$"), (2*math.pi, r"$2\pi$"),
                (3*math.pi, r"$3\pi$"), (4*math.pi, r"$4\pi$")]:
    ax.plot([xv, xv], [-0.28, 0.28], color='k', lw=1.1)
    ax.text(xv, -0.75, lab, ha='center', va='top', fontsize=12)
for yv in (7, -1):
    ax.plot([-0.22, 0.22], [yv, yv], color='k', lw=1.1)
    ax.text(-0.35, yv, str(yv).replace("-", "−"),
            ha='right', va='center', fontsize=11)
ax.axis('off')
fig.savefig(os.path.join(S, "q11axes.png"), dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close(fig)

# --- Q9 graph paper (2 mm grid) ---------------------------------------
fig, ax = plt.subplots(figsize=(6.9, 8.4))
W, H = 26, 32
ax.set_xlim(0, W); ax.set_ylim(0, H)
for i in np.arange(0, W + .001, .2): ax.plot([i, i], [0, H], color='0.72', lw=.28)
for j in np.arange(0, H + .001, .2): ax.plot([0, W], [j, j], color='0.72', lw=.28)
for i in np.arange(0, W + .001, 1.):  ax.plot([i, i], [0, H], color='0.42', lw=.7)
for j in np.arange(0, H + .001, 1.):  ax.plot([0, W], [j, j], color='0.42', lw=.7)
ax.set_aspect('equal'); ax.axis('off')
fig.savefig(os.path.join(S, "graphpaper.png"), dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close(fig)
print("diagrams done")
