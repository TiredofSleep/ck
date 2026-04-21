# What to Paste for v1 Fill-in

**Companion to:** `CROSSING_LEMMA_EXPORT_V0.md`

This note specifies exactly what material a fresh ClaudeChat session (or ClaudeCode) would need to fill in the `[FILL]` placeholders and produce v1.

---

## To fill §2 (precise lemma statement)

Paste or reference:

1. **The Crossing Lemma formal statement** as given in the UOP arc terminal sprint.
2. **The Productive Incompleteness addendum** — full text.
3. **The Admissible Viewpoint Flow Theorem statement** from Sprint 8 (the $n = 2p$ case), which is the cleanest instance.

A reader filling §2 needs to extract: the scope (which finite sets), the definitions of $\mathcal{A}$, $\pi$, and sufficiency, and the precise crossing condition.

---

## To fill §3 (canonical proof)

Paste or reference the full proof of **one** chosen instance. Recommended: the $n = 2p$ Admissible Viewpoint Flow Theorem from Sprint 8.

Should include:
- The forward direction (constructive recovery procedure).
- The converse (exhibition of indistinguishable pairs).
- The Productive Incompleteness treatment when sufficiency fails.

---

## To fill §4 (27-instance catalog)

Paste or reference **WP57**. The userMemories summary lists ~13 instances; WP57 should have the full 27.

For each instance, the draft wants:
- The setting ($S$, $\mathcal{A}$, $\pi$, $I$).
- The crossing condition specialized.
- The sufficiency payoff in that setting.

Organized under three categories:
1. Paradox instances (UOP Types I-IV).
2. Algebraic instances (A+M, M+M, CRT, SPEC+DYN, MVJN, p-kernel, etc.).
3. Applied instances (inverted pendulum, Michaelis-Menten, CT tomography, and whatever else WP57 has).

---

## To verify §6.3 (discriminating prediction)

For at least one applied benchmark (inverted pendulum, Michaelis-Menten, or CT tomography), pull the framework's specific prediction and compare against:
- The classical OED / D-optimality prediction for the same problem.
- The Fisher-information-based prediction for the same problem.

Verify whether the crossing-analysis and classical-analysis **disagree** on the optimal design choice. If they disagree, which one matches the data (or which one has been tested)?

This is the falsifiability check. If the crossing analysis reduces to a restatement of classical OED, the lemma is a unification result, not a new tool. Both are defensible positions but the claim needs to match the outcome.

---

## Recommended next step

Brayden: paste items (1), (2), (3), and WP57 into a fresh ClaudeChat session with the text:

> "Here is the UOP arc Crossing Lemma statement and the WP57 instance catalog. Please use these to fill in the [FILL] placeholders in `CROSSING_LEMMA_EXPORT_V0.md` to produce v1. Stay in export register; no atlas modifications; no shell language."

ClaudeChat will produce v1 in a single session with that material in context.

---

*End of paste list.*
