# BOM notes

Every line in `bom/bom.csv` is priced (TRL 3). Prices are estimates for one-off purchase in 2026 US dollars, with a supplier or supplier type; they are not quotes. Item numbers 1 to 15 match the exploded view (`media/exploded.png`), the components table in SGN-PRC-001 and the model in `cad/src/model.py`; item 16 (hardware, kickstand and consumables) has no callout. The totals below are printed by `docs/04-calcs/sizing.py` (SGN-CAL-001), which reads this BOM and the budget in `project.yaml`.

**The SwapCell pack (item 11) is not included in the total.** By Amish's 2026-09-25 portfolio rule a shared SwapCell pack is priced once, in the SwapCell BOM (about $414 in prototype parts), and excluded from each dependent kit budget. It is listed at $0.00 so the numbering matches the exploded view.

| Group | Items | Cost |
| --- | --- | --- |
| Frame, deck and belt | 1 to 5 | $246 |
| Wheels, motor, steering and brakes | 6 to 9 | $262 |
| SwapCell receiver (class V1), electrics and guards | 10, 12 to 15 | $167 |
| Hardware, kickstand and consumables | 16 | $38 |
| **StepGen total, pack excluded** | 1 to 10, 12 to 16 | **$713** |
| SwapCell pack (not in total) | 11 | about $414, SwapCell BOM |

Against the $650 budget Amish set on 2026-09-25, the total is **$63 (10 %) over**, so requirement R12 is not met. Changes since TRL 2 ($630): the receiver cradle now meets SwapCell latch class V1 with an over-centre lever, a floating receptacle, the 10 kΩ INTERLOCK coding resistor and a key switch (item 10, $22 to $55, and item 13); the motor is specified for a 20 in wheel and the wheel build is priced separately (item 6, $95 to $110); the fork has a 30 mm offset (item 7, $60 to $70); a kickstand is added (item 16).

Ways to close the gap, proposed, awaiting Amish (see `docs/REVIEW.md`):

- **Salvage route.** A used walking-pad treadmill for items 2 and 3 (about $40 instead of $145) and a donor 20 in bike for items 7 and 9 (about $50 instead of $120) bring the total to about $538. Recommended as the reference build path, with new parts as the fallback.
- **Raise the budget** to about $720 for an all-new-parts build.

The optional belt-roller generator (see SGN-PRC-001) is not in this BOM. It would add about $35 to $50 (a small BLDC motor, rectifier and boost stage) and is not in the first concept (decided by Amish, 2026-09-25).
