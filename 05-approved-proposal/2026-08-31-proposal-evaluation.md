# Approved Proposal Evaluation — "Dowlati Fard - 05.pdf" (18 Apr 2025)

Source: ~/Documents/Thesis/proposal/Dowlati Fard - 05.pdf (v05; 12+ earlier
versions in folder). Evaluated 2026-08-31.

## 1. The canonical facts this document establishes
| Field | Value |
|---|---|
| Official EN title | **Load-Balancing in Distributed SDVN controllers with DQN+LSTM** |
| Student / program | Farzam Dowlati Fard — MSc (6 units), Computer Eng. — Software, IAU Science & Research Branch (Tehran) |
| Supervisor | Dr. Seyyed Hamid Haj Seyyed Javadi (Shahed Univ.) |
| Approved tools (per doc) | Python, **Mininet-WiFi + Ryu** ("Emulation vs Simulation" listed as implementation novelty), NGSIM + HighD trace datasets "if available" |
| Comparison target (per doc) | **Marwein et al., 2024, Computer Networks 254:110805** — "how much improvement vs the reference scheme?" is literally research question #2 |
| Schedule (Gantt in form) | 12 months from Farvardin 1404 (≈ Mar 2025): lit→design→modeling→KPI tuning→writing. We are past its own final band — repo acceleration matters. |

## 2. What the proposal COMMITS to (contract with the committee)
- **Problem:** imbalance across distributed SDVN controllers in dense/
  emergency traffic → latency, throughput collapse, QoS loss. ✔ matches LR.
- **Method reading — RQ0 is answered in the approved text as (b)-flavored:**
  "LSTM extracts temporal dependencies and predicts future traffic
  patterns; then DQN, *using these predictions*, decides the optimal
  load-distribution policy" (methodology §ب, conceptual model). The
  motivation frames DQN vs LSTM as *complementary limitations*
  (memory-without-decision vs decision-without-memory).
- **Variable set:** C_cpu, T_ctrl (throughput), H_freq (handover frequency),
  H_delay (handover latency), L_net, D_veh (density), Le2e, Ploss, α, γ, θ, ω.
- **Formulas:** E_lb = 1 − σ(C_cpu)/μ(C_cpu)  [= 1 − CV; a fairness index,
  kin of Jain's]; QoS = 1/(Le2e + Ploss + H_delay); η_ctrl = T_ctrl/(C_cpu+ε);
  **R = ω₁η_ctrl + ω₂QoS − ω₃O_ctrl** (O_ctrl = control overhead);
  vanilla DQN SGD update shown.
- **Hypotheses (doc):** H1 DQN+LSTM *reduces switch handover* vs traditional/
  heuristic schemes; H2 adaptive scheme → better balance → higher capacity;
  H3 tuning α + LSTM time-steps materially improves performance; H4 stable
  under dynamic/high traffic.
- **RQs (doc):** RQ1 how to combine DQN+LSTM in SDN for vehicular LB;
  RQ2 how much improvement (controller load, handover latency) vs the
  reference scheme [Marwein], and which network/DL params matter most;
  RQ3 behavior in real-time / dynamic traffic.

## 3. Contradictions with our working repo — adjudication needed
### 3a. RQ0: doc = predict-then-act pipeline (b); LR nodes 30/43 favored recurrent encoder (a)
The committed document says *LSTM predicts → DQN decides*; node 43 recommended
the DRQN-style encoder. Resolution options:
- **O1 (recommended): two-tier claim.** Implement the proposal as written —
  LSTM forecaster feeding DQN — AND run the recurrent-encoder (DRQN-style)
  variant as the thesis's *internal architecture comparison*, framed as the
  answer to proposal RQ2's "which parameters/architecture matter most".
  Inside the approved text (no amendment); matches Xiao et al. 2024 precedent
  (pipeline prediction + migration in SDN — V, local PDF read); turns the
  ambiguity into an experiment (ablation: pipeline vs encoder vs stacked-window).
  Cost: one extra variant — cheap on our fast abstract env.
- O2: strictly pipeline — loses the DRQN robustness/observability story.
- O3: strictly encoder — contradicts approved text; needs supervisor sign-off.
**Action adopted:** O1 in methodology; supervisor Q#1 rewritten.

### 3b. Environment: doc commits Mininet-WiFi + Ryu; our memo chose abstract env
The proposal's novelty bullet literally says implementation in Mininet-WiFi +
Ryu, "Emulation vs Simulation". Our 2026-08-31 decision memo demoted Mininet
to validation-only. These reconcile as the **two-tier architecture** the memo
already reserved:
- Tier 1 (hidden layer, RL training): abstract NumPy env (10⁷–10⁸ steps).
- Tier 2 (approved deliverable, per the form's own words): trained policies
  ported to **Mininet-WiFi + Ryu with SUMO/NGSIM-fed mobility** — the
  emulation-vs-simulation fidelity chapter the proposal promised. The user's
  folder already contains the seed script (`MN/vanet-sumo.py`, mn_wifi 802.11p
  + TraCI) → archived into the repo this commit.
This satisfies the committee text, the RL throughput reality, and adds an
evaluation chapter ("does the abstract-trained policy transfer to
emulation?"). **No proposal amendment needed.** Memo §5 updated: validation
tier is Mininet-**WiFi** + Ryu specifically, not plain Mininet.

### 3c. Baseline list must now include Marwein 2024 by name
The proposal names Marwein as *the* reference; our B0–B5 shortlist lacked it.
V-read of local PDF: hierarchical heterogeneous controllers,
vertical-handover-aware load distribution, analytical model + **MATLAB**
simulation — **no RL, no LSTM, no OpenFlow artifacts**. Because its
evaluation is analytical/MATLAB (not OpenFlow), exact porting is not
meaningful; instead implement its load-partitioning *policy logic* as a
baseline in our env (B6: "Marwein-style hierarchical partition"), and cite
its published curves where comparable. Added to 50-synthesis + bib.

## 4. Evaluation of the document itself (quality, as an outside reader)
Strengths: correct problem, credible method framing, concrete formulas and
variable inventory, named comparison target, named datasets — committee-ready
skeleton.
Weaknesses to fix in the thesis prose (NOT in the approved form):
1. "شبکه‌های عصبی عمیق (DQN)" mislabel in §ج (DQN ≠ generic DNN) — cosmetic,
   fix in the thesis translation.
2. **Handover conflated with controller-migration** (H_freq is *vehicle*
   handover; our action is *master-role* change). The thesis must separate
   these two churn types explicitly — examiners will spot the conflation
   (LR-45 gives the protocol vocabulary).
3. E_lb = 1−CV can go negative and rewards low-mean/high-noise regimes;
   present it as the proposal-committed primary metric with Jain's index
   (our metric contract) as the robustness check.
4. Reward R = ω₁η_ctrl + ω₂QoS − ω₃O_ctrl mixes unnormalized units
   (throughput/CPU vs 1/latency); the ω weights need a documented tuning
   protocol — covered by our normalized-reward note.
5. Timeline slippage vs its own Gantt (§1) — plan the accelerated path
   honestly in the progress report.
6. Reference list is thin for defense (6 sources); our literature layers
   (01 + 04) solve this — harvest into the formal related-work chapter.

## 5. What this commit did with it
- README + research-questions: adopted the official EN title; RQ0 → O1.
- 50-synthesis: gap-risk #2 (Temporal-Kumari online RL) and #4 (Liu-like
  predictive papers) **closed** via local PDFs (V-tier: Kumari'24 online RL
  = memoryless Q-learning, no LSTM/vehicle; Xiao'24 = LSTM→migration
  pipeline, general SDN, Mininet); B6-Marwein added.
- 44/45/46: added local-PDF V-reads (ESCALB verified as IoT not vehicular;
  TSSM time-sharing migration baseline; Laclau predictive config — in-
  vehicle Ethernet scope, *not* control-plane LB → excluded from our
  cluster, noted).
- references.bib: +8 approved-proposal-era entries.
- New assets: proposal PDF copy, `papers-index.md` (full audit of 24 PDFs),
  `vanet-sumo.py` seed archived under 02-methodology/env-decisions/mnwifi-validation/.
