"""StepGen concept media from the parametric model (TRL 3).

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py; not for fabrication.

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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import PARAMS, geometry, build_parts  # noqa: E402  (single source of geometry, TRL 3)

G = geometry()
DECK_Z = PARAMS["deck_z"]
BAR = (PARAMS["bar_x"], PARAMS["bar_z"])


def tube3(a, b, r):
    """Round tube between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


_parts, deck_frame = build_parts()
parts = [Part(n, sh, col, bom, ex) for n, sh, col, bom, ex in _parts]


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
    node(0.3, ey, "SwapCell pack", "182 W out (est.)")
    node(3.4, ey, "Controller", "170 W to motor (est.)")
    node(6.5, ey, "250 W hub motor", "136 W at wheel (est.)")
    node(9.6, ey, "Wheel at 20 km/h", "9.1 Wh/km from pack (est.)", w=2.8)
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
    node(6.5, cy, "Free-running belt", "30 to 41 W into drag (est.)", fc="#F9FAFB", ec="#4B5563")
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
    ax.text(1.35, 2.55, "to pack: about 6 % more\nrange (est.); would use\nSwapCell v0.3 mode 4;\nnot fitted (decided)",
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
                     "250 W rear hub motor, assist cut at 25 km/h (decided)",
                     "About 9.1 Wh/km at 20 km/h; about 45 km per SwapCell, flat (SGN-CAL-001)",
                     "Belt top 240 mm above ground; 20 in wheels; 2.35 x 0.61 m",
                     "About 35 kg without pack; parts about $546 (salvage build), pack excluded"],
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
