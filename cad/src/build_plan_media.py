"""StepGen prototype build plan pictures (SGN-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...] [only=NN,NN]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/SGN-DWG-101 to 114        making sketches for the made components
    docs/05-build-plan/rail-holes.png      hole and slot positions in the deck rails
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as M  # noqa: E402
from model import PARAMS as P, build_components, geometry, derived, bx, fuse, steer_plane, dt_plane  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
G = geometry()
D = derived()
C = build_components()
FX, R = G["front_x"], P["wheel_r"]
RRX, FRX, RZ = P["rear_roller_x"], G["front_roller_x"], G["roll_z"]
ONLY = None
for a in sys.argv[1:]:
    if a.startswith("only="):
        ONLY = {int(x) for x in a[5:].split(",")}


def want(n):
    return ONLY is None or n in ONLY


def S(*ks):
    return fuse([C[k].shape for k in ks])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def P_(key, name=None, explode=(0, 0, 0)):
    return part(name or C[key].name, C[key].shape, C[key].color, explode)


FRM = "#A8A29E"       # frame steel in close-ups, lighter so the parts on it stand out


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & bx(x0, x1, y0, y1, z0, z1)


# sub-shapes the model keeps together
RING = C["sensor"].shape & bx(FRX - 30, FRX + 30, -213.5, -209.5, 150, 260)
HALL = C["sensor"].shape - bx(FRX - 30, FRX + 30, -213.5, -209.5, 150, 260)
ROT_F = C["rotors"].shape & bx(FX - 100, FX + 100, -100, 100, 0, 600)
ROT_R = C["rotors"].shape & bx(-100, 100, -100, 100, 0, 600)
TAB_L = C["frame"].shape & bx(-100, -19, -80, -60, 170, 250)


# ----------------------------------------------------------------- named parts, in build order
def made():
    m = [
        ("frame", P_("frame", "Main frame (welded)")),
        ("kick", P_("kickstand")),
        ("carriers", P_("carriers", "Idler carrier bars (2)")),
        ("belt", P_("belt")),
        ("front_roller", part("Front end roller with magnet ring", C["front_roller"].shape + RING, C["front_roller"].color)),
        ("rear_roller", P_("rear_roller", "Rear end roller, one-way bearing, tension bolts")),
        ("idlers", P_("idlers")),
        ("drag", P_("drag")),
        ("hall", part("Hall sensor on its bracket", HALL, C["sensor"].color)),
        ("fork", P_("fork")),
        ("column", P_("column")),
        ("bar", part("Handlebar, grips, levers, controls", S("bar", "levers", "controls"), C["bar"].color)),
        ("front_wheel", part("Front wheel, rotor and caliper", C["front_wheel"].shape + ROT_F + C["caliper_f"].shape, C["front_wheel"].color)),
        ("rear_wheel", part("Rear wheel with hub motor, rotor, torque arms", S("rear_wheel", "torque_arms") + ROT_R, C["rear_wheel"].color)),
        ("caliper_r", P_("caliper_r")),
        ("controller", P_("controller")),
        # the harness with its run inside the left rail drawn too, so pulled out it reads as one cable
        ("harness", part(C["harness"].name, C["harness"].shape + M.tube3((P["rail_x0"] + 60, -(P["rail_y"] + 15) - 6, 196.0),
                                                                         (P["rail_x1"] - 15, -(P["rail_y"] + 15) - 6, 196.0), 3.5),
                         C["harness"].color)),
        ("cradle", P_("cradle")),
        ("covers", P_("covers")),
        ("heel", P_("heel")),
        ("fender", P_("fender")),
        ("toe", P_("toe")),
        ("boards", P_("boards")),
        ("pack", P_("pack")),
    ]
    return dict(m)


# ----------------------------------------------------------------- overview
def overview():
    Mp = made()
    off = {"frame": (0, 0, 0), "kick": (0, -330, -160), "carriers": (0, 0, 300), "belt": (0, 0, 620),
           "front_roller": (300, 0, 620), "rear_roller": (-300, 0, 620), "idlers": (0, 0, 450), "drag": (-80, 420, 150),
           "hall": (80, -420, 40), "fork": (380, 0, -40), "column": (380, 0, 330), "bar": (380, 0, 560),
           "front_wheel": (760, 0, -150), "rear_wheel": (-560, 0, -40), "caliper_r": (-560, -260, -330),
           "controller": (330, -450, -170), "harness": (0, -700, -330), "cradle": (120, 480, 380), "covers": (0, 0, 830),
           "heel": (-330, 0, 420), "fender": (-640, 0, 420), "toe": (480, 0, 420), "boards": (0, 0, 1000), "pack": (120, 760, 700)}
    # the Hall sensor and the rear caliper are too small to show under a number badge, so here they are
    # drawn with the part they sit on (as the front caliper is with the front wheel)
    Mp["front_roller"] = part("Front end roller, magnet ring, Hall sensor", Mp["front_roller"].shape + HALL, C["front_roller"].color)
    Mp["rear_wheel"] = part("Rear wheel, hub motor, rotor, torque arms, caliper", Mp["rear_wheel"].shape + C["caliper_r"].shape,
                            C["rear_wheel"].color)
    del Mp["hall"], Mp["caliper_r"]
    parts = []
    for k, p in Mp.items():
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "StepGen prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front left and above; the SwapCell pack (22) is fitted last",
                       elev=20, azim=-62, size=(14, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def flat(shape, pl):
    return pl.to_local_coords(shape)


def sheets():
    import build123d as b
    Mp = made()
    base = dict(project="StepGen", date=DATE)
    out = []
    fr = C["frame"].shape
    yi, yo = P["rail_y"] - 15, P["rail_y"] + 15
    X0, X1, Z0 = P["rail_x0"], P["rail_x1"], P["rail_z0"]
    deck = [Mp["belt"], Mp["idlers"], Mp["carriers"]]

    def sheet(n, part_, neigh, title, material, notes, **kw):
        if want(n):
            out.append(bv.component_sheet(part_, neigh, dwg_no=f"SGN-DWG-{n}", title=title, material=material, notes=notes,
                                          **base, **kw))

    # 101 deck rail (right; the left rail is its mirror image)
    rail_r = win(fr, X0 + 0.01, X1 - 0.01, yi - 0.01, yo + 0.01, Z0 + 0.01, Z0 + 59.99)
    sheet(101, Part("Deck rail", rail_r, "#4B5563"), [Mp["belt"], Mp["idlers"], Mp["front_roller"], Mp["rear_roller"]],
          "StepGen deck rail (make 2, a right and a left): making sketch", "Mild steel RHS 60 x 30 x 2 mm, S235 class, 1150 mm",
          view_shape=b.Pos(-X0, -P["rail_y"], -Z0) * rail_r, inset_view=(22, 60),
          notes=["Cut two 1150 mm lengths of 60 x 30 x 2 RHS, square ends. Stand them",
                 "  on edge (60 mm tall). The right and left rails are mirror images.",
                 "Distances from the rear end; heights from the bottom face.",
                 "Rear axle slot through both side walls: 17 mm tall, 30 to 75 mm",
                 "  from the rear end, centred 42 mm up. Drill 17 mm at each end, saw out.",
                 "Front axle hole through both walls: 10.5 mm, 1100 mm from the rear",
                 "  end, 42 mm up; weld a 16 x 3 mm tube 26 mm long inside between them.",
                 "Inside wall: four 9 mm holes for M6 rivet nuts at 130, 430, 730 and",
                 "  1020 mm, 25 mm up (carrier bars).",
                 "Top face: four 9 mm holes for M6 rivet nuts on the centre line at",
                 "  90, 430, 770 and 1090 mm (side board spacers).",
                 "Right rail only: 8.5 mm hole through both walls at 50 mm, 22 mm up,",
                 "  and an M8 nut welded over it outside (drag screw).",
                 "Left rail only: 12 mm grommet holes in the outer wall at 60 and 1135 mm,",
                 "  26 mm up (harness), and two M3 rivet nuts inside at 1092 and 1108 mm,",
                 "  16 mm up (sensor bracket). Full layout: picture rail-holes.png."])

    # 102 cross members and nose beam
    xm = fuse([win(fr, cx + 0.01, cx + 30.1, -yo - 0.1, yo + 0.1, Z0 - 25.1, Z0 - 0.01) for cx in P["cross_x"]])
    nose = win(fr, X1 + 0.01, X1 + 60.1, -yo - 0.1, yo + 0.1, Z0 - 0.1, Z0 + 39.99)
    sheet(102, Part("Cross members and nose beam", xm + nose, "#4B5563"), [Mp["frame"]],
          "StepGen cross members (make 2) and nose beam: making sketch", "Mild steel RHS 25 x 25 x 2 mm and 60 x 40 x 2 mm",
          view_shape=b.Pos(-X0, 0, -Z0) * (xm + nose), inset_view=(-25, -60),
          notes=["Cross members: cut two 500 mm lengths of 25 x 25 x 2 RHS.",
                 "  They are welded under the rails, flush with the rails' outer faces:",
                 "  rear one 0 to 30 mm from the rails' rear ends, middle one 560 to 590.",
                 "  Drill two 9 mm holes in the top face of the rear one for M6 rivet",
                 "  nuts, 80 mm each side of centre, 14 mm from its front face (heel guard).",
                 "Nose beam: cut 500 mm of 60 x 40 x 2 RHS, lying flat (40 mm tall).",
                 "  Its rear face butts the front ends of both rails, bottoms flush,",
                 "  outer ends flush with the rails' outer faces.",
                 "  The down tube stands on the middle of its top face (sheet 103).",
                 "  Four 9 mm holes in the top for M6 rivet nuts, 12 mm from the rear",
                 "  face, 80 and 180 mm each side of centre (toe guard flanges).",
                 "Cap every open RHS end with 2 mm plate, welded all round."])

    # 103 down tube, laid flat along its axis
    DP = dt_plane()
    dtube = (fr & M.tube3((G["dt_lo"][0], 0, G["dt_lo"][1] - 60), (G["dt_hi"][0], 0, G["dt_hi"][1]), P["down_tube_r"] + 0.05)) \
        - bx(1300, 1800, -100, 100, 0, G["nose_top"] + 0.01) - M.lcyl(steer_plane(), -60, 210, P["head_r"])
    dt_flat = flat(dtube, DP)
    bb = dt_flat.bounding_box()
    sheet(103, Part("Down tube", dtube, "#4B5563"), [Mp["frame"], Mp["cradle"], Mp["controller"]],
          "StepGen down tube: making sketch", "Mild steel tube 44 x 2 mm, S235 class",
          view_shape=dt_flat, inset_view=(15, -70),
          notes=[f"Cut 44 x 2 mm tube about {bb.size.X + 20:.0f} mm long and trim to fit.",
                 f"It rises at {G['dt_ang']:.1f} degrees from the nose beam to the head tube.",
                 f"Foot: cut at {90 - G['dt_ang']:.1f} degrees off square so it stands flat on",
                 "  the nose beam's top, centred on the beam (30 mm from its rear face).",
                 "Top: fish-mouth it onto the 50 mm head tube at 40.5 degrees included",
                 "  angle (print a tube-mitre template). Its axis meets the head tube's",
                 "  axis 100 mm above the head tube's bottom end.",
                 f"Centre to centre along its axis: {G['dt_len']:.0f} mm.",
                 "Welded on later (sheet 105): two cradle tabs on its top (rider side),",
                 "  and the controller plate on its left side, low down.",
                 "Check: with the frame in the jig, the tube sits flat on the beam and",
                 "  the head tube's angle reads 70 degrees from the ground plane."])

    # 104 rear stays and dropouts (left side shown; the right side has no caliper tab)
    stays = win(fr, -100, X0 + 0.1, -yo - 1, -60, 140, 290)
    sheet(104, Part("Rear stays and dropouts", stays, "#4B5563"), [Mp["frame"], Mp["rear_wheel"]],
          "StepGen rear stays and dropouts (left side shown): making sketch",
          "Steel tube 22 x 1.6 mm; dropouts 6 mm steel plate", view_shape=stays, inset_view=(15, -110),
          notes=["Dropouts: two 60 x 60 mm pieces of 6 mm plate. Slot each from the",
                 "  bottom edge: 12.2 mm wide, round end 30 mm up (the axle centre).",
                 "  The left one carries a caliper tab 75 x 60 mm on its rear edge.",
                 "  Set them 135 mm apart inside (motor axle width) on a dummy axle.",
                 "Upper stays (2): 22 x 1.6 tube about 290 mm, from the rail end cap",
                 "  (centred 35 mm up the cap) to the dropout's front edge, 2 mm below",
                 "  the axle line.",
                 "Lower stays (2): about 282 mm, from the rear cross member's rear face",
                 "  (35 mm in from the rail's outer face, 13 mm up) to the dropout,",
                 "  14 mm below the axle line.",
                 "Each stay's dropout end is slotted 6 mm to take the plate; trim any",
                 "  tube inside the plate's inner face so the hub fits.",
                 "Caliper tab: drill the two post-mount holes with the caliper and rotor",
                 "  in place (step 12), 74 mm apart, 6.5 mm."])

    # 105 small welded parts
    parts_small = []
    pieces = [
        ("end caps", win(fr, X0 - 3.05, X0 + 0.01, yi - 0.1, yo + 0.1, Z0 - 0.1, Z0 + 60.1), (0, 0, 0)),
        ("tension lugs", win(fr, X0 + 1.9, X0 + 12.1, yo - 0.01, yo + 13.1, RZ - 10.1, RZ + 10.1), (60, 0, 0)),
        ("kickstand plate", win(fr, P["kick_x"] - 25.1, P["kick_x"] + 25.1, -yo - 4.1, -yo + 0.01, 171, 209), (0, 0, 0)),
    ]
    for _, sh, _o in pieces:
        parts_small.append(sh)
    tabs = fr & fuse([M.lbox(DP, t - 20.1, t + 20.1, -15.1, 15.1, 21.0, P["cradle_off"] + 0.1) for t in (D["tc"] - 120, D["tc"] + 120)])
    cplate = fr & M.lbox(DP, P["ctrl_t"][0] - 5.1, P["ctrl_t"][1] + 5.1, -24.6, -22.3, -25.1, 25.1)
    lay = (b.Pos(-X0, -P["rail_y"], -Z0) * parts_small[0] + b.Pos(-X0 + 60, -P["rail_y"], -Z0) * parts_small[1]
           + b.Pos(-P["kick_x"] + 160, yo, -Z0) * parts_small[2]
           + b.Pos(260, 0, 0) * flat(tabs, b.Plane(origin=DP.from_local_coords((D["tc"], 0, 0)), x_dir=DP.x_dir, z_dir=DP.z_dir))
           + b.Pos(260, 120, 0) * flat(cplate, b.Plane(origin=DP.from_local_coords((P["ctrl_t"][0], 0, 0)), x_dir=DP.x_dir, z_dir=(0, -1, 0))))
    sheet(105, Part("Small welded parts", fuse(parts_small) + tabs + cplate, "#4B5563"), [Mp["frame"]],
          "StepGen small welded parts: making sketch", "Mild steel plate and flat bar, S235 class",
          view_shape=lay, inset_view=(20, -60),
          notes=["End caps (2): 60 x 30 x 3 mm plate, welded over the rails' rear ends;",
                 "  the upper stays land on them.",
                 "Tension lugs (2): 20 x 13 x 10 mm, cut from 20 x 10 flat bar; 8.5 mm",
                 "  hole along the rail, 7 mm out from the rail. Weld to the outer face",
                 "  of each rail 2 to 12 mm from its rear end, centred 42 mm up.",
                 "Kickstand plate: 50 x 36 x 4 mm, on the left rail's outer face 225 to",
                 "  275 mm from its rear end, 2 mm up; drill to suit the kickstand.",
                 "Cradle tabs (2): 40 mm of 30 x 12 flat bar, one face filed to a 22 mm",
                 "  radius to sit on the down tube; top 10 mm above the tube. Drill",
                 "  5 mm and tap M6 through. Centres 240 mm apart, the lower one",
                 f"  {D['tc'] - 120:.0f} mm up the tube from its foot, on its rider side.",
                 "Controller plate: 160 x 50 x 3 mm on the down tube's left side,",
                 "  from 20 to 180 mm up the tube; four holes to suit the controller.",
                 "Grind every weld on a surface another part sits on flat."])

    # 106 frame weld-up
    sheet(106, Part("Main frame", fr, "#4B5563"), [Mp["belt"], Mp["rear_wheel"], Mp["front_wheel"], Mp["fork"]],
          "StepGen main frame: weld-up sketch", "Welded mild steel, S235 class; paint after welding",
          inset_view=(22, -58),
          notes=["Weld on a flat table in this order, tacking everything first:",
                 "1. Rails on edge, parallel, 440 mm apart inside; cross members under",
                 "  them; nose beam across their front ends. Check the diagonals agree",
                 "  within 2 mm, then weld.",
                 "2. Head tube held in a jig at 70 degrees, its bottom end 640 mm above the",
                 "  table plane under the wheels (470 mm above the rails' underside),",
                 "  1410 mm ahead of the rails' rear ends, on the centre line.",
                 "3. Down tube between the nose beam and the head tube (sheet 103).",
                 "4. Dropouts on a dummy 135 mm axle, axle 77 mm above the rails' underside",
                 "  and 270 mm behind their rear ends; then the four stays.",
                 "5. End caps, lugs, plates, tabs and nuts (sheet 105).",
                 "Weld in short runs, alternating sides, to limit distortion.",
                 "Check: rails flat and parallel within 2 mm; head tube on the centre line",
                 "  within 1 mm; rear axle square to the centre line; then paint."])

    # 107 carrier bar
    car = C["carriers"].shape & bx(300, 1400, 210, 230, 150, 260)
    car_bar = car & bx(300, 1400, P["carrier_y"] - 0.01, P["carrier_y"] + 3.1, 150, 260)
    sheet(107, Part("Idler carrier bar", car_bar, C["carriers"].color), [Mp["frame"], Mp["idlers"]],
          "StepGen idler carrier bar (make 2): making sketch", "Aluminium flat bar 50 x 3 mm, 6060 or 6063 class",
          view_shape=b.Pos(-360, -P["carrier_y"], -182) * car_bar, inset_view=(25, 60),
          notes=["Cut two 970 mm lengths of 50 x 3 mm aluminium flat bar.",
                 "Distances from the rear end; heights from the bottom edge.",
                 "Idler axle holes: fourteen at 30 mm, then every 70 mm (to 940 mm),",
                 "  40 mm up. Size them to the rollers' spring axles (8.2 mm for 8 mm round",
                 "  axles; for hex axles use a matching hex hole).",
                 "Screw holes: four 6.5 mm at 40, 340, 640 and 930 mm, 13 mm up.",
                 "Drill the two bars clamped together so every hole matches.",
                 "Fit: the bar sits flat on the rail's inside wall, its bottom edge",
                 "  12 mm above the rail's underside, rear end 90 mm from the rail's rear",
                 "  end; four M6 button-head screws into rivet nuts.",
                 "Check: the bars are parallel, 434 mm apart inside."])

    # 108 sensor bracket
    br = HALL & bx(FRX - 11, FRX + 11, -220.1, -217.51, 180, 205)
    sheet(108, Part("Sensor bracket", br, C["sensor"].color), [Mp["frame"], Mp["front_roller"], Mp["hall"]],
          "StepGen Hall sensor bracket: making sketch", "Aluminium plate 2.5 mm", view_shape=b.Pos(-FRX, 220, -183) * br,
          inset_view=(10, 120),
          notes=["Cut a 20 x 16 mm piece of 2.5 mm aluminium plate.",
                 "Two 3.2 mm holes, 2 mm from the short edges, 3 mm up from the bottom.",
                 "Glue or screw the Hall sensor to its face, centred 11 mm up,",
                 "  sensing face outward, 3 mm proud of the bracket.",
                 "Fit: on the left rail's inside wall, centred under the front axle,",
                 "  bottom 13 mm above the rail's underside, with two M3 screws into",
                 "  rivet nuts. The sensor then faces the magnet ring on the roller end",
                 "  18 mm below the axle, with a 1.5 mm air gap.",
                 "Check: turn the roller by hand; the sensor light (or a meter)",
                 "  shows 8 pulses per turn."])

    # 109 steering column, in the steering axis frame
    SP = steer_plane()
    col = C["column"].shape
    sheet(109, Part("Steering column", col, C["column"].color), [Mp["fork"], Mp["frame"], Mp["bar"]],
          "StepGen steering column: making sketch", "Steel tube 38 x 2, 33.7 x 2.3, 30 x 2 and 26.9 x 2.3 mm",
          view_shape=flat(col, SP), inset_view=(15, -70),
          notes=["Clamp sleeve: 80 mm of 33.7 x 2.3 tube (bore 29.1 mm, a slip fit on",
                 "  the 28.6 mm steerer). Saw a 3 mm slot 50 mm up from its bottom at",
                 "  the back; weld two 13 x 6 x 30 mm lugs either side, drill 6.5 and",
                 "  tap one M6, for two M6 clamp bolts.",
                 "Column: 38 x 2 tube 441 mm long; it slides 30 mm over the sleeve's top",
                 "  and is welded all round; 3 mm cap plate on its top.",
                 "Stem: 53 mm of 30 x 2 tube, horizontal, welded to the column's back,",
                 "  its centre 20 mm below the column top.",
                 "Bar clamp: 40 mm of 26.9 x 2.3 tube (bore 22.3), crosswise on the",
                 "  stem's end, slotted underneath with two M6 bolts like the sleeve.",
                 "Fit: the sleeve sits on the headset top cover and clamps the steerer;",
                 "  the bar centre ends up 1230 mm above the ground.",
                 "Check: column and steerer in line within 1 mm over 400 mm."])

    # 110 receiver cradle, in the down tube frame
    cr = C["cradle"].shape
    sheet(110, Part("Receiver cradle", cr, C["cradle"].color), [Mp["frame"], Mp["pack"]],
          "StepGen receiver cradle with lever: making sketch", "Steel sheet 3 mm, plate 12 mm, flat bar 30 x 8 mm",
          view_shape=flat(cr, DP), inset_view=(10, 130),
          notes=["Channel: one 3 mm blank 370 mm long, folded to a 98 mm wide base with",
                 "  60 mm walls (inside 92 mm: 1 mm clearance each side of the pack).",
                 "  Leave the walls 40 mm taller for the last 45 mm at the upper end",
                 "  (the ears that carry the lever pin).",
                 "End stop: 12 mm plate 92 x 70 mm welded across the lower end, 15 mm",
                 "  in; the pack's receptacle mounts on it on its floating mount.",
                 "Lever: 30 x 8 mm bar 127 mm long on an 8 mm pin through the ears,",
                 "  with a pad block 40 x 10 x 58 mm that presses the pack's handle end.",
                 "  Set the over-centre point so it closes with 50 N or less at the end",
                 "  and gives 330 N or more on the pack, with a detent.",
                 "Two 6.5 mm holes in the base, 240 mm apart, to the down tube tabs.",
                 "Fit: base on the tabs, M6 bolts; the pack slides down onto the",
                 "  receptacle and the lever closes over its top.",
                 "Check: SwapCell interface v0.3 envelope gauge slides in freely."])

    # 111 heel guard
    sheet(111, Part("Heel guard", C["heel"].shape, "#9CA3AF"), [Mp["frame"], Mp["rear_wheel"], Mp["fender"]],
          "StepGen heel guard: making sketch", "Aluminium sheet 2 mm, 5052 class",
          view_shape=b.Pos(-X0, 0, -Z0) * C["heel"].shape, inset_view=(25, -130),
          notes=["Cut a blank 436 mm wide by 215 mm. Fold the bottom 25 mm forward",
                 "  at 90 degrees (the flange).",
                 "Flange: two 6.5 mm holes, 80 mm each side of centre, 13 mm from the",
                 "  plate (M6 screws into the rear cross member's rivet nuts).",
                 "Upright: two 4.2 mm holes 120 mm up, 20 mm each side of centre,",
                 "  for the fender's front tab (4 mm rivets).",
                 "Round the top corners to 10 mm; deburr all edges.",
                 "Fit: stands between the rails, 2 mm clear of each, its back face",
                 "  level with the rails' rear ends; 190 mm tall.",
                 "Check: 20 mm or more from the belt as it goes round the rear roller."])

    # 112 roller covers
    covers = C["covers"].shape
    sheet(112, Part("Roller covers", covers, "#94A3B8"), [Mp["frame"], Mp["front_roller"], Mp["rear_roller"], Mp["belt"]],
          "StepGen roller covers (rear and front): making sketch", "Aluminium sheet 2 mm, 5052 class",
          # drawn side by side (front cover moved back to 200 mm ahead of the rear one) so both profiles read at 1:5
          view_shape=b.Pos(-RRX, 0, -RZ) * (win(covers, -5000, (RRX + FRX) / 2, -2000, 2000, -2000, 2000) +
                                            b.Pos(-(FRX - RRX) + 200, 0, 0) * win(covers, (RRX + FRX) / 2, 5000, -2000, 2000, -2000, 2000)),
          inset_view=(20, -60),
          notes=["Both covers are 440 mm wide (the gap between the rails).",
                 "Rear cover: a half round, 41 mm mean radius, 129 mm of sheet. Roll it",
                 "  round a 80 mm bar. It wraps the back of the rear roller.",
                 "Front cover: 41 mm mean radius, 102 degrees of arc (73 mm of sheet),",
                 "  from straight below the front roller round to 12 degrees above",
                 "  the axle at the front.",
                 "Each cover has a 15 mm tab bent out flat at each end; the tabs lie on",
                 "  the rails' inside walls, one M5 screw each into a rivet nut.",
                 "Fit: 14 mm or more from the belt all round; the rear cover guards the",
                 "  rear roller, the front cover the in-running nip under the front",
                 "  roller.",
                 "Check: the belt turns by hand without touching either cover."])

    # 113 toe guard
    sheet(113, Part("Toe guard", C["toe"].shape, "#9CA3AF"), [Mp["frame"], Mp["belt"], Mp["covers"]],
          "StepGen toe guard: making sketch", "Aluminium sheet 2 mm, 5052 class",
          view_shape=b.Pos(-X1, 0, -G["nose_top"]) * C["toe"].shape, inset_view=(20, -150),
          notes=["Cut a blank 436 mm wide by 153 mm; cut an 80 mm wide notch 25 mm",
                 "  deep in the middle of one long edge (it clears the down tube).",
                 "Fold the 25 mm flanges either side of the notch by 110 degrees,",
                 "  so the guard leans back 20 degrees when the flanges lie flat.",
                 "Flanges: four 6.5 mm holes, 80 and 180 mm each side of centre,",
                 "  12 mm from the fold (M6 screws into the nose beam's rivet nuts).",
                 "Round the top corners to 10 mm; deburr all edges.",
                 "Fit: on the nose beam's top, its fold on the beam's rear edge; its top",
                 "  edge is 120 mm above the beam, over the front end of the belt.",
                 "Check: 15 mm or more from the belt; 2 mm or more from the front cover."])

    # 114 side board and spacers
    bd = C["boards"].shape & bx(300, 1400, 180, 280, 225, 260)
    sheet(114, Part("Side board", bd, "#CBD5E1"), [Mp["frame"], Mp["belt"], Mp["carriers"]],
          "StepGen side board (make 2) and spacers: making sketch", "HDPE sheet 6 mm; aluminium tube 12 x 2 mm",
          view_shape=b.Pos(-330, -195, -230) * bd, inset_view=(30, 70),
          notes=["Boards: cut two 1060 x 70 mm strips of 6 mm HDPE; round the",
                 "  corners to 10 mm and chamfer the inner top edge 2 mm.",
                 "Four 6.5 mm holes in each, 40 mm from the inner edge, at 30, 370,",
                 "  710 and 1030 mm from the rear end.",
                 "Spacers: eight 13 mm lengths of 12 x 2 mm aluminium tube.",
                 "Fit: each board on four spacers on the rail top, M6 x 25 button-head",
                 "  screws into the rail's rivet nuts. The board's inner edge lies 5 mm",
                 "  over the belt edge and 3 mm above it; its rear end 60 mm from the",
                 "  rail's rear end.",
                 "Check: slide a 2 mm feeler between board and belt along its length."])
    return out


# ----------------------------------------------------------------- rail layout
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyBboxPatch
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    fig = plt.figure(figsize=(13, 8.2), dpi=150)
    fig.text(0.03, 0.975, "Deck rails: holes, slots and nuts", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.945, "Each rail is 1150 mm of 60 x 30 x 2 RHS on edge. Distances in mm from the rail's rear end (left in every view); "
             "heights from its underside. The right rail is shown; the left rail is its mirror image.", fontsize=8.2, color=MUT, va="top")
    faces = [("Outer wall, seen from outside the vehicle (grey: the tension lug, welded on)", 0.66, 60), ("Inner wall, seen from the belt side", 0.38, 60),
             ("Top face, seen from above: M6 rivet nuts for the side board spacers", 0.19, 30)]
    feats = [
        [("slot", 30, 75, 42, 17, "rear axle slot, 17 tall,\nthrough both walls"), ("hole", 1100, 42, 10.5, "front axle hole 10.5,\nboth walls"),
         ("hole", 50, 22, 8.5, None), ("lug", 2, 12, 42, 20, None)],
        [("slot", 30, 75, 42, 17, None), ("hole", 1100, 42, 10.5, None), ("hole", 50, 22, 8.5, None),
         ("riv", 130, 25), ("riv", 430, 25), ("riv", 730, 25), ("riv", 1020, 25)],
        [("rivt", 90), ("rivt", 430), ("rivt", 770), ("rivt", 1090)],
    ]
    for fi, (name, y0, H) in enumerate(faces):
        ax = fig.add_axes([0.06, y0, 0.88, 0.2 if H == 60 else 0.1])
        ax.set_xlim(-30, 1180); ax.set_ylim(-26, H + 12); ax.set_axis_off()
        ax.add_patch(Rectangle((0, 0), 1150, H, fc="#F3F4F6", ec=INK, lw=1.1))
        ax.text(0, H + 4, name, fontsize=9, fontweight="bold", color=INK, va="bottom")
        xs, zs = [], []
        for f in feats[fi]:
            if f[0] == "slot":
                _, a, b_, zc, hh, lab = f
                ax.add_patch(FancyBboxPatch((a + 3, zc - hh / 2), b_ - a - 6, hh, boxstyle="round,pad=3", fc="white", ec=INK, lw=1))
                xs += [a, b_]; zs.append(zc)
                if lab:
                    ax.text(b_ + 12, zc + 6, lab, fontsize=7, color=INK, va="center")
            elif f[0] == "hole":
                _, x, z, dd, lab = f
                ax.plot([x], [z], "o", ms=dd * 0.9, mfc="white", mec=INK, mew=1)
                xs.append(x)
                if not (fi == 1 and z == 22):
                    zs.append(z)
                if lab:
                    ax.text(x - 14, z + 6, lab, fontsize=7, color=INK, va="center", ha="right")
            elif f[0] == "lug":
                _, a, b_, zc, hh, _l = f
                ax.add_patch(Rectangle((a, zc - hh / 2), b_ - a, hh, fc="#D1D5DB", ec=INK, lw=0.8))
            elif f[0] == "riv":
                _, x, z = f
                ax.plot([x], [z], "o", ms=8, mfc="white", mec=AC, mew=1.2)
                ax.text(x, z + 9, "M6 rivet nut\n(carrier bar)", fontsize=6.5, color=AC, ha="center", va="bottom")
                xs.append(x); zs.append(z)
            elif f[0] == "rivt":
                _, x = f
                ax.plot([x], [15], "o", ms=8, mfc="white", mec=AC, mew=1.2)
                xs.append(x)
        if fi == 0:
            ax.text(62, 12, "drag screw hole 8.5 (right rail only;\nM8 nut welded outside)", fontsize=7, color=INK, va="center")
        for i, x in enumerate(sorted(set(xs))):
            ax.plot([x, x], [0, -5], color=AC, lw=0.5)
            ax.text(x, -7 - 9 * (i % 2), f"{x:g}", fontsize=7, color=AC, ha="center", va="top")
        for z in sorted(set(zs)):
            ax.plot([-8, 0], [z, z], color=AC, lw=0.5)
            ax.text(-10, z, f"{z:g}", fontsize=6.5, color=AC, ha="right", va="center")
    fig.text(0.06, 0.105, "Left rail only: two 12 mm grommet holes in the outer wall at 60 and 1135 mm, 26 mm up (the harness runs inside "
             "the rail);", fontsize=8, color=INK)
    fig.text(0.06, 0.082, "  two M3 rivet nuts in the inner wall at 1092 and 1108 mm, 16 mm up (sensor bracket).", fontsize=8, color=INK)
    fig.text(0.06, 0.055, "Both rails: a 16 x 3 mm crush tube 26 mm long welded between the walls at the front axle hole; a tension lug "
             "outside at the rear end; a 3 mm end cap.", fontsize=8, color=INK)
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/stepgen", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "rail-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "rail-holes.png"


# ----------------------------------------------------------------- joints
def joints():
    out = []
    fr = C["frame"].shape

    def j(n, parts, title, sub, **kw):
        if want(n):
            out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, size=(8, 6), **kw))

    # 01 rear dropout, right side, from outside
    w = (-30, 52, 55, 100, 208, 285)
    j(1, [part("Dropout plate and stay ends", win(fr, *w), FRM),
          part("Hub motor axle, locknut and nut", win(C["rear_wheel"].shape, -30, 52, 40, 100, 208, 285), C["rear_wheel"].color),
          part("Torque arm (M6 bolt to the dropout)", win(C["torque_arms"].shape, *w), "#D4A017")],
      "rear dropout, right side", "Seen from outside and above. Axle in the slot; torque arm on the outside face; axle nut on the arm",
      elev=25, azim=60)
    # 02 rear caliper on the left dropout tab
    w = (-110, 10, -90, -35, 160, 280)
    j(2, [part("Left dropout and caliper tab", win(fr, *w), FRM),
          part("Rear rotor, 160 mm", win(ROT_R, *w), "#6B7280"),
          part("Rear caliper, two M6 bolts", win(C["caliper_r"].shape, *w), "#B91C1C")],
      "rear caliper on the left dropout tab", "Seen from behind and inside. The caliper sits on the tab's inside face, across the rotor",
      elev=15, azim=155)
    # 03 rail rear end, right side
    w = (225, 360, 150, 280, 140, 260)
    lug = win(fr, 271.9, 282.1, 249.99, 263.1, 190, 235)
    stay = win(fr, 240, 267.0, 150, 280, 140, 260)
    j(3, [part("Deck rail and end cap", win(fr, 267.0, 360, 150, 280, 165, 260) - lug, FRM),
          part("Upper and lower stays", stay, "#4B5563"),
          part("Tension lug (welded)", lug, "#0E7490"),
          part("Rear axle end in its slot", win(C["rear_roller"].shape, 300, 360, 236, 280, 190, 240), "#2563EB"),
          part("M8 tension bolt", win(C["rear_roller"].shape, 255, 300, 245, 275, 195, 230), "#111827"),
          part("Drag screw (right side only)", win(C["drag"].shape, *w), "#D4A017")],
      "rear end of the right rail", "Seen from outside and behind, low down. The tension bolt pulls the axle back along its slot",
      elev=8, azim=118)
    # 04 idler in the carrier, cut across at an idler
    xi = D["idler_x"][5]
    w = (xi - 40, xi + 40, 150, 270, 160, 265)
    j(4, [part("Deck rail", win(fr, *w), FRM),
          part("Carrier bar and M6 screw", win(C["carriers"].shape, *w), C["carriers"].color),
          part("Idler roller and spring axle", win(C["idlers"].shape, *w), "#94A3B8"),
          part("Belt", win(C["belt"].shape, *w), "#111827"),
          part("Side board on its spacer", win(C["boards"].shape, *w), "#CBD5E1")],
      "idler roller in the carrier bar (right side)", "Cut across the deck at the sixth idler, seen from the front",
      elev=8, azim=-5)
    # 05 front roller left end, cut on the axle line
    w = (FRX - 45, FRX + 45, -265, -150, 160, 260)
    cut = bx(FRX - 45, FRX + 0.5, -265, -150, 160, 260)
    j(5, [part("Deck rail and crush tube", win(fr, *w) & cut, FRM),
          part("Front roller, axle, spacer, M10 bolt", win(C["front_roller"].shape, *w) & cut, "#475569"),
          part("Magnet ring on the roller end", RING & cut, "#0EA5E9"),
          part("Hall sensor on its bracket", HALL & cut, "#D97706")],
      "front roller, left end, with the speed sensor", "Cut through the axle, seen from the front. 1.5 mm air gap between sensor and ring",
      elev=10, azim=-20)
    # 06 drag screw, cut at the screw
    w = (RRX - 30, RRX + 0.5, 150, 285, 168, 250)
    j(6, [part("Right rail and welded M8 nut", win(fr, *w), FRM),
          part("Rear roller end, spacer and axle", win(C["rear_roller"].shape, RRX - 30, RRX + 0.5, 180, 285, 168, 250), "#475569"),
          part("Drag screw with felt tip", win(C["drag"].shape, *w), "#D4A017")],
      "belt drag screw (right rear)", "Cut through the screw, seen from the front. Screw in: more drag; out: none",
      elev=10, azim=-25)
    # 07 nose: rails, beam, down tube foot, toe guard flange, controller
    w = (1395, 1530, -270, 40, 160, 300)
    j(7, [part("Nose beam, rail ends and down tube foot", win(fr, *w), FRM),
          part("Toe guard and flange", win(C["toe"].shape, *w), "#D1D5DB"),
          part("Controller", win(C["controller"].shape, *w), C["controller"].color),
          part("Harness to the left rail", win(C["harness"].shape, *w), "#111827")],
      "nose beam, down tube foot and toe guard (left half)", "Seen from the front left. Every part sits flat on the beam's top",
      elev=25, azim=-40)
    # 08 head tube, cut on the centre plane
    SP = steer_plane()
    hz = M.axis_pt(-45)[2]
    w = (1560, 1800, 0, 90, hz, M.axis_pt(270)[2])
    j(8, [part("Head tube and down tube", win(fr, *w), FRM),
          part("Fork crown, steerer and headset", win(C["fork"].shape, *w), "#475569"),
          part("Column clamp sleeve and column", win(C["column"].shape, *w), "#0F766E")],
      "head tube, headset and column clamp", "Cut on the centre line, seen from the left. The sleeve clamps the steerer above the headset",
      elev=12, azim=-70)
    # 09 stem and bar clamp, cut on the centre plane
    w = (1370, 1480, 0, 75, 1180, 1300)
    j(9, [part("Column and stem", win(C["column"].shape, *w), "#0F766E"),
          part("Handlebar in the bar clamp", win(C["bar"].shape, *w), "#1F2937"),
          part("Display on its clamp", win(C["controls"].shape, *w), "#2563EB")],
      "stem and bar clamp", "Cut on the centre line, seen from the left and slightly above",
      elev=15, azim=-75)
    # 10 cradle, cut on the centre plane
    DP = dt_plane()
    lo = DP.from_local_coords((D["tc"] - 220, 0, 0)); hi = DP.from_local_coords((D["tc"] + 260, 0, 160))
    w = (min(lo.X, hi.X) - 120, max(lo.X, hi.X) + 140, 0, 80, lo.Z - 60, hi.Z + 60)
    j(10, [part("Down tube and tabs", win(fr, *w) - M.lcyl(steer_plane(), -100, 300, 26), FRM),
           part("Cradle, end stop and lever", win(C["cradle"].shape, *w), C["cradle"].color),
           part("SwapCell pack", win(C["pack"].shape, *w), C["pack"].color)],
      "receiver cradle and pack", "Cut on the centre line, seen from the left. Lever pad on the handle end; pack on the end stop",
      elev=12, azim=-75)
    # 11 front caliper
    w = (FX - 110, FX + 10, -80, -10, R - 20, R + 110)
    j(11, [part("Fork leg and post mount", win(C["fork"].shape, *w), FRM),
           part("Front rotor, 160 mm", win(ROT_F, *w), "#6B7280"),
           part("Front caliper, two M6 bolts", win(C["caliper_f"].shape, *w), "#B91C1C")],
      "front caliper on the fork's post mount", "Seen from inside the fork, behind the left leg. The caliper sits on the post mount, across the rotor",
      elev=15, azim=150)
    # 12 heel guard flange and fender front end, cut on the centre plane
    w = (230, 330, 0, 80, 140, 380)
    j(12, [part("Rear cross member and rail", win(fr, *w), FRM),
           part("Heel guard and flange (M6 screws)", win(C["heel"].shape, *w), "#9CA3AF"),
           part("Fender front end, riveted", win(C["fender"].shape, *w), "#6B7280"),
           part("Rear roller cover", win(C["covers"].shape, *w), "#CBD5E1"),
           part("Belt round the rear roller", win(C["belt"].shape + C["rear_roller"].shape, *w), "#111827")],
      "heel guard, fender and rear cover", "Cut on the centre line, seen from the left",
      elev=0, azim=-90)
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    Mp = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, label_done=False, **kw))

    def mv(p, e):
        # the part being fitted is always in colour: grey, white or black parts take the kit's accent colour
        import colorsys
        r, g, b_ = (int(p.color[i:i + 2], 16) / 255 for i in (1, 3, 5))
        _h, li, sa = colorsys.rgb_to_hls(r, g, b_)
        col = p.color if sa > 0.3 and 0.2 < li < 0.9 else bv.NEW
        return Part(p.name, p.shape, col, None, tuple(e), p.alpha)
    fr = Mp["frame"]
    st(1, [fr], [mv(Mp["kick"], (0, -150, 0))], "kickstand onto the frame",
       "Two bolts through the welded plate on the left rail; leg folds back along the rail", elev=15, azim=-70)
    st(2, [fr, Mp["kick"]], [mv(Mp["carriers"], (0, 0, 220))], "idler carrier bars into the rails",
       "Four M6 button-head screws each, into rivet nuts in the rails' inside walls", elev=35, azim=-60)
    deck0 = [fr, Mp["kick"], Mp["carriers"]]
    st(3, deck0, [mv(Mp["belt"], (0, 0, 260)), mv(Mp["front_roller"], (200, 0, 260))], "belt between the rails, front roller into it",
       "Lay the belt loop between the rails; slide the roller into its front end; M10 bolts through the rails", elev=30, azim=-60)
    st(4, deck0 + [Mp["belt"], Mp["front_roller"]], [mv(Mp["rear_roller"], (-150, 0, 200))],
       "rear roller into the belt and the rail slots",
       "Axle ends into the slots; M8 tension bolts through the lugs into the axle ends, loose for now", elev=30, azim=-50)
    deck1 = deck0 + [Mp["belt"], Mp["front_roller"], Mp["rear_roller"]]
    st(5, deck1, [mv(Mp["idlers"], (0, 0, -200))], "idler rollers into the belt loop",
       "Push each roller in under the top run; press its spring axles into the carrier holes", elev=-25, azim=-60)
    deck2 = deck1 + [Mp["idlers"]]
    # step 6 fits two small parts a metre apart, so it gets two close-ups: 06 the drag screw, 06b the sensor
    def near(parts, *w):
        res = []
        for q in parts:
            sh = win(q.shape, *w)
            try:
                if sh.volume > 1.0:
                    res.append(Part(q.name, sh, q.color, None, (0, 0, 0), q.alpha))
            except Exception:
                pass
        return res
    wd = (RRX - 110, RRX + 160, 60, 330, 120, 330)
    st(6, near(deck2, *wd), [mv(Mp["drag"], (0, 110, 0))], "drag screw (rear end of the right rail)",
       "Screw it through the welded nut and both rail walls until the felt just touches the roller, then back it off",
       elev=20, azim=150)
    if want(6):
        out.append(bv.step(near([fr, Mp["front_roller"]], FRX - 110, FRX + 90, -300, -195, 140, 300), [mv(Mp["hall"], (0, 70, -60))],
                           OUT / "step-06b.png", "Step 6 (continued): speed sensor (front end of the left rail)",
                           subtitle="Sensor bracket on the left rail's inside wall, two M3 screws; sensor faces the magnet ring",
                           label_done=True, elev=12, azim=70))
    deck3 = deck2 + [Mp["drag"], Mp["hall"]]
    st(7, deck3, [mv(Mp["fork"], (0, 0, -260))], "fork and headset into the head tube",
       "Headset cups into the head tube, crown race on the fork, fork up through the head tube", elev=15, azim=-60)
    st(8, deck3 + [Mp["fork"]], [mv(Mp["column"], (-90, 0, 250))], "steering column onto the steerer",
       "Set the headset preload first; slide the sleeve down onto the top cover; two M6 clamp bolts", elev=15, azim=-60)
    st(9, deck3 + [Mp["fork"], Mp["column"]], [mv(Mp["bar"], (0, 0, 200))], "handlebar, grips, levers and controls",
       "Bar into the clamp, centred; two M6 bolts; then grips, levers, display, selector, key and lanyard switch",
       elev=20, azim=-55)
    front = deck3 + [Mp["fork"], Mp["column"], Mp["bar"]]
    st(10, front, [mv(Mp["front_wheel"], (0, 0, -220))], "front wheel, rotor and caliper",
       "Rotor on the hub (six bolts); wheel into the fork; caliper on the post mount, centred on the rotor", elev=15, azim=-60)
    front2 = front + [Mp["front_wheel"]]
    st(11, front2, [mv(Mp["rear_wheel"], (0, 0, -220))], "rear wheel with hub motor and torque arms",
       "Rotor on the motor; axle up into the dropout slots; torque arms on the outside; axle nuts to the maker's torque",
       elev=15, azim=-60)
    st(12, near(front2 + [Mp["rear_wheel"]], -220, 160, -220, 60, 40, 440), [mv(Mp["caliper_r"], (0, -130, 0))], "rear caliper",
       "Close-up from behind and left. On the left dropout tab, two M6 bolts; centre it on the rotor before tightening",
       elev=15, azim=-130)
    wheels = front2 + [Mp["rear_wheel"], Mp["caliper_r"]]
    st(13, wheels, [mv(Mp["controller"], (0, -200, 0)), mv(Mp["harness"], (0, -320, 0))], "controller and wiring harness",
       "Controller on its plate (four bolts); harness through the left rail and up the down tube; fuse out", elev=15, azim=-70)
    elec = wheels + [Mp["controller"], Mp["harness"]]
    st(14, elec, [mv(Mp["cradle"], (-180, 0, 120))], "receiver cradle onto the down tube",
       "Two M6 bolts into the tabs; plug the receptacle lead into the harness", elev=15, azim=-70)
    st(15, elec + [Mp["cradle"]], [mv(Mp["covers"], (0, 0, 220)), mv(Mp["heel"], (-150, 0, 150))],
       "roller covers and heel guard", "Cover tabs on the rails' inside walls (M5); heel guard flange on the rear cross member (two M6)",
       elev=30, azim=-50)
    g2 = elec + [Mp["cradle"], Mp["covers"], Mp["heel"]]
    st(16, g2, [mv(Mp["fender"], (-150, 0, 150)), mv(Mp["toe"], (120, 0, 150))], "fender and toe guard",
       "Fender stays to the dropouts, front tab riveted to the heel guard; toe guard flanges on the nose beam (four M6)",
       elev=25, azim=-55)
    g3 = g2 + [Mp["fender"], Mp["toe"]]
    st(17, g3, [mv(Mp["boards"], (0, 0, 200))], "side boards",
       "Each on four spacers, M6 x 25 screws into the rail tops; 3 mm above the belt", elev=30, azim=-60)
    st(18, g3 + [Mp["boards"]], [mv(Mp["pack"], (-100, 0, 260))], "SwapCell pack (only after the safety stops)",
       "Slide the pack down the cradle onto its receptacle; close the lever over its handle end", elev=15, azim=-70)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(13, 7.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 130); ax.set_ylim(0, 76); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 74, "StepGen prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 70.6, "Bought modules wired at block level; no circuit board is laid out and no firmware is written. Stranded copper; "
            "ferrules or crimped terminals on every end.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(128, 1.5, "github.com/BoujeeEnjinia1701/stepgen", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.8, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.0, sub, ha="center", va="top", fontsize=7.0, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0, ls="-"):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.0, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, GRN = "#B91C1C", "#1D4ED8", "#6B7280", "#047857"
    blk(3, 44, 18, 14, "SwapCell pack", "13S, 39 to 54.6 V,\n468 Wh; in the\nclass V1 cradle", "#C2410C")
    blk(27, 46, 14, 10, "20 A fuse", "sealed holder,\non the down tube", RED)
    blk(48, 42, 19, 14, "Motor controller", "48 V, 15 A sine wave;\nbrake-cut and speed\ncommand inputs", "#115E59")
    blk(76, 42, 17, 14, "250 W hub motor", "rear wheel;\nphases and\nHall sensors", "#0F766E")
    blk(48, 18, 19, 14, "Walking logic board", "ESP32 with CAN;\n60 V buck to 5 V;\nSwapCell host", "#2563EB")
    blk(3, 20, 18, 12, "Key switch", "in series with the\n10 kOhm coding\nresistor", MUT)
    blk(76, 27, 17, 10, "Belt speed sensor", "Hall, 8 magnets\non the roller", "#0EA5E9")
    blk(76, 13, 17, 10, "Display, selector", "speed, level, charge;\n3 levels", "#2563EB")
    blk(102, 44, 24, 10, "Brake levers (2)", "cut-off switches", RED)
    blk(102, 28, 24, 10, "Lanyard stop", "magnetic, opens\nwhen pulled", RED)
    wire([(21, 51), (27, 51)], RED, 3.0); lab(24, 53.3, "2.5 mm²", RED, "center")
    wire([(41, 51), (48, 51)], RED, 3.0); lab(44.5, 53.3, "2.5 mm²", RED, "center")
    wire([(67, 49), (76, 49)], GRN, 3.0); lab(71.5, 51.3, "motor cable", GRN, "center")
    wire([(34, 46), (34, 24), (48, 24)], RED, 1.4); lab(34.6, 36, "0.5 mm²,\nbuck input", RED)
    wire([(9, 44), (9, 32)], GRY, 1.4); lab(9.6, 38, "INTERLOCK\nto SGND,\n0.25 mm²", GRY)
    wire([(17, 44), (17, 41), (43, 41), (43, 28), (48, 28)], BLU, 1.4); lab(19, 42.6, "CAN H and L, twisted, 0.25 mm²", BLU)
    wire([(57.5, 32), (57.5, 42)], BLU, 1.4); lab(58.2, 37, "speed command,\n0.25 mm²", BLU)
    wire([(76, 31), (67, 31)], BLU, 1.4); lab(71.5, 33, "pulses", BLU, "center")
    wire([(76, 18), (71, 18), (71, 22), (67, 22)], BLU, 1.4); lab(71.5, 15.6, "0.25 mm²", BLU, "center")
    wire([(102, 49), (98, 49), (98, 61), (57.5, 61), (57.5, 56)], RED, 1.4); lab(78, 62.6, "brake-cut, hardwired to the controller", RED, "center")
    wire([(102, 33), (98, 33), (98, 49)], RED, 1.4)
    wire([(114, 28), (114, 10), (57.5, 10), (57.5, 18)], GRY, 1.0, ":"); lab(86, 8.4, "switch states also read by the logic board", GRY, "center")
    ax.text(3, 4.6, "Safety: fuse out and pack out until the stop points in section 6 of the plan are passed. Every circuit is below 60 V DC. "
            "Turning the key off cuts the pack output at once: key off only at a standstill.", fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 67.2, "Red: power and safety cut-offs. Green: motor. Blue: signals. Grey: interlock loop and monitoring. Wire runs between the "
            "down tube and the rear wheel go inside the left deck rail.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = [a for a in sys.argv[1:] if not a.startswith("only=")] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
