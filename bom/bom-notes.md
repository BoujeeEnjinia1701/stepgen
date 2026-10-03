# BOM notes

Every line in `bom/bom.csv` is priced (TRL 3). Prices are estimates for one-off purchase in 2026 US dollars, with a supplier or supplier type; they are not quotes. Item numbers 1 to 15 match the exploded view (`media/exploded.png`), the components table in SGN-PRC-001 and the model in `cad/src/model.py`; item 16 (hardware, kickstand and consumables) has no callout. The totals below are printed by `docs/04-calcs/sizing.py` (SGN-CAL-001), which reads this BOM and the budget in `project.yaml`.

**The SwapCell pack (item 11) is not included in the total.** By Amish's 2026-09-25 portfolio rule a shared SwapCell pack is priced once, in the SwapCell BOM (about $414 in prototype parts), and excluded from each dependent kit budget. It is listed at $0.00 so the numbering matches the exploded view.

| Group | Items | Cost (new parts) |
| --- | --- | --- |
| Frame, deck and belt | 1 to 5 | $264 |
| Wheels, motor, steering and brakes | 6 to 9 | $266 |
| SwapCell receiver (class V1), electrics and guards | 10, 12 to 15 | $178 |
| Hardware, kickstand and consumables | 16 | $42 |
| **StepGen total, all new parts, pack excluded** | 1 to 10, 12 to 16 | **$750** |
| **Reference build (salvage route), pack excluded** | items 2 and 3 from a walking pad, the front wheel and item 9 from a donor bike, fork and headset new | **$610** |
| SwapCell pack (not in total) | 11 | about $414, SwapCell BOM |

**Value engineering.** `budget_usd` ($650) is a hypothetical value-engineering target, not a limit (Amish, 2026-10-01). Value-engineering target: USD 650. Estimated cost of the constructable design: USD 610 on the reference build (USD 40 under the target); USD 750 with all new parts (USD 100 over the target).

**Reference build.** Amish decided on 2026-09-25 (SGN-DDR-002) to make the salvage route the reference build, with new parts as the fallback. A used walking-pad treadmill supplies items 2 and 3 (about $40 instead of $150) and a donor 20 in bike supplies the front wheel and the brakes (about $50 instead of $120 for items 7 and 9). The donor's 20 in fork is too short for StepGen's head tube (SGN-DDR-003), so the fork and headset are bought new (about $40). The salvage prices are estimates and depend on the local second-hand market.

Changes for construction (SGN-DDR-003, 2026-10-01): item 1 restated as a welded frame with a nose beam, two cross members under the rails, four stays, a bought machined ZS44 head tube and welded plates ($83 to $92); item 2 adds axle bolts and tension bolts ($95 to $97); item 3 has aluminium carrier bars and rivet nuts ($50 to $53); item 4 is a one-way bearing inside the rear roller and a drag screw ($20 to $15); item 5 adds a bracket ($6 to $7); item 7 is a 26 in size fork on the 20 in wheel; item 8 is a welded column that clamps the steerer and a straight 580 mm bar ($32 to $36); item 14 adds flanges, spacers and a bought fender ($32 to $42); item 15 adds grommets ($16 to $17); item 16 adds rivet nuts ($38 to $42).

Changes since TRL 2 ($630): the receiver cradle now meets SwapCell latch class V1 with an over-centre lever, a floating receptacle, the 10 kΩ INTERLOCK coding resistor and a key switch (item 10, $22 to $55, and item 13; the key switch was decided by Amish on 2026-09-25, SGN-DDR-002); the motor is specified for a 20 in wheel and the wheel build is priced separately (item 6, $95 to $110); the fork has a 30 mm offset (item 7, $60 to $70); a kickstand is added (item 16); the deck rails grow from 50 x 25 x 2 mm to 60 x 30 x 2 mm for weld fatigue (item 1, $75 to $83, SGN-DDR-002).

The optional belt-roller generator (see SGN-PRC-001) is not in this BOM. It would add about $35 to $50 (a small BLDC motor, rectifier and boost stage) and is not in the first concept (decided by Amish, 2026-09-25).

Rotor carriers (decision of 2026-10-02): the 28 laced spokes and the rotor carriers on the wheels are appearance only. When the wheel build is specified, the 6-bolt carrier on the rear hub (line 6) and on the front hub (line 7) is confirmed against the hub bought, together with the 160 mm rotors (line 9). No quantity or price changed.
