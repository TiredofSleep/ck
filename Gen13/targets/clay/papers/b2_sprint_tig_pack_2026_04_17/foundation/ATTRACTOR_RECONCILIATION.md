# Attractor Reconciliation
## Foundation Document — Resolving Two Coexisting Conventions for $h$

---

## Purpose

S31-pilot-v1.0 exposed that the program has been operating with two different definitions of the attractor $h$ on Z/10, treated as interchangeable but yielding incompatible canonical constructions. This document:

1. States what $h$ does in the program.
2. Separates the two conventions and their scopes.
3. Audits which convention each prior sprint implicitly used.
4. Identifies where the conventions conflict.
5. Proposes resolution paths.
6. Recommends one path with justification.

No sprint runs until this reconciliation is settled.

---

## 1. What Does $h$ Do?

The attractor $h$ appears in two functional roles in the program:

**Role R1 — structural output.** In the canonical construction $C_0(R, h, \sigma)$, the value of $h$ is used as the *output* the construction assigns to cells that are not covered by the V0 zero-rule or the shell-stability rule. That is: $h$ is what $C_0$ "fills the table with" by default. Every non-V0, non-shell-stable cell gets value $h$.

**Role R2 — structural position.** In the broader discourse of the program, $h$ is identified as a distinguished element of the carrier — e.g., "the largest odd unit," "the $v_2$-maximum element," "the attractor that HARMONY collapses toward." The position of $h$ within $R_n$ is meant to be structurally meaningful, independent of what numerical value gets assigned.

These two roles are in tension. Role R1 treats $h$ as a number that gets stamped into 70–80% of the cells of the canonical table. Role R2 treats $h$ as an element whose structural identity tells us something about the ring. The same symbol $h$ has been doing both jobs without explicit reconciliation.

---

## 2. The Two Conventions in Detail

### Convention A — Published TSML theorem: $h = 7$ on Z/10

**Definition scope.** Applies to the Z/10 local chart. The theorem was calibrated with $h = 7$, which is the unique $v_2$-maximum element (shell 1) among the odd units of $U(10) = \{1, 3, 7, 9\}$. Specifically, $\sigma(7) = v_2(3 \cdot 7 + 1) = v_2(22) = 1$, and among odd units with $\sigma = 1$, there is $\{3, 7\}$; 7 is the larger.

**Verification (audit performed prior to this document).** Under $h = 7$:
- Canonical $C_0$ reproduces the published TSML theorem table on all 92 non-overlay cells.
- All 8 overlay cells are visible (planted value ≠ canonical value) by direct cell-by-cell check.
- Seam detection is unambiguous.

**Theoretical basis.** The theorem is proven for Z/10 with this specific $h$. Other conventions may produce valid constructions, but they are different constructions, not the one in the published proof.

### Convention B — Cross-carrier extension: $h = \max$ odd unit

**Definition scope.** Applies to any ring in the compatibility family. On Z/10, this gives $h = 9$. On Z/14, $h = 13$. On Z/22, $h = 21$. Generally $h_n = n - 1$ for every even carrier in the 29-carrier subfamily.

**Verification (audit performed prior to this document).** Under $h = 9$ on Z/10:
- Canonical $C_0$ matches published TSML on only 19 of 92 non-overlay cells.
- 2 of 8 overlay cells become invisible (planted value = canonical value): $(2, 9)$ and $(9, 2)$ under MAX overlay.
- The resulting construction is a different mathematical object from the published theorem.

**Theoretical basis.** This rule emerged from Sprint 21's prior-free discovery, which reported that "$h = \max$ odd unit" consistently identified a structural position across four tested carriers $\{10, 14, 22, 34\}$ without requiring canonical priors. That was stated as a *discovery invariant* at the time. It was not framed as a redefinition of the canonical construction.

---

## 3. Are These Two Different Objects?

Yes. They are two different maps from rings to distinguished elements:

- Convention A: $\phi_{\text{thm}}(R_n) = $ the specific element chosen by the theorem's construction on $R_n$. On Z/10 this is 7. On other rings it has not been defined in writing — because the theorem has only been proved on Z/10.

- Convention B: $\phi_{\text{ext}}(R_n) = \max\{u \in U(R_n) : u \text{ odd}\}$. This is defined on every ring in the compatibility family. On Z/10 it is 9.

On Z/10 specifically, $\phi_{\text{thm}} = 7$ and $\phi_{\text{ext}} = 9$. These are different. There is no a priori reason they should agree — $\phi_{\text{thm}}$ reflects a theorem's internal choice ($v_2$-maximum among odd units, with tie-break to shell 1), while $\phi_{\text{ext}}$ reflects a different selection rule (max odd unit, irrespective of shell).

The conventions were silently treated as compatible because both agree on the *type of thing* $h$ is (an odd unit of the ring). They disagree on the *specific odd unit*.

---

## 4. Convention Table by Program Context

| Context | Current $h$ rule used | Justification given | Consequences | Conflict status |
|---|---|---|---|---|
| Published Z/10 TSML theorem | $h = 7$ (Convention A) | Theorem calibration; $v_2$-max among odd units | $C_0$ reconstructs 92/100 cells; 3-layer tower completes | Locked: theorem is proven this way |
| Canonical $C_0$ on Z/10 in B1 | $h = 7$ implicitly, via theorem | B1 used published TSML as ground truth | Recovery tested against correct construction | Consistent with A |
| B1 benchmark results | $h = 7$ via TSML as ground truth | Inherited from B1 spec | All B1 metrics at ceiling because canonical priors were correct | Consistent with A |
| Sprint 21 prior-free discovery | $h = \max$ odd unit (Convention B) | Emerged from data without canonical prior; tested across 4 carriers | Identified structural pattern across family | B explicitly proposed here |
| Sprint 25 corridor closure | $h$ via Convention B on 23 carriers | Extended discovery to more carriers | Proved $\{\text{MAX}, \text{MIN}\}$ closure | Consistent with B |
| Sprint 26 shell-recovery | Same as Sprint 25 (B) | Same extension logic | W3-freq ARI recovery | Consistent with B |
| S28-v1.0 basin ratio | $h = \max$ odd unit (B) | Extended to all 29 carriers | Basin ratios computed under B's $h$ values | Consistent with B |
| S29-v1.0 anchored curve | B, with Z/10 anchor $\beta = 0.79$ | Anchor computed under B convention | Entire family measured under B | Consistent with B |
| S30-v1.0 seam topology | Implicit B | All seams computed from noised-$C_0$ under B's $h$ | Empty seams (noise-immunity issue, unrelated to $h$) | Consistent with B |
| S30b-v1.0 detectability | B | Same extractor family | Per-seed seams seed-dependent (sampling issue, unrelated) | Consistent with B |
| S31-pilot-v1.0 Z/10 recovery | **B for $C_0$, A for planted overlay** | First sprint to cross-reference Z/10 theorem overlays against B's canonical | 2 of 8 overlay cells invisible | **Conflict exposed** |

**Observation.** The program has been internally consistent within each "era" (early B1 used A; Sprints 21+ used B) but never explicitly noted the transition. S31-pilot is the first sprint that tried to use both simultaneously — planted overlays defined under A, canonical $C_0$ defined under B — and the conflict surfaced.

---

## 5. Where Does the Conflict Actually Bite?

The conflict bites only in contexts that compare cell-value outputs of two constructions defined under different $h$ conventions. Most sprints only use one construction at a time:

- Sprints computing $\beta(R_n)$ as a scalar from a single $C_0$: one $h$ convention used internally, no conflict.
- Sprints generating noised data from a single generator: one $h$ convention, no conflict.
- Sprints testing empirical-vs-canonical seams: the same $C_0$ defines both "empirical via mode from that generator" and "canonical"; no cross-convention comparison.

The conflict appears only when:

- Planted overlays defined in one convention are compared to canonical cells computed in the other (S31-pilot).
- Future sprints that use the published Z/10 TSML as a reference for recovery on Z/10 while computing "canonical" under the other convention.

Sprints 21–30b are internally consistent because they all used Convention B throughout. They do not change their verdicts under reconciliation. But their relationship to Convention A's theorem — the one proved on Z/10 with $h = 7$ — is looser than was implicitly assumed.

---

## 6. Resolution Paths

### Path A — Bifurcated Program: Two Conventions, Separate Scopes

**The proposal.** Keep both conventions, explicitly scoped:

- $h_{\text{thm}}(R_n)$ is a *theorem-local* object. On Z/10, $h_{\text{thm}} = 7$. On other rings, $h_{\text{thm}}$ is undefined *until a theorem is proved for that ring*.
- $h_{\text{ext}}(R_n) = \max$ odd unit is a *family-heuristic* object, defined on every ring in the compatibility family. On Z/10, $h_{\text{ext}} = 9$.

These are different functions. They must never be substituted for each other without explicit note.

**Consequences.**
- Published theorem is preserved exactly as is; $h = 7$ remains the theorem's choice.
- Cross-carrier work continues under $h_{\text{ext}}$, understood as an extension heuristic, not a theorem.
- Any sprint that compares Z/10 theorem objects (like the published seam) to canonical constructions must use $h_{\text{thm}} = 7$. Any sprint that tests cross-carrier patterns uses $h_{\text{ext}}$ consistently across the family.
- The apparent coincidence of Sprint 21's finding (attractor = max odd unit = $h_{\text{ext}}$) with the theorem's $h_{\text{thm}}$ on Z/10 is explicitly *not* a coincidence in mathematical content — they are different elements that merely both happen to be odd units of Z/10.

**Strengths.**
- Preserves all prior results without reinterpretation.
- Theorem retains its integrity.
- Extension heuristic retains its cross-carrier evidence (Sprint 21's 4-carrier discovery, Sprint 25's 23-carrier closure).
- Makes the convention explicit in all future specs.

**Weaknesses.**
- Two objects to track. Requires clear labeling in every spec.
- The extension heuristic becomes formally a *different object* from the theorem on Z/10, which is philosophically awkward for a transport program — the "anchor" is not actually the same type of thing as the extension.

### Path B — Unified Rule: Pick One, Backpropagate

**The proposal.** Decide that one convention is the *real* attractor rule, and revise the other's use retroactively.

**Sub-path B1: Unify under $h_{\text{thm}}$ (theorem-calibrated).** Retroactively reinterpret Sprints 21, 25, 26, 28, 29, 30, 30b as having used the wrong $h$. Recompute where needed. The advantage: theorem integrity is preserved as primary. The cost: extensive recomputation and the possibility that Sprint 21's cross-carrier pattern (which motivated $h = \max$ odd unit) dissolves under a different rule, meaning Sprint 21's finding may not survive.

**Sub-path B2: Unify under $h_{\text{ext}}$ (family-heuristic).** Revise the Z/10 local theorem itself to use $h = 9$. Reprove. The advantage: single consistent rule across the program. The cost: the published theorem is replaced, and the new construction at $h = 9$ does not reconstruct the published 73/17/4/2/2/2 cell counts — it produces a different table entirely. The published theorem would need to be retired or reframed as a specific case of a more general family.

**Strengths.**
- Single convention throughout the program.
- Conceptual cleanness.

**Weaknesses.**
- Either sub-path is expensive.
- B1 risks dissolving the transport program's best cross-carrier evidence.
- B2 discards a proven theorem.

### Path C — Explicit Transport Program, Separate Theorem

**The proposal.** Formally acknowledge that the "transport program" and the "Z/10 local theorem" are separate projects with different goals:

- **Local theorem project:** Z/10 TSML, $h = 7$, proved. This is a specific result about a specific ring. No cross-carrier claims.
- **Transport program:** cross-carrier investigation under $h_{\text{ext}}$. Asks whether rule-shapes and invariants generalize across the compatibility family. Not required to reproduce the Z/10 theorem exactly on any other carrier.

The two projects share conceptual language ("canonical construction," "attractor," "seam," "shell") but use it under explicitly different conventions.

**Consequences.**
- Same mathematical content as Path A, but framed at a higher level.
- Any sprint must declare which project it belongs to.
- The "grammar transfer" question the program is really asking becomes: *does the transport program's structure behave like the theorem project's structure on Z/10?* This is a relational question, not an identity claim.
- The "physics" question is explicitly deferred and decoupled from both.

**Strengths.**
- Matches what the program has actually been doing.
- Removes the pretense that the theorem and the transport heuristic are the same object.
- Makes the deeper question — "do we see structural resemblance between a theorem and a heuristic extension?" — explicit and testable.
- Preserves every prior result within its correct scope.

**Weaknesses.**
- Formally separates two things that the program emotionally wants to be one thing.
- Requires rewriting some prior documentation to reflect scoping.

---

## 7. Recommendation

**Path C is the cleanest going forward.**

The path A / path C distinction is small in practice — both preserve both conventions scoped separately. Path C is preferred because it makes the *epistemic structure* of the program explicit, not just the notation. It says out loud what has been implicitly true since Sprint 21: there is a theorem on Z/10, and there is a cross-carrier investigation. They share vocabulary and inspiration but are formally different objects. This is in fact what the "framing reset" in `TSML_IS_NOT_PHYSICS.md` already argued at a higher level — Z/10 is a local chart, the transported object is *grammar*, not the table.

Adopting Path C operationalizes that framing. Every sprint gets a label: "local theorem" or "transport program." The attractor convention follows from the label. S31-pilot's conflict would have been caught at spec-design time if the pilot had been required to declare which project it belongs to — and the declaration would have forced the spec-writer to decide whether the planted overlays (theorem-project objects) should be tested against a canonical $C_0$ also computed in the theorem project ($h = 7$) or in the transport program ($h = \max$ odd unit).

**Under Path C, a revised S31-pilot would be simple:** declare the sprint as a local-theorem-project recovery test, use $h = 7$, recompute the canonical $C_0$, plant the theorem's overlays, and run. The auditable expectation is that all 8 overlay cells are detectable and recovery should be near-perfect at clean noise. That is the sprint S31-pilot was supposed to be.

**Paths A and B are available but inferior.** Path A is equivalent to C at the technical level but weaker at the framing level. Path B1 destroys cross-carrier evidence; Path B2 discards a proven theorem. Neither is worth the cost.

---

## 8. What Path C Requires in Practice

If Path C is adopted:

1. **Spec headers going forward must declare project scope.** Every new spec begins with a line stating "local theorem project" or "transport program," and the attractor convention follows deterministically.

2. **Prior sprints get retroactive scope tags.** Sprints 21, 25, 26, 28, 29, 30, 30b are tagged *transport program*; B1, B2, B3, and the Z/10 theorem work are tagged *local theorem project*.

3. **The split document `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md` gains a clarifying preamble.** It already distinguishes Z/10-local from transportable, but the preamble should now explicitly state that the left column belongs to the local theorem project and the right column belongs to the transport program.

4. **Cross-project sprints require explicit bridge specs.** S31-pilot attempted a cross-project sprint without declaring so. A future cross-project sprint (e.g., "do the theorem's overlays reappear in the transport program's empirical data?") would need explicit rules for how the bridging is done, which convention governs which object, and what a conflict means.

5. **The `ATTRACTOR_RECONCILIATION.md` document (this one) becomes a reference.** Any spec that touches $h$ points back to this document for the convention used.

No prior sprint's verdict changes under Path C. The scope tags are documentation, not recomputation.

---

## 9. Integrity Statement

This document resolves a real ambiguity in the program's foundations. The ambiguity was present but invisible for many sprints because sprints stayed within one convention. S31-pilot surfaced it at the first cross-convention sprint, which is exactly what a well-designed pre-registration process should do: catch foundation bugs before they accumulate.

Reconciliation does not constitute "rescue" of S31-pilot. Its FAIL verdict stands, attributed explicitly to the convention mismatch now documented. A successor pilot under Path C would be a new sprint (S31-pilot-v2.0 or a differently named test) with a new pre-registration. This document enables that successor but does not authorize it — that is a separate decision.
