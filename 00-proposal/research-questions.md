# Research Questions (draft v0)

**RQ0 (definition — pin down the method reading):**
Does "DQN+LSTM" mean (a) DQN with LSTM as recurrent state encoder
(POMDP formulation), or (b) LSTM load *forecaster* feeding a *classic* DQN
(predict-then-act pipeline)? Recommend (a), with (b) as an ablation.

> **UPDATE 2026-08-31 (LR nodes 30/43): proposed answer = (a)** — recurrent
> encoder (DRQN lineage; architectural twin arXiv:2605.30630), with (b)
> (arXiv:2208.03460 pattern) demoted to ablation B5. Evidence in
> 04-literature-review/43-dqn-lstm-hybrids.md §4. Awaiting supervisor sign-off.

**RQ1 (problem):** What characterizes control-plane load imbalance in
distributed SDVNs, and how does it correlate with vehicle mobility patterns
(zone crossings, RSU handovers)?

**RQ2 (method):** Can an LSTM-encoded DQN outperform static (least-loaded,
threshold) and memoryless (vanilla DQN) baselines on control-plane load
skew and reassignment stability under VANET mobility?

**RQ3 (latency cost):** What is the trade-off between load-balance quality
and switch-migration cost / control-plane response time?

**RQ4 (generalization):** Does the agent transfer across traffic regimes
(highway vs urban density, different controller counts) without full retraining?

## Hypotheses
- H1: memoryless DQN degrades as vehicle density grows (observability worsens);
  recurrent agent's advantage scales with density.
- H2: proactive (history-driven) LB reduces peak-controller overload events vs reactive threshold schemes.
