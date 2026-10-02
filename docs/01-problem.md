---
doc_id: SGN-PRB-001
title: StepGen problem statement
project: StepGen
doc_type: Problem statement
version: "0.6"
status: Draft
date: '2026-10-02'
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Concept changed at Amish's direction from a stationary stepper generator to a walking-treadmill vehicle
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record Amish's decisions (SGN-DDR-001) on budget, legal route and co-design partners; SwapCell interface v0.3; numbers checked against SGN-CAL-001
- version: "0.5"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Decisions of 2026-10-02: first user group, the Netherlands as first country (RDW), balance as a fixed co-design test, stride check'
---

# StepGen problem statement

Many people who would benefit from an electric bike never use one because riding needs cycling skill, confidence on pedals and a seated posture that does not suit everyone. Walking is the one way of moving that almost everyone already knows. StepGen asks whether a small electric vehicle can be driven by walking: the rider stands upright on a short treadmill belt between the wheels, walks at an ordinary pace, and the vehicle moves forward at e-bike speed.

> **Concept change.** Amish decided on 2026-09-24 that StepGen is a walking-treadmill vehicle in the manner of the Dutch Lopifit walking bike, not a stationary stepper generator. The earlier generator concept, which charged a PowerBox, is dropped entirely. Version 0.2 of this document describes the earlier concept and remains in Git history. On 2026-09-25 Amish accepted the TRL 2 recommendations, including a $650 budget, the route for the legal question and the move to SwapCell interface v0.3 (SGN-DDR-001). The same day he accepted the TRL 3 recommendations, including a salvage reference build that keeps the $650 budget (SGN-DDR-002).

## The problem

Short trips of 2 to 15 km (about 1 to 9 mi) to work, school, a market or a clinic are too long to walk comfortably and too short or too costly for a car or a taxi. E-bikes fill this gap well for people who already cycle. They leave out:

- people who never learned to ride, which is common among adults in many countries and among women in some communities;
- older adults and people with some balance or joint limits who are nervous on a saddle and pedals;
- people whose clothing, such as long skirts or wraps, makes a diamond-frame bike awkward;
- people for whom a seated, pedalling posture is uncomfortable, for example after hip or knee problems, while ordinary walking is fine.

Walking needs no new skill. On a walking vehicle the rider stands, holds a handlebar and walks. The walking motion is a natural control input: walk and the vehicle goes, stop walking and it slows. The rider gets light exercise at a walking effort while covering distance at bicycle speeds.

## Why the belt is a control input, not the engine

A person walking puts only a small horizontal force into the ground, because walking is mostly about supporting and moving body weight, not pushing backward hard. On a free-running belt over a roller bed this is about 22 to 30 N (5 to 7 lbf) at 5 km/h, or roughly 30 to 41 W of mechanical power (estimate, see SGN-CAL-001). This vehicle at 20 km/h on the flat needs about 136 W at the wheel with an 80 kg rider. A purely mechanical belt-to-wheel drive would therefore move at about walking pace and would feel harder than walking, and people who built such drives report that they are slower than simply walking ([SolidSmack, "Walk Don't Ride"](https://www.solidsmack.com/design/evolution-unusual-treadmill-bicycle/)).

StepGen is framed around that fact. The belt tells the vehicle that the rider is walking and how fast; an electric hub motor supplies most of the propulsion; and a shared SwapCell battery pack supplies the energy. This is also how the Lopifit works: its 250 W motor drives the vehicle, and the belt does not recharge the battery ([New Atlas](https://newatlas.com/urban-transport/lopifit-electric-scooter-treadmill-bike-walking/)).

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Adults who do not cycle | Cover 2 to 15 km trips without learning to ride | Towns and peri-urban areas with cycle lanes or quiet roads |
| Older adults and people with mild balance or joint limits | An upright, familiar movement with a handlebar to hold | Short errands, clinic visits; must be able to step off easily |
| Commuters who want light exercise | Arrive without sweating, get some walking in | Flat to rolling urban routes, 5 to 15 km each way |
| Riders who share batteries across portfolio vehicles | One pack that also runs SunSpoke, WaterWalker assist and a PowerBox | Households or groups with a SwapCell dock |
| Local builders and bike mechanics | A frame and parts they can build, fix and adapt | Garage or market-town workshop with a welder |

## Constraints

- Garage-buildable prototype with a budget of $650 USD in `project.yaml` (decided by Amish, 2026-09-25), excluding the SwapCell pack, which is priced once in the SwapCell project. Amish decided on 2026-09-25 (SGN-DDR-002) that the reference build uses a salvaged walking-pad treadmill and a donor 20 in bike, which prices at about $546; an all-new build (about $721) is the fallback (see SGN-CAL-001).
- Uses the shared SwapCell pack (interface v0.3: 13S lithium-ion, about 46.8 V nominal, 39.0 to 54.6 V, about 468 Wh, 2.85 kg), with a 10 kΩ coding resistor in the INTERLOCK loop for wake and a vehicle receiver to latch class V1. StepGen must not change the interface locally; conflicts go back to the SwapCell project.
- Legal in intent: stay inside pedelec-like limits (250 W rated motor, assist cut before 25 km/h, motor only while the rider walks) so the vehicle can be argued to be as safe and as limited as an e-bike. Whether it legally counts as one is an open question (see below).
- Safe for untrained riders: no reachable pinch points, motor cut-off when the rider stops walking, lets go of a lanyard or pulls a brake.
- Rider can put a foot on the ground easily: low deck, open sides.
- Fits a cycle lane, a lift and a hallway: narrow and not much longer than a long bicycle.
- Every circuit stays below 60 V DC.

> **Safety:** StepGen puts a standing person on a moving belt on a moving vehicle at up to 25 km/h, powered by a 468 Wh lithium-ion pack at up to 54.6 V DC. Falls, pinch points at the belt rollers and rear tire, braking with feet on a belt, pack retention and battery fire are the main hazards; SGN-PRC-001 lists the controls. Nothing in this repo clears the design for building or riding.

## Legal status

On current rules StepGen does not clearly fit the e-bike category anywhere, because e-bike definitions assume pedals.

- **EU.** Pedal-assisted cycles with a continuous rated motor power up to 250 W, whose assistance is cut before 25 km/h and only while the rider pedals, are excluded from moped type approval ([Wikipedia summary of EN 15194 and Regulation 168/2013](https://en.wikipedia.org/wiki/Pedelec)). A walking vehicle has no pedals. In the Netherlands, guidance for walking bikes says an electric walking bike may use the pavement only up to 6 km/h and must otherwise use the cycle path or road, and that liability insurance is required for electric versions ([Scouters.nl](https://www.scouters.nl/hulpmiddel-keuze/loopfiets-volwassenen/)). Status in other member states is not established here.
- **US.** Federal law defines a low-speed electric bicycle as a two- or three-wheeled vehicle with fully operable pedals and a motor under 750 W with a top motor-only speed under 20 mph ([15 USC 2085](https://uscode.house.gov/view.xhtml?req=granuleid%3AUSC-prelim-title15-section2085&num=0&edition=prelim)). Most states use three classes: class 1 (assist only while pedalling, to 20 mph), class 2 (throttle, to 20 mph) and class 3 (assist only while pedalling, to 28 mph), and all of them require operable pedals ([Redtail, state guide](https://redtailebikes.com/blogs/journal/electric-bike-laws)).

The design therefore targets the stricter EU limits. Amish decided on 2026-09-25 that a first target country is picked and the vehicle's legal category confirmed there before any road use. Amish decided on 2026-10-02 that the first country is the Netherlands, with the category confirmed with the Dutch vehicle authority (RDW) before any road use. EU pedelec rules cover pedal-assisted cycles, so a pedal-less vehicle may fall outside them, and the RDW check may set a lower speed cap or require type approval.

## Out of scope

- Generating household electricity. The earlier stepper generator concept is dropped; StepGen does not charge a PowerBox. It draws from a SwapCell pack like the other portfolio vehicles.
- Cargo carrying beyond a small bag or basket.
- Speeds above 25 km/h, or motors above 250 W rated.
- Mains-voltage electronics or a built-in charger. Packs charge in a SwapCell dock.
- Off-road use.

## Prior work

- **Lopifit (Netherlands).** An electric walking bike with a treadmill belt between a 28 in front wheel and a 20 in rear wheel, a 250 W motor, a 960 Wh battery of about 5 kg, disc brakes front and rear, a top speed of 25 km/h and a claimed range of 50 to 70 km. It is about 2.22 m long, 0.42 m wide and about 55 kg, with a handlebar height of about 1.2 m, and costs from about €2,999 ([Lopifit](https://www.lopifit.com/what-is-a-lopifit/)). Its handles carry sensors that stop the treadmill with a small hand movement. It proves the concept works and is sold, but its price and mass put it out of reach of the users above.
- **Mechanical treadmill bikes.** Belt-driven bicycles without a motor have been built by hobbyists. The reported result is that they are slower than walking because the belt cannot deliver useful torque at low speed ([SolidSmack](https://www.solidsmack.com/design/evolution-unusual-treadmill-bicycle/)).
- **Stand-up elliptical bikes (ElliptiGO).** Mechanical, upright, with an elliptical stride that does deliver strong propulsion, but this is a running-like exercise machine for fit users, not a walking vehicle ([Wikipedia](https://en.wikipedia.org/wiki/ElliptiGO)). The upright posture also costs more air drag than a crouched cyclist.
- **Kick scooters and e-scooters.** Standing, easy to learn, but e-scooters use a throttle and give no exercise, and small wheels cope poorly with rough surfaces.
- **Portfolio siblings.** SunSpoke (bolt-on e-bike kit) and WaterWalker (walking water carrier with optional assist) share the SwapCell pack and the same 250 W hub motor class.

## User research and co-design

Design with, not for: this design is for people the author may not be part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO, cycling charity, older-adult group or university). By Amish's 2026-09-25 rule, community designs pick co-design partners per area later, so the partner stays open.
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate trip distance, route, speed, balance, step-off and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

First-session questions:

- Does walking on a moving vehicle feel safe, and at what speed does it stop feeling safe?
- Can users step on and off, and put a foot down, without help?
- Is two-wheel balance acceptable for non-cyclists, or is a three-wheel version needed? A fixed co-design test (decided by Amish, 2026-10-02): if most non-cyclists cannot ride at walking pace after a short trial, the three-wheel version is designed.
- Where would the vehicle be kept, and can users lift or wheel it into a building?

## Open questions

- Which user group to start with? Decided by Amish on 2026-10-02: non-cycling adults of working age who walk or take transit, with older adults as the second group once balance is understood. The partner is picked later, per area.
- Can a two-wheeled walking vehicle be balanced by people who never learned to cycle, or does the first prototype need three wheels? To be learned in co-design, as a fixed test (decided by Amish, 2026-10-02): keep two wheels for now and make balance a fixed co-design test: if most non-cyclists cannot ride at walking pace after a short trial, the three-wheel version is designed.
- What is the legal category of a pedal-less walking vehicle in the first target country? The route is decided (confirm before any road use), and the country is the Netherlands, with the category confirmed with the RDW (decided by Amish, 2026-10-02).
- Is a 1.0 m belt long enough for the intended users? SGN-CAL-001 shows it fits a 1.75 m rider only up to 5 km/h. To be learned in co-design, where stride length on the belt is one of the checks (decided by Amish, 2026-10-02).
