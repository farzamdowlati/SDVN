# 30 — Methods: DQN, Recurrence, and the LSTM Justification

Status: complete · Prev: 20-problem.md (problem statement v1) · This node
supplies the vocabulary all 41–46 leaves use to classify "method" columns.

## 1. Scope
Covers: RL formalization of the node-20 problem; DQN and its stability
lineage; why recurrent (LSTM) variants exist; the honest case *for and
against* recurrency here; LSTM's separate track record as a forecaster.
Does NOT cover: specific network-application papers (41–46).

## 2. Background (SE-reader version)

**RL vocabulary frozen here.** Environment = the SDVN control plane +
mobility generator. Agent = our balancer. Each slot: observe state s, pick
discrete action a (migrate switch i→domain j, or no-op), receive reward r.
Q-learning seeks Q(s,a)=expected return; **DQN** approximates Q with a
network, trained off-policy with a replay buffer (Mnih lineage; survey V:
Li 1701.07274).

**Two known DQN pathologies and their fixes (V abstracts):**
- *Overestimation bias* → **Double DQN** (van Hasselt 1509.06461): decouple
  action-selection from evaluation; measurably better in Atari.
- *Many similar-valued actions* → **Dueling DQN** (Wang 1511.06581):
  separate V(s) and advantage A(s,a). Relevant to us: most (switch,domain)
  pairs are near-equivalent no-ops — exactly the "many similar-valued
  actions" regime the dueling paper names.
Thesis stance: Double+Dueling+LSTM = the credible default variant stack;
the plain-DQN-vs-variants comparison becomes an ablation axis (methodology).

**The MDP→POMDP argument (V: Hausknecht & Stone 1507.06527).** Classic DQN
assumes the Markov state is observed. In a distributed control plane,
each controller sees **only its own domain's** queue and its own switches'
recent history — other domains' internal load is not observable except via
East-West chatter we don't control. Formally a **POMDP**; the belief state
is a function of the observation *history*.

**DRQN — the exact "DQN+LSTM" mechanism (V).** Hausknecht & Stone replace
DQN's first post-feature FC layer with an **LSTM**: Q-network over
recurrent hidden state h_t = f(h_{t-1}, o_t). Their findings, stated
precisely because our examiners will know this paper:
1. With equal history length, recurrence ≈ frame-stacking (no systematic
   Atari advantage);
2. Recurrence *degrades far less* when observation quality drops at test
   time and *scales better* when it improves — robustness to observability
   shift is the real payoff.

**The honest case for LSTM in SDVN (our argument, built on those findings):**
- (a) **Observability varies by regime** (urban density vs highway lull;
  day/night telemetry storms) — precisely DRQN's robustness case, not the
  "stack more frames" case;
- (b) **Effective horizons differ per zone** — a fixed stack window is
  wrong for both a bus corridor and a midnight ring road simultaneously;
  recurrent state adapts its integration depth;
- (c) **Mobility surges are predictable in load *history*** (spike shape
  precedes the spike) — the agent's value function implicitly forecasts,
  fusing node-20's "predictive regime" into one model instead of a two-stage
  forecaster+actor (whose error compounds).
- Counter-premise to defeat with ablation: a vanilla DQN on *stacked recent
  frames* (memoryless-ish but windowed) is a STRONG baseline — if it ties,
  the LSTM claim dies. We commit to running it (methodology note added).

**LSTM as forecaster (separate track record; S-tier, all snippet-found but
high-confidence classics):** Ma et al. 2015 (Travel-time/speed prediction,
cited ≈2,820), Shao et al. 2016 (traffic-flow LSTM, IEEE, cited ≈179), and
an active 2024–25 line (CNN-LSTM on cellular data, probabilistic density
forecasting). Consensus: transportation time-series are LSTM-friendly —
supports (c). These papers *forecast traffic*, not control-plane load —
the transfer is our formulation's job.

## 3. Findings
- Method space for our problem = {DQN, Double, Dueling} × {memoryless,
  stacked-window, recurrent} × {reactive obs, predictive obs}; DRQN covers
  cell (recurrent, value-based); 44–46 leaves populate application cells.
- POMDP formulations in networking are established (Yang 2020 multi-agent
  POMDP, S) — we are single-agent ⇒ simpler; do not borrow MARL complexity
  we don't need.
- Nothing in the V-lineage is SDVN-control-plane-specific ⇒ architecture
  combo is NOT the contribution (confirmed); the contribution is the
  formulation + domain + evaluation (per title-evaluation doc).

## 4. Critical reading
- The DRQN paper's own conclusion cuts *both* ways: reviewers may say "so
  why LSTM, stacking is equivalent?" — we must pre-empt with the
  observability-shift argument (b/robustness) + an experiment that varies
  observability (a designed contribution, cheap to add: randomly mask
  cross-domain telemetry at eval).
- Survey-level claims about "LSTM predicts traffic well" don't transfer
  automatically to packet-in arrival processes; our load-trace experiments
  must show autocorrelation of *controller load* specifically (data: from
  simulator, not from these papers).

## 5. Relation to thesis
Method section of the thesis builds on this file directly: Q-network spec,
variant stack, the two baselines the ablation must include (stacked-window
DQN; plain DQN), and the observability-masking evaluation design that turns
the DRQN caveat into our strongest experiment.

## 6. Sources
| # | Source | Tier | Role |
|---|--------|------|------|
| 1 | Hausknecht & Stone, DRQN, arXiv:1507.06527 | V | core mechanism + caveats |
| 2 | van Hasselt et al., Double DQN, arXiv:1509.06461 | V | bias fix |
| 3 | Wang et al., Dueling, arXiv:1511.06581 | V | advantage factorization |
| 4 | Li, DRL overview, arXiv:1701.07274 | V | terminology |
| 5 | Ma'15 (2.8k), Shao'16 (179), CNN-LSTM'24, prob. LSTM'25 | S | forecasting precedent |
| 6 | Yang'20 POMDP-MARL; Xiang'21 DRL-net survey | S | POMDP precedent |

## 7. Open threads
- Add "observability-masking eval" + "stacked-window DQN baseline" to
  02-methodology/methodology-outline.md (doing it now as part of node 30 commit).
- Verify Mnih 2013/2015 exact cite version for bib (1312.5602 vs 1507.06527-adjacent Nat.Compat note).
- Search "LSTM DQN network slicing / radio" deeper → node 43 (hybrids).