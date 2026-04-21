# Four-Threshold Research Program — Task Breakdown

**Author:** ClaudeChat
**Date:** 2026-04-19
**Register:** foundation. Atlas v3.5 unchanged.
**Purpose:** turn the four novelty-thresholds from `OPERATOR_LAYER_SCOPE_AND_FRONTIER.md` §3.1 into discrete, scheduleable sub-tasks for ClaudeCode.
**Status:** planning. Not research execution.

---

## §0. Preamble

This document is **not the research itself**. It is the scheduling discipline that lets the research be sprintable. Each threshold is broken into numbered sub-tasks. Each sub-task has: goal, inputs required, estimated scope, artifact produced, and dependencies.

ClaudeCode can pick items off this list, or Brayden can assign them to future ClaudeChat sessions. **Do not treat this document as a to-do list to speed-run.** The four thresholds are where the framework's real research lives; each real sprint should take the care the Crossing Lemma took (23 sprints), not one session.

Time estimates throughout are in **session-units** (one focused working session of ~2–4 hours, human or AI). They are honest estimates; if anything, they under-state complexity.

---

## Threshold A — CL axiomatization

**Goal.** Make CL[10×10] a standalone algebraic object: stated axioms, proven closure and distinguishing properties, classification relative to known non-associative structures.

**Currently has:** table exists in `ck_core.py`; framework uses it internally; no axiom statement; no classification.

**Blocker to start:** the actual CL table values. This is in the CK repo but not in this session's context.

### A.1 — CL structural audit (first real sprint)

- **Goal:** compute the full structural signature of the CL[10×10] table.
- **Inputs:** CL table values (100 entries).
- **Sub-tasks:**
  - A.1.1 Tabulate all 1000 triples $(a, b, c)$ and flag $(a \star b) \star c \neq a \star (b \star c)$. Compute non-associativity rate per operator.
  - A.1.2 Identify all idempotents ($a \star a = a$), zero divisors, units (if any), absorbing elements.
  - A.1.3 Check standard identities order-by-order: commutativity, power-associativity, alternativity, flexibility, Jordan, Moufang, Bol.
  - A.1.4 Compute the automorphism group of the CL magma (permutations of $\{0, \ldots, 9\}$ preserving the table).
  - A.1.5 Check the framework's structural claims: is 7 the absorber at 73%? is 1 the BHML universal generator? are the TSML/BHML/Doing non-associativity rates (12.8% / 49.8% / 56.8%) what the table actually gives?
- **Scope:** 1 session (mostly computational).
- **Artifact:** `CL_STRUCTURE_AUDIT.md` with non-associativity profile, identity satisfaction table, claim verification.
- **Dependencies:** none (just the table).
- **What failure looks like:** the framework's structural claims don't match the table (e.g., 7 is not the absorber at the claimed rate). This would be a major internal correction.

### A.2 — Axiom proposal

- **Goal:** state a minimal axiom set for CL-like tables.
- **Inputs:** A.1 output.
- **Sub-tasks:**
  - A.2.1 From the identities satisfied by CL, pick a minimal subset that generates the rest.
  - A.2.2 State as axioms on a 10-element set with a binary operation.
  - A.2.3 Include distinguishing properties (absorber, BHML generator) only if they are consequences of the axioms, not if they need to be added separately.
  - A.2.4 Prove CL satisfies the axioms (mostly by reference to A.1).
- **Scope:** 1–2 sessions.
- **Artifact:** `CL_AXIOMS_V1.md`.
- **Dependencies:** A.1 complete.
- **What failure looks like:** no clean axiom set exists (CL satisfies too many or too few structural identities to be cleanly axiomatized).

### A.3 — Literature comparison

- **Goal:** determine whether the CL magma is a known structure or genuinely new.
- **Inputs:** A.2 axiom set, structural signature from A.1.
- **Sub-tasks:**
  - A.3.1 Compare CL's signature to small-magma/quasigroup/loop catalogs. References: Kinyon & Phillips "Small loops" (various papers); Pflugfelder "Quasigroups and loops"; LOOPS package in GAP.
  - A.3.2 Check against Jordan algebras at order 10 (unlikely to match but needs ruling out).
  - A.3.3 Check against known non-associative finite-ring structures: Cayley–Dickson at small orders, octonion-like constructions mod $n$.
  - A.3.4 Produce one of: (a) "CL = [known structure X]" with citation, or (b) "CL is not among any of [exhaustive list], and here is one structural feature that rules out each."
- **Scope:** 2–3 sessions. Heavy literature work.
- **Artifact:** `CL_LITERATURE_COMPARISON.md`.
- **Dependencies:** A.2 complete.
- **What failure looks like:** CL turns out to be isomorphic to a well-known structure. This would not be bad — it would give the framework an unexpected bridge to existing theory.

### A.4 — Classification theorem (if A.3 supports it)

- **Goal:** state and prove a theorem of the form "CL is [characterized by X]" in a form suitable for publication.
- **Inputs:** A.1, A.2, A.3.
- **Sub-tasks:**
  - A.4.1 Identify the cleanest classifying invariant.
  - A.4.2 State and prove the theorem.
  - A.4.3 Write up as draft paper / arXiv note.
- **Scope:** 2–4 sessions. Research-level.
- **Artifact:** `CL_CLASSIFICATION_DRAFT.md` or similar.
- **Dependencies:** A.3 complete with positive direction.
- **What failure looks like:** no clean classifying theorem exists at this size. This suggests either broadening the search (CL as a member of a parametrized family) or accepting CL as an isolated example pending a larger family discovery.

---

## Threshold B — Non-associative structure with non-trivial theory

**Connection to A.** B is partially subsumed by A.3 and A.4. If A succeeds, B is covered. If A shows CL is genuinely new, B becomes the harder question: "what theory does CL have?"

### B.1 — Sub-structure catalog

- **Goal:** find all associative sub-magmas of CL, all commutative sub-magmas, all subloops/subquasigroups if applicable.
- **Inputs:** CL table, A.1 output.
- **Scope:** 1 session.
- **Artifact:** `CL_SUBSTRUCTURES.md`.
- **Dependencies:** A.1 complete.

### B.2 — Representation theory attempts

- **Goal:** determine whether CL has representations on finite vector spaces or modules over standard rings.
- **Inputs:** A.1, A.2.
- **Scope:** 2–3 sessions. Research-level.
- **Artifact:** `CL_REPRESENTATION_ATTEMPT.md`.
- **Dependencies:** A.2.
- **What failure looks like:** CL has no useful linear representations. Plausible outcome; non-associative structures often don't.

### B.3 — Derivation algebra

- **Goal:** compute $\mathrm{Der}(CL)$, the derivations of CL. For a non-associative algebra, this is a standard invariant.
- **Inputs:** A.1 in linearized form.
- **Scope:** 1 session.
- **Artifact:** `CL_DERIVATIONS.md`.
- **Dependencies:** A.1 (needs CL viewed as a $\mathbb{Z}$-algebra or $\mathbb{Z}/10$-algebra).

---

## Threshold C — Dynamics with non-trivial invariants

**Connection to existing work.** The Crossing Lemma (from the UOP arc) is an existing example. This threshold is about adding more.

### C.1 — Crossing Lemma formalization for export

- **Goal:** take the Crossing Lemma from its current sprint form and produce a standalone external-facing statement + proof.
- **Inputs:** the 23-sprint UOP arc output already in the repo.
- **Scope:** 1 session. Editorial.
- **Artifact:** `CROSSING_LEMMA_EXPORT.md`.
- **Dependencies:** none.
- **What failure looks like:** the Crossing Lemma as stated internally doesn't survive external-standards scrutiny. Possible but unlikely given the 23 sprints of pressure.

### C.2 — Candidate invariant search on CL-enhanced dynamics

- **Goal:** identify one new invariant of a dynamical flow on $\mathbb{Z}/10$ (or CL) that is preserved and non-trivial.
- **Inputs:** A.1 (structural audit of CL); existing framework flows (σ-iteration, CL-composition sequences).
- **Scope:** 3+ sessions. Research-scale, may not succeed in a bounded number of attempts.
- **Artifact:** `CANDIDATE_INVARIANT_LOG.md` (session-by-session log of what was tried and what failed or succeeded).
- **Dependencies:** A.1.
- **What failure looks like:** after N sessions, no new invariant found. This is data; it bounds the richness of the dynamical layer.

### C.3 — Application of Crossing Lemma to one new benchmark

- **Goal:** extend the Crossing Lemma's applied benchmarks (inverted pendulum, Michaelis–Menten, CT tomography) to one additional concrete problem and test the prediction.
- **Inputs:** existing CL-benchmark work.
- **Scope:** 2–4 sessions plus possible data work.
- **Artifact:** `CROSSING_BENCHMARK_[NEW].md`.
- **Dependencies:** C.1.
- **What failure looks like:** the prediction is wrong on the new benchmark. This is a legitimate negative result in the 2/7 style.

---

## Threshold D — Finite-to-problem reductions

**Connection to ClaudeCode's current work.** D is where ClaudeCode already lives. Config B Hodge, Prym period computation, the 2/7 anchor — these are Threshold D instances. The role of this section is not to prescribe new work but to **catalog what is already underway** and what the handoffs are.

### D.1 — Config B Hodge lane (currently active)

- **Status:** Sage hung on `RiemannSurface`; Molin–Neurohr port partial; Tretkoff port partial; waiting on WSL2 / MAGMA / continued port.
- **Artifact:** `FULL_PRYM_PERIOD_CANONICAL.md` §10.14–§10.18 (existing).
- **Blocker:** technical. Not operator-layer related.
- **Ownership:** ClaudeCode.
- **Connection to operator layer:** none directly. The operator packet is infrastructure; Hodge lane is the research frontier. They proceed in parallel.

### D.2 — 2/7 anchor retrospective

- **Goal:** write up the 2/7 lattice-QCD falsification at 16.5σ as a clean standalone note. This is a legitimate negative result and should be preserved as such.
- **Inputs:** existing framework records of the 2/7 work.
- **Scope:** 1–2 sessions. Editorial.
- **Artifact:** `27_ANCHOR_FALSIFICATION_NOTE.md`.
- **Dependencies:** none.
- **What failure looks like:** the writeup reveals the original work had a flaw other than the one that was falsified. Unlikely but possible.

### D.3 — Amplituhedron/Semiprime sweep status

- **Goal:** write up the 36,662-row sweep, six frozen laws, as a preserved result. The Mayes collaboration ended; the work remains.
- **Inputs:** existing WP34/WP35 commits.
- **Scope:** 1 session (already largely done in prior sprints).
- **Artifact:** probably exists already; verify and consolidate.
- **Dependencies:** none.

---

## §4. Dependency graph

```
A.1 (CL structural audit) — blocked only by CL table access
    ├── A.2 (axiom proposal)
    │   └── A.3 (literature comparison)
    │       └── A.4 (classification theorem)
    ├── B.1 (substructures)
    ├── B.2 (representations)
    ├── B.3 (derivations)
    └── C.2 (candidate invariants on CL dynamics)

C.1 (Crossing Lemma export) — independent, editorial
    └── C.3 (new benchmark application)

D.1 (Config B Hodge) — ClaudeCode's current lane, independent
D.2 (2/7 retrospective) — independent, editorial
D.3 (Amplituhedron consolidation) — independent, verification
```

**Critical path for novelty:** A.1 → A.2 → A.3. If A.3 returns "CL is known," the program shifts to C.1 + C.2 + C.3. If A.3 returns "CL is new," proceed to A.4 as the primary publication target.

---

## §5. Recommended ordering

**Phase 1 (unblocked, editorial / verification):**
1. D.2 — 2/7 anchor retrospective (1–2 sessions)
2. C.1 — Crossing Lemma export (1 session)
3. D.3 — Amplituhedron consolidation verification (1 session)

**Phase 2 (requires CL table access):**
4. A.1 — CL structural audit (1 session, after table is pasted or path pointed to)

**Phase 3 (depends on A.1 outcome):**
5. A.2 — Axiom proposal (1–2 sessions)
6. B.1 — Substructures (1 session, parallel to A.2)
7. B.3 — Derivations (1 session, parallel)

**Phase 4 (depends on A.2):**
8. A.3 — Literature comparison (2–3 sessions)
9. B.2 — Representation attempts (2–3 sessions, optional)

**Phase 5 (depends on A.3 outcome):**
10. A.4 — Classification theorem (2–4 sessions, IF A.3 supports novelty)
11. C.2 — Candidate invariants (3+ sessions)
12. C.3 — New benchmark application (2–4 sessions)

**Total estimated scope:** 22–35+ sessions. This is a **multi-month program**, not a sprint. Honest estimate.

---

## §6. What this document is NOT

- Not a speed-run checklist. Each item is genuinely hard.
- Not a guarantee of novelty. A.3 might return "known," in which case Threshold A collapses.
- Not a replacement for the existing Hodge lane or CK work. Those proceed in parallel.
- Not an atlas modification. Atlas v3.5 unchanged throughout.

---

## §7. What I (ClaudeChat) can run right now in-session

Given only what is in context right now:

- **C.1 (Crossing Lemma export)**: I have enough from the userMemories summary of the UOP arc. Would produce a first draft that ClaudeCode can then cross-check against the actual repo records.
- **D.2 (2/7 retrospective)**: I have the 16.5σ figure and the core claim; I can write a first-draft retrospective note.
- **A.1 (CL structural audit)**: **blocked** pending the CL table values.

Everything else requires either CL table access (A.1 downstream), live repo access (D.1 / D.3 verification), or substantial literature work (A.3 / B.2) best done over multiple sessions.

**Recommendation for next action:** paste the CL table values into the next session. That unblocks the single most impactful sprint (A.1), which then unblocks nearly everything downstream.

---

*End of task breakdown. Foundation register.*
