"""StepGen sizing calculations (SGN-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes
docs/04-calcs/results.csv (requirement, value, target, status).

Geometry comes from cad/src/model.py (PARAMS and geometry()), the BOM from
bom/bom.csv and the budget from project.yaml, so the note, the model and the
BOM share one source. All values are first-principles estimates, not measurements.
"""
import csv
import importlib.util
import math
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("model", ROOT / "cad/src/model.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
P, G = model.PARAMS, model.geometry()

g = 9.81
RHO = 1.2               # air density, kg/m3
CRR = 0.010             # 20 x 1.75 in tires on pavement
CDA = 0.70              # standing rider plus vehicle, m2
ETA_M, ETA_C = 0.80, 0.95
ETA = ETA_M * ETA_C
AUX_W = 3.0             # logic board, display, controller standby
V_NOM, V_MIN = 46.8, 39.0
E_TERM = 457.0          # Wh at the pack terminals per full cycle (SWC-CAL-001)
RESERVE = 0.10
RIDER = 80.0            # design rider, kg
RIDER_MAX = 120.0       # heaviest rider for structure, kg
RIDER_H = 1.75          # m
PACK_KG = 2.85          # SwapCell pack (SWC-CAL-001)
R_WHEEL = P["wheel_r"] / 1000
P_RATED = 250.0         # W at the wheel, rated continuous
REAL_FACTOR = 1.4       # energy multiplier for stops, hills and wind (assumption)

rows = []


def res(rid, value, target, status):
    rows.append((rid, value, target, status))


def hdr(t):
    print(f"\n== {t} ==")


# ---------------------------------------------------------------- 1 geometry
hdr("1 Geometry (from cad/src/model.py)")
print(f"length {G['length']:.0f} mm; width at grips {G['width']:.0f} mm; wheelbase {G['wheelbase']:.0f} mm")
print(f"belt: roller pitch {P['roller_pitch']:.0f} mm, usable {G['belt_usable']:.0f} mm, width {P['belt_w']:.0f} mm, "
      f"top {P['deck_z']:.0f} mm above ground")
print(f"ground clearance {G['ground_clearance']:.0f} mm; bar {P['bar_z']:.0f} mm above ground, "
      f"{G['bar_above_belt']:.0f} mm above the belt")
print(f"head angle {P['head_angle']:.0f} deg, fork offset {P['fork_offset']:.0f} mm, trail {G['trail']:.1f} mm, "
      f"wheel flop {G['trail'] * math.sin(math.radians(P['head_angle'])) * math.cos(math.radians(P['head_angle'])):.1f} mm")

# ---------------------------------------------------------------- 2 mass
hdr("2 Mass and centre of mass")
ST = 7850.0  # steel kg/m3


def rhs(h, b, t):          # rectangular hollow section area, mm2
    return 2 * (h + b) * t - 4 * t * t


def chs(d, t):             # circular hollow section area, mm2
    return math.pi * (d - t) * t


def kg(area_mm2, length_mm, rho=ST):
    return area_mm2 * 1e-6 * length_mm * 1e-3 * rho


rail_len = P["rail_x1"] - P["rail_x0"]
lower_stay = math.dist((P["rail_x0"], P["rail_y"], G["roll_z"] - 15), (0, 70, P["wheel_r"]))
upper_stay = math.dist((P["rail_x0"] + 180, P["rail_y"], G["roll_z"] + 5), (0, 70, P["wheel_r"] + 10))
nose_len = math.dist((P["rail_x1"], P["rail_y"], G["roll_z"] - 15), (G["dt_lo"][0], 40, G["dt_lo"][1]))
frame_items = [
    ("deck rails 50x25x2 RHS", kg(rhs(50, 25, 2), 2 * rail_len)),
    ("cross members 25x25x2 RHS", kg(rhs(25, 25, 2), 3 * 2 * P["rail_y"])),
    ("rear stays 22x1.6", kg(chs(22, 1.6), 2 * lower_stay + 2 * upper_stay)),
    ("nose tubes 28x1.6 and block", kg(chs(28, 1.6), 2 * nose_len) + 0.40),
    ("down tube 44x2", kg(chs(44, 2), G["dt_len"])),
    ("head tube 44x3", kg(chs(44, 3), P["head_len"])),
    ("dropouts, roller plates, tensioner, tabs", 0.70),
]
frame_kg = sum(m for _, m in frame_items)
for n, m in frame_items:
    print(f"  frame: {n:42s} {m:5.2f} kg")
print(f"  frame total {frame_kg:.1f} kg")

col_len = (P["bar_z"] - G["head_top"][1]) / G["steer_dir"][1]
steer_kg = kg(chs(38, 2), col_len) + 0.30 + 0.35 + 0.20
dtx0, dtz0 = G["dt_lo"]; dtx1, dtz1 = G["dt_hi"]
pack_x = dtx0 + (dtx1 - dtx0) * P["pack_pos"]; pack_z = dtz0 + (dtz1 - dtz0) * P["pack_pos"] + 60
# item, mass kg, x mm, z mm, basis
masses = [
    ("1 Main frame", frame_kg, 800, 260, "tube list above"),
    ("2 Belt and end rollers", 3.8, 845, 215, "belt 1.3 kg (1.5 kg/m2), rollers 2 x 1.1 kg, tensioner 0.3 kg"),
    ("3 Roller bed", 3.0, 845, 222, "14 x 0.15 kg rollers, carriers 0.9 kg"),
    ("4 Anti-reverse clutch and drag", 0.4, P["rear_roller_x"], 215, "estimate"),
    ("5 Belt speed sensor", 0.05, G["front_roller_x"], 215, "estimate"),
    ("6 Rear wheel with hub motor", 4.3, 0, P["wheel_r"], "motor 2.5 kg, rim, spokes, tire, tube 1.6 kg, rotor 0.2 kg"),
    ("7 Front wheel, fork, headset", 3.0, G["front_x"], 300, "wheel 1.6 kg, fork 1.1 kg, headset 0.3 kg"),
    ("8 Steering column, bar, grips", steer_kg, 1480, 950, f"38x2 column {col_len:.0f} mm, stem, bar, grips"),
    ("9 Brakes", 1.1, 900, 450, "2 calipers, rotors, levers, cables"),
    ("10 Receiver cradle, class V1", 1.0, pack_x, pack_z - 40, "3 mm steel cradle, lever, receptacle"),
    ("12 Controller and logic board", 0.6, 1500, 280, "estimate"),
    ("13 Display, selector, lanyard, key", 0.3, P["bar_x"], P["bar_z"], "estimate"),
    ("14 Guards", 2.0, 600, 300, "about 0.63 m2 of 1 mm aluminium plus brackets"),
    ("15 Harness with fuse", 0.4, 900, 250, "estimate"),
    ("16 Hardware and kickstand", 0.9, 500, 250, "kickstand 0.4 kg, fasteners 0.5 kg"),
]
veh_kg = sum(m for _, m, *_ in masses)
for n, m, *_ in masses:
    print(f"  {n:38s} {m:5.2f} kg")
veh_pack = veh_kg + PACK_KG
m_tot = veh_pack + RIDER
print(f"vehicle without pack {veh_kg:.1f} kg; with pack {veh_pack:.1f} kg; with 80 kg rider {m_tot:.1f} kg")
print(f"margin to 40 kg: {40 - veh_pack:.1f} kg ({(40 - veh_pack) / veh_kg * 100:.0f} % of vehicle mass); "
      f"with a 10 % growth allowance {veh_kg * 1.1 + PACK_KG:.1f} kg")
vx = (sum(m * x for _, m, x, _, _ in masses) + PACK_KG * pack_x) / veh_pack
vz = (sum(m * z for _, m, _, z, _ in masses) + PACK_KG * pack_z) / veh_pack
rider_z = P["deck_z"] + 0.56 * RIDER_H * 1000
cx = (veh_pack * vx + RIDER * P["rider_x"]) / m_tot
cz = (veh_pack * vz + RIDER * rider_z) / m_tot
print(f"vehicle CoM x {vx:.0f} mm, z {vz:.0f} mm; rider CoM x {P['rider_x']:.0f} mm, z {rider_z:.0f} mm")
print(f"combined CoM x {cx:.0f} mm from the rear axle, z {cz:.0f} mm; static rear load {(G['wheelbase'] - cx) / G['wheelbase'] * 100:.0f} %")

# ---------------------------------------------------------------- 3 road load
hdr("3 Road load, power, current, energy and range")


def f_road(v, grade=0.0, m=m_tot):
    th = math.atan(grade)
    return CRR * m * g * math.cos(th) + m * g * math.sin(th) + 0.5 * RHO * CDA * v * v


E_USE = E_TERM * (1 - RESERVE)
print(f"usable energy {E_USE:.0f} Wh ({E_TERM:.0f} Wh at the terminals less {RESERVE * 100:.0f} % reserve)")
table = {}
for kmh in (15, 20, 25):
    v = kmh / 3.6
    fr = CRR * m_tot * g; fa = 0.5 * RHO * CDA * v * v
    pw = (fr + fa) * v
    pp = pw / ETA + AUX_W
    whkm = pp / kmh
    rng = E_USE / whkm
    table[kmh] = (pw, pp, whkm, rng)
    print(f"{kmh} km/h: rolling {fr * v:.0f} W, air {fa * v:.0f} W, wheel {pw:.0f} W, pack {pp:.0f} W, "
          f"{pp / V_NOM:.1f} A at {V_NOM} V ({pp / V_MIN:.1f} A at {V_MIN} V), {whkm:.1f} Wh/km, "
          f"range {rng:.0f} km flat, about {rng / REAL_FACTOR:.0f} km in real use")
pw20, pp20 = table[20][0], table[20][1]
print(f"20 km/h losses: controller {pw20 / ETA * (1 - ETA_C):.0f} W, motor and gear {pw20 / ETA_M - pw20:.0f} W")
# top speed on the flat at the rated wheel power
v = 5.0
for _ in range(60):
    v -= (f_road(v) * v - P_RATED) / (f_road(v) + RHO * CDA * v * v)
print(f"speed at which road load equals {P_RATED:.0f} W on the flat: {v * 3.6:.1f} km/h (assist cut at 25 km/h)")
i_max = (P_RATED / ETA + AUX_W)
print(f"pack draw at the {P_RATED:.0f} W wheel cap: {i_max:.0f} W, {i_max / V_NOM:.1f} A nominal, {i_max / V_MIN:.1f} A at {V_MIN} V "
      f"(controller limit 15 A)")

# ---------------------------------------------------------------- 4 hill and motor
hdr("4 Hill, acceleration and motor")
v8 = 8 / 3.6
f8 = f_road(v8, 0.08)
p8 = f8 * v8
print(f"8 % at 8 km/h: force {f8:.0f} N, wheel {p8:.0f} W ({(P_RATED - p8) / P_RATED * 100:.0f} % margin to {P_RATED:.0f} W), "
      f"torque {f8 * R_WHEEL:.1f} N m, pack {(p8 / ETA + AUX_W) / V_NOM:.1f} A")
for gr in (0.05, 0.08, 0.10):
    lo, hi = 0.1, 15.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if f_road(mid, gr) * mid > P_RATED:
            hi = mid
        else:
            lo = mid
    print(f"  speed on a {gr * 100:.0f} % grade at {P_RATED:.0f} W: {lo * 3.6:.1f} km/h")
rpm25 = 25 / 3.6 / (2 * math.pi * R_WHEEL) * 60
print(f"wheel speed at 25 km/h {rpm25:.0f} rpm; at 8 km/h {8 / 3.6 / (2 * math.pi * R_WHEEL) * 60:.0f} rpm")
A_LIM = 1.0
f_acc = m_tot * A_LIM + f_road(0.0)
print(f"torque limit for {A_LIM} m/s2 from rest: {f_acc:.0f} N, {f_acc * R_WHEEL:.1f} N m (firmware current limit)")
t, v, dt = 0.0, 0.0, 0.01
t20 = None
while v < 25 / 3.6 - 0.05 and t < 300:
    fdrive = min(f_acc, P_RATED / max(v, 0.01))
    a = (fdrive - f_road(v)) / m_tot
    v += a * dt; t += dt
    if t20 is None and v >= 20 / 3.6:
        t20 = t
print(f"acceleration at the {P_RATED:.0f} W cap: 0 to 20 km/h in {t20:.0f} s; 0 to 25 km/h in {t:.0f} s")
for kmh in (5, 10, 20, 25):
    vv = kmh / 3.6
    a = min(A_LIM, (P_RATED / vv - f_road(vv)) / m_tot)
    print(f"  maximum acceleration at {kmh} km/h: {a:.2f} m/s2")

# ---------------------------------------------------------------- 5 belt
hdr("5 Belt drag, walking power and belt length")
MU_BED = 0.02
F_BEND = 5.0            # belt flexing over two end rollers (assumption)
T0 = 500.0              # belt tension per run (tensioner setting)
F_BRG = 2 * (0.0015 * 2 * T0 * 0.008 / (P["roller_r"] / 1000))
F_DRAG = (0.0, 8.0)
f_bed = MU_BED * RIDER * g
f_walk = [f_bed + F_BEND + F_BRG + d for d in F_DRAG]
v5 = 5 / 3.6
print(f"roller bed {f_bed:.1f} N + bending {F_BEND:.1f} N + end roller bearings {F_BRG:.1f} N + drag 0 to 8 N "
      f"= {f_walk[0]:.1f} to {f_walk[1]:.1f} N at 5 km/h")
print(f"walking power into the belt {f_walk[0] * v5:.0f} to {f_walk[1] * v5:.0f} W at 5 km/h; "
      f"{f_walk[0] * 4 / 3.6:.0f} to {f_walk[1] * 6 / 3.6:.0f} W over 4 to 6 km/h")
print(f"slider deck for comparison (mu 0.1 to 0.2): {0.1 * RIDER * g:.0f} to {0.2 * RIDER * g:.0f} N")
need = {}
for h in (1.60, 1.75, 1.90):
    for kmh, k in ((5, 0.40), (6, 0.45)):
        need[(h, kmh)] = k * h + 0.15 * h
        print(f"  rider {h:.2f} m at {kmh} km/h: step {k * h:.2f} m + foot {0.15 * h:.2f} m = belt {need[(h, kmh)]:.2f} m "
              f"({'fits' if need[(h, kmh)] <= G['belt_usable'] / 1000 else 'does not fit'} {G['belt_usable'] / 1000:.2f} m)")
pitch_190 = (need[(1.90, 6)] * 1000 + 2 * P["roller_r"])
print(f"roller pitch for a 1.90 m rider at 6 km/h: {pitch_190:.0f} mm; vehicle length then about "
      f"{(G['length'] + pitch_190 - P['roller_pitch']) / 1000:.2f} m")
# mechanical drive comparison
lo, hi = 0.1, 5.0
for _ in range(60):
    mid = (lo + hi) / 2
    if f_road(mid) * mid > 40.0:
        hi = mid
    else:
        lo = mid
print(f"if 40 W of walking drove the wheel with no loss: {lo * 3.6:.1f} km/h on the flat; "
      f"a 3 % grade at 5 km/h needs {f_road(v5, 0.03) * v5:.0f} W")
gen_w = (5, 10)
print(f"optional roller generator: {gen_w[0]} to {gen_w[1]} W to the pack, {gen_w[0] / V_NOM:.2f} to {gen_w[1] / V_NOM:.2f} A "
      f"charge in SwapCell mode 4; range gain at 20 km/h about {gen_w[1] / pp20 * 100:.0f} %")

# ---------------------------------------------------------------- 6 control timing
hdr("6 Control timing (R2)")
pitch = 2 * math.pi * P["roller_r"] / 8
v_on = 1.5 / 3.6
per = pitch / 1000 / v_on
stop_det = 3 * per
t_off = stop_det + 0.010 + 0.100 + 0.010
print(f"magnet pitch {pitch:.1f} mm of belt; pulse period at 1.5 km/h {per * 1000:.0f} ms; "
      f"{0.5 / per:.0f} pulses in the 0.5 s start window")
print(f"belt-stop to motor-off: detect {stop_det * 1000:.0f} ms + logic 10 ms + controller ramp 100 ms + current decay 10 ms "
      f"= {t_off * 1000:.0f} ms (target 500 ms)")
print(f"brake lever or lanyard (hardwired to the controller brake-cut input): about 30 ms; "
      f"coast during {t_off * 1000:.0f} ms at 25 km/h {25 / 3.6 * t_off:.1f} m")

# ---------------------------------------------------------------- 7 braking and stability
hdr("7 Braking, pitch-over, cornering and steering column")
A_BR = 3.0
v25 = 25 / 3.6
print(f"stop from 25 km/h at {A_BR} m/s2: {v25 ** 2 / (2 * A_BR):.1f} m after the brakes act")
L_wb, h = G["wheelbase"] / 1000, cz / 1000
xr = cx / 1000
MU = 0.7
a_rear = MU * g * (L_wb - xr) / (L_wb + MU * h)
a_front = MU * g * xr / (L_wb - MU * h)
a_pitch = g * (L_wb - xr) / h
print(f"rear brake alone (tire mu {MU}): {a_rear:.2f} m/s2, {v25 ** 2 / (2 * a_rear):.1f} m; "
      f"front alone: {a_front:.2f} m/s2, {v25 ** 2 / (2 * a_front):.1f} m")
print(f"vehicle pitch-over limit (rider fixed to deck): {a_pitch:.1f} m/s2; rider must resist {RIDER * A_BR:.0f} N at {A_BR} m/s2")
F_brk = RIDER * A_BR
MU_W = 0.3
cap = math.exp(MU_W * math.pi)
t0_min = F_brk / 2 * (cap + 1) / (cap - 1)
print(f"belt on the locked rear roller: capstan ratio {cap:.2f}; tension per run for {F_brk:.0f} N without slip "
      f"{t0_min:.0f} N (set {T0:.0f} N); sprag torque {F_brk * P['roller_r'] / 1000:.1f} N m")
lean = G["lean_clearance_deg"]
for kmh in (15, 25):
    vv = kmh / 3.6
    print(f"  lean clearance {lean:.1f} deg: minimum turn radius at {kmh} km/h {vv * vv / (g * math.tan(math.radians(lean))):.1f} m")
# deck rail bending, simply supported, point load at mid span, two rails share
E, FY = 200e3, 235.0
Lr = rail_len
I_r = (25 * 50 ** 3 - 21 * 46 ** 3) / 12
Z_r = I_r / 25
P_des = RIDER_MAX * g * 2.5 / 2
M_des = P_des * Lr / 4
s_des = M_des / Z_r
d_des = P_des * Lr ** 3 / (48 * E * I_r)
P_step = RIDER * g * 1.2 / 2
s_step = P_step * Lr / 4 / Z_r
cycles = 1.9 * 3600 * 365 * 5
fat_lim = 0.737 * 71 / 1.35
print(f"deck rail 50x25x2: I {I_r:.0f} mm4, Z {Z_r:.0f} mm3; design load {RIDER_MAX:.0f} kg x 2.5 g: "
      f"{s_des:.0f} MPa (factor {FY / s_des:.1f} on {FY:.0f} MPa), deflection {d_des:.1f} mm")
print(f"  walking stress range {s_step:.1f} MPa for about {cycles / 1e6:.1f} million steps in 5 years (1 h a day); "
      f"FAT 71 weld limit with gamma 1.35: {fat_lim:.1f} MPa")
I_60 = (30 * 60 ** 3 - 26 * 56 ** 3) / 12
print(f"  option 60x30x2 rails: walking stress range {P_step * Lr / 4 / (I_60 / 30):.1f} MPa, "
      f"mass +{kg(rhs(60, 30, 2) - rhs(50, 25, 2), 2 * Lr):.2f} kg")
F_bar = 500.0
arm = P["bar_z"] - G["head_top"][1]
for d, t in ((32, 2), (38, 2)):
    Zc = math.pi * (d ** 4 - (d - 2 * t) ** 4) / (32 * d)
    s = F_bar * arm / Zc
    print(f"steering column {d}x{t}: {F_bar:.0f} N at the bar, arm {arm:.0f} mm, {s:.0f} MPa, factor {FY / s:.1f}")

# ---------------------------------------------------------------- 8 SwapCell v0.3
hdr("8 SwapCell interface v0.3 (items W, C, V)")
R_UP, R_CODE, V_S = 100e3, 10e3, 3.3
for r in (R_CODE * 0.99, R_CODE, R_CODE * 1.01 + 0.2):
    print(f"  INTERLOCK loop {r / 1000:.2f} kOhm: node {V_S * r / (R_UP + r):.3f} V (accept 0.24 to 0.37 V)")
print(f"loop current {V_S / (R_UP + R_CODE) * 1e6:.0f} uA; key off opens the loop: output off within 1 ms, "
      f"pack sleeps after 60 s at 100 uA (about 0.72 % per month)")
M_DES, G_SINE, G_SHOCK = 3.5, 8.0, 25.0
f_sine, f_shock = M_DES * g * G_SINE, M_DES * g * G_SHOCK
print(f"class V1 loads for a 3.5 kg design pack: {f_sine:.0f} N at 8 g, {f_shock:.0f} N at 25 g; "
      f"proof {2 * f_shock:.0f} N; receiver preload {1.2 * f_sine:.0f} N; lever ratio {1.2 * f_sine / 50:.1f} at 50 N")
A_M6 = 20.1
print(f"cradle: two M6 8.8 bolts in shear at 25 g: {f_shock / (2 * A_M6):.0f} MPa (factor {0.6 * 800 / (f_shock / (2 * A_M6)):.0f} "
      f"on 480 MPa)")
Zdt = math.pi * (44 ** 4 - 40 ** 4) / (32 * 44)
print(f"down tube 44x2 under 25 g shock at 60 mm standoff: {f_shock * 60 / Zdt:.0f} MPa")
print(f"pack current in use: {pp20 / V_NOM:.1f} A cruise, {i_max / V_MIN:.1f} A maximum; legacy limit 15 A; "
      f"pack heat at the maximum about {(i_max / V_MIN) ** 2 * 0.110:.1f} W (110 mOhm)")

# ---------------------------------------------------------------- 9 cost
hdr("9 Cost")
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
tot = 0.0
for r in bom:
    c = float(r["unit_cost_usd"]) * float(r["qty"])
    if not r["Item"].startswith("11 "):
        tot += c
print(f"BOM lines {len(bom)}, all priced: {all(r['unit_cost_usd'].strip() for r in bom)}")
print(f"StepGen parts total (pack excluded) ${tot:.0f} against budget ${budget:.0f}: "
      f"{'over' if tot > budget else 'under'} by ${abs(tot - budget):.0f} ({abs(tot - budget) / budget * 100:.0f} %)")
cost = {r["Item"].split()[0]: float(r["unit_cost_usd"]) for r in bom}
salv = tot - (cost["2"] + cost["3"] - 40) - (cost["7"] + cost["9"] - 50)
print(f"salvage route (walking-pad treadmill for items 2 and 3 at $40, donor 20 in bike for items 7 and 9 at $50): ${salv:.0f}")

# ---------------------------------------------------------------- results
hdr("Results by requirement")
res("R1", f"Usable belt {G['belt_usable'] / 1000:.2f} m x {P['belt_w'] / 1000:.2f} m; push {f_walk[0]:.0f} to {f_walk[1]:.0f} N at 5 km/h; "
    f"1.00 m fits a 1.75 m rider only up to 5 km/h", "1.0 m, 0.36 m, 30 N at 5 km/h", "At risk")
res("R2", f"Belt-stop to motor-off {t_off * 1000:.0f} ms; brake and lanyard about 30 ms; start after {0.5 / per:.0f} pulses in 0.5 s",
    "Start after 0.5 s above 1.5 km/h; off within 0.5 s", "Met (on paper)")
res("R3", f"Cut at 25 km/h, beginner 15 km/h; torque limit {f_acc * R_WHEEL:.0f} N m gives {A_LIM} m/s2",
    "25 km/h, 15 km/h mode, 1.0 m/s2 or less", "Met (on paper)")
res("R4", "250 W rated motor specified; wheel power capped at 250 W", "250 W rated or less", "Met (on paper)")
res("R5", f"{table[20][3]:.0f} km at 20 km/h on the flat ({table[20][2]:.1f} Wh/km); about {table[20][3] / REAL_FACTOR:.0f} km in real use",
    "30 km at 20 km/h", "Met")
res("R6", f"{p8:.0f} W at the wheel for 8 % at 8 km/h ({(P_RATED - p8) / P_RATED * 100:.0f} % margin)", "8 % at 8 km/h within 250 W",
    "At risk")
res("R7", f"{v25 ** 2 / (2 * A_BR):.1f} m at 3 m/s2; rear brake alone {v25 ** 2 / (2 * a_rear):.1f} m; belt held by sprag with {T0:.0f} N tension",
    "Two brakes; 10 m from 25 km/h; belt cannot run forward", "Met (on paper)")
res("R8", f"Belt top {P['deck_z']:.0f} mm; side boards 6 mm proud of the belt, no rails", "250 mm or less; open sides", "Met")
res("R9", "Guards modelled at both nips, rear tire and belt ends; gaps not yet checked against ISO 13857",
    "Nips, spokes and rear tire guarded", "Not verifiable at TRL 3")
res("R10", f"{G['length'] / 1000:.2f} m long, {G['width'] / 1000:.2f} m wide, {veh_pack:.1f} kg with pack "
    f"({40 - veh_pack:.1f} kg margin, less than a 10 % growth allowance)", "2.4 m, 0.65 m, 40 kg", "At risk")
res("R11", f"Interface v0.3: 10 kOhm coded INTERLOCK (node 0.30 V), vehicle heartbeat mode 2; {i_max / V_MIN:.1f} A maximum; below 60 V",
    "SwapCell v0.3 unchanged; 15 A or less; below 60 V DC", "Met (on paper)")
res("R12", f"${tot:.0f} excluding the pack; salvage route about ${salv:.0f}", f"${budget:.0f} excluding the pack",
    "Not met" if tot > budget else "Met")
res("R13", f"Class V1 receiver specified: preload {1.2 * f_sine:.0f} N, lever ratio {1.2 * f_sine / 50:.1f}, bolts factor "
    f"{0.6 * 800 / (f_shock / (2 * A_M6)):.0f} at 25 g", "SwapCell latch class V1, no release or contact break",
    "Not verifiable at TRL 3")
for r in rows:
    print(" | ".join(r))
with (Path(__file__).parent / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    w.writerows(rows)
print("\nwrote docs/04-calcs/results.csv")
