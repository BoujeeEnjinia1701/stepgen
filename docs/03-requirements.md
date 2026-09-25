---
doc_id: SGN-REQ-001
title: StepGen requirements
project: StepGen
doc_type: Requirements
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
  change: First measurable requirements for TRL 2
---

# StepGen requirements

These are first-pass requirements for the concept. Targets are proposals for review and will be checked by calculation at TRL 3 and revised after co-design with users.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Accept the mechanical power a person can sustain | 50 to 100 W nominal at the pedals (70 kg user, 15 cm step, 30 to 60 steps per minute); drivetrain and generator rated for 250 W peak | Work-per-step calculation; component ratings |
| R2 | Store a useful amount of energy per hour of stepping | 35 Wh or more at 30 steps per minute and 60 Wh or more at 60 steps per minute, for the nominal user | Efficiency chain calculation; later metered bench test |
| R3 | Comfortable step height | Adjustable 10 to 20 cm at the foot, nominal 15 cm; pedal top no higher than 30 cm above the floor | Linkage geometry in the model |
| R4 | Resistance suits a wide range of users | 5 or more selectable resistance levels; users of 40 to 120 kg can step at 30 to 60 steps per minute without bottoming out; display shows level, steps, W and Wh | Load-line calculation per user mass; design review |
| R5 | Charge the PowerBox correctly | Output 39.0 to 54.6 V DC (13S pack at 46.8 V nominal, assumed; to confirm against PowerBox), charge current limited to 3 A, charging stops when the pack is full or the PowerBox signals a fault | Charger specification; interface review with PowerBox |
| R6 | Efficient energy chain | 65 % or more from pedal work to energy stored in the pack at nominal load | Loss budget calculation; later measurement |
| R7 | Safe extra-low voltage | Every conductor under 60 V DC in all conditions, including generator overspeed to 3,000 rpm and a disconnected load | Generator constant (Kv) and overspeed calculation |
| R8 | Quiet indoor use | 60 dBA or less at 1 m while stepping at 60 steps per minute | Component noise estimate; later sound level measurement |
| R9 | Fits a small room and can be moved | Footprint 0.9 x 0.7 m or less, height 1.3 m or less, mass 35 kg or less, movable by two people | Massing model; mass estimate |
| R10 | Guard all moving parts | Chains, sprockets, belt, flywheel and generator fully enclosed; no drivetrain part reachable by hand or foot; crush gaps at the pedals of at least 50 mm for toes and 25 mm for fingers, or fully closed | Design review against guarding practice (ISO 13854 and ISO 13857) |
| R11 | Safe for untrained users | Handrail on both sides at about 1.0 m above the floor; non-slip pedal treads; elastomer end stops so a pedal cannot drop hard if the controller fails; frame stable with a 120 kg user leaning on one rail; emergency stop that brakes the flywheel | Stability calculation; design review |
| R12 | Low cost and buildable | Parts cost $400 or less; built with common hand tools, a drill press and basic welding or bolted steel; bicycle parts where possible | Priced BOM |

## Assumptions

- Mechanical work per step equals body weight times step height: 70 kg x 9.81 m/s² x 0.15 m = about 103 J per step.
- A step is one pedal going down; 30 to 60 steps per minute is 0.5 to 1 step per second.
- The PowerBox pack is a 13-series lithium-ion pack (46.8 V nominal, about 39 to 54.6 V). The PowerBox design must confirm this.
- Users step at a cadence they choose; the load controller sets the resistance so the pedal descends at a comfortable speed for that user's weight.

## Requirements at risk

- **R2 at the low end and the pitch figure.** The nominal user at 30 steps per minute stores about 36 Wh per hour, only just above the 35 Wh target. The figure of 60 to 100 Wh per hour in the current pitch is reached only at the top of the cadence band or by heavier users; see the precis and review note.
- **R8** is unverified. Chain and belt noise at the generator speed is not yet estimated.
- **R12** is met with almost no margin (about $397 of $400).
