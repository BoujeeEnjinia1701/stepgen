# Review note: StepGen

## Session 2026-10-02: open decisions decided by Amish

Authority: Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." The recommendations approved are those written for the open decisions in the design decisions register. No model, BOM quantity or price, or picture was changed; where a decision needs one, it is listed below as a follow-up. `trl` and `trl_target` stay at 3. No commit or push.

### Decisions recorded

7, all moved to "Decisions made" in `docs/06-design-decisions.md`, dated 2026-10-02:

1. Design for construction (SGN-DDR-003) accepted: P1 to P17 as made.
2. First user group: non-cycling adults of working age who walk or take transit; older adults second, once balance is understood.
3. First target country: the Netherlands, with the legal category confirmed with the RDW before any road use.
4. Rider pose: shorter stride accepted for the renders; stride length on the 1.0 m belt added to the co-design checks.
5. Wheel detail: appearance only; rotor carriers confirmed when the wheel build is specified.
6. Branding: wordmark, pinstripe and accent colours as the reference scheme; the "250 W 25 km/h" rating decal dropped from the renders until the legal category is confirmed.
7. Three-wheel version: keep two wheels; balance becomes a fixed co-design test, and the three-wheel version is designed if most non-cyclists cannot ride at walking pace after a short trial.

### Documents changed

- `docs/06-design-decisions.md` (SGN-DEC-001 v0.2)
- `docs/decisions/0003-design-for-construction.md` (SGN-DDR-003 v0.2): accepted; status stays Draft
- `docs/decisions/0001-trl2-review-decisions.md` (SGN-DDR-001 v0.3): items 13 and 14 decided; balance test noted on item 1
- `docs/decisions/0002-recommendations-accepted.md` (SGN-DDR-002 v0.2): items 6 and 7 decided
- `docs/01-problem.md` (SGN-PRB-001 v0.6): user group, country, balance test, stride check
- `docs/02-concept.md` (SGN-PRC-001 v0.7): country and RDW check; balance test
- `docs/03-requirements.md` (SGN-REQ-001 v0.7): legal classification note
- `docs/05-build-plan.md` (SGN-BLD-001 v0.2): safety stop S7 names the RDW check

### Follow-up actions to carry approved decisions into the design

1. Decision 5 (bom): Confirm the rotor carriers against the hub and front hub when the wheel build is specified (BOM lines for the wheels).
2. Decision 6 (pictures): Remove the "250 W 25 km/h" rating decal from `cad/src/product_model.py` and re-render the photoreal renders, card and social preview on Amish's Mac.
3. Decision 3 (calcs): Once the RDW check is done, restate R3 and R4 in SGN-REQ-001 and SGN-CAL-001 if it sets a lower speed cap or requires type approval.

### Points found in the review

- The 250 W, 25 km/h limits follow EU pedelec rules, which cover only pedal-assisted cycles; a pedal-less vehicle probably falls outside them, so the legal check in item 3 may force a lower speed cap or type approval.

## Session 2026-10-01: design made constructable and prototype build plan (kit 1.7.0)

Under Amish's 2026-09-30 approval of the build plan format ("Extend this across all the other repos") and his instruction to make each design physically buildable while drawing it, this session brought StepGen to the approved standard. TRL stays at 3; nothing was built or tested.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, root `CLAUDE.md`).
- `cad/src/model.py` rebuilt from 29 components, each made or bought and fixed to its neighbours, with 72 build123d constructability checks (`python cad/src/model.py --check`): all pass. STEP and STL re-exported.
- `docs/decisions/0003-design-for-construction.md` (SGN-DDR-003, draft): every change and its reason.
- `docs/05-build-plan.md` (SGN-BLD-001 v0.1) from the kit template, with pictures for every component, joint and step.
- `docs/06-design-decisions.md` (SGN-DEC-001 v0.1): open decisions, items to confirm when parts are bought, value engineering, decisions made.
- `cad/src/build_plan_media.py`: overview, 14 making sketches (SGN-DWG-101 to 114), 12 joint close-ups, 19 step pictures (step 6 has two close-ups), a rail hole layout and a wiring diagram. Every picture was looked at and these fixed: the harness is drawn as one cable (its run inside the left rail included) in the overview and step 13; the Hall sensor and rear caliper, too small to show under a number badge, are drawn with the front roller and rear wheel in the overview (22 numbered components); the part being fitted in each step is always in colour; steps 6 and 12 are close-ups; joints 3, 5 and 8 recoloured and re-angled so each part reads; the roller cover sketch draws the two covers side by side so their profiles read. `python .kit/drawing.py --check-text` finds no overlaps.
- `cad/src/sheets.py`: general arrangement SGN-DWG-001 to Rev P3. `cad/src/concept_media.py`: concept media regenerated.
- `docs/04-calcs/sizing.py` and SGN-CAL-001 v0.3 re-run; SGN-PRC-001 and SGN-REQ-001 to v0.6; `bom/bom.csv` and `bom/bom-notes.md` restated and repriced; `project.yaml` (`design_state: constructable`, new evidence); README links line and "Building the prototype" section.

### Design changes made for construction (SGN-DDR-003)

1. Upper rear stays no longer pass through the rear roller and belt: two stays a side, from the rail end caps and the rear cross member to the dropouts.
2. Brake rotors moved inside the dropouts and fork legs; rear caliper on a tab on the left dropout, front caliper on the fork's post mount.
3. Dropouts as 6 mm plates 135 mm apart with slots open downward; torque arms added.
4. Bought head tube machined for a ZS44 headset (50 x 3 mm) replaces the 44 x 3 mm tube; 26 in size fork (axle to crown about 410 mm) carries the 20 in wheel; headset modelled. Steering geometry unchanged.
5. Down tube joins the head tube's side 100 mm above its bottom, so the fork turns 45 degrees each way clear of the frame.
6. Nose tubes and block replaced by a 60 x 40 x 2 mm nose beam across the rail ends.
7. Two cross members welded under the rails (were cut into them); ground clearance 145 mm (was 148 mm).
8. End rollers on fixed axles bolted to the rails; rear axle in slots with M8 tension bolts; anti-reverse clutch is a one-way bearing inside the rear roller; belt drag is a felt-tipped screw through the right rail; magnet ring on the front roller end with the sensor inside the left rail. Lean clearance 32.6 degrees (was 30).
9. Roller centres 3 mm lower so the belt wraps them (it overlapped); belt top still 240 mm.
10. Idler carriers are 50 x 3 mm aluminium bars screwed inside the rails.
11. Side boards on 13 mm spacers, 9 mm proud of the belt (was 6 mm and floating).
12. Heel guard, roller covers and toe guard given flanges and tabs to the frame; bought fender riveted to the heel guard and stayed to the dropouts; front cover now covers the in-running nip under the front roller.
13. Receiver cradle is a folded 3 mm channel on two welded tabs with an end stop plate and an over-centre lever beside the pack handle; pack 0.54 of the way up the down tube (was 0.55).
14. Controller moved from under the down tube (in the front tire's path) to a plate on its left side.
15. Welded steering column that clamps the steerer; straight 580 mm bar (width 0.58 m, was 0.61 m); controls each on their own clamp; display faces the rider.
16. Kickstand on a welded plate; harness inside the left rail between grommets.
17. Overall length 2.38 m with the fender (2.35 m over the tires).

### Key results (SGN-CAL-001 v0.3)

- Vehicle 35.1 kg without the pack, 37.9 kg with it (R10 margin 2.1 kg, at risk as before); 2.38 m long, 0.58 m wide.
- Value-engineering target: USD 650. Estimated cost of the constructable design: USD 610 on the salvage reference build (USD 40 under the target; was USD 546). The donor bike's fork no longer fits the head tube, so the fork and headset are bought (about USD 40). All new: USD 750 (USD 100 over the target).
- Requirement status unchanged: none not met; R1, R6, R10 at risk; R9 and R13 not verifiable at TRL 3; the rest met on paper.

### Decisions proposed and awaiting Amish

Listed in `docs/06-design-decisions.md`: acceptance of SGN-DDR-003 (P1 to P17), first user group, first target country, three render appearance items, and the three-wheel version (open until co-design). Eight items to confirm when parts are bought, including the 26 in fork with 30 mm offset.

### Stale on Amish's Mac

The design changed visibly, so `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` are stale (they show the nose tubes, swept grips, outboard clutch housing and solid cradle). They were not regenerated here.

### Safety

Unchanged in substance. The build plan adds safety stops for welding, first standing on the belt, the pack and first power (SGN-BLD-001 section 6). The key switch still cuts the pack at once and is for use at a standstill only.

### Recommended next step

Amish reviews SGN-DDR-003 and the register. TRL 4 (building and testing to the plan) stays on hold under the portfolio cap.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; the render images themselves (`media/render-hero.png`, `media/render-exploded.png` and a detail view) are produced later by the portfolio render run.

### What was done

- `cad/src/product_model.py`: `product_parts()` returns 96 parts (67 shell, 21 internal, 7 accessory, 1 context), each with a colour, a material class, its BOM line and an explode offset, plus `TITLE` and three `RENDER_VIEWS` (hero with the rider, exploded, and a detail view without the rider). Geometry reuses `PARAMS` and `geometry()` from `cad/src/model.py`; every main dimension and interface is unchanged.
- Appearance detail added:
  - Painted steel frame with rounded rectangular deck rails, a teal pinstripe, a "STEPGEN" wordmark and a "250 W 25 km/h" decal on the rail sides; headset cups; the kickstand stowed as in model.py.
  - Belt with a fine tread texture; crowned end rollers with axle nuts; the 14 idler rollers on their aluminium angle carriers.
  - Light grey guards (rear fender, heel guard with a rear reflector, roller covers, toe guard with a teal accent) and side boards with ribbed rubber foot pads and screws.
  - 20 in wheels with treaded tires, rims, 28 laced spokes, valves and drilled 160 mm rotors on spider carriers; calipers.
  - Hub motor with a painted shell, aluminium side covers, a bolt circle, a teal band, axle nuts, torque arms and its cable.
  - Anti-reverse clutch housing with a teal drag knob; belt-speed sensor with a clear cap over the 8-magnet ring and a lit pulse light.
  - Controller in a finned case with a clear side window over the walking logic board, ESP32 module and a lit status light; cable glands; the wiring harness with a sealed 20 A fuse holder and cable ties.
  - SwapCell pack (interface v0.3) in the SwapCell visual language: grey tray, light lid, lit charge bar, interface label and ribbed carry handle; class V1 cradle with the teal over-centre lever, pivot and tube clamps.
  - Handlebar with ribbed grips and teal bar-end plugs, brake levers with cut-off switch bodies, display with a lit readout, level selector with a lit ready light, key switch and a red magnetic lanyard stop with a coiled cord.
- Context: the shared clay mannequin (`.kit/context_parts.py`, 1.75 m) standing on the belt with its pelvis over `rider_x` (950 mm), in a walking stride, with both hands on the grips (arm angles solved to the grip points).
- `README.md`: hero image now points to `media/render-hero.png`, with an "Exploded render" link added to the links line.
- Previews (matplotlib, clear parts left out) were checked for the hero, exploded and detail views.

### Where the appearance model differs from model.py

Each item is **Proposed, awaiting Amish**.

1. **Rider pose.** The mannequin uses the "push" preset (hands closed on the grips) with walk-type leg angles and a shorter stride than the kit's walk preset: the preset stride put the leading toe on the toe guard, since the usable belt is 1.0 m. Recommendation: accept for renders; the rider's stride on a 1.0 m belt is worth checking in co-design, because a long stride may reach the toe guard.
2. **Display tilt.** model.py tilts the display top 20 degrees toward the rider, so the screen face on the rider side points slightly downward, away from the rider's eyes. The appearance model keeps the model.py envelope and tilt. Recommendation: reverse the tilt in model.py at the next model update so the screen faces up toward the rider.
3. **Wheel detail.** model.py draws 12 radial placeholder spokes; the appearance model shows 28 laced spokes, a tread and a spider carrier for each rotor (the rotors sit outboard of the hub in model.py). Recommendation: accept as appearance only; confirm the rotor carrier arrangement when the wheel build is specified.
4. **Branding and markings.** The wordmark, rating decal, pinstripe and accent colours are appearance choices, not part of the BOM. Recommendation: accept, or give a preferred marking scheme.

### TRL status

This is an appearance model only, for renders: no tolerances, fabrication detail, PCB layout or build steps. `trl` stays 3 and TRL 4 remains on hold under the portfolio cap.

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to fix the weaker sources in the README. Every link below was fetched and checked against the claim. No controlled document changed; TRL stays at 3.

| README location | Old source | New source |
| --- | --- | --- |
| Concept rationale (Lopifit price and mass) | Lopifit, "What is a Lopifit?" | Kept (manufacturer's own page; states from €2,999 and 55 kg gross) |
| Countries: Netherlands | Scouters.nl (retailer guidance on 6 km/h pavement rule) | Government of the Netherlands, bicycle policy (27 % of journeys by bicycle; over half of car trips under 7.5 km) and Lopifit; the pavement-rule claim was dropped from the README |
| Countries: India | None | IEA, Global EV Outlook 2024 (second-largest electric two-wheeler market, sales up 40 % in 2023, over 15 % cheaper than petrol after subsidies) |
| Countries: East Africa (for example Kenya) | None | Row narrowed to Kenya; UNEP electric two and three wheelers programme page |
| Countries: Latin America (for example Brazil) | None | Row rewritten as Latin America; IEA, Global EV Outlook 2024 (role of two- and three-wheelers in daily transport). An IBGE census source for Brazil could not be fetched, so Brazil-specific claims were removed |
| What sparked the idea | Lopifit, "What is a Lopifit?" | Strengthened: same page plus Lopifit, "Our story"; wording now matches the source (Dutch invention by Bruin Bergmeester; company based in Utrecht) |

Open: `docs/01-problem.md` still cites Scouters.nl for the Dutch 6 km/h pavement rule and Wikipedia, Redtail, New Atlas and SolidSmack elsewhere. No primary source for the Dutch rule was verified this session; replacing these is left for the next problem-statement revision.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (SGN-DDR-002 v0.1). TRL stays at 3 (`trl: 3`, `trl_target: 3`).

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| 1 | Cost (R12): keep $650, salvage route is the reference build, new parts the fallback | R12 not met, $713 all new | R12 met on paper, $546 reference build; $721 all new (reported, not held to R12). `budget_usd` unchanged at $650; R12 text restated |
| 2 | Belt length: keep 1.05 m pitch and 2.35 m length until co-design | R1 at risk | No geometry change; R1 still at risk, held until co-design |
| 3 | Deck rails 50 x 25 x 2 mm to 60 x 30 x 2 mm | Weld stress range 37.6 MPa (limit 38.8); static factor 2.0; frame 11.4 kg; vehicle 34.0 kg, 36.8 kg with pack; hill 233 W; BOM item 1 $75 | 25.5 MPa; factor 3.0; frame 12.5 kg; vehicle 35.0 kg, 37.9 kg with pack (R10 margin 3.2 to 2.1 kg); hill 235 W (R6 margin 7 to 6 %); item 1 $83 |
| 4 | Key switch in series with the 10 kΩ INTERLOCK coding resistor, standstill use only | Proposed (already modelled and priced) | Decided; wording updated |
| 5 | Raise the legacy-to-heartbeat question with SwapCell | Flag | Cross-repo action (below) |

Files changed: `cad/src/model.py` (rail parameters), STEP and STL re-exported; `cad/src/sheets.py` and SGN-DWG-001 at **Rev P2** (rails and mass notes); `cad/src/concept_media.py` (key figures) and all media regenerated and checked by eye; `docs/04-calcs/sizing.py` (rail section from the model, R12 on the reference build), `results.csv` and SGN-CAL-001 v0.2; `bom/bom.csv` item 1 and `bom/bom-notes.md`; SGN-PRB-001, SGN-PRC-001 and SGN-REQ-001 at v0.5; SGN-DDR-001 v0.2 (item 15 decided); `project.yaml` (DDR-002 in `trl_evidence`); `README.md` (numbers, key components, and new sections Concept rationale, Burning platform, Where it could be used, What sparked the idea); all PDFs re-rendered and every generated file re-rendered with the designmolecule.com footer.

### Requirement status (SGN-CAL-001 v0.2)

- **Not met:** none.
- **At risk:** R1 (1.00 m belt fits a 1.75 m rider only up to 5 km/h; kept until co-design), R6 (235 W for 8 % at 8 km/h, 6 % margin), R10 (37.9 kg with pack, 2.1 kg margin).
- **Not verifiable at TRL 3:** R9 (guard gaps to ISO 13857), R13 (latch class V1 retention).
- **Met on paper:** R2, R3, R4, R5 (45 km), R7, R8, R11, R12 ($546 reference build).

### Still Proposed, awaiting Amish (no recommendation)

- First user group (non-cycling adults, older adults or commuters).
- First target country for the legal category.

### Cross-repo actions

- **SwapCell:** v0.3 does not say whether a pack in legacy discharge moves to mode 2 when a heartbeat arrives; StepGen's logic board, powered from the pack after a key-on wake, needs that. Not edited from this repo.

### Safety

Unchanged from the TRL 3 session, except that the deck-rail weld fatigue concern is closed on paper (still needs a test). R12 now depends on salvaged treadmill and bike parts, whose condition must be checked before use. The key switch cuts the pack without warn-then-derate and is for use at a standstill only.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No test article, test plan, build log, PCB or firmware was created.

## Session 2026-09-25: TRL 3

TRL 3 (analytical proof of concept on paper) is reached and is the hard stop. TRL 4 is on hold by Amish's instruction ("Make sure we don't proceed to TRL 4 on any of them"). The design meets its range, speed, braking, step-off, power and SwapCell interface requirements on paper, but **R12 (cost) is not met** at $713 against the new $650 budget, and R1, R6 and R10 are at risk.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (SGN-DDR-001 v0.1): Amish's 2026-09-25 decisions on every TRL 2 review item that had a recommendation, the cross-cutting approvals (SwapCell interface v0.3, shared-pack pricing, co-design partners later), the area move, and the items that stay open.
- `docs/04-calcs/01-sizing.md` (SGN-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: geometry, mass and centre of mass, road load, energy and range, hill and acceleration, belt drag and belt length, control timing, braking and belt slip, cornering, deck-rail and steering-column strength, SwapCell v0.3 wake and latch class V1, and cost. The script reads the model parameters, the BOM and the budget, and prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model (all key dimensions in `PARAMS`, derived geometry in `geometry()`), exporting `cad/step/stepgen-assembly.step`, `stepgen-frame.step`, `stepgen-deck.step`, `stepgen-receiver.step` and matching STL files in `cad/stl/`. Changes from the TRL 2 massing model: 30 mm fork offset (trail 58 mm instead of about 90 mm), head tube moved back 30 mm so the length stays 2.35 m, 38 mm steering column, class V1 receiver cradle with an over-centre lever, stowed kickstand.
- `cad/src/sheets.py` and `cad/drawings/SGN-DWG-001` (SVG, PDF, PNG): general arrangement at Rev P1, third-angle views at 1:20, isometric view and a key-dimension and interface box, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". SGN-DWG-001 was free; the concept sheet is SGN-DWG-010.
- `cad/src/concept_media.py`: now imports its geometry from `model.py`. All media regenerated and checked by eye: hero, blueprint SGN-DWG-010, cutaway, exploded view (callouts 1 to 15), flow (estimates marked, numbers from SGN-CAL-001), `model.glb` and `viewer.html`. Temporary `media/_views*` folders deleted.
- `bom/bom.csv` and `bom/bom-notes.md`: all 16 lines priced with a supplier or supplier type; pack at $0.00, priced once in SwapCell.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md`: decisions recorded, SwapCell interface v0.3, numbers corrected to SGN-CAL-001, new R13 (pack retention to latch class V1), R12 at $650, a status column in the requirements, safety notes added to the problem statement and requirements. **Version note:** these three documents were already at 0.3 from the earlier 2026-09-25 concept change, so they are now at **0.4** (the brief asked for 0.3, which would not be a new version).
- `project.yaml`: `trl: 3`, `trl_target: 3`, `trl_evidence` lists the documents, CAL-001, model, STEP files, drawing and BOM; `area: Mobility and Logistics`; `budget_usd: 650`; the `cleantech` tag removed. Pitch and problem unchanged (no rewording was recommended).
- `README.md`: TRL 3 badge, area, budget, TRL 3 numbers and links to the drawing and sizing note.
- `docs/pdf/`: PDFs of every controlled document at its current version.

### Requirements (SGN-CAL-001, Table 5)

| ID | Status | Value |
| --- | --- | --- |
| R12 cost | **Not met** | $713 excluding the pack against $650; about $538 on a salvage route |
| R1 walking on the belt | At risk | 1.00 m usable, 22 to 30 N push; fits a 1.75 m rider only up to 5 km/h |
| R6 hill | At risk | 233 W for 8 % at 8 km/h, 7 % margin to 250 W |
| R10 size and mass | At risk | 2.35 m, 0.61 m met; 36.8 kg with pack leaves 3.2 kg |
| R9 guards | Not verifiable at TRL 3 | Guards modelled; ISO 13857 gaps need hardware |
| R13 pack retention (class V1) | Not verifiable at TRL 3 | 330 N preload, lever ratio 6.6, bolt factor 22 at 25 g |
| R2 motor only while walking | Met (on paper) | 261 ms belt stop to motor off; 30 ms from brakes or lanyard |
| R3 speed and acceleration | Met (on paper) | 25 km/h cut, 15 km/h mode, 32 N m torque limit for 1.0 m/s² |
| R4 motor class | Met (on paper) | 250 W rated |
| R5 range | Met | 45 km at 20 km/h on the flat (9.1 Wh/km); about 32 km in real use |
| R7 braking | Met (on paper) | 8.0 m from 25 km/h; 9.6 m on the rear brake alone |
| R8 step-off | Met | Belt top 240 mm |
| R11 SwapCell v0.3 | Met (on paper) | 10 kΩ coded INTERLOCK (0.30 V), heartbeat mode 2, 8.5 A maximum |

Other results without a requirement: deck-rail weld fatigue is **at risk** (37.6 MPa walking stress range against a 38.8 MPa limit); the 38 x 2 mm steering column has a factor of 2.0; lean clearance is 30°; belt tension of 500 N per run keeps the belt from slipping under 240 N of braking push.

### Decisions recorded (SGN-DDR-001)

Decided by Amish, 2026-09-25, go with recommendation: two-wheel long-wheelbase form factor (three-wheel open until co-design); 20 in wheels; 250 W rear geared hub, 25 km/h cut, 15 km/h beginner mode; 30 km at 20 km/h range target; no roller generator in the first concept; area Mobility and Logistics; budget $650, pack excluded; confirm the legal category in a first target country before any road use; a decision record. Cross-cutting: SwapCell interface v0.3 (StepGen uses items W and V, not C); shared packs priced once; co-design partners picked per area later.

### Proposed, awaiting Amish

*Update 2026-09-25: items 3 to 7 are now "Decided by Amish, 2026-09-25: go with recommendation" (SGN-DDR-002); items 1 and 2 stay Proposed, awaiting Amish.*

1. **First user group.** Non-cycling adults, older adults or commuters. No recommendation. Still Proposed, awaiting Amish.
2. **First target country** for the legal category. No recommendation. Still Proposed, awaiting Amish.
3. **Cost overrun (R12).** Options: (a) keep $650 and make the salvage route (used walking-pad treadmill, donor 20 in bike; about $538) the reference build, with new parts as fallback; (b) raise `budget_usd` to about $720 for new parts; (c) cut scope (for example drop the display for a simple LED). Recommended: (a). `project.yaml` stays at $650. **Decided by Amish, 2026-09-25: go with recommendation.**
4. **Belt length (R1 against R10).** Options: (a) keep the 1.05 m roller pitch and 2.35 m length until co-design shows the riders' heights and pace; (b) lengthen to about 1.19 m, which fits a 1.90 m rider at 6 km/h but makes the vehicle about 2.49 m and needs R10 relaxed to 2.5 m; (c) cap belt speed in firmware for the short belt. Recommended: (a), revisit after co-design. **Decided by Amish, 2026-09-25: go with recommendation.**
5. **Deck rails.** Change from 50 x 25 x 2 mm to 60 x 30 x 2 mm to take the weld stress range from 37.6 to 25.5 MPa, for 1.08 kg (mass then about 37.9 kg with pack). Recommended. Not applied to the model, because it uses a third of the R10 mass margin. **Decided by Amish, 2026-09-25: go with recommendation;** now applied.
6. **Key switch in the INTERLOCK loop.** Options: (a) a key switch in series with the 10 kΩ coding resistor (off opens the loop and sleeps the pack; on wakes it; also a simple immobiliser); (b) a soft power button that sends a sleep request, with the pack's own wake button to start. Recommended: (a), used at a standstill only. **Decided by Amish, 2026-09-25: go with recommendation.**
7. **Flag to the SwapCell project (not a StepGen decision).** v0.3 does not say whether a pack in legacy discharge moves to mode 2 when a heartbeat arrives, which a host powered from the pack output needs after a key-on wake. **Decided by Amish, 2026-09-25: go with recommendation** (raise with SwapCell; cross-repo action).

### Safety concerns

- Falls on a moving belt, a rider stopping abruptly or leaving the deck at speed: free-running belt, 261 ms motor cut-off, 30 ms lanyard and brake cut, low open deck. Rider dynamics need a test.
- Braking with feet on a belt: the sprag and 500 N belt tension hold the belt; the rider must resist about 240 N at 3 m/s², and harder stops can pitch the rider over the bar.
- Pinch points at both belt nips, the rear tire behind the heel and the spokes: guards modelled, ISO 13857 gaps unverified (R9).
- Weld fatigue at the deck rails is at the limit (proposal 5).
- Pack retention: a pack leaving its cradle at speed is a 2.85 kg projectile with live contacts; class V1 is specified but unverified (R13).
- The key switch cuts the pack at once, without warn-then-derate; use only at a standstill.
- Lithium pack at up to 54.6 V: SwapCell BMS, coded interlock and derating apply; charge only in a dock; 20 A harness fuse. Helmet essential; the rider's head is about 2 m up.
- Legal category unresolved: no road use until it is confirmed in the target country.

### Other notes

- No TRL 4 material exists in the repo (`build-log/` holds only its README; `electronics/` and `firmware/` are empty). None was created.
- The TRL 2 note listed no unchecked citations, and no new citations were added, so no web check was needed.

### Recommended next step

TRL 4 is on hold by Amish's instruction, and this session stops at TRL 3. Next: Amish decides items 1 to 6 above, and the SwapCell project answers item 7. After that, paper work that stays within TRL 3: apply the chosen rail size and belt length to the model and recalculate, and a desk study of the legal category in the chosen country. Co-design sessions with users, once a partner is picked for the area, should come before any hardware.

For the record only, TRL 4 would need: a test article (at least a belt-deck rig and a class V1 receiver cradle), a lab test plan and report (SGN-TST) covering belt drag and walking feel, motor cut-off timing, braking with a standing rider, weld details and V1 vibration and shock, and dated build-log entries. None of this should start until Amish lifts the hold.

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

*Update 2026-09-25: items 1 to 8 were decided by Amish on 2026-09-25 (go with recommendation, SGN-DDR-001); item 9 (first user group) stays Proposed, awaiting Amish.*

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

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-02: approved follow-ups carried out

Amish approved all follow-up actions from the open-decision sign-off on 2026-10-02. No CAD model, calculation result, drawing or build plan picture changed.

### Approved follow-ups carried out

1. Decision 5, BOM: done. `bom/bom-notes.md` records that the rotor carriers on the rear and front hubs (lines 6 and 7) are confirmed against the hubs bought when the wheel build is specified. No quantity or price changed.
2. Decision 6, pictures: appearance model done. The "250 W 25 km/h" rating decal is removed from `cad/src/product_model.py`; render scenes exported to `/home/claude/renders/stepgen` for the views hero, exploded and detail (one .npz and .json each, plus `stepgen__jobs.json`). Not done here: the photoreal renders, `media/card.png` and `media/social-preview.png` are made on Amish's Mac next.
3. Decision 3, calculations: not done, the RDW check has not happened (outreach by Amish). R3 and R4 stay as they are until it sets a lower speed cap or requires type approval.

### Results

- Requirement status changes: none.
- Value-engineering target: USD 650. Estimated cost of the constructable design: USD 610 on the reference build (USD 40 under the target). `budget_usd` is unchanged. Mass is unchanged.

### Documents changed

No controlled document changed, so no version was bumped. Files changed: `cad/src/product_model.py`, `bom/bom-notes.md`.

### Cross-repo actions

None.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
