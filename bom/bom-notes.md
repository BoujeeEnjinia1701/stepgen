# BOM notes

Every line in `bom/bom.csv` is priced (TRL 3). Prices are estimates for one-off purchase in 2026 US dollars, with a supplier or supplier type; they are not quotes. Item numbers 1 to 15 match the exploded view (`media/exploded.png`), the components table in SGN-PRC-001 and the model in `cad/src/model.py`; item 16 (hardware, kickstand and consumables) has no callout. The totals below are printed by `docs/04-calcs/sizing.py` (SGN-CAL-001), which reads this BOM and the budget in `project.yaml`.

**The SwapCell pack (item 11) is not included in the total.** By Amish's 2026-09-25 portfolio rule a shared SwapCell pack is priced once, in the SwapCell BOM (about $414 in prototype parts), and excluded from each dependent kit budget. It is listed at $0.00 so the numbering matches the exploded view.

| Group | Items | Cost (new parts) |
| --- | --- | --- |
| Frame, deck and belt | 1 to 5 | $254 |
| Wheels, motor, steering and brakes | 6 to 9 | $262 |
| SwapCell receiver (class V1), electrics and guards | 10, 12 to 15 | $167 |
| Hardware, kickstand and consumables | 16 | $38 |
| **StepGen total, all new parts, pack excluded** | 1 to 10, 12 to 16 | **$721** |
| **Reference build (salvage route), pack excluded** | as above, items 2, 3, 7 and 9 salvaged | **$546** |
| SwapCell pack (not in total) | 11 | about $414, SwapCell BOM |

**Reference build.** Amish decided on 2026-09-25 (SGN-DDR-002) to keep the $650 budget and make the salvage route the reference build, with new parts as the fallback. A used walking-pad treadmill supplies items 2 and 3 (about $40 instead of $145) and a donor 20 in bike supplies items 7 and 9 (about $50 instead of $120). The reference build is **$546, $104 under the $650 budget**, so requirement R12 is met on paper. The all-new-parts total of $721 is $71 (11 %) over and is reported, not held to R12. The salvage prices are estimates and depend on the local second-hand market.

Changes since TRL 2 ($630): the receiver cradle now meets SwapCell latch class V1 with an over-centre lever, a floating receptacle, the 10 kΩ INTERLOCK coding resistor and a key switch (item 10, $22 to $55, and item 13; the key switch was decided by Amish on 2026-09-25, SGN-DDR-002); the motor is specified for a 20 in wheel and the wheel build is priced separately (item 6, $95 to $110); the fork has a 30 mm offset (item 7, $60 to $70); a kickstand is added (item 16); the deck rails grow from 50 x 25 x 2 mm to 60 x 30 x 2 mm for weld fatigue (item 1, $75 to $83, SGN-DDR-002).

The optional belt-roller generator (see SGN-PRC-001) is not in this BOM. It would add about $35 to $50 (a small BLDC motor, rectifier and boost stage) and is not in the first concept (decided by Amish, 2026-09-25).
