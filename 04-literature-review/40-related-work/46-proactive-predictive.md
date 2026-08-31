# 46 — Related Work: Proactive & Prediction-Driven Control-Plane Management

Status: complete · The regime node: evidence that *foresight* improves
control-plane decisions — the conceptual bridge justifying our LSTM.

## 1. Scope
Schemes that act on *predicted* future network/control state: predictive
association (POSCAD), LSTM-forecast pipelines (slicing/MEC), digital-twin
proactive SDVN control, and vehicular handover prediction feeding SDN.
Hybrid *architectures* (encoder-vs-pipeline) classified in 43; here: the
*when to act* dimension.

## 2. Findings

**A. Theory says foresight pays — POSCAD, arXiv:2008.01648 (V, full abstract).**
Stochastic optimization of joint switch-controller association + control
devolution: (i) without prediction ⇒ near-optimal time-averaged cost with
tunable queue-stability trade-off; (ii) *with mild future information* ⇒
"significant reduction in request latencies, even faced with prediction
errors." Two things we take: (1) the claim "prediction helps association"
is **already theorem-grade** (non-vehicular); (2) graceful degradation with
prediction error ⇒ our imperfect LSTM is defensible. Our contribution turns
the *how to use the prediction* knob from hand-derived to learned.

**B. Mobile-network practice does it — Vehicular SDN mobility mgmt.**
- MM-SDVN / trajectory-prediction proactive mobility mgmt (S): virtual cells
  + trajectory prediction to cut handover frequency — vehicle-side analogue
  of POSCAD: predict → pre-configure.
- Duo 2020 MDPI (S, cited 57): SDN handover in cellular/802.11p — controller
  *monitors vehicle movement + cluster info* to preempt handover cost.
  Confirms: movement state IS observable to the controller in SDVN designs.
- Ankome 2026 "Reactive→Predictive mobility mgmt" systematic review (S):
  the field's own verdict that prediction is the direction. Our thesis =
  same argument applied one layer up (controller load, not connectivity).

**C. Digital-twin route — arXiv:2409.04622 (V, abstract).** DT of CAV/SDVN:
data-driven proactive control; flow-table overflow mitigation via flow-entry
lifespan optimization (50% TCAM reduction), roundabout waiting-time −22%.
Reads as: *predict traffic digitally, act in the control plane physically*.
Contrast: their actuator = flow-rule TTL (data-plane aging), ours =
association (control-plane topology). Same philosophy, different lever —
the DT-as-load-forecast source is future work worth naming.

**D. Prediction feeding load balancing, server-side.** Tam & Kang LSTM
predicts server load for MEC LB decisions (S); Rammohan 2025 edge-LSTM +
MAPPO-PPO-DDPG forecasts network states proactively (S); attention-LSTM
controller-load prediction (Liu'23, ACM, S — *title says "Controller Load
Prediction"!* ⇒ read next, see threads).

**E′. Two new V-tier local reads.** (i) **Xiao et al. 2024 (J. Supercomputing; local PDF)** — *deep-learning (LSTM×25 occurrences) controller-load prediction → switch migration* in general SDN, Mininet-validated, reports −16%/−8% migration cost vs time-sharing/distributed-decision baselines: the **pipeline reading (b) exists and is current** — but memory-in-DQN absent, vehicular absent. (ii) **Laclau et al. 2023 (arXiv:2308.13215, V)** — "Predictive Network Configuration for **Software Defined Vehicles**" = in-vehicle Ethernet — a *false friend* by title; excluded from our cluster (recorded in papers-index #19 to prevent future mis-citation).

**F. Negative result (searched, absent):** no paper found combining
predictive control-plane load balancing + vehicular mobility + learned
(recurrent) policy. Cluster 43-B pipelines predict radio demand; 45's
Zhong predicts *link* load for thresholds; 46-D predicts *server* load;
46-A proves foresight pays on *general* SDN. The four pieces of our jigsaw
each exist somewhere — never assembled. That's the gap, positively stated.

## 3. Critical reading
- "Predictive" papers vary in horizon: next-slot (LSTM one-step) vs seconds
  ahead (handover prep); our control loop (≈EASM 20 s rounds, CMC 10 s)
  needs *seconds-to-tens-of-seconds* horizon — the regime where one-step
  LSTM forecasts shine and POSCAD's mild-VOI assumptions live. State this
  horizon alignment in the proposal.
- Liu'23 attention-LSTM *controller load prediction* may partially claim our
  forecasting story (prediction only, no control loop — check!). If it
  exists, our framing shifts subtly: contribution = closing the
  predict→act loop with RL in SDVN, using their prediction as baseline.

## 4. Relation to thesis
This node converts "why LSTM?" from a modeling taste into a cited research
program: POSCAD (theory) + slicing/MEC (method pattern) + handover/DT
(domain pattern) ⇒ "we implement the learned, recurrent instance of
predictive control-plane LB for mobility-driven load, the one assembly the
literature lacks." Evaluation design: report *lead time* — how many
seconds before an overload event our agent acts vs reactive baselines.

## 5. Sources
| # | Source | Tier |
|---|--------|------|
| 1 | arXiv:2008.01648 POSCAD | V |
| 2 | arXiv:2409.04622 DT-SDVN | V |
| 3 | MM-SDVN; Duo'20; Ankome'26; Tam&Kang; Rammohan'25; Liu'23 attn-LSTM | S |
| 4 | arXiv:2208.03460 (from 43, cross-referenced) | V |

## 6. Open threads
- **PRIORITY: fetch Liu et al. 2023 (ACM ICC-ee?) "Attention-based LSTM for
  Controller Load Prediction"** — closest forecaster to our exact signal;
  decide whether we cite-and-extend. (Campus access likely needed.)
- Define "lead time" metric formally → methodology update (50 to fold in).
- Check POSCAD's queue-stability bound can serve as our theoretical anchor
  chapter's non-RL reference point.