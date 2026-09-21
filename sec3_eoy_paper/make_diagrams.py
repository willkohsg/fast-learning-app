import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, math, os
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(S, exist_ok=True)

# ---------- 1. PLAQUE ----------
fig, ax = plt.subplots(figsize=(3.6, 4.2))
q = 2.0; p = 2.6
h = math.sqrt(3)/2*q
# rectangle
ax.plot([0,0,q,q], [p,0,0,p], color='k', lw=1.4)
# triangle
ax.plot([0, q/2, q], [p, p+h, p], color='k', lw=1.4)
# dashed top of rectangle
ax.plot([0,q],[p,p], color='k', lw=1.1, ls=(0,(4,3)))
# p dimension arrow (right side)
xo = q + 0.28
ax.annotate("", xy=(xo, 0), xytext=(xo, p), arrowprops=dict(arrowstyle='<->', lw=1.1, color='k'))
ax.text(xo + 0.12, p/2, "p m", va='center', ha='left', fontsize=12, style='italic')
# q dimension arrow (bottom)
yo = -0.32
ax.annotate("", xy=(0, yo), xytext=(q, yo), arrowprops=dict(arrowstyle='<->', lw=1.1, color='k'))
ax.text(q/2, yo - 0.24, "q m", va='top', ha='center', fontsize=12, style='italic')
ax.set_xlim(-0.5, q+1.15); ax.set_ylim(-0.95, p+h+0.3)
ax.set_aspect('equal'); ax.axis('off')
fig.savefig(os.path.join(S,"plaque.png"), dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

# ---------- 2. TRIG AXES ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4))
ax.set_xlim(-0.55, 2*math.pi + 0.55); ax.set_ylim(-13.5, 6.5)
# axes
ax.annotate("", xy=(2*math.pi + 0.5, 0), xytext=(-0.5, 0), arrowprops=dict(arrowstyle='->', lw=1.2, color='k'))
ax.annotate("", xy=(0, 6.2), xytext=(0, -13.2), arrowprops=dict(arrowstyle='->', lw=1.2, color='k'))
ax.text(2*math.pi + 0.62, 0, "x", fontsize=12, style='italic', va='center')
ax.text(0.12, 6.4, "y", fontsize=12, style='italic', ha='left')
ax.text(-0.18, -0.85, "0", fontsize=11, ha='right')
# x ticks
xt = [(math.pi/2, r"$\frac{\pi}{2}$"), (math.pi, r"$\pi$"),
      (3*math.pi/2, r"$\frac{3\pi}{2}$"), (2*math.pi, r"$2\pi$")]
for xv, lab in xt:
    ax.plot([xv, xv], [-0.45, 0.45], color='k', lw=1.1)
    ax.text(xv, -1.3, lab, ha='center', va='top', fontsize=12)
# y ticks
for yv in (4, -10):
    ax.plot([-0.22, 0.22], [yv, yv], color='k', lw=1.1)
    ax.text(-0.35, yv, str(yv).replace("-", "\u2212"), ha="right", va="center", fontsize=11)
ax.axis('off')
fig.savefig(os.path.join(S,"trigaxes.png"), dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

# ---------- 3. GRAPH PAPER (2 mm grid) ----------
fig, ax = plt.subplots(figsize=(6.9, 8.6))
W, H = 26, 34   # in units of 5 small squares -> major cm lines
ax.set_xlim(0, W); ax.set_ylim(0, H)
for i in np.arange(0, W + 0.001, 0.2):
    ax.plot([i, i], [0, H], color='0.72', lw=0.28)
for j in np.arange(0, H + 0.001, 0.2):
    ax.plot([0, W], [j, j], color='0.72', lw=0.28)
for i in np.arange(0, W + 0.001, 1.0):
    ax.plot([i, i], [0, H], color='0.42', lw=0.7)
for j in np.arange(0, H + 0.001, 1.0):
    ax.plot([0, W], [j, j], color='0.42', lw=0.7)
ax.set_aspect('equal'); ax.axis('off')
fig.savefig(os.path.join(S,"graphpaper.png"), dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print("diagrams done")
