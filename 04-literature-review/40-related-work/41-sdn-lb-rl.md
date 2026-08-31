# 41 — Related Work: RL/DRL for Controller Load Balancing in (General) SDN

Status: complete · The "closest method" cluster; none of it is vehicular.

## 1. Scope
Papers where an RL/DRL agent balances *control-plane* load across
multi-controller SDN (general topology, non-vehicular). Classical LB goes
to 45; placement goes to 44; hybrid architectures go to 43.

## 2. Background
Reading grid (per node 30's vocabulary): each paper = (state features ×
memory model × action × reward). The interesting variance is whether the
agent remembers anything across steps — in this cluster: mostly NO.

## 3. Findings (organized by contribution type)

**A. The value-based anchor — arXiv:2103.06579 (V-abstract).**
Two-stage: compute migrate-out/in domain pairs from load-ratio deviation
(deterministic), then RL picks migration *triplets* under a no-conflict
constraint to minimize total cost. Metrics: controller resource utilization,
packet-in response rate, migration overhead. **Memoryless state** (per-round
load ratios) and **non-vehicular**. ⇒ Our #1 method baseline family; our
claim is that adding history (recurrence) + mobility beats per-round greedy
pairing when load surges are *predictable*.

**B. DRL switch-migration strategies.**
- Xiang et al. 2022, DRL-SMS (S, cited 24): DRL for multi-controller SDN migration.
- Yeo et al. 2021, Electronics (S, cited 40): RL-based switch+controller
  dynamic assignment for balanced distribution.
- Lv 2025, *Energy-aware controller LB, multi-agent RL* (S): IoT flavor —
  shows the reward terms now include energy; our design should mention it as future work.
Common ground: state = current load snapshot; action = migration set;
reward = load balance ± cost. None uses recurrent state; none models vehicles.

**C. Policy-gradient & hierarchical variants.**
- Kołakowski 2024 (S, IEEE): hierarchical DRL LB in heterogeneous network —
  scale of action space handled by hierarchy; relevant if our (switch×domain)
  action space explodes (methodology risk register).
- Xu 2023 (S, cited 27): load-aware *dynamic placement* with DRL —
  boundary paper with 44; placement-as-action, not migration.
- Constrained RL sync, 2403.08775 (V-abstract): latency constraint +
  value-vs-policy robustness finding (already used in nodes 20/30).

**D. MARL for network LB.** Yao 2022 (S): multi-agent RL for network load
balancing — one controller per agent is the natural SDVN extension (our
single-centralized-agent assumption needs a paragraph defending against
this line).

**E. Predictive+RL (bridge to 43/46).**
- **POSCAD, arXiv:2008.01648 (V-abstract — key find).** Joint dynamic
  switch-controller association + control devolution; stochastic network
  optimization, time-averaged cost, queue stability with *tunable
  trade-off*; **prediction improves latency beyond the no-prediction bound
  and stays robust to prediction error.** Not RL (Lyapunov-style online),
  general SDN — but it *proves the thesis premise* that foresight helps the
  control plane, and supplies the theoretical framing (queue stability) an
  examiner will ask for. Our agent is its learned counterpart.
- Transformer-DQN (2501.12829, V-abstract): TFT forecaster → DQN actor for
  *dynamic LB*; SDN-flavored sim, baselines RR/WRR, modest effect sizes.
  ⚠ careful: this looks like "routing/data-plane LB", not controller-CPU LB —
  verify full text before calling it control-plane. It IS the literature's
  existence proof for RQ0 reading (b) (forecast-then-act).

## 4. Critical reading
- Uniform weakness: synthetic loads, static topologies, small controller
  counts (≤4–6 typical), and **metrics reported without a load model**
  (rate vs CPU ambiguous — per node 20 §4).
- RL papers rarely report *migration count / instability* — the thing that
  killed classic schemes. When they do (2103.06579 "minimum cost"), it's a
  constraint, not a measured axis. ⇒ our instability-metric experiment has
  headroom for contribution credibility.
- 2103.06579's own baseline family (threshold, least-loaded) matches ours;
  expect to replicate its setup as the "general SDN" arm of evaluation.

## 5. Relation to thesis
This cluster defines the **methodological bar we must beat** in a non-
vehicular setting, and — critically — no member has: recurrent state,
mobility-driven load, or an observability-adaptive agent. The gap from node
20's statement remains intact after this cluster; POSCAD supplies the
"prediction pays" citation.

## 6. Sources
| # | Source | Tier |
|---|--------|------|
| 1 | 2103.06579 RL-LB (Li et al.) | V |
| 2 | 2008.01648 POSCAD (Huang et al.) | V |
| 3 | 2501.12829 TFT+DQN LB (Owusu et al.) | V (scope caveat pending full read) |
| 4 | 2403.08775 constrained RL sync | V |
| 5 | Xiang'22 DRL-SMS; Yeo'21; Lv'25; Kołakowski'24; Xu'23; Li'24 JPDC; Yao'22 MARL | S |

## 7. Open threads
- Full-read POSCAD → import queue-stability theorem framing into 50/motivation.
- Full-read 2501.12829 → classify data-plane vs control-plane (decides its cluster).
- Pull exact baseline tables from 2308.02149 survey (open thread from 20).