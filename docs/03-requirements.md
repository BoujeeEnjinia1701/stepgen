---
doc_id: SGN-REQ-001
title: StepGen requirements
project: StepGen
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
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
---

# StepGen requirements

These are first-pass requirements for the walking-treadmill vehicle. Every target is a proposal for review, will be checked by calculation at TRL 3 and will be revised after co-design with users. The stepper generator requirements of version 0.2 are withdrawn with that concept.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Natural walking on the belt | Usable belt length 1.0 m or more between roller tangents and belt width 0.36 m or more; horizontal force to walk the belt 30 N or less at 5 km/h for an 80 kg rider | Deck geometry in the model; belt drag calculation |
| R2 | Motor runs only while the rider walks | Assist starts only when belt speed stays above 1.5 km/h for 0.5 s; assist power rises with belt speed; motor off within 0.5 s of the belt stopping, either brake lever being pulled or the lanyard coming out | Control logic review; timing budget |
| R3 | Speed limit | Assist cut off at 25 km/h or less, set in firmware; a beginner mode capped at 15 km/h; acceleration limited to 1.0 m/s² or less | Controller configuration; dynamics calculation |
| R4 | Motor power in the pedelec class | Rated continuous motor power 250 W or less | Motor datasheet |
| R5 | Range on one shared pack | 30 km or more at a steady 20 km/h on flat pavement with an 80 kg rider, using the usable energy of one SwapCell pack | Road-load and energy calculation |
| R6 | Hill capability | Climb an 8 % grade at 8 km/h or more with an 80 kg rider, within the motor's rating | Road-load calculation |
| R7 | Braking | Two independent hand brakes; stop from 25 km/h within 10 m of brake application on dry pavement, at a deceleration a standing rider can hold (about 3 m/s²); the belt cannot run forward under the rider's feet when braking | Brake calculation; clutch specification |
| R8 | Rider can step off and put a foot down | Belt top 250 mm or less above the ground; open sides with no rail higher than the deck along the belt | Massing model |
| R9 | Guard pinch and entanglement points | Belt in-running nips at both rollers, wheel spokes and the rear tire all covered or out of reach of feet, toes and fingers; heel guard between the belt's rear end and the rear tire | Design review against ISO 13857 reach distances |
| R10 | Size and mass | Length 2.4 m or less, width 0.65 m or less at the handlebar, mass 40 kg or less with the pack | Massing model; mass estimate |
| R11 | Shared SwapCell pack | Uses the SwapCell interface v0.2 unchanged: host heartbeat, interlock, receiver cradle; continuous current 15 A or less; every circuit below 60 V DC | Interface review with the SwapCell project |
| R12 | Low cost and buildable | Parts cost $400 or less excluding the SwapCell pack; built with hand tools, a drill press and basic welding; bicycle and treadmill parts where possible | Priced BOM |

## Assumptions

- Rider 80 kg; vehicle about 35 kg without the pack; SwapCell pack about 2.8 kg; total about 118 kg.
- Rolling resistance coefficient 0.010 for 20 x 1.75 in tires on pavement; standing rider drag area CdA about 0.70 m²; air density 1.2 kg/m³.
- Motor and gearbox efficiency 80 %, controller efficiency 95 % (geared hub motor at part load).
- Usable pack energy about 410 Wh: the SwapCell precis gives about 454 Wh at the terminals per full cycle, and a 10 % reserve is kept.
- Walking speed on the belt 4 to 6 km/h; belt rolling-bed friction coefficient about 0.02.

## Requirements not met or at risk

- **R12 is not met.** Parts are estimated at about $630 excluding the SwapCell pack, about $230 over the $400 budget. A budget change is proposed, awaiting Amish (see SGN-PRC-001 and the review note).
- **R6 is met with a thin margin.** An 8 % climb at 8 km/h needs about 236 W at the wheel, close to the 250 W rating.
- **R10 is met with a thin margin on length** (about 2.35 m against 2.4 m).
- **Legal classification is unresolved.** R3 and R4 follow EU pedelec limits, but a vehicle without pedals may not qualify as a pedelec in the EU or as an e-bike in the US (see SGN-PRB-001).
- **R11** depends on SwapCell interface choices that are still open, including the connector family and the vibration rating of the latch.
