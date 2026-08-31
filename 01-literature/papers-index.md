# Local Paper Library Index — ~/Documents/Thesis/Papers (+ root PDFs)

Audited 2026-08-31 (pymupdf first-pages / full-text term scans; V-tier where
marked). Mapping column = our LR tree (04-literature-review/). Files are NOT
copied into the repo (copyright); this index + bib entries are the interface.

| # | File | Identity (V: title/authors from PDF) | Cluster / node | Status update |
|---|------|--------------------------------------|----------------|---------------|
| 1 | phibadeity-s-marwein-efficient-load-distribution-in.pdf | Marwein, Sur, Kandar — *Efficient load distribution in heterogeneous vehicular networks using hierarchical controllers*, Computer Networks 254:110805 (2024) | 50-synthesis **B6**; proposal's reference scheme | V-read: analytical + MATLAB, no RL, handover-driven hierarchy. Cite as proposal-mandated comparison. |
| 2 | Optimizing_SDN_Controller_Load_Balancing_Using_Online_Reinforcement_Learning.pdf | Kumari, Roy, Sairam — *Optimizing SDN Controller LB Using Online RL*, IEEE Access 12 (2024), DOI 10.1109/ACCESS.2024.3459952 | 41; 50-risk#2 | V-scan: Q-learning online, **0× LSTM/recurrent/vehicle**. Risk #2 CLOSED — not recurrent, not SDVN. Add to 41 as newest memoryless-RL anchor. |
| 3 | s11227-023-05658-6.pdf | Xiao, Pan, Liu, Liu — *LB strategy for SDN multi-controller clusters based on load prediction*, J. Supercomputing 80:5136 (2024) | 43/46; **RQ0 evidence** | V-scan: **LSTM(25×) predicts controller load → migration decision**, Mininet, general SDN. = the literature's existence proof of reading (b) — the exact pipeline form. -16%/8% migration cost vs TSSM (their numbers). |
| 4 | TSSM_...pdf | Lai, Wang, et al. — *TSSM: Time-Sharing Switch Migration to Balance Loads of Distributed SDN Controllers*, IEEE TNSM 19(2) 2022 | 45 baseline catalog | V-read: time-sharing (sequential co-ownership) migration, ONOS impl. New baseline family member; interesting alternative action-space (fractional-ish). |
| 5 | 1-s2.0-S1319157823001209-main.pdf | Ali, Jhaveri, Alswailim, Roh — *ESCALB: effective slave controller allocation-based LB*, J. King Saud Univ. CS (2023) | 45 verification | V-read: **IoT multi-domain, not vehicular** (vehicle=2× incidental) — verification task closed. Keep as reactive-τ family, general SDN. |
| 6 | 2308.02149v1.pdf | — *AI-based LB in SDN: comprehensive survey* (2023) | 20/41 metric harvest | Full PDF local → open thread "harvest metric tables" now possible offline (40 pp). Queue for metric-contract validation. |
| 7 | 2403.08775v1.pdf | Panitsas, Mudvari, Tassiulas (Yale) — *Constrained RL for Adaptive Controller Synchronization in Distributed SDN* (2024) | 20/41 | V already; authors CONFIRMED (bib note "TBD" can be removed — done this commit). |
| 8 | Distributed_SDN_Control_Survey_Taxonomy_and_Challenges.pdf | Bannour, Souihi, Mellouk — IEEE COMST 20(1):333 (2018) | 10 cluster-2 | S→V available locally; cite with confidence. |
| 9 | s10922-020-09575-4.pdf | Ahmad, et al. — *Scalability, Consistency, Reliability, Security in SDN Controllers: survey*, JNSM 29:9 (2021) | 10 | V available; matches S-snippet cited-291. |
| 10 | 1-s2.0-S1389128619306553-main.pdf | Ben Jaballah, Conti, Lal — *Security and design requirements for software-defined VANETs*, Comput. Networks 169:107099 (2020) | 10 (SDVN challenges) | security flavor; use for threat-model aside only. |
| 11 | 1-s2.0-S2214209623000931-main.pdf | Indukuri et al. — *Comprehensive survey on SDN and blockchain-based secure vehicular networks*, Veh. Comm. 44:100663 (2023) | 10 | background cite. |
| 12 | 1-s2.0-S1383762120302113-main.pdf | **Islam et al. — *SDVN: a survey*, Journal of Systems Architecture 114:101961 (2021)** | 10 cluster-1 | This IS our node-10 S-tier "Islam SDVN survey" → upgrade to V (local full text). |
| 13 | s12083-023-01448-2.pdf (+ LBABC copy; .key slides) | Sridevi, Saifu et al. — *LBABC: Distributed controller LB using artificial bee colony in SDN*, PPNA 16:947 (2023) | 45 (heuristic family) | metaheuristic baseline — cite as non-RL optimizer lineage (vs GA+GD Huang). Duplicate file in Papers/ and Thesis root (same paper; root copy is the read one). |
| 14 | s11227-022-04313-w.pdf | Ashraf et al. — *Scalable offloading using ML for distributed multi-controller SDN*, J. Supercomputing 78 (2022) | 41-D adjacent | ML-offloading, general SDN. |
| 15 | s10922-022-09642-y.pdf | Malbašić et al. — *Hybrid SDN Networks: Multi-parameter Server LB*, JNSM 30:30 (2022) | 41 boundary | **server**-plane LB — cite for the "LB polysemy" warning (node 20/42). |
| 16 | 2103.14225v1.pdf | — *SD-VEC: Software-Defined Vehicular Edge Computing* (2021) | 10 cluster-1 | already in map as V; PDF local. |
| 17 | 2308.04564v1.pdf | Chen, Ruffini — *Resource Cooperation in MEC and SDN based Vehicular Networks* (2023) | 10 | edge-resource adjacent. |
| 18 | 2018-IEEE MNET.pdf | — *CVEC: collaborative vehicular edge computing framework*, IEEE Network 2018 | 10 | background. |
| 19 | 2308.13215v1.pdf | Laclau, Bonnet, Ducourthial, Li, Lin — *Predictive Network Configuration with Hierarchical Spectral Clustering for Software Defined Vehicles* (2023) | 46 scope-check | ⚠ "SDV" here = **in-vehicle Ethernet**, NOT road vehicular networking — excluded from control-plane-LB cluster (good catch: title would have poisoned node 46). |
| 20 | Deep_Active_Learning_..._SDVN.pdf | Ahmed, Lin, et al. — *Deep Active Learning Intrusion Detection and LB in SDVN*, IEEE T-ITS 24(1):953 (2023) | 42/50 | V-read: **sensor-data↔DC task LB + IDS**, not controller-CPU. Proposal ref [4] — cite carefully as data-plane LB so examiners don't think our locus overlaps it. |
| 21 | SDN-Based_Service_Mobility_Management...pdf | Shah, Gregory, Li, et al. — IEEE IoT-J 9(15) 2022 | 46 | service-migration under mobility; adjacent framing. |
| 22 | A_Multi-objective_..._SDVN_Controllers_Placement_Problem.pdf | Alouache, Yassa et al. — multi-objective SDVN **CPP** | 44 | placement cluster addition (NSGA-family precedent). |
| 23 | Dowlati Fard.pdf (root) | student's own earlier draft material | — | check content before reuse. |
| 24 | Black/Culver/Goransson *Software Defined Networks: A Comprehensive Approach* (root) | book (Morgan Kaufmann 2016) | 10 | textbook citation for SDN fundamentals chapter. |

**Duplicates noted:** `Optimizing...(1).pdf` = same file (gitignore-level hygiene: keep one when imported into any index).

## Harvest actions generated (from proposal-eval + this audit)
1. Read 2308.02149 metric tables offline (open thread from node 20/41) → validate metric contract.
2. Marwein: extract its mode-comparison numbers for the B6 sanity band.
3. Xiao'24: note their LSTM horizon + feature list (pipeline arm of our architecture ablation).
4. TSSM: decide if time-sharing belongs in our action space as extended ablation (later).
