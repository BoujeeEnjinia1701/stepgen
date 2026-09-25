---
doc_id: SGN-PRC-001
title: StepGen design precis
project: StepGen
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-24'
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
---

# StepGen design precis

StepGen is a manual stepper generator: the user walks in place on two rocker-linked pedals, one-way clutches turn each pedal's downstroke into rotation, a 40:1 chain and belt step-up spins a small flywheel and a BLDC motor used as a generator, and a load controller charges a PowerBox while setting how hard the pedals feel. First-order numbers give 50 to 100 W at the pedals and about 35 to 70 Wh stored per hour for a 70 kg user, enough to keep lights, phones, a radio and a router going through an outage. It will not run a fridge or a kettle.

![Hero render](../media/hero.png)

## How it works

1. **Step.** The user stands on two pedals, holds the handrail and walks in place. Each pedal pivots at its rear end. A rocker beam under the front ends links the pedals, so as one goes down the other comes up. Body weight does the work: each step lowers the user by the step height.
2. **Rectify the motion.** A short chain runs from the front tip of each pedal to its own one-way clutch (a 16-tooth single-speed bicycle freewheel) on a common jackshaft. The pedal going down drives the shaft; the other freewheels while a light return spring takes up its chain. Both left and right strokes therefore turn the jackshaft the same way.
3. **Step up the speed.** A 48:12 chain stage (4:1) and a poly-V belt stage (10:1) raise the jackshaft's 20 to 45 rpm to roughly 900 to 1,800 rpm at the generator.
4. **Smooth.** A 300 mm steel flywheel on the generator shaft carries the generator through the gap between steps, so its voltage stays steady and the pedals feel smooth.
5. **Generate.** A three-phase BLDC outrunner, run as a generator, produces about 15 to 30 V at working speed.
6. **Control and charge.** A three-phase rectifier feeds a DC bus. A load controller (microcontroller plus a buck-boost charger) draws the current that sets the step resistance, and charges the PowerBox at 39 to 54.6 V, 3 A maximum. A brake resistor absorbs energy when the pack is full, so the pedals never go slack.
7. **Show.** A small display on the handrail shows resistance level, steps, watts and watt-hours.

![Energy flow](../media/flow.png)

Figure 1. Energy flow at 75 W of pedal work. All values are estimates.

## Main components

Numbers match the exploded view and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Base frame | 40 x 40 x 2 mm steel square tube, 850 x 620 mm, welded or bolted | Carries pedal pivots and jackshaft bearings |
| 2 | Pedals on rocker | Two 380 mm steel pedal arms with non-slip treads, rear pivots, rocker beam linking the front ends | Adjustable end stops set step height 10 to 20 cm; elastomer bumpers |
| 3 | One-way clutches and jackshaft | Two 16T single-speed bicycle freewheels on a 20 mm shaft in pillow-block bearings | Proposed, awaiting Amish (alternative: sprag clutch bearings) |
| 4 | Chain drive, 4:1 | Pedal chains with return springs; 48T to 12T #40 or bicycle chain stage | Bicycle chain keeps parts cheap and familiar |
| 5 | Belt step-up, 10:1 | Poly-V (PJ section) pulleys about 200 mm and 20 mm on an intermediate shaft | Quieter than a second chain stage |
| 6 | Flywheel, 300 mm | 6 mm laser-cut steel disc, about 3.3 kg, on the generator shaft | Balanced; fully enclosed |
| 7 | BLDC generator | 63 mm class sensorless outrunner, Kv about 60 rpm/V, rated 250 W or more | Proposed, awaiting Amish |
| 8 | Drivetrain guard | Closed shell of 1 mm aluminum sheet with steel mesh vents | Removable only with tools |
| 9 | Handrail | 32 mm steel tube, two posts, top bar and side grips at about 1.0 m | Foam grips |
| 10 | Rectifier and load controller | Three-phase bridge, microcontroller, buck-boost charger, brake resistor, fuse, emergency stop | Inside the guard |
| 11 | Display and level selector | Small LCD or OLED with a rotary knob on the top bar | Level, steps, W, Wh |
| 12 | Output lead to PowerBox | 2 m twin cable, 2.5 mm², fused, polarized connector | Connector to match PowerBox, to confirm |

![Exploded view](../media/exploded.png)

Figure 2. Exploded view with BOM numbers.

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

### Power at the pedals

Mechanical work per step is body weight times step height. For the nominal user (70 kg, 15 cm): 70 x 9.81 x 0.15 = 103 J per step.

Table 1. Pedal power and stored energy for the nominal user (estimates).

| Cadence | Pedal work | Stored per hour at 70 % | Requirement |
| --- | --- | --- | --- |
| 30 steps per minute | 52 W | about 36 Wh | R2 (35 Wh) met, thin margin |
| 45 steps per minute | 77 W | about 54 Wh | |
| 60 steps per minute | 103 W | about 72 Wh | R2 (60 Wh) met |
| 60 steps per minute, 100 kg, 20 cm | 196 W | about 137 Wh | Within 250 W rating (R1) |

The current pitch quotes 60 to 100 Wh stored per hour. That figure needs about 85 to 145 W at the pedals, which the nominal user reaches only at the top of the cadence band. A range of about 35 to 70 Wh per hour is the honest figure for a 70 kg user. Changing the pitch is proposed, awaiting Amish.

### Efficiency chain

Table 2. Loss budget from pedal to pack (estimates; R6 target 65 %).

| Stage | Efficiency | Basis |
| --- | --- | --- |
| Drivetrain (freewheels, chains, belt, bearings) | 90 % | Bicycle chain about 97 % per stage, poly-V belt about 95 %, freewheel and bearing drag |
| Generator | 85 % | Outrunner well below rated load; copper and iron losses |
| Rectifier | 97 % | Two diode drops of about 0.5 V on a 25 V bus; synchronous rectification could reach 99 % |
| Charge controller | 94 % | Buck-boost converter at 20 to 100 W |
| Pedal to pack | about 70 % | Product of the above; R6 met |

At 75 W of pedal work this leaves about 52 W into the pack (Figure 1). Controller standby draw of about 1 W is not included.

### Gear ratio and generator speed

- Each step pulls about 150 mm of chain over a 16T freewheel (pitch diameter about 65 mm, circumference about 203 mm): about 0.74 revolutions per step.
- Jackshaft mean speed: 0.74 x 30 to 60 steps per minute = about 22 to 44 rpm. The shaft turns only during the downstroke, so peak speed is roughly twice this; the flywheel evens it out.
- Total step-up 4 x 10 = 40:1 gives a mean generator speed of about 900 to 1,800 rpm.
- With Kv about 60 rpm/V the open-circuit voltage is about 15 to 30 V at working speed and 50 V at an overspeed of 3,000 rpm, so the generator stays below 60 V DC (R7). A higher Kv motor would need a higher ratio or would give a lower, less efficient bus voltage.

### Flywheel sizing idea

- The flywheel only has to bridge the gap between steps, not store energy. At 30 steps per minute the gap is up to about 1 s, during which the generator draws about 36 J at 36 W.
- A 300 mm x 6 mm steel disc: mass = pi x 0.15² x 0.006 x 7,850 = about 3.3 kg; inertia J = 0.5 x 3.3 x 0.15² = about 0.037 kg·m².
- Stored energy at 900 rpm (94 rad/s): 0.5 x 0.037 x 94² = about 165 J. Losing 36 J drops speed by about 12 %, which the controller can ride through. At 1,800 rpm the stored energy is about 660 J and the rim speed about 28 m/s.
- Putting the flywheel on the slow jackshaft instead would need about 40² = 1,600 times the inertia for the same smoothing, which is why it sits on the fast shaft.

### Resistance and user weight

The load controller sets generator current, and so the torque that resists the pedals. A pedal descends at the speed where body weight balances that torque. Five levels span roughly 30 to 200 W of absorbed power, so a 40 kg user on level 1 and a 120 kg user on level 5 can both step at 30 to 60 steps per minute (R4). The controller ramps the load from zero at start and holds a minimum load, so the pedals never drop freely while someone is standing on them.

### Size, mass and cost

- Footprint 0.85 x 0.62 m, height about 1.1 m to the top of the display (R9 met).
- Mass about 34 kg: frame 9 kg, pedals and rocker 5 kg, handrail 5 kg, drivetrain 4 kg, flywheel 3.3 kg, generator 2.5 kg, guard 4.5 kg, electronics and lead 2 kg (R9 met, thin margin).
- Parts cost about $397 (R12 met, almost no margin). See `bom/bom.csv`.

## Key design choices

All choices below are proposed, awaiting Amish.

- **Stepper, not bicycle.** Walking in place needs no bicycle, riding skill or balance, and suits more users. The cost is that output depends on body weight. Proposed, awaiting Amish.
- **Freewheels on a jackshaft rather than a rack and pinion.** Bicycle freewheels are cheap, easy to find and proven in stair steppers. Alternative: sprag clutch bearings (quieter, more costly). Recommendation: bicycle freewheels for the first build. Proposed, awaiting Amish.
- **Small fast flywheel on the generator shaft.** About 3.3 kg instead of about 20 kg for a slow flywheel, at the cost of a higher rim speed that demands a full enclosure. Recommendation: fast flywheel. Proposed, awaiting Amish.
- **Chain then belt step-up (4:1 then 10:1).** The belt stage runs at the higher speed where chain noise would be worst. Alternative: a planetary gearbox (compact, costly). Proposed, awaiting Amish.
- **Generator voltage below the pack, with a buck-boost charger.** Keeps the generator well under 60 V even at overspeed. Alternative: a lower-Kv generator matched to the pack voltage with a simple buck charger, which risks exceeding 60 V at overspeed. Recommendation: buck-boost. Proposed, awaiting Amish.
- **No battery in StepGen.** All storage stays in the PowerBox, so StepGen has no lithium cells of its own. Proposed, awaiting Amish.

## Safety

> **Safety:** StepGen is moving machinery that a person stands on, driving a lithium-ion battery. Every hazard below needs a guard or a design control before a first build.

- **Pinch and crush points.** Pedal to frame, pedal to rocker, chain onto sprocket, belt onto pulley and the flywheel rim. Keep crush gaps at the pedals at 50 mm or more for toes and 25 mm or more for fingers, or close them completely (R10). Nothing in the drivetrain may be reachable by hand or foot.
- **Guarding.** The drivetrain guard (8) fully encloses chains, belt, flywheel and generator, and needs tools to open. The flywheel rim runs at up to about 28 m/s; the guard must be strong enough to contain it if it comes loose. Children must not be able to reach inside.
- **Falls.** Handrails on both sides (9), non-slip treads, pedal top no higher than 30 cm, and elastomer end stops so a pedal cannot drop hard if the controller loses load. The controller ramps resistance gently at start and never removes load suddenly while a user is on the pedals.
- **Electrical.** All circuits stay below 60 V DC (R7). The generator is sized so that even at 3,000 rpm overspeed with no load it produces about 50 V. The output lead is fused at the StepGen end. The PowerBox pack is lithium-ion: charge only within its voltage and current limits, and respect any fault signal from the PowerBox.
- **Emergency stop.** A stop button shorts the generator phases through the brake resistor, which brakes the flywheel within seconds.
- **Exertion.** Stepping at 60 steps per minute is vigorous exercise. Users with heart or joint conditions should start at low resistance and slow cadence; the display should show elapsed time.

## Open questions for TRL 3

- Confirm the PowerBox pack voltage window, charge current limit, connector and any communication or fault signal.
- Estimate noise from chains, belt and generator (R8).
- Check freewheel engagement lag at 30 steps per minute: does it waste part of each stroke?
- Size the rocker beam, pedal pivots and frame for a 120 kg user stepping hard, and check tip stability with a user leaning on one rail.
- Choose the generator: a hobby outrunner, an e-scooter motor or a salvaged motor. Proposed: 63 mm outrunner, awaiting Amish.
- Identify a partner and user group for co-design; learn whether sustained stepping is acceptable to older users.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
