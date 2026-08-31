# 45 — Related Work: Switch-Migration Mechanisms, Roles, and Stability

Status: complete · The actuator deep-dive: what "migrating a switch" costs,
at protocol level, and how the LB literature scores it.

## 1. Scope
The migration mechanism itself (OpenFlow role machinery), the classical
threshold/heuristic migration schemes (our reactive baselines), and the
stability/thrashing problem. Load-balancing *policies* that happen to
migrate are elsewhere (41 general SDN RL; 42 SDVN classical).

## 2. Background — how migration works (protocol level)
OpenFlow 1.3 gives a switch up to three controller channels with roles
**master / equal / slave** (V-doc-level: OVS/OpenFlow docs, S-figures).
Migration = role change: a target controller sends `ROLE_REQUEST`
(role=equal), the switch flips its master; the old master demotes to
slave. Costs: (i) channel/session setup latency; (ii) flow-state handling —
slave keeps rules, but ownership metadata moves; (iii) consistency window
where two controllers *think* they manage the switch (East-West sync —
41/2403.08775 V); (iv) in-flight packet-ins during flip (Anis'21 thesis
notes the valid-scope subtleties, S). The Ryu default flow timeout of 10 s
(CMC'21's interval choice, V) is a concrete example of protocol timing
shaping control-loop granularity — our simulator inherits these constraints.
⇒ Methodology must model migrations as *role transitions with a cost +
cooldown*, not instantaneous set-membership changes.

## 3. Findings — the heuristic family (reactive baselines catalog)
| Scheme | Trigger | Selection rule | Source |
|---|---|---|---|
| Least-loaded | periodic | max-load switch → min-load ctrl | folklore; in all surveys |
| Threshold | load>τ | pairwise | CMC'21 (latency-τ, V); Kazemiesfeh'25 multi-level τ (S, cited 27) |
| BalCon / BalConPlus | load gap | minimize sync cost; initial + incremental balancing | Temple ITC paper (S) |
| SMDM (Wang'17) | utility | decision-making over candidate pairs, elastic scaling aware | S, cited ≈170 |
| DHA | load ratio | distributed hoping-style | 2-hop refs (S, cited by CMC'21) |
| TSSM/improved (Ethilu'23) | threshold | three-stage selection | S |
| **TSSM (Lai et al., IEEE TNSM 2022)** | threshold + assistant | **time-sharing**: two controllers sequentially share one switch's load; ONOS-implemented | **V (local PDF)** |
| ESCALB (Ali'23) | — | slave-controller allocation focus, **IoT multi-domain (NOT vehicular — verified V)** | V (local PDF) |
| Fractional (AL-Tam'19) | continuous | *fractional* migration — split switch load across controllers | S, cited 47 |
| Zhong'22 dual-weight | prediction | weight = f(predicted load, distance) | S, cited 50 — *predictive* reactive hybrid |
(For table: pull survey numbers in 50; Naji'25 IET survey = master list to
mine, V-url/S-content.)

**Stability/thrashing evidence.** EASM's "trigger factor" exists precisely
because naive schemes migrate repeatedly (V); CMC'21's 10 s window is a
manual anti-thrash damper (V); fractional migration treats oscillation
smoothness as the selling point (S). Nobody *measures* re-migration rate
as a headline metric — our instability metric (node 20) is a gap the field
itself left open; cite this absence as motivation.

## 4. Critical reading
- Most schemes decide per-switch independently ⇒ herd effects: all hot
  controllers dump onto the same cool one (the "migrate-in stampede");
  joint RL selection (2103.06579 style) is exactly why RL is invited here.
- Migration cost is modeled inconsistently (count-based vs time vs sync
  bytes) — when we benchmark their schemes, fix ONE cost model and say so.
- ESCALB's citation count (105) vs our snippet knowledge (slave allocation)
  mismatch: read before citing; possible over-claim risk.

## 5. Relation to thesis
Action space finalized here: `migrate(s → d)` discrete role-transitions with
protocol-accurate cost/cooldown; the CMC'21 latency-threshold scheme +
least-loaded + EASM-style efficiency trigger = our named reactive baselines
(→50 matrix). The 10 s Ryu-timeout constraint goes into methodology
simulation parameter list.

## 6. Sources
| # | Source | Tier |
|---|--------|------|
| 1 | EASM 1711.08659 | V |
| 2 | CMC'21 §4–5 (migration protocol) | V |
| 3 | OpenFlow 1.3 / OVS docs role machinery | V-doc |
| 4 | BalCon, SMDM, DHA, TSSM, ESCALB, AL-Tam fractional, Zhong | S |
| 5 | Naji'25 IET survey (switch-migration LB) | S (URL open, content pending) |
| 6 | Anis'21 thesis role-scope notes | S |

## 7. Open threads
- Full read Naji'25 survey (IET is open access) → harvest their scheme taxonomy straight into 50's matrix (V-upgrade).
- Read AL-Tam fractional — is partial migration compatible with our action space as an *extension*? (interesting future work line).
- ESCALB verification task added to campus-access queue.