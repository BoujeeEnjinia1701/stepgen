---
doc_id: SGN-DDR-003
title: StepGen design for construction
project: StepGen
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction and open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** draft. The changes in Tables 1 and 2 were made under Amish's 2026-09-30 instruction to make the design physically buildable; they are open for his review. Nothing here changes what StepGen does, its pitch or its safety case. Nothing here is recorded as accepted.

## Context

On 2026-09-30 Amish approved the build plan format for the portfolio and asked for it to be extended to every repo, with outstanding decisions kept in a separate design decisions register. For the drawings he wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations."

The TRL 3 model of SGN-DDR-002 was a massing model: correct sizes and interfaces, but many parts were simplified shapes that overlapped, floated or had no fixing. A build123d check of that model found 23 pairs of components that overlapped (the upper rear stays ran through the rear roller and belt; the brake rotors sat outside the dropouts; the fork crown overlapped the down tube) and many parts with nothing holding them (cross members, roller bed carriers, side boards, guards, controller, kickstand).

The changes below keep what StepGen does: the same 20 in wheels, wheelbase (1855 mm), steering geometry (70 degrees, 30 mm offset, 58 mm trail), belt (1.05 m roller pitch, 400 mm wide, top 240 mm above the ground), roller bed, motor, brakes, pack position and SwapCell interface v0.3 receiver, bar height and controls. Every change is in `cad/src/model.py`, which is now built from 29 components and runs 72 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must stay apart are apart by at least the stated gap, no two components overlap, and the front wheel and fork clear the frame, toe guard, controller, cradle and pack at 45 degrees of steering lock each way. All 72 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The upper rear stays ran from the rails 450 mm ahead of the axle through the rear roller and the belt. | Two stays each side, 22 x 1.6 mm: an upper stay from a 3 mm end cap on the rail's rear end, and a lower stay from the rear face of the rear cross member, both to the dropout. | The stays now stay behind the deck. The two stays per side form a triangle in the vertical plane, so the cantilevered rear end is stiff. |
| P2 | The brake rotors sat outside the dropouts and fork legs (rear 95 mm, front 70 mm from the centre line), where a disc hub cannot carry them; the calipers had no mount. | Rotors on the hubs' 6-bolt mounts inside the dropouts: rear 52 mm and front 34.5 mm left of centre. Rear caliper on a tab on the left dropout plate; front caliper on the fork's post mount. | Standard disc positions for a 135 mm motor hub and a 100 mm front hub. |
| P3 | The dropouts were blocks with no slot; the hub motor had no torque arms modelled. | 6 mm dropout plates 135 mm apart inside, slots open downward; a torque arm on the outside of each dropout. | A hub motor in steel dropouts needs torque arms; the slot lets the wheel drop out. |
| P4 | The fork legs overlapped the front hub, and the fork crown and steerer had no headset. The 44 x 3 mm head tube could not take a headset. | Fork legs either side of a 100 mm hub; a bought steel head tube 50 x 3 mm machined for a ZS44 headset; headset modelled. The fork is a 26 in size rigid fork (axle to crown about 410 mm) carrying the 20 in wheel, because the head tube sits 640 mm up. | Keeps the decided head angle, offset, trail and bar height. A 20 in fork is about 80 mm too short for this head tube. |
| P5 | The down tube met the head tube at its bottom end and overlapped the fork crown; at even 35 degrees of steering the crown would strike it. | The down tube's axis meets the steering axis 100 mm above the head tube's bottom, and it is mitred to the head tube's side. | The fork now turns 45 degrees each way with 10 mm to spare (checked); the crown reaches the down tube between 50 and 60 degrees. |
| P6 | Two nose tubes and a block crossed under the front of the deck; the down tube stood on the block. | A 60 x 40 x 2 mm nose beam across the front ends of the rails; the down tube stands on its top. | One straight member, square cuts, flat faces for the down tube, the toe guard and the harness. |
| P7 | The three cross members cut 15 mm into each rail and floated. | Two 25 x 25 x 2 mm cross members welded under the rails (rear and middle); the nose beam ties the front. Ground clearance 145 mm (was 148 mm). | A cross member under the rails is welded on two full faces and clears the belt's return run by 14 mm. |
| P8 | The end rollers' axles passed through the rails with no fixing; the tensioner and the anti-reverse clutch housing were shapes outside the right rail with no mount; the speed sensor's magnet ring sat outside the rail on an axle that does not turn. | Fixed 17 mm axles: the front one held by an M10 bolt through each rail (with a crush tube welded inside the rail); the rear one in 45 mm slots, pulled back by two M8 tension bolts through welded lugs. The anti-reverse clutch is a one-way bearing of the same size as the roller's own bearing (CSK17 class for a 6203), pressed into the rear roller. The belt drag is a felt-tipped M8 thumb screw through the right rail onto the rear roller's end. The magnet ring is glued to the front roller's left end face, read by a Hall sensor on a small bracket inside the left rail. | Treadmill rollers have fixed axles and internal bearings; this keeps a salvaged roller usable and puts nothing outboard. The bearing takes about 6 N m against about 56 N m rated. Lean clearance rises from 30 to 32.6 degrees, now set by the kickstand. |
| P9 | The belt overlapped the rollers by 3 mm (the roller centres were set from the belt top without the belt's thickness). | Roller centres 3 mm lower, so the belt wraps the rollers and its top is still 240 mm above the ground. | Belt top and step-off height unchanged. |
| P10 | The idler rollers ran into their carriers; the carriers floated inside the rails. | Two 50 x 3 mm aluminium carrier bars bolted flat to the rails' inside walls with M6 rivet nuts; the idlers' spring axles snap into holes in the bars. | The rollers' standard spring axles need a flat bar with holes; rivet nuts work in a 2 mm wall. |
| P11 | The side boards floated 10 mm above the rails and touched the belt edge. | 6 mm HDPE boards on four 13 mm spacers per side, bolted into rivet nuts in the rail tops; 5 mm over the belt edge with 3 mm clearance above it (now 9 mm proud of the belt). | The boards still cover the belt edges and leave the sides open (R8). |
| P12 | The heel guard, roller covers and toe guard floated; the fender ran into the heel guard. | Heel guard with a bottom flange screwed to the rear cross member; roller covers with end tabs screwed to the rails' inside walls; toe guard leaning back 20 degrees with flanges on the nose beam (notched round the down tube); a bought 20 in fender riveted to the heel guard and stayed to the dropouts. | Every guard has a flat face to fix to. The front cover now covers the front roller's lower front quarter, where the in-running nip is. |
| P13 | The receiver cradle was a 16 mm solid block on the down tube; its lever post stood where the pack's handle is. | A folded 3 mm channel on two welded tabs (two M6 bolts), a 12 mm end stop plate with the floating receptacle, and an over-centre lever on a pin between ears on the channel walls, its pad pressing the pack's handle end. The pack sits 0.54 of the way up the down tube (was 0.55). | Keeps class V1 preload (330 N) and the 1 mm guide clearance, and puts the lever beside, not on, the handle. |
| P14 | The controller sat under the down tube, in the front tire's path when steering, with no fixing. | On a welded plate on the left side of the down tube, low down. | Checked clear of the front wheel at 45 degrees of lock. |
| P15 | The steering column had no joint to the fork steerer; the stem and bar had no clamp; the grip bends and controls overlapped each other. | A welded column: a slotted 33.7 x 2.3 mm sleeve that clamps the 28.6 mm steerer above the headset with two M6 bolts, the 38 x 2 mm column, a 30 x 2 mm stem and a slotted 26.9 x 2.3 mm bar clamp. A straight 580 mm bar (was 612 mm over swept grips); display, level selector, key switch, lanyard switch and brake levers each on their own bar clamp, apart. The display now faces the rider. | Stock tube sizes slip-fit each other, so it needs no lathe. Width falls from 0.61 to 0.58 m. |
| P16 | The kickstand overlapped the left rail with no mount; the harness ran through the frame and guards. | A bought side kickstand on a welded plate on the left rail. The harness runs inside the left rail between two grommets, along the nose beam, up the left side of the down tube and up the column. | Both now have a place to sit; the harness is out of reach of the belt and wheels. |
| P17 | The rear fender (added in P12) reaches 30 mm behind the rear tire. | Overall length 2.38 m (2.35 m over the tires). | Still inside R10's 2.4 m. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Frame 12.7 kg (was 12.5 kg); vehicle 35.1 kg without the pack, 37.9 kg with it; R10 margin 2.1 kg, unchanged at the first decimal (SGN-CAL-001 v0.3). | Nose beam, end caps, plates and the heavier head tube against two cross members and lighter stays. |
| Cost | BOM lines 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 15 and 16 restated and repriced. The donor bike's fork no longer fits, so the reference build buys the fork and headset (about USD 40). Value-engineering target USD 650; estimated cost of the constructable design USD 610 on the reference build (USD 40 under the target, was USD 546); all-new fallback USD 750 (was USD 721). | Parts added for construction and the fork change of P4. |
| Geometry | Length 2.38 m with the fender, width 0.58 m, height 1.29 m, ground clearance 145 mm, lean clearance 32.6 degrees. Wheelbase, trail, belt and bar height unchanged. | P7, P8, P15, P17. |
| Drawing | SGN-DWG-001 Rev P3; making sketches SGN-DWG-101 to 114 added. | Follows the model. |
| Documents | SGN-CAL-001 v0.3, SGN-PRC-001 v0.6, SGN-REQ-001 v0.6, `bom/bom-notes.md`. No requirement changed status. R12 is reported against the value-engineering target. | Follows the model. |

*Table 3. Proposed, awaiting Amish.* None. No change in this record alters what the vehicle does, its pitch or its safety case. Items to confirm when parts are bought are listed in the design decisions register (SGN-DEC-001).

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan SGN-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged: none not met; R1, R6 and R10 at risk; R9 and R13 not verifiable at TRL 3; the rest met on paper (SGN-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept bracket shapes (nose tubes, grip bends, outboard clutch housing, solid cradle). They need updating on Amish's Mac, where Blender is.
- The salvage reference build now buys its fork and headset; the donor bike still supplies the front wheel and brakes.
