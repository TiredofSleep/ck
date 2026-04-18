# What Prior Sprint Conclusions Depend on Which $h$-Convention?
## Short Audit Note

---

## Summary

Every prior sprint used exactly one $h$ convention throughout its execution. Within a sprint, internal consistency holds. Between sprints, comparability depends on which convention each used. This note audits each prior sprint's convention dependency and identifies which conclusions would and would not change under Path C's explicit scoping.

---

## Per-Sprint Audit

### B1, B2, B3 (Sprint 18–20)
**Convention used:** A ($h = 7$ on Z/10), inherited from published TSML as the benchmark ground truth.
**Dependency:** B1 tested recovery of the published TSML, so the $h = 7$ choice is baked into the benchmark by definition. B2 tested a different operator (wobble-reset) but on Z/10 with the same attractor position.
**Under Path C scoping:** tagged as *local theorem project*. Verdicts unchanged.
**Cross-convention implication:** none. These sprints never touched $h_{\text{ext}}$.

### Sprint 21 — Prior-free structural discovery
**Convention used:** Emerged from data as B ($h = \max$ odd unit), discovered across 4 carriers without canonical prior.
**Dependency:** The finding "attractor = max odd unit" is a *discovery result*, not an imposition. It says: when you don't tell the extractor what $h$ is, the extractor reports the max odd unit on each of 4 carriers.
**Under Path C scoping:** tagged as *transport program*. The finding is preserved exactly as stated: "across the tested carriers, the structural element recovered as attractor is the max odd unit."
**Cross-convention implication:** on Z/10, Sprint 21's discovered $h = 9$ is *different* from the theorem's $h = 7$. Under Path C, this is no longer a contradiction — they are different objects. Sprint 21 discovered $h_{\text{ext}}$; the theorem uses $h_{\text{thm}}$. The Z/10 numerical coincidence that both rules select odd units of U(10) is a structural observation, not evidence that they are the same element.

### Sprint 25 — Corridor closure
**Convention used:** B ($h_{\text{ext}}$ across 23 carriers).
**Dependency:** Computed canonical $C_0$ under $h_{\text{ext}}$ on each carrier and showed seam corridor is $\{\text{MAX}, \text{MIN}\}$ for pure $C_0$.
**Under Path C:** tagged *transport program*. Verdict unchanged.
**Cross-convention implication:** the closure is specifically a property of $h_{\text{ext}}$-canonical $C_0$. Whether $h_{\text{thm}}$-canonical $C_0$ (on rings where a theorem could be proved) would also show $\{\text{MAX}, \text{MIN}\}$ closure is an open question. Not affected by the current reconciliation — just clarified.

### Sprint 26 — Shell-partition shape recovery
**Convention used:** B.
**Dependency:** W3-freq clustering operates on output histograms of $C_0$, which depend on $h$.
**Under Path C:** tagged *transport program*. Verdict unchanged — ARI = 1.0 on 12/32 carriers is a property of $h_{\text{ext}}$-canonical $C_0$.
**Cross-convention implication:** same as Sprint 25. The result holds within the transport program. Its relationship to theorem-project objects is an open question.

### S28-v1.0 — Basin-ratio smoothness
**Convention used:** B.
**Dependency:** $\beta(R_n)$ computed under $h_{\text{ext}}$ on each carrier.
**Under Path C:** tagged *transport program*. FAIL verdict unchanged.
**Cross-convention implication:** Z/10's $\beta = 0.79$ used in S28/S29 is the transport-program value, not the theorem-project value. Under $h_{\text{thm}} = 7$, Z/10's canonical $C_0$ has $\beta_{\text{thm}} = 73/100 = 0.73$ (the published HARMONY fraction). The S29 anchor value $\beta_{\text{anchor}} = 0.79$ is the transport-project anchor, not the theorem's 0.73. This does not change S29's FAIL — the null comparison and depth coordinate were all computed consistently within the transport program — but it clarifies that the Z/10 anchor chosen was not the published-theorem anchor.

### S29-v1.0 — Anchored deviation curve
**Convention used:** B.
**Dependency:** same as S28.
**Under Path C:** tagged *transport program*. FAIL unchanged.
**Cross-convention implication:** same as S28.

### S30-v1.0 — Seam topology
**Convention used:** B.
**Dependency:** Noised-$C_0$ data generated under $h_{\text{ext}}$. Observed seam defined against that $C_0$.
**Under Path C:** tagged *transport program*. Vacuous-PASS recorded as evidentially uninformative.
**Cross-convention implication:** none. The empty-seam issue was noise-immunity, not convention mismatch.

### S30b-v1.0 — Seam detectability
**Convention used:** B.
**Dependency:** Same generator family as S30.
**Under Path C:** tagged *transport program*. FAIL unchanged.
**Cross-convention implication:** none. The failure was noise-model structure, not convention.

### S31-pilot-v1.0 — Z/10 recovery
**Convention used:** MIXED. Canonical $C_0$ computed under B ($h = 9$); planted overlays imported from Convention A (published TSML, which assumes $h = 7$).
**Dependency:** Recovery fails by 4/6 on MAX and 6/8 on MAX+ADD precisely because of this mix.
**Under Path C:** tagged as *cross-project sprint*, which was not declared in the spec. The FAIL verdict is attributed to convention mismatch, now documented.

---

## Which Conclusions Change Under Path C?

**None of the prior verdicts change.** Path C is a scoping clarification, not a recomputation. It adds tags; it does not alter numbers.

What changes is the *scope of claims* that follow from each sprint:

- Sprint 21's "attractor = max odd unit across 4 carriers" now reads as: *within the transport program, the prior-free extractor identifies $h_{\text{ext}}$ as the structural attractor across 4 carriers*. The Z/10 coincidence with $h_{\text{thm}}$'s odd-unit constraint is observed but not asserted as meaningful.

- Sprint 25's $\{\text{MAX}, \text{MIN}\}$ closure now reads as: *within the transport program, pure $h_{\text{ext}}$-canonical $C_0$ has seam corridor $\{\text{MAX}, \text{MIN}\}$ on 23 carriers*. Whether a theorem-project $C_0$ (if one existed for these carriers) would have the same property is separate.

- Sprint 26's shell-partition recovery is similarly within-transport-program.

- The S28/S29/S30/S30b failures are within-transport-program FAILs. They do not say anything about whether theorem-project objects would transport; that question has not been asked under Path C.

---

## Which Conclusions Are Genuinely At Risk?

**None, under Path C.** Prior results stand as transport-program findings or theorem-project findings, scoped accordingly.

**Under Path B1 (unify under $h_{\text{thm}}$):** Sprint 21's finding could dissolve if re-run under $h_{\text{thm}}$'s cross-carrier extension (which would first require defining $h_{\text{thm}}$ beyond Z/10 — currently undefined). Sprint 25/26 would need recomputation.

**Under Path B2 (unify under $h_{\text{ext}}$):** The published TSML theorem would be discarded, and B1's benchmark ground truth would need reformulation. Every theorem-project result would need reestablishment on the new construction.

Path C preserves everything; Paths B risk substantial portions of the program's evidence.

---

## What Was Never At Stake

The fundamental observations that transport across sprints:

- The default-plus-seam architecture of $C_0$ (any sensible $h$).
- The forced finite rule menu on the seam (invariant under $h$ choice in the 23 carriers tested).
- The existence of a shell partition via $v_2(3u+1)$ (independent of $h$).
- Sprint 26's asymptotic shell-shape recovery (holds under $h_{\text{ext}}$ by computation; expected under other conventions but unverified).

These are properties of the canonical construction *family*, not of any specific $h$ value. They are preserved regardless of reconciliation path.

---

## Conclusion

Path C changes nothing computationally. It adds four things:

1. Explicit scope tag on every prior sprint.
2. Clear vocabulary separating $h_{\text{thm}}$ from $h_{\text{ext}}$.
3. A requirement that future specs declare their project scope.
4. A new category of "cross-project sprint" with explicit bridging rules.

Under this scoping, all prior verdicts stand, all prior evidence is preserved, and the S31-pilot convention mismatch becomes a caught-at-design-time issue rather than a foundation crisis.
