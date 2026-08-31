# Title Evaluation

> **"Load-Balancing in the Control Plane of Distributed Software-Defined Vehicular Networks using DQN+LSTM"**

## 1. Decomposition of the title
| Phrase | Role in the thesis | Interpretation |
|--------|-------------------|----------------|
| Load-Balancing | **Problem / objective** | Keep controller CPU/memory/request load even; avoid hot controllers; migrate switches/assignment |
| Control Plane | **Locus of the problem** | The problem lives in the *controller layer* (management traffic: packet-ins/outs, flow setup), NOT data-plane traffic engineering. This distinction must be defended in every chapter |
| Distributed | **Architecture constraint** | Multi-controller SDVN — the reason load imbalance exists at all (single controller ⇒ nothing to balance) |
| Software-Defined Vehicular Networks | **Domain** | SDN applied to VANETs: vehicles as switches/hosts, RSUs, fast topology churn |
| DQN+LSTM | **Method** | Deep Q-Network whose observation encoder is an LSTM — i.e. *partially observable, sequential* state. Alternative reading: LSTM forecasts load, DQN acts on forecast. **The ambiguity must be pinned down** (see RQ0) |

## 2. Strengths
- **Right-sized novelty.** SDVN controller load balancing with RL is an active
  but not saturated niche; the *vehicular* + *control-plane* combination is the
  defensible contribution — general SDN controller LB is already well covered
  (e.g. RL-based: arXiv:2103.06579).
- **Why LSTM is justified here (not decoration).** VANET controller load is
  *temporally autocorrelated* (traffic flow patterns, rush hours) and partially
  observable (a controller sees only its own domain's requests). DQN assumes
  Markov states; the LSTM is the principled fix for POMDP-like observability.
  This is the strongest argument in the title — the proposal should lead with it.
- **Measurable outcomes exist** (response time, load standard deviation,
  control-plane latency, migration count) → clean evaluation chapter.

## 3. Weaknesses / risks in the current wording
1. **"distributed" placement** — grammatically modifies SDVN; intended to
   modify *control plane*. Recommend: *"Distributed Control-Plane Load
   Balancing in Software-Defined Vehicular Networks using DQN+LSTM"*.
2. **The bracketed fragment** "[control plane of a]" reads like a live editing
   note — resolve before submission; the reader must never doubt the scope.
3. **"DQN+LSTM" is informal.** Committees prefer *"a DQN with an LSTM state
   encoder"* or *"recurrent DQN (R-DQN)"*. Note that **recurrent DQN is not new**
   (Hausknecht & Stone's R-DQN, DRQN series) — novelty claim must rest on
   *application + formulation*, not on the network combo itself.
4. **Silent on *what* is balanced.** Switch–controller reassignment? Flow-rule
   placement? Master/equal/slave roles? The proposal doc must answer this.
5. **No vehicle-mobility story.** Reviewers will ask why SDVN ≠ SDN: the
   answer (mobility-induced load hotspots at RSU/city-zone boundaries) must be
   made first-class, or the "vehicular" word is a costume.

## 4. Verdict
Title is **viable and fundable-looking** with moderate wording surgery. Core
research risk is scope drift into generic SDN; core writing risk is leaving
"control plane" vs "data plane" ambiguous. Both are handled in the proposal
docs in this folder.
