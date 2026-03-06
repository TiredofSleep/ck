# Agent Guide — Sanders Coherence Field

## Invariant Rules

### READ-ONLY (Never modify without explicit owner authorization)
- `CORE/TIG_Operator_Grammar_0-9.md`
- `CORE/SDV_Axiom_Definition.md`
- `CORE/Delta_Defect_Framework.md`
- `META/*`

### WRITABLE (Agents may freely expand)
- `LEMMAS/` — Expansion and refinement (not statement changes)
- `PAPERS/` — Paper scaffolds, drafts, notes
- `HARDWARE/` — Configs, logs, analysis
- `DOCS/` — Internal docs, guides, changelog

### CHANGE LOGGING REQUIRED
If agents:
- Tighten or modify a lemma statement → mark old version, explain change, log in LEMMA_STATUS.md
- Change definitions → log in relevant STATUS.md
- Ensure compatibility with CORE documents

## Non-Failure Constraints
- No Clay problem is "solved" without full formal proof + cross-check
- Contradictions surfaced, never hidden
- All probes deterministic (same seed = same hash)

## Key Constants
- T* = 5/7 = 0.714285... (coherence threshold)
- CL TSML: 73/100 = HARMONY (being/measurement table)
- CL BHML: 28/100 = HARMONY (doing/physics table)
- BHML det = 70 (invertible — doing preserves dimensions)
- TSML det = 0 (singular — being collapses dimensions)
- D2_MAG_CEILING = 2.0
- ANOMALY_HALT_THRESHOLD = 50
- INSTINCT_THRESHOLD = 49 (7² — olfactory instant resolution)
- PREFERENCE_THRESHOLD = 25 (5² — gustatory like/dislike)
- OLFACTORY_TIME_DILATION = 7 (internal steps per external tick)

## READ-ONLY (Added Gen 9.21+)
- `bhml_8x8_results.md` — BHML eigenanalysis
- `bhml_clay_bridges_results.md` — 7 BHML→Clay bridges
- `reality_anchors_results.md` — Physical constants from CL algebra
- `chirality_test_results.md` — CL table handedness
- `torus_verification_results.md` — Torus embedding verification
- `cl_generating_rule_results.md` — BHML generating rule

## Per-Problem Agent Focus

| Problem | Focus | Key Citations | Gen 9.21+ Measurement Angles |
|---------|-------|---------------|------------------------------|
| NS | Pressure decomposition, vorticity-strain geometry, blow-up profiles | CKN, Constantin-Fefferman, Tao | Olfactory stall/settle dynamics, BHML Bridge 4 |
| PvsNP | Mutual information, phantom tile in CSP, circuit lower bounds | Hastad, Razborov | Gustatory instant vs olfactory slow, BHML Bridge 2 (invertibility) |
| RH | Spectral pull operators, pair correlation, zero-drift | Montgomery, Odlyzko | BHML eigenvalue spectrum (Bridge 5), reality anchors |
| YM | Lattice Monte Carlo, Wilson loops, confinement | Jaffe-Witten, Creutz | BHML spectral gap (Bridge 3), olfactory time dilation |
| BSD | Regulator computations, p-adic heights, Euler systems | Kolyvagin, Kato | Olfactory 5×5 CL matrices (Bridge 6), lattice chain winding |
| Hodge | Motive classification, Tate conjecture, periods | Deligne, Voisin, Andre | Fractal comprehension I/O decomposition (Bridge 7) |
