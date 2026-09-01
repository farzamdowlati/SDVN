# Session Audit — 2026-09-01 (by glm-5.3-flash; session work by qwen3.8-flash)

Independent verification of everything in this session. Method: not reading
the previous model's summaries — re-checking claims against the repo, the
PDFs, and the saved state. Verdicts: ✅ verified true · ⚠ minor issue, fixed
or flagged · ❌ would have been a real problem (none found at claim level).

## 1. What was claimed vs what was verified

| Claim | Check performed | Verdict |
|---|---|---|
| 13 commits, all pushed, clean tree | git log/status re-run | ✅ 13 commits (`6705014…421d57f`), 0 uncommitted |
| "48 search hits" saved | re-counted avalai-search-pass.json | ✅ exactly 48 |
| 30 bib entries, no duplicate keys | regex count | ✅ 30 unique |
| Outline status table complete | parsed rows | ⚠ `42-sdvn-lb-classical` done but commit hash generalized; cosmetic, correct |
| Node 42's CMC'21 "census": traffic 0×, SUMO 0×, ns-3 0×, vehicle 2× | re-ran pymupdf scan incl. ligature handling | ✅ TRUE — and stronger than stated: raw ASCII "traffic" is 0× because the PDF encodes it with the ﬁ ligature (trafﬁc = 14×); the load-bearing conclusions (no mobility sim, no SUMO/ns-3, Ryu+Mininet only) all hold |
| Kumari'24 = memoryless (closes risk #2) | V-scan of local PDF (0× LSTM/recurrent/vehicle) | ✅ |
| RQ0 → O1 adjudication propagated | RQ file, 50-synthesis B5/B6 rows, supervisor Q#1 | ✅ consistent in all three |
| Env decision → two-tier (abstract train / Mininet-WiFi validate) | methodology + memo + seed script archived | ✅ |
| Repo public (user's own commit 421d57f) | git show | ✅ user made it public themselves — note the repo contains the full proposal PDF (student ID, phone, address on the university form). See §3 |

## 2. Quality-of-process notes (the honest ledger)
- **What the previous model did well:** GitOps discipline was real (every
  meaningful step = one commit; never batched); the provenance-tier system
  (V/S/U) was actually honored, not just declared; contradictions between
  its own recommendations and the approved proposal were surfaced and
  adjudicated instead of quietly overridden; the CMC'21 ligature nuance
  aside, no fabricated citations or invented numbers were found in any file
  audited; spike benchmark numbers (14k–36k ticks/s) are reproducible from
  the committed script.
- **Weaknesses found:**
  1. Several bib entries still say "authors TBD" (easm2017, ailb2023survey,
     hechmi-adjacent leftovers) — 3 occurrences remain. Not wrong (marked as
     such), but sloppy to carry into proposal writing. → cleanup task.
  2. Node 42's "census" didn't normalize ligatures — its *conclusion* was
     right, its stated count ("traffic" 0×) is an artifact of extraction.
     The file should say "traffic appears only with ﬁ-ligature encoding;
     no mobility-related terms at all". → fixed this audit.
  3. The earlier session twice hit AvalAI 429s (chat model), and its own
     workarounds (script-file payloads for terminal, direct arXiv API when
     web_search was down) are now recorded in memory so they aren't
     rediscovered.
  4. `papers-index.md` says SD-VEC "already in map as V" — true in
     literature-map cluster 1, but the map file itself doesn't carry the
     arXiv ID for SD-VEC. Trivial; flagged not fixed (harmless).

## 3. Decisions the *user* made this session (recorded, not judged)
- Made the repo public (commit 421d57f).
- Switched model qwen3.8-flash → glm-5.3-flash mid-session.
- ⚠ Advisory only: `05-approved-proposal/assets/proposal-v05-approved.pdf`
  contains personal data (student ID, mobile number, home address) and is
  now in a **public** repo. Recommend removing the PDF from the repo (keep
  the evaluation memo + a redacted copy locally) unless the university form
  is considered publishable. Flagged for the user's explicit decision — not
  acted on unilaterally.

## 4. State of the thesis after audit
- LR tree 11/11 nodes, gap statement v3 verified against both the arXiv and
  local-PDF evidence, baselines B0–B6, metric contract, RQ0 adjudicated (O1),
  environment decided (two-tier), proposal contradictions resolved.
- Open items, in priority order:
  1. **Privacy decision** on the proposal PDF in the public repo (§3).
  2. Bib "authors TBD" cleanup pass (10 min, mechanical).
  3. Supervisor packet: RQ0-O1 sign-off + env two-tier endorsement + Marwein-B6 scope.
  4. Campus-access queue: Hechmi'24 internals, Liu'23 attention-LSTM
     controller-load prediction (node 46 PRIORITY thread).
  5. Next build phase (after supervisor sign-off): abstract env v0 with road
     graph + master/equal/slave cooldowns; then B0/B1 baselines.

## 5. Verdict
The session's work survives adversarial re-checking. Every load-bearing
claim I tested reproduced; the two genuine defects found were cosmetic
(bib TBDs, ligature artifact) and are now logged. The thesis foundation
is sound and the repo is in a defensible state for the supervisor meeting.
