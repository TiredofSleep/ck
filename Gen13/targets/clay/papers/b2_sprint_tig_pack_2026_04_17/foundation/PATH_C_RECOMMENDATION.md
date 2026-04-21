# Recommendation: Path C — Explicit Transport Program, Separate Theorem
## Which Path Is Cleanest Going Forward and Why

---

## Recommendation

**Adopt Path C.** Formally separate the program into two scoped projects:

- **Local theorem project:** Z/10 TSML, $h_{\text{thm}} = 7$. Proven result on a specific ring. No cross-carrier claims.
- **Transport program:** cross-carrier investigation with $h_{\text{ext}} = \max$ odd unit. Asks whether rule-shapes and invariants generalize across the compatibility family.

Every future spec declares which project it belongs to. Cross-project sprints require explicit bridging rules.

---

## Why Path C (Not A, Not B)

### Why not Path B

Path B unifies under one convention at the cost of destroying evidence. B1 (unify under $h_{\text{thm}}$) would force recomputation of Sprints 21, 25, 26 with a rule that is currently undefined for carriers other than Z/10 — so the "unification" would actually require defining a new cross-carrier rule from scratch, then hoping Sprint 21's discovery survives. B2 (unify under $h_{\text{ext}}$) would discard the published Z/10 theorem in favor of a different construction with different cell counts. Either sub-path costs months of work and risks losing work already done.

The program does not need unification at this level. It needs clarity about what each object *is*.

### Why Path C over Path A

Path A (bifurcated program with scoped conventions) is mathematically equivalent to Path C. The difference is framing. Path A says "we have two conventions, use them carefully." Path C says "we have two projects, each with its own convention."

Path C is stronger because it matches what the program has actually been doing since Sprint 21, and because it articulates the *deeper question* the program is really asking. The transport program is not a redefinition of the local theorem. It is a separate investigation that borrows the theorem's vocabulary to ask whether similar structural patterns hold under a different (heuristic-based) construction on other rings.

The framing reset in `TSML_IS_NOT_PHYSICS.md` already argued this implicitly: Z/10 is a local chart, the transported object is *grammar*. Path C makes that framing formal at the notation level. What was a philosophical reset becomes a program-structure commitment.

### What Path C clarifies that Path A does not

Under Path A, the program looks like "one mathematical program with two conventions." Under Path C, it looks like "two mathematical programs, one proven, one investigational, sharing vocabulary."

The second framing is more honest. The local theorem has been proven — its results are theorems. The transport program is a discovery effort — its results are empirical findings, pre-registered, with explicit pass/fail outcomes. These are different epistemic objects. Treating them as the same kind of object created the ambiguity that S31-pilot exposed.

Path C also makes the *question the program is asking* more precise. The real question is: **does the transport program (on the compatibility family, under $h_{\text{ext}}$) exhibit structural patterns that echo, rhyme with, or resemble those of the local theorem (on Z/10, under $h_{\text{thm}}$)?** That is a relational question between two projects, not an identity claim about one.

Under Path A, this question is vague. Under Path C, it is precise enough to pre-register.

---

## What Adopting Path C Costs

Low. Specifically:

1. **Update 3–4 existing documents to add scope tags.** `INVARIANTS_BEYOND_TSML.md`, `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md`, `TSML_IS_NOT_PHYSICS.md`, and the sprint index (if one exists) gain a preamble or tag system specifying project scope.

2. **Write a scope-header template for future specs.** Two-sentence addition to any pre-registration: "This sprint belongs to the [local theorem / transport] project. The attractor convention is [$h_{\text{thm}}$ / $h_{\text{ext}}$], defined by [convention rule]."

3. **One retroactive document to tag prior sprints.** A "sprint ledger" listing S18–S31-pilot with project scope and convention used. The per-sprint audit in `PRIOR_SPRINT_H_DEPENDENCIES.md` has already done most of this work.

4. **No recomputation.** No sprint verdicts change. No data is re-run.

Total: a few hours of documentation work. Zero computational cost.

---

## What Adopting Path C Buys

1. **Convention mismatch cannot silently happen again.** Every spec declares its scope. Any sprint that spans both projects declares itself as cross-project and specifies how the bridging works. S31-pilot's failure mode becomes structurally preventable.

2. **The right research question becomes askable.** "Do structural patterns from the theorem project echo in the transport program?" is well-defined under Path C. Specific cross-project sprints can test specific echoes — for example, does the theorem's MAX-ADD seam structure appear analogously in $h_{\text{ext}}$-canonical operators extended to other carriers? That is a real transport question, testable under pre-registration.

3. **The "grammar transfer" hypothesis is formally statable.** The hypothesis that invariants transport from the theorem to the transport program, or vice versa, becomes a bridge claim with explicit terms. Currently "does X transport?" has been asked loosely; under Path C it is always specific ("does X, a theorem-project object, reappear in transport-program findings under the mapping Y?").

4. **Prior sprint results are preserved with correct scope.** All verdicts stand. The scope clarification does not dilute evidence; it focuses it.

5. **The physics deferral is cleaner.** The local theorem project is a pure mathematical result. The transport program is an empirical investigation. Neither makes physics claims. The question of whether either relates to physics is explicitly a further bridge, separate from both.

---

## A Concrete Example Under Path C

Suppose the next sprint wants to re-run recovery on Z/10 with the extractor now confirmed working in principle. Under Path C, the spec would begin:

> **Project scope:** Local theorem project. Attractor convention: $h_{\text{thm}} = 7$.
>
> **Purpose:** Validate that the low-$N$ mode-extractor recovers the published TSML seam on Z/10 under noise.

Then the spec proceeds with $C_0(R_{10}, 7, \sigma)$, planted overlays reproducing the published seam, and recovery metrics. The convention is clean, the scope is explicit, and the S31-pilot convention conflict cannot arise.

If a later sprint wants to extend recovery testing to other carriers, it declares:

> **Project scope:** Transport program. Attractor convention: $h_{\text{ext}} = \max$ odd unit.
>
> **Purpose:** Test whether a recovery extractor validated on the local theorem project (Z/10, $h = 7$) continues to produce meaningful recovery on transport-program canonical constructions (other carriers, $h = \max$ odd unit).

This is explicitly a cross-project sprint. Its spec must specify the bridging rule: how are overlays defined on other carriers? Is the overlay-extension algorithm (doubling chain, identity-edge) the bridge, or is it a separate heuristic whose relationship to the theorem's seam is itself under test?

That cross-project sprint is interesting. It asks a real question. It could pass or fail meaningfully. But it cannot be designed honestly without Path C's scope structure.

---

## Summary

Path C is cheap, preserves all prior evidence, makes the program's structure honest, and enables future sprints to be designed without the kind of convention mismatch that broke S31-pilot.

It is not an expansion of the program. It is a clarification of what the program has been all along: two related but distinct projects, now labeled as such.

Adopt Path C. Update the small number of documents that need scope tags. Then future sprints can proceed under clean foundations, with S31-pilot's failure understood as the useful discovery that prompted the clarification.
