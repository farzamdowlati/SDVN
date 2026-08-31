# Literature Map (anchor papers — links verified against arXiv API, 2026-08-31)

Legend: ★ core anchor · ○ supporting · ⚠ read in full before citing as related work

## Cluster 1 — SDVN foundations
- ○ [1702.03675] Ge, Li, Li — *5G Software Defined Vehicular Networks* (2017)
- ★ [1706.05536] Alioua, Senouci, Moussaoui — *dSDiVN: a distributed SDN architecture for Infrastructure-less Vehicular Networks* (2017) — direct precedent for distributed SDVN control plane
- ○ [2102.00953] *QoS-aware Link Scheduling Strategy for Data Transmission in SDVN* (2021)
- ○ [2409.04622] *Digital Twin Enabled Data-Driven Approach for Traffic Efficiency and SDVN Optimization* (2024)

## Cluster 2 — Distributed control-plane problems (placement, sync, LB)
- ★ [1902.09451] Huang, Chen, Fu, Wen — *Optimizing Controller Placement for SDN* (2019)
- ○ [1905.04649] Kumari, Sairam — *A Survey of Controller Placement Problem in SDN* (2019)
- ★ [2103.06579] Li, Zhou, Gao, Qin — *SDN Controller Load Balancing Based on Reinforcement Learning* (2021) — closest prior work; NOTE: plain SDN, not vehicular ⇒ your gap
- ★ [2403.08775] *Constrained RL for Adaptive Controller Synchronization in Distributed SDN* (2024)
- ○ [1711.08659] *EASM: Efficiency-Aware Switch Migration for Balancing Controller Loads in SDN* (2017) — baseline family
- ○ [2308.02149] *AI-based load balancing in SDN: a comprehensive survey* (2023)

## Cluster 3 — RL / DQN+LSTM methods
- ★ [1312.5602] Mnih et al. — *Playing Atari with Deep Reinforcement Learning* (2013) — DQN origin cite
- ★ [1507.06527] Hausknecht & Stone — *Deep Recurrent Q-Learning for Partially Observable MDPs* (DRQN, 2015) — the exact lineage of "DQN+LSTM"
- ○ [1701.07274] Li — *Deep Reinforcement Learning: An Overview* (2017)
- ○ Dueling/Double DQN + recurrent variants — build on the two anchors above
- ○ [2605.30630] *Temporally Encoded Double DQN for Proactive PRB Allocation in O-RAN* (2026) — evidence the recurrent/proactive-DQN pattern is current

## Cluster 4 — RL in vehicular / edge networks
- ○ [2003.01005] *Eco-Vehicular Edge Networks: Distributed Multi-Agent RL* (2020)
- ○ [2105.15022] Talpur, Gurusamy — *RL-based Dynamic Service Placement in Vehicular Networks* (2021)
- ○ [2410.03472] *DRL for Delay-Optimized Task Offloading in Vehicular Fog Computing* (2024)

## Cluster 5 — non-arXiv anchors (found via AvalAI/serper pass, 2026-08-31)
- ★ [CMC 2021] *Load Balancing Algorithm for Migrating Switches in Software-Defined Vehicular Networks* (techscience.com/cmc/v67n1/41207) — **closest prior work overall**: SDVN + switch-migration LB, but classical algorithm, no RL. Cite + differentiate early.
- ★ [IEEE Access 2024, Hechmi] *Enhancing QoS for Dynamic Load Balancing in 6G… A Hybrid Approach Combining DQN and LSTM* (ieeexplore 10987235) — proves the DQN+LSTM combo is publishable; NOT vehicular control plane ⇒ still your gap.
- ○ [IET Networks 2025, Naji] *A Survey of Load Balancing Approaches Based on Switch Migration in SDN* — backbone for Cluster C related work.
- ○ [ACM 2025] *Load Balancing in the Internet of Vehicles: A Comprehensive Review* — confirms the LB-vs-control-plane confusion reviewers will raise; use its taxonomy.
- ○ [ScienceDirect 2018, Wang, cited 65] *Load-balancing routing in SDN with… distributed control plane* + [Electronics 2021, Yeo, cited 40] RL-based switch/controller assignment.
- ○ [Comp. Networks 2022, Zhong, cited 50] *Prediction-based dual-weight switch migration* — master/equal/slave roles; strong reactive baseline.
- ○ [MDPI Applied Sciences 2025, Li] *A Multi-Area SDVN Control…* — traffic prediction → load balancing in SDVN (nearest to your proactive-LSTM framing).
- ⚠ All Cluster-5 items found by search-snippet level; read in full (or at least abstract+method) before citing.

## Gap statement (v2 — sharpened after Cluster 5)
> RL-based controller LB exists in SDN (★2103.06579). DQN+LSTM hybrids exist
> for load balancing outside vehicular control planes (★IEEE Hechmi 2024).
> SDVN switch-migration LB exists WITHOUT learning (★CMC 2021).
> **The unclaimed intersection: a recurrent (LSTM-encoded) DQN performing
> control-plane load balancing in a *distributed* SDVN under mobility.**
> The two ★ papers are the thesis's primary differentiation obligations.
