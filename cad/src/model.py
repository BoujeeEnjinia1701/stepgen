"""StepGen parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl.

Massing-plus detail: correct interfaces (belt deck, wheel and steering geometry,
SwapCell interface v0.3 receiver with latch class V1 lever) and main dimensions;
not fabrication detail. PRELIMINARY, NOT FOR FABRICATION.

Axes: X is the direction of travel (front is +X), Y is across the vehicle, Z is up.
Rear axle at X = 0, ground at Z = 0. Units mm.

The calculation note (docs/04-calcs/sizing.py, SGN-CAL-001) imports PARAMS and
geometry() from this file, so the numbers and the model share one source.
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Wheels (decided: 20 in, ETRTO 406, front and rear)
    "wheel_r": 247.0,          # 20 x 1.75 in tire, outside diameter about 494 mm
    "tire_r": 22.0,            # tire section radius
    # Belt deck
    "roller_r": 25.0,          # 50 mm crowned end rollers
    "rear_roller_x": 320.0,    # rear end roller centre
    "roller_pitch": 1050.0,    # end roller centres
    "deck_z": 240.0,           # top of the belt above the ground (R8: 250 or less)
    "belt_w": 400.0,           # belt width (R1: 360 or more)
    "belt_t": 3.0,
    "bed_n": 14,               # idler rollers under the top run
    "bed_r": 15.0,             # 30 mm idler rollers
    # Frame
    "rail_y": 235.0,           # deck rail centre line from the vehicle centre line
    "rail_w": 30.0, "rail_h": 60.0, "rail_t": 2.0,   # 60 x 30 x 2 mm RHS on edge (SGN-DDR-002: was 50 x 25 x 2)
    "rail_x0": 270.0, "rail_x1": 1420.0,
    "down_tube_r": 22.0,       # 44 mm tube
    # Steering (TRL 3: fork offset added so trail is about 58 mm)
    "head_angle": 70.0,        # head tube angle from horizontal, degrees
    "head_bot_x": 1680.0, "head_bot_z": 640.0,
    "head_len": 150.0,
    "fork_offset": 30.0,       # rake, perpendicular to the steering axis
    "column_r": 19.0,          # 38 x 2 mm steel steering column (SGN-CAL-001 section 7)
    "bar_x": 1400.0, "bar_z": 1230.0,   # handlebar centre, about 0.99 m above the belt
    "bar_half": 290.0,         # half width over the grips
    # SwapCell pack and receiver (interface v0.3)
    "pack_l": 340.0, "pack_w": 90.0, "pack_d": 80.0,
    "pack_pos": 0.55,          # pack centre along the down tube (fraction of length)
    "cradle_t": 16.0,
    "lever_len": 120.0,        # over-centre lever, class V1 preload 330 N (ratio 6.6 or more)
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
    g["roll_z"] = p["deck_z"] - p["roller_r"]
    g["front_roller_x"] = p["rear_roller_x"] + p["roller_pitch"]
    g["belt_usable"] = p["roller_pitch"] - 2 * p["roller_r"]
    g["length"] = front_x + 2 * R
    g["width"] = 2 * (p["bar_half"] + 16.0)            # grips are 32 mm diameter
    g["bar_above_belt"] = p["bar_z"] - p["deck_z"]
    g["dt_lo"] = (p["rail_x1"] + 60.0, g["roll_z"] - 5.0)
    g["dt_hi"] = hb
    dx, dz = hb[0] - g["dt_lo"][0], hb[1] - g["dt_lo"][1]
    g["dt_len"] = math.hypot(dx, dz)
    g["dt_ang"] = math.degrees(math.atan2(dz, dx))
    # Lowest frame part: the deck cross members
    g["ground_clearance"] = g["roll_z"] - 55.0 - 12.5
    # Lean clearance: outermost low point is the clutch housing on the rear roller
    clutch_y = p["rail_y"] + 45.0 + 22.5
    clutch_z = g["roll_z"] - 38.0
    g["lean_clearance_deg"] = math.degrees(math.atan2(clutch_z, clutch_y))
    return g


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset)."""
    from build123d import Box, Cylinder, Torus, Pos, Rot, Solid, Plane, Vector

    g = geometry(p)
    R, TR, RR = p["wheel_r"], p["tire_r"], p["roller_r"]
    RR_X, FR_X = p["rear_roller_x"], g["front_roller_x"]
    DECK_Z, ROLL_Z, BELT_W = p["deck_z"], g["roll_z"], p["belt_w"]
    RAIL_Y, RAIL_X0, RAIL_X1 = p["rail_y"], p["rail_x0"], p["rail_x1"]
    FRONT_X = g["front_x"]
    HB = (p["head_bot_x"], p["head_bot_z"])
    HT, CT = g["head_top"], g["col_top"]
    BAR = (p["bar_x"], p["bar_z"])
    s_dir, n_dir = g["steer_dir"], g["steer_normal"]

    def tube3(a, b, r):
        a = Vector(*a); b = Vector(*b); d = b - a
        return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))

    def box_x(x0, x1, y, z, w, h):
        return Pos((x0 + x1) / 2, y, z) * Box(x1 - x0, w, h)

    def tyre_rim(cx):
        tyre = Pos(cx, 0, R) * Rot(90, 0, 0) * Torus(R - TR, TR)
        rim = Pos(cx, 0, R) * Rot(90, 0, 0) * (Cylinder(R - 2 * TR, 20) - Cylinder(R - 2 * TR - 14, 22))
        spokes = None
        for k in range(12):
            t = math.radians(k * 30 + 15)
            sp = tube3((cx, 0, R), (cx + (R - 55) * math.cos(t), 0, R + (R - 55) * math.sin(t)), 2.0)
            spokes = sp if spokes is None else spokes + sp
        return tyre + rim + spokes

    # 1 Main frame
    rz = ROLL_Z - 15
    rails = (box_x(RAIL_X0, RAIL_X1, -RAIL_Y, rz, p["rail_w"], p["rail_h"])
             + box_x(RAIL_X0, RAIL_X1, RAIL_Y, rz, p["rail_w"], p["rail_h"]))
    cross = None
    for x in (RAIL_X0 + 15, (RAIL_X0 + RAIL_X1) / 2, RAIL_X1 - 15):
        c = Pos(x, 0, ROLL_Z - 55) * Box(30, 2 * RAIL_Y, 25)
        cross = c if cross is None else cross + c
    rear_stays = (tube3((RAIL_X0, -RAIL_Y, rz), (0, -70, R), 11) + tube3((RAIL_X0, RAIL_Y, rz), (0, 70, R), 11)
                  + tube3((RAIL_X0 + 180, -RAIL_Y, ROLL_Z + 5), (0, -70, R + 10), 9)
                  + tube3((RAIL_X0 + 180, RAIL_Y, ROLL_Z + 5), (0, 70, R + 10), 9))
    dropouts = Pos(0, -70, R) * Box(40, 6, 40) + Pos(0, 70, R) * Box(40, 6, 40)
    DT_LO, DT_HI = g["dt_lo"], g["dt_hi"]
    nose = (tube3((RAIL_X1, -RAIL_Y, rz), (DT_LO[0], -40, DT_LO[1]), 14)
            + tube3((RAIL_X1, RAIL_Y, rz), (DT_LO[0], 40, DT_LO[1]), 14)
            + Pos(DT_LO[0], 0, DT_LO[1]) * Box(40, 110, 30))
    down_tube = tube3((DT_LO[0], 0, DT_LO[1]), (DT_HI[0], 0, DT_HI[1]), p["down_tube_r"])
    head_tube = tube3((HB[0], 0, HB[1]), (HT[0], 0, HT[1]), 22)
    kick = tube3((RAIL_X0 + 160, -RAIL_Y - 20, rz - 5), (RAIL_X0 - 60, -RAIL_Y - 20, rz + 10), 7)   # kickstand, stowed along the rail
    deck_frame = rails + cross + rear_stays + dropouts + nose
    frame = deck_frame + down_tube + head_tube + kick

    # 2 Belt and end rollers
    def roller(x):
        return Pos(x, 0, ROLL_Z) * Rot(90, 0, 0) * Cylinder(RR, BELT_W + 30)

    def axle(x):
        return Pos(x, 0, ROLL_Z) * Rot(90, 0, 0) * Cylinder(8, 2 * RAIL_Y + 40)

    def wrap(x):
        return Pos(x, 0, ROLL_Z) * Rot(90, 0, 0) * (Cylinder(RR + p["belt_t"], BELT_W) - Cylinder(RR, BELT_W + 2))

    bt = p["belt_t"]
    belt = (box_x(RR_X, FR_X, 0, DECK_Z - bt / 2, BELT_W, bt) + box_x(RR_X, FR_X, 0, ROLL_Z - RR + bt / 2, BELT_W, bt)
            + wrap(RR_X) + wrap(FR_X))
    end_rollers = roller(RR_X) + roller(FR_X) + axle(RR_X) + axle(FR_X)

    # 3 Roller bed under the top run
    bed = None
    nb, br = p["bed_n"], p["bed_r"]
    for k in range(nb):
        x = RR_X + 70 + k * (FR_X - RR_X - 140) / (nb - 1)
        r = Pos(x, 0, DECK_Z - bt - br) * Rot(90, 0, 0) * Cylinder(br, BELT_W - 10)
        bed = r if bed is None else bed + r
    bed = bed + box_x(RR_X + 50, FR_X - 50, -BELT_W / 2 + 5, DECK_Z - 18, 10, 30) \
        + box_x(RR_X + 50, FR_X - 50, BELT_W / 2 - 5, DECK_Z - 18, 10, 30)

    # 4 Anti-reverse clutch and belt drag (rear roller, +Y end)
    clutch = Pos(RR_X, RAIL_Y + 45, ROLL_Z) * Rot(90, 0, 0) * Cylinder(38, 45)

    # 5 Belt speed sensor (front roller, -Y end)
    sensor = (Pos(FR_X, -RAIL_Y - 30, ROLL_Z) * Rot(90, 0, 0) * Cylinder(30, 8)
              + Pos(FR_X, -RAIL_Y - 45, ROLL_Z + 40) * Box(30, 20, 30))

    # 6 Rear wheel with geared hub motor
    rear_motor = Pos(0, 0, R) * Rot(90, 0, 0) * Cylinder(85, 80)
    rear_tyre = tyre_rim(0.0)

    # 7 Front wheel, fork (with offset) and headset
    crown = (HB[0] + s_dir[0] * -25, HB[1] + s_dir[1] * -25)
    fork = (tube3((FRONT_X, -55, R), (crown[0], -55, crown[1]), 11)
            + tube3((FRONT_X, 55, R), (crown[0], 55, crown[1]), 11)
            + Pos(crown[0], 0, crown[1]) * Box(45, 130, 25)
            + Pos(FRONT_X, 0, R) * Rot(90, 0, 0) * Cylinder(30, 100))
    front_tyre = tyre_rim(FRONT_X)

    # 8 Steering column, stem, handlebar and grips
    bh = p["bar_half"]
    steering = (tube3((HT[0], 0, HT[1]), (CT[0], 0, CT[1]), p["column_r"])
                + tube3((CT[0], 0, CT[1]), (BAR[0], 0, BAR[1]), 15)
                + tube3((BAR[0], -bh + 20, BAR[1]), (BAR[0], bh - 20, BAR[1]), 11)
                + tube3((BAR[0], -bh + 20, BAR[1]), (BAR[0] - 60, -bh, BAR[1] - 10), 16)
                + tube3((BAR[0], bh - 20, BAR[1]), (BAR[0] - 60, bh, BAR[1] - 10), 16))

    # 9 Brakes: 160 mm rotors, calipers, levers with motor cut-off switches
    brakes_rear = (Pos(0, -95, R) * Rot(90, 0, 0) * (Cylinder(80, 3) - Cylinder(30, 4))
                   + Pos(55, -95, R + 55) * Box(45, 25, 35))
    brakes_front = (Pos(FRONT_X, -70, R) * Rot(90, 0, 0) * (Cylinder(80, 3) - Cylinder(25, 4))
                    + Pos(FRONT_X - 55, -70, R + 55) * Box(45, 25, 35))
    levers = (tube3((BAR[0] - 20, -200, BAR[1] + 5), (BAR[0] - 90, -240, BAR[1] - 15), 6)
              + tube3((BAR[0] - 20, 200, BAR[1] + 5), (BAR[0] - 90, 240, BAR[1] - 15), 6))

    # 10 SwapCell receiver cradle (latch class V1) on the down tube
    L = g["dt_len"]
    ux, uz = (DT_HI[0] - DT_LO[0]) / L, (DT_HI[1] - DT_LO[1]) / L
    nx, nz = -uz, ux

    def on_dt(t, off):
        return (DT_LO[0] + ux * t + nx * off, DT_LO[1] + uz * t + nz * off)

    ang = g["dt_ang"]
    ct = p["cradle_t"]
    pl, pw, pd = p["pack_l"], p["pack_w"], p["pack_d"]
    tc = L * p["pack_pos"]
    c = on_dt(tc, p["down_tube_r"] + ct / 2)
    # base plate, two side guides (1 mm clearance to the pack guide faces), lower end stop with receptacle
    cradle = Pos(c[0], 0, c[1]) * Rot(0, -ang, 0) * (
        Box(pl + 30, pw + 14, ct)
        + Pos(0, (pw + 2) / 2 + 3, ct / 2 + 30) * Box(pl - 40, 6, 60)
        + Pos(0, -(pw + 2) / 2 - 3, ct / 2 + 30) * Box(pl - 40, 6, 60)
        + Pos(-(pl + 30) / 2 + 6, 0, ct / 2 + 35) * Box(12, pw + 14, 70))
    # over-centre lever at the upper end, pressing the pack onto the end stop (preload 330 N or more)
    lv = on_dt(tc + pl / 2 + 20, p["down_tube_r"] + ct + pd - 5)
    lever = Pos(lv[0], 0, lv[1]) * Rot(0, -ang - 35, 0) * Box(p["lever_len"], 30, 10)
    pivot = on_dt(tc + pl / 2 + 22, p["down_tube_r"] + ct + 30)
    lever_post = Pos(pivot[0], 0, pivot[1]) * Rot(0, -ang, 0) * Box(14, 40, 60)
    cradle = cradle + lever + lever_post

    # 11 SwapCell pack (340 x 90 x 80 mm, connector end down the tube)
    pc = on_dt(tc, p["down_tube_r"] + ct + pd / 2)
    pack = Pos(pc[0], 0, pc[1]) * Rot(0, -ang, 0) * Box(pl, pw, pd)
    hd = on_dt(tc + pl / 2 + 17, p["down_tube_r"] + ct + pd / 2)
    pack = pack + Pos(hd[0], 0, hd[1]) * Rot(0, -ang, 0) * Box(34, 84, 22)       # handle zone

    # 12 Controller and walking logic board, under the down tube
    q = on_dt(L * 0.25, -(p["down_tube_r"] + 25))
    controller = Pos(q[0], 0, q[1]) * Rot(0, -ang, 0) * Box(150, 70, 40)

    # 13 Display, level selector, lanyard stop and key switch
    display = (Pos(BAR[0] + 10, 0, BAR[1] + 45) * Rot(0, -20, 0) * Box(25, 110, 70)
               + Pos(BAR[0] - 20, 140, BAR[1] + 10) * Box(35, 30, 30)
               + Pos(BAR[0] - 20, -140, BAR[1] + 12) * Cylinder(16, 30))

    # 14 Guards
    heel = Pos(0, 0, R) * Rot(90, 0, 0) * (Cylinder(R + 45, 70) - Cylinder(R + 40, 72))
    heel = heel & (Pos(R / 2 + 40, 0, R + 200) * Box(R + 110, 100, 400))
    heel = heel + Pos(RAIL_X0 - 5, 0, DECK_Z + 60) * Box(10, BELT_W + 60, 120)
    side_boards = box_x(RAIL_X0, RAIL_X1, -RAIL_Y, DECK_Z + 3, 70, 6) + box_x(RAIL_X0, RAIL_X1, RAIL_Y, DECK_Z + 3, 70, 6)
    cov = lambda x, sgn: (Pos(x, 0, ROLL_Z) * Rot(90, 0, 0) * (Cylinder(RR + 20, BELT_W + 40) - Cylinder(RR + 16, BELT_W + 42))) \
        & (Pos(x + sgn * 60, 0, ROLL_Z) * Box(120, BELT_W + 60, 200))
    toe = Pos(FR_X + 35, 0, DECK_Z + 45) * Rot(0, -20, 0) * Box(8, BELT_W + 60, 90)
    guards = heel + side_boards + cov(RR_X, -1) + cov(FR_X, 1) + toe

    # 15 Wiring harness with fuse
    w0 = (q[0] - 60, -45, q[1] - 20)
    harness = (tube3(w0, (RAIL_X1 - 40, -RAIL_Y + 20, ROLL_Z - 45), 5)
               + tube3((RAIL_X1 - 40, -RAIL_Y + 20, ROLL_Z - 45), (RAIL_X0 + 20, -RAIL_Y + 20, ROLL_Z - 45), 5)
               + tube3((RAIL_X0 + 20, -RAIL_Y + 20, ROLL_Z - 45), (5, -60, R + 30), 5))
    harness_up = (tube3((HT[0], -24, HT[1]), (CT[0], -24, CT[1] - 20), 5)
                  + tube3((CT[0], -24, CT[1] - 20), (BAR[0] + 5, -60, BAR[1] - 10), 5)
                  + tube3(w0, (HB[0] - 40, -40, HB[1] - 30), 5)
                  + tube3((HB[0] - 40, -40, HB[1] - 30), (HT[0], -24, HT[1]), 5))

    return [
        ("Main frame", frame, "#4B5563", 1, (0, 0, -260)),
        ("Belt and end rollers", belt + end_rollers, "#111827", 2, (0, 0, 420)),
        ("Roller bed", bed, "#94A3B8", 3, (0, 0, 180)),
        ("Anti-reverse clutch and belt drag", clutch, "#D4A017", 4, (250, 700, 250)),
        ("Belt speed sensor", sensor, "#0EA5E9", 5, (0, -420, 280)),
        ("Rear wheel with 250 W geared hub motor", rear_motor, "#0F766E", 6, (-160, 0, -380)),
        ("Rear tire and rim (with item 6)", rear_tyre, "#1F2937", None, (-160, 0, -380)),
        ("Front wheel, fork and headset", fork, "#6B7280", 7, (480, 0, -80)),
        ("Front tire and rim (with item 7)", front_tyre, "#1F2937", None, (480, 0, -80)),
        ("Steering column, handlebar and grips", steering, "#374151", 8, (300, 0, 380)),
        ("Brakes with motor cut-off levers", brakes_rear, "#B91C1C", 9, (-160, -300, -380)),
        ("Front brake (with item 9)", brakes_front, "#B91C1C", None, (480, 0, -80)),
        ("Brake levers (with item 9)", levers, "#B91C1C", None, (300, 0, 380)),
        ("SwapCell receiver cradle, class V1", cradle, "#7C3AED", 10, (240, 0, 330)),
        ("SwapCell pack (not in parts cost)", pack, "#C2410C", 11, (330, 0, 620)),
        ("Controller and walking logic board", controller, "#115E59", 12, (220, -420, -220)),
        ("Display, selector, lanyard, key switch", display, "#2563EB", 13, (420, 0, 560)),
        ("Guards (heel, roller, side, toe)", guards, "#CBD5E1", 14, (250, 520, 80)),
        ("Wiring harness with fuse", harness, "#1F2937", 15, (0, -420, -200)),
        ("Harness to the handlebar (with item 15)", harness_up, "#1F2937", None, (0, -420, -200)),
    ], deck_frame


def assembly(parts):
    from build123d import Compound
    kids = []
    for name, shape, *_ in parts:
        shape.label = name
        kids.append(shape)
    return Compound(children=kids, label="StepGen assembly")


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    import copy
    parts, _ = build_parts()
    by = {n: copy.copy(s) for n, s, *_ in parts}   # copies, so the sub-assemblies do not re-parent the parts
    asm = assembly(parts)
    groups = {
        "stepgen-assembly": asm,
        "stepgen-frame": by["Main frame"],
        "stepgen-deck": Compound(children=[by["Belt and end rollers"], by["Roller bed"],
                                           by["Anti-reverse clutch and belt drag"], by["Belt speed sensor"]]),
        "stepgen-receiver": by["SwapCell receiver cradle, class V1"],
    }
    for stem, shape in groups.items():
        export_step(shape, str(root / "step" / f"{stem}.step"))
        export_stl(shape, str(root / "stl" / f"{stem}.stl"))
    g = geometry()
    bb = asm.bounding_box()
    print(f"length {bb.size.X:.0f} mm (geometry {g['length']:.0f}), width {bb.size.Y:.0f} mm, height {bb.size.Z:.0f} mm")
    print(f"wheelbase {g['wheelbase']:.0f} mm, trail {g['trail']:.1f} mm, usable belt {g['belt_usable']:.0f} mm")
    print("wrote " + ", ".join(f"cad/step/{s}.step" for s in groups) + " and matching STL files")
