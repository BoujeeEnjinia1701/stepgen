"""StepGen product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: painted steel frame with rounded rectangular deck rails,
a teal pinstripe and wordmark; treadmill belt with a fine tread on crowned end rollers and the idler
bed; light grey guards with rubber foot pads on the side boards; 20 in wheels with laced spokes,
treaded tires and drilled disc rotors; the 250 W geared hub motor with its cover, bolt circle and
torque arms; the anti-reverse clutch; the belt-speed sensor under a clear cap that shows its magnet
ring; the controller in a finned case with a clear side window over the walking logic board and a lit
status light; the SwapCell pack (interface v0.3) in its class V1 cradle with the teal over-centre
lever and a lit charge bar; and the handlebar with ribbed grips, brake levers with cut-off switches,
a lit display, the level selector, the key switch and the coiled lanyard. Context is the shared clay
mannequin walking on the belt with both hands on the grips.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, geometry() and build_parts() in model.py.
Axes as model.py: X is the direction of travel (front is +X), Y is across the vehicle (the rider's
left is +Y), Z is up; rear axle at X = 0, ground at Z = 0. Units mm.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Align, Axis, Box, Compound, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere,
                       Text, Torus, Vector, extrude, fillet)
from model import PARAMS, geometry

TITLE = "StepGen: walking-treadmill e-bike with a 250 W hub motor"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 22, "az": -52,
     "note": "Product render from the front right and above (about 22 deg elevation); the rider walks on the belt "
             "between the wheels with both hands on the grips, SwapCell pack on the down tube, hub motor at the rear"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): belt and end rollers, idler bed, "
             "guards and foot pads above the frame; hub motor wheel at the rear; fork and front wheel ahead; steering "
             "column and handlebar controls; SwapCell pack and cradle; controller, sensor and clutch at the sides"},
    {"name": "detail", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 16, "az": -128,
     "note": "Detail from the rear right, slightly above (about 16 deg elevation), without the rider: 250 W hub motor "
             "and rear disc brake at left, heel guard and fender, belt deck with its foot pads, SwapCell pack with its "
             "charge bar lit and the handlebar controls at right"},
]

FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

# Colours (restrained product palette; kit accent)
C_FRAME = "#30353C"      # painted steel
C_GUARD = "#DCDFE3"      # HDPE guards
C_PAD = "#1D2024"        # rubber foot pads
C_ACCENT = "#0F766E"
C_BELT = "#16181B"
C_TIRE = "#1A1C1F"
C_RIM = "#B8BEC6"
C_SPOKE = "#9EA5AD"
C_MOTOR = "#24282E"
C_ALU = "#C3C8CE"
C_METAL = "#A9AFB7"
C_DARK = "#2B2F36"
C_BLACK = "#15181C"
C_WINDOW = "#DCEBF5"
C_PCB = "#166534"
C_CHIP = "#111827"
C_LED_G = "#22C55E"
C_LCD = "#5EEAD4"
C_LIGHT = "#2DD4BF"
C_LABEL = "#F4F4F2"
C_WHITE = "#F3F4F6"
C_TRAY = "#4B5563"
C_LID = "#E5E7EB"
C_RED = "#B91C1C"
C_MAGNET = "#3A4048"
C_CLAY = "#9CA3AF"

G = geometry()


# ------------------------------------------------------------------ helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _tube(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    """Round tube through `points` with spherical joints."""
    out = None
    for a, c in zip(points, points[1:]):
        seg = _tube(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _comp(shapes):
    shapes = [s for s in shapes if s is not None]
    return Compound(children=shapes)


def _text(pl, txt, size, h):
    try:
        return extrude(pl * Text(txt, font_size=size, font_path=FONT, align=(Align.CENTER, Align.CENTER)),
                       amount=h)
    except Exception:
        return None


def _hex_y(x, y, z, af, h):
    """Hex prism along Y (across flats `af`), centred on (x, y, z)."""
    return Pos(x, y - h / 2, z) * Rot(-90, 0, 0) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


# ------------------------------------------------------------------ wheels
def _wheel(cx, R, TR, flange_r, flange_y, n_spokes=28):
    """Tire (torus) with tread blocks, rim with a brake-free profile, laced spokes and a valve."""
    tire = Pos(cx, 0, R) * Rot(90, 0, 0) * Torus(R - TR, TR)
    blocks = []
    nb = 72
    for k in range(nb):
        th = 360.0 * k / nb
        dy = 5.0 if k % 2 else -5.0
        blocks.append(Pos(cx, 0, R) * Rot(0, th, 0) * Pos(0, dy * 0.7, R - 0.9) * Box(8.0, 10.0, 2.2))
    tread = _comp(blocks)
    rim_o, rim_i = R - 2 * TR + 2.0, R - 2 * TR - 14.0
    rim = Pos(cx, 0, R) * Rot(90, 0, 0) * (Cylinder(rim_o, 22) - Cylinder(rim_i, 24))
    rim -= Pos(cx, 0, R) * Rot(90, 0, 0) * (Cylinder(rim_o + 1, 12) - Cylinder(rim_o - 2.5, 13))   # bead seat channel
    spokes = []
    for k in range(n_spokes):
        side = 1 if k % 2 else -1
        a0 = math.radians(360.0 * k / n_spokes)
        a1 = a0 + math.radians(24.0 * (1 if (k // 2) % 2 else -1))
        p0 = (cx + flange_r * math.cos(a0), side * flange_y, R + flange_r * math.sin(a0))
        p1 = (cx + (rim_i + 1) * math.cos(a1), side * 4.0, R + (rim_i + 1) * math.sin(a1))
        spokes.append(_tube(p0, p1, 1.0))
    valve = _tube((cx, 0, R + rim_i - 6), (cx, 0, R + rim_i + 20), 3.0)
    return tire, tread, rim, _comp(spokes), valve


# ------------------------------------------------------------------ mannequin
def _rider_joints(P):
    """Walk pose (shortened stride to stay on the 1.0 m usable belt) with hands solved onto the grips."""
    from context_parts import mannequin_landmarks
    legs = dict(hip_flex_l=16.0, knee_flex_l=5.0, ankle_flex_l=4.0,
                hip_flex_r=-8.0, knee_flex_r=30.0, ankle_flex_r=6.0, torso_lean=6.0, head_tilt=-4.0)
    px = P["rider_x"]
    bh, bx, bz = P["bar_half"], P["bar_x"], P["bar_z"]
    grips = {"l": (bx - 32, bh - 12, bz - 6), "r": (bx - 32, -(bh - 12), bz - 6)}

    def local(w):                       # world to mannequin frame (figure faces -Y, left at +X)
        return (w[1], -(w[0] - px), w[2] - P["deck_z"])

    j = dict(legs)
    for side in "lr":
        tgt = local(grips[side])
        x = [12.0, 75.0, 20.0]
        idx = 0 if side == "l" else 1

        def err(v):
            jj = dict(j)
            jj[f"shoulder_flex_{side}"], jj[f"elbow_flex_{side}"], jj[f"shoulder_abd_{side}"] = v
            h = mannequin_landmarks(1750, "push", **jj)["hands"][idx]
            return sum((a - b) ** 2 for a, b in zip(h, tgt))
        # coordinate descent (keeps the model free of a SciPy dependency)
        step = 8.0
        best = err(x)
        while step > 0.02:
            moved = False
            for i in range(3):
                for s in (1, -1):
                    y = list(x)
                    y[i] += s * step
                    e = err(y)
                    if e < best:
                        best, x, moved = e, y, True
            if not moved:
                step /= 2
        j[f"shoulder_flex_{side}"], j[f"elbow_flex_{side}"], j[f"shoulder_abd_{side}"] = x
    return j


# ------------------------------------------------------------------ parts
def product_parts(P=PARAMS, with_rider=True):
    g = geometry(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    R, TR, RR = P["wheel_r"], P["tire_r"], P["roller_r"]
    RR_X, FR_X = P["rear_roller_x"], g["front_roller_x"]
    DECK_Z, ROLL_Z, BW = P["deck_z"], g["roll_z"], P["belt_w"]
    RY, RX0, RX1 = P["rail_y"], P["rail_x0"], P["rail_x1"]
    FX = g["front_x"]
    HB = (P["head_bot_x"], P["head_bot_z"])
    HT, CT = g["head_top"], g["col_top"]
    BAR = (P["bar_x"], P["bar_z"])
    s_dir = g["steer_dir"]
    rz = ROLL_Z - 15                         # rail centre height, as model.py

    # explode offsets (vehicle scale)
    E_FRAME = (0, 0, 0)
    E_BELT = (0, 0, 520)
    E_BED = (0, 0, 300)
    E_GUARD = (0, 0, 150)
    E_REAR = (-420, 0, 0)
    E_FRONT = (480, 0, 0)
    E_STEER = (260, 0, 420)
    E_CTRLS = (260, 0, 560)
    E_CRADLE = (120, 0, 240)
    E_PACK = (200, 0, 560)
    E_CTRL = (120, -420, -120)
    E_HARN = (0, -300, -200)

    # ============================================================ 1 main frame (painted steel)
    def rail(y):
        r = _box((RX0 + RX1) / 2, y, rz, RX1 - RX0, P["rail_w"], P["rail_h"])
        return _fillet_try(r, _edges_par(r, Axis.X), [4.0, 3.0, 2.0])

    frame = rail(-RY) + rail(RY)
    for x in (RX0 + 15, (RX0 + RX1) / 2, RX1 - 15):
        c = _box(x, 0, ROLL_Z - 55, 30, 2 * RY, 25)
        c = _fillet_try(c, _edges_par(c, Axis.Y), [3.0, 2.0])
        frame += c
    for sy in (-1, 1):
        frame += _pipe([(RX0 + 10, sy * RY, rz), (0, sy * 70, R)], 11)
        frame += _pipe([(RX0 + 180, sy * RY, ROLL_Z + 5), (0, sy * 70, R + 10)], 9)
        d = _box(0, sy * 70, R, 40, 6, 40)
        d = _fillet_try(d, _edges_par(d, Axis.Y), [8.0, 5.0])
        frame += d
    DT_LO, DT_HI = g["dt_lo"], g["dt_hi"]
    for sy in (-1, 1):
        frame += _pipe([(RX1 - 10, sy * RY, rz), (DT_LO[0], sy * 40, DT_LO[1])], 14)
    nose = _box(DT_LO[0], 0, DT_LO[1], 40, 110, 30)
    frame += _fillet_try(nose, _edges_par(nose, Axis.Y), [6.0, 4.0])
    frame += _tube((DT_LO[0], 0, DT_LO[1]), (DT_HI[0], 0, DT_HI[1]), P["down_tube_r"])
    frame += Pos(DT_HI[0], 0, DT_HI[1]) * Sphere(P["down_tube_r"])
    frame += _tube((HB[0], 0, HB[1]), (HT[0], 0, HT[1]), 22)
    add("Main frame (painted steel)", frame, C_FRAME, "painted", 1, "shell", E_FRAME)

    # headset cups
    cups = None
    for (pt, sgn) in ((HB, -1), (HT, 1)):
        a = Vector(pt[0], 0, pt[1])
        dv = Vector(s_dir[0], 0, s_dir[1]) * sgn
        c = Solid.make_cylinder(24.5, 9.0, Plane(origin=a, z_dir=dv))
        cups = c if cups is None else cups + c
    add("Headset cups", cups, C_METAL, "metal", 7, "shell", E_FRAME)

    # pinstripe and wordmark on both rail outer faces
    stripe = None
    for sy in (-1, 1):
        s = _box((RX0 + RX1) / 2 + 20, sy * (RY + P["rail_w"] / 2 + 0.2), rz - 18, RX1 - RX0 - 120, 0.6, 6)
        stripe = s if stripe is None else stripe + s
    add("Rail pinstripe (teal)", stripe, C_ACCENT, "painted", 1, "shell", E_FRAME)
    yface = -(RY + P["rail_w"] / 2)
    wm = _text(Plane(origin=(RX1 - 250, yface, rz + 6), x_dir=(1, 0, 0), z_dir=(0, -1, 0)), "STEPGEN", 26, 0.6)
    if wm is not None:
        add("Wordmark decal", wm, C_WHITE, "paper", 1, "shell", E_FRAME)
    # no rating decal: the "250 W 25 km/h" rating stays off the renders until the legal category is confirmed (SGN-DEC-001, 2026-10-02)

    # kickstand, stowed along the left-hand (-Y) rail (BOM 16)
    k0, k1 = (RX0 + 160, -RY - 20, rz - 5), (RX0 - 60, -RY - 20, rz + 10)
    kick = _tube(k0, k1, 7) + Pos(*k1) * Sphere(7)
    kick += _box(RX0 + 150, -RY - 12, rz - 5, 40, 16, 22)
    foot = _box(RX0 - 66, -RY - 20, rz + 10, 18, 26, 8)
    kick += _fillet_try(foot, _edges_par(foot, Axis.Z), [3.0, 2.0])
    add("Side kickstand (stowed)", kick, C_DARK, "painted", 16, "shell", (0, -200, -120))

    # ============================================================ 2 belt and end rollers
    bt = P["belt_t"]
    top = _box((RR_X + FR_X) / 2, 0, DECK_Z - bt / 2, FR_X - RR_X, BW, bt)
    bot = _box((RR_X + FR_X) / 2, 0, ROLL_Z - RR + bt / 2, FR_X - RR_X, BW, bt)
    wraps = None
    for x in (RR_X, FR_X):
        w = Pos(x, 0, ROLL_Z) * Rot(90, 0, 0) * (Cylinder(RR + bt, BW) - Cylinder(RR, BW + 2))
        wraps = w if wraps is None else wraps + w
    belt = top + bot + wraps
    add("Treadmill belt", belt, C_BELT, "rubber", 2, "shell", E_BELT)
    ribs = []
    n = int((FR_X - RR_X) / 16)
    for k in range(n):
        x = RR_X + 8 + k * (FR_X - RR_X - 16) / (n - 1)
        ribs.append(_box(x, 0, DECK_Z + 0.35, 3.0, BW - 24, 0.7))
    add("Belt tread texture", _comp(ribs), "#202328", "rubber", 2, "shell", E_BELT)

    rolls = None
    for x in (RR_X, FR_X):
        r = _ycyl(x, 0, ROLL_Z, RR, BW + 30)
        r = _fillet_try(r, r.edges(), [2.0, 1.0])
        r += _ycyl(x, 0, ROLL_Z, 8, 2 * RY + 40)
        rolls = r if rolls is None else rolls + r
    add("End rollers and axles", rolls, C_ALU, "metal", 2, "internal", E_BELT)
    nuts = None
    for x in (RR_X, FR_X):
        for sy in (-1, 1):
            h = _hex_y(x, sy * (RY + P["rail_w"] / 2 + 4), ROLL_Z, 17, 8)
            nuts = h if nuts is None else nuts + h
    add("Roller axle nuts", nuts, C_METAL, "metal", 2, "shell", E_FRAME)

    # ============================================================ 3 roller bed
    bed = []
    nb, br = P["bed_n"], P["bed_r"]
    for k in range(nb):
        x = RR_X + 70 + k * (FR_X - RR_X - 140) / (nb - 1)
        r = _ycyl(x, 0, DECK_Z - bt - br, br, BW - 10)
        bed.append(r)
    add("Idler rollers (14)", _comp(bed), C_ALU, "metal", 3, "internal", E_BED)
    carriers = None
    for sy in (-1, 1):
        a = _box((RR_X + FR_X) / 2, sy * (BW / 2 - 5), DECK_Z - 18, FR_X - RR_X - 100, 10, 30)
        a -= _box((RR_X + FR_X) / 2, sy * (BW / 2 - 5) - sy * 3, DECK_Z - 14, FR_X - RR_X - 90, 6, 30)
        carriers = a if carriers is None else carriers + a
    add("Roller bed carriers (aluminium angle)", carriers, C_ALU, "metal", 3, "internal", E_BED)

    # ============================================================ 4 anti-reverse clutch (+Y end of the rear roller)
    cy_ = RY + 45
    cl = _ycyl(RR_X, cy_, ROLL_Z, 38, 45)
    cl = _fillet_try(cl, cl.edges(), [5.0, 3.0])
    for k in range(10):
        a = math.radians(36 * k)
        cl -= _box(RR_X + 38 * math.cos(a), cy_, ROLL_Z + 38 * math.sin(a), 5, 30, 5).rotate(
            Axis((RR_X + 38 * math.cos(a), cy_, ROLL_Z + 38 * math.sin(a)), (0, 1, 0)), -math.degrees(a))
    add("Anti-reverse clutch housing", cl, C_DARK, "metal", 4, "internal", (0, 380, 300))
    cap = _ycyl(RR_X, cy_ + 23.5, ROLL_Z, 22, 3)
    cap = _fillet_try(cap, cap.edges(), [1.0, 0.5])
    add("Clutch cap and drag knob", cap + _ycyl(RR_X, cy_ + 28, ROLL_Z, 9, 8), C_ACCENT, "plastic", 4, "internal",
        (0, 420, 300))

    # ============================================================ 5 belt speed sensor (-Y end of the front roller)
    sy_ = -RY - 30
    ES = (0, -400, 300)
    base = _ycyl(FR_X, sy_ + 2.5, ROLL_Z, 30, 3)
    add("Sensor base plate", base, C_DARK, "plastic", 5, "internal", ES)
    mags = None
    for k in range(8):
        a = math.radians(45 * k + 22.5)
        m = _ycyl(FR_X + 20 * math.cos(a), sy_ - 1.0, ROLL_Z + 20 * math.sin(a), 4.0, 3.0)
        mags = m if mags is None else mags + m
    mags += _ycyl(FR_X, sy_ - 0.5, ROLL_Z, 12, 2.0)
    add("Magnet ring (8 magnets)", mags, C_MAGNET, "metal", 5, "internal", ES)
    cap = _ycyl(FR_X, sy_ - 1.5, ROLL_Z, 30, 5) - _ycyl(FR_X, sy_ + 0.5, ROLL_Z, 28.5, 5)
    cap = _fillet_try(cap, cap.faces().sort_by(Axis.Y)[0].edges(), [2.0, 1.0])
    add("Sensor clear cap", cap, C_WINDOW, "clear", 5, "internal", (0, -470, 300))
    hs = _box(FR_X, -RY - 45, ROLL_Z + 40, 30, 20, 30)
    hs = _fillet_try(hs, hs.edges(), [4.0, 2.0])
    add("Hall sensor housing", hs, C_DARK, "plastic", 5, "internal", ES)
    led = _ycyl(FR_X + 7, -RY - 55.3, ROLL_Z + 48, 2.2, 1.2)
    add("Sensor pulse light (lit)", led, C_LED_G, "emissive", 5, "internal", ES)

    # ============================================================ 6 rear wheel with geared hub motor
    tire, tread, rim, spokes, valve = _wheel(0.0, R, TR, 72.0, 36.0)
    add("Rear tire", tire, C_TIRE, "rubber", 6, "shell", E_REAR)
    add("Rear tire tread", tread, C_TIRE, "rubber", 6, "shell", E_REAR)
    add("Rear rim", rim, C_RIM, "metal", 6, "shell", E_REAR)
    add("Rear spokes", spokes, C_SPOKE, "metal", 6, "shell", E_REAR)
    add("Rear valve", valve, C_METAL, "metal", 6, "shell", E_REAR)
    hub = _ycyl(0, 0, R, 85, 80)
    hub = _fillet_try(hub, hub.edges(), [14.0, 10.0, 6.0])
    for sy in (-1, 1):
        hub += _ycyl(0, sy * 36, R, 80, 4)
    add("Hub motor shell (250 W, geared)", hub, C_MOTOR, "painted", 6, "shell", E_REAR)
    covers, bolts = None, None
    for sy in (-1, 1):
        c = _ycyl(0, sy * 42, R, 52, 6)
        c = _fillet_try(c, c.faces().sort_by(Axis.Y)[0 if sy < 0 else -1].edges(), [3.0, 1.5])
        covers = c if covers is None else covers + c
        for k in range(6):
            a = math.radians(60 * k + 30)
            b = _ycyl(42 * math.cos(a), sy * 45.5, R + 42 * math.sin(a), 3.0, 1.6)
            bolts = b if bolts is None else bolts + b
    add("Hub motor side covers", covers, C_ALU, "metal", 6, "shell", E_REAR)
    add("Hub motor cover screws", bolts, C_DARK, "metal", 6, "shell", E_REAR)
    band = _ycyl(0, -20, R, 85.6, 6) - _ycyl(0, -20, R, 80, 8)
    add("Hub motor accent band", band, C_ACCENT, "painted", 6, "shell", E_REAR)
    axle = _ycyl(0, 0, R, 6, 170)
    for sy in (-1, 1):
        axle += _hex_y(0, sy * 79, R, 18, 7)
    add("Rear axle and nuts", axle, C_METAL, "metal", 6, "shell", E_REAR)
    arms = None
    for sy in (-1, 1):
        t = Pos(0, sy * 76, R) * Rot(0, -35, 0) * Pos(35, 0, 0) * Box(90, 4, 22)
        t = _fillet_try(t, _edges_par(t, Axis.Y), [6.0, 3.0])
        arms = t if arms is None else arms + t
    add("Torque arms", arms, C_DARK, "metal", 6, "shell", E_REAR)
    cable = _pipe([(0, 60, R), (40, 95, R + 30), (RX0 - 20, RY - 10, rz + 20)], 4.0)
    add("Motor cable", cable, C_BLACK, "rubber", 6, "shell", E_REAR)

    # ============================================================ 7 front wheel, fork and headset
    tire, tread, rim, spokes, valve = _wheel(FX, R, TR, 22.0, 34.0, 28)
    add("Front tire", tire, C_TIRE, "rubber", 7, "shell", E_FRONT)
    add("Front tire tread", tread, C_TIRE, "rubber", 7, "shell", E_FRONT)
    add("Front rim", rim, C_RIM, "metal", 7, "shell", E_FRONT)
    add("Front spokes", spokes, C_SPOKE, "metal", 7, "shell", E_FRONT)
    add("Front valve", valve, C_METAL, "metal", 7, "shell", E_FRONT)
    fhub = _ycyl(FX, 0, R, 18, 90)
    for sy in (-1, 1):
        fhub += _ycyl(FX, sy * 34, R, 24, 3)
    fhub += _ycyl(FX, -44, R, 26, 6)
    add("Front hub (disc)", fhub, C_ALU, "metal", 7, "shell", E_FRONT)
    crown = (HB[0] - s_dir[0] * 25, HB[1] - s_dir[1] * 25)
    fork = None
    for sy in (-1, 1):
        leg = _pipe([(FX, sy * 55, R), (crown[0], sy * 55, crown[1])], 11)
        leg += _box(FX, sy * 55, R, 26, 8, 30)
        fork = leg if fork is None else fork + leg
    cr = _box(crown[0], 0, crown[1], 45, 130, 25)
    cr = _fillet_try(cr, _edges_par(cr, Axis.Y), [10.0, 6.0])
    cr = _fillet_try(cr, _edges_par(cr, Axis.X), [4.0, 2.0])
    fork += cr
    add("Fork (painted steel)", fork, C_FRAME, "painted", 7, "shell", E_FRONT)
    fax = _ycyl(FX, 0, R, 5, 130)
    for sy in (-1, 1):
        fax += _hex_y(FX, sy * 62, R, 15, 6)
    add("Front axle and nuts", fax, C_METAL, "metal", 7, "shell", E_FRONT)

    # ============================================================ 9 brakes (rotors, calipers)
    def rotor(cx, y):
        r = _ycyl(cx, y, R, 80, 2.0) - _ycyl(cx, y, R, 58, 3)
        for k in range(18):
            a = math.radians(20 * k)
            r -= _ycyl(cx + 69 * math.cos(a), y, R + 69 * math.sin(a), 3.2, 3)
        spider = _ycyl(cx, y, R, 30, 2.4) - _ycyl(cx, y, R, 12, 3)
        for k in range(6):
            a = math.radians(60 * k)
            spider += _tube((cx + 20 * math.cos(a), y, R + 20 * math.sin(a)),
                            (cx + 62 * math.cos(a + 0.3), y, R + 62 * math.sin(a + 0.3)), 4.5)
        return r + spider

    def caliper(x, y, z):
        c = _box(x, y, z, 45, 25, 35)
        c = _fillet_try(c, c.edges(), [6.0, 4.0, 2.0])
        c -= _box(x, y, z - 12, 50, 6, 20)
        return c

    add("Rear brake rotor (160 mm)", rotor(0, -95), C_METAL, "metal", 9, "shell", (E_REAR[0], -120, 0))
    carrier = _ycyl(0, -67, R, 30, 56)
    add("Rear rotor carrier", carrier, C_DARK, "metal", 9, "shell", (E_REAR[0], -120, 0))
    add("Rear brake caliper", caliper(55, -95, R + 55), C_DARK, "painted", 9, "shell", (E_REAR[0], -160, 60))
    add("Front brake rotor (160 mm)", rotor(FX, -70), C_METAL, "metal", 9, "shell", (E_FRONT[0], -120, 0))
    add("Front brake caliper", caliper(FX - 55, -70, R + 55), C_DARK, "painted", 9, "shell",
        (E_FRONT[0], -160, 60))

    # ============================================================ 8 steering column, stem, bar and grips
    bh = P["bar_half"]
    steer = _tube((HT[0], 0, HT[1]), (CT[0], 0, CT[1]), P["column_r"])
    steer += Pos(CT[0], 0, CT[1]) * Sphere(P["column_r"])
    steer += _tube((CT[0], 0, CT[1]), (BAR[0], 0, BAR[1]), 15)
    add("Steering column and stem (painted steel)", steer, C_FRAME, "painted", 8, "shell", E_STEER)
    bar = _tube((BAR[0], -bh + 20, BAR[1]), (BAR[0], bh - 20, BAR[1]), 11)
    for sy in (-1, 1):
        bar += Pos(BAR[0], sy * (bh - 20), BAR[1]) * Sphere(11)
        bar += _tube((BAR[0], sy * (bh - 20), BAR[1]), (BAR[0] - 60, sy * bh, BAR[1] - 10), 11)
    add("Handlebar (580 mm)", bar, C_DARK, "metal", 8, "shell", E_STEER)
    clamp = _box(BAR[0], 0, BAR[1], 44, 52, 40)
    clamp = _fillet_try(clamp, clamp.edges(), [10.0, 6.0, 3.0])
    add("Stem bar clamp", clamp, C_ALU, "metal", 8, "shell", E_STEER)
    grips, plugs = None, None
    for sy in (-1, 1):
        a = Vector(BAR[0], sy * (bh - 20), BAR[1]) + (Vector(-60, sy * 20, -10) * 0.12)
        b = Vector(BAR[0] - 60, sy * bh, BAR[1] - 10) + (Vector(-60, sy * 20, -10).normalized() * 6)
        d = (b - a)
        L = d.length
        pl = Plane(origin=a, z_dir=d.normalized())
        gsh = Solid.make_cylinder(16, L, pl)
        for k in range(1, 9):
            ring = Solid.make_cylinder(17, 1.6, Plane(origin=a + d.normalized() * (L * k / 9.0 - 0.8),
                                                      z_dir=d.normalized()))
            ring -= Solid.make_cylinder(14.8, 1.6, Plane(origin=a + d.normalized() * (L * k / 9.0 - 0.8),
                                                         z_dir=d.normalized()))
            gsh -= ring
        flange = Solid.make_cylinder(19, 4, Plane(origin=a - d.normalized() * 4, z_dir=d.normalized()))
        gsh += flange
        grips = gsh if grips is None else grips + gsh
        pg = Solid.make_cylinder(15, 4, Plane(origin=b, z_dir=d.normalized()))
        plugs = pg if plugs is None else plugs + pg
    add("Grips (ribbed rubber)", grips, C_BLACK, "rubber", 8, "shell", E_CTRLS)
    add("Bar end plugs", plugs, C_ACCENT, "plastic", 8, "shell", E_CTRLS)

    # brake levers with cut-off switches (BOM 9)
    levers, bodies = None, None
    for sy in (-1, 1):
        body = _box(BAR[0] - 4, sy * 205, BAR[1] + 4, 34, 26, 30)
        body = _fillet_try(body, body.edges(), [6.0, 4.0, 2.0])
        bodies = body if bodies is None else bodies + body
        blade = _pipe([(BAR[0] - 20, sy * 200, BAR[1] + 5), (BAR[0] - 55, sy * 222, BAR[1] - 4),
                       (BAR[0] - 90, sy * 240, BAR[1] - 15)], 5)
        levers = blade if levers is None else levers + blade
    add("Brake lever bodies with cut-off switches", bodies, C_DARK, "plastic", 9, "shell", E_CTRLS)
    add("Brake lever blades", levers, C_METAL, "metal", 9, "shell", E_CTRLS)

    # display (BOM 13): same envelope and tilt as model.py; screen on the rider side (-X)
    dpl = Pos(BAR[0] + 10, 0, BAR[1] + 45) * Rot(0, -20, 0)
    disp = Box(25, 110, 70)
    disp = _fillet_try(disp, _edges_par(disp, Axis.X), [8.0, 5.0])
    disp = _fillet_try(disp, disp.faces().sort_by(Axis.X)[-1].edges(), [4.0, 2.0])
    add("Display housing", dpl * disp, C_BLACK, "plastic", 13, "shell", E_CTRLS)
    glass = Pos(-12.6, 0, 3) * Box(0.8, 92, 50)
    add("Display glass", dpl * glass, "#0E1216", "screen", 13, "shell", E_CTRLS)
    rd = (Pos(-13.1, 14, 10) * Box(0.3, 44, 16) + Pos(-13.1, -26, 12) * Box(0.3, 22, 6)
          + Pos(-13.1, -26, 2) * Box(0.3, 22, 3) + Pos(-13.1, 0, -14) * Box(0.3, 80, 4))
    add("Display readout (lit)", dpl * rd, C_LCD, "emissive", 13, "shell", E_CTRLS)
    dmark = Pos(13.1, 0, 22) * Box(0.4, 60, 6)
    add("Display front badge", dpl * dmark, C_ACCENT, "painted", 13, "shell", E_CTRLS)

    # level selector on the left bar (+Y)
    sel = _box(BAR[0] - 20, 140, BAR[1] + 10, 35, 30, 30)
    sel = _fillet_try(sel, sel.edges(), [6.0, 4.0, 2.0])
    add("Level selector pod", sel, C_DARK, "plastic", 13, "shell", E_CTRLS)
    btns = None
    for k, x in enumerate((-10, 0, 10)):
        b = Pos(BAR[0] - 20 + x, 140, BAR[1] + 26) * Cylinder(3.8, 3)
        b = _fillet_try(b, b.faces().sort_by(Axis.Z)[-1].edges(), [1.0, 0.5])
        btns = b if btns is None else btns + b
    add("Level buttons", btns, C_ACCENT, "rubber", 13, "shell", E_CTRLS)
    ld = Pos(BAR[0] - 20 - 12, 140, BAR[1] + 18) * Sphere(2.2) & _box(BAR[0] - 34, 140, BAR[1] + 18, 6, 6, 6)
    add("Ready light (lit)", ld, C_LED_G, "emissive", 13, "shell", E_CTRLS)

    # key switch and magnetic lanyard stop on the right bar (-Y)
    kx, ky, kz = BAR[0] - 20, -140, BAR[1] + 12
    ks = Pos(kx, ky, kz) * Cylinder(16, 30)
    ks = _fillet_try(ks, ks.edges(), [3.0, 1.5])
    add("Key switch and lanyard stop body", ks, C_DARK, "plastic", 13, "shell", E_CTRLS)
    kf = Pos(kx, ky, kz + 15.5) * Cylinder(9, 2) - Pos(kx, ky, kz + 16.5) * Box(1.6, 8, 3)
    key = Pos(kx, ky, kz + 24) * Box(2, 7, 14) + Pos(kx, ky, kz + 35) * Box(3, 18, 12)
    add("Key cylinder and key", kf + key, C_METAL, "metal", 13, "shell", E_CTRLS)
    puck = _tube((kx - 16, ky, kz), (kx - 30, ky, kz), 11)
    puck = _fillet_try(puck, puck.edges(), [2.0, 1.0])
    add("Lanyard magnet puck", puck, C_RED, "plastic", 13, "shell", E_CTRLS)
    coils = []
    top_c = Vector(kx - 34, ky, kz - 8)
    for k in range(9):
        c = top_c + Vector(-2.0 * k, 0.0, -7.5 * k)
        coils.append(Pos(*c) * Rot(0, -12, 0) * (Cylinder(8.6, 3.2) - Cylinder(5.4, 4)))
    coils.append(Pos(*(top_c + Vector(-18, 0, -72))) * Box(10, 6, 16))       # clip
    add("Lanyard coiled cord", _comp(coils), C_RED, "fabric", 13, "shell", E_CTRLS)

    # ============================================================ 10 SwapCell cradle and 11 pack (down tube frame)
    L = g["dt_len"]
    ux, uz = (DT_HI[0] - DT_LO[0]) / L, (DT_HI[1] - DT_LO[1]) / L
    nx, nz = -uz, ux
    ang = g["dt_ang"]

    def on_dt(t, off):
        return (DT_LO[0] + ux * t + nx * off, DT_LO[1] + uz * t + nz * off)

    def place(t, off, shape):
        c = on_dt(t, off)
        return Pos(c[0], 0, c[1]) * Rot(0, -ang, 0) * shape

    ct = P["cradle_t"]
    pl, pw, pd = P["pack_l"], P["pack_w"], P["pack_d"]
    tc = L * P["pack_pos"]
    base = Box(pl + 30, pw + 14, ct)
    base = _fillet_try(base, _edges_par(base, Axis.Z), [8.0, 5.0])
    for sy in (-1, 1):
        gd = Pos(0, sy * ((pw + 2) / 2 + 3), ct / 2 + 30) * Box(pl - 40, 6, 60)
        gd = _fillet_try(gd, _edges_par(gd, Axis.Y), [8.0, 4.0])
        base += gd
    stop = Pos(-(pl + 30) / 2 + 6, 0, ct / 2 + 35) * Box(12, pw + 14, 70)
    base += _fillet_try(stop, _edges_par(stop, Axis.X), [4.0, 2.0])
    add("SwapCell receiver cradle, class V1", place(tc, P["down_tube_r"] + ct / 2, base), C_DARK, "painted", 10,
        "shell", E_CRADLE)
    post = Box(14, 40, 60)
    post = _fillet_try(post, _edges_par(post, Axis.Y), [5.0, 3.0])
    add("Latch lever post", place(tc + pl / 2 + 22, P["down_tube_r"] + ct + 30, post), C_DARK, "painted", 10,
        "shell", E_CRADLE)
    lv = on_dt(tc + pl / 2 + 20, P["down_tube_r"] + ct + pd - 5)
    lev = Box(P["lever_len"], 30, 10)
    lev = _fillet_try(lev, _edges_par(lev, Axis.Z), [8.0, 5.0])
    lev = _fillet_try(lev, _edges_par(lev, Axis.Y), [3.0, 2.0])
    add("Over-centre latch lever", Pos(lv[0], 0, lv[1]) * Rot(0, -ang - 35, 0) * lev, C_ACCENT, "painted", 10,
        "shell", (E_CRADLE[0] + 80, 0, E_CRADLE[2] + 420))
    pivot = place(tc + pl / 2 + 22, P["down_tube_r"] + ct + 30, Pos(0, 0, 18) * Rot(90, 0, 0) * Cylinder(5, 46))
    add("Lever pivot pin", pivot, C_METAL, "metal", 10, "shell", E_CRADLE)
    straps = None
    for t in (tc - 120, tc + 120):
        st = place(t, 0, Rot(0, 90, 0) * (Cylinder(P["down_tube_r"] + 3, 24) - Cylinder(P["down_tube_r"] - 1, 26)))
        straps = st if straps is None else straps + st
    add("Cradle tube clamps", straps, C_DARK, "painted", 10, "shell", E_CRADLE)

    # pack (SwapCell visual language: grey tray, light lid, lit charge bar), centred as model.py
    poff = P["down_tube_r"] + ct + pd / 2
    tray = Box(pl, pw, pd * 0.55)
    tray = _fillet_try(tray, _edges_par(tray, Axis.Z), [10.0, 6.0])
    tray = _fillet_try(tray, tray.faces().sort_by(Axis.Z)[0].edges(), [4.0, 2.0])
    tray = Pos(0, 0, -pd / 2 + pd * 0.275) * tray
    lid = Box(pl, pw, pd * 0.45 - 1.0)
    lid = _fillet_try(lid, _edges_par(lid, Axis.Z), [10.0, 6.0])
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Z)[-1].edges(), [6.0, 4.0, 2.0])
    lid = Pos(0, 0, pd / 2 - (pd * 0.45 - 1.0) / 2) * lid
    add("SwapCell pack tray", place(tc, poff, tray), C_TRAY, "painted", 11, "accessory", E_PACK)
    add("SwapCell pack lid", place(tc, poff, lid), C_LID, "plastic", 11, "accessory", E_PACK)
    bar_c = Pos(20, -pw / 2 - 0.3, pd / 2 - 16) * Box(120, 1.2, 8)
    add("Pack charge bar frame", place(tc, poff, bar_c), C_BLACK, "plastic", 11, "accessory", E_PACK)
    segs = None
    for k in range(4):
        sgm = Pos(-24 + 24 * k + 20 - 16, -pw / 2 - 0.8, pd / 2 - 16) * Box(20, 0.6, 5)
        segs = sgm if segs is None else segs + sgm
    add("Pack charge bar (lit)", place(tc, poff, segs), C_LIGHT, "emissive", 11, "accessory", E_PACK)
    lab = Pos(-90, -pw / 2 - 0.3, -6) * Box(110, 0.6, 30)
    add("Pack interface label", place(tc, poff, lab), C_LABEL, "paper", 11, "accessory", E_PACK)
    ink = (Pos(-118, -pw / 2 - 0.7, 0) * Box(40, 0.4, 8) + Pos(-80, -pw / 2 - 0.7, -2) * Box(50, 0.4, 3)
           + Pos(-90, -pw / 2 - 0.7, -12) * Box(90, 0.4, 3))
    add("Pack label print", place(tc, poff, ink), C_ACCENT, "paper", 11, "accessory", E_PACK)
    hdl = Box(34, 84, 22)
    hdl = _fillet_try(hdl, hdl.edges(), [8.0, 5.0, 3.0])
    for k in range(5):
        hdl -= Pos(-12 + 6 * k, 0, 11) * Box(2.2, 90, 2.4)
    add("Pack carry handle (ribbed)", place(tc + pl / 2 + 17, poff, hdl), C_BLACK, "rubber", 11, "accessory", E_PACK)

    # ============================================================ 12 controller in a finned case with a side window
    qt, qo = L * 0.25, -(P["down_tube_r"] + 25)
    cw, cdp, chh = 150.0, 70.0, 40.0
    case = Box(cw, cdp, chh)
    case = _fillet_try(case, _edges_par(case, Axis.X), [6.0, 4.0])
    case = _fillet_try(case, _edges_par(case, Axis.Y) + _edges_par(case, Axis.Z), [3.0, 1.5])
    case -= Box(cw - 5, cdp - 5, chh - 5)
    case -= Pos(0, -cdp / 2, 0) * Box(104, 8, 22)                    # window opening (-Y side)
    for k in range(7):                                               # fins on the underside
        case += Pos(0, -24 + 8 * k, -chh / 2 - 3) * Box(cw - 20, 2.2, 6)
    add("Controller case (finned aluminium)", place(qt, qo, case), C_DARK, "metal", 12, "internal", E_CTRL)
    pane = Pos(0, -cdp / 2 + 1.2, 0) * Box(110, 1.6, 28)
    add("Controller clear window", place(qt, qo, pane), C_WINDOW, "clear", 12, "internal", E_CTRL)
    pcb = Pos(0, 4, 0) * Box(cw - 12, 1.6, chh - 12)
    add("Walking logic board", place(qt, qo, pcb), C_PCB, "plastic", 12, "internal", E_CTRL)
    chips = (Pos(-30, -2, 2) * Box(26, 8, 18) + Pos(10, -1, -4) * Box(14, 5, 10) + Pos(40, -1.5, 4) * Box(10, 6, 8)
             + Pos(-2, -5, 8) * Rot(90, 0, 0) * Cylinder(4, 12) + Pos(26, -4, -6) * Box(8, 10, 8))
    add("Logic board components", place(qt, qo, chips), C_CHIP, "plastic", 12, "internal", E_CTRL)
    shield = Pos(-30, -6.5, 2) * Box(22, 1.0, 14)
    add("ESP32 module shield", place(qt, qo, shield), C_METAL, "metal", 12, "internal", E_CTRL)
    sled = Pos(52, -3, 8) * Sphere(2.6) & Pos(52, -3, 8) * Box(6, 6, 6)
    add("Controller status light (lit)", place(qt, qo, sled), C_LED_G, "emissive", 12, "internal", E_CTRL)
    glands = None
    for sx in (-1, 1):
        for y in (-14, 14):
            gl = Pos(sx * (cw / 2 + 5), y, 0) * Rot(0, 90, 0) * Cylinder(7, 10)
            glands = gl if glands is None else glands + gl
    add("Controller cable glands", place(qt, qo, glands), C_BLACK, "rubber", 12, "internal", E_CTRL)
    tabs = None
    for x in (-50, 50):
        tb = Pos(x, 0, chh / 2 + 2.5) * Box(18, 30, 5)
        tabs = tb if tabs is None else tabs + tb
    add("Controller mounting tabs", place(qt, qo, tabs), C_DARK, "metal", 12, "internal", E_CTRL)

    # ============================================================ 14 guards
    heel = Pos(0, 0, R) * Rot(90, 0, 0) * (Cylinder(R + 45, 70) - Cylinder(R + 40, 72))
    heel &= Pos(R / 2 + 40, 0, R + 200) * Box(R + 110, 100, 400)
    heel = _fillet_try(heel, heel.edges(), [1.8, 1.0])
    add("Rear fender", heel, C_GUARD, "plastic", 14, "shell", (-300, 0, 260))
    hp = _box(RX0 - 5, 0, DECK_Z + 60, 10, BW + 60, 120)
    hp = _fillet_try(hp, _edges_par(hp, Axis.X), [12.0, 8.0])
    hp = _fillet_try(hp, hp.faces().sort_by(Axis.X)[-1].edges(), [2.0, 1.0])
    add("Heel guard", hp, C_GUARD, "plastic", 14, "shell", (-220, 0, 300))
    refl = _box(RX0 - 10.4, 0, DECK_Z + 80, 0.8, 90, 22)
    add("Rear reflector", refl, "#9F1D1D", "plastic", 14, "shell", (-220, 0, 300))
    sb = None
    for sy in (-1, 1):
        b = _box((RX0 + RX1) / 2, sy * RY, DECK_Z + 3, RX1 - RX0, 70, 6)
        b = _fillet_try(b, _edges_par(b, Axis.X), [2.5, 1.5])
        b = _fillet_try(b, _edges_par(b, Axis.Z), [8.0, 4.0])
        sb = b if sb is None else sb + b
    add("Side boards", sb, C_GUARD, "plastic", 14, "shell", E_GUARD)
    pads = []
    for sy in (-1, 1):
        for k in range(int((RX1 - RX0 - 80) / 12)):
            pads.append(_box(RX0 + 46 + 12 * k, sy * (RY + 4), DECK_Z + 6.6, 5.0, 50, 1.2))
    add("Foot pad ribs (rubber)", _comp(pads), C_PAD, "rubber", 14, "shell", E_GUARD)
    for x, sgn, nm in ((RR_X, -1, "Rear roller cover"), (FR_X, 1, "Front roller cover")):
        c = Pos(x, 0, ROLL_Z) * Rot(90, 0, 0) * (Cylinder(RR + 20, BW + 40) - Cylinder(RR + 16, BW + 42))
        c &= Pos(x + sgn * 60, 0, ROLL_Z) * Box(120, BW + 60, 200)
        c = _fillet_try(c, c.edges(), [1.2, 0.6])
        add(nm, c, C_GUARD, "plastic", 14, "shell", (sgn * 160, 0, 380))
    toe = Pos(FR_X + 35, 0, DECK_Z + 45) * Rot(0, -20, 0) * Box(8, BW + 60, 90)
    toe = _fillet_try(toe, toe.edges(), [2.5, 1.5])
    add("Toe guard", toe, C_GUARD, "plastic", 14, "shell", (260, 0, 320))
    tstripe = Pos(FR_X + 39.5, 0, DECK_Z + 60) * Rot(0, -20, 0) * Box(0.8, BW + 20, 10)
    add("Toe guard accent", tstripe, C_ACCENT, "painted", 14, "shell", (260, 0, 320))
    gscr = None
    for x in (RX0 + 60, (RX0 + RX1) / 2, RX1 - 60):
        for sy in (-1, 1):
            sc = Pos(x, sy * (RY + 24), DECK_Z + 6.8) * Cylinder(4.0, 1.6)
            gscr = sc if gscr is None else gscr + sc
    add("Side board screws", gscr, C_METAL, "metal", 16, "shell", E_GUARD)

    # ============================================================ 15 wiring harness with fuse
    q = on_dt(qt, qo)
    w0 = (q[0] - 60, -45, q[1] - 20)
    har = _pipe([w0, (RX1 - 40, -RY + 20, ROLL_Z - 45), (RX0 + 20, -RY + 20, ROLL_Z - 45), (5, -60, R + 30)], 4.5)
    har += _pipe([w0, (HB[0] - 40, -40, HB[1] - 30), (HT[0], -26, HT[1]), (CT[0], -26, CT[1] - 20),
                  (BAR[0] + 5, -60, BAR[1] - 10)], 4.0)
    add("Wiring harness", har, C_BLACK, "rubber", 15, "internal", E_HARN)
    fuse = _box(RX1 - 120, -RY + 20, ROLL_Z - 45, 44, 16, 22)
    fuse = _fillet_try(fuse, fuse.edges(), [4.0, 2.0])
    add("Sealed fuse holder (20 A)", fuse, C_RED, "plastic", 15, "internal", E_HARN)
    ties = None
    for t in (0.2, 0.5, 0.8):
        x = RX1 - 40 + t * (RX0 + 20 - (RX1 - 40))
        tie = Pos(x, -RY + 20, ROLL_Z - 45) * Rot(0, 90, 0) * (Cylinder(6.5, 3) - Cylinder(4.5, 4))
        ties = tie if ties is None else ties + tie
    add("Cable ties", ties, C_BLACK, "plastic", 16, "internal", E_HARN)

    # ============================================================ context: clay mannequin walking on the belt
    if with_rider:
        from context_parts import mannequin
        j = _rider_joints(P)
        person = Pos(P["rider_x"], 0, DECK_Z) * Rot(0, 0, 90) * mannequin(1750, "push", **j)
        add("Rider, 1.75 m (clay mannequin, walking)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:10.2f} cm3")
