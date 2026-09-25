# StepGen

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** CleanTech · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $400 USD · **Difficulty:** 3 of 5

Walking-treadmill vehicle: the rider stands upright and walks at a normal pace on a short free-running belt between the wheels, a belt-speed sensor sets the assist of a 250 W hub motor, and the vehicle moves at e-bike speed (up to 25 km/h) on a shared SwapCell pack. Walking is the control input; the motor does the work.

![StepGen concept: a rider walking upright on the belt deck between two 20 in wheels](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Many people who would gain from an e-bike never ride one because cycling needs riding skill, balance on pedals and a seated posture that does not suit everyone, while walking is natural and needs none of these. Short trips of 2 to 15 km stay too long to walk and too costly by car. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

Walking-treadmill vehicle: the rider stands upright and walks at a normal pace on a short free-running belt between the wheels, a belt-speed sensor sets the assist of a 250 W hub motor, and the vehicle moves at e-bike speed (up to 25 km/h) on a shared SwapCell pack. Walking is the control input; the motor does the work.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Long-wheelbase steel frame with two 20 in wheels
- Free-running treadmill belt on a roller bed, with an anti-reverse clutch
- Belt-speed sensor that sets the motor assist
- 250 W geared rear hub motor and 48 V controller, assist cut at 25 km/h (proposed)
- Shared 48 V SwapCell pack in a down-tube cradle (not in the parts cost)
- Two disc brakes with motor cut-off levers and a lanyard stop switch
- Guards over the belt rollers and the rear tire

First-order estimates: about 9 Wh/km at 20 km/h, about 35 to 46 km per SwapCell pack on the flat, about 35 kg without the pack, and about $630 in parts excluding the pack (over the $400 budget; see the [review note](docs/REVIEW.md)).

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> A rider stands on a moving belt on a moving vehicle. The motor must run only while the rider walks and stop when the belt stops, a brake is pulled or the lanyard comes out. Guard the belt rollers and the rear tire, keep the deck low with open sides, limit speed to 25 km/h, and wear a helmet. The SwapCell pack is a 468 Wh lithium-ion battery; every circuit stays under 60 V DC.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (SGN-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `SGN-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
