# 43 — Related Work: DQN+LSTM Hybrids Outside the SDVN Control Plane

Status: complete · Resolves RQ0 empirically: BOTH readings of "DQN+LSTM" exist
in the literature; the recurrent-encoder form is the stronger, newer lineage.

## 1. Scope
Papers pairing a DQN with an LSTM (as encoder or as forecaster) in
networking/resource domains — NONE of which touches multi-controller
control-plane load balancing. Purpose: borrow their design legitimacy, and
map exactly what is transferable to our problem.

## 2. Findings

**A. Recurrent-encoder form (RQ0-a) — now mainstream in 5G/B5G scheduling.**
- **arXiv:2605.30630 (V) — the architectural twin.** *Temporally Encoded
  Double DQN for Proactive PRB Allocation in O-RAN Industrial Networks*:
  **LSTM encoder inside a Double DQN** over slice-level KPI sequences, CTMC
  traffic model for burstiness, xApp in O-RAN. Results: better slice
  satisfaction + buffer stability; **"longest sequence window provides the
  strongest gains"** — direct evidence that recurrence depth buys performance
  when load is temporally correlated (our SDVN premise).
  Differences to us: radio PRBs, industrial traffic, not controller CPU.
- **ARDDQN, arXiv:2405.11013 (V).** DDQN + RNN head for UAV path planning;
  *ablation done right*: LSTM vs Bi-LSTM vs GRU vs Bi-GRU vs no-RNN — a
  template we should mirror (our 30-node stack: no-recurrence / stacked-window
  / LSTM / GRU optional).
- Elsayed 2020, ISCC'22 (S): LSTM-captured Q-value history in mmWave RRM —
  same pattern across venues.

**B. Forecast-then-act pipeline (RQ0-b).**
- **arXiv:2208.03460 (V).** *LSTM predicts traffic demand + user locations →
  DQN allocates inter-slice radio resources*, explicitly motivated by
  **mobility** — the closest structural analogue to our (c) argument (node
  30), but in RAN slicing, not control plane. Two-stage error compounding
  critique applies to them too; we cite it as the pipeline alternative and
  run a small ablation if time allows.
- Tam & Kang (S, Semantic Scholar): LSTM-predicted server load feeding MEC
  LB decisions — the *server*-side cousin of our *controller*-side claim.
- Hechmi 2024 IEEE (S, snippet-only — full text paywalled): "hybrid DQN +
  LSTM for dynamic load balancing in 6G inter-domain". Our earlier
  literature-map flagged this as ★; its precise internal architecture
  (encoder vs pipeline) is **UNVERIFIED until campus access** — open thread.

**C. What this cluster says about our method risk.**
- Nobody in this cluster is doing control-plane switch-migration actions;
  all allocate *resources* (PRBs, slices, paths, tasks). Our action space
  (re-association under master/equal/slave protocol) is the novelty locus —
  combined with mobility (42) and recurrence (43-A). The three-way
  intersection remains empty after this node.

## 3. Critical reading
- 2605.30630 is very recent (2026) and arXiv-only → check for venue/revision
  before final citation; its CTMC traffic model is a good idea to steal for
  our synthetic-load cross-check (mobility trace + CTMC burstiness).
- Recurrent-hybrid papers routinely skip the stacked-window DQN baseline
  (the honest rival from node 30); we will not — our contribution's credibility
  depends on beating it.
- Pipeline papers (B) treat prediction quality as free; POSCAD (41) showed
  performance degrades gracefully with prediction error — cite POSCAD when
  justifying end-to-end recurrence over pipeline.

## 4. Relation to thesis → **RQ0 resolution proposed**
Evidence supports reading (a): DQN **with LSTM as recurrent state encoder**
(= DRQN lineage of 30 + the 2026 O-RAN twin), with (b) LSTM-forecaster→DQN
retained as an ABLATION and as the reading credited to Hechmi/Tam until
verified. Pending supervisor sign-off (03-open-questions #1 updated after
this node — see commit message).

## 5. Sources
| # | Source | Tier |
|---|--------|------|
| 1 | arXiv:2605.30630 LSTM-DoubleDQN O-RAN | V |
| 2 | arXiv:2405.11013 ARDDQN | V |
| 3 | arXiv:2208.03460 LSTM+DQN slicing | V |
| 4 | Hechmi IEEE 10987235 | S (paywalled — full-read thread) |
| 5 | Elsayed'20; ISCC'22; Tam&Kang; Nimmalapudi arXiv:2006.16733 | S |

## 6. Open threads
- Verify 2605.30630 venue + read their LSTM/GRU config (window length k!).
- Campus-access task: Hechmi full text → classify encoder-vs-pipeline.
- Steal CTMC burstiness model for methodology experiment matrix.