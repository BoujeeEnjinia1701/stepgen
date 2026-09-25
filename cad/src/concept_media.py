"""StepGen concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

StepGen is a walking-treadmill vehicle: the rider stands upright and walks on a short
free-running belt between the wheels, a belt-speed sensor sets the assist of a rear hub
motor, and a shared SwapCell pack supplies the energy.

Axes: X is the direction of travel (front is +X), Y is across the vehicle, Z is up.
Rear axle at X = 0, ground at Z = 0. Units mm.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Torus, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, ACCENT, INK
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Main dimensions (mm). Proposed values, awaiting Amish (see docs/02-concept.md).
WHEEL_R = 247.0            # 20 x 1.75 in (ETRTO 406) tire, outside diameter about 494 mm
TIRE_R = 22.0              # tire section radius
ROLL_R = 25.0              # belt end roller radius (50 mm crowned rollers)
RR_X, FR_X = 320.0, 1370.0 # rear and front belt roller centres: 1.05 m apart
DECK_Z = 240.0             # top of the belt above the ground
ROLL_Z = DECK_Z - ROLL_R   # roller centre height
BELT_W = 400.0             # belt width
RAIL_Y = 235.0             # deck side rail centre line
RAIL_W, RAIL_H = 25.0, 50.0
RAIL_X0, RAIL_X1 = 270.0, 1420.0
HEAD_ANG = 70.0            # head tube angle from horizontal
HEAD_BOT = (1710.0, 640.0) # bottom of the head tube (x, z)
BAR = (1400.0, 1230.0)     # handlebar centre (about 0.99 m above the belt)

s_dir = (-math.cos(math.radians(HEAD_ANG)), math.sin(math.radians(HEAD_ANG)))  # steering axis, up and back
FRONT_X = HEAD_BOT[0] - s_dir[0] * (HEAD_BOT[1] - WHEEL_R) / s_dir[1]            # front axle on the steering axis
HEAD_TOP = (HEAD_BOT[0] + s_dir[0] * 150, HEAD_BOT[1] + s_dir[1] * 150)
COL_TOP_Z = BAR[1]
COL_TOP = (HEAD_BOT[0] + s_dir[0] * (COL_TOP_Z - HEAD_BOT[1]) / s_dir[1], COL_TOP_Z)

TYRE = "#1F2937"


def tube3(a, b, r):
    """Round tube between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def box_x(x0, x1, y, z, w, h):
    return Pos((x0 + x1) / 2, y, z) * Box(x1 - x0, w, h)


def tyre_rim(cx):
    tyre = Pos(cx, 0, WHEEL_R) * Rot(90, 0, 0) * Torus(WHEEL_R - TIRE_R, TIRE_R)
    rim = Pos(cx, 0, WHEEL_R) * Rot(90, 0, 0) * (Cylinder(WHEEL_R - 2 * TIRE_R, 20) - Cylinder(WHEEL_R - 2 * TIRE_R - 14, 22))
    spokes = None
    for k in range(12):
        t = math.radians(k * 30 + 15)
        s = tube3((cx, 0, WHEEL_R), (cx + (WHEEL_R - 55) * math.cos(t), 0, WHEEL_R + (WHEEL_R - 55) * math.sin(t)), 2.0)
        spokes = s if spokes is None else spokes + s
    return tyre + rim + spokes


# ---------------- 1 Main frame ----------------
rails = (box_x(RAIL_X0, RAIL_X1, -RAIL_Y, ROLL_Z - 15, RAIL_W, RAIL_H)
         + box_x(RAIL_X0, RAIL_X1, RAIL_Y, ROLL_Z - 15, RAIL_W, RAIL_H))
cross = None
for x in (RAIL_X0 + 15, 845.0, RAIL_X1 - 15):
    c = Pos(x, 0, ROLL_Z - 55) * Box(30, 2 * RAIL_Y, 25)
    cross = c if cross is None else cross + c
rear_stays = (tube3((RAIL_X0, -RAIL_Y, ROLL_Z - 15), (0, -70, WHEEL_R), 11)
              + tube3((RAIL_X0, RAIL_Y, ROLL_Z - 15), (0, 70, WHEEL_R), 11)
              + tube3((RAIL_X0 + 180, -RAIL_Y, ROLL_Z + 5), (0, -70, WHEEL_R + 10), 9)
              + tube3((RAIL_X0 + 180, RAIL_Y, ROLL_Z + 5), (0, 70, WHEEL_R + 10), 9))
dropouts = Pos(0, -70, WHEEL_R) * Box(40, 6, 40) + Pos(0, 70, WHEEL_R) * Box(40, 6, 40)
nose = (tube3((RAIL_X1, -RAIL_Y, ROLL_Z - 15), (RAIL_X1 + 60, -40, ROLL_Z - 5), 14)
        + tube3((RAIL_X1, RAIL_Y, ROLL_Z - 15), (RAIL_X1 + 60, 40, ROLL_Z - 5), 14)
        + Pos(RAIL_X1 + 60, 0, ROLL_Z - 5) * Box(40, 110, 30))
DT_LO = (RAIL_X1 + 60, 0.0, ROLL_Z - 5)
DT_HI = (HEAD_BOT[0], 0.0, HEAD_BOT[1])
down_tube = tube3(DT_LO, DT_HI, 22)
head_tube = tube3((HEAD_BOT[0], 0, HEAD_BOT[1]), (HEAD_TOP[0], 0, HEAD_TOP[1]), 22)
frame = rails + cross + rear_stays + dropouts + nose + down_tube + head_tube
deck_frame = rails + cross + rear_stays + dropouts + nose

# ---------------- 2 Belt and end rollers ----------------
roller = lambda x: Pos(x, 0, ROLL_Z) * Rot(90, 0, 0) * Cylinder(ROLL_R, BELT_W + 30)
axles = lambda x: Pos(x, 0, ROLL_Z) * Rot(90, 0, 0) * Cylinder(8, 2 * RAIL_Y + 40)
belt_top = box_x(RR_X, FR_X, 0, DECK_Z - 1.5, BELT_W, 3)
belt_bot = box_x(RR_X, FR_X, 0, ROLL_Z - ROLL_R + 1.5, BELT_W, 3)
wrap = lambda x: Pos(x, 0, ROLL_Z) * Rot(90, 0, 0) * (Cylinder(ROLL_R + 3, BELT_W) - Cylinder(ROLL_R, BELT_W + 2))
belt = belt_top + belt_bot + wrap(RR_X) + wrap(FR_X)
end_rollers = roller(RR_X) + roller(FR_X) + axles(RR_X) + axles(FR_X)

# ---------------- 3 Roller bed under the top run ----------------
bed = None
n_bed = 14
for k in range(n_bed):
    x = RR_X + 70 + k * (FR_X - RR_X - 140) / (n_bed - 1)
    r = Pos(x, 0, DECK_Z - 3 - 15) * Rot(90, 0, 0) * Cylinder(15, BELT_W - 10)
    bed = r if bed is None else bed + r
bed_rails = box_x(RR_X + 50, FR_X - 50, -BELT_W / 2 + 5, DECK_Z - 18, 10, 30) + box_x(RR_X + 50, FR_X - 50, BELT_W / 2 - 5, DECK_Z - 18, 10, 30)
roller_bed = bed + bed_rails

# ---------------- 4 Anti-reverse clutch and belt drag (rear roller, +Y end) ----------------
clutch = Pos(RR_X, RAIL_Y + 45, ROLL_Z) * Rot(90, 0, 0) * Cylinder(38, 45)

# ---------------- 5 Belt speed sensor (front roller, -Y end) ----------------
sensor = (Pos(FR_X, -RAIL_Y - 30, ROLL_Z) * Rot(90, 0, 0) * Cylinder(30, 8)
          + Pos(FR_X, -RAIL_Y - 45, ROLL_Z + 40) * Box(30, 20, 30))

# ---------------- 6 Rear wheel with geared hub motor ----------------
rear_motor = Pos(0, 0, WHEEL_R) * Rot(90, 0, 0) * Cylinder(85, 80)
rear_tyre = tyre_rim(0.0)

# ---------------- 7 Front wheel, fork and headset ----------------
fork = (tube3((FRONT_X, -55, WHEEL_R), (HEAD_BOT[0], -55, HEAD_BOT[1] - 20), 11)
        + tube3((FRONT_X, 55, WHEEL_R), (HEAD_BOT[0], 55, HEAD_BOT[1] - 20), 11)
        + Pos(HEAD_BOT[0], 0, HEAD_BOT[1] - 15) * Box(45, 130, 25)
        + Pos(FRONT_X, 0, WHEEL_R) * Rot(90, 0, 0) * Cylinder(30, 100))
front_tyre = tyre_rim(FRONT_X)

# ---------------- 8 Steering column, handlebar and grips ----------------
column = tube3((HEAD_TOP[0], 0, HEAD_TOP[1]), (COL_TOP[0], 0, COL_TOP[1]), 16)
stem = tube3((COL_TOP[0], 0, COL_TOP[1]), (BAR[0], 0, BAR[1]), 15)
bars = (tube3((BAR[0], -270, BAR[1]), (BAR[0], 270, BAR[1]), 11)
        + tube3((BAR[0], -270, BAR[1]), (BAR[0] - 60, -290, BAR[1] - 10), 16)
        + tube3((BAR[0], 270, BAR[1]), (BAR[0] - 60, 290, BAR[1] - 10), 16))
steering = column + stem + bars

# ---------------- 9 Brakes: disc rotors, calipers, levers with motor cut-off ----------------
rot_r = Pos(0, -95, WHEEL_R) * Rot(90, 0, 0) * (Cylinder(80, 3) - Cylinder(30, 4))
rot_f = Pos(FRONT_X, -70, WHEEL_R) * Rot(90, 0, 0) * (Cylinder(80, 3) - Cylinder(25, 4))
cal_r = Pos(55, -95, WHEEL_R + 55) * Box(45, 25, 35)
cal_f = Pos(FRONT_X - 55, -70, WHEEL_R + 55) * Box(45, 25, 35)
levers = (tube3((BAR[0] - 20, -200, BAR[1] + 5), (BAR[0] - 90, -240, BAR[1] - 15), 6)
          + tube3((BAR[0] - 20, 200, BAR[1] + 5), (BAR[0] - 90, 240, BAR[1] - 15), 6))
brakes_rear = rot_r + cal_r
brakes_front = rot_f + cal_f

# ---------------- 10 SwapCell receiver cradle and host adapter, on the down tube ----------------
dt = (DT_HI[0] - DT_LO[0], DT_HI[2] - DT_LO[2])
dt_len = math.hypot(*dt)
ux, uz = dt[0] / dt_len, dt[1] / dt_len
nx, nz = -uz, ux                                  # normal on the upper, rear side of the down tube
dt_ang = math.degrees(math.atan2(dt[1], dt[0]))


def on_dt(t, off):
    return (DT_LO[0] + ux * t + nx * off, DT_LO[2] + uz * t + nz * off)


c = on_dt(dt_len * 0.55, 22 + 8)
cradle = Pos(c[0], 0, c[1]) * Rot(0, -dt_ang, 0) * (Box(370, 104, 16) + Pos(-180, 0, 30) * Box(12, 104, 60))
h = on_dt(dt_len * 0.55 + 205, 22 + 30)
adapter = Pos(h[0], 0, h[1]) * Rot(0, -dt_ang, 0) * Box(40, 70, 35)
cradle = cradle + adapter

# ---------------- 11 SwapCell pack (340 x 90 x 80 mm) ----------------
p = on_dt(dt_len * 0.55, 22 + 16 + 40)
pack = Pos(p[0], 0, p[1]) * Rot(0, -dt_ang, 0) * Box(340, 90, 80)

# ---------------- 12 Controller and walking logic board, under the down tube ----------------
q = on_dt(dt_len * 0.25, -(22 + 25))
controller = Pos(q[0], 0, q[1]) * Rot(0, -dt_ang, 0) * Box(150, 70, 40)

# ---------------- 13 Display, level selector and lanyard stop switch ----------------
display = (Pos(BAR[0] + 10, 0, BAR[1] + 45) * Rot(0, -20, 0) * Box(25, 110, 70)
           + Pos(BAR[0] - 20, 140, BAR[1] + 10) * Box(35, 30, 30)            # level selector
           + Pos(BAR[0] - 20, -140, BAR[1] + 12) * Rot(0, 0, 0) * Cylinder(16, 30))  # lanyard stop switch

# ---------------- 14 Guards: heel guard over the rear tyre, roller covers, side boards, toe guard ----------------
heel = Pos(0, 0, WHEEL_R) * Rot(90, 0, 0) * (Cylinder(WHEEL_R + 45, 70) - Cylinder(WHEEL_R + 40, 72))
heel = heel & (Pos(WHEEL_R / 2 + 40, 0, WHEEL_R + 200) * Box(WHEEL_R + 110, 100, 400))
heel = heel + Pos(RAIL_X0 - 5, 0, DECK_Z + 60) * Box(10, BELT_W + 60, 120)        # heel stop plate at the belt's rear end
side_boards = box_x(RAIL_X0, RAIL_X1, -RAIL_Y, DECK_Z + 3, 70, 6) + box_x(RAIL_X0, RAIL_X1, RAIL_Y, DECK_Z + 3, 70, 6)
covers = (Pos(RR_X, 0, ROLL_Z) * Rot(90, 0, 0) * (Cylinder(ROLL_R + 20, BELT_W + 40) - Cylinder(ROLL_R + 16, BELT_W + 42)))
covers = covers & (Pos(RR_X - 60, 0, ROLL_Z) * Box(120, BELT_W + 60, 200))
covers_f = (Pos(FR_X, 0, ROLL_Z) * Rot(90, 0, 0) * (Cylinder(ROLL_R + 20, BELT_W + 40) - Cylinder(ROLL_R + 16, BELT_W + 42)))
covers_f = covers_f & (Pos(FR_X + 60, 0, ROLL_Z) * Box(120, BELT_W + 60, 200))
toe = Pos(FR_X + 35, 0, DECK_Z + 45) * Rot(0, -20, 0) * Box(8, BELT_W + 60, 90)
guards = heel + side_boards + covers + covers_f + toe

# ---------------- 15 Wiring harness with fuse ----------------
w0 = (q[0] - 60, -45, q[1] - 20)
w1 = (5, -60, WHEEL_R + 30)
harness_up = (tube3((HEAD_TOP[0], -22, HEAD_TOP[1]), (COL_TOP[0], -22, COL_TOP[1] - 20), 5)
              + tube3((COL_TOP[0], -22, COL_TOP[1] - 20), (BAR[0] + 5, -60, BAR[1] - 10), 5)
              + tube3(w0, (HEAD_BOT[0] - 40, -40, HEAD_BOT[1] - 30), 5)
              + tube3((HEAD_BOT[0] - 40, -40, HEAD_BOT[1] - 30), (HEAD_TOP[0], -22, HEAD_TOP[1]), 5))
harness = (tube3(w0, (RAIL_X1 - 40, -RAIL_Y + 20, ROLL_Z - 45), 5)
           + tube3((RAIL_X1 - 40, -RAIL_Y + 20, ROLL_Z - 45), (RAIL_X0 + 20, -RAIL_Y + 20, ROLL_Z - 45), 5)
           + tube3((RAIL_X0 + 20, -RAIL_Y + 20, ROLL_Z - 45), w1, 5))

parts = [
    Part("Main frame", frame, "#4B5563", 1, (0, 0, -260)),
    Part("Belt and end rollers", belt + end_rollers, "#111827", 2, (0, 0, 420)),
    Part("Roller bed", roller_bed, "#94A3B8", 3, (0, 0, 180)),
    Part("Anti-reverse clutch and belt drag", clutch, "#D4A017", 4, (250, 700, 250)),
    Part("Belt speed sensor", sensor, "#0EA5E9", 5, (0, -420, 280)),
    Part("Rear wheel with 250 W geared hub motor", rear_motor, ACCENT, 6, (-160, 0, -380)),
    Part("Rear tire and rim (with item 6)", rear_tyre, TYRE, None, (-160, 0, -380)),
    Part("Front wheel, fork and headset", fork, "#6B7280", 7, (480, 0, -80)),
    Part("Front tire and rim (with item 7)", front_tyre, TYRE, None, (480, 0, -80)),
    Part("Steering column, handlebar and grips", steering, "#374151", 8, (300, 0, 380)),
    Part("Brakes with motor cut-off levers", brakes_rear, "#B91C1C", 9, (-160, -300, -380)),
    Part("Front brake (with item 9)", brakes_front, "#B91C1C", None, (480, 0, -80)),
    Part("Brake levers (with item 9)", levers, "#B91C1C", None, (300, 0, 380)),
    Part("SwapCell receiver cradle and host adapter", cradle, "#7C3AED", 10, (240, 0, 330)),
    Part("SwapCell pack (not in parts cost)", pack, "#C2410C", 11, (330, 0, 620)),
    Part("Controller and walking logic board", controller, "#115E59", 12, (220, -420, -220)),
    Part("Display, level selector, lanyard stop", display, "#2563EB", 13, (420, 0, 560)),
    Part("Guards (heel, roller, side, toe)", guards, "#CBD5E1", 14, (250, 520, 80)),
    Part("Wiring harness with fuse", harness, "#1F2937", 15, (0, -420, -200)),
    Part("Harness to the handlebar (with item 15)", harness_up, "#1F2937", None, (0, -420, -200)),
]


# ---------------- Rider, 1.75 m, standing on the belt mid-stride and holding the bars ----------------
def rider(height=1750.0, x=950.0, z=DECK_Z):
    k = height / 1750.0
    hip_z = z + 860 * k
    stride = 270 * k
    legs = None
    for dy, dx in ((-95, stride), (95, -stride)):
        leg = tube3((x, dy * k, hip_z), (x + dx, dy * k, z + 70 * k), 62 * k)
        foot = Pos(x + dx + 40 * k, dy * k, z + 35 * k) * Box(250 * k, 95 * k, 70 * k)
        legs = leg + foot if legs is None else legs + leg + foot
    torso = Pos(x + 10 * k, 0, hip_z + 300 * k) * Box(210 * k, 360 * k, 620 * k)
    neck = Pos(x + 15 * k, 0, z + 1520 * k) * Cylinder(45 * k, 90 * k)
    head = Pos(x + 20 * k, 0, z + 1635 * k) * Sphere(105 * k)
    arms = None
    for s in (-1, 1):
        a = tube3((x + 10 * k, s * 205 * k, hip_z + 560 * k), (BAR[0] - 70, s * 250, BAR[1] + 5), 42 * k)
        arms = a if arms is None else arms + a
    return Part("rider, 1.75 m,", legs + torso + neck + head + arms, "#9CA3AF", None)


def flow_figure(out):
    """Energy and control flow at a 20 km/h cruise on the flat. All values are estimates."""
    fig, ax = plt.subplots(figsize=(13.5, 7.2), dpi=160)
    ax.set_xlim(0, 13.5); ax.set_ylim(0, 7.2); ax.set_axis_off()

    def node(x, y, name, val, w=2.25, h=0.95, dashed=False, fc="#F0FDFA", ec=ACCENT):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    fc=fc, ec=ec, lw=1.4, ls="--" if dashed else "-"))
        ax.text(x + w / 2, y + h * 0.66, name, ha="center", va="center", fontsize=8.8, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h * 0.28, val, ha="center", va="center", fontsize=8.4, color=ec)

    def arrow(p0, p1, w=2.0, color=ACCENT, ls="-", alpha=0.6):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=14, lw=w, color=color, ls=ls, alpha=alpha))

    def line(pts, color, ls=":", w=1.2, alpha=0.8):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, ls=ls, lw=w, alpha=alpha)

    ax.text(0.0, 7.05, "StepGen: energy and control flow at a 20 km/h cruise, flat road, 118 kg with rider (all values are estimates)",
            fontsize=10, fontweight="bold", color=INK, va="top")
    ax.text(0.0, 6.72, "CONCEPT, NOT FOR FABRICATION", fontsize=6.5, color="#B45309", va="top")

    # energy path (top row), losses drawn upward
    ey, h = 4.0, 0.95
    ax.text(0.3, ey + h + 0.2, "Energy path", fontsize=8.5, color=ACCENT, fontweight="bold")
    node(0.3, ey, "SwapCell pack", "179 W out (est.)")
    node(3.4, ey, "Controller", "170 W to motor (est.)")
    node(6.5, ey, "250 W hub motor", "136 W at wheel (est.)")
    node(9.6, ey, "Wheel at 20 km/h", "9.0 Wh/km from pack (est.)", w=2.8)
    arrow((2.6, ey + 0.47), (3.35, ey + 0.47), 6.5)
    arrow((5.7, ey + 0.47), (6.45, ey + 0.47), 6.2)
    arrow((8.8, ey + 0.47), (9.55, ey + 0.47), 5.2)
    for x, txt in ((4.52, "Controller loss about 9 W"), (7.62, "Motor and gear loss about 34 W"),
                   (11.0, "Road load: rolling 64 W, air 72 W")):
        arrow((x, ey + h + 0.05), (x, ey + h + 0.6), 1.8, "#C2410C")
        ax.text(x, ey + h + 0.78, txt + " (est.)", ha="center", va="center", fontsize=7.8, color="#C2410C")

    # control path (middle row), right to left, sensor directly under the controller
    cy = 2.0
    ax.text(3.4, cy - 0.25, "Control path: walking sets the assist", fontsize=8.5, color="#4B5563", fontweight="bold")
    node(3.4, cy, "Belt speed sensor", "signal, not energy", fc="#F9FAFB", ec="#4B5563")
    node(6.5, cy, "Free-running belt", "20 to 40 W into drag (est.)", fc="#F9FAFB", ec="#4B5563")
    node(9.6, cy, "Rider walks", "4 to 6 km/h, upright", w=2.8, fc="#F9FAFB", ec="#4B5563")
    arrow((9.55, cy + 0.47), (8.8, cy + 0.47), 2.0, "#4B5563")
    arrow((6.45, cy + 0.47), (5.7, cy + 0.47), 1.2, "#4B5563", ls="--")
    arrow((4.52, cy + h + 0.03), (4.52, ey - 0.05), 1.4, "#4B5563", ls="--")
    ax.text(4.7, 3.47, "assist power = belt speed x level, capped at 250 W and 25 km/h;\n"
                       "motor off within 0.5 s when the belt stops, a brake lever is pulled\nor the lanyard is out",
            ha="left", va="center", fontsize=7.6, color="#4B5563")

    # optional regen (bottom row, dashed)
    ry = 0.25
    node(0.3, ry, "Optional roller generator", "about 5 to 10 W (est.)", w=2.9, dashed=True, fc="white", ec="#A16207")
    line([(7.62, cy - 0.03), (7.62, ry + 0.47)], "#A16207")
    arrow((7.62, ry + 0.47), (3.25, ry + 0.47), 1.0, "#A16207", ls=":")
    ax.text(5.45, ry + 0.62, "extra walking effort about 15 W (est.)", ha="center", va="bottom", fontsize=7.4, color="#A16207")
    arrow((1.2, ry + h + 0.03), (1.2, ey - 0.05), 1.0, "#A16207", ls=":")
    ax.text(1.35, 2.55, "to pack: about 5 % more\nrange (est.); needs a\nSwapCell charge-while-\ndriving mode (gap)",
            ha="left", va="center", fontsize=7.4, color="#A16207")

    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white", bbox_inches="tight"); plt.close(fig)
    return out


DECK_PARTS = ("Main frame", "Belt and end rollers", "Roller bed", "Anti-reverse clutch and belt drag",
              "Belt speed sensor", "Rear wheel with 250 W geared hub motor", "Rear tire and rim (with item 6)",
              "Guards (heel, roller, side, toe)")

if __name__ == "__main__":
    from concept import _render, cutaway_parts
    render_all(
        parts, project="StepGen", title="Walking-treadmill vehicle concept", dwg_no="SGN-DWG-010",
        key_figures=["Rider walks at 4 to 6 km/h on a 1.05 m free-running belt",
                     "250 W rear hub motor, assist cut at 25 km/h (proposed)",
                     "About 9 Wh/km at 20 km/h; about 35 to 46 km per SwapCell (estimate)",
                     "Belt top 240 mm above ground; 20 in wheels; about 2.35 x 0.62 m",
                     "About 35 kg without pack; parts about $630, pack excluded (estimate)"],
        scale_figure=False, context=[rider()], cut=False, flow=None,
    )
    # Cutaway of the belt deck: section on the vehicle centre line, seen from the left, low camera
    deck = [Part("Deck frame", deck_frame, "#4B5563", 1)] + [p for p in parts if p.name in DECK_PARTS and p.name != "Main frame"]
    cut_png = _render(cutaway_parts(deck), Path("media") / "cutaway.png", azim=-90, elev=10, size=(10, 10))
    img = plt.imread(cut_png)[..., :3]                      # the kit fits the long side to the short one; crop to content
    ink = (img < 0.97).any(-1)
    rows, cols = ink.any(1).nonzero()[0], ink.any(0).nonzero()[0]
    m = 40
    img = img[max(rows[0] - m, 0):rows[-1] + m, max(cols[0] - m, 0):cols[-1] + m]
    hgt, wid = img.shape[:2]
    fig = plt.figure(figsize=(10, 10 * (hgt + 170) / wid), dpi=160)
    ax = fig.add_axes([0, 90 / (hgt + 170), 1, hgt / (hgt + 170)]); ax.imshow(img); ax.set_axis_off()
    fig.text(0.02, 0.97, "StepGen: cutaway of the belt deck (section on the centre line)", fontsize=9, fontweight="bold",
             color=INK, va="top")
    fig.text(0.02, 0.97 - 22 / (hgt + 170) * 1.6, "CONCEPT, NOT FOR FABRICATION", fontsize=6.5, color="#B45309", va="top")
    fig.text(0.02, 0.02, "Belt top run (black) on a bed of 30 mm rollers between 50 mm end rollers; anti-reverse clutch "
             "(yellow) on the rear roller; heel guard over the rear tire", fontsize=7.5, color="#4B5563", va="bottom")
    fig.savefig(cut_png, facecolor="white"); plt.close(fig)
    flow_figure(Path("media") / "flow.png")
