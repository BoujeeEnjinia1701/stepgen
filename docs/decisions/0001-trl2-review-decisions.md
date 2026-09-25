---
doc_id: SGN-DDR-001
title: StepGen TRL 2 review decisions
project: StepGen
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review, the move to SwapCell interface v0.3 and the items that stay open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 12); items 13 to 15 remain proposed, awaiting Amish

## Context

The TRL 2 review note (`docs/REVIEW.md`, session "concept change to a walking-treadmill vehicle") listed nine items as "Proposed, awaiting Amish", most with a recommendation. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." In the same instruction he approved three additions to the SwapCell interface (a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles), a pricing rule for shared SwapCell packs, and a rule that community designs pick co-design partners per area later. He also confirmed the move of StepGen from the CleanTech area to Mobility and Logistics.

The concept change itself (a walking-treadmill vehicle instead of a stationary stepper generator) was decided by Amish on 2026-09-24 and is recorded in SGN-PRB-001, SGN-PRC-001 and the review note. It is not repeated here.

This record lists what the 2026-09-25 instruction decides, and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 session) and SGN-PRC-001 v0.3. They are not repeated here.

## Decision

*Table 1. Decided items. Each is "Decided by Amish, 2026-09-25: go with recommendation" unless the row says otherwise.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Form factor | Decided by Amish, 2026-09-25: go with recommendation. Two-wheel, long-wheelbase, bike type (about 2.35 m) so that a natural stride fits on the belt; the three-wheel tadpole version stays open until co-design shows whether non-cyclists can balance | SGN-PRC-001 v0.4, SGN-DWG-001 |
| 2 | Wheels | Decided by Amish, 2026-09-25: go with recommendation. 20 in (ETRTO 406) front and rear | SGN-PRC-001 v0.4, `bom/bom.csv` items 6 and 7 |
| 3 | Motor and speed class | Decided by Amish, 2026-09-25: go with recommendation. 250 W rated rear geared hub, assist cut at 25 km/h, 15 km/h beginner mode (EU pedelec limits) | SGN-REQ-001 R3 and R4 |
| 4 | Target range | Decided by Amish, 2026-09-25: go with recommendation. 30 km at 20 km/h on the flat on one SwapCell pack | SGN-REQ-001 R5 |
| 5 | Regeneration | Decided by Amish, 2026-09-25: go with recommendation. No roller generator in the first concept; keep a mounting point on the front roller. SwapCell v0.3 mode 4 now removes the interface gap, but the decision stands | SGN-PRC-001 v0.4 |
| 6 | Area | Decided by Amish, 2026-09-25: go with recommendation, and confirmed for this session. `area` moves from CleanTech to Mobility and Logistics, matching SunSpoke and WaterWalker | `project.yaml` |
| 7 | Budget | Decided by Amish, 2026-09-25: go with recommendation. `budget_usd` raised from $400 to $650, SwapCell pack excluded | `project.yaml`, SGN-REQ-001 R12 |
| 8 | Legal route | Decided by Amish, 2026-09-25: go with recommendation. Pick a first target country and confirm the vehicle's legal category there before any road use. Which country is not decided (item 14) | SGN-PRB-001 v0.4, SGN-REQ-001 |
| 9 | SwapCell interface | Decided by Amish, 2026-09-25 (cross-cutting): StepGen builds to SwapCell interface v0.3. It uses item W (10 kΩ coding resistor in the INTERLOCK loop, which wakes the pack), fits a receiver to item V (latch class V1: 1.72 kN pack latch proof, 330 N or more receiver preload) and does not use item C (charge-discharge mode) because no generator is fitted | SGN-REQ-001 R11 and R13, SGN-PRC-001 v0.4 |
| 10 | Shared pack pricing | Decided by Amish, 2026-09-25 (cross-cutting): the SwapCell pack is priced once, in the SwapCell BOM, and excluded from the StepGen budget | `bom/bom.csv` item 11, `bom/bom-notes.md` |
| 11 | Co-design partner | Decided by Amish, 2026-09-25 (cross-cutting): community designs pick co-design partners per area later. The partner stays open | SGN-PRB-001 v0.4 |
| 12 | Decision record | Decided by Amish, 2026-09-25: go with recommendation (TRL 2 suggestion). This record is SGN-DDR-001 | This file |

### Items that remain open

These items had no recommendation to accept, or arose at TRL 3, and stay **Proposed, awaiting Amish**:

- **13. First user group.** Non-cycling adults, older adults or commuters. No preference was stated, and the partner is left open by item 11.
- **14. First target country** for the legal classification (item 8 decides the route, not the country).
- **15. New TRL 3 items** from SGN-CAL-001, each with options and a recommendation in `docs/REVIEW.md` (session 2026-09-25: TRL 3): the cost overrun against the new $650 budget, belt length for tall riders, deck rail size for weld fatigue, and a key switch in the INTERLOCK loop.

## Consequences

- SGN-PRB-001, SGN-PRC-001 and SGN-REQ-001 move to version 0.4 (they were already at 0.3 from the 2026-09-25 concept change) and no longer mark items 1 to 12 as proposed.
- R12 now reads $650. The priced BOM is about $713, so R12 is **not met** (SGN-CAL-001); options are in the review note.
- R11 now cites SwapCell interface v0.3, and a new requirement R13 covers pack retention to latch class V1.
- TRL 3 is the hard stop. TRL 4 (a test article, lab tests and a build log) is on hold by Amish's instruction.
