# 10 — Foundations: SDN, SDVN, and the Distributed Control Plane

Status: complete · Node contract: ../00-outline.md · Provenance: V = read via tool, S = snippet-level, U = secondhand

## 1. Scope
Covers: the SDN control-plane model; why it becomes *distributed*; what
"control-plane load" physically is; and the vehicular (SDVN) overlay of these
ideas. Does NOT cover: load-balancing algorithms themselves (node 20), RL
(30), or related-work papers with results (41–46).

## 2. Background (for an SE reader)

**SDN in one paragraph.** A conventional router decides forwarding locally,
per-packet, from logic baked into the vendor box. SDN splits this: a *control
plane* — a software program (the "controller") — computes forwarding policy,
and simple *data-plane* devices just execute a flow table. The interface
between them is southbound (OpenFlow is the reference). The engineering
consequence: network behavior becomes ordinary software you can version,
test, and scale horizontally — which is exactly why this is a *Software
Engineering* thesis, not just a networking one.

**The controller's workload is request-driven.** When a switch sees a packet
with no matching flow entry, it packages the header into a `packet-in`
message and asks the controller. The controller replies with `packet-out` /
`flow-mod`. Therefore controller CPU is consumed by: new-flow arrivals,
telemetry, topology events, and *replies*, not by forwarding bytes.
Classic measurement: Tootoonchian & Ganjali, *On Controller Performance in
SDN* (HOT-ICE 2012, V: full PDF found via search) — a single controller
saturates at a modest packet-in rate; this is the load we balance. [U-tier
summary; the specific numbers to be quoted in node 20 after a careful read]

**Why distribute.** One controller ⇒ single point of failure, unbounded
latency to distant switches, and a hard CPU ceiling. Multi-controller SDN
fixes all three but trades them for two new problems: (i) switches must be
*assigned* to controllers (the Controller Placement Problem, CPP), and (ii)
the controllers must stay *consistent* with each other (East-West traffic).
Surveys establishing this frame: Bannour et al., *Distributed SDN Control:
Survey, Taxonomy, Challenges* (S); Oktian & Lee, *Distributed SDN
controller system: design choice* (S, cited ≈269); Ahmad et al. 2021
(S, cited ≈291). The consensus: distributed control **creates** load
imbalance as a first-class failure mode — our thesis's reason to exist.

**SDVN = SDN applied to vehicular networks.** Ge et al., *5G Software
Defined Vehicular Networks* (V, abstract): SDN+5G+fog cells to cover
vehicles and *reduce frequent RSU handovers* — the mobility load argument
in the authors' own words. Islam et al., *SDVN: a survey* (S, cited ≈97):
heterogeneity, intermittent connectivity, QoS as defining SDVN challenges.

**Crucial SDVN asymmetry for our problem.** In datacenter SDN, switches are
fixed and the *workload* moves. In SDVN, the "switches" (vehicles, RSUs)
move; controller domains (cities, highway corridors) are static. A platoon
crossing a domain border is a synchronized storm of packet-ins +
association churn: load hotspots are *created by mobility itself*. Predicting
that churn is where an LSTM earns its place (defended in node 30).

## 3. Findings (structured, not listed)

- **Load taxonomy.** Three sources of control-plane load recur across
  sources: flow-setup (packet-in), management/telemetry, and membership
  churn (association changes, handovers). [frame synthesized from V/U srcs]
- **The two SDVN architecture families:** infrastructure-based (RSU/fog
  controllers — majority) vs infrastructure-less/mobile-controller
  (dSDiVN, V-abstract: cluster-based, *mobile controllers*, failure
  anticipation). Our title's "distributed control plane" most naturally
  denotes the first; the second is the frontier (node 20 picks the scope).
- **CPP is the adjacent, older subfield.** Huang et al. 1902.09451 (V):
  prior CPP work ignored controller *workload distribution* — the gap they
  name is *literally our load metric* showing up in placement papers.
  GA+GD hybrid solves it — non-learning in the RL sense.
- **Switch migration is the actuator.** Ye et al., *Maximizing SDN control
  resource utilization via switch migration* (S, cited ≈49): load can be
  rebalanced *without moving controllers* by re-associating switches —
  the action space our agent drives. Master/equal/slave roles (ONOS model)
  make migration a role-change protocol, not a wire event (preview → 45).
- **Predictive association already exists (non-vehicular).** arXiv:2008.01648
  (V-level: html found) *Predictive Switch-Controller Association* —
  confirms the predict-then-act template before we claim it (node 46).

## 4. Critical reading
- Citation counts (269/291/339 on design-choice papers) measure the *SDN*
  distributed-CP conversation; SDVN-specific LB is a much thinner, younger
  literature — do not overestimate how "solved" our exact problem is.
- "Distributed control plane" is used in two senses (multi-instance
  controllers vs geographically split domains). Our title must pin one (→
  Q-list #2).
- Survey claims in this node are S-tier until read in full; the thesis text
  must not quote them without a V pass later.

## 5. Relation to thesis
Terminology frozen here: *control-plane load* = packet-in/flow-setup +
churn rate per controller; *load balancing* = keeping that load even across
domains by re-association (45) / placement (44); the SDVN twist = mobility
makes load non-stationary ⇒ sequential decision-making under partial
observability (→ 30).

## 6. Sources
| # | Source | Tier | How obtained |
|---|--------|------|--------------|
| 1 | Ge et al., 5G SDVN, arXiv:1702.03675 | V | arXiv API abstract |
| 2 | Alioua et al., dSDiVN, arXiv:1706.05536 | V | arXiv API abstract |
| 3 | Huang et al., CPP+load, arXiv:1902.09451 | V | arXiv API abstract |
| 4 | Zhang et al., SDVN QoS sched, arXiv:2102.00953 | V | arXiv API abstract |
| 5 | Tootoonchian & Ganjali, controller perf | V(pdf)/U(read pending) | serper, USENIX link |
| 6 | Islam et al., SDVN survey (J. Netw. Comput. Appl.) | S | serper snippet |
| 7 | Oktian & Lee; Bannour; Ahmad — distributed CP surveys | S | serper snippets |
| 8 | Ye et al., switch migration (Comp. Networks) | S | serper snippet |
| 9 | arXiv:2008.01648 predictive association | S/V-html | serper |

## 7. Open threads
- Read Tootoonchian PDF → concrete packet-in saturation numbers for 20.
- Decide "distributed" sense (→ supervisor Q#2), log in 20.
- dSDiVN full read: is our agent applicable to mobile controllers too? (46)
- Collect the exact OpenFlow churn message flow for the modeling chapter (45).