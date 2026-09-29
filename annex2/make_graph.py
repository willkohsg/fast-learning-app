# -*- coding: utf-8 -*-
"""Annex A (Set 2) - the drawn straight-line graph answering Q9(a).

Power law: y = a x^b  ->  lg y = lg a + b lg x, so lg y against lg x is linear
with gradient b and vertical intercept lg a. The five points lie on
lg y = 0.477 + 0.5 lg x, i.e. y = 3 sqrt(x).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

BLACK, BLUE, RED = "#14181d", "#1F4E9C", "#C00000"
GRID_MINOR, GRID_MAJOR = "#f0c9cd", "#d98f97"      # exam graph paper pink

XMAX, YMAX = 2.2, 1.6
XSTEP, YSTEP = 0.2, 0.2
XMINOR, YMINOR = 0.04, 0.04
CELL = 44.0                                        # px per major interval
L, T = 92.0, 30.0                                  # plot-area origin on the canvas
W = CELL * (XMAX / XSTEP)
H = CELL * (YMAX / YSTEP)

DATA = [(0.0, 0.477), (0.602, 0.778), (1.204, 1.079), (1.556, 1.255), (2.000, 1.477)]
A, B = 0.477, 0.5                                   # lg y = lg a + b lg x


def px(x):
    return L + x / XMAX * W


def py(y):
    return T + H - y / YMAX * H


def fmt(v, dp):
    return ("%%.%df" % dp) % v


o = []
add = o.append
add('<svg xmlns="http://www.w3.org/2000/svg" width="%g" height="%g" '
    'viewBox="0 0 %g %g" font-family="Liberation Serif, Georgia, serif">'
    % (L + W + 40, T + H + 92, L + W + 40, T + H + 92))
add('<rect width="100%" height="100%" fill="#ffffff"/>')

# --- graph paper -----------------------------------------------------------
def rule(xstep, ystep, colour, width):
    for i in range(int(round(XMAX / xstep)) + 1):
        x = px(i * xstep)
        add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%g"/>'
            % (x, T, x, T + H, colour, width))
    for i in range(int(round(YMAX / ystep)) + 1):
        y = py(i * ystep)
        add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%g"/>'
            % (L, y, L + W, y, colour, width))

rule(XMINOR, YMINOR, GRID_MINOR, 0.45)
rule(XSTEP, YSTEP, GRID_MAJOR, 0.9)

# --- axes ------------------------------------------------------------------
add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.6"/>'
    % (L, T + H, L + W, T + H, BLACK, ))
add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.6"/>'
    % (L, T, L, T + H, BLACK))

for i in range(int(round(XMAX / XSTEP)) + 1):
    v = i * XSTEP
    x = px(v)
    add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.4"/>'
        % (x, T + H, x, T + H + 5, BLACK))
    add('<text x="%.2f" y="%.2f" font-size="11" fill="%s" text-anchor="middle">%s</text>'
        % (x, T + H + 18, BLACK, fmt(v, 1)))
for i in range(int(round(YMAX / YSTEP)) + 1):
    v = i * YSTEP
    y = py(v)
    add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.4"/>'
        % (L - 5, y, L, y, BLACK))
    add('<text x="%.2f" y="%.2f" font-size="11" fill="%s" text-anchor="end">%s</text>'
        % (L - 9, y + 3.6, BLACK, fmt(v, 1)))

# axis titles, written as the fractions the syllabus expects
def frac_label(x, y, num, den, colour, size=13):
    half = size * 0.34
    add('<g font-size="%g" fill="%s" text-anchor="middle">'
        '<text x="%.2f" y="%.2f">%s</text>'
        '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.1"/>'
        '<text x="%.2f" y="%.2f" font-style="italic">%s</text></g>'
        % (size, colour, x, y - half - 2, num,
           x - size * 0.42, y, x + size * 0.42, y, colour,
           x, y + size + half - 3, den))

add('<text x="%.2f" y="%.2f" font-size="14" fill="%s" text-anchor="middle">lg&#8201;<tspan font-style="italic">x</tspan></text>' % (px(XMAX/2), T + H + 48, BLACK))
add('<text x="%.2f" y="%.2f" font-size="14" fill="%s" text-anchor="middle">lg&#8201;<tspan font-style="italic">y</tspan></text>' % (L - 48, T + H/2, BLACK))

# --- the line of best fit (blue ink) ---------------------------------------
add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="2"/>'
    % (px(0), py(A), px(XMAX), py(A + B * XMAX), BLUE))

# plotted points as exam crosses
for x, y in DATA:
    cx, cy = px(x), py(y)
    add('<g stroke="%s" stroke-width="1.8">'
        '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>'
        '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/></g>'
        % (BLUE, cx - 5, cy - 5, cx + 5, cy + 5, cx - 5, cy + 5, cx + 5, cy - 5))

# --- gradient triangle and intercept (red ink) -----------------------------
x1, x2 = 0.0, 2.0
y1, y2 = A + B * x1, A + B * x2
add('<path d="M %.2f %.2f L %.2f %.2f L %.2f %.2f" fill="none" stroke="%s" '
    'stroke-width="1.3" stroke-dasharray="5 3"/>'
    % (px(x1), py(y1), px(x2), py(y1), px(x2), py(y2), RED))
add('<text x="%.2f" y="%.2f" font-size="11.5" fill="%s" text-anchor="middle">%s</text>'
    % ((px(x1) + px(x2)) / 2, py(y1) + 16, RED, "2.00"))
add('<text x="%.2f" y="%.2f" font-size="11.5" fill="%s" text-anchor="start">%s</text>'
    % (px(x2) + 7, (py(y1) + py(y2)) / 2 + 4, RED, "1.00"))

# intercept marker
add('<circle cx="%.2f" cy="%.2f" r="4.2" fill="none" stroke="%s" stroke-width="1.8"/>'
    % (px(0), py(A), RED))
add('<text x="%.2f" y="%.2f" font-size="11.5" fill="%s">%s</text>'
    % (px(0) + 10, py(A) + 17, RED, "intercept = lg a = 0.477"))

add('</svg>')

out = os.path.join(HERE, "q9a_graph.svg")
open(out, "w").write("\n".join(o))
print("wrote", out)
