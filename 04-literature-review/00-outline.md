# Literature Review & Background — Tree Outline

The execution plan for this phase. Each node is a chunk of research that
becomes one MD file and one git commit. Nodes are ordered so that later
leaves always read from already-written parents (no forward references).

## Node contract (every LR*.md follows it)

```
# <Title>
## 1. Scope            — exactly what this file covers, and what it does not
## 2. Background       — concepts a reader needs, written for an SE audience
## 3. Findings         — the actual literature, organized not listed
## 4. Critical reading — disagreements, weaknesses, what the papers hide
## 5. Relation to thesis — the "so what" for OUR title
## 6. Sources          — every claim traced; verified-vs-inferred marked
## 7. Open threads     — leads this node produced that other nodes pick up
```

Rules applied to every node:
- **Provenance tier on each source:** `V` = abstract/full text read via tool,
  `S` = search snippet + metadata only, `U` = cited by a V-source but not
  independently checked. No `S` source may carry a load-bearing claim.
- **Differentiation obligation:** any paper that overlaps our title gets an
  explicit "what they did NOT do" line, because examiners will ask.
- No invented citations, no invented numbers. Missing data is written as
  "not stated in the accessible text".

## The tree

```
LR (this phase)
├── 10-foundations.md          SDN → SDVN → distributed control plane
├── 20-problem.md              what control-plane load IS; LB as a problem class
├── 30-methods.md              RL → DQN → recurrent DQN / POMDP → LSTM forecasting
├── 40-related-work/           the empirical core, 6 leaves
│   ├── 41-sdn-lb-rl.md            RL/DRL for SDN controller LB (general SDN)
│   ├── 42-sdvn-lb-classical.md    SDVN controller LB WITHOUT learning  ★closest
│   ├── 43-dqn-lstm-hybrids.md     DQN+LSTM and successor hybrids, other domains
│   ├── 44-cpp-mobility.md         controller placement + mobility-aware variants
│   ├── 45-switch-migration.md     migration mechanisms + master/equal/slave roles
│   └── 46-proactive-predictive.md  prediction-driven control-plane management
└── 50-synthesis.md            taxonomy matrix, gap statement v3, baseline shortlist
```

## Traversal order and rationale

Depth-first 10 → 20 → 30 → 41..46 → 50.
Foundations first so terminology is fixed once; problem statement second so
the methods chapter knows what it must optimize; methods third so the
related-work leaves can judge papers on a shared vocabulary; empirical leaves
next (the biggest block, 6 independent searches); synthesis last, purely
mechanical assembly of what the leaves concluded.

## Effort budget

- 10/20/30: 1 search pass + 1–3 abstract reads each.
- 41..46: 2–3 targeted queries + abstract/excerpt reads; ★papers get deeper
  treatment than the rest.
- 50: no new searching; assembly + gap re-verification only.

## Done when

Every node exists with sections 1–7 populated, and 50-synthesis.md contains a
comparison matrix in which no existing row matches our full (domain × plane ×
method) cell — i.e. the gap is *argued* rather than asserted.

## Status

Tracked per-file; update the table below as nodes complete.

| Node | Status | Commit |
|------|--------|--------|
| 00-outline | done | be95ef0 |
| 10-foundations | done | bab512c |
| 20-problem | done | 2c0d389 |
| 30-methods | done | this commit |
| 41-sdn-lb-rl | pending | — |
| 42-sdvn-lb-classical | pending | — |
| 43-dqn-lstm-hybrids | pending | — |
| 44-cpp-mobility | pending | — |
| 45-switch-migration | pending | — |
| 46-proactive-predictive | pending | — |
| 50-synthesis | pending | — |
