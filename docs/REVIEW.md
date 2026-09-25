# Review note: StepGen

## Session 2026-09-24: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (SGN-PRB-001 v0.2): the problem, an honest energy framing table (what one hour of stepping covers and what it does not), why a stepper instead of a bicycle, users and context, constraints, out of scope, prior work, co-design checklist kept.
- `docs/03-requirements.md` (SGN-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets, planned verification, assumptions and requirements at risk.
- `docs/02-concept.md` (SGN-PRC-001 v0.2): how it works, 12 main components numbered to match the exploded view and BOM, pedal power table, efficiency chain, gear ratio and generator speed, flywheel sizing idea, resistance, size, mass and cost, proposed design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model (base frame, pedals on a rocker, freewheels and jackshaft, chain stage, belt stage, flywheel, generator, guard, handrail, controller, display, output lead) with the 1.75 m scale figure. The guard, handrail and display are left out of the cutaway so the drivetrain shows.
- `media/`: hero, blueprint sheet (PNG, SVG and PDF), cutaway, exploded view with BOM callouts, energy flow diagram (values marked as estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 13 lines with indicative prices, items 1 to 12 numbered to match the exploded view; `bom/bom-notes.md`.
- `README.md`: hero image and links line added before "Problem".
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Work per step | 103 J (70 kg, 15 cm) | |
| Pedal power | 52 to 103 W at 30 to 60 steps per minute | R1 met |
| Pedal to pack efficiency | about 70 % (drivetrain 90 %, generator 85 %, rectifier 97 %, charger 94 %) | R6 (65 %) met |
| Stored per hour | about 36 to 72 Wh | R2 met, thin margin at 30 steps per minute |
| Gear ratio and generator speed | 40:1, about 900 to 1,800 rpm mean | |
| Generator voltage | about 15 to 30 V working, about 50 V at 3,000 rpm overspeed (Kv about 60) | R7 (under 60 V) met |
| Flywheel | 300 mm x 6 mm steel, about 3.3 kg, J about 0.037 kg·m², about 12 % speed dip between steps at 30 steps per minute | |
| Footprint and mass | 0.85 x 0.62 m, about 1.1 m high, about 34 kg | R9 met, thin mass margin |
| Parts cost | about $397 | R12 met, almost no margin |

Requirements not met or unverified:

- **The pitch figure of 60 to 100 Wh stored per hour is not supported for the nominal user.** At 70 % efficiency it needs about 85 to 145 W at the pedals. The honest range for a 70 kg user at 30 to 60 steps per minute is about 35 to 70 Wh per hour. `project.yaml` and the README pitch still say "40 to 100 W, or about 60 to 100 Wh"; they were not changed because the pitch is Amish's decision.
- **R8 (noise 60 dBA at 1 m)** is unverified; no noise estimate yet.
- **R5** depends on the PowerBox pack being 13-series (39 to 54.6 V); this is assumed, not confirmed.

### Proposed, awaiting Amish

1. Pitch: change to "50 to 100 W at the pedals, or about 35 to 70 Wh stored per hour for a 70 kg user". Alternative: keep 60 to 100 Wh but state that it applies to heavier users or 60 steps per minute. Recommendation: change it.
2. One-way clutches: two 16T bicycle freewheels (recommended, cheap and proven) or sprag clutch bearings (quieter, more costly).
3. Flywheel: small fast flywheel on the generator shaft (recommended, about 3.3 kg) or a heavy slow flywheel on the jackshaft (about 20 kg or more).
4. Step-up: chain 4:1 then poly-V belt 10:1 (recommended) or a planetary gearbox.
5. Electrical: generator below pack voltage with a buck-boost charger (recommended, keeps every circuit under 60 V) or a lower-Kv generator with a buck charger.
6. Generator: 63 mm class outrunner, Kv about 60 (recommended), an e-scooter motor, or a salvaged motor.
7. No battery inside StepGen; all storage in the PowerBox.
8. Budget stays at $400. It is met with about $3 of margin; salvaged bicycle parts could free $50 to $100. No budget change is proposed now.
9. First user group and partner: outage-prone city households, a settlement community organization, or a community hub.

### Safety concerns

- Moving machinery that a person stands on: pinch and crush points at the pedals, chains, belt and flywheel. Full guarding and ISO 13854 crush gaps are required (R10).
- Flywheel rim speed up to about 28 m/s: the guard must contain a loose disc; a burst and containment check is needed at TRL 3.
- Falls: handrails on both sides, non-slip treads, low pedal height, end stops, and a controller that never removes load suddenly.
- Electrical: every circuit under 60 V DC including overspeed; the PowerBox is lithium-ion, so charging must respect its limits and fault signal. Fused output lead; emergency stop brakes the flywheel.
- Exertion: sustained stepping at 60 steps per minute is vigorous; the documents say so.

### Recommended next step

Review this note and the media, decide the pitch wording and the proposed choices above, and confirm the PowerBox interface. If approved, run `/advance-trl3` to write the calculation note (efficiency chain, gear ratio, flywheel, generator voltage and overspeed, frame and tip stability, noise estimate), build the parametric model with STEP export and the drawing sheet, and complete the priced BOM.
