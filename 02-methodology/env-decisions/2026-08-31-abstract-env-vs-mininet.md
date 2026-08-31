# Environment Decision Memo — Abstract Python env vs Mininet emulation (vs NS-3)

Date: 2026-08-31 · Status: **DECIDED** (see §5) · Raised by: Farzam
("avoid heavy emulators for tens/hundreds of nodes; model [Xi,Yi,Zi] on
discrete intervals incl. RSU handoffs — is it lighter?")

## 1. The question, correctly framed
Our RL training budget is in *environment steps*, not wall-clock
convenience. A DQN ablation matrix (density × controllers × 6 agent
variants × seeds) needs **10⁷–10⁸ ticks**. The environment choice must be
made against that number.

## 2. Why Mininet specifically hurts RL
- Mininet is an *emulator* pinned to **real time**: 1 sim-hour ≥ 1 wall-hour
  (VT-Mininet exists to virtualize time but is a research fork, not the
  standard stack — and still pays full Linux/namespace/OVS syscall cost per
  packet event).
- Evidence the field already felt this: MininetGym (SFin/Elsevier 2025, S)
  and mininet-gym (UniMoRE, S) exist *just to paper over gym/real-time
  coupling*; RayNet (arXiv:2302.04519 / ACM 2024, V-level abstract, cited 15)
  motivates itself by exactly our problem: RL training wants deterministic,
  *accelerable* simulators, and recommends ns-3+gym when radio fidelity
  matters; ns3-gym (S) + trace-based ns3-gym work (S) confirm the pattern —
  and note ns-3 is ~minutes-per-experiment too, not ticks-fast.
- Mininet also fights us on scale: each node = a namespace + an OVS process;
  100+ RSU/vehicle switches + 3 controllers is heavy but survivable —
  1000 vehicles is a different animal. And our thesis does NOT exercise
  data-plane packet forwarding fidelity — it exercises **request-arrival
  dynamics**, which emulation computes expensively and abstractly ignores.

## 3. The measured spike (this folder, `spike_env_bench.py`)
Pure-Python/NumPy discrete-tick model — kinematics, nearest-RSU association
with 10% hysteresis, Poisson packet-ins ∝ local density, handover-triggered
registration bursts, M/M/1-style controller queues. Numbers (Apple-silicon
laptop, single core):

| Vehicles | ticks/s | 1 sim-hour | speed-up vs real-time |
|---------:|--------:|-----------:|----------------------:|
| 100 | ≈36,000 | 0.10 s | ≈36,000× |
| 300 | ≈27,000 | 0.13 s | ≈27,000× |
| 1,000 | ≈14,000 | 0.26 s | ≈14,000× |

A 24-hour simulated urban day (86,400 ticks) at N=1,000: **≈6.2 s.**
A full DQN run (1M ticks) ≈ 70 s of environment time — training becomes
compute-bound on the *network*, not the emulator. This is the qualitative
difference: Mininet cannot even represent 1M steps; our loop does an
experiment-hour per keystroke.

(Sanity note: the spike's handover/overload counters behave sensibly —
overload events 0 at cap=400 means capacity was generous; a knob, not a bug.
The spike is throughput-proof only; the real env adds road graphs.)

## 4. What we LOSE and how we cover it (honest ledger)
| Lost with abstract env | Mitigation |
|---|---|
| Radio-layer fidelity (SNR, interference, real 802.11p behavior) | Our problem is control-plane request load — largely *independent* of radio PHY; cite this as scope. POSCAD (V) made the same modeling abstraction for association work. |
| OpenFlow protocol timing (10 s Ryu timeouts, role-change handshakes) | Re-implement as *timers in the tick model* (cooldown + cost terms, per LR-45) — they are scalar parameters, not emergent effects. |
| Credibility optics ("not a real network") | Two-layer defense: (1) SUMO as the *mobility source* (professional, trace-driven — answers the CMC'21 'no vehicles' critique better than Mininet did for them); (2) **a small Mininet validation experiment** — replicate ONE trained-policy scenario at 3 controllers/15 RSUs, show metric agreement (direction, not magnitude). 2 days of work, closes the examiner question permanently. |
| Wireless-in-motion realism (the part of Farzam's suggestion that is NOT just kinematics) | Middle path: SUMO supplies mobility physics (car-following/Krauss model — real "wireless in motion" proxies via position→RSS models if ever needed); our tick env consumes positions. Building raw [x,y,z]+physics in our own loop = re-inventing SUMO worse; import its trajectory stream (TraCI file or FLOWS) at 1 Hz instead. |

Farzam's original framing ("a set of [Xi,Yi,Zi], discrete intervals,
computes handoffs") is exactly right — with one refinement: don't hand-roll
mobility physics; buy it from SUMO, hand-roll only the *control-plane*
queue/arrival layer (which nobody provides anyway).

## 5. DECISION
**Primary research environment: the abstract discrete-tick Python
(NumPy) simulator, driven by SUMO-generated mobility traces (or FLOWS),
with explicit protocol-cost/cooldown parameters harvested from LR-45.**

Role of the other stacks, demoted but kept:
- Mininet: *validation vignette only* (one topology, one policy, sanity
  table in the evaluation chapter) + a convenient source of realistic
  packet-in size distributions if we want them.
- NS-3/Veins: **out** for training; optional in future work only.
  Justified by RayNet's own argument: choose fidelity where the problem
  needs it; ours needs arrival dynamics, not radio.

Rationale compressed: (a) RL needs 10⁷–10⁸ steps — emulation is ~4 orders
of magnitude too slow (measured, §3); (b) the thesis claims *control-plane
arrival dynamics under mobility*, which the abstract model represents
directly with fewer confounders; (c) radio fidelity — the only real loss —
is outside our mechanism of action; (d) defense-in-depth via trace-based
mobility + one emulation check neutralizes the "toy model" objection.

## 6. Consequences for other docs
- 02-methodology/methodology-outline.md table: Mininet+SUMO hybrid is now
  *validation*, abstract env is *primary* → amended next touch.
- LR node 42 lesson applied: CMC'21's static-topology sin is avoided *by
  construction* (SUMO trace ingestion is a hard dependency).
- Supervisor Q#4 answered by this memo (trace-based abstract env + mininet
  validation); update 03-open-questions accordingly.
- New methodology task: define the SUMO→env interface (position frames at
  1 Hz, city network choice e.g. TUM/highway scenario; N ∈ {100..1000}).