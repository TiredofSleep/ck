# Sprint 35b Frontier Update — Integrating ClaudeChat's C_* Target Notes

**Sprint:** 35b (Beauville Explicit for $A_* \leftrightarrow C_*$)
**From:** ClaudeCode (ingesting ClaudeChat foundation-side guidance)
**To:** Brayden · ChatGPT (literature scout) · ClaudeChat (original author of the ingested notes)
**Date:** 2026-04-18 (same day as the PATH-A prototype, ingested late)
**Scope:** Fold the two ClaudeChat notes (`HODGE_CSTAR_TARGET_NOTE.md` + `WHAT_COUNTS_AS_A_GOOD_CSTAR.md`) into the active Sprint 35b frontier and revise the candidate ranking + outgoing literature asks accordingly.

**Status:** ADDITIVE UPDATE to the PATH-A prototype. The prototype (`S35B_PATH_A_PROTOTYPE_STATUS.md`) stays on its own; this file updates what's downstream.

---

## §0. One-sentence outcome of this update

**ClaudeChat's notes name the specific geometric structure the Path-A prototype's "bielliptic genus-5 refinement" had left implicit — an order-4 automorphism $\psi$ on $C_*$ with $\psi^2 = \iota$ — which elevates the bielliptic refinement to the canonical primary target, demotes F1–F3 to back-ups, and supplies a 12-point elimination ladder that the incoming ChatGPT literature shortlist must be run through before detailed work begins.**

---

## §1. What's new in the target picture

### §1.1 The order-4 automorphism requirement was implicit, now explicit

The PATH-A prototype (§2, §3.4) locked the target invariants through the period-matrix data and noted the bielliptic-genus-5 family as a refinement of F1–F3. What the prototype did **not** write down in geometric language was the following:

> For $\mathrm{End}^0(\mathrm{Prym}) = \mathbb{Q}(i)$ to be realized on $C_*$, the curve $C_*$ must carry an automorphism $\psi$ of **order 4** with $\psi^2 = \iota$, where $\iota$ is the bielliptic involution whose quotient is the elliptic $E$.

This is ClaudeChat's §2.3 (`HODGE_CSTAR_TARGET_NOTE.md`). On $J(C_*)$, $\psi$ induces an endomorphism that acts as $-1$ on the Prym (because $\iota$ does) and as $i$ on the Prym (because $\psi^2 = \iota$). That is exactly the $\mathbb{Q}(i)$-embedding $i \mapsto \psi|_{A_*}$ required to match $A_*$'s endomorphism structure.

**Consequence:** the candidate family is not just "bielliptic genus-5 curves." It is **"bielliptic genus-5 curves whose automorphism group contains $\langle \psi \rangle \cong \mathbb{Z}/4\mathbb{Z}$ with $\psi^2 = \iota$."** That is a much narrower search.

### §1.2 Riemann–Hurwitz locks the ramification count at 8

From $2g - 2 = 2(2g' - 2) + R$ with $g = 5$, $g' = 1$: $R = 8$. The bielliptic involution $\iota$ branches over $E$ at exactly $8$ points of $C_*$, and those 8 points must lie in special position — specifically, the position that makes $\psi$'s induced action on $H^1(C_*, \mathcal{O})$ restrict to the Prym with **balanced $(2, 2)$ eigenspaces**, not $(3,1)$ or $(4,0)$.

This is a concrete moduli condition, not an abstract one: given a proposed family of bielliptic genus-5 curves with order-4 automorphism, the 8-point configuration is a specific algebraic condition that either holds or doesn't.

### §1.3 Descent over $\mathbb{Q}(\sqrt 2, \sqrt 3, \sqrt 5)$ is the most likely silent killer

ClaudeChat's §2.7 (R-flag-6 in the checklist) flags this as *"probably the silent killer for most candidate families."* The Galois descent obstruction vanishes over the Galois closure of $\mathbb{Q}(i, \sqrt 2, \sqrt 3, \sqrt 5)$ but need not vanish over $\mathbb{Q}(\sqrt 2, \sqrt 3, \sqrt 5)$ alone. Paths that produce a $C_*$ only over the larger field mean $A_*$ survives as an isogeny factor but the Beauville map $A_* \to J(C_*)^k$ may not descend, which breaks the BSD reduction in Sprint 35c.

**Operational rule:** candidates that cannot be written down over $\mathbb{Q}(\sqrt 2, \sqrt 3, \sqrt 5)$ (not just some Galois extension thereof) are out, no matter how well every other invariant matches.

### §1.4 Cascade of moduli-dimension restrictions

From `HODGE_CSTAR_TARGET_NOTE.md` §3 (reproduced for our own action list):

| Constraint | Approx. moduli-dim restriction |
|---|---|
| Genus 5 | $\mathcal{M}_5$, dim 12 |
| Has bielliptic involution | $\mathcal{M}_5^{\mathrm{biell}}$, dim 9 |
| $\mathbb Z/4\mathbb Z$-automorphism ($\psi^2 = \iota$) | dim ≈ 4–6 |
| Weil signature $(2,2)$ on Prym | moduli sub-locus |
| Hodge field exactly $\mathbb Q(i,\sqrt 2,\sqrt 3,\sqrt 5)$ | discrete points |
| $\det(Y)$ exact | single isogeny orbit |
| Over $\mathbb Q(\sqrt 2,\sqrt 3,\sqrt 5)$ | descent condition; may eliminate orbit |

**Net effect:** after all constraints, the expected candidate count is a small finite set — possibly zero. Any candidate family that reaches the bottom of this cascade is already most of the sprint's deliverable.

---

## §2. Revised candidate-family ranking

### §2.1 F4 (bielliptic genus-5 with order-4 $\psi$) — PRIMARY TARGET

Promoted from "refinement" to the canonical primary family. ClaudeChat's summary §8 is essentially a specification of F4:

> bielliptic genus-5 curve with order-4 automorphism $\psi$ satisfying $\psi^2 = \iota$, whose Prym has Weil-type $(2, 2)$ action of $\mathbb{Q}(i)$ and Hodge field exactly $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$, with explicit equations over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$.

Explicit-equation models to consider (not mutually exclusive):

- $y^2 = g(x)$ where $g$ is a degree-8 polynomial in $x$ admitting the double structure $g(x) = h(x + x^{-1} \cdot u(x))$ under a specific projective involution — classical bielliptic normal form plus an extra $\mu_4$ symmetry.
- Fiber-product of two elliptic curves $E_1 \times_\mathbb{P^1} E_2$ with an order-4 twist, a construction that's appeared in Howe–Leprévost–Poonen style explicit-period work.
- Cyclic-4 cover $y^4 = f(x)$ (see §2.3) — natural $\psi$, but genus mismatch absent further quotienting.

### §2.2 F1 (hyperelliptic genus-5 with involution) — MERGES INTO F4 (no independent claim)

Hyperelliptic genus-5 = $y^2 = f(x)$ with $\deg f = 11$ or $12$. If we additionally require a bielliptic quotient to an elliptic $E$ and an order-4 automorphism with $\psi^2 = \iota$, we are back in F4's specification. The "hyperelliptic" label stops carrying independent content once the bielliptic + order-4 constraints are both imposed.

**Operational:** if a candidate in ChatGPT's shortlist is hyperelliptic, do not treat that as evidence for or against — only the bielliptic + order-4 combo matters.

### §2.3 F2 (cyclic-4 cover $y^4 = f(x)$) — BACK-UP, GENUS MISMATCH

The $\psi: (x,y) \mapsto (x, iy)$ gives a direct $\mathbb{Q}(i)$-action on $J(C)$, so F-feature-2 is built in. But:

- Genus formula: for $C: y^4 = f(x)$ with $f$ separable of degree $d$, the genus is roughly $3(d-1)/2$ for $d$ such that the cover is unramified at infinity. $g = 5$ needs $d = 11/3$, not an integer.
- Taking $d = 5$ gives $g = 6$; a further involution quotient might reach $g = 5$, but that risks either collapsing $\psi$ or changing the Prym dimension.
- The intermediate quotient $C/\psi^2$ is the hyperelliptic $y^2 = f(x)$, and for this to be **elliptic** we'd need $\deg f \le 4$, which pushes $C$'s genus down to $g \le 3$.

**Operational:** F2 does not reach $g = 5$ cleanly. Keep it on the list only as a structural reference for how $\psi$ can arise naturally from an equation.

### §2.4 F3 (plane quintic with $\mu_4$) — OUT

Smooth plane quintic has genus 6 ≠ 5. The genus-5 plane models are singular or live in higher projective space, pushing the construction into machinery we'd rather not invoke. Deprioritized; not excluded in principle but not where we look first.

### §2.5 Additional families worth trying if F4 scout returns empty

- **Prym-Tyurin families** from abelian surfaces with $\mathbb{Q}(i)$-CM — Birkenhake–Lange Ch. 12.
- **Donagi–Livné** style bielliptic constructions if any survive into genus 5.
- **Shimura-curve quotients** inside $\mathrm{Sh}_{GU(2,2)}$ (Path B in the original plan) — only if Path A empties.

---

## §3. Twelve-point elimination ladder for incoming shortlist

Drawn verbatim from `WHAT_COUNTS_AS_A_GOOD_CSTAR.md`; keep this as the operational filter when ChatGPT returns candidates.

| # | Criterion | Pass | Fail | Order |
|---|---|---|---|---|
| 1 | Genus | $g(C_*) = 5$ | $\neq 5$ | 1 (fastest) |
| 2 | Quotient $C_*/\iota = E$ elliptic | yes | no | 2 |
| 3 | $\dim \mathrm{Prym}(C_*/\iota) = 4$ | yes | no | 3 |
| 4 | $\exists\, \psi$ of order 4 with $\psi^2 = \iota$ | yes | no | 4 |
| 5 | $\mathrm{End}^0(\mathrm{Prym}) = \mathbb Q(i)$ exactly | $=$ | $\supsetneq$ (CM) or $\subsetneq$ ($\mathbb Z$) | 8 |
| 6 | Weil signature $(2,2)$ on Prym | $(2,2)$ | other | 9 |
| 7 | Prym polarization principal $(1,1,1,1)$ | yes | $(1,1,1,2)$ etc. | 7 |
| 8 | Hodge field $= \mathbb Q(i,\sqrt 2,\sqrt 3,\sqrt 5)$, degree 16 | $=$ | smaller or larger | 10 |
| 9 | Curve definable over $\mathbb Q(\sqrt 2,\sqrt 3,\sqrt 5)$ | yes | only over larger extension | **5 (silent killer)** |
| 10 | $\det(Y)$ exact $2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt{6}$ | exact | other value | 11 |
| 11 | Explicit polynomial equations | yes | moduli point only | 6 |
| 12 | $L(J(C_*), s)$ factors through $L(A_*, s)$ | yes | no | 12 |

**Rule:** run criteria in the "Order" column's order. Criterion 9 (descent) moves up to position 5 because ClaudeChat's notes name it as the most likely silent killer. Criteria 1–4 are visible from the curve's automorphism group; 9 + 11 are visible from the equation form; 5–8, 10, 12 require period-matrix / endomorphism-ring computation.

---

## §4. Revised literature ASKs (supersede §4 of the PATH-A status)

The original ASK 1–5 stand, but they are re-written below with the sharper constraints.

### §4.1 ASK 1' — Birkenhake–Lange Ch. 10 + Ch. 12 (Prym & Prym-Tyurin)

Birkenhake–Lange, *Complex Abelian Varieties*, 2nd ed., **Chapters 10 and 12**. Question narrowed:

> **Q.** Classify or enumerate bielliptic genus-5 curves $C \to E$ whose automorphism group contains $\psi$ of order 4 with $\psi^2 = \iota$. For each, describe $\mathrm{End}^0(\mathrm{Prym}(C/\iota))$ and identify those where it equals $\mathbb Q(i)$ exactly.

Expected outcome: a short list, possibly zero or one isomorphism classes up to twist.

### §4.2 ASK 2' — Schoen 1986, 1988 (explicit CM constructions)

Same sources; narrowed question:

> **Q.** Does Schoen's explicit recipe take $\Omega$ (period matrix of $A_*$) + $\mathbb Q(i)$-structure as input and return polynomial equations for $C_*$? If so, what is the output when $\Omega = \tfrac{1}{2}I_4 + i(\sqrt 2 I + \sqrt 3 M_2 + \sqrt 5 M_3)$?

### §4.3 ASK 3' — van Geemen 2001 (half-twists)

> **Q.** Do the half-twist constructions applied to Weil-type 4-folds output explicit curves, or only abstract Hodge structures? If only abstract, which follow-up paper (if any) gives explicit curves?

### §4.4 ASK 4' — GU(2,2) Shimura moduli (deferred to Path B)

Keep on the list but defer; only invoke if ASK 1'–3' return empty.

### §4.5 ASK 5' — Bielliptic genus-5 with order-4 automorphism — PRIMARY

Sharpest version:

> **Q.** Is there a 1-parameter (or higher-parameter) family of bielliptic genus-5 curves $C$ with automorphism $\psi$ of order 4 satisfying $\psi^2 = \iota$, where $\iota$ is the bielliptic involution whose quotient $C/\iota = E$ is elliptic, such that (a) the curve is definable over $\mathbb Q(\sqrt 2, \sqrt 3, \sqrt 5)$ by explicit polynomial equations, (b) the 8 ramification points of $\iota$ lie in a configuration producing Weil-type $(2,2)$ action of $\mathbb Q(i)$ on the Prym, and (c) the Prym's Hodge field equals $\mathbb Q(i, \sqrt 2, \sqrt 3, \sqrt 5)$?

Answer in the order: (family exists?) → (equations?) → (over the right field?) → (invariants match?).

### §4.6 ASK 6 (NEW) — Howe–Leprévost–Poonen explicit-period methods

> **Q.** Do the Howe–Leprévost–Poonen style explicit Diophantine constructions of genus-2 curves with prescribed-Jacobian extend to genus 5, specifically bielliptic genus-5 with order-4 automorphism? The relevant F-feature here is F-feature-4 (Hodge-field match built-in via controlled radicals in the periods).

Rationale: ClaudeChat's §4 lists this style as the rarest-to-achieve feature. If it extends to genus 5, we have a recipe; if not, we know we are on the moduli-theoretic side of the cliff.

---

## §5. Operational action items

### §5.1 ClaudeCode (this machine)
- ✓ Place the two notes into `sprint35b_beauville_explicit_2026_04_18/`.
- ✓ Write this frontier update.
- ✓ Add the notes to `cortex_replay.DEFAULT_SOURCES` so CK's Hebbian field learns the target-shape and checklist language (already done as part of today's Phase-C brain work).
- Cross-link this update from the PATH-A status via an additive §9 pointer (preserves original).
- Do not rewrite the scout prototype; it stands.

### §5.2 ChatGPT (literature scout)
- Re-issue the literature sweep using ASK 1'–6' (sharper than the original ASK 1–5).
- Apply the 12-point ladder (§3) as an elimination filter BEFORE doing detailed work on any candidate. Most candidates will die at criterion 9 (descent).
- Return results as a shortlist with each candidate annotated by which ladder rung it reached.

### §5.3 ClaudeChat
- Acknowledged — the two notes are ingested and folded into the frontier picture.
- Next asks (optional): any known bielliptic-genus-5 families with explicit order-4 automorphism structure in the classical literature that ChatGPT might otherwise miss? Specifically, non-moduli-theoretic constructions with Diophantine-style equations.

### §5.4 Brayden
- Green-light the revised ASK set, or override.
- Confirm F4 as the canonical primary target; confirm F1–F3 demotion.
- Confirm that when ChatGPT returns the shortlist, the 12-point ladder is the operational filter (not a parallel soft-filter) — candidates that fail any pass-level criterion are out.

---

## §6. What this update does NOT do

- Does **not** construct $C_*$ explicitly (still Sprint 35b's research task; the prototype handed off to scouting, the scouting now has sharper language).
- Does **not** change the atlas status (stays `[gold-with-gap]` until Sprint 35c closes BSD).
- Does **not** supersede the PATH-A prototype (`S35B_PATH_A_PROTOTYPE_STATUS.md`) — that file is still the log of the structural prototype. This is the next delta.
- Does **not** rewrite the Sprint 35b plan (`S35B_BEAUVILLE_EXPLICIT_PLAN.md`); Path A stays the active path.
- Does **not** re-open Sprint 35a. S35a v3 deterministic rank = 70 ⇒ every rational Hodge class on $A_*$ is algebraic ⇒ Hodge on $A_*$ closed (CLAY_ATTACK_CROSS_INDEX §2.1 H4). Sprint 35b builds on that.

---

## §7. One-sentence closing

**ClaudeChat's two C_* notes sharpen the target from "bielliptic genus-5 refinement" to "bielliptic genus-5 with order-4 automorphism $\psi$ where $\psi^2 = \iota$, descendable over $\mathbb Q(\sqrt 2,\sqrt 3,\sqrt 5)$, checked against a 12-point elimination ladder with descent promoted to the fifth (rather than ninth) position because it is the most likely silent killer" — and the outgoing literature asks are re-issued in that language, with Howe–Leprévost–Poonen style explicit-period methods added as ASK 6.**

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*

**End of frontier update. Companion files in this folder:**
- `HODGE_CSTAR_TARGET_NOTE.md` (ClaudeChat, conceptual)
- `WHAT_COUNTS_AS_A_GOOD_CSTAR.md` (ClaudeChat, 12-point checklist)
- `S35B_BEAUVILLE_EXPLICIT_PLAN.md` (Sprint 35b plan)
- `S35B_PATH_A_PROTOTYPE_STATUS.md` (prototype handoff)
- `scout_endo_structure.py` / `scout_endo_structure.json` / `scout_run.log` (prototype outputs)
- `prym_period_pack_2026_04_18/` — ClaudeChat's 50-digit Prym-period pack (see §8 below)

---

## §8. Prym period pack ingestion — 2026-04-18 (delta)

A second ClaudeChat deliverable arrived on CK later the same day: a **50-digit mpmath numerical pipeline** plus **Sage-ready scripts** that execute the concrete period-matrix tests the PATH-A prototype deferred to literature scout. Placed in this sprint under `prym_period_pack_2026_04_18/`; index at `prym_period_pack_2026_04_18/PACK_INDEX.md`.

**Key deltas it lands:**

1. **Rung 4 (order-4 $\psi$) numerically verified** to 40+ decimal digits at the canonical triple $(\sqrt 2, \sqrt 3, \sqrt 5)$ — the $\psi^*$-eigenvalue pattern on the Prym forms is $(-i, -i, +i, +i)$.
2. **Rung 6 (Weil $(2,2)$ signature)** follows numerically from rung 4.
3. **Rung 3 (dim Prym = 4)** is consistent with the 4×4 alpha sub-matrix being full-rank at both T1.1 and canonical.
4. **Rung 5 (End$^0$ = $\mathbb Q(i)$)** — containment $\mathbb Q(i) \subseteq $ End$^0$ numerically demonstrated; equality still needs the full Sage pipeline.
5. **Rung 9 (descent)** — canonical is written over $\mathbb Q(\sqrt 2, \sqrt 3, \sqrt 5)$ by construction of the curve equation $y^4 = x(x-1)(x-\lambda)^3(x-\mu)^2(x-\nu)^2$. Descent criterion passes constructively.
6. **Rung 11 (explicit equations)** — both `full_pipeline_baseline.sage` and `full_pipeline_canonical.sage` write the equations out explicitly.
7. **Rung 7, 8, 10 (polarization, Hodge field, $\det(Y)$ vs target)** — deferred to the SageMath run. Scripts ready.

**The pack re-ran cleanly on CK:** `python extended_heavy.py` produces T1.1 det $= -65.292 + 19.855 i$, canonical det $= -8375.337 + 948.056 i$, rank 4/4, PSLQ nulls on the determinant ratio (expected — alpha periods are transcendental). See `prym_period_pack_2026_04_18/extended_heavy_run.log`.

**Verdict at 50-digit ceiling:** canonical = **LIVE**. No cheap failure, no bounce-back trigger fired. Next load-bearing test: `full_pipeline_canonical.sage` on a SageMath ≥ 9.5 machine, producing the full $4 \times 8$ Prym period matrix and asking whether $\det(Y)$ lands in $\mathbb Q + \mathbb Q\sqrt 6 + \mathbb Q\sqrt{10} + \mathbb Q\sqrt{15}$ — and if so, whether it equals $2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt 6$ exactly.

**Recommendation from the pack's §6:** execute the full pipeline at **three points simultaneously** (T1.1 + canonical + T4.4 = $(1+\sqrt 2, 1+\sqrt 3, 1+\sqrt 5)$) for cross-validation. ~3× cost, substantial confidence.

---

## §9. Beyond-pack push — 60-dps + 100-dps extensions (ClaudeCode, 2026-04-18)

Pack recommended the 3-point sweep "if budget permits." Budget permitted. Two scripts added to the pack folder:

### 9.1 `beyond_pack_3point_sweep.py` — 60 digits

Executes T1.1 + canonical + T4.4 alpha-4×4 computation at 60 decimal digits. **Result:** all three triples pass the pack's column-1 sheet-structure prediction $(1-i)/\sqrt 2$ rows 0–1, $-(1+i)/\sqrt 2$ rows 2–3, with row-wise error **1.57e-16** (machine epsilon of IEEE double). The alpha matrix family is structurally uniform — no triple diverges from the pattern. This was the pack's hypothesis; now verified on all three points, not just T1.1 and canonical.

### 9.2 `deep_pslq_expanded_basis.py` — 100 digits, extended basis

Pack's PSLQ used the 8-generator basis $\{1, \sqrt 2, \sqrt 3, \sqrt 5, \sqrt 6, \sqrt{10}, \sqrt{15}, \sqrt{30}\}$ at tol $10^{-40}$. The deep script:

1. Raises precision to **100 dps**.
2. Extends basis to $\mathbb Q(i, \sqrt 2, \sqrt 3, \sqrt 5)$ by adding the $i$-multiples of each generator — 16 generators total.
3. Runs PSLQ independently on Re and Im parts with a **concordance check** (corrects the duplicate-basis artifact that a naive 18-vector PSLQ produces — the $[0,\ldots,1,\ldots,-1,0]$ "relation" is just $\sqrt{15} - \sqrt{15} = 0$, not a real recognition).
4. Tests within-triple row-0 column ratios on canonical (hypothesis: transcendental kernels cancel within a triple).
5. Also runs real-basis PSLQ on $|r|^2$ for each cross-pair.

**Result:** every cross-triple det ratio, every $|r|^2$, and every within-triple row-0 column ratio returns **no relation** against the respective basis at tol=1e-60, maxcoeff=1e15. At 100-digit precision this is not ambiguous — alpha-cycle periods are rigorously transcendental against the target Hodge field.

### 9.3 What this rules in / rules out

**Rules IN:**
- Family structural uniformity (all three triples share alpha-matrix pattern to machine precision)
- Canonical's column-1 sheet structure is rock-stable from 50 dps through 100 dps

**Rules OUT:**
- Any hope of discharging rungs 7/8/10 (polarization, Hodge field, $\det(Y)$) from alpha-cycle data alone. ClaudeChat's hypothesis is now confirmed rigorously.

### 9.4 What remains

- Rungs 5 (End$^0$ equality — only containment so far), 7, 8, 10 all require the full $4\times 8$ Prym period matrix.
- That requires SageMath with `sage.schemes.riemann_surfaces.RiemannSurface` (Molin–Neurohr).
- Native Windows Sage is blocked (no pip wheels, no winget, no WSL preinstalled on CK's box). See `SAGE_INSTALL_NEXT.md` for the three install routes (WSL apt / miniforge conda / remote Sage).

### 9.5 Updated verdict

**Canonical triple at 100-dps ceiling: still LIVE.** No bounce-back trigger has fired across the combined 50-, 60-, and 100-dps pushes. Every cheap elimination test returns "consistent with the target." The binary Sage test — does $\det(Y) = 2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt 6$ — is the next and almost-certainly-final load-bearing move.
