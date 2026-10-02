---
doc_id: SGN-DEC-001
title: StepGen design decisions register
project: StepGen
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened; open decisions gathered from the review note, the decision records and the build plan work
---

# StepGen design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Design for construction changes P1 to P17 | Accept as made; or ask for any change to be reworked | Accept: none changes what the vehicle does, its pitch or its safety case, and all 72 model checks pass | The whole build plan | SGN-DDR-003 |
| 2 | First user group | Non-cycling adults, older adults or commuters | None yet | Bar height, belt length and beginner mode settings after co-design | SGN-DDR-001 item 13, SGN-DDR-002 item 6 |
| 3 | First target country for the legal category | Any country with a co-design partner | None yet | Road use only; not part of the TRL 3 build | SGN-DDR-001 items 8 and 14, SGN-DDR-002 item 7 |
| 4 | Rider pose in the photoreal renders | Accept the shorter stride used; or another pose | Accept for renders; check the stride on a 1.0 m belt in co-design | Renders only | `docs/REVIEW.md`, 2026-09-26, item 1 |
| 5 | Wheel detail in the appearance model | Accept 28 laced spokes and rotor carriers as appearance only | Accept; the rotor positions now follow SGN-DDR-003 | Renders only | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 6 | Branding and markings on renders | Accept the wordmark, rating decal and accent colours; or give a scheme | Accept, or give a preferred scheme | Renders only | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 7 | Three-wheel version | Keep two wheels; build a three-wheel version for riders who cannot balance | Keep open until co-design shows whether non-cyclists can balance | Not in this build | SGN-DDR-001 item 1 |

The SwapCell question of how a pack in legacy discharge moves to discharge mode when a heartbeat arrives (SGN-DDR-002 item 5) is a cross-repo action for the SwapCell project, not a StepGen decision. The display tilt (`docs/REVIEW.md`, 2026-09-26, item 2) is resolved in the model by SGN-DDR-003 P15.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The fork: 1 1/8 in threadless rigid steel, 26 in size (axle to crown about 410 mm), 30 mm offset, post-mount disc tabs, steerer 220 mm or longer. If only 38 to 45 mm offsets are found, trail falls from 58 mm to about 42 to 49 mm | Sets trail and steering feel; a 20 in fork is too short for the head tube | SGN-DDR-003 P4 |
| 2 | The head tube is machined for a ZS44 headset and the headset's crown race fits the fork | The headset must fit both | SGN-DDR-003 P4 |
| 3 | The walking-pad treadmill: belt 400 mm or wider, end rollers about 50 mm and 420 mm long, bearings 6203 size on fixed axles that can be drilled and tapped | The one-way bearing (CSK17) and the axle fixings assume these | SGN-DDR-003 P8 |
| 4 | The idler rollers' spring axles: 8 mm round or hex | Sets the carrier bar hole size | SGN-DDR-003 P10 |
| 5 | The hub motor: 135 mm axle width, axle flats that take the torque arms, 6-bolt rotor mount | Sets the dropout spacing and the rear brake | SGN-DDR-003 P2, P3 |
| 6 | The controller fits a 150 x 70 x 40 mm space and has a brake-cut input that both levers and the lanyard can open | Sets the controller plate and the cut-off wiring | SGN-DDR-003 P14 |
| 7 | The SwapCell pack's guide faces and handle end match the cradle (interface v0.3 envelope) | Sets the cradle's inside width and the lever pad | SGN-DDR-003 P13 |
| 8 | The second-hand prices: about USD 40 for a walking-pad treadmill and USD 50 for a donor 20 in bike | The reference build cost depends on them | SGN-DDR-002 item 1 |

## Value engineering

Value-engineering target: USD 650 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 610 on the salvage reference build, pack excluded (USD 40 under the target); USD 750 with all new parts (USD 100 over the target). Main cost drivers and savings worth trying:

- The largest lines are the rear wheel with its hub motor (USD 110), the belt and end rollers (USD 97 new, from about USD 40 salvaged with the idlers), the main frame (USD 92, of which USD 25 is the machined head tube), the front wheel, fork and headset (USD 70), and the receiver cradle (USD 55, of which USD 30 is the receptacle).
- Making the design constructable raised the reference build from USD 546 to USD 610: about USD 40 because the donor bike's fork is too short for the head tube, and the rest for the nose beam, head tube, carrier bars, guards, fender, rivet nuts and fixings.
- Savings worth trying: a donor bike with a 26 in fork as well as a 20 in front wheel would save the USD 40 fork; a donor walking pad whose rollers already take a one-way bearing saves the bearing; buying the receptacle with the SwapCell project's batch may halve its price.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-24 | StepGen becomes a walking-treadmill vehicle; the stationary stepper generator is dropped | Amish: "as the person walks his scooter / bike moves forward but hes upright walking instead of pedalling" | SGN-PRB-001, SGN-PRC-001 |
| 2026-09-25 | TRL 2 review items: two-wheel long-wheelbase form, 20 in wheels, 250 W rear hub with a 25 km/h cut and 15 km/h beginner mode, 30 km range target, no roller generator, Mobility and Logistics area, USD 650 budget (pack excluded), legal route, SwapCell interface v0.3, shared-pack pricing, co-design partners later | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | SGN-DDR-001 |
| 2026-09-25 | Salvage route as the reference build within USD 650; belt kept at 1.05 m until co-design; 60 x 30 x 2 mm deck rails; key switch in the INTERLOCK loop; raise the legacy-to-heartbeat question with SwapCell | Amish: "i accept all your recommendations, go with them across all repos." | SGN-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep outstanding decisions out of the build plan, in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SGN-DDR-003 (draft, open item 1) |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | This register, Value engineering |
