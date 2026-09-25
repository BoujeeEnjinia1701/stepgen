---
doc_id: SGN-PRC-001
title: StepGen design precis
project: StepGen
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, efficiency chain, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Concept changed at Amish's direction from a stationary stepper generator to a walking-treadmill vehicle
---

# StepGen design precis

StepGen is a walking-treadmill vehicle. The rider stands upright on a 1.05 m free-running belt between two 20 in wheels and walks at an ordinary 4 to 6 km/h; a sensor on the belt roller reads the walking speed, and a 250 W geared hub motor in the rear wheel, powered by a shared SwapCell pack, drives the vehicle at up to 25 km/h. The belt is a control input, not the engine: walking puts only about 20 to 40 W into the belt, while cruising at 20 km/h needs about 136 W at the wheel. First-order numbers suggest about 9 Wh/km at 20 km/h, about 35 to 46 km on one SwapCell pack on the flat, a vehicle mass of about 35 kg without the pack and a parts cost of about $630 excluding the pack, which is over the $400 budget.

> **Concept change.** Amish decided on 2026-09-24 that StepGen becomes a walking-treadmill vehicle like the Lopifit walking bike: "as the person walks his scooter / bike moves forward but hes upright walking instead of pedalling". The stationary stepper generator of version 0.2 is dropped entirely and no longer charges a PowerBox. Everything else in this document is proposed, awaiting Amish.

![Hero render](../media/hero.png)

*Figure 1. StepGen massing model with a 1.75 m rider standing on the belt mid-stride. Concept, not for fabrication.*

## How it works

1. **Step on.** The rider stands on the belt deck, which is 240 mm (9.4 in) above the ground with open sides, holds the handlebar and clips the lanyard stop to a wrist or belt.
2. **Walk.** The rider walks forward at a normal pace. The belt is not powered: the rider's feet push it rearward over a bed of small rollers, the way a non-motorized treadmill works. An anti-reverse clutch on the rear roller lets the belt run only rearward.
3. **Sense.** A Hall sensor on the front roller reads belt speed, which equals walking speed. The logic board also reads both brake levers, the lanyard switch and the level selector.
4. **Assist.** When the belt has run above 1.5 km/h for 0.5 s, the logic board commands motor power in proportion to belt speed, scaled by the selected level (three levels proposed) and capped at 250 W and 25 km/h. Walking faster asks for more power; walking slower asks for less.
5. **Drive.** The controller drives a 250 W geared hub motor in the 20 in rear wheel from the SwapCell pack at about 39 to 54.6 V.
6. **Stop.** When the rider stops walking, pulls either brake lever or loses the lanyard, the motor turns off within 0.5 s. Two disc brakes stop the vehicle. The anti-reverse clutch holds the belt, so the rider's feet brace on it as on a scooter deck instead of sliding forward.
7. **Step off.** The rider steps sideways off the low deck.

![Energy flow](../media/flow.png)

*Figure 2. Energy and control flow at a 20 km/h cruise on the flat. The energy path runs from the pack to the wheel; walking is on the control path. The optional roller generator is dashed. All values are estimates.*

![Cutaway](../media/cutaway.png)

*Figure 3. Section through the belt deck on the vehicle centre line.*

## Main components

Numbers match the exploded view and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Main frame | Welded mild steel: 25 x 50 mm deck rails, cross members, rear stays, nose, down tube and head tube | Wheelbase about 1.85 m |
| 2 | Belt and end rollers | 400 mm treadmill belt, two 50 mm crowned rollers 1.05 m apart, tensioner | Belt top 240 mm above the ground |
| 3 | Roller bed | 14 idler rollers, 30 mm, under the top run | Keeps belt drag low; a slider deck would need several times the push force |
| 4 | Anti-reverse clutch and belt drag | Sprag one-way bearing on the rear roller, adjustable drag | Belt runs rearward only; drag sets the feel |
| 5 | Belt speed sensor | Hall sensor and 8-magnet ring on the front roller | The only input that commands assist |
| 6 | Rear wheel with 250 W geared hub motor | 48 V 250 W geared hub in a 20 in rim, torque arms | Proposed, awaiting Amish |
| 7 | Front wheel, fork and headset | 20 in wheel, steel disc fork, 70° head angle | |
| 8 | Steering column, handlebar and grips | Column to a 1.23 m bar height (0.99 m above the belt), 580 mm bar | Bar height to be adjustable after co-design |
| 9 | Brakes with motor cut-off levers | Two mechanical disc brakes, 160 mm rotors, cut-off switches in both levers | |
| 10 | SwapCell receiver cradle and host adapter | Cradle on the down tube; microcontroller heartbeat and interlock | Same design as SunSpoke |
| 11 | SwapCell pack | 13S2P, about 46.8 V nominal, about 468 Wh, 2.8 kg | Shared; not in the StepGen parts cost |
| 12 | Controller and walking logic board | 48 V, 15 A sine-wave controller; ESP32 with CAN | Logic is a labeled sketch until TRL 3 |
| 13 | Display, level selector, lanyard stop | Speed, level and charge display; magnetic lanyard switch | |
| 14 | Guards | Heel guard and fender over the rear tire, roller end covers, side boards, toe guard | See Safety |
| 15 | Wiring harness with fuse | Keyed waterproof connectors, 20 A fuse | |

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with BOM numbers. Item 16 (hardware) has no callout.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions: rider 80 kg, vehicle about 35 kg, SwapCell pack 2.8 kg, total about 118 kg; rolling resistance coefficient 0.010; standing rider drag area CdA about 0.70 m² (larger than a seated upright cyclist); air density 1.2 kg/m³; motor and gearbox 80 % and controller 95 % efficient; usable pack energy about 410 Wh (the SwapCell precis gives about 454 Wh at the terminals per full cycle, and a 10 % reserve is kept); belt rolling-bed friction coefficient about 0.02.

*Table 1. Key numbers (estimates).*

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Walking speed on the belt | 4 to 6 km/h (2.5 to 3.7 mph) | Normal adult walking pace | R1 |
| Vehicle speed | Up to 25 km/h (15.5 mph); 15 km/h beginner mode; about 20 km/h typical cruise | Assist cut-off set in firmware | R3 met by design |
| Motor power | 250 W rated; about 136 W at the wheel at 20 km/h and about 221 W at 25 km/h | Road load: rolling 0.010 x 118 kg x 9.81 x v, plus air 0.5 x 1.2 x 0.70 x v³ | R4 met |
| Pack power and current | About 179 W and 3.8 A at 20 km/h; about 291 W and 6.2 A at 25 km/h; 15 A controller limit | Wheel power over 0.80 x 0.95 at 46.8 V | R11 met |
| Energy per km | About 6.9 Wh/km at 15 km/h, 9.0 Wh/km at 20 km/h, 11.6 Wh/km at 25 km/h | Pack power over speed, flat, steady, no wind | |
| Range on one SwapCell pack | About 60 km at 15 km/h, 46 km at 20 km/h, 35 km at 25 km/h on the flat; perhaps 25 to 35 km with hills, stops and wind | 410 Wh usable | R5 (30 km at 20 km/h) met |
| Hill | 8 % grade at 8 km/h needs about 236 W at the wheel; 5 % at 15 km/h needs about 319 W, so the vehicle slows to about 12 km/h there | Grade plus road load | R6 met, thin margin |
| Mass | About 35 kg without the pack, about 38 kg with it | Frame 11.5, belt and rollers 4.5, roller bed 2.5, rear motor wheel 4.5, front wheel and fork 3.5, steering 2.5, guards 2.0, brakes 1.2, electrics and hardware 3.2 kg | R10 (40 kg) met, thin margin |
| Size | About 2.35 m long, 0.62 m wide at the bar, about 1.3 m to the top of the display | Massing model | R10 met, thin margin on length |
| Belt | 1.05 m between roller centres (about 1.0 m usable inside the heel and toe guards), 400 mm wide, top 240 mm above the ground, about 145 mm ground clearance | Massing model | R1, R8 met |
| Rider power into the belt | About 15 to 30 N of push, or about 20 to 40 W at 4 to 6 km/h, all dissipated as belt drag | Rolling bed 0.02 x 80 kg x 9.81 = 16 N, plus roller bearings, belt flexing and the drag setting | R1 met |
| Rider effort | About 250 to 350 W metabolic, light exercise similar to ordinary walking | About 3 to 3.5 MET for an 80 kg adult | |
| Braking | About 8 m from 25 km/h at 3 m/s² after the brakes are applied | v² / 2a | R7 met on paper |
| Optional roller generator | About 5 to 10 W to the pack for about 15 W of extra walking effort; about 5 % more range (about 46 to 48 km at 20 km/h) | Small BLDC at about 60 % from belt to pack | Not recommended now |

### Why the motor does the work

Walking on the belt delivers about 20 to 40 W, and all of it is spent pushing the belt over its rollers. Even if a mechanical drive delivered all 30 to 40 W to the wheel, road load limits the vehicle to about 7 to 9 km/h on flat pavement, and it would stall on a 3 % grade, which needs about 64 W at 5 km/h. After drivetrain losses, walking pace is the realistic result. This matches reports from mechanical treadmill-bike builders ([SolidSmack](https://www.solidsmack.com/design/evolution-unusual-treadmill-bicycle/)). The Lopifit also drives its wheel with a 250 W motor, not with the belt ([New Atlas](https://newatlas.com/urban-transport/lopifit-electric-scooter-treadmill-bike-walking/)).

### Assist law (sketch, not firmware)

A labeled sketch of the control rule, to be written properly at TRL 3:

- Assist power P = k(level) x v_belt, with k chosen so that walking at 5 km/h gives about 100, 175 or 250 W at levels 1, 2 and 3. Power is capped at 250 W and tapered to zero between 23 and 25 km/h (15 km/h in beginner mode).
- The power command ramps at no more than about 100 W/s, so the vehicle cannot surge ahead of the rider. Near top speed the 250 W limit keeps acceleration to about 0.5 m/s².
- Assist is off unless the belt has run above 1.5 km/h for 0.5 s, and it turns off within 0.5 s of the belt stopping, either brake lever or the lanyard switch.

### SwapCell interface

StepGen uses the SwapCell interface v0.2 without change. The host adapter sends the heartbeat and closes the interlock so the pack enables discharge. Continuous current stays below 15 A, which also fits the pack's proposed legacy mode and its thermal limit, which is at risk at 20 A. Known gaps that StepGen depends on, to be flagged to the SwapCell project rather than solved here:

- The connector family and the vibration and shock rating of the latch (3 g is a placeholder) are not yet set. A vehicle with 20 in wheels on rough pavement needs a real figure.
- The behavior rules allow charging only when a dock heartbeat requests it. Charging from a vehicle while it is driving, which the optional roller generator would need, is not defined.
- The CAN bit layout is TRL 3 work, so the logic board's message handling cannot be finished before it.

## Key design choices

All choices below are proposed, awaiting Amish, except the change to a walking vehicle, which Amish decided.

- **Form factor: two-wheel, long wheelbase, bike type.** Recommended. A walking stride at 5 km/h is about 0.7 m, so the belt needs about 1.0 m of usable length. That sets a long wheelbase (about 1.85 m). Two wheels keep the vehicle narrow for cycle lanes and doors. Alternatives: (a) a compact scooter type with 12 to 16 in wheels and a belt of about 0.7 m, which is shorter and lighter but forces short shuffling steps and copes poorly with rough surfaces; (b) a three-wheel tadpole version with two front wheels, which stands up on its own and suits riders without two-wheel balance, but is wider (about 0.75 m), heavier and less stable in fast turns with a standing rider. Recommendation: two wheels for the first concept, with the three-wheel version kept open until co-design shows whether non-cyclists can balance.
- **Wheels: 20 in (ETRTO 406) front and rear.** Recommended. One tire size, a low deck, common parts. Alternatives: a 28 in front wheel like the Lopifit (rolls better over rough ground, longer vehicle), or 16 in wheels (shorter, harsher ride).
- **Motor and speed class: 250 W rated rear geared hub, assist cut at 25 km/h, 15 km/h beginner mode.** Recommended, because it stays within EU pedelec limits and a standing rider has high drag and a high centre of mass. Alternatives: a US class 1 style limit of 20 mph (32 km/h) with a 500 to 750 W motor (more hill ability, more risk for a standing rider, and not legal as a pedelec in the EU), or a lower 20 km/h cap throughout.
- **Rear drive, not front.** The rider's weight sits mostly over the rear half of the deck, which gives the rear wheel traction, and the steering stays light. Alternative: a front hub motor as in SunSpoke (simpler wiring, but a light front wheel can spin on wet surfaces).
- **Roller bed rather than a slider deck.** A slider deck (belt on a waxed board) has a friction coefficient of about 0.1 to 0.2, which would need about 80 to 160 N of push from an 80 kg rider. A roller bed cuts this to about 15 to 30 N.
- **Anti-reverse clutch on the belt.** Lets the rider brace against the belt when braking. Without it, a free belt would let the feet slide forward under deceleration.
- **Pack on the down tube, ahead of the rider's feet.** Keeps the pack clear of the stride and easy to swap from the side. Alternatives: under the deck (too little ground clearance) or on the steering column (heavier steering).
- **Regeneration from the belt: not in the first concept.** Recommended. It would return only about 5 to 10 W, costs about $35 to $50, makes walking harder, and needs a SwapCell charge mode that does not yet exist. Keep a mounting point on the front roller for a later study.

## Safety

> **Safety:** StepGen is a moving vehicle with a moving belt that a person stands on, driven by a 468 Wh lithium-ion pack at up to 54.6 V DC. Every hazard below needs a design control before any build.

- **Falls on a moving belt.** A rider who trips or stops walking abruptly on a belt can fall. Controls: the belt is free-running, so it stops when the rider stops; the motor turns off within 0.5 s when the belt stops; handlebar at about hip-to-waist height; non-slip belt surface; low deck (240 mm) with open sides so a foot can go down. The dynamics of a rider who stumbles while the vehicle coasts at 20 km/h need a proper study at TRL 3.
- **Dead-man and lanyard cut-off.** A magnetic lanyard clipped to the rider cuts motor power if the rider leaves the deck. Handle sensors like those on the Lopifit ([Lopifit](https://www.lopifit.com/what-is-a-lopifit/)) are an option to study.
- **Braking with feet on a belt.** Under braking the rider's body pushes forward. The anti-reverse clutch stops the belt moving forward, so the feet can brace; the toe guard gives a stop. Braking at about 3 m/s² asks an 80 kg rider to resist about 240 N, which the legs and arms can share. Harder stops risk pitching the rider over the bar, so brake modulation and bar height need checking.
- **Pinch and entanglement.** In-running nips where the belt meets each end roller can trap toes, fingers and clothing, and the rear tire runs close behind the heel. Controls: roller end covers, side boards over the belt edges, a heel guard and fender over the rear tire, and spoke guards. Guard gaps follow ISO 13857 reach distances. Long skirts and laces are a specific risk to check in co-design.
- **Speed.** Assist is cut at 25 km/h and a beginner mode limits it to 15 km/h. Acceleration is limited so the vehicle cannot pull away from the rider.
- **Helmet.** Riders should wear a bicycle helmet. A standing rider's head is about 2 m above the ground, higher than on a bicycle, so a fall is from a greater height.
- **Stability.** A standing rider raises the centre of mass. Tip-over in turns, on cross-slopes and when stepping on or off must be checked at TRL 3, and a kickstand is needed so the vehicle does not fall when parked.
- **Electrical and battery.** Every circuit stays below 60 V DC. The SwapCell pack's BMS, interlock and warn-then-derate behavior apply; a sudden loss of power at speed is less dangerous here than a sudden surge, but both are covered by the ramp limit. A 20 A fuse protects the harness. Packs are charged only in a SwapCell dock, never on the vehicle.
- **Legal use.** Until the legal category is known, StepGen should be used only where the rules allow it.

## Open questions for TRL 3

- Legal category of a pedal-less walking vehicle in the first target country, and whether pedelec-equivalent limits are enough.
- Can non-cyclists balance a two-wheeled walking vehicle, or does the first prototype need three wheels? (Co-design.)
- Belt drag and walking feel: roller bed spacing, drag setting and whether 1.0 m of belt is enough for tall riders at 6 km/h.
- Rider dynamics when stumbling, stopping walking abruptly or braking hard; required bar height and handle position.
- Frame stiffness and fatigue for a 120 kg rider on a 1.85 m wheelbase with a standing load.
- Steering geometry for a standing rider at 25 km/h (head angle, trail, bar reach).
- SwapCell latch vibration rating and connector choice; flag any conflict to the SwapCell project.
- Whether the optional roller generator is worth studying further once SwapCell defines a charge-while-driving mode.
- Cost reduction with salvaged treadmills and bikes, to approach the budget.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
