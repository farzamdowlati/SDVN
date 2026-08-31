# 44 — Related Work: Controller Placement & Mobility-Aware Variants (the boundary we must fence)

Status: complete · Purpose: define where CPP ends and our LB problem begins —
the #1 "how is this different from placement?" examiner question answered here.

## 1. Scope
CPP in SDN/SDVN — static, dynamic, mobility-aware, DRL-driven — as the
ADJACENT field. We do not place controllers; we assign switches to
controllers. But the boundary papers must be cited or the defense asks.

## 2. Findings

**A. Static CPP canon.** Huang et al. arXiv:1902.09451 (V, from node 10):
placement objective already includes controller *workload distribution* +
delay trade-off — GA+GD, NP-hard framing. Kumari survey 1905.04649 (V-abs):
the taxonomy (assign vs place vs migrate) we borrow below.

**B. Dynamic/vehicular CPP — our direct neighbors.**
- Toufga et al. 2020 (Sensors, S-snippet, cited ≈56; HAL mirror), *Towards
  Dynamic Controller Placement in SDVN*: controllers themselves relocate
  between RSU/cloud sites following vehicle-density clusters — placement on
  a coarse timescale (min), our re-association on a fine one (s). Distinct
  actuator, distinct timescale — the sentence we need.
- MobiPlace (S): mobility-aware CPP for SDVN; same category (where to put
  the boxes), complementary not competing — could *feed* our state features.
- Xu 2023 DRL load-aware dynamic placement (S, cited 27) and Li 2024 JPDC
  DRL placement (S, cited 20): DRL used for *placement* decisions — proves
  DRL-in-SDVN-control-plane is an accepted methodological frame (precedent
  for our MDP formulation style), again different action variable.
- Antonopoulos 2026 SDN vehicular platform (S): mobility-aware SDN testbed —
  infrastructure reference; cites RSU-switch architecture similar to ours.
- MOTA-SVB 2026 (S, seen in 42): trajectory-aware + BFT placement — 2026
  liveness check: placement+mobility is STILL the active vehicular-CP
  subfield, and none of these papers balances *within* fixed domains by
  migrating switches with a recurrent agent.

**C. The taxonomy that fences us in (stolen from the CPP literature):**
three coupled decisions — (1) how many/where controllers = placement (B),
(2) which switch belongs to which controller = association/migration (our
paper), (3) which controller is master per switch = roles (→45). Papers
combining (1)+(2): few (Huang's GA+GD jointly optimizes; fractional
migration AL-Tam 45-C does (2)+(3)). We own (2) with learning.

## 3. Critical reading
- Dynamic-CPP papers change domains every ~minutes with heavy re-sync;
  they *implicitly admit* a fine-grained balancing layer must exist between
  relocations — nobody builds it ⇒ narrative opening for our thesis
  ("placement moves the map; we move the borders' contents").
- DRL-placement papers share our weaknesses: synthetic demand, tiny
  controller counts; none evaluates under handover-storm bursts.

## 4. Relation to thesis
Related-work section will present CPP as a sibling problem with an explicit
comparison table (actuator / timescale / state / objective / learning?) —
draft that table now, finalize in 50. Placement costs are a possible
future-work coupling (joint placement+association); record as scope limit.

## 5. Sources
| # | Source | Tier |
|---|--------|------|
| 1 | Huang 1902.09451; Kumari 1905.04649 | V |
| 2 | Toufga 2020; MobiPlace; Xu 2023; Li 2024; Antonopoulos 2026; MOTA-SVB 2026 | S |
| 3 | dSDiVN mobile controllers (node 10) | V |

## 6. Open threads
- Read Toufga full text (HAL PDF is open) → extract their timescale numbers for the comparison table.
- Check if any paper = "joint dynamic placement + switch migration" (searched once, negative — recheck in 50).