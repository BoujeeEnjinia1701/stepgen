# Review note: StepGen

## Session 2026-09-25: concept change to a walking-treadmill vehicle (TRL 2)

### Concept change (decided by Amish)

On 2026-09-24 Amish decided that StepGen is a walking-treadmill vehicle, like the Dutch Lopifit walking bike: "as the person walks his scooter / bike moves forward but hes upright walking instead of pedalling". The stationary stepper generator concept of version 0.2, which charged a PowerBox, is dropped entirely. PowerBox therefore loses StepGen as a charging source; the PowerBox repo was not touched in this session. This is the only item in this note recorded as decided. Everything else is proposed, awaiting Amish.

### What was done

- `docs/01-problem.md` (SGN-PRB-001 v0.3): new problem (personal mobility for people who do not cycle), why the belt is a control input and not the engine, users, constraints, legal status in the EU and US with sources, out of scope, prior work (Lopifit, mechanical treadmill bikes, ElliptiGO, scooters), co-design checklist and first-session questions.
- `docs/02-concept.md` (SGN-PRC-001 v0.3): how it works, 15 components numbered to match the exploded view and BOM, key numbers table, why the motor does the work, assist law sketch, SwapCell interface use and gaps, design choices, safety, open questions for TRL 3.
- `docs/03-requirements.md` (SGN-REQ-001 v0.3): the stepper requirements withdrawn and 12 new requirements (R1 to R12) with assumptions and requirements at risk.
- `cad/src/concept_media.py`: new massing model (frame, belt and end rollers, roller bed, anti-reverse clutch, belt speed sensor, 20 in wheels with rear hub motor, fork, steering column, brakes, SwapCell cradle and pack, controller, display and lanyard stop, guards, harness) with a 1.75 m rider standing on the belt mid-stride and holding the bar. A custom two-path flow diagram (energy and control) and a cropped deck cutaway are drawn in the same script. `cad/src/model.py` is still the scaffold placeholder and was not used.
- `media/`: hero, blueprint sheet SGN-DWG-010 (PNG, PDF, SVG), cutaway of the belt deck, exploded view with callouts 1 to 15, energy and control flow (estimates marked), `model.glb` and `viewer.html`. All regenerated; all carry "CONCEPT, NOT FOR FABRICATION".
- `bom/bom.csv` and `bom/bom-notes.md`: new 16-line BOM, items 1 to 15 matching the exploded view; the SwapCell pack is listed at $0.00 and excluded from the total, as in PowerBox.
- `project.yaml`: new `pitch`, `problem` (with the co-design sentence) and tags. `area`, `budget_usd`, `trl` and `trl_target` unchanged.
- `README.md`: pitch, problem, key components, safety and hero caption updated; hero image and links line kept before "Problem".
- `docs/pdf/`: PDFs of the three documents at v0.3.
- `docs/04-calcs/` holds only `.gitkeep`, so there were no stepper calculations to update. `docs/decisions/` holds only the template, so there was no stepper decision record to supersede and no new record was added (see suggestions).

### Key results (estimates, to be checked at TRL 3)

Assumptions: 80 kg rider, about 35 kg vehicle, 2.8 kg pack (about 118 kg total), Crr 0.010, CdA 0.70 m², motor 80 % and controller 95 % efficient, about 410 Wh usable from one SwapCell pack.

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Walking speed on the belt | 4 to 6 km/h | R1 |
| Rider push and power into the belt | 15 to 30 N, about 20 to 40 W (all spent as belt drag) | R1 (30 N) met |
| Vehicle speed | Up to 25 km/h; 15 km/h beginner mode; about 20 km/h cruise | R3 met by design |
| Motor | 250 W rated rear geared hub; about 136 W at the wheel at 20 km/h, 221 W at 25 km/h | R4 met |
| Pack draw | About 179 W (3.8 A) at 20 km/h; about 291 W (6.2 A) at 25 km/h; 15 A limit | R11 met |
| Energy per km | About 6.9, 9.0 and 11.6 Wh/km at 15, 20 and 25 km/h | |
| Range per SwapCell pack | About 60, 46 and 35 km at 15, 20 and 25 km/h on the flat; perhaps 25 to 35 km in real use | R5 (30 km at 20 km/h) met |
| Hill | 8 % at 8 km/h needs about 236 W at the wheel | R6 met, thin margin |
| Mass | About 35 kg without the pack, 38 kg with it | R10 (40 kg) met, thin margin |
| Size | About 2.35 m long, 0.62 m wide, belt top 240 mm above the ground, belt 1.05 m by 400 mm | R8, R10 met; length margin thin |
| Braking | About 8 m from 25 km/h at 3 m/s² | R7 met on paper |
| Optional roller generator | About 5 to 10 W back to the pack for about 15 W more walking effort; about 5 % more range | Not recommended now |
| Mechanical belt drive (for comparison) | About 7 to 9 km/h at best on the flat; stalls on a 3 % grade | Why the motor does the work |
| Parts cost | About $630 excluding the SwapCell pack (pack about $370 more) | R12 ($400) **not met** |

Requirements not met or at risk:

- **R12 (cost) is not met.** About $630 excluding the pack, about $230 over $400. Salvaged treadmill and bike parts might bring it to about $450 to $500, still over budget.
- **R6 and R10** are met with thin margins (hill power close to the 250 W rating; length 2.35 m against 2.4 m; mass 38 kg against 40 kg).
- **Legal category is unresolved.** EU pedelec rules and US e-bike definitions both assume pedals. The design follows EU pedelec limits, but that may not be enough for road use.
- **R11** depends on SwapCell choices that are still open (connector family, latch vibration rating, CAN bit layout).

### Proposed, awaiting Amish

1. **Form factor.** Recommended: two-wheel, long-wheelbase, bike type (about 2.35 m, like the Lopifit), because a natural stride needs about 1.0 m of belt. Alternatives: a compact scooter type (short belt, shuffling steps, small wheels) or a three-wheel tadpole (stable at rest for non-cyclists, but wider and heavier). Keep the three-wheel option open until co-design.
2. **Wheels.** Recommended: 20 in front and rear. Alternatives: 28 in front with 20 in rear (Lopifit layout) or 16 in all round.
3. **Motor and speed class.** Recommended: 250 W rated rear geared hub, assist cut at 25 km/h, 15 km/h beginner mode (EU pedelec limits). Alternatives: US class 1 style 32 km/h (20 mph) with 500 to 750 W, or a 20 km/h cap throughout.
4. **Target range.** Recommended: 30 km at 20 km/h on the flat on one SwapCell pack (R5). Alternative: a double pack for longer trips, which SwapCell lists only as a later variant.
5. **Regeneration option.** Recommended: no roller generator in the first concept; keep a mounting point on the front roller. It returns only about 5 to 10 W and needs a SwapCell charge-while-driving mode that does not exist.
6. **Area.** Proposed: move `area` from CleanTech to Mobility and Logistics, matching SunSpoke and WaterWalker. `project.yaml` still says CleanTech.
7. **Budget.** Proposed: raise `budget_usd` from $400 to about $650 (pack excluded). Alternative: keep $400 and design around a salvaged treadmill and a donor bike, which the estimate suggests would still land at about $450 to $500. `project.yaml` still says $400.
8. **Legal route.** Proposed: pick a first target country and confirm the vehicle's legal category there before any road use.
9. **First user group and partner.** Non-cycling adults, older adults or commuters.

### Safety concerns

- Falls on a moving belt: stumbling, stopping walking abruptly, and a rider leaving the deck at speed. Free-running belt, 0.5 s motor cut-off, lanyard stop, low open deck and handlebar are the controls; rider dynamics need a TRL 3 study.
- Braking with feet on a belt: without the anti-reverse clutch the feet would slide forward. Hard braking can pitch a standing rider over the bar.
- Pinch points: belt in-running nips at both rollers, the rear tire behind the heel, spokes, and clothing such as long skirts. Guards to ISO 13857 reach distances.
- Speed and height: 25 km/h limit and a beginner mode; the rider's head is about 2 m up, so a helmet is essential.
- Stability of a standing rider in turns and when parked; kickstand needed.
- Lithium pack at up to 54.6 V: SwapCell BMS, interlock and warn-then-derate rules apply; charge only in a dock; 20 A harness fuse.

### Suggestions (not done)

- Add a design decision record (`docs/decisions/0001-...`) for the concept change, if Amish wants one; the prompt asked for it only if a stepper record already existed.
- Tell the SwapCell project about the two gaps StepGen hits: latch vibration rating for vehicles, and charging from a vehicle while driving.

### Recommended next step

Review this note and the media, and decide the proposed items above, especially form factor, speed class, budget and area. Start co-design with non-cycling users before `/advance-trl3`, since balance and step-off may change the form factor. If approved, `/advance-trl3` should do the calculation note (road load and range, hill and acceleration, belt drag and roller bed, braking and rider dynamics, frame loads and steering geometry, stability), the parametric model with STEP export and drawing sheet, and a fully priced BOM.
