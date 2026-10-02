---
doc_id: SGN-BLD-001
title: StepGen prototype build plan
project: StepGen
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (SGN-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: 'Safety stop S7: legal category confirmed with the RDW before road use (decided by Amish, 2026-10-02)'
---

# StepGen prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order; the SwapCell pack (22) goes in last, after the safety stops.*

The prototype is one StepGen walking vehicle: a welded steel frame carrying a free-running treadmill belt between two 20 in wheels, a 250 W hub motor in the rear wheel, a steering column with a handlebar at 1.23 m, and a SwapCell pack in a cradle on the down tube. Figure 1 shows the 22 components in the order you make or fit them. Nine are made in a workshop with a welder: the frame (from rails, cross members, a nose beam, a down tube, stays, dropouts and small plates), the two idler carrier bars, the sensor bracket, the steering column, the receiver cradle, the heel guard, the two roller covers, the toe guard and the two side boards. The rest are bought and fitted: belt and rollers (from a used walking-pad treadmill), idler rollers, fork, wheels, hub motor, brakes, controller, logic board, controls, harness, kickstand and fender. The work is sawing, drilling and welding steel tube and plate, folding aluminium sheet, cutting plastic sheet, and bolting and wiring bought parts. The parts cost about USD 610 on the salvage route, pack excluded, from the bill of materials.

> **Safety:** StepGen carries a 468 Wh lithium-ion pack at up to 54.6 V DC and has a moving belt that a person stands on. Keep the pack out of the cradle and the fuse out until section 6 says otherwise. Welding needs a proper welding screen, gloves and ventilation; galvanised or painted steel must be ground clean before welding. Cut steel and aluminium edges are sharp: deburr everything.

## 2. What changed to make it buildable

The concept showed what StepGen does; many of its parts could not be made or fixed as drawn. Each change below keeps what the vehicle does, and all of them are recorded in decision record SGN-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Rear stays | Upper stays running through the rear roller and the belt | An upper stay from each rail's end cap and a lower stay from the rear cross member, both to the dropout (Figures 7 and 10) | The stays stay behind the deck and form a stiff triangle |
| Brakes | Rotors outside the dropouts and fork legs, calipers with no mount | Rotors on the hubs inside the dropouts; rear caliper on a tab on the left dropout, front caliper on the fork's post mount (Figures 9 and 28) | Standard disc positions for these hubs |
| Head tube and fork | A plain 44 mm tube; fork legs overlapping the hub | A bought head tube machined for a ZS44 headset; a 26 in size rigid fork carrying the 20 in wheel (Figure 19) | A headset needs a machined bore; the head tube sits higher than a 20 in fork reaches |
| Down tube | Joined at the bottom of the head tube, where the fork crown hit it | Joined 100 mm higher, on the side of the head tube (Figure 19) | The fork turns 45 degrees each way with room to spare |
| Front of the deck | Two nose tubes and a block | One nose beam across the rail ends; the down tube stands on it (Figure 6) | Flat faces for the down tube, the toe guard and the harness |
| Cross members | Cut into the rails, not fixed | Welded under the rails (Figure 4) | Full weld faces; clear of the belt |
| End rollers | Axles with no fixing; tensioner and anti-reverse clutch outside the rail with no mount | Fixed axles bolted to the rails; rear axle in slots with tension bolts; a one-way bearing inside the rear roller; a felt-tipped drag screw (Figures 10, 15 and 16) | Keeps a salvaged treadmill roller usable; nothing sticks out |
| Speed sensor | A magnet ring outside the rail on an axle that does not turn | A magnet ring on the front roller's end, read by a sensor on a bracket inside the rail (Figure 15) | The roller turns; its axle does not |
| Roller bed | Rollers running into floating carriers | Carrier bars screwed to the rails' inside walls; the rollers' spring axles clip into them (Figure 13) | Uses the rollers' standard axles |
| Guards and side boards | Floating plates | Each with a flange or tab screwed to the frame; side boards on spacers (Figures 23 to 27) | Every guard is fixed |
| Receiver cradle | A solid block; the lever stood where the pack's handle is | A folded channel on two tabs with an end stop and an over-centre lever beside the handle (Figures 21 and 22) | Same preload and fit, and it can be made |
| Controller | Under the down tube, in the front tire's path | On a plate on the left of the down tube (Figure 6) | Clear of the wheel at full lock |
| Steering column and bar | No joint to the fork; grip bends and controls overlapping | A welded column that clamps the steerer; a straight 580 mm bar with each control on its own clamp (Figures 19 and 20) | Stock tube sizes slide into each other; no lathe needed |
| Kickstand and wiring | No mount; harness through the frame | Kickstand on a welded plate; harness inside the left rail (Figures 6 and 11) | Each has a place to sit, away from the belt and wheels |

The vehicle is now 2.38 m long including the rear fender, 0.58 m wide and 35.1 kg without the pack. Wheelbase, steering geometry, belt length and height, and bar height are unchanged.

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen by the rider standing on the belt, facing forward. "Rear end" of a rail is the end nearer the rear wheel. Workshop tolerance is 1 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Main frame

The frame is welded from seven kinds of piece, made first (sections 3.1.1 to 3.1.6) and then welded up in a jig (section 3.1.7). Mild steel, S235 class, throughout.

#### 3.1.1 Deck rails (make 2, a right and a left)

![Figure 2. Making sketch of the deck rail](../cad/drawings/SGN-DWG-101.png)

*Figure 2. Deck rail making sketch (SGN-DWG-101).*

![Figure 3. Hole and slot positions in the deck rails](05-build-plan/rail-holes.png)

*Figure 3. Every hole, slot and nut in the rails, measured from the rear end and up from the underside.*

**What it is and what it is made from.** The two long side members that carry the belt, the rollers and the rider. 60 x 30 x 2 mm rectangular hollow section, standing on edge, 1150 mm long.

**How to make it.**

1. Cut two 1150 mm lengths, square. Mark one face of each as the outer wall; the right and left rails are mirror images, so mark them as a pair.
2. Rear axle slot, through both side walls: 17 mm tall, from 30 to 75 mm from the rear end, centred 42 mm up. Drill 17 mm at each end and saw out between; file straight.
3. Front axle hole, through both side walls: 10.5 mm, 1100 mm from the rear end, 42 mm up. Slide a 26 mm length of 16 x 3 mm tube inside between the walls on a 10 mm bolt and weld it in through the hole edges (the crush tube).
4. Inside wall: four 9 mm holes at 130, 430, 730 and 1020 mm, 25 mm up, and fit M6 rivet nuts (carrier bars).
5. Top face: four 9 mm holes on the centre line at 90, 430, 770 and 1090 mm, and fit M6 rivet nuts (side board spacers).
6. Right rail only: an 8.5 mm hole through both walls at 50 mm, 22 mm up; weld an M8 nut over it on the outside (drag screw).
7. Left rail only: 12 mm holes in the outer wall at 60 and 1135 mm, 26 mm up, for grommets (the harness runs inside); two M3 rivet nuts in the inside wall at 1092 and 1108 mm, 16 mm up (sensor bracket).
8. Deburr every hole inside and out.

**How it fits the parts next to it.** The rails stand on edge, 440 mm apart inside, with the cross members welded under them and the nose beam across their front ends (section 3.1.7).

**Check before moving on.** Lay the two rails side by side, outer walls out: every hole and slot pair lines up.

#### 3.1.2 Cross members and nose beam

![Figure 4. Making sketch of the cross members and nose beam](../cad/drawings/SGN-DWG-102.png)

*Figure 4. Cross members and nose beam making sketch (SGN-DWG-102).*

**What they are and what they are made from.** Two cross members tie the rails together from underneath; the nose beam ties their front ends and carries the down tube. 25 x 25 x 2 mm and 60 x 40 x 2 mm rectangular hollow section.

**How to make them.**

1. Cut two 500 mm lengths of 25 x 25 x 2 mm and one 500 mm length of 60 x 40 x 2 mm.
2. Rear cross member: two 9 mm holes in its top face, 80 mm each side of centre, 14 mm from its front face; fit M6 rivet nuts (heel guard).
3. Nose beam, lying flat (40 mm tall): four 9 mm holes in its top, 12 mm from its rear face, 80 and 180 mm each side of centre; fit M6 rivet nuts (toe guard).
4. Cap every open end with 2 mm plate, welded all round.

**How they fit the parts next to them.** The cross members sit under the rails, flush with the rails' outer faces: the rear one from 0 to 30 mm from the rails' rear ends, the middle one from 560 to 590 mm. The nose beam's rear face butts both rails' front ends, its underside flush with theirs.

**Check before moving on.** Each piece is 500 mm long within 1 mm and its ends are square.

#### 3.1.3 Down tube

![Figure 5. Making sketch of the down tube](../cad/drawings/SGN-DWG-103.png)

*Figure 5. Down tube making sketch (SGN-DWG-103), drawn laid flat along its axis.*

**What it is and what it is made from.** The tube from the nose beam up to the head tube, which carries the pack cradle and the controller. 44 x 2 mm steel tube.

**How to make it.**

1. Cut about 568 mm and trim to fit in the jig.
2. Foot: cut 20.5 degrees off square, so the tube stands at 69.5 degrees on the nose beam's flat top, centred on the beam.
3. Top: fish-mouth it to the 50 mm head tube at a 40.5 degree included angle. Print a tube mitre template for 44 mm onto 50 mm and file to it.

![Figure 6. Joint 7: nose beam, down tube foot and toe guard](05-build-plan/joint-07.png)

*Figure 6. Left half of the nose: the down tube stands on the nose beam; the toe guard's flange and the harness lie on its top; the controller sits on its plate on the down tube.*

**How it fits the parts next to it.** Its foot stands on the middle of the nose beam's top; its axis meets the head tube's axis 100 mm above the head tube's bottom end, 559 mm from the foot (Figure 6 and Figure 19).

**Check before moving on.** In the jig the foot sits flat on the beam and the fish-mouth closes on the head tube with no gap over 1 mm.

#### 3.1.4 Rear stays and dropouts

![Figure 7. Making sketch of the rear stays and dropouts](../cad/drawings/SGN-DWG-104.png)

*Figure 7. Rear stays and dropouts making sketch (SGN-DWG-104), left side.*

**What they are and what they are made from.** The rear triangle on each side that holds the hub motor: an upper and a lower stay of 22 x 1.6 mm tube and a 6 mm steel dropout plate. The left dropout carries the rear caliper tab.

**How to make them.**

1. Dropouts: cut two 60 x 60 mm squares of 6 mm plate; on the left one, leave a 75 x 60 mm tab on its rear edge. Slot each from its bottom edge: 12.2 mm wide, round end 30 mm up (the axle centre).
2. Upper stays: two lengths of about 290 mm. Lower stays: two of about 282 mm. Cut them long.
3. Slot each stay's dropout end 6 mm wide and 20 mm deep to take the plate.
4. Trim the stays to fit in the jig (section 3.1.7): each upper stay lands on the rail's end cap, centred 35 mm up; each lower stay lands on the rear cross member's rear face, 35 mm in from the rail's outer face and 13 mm up.

**How they fit the parts next to them.**

![Figure 8. Joint 1: the rear dropout, right side](05-build-plan/joint-01.png)

*Figure 8. The motor's axle sits in the dropout's slot; a torque arm bolts to the outside of the dropout and the axle nut tightens onto it.*

![Figure 9. Joint 2: rear caliper on the left dropout tab](05-build-plan/joint-02.png)

*Figure 9. The rear caliper bolts to the inside face of the left dropout's tab, straddling the rotor.*

The dropouts sit 135 mm apart inside, the motor axle's width. Any stay tube that reaches inside a dropout's inner face is ground away so the hub fits. The caliper tab's two holes are drilled with the caliper and rotor in place (step 12).

**Check before moving on.** On a 135 mm dummy axle, the two slots line up and the plates are parallel.

#### 3.1.5 Small welded parts

![Figure 10. Joint 3: rear end of the right rail](05-build-plan/joint-03.png)

*Figure 10. The rail's end cap carries the upper stay; the tension lug beside it carries the bolt that pulls the rear roller's axle back along its slot. The drag screw is on this rail only.*

![Figure 11. Making sketch of the small welded parts](../cad/drawings/SGN-DWG-105.png)

*Figure 11. End cap, tension lug, kickstand plate, cradle tabs and controller plate (SGN-DWG-105).*

**What they are and what they are made from.** Mild steel plate and flat bar:

- End caps (2): 60 x 30 x 3 mm, over the rails' rear ends.
- Tension lugs (2): 20 x 13 x 10 mm from 20 x 10 mm flat bar, with an 8.5 mm hole along the rail, 7 mm out from the rail; on each rail's outer wall, 2 to 12 mm from the rear end, centred 42 mm up.
- Kickstand plate: 50 x 36 x 4 mm, on the left rail's outer wall, 225 to 275 mm from the rear end, 2 mm up; drilled to suit the kickstand bought.
- Cradle tabs (2): 40 mm lengths of 30 x 12 mm flat bar, one face filed to a 22 mm radius to sit on the down tube, the top face 10 mm above the tube; drilled 5 mm and tapped M6. On the down tube's rider side, 240 mm apart, the lower one 182 mm up the tube from its foot.
- Controller plate: 160 x 50 x 3 mm, on the left side of the down tube from 20 to 180 mm up the tube, with four holes to suit the controller bought.

**How to make them.** Saw, file and drill each from the sizes above. Grind every weld on a face that another part sits on.

**Check before moving on.** Each lug's hole lines up with the rail's slot centre (42 mm up).

#### 3.1.6 Head tube

A bought steel head tube, 50 x 3 mm and 150 mm long, machined at both ends for a ZS44 semi-integrated headset (cups pressed into the tube). It is welded in as it comes.

#### 3.1.7 Welding up the frame

![Figure 12. Weld-up sketch of the main frame](../cad/drawings/SGN-DWG-106.png)

*Figure 12. Main frame weld-up sketch (SGN-DWG-106).*

**How to make it.** Weld on a flat table, tacking everything first and welding in short runs, alternating sides, to limit distortion.

1. Set the rails on edge, parallel, 440 mm apart inside, outer walls out. Tack the cross members under them and the nose beam across their front ends. Check the diagonals agree within 2 mm, then weld.
2. Hold the head tube in a jig at 70 degrees from the ground plane, on the centre line, its bottom end 1410 mm ahead of the rails' rear ends and 470 mm above the rails' underside (640 mm above the ground).
3. Fit and weld the down tube between the nose beam and the head tube.
4. Set the dropouts on a 135 mm dummy axle, 270 mm behind the rails' rear ends and 77 mm above the rails' underside, square to the centre line. Fit and weld the four stays.
5. Weld on the end caps, tension lugs, kickstand plate, cradle tabs, controller plate and the drag screw nut.
6. Clean, prime and paint; keep paint off the head tube's bores and the faces where the dropouts meet the hub.

**Check before moving on.** Rails flat and parallel within 2 mm; head tube on the centre line within 1 mm; the dummy axle square to the centre line within 1 mm over its length.

### 3.2 Idler carrier bars (make 2)

![Figure 13. Joint 4: idler roller in the carrier bar](05-build-plan/joint-04.png)

*Figure 13. Cut across the deck: the idler's spring axle clips into the carrier bar, which is screwed to the rail; the belt runs on the idler; the side board sits on its spacer above.*

![Figure 14. Making sketch of the idler carrier bar](../cad/drawings/SGN-DWG-107.png)

*Figure 14. Idler carrier bar making sketch (SGN-DWG-107).*

**What it is and what it is made from.** The flat bar inside each rail that carries the ends of the 14 idler rollers under the belt. Aluminium flat bar 50 x 3 mm, 970 mm long.

**How to make it.**

1. Cut two 970 mm lengths. Clamp them together and drill both at once so every hole matches.
2. Idler holes: fourteen, the first 30 mm from the rear end and then every 70 mm, 40 mm up from the bottom edge. Size them to the rollers' spring axles: 8.2 mm for 8 mm round axles, or a matching hex hole for hex axles.
3. Screw holes: four 6.5 mm holes at 40, 340, 640 and 930 mm, 13 mm up.

**How it fits the parts next to it.** It sits flat on the rail's inside wall, bottom edge 12 mm above the rail's underside, rear end 90 mm from the rail's rear end, held by four M6 button-head screws into the rivet nuts. The idlers' tops are then 237 mm above the ground, just under the belt.

**Check before moving on.** The two bars are parallel and 434 mm apart inside.

### 3.3 Belt, end rollers and idler rollers (bought, from a walking-pad treadmill)

**What to buy.** A used walking-pad treadmill with a belt at least 400 mm wide, or new parts to the same specification: a 400 mm belt loop about 2.2 m round; two 50 mm crowned end rollers about 420 mm long with 6203 size bearings on fixed 17 mm axles; 14 gravity conveyor rollers 30 mm across and 410 mm long with 8 mm spring axles.

**What to do to them.**

1. Front roller: glue a ring of 8 magnets, 24 to 44 mm across, to its left end face, alternate poles out, with epoxy. Drill and tap its axle ends M10 if they are not already.
2. Rear roller: press out the bearing at its right end and press in a one-way bearing of the same size (CSK17 class, 17 x 40 x 12 mm), so the roller turns freely when the belt moves rearward and locks when it would move forward. Cross-drill and tap each axle end M8, 6 mm in from the end, along the vehicle.
3. Make four spacer washers, 22 mm across, to fill the 10 mm between each roller end and the rail.

**How they fit the parts next to them.**

![Figure 15. Joint 5: front roller, left end, with the speed sensor](05-build-plan/joint-05.png)

*Figure 15. The front axle is held by an M10 bolt through the rail and its crush tube; the magnet ring on the roller end passes 1.5 mm from the sensor.*

The front roller's axle sits between the rails' inside walls on its spacers and is held by an M10 bolt through each rail. The rear roller's axle runs through the rails' slots and out 12 mm each side, where the M8 tension bolts from the lugs screw into it (Figure 10). The belt loops round both rollers; the idlers sit inside the loop.

**Check before moving on.** The rear roller spins freely one way and locks the other; the front roller spins freely; the magnets are all flush.

### 3.4 Belt drag screw (bought)

![Figure 16. Joint 6: the drag screw](05-build-plan/joint-06.png)

*Figure 16. Cut through the drag screw: its felt tip presses on the rear roller's right end face, 20 mm below the axle.*

**What to buy.** An M8 x 60 mm knurled thumb screw with a 12 mm felt pad glued to its tip, and an M8 lock nut.

**How it fits the parts next to it.** It screws through the nut on the right rail and the rail's two walls; its felt tip presses on the rear roller's end face. Screwing it in adds belt drag, up to about 8 N at the belt; backed off, it adds none. The lock nut holds the setting.

**Check before moving on.** With the screw backed off, the belt pulls by hand with no rubbing.

### 3.5 Sensor bracket

![Figure 17. Making sketch of the sensor bracket](../cad/drawings/SGN-DWG-108.png)

*Figure 17. Hall sensor bracket making sketch (SGN-DWG-108).*

**What it is and what it is made from.** A small plate that holds the belt speed sensor facing the magnet ring. Aluminium plate 2.5 mm, 20 x 16 mm.

**How to make it.** Cut the plate; drill two 3.2 mm holes, 2 mm from the short edges and 3 mm up from the bottom; glue or screw the Hall sensor to its face, centred 11 mm up, sensing face outward and 3 mm proud.

**How it fits the parts next to it.** On the left rail's inside wall, centred under the front axle, held by two M3 screws into the rivet nuts; the sensor faces the magnet ring 18 mm below the axle (Figure 15).

**Check before moving on.** Turning the roller by hand gives 8 pulses per turn on a meter or the sensor's light.

### 3.6 Steering column

![Figure 18. Making sketch of the steering column](../cad/drawings/SGN-DWG-109.png)

*Figure 18. Steering column making sketch (SGN-DWG-109), drawn along the steering axis.*

**What it is and what it is made from.** The welded column that clamps the fork's steerer above the headset and carries the handlebar at 1.23 m. Steel tube in four stock sizes that slide inside each other: 33.7 x 2.3 mm (sleeve), 38 x 2 mm (column), 30 x 2 mm (stem) and 26.9 x 2.3 mm (bar clamp).

**How to make it.**

1. Sleeve: cut 80 mm of 33.7 x 2.3 mm tube (bore 29.1 mm, a slip fit on the 28.6 mm steerer). Saw a 3 mm slot 50 mm up from its bottom at the back. Weld two 13 x 6 x 30 mm lugs either side of the slot; drill both 6.5 mm and tap the far one M6.
2. Column: cut 441 mm of 38 x 2 mm tube. Slide it 30 mm over the top of the sleeve and weld all round. Weld a 3 mm cap plate on its top.
3. Stem: cut 53 mm of 30 x 2 mm tube; fish-mouth one end to the column. Weld it to the back of the column, level, its centre 20 mm below the column top.
4. Bar clamp: cut 40 mm of 26.9 x 2.3 mm tube (bore 22.3 mm). Weld it crosswise on the stem's free end. Slot it underneath and add two lugs and an M6 bolt as for the sleeve.

![Figure 19. Joint 8: head tube, headset and column clamp](05-build-plan/joint-08.png)

*Figure 19. Cut on the centre line: the headset sits in the head tube, the column's sleeve sits on the headset's top cover and clamps the steerer. The down tube joins the head tube's side.*

![Figure 20. Joint 9: stem and bar clamp](05-build-plan/joint-09.png)

*Figure 20. The bar clamp on the stem's end holds the handlebar; the display clamps beside it.*

**How it fits the parts next to it.** The sleeve sits on the headset's top cover and clamps the steerer with its two bolts (Figure 19); the bar clamp holds the 22.2 mm handlebar (Figure 20).

**Check before moving on.** On a straight 28.6 mm bar, column and bar are in line within 1 mm over 400 mm, and the stem is square to the column.

### 3.7 Receiver cradle

![Figure 21. Making sketch of the receiver cradle](../cad/drawings/SGN-DWG-110.png)

*Figure 21. Receiver cradle making sketch (SGN-DWG-110).*

**What it is and what it is made from.** The SwapCell receiver to latch class V1: a folded steel channel that the pack slides into, an end stop carrying the pack's connector, and an over-centre lever that presses the pack onto it. Steel sheet 3 mm, plate 12 mm, flat bar 30 x 8 mm.

**How to make it.**

1. Channel: cut one 3 mm blank 370 mm long and fold it to a base 98 mm wide with 60 mm walls, so it is 92 mm wide inside (1 mm clearance each side of the pack). Leave the last 45 mm of each wall at the upper end 40 mm taller (the ears).
2. End stop: cut 12 mm plate to 92 x 70 mm and weld it across the lower end, 15 mm in from the channel's end. Mount the pack's receptacle on it on its floating mount.
3. Lever: a 127 mm length of 30 x 8 mm bar on an 8 mm pin through the ears, with a pad block 40 x 10 x 58 mm welded under it that presses the pack's handle end. Set the over-centre point so it closes with 50 N or less at its end and holds 330 N or more on the pack, with a detent.
4. Base: two 6.5 mm holes, 240 mm apart, to match the down tube's tabs.

**How it fits the parts next to it.**

![Figure 22. Joint 10: receiver cradle and pack](05-build-plan/joint-10.png)

*Figure 22. Cut on the centre line: the pack sits on the base against the end stop; the lever's pad presses its handle end.*

The base sits on the two tabs on the down tube, two M6 bolts. The pack slides down the channel onto the receptacle and the lever closes over its top.

**Check before moving on.** A SwapCell interface v0.3 envelope gauge slides in and out freely; the lever snaps over centre.

### 3.8 Heel guard

![Figure 23. Making sketch of the heel guard](../cad/drawings/SGN-DWG-111.png)

*Figure 23. Heel guard making sketch (SGN-DWG-111).*

**What it is and what it is made from.** The upright plate between the rear end of the belt and the rear tire. Aluminium sheet 2 mm, 5052 class.

**How to make it.**

1. Cut a blank 436 x 215 mm. Fold the bottom 25 mm forward at 90 degrees (the flange).
2. Flange: two 6.5 mm holes, 80 mm each side of centre, 13 mm from the upright.
3. Upright: two 4.2 mm holes 120 mm up, 20 mm each side of centre, for the fender's front tab.
4. Round the top corners to 10 mm; deburr all edges.

**How it fits the parts next to it.** It stands between the rails, 2 mm clear of each, its back face level with the rails' rear ends, 190 mm tall; the flange lies on the rear cross member, two M6 screws into the rivet nuts. The fender's front end is riveted to it (Figure 25).

**Check before moving on.** At least 20 mm from the belt where it turns round the rear roller.

### 3.9 Roller covers (a rear and a front)

![Figure 24. Making sketch of the roller covers](../cad/drawings/SGN-DWG-112.png)

*Figure 24. Roller covers making sketch (SGN-DWG-112).*

![Figure 25. Joint 12: heel guard, fender and rear cover](05-build-plan/joint-12.png)

*Figure 25. Cut on the centre line: the heel guard's flange on the rear cross member, the fender riveted to the heel guard, and the rear cover round the back of the rear roller.*

**What they are and what they are made from.** Curved guards over the belt where it turns round each end roller. Aluminium sheet 2 mm, 440 mm wide.

**How to make them.**

1. Rear cover: 129 mm of sheet rolled round an 80 mm bar to a half round, 41 mm mean radius.
2. Front cover: 73 mm of sheet rolled to the same radius (a 102 degree arc).
3. Bend a 15 mm tab out flat at each end of each cover; drill one 5.5 mm hole in each tab.

**How they fit the parts next to them.** The rear cover wraps the back of the rear roller; the front cover runs from straight under the front roller round to just above its axle at the front, covering the nip where the belt runs onto the roller. Each tab lies on a rail's inside wall, one M5 screw into a rivet nut set where the tab falls. Each cover is at least 14 mm from the belt.

**Check before moving on.** The belt turns by hand without touching either cover.

### 3.10 Toe guard

![Figure 26. Making sketch of the toe guard](../cad/drawings/SGN-DWG-113.png)

*Figure 26. Toe guard making sketch (SGN-DWG-113).*

**What it is and what it is made from.** The plate across the front end of the belt that stops the rider's toes. Aluminium sheet 2 mm.

**How to make it.**

1. Cut a blank 436 x 153 mm; cut an 80 mm wide notch, 25 mm deep, in the middle of one long edge.
2. Fold the 25 mm flanges either side of the notch by 110 degrees, so the guard leans back 20 degrees when the flanges lie flat.
3. Flanges: four 6.5 mm holes, 80 and 180 mm each side of centre, 12 mm from the fold. Round the top corners; deburr.

**How it fits the parts next to it.** The flanges lie on the nose beam's top, fold on its rear edge, notch round the down tube, four M6 screws into the rivet nuts (Figure 6). Its top edge is 120 mm above the beam, over the front end of the belt.

**Check before moving on.** At least 15 mm from the belt and 2 mm from the front cover.

### 3.11 Side boards (make 2) and spacers

![Figure 27. Making sketch of the side board](../cad/drawings/SGN-DWG-114.png)

*Figure 27. Side board making sketch (SGN-DWG-114).*

**What they are and what they are made from.** The flat strips over each rail that cover the belt edges and give a firm place to put a foot. HDPE sheet 6 mm; aluminium tube 12 x 2 mm for the spacers.

**How to make them.**

1. Cut two 1060 x 70 mm strips; round the corners to 10 mm and chamfer the inner top edge 2 mm.
2. Drill four 6.5 mm holes in each, 40 mm from the inner edge, at 30, 370, 710 and 1030 mm from the rear end.
3. Cut eight 13 mm lengths of 12 x 2 mm tube (the spacers).

**How they fit the parts next to them.** Each board sits on four spacers on the rail top, held by M6 x 25 mm button-head screws into the rail's rivet nuts (Figure 13). Its inner edge lies 5 mm over the belt edge and 3 mm above it; its rear end is 60 mm from the rail's rear end.

**Check before moving on.** A 2 mm feeler slides between board and belt along the whole length.

### 3.12 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

![Figure 28. Joint 11: front caliper on the fork's post mount](05-build-plan/joint-11.png)

*Figure 28. The front caliper bolts to the post mount behind the left fork leg, straddling the rotor.*

- **Fork and headset (line 7).** A 1 1/8 in threadless steel rigid fork with post-mount disc tabs, for 26 in wheels (axle to crown about 410 mm), 30 mm offset, 100 mm hub spacing, steerer at least 220 mm; a ZS44 semi-integrated headset. Cut the steerer so it ends 3 mm below the top of the column's sleeve.
- **Front wheel (line 7).** 20 in (ETRTO 406) with a 6-bolt disc hub, 100 mm spacing, tire 20 x 1.75 in and tube. From a donor 20 in bike, or new.
- **Rear wheel with hub motor (line 6).** A 48 V 250 W geared hub motor for a 20 in wheel, 135 mm axle width, 6-bolt rotor mount, laced into a 20 in rim with a 20 x 1.75 in tire; two torque arms to fit its axle flats.
- **Brakes (line 9).** Two mechanical disc calipers for 160 mm rotors (post mount), two 6-bolt 160 mm rotors, two levers with built-in motor cut-off switches, cables.
- **Controller and logic board (line 12).** A 48 V (to 54.6 V), 15 A sine-wave hub motor controller with brake-cut and speed-command inputs, in a case no larger than 150 x 70 x 40 mm; an ESP32 board with a CAN transceiver and a 60 V input buck converter. No firmware is written at this stage.
- **Controls (line 13).** Handlebar display for speed, level and charge; three-position level selector; key switch; magnetic lanyard stop switch with a wrist or belt clip; each with its own 22.2 mm bar clamp.
- **Handlebar and grips (line 8).** A straight 580 mm flat bar, 22.2 mm, steel or aluminium; grips 130 mm long.
- **Harness (line 15).** Waterproof keyed connectors, a 20 A blade fuse in a sealed holder, cable and two grommets, spiral wrap, cable ties.
- **Kickstand (line 16).** A side kickstand with a two-bolt plate, about 230 mm long, for 20 in wheels.
- **Fender (line 14).** A 20 in rear fender, 60 mm wide, with two stays and a front tab.
- **Fixings (lines 3, 14 and 16).** M6 rivet nuts (22), M3 rivet nuts (2), M5 rivet nuts (4); M6 button-head screws and washers; two M10 bolts for the front axle; two M8 x 60 mm tension bolts with lock nuts; four M6 bolts for the calipers.
- **SwapCell pack (line 11).** Built by the SwapCell project to interface v0.3; not part of this build's parts cost.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: kickstand onto the frame

![Step 1](05-build-plan/step-01.png)

Two bolts through the plate on the left rail, nyloc nuts; the leg folds back along the rail.

### Step 2: idler carrier bars into the rails

![Step 2](05-build-plan/step-02.png)

Four M6 button-head screws each, into the rivet nuts in the rails' inside walls.

### Step 3: belt between the rails, front roller into it

![Step 3](05-build-plan/step-03.png)

Lay the belt loop between the rails. Slide the front roller, with its spacers, into the loop's front end, line its axle up with the rails' holes, and fit an M10 bolt and washer through each rail into the axle. Tighten so the axle cannot turn.

### Step 4: rear roller into the belt and the rail slots

![Step 4](05-build-plan/step-04.png)

Slide the rear roller, with its spacers, into the loop's rear end; its axle ends drop into the slots in both rails. Fit an M8 tension bolt through each lug into the axle end, finger tight.

### Step 5: idler rollers into the belt loop

![Step 5](05-build-plan/step-05.png)

Seen from below. Push each idler in under the belt's top run and press its spring axles into a pair of holes in the carrier bars. Then tension the belt: turn both tension bolts evenly until the belt is held at about 500 N each side (it lifts about 10 mm with a 50 N pull at its middle), then centre its tracking by turning one bolt a quarter turn at a time. Lock the bolts with their nuts. **Hold point:** the belt turns by hand rearward and will not move forward.

### Step 6: drag screw and speed sensor

![Step 6, drag screw](05-build-plan/step-06.png)

Drag screw through the welded nut on the right rail until its felt just touches the rear roller's end, then back it off and fit the lock nut.

![Step 6, speed sensor](05-build-plan/step-06b.png)

Sensor bracket on the left rail's inside wall under the front axle, two M3 screws, the sensor facing the magnet ring; run its cable through the rail's front grommet.

### Step 7: fork and headset into the head tube

![Step 7](05-build-plan/step-07.png)

Press the headset cups into the head tube, fit the crown race on the fork, grease the bearings, and slide the fork up through the head tube. Fit the top cover.

### Step 8: steering column onto the steerer

![Step 8](05-build-plan/step-08.png)

Set the headset preload first with a temporary stem or a steerer clamp collar, then remove it. Slide the column's sleeve down onto the top cover, line the bar clamp up square to the fork, and tighten the two M6 clamp bolts. Check the steering turns freely with no play.

### Step 9: handlebar, grips, levers and controls

![Step 9](05-build-plan/step-09.png)

Bar into the clamp, centred, two M6 bolts. Then the grips, the brake levers inboard of them, the display on the right of the clamp, the selector and key switch on the left, and the lanyard switch beside the display.

### Step 10: front wheel, rotor and caliper

![Step 10](05-build-plan/step-10.png)

Bolt the rotor to the hub (six bolts, threadlocker). Fit the wheel into the fork. Bolt the caliper to the post mount, centred on the rotor; connect the left lever's cable.

### Step 11: rear wheel with hub motor and torque arms

![Step 11](05-build-plan/step-11.png)

Bolt the rotor to the motor. Lift the wheel up into the dropout slots, motor cable on the left. Fit the torque arms on the outside of the dropouts with their M6 bolts, then the axle nuts to the motor maker's torque. **Hold point:** the torque arms bear on the axle flats on both sides.

### Step 12: rear caliper

![Step 12](05-build-plan/step-12.png)

Seen from behind and to the left, close up. Hold the caliper on the left dropout tab, centred on the rotor; mark and drill the two 6.5 mm holes, then bolt it on and connect the right lever's cable.

### Step 13: controller and wiring harness

![Step 13](05-build-plan/step-13.png)

Controller on its plate, four bolts. Run the harness as in Figure 29: from the controller down to the nose beam, through the left rail between its grommets to the rear, and along the left upper stay to the motor; and up the left side of the down tube and the column to the handlebar, with a loose loop at the head tube so the bar turns 45 degrees each way. Fuse out.

![Figure 29. Block-level wiring](05-build-plan/wiring.png)

*Figure 29. Block-level wiring with wire sizes. No circuit board is laid out; bought modules are wired together.*

Wire it like this, with crimped terminals or ferrules on every end:

1. Cradle receptacle to the fuse holder and on to the controller's battery input: 2.5 mm² (14 AWG).
2. Fuse output to the logic board's buck converter input: 0.5 mm² (20 AWG).
3. Receptacle INTERLOCK and SGND pins through the key switch and the 10 kΩ ±1 % coding resistor in series: 0.25 mm² (24 AWG).
4. Receptacle CAN pins to the logic board's CAN transceiver: 0.25 mm², twisted pair.
5. Brake lever switches and the lanyard switch to the controller's brake-cut input, and also to two logic board inputs: 0.25 mm².
6. Belt speed sensor, display and level selector to the logic board: 0.25 mm².
7. Logic board's speed command output to the controller's speed input: 0.25 mm².
8. Motor cable to the controller, through its keyed connector.

### Step 14: receiver cradle onto the down tube

![Step 14](05-build-plan/step-14.png)

Two M6 bolts into the tabs. Plug the receptacle's lead into the harness.

### Step 15: roller covers and heel guard

![Step 15](05-build-plan/step-15.png)

Cover tabs on the rails' inside walls, one M5 screw each. Heel guard flange on the rear cross member, two M6 screws.

### Step 16: fender and toe guard

![Step 16](05-build-plan/step-16.png)

Fender stays to the dropouts, front tab riveted to the heel guard with two 4 mm rivets. Toe guard flanges on the nose beam, four M6 screws.

### Step 17: side boards

![Step 17](05-build-plan/step-17.png)

Each board on its four spacers, M6 x 25 mm screws into the rail tops.

### Step 18: SwapCell pack

![Step 18](05-build-plan/step-18.png)

Only after safety stops S1 to S6. Key off. Slide the pack down the cradle onto its receptacle and close the lever over its handle end until it snaps over centre.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of SGN-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Belt direction and drag | R1, R7 | Pull the belt by hand both ways; spring balance at 5 km/h equivalent push with the drag screw off and fully in | Runs rearward only; 22 to 30 N push with 80 kg on the deck (measured at TRL 4) |
| Belt tension and tracking | R1 | Turn the belt 20 turns by hand | Stays within 5 mm of centre; no slip on the rear roller when braced |
| Step-off height and side boards | R8 | Tape measure; feeler | Belt top 240 mm or less above the floor; 2 mm or more under each board |
| Steering | R10 | Turn the bar to 45 degrees each way | Nothing touches; harness loop not tight |
| Brakes | R7 | Squeeze each lever with the wheels lifted | Each wheel locks; the motor cut-off switch opens on each lever |
| Wake and sleep | R11 | Pack in, key on, then key off (fuse in, wheels lifted) | Pack wakes on key on; output off within 1 ms of key off |
| Motor only while walking | R2 | Wheels lifted; turn the belt by hand, stop it; pull a brake lever; pull the lanyard | Motor runs only while the belt turns above 1.5 km/h; stops within 0.5 s of each stop |
| Speed limit | R3 | Wheels lifted, belt turned fast by hand | Assist cut at 25 km/h (15 km/h in beginner mode) on the display |
| Pack retention | R13 | Lever force with a spring balance; pull on the pack | Lever closes with 50 N or less; the pack does not move |
| Guards | R9 | Reach gauge to ISO 13857 at both belt ends and the rear tire | No finger or toe reaches a nip |
| Size and mass | R10 | Tape measure; scale | 2.4 m or less long, 0.65 m or less wide, 40 kg or less with the pack |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the frame is welded.** Welding screen, gloves, mask and ventilation in place; galvanising and paint ground off; fire extinguisher at hand.
- **S2. Before anyone stands on the belt.** All frame welds inspected with no cracks; every axle bolt and tension bolt tight with its lock nut; side boards, heel guard, toe guard and covers fitted; both brakes work; the kickstand holds the vehicle upright.
- **S3. Before the pack comes into the workshop.** Pack charged only in a SwapCell dock, never on the vehicle; a non-combustible place to stand the vehicle; a fire extinguisher for electrical fires within reach.
- **S4. Before the fuse goes in.** With the pack out, the harness checked end to end; the receptacle's power pins read open to the frame; the key switch opens the INTERLOCK loop; every connector seated.
- **S5. Before the motor is powered.** Rear wheel lifted clear of the floor on a stand; lanyard clipped to the tester; both brake levers cut the motor; fingers and clothing clear of the belt ends and the rear tire.
- **S6. Before the pack goes in.** S4 and S5 done; the cradle lever snaps over centre; key off.
- **S7. Before the first ride (TRL 4, outside this plan).** All first checks passed; helmet and a closed, flat, private area; the legal category confirmed with the Dutch vehicle authority (RDW) before any road use (first country decided by Amish, 2026-10-02).

## 7. Tools, skills and workspace

**Tools.** Bandsaw or hacksaw and a metal-cutting chop saw; bench drill with a vice; drills 3 to 17 mm and a step drill; M3, M6 and M8 taps; rivet nut tool for M3, M5 and M6; angle grinder with cutting and flap discs; files including a half round for fish-mouths; MIG or stick welder for 2 to 6 mm mild steel; a flat welding table with clamps and a simple jig for the head tube angle; sheet metal folder or two lengths of angle in a vice for 2 mm aluminium up to 440 mm wide; a 80 mm bar for rolling the covers; jigsaw for HDPE; headset press (or a threaded rod and washers) and a crown race setter; bearing press or a vice with sockets for the one-way bearing; spoke and cone spanners as needed; torque wrench 5 to 40 N·m; multimeter; spring balance to 100 N; tape measure, square, protractor, calipers.

**Skills.** Basic metalwork and steel welding (a local welder can weld the frame from the cut pieces); bicycle mechanics (headset, disc brakes, wheel fitting); crimping and simple wiring. Every circuit is below 60 V DC; no mains wiring is part of this build.

**Workspace.** A welding area apart from the assembly bench; a bench at least 2.5 m long or two trestles for the frame; a stand that holds the rear wheel off the floor; the safe pack area of S3.

**Personal protective equipment.** Welding helmet, gloves and jacket; safety glasses for cutting, drilling and grinding; hearing protection when grinding and sawing; cut-resistant gloves for sheet; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/SGN-DWG-101` to `SGN-DWG-114`.
- General arrangement: `cad/drawings/SGN-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (SGN-CAL-001 v0.3) and `docs/04-calcs/sizing.py`.
- Bill of materials: `bom/bom.csv` and `bom/bom-notes.md`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (SGN-DDR-003), with SGN-DDR-001 and SGN-DDR-002; the register `docs/06-design-decisions.md` (SGN-DEC-001).
- Requirements: `docs/03-requirements.md` (SGN-REQ-001 v0.6).
