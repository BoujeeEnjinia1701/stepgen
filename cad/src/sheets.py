"""StepGen general arrangement drawing SGN-DWG-001 (Rev P3).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/SGN-DWG-001.svg, .pdf and .png from the parametric model.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, geometry, build_parts, assembly  # noqa: E402

G = geometry()
parts, _ = build_parts()
asm = assembly(parts)
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="StepGen", title="General arrangement, walking-treadmill vehicle", dwg_no="SGN-DWG-001",
          rev="P3", author="Amish Chadha", date="2026-10-01", concept=True,
          material="Frame: welded mild steel (S235 class) RHS and tube; guards Al sheet and HDPE. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA for TRL 3 (SGN-CAL-001), SwapCell v0.3", "2026-09-25", "AC"),
                     ("P2", "Deck rails 60 x 30 x 2 (SGN-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Design for construction (SGN-DDR-003)", "2026-10-01", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 80, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions (mm) and interfaces", [
    f"Overall {G['length']:.0f} long (fender) x {G['width']:.0f} wide (bar) x 1293 high",
    f"Wheelbase {G['wheelbase']:.0f}; 20 in (ETRTO 406) wheels, tire OD {2 * P['wheel_r']:.0f}",
    f"Head angle {P['head_angle']:.0f} deg, fork offset {P['fork_offset']:.0f}, trail {G['trail']:.0f}",
    f"Belt {P['belt_w']:.0f} wide; end rollers {P['roller_pitch']:.0f} apart, usable {G['belt_usable']:.0f}",
    f"Belt top {P['deck_z']:.0f} above ground; ground clearance {G['ground_clearance']:.0f}",
    f"Bar {P['bar_z']:.0f} above ground ({G['bar_above_belt']:.0f} above belt)",
    f"Lean clearance {G['lean_clearance_deg']:.0f} deg (kickstand)",
    f"Deck rails {P['rail_h']:.0f} x {P['rail_w']:.0f} x {P['rail_t']:.0f} RHS; column 38 x 2; down tube 44 x 2",
    "Head tube 50 x 3 machined, ZS44; fork 26 in size, 20 in wheel",
    "SwapCell v0.3 receiver, latch class V1 on down tube:",
    "  preload 330 N via over-centre lever with detent,",
    "  10 kOhm INTERLOCK coding resistor in series with key",
    "Mass about 35.1 kg without pack, 37.9 kg with pack",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=124, width=140)
s.save(ROOT / "cad/drawings/SGN-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/SGN-DWG-001.svg, .pdf, .png")
