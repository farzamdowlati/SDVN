# 50 — Synthesis: Taxonomy Matrix, Gap Statement v3, Baseline Shortlist

Status: complete (assembly node — no new searching beyond one final gap
re-check, 2 queries, 2026-08-31). Input: nodes 10–46.

## 1. The comparison matrix
Cell = does a paper cover it? (V/S tiers marked; blank ⇒ absent per that source)

| Paper | Domain | Plane/locus | Actuator | Memory | Learning | Mobility in eval |
|---|---|---|---|---|---|---|
| Li'21 2103.06579 (V) | SDN | ctrl-plane | migration triplets | ✗ (round load ratios) | DRL (value) | ✗ synthetic |
| EASM'17 1711.08659 (V) | SDN | ctrl-plane | switch migration | ✗ | ✗ heuristic | ✗ synthetic |
| CMC'21 Babbar (V-full) | **"SDVN"** | ctrl-plane | migration, latency-τ | ✗ | ✗ | **✗ (static Mininet)** |
| Zhong'22 (S) | SDN | ctrl-plane | dual-weight migration | partial (link predictor) | ✗ | ✗ |
| Kazemiesfeh'25 (S) | SDN | ctrl-plane | multi-τ migration | ✗ | ✗ | ✗ |
| Xu'23 / Li'24 JPDC (S) | SDN | ctrl-plane | **placement** | — | DRL | ✗ |
| Toufga'20 / MobiPlace (S) | **SDVN** | ctrl-plane | **placement (dynamic)** | ✗ | ✗ (densities) | ✓ density-driven |
| POSCAD'20 2008.01648 (V) | SDN | ctrl-plane | assoc + devolution | ✗ (theory w/ VOI) | ✗ online opt | ✗ |
| Owusu'25 2501.12829 (V) | SDN | **data-plane? (verify)** | routing LB | TFT history | DQN+forecast | ✗ |
| Hechmi'24 IEEE (S) | 6G | LB (unclass.) | ? | ? | DQN+LSTM | ? |
| O-RAN'26 2605.30630 (V) | 5G RAN | radio sched. | PRB | **✓ LSTM enc** | **Double DQN** | ✗ CTMC |
| Slicing'22 2208.03460 (V) | 5G RAN | radio sched. | slice alloc. | forecast-only | LSTM→DQN | ✓ (user mobility) |
| ARDDQN'24 (V) | UAV | path plan | movement | ✓ LSTM+attn | DDQN | ✓ (its own motion) |
| **OURS** | **SDVN** | **ctrl-plane** | **switch migration** | **✓ LSTM(DRQN)** | **Double+Duel DQN** | **✓ SUMO/Veins traces** |

Reading the table: the last row is the only one where every column in bold
simultaneously holds. Nearest neighbors each fail ≥2 axes — CMC'21 (no
mobility, no learning), 2605.30630 (wrong locus), 2103.06579 (no memory,
no mobility), POSCAD (no learning).

## 2. Gap statement v3 (final, proposal-grade)
> Control-plane load balancing via switch migration is established for
> general SDN — with heuristics (EASM, threshold schemes), online
> optimization with proven value-of-foresight (POSCAD), and memoryless RL
> (2103.06579). Its vehicular counterpart is published but notional: the
> closest SDVN-titled scheme evaluates on a static testbed with no mobility
> model (CMC'21, full-text verified). Meanwhile, recurrent DQN agents
> (LSTM-encoded Double DQN) have become the credible answer to temporally
> correlated, partially observable network control (O-RAN 2605.30630; DRQN
> lineage). **What no identified work provides is a recurrent, learned
> controller load balancer for a distributed SDVN control plane under real
> vehicle-mobility-driven load dynamics — predicting mobility-induced
> packet-in surges and acting with protocol-accurate, migration-cost-aware,
> stability-constrained switch re-association.**

## 3. Residual risks (what could still kill the gap)
1. **Temporal-DQN LB (PMC 2024, S)** — title collides with our framing;
   likely data/server-plane. Classify before proposal defense. [HIGH]
2. **Sadhana'25 online-sequential SDN CP LB (S)** — memoryless but "online";
   confirm it is not recurrent. [MED]
3. **Hechmi'24** internals (encoder vs pipeline) unknown until full read;
   if it is recurrent+control-plane, our §2 wording survives (still not
   vehicular) but the "DQN+LSTM in CP" phrase must gain a qualifier. [MED]
4. **Liu'23 attention-LSTM controller-load *prediction*** (node 46 priority):
   if it includes an actuator, reposition contribution as "closing the loop
   in SDVN". [MED — likely low, prediction-only venues]
5. arXiv-only sweep cannot see IEEE paywalled full texts; campus pass is the
   standing mitigation (03-open-questions #7). [STRUCTURAL]

## 4. Baseline shortlist for the evaluation chapter (from 41/45)
| Rank | Baseline | Why |
|---|---|---|
| B0 | least-loaded (periodic) | folklore floor, every paper compares it |
| B1 | latency-threshold (CMC'21 reimpl.) | the *published SDVN* scheme — named-lineage credibility |
| B2 | efficiency-trigger (EASM-style) | best classical reactive; adds migration-cost awareness |
| B3 | memoryless DQN (2103.06579-style triplet RL) | the RL floor our recurrence must beat |
| B4 | stacked-window DQN | node-30's honest rival (kills LSTM claim if it ties) |
| B5 | forecast→DQN pipeline (2208.03460 pattern) | RQ0-(b) ablation |
Ablations: plain DQN vs +Double vs +Dueling vs +LSTM(+GRU optional);
observability-masking eval (node 30); lead-time metric (node 46).

## 5. Metric contract (folded from 20/45/46; methodology update follows)
Primary: Jain's fairness index over controller load; p95 packet-in response
latency. Guard-rails: migrations/slot (cost), re-migration-within-2T rate
(instability), overload-event count. Novel reporting: **lead time** before
predicted overload where action was taken (our proactive claim, falsifiable).

## 6. Contribution statement (one line, for the proposal abstract)
"A recurrent deep-Q load balancer that anticipates mobility-driven
control-plane overload in distributed SDVNs and migrates switches under
protocol-accurate cost and stability constraints — evaluated where prior
'SDVN' schemes never went: with real vehicle movement."

## 7. Where this feeds next
- 00-proposal docs: RQ0 answer written per 43; gap stmt v3 replaces v2 in
  01-literature/literature-map.md on next touch.
- 02-methodology: metric contract + lead-time + masking → commit with this node.
- Supervisor questions: 1 (RQ0 — proposed answer now in lit evidence),
  2 (scope=migration confirmed by 44's fence), 4 (SUMO now *mandatory* per
  CMC'21 cautionary lesson), + new: risk items #1–4 above as their own queue.
