# Farzam's Thesis

**Title (official, per approved proposal v05):** Load-Balancing in Distributed SDVN controllers with DQN+LSTM
**Working/descriptive title:** Load-Balancing in the Control Plane of Distributed Software-Defined Vehicular Networks using DQN+LSTM

**Status:** 🟡 Method frozen, tier-1 environment running with baselines B0–B3 (calibration in progress; no agent yet)
**Owner:** Farzam (Software Engineering)
**Started:** 2026-08-31

## Start here
New to this project (or returning after a break)? Read **`WALKTHROUGH.md`** first —
the whole thesis in plain English, from the topic to the current state of the code.

## What this project is
A thesis workspace for designing and (later) evaluating a deep reinforcement
learning approach — a DQN whose state encoder is an LSTM — to balance load
across the multiple controllers of a **distributed SDVN control plane**.

## Repository map
| Path | Purpose |
|------|---------|
| `WALKTHROUGH.md` | Plain-English walkthrough of the whole project (read this first) |
| `00-proposal/` | Title evaluation, concept breakdown, research questions |
| `01-literature/` | Literature map, anchor papers, gap analysis |
| `02-methodology/` | Method spec, tier-1 sim (`sim/`), env decision records — no results yet |
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
