# Concept Breakdown — the four pillars

## Pillar A — Software-Defined Vehicular Networks (SDVN)
- SDN trio: control/data plane separation, southbound (OpenFlow-like), global view.
- Vehicular twist: switches/hosts move at 60+ km/h ⇒ topology churn, frequent
  handovers, link breakage; RSUs and roadside edge servers as the physical substrate.
- Canonical background: "5G Software Defined Vehicular Networks" (arXiv:1702.03675);
  distributed architecture precedent: dSDiVN (arXiv:1706.05536).

## Pillar B — Distributed control plane
- Why distributed: one controller ≠ scalability, ≠ fault tolerance for city-wide VANET.
- New problems it creates: **controller load imbalance**, switch-to-controller
  assignment, domain consistency, controller-to-controller (East-West) sync traffic.
- Load sources: packet-in storms from new flows, churn of registrations as
  vehicles cross domain borders, telemetry.
- Adjacent literature: Controller Placement Problem (arXiv:1902.09451, survey
  arXiv:1905.04649), sync/consistency (arXiv:2403.08775).

## Pillar C — Control-plane load balancing (the decision problem)
- **State:** per-controller load (CPU, req/s, flow-table occupancy), switch→controller
  mapping, vehicle density/velocity per zone, recent load history (→ why sequence).
- **Action:** reassign switch(es)/vehicle-groups between controller domains;
  (optionally) spawn/retire elastic controller instances.
- **Reward:** negative weighted sum of: load skew (std dev / Jain's index),
  reassignment/migration cost, control-plane response latency.
- **Constraints:** stability (no ping-pong thrashing), sync-window delay when a
  switch migrates, consistency of flow state.
- Classic baselines the RL must beat: round-robin, least-loaded, threshold-based
  switch migration, and possibly a plain-DRL (Markov-DQN) variant.

## Pillar D — DQN + LSTM (the agent)
- DQN: value-based, discrete actions — fits "which switch moves where".
- LSTM: encodes last-k load/traffic history ⇒ handles partial observability +
  predicts mobility-driven surges before they hit a controller (proactive LB,
  a headline selling point).
- Honest lineage: this is a *recurrent* DQN (DRQN/R-DQN family, arXiv:1507.06527
  and successors). Thesis novelty = formulation + SDVN context, **not** the
  architecture combo per se.
- Modern variants worth one paragraph each in background: Double/Dueling
  DQN, Rainbow; note DRL-for-networking survey coverage (arXiv:1701.07274).

## Cross-pillar dependency diagram
```
[A SDVN mobility] --generates--> [C load dynamics] --observed by--> [B distributed CP]
        ^                                |                                 v
        +--------- physical substrate ---+------[D DQN+LSTM decides reassignments]
```
