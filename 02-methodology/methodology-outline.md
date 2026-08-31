# Methodology Outline (design only — no implementation)

## Simulation environment (candidates — decide with supervisor)
| Option | Pros | Cons |
|--------|------|------|
| Mininet + Ryu/ONOS + SUMO traffic gen | Fast, scriptable SDN control plane; SUMO = realistic mobility | Not road-accurate VANET radio |
| NS-3 + Veins/INET + (SUMO) | Standard VANET fidelity | Steeper; SDN stacks are community add-ons |
| Custom Python discrete-event sim | Full control over state/action | Re-inventing; credibility risk in defense |
Working assumption: **Mininet+SUMO hybrid** for control-plane experiments; justify radio abstraction explicitly.

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

## Experiment matrix (sketch)
Traffic density × number of controllers × mobility pattern × agent variant.

## Deliverable checkpoints
proposal → environment spike → baseline runs → agent v1 → ablations → writing.
