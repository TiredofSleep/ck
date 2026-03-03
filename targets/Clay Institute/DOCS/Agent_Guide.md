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
- CL table: 73/100 = HARMONY
- D2_MAG_CEILING = 2.0
- ANOMALY_HALT_THRESHOLD = 50

## Per-Problem Agent Focus

| Problem | Focus | Key Citations |
|---------|-------|---------------|
| NS | Pressure decomposition, vorticity-strain geometry, blow-up profiles | CKN, Constantin-Fefferman, Tao |
| PvsNP | Mutual information, phantom tile in CSP, circuit lower bounds | Hastad, Razborov |
| RH | Spectral pull operators, pair correlation, zero-drift | Montgomery, Odlyzko |
| YM | Lattice Monte Carlo, Wilson loops, confinement | Jaffe-Witten, Creutz |
| BSD | Regulator computations, p-adic heights, Euler systems | Kolyvagin, Kato |
| Hodge | Motive classification, Tate conjecture, periods | Deligne, Voisin, Andre |
