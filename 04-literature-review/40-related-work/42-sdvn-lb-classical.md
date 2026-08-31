# 42 — Related Work: SDVN Control-Plane LB *Without* Learning (★ the title collision)

Status: complete · Full-text V (PDF read: Babbar et al., CMC 67(1), DOI 10.32604/cmc.2021.014627, 16 pp.)

## 1. Scope
The paper whose title overlaps ours most: *Load Balancing Algorithm for
Migrating Switches in Software-Defined Vehicular Networks* (CMC 2021).
Plus its cited SDVN-adjacent family. This file is a case study as much as a
review node.

## 2. What they actually do (V, full text)
- **Load model:** per-controller load = count of packet-in requests from its
  switches in window Z (Eq. 2); latency = mean(response_time − arrival) per
  packet-in (Eqs. 1, 3). Latency doubles as the *imbalance detector*.
- **Algorithm:** fixed threshold τ on average latency; controllers split into
  SRC_C (over τ) / DST_C (≤ τ) every 10 s (10 s chosen because Ryu's default
  flow timeout is 10 s — implementation-driven, not traffic-driven); migrate
  switches from overloaded to least-loaded destination; multiple overloaded
  controllers resolved in one pass; goal = hit balance with *fewest
  migrations* ("switch-V" variant in their figures).
- **Evaluation:** Mininet + Ryu, OpenFlow 1.3, 3 controllers, 7 OVS, 15
  hosts, iperf TCP/UDP load injection, 250 "users", 1000 s runs.
  Baselines: DHA, SMDM (Wang'17 decision-making), OCLB, TPLB.
  Claims: ≈25% latency reduction; fewest switches migrated; stable by 150 s.
- **Future work they name:** migration cost and switch–controller distance.

## 3. The critical finding (why this HELPS us — and hurts them)
**The paper is called SDVN but simulates no vehicles.** Keyword census of the
full text: "traffic" 0× in system description (only via iperf load),
"vehicle" 2× (intro framing + references), SUMO 0×, ns-3 0×, no mobility
model, no handover events, no road topology. The imbalance they balance is
**artificially injected packet-in load on a static topology** — i.e. plain
multi-controller SDN LB with a latency threshold.
Consequences:
1. Our differentiation obligation *shrinks and sharpens*: they neither model
   mobility nor learn; we must do **both**, and our claim becomes: *the first
   control-plane LB for SDVN evaluated under genuine vehicle-mobility-driven
   load dynamics, by a recurrent DQN.*
2. Their baseline list (DHA/SMDM/OCLB/TPLB) is a ready-made reactive-
   threshold comparison set for our evaluation (S-tier until each read).
3. **Warning-by-example:** a paper can publish "SDVN" in the title with zero
   SDVN in the evaluation. Our defense: mobility traces (SUMO/Veins) are
   non-negotiable in the methodology — a reviewer WILL ask "where are the
   vehicles?" and we will have the answer theirs lacks.
4. They conflate load with latency (load=count, trigger=latency) — a latency
   spike can also come from distance/CPU contention; our formal statement
   (node 20) keeps them as separate terms.

## 4. Surrounding family (S-tier, from their survey + our searches)
- Belgaum et al. 2020, IEEE Access, *Systematic review of LB techniques in SDN* (their ref [6]) — taxonomy source to harvest (→45/50).
- Zhang et al. 2020, IEEE TVT, *Task offloading in vehicular edge computing: a load-balancing solution* ([4]) — **data-plane task LB in vehicles**, different problem; good contrast paragraph material.
- MOTA-SVB 2026 (Springer, S): trajectory-aware controller placement + BFT — nearest 2026 neighbor of SDVN+placement; recheck gap v3 against it.
- LAERS 2026 (ScienceDirect, S): load-aware routing in SDVN — again data-plane; watch "load balancing" polysemy when writing related work.
- Kazemiesfeh 2025 (arXiv:2504.17046, cited 27, V-abstract-level): multi-level *thresholds* controller LB, general SDN — confirms threshold family is still the live baseline in 2025 ⇒ our reactive-baseline choice is current, not a strawman.

## 5. Relation to thesis
- Cite as **the closest prior work + the cautionary example**. One sentence
  for the defense: "the nearest published SDVN controller-LB scheme is
  threshold-based, memoryless, and evaluated on a static topology without
  mobility [CMC'21]; our work supplies all three missing ingredients."
- Their algorithm = a *strong candidate baseline #2* (after least-loaded)
  because reimplementing a published latency-threshold SDVN scheme is
  directly comparable and reviewers like named-lineage baselines.

## 6. Sources
| # | Source | Tier |
|---|--------|------|
| 1 | Babbar et al., CMC 2021 (full PDF read via pymupdf; PDF archived /tmp→ should mirror into repo) | V |
| 2 | Belgaum'20 IEEE Access survey | U→S (from their ref list) |
| 3 | Zhang'20 IEEE TVT offloading | U |
| 4 | MOTA-SVB'26; LAERS'26; Kazemiesfeh'25 | S |

## 7. Open threads
- Archive the PDF into `01-literature/pdfs/` (open-access CC-BY 4.0 — safe to store, do not redistribute off-repo beyond license) — done this commit if size allows; gitignore allows since repo is private & file small.
- Locate & read DHA/SMDM/OCLB/TPLB originals → 45 (baseline mechanisms) + 50 (metric table).
- Re-run gap check against 2026 papers (MOTA-SVB, LAERS) in node 50 with one fresh query.