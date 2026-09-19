# Meta-analysis — 36-month harvest (2023-09-19 … 2026-09-19)

Provenance: **[S]** = abstract/metadata level (harvest: OpenAlex, IEEE Xplore API,
Crossref, arXiv, S2 — 2,617 unique in-window papers) · **[V]** = read in full
(22 PDFs in the local library, indexed in `01-literature/papers-index.md`) ·
**[U]** = inference/judgement of this memo, not yet verified against a source.

Scope: the 30 papers with a load-balancing / controller-placement signal in the
control plane (T1+T2 of `01-literature/2026-09-search-shortlist.md`). Full corpus:
`~/research/thesis-search-2026-09/records.jsonl`.

## 1. Structured matrix (abstract-level fields [S])

| # | Paper (short) | Year | recurrent | RL | predict | vehicular | mobility | fractional | cites |
|---|---|---|---|---|---|---|---|---|---|
| 1 | MARL LB, 6G SDN vehicle networks (TVT) | 2026 | – | ✓ | – | ✓ | ✓ | – | 5 |
| 2 | DDPG load-aware controller placement, IoV (IoT-J) | 2025 | – | ✓ | – | ✓ | – | – | 2 |
| 3 | BiLSTM LB in distributed SDN (JSC) | 2025 | ✓ | – | – | – | – | – | 12 |
| 4 | GRU seq2seq controller load prediction (APNet) | 2025 | ✓ | – | ✓ | – | – | – | 0 |
| 5 | CLB-LP: LB via deep-learning load prediction (TNSE) | 2025 | – | – | ✓ | – | – | – | 10 |
| 6 | Proactive joint LB, fuzzy-LSTM (IoT-J) | 2026 | ✓ | – | ✓ | – | – | – | 0 |
| 7 | BSM-LP: bidirectional migration + load prediction (IoT-J) | 2024 | ✓ | – | ✓ | – | – | – | 6 |
| 8 | MOOO-RDQN: recurrent DQN, controller placement (JNCA) | 2025 | ✓ | ✓ | – | – | – | – | 11 |
| 9 | Temporal deep-Q LB in SDN (Sensors) | 2024 | ✓ | ✓ | ✓ | – | – | – | 22 |
| 10 | Multi-area SDVN control-plane deployment (Appl. Sci.) | 2025 | – | – | ✓ | ✓ | ✓ | – | 3 |
| 11 | Survey: routing + LB in SDVN (Wireless Networks) | 2024 | – | – | – | ✓ | – | – | 12 |
| 12 | Hechmi: DQN+PPO dynamic LB, 6G (ComNet conf.) | 2024 | ✓ | ✓ | ✓ | – | – | – | 1 |
| 13 | 6G SDVN: AI controller selection, UAV VANETs (OJ-COMS) | 2026 | – | ✓ | – | ✓ | ✓ | – | 0 |
| 14 | LALB: prediction-driven latency-aware migration (ICWOC) | 2026 | ✓ | – | ✓ | – | – | – | 0 |
| 15 | FractionalLB: fractional switch migration (Networking Letters) | 2024 | – | – | – | – | – | ✓ | 5 |
| 16 | DSFSM: delay-sensitive fractional migration (ICNC) | 2025 | – | – | – | – | – | ✓ | 3 |
| 17 | OptiGSM: greedy minimum-migration (TNSM) | 2024 | – | – | – | – | – | – | 16 |
| 18 | AP-DQN: controller placement (Results in Eng.) | 2026 | – | ✓ | – | – | – | – | 0 |
| 19 | CAPFUL: dynamic controller placement, DRL (CCNCPS) | 2025 | – | ✓ | – | – | – | ✓ | 1 |
| 20 | Joint SDN sync + placement, DRL (NOMS) | 2024 | – | ✓ | – | – | – | – | 6 |
| 21 | Hierarchical DRL LB, multi-domain SDN (IFIP Netw.) | 2024 | – | ✓ | – | – | – | – | 4 |
| 22 | Multi-threshold controller LB + migration (ComNet) | 2025 | – | – | – | – | – | – | 14 |
| 23 | Traffic-driven controller LB, multi-controller (Network) | 2024 | – | – | – | – | – | – | 7 |
| 24 | Survey: switch-migration LB approaches (IET Networks) | 2025 | – | – | – | – | – | – | 1 |
| 25 | Predictive control-plane balancing, GA + game theory (TNSM) | 2025 | ✓ | – | ✓ | – | – | – | 2 |
| 26 | AI-enabled LB + mobility mgmt, IoV in SDN (IWCMC) | 2025 | – | ✓ | – | ✓ | ✓ | – | 2 |
| 27 | Adaptive LB, distributed multi-controller, migration (COMSNETS) | 2025 | – | – | – | – | – | – | 3 |
| 28 | MBL-DSDN: micro-cluster LB, distributed SDN (JSC) | 2024 | ✓ | – | – | – | – | – | 13 |
| 29 | Multi-level threshold SDN controller LB (SCIoT) | 2024 | – | – | – | – | – | – | 11 |
| 30 | Opti-Route: ML controller placement (Access) | 2025 | – | ✓ | – | ✓ | – | – | 0 |

Tag counts across the 30 [U]: recurrent 10 · RL 13 · predictive 9 · vehicular 7 ·
mobility 4 · fractional 3. **Recurrent ∧ RL ∧ vehicular = 0** (nearest: #9
recurrent+RL, non-vehicular; #1 RL+vehicular+mobility, memoryless, not LB-in-the-
control-plane-with-recurrence).

## 2. What the corpus says (headline findings)

1. **"Predict, then migrate" is now the standard control-plane LB formula** —
   deep-learned controller-load prediction feeding a migration/placement decision
   (#3, #4, #5, #6, #7, #14, #25). It is no longer a novelty claim by itself.
   [S]
2. **Prediction is where recurrence lives; the *policy* is memoryless.** Every
   recurrent paper here uses LSTM/GRU/Seq2Seq to forecast load, then hands the
   forecast to a threshold, greedy, or classical optimiser. RL papers use
   instantaneous state (DQN/DDPG/MARL) with no recurrent Q-function — except #8,
   whose title claims RDQN for placement, and #9 ("temporal" DQ). [S]
3. **The vehicular control plane is a separate, less mature lane**: RL there buys
   controller *selection/placement* (#2, #13, #30) or LB at a different layer (#1),
   and mobility is handled as handover management (#10, #26). None evaluates
   LB under a mobility model. [S]
4. **Action-space innovation is migrating from binary to fractional**: FractionalLB,
   DSFSM (#15, #16) and the older TSSM time-sharing scheme replace "move a switch"
   with "move a share of a switch's load" — a continuous/fractional action space is
   now a defensible design choice rather than an exotic one. [S]
5. **Evaluation is fragmented and mobility-poor**: Mininet/ONOS-class testbeds with
   custom topologies; metrics cluster on load variance / Jain fairness, migration
   count or cost, response latency, packet loss and convergence time. No shared SDVN
   benchmark, no standard mobility scenario. [S]
6. **Existing local full texts [V]** (from the pre-harvest library) confirm the same
   picture from the other side: the proposal's mandated baseline (Marwein 2024) is
   analytical + MATLAB with handover-driven hierarchy and no learning; the two
   "closest prior work" anchors (CMC 2021 SDVN switch migration; Kumari 2024 online
   Q-learning) are, respectively, non-learning and non-recurrent/non-vehicular.

## 3. Gap statement v3 (proposed — not yet applied to `literature-map.md`)

> Load-balancing in the SDN control plane is now routinely predictive (recurrent
> forecasters + threshold/greedy/optimiser decisions) and increasingly fractional,
> but this literature is almost entirely non-vehicular and treats the policy as
> memoryless. In vehicular SDN, reinforcement learning tackles controller
> selection/placement and mobility is handled separately as handover management;
> the recurrent encoding that would let a controller-level policy reason over
> mobility-driven, partially observable load dynamics has not been used as the
> Q-function's state encoder in a distributed SDVN control plane.
> **Unclaimed intersection: a recurrent (LSTM-encoded) DQN performing control-plane
> load balancing in a distributed SDVN, evaluated under an explicit mobility model.**

Differentiation obligations (papers that must be cited and contrasted explicitly):
#1 (RL+LB already in a 6G SDN vehicular setting), #3 (BiLSTM in distributed SDN
LB), #4/#5 (recurrent controller-load prediction), #8 (RDQN for placement).

## 4. Consequences for the simulation design

- The state must be **partially observable by construction** — per-controller local
  observations (own load, local flow arrivals), not a global load vector — otherwise
  the recurrent encoder has nothing to solve. [U]
- The mobility model is a **first-class experimental variable**: vehicle speed /
  density / handover rate must enter the scenario matrix, because rapid handover is
  what makes load dynamic and non-stationary. [U]
- Report the union of the community's metrics (load variance + Jain fairness,
  migration count and cost, control-plane response latency, packet loss, convergence)
  *plus* mobility-specific ones (handover-induced migration rate, transient imbalance
  during handover storms). [U]
- Fractional migration (#15, #16) is a credible richer action space; keep discrete
  binary migration as the primary action set for comparability with B0–B6, and treat
  fractional as an ablation. [U]

## 5. Next steps

1. **Deeper dive (tonight):** full texts for #1, #2, #3, #4, #5, #6, #7, #8 —
   method + experiments only, recorded as one memo per paper-group.
2. **Method freeze:** state/action/reward, POMDP framing, environment tier
   (NumPy tick env trained; Mininet-WiFi + Ryu validation), metric contract.
3. **Simulation = the actual job:** env skeleton (tick loop, controllers, mobility,
   actuator), baseline catalogue interfaces B0–B6, then DQN+LSTM agent, then train →
   evaluate → Mininet validation.
