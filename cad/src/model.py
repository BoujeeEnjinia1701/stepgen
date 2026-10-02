"""StepGen parametric model (build123d), TRL 3, constructable design (SGN-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL into cad/step and cad/stl, then prints the checks
    python cad/src/model.py --check    prints the constructability checks only

The model is built from components (build_components), each one a part that is made or bought and
fixed to its neighbours: every joint is face to face, bolted, welded, clamped or pressed, and every
moving part has its clearance. checks() tests this with build123d: parts that must touch do touch,
parts that must stay apart are apart by at least the stated gap, no two components overlap, and the
front wheel clears the frame at 45 degrees of steering lock. PRELIMINARY, NOT FOR FABRICATION.

Axes: X is the direction of travel (front is +X), Y is across the vehicle (+Y is the rider's left
looking forward is -Y; "left" below means -Y), Z is up. Rear axle at X = 0, ground at Z = 0. Units mm.

The calculation note (docs/04-calcs/sizing.py, SGN-CAL-001) imports PARAMS and geometry() from this
file, so the numbers and the model share one source. build_parts() groups the components by BOM
line for the concept media and the general arrangement sheet.
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Wheels (decided: 20 in, ETRTO 406, front and rear)
    "wheel_r": 247.0,          # 20 x 1.75 in tire, outside diameter about 494 mm
    "tire_r": 22.0,            # tire section radius
    # Belt deck
    "roller_r": 25.0,          # 50 mm crowned end rollers
    "roller_half": 210.0,      # end roller length 420 mm (belt 400 mm wide)
    "axle_r": 8.5,             # 17 mm fixed roller axles (6203 size bearings)
    "rear_roller_x": 320.0,    # rear end roller centre (nominal tension position)
    "roller_pitch": 1050.0,    # end roller centres
    "deck_z": 240.0,           # top of the belt above the ground (R8: 250 or less)
    "belt_w": 400.0,           # belt width (R1: 360 or more)
    "belt_t": 3.0,
    "bed_n": 14,               # idler rollers under the top run
    "bed_r": 15.0,             # 30 mm idler rollers
    "carrier_y": 217.0,        # inside face of the 50 x 3 mm idler carrier bars
    # Frame
    "rail_y": 235.0,           # deck rail centre line from the vehicle centre line
    "rail_w": 30.0, "rail_h": 60.0, "rail_t": 2.0,   # 60 x 30 x 2 mm RHS on edge (SGN-DDR-002)
    "rail_x0": 270.0, "rail_x1": 1420.0,
    "rail_z0": 170.0,          # underside of the deck rails
    "cross_x": (270.0, 830.0), # rear edges of the two 25 x 25 x 2 mm cross members under the rails
    "nose_w": 60.0, "nose_h": 40.0,   # 60 x 40 x 2 mm nose beam across the front ends of the rails
    "down_tube_r": 22.0,       # 44 x 2 mm tube
    "stay_r": 11.0,            # 22 x 1.6 mm rear stays
    "dropout_y": 67.5,         # inside faces of the rear dropouts (135 mm hub)
    "dropout_t": 6.0,
    # Steering (TRL 3: fork offset added so trail is about 58 mm)
    "head_angle": 70.0,        # head tube angle from horizontal, degrees
    "head_bot_x": 1680.0, "head_bot_z": 640.0,
    "head_len": 150.0,
    "head_r": 25.0, "head_bore_r": 22.0,   # bought machined head tube for a ZS44 headset
    "dt_join": 100.0,           # down tube axis meets the steering axis this far above the head tube bottom
    "fork_offset": 30.0,       # rake, perpendicular to the steering axis
    "fork_leg_y": 61.0,        # fork leg centres (100 mm hub between the dropout faces)
    "steerer_r": 14.3,         # 1 1/8 in threadless steerer
    "column_r": 19.0,          # 38 x 2 mm steel steering column (SGN-CAL-001 section 7)
    "bar_x": 1400.0, "bar_z": 1230.0,   # handlebar centre, about 0.99 m above the belt
    "bar_half": 290.0,         # 580 mm straight bar
    "bar_r": 11.1,             # 22.2 mm bar
    # Brakes (rotor planes, left side)
    "rear_rotor_y": -52.0, "front_rotor_y": -34.5, "rotor_r": 80.0,
    # SwapCell pack and receiver (interface v0.3)
    "pack_l": 340.0, "pack_w": 90.0, "pack_d": 80.0,
    "pack_pos": 0.54,          # pack centre along the down tube (fraction of length)
    "cradle_t": 3.0,           # folded 3 mm steel cradle
    "cradle_off": 32.0,        # underside of the cradle above the down tube axis (welded tabs)
    "lever_len": 120.0,        # over-centre lever, class V1 preload 330 N (ratio 6.6 or more)
    # Kickstand (left rail) and controller (left side of the down tube)
    "kick_x": 520.0,
    "ctrl_t": (25.0, 175.0),
    # Rider reference (for the calculation note and media)
    "rider_x": 950.0,          # rider's centre of mass over the belt
}


def geometry(p=PARAMS):
    """Derived points and dimensions (pure Python; no build123d needed)."""
    g = {}
    a = math.radians(p["head_angle"])
    s = (-math.cos(a), math.sin(a))                     # steering axis, up and back
    n = (math.sin(a), math.cos(a))                      # forward normal to the steering axis
    hb = (p["head_bot_x"], p["head_bot_z"])

    def on_axis(z):
        return hb[0] + s[0] * (z - hb[1]) / s[1]

    R = p["wheel_r"]
    z_a = R - p["fork_offset"] * n[1]                   # point on the axis level with the offset axle
    front_x = on_axis(z_a) + p["fork_offset"] * n[0]
    ground_x = on_axis(0.0)
    g["steer_dir"], g["steer_normal"] = s, n
    g["front_x"] = front_x
    g["wheelbase"] = front_x
    g["trail"] = ground_x - front_x
    g["head_top"] = (hb[0] + s[0] * p["head_len"], hb[1] + s[1] * p["head_len"])
    g["col_top"] = (on_axis(p["bar_z"]), p["bar_z"])
    g["roll_z"] = p["deck_z"] - p["roller_r"] - p["belt_t"]     # belt wraps the rollers; its top is the deck
    g["front_roller_x"] = p["rear_roller_x"] + p["roller_pitch"]
    g["belt_usable"] = p["roller_pitch"] - 2 * p["roller_r"]
    g["length"] = front_x + R + 277.0                   # front tire to the back of the rear fender (277 mm radius)
    g["length_tires"] = front_x + 2 * R
    g["width"] = 2 * p["bar_half"]                      # straight 580 mm bar
    g["bar_above_belt"] = p["bar_z"] - p["deck_z"]
    g["nose_top"] = p["rail_z0"] + p["nose_h"]
    g["dt_lo"] = (p["rail_x1"] + p["nose_w"] / 2, g["nose_top"])     # foot of the down tube, on the nose beam
    g["dt_hi"] = (hb[0] + s[0] * p["dt_join"], hb[1] + s[1] * p["dt_join"])
    dx, dz = g["dt_hi"][0] - g["dt_lo"][0], g["dt_hi"][1] - g["dt_lo"][1]
    g["dt_len"] = math.hypot(dx, dz)
    g["dt_ang"] = math.degrees(math.atan2(dz, dx))
    # Lowest frame parts: the two cross members, welded under the rails
    g["ground_clearance"] = p["rail_z0"] - 25.0
    # Lean clearance: the outermost low point is the kickstand body on the left rail
    g["lean_clearance_deg"] = math.degrees(math.atan2(175.0, p["rail_y"] + 15.0 + 24.0))
    return g


# ------------------------------------------------------------------ helpers (build123d)
def _b():
    import build123d as b
    return b


def tube3(a, b_, r):
    """Solid round bar between two points."""
    b = _b()
    a = b.Vector(*a); c = b.Vector(*b_); d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def bx(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def ycyl(x, z, y0, y1, r, ri=0.0):
    """Cylinder (or ring, inner radius ri) along Y at (x, z)."""
    b = _b()
    c = b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, y1 - y0)
    if ri > 0:
        c = c - b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(ri, y1 - y0 + 2)
    return c


def lbox(pl, x0, x1, y0, y1, z0, z1):
    """Box given in the local coordinates of a plane."""
    b = _b()
    return pl.location * b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def lcyl(pl, z0, z1, r, ri=0.0, x=0.0, y=0.0):
    """Cylinder (or ring) along the local Z of a plane."""
    b = _b()
    c = pl.location * b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)
    if ri > 0:
        c = c - pl.location * b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(ri, z1 - z0 + 2)
    return c


def sector(cx, cz, ri, ro, a0, a1, y0, y1, n=48):
    """Annular sector in the XZ plane about (cx, cz), angles in degrees from +X toward +Z, extruded y0..y1."""
    b = _b()
    angs = [math.radians(a0 + (a1 - a0) * k / n) for k in range(n + 1)]
    pts = [(cx + ro * math.cos(t), cz + ro * math.sin(t)) for t in angs]
    ri = ri / math.cos(math.radians(abs(a1 - a0) / n / 2))     # inner chords stay outside the true radius
    pts += [(cx + ri * math.cos(t), cz + ri * math.sin(t)) for t in reversed(angs)]
    face = b.Plane.XZ * b.Polygon(*pts, align=None)
    sol = b.extrude(face, amount=(y1 - y0) / 2, both=True)
    return b.Pos(0, (y0 + y1) / 2, 0) * sol


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def mirror_y(shape):
    b = _b()
    return shape.mirror(b.Plane.XZ)


def both(shape):
    return shape + mirror_y(shape)


# ------------------------------------------------------------------ frames of reference
def steer_plane(p=PARAMS):
    """Local x: forward normal to the steering axis; local y: global Y; local z: up the steering axis.
    Origin at the bottom of the head tube."""
    b = _b()
    a = math.radians(p["head_angle"])
    return b.Plane(origin=(p["head_bot_x"], 0, p["head_bot_z"]), x_dir=(math.sin(a), 0, math.cos(a)),
                   z_dir=(-math.cos(a), 0, math.sin(a)))


def dt_plane(p=PARAMS):
    """Local x (t): up the down tube from its foot; local y: global Y; local z (o): normal, toward the rider."""
    b = _b()
    g = geometry(p)
    ux, uz = (g["dt_hi"][0] - g["dt_lo"][0]) / g["dt_len"], (g["dt_hi"][1] - g["dt_lo"][1]) / g["dt_len"]
    return b.Plane(origin=(g["dt_lo"][0], 0, g["dt_lo"][1]), x_dir=(ux, 0, uz), z_dir=(-uz, 0, ux))


def axis_pt(sv, p=PARAMS):
    a = math.radians(p["head_angle"])
    return (p["head_bot_x"] - math.cos(a) * sv, 0.0, p["head_bot_z"] + math.sin(a) * sv)


def derived(p=PARAMS):
    """Positions used by the build plan and the checks."""
    g = geometry(p)
    d = {}
    d["tc"] = g["dt_len"] * p["pack_pos"]
    d["pack_t"] = (d["tc"] - p["pack_l"] / 2, d["tc"] + p["pack_l"] / 2)
    d["front_axle"] = (g["front_x"], p["wheel_r"])
    d["idler_x"] = [p["rear_roller_x"] + 70 + k * (p["roller_pitch"] - 140) / (p["bed_n"] - 1) for k in range(p["bed_n"])]
    d["col_top_s"] = (1250.0 - p["head_bot_z"]) / math.sin(math.radians(p["head_angle"]))
    d["upper_stay"] = ((p["rail_x0"] - 3.0, p["rail_y"], 205.0), (30.0, p["dropout_y"] + p["dropout_t"], 245.0))
    d["lower_stay"] = ((p["cross_x"][0], 200.0, 157.0), (30.0, p["dropout_y"] + p["dropout_t"], 233.0))
    d["stay_len"] = [math.dist(*d["upper_stay"]), math.dist(*d["lower_stay"])]
    return d


# ------------------------------------------------------------------ components
class Comp:
    def __init__(self, key, name, shape, bom, color):
        self.key, self.name, self.shape, self.bom, self.color = key, name, shape, bom, color


COLORS = {
    "frame": "#4B5563", "carriers": "#94A3B8", "idlers": "#CBD5E1", "front_roller": "#64748B", "rear_roller": "#64748B",
    "belt": "#111827", "drag": "#D4A017", "sensor": "#0EA5E9", "fork": "#6B7280", "front_wheel": "#1F2937",
    "column": "#374151", "bar": "#1F2937", "levers": "#B91C1C", "controls": "#2563EB", "rear_wheel": "#0F766E",
    "torque_arms": "#0E7490", "rotors": "#9CA3AF", "caliper_f": "#B91C1C", "caliper_r": "#B91C1C",
    "controller": "#115E59", "harness": "#111827", "cradle": "#7C3AED", "pack": "#C2410C", "heel": "#E5E7EB",
    "fender": "#D1D5DB", "covers": "#E2E8F0", "toe": "#E5E7EB", "boards": "#F1F5F9", "kickstand": "#1F2937",
}


def build_components(p=PARAMS):
    """Every component of the constructable design, keyed, in build order."""
    b = _b()
    g = geometry(p)
    d = derived(p)
    C = {}

    def add(key, name, shape, bom):
        C[key] = Comp(key, name, shape, bom, COLORS[key])

    R, TR, RR = p["wheel_r"], p["tire_r"], p["roller_r"]
    RRX, FRX = p["rear_roller_x"], g["front_roller_x"]
    DECK, RZ = p["deck_z"], g["roll_z"]
    RY, RW, RH, RT = p["rail_y"], p["rail_w"], p["rail_h"], p["rail_t"]
    X0, X1, Z0 = p["rail_x0"], p["rail_x1"], p["rail_z0"]
    yi, yo = RY - RW / 2, RY + RW / 2            # rail inner and outer faces (220, 250)
    AX = p["axle_r"]
    ZD = RZ - 20.0                               # drag screw height
    ZH = 196.0                                   # harness height along the left rail
    RH_ = p["roller_half"]
    DY, DT = p["dropout_y"], p["dropout_t"]
    SP = steer_plane(p)
    DP = dt_plane(p)
    L = g["dt_len"]
    tc = d["tc"]
    FX = g["front_x"]

    # ---------------------------------------------------------------- 1 main frame (welded)
    rail = bx(X0, X1, yi, yo, Z0, Z0 + RH) - bx(X0 - 1, X1 + 1, yi + RT, yo - RT, Z0 + RT, Z0 + RH - RT)
    rail = rail - bx(RRX - 20, RRX + 25, yi - 1, yo + 1, RZ - AX, RZ + AX)                    # rear axle slot
    rail = rail - ycyl(FRX, RZ, yi - 1, yo + 1, 5.0)                                         # front axle bolt
    rail = rail + ycyl(FRX, RZ, yi + RT, yo - RT, 8.0, 5.0)                                  # crush sleeve
    rail_l = mirror_y(rail)
    rail_r = rail - ycyl(RRX, ZD, yi - 1, yo + 1, 4.0)                                       # drag screw hole
    caps = both(bx(X0 - 3, X0, yi, yo, Z0, Z0 + RH))
    cross = fuse([bx(cx, cx + 30, -yo, yo, Z0 - 25, Z0) for cx in p["cross_x"]])
    nose = bx(X1, X1 + p["nose_w"], -yo, yo, Z0, Z0 + p["nose_h"]) - \
        bx(X1 + RT, X1 + p["nose_w"] - RT, -yo - 1, yo + 1, Z0 + RT, Z0 + p["nose_h"] - RT)
    # head tube (bought, machined for a ZS44 headset) and down tube mitred to it and to the nose beam
    head = lcyl(SP, 0, p["head_len"], p["head_r"], p["head_bore_r"])
    head_outer = lcyl(SP, -60, p["head_len"] + 60, p["head_r"])
    ux, uz = (g["dt_hi"][0] - g["dt_lo"][0]) / L, (g["dt_hi"][1] - g["dt_lo"][1]) / L
    dt = tube3((g["dt_lo"][0] - ux * 40, 0, g["dt_lo"][1] - uz * 40), (g["dt_hi"][0], 0, g["dt_hi"][1]), p["down_tube_r"])
    dt = (dt & bx(1300, 1800, -100, 100, g["nose_top"], 900)) - head_outer
    # rear stays (upper to the rail end caps, lower to the rear cross member) and dropouts
    us0, us1 = d["upper_stay"]
    ls0, ls1 = d["lower_stay"]
    stays = (tube3(us0, us1, p["stay_r"]) + tube3(ls0, ls1, p["stay_r"]))
    stays = stays - bx(-100, 400, -DY, DY, 0, 400)
    stays = both(stays)
    slot = bx(-6.1, 6.1, -200, 200, 200, R) + ycyl(0, R, -200, 200, 6.1)
    drop = bx(-20, 40, DY, DY + DT, R - 30, R + 30)
    drop_l = mirror_y(drop) + bx(-95, -20, -DY - DT, -DY, 182, 242)                           # caliper tab, left
    drops = (drop + drop_l) - slot
    # tabs and small parts welded on
    lugs = both(bx(X0 + 2, X0 + 12, yo, yo + 13, RZ - 10, RZ + 10) - b.Pos(X0 + 7, yo + 7, RZ) * b.Rot(0, 90, 0) * b.Cylinder(4.0, 20))
    drag_nut = ycyl(RRX, ZD, yo, yo + 7, 7.0, 4.0)
    kick_plate = bx(p["kick_x"] - 25, p["kick_x"] + 25, -yo - 4, -yo, 172, 208)
    ctrl_plate = lbox(DP, p["ctrl_t"][0] - 5, p["ctrl_t"][1] + 5, -24.5, -21.5, -25, 25)
    tabs = fuse([lbox(DP, t - 20, t + 20, -15, 15, 15, p["cradle_off"]) for t in (tc - 120, tc + 120)])
    frame = fuse([rail_r, rail_l, caps, cross, nose, head, dt, stays, drops, lugs, drag_nut, kick_plate, ctrl_plate, tabs])
    add("frame", "Main frame (welded)", frame, 1)

    # ---------------------------------------------------------------- 3 roller bed
    cy = p["carrier_y"]
    car = bx(RRX + 40, FRX - 40, cy, cy + 3, 182, 232)
    heads = fuse([ycyl(x, 195, cy - 3.3, cy, 5.5) for x in (400, 700, 1000, 1290)])
    add("carriers", "Idler carrier bars (2), on the rails", both(car + heads), 3)
    zi = DECK - p["belt_t"] - p["bed_r"]
    idl = fuse([ycyl(x, zi, -205, 205, p["bed_r"]) + ycyl(x, zi, -cy, cy, 4.0) for x in d["idler_x"]])
    add("idlers", "Idler rollers (14)", idl, 3)

    # ---------------------------------------------------------------- 2 end rollers and belt
    spacers = lambda x: ycyl(x, RZ, RH_, yi, 11.0, AX) + ycyl(x, RZ, -yi, -RH_, 11.0, AX)  # noqa: E731
    fr = ycyl(FRX, RZ, -RH_, RH_, RR) + ycyl(FRX, RZ, -yi, yi, AX) + spacers(FRX)
    fbolts = both(ycyl(FRX, RZ, yi, yo, 5.0) + ycyl(FRX, RZ, yo, yo + 2, 12.0) + ycyl(FRX, RZ, yo + 2, yo + 9, 8.5))
    add("front_roller", "Front end roller, axle and bolts", fr + fbolts, 2)
    rr = ycyl(RRX, RZ, -RH_, RH_, RR) + ycyl(RRX, RZ, -yo - 12, yo + 12, AX) + spacers(RRX)
    tb = both(b.Pos(RRX - 30, yo + 7, RZ) * b.Rot(0, 90, 0) * b.Cylinder(4.0, 60)
              + b.Pos(X0 - 3, yo + 7, RZ) * b.Rot(0, 90, 0) * b.Cylinder(6.5, 10))
    add("rear_roller", "Rear end roller with one-way bearing, axle and tension bolts", rr + tb, 2)
    bt = p["belt_t"]
    BW = p["belt_w"] / 2
    belt = (bx(RRX, FRX, -BW, BW, DECK - bt, DECK) + bx(RRX, FRX, -BW, BW, RZ - RR - bt, RZ - RR)
            + sector(RRX, RZ, RR, RR + bt, 90, 270, -BW, BW) + sector(FRX, RZ, RR, RR + bt, -90, 90, -BW, BW))
    add("belt", "Belt", belt, 2)

    # ---------------------------------------------------------------- 4 belt drag screw (one-way bearing is inside the rear roller)
    drag = ycyl(RRX, ZD, RH_, RH_ + 4, 6.0) + ycyl(RRX, ZD, RH_ + 4, yo + 12, 4.0) + ycyl(RRX, ZD, yo + 12, yo + 22, 8.0)
    add("drag", "Belt drag screw (felt tip)", drag, 4)

    # ---------------------------------------------------------------- 5 belt speed sensor
    zs = RZ - 18
    sens = (ycyl(FRX, RZ, -RH_ - 3, -RH_, 22.0, 12.0) + bx(FRX - 5, FRX + 5, -yi + 2.5, -yi + 5.5, zs - 5, zs + 5)
            + bx(FRX - 10, FRX + 10, -yi, -yi + 2.5, 183, 199))
    add("sensor", "Belt speed sensor: magnet ring, Hall sensor, bracket", sens, 5)

    # ---------------------------------------------------------------- 7 fork and headset (bought)
    a = math.radians(p["head_angle"])
    crown = lbox(SP, -25, 25, -72, 72, -30, -5)
    steerer = lcyl(SP, -5, 206, p["steerer_r"])
    hs = (lcyl(SP, 0, 8, p["head_bore_r"], p["steerer_r"]) + lcyl(SP, p["head_len"] - 8, p["head_len"], p["head_bore_r"], p["steerer_r"])
          + lcyl(SP, p["head_len"], p["head_len"] + 8, p["head_r"], p["steerer_r"]) + lcyl(SP, -5, 0, p["head_r"], p["steerer_r"]))
    fy = p["fork_leg_y"]
    A = b.Vector(FX, 0, R)
    legs, fdrops = [], []
    for sgn in (1, -1):
        top = b.Vector(*axis_pt(-25, p)) + b.Vector(0, sgn * fy, 0)
        bot = A + b.Vector(0, sgn * fy, 0)
        dv = (top - bot).normalized()
        legs.append(tube3(tuple(bot + dv * 25), tuple(top), 11.0))
        lp = b.Plane(origin=bot, x_dir=b.Vector(dv.Z, 0, -dv.X), z_dir=dv)
        y0, y1 = (50 - fy, 55 - fy) if sgn > 0 else (fy - 55, fy - 50)
        fdrops.append(lbox(lp, -12, 12, y0, y1, -12, 40))
    fslot = (b.Plane(origin=A, x_dir=(1, 0, 0), z_dir=(0, 1, 0)).location * b.Cylinder(5.1, 200))
    leg_dir = (b.Vector(*axis_pt(-17.5, p)) - A).normalized()
    fslot = fslot + b.Plane(origin=A - leg_dir * 10, x_dir=(leg_dir.Z, 0, -leg_dir.X), z_dir=leg_dir).location * b.Box(10.2, 200, 20)
    fdrop = fuse(fdrops) - fslot
    # caliper post on the left leg, along the ray at 150 degrees from the axle
    ca = math.radians(150)
    cp = b.Plane(origin=A, x_dir=(math.cos(ca), 0, math.sin(ca)), z_dir=(0, 1, 0))
    ftab = lbox(cp, 40, 92, -20, 48, -54, -46)
    fork = fuse([crown, steerer] + legs + [fdrop, ftab])
    add("fork", "Fork and headset", fork + hs, 7)

    # ---------------------------------------------------------------- 7 front wheel (bought)
    def rim_tire(cx):
        tire = b.Pos(cx, 0, R) * b.Rot(90, 0, 0) * b.Torus(R - TR, TR)
        rim = ycyl(cx, R, -10, 10, R - 2 * TR, R - 2 * TR - 14)
        return tire + rim

    def spokes(cx, r0):
        out = None
        for k in range(12):
            t = math.radians(k * 30 + 15)
            sp = tube3((cx + r0 * math.cos(t), 0, R + r0 * math.sin(t)),
                       (cx + (R - 2 * TR - 10) * math.cos(t), 0, R + (R - 2 * TR - 10) * math.sin(t)), 2.0)
            out = sp if out is None else out + sp
        return out
    fw = rim_tire(FX) + spokes(FX, 15) + ycyl(FX, R, -50, 50, 22.0) + ycyl(FX, R, -61, 61, 5.0) \
        + both(ycyl(FX, R, 55, 61, 9.0))
    add("front_wheel", "Front wheel", fw, 7)

    # ---------------------------------------------------------------- 8 steering column (welded) and bar
    cts = d["col_top_s"]
    sleeve = lcyl(SP, p["head_len"] + 8, p["head_len"] + 88, 16.85, p["steerer_r"])
    clamp_lugs = lbox(SP, -29, -16, 3, 9, 168, 198) + lbox(SP, -29, -16, -9, -3, 168, 198)
    col = lcyl(SP, p["head_len"] + 58, cts, p["column_r"], 17.0) + lcyl(SP, cts - 3, cts, p["column_r"])
    cx_bar = g["col_top"][0]
    stem = b.Pos((cx_bar + p["bar_x"] + 12) / 2, 0, p["bar_z"]) * b.Rot(0, 90, 0) * b.Cylinder(15.0, cx_bar - p["bar_x"] - 12)
    bclamp = ycyl(p["bar_x"], p["bar_z"], -20, 20, 13.45, p["bar_r"])
    add("column", "Steering column (welded)", fuse([sleeve, clamp_lugs, col, stem, bclamp]), 8)
    BX, BZ, BH = p["bar_x"], p["bar_z"], p["bar_half"]
    bar = ycyl(BX, BZ, -BH, BH, p["bar_r"]) + both(ycyl(BX, BZ, 160, BH, 16.0, p["bar_r"]))
    add("bar", "Handlebar and grips", bar, 8)

    # ---------------------------------------------------------------- 9 brake levers, 13 controls
    lev = None
    for sgn in (1, -1):
        l_ = (ycyl(BX, BZ, sgn * 128 if sgn > 0 else -142, sgn * 142 if sgn > 0 else -128, 16.0, p["bar_r"])
              + tube3((BX + 18, sgn * 135, BZ + 3), (BX + 32, sgn * 150, BZ - 8), 5.0)
              + tube3((BX + 32, sgn * 150, BZ - 8), (BX + 32, sgn * 235, BZ - 15), 5.0))
        lev = l_ if lev is None else lev + l_
    add("levers", "Brake levers with motor cut-off switches", lev, 9)
    disp = ycyl(BX, BZ, 40, 60, 15.0, p["bar_r"]) + b.Pos(BX, 55, BZ + 38) * b.Rot(0, 20, 0) * b.Box(20, 60, 45)
    sel = ycyl(BX, BZ, -50, -38, 15.0, p["bar_r"]) + bx(BX - 15, BX + 15, -59, -29, BZ + 14, BZ + 39)
    key = ycyl(BX, BZ, -80, -68, 15.0, p["bar_r"]) + b.Pos(BX, -74, BZ + 26) * b.Cylinder(12.0, 24)
    lany = ycyl(BX, BZ, 95, 107, 15.0, p["bar_r"]) + bx(BX - 12, BX + 12, 88, 114, BZ + 14, BZ + 34)
    add("controls", "Display, level selector, key switch, lanyard stop", fuse([disp, sel, key, lany]), 13)

    # ---------------------------------------------------------------- 6 rear wheel with hub motor, torque arms
    rw = (rim_tire(0.0) + spokes(0.0, 80) + ycyl(0, R, -40, 40, 85.0) + ycyl(0, R, -DY, DY, 12.0)
          + ycyl(0, R, -84.5, 84.5, 6.0) + both(ycyl(0, R, DY + DT + 5, 84.5, 9.0))
          + ycyl(0, R, -51, -40, 28.0))
    add("rear_wheel", "Rear wheel with 250 W hub motor", rw, 6)
    arm = bx(-15, 15, DY + DT, DY + DT + 5, R - 15, R + 28) - ycyl(0, R, 0, 200, 6.1)
    add("torque_arms", "Torque arms (2)", both(arm), 6)

    # ---------------------------------------------------------------- 9 rotors and calipers
    rf = ycyl(FX, R, p["front_rotor_y"] - 1, p["front_rotor_y"] + 1, p["rotor_r"], 22.0)
    rrot = ycyl(0, R, p["rear_rotor_y"] - 1, p["rear_rotor_y"] + 1, p["rotor_r"], 28.0)
    add("rotors", "Brake rotors (2), 160 mm", rf + rrot, 9)
    cal_f = lbox(cp, 50, 90, -20, 20, -46, -24) - lbox(cp, 49, 82, -25, 25, p["front_rotor_y"] - 2, p["front_rotor_y"] + 2)
    add("caliper_f", "Front brake caliper", cal_f, 9)
    ra = math.radians(210)
    rp = b.Plane(origin=(0, 0, R), x_dir=(math.cos(ra), 0, math.sin(ra)), z_dir=(0, 1, 0))
    cal_r = lbox(rp, 50, 90, -20, 20, -DY, -44) - lbox(rp, 49, 82, -25, 25, p["rear_rotor_y"] - 2, p["rear_rotor_y"] + 2)
    add("caliper_r", "Rear brake caliper", cal_r, 9)

    # ---------------------------------------------------------------- 12 controller on its plate
    ctrl = lbox(DP, p["ctrl_t"][0], p["ctrl_t"][1], -94.5, -24.5, -20, 20)
    add("controller", "Controller and walking logic board", ctrl, 12)

    # ---------------------------------------------------------------- 10 receiver cradle, class V1, with its lever
    pt0, pt1 = d["pack_t"]
    o0 = p["cradle_off"]
    o1 = o0 + p["cradle_t"]
    base = lbox(DP, tc - 185, tc + 185, -49, 49, o0, o1)                     # one blank: base and guides folded up
    stop = lbox(DP, pt0 - 12, pt0, -46, 46, o1, o1 + 70)                      # 12 mm end stop plate welded in
    guides = both(lbox(DP, tc - 150, tc + 215, 46, 49, o1, o1 + 60) + lbox(DP, tc + 190, tc + 235, 46, 49, o1 + 60, o1 + 100))
    pin = DP.location * b.Pos(tc + 225, 0, o1 + 93) * b.Rot(90, 0, 0) * b.Cylinder(4.0, 98)
    lever = lbox(DP, tc + 105, tc + 232, -15, 15, o1 + 89, o1 + 97) + lbox(DP, pt1 + 34, pt1 + 44, -20, 20, o1 + 31, o1 + 89)
    add("cradle", "Receiver cradle with over-centre lever", fuse([base, stop, guides, pin, lever]), 10)
    pack = lbox(DP, pt0, pt1, -45, 45, o1, o1 + p["pack_d"]) + lbox(DP, pt1, pt1 + 34, -42, 42, o1 + 29, o1 + 51)
    add("pack", "SwapCell pack (not in parts cost)", pack, 11)

    # ---------------------------------------------------------------- 15 harness (internal in the left rail between the grommets)
    hr = 3.5

    def run(pts):
        return fuse([tube3(pts[k], pts[k + 1], hr) for k in range(len(pts) - 1)] +
                    [b.Pos(*q) * b.Sphere(hr) for q in pts])

    def dtp(t, y, o):
        v = DP.from_local_coords((t, y, o))
        return (v.X, v.Y, v.Z)
    c0 = dtp(p["ctrl_t"][0] - hr - 1, -59.5, 0)
    low = run([c0, (c0[0], -59.5, g["nose_top"] + hr + 0.5), (c0[0], -yo - 6, g["nose_top"] + hr + 0.5),
               (c0[0], -yo - 6, ZH), (X1 - 15, -yo - 6, ZH)])
    rear = run([(X0 + 60, -yo - 6, ZH), (X0 - 8, -yo - 6, ZH), (40, -100, 226), (14, -100, 232)])
    s_lo = p["head_len"] + 110
    col_pt = lambda sv, y: (axis_pt(sv, p)[0], y, axis_pt(sv, p)[2])  # noqa: E731
    up = run([dtp(p["ctrl_t"][1] + hr + 1, -59.5, 0), dtp(p["ctrl_t"][1] + 12, -26.5, 0), dtp(L - 70, -26.5, 0),
              col_pt(100, -42), col_pt(s_lo, -23.5), col_pt((BZ - 25 - p["head_bot_z"]) / math.sin(a), -23.5), (BX + 8, -40, BZ - 25)])
    add("harness", "Wiring harness with fuse", low + rear + up, 15)

    # ---------------------------------------------------------------- 14 guards
    heel = bx(X0, X0 + 2, -yi + 2, yi - 2, Z0, 360) + bx(X0 + 2, X0 + 27, -yi + 2, yi - 2, Z0, Z0 + 2)
    add("heel", "Heel guard", heel, 14)
    a_front = math.degrees(math.acos(X0 / 277.0))
    fend = sector(0, R, 275, 277, a_front, 200, -30, 30)
    fstays = (ycyl(-15, 225, DY + DT, DY + DT + 6, 2.5) + tube3((-15, DY + DT + 6, 225), (-274.9, 27, 222.7), 2.5)
              + ycyl(-90, 195, -DY - DT - 6, -DY - DT, 2.5) + tube3((-90, -DY - DT - 6, 195), (-274.9, -27, 222.7), 2.5)
              + b.Pos(-15, DY + DT + 6, 225) * b.Sphere(2.5) + b.Pos(-90, -DY - DT - 6, 195) * b.Sphere(2.5))
    add("fender", "Rear fender and stays", fend + fstays, 14)
    covers = sector(RRX, RZ, 40, 42, 90, 270, -yi, yi) + sector(FRX, RZ, 40, 42, -90, 12, -yi, yi)
    add("covers", "Roller covers (2)", covers, 14)
    tp = b.Plane(origin=(X1, 0, g["nose_top"]), x_dir=(math.cos(math.radians(20)), 0, math.sin(math.radians(20))),
                 z_dir=(-math.sin(math.radians(20)), 0, math.cos(math.radians(20))))
    toe = lbox(tp, -2, 0, -218, 218, 0, 128) + both(bx(X1, X1 + 25, 40, 218, g["nose_top"], g["nose_top"] + 2))
    add("toe", "Toe guard", toe, 14)
    sx = (360, 700, 1040, 1360)
    boards = both(bx(330, 1390, 195, 265, 243, 249) + fuse([b.Pos(x, RY, 236.5) * b.Cylinder(6.0, 13) for x in sx]))
    add("boards", "Side boards (2) on spacers", boards, 14)

    # ---------------------------------------------------------------- 16 kickstand
    kx = p["kick_x"]
    kick = bx(kx - 20, kx + 20, -yo - 24, -yo - 4, 175, 205) + tube3((kx - 5, -yo - 14, 183), (300, -yo - 14, 183), 7.0)
    add("kickstand", "Kickstand", kick, 16)
    return C


# ------------------------------------------------------------------ grouped by BOM line (concept media, GA sheet)
GROUPS = [
    ("Main frame", ["frame"], 1, (0, 0, -260)),
    ("Belt and end rollers", ["belt", "front_roller", "rear_roller"], 2, (0, 0, 420)),
    ("Roller bed", ["idlers", "carriers"], 3, (0, 0, 180)),
    ("Anti-reverse bearing and belt drag", ["drag"], 4, (250, 700, 250)),
    ("Belt speed sensor", ["sensor"], 5, (0, -420, 280)),
    ("Rear wheel with 250 W geared hub motor", ["rear_wheel", "torque_arms"], 6, (-160, 0, -380)),
    ("Front wheel, fork and headset", ["fork", "front_wheel"], 7, (480, 0, -80)),
    ("Steering column, handlebar and grips", ["column", "bar"], 8, (300, 0, 380)),
    ("Brakes with motor cut-off levers", ["levers", "rotors", "caliper_f", "caliper_r"], 9, (300, -300, 380)),
    ("SwapCell receiver cradle, class V1", ["cradle"], 10, (240, 0, 330)),
    ("SwapCell pack (not in parts cost)", ["pack"], 11, (330, 0, 620)),
    ("Controller and walking logic board", ["controller"], 12, (220, -420, -220)),
    ("Display, selector, lanyard, key switch", ["controls"], 13, (420, 0, 560)),
    ("Guards (heel, roller, side, toe, fender)", ["heel", "fender", "covers", "toe", "boards"], 14, (250, 520, 80)),
    ("Wiring harness with fuse", ["harness"], 15, (0, -420, -200)),
    ("Kickstand and hardware", ["kickstand"], 16, (0, -300, -300)),
]


def build_parts(p=PARAMS):
    """Return ([(name, shape, colour, bom_item, explode_offset)], frame shape) grouped by BOM line."""
    C = build_components(p)
    out = []
    for name, keys, bom, ex in GROUPS:
        out.append((name, fuse([C[k].shape for k in keys]), C[keys[0]].color, bom, ex))
    return out, C["frame"].shape


def assembly(parts):
    from build123d import Compound
    kids = []
    for name, shape, *_ in parts:
        shape.label = name
        kids.append(shape)
    return Compound(children=kids, label="StepGen assembly")


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def _bb_hit(a, b_, pad=1.0):
    A, B = a.bounding_box(), b_.bounding_box()
    return not (A.max.X + pad < B.min.X or B.max.X + pad < A.min.X or A.max.Y + pad < B.min.Y or B.max.Y + pad < A.min.Y
                or A.max.Z + pad < B.min.Z or B.max.Z + pad < A.min.Z)


def checks(p=PARAMS):
    """Constructability checks. Returns (description, overlap mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    b = _b()
    g = geometry(p)
    R = p["wheel_r"]
    # deck
    chk("Carrier bars on the rail inside faces", S("carriers"), S("frame"), "touch")
    chk("Idler axles in the carrier bars", S("idlers"), S("carriers"), "touch")
    chk("Belt on the idlers", S("belt"), S("idlers"), "touch")
    chk("Belt on the front roller", S("belt"), S("front_roller"), "touch")
    chk("Belt on the rear roller", S("belt"), S("rear_roller"), "touch")
    chk("Front roller axle and bolts on the rails", S("front_roller"), S("frame"), "touch")
    chk("Rear roller axle in the rail slots, tension bolts on the lugs", S("rear_roller"), S("frame"), "touch")
    chk("Belt clear of the frame", S("belt"), S("frame"), 10.0)
    chk("Belt clear of the carrier bars", S("belt"), S("carriers"), 10.0)
    chk("Belt clear of the side boards", S("belt"), S("boards"), 2.0)
    chk("Belt clear of the roller covers", S("belt"), S("covers"), 10.0)
    chk("Belt clear of the heel guard", S("belt"), S("heel"), 15.0)
    chk("Belt clear of the toe guard", S("belt"), S("toe"), 10.0)
    chk("Idlers clear of the frame", S("idlers"), S("frame"), 2.0)
    chk("Idlers clear of the end rollers", S("idlers"), S("front_roller") + S("rear_roller"), 5.0)
    chk("Drag screw felt tip on the rear roller end", S("drag"), S("rear_roller"), "touch")
    chk("Drag screw in its welded nut and rail holes", S("drag"), S("frame"), "touch")
    chk("Magnet ring on the front roller end", S("sensor"), S("front_roller"), "touch")
    chk("Sensor bracket on the left rail", S("sensor"), S("frame"), "touch")
    chk("Roller covers on the rail inside faces", S("covers"), S("frame"), "touch")
    chk("Roller covers clear of the rollers", S("covers"), S("front_roller") + S("rear_roller"), 5.0)
    chk("Roller covers clear of the sensor", S("covers"), S("sensor"), 2.0)
    chk("Side boards on their spacers, spacers on the rails", S("boards"), S("frame"), "touch")
    chk("Heel guard on the rear cross member", S("heel"), S("frame"), "touch")
    chk("Toe guard flanges on the nose beam", S("toe"), S("frame"), "touch")
    chk("Toe guard clear of the front roller cover", S("toe"), S("covers"), 2.0)
    # steering
    chk("Headset in the head tube", S("fork"), S("frame"), "touch")
    chk("Steering column clamp on the steerer and headset", S("column"), S("fork"), "touch")
    chk("Steering column clear of the frame", S("column"), S("frame"), 3.0)
    chk("Handlebar in the bar clamp", S("bar"), S("column"), "touch")
    chk("Brake levers on the bar", S("levers"), S("bar"), "touch")
    chk("Controls on the bar", S("controls"), S("bar"), "touch")
    chk("Controls clear of the brake levers", S("controls"), S("levers"), 3.0)
    chk("Controls clear of the stem and clamp", S("controls"), S("column"), 2.0)
    chk("Front hub between the fork dropouts", S("front_wheel"), S("fork"), "touch")
    chk("Front tire clear of the fork", b.Pos(0, 0, 0) * (S("front_wheel") & bx(g["front_x"] - 260, g["front_x"] + 260, -30, 30, 0, 600)) - ycyl(g["front_x"], R, -60, 60, 30), S("fork"), 5.0)
    chk("Front rotor on the hub", S("rotors"), S("front_wheel"), "touch")
    chk("Front caliper on the fork post", S("caliper_f"), S("fork"), "touch")
    chk("Front caliper clear of the rotor", S("caliper_f"), S("rotors"), 0.5)
    chk("Front caliper clear of the wheel", S("caliper_f"), S("front_wheel"), 3.0)
    # rear wheel
    chk("Hub motor between the dropouts", S("rear_wheel"), S("frame"), "touch")
    chk("Torque arms on the dropouts", S("torque_arms"), S("frame"), "touch")
    chk("Axle nuts on the torque arms", S("torque_arms"), S("rear_wheel"), "touch")
    chk("Rear rotor on the motor's rotor boss", S("rotors"), S("rear_wheel"), "touch")
    chk("Rotors clear of the frame and fork", S("rotors"), S("frame") + S("fork"), 5.0)
    chk("Rear caliper on the left dropout tab", S("caliper_r"), S("frame"), "touch")
    chk("Rear caliper clear of the rotor", S("caliper_r"), S("rotors"), 0.5)
    chk("Rear caliper clear of the motor and wheel", S("caliper_r"), S("rear_wheel"), 2.0)
    tire_r = S("rear_wheel") & bx(-260, 260, -30, 30, 0, 600) - ycyl(0, R, -100, 100, 100)
    chk("Rear tire clear of the frame", tire_r, S("frame"), 10.0)
    chk("Rear wheel clear of the heel guard", S("rear_wheel"), S("heel"), 15.0)
    chk("Rear wheel clear of the fender and its stays", S("rear_wheel"), S("fender"), 10.0)
    chk("Fender front end on the heel guard", S("fender"), S("heel"), "touch")
    chk("Fender stays on the dropouts", S("fender"), S("frame"), "touch")
    chk("Fender stays clear of the caliper", S("fender"), S("caliper_r"), 3.0)
    chk("Fender clear of the torque arms", S("fender"), S("torque_arms"), 2.0)
    # electrics, cradle, pack
    chk("Controller on its plate", S("controller"), S("frame"), "touch")
    chk("Cradle on its two welded tabs", S("cradle"), S("frame"), "touch")
    chk("Pack on the cradle base, end stop and lever pad", S("pack"), S("cradle"), "touch")
    chk("Pack clear of the frame", S("pack"), S("frame"), 3.0)
    chk("Pack clear of the toe guard", S("pack"), S("toe"), 10.0)
    chk("Cradle clear of the head tube, fork and column", S("cradle"), S("fork") + S("column"), 10.0)
    chk("Cradle clear of the controller", S("cradle"), S("controller"), 5.0)
    chk("Harness clear of the belt", S("harness"), S("belt"), 5.0)
    chk("Harness clear of the rear wheel and rotor", S("harness"), S("rear_wheel") + S("rotors"), 3.0)
    chk("Harness clear of the kickstand", S("harness"), S("kickstand"), 1.0)
    chk("Harness clear of the rear roller and tension bolts", S("harness"), S("rear_roller"), 1.0)
    chk("Harness clear of the cradle and pack", S("harness"), S("cradle") + S("pack"), 3.0)
    chk("Harness clear of the steering column", S("harness"), S("column"), 0.5)
    chk("Kickstand on its welded plate", S("kickstand"), S("frame"), "touch")
    # steering lock: front wheel, fork, front rotor and caliper turned 45 degrees each way
    a = math.radians(p["head_angle"])
    ax = b.Axis((p["head_bot_x"], 0, p["head_bot_z"]), (-math.cos(a), 0, math.sin(a)))
    fr_rot = S("rotors") & bx(g["front_x"] - 100, g["front_x"] + 100, -100, 100, 0, 600)
    turn = fuse([S("front_wheel"), S("fork") - lcyl(steer_plane(p), -31, 400, 40), fr_rot, S("caliper_f")])
    others = fuse([S("frame"), S("toe"), S("controller"), S("cradle"), S("pack"), S("harness")])
    for ang in (45, -45):
        chk(f"Front wheel and fork at {ang:+d} degrees of lock clear of the frame, pack and guards",
            turn.rotate(ax, ang), others, 10.0)
    # no two components overlap
    keys = list(C)
    bad = []
    n = 0
    for i, ka in enumerate(keys):
        for kb in keys[i + 1:]:
            if not _bb_hit(S(ka), S(kb)):
                continue
            n += 1
            v = _vol(S(ka), S(kb))
            if not (v < 1e-2):
                bad.append(f"{ka}/{kb} {v:.1f}")
    rows.append((f"No two components overlap ({n} neighbouring pairs tested)" + (": " + ", ".join(bad) if bad else ""),
                 0.0, 0.0, "touch", not bad))
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:75s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    C = build_components()
    groups = {
        "stepgen-assembly": [c.shape for c in C.values()],
        "stepgen-frame": [C["frame"].shape],
        "stepgen-deck": [C[k].shape for k in ("belt", "front_roller", "rear_roller", "idlers", "carriers", "drag", "sensor")],
        "stepgen-receiver": [C["cradle"].shape],
    }
    for stem, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(root / "step" / f"{stem}.step"))
        export_stl(c, str(root / "stl" / f"{stem}.stl"), tolerance=0.5, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{stem}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    g = geometry()
    print(f"wheelbase {g['wheelbase']:.0f} mm, trail {g['trail']:.1f} mm, usable belt {g['belt_usable']:.0f} mm, "
          f"down tube {g['dt_len']:.0f} mm at {g['dt_ang']:.1f} deg")
    print("wrote " + ", ".join(f"cad/step/{s}.step" for s in groups) + " and matching STL files")
    print_checks()
