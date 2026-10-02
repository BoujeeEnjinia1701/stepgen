---
doc_id: SGN-REQ-001
title: StepGen requirements
project: StepGen
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Concept changed at Amish's direction from a stationary stepper generator to a walking-treadmill vehicle
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record Amish's decisions (SGN-DDR-001); R11 to SwapCell interface v0.3; new R13 (latch class V1); R12 budget $650; status of every requirement from SGN-CAL-001
- version: "0.5"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from SGN-CAL-001 v0.3 for the constructable design (SGN-DDR-003); R12 reported against the value-engineering target
---

# StepGen requirements

These are the requirements for the walking-treadmill vehicle at TRL 3. Amish decided the targets for form factor, wheels, speed class, range and budget on 2026-09-25 (SGN-DDR-001), and accepted the TRL 3 recommendations on cost route, belt length, deck rails and key switch the same day (SGN-DDR-002); the rest remain engineering targets to be revised after co-design with users. Every requirement has been checked by calculation in SGN-CAL-001, and Table 1 gives its status. The stepper generator requirements of version 0.2 are withdrawn with that concept.

*Table 1. Requirements and status (SGN-CAL-001).*

| ID | Requirement | Target | Verification | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Natural walking on the belt | Usable belt length 1.0 m or more between roller tangents and belt width 0.36 m or more; horizontal force to walk the belt 30 N or less at 5 km/h for an 80 kg rider | Deck geometry in the model; belt drag calculation | At risk: 1.00 m and 22 to 30 N meet the target, but 1.00 m fits a 1.75 m rider only up to 5 km/h; belt kept until co-design (SGN-DDR-002) |
| R2 | Motor runs only while the rider walks | Assist starts only when belt speed stays above 1.5 km/h for 0.5 s; assist power rises with belt speed; motor off within 0.5 s of the belt stopping, either brake lever being pulled or the lanyard coming out | Control logic review; timing budget | Met on paper: 261 ms from belt stop, about 30 ms from a brake lever or the lanyard |
| R3 | Speed limit | Assist cut off at 25 km/h or less, set in firmware; a beginner mode capped at 15 km/h; acceleration limited to 1.0 m/s² or less (decided by Amish, 2026-09-25) | Controller configuration; dynamics calculation | Met on paper: 32 N m torque limit |
| R4 | Motor power in the pedelec class | Rated continuous motor power 250 W or less (decided by Amish, 2026-09-25) | Motor datasheet | Met on paper |
| R5 | Range on one shared pack | 30 km or more at a steady 20 km/h on flat pavement with an 80 kg rider, using the usable energy of one SwapCell pack (decided by Amish, 2026-09-25) | Road-load and energy calculation | Met: 45 km |
| R6 | Hill capability | Climb an 8 % grade at 8 km/h or more with an 80 kg rider, within the motor's rating | Road-load calculation | At risk: 235 W against 250 W |
| R7 | Braking | Two independent hand brakes; stop from 25 km/h within 10 m of brake application on dry pavement, at a deceleration a standing rider can hold (about 3 m/s²); the belt cannot run forward under the rider's feet when braking | Brake calculation; clutch specification | Met on paper: 8.0 m; 9.6 m on the rear brake alone |
| R8 | Rider can step off and put a foot down | Belt top 250 mm or less above the ground; open sides with no rail higher than the deck along the belt | Massing model | Met: 240 mm |
| R9 | Guard pinch and entanglement points | Belt in-running nips at both rollers, wheel spokes and the rear tire all covered or out of reach of feet, toes and fingers; heel guard between the belt's rear end and the rear tire | Design review against ISO 13857 reach distances | Not verifiable at TRL 3 |
| R10 | Size and mass | Length 2.4 m or less, width 0.65 m or less at the handlebar, mass 40 kg or less with the pack | Model; mass estimate | At risk: 2.38 m (with the fender) and 0.58 m met; 37.9 kg leaves 2.1 kg |
| R11 | Shared SwapCell pack | Uses the SwapCell interface v0.3 unchanged: 10 kΩ coding resistor in the INTERLOCK loop (wake, item W), CAN host heartbeat as a vehicle requesting discharge, receiver cradle to the v0.3 envelope; continuous current 15 A or less; every circuit below 60 V DC | Interface review with the SwapCell project | Met on paper: 8.5 A maximum |
| R12 | Low cost and buildable | Parts cost $650 or less excluding the SwapCell pack on the reference build, which uses a salvaged walking-pad treadmill (items 2 and 3) and a donor 20 in bike (items 7 and 9); new parts are the fallback and are reported but not held to this figure (decided by Amish, 2026-09-25, SGN-DDR-001 and SGN-DDR-002; the pack is priced once in the SwapCell BOM); built with hand tools, a drill press and basic welding | Priced BOM | Under the value-engineering target on paper: USD 610, USD 40 under (all new USD 750, USD 100 over) |
| R13 | Pack retention in the vehicle | Receiver cradle meets SwapCell latch class V1 (interface v0.3 item V): no latch release and no power-contact break of 1 ms or longer under 8 g sine and 25 g shocks; pack latch proof 1.72 kN; receiver preload 330 N or more through an over-centre lever with a detent | Paper sizing now; test at TRL 4 (on hold) | Not verifiable at TRL 3 |

> **Safety:** R2, R3, R7, R8, R9 and R13 are safety requirements for a person standing on a moving belt on a vehicle with a 468 Wh lithium-ion pack. Meeting them on paper does not make the vehicle safe to build or ride; they need test evidence at TRL 4, which is on hold.

## Assumptions

- Rider 80 kg and 1.75 m; vehicle 35.1 kg without the pack; SwapCell pack 2.85 kg; total 117.9 kg.
- Rolling resistance coefficient 0.010 for 20 x 1.75 in tires on pavement; standing rider drag area CdA about 0.70 m²; air density 1.2 kg/m³.
- Motor and gearbox efficiency 80 %, controller efficiency 95 %, 3 W of auxiliary load.
- Usable pack energy 411 Wh: the SwapCell sizing note gives 457 Wh at the terminals per full cycle, and a 10 % reserve is kept.
- Walking speed on the belt 4 to 6 km/h; belt rolling-bed coefficient about 0.02.
- The full list is in SGN-CAL-001, Table 1.

## Requirements not met or at risk

- **R1 is at risk.** The 1.0 m target is met exactly, but a 1.75 m rider at 6 km/h, or a 1.90 m rider at 5 km/h, needs more belt. A longer belt breaks the 2.4 m length of R10. Decided by Amish, 2026-09-25 (SGN-DDR-002): keep the 1.05 m roller pitch and revisit after co-design.
- **R6 is at risk.** The 8 % climb needs 235 W at the wheel, a 6 % margin to the 250 W rating.
- **R10 is at risk on mass.** 37.9 kg with the pack leaves 2.1 kg, less than a 10 % growth allowance. The 60 x 30 x 2 mm deck rails (SGN-DDR-002) added 1.08 kg to close the weld fatigue concern.
- **R12 depends on salvage.** `budget_usd` is a hypothetical value-engineering target, not a limit (Amish, 2026-10-01). Value-engineering target: USD 650. Estimated cost of the constructable design: USD 610 on the salvage reference build (USD 40 under the target); the USD 40 and USD 50 salvage prices are estimates, and an all-new build (USD 750) would be USD 100 over the target.
- **R9 and R13** can only be verified on hardware, which is TRL 4 work and on hold by Amish's instruction.
- **Legal classification is unresolved.** R3 and R4 follow EU pedelec limits, but a vehicle without pedals may not qualify as a pedelec in the EU or as an e-bike in the US (see SGN-PRB-001). Amish decided on 2026-09-25 that the category is confirmed in a first target country before any road use; the country is still open.
