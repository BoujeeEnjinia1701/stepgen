---
doc_id: SGN-PRB-001
title: StepGen problem statement
project: StepGen
doc_type: Problem statement
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work, honest energy framing)
---

# StepGen problem statement

When the grid fails, many households lose the small loads that matter most: lights, phone charging, a radio and an internet router. These loads add up to only tens of watts, yet homes without roof space, sun or money for solar have no way to keep them running, and the human-powered options that exist mostly assume the user can ride a bicycle.

## The problem

Outage-prone cities, informal settlements and off-grid homes often lose power for hours at a time. A small battery power station such as the portfolio's PowerBox (a SwapCell-based pack of about 46.8 V nominal) can carry essential loads through an outage, but only if something recharges it. Solar is the usual answer. It fails when there is no secure roof or yard, during long cloudy or smoky periods, and at night.

Human power can fill part of that gap, but only part of it. A healthy adult can sustain roughly 50 to 100 W of mechanical work for an hour. After drivetrain and electrical losses that is tens of watt-hours stored, not kilowatt-hours. StepGen is framed around that honest number:

| Load (typical) | Energy | What one hour of stepping (about 35 to 70 Wh stored) covers |
| --- | --- | --- |
| LED lamp, 5 W | 5 Wh per hour of light | 4 lamps for about 2 to 3 h |
| Phone charge | 10 to 15 Wh per charge | 3 to 5 phone charges |
| Wi-Fi router, 8 to 12 W | about 10 Wh per hour | about 3 to 6 h of connectivity |
| Radio, 2 to 5 W | 2 to 5 Wh per hour | an evening of listening |
| Refrigerator | 1 to 2 kWh per day | Not covered. Days of stepping per day of use |
| Kettle, 2 kW | about 100 Wh per boil | Not covered |

StepGen will not power a home. It keeps communication and light going through an outage.

## Why a stepper and not a bicycle

Pedal generators built on bicycles or bicycle trainers work, but they exclude many people: those without a bicycle, those who never learned to ride, older adults with balance concerns, people whose clothing makes riding impractical, and children too small for the frame. Walking in place on two pedals is a movement nearly everyone already knows. A handrail carries balance, no special clothing is needed, and the same machine suits users of very different heights because there is no saddle or crank reach to set.

The stepper also has an honest limit: body weight does the work, so a light user produces less power than a heavy one at the same cadence, and sustained stepping at 60 steps per minute is vigorous exercise. The requirements treat both as design inputs.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Household in an outage-prone city | Keep phones, lights and router running through daily or weekly outages | Apartment or small house; limited floor space; no roof access |
| Household in an informal settlement | Reliable light and phone charging where grid supply is irregular or informal | Small dwellings; security concerns; low cash budget |
| Off-grid rural home | A top-up source for a small battery when solar is weak | Seasonal cloud, dust or smoke; long evenings |
| People who cannot or do not cycle | A human-power option that does not need a bicycle, riding skill or balance | Older adults, people with some mobility limits, people in clothing unsuited to riding |
| Community hub (clinic, school, shelter) | Shared charging point run by volunteers in turns | Several users per day of different body weights |

## Constraints

- Garage-buildable prototype for about $400 USD, using bicycle parts, standard steel tube and off-the-shelf electronics.
- Charges a PowerBox pack at about 46.8 V nominal. Every conductor must stay at safe extra-low voltage, under 60 V DC, in all conditions.
- Fits in a small room: about the floor area of a doormat and a chair, and light enough for two people to move.
- Safe for untrained users of 40 to 120 kg: no exposed moving parts, a handrail, and no hazard if the load controller fails.
- Quiet enough to use indoors at night.
- No mains connection; the stepper only feeds the PowerBox.

## Out of scope

- Mains-voltage output. The PowerBox handles any inverter; StepGen stays at low-voltage DC.
- Running high-power loads (fridges, kettles, heaters, pumps) or whole-home backup.
- A built-in battery. Storage lives in the PowerBox.
- Exercise tracking beyond steps, watts and watt-hours on the display.
- Grid export or any grid connection.

## Prior work

- **Bicycle pedal generators and generator trainers.** Well documented in the maker and development community. Fit riders sustain roughly 75 to 150 W. Their limits are the need for a bicycle and riding ability, and many designs leave chains and rollers exposed.
- **Hand-crank generators** in radios, torches and phone chargers. Very accessible but limited to roughly 5 to 20 W, which is too little to recharge a power station usefully.
- **Self-powered gym equipment.** Commercial steppers, ellipticals and bikes that power their own consoles or feed energy back to a building. They show that stepping motions drive generators well, but they are costly, heavy and not built for low-income settings.
- **Energy-harvesting floor tiles.** These capture a few joules per footstep, so they suit sensors and signage, not household charging.
- **Stair-stepper exercise machines** already use rocker-linked pedals with one-way clutches and a flywheel or fan brake. StepGen borrows this proven mechanism and replaces the brake with a generator.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

## Open questions

- Which user group and partner to start with: an outage-prone city household network, a settlement community organization, or a community hub? Proposed, awaiting Amish.
- Is sustained stepping acceptable to older or less fit users, or should StepGen add a seated option later? To be learned in co-design.
