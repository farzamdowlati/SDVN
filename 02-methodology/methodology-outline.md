# Methodology Outline (design only — no implementation)

## Simulation environment — **DECIDED 2026-08-31**
Abstract discrete-tick Python/NumPy environment fed by SUMO mobility traces
is the PRIMARY training platform; Mininet demoted to a single validation
vignette; NS-3 out of scope. Full rationale + measured throughput
(~14k–36k ticks/s; 24 sim-hours in seconds; emulation ≈4 orders slower for
RL-scale step budgets): `env-decisions/2026-08-31-abstract-env-vs-mininet.md`
and spike code `env-decisions/spike_env_bench.py`.

## Agent design (outline, per Pillar D)
- Observation: sliding window (k steps) of per-controller load features + zone vehicle counts.
- Recurrent encoder: LSTM (hidden h) → MLP → Q-values over discrete actions
  (migrate switch s_i to domain d_j, or no-op).
- Training: replay buffer over *sequences* (episode-aware sampling), Double/Dueling
  variants as ablation axes.
- Evaluation metrics: Jain's fairness index on controller load, p95 packet-in
  service time, number of migrations, instability (re-migration within T),
  overload-event count.
- Baselines: least-loaded, threshold-based migration (cf. EASM), vanilla
  memoryless DQN, random.
- REQUIRED per LR node 30: (i) stacked-window DQN baseline (recent-frames
  history, no recurrence) — the honest test of the LSTM claim;
  (ii) observability-masking eval (randomly drop cross-domain telemetry at
  test time) — turns the DRQN robustness finding into our experiment;
  (iii) Double+Dueling recurrent variant as default agent, plain DQN as ablation.

## Evaluation metrics (metric contract — LR node 50)
- Primary: Jain's fairness index on controller load; p95 packet-in response latency.
- Guard-rails: migrations per slot (cost), re-migration-within-2T (instability),
  overload-event count.
- Novel: LEAD TIME — seconds before an overload event at which the agent acts
  (falsifies/proves the proactive claim vs reactive baselines B0–B2).

## Experiment matrix (sketch)
Traffic density × number of controllers × mobility pattern × agent variant.

## Deliverable checkpoints
proposal → environment spike → baseline runs → agent v1 → ablations → writing.
