# 20 — The Problem: Control-Plane Load and Load Balancing as a Decision Problem

Status: complete · Prev: 10-foundations.md · Terminology inherited from node 10.

## 1. Scope
Covers: what counts as "load" on a controller; how imbalance forms; the
mechanisms (actuators) available to fix it; the cost of acting; metrics for
success; and the formal problem statement our thesis will attack. Does NOT
cover: learning algorithms (30) or paper-by-paper related work (41–46).

## 2. Background

**Defining load (V-grade anchors).** A controller serves requests; load is
therefore a *service queue*, not traffic volume. Measurable per-controller
quantities used across the literature [Zhu benchmarking arXiv:1902.04491 S;
Tootonchian HOT-ICE S]:
1. **Request rate** — packet-ins/s from the controller's switches;
2. **CPU utilization** of the controller process/node;
3. **Flow-setup latency / RTT** — the user-visible consequence (the snippet
   from the V-found HOT-ICE paper: a 10 ms flow-setup delay adds ≈10% to
   interactive flows — to be re-read for the exact claim);
4. **Flow-table occupancy** and memory.
For our MDP we will need ONE primary load signal; the field's default is
request rate ≈ proxy for CPU (EASM uses "load" as a composite ratio — V).

**How imbalance forms (V: EASM + RL-LB abstracts).** Dynamic traffic ⇒ some
domains' switch sets generate more first-packets than others ⇒ queue growth
⇒ rising flow-setup delay and (beyond capacity) dropped control messages,
i.e. stalled flows. In SDVN the same happens *spatially*: vehicle density
shifts with rush hours/platoons (node 10 asymmetry).

**Actuators — the ladder of intervention cost** [synthesis; migration
family V]:
| Actuator | Granularity | Cost | Literature |
|---|---|---|---|
| Switch/vehicle-group **migration** (re-association) | per-switch | sync + transient double-ownership | EASM, BalCon, Zhong, CMC'21 |
| Master/equal/slave **role adjustment** | per-switch-pair | lower (no session move) | Zhong 2022 V-snippet |
| **Elastic controllers** (spin up/down) | per-instance | boot + re-partition | Sufiev MDPI'19 S |
| **Placement** (where domains live) | offline | minutes–planning | CPP, Huang V |
Thesis scope decision: **migration/roles** are our actions (fast, fine-
grained); placement is *adjacent work*, not ours (defended vs 44).

**The cost of acting — migration.** Moving a switch = transfer/rebuild of
session state, East-West sync traffic, possible brief inconsistency;
hence *stability*: a bad balancer oscillates ("ping-pong", thrashing) and
pays migration cost forever. EASM's headline insight (V): optimizing pure
balance is wrong — optimize **balance rate ÷ migration cost** jointly.
This is the origin of the reward term we'll need.

## 3. Findings
- **Consensus problem definition.** (multi-controller SDN) partition switches
  ⇒ minimize load skew subject to response-delay and migration-budget
  constraints. Jain's Fairness Index (S, standard) or σ/max-deviation over
  controller load is the de-facto objective [survey 2308.02149 V confirms a
  metrics catalogue exists — harvest in 41].
- **Two control regimes.** Reactive (trigger on threshold crossing —
  EASM-style "trigger factor") vs predictive (act before overload arrives —
  Zhong dual-weight prediction S; 2008.01648 predictive association S).
  **Our thesis claims the predictive-recurrent regime, in SDVN, with RL.**
- **RL already tried on the reactive side.** arXiv:2103.06579 (V): computes
  migrate-out/in domain pairs from load-ratio deviation, then uses RL to pick
  migration *triplets* globally ⇒ faster packet-in response, less overhead.
  So "RL for controller LB" is *not* novel — the novelty bar is: recurrent
  (history-aware) agent + vehicular mobility + control-plane focus.
- **Value vs policy, and a warning (V: 2403.08775).** In distributed-CP DRL,
  value-based methods optimize single metrics well but **policy-based are
  more robust to sudden reconfiguration**. Our title fixes DQN (value);
  the related-work chapter must acknowledge this honestly and argue why
  discrete-action DQN still fits (switch-migration actions ARE discrete;
  robustness handled by the LSTM).

## 4. Critical reading
- Papers conflate "load" (CPU?) with "request rate" without measurement
  protocol; a simulator can hide queue dynamics. Our methodology must state
  the load model explicitly (→ 02-methodology update later).
- Most LB results (EASM, 2103.06579) evaluate with *synthetic* dynamic
  traffic, not mobility traces ⇒ they never confront what we claim to model
  (predictable *spatial* surges). Double-edged: weakness of theirs, bar for us.
- Migration-cost numbers are simulator-dependent; do not quote absolute
  ms/MB across papers — only orderings.

## 5. Relation to thesis — the formal problem statement (draft v1)
> Given N controller domains serving a partitioned SDVN, where per-domain
> load evolves with vehicle mobility, choose per-time-slot switch
> (re-)associations minimizing a weighted objective of
> **load skew (Jain) + flow-setup delay + migration cost + instability**,
> under partial observability of other domains' internal state —
> solved by a recurrent DQN whose LSTM encoder summarizes per-domain load
> history (⇒ anticipates mobility-driven surges).
Each term here maps to at least one V-source above; no term is invented by us.

## 6. Sources
| # | Source | Tier | Note |
|---|--------|------|------|
| 1 | EASM arXiv:1711.08659 | V-abstract | trigger factor, efficiency, −21.9%/+30.4% |
| 2 | RL-LB arXiv:2103.06579 | V-abstract | migration triplet selection |
| 3 | AI-LB survey arXiv:2308.02149 | V-abstract | metrics catalogue |
| 4 | Constrained-RL sync arXiv:2403.08775 | V-abstract | value vs policy robustness |
| 5 | Tootoonchian HOT-ICE'12 | S(snippet) | 10 ms flow-setup effect; read PDF in 41 |
| 6 | Zhu benchmarking arXiv:1902.04491 | S | metric list (RTT, setup latency) |
| 7 | Zhong'22 dual-weight; BalCon (Temple PDF); Wang'17 IEEE Access; Sufiev'19 | S | reactive baselines family |
| 8 | Jain's index refs | S | standard formula, no single-owner cite needed |

## 7. Open threads
- Harvest the 2308.02149 metric tables → feeds 50-synthesis matrix (during 41).
- Read HOT-ICE PDF fully → saturation numbers for the motivation chapter.
- Decide primary load signal (rate vs CPU) → supervisor question, methodology update.
- "Which papers report instability/thrashing explicitly?" → search in 45.