"""StepGen concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X forward (the user faces +X), Y across, Z up. Units mm. Floor at Z = 0.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all

# Overall envelope (see docs/02-concept.md and REQ R9)
BASE_L, BASE_W, TUBE = 850.0, 620.0, 40.0      # base frame, 40 x 40 mm square tube
PEDAL_L, PEDAL_W, PEDAL_T = 380.0, 130.0, 25.0
PEDAL_Y = 95.0                                  # pedal centerlines at +/- Y
PIVOT_X, PIVOT_Z = -400.0, 110.0                # rear pedal pivot
TILT = 11.0                                     # pedal tilt in degrees; front travel about 150 mm peak to peak
DRIVE_X = 190.0                                 # jackshaft position
RAIL_H = 1000.0                                 # handrail height above floor

# 1 Base frame: two side rails, three cross members, rear pivot block
side = lambda y: Pos(0, y, TUBE / 2) * Box(BASE_L, TUBE, TUBE)
cross = lambda x: Pos(x, 0, TUBE / 2) * Box(TUBE, BASE_W, TUBE)
pivot_post = lambda y: Pos(PIVOT_X, y, (PIVOT_Z + TUBE) / 2) * Box(50, 30, PIVOT_Z)
frame = (side(-BASE_W / 2 + TUBE / 2) + side(BASE_W / 2 - TUBE / 2)
         + cross(-BASE_L / 2 + TUBE / 2) + cross(0) + cross(BASE_L / 2 - TUBE / 2)
         + pivot_post(0) + pivot_post(-200) + pivot_post(200))

# 2 Pedals on a rocker: pedals pivot at the rear; a rocker beam under their front ends links them
def pedal(y, ang):
    tread = Pos(PEDAL_L / 2, 0, PEDAL_T / 2) * Box(PEDAL_L, PEDAL_W, PEDAL_T)
    return Pos(PIVOT_X, y, PIVOT_Z) * Rot(0, ang, 0) * tread

pedals = pedal(-PEDAL_Y, TILT) + pedal(PEDAL_Y, -TILT)
rocker_pivot = Pos(-60, 0, 90) * Box(40, 40, 100)
rocker_beam = Pos(-60, 0, 150) * Rot(-9, 0, 0) * Box(30, 2 * PEDAL_Y + 60, 20)
rocker = rocker_pivot + rocker_beam

# 3 One-way clutches (2 x 16T single-speed freewheels) on the jackshaft
JS_Z = 170.0
jackshaft = Pos(DRIVE_X, 0, JS_Z) * Rot(90, 0, 0) * Cylinder(10, 460)
clutches = (Pos(DRIVE_X, -PEDAL_Y, JS_Z) * Rot(90, 0, 0) * Cylinder(32, 30)
            + Pos(DRIVE_X, PEDAL_Y, JS_Z) * Rot(90, 0, 0) * Cylinder(32, 30))
clutch_asm = jackshaft + clutches
js_bearings = (Pos(DRIVE_X, -230, (JS_Z + TUBE) / 2) * Box(40, 30, JS_Z)
               + Pos(DRIVE_X, 230, (JS_Z + TUBE) / 2) * Box(40, 30, JS_Z))

# 4 Chain drive: pedal chains (front tip of each pedal to its freewheel) and the 4:1 stage-1 chain
def pedal_chain(y, ang_sign):
    tip_z = PIVOT_Z + ang_sign * 0.19 * PEDAL_L   # approximate front-tip height
    run = Pos((PIVOT_X + PEDAL_L + DRIVE_X) / 2, y, (tip_z + JS_Z) / 2) * Box(DRIVE_X - PIVOT_X - PEDAL_L + 30, 8, 8)
    return run

S1_Y = 180.0
INT_X, INT_Z = 290.0, 260.0                      # intermediate shaft
stage1 = (Pos(DRIVE_X, S1_Y, JS_Z) * Rot(90, 0, 0) * Cylinder(95, 8)           # 48T sprocket
          + Pos(INT_X, S1_Y, INT_Z) * Rot(90, 0, 0) * Cylinder(26, 8)          # 12T sprocket
          + Pos((DRIVE_X + INT_X) / 2, S1_Y, (JS_Z + INT_Z) / 2 + 60) * Rot(0, -33, 0) * Box(170, 8, 8)
          + Pos((DRIVE_X + INT_X) / 2, S1_Y, (JS_Z + INT_Z) / 2 - 60) * Rot(0, -33, 0) * Box(170, 8, 8))
chain = pedal_chain(-PEDAL_Y, 1) + pedal_chain(PEDAL_Y, -1) + stage1

# 5 Belt step-up (10:1) from intermediate shaft to generator shaft
GEN_X, GEN_Z = 270.0, 470.0
belt_stage = (Pos(INT_X, -150, INT_Z) * Rot(90, 0, 0) * Cylinder(110, 20)       # large pulley
              + Pos(INT_X, 20, INT_Z) * Rot(90, 0, 0) * Cylinder(12, 360)      # intermediate shaft
              + Pos(GEN_X, -150, GEN_Z) * Rot(90, 0, 0) * Cylinder(14, 20)     # small pulley
              + Pos(INT_X - 100, -150, (INT_Z + GEN_Z) / 2) * Box(8, 16, GEN_Z - INT_Z)
              + Pos(INT_X + 100, -150, (INT_Z + GEN_Z) / 2) * Box(8, 16, GEN_Z - INT_Z))

# 6 Flywheel on the generator shaft (300 mm x 6 mm steel disc, about 3.3 kg)
flywheel = Pos(GEN_X, 60, GEN_Z) * Rot(90, 0, 0) * Cylinder(150, 6)
gen_shaft = Pos(GEN_X, 0, GEN_Z) * Rot(90, 0, 0) * Cylinder(8, 320)

# 7 BLDC generator
generator = Pos(GEN_X, 160, GEN_Z) * Rot(90, 0, 0) * Cylinder(70, 70)

# 8 Drivetrain guard: closed sheet-steel shell over the whole drivetrain (hollow so the cutaway shows inside)
G_X0, G_X1, G_Z1 = 60.0, BASE_L / 2, 640.0
g_outer = Pos((G_X0 + G_X1) / 2, 0, (TUBE + G_Z1) / 2) * Box(G_X1 - G_X0, BASE_W - 60, G_Z1 - TUBE)
g_inner = Pos((G_X0 + G_X1) / 2, 0, (TUBE + G_Z1) / 2 - 2) * Box(G_X1 - G_X0 - 4, BASE_W - 64, G_Z1 - TUBE - 2)
guard = g_outer - g_inner

# 9 Handrail: two front posts, a top bar and side grips reaching back over the pedals
POST_X = BASE_L / 2 - 20
post = lambda y: Pos(POST_X, y, RAIL_H / 2) * Cylinder(19, RAIL_H)
grip = lambda y: Pos(POST_X - 240, y, RAIL_H) * Rot(0, 90, 0) * Cylinder(16, 480)
handrail = (post(-BASE_W / 2 + 20) + post(BASE_W / 2 - 20)
            + Pos(POST_X, 0, RAIL_H) * Rot(90, 0, 0) * Cylinder(16, BASE_W - 40)
            + grip(-BASE_W / 2 + 20) + grip(BASE_W / 2 - 20))

# 10 Rectifier and load controller box (inside the guard, on the front cross member)
controller = Pos(400, -180, TUBE + 60) * Box(40, 160, 120)

# 11 Display and resistance selector on the top bar
display = Pos(POST_X - 30, 0, RAIL_H + 70) * Rot(0, -25, 0) * Box(30, 160, 100)

# 12 Output lead to the PowerBox (2 m in service; a short stub shown)
lead = (Pos(POST_X + 60, -180, TUBE + 60) * Rot(0, 90, 0) * Cylinder(6, 120)
        + Pos(POST_X + 120, -180, 30) * Cylinder(6, 60)
        + Pos(POST_X + 160, -180, 6) * Rot(0, 90, 0) * Cylinder(6, 80))

parts = [
    Part("Base frame", frame + js_bearings, "#4B5563", 1, (0, 0, -140)),
    Part("Pedals on rocker", pedals + rocker, "#1F2937", 2, (-260, 0, 60)),
    Part("One-way clutches and jackshaft", clutch_asm, "#D4A017", 3, (0, 0, 120)),
    Part("Chain drive, 4:1", chain, "#9CA3AF", 4, (0, 300, 120)),
    Part("Belt step-up, 10:1", belt_stage, "#6B7280", 5, (0, -380, 260)),
    Part("Flywheel, 300 mm", flywheel + gen_shaft, "#0F766E", 6, (0, 160, 380)),
    Part("BLDC generator", generator, "#C2410C", 7, (0, 420, 380)),
    Part("Drivetrain guard", guard, "#CBD5E1", 8, (-350, 0, 1250)),
    Part("Handrail", handrail, "#374151", 9, (950, 0, 0)),
    Part("Rectifier and load controller", controller, "#15803D", 10, (380, -380, 0)),
    Part("Display and level selector", display, "#111827", 11, (1100, 0, 250)),
    Part("Output lead to PowerBox", lead, "#B91C1C", 12, (500, -500, 0)),
]

render_all(
    parts, project="StepGen", title="Stepper generator concept", dwg_no="SGN-DWG-010",
    key_figures=["Pedal work 50 to 100 W (70 kg, 15 cm, 30 to 60 steps/min)",
                 "About 70 % pedal to pack (estimate)",
                 "About 35 to 70 Wh stored per hour (estimate)",
                 "Charges a 46.8 V PowerBox; all circuits under 60 V DC",
                 "Footprint 0.85 x 0.62 m, about 34 kg (estimate)"],
    cut_exclude=("Drivetrain guard", "Handrail", "Display and level selector"),
    flow={"title": "energy flow at 75 W pedal work (all values are estimates)", "unit": "W",
          "stages": [("Pedal work", 75), ("Generator shaft", 67.5), ("DC bus", 55.7), ("Stored in pack", 52.3)],
          "losses": [(0, "Drivetrain loss (est.)", 7.5), (1, "Generator, rectifier (est.)", 11.8),
                     (2, "Charger (est.)", 3.4)]},
)
