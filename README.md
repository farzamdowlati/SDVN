# Farzam's Thesis

**Title (official, per approved proposal v05):** Load-Balancing in Distributed SDVN controllers with DQN+LSTM
**Working/descriptive title:** Load-Balancing in the Control Plane of Distributed Software-Defined Vehicular Networks using DQN+LSTM

**Status:** 🟡 Initiated — scoping & curation phase (no implementation yet)
**Owner:** Farzam (Software Engineering)
**Started:** 2026-08-31

## What this project is
A thesis workspace for designing and (later) evaluating a deep reinforcement
learning approach — a DQN whose state encoder is an LSTM — to balance load
across the multiple controllers of a **distributed SDVN control plane**.

## Repository map
| Path | Purpose |
|------|---------|
| `00-proposal/` | Title evaluation, concept breakdown, research questions |
| `01-literature/` | Literature map, anchor papers, gap analysis |
| `02-methodology/` | High-level method outline (agent, environment, metrics) — no code |
| `03-open-questions/` | Things to resolve with supervisor |
| `04-literature-review/` | Literature review & background study (tree of nodes, see 00-outline.md) |
| `05-approved-proposal/` | Official approved proposal v05 + evaluation & contradiction adjudication |
| `references.bib` | Verified BibTeX for anchor papers |

## GitOps convention
- Single source of truth: this local folder (`/Users/farzam/farzams-thesis`).
- Remote: `https://github.com/farzamdowlati/SDVN` (public, branch `main`).
- After every meaningful step (doc change, literature pass, decision): commit with a
  descriptive message and push. No batched mega-commits at the end.

## Explicit non-goals (for now)
- No simulations, no model code, no experiment results until the proposal is approved.

## Quick orientation read
1. `00-proposal/title-evaluation.md`
2. `00-proposal/concept-breakdown.md`
3. `01-literature/literature-map.md`
