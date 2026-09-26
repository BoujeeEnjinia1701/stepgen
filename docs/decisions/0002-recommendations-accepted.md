---
doc_id: SGN-DDR-002
title: StepGen recommendations accepted
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
  change: Record Amish's 2026-09-25 acceptance of the TRL 3 review recommendations, what changed in the repo and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 5); items 6 and 7 remain proposed, awaiting Amish

## Context

The TRL 3 review note (`docs/REVIEW.md`, session "2026-09-25: TRL 3") listed seven items as "Proposed, awaiting Amish", and SGN-DDR-001 carried them as its open item 15. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item that had a recommendation is therefore decided as recommended. Items with no recommendation stay open. TRL 3 remains the hard stop; TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 3 session) and SGN-CAL-001 v0.1. Where several options were offered, the recommended option is the decision.

## Decision

*Table 1. Items decided on 2026-09-25. Each is "Decided by Amish, 2026-09-25: go with recommendation".*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 | Cost overrun (R12) | Option (a): keep `budget_usd` at $650 and make the salvage route (a used walking-pad treadmill for items 2 and 3, a donor 20 in bike for items 7 and 9) the reference build, with new parts as the fallback | `budget_usd` unchanged at $650. R12 in SGN-REQ-001 restated to apply to the reference build. `docs/04-calcs/sizing.py` now checks R12 on the reference build: **not met at $713 becomes met on paper at $546** (all-new fallback $721 after item 3). `bom/bom-notes.md` shows both totals |
| 2 | Belt length (R1 against R10) | Option (a): keep the 1.05 m roller pitch and 2.35 m length; revisit after co-design shows the riders' heights and pace | No geometry change. R1 stays at risk, now marked as held until co-design in SGN-REQ-001, SGN-PRC-001 and SGN-CAL-001 |
| 3 | Deck rails | Change from 50 x 25 x 2 mm to 60 x 30 x 2 mm RHS | `cad/src/model.py` (`rail_w` 25 to 30, `rail_h` 50 to 60), STEP and STL re-exported, SGN-DWG-001 to Rev P2, media regenerated. Weld stress range **37.6 to 25.5 MPa** (limit 38.8 MPa); static factor 2.0 to 3.0. Frame 11.4 to 12.5 kg; vehicle **34.0 to 35.0 kg**, **36.8 to 37.9 kg** with the pack (R10 margin 3.2 to 2.1 kg, still at risk). Hill power 233 to 235 W (R6 margin 7 to 6 %). BOM item 1 **$75 to $83** |
| 4 | Key switch in the INTERLOCK loop | Option (a): a key switch in series with the 10 kΩ coding resistor; off opens the loop and sleeps the pack, on wakes it; also a simple immobiliser; used at a standstill only | Already modelled and priced (BOM items 10 and 13); SGN-PRC-001 and SGN-CAL-001 now mark it as decided instead of proposed |
| 5 | Flag to the SwapCell project | Raise with SwapCell: v0.3 does not say whether a pack in legacy discharge moves to mode 2 when a heartbeat arrives | Listed under "Cross-repo actions" in `docs/REVIEW.md`. The SwapCell repo is not edited from here |

### Items that remain open

These had no recommendation and stay **Proposed, awaiting Amish**:

- **6. First user group.** Non-cycling adults, older adults or commuters (SGN-DDR-001 item 13).
- **7. First target country** for the legal category (SGN-DDR-001 item 14).

## Consequences

- SGN-PRB-001, SGN-PRC-001 and SGN-REQ-001 move from 0.4 to 0.5; SGN-CAL-001 moves from 0.1 to 0.2; SGN-DDR-001 moves from 0.1 to 0.2 to mark its item 15 as decided.
- Requirement status: R12 moves from not met to met on paper. No requirement is now not met. R1, R6 and R10 remain at risk; R9 and R13 remain not verifiable at TRL 3.
- The deck-rail weld fatigue concern in the TRL 3 review is closed on paper; it still needs a test at TRL 4.
- The salvage prices ($40 for a walking-pad treadmill, $50 for a donor bike) are estimates; R12 now depends on them.
- `trl` and `trl_target` stay at 3. No TRL 4 work (test article, test plan, build log, firmware) is started; it is on hold by Amish's instruction.
