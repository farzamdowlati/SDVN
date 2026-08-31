# Open Questions (for supervisor / proposal defense)

1. Method reading of "DQN+LSTM": recurrent DQN (encoder) vs predict-then-act
   pipeline? (See RQ0 — recommend former, ablate latter.)
2. What exactly is balanced: switch↔controller assignment only, or also
   elastic controller instances (placement-adjacent)?
3. Domain scope: highway, urban, or both? RSU/roadside topology assumptions?
4. Simulator policy: Mininet+SUMO acceptable for a networking-flavored SE
   thesis, or does the committee expect NS-3/Veins?
5. Contribution framing: application novelty (defensible) vs architecture
   novelty (weak — R-DQN exists). Confirm framing before the proposal text.
6. Title wording surgery proposed in title-evaluation.md — acceptable?
7. Formal related-work pass: first non-arXiv sweep DONE (see ../01-literature/avalai-search-pass.json,
   48 hits incl. IEEE/ACM/Elsevier) — but full-text access to IEEE Xplore still needs campus credentials.
