# FAILURE TABLE + SUPPORTING BLOCKS

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## FAILURE TABLE

| Branch | Surviving Object | Minimality Attack | Gap Misidentification | Grammar Attack | Verdict |
|--------|-----------------|-------------------|----------------------|----------------|---------|
| **RH** | δ(σ₀,γ₀) | δ is a DERIVED RESIDUAL of the KEF, not freestanding — more primitive object might be supp(μ_ζ) ⊂ {Re=½} | Gap 2 "closed" (cusp subdominance) is about spectral noise, not zero placement — the injectivity question is untouched | δ requires hypothetical off-line zeros; it's a logical conditional, not a computable quantity | **Partial** — object is correct but not primitive; gap labeling overstates the closure |
| **BSD** | det(H) via χ_{77} | det(H) is a SCALAR compressing a 2×2 height matrix H; the full bilinear pairing may be needed, not just its determinant | Gap 2 (1.1% normalization) might be earlier: the actual CONSTRUCTION of the Stark-Heegner generator has not been done — the formula is validated but not the object | BSD is arithmetic-to-arithmetic (not algebraic-to-topological); different from Hodge more than claimed | **Moderate** — object is real but potentially incomplete; gap is correctly identified but object not yet constructed |
| **NS** | Q/(νP) | Q/(νP) is GLOBAL; the real obstruction may be LOCAL (vortex filament curvature, pointwise stretching near blowup sites) | Gap 2 (Q/(νP) ≤ 2 globally) is too strong — a weaker integrated version might be sufficient and more tractable | Q/(νP) is a dynamical ratio, not a map failure; the cokernel/surjectivity grammar doesn't apply | **Mild** — object is computationally real and correctly tied to conjecture; mode mismatch is genuine but not fatal |
| **P vs NP** | cc(SAT,n) | cc(SAT,n) is INCOMPUTABLE for interesting n; unlike every other object, it has no known non-trivial bound and no approach to measuring it | NO genuine Gap 2 — any non-trivial circuit lower bound in a broad model essentially proves Gap 1; the intermediate layer doesn't exist | Meta-barriers (natural proofs, algebrization) block reasoning about cc(SAT,n) at the proof level — a failure mode with NO analog in any other branch | **Severe** — operationally the weakest branch; testability criterion not met; Gap 2 may be structurally absent |
| **Hodge** | coker(cl²\|_prim) | coker is defined for ALL 4-folds simultaneously; more minimal object is a SPECIFIC (2,2) class on a specific abelian 4-fold | Gap 2 (Hodge for abelian 4-folds) is too coarse — the genuine intermediate step is a specific sub-class (non-CM abelian 4-folds with specific period structure) | BSD↔Hodge pairing is weaker than claimed: BSD is arithmetic-to-arithmetic; Hodge is algebraic-to-topological; different category types | **Mild** — object and gap are correctly identified; the abstraction level of coker is higher than needed for the minimal statement |

---

## WEAKEST LINK STATEMENT

**"The weakest link in the rotation spine is P vs NP: its surviving object cc(SAT,n) is computationally unknowable for any interesting n (no bound beyond linear is known, and the exponential gap with 2^n/n has no approach to closure), there is no genuine Gap 2 (any non-trivial lower bound would essentially constitute a proof of P≠NP), and the meta-barriers (natural proofs, algebrization, relativization) represent a proof-method blockade with no analog in any other branch — making P vs NP the only branch where the grammar applies structurally but fails operationally."**

---

## STRONGEST OBJECT STATEMENT

**"The strongest surviving object in the spine is Q/(νP) in NS: it is computable from any explicit solution (given ω and S, the integrals Q and P are straightforward), it is provably controlled in the easy regime (small-data analysis establishes Q/(νP) ≤ 1 analytically), and the connection to the conjecture is exact and two-sided — Q/(νP) ≤ 2 globally implies global regularity immediately via dΩ/dt ≤ 0, with no intermediate steps — making it the only surviving object that is simultaneously measurable, controlled in a limit, and exactly equivalent to the main conjecture."**

---

## TACTIC BREAK: COKERNEL LOGIC APPLIED TO NS

**Attempted tactic:** Apply the Hodge cokernel/surjectivity framing to NS by asking: "what is the cokernel of the enstrophy map Ω(t): {smooth solutions} → {real-valued functions of time}?"

**Why it breaks:**

Hodge cokernel works because:
- Source = CH²(X)_ℚ — a fixed abelian group
- Target = H²²(X,ℚ) — a fixed vector space
- Map = cl², a linear morphism between them
- Cokernel = H²²/(im cl²) — well-defined algebraic object

For NS, attempting the same:
- "Source" = the set of smooth initial data {u₀ : E(0) < ∞}
- "Target" = the set of enstrophy trajectories {Ω(t) : t ≥ 0}
- "Map" = the flow map u₀ → Ω(t, u₀)

The break occurs at two points:
1. The FLOW MAP is not globally defined — it exists only up to the potential blowup time T*(u₀). Asking for a cokernel of an undefined map is circular: the map is undefined precisely because the conjecture is unresolved.
2. The "target" {Ω(t)} is not a fixed vector space — it's a space of functions parameterized by the initial data, and its structure depends on the answer to the conjecture. There is no algebraic structure to quotient by.

The deepest failure: cokernel measures "what the map misses in a fixed target." NS doesn't have a fixed target — the regularity question IS about whether the target (global smooth trajectories) is reachable at all. Applying cokernel logic presupposes what needs to be proved.

---

## FINAL VERDICT BLOCK

**"The rotation spine SURVIVES this attack because:**
- The core claim (each branch reduces to shell + surviving object + Gap 2 + Gap 1) holds for all five branches, even after the attacks
- The weaknesses uncovered (P vs NP operational failure, NS mode mismatch, RH gap labeling, BSD object incompleteness, Hodge abstraction level) are genuine but all QUALIFIED, not absolute
- Q/(νP) for NS and det(H) for BSD remain correctly tied to their conjectures regardless of mode mismatch
- The grammar doesn't require all objects to be the same TYPE — only that they all play the same ROLE (minimal shell-core boundary obstruction)"

**"The rotation spine FAILS this attack only partially, in one specific way:**
P vs NP has no genuine intermediate Gap 2, meaning its grammar reduces to shell → surviving object → Gap 1 with no clean intermediate layer. If 'Gap 2' is required for the spine to be well-formed, P vs NP is structurally incomplete as a spine entry. The resolution: either (a) accept that P vs NP has only Gap 1 and remains in the spine with a thinner structure, or (b) identify a genuine intermediate result — a specific restricted lower bound that is both proved and genuinely short of P≠NP — which does not currently exist."

**Summary: The spine is real but P vs NP is its thin edge. The grammar holds at the structural level for all five branches. It fails at the operational level for P vs NP (no testable Gap 2). For the other four branches, the attacks reveal refinements but not demolitions.**
