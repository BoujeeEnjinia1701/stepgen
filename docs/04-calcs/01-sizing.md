---
doc_id: SGN-CAL-001
title: StepGen sizing calculations
project: StepGen
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (geometry, mass, road load and range, hill and acceleration, belt, control timing, braking and structure, SwapCell interface v0.3, cost)
---

# StepGen sizing calculations

On paper the walking-treadmill vehicle meets its range, speed, braking, step-off, power and SwapCell interface requirements, but **R12 (cost) is not met**: the priced BOM is about $713 against the new $650 budget. Three requirements are **at risk**: R1 (a 1.00 m belt fits a 1.75 m rider only up to 5 km/h), R6 (the 8 % hill needs 233 W, a 7 % margin to the 250 W rating) and R10 (36.8 kg with the pack, a 3.2 kg margin that is smaller than a 10 % mass-growth allowance). Guarding (R9) and pack retention to SwapCell latch class V1 (R13) cannot be verified until hardware exists, which is TRL 4 work and on hold by Amish's instruction.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script takes its geometry from `cad/src/model.py`, its prices from `bom/bom.csv` and its budget from `project.yaml`, so the note, the model and the BOM share one source. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Design rider | 80 kg, 1.75 m, centre of mass 0.56 of height above the belt | Typical adult |
| Heaviest rider (structure) | 120 kg | Upper design mass |
| SwapCell pack | 2.85 kg; 457 Wh at the terminals per full cycle; 10 % reserve kept | SWC-CAL-001 (interface v0.3) |
| Rolling resistance | Crr 0.010 | 20 x 1.75 in tires on pavement |
| Air drag | CdA 0.70 m², air density 1.2 kg/m³ | Standing rider, larger than a seated upright cyclist |
| Drivetrain | Motor and gear 80 %, controller 95 % | Geared hub at part load |
| Auxiliary load | 3 W | Logic board, display, controller standby |
| Pack voltage | 46.8 V nominal, 39.0 V minimum | SwapCell 13S |
| Real-use energy factor | x 1.4 | Stops, hills, wind; indicative only |
| Belt over the roller bed | Rolling coefficient 0.02 on the rider's weight | Belt indentation over 30 mm rollers |
| Belt bending and bearings | 5 N bending at two end rollers; bearing friction coefficient 0.0015 | Estimates |
| Belt tension | 500 N per run (tensioner setting) | Chosen in section 7 |
| Step and foot length | Step 0.40 x height at 5 km/h and 0.45 x height at 6 km/h; foot 0.15 x height | Typical adult gait; to be checked in co-design |
| Tire to road friction | 0.7 | Dry pavement |
| Steel | S235 class, yield 235 MPa, E 200 GPa; welded detail FAT 71 with partial factor 1.35 | Eurocode 3 style check |
| Walking load | 1.2 x body weight per step; 1.9 steps/s, 1 h a day for 5 years | Estimate |
| Class V1 environment | 8 g sine, 25 g shock, 3.5 kg design pack | SwapCell interface v0.3 item V |

## 2. Geometry and mass

The model gives a vehicle 2349 mm long, 612 mm wide at the grips, with a 1855 mm wheelbase. The belt runs on end rollers 1050 mm apart, leaving 1000 mm of usable length, 400 mm wide, with its top 240 mm above the ground. Ground clearance under the cross members is 148 mm. The bar is 1230 mm above the ground (990 mm above the belt). A 70° head angle with a 30 mm fork offset gives 58.0 mm of trail and 18.6 mm of wheel flop, in the range of ordinary bicycles. The TRL 2 model had no fork offset, which gave about 90 mm of trail.

*Table 2. Mass estimate.*

| Item | Mass (kg) | Basis |
| --- | --- | --- |
| 1 Main frame | 11.4 | Deck rails 5.13, cross members 2.04, rear stays 1.29, nose 0.83, down tube 0.98, head tube 0.46, plates 0.70 |
| 2 Belt and end rollers | 3.8 | Belt 1.3, two rollers 2.2, tensioner 0.3 |
| 3 Roller bed | 3.0 | 14 rollers at 0.15 kg, carriers 0.9 |
| 4 Clutch and drag | 0.4 | Estimate |
| 5 Belt speed sensor | 0.05 | Estimate |
| 6 Rear wheel with hub motor | 4.3 | Motor 2.5, rim, spokes, tire and tube 1.6, rotor 0.2 |
| 7 Front wheel, fork, headset | 3.0 | Wheel 1.6, fork 1.1, headset 0.3 |
| 8 Steering column, bar, grips | 1.7 | 38 x 2 mm column, stem, bar, grips |
| 9 Brakes | 1.1 | Two calipers, rotors, levers, cables |
| 10 Receiver cradle, class V1 | 1.0 | 3 mm steel cradle, lever, receptacle |
| 12 Controller and logic board | 0.6 | Estimate |
| 13 Display, selector, lanyard, key | 0.3 | Estimate |
| 14 Guards | 2.0 | About 0.63 m² of 1 mm aluminium plus brackets |
| 15 Harness | 0.4 | Estimate |
| 16 Hardware and kickstand | 0.9 | Kickstand 0.4, fasteners 0.5 |
| **Vehicle without pack** | **34.0** | |
| SwapCell pack | 2.85 | SWC-CAL-001 |
| **Vehicle with pack** | **36.8** | R10 limit 40 kg |

The margin to 40 kg is 3.2 kg, or 9 % of the vehicle mass; a 10 % growth allowance would take the vehicle to 40.2 kg, so R10 is **at risk** on mass. With an 80 kg rider the total is 116.8 kg. The vehicle's centre of mass is 913 mm ahead of the rear axle and 326 mm up; the rider's is at 950 mm and 1220 mm; together 938 mm and 938 mm, with 49 % of the static load on the rear wheel.

## 3. Road load, energy and range

Wheel power is rolling plus air drag, P = (Crr m g + ½ ρ CdA v²) v. Pack power is wheel power over 0.76 plus 3 W. Usable energy is 411 Wh.

*Table 3. Steady speed on the flat, 116.8 kg.*

| Speed | Rolling | Air | Wheel | Pack | Current at 46.8 V (39.0 V) | Energy | Range, flat | Real use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15 km/h | 48 W | 30 W | 78 W | 106 W | 2.3 A (2.7 A) | 7.1 Wh/km | 58 km | about 42 km |
| 20 km/h | 64 W | 72 W | 136 W | 182 W | 3.9 A (4.7 A) | 9.1 Wh/km | 45 km | about 32 km |
| 25 km/h | 80 W | 141 W | 220 W | 293 W | 6.3 A (7.5 A) | 11.7 Wh/km | 35 km | about 25 km |

At 20 km/h the controller loses about 9 W and the motor and gear about 34 W. Road load equals the 250 W rating at 26.4 km/h, so the 25 km/h assist cut-off, not the motor, sets top speed. At the 250 W wheel cap the pack supplies 332 W: 7.1 A at 46.8 V, 8.5 A at 39.0 V, well inside the 15 A controller limit. **R5 is met**: 45 km against 30 km at 20 km/h.

## 4. Hill, acceleration and motor

An 8 % grade at 8 km/h needs 105 N at the wheel, which is 233 W (a 7 % margin to 250 W), 25.9 N m at the hub and 6.6 A from the pack. At 250 W the vehicle climbs a 5 % grade at 12.2 km/h, 8 % at 8.6 km/h and 10 % at 7.1 km/h. R6 is met, but the margin is thin, so it is marked **at risk**.

The wheel turns at 268 rpm at 25 km/h and 86 rpm at 8 km/h, so the hub motor must be wound for a 20 in wheel: about 400 rpm no-load at 48 V, which leaves about 325 rpm at 39 V. To hold acceleration from rest to 1.0 m/s² (R3), the firmware limits drive force to 128 N, a hub torque of 31.7 N m. With the 250 W cap the vehicle reaches 20 km/h in about 12 s and 25 km/h in about 26 s; the available acceleration falls from 1.00 m/s² at 5 km/h to 0.64 at 10 km/h, 0.18 at 20 km/h and 0.04 at 25 km/h. The vehicle cannot surge away from a walking rider.

## 5. Belt drag, walking power and belt length

The push needed to walk the belt at 5 km/h is 15.7 N for the roller bed, 5.0 N for belt bending and 1.0 N for the end roller bearings, plus 0 to 8 N from the drag setting: **21.7 to 29.7 N**, inside the 30 N of R1 even at full drag. Walking puts 30 to 41 W into the belt at 5 km/h, and 24 to 49 W over 4 to 6 km/h, all of it dissipated as drag. A slider deck with a friction coefficient of 0.1 to 0.2 would need 78 to 157 N, which confirms the roller bed.

The belt length is the weak point of R1. With the step and foot assumptions of Table 1:

*Table 4. Belt length needed (step plus foot) against 1.00 m usable.*

| Rider | 5 km/h | 6 km/h |
| --- | --- | --- |
| 1.60 m | 0.88 m, fits | 0.96 m, fits |
| 1.75 m | 0.96 m, fits | 1.05 m, does not fit |
| 1.90 m | 1.04 m, does not fit | 1.14 m, does not fit |

R1's target of 1.0 m is met exactly, but the target itself is short for tall riders or brisk walking, so R1 is **at risk**. A 1.90 m rider at 6 km/h needs a roller pitch of about 1190 mm, which would make the vehicle about 2.49 m long and break R10 (2.4 m). This trade is proposed, awaiting Amish (review note).

For comparison, if 40 W of walking drove the wheel with no loss at all, the vehicle would reach only 9.9 km/h on the flat, and a 3 % grade at 5 km/h needs 65 W. This is why the motor does the work. The optional roller generator (not fitted, SGN-DDR-001 item 5) would return 5 to 10 W, a charge of 0.11 to 0.21 A in SwapCell mode 4, and about 6 % more range at 20 km/h.

## 6. Control timing (R2)

The 8-magnet ring on the 50 mm front roller gives a pulse every 19.6 mm of belt, or every 47 ms at the 1.5 km/h start threshold, so the 0.5 s start window sees 11 pulses. When the belt stops, the logic board declares a stop after three missed periods (141 ms), then adds 10 ms of logic, a 100 ms controller ramp-down and 10 ms of current decay: **261 ms from belt stop to motor off**, inside the 500 ms target. The brake-lever switches and the lanyard switch are wired to the controller's brake-cut input, so they act in about 30 ms. At 25 km/h the vehicle coasts 1.8 m in 261 ms. R2 is **met on paper**; the logic exists only as a labeled sketch.

## 7. Braking, stability and structure

At 3 m/s² the vehicle stops from 25 km/h in 8.0 m after the brakes act (R7, 10 m). With the combined centre of mass at 938 mm and 938 mm, the rear brake alone can give 2.51 m/s² (9.6 m) and the front alone 5.38 m/s² (4.5 m), so either brake alone still stops within 10 m. The vehicle would pitch over only at 9.6 m/s² if the rider were fixed to the deck; the practical limit is the rider, who must resist 240 N at 3 m/s².

The anti-reverse sprag holds the rear roller, so the rider can brace on the belt. With 180° of wrap and a friction coefficient of 0.3 the capstan ratio is 2.57, so the belt needs 273 N of tension per run not to slip under 240 N; the tensioner is set to 500 N. The sprag sees only 6.0 N m.

The lowest outboard part when leaning is the clutch housing, which gives 30.3° of lean clearance: a minimum turn radius of 3.0 m at 15 km/h and 8.4 m at 25 km/h.

The deck rails (50 x 25 x 2 mm RHS on edge, I = 90,079 mm⁴, Z = 3603 mm³) carry a 120 kg rider at 2.5 g at mid span at 117 MPa, a factor of 2.0 on yield, with 2.6 mm of deflection. Fatigue is tighter: each step gives a 37.6 MPa stress range, about 12.5 million times in five years of daily use, against 38.8 MPa for a FAT 71 weld with a partial factor of 1.35. The weld details are therefore **at risk**. Rails of 60 x 30 x 2 mm cut the range to 25.5 MPa for 1.08 kg more (proposed, awaiting Amish, because it eats into the R10 mass margin). There is no numbered requirement for structure; this is reported for the review.

The steering column must carry the rider's push at the bar, taken as 500 N at 449 mm above the head tube. A 32 x 2 mm column reaches 169 MPa (factor 1.4); the chosen **38 x 2 mm column** reaches 116 MPa (factor 2.0).

## 8. SwapCell interface v0.3

StepGen uses the interface unchanged (R11, R13).

- **Wake (item W).** The receiver fits a 10 kΩ ±1 % coding resistor between INTERLOCK and SGND. With the pack's 100 kΩ pull-up to 3.3 V the node sits at 0.297 to 0.303 V for 9.90 to 10.10 kΩ (plus 0.2 Ω of wiring and switch), inside the 0.24 to 0.37 V window, and the loop draws 30 µA. StepGen proposes a key switch in series with the resistor: key off opens the loop, the pack opens its output within 1 ms and sleeps after 60 s at 100 µA (about 0.72 % per month); key on pulls the node below 1.0 V and wakes the pack with no supply from the vehicle. The WAKE pin is not used.
- **Heartbeat.** The logic board is the SwapCell host: host type 0 (vehicle), requested mode 2 (discharge), host discharge limit 15.0 A. In use the pack supplies 3.9 A at a 20 km/h cruise and at most 8.5 A, inside the 15 A legacy limit, and the pack makes only about 8.0 W of heat at that maximum (110 mΩ), far from the 20 A case that puts SwapCell R3 at risk. Every circuit stays below 60 V DC.
- **Charge-discharge mode (item C).** Not used. The geared hub freewheels, so there is no regenerative braking, and the roller generator is not fitted.
- **Latch class V1 (item V).** For a 3.5 kg design pack, 8 g gives 275 N and 25 g gives 858 N. The pack latch proof is 1717 N (1.72 kN). The receiver must preload the pack against its end stop with 330 N or more, which an over-centre lever with a ratio of 6.6 gives at a 50 N hand force. The cradle's two M6 8.8 bolts see 21 MPa in shear at 25 g (a factor of 22 on 480 MPa), and the 44 x 2 mm down tube sees 19 MPa from the shock at a 60 mm standoff. Retention under vibration can only be shown by test, so R13 is **not verifiable at TRL 3**.
- **Flag to SwapCell.** The vehicle's logic board is powered from the pack output, so after a key-on wake the pack will enter legacy discharge (no heartbeat within 2 s) before the board can send one. The v0.3 behavior rules do not say whether a pack in legacy discharge moves to mode 2 when a heartbeat arrives. This is flagged to the SwapCell project, not changed here.

## 9. Cost

All 16 BOM lines are priced. The StepGen parts total, pack excluded, is **$713 against the $650 budget: over by $63 (10 %)**. R12 is **not met**. A salvage route (a used walking-pad treadmill for items 2 and 3 at about $40, and a donor 20 in bike for items 7 and 9 at about $50) would bring the total to about $538. Options are proposed, awaiting Amish, in the review note.

## 10. Results against requirements

*Table 5. Requirement status. "At risk" means met on paper with less than 10 % margin or resting on an unverified assumption.*

| ID | Value | Target | Status |
| --- | --- | --- | --- |
| R1 | Usable belt 1.00 m x 0.40 m; push 22 to 30 N at 5 km/h; 1.00 m fits a 1.75 m rider only up to 5 km/h | 1.0 m, 0.36 m, 30 N at 5 km/h | At risk |
| R2 | Belt stop to motor off 261 ms; brake and lanyard about 30 ms; start after 11 pulses in 0.5 s | Start after 0.5 s above 1.5 km/h; off within 0.5 s | Met (on paper) |
| R3 | Cut at 25 km/h, beginner 15 km/h; torque limit 32 N m gives 1.0 m/s² | 25 km/h, 15 km/h mode, 1.0 m/s² or less | Met (on paper) |
| R4 | 250 W rated motor specified; wheel power capped at 250 W | 250 W rated or less | Met (on paper) |
| R5 | 45 km at 20 km/h on the flat (9.1 Wh/km); about 32 km in real use | 30 km at 20 km/h | Met |
| R6 | 233 W at the wheel for 8 % at 8 km/h (7 % margin) | 8 % at 8 km/h within 250 W | At risk |
| R7 | 8.0 m at 3 m/s²; rear brake alone 9.6 m; belt held by the sprag with 500 N tension | Two brakes; 10 m from 25 km/h; belt cannot run forward | Met (on paper) |
| R8 | Belt top 240 mm; side boards 6 mm proud of the belt, no rails | 250 mm or less; open sides | Met |
| R9 | Guards modelled at both nips, the rear tire and belt ends; gaps not yet checked against ISO 13857 | Nips, spokes and rear tire guarded | Not verifiable at TRL 3 |
| R10 | 2.35 m long, 0.61 m wide, 36.8 kg with the pack (3.2 kg margin) | 2.4 m, 0.65 m, 40 kg | At risk |
| R11 | Interface v0.3: 10 kΩ coded INTERLOCK (node 0.30 V), vehicle heartbeat mode 2; 8.5 A maximum; below 60 V | SwapCell v0.3 unchanged; 15 A or less; below 60 V DC | Met (on paper) |
| R12 | $713 excluding the pack; salvage route about $538 | $650 excluding the pack | **Not met** |
| R13 | Class V1 receiver specified: preload 330 N, lever ratio 6.6, bolt factor 22 at 25 g | SwapCell latch class V1, no release or contact break | Not verifiable at TRL 3 |

## 11. Checks against the documents

The TRL 2 figures were checked against this note and the documents were corrected where they differed: vehicle mass 35 kg became 34.0 kg (36.8 kg with the heavier 2.85 kg pack), 9.0 Wh/km became 9.1 Wh/km once the 3 W auxiliary load was included, range 46 km became 45 km, pack power 179 W became 182 W, walking power 20 to 40 W became 30 to 41 W at 5 km/h, the 8 % hill 236 W became 233 W, the no-loss mechanical drive 7 to 9 km/h became 9.9 km/h, trail went from about 90 mm (no fork offset) to 58 mm, and the parts cost $630 became $713.

> **Safety:** These are paper sizings for a vehicle a person stands and walks on, driven by a 468 Wh lithium-ion pack at up to 54.6 V DC. The braking, belt-slip, fatigue, steering-column and latch figures above are not a substitute for testing, which is TRL 4 work and on hold. Nothing here clears the design for building or riding.
