# Cover letter — J32: Operad D₄ Obstruction + P_56 Canonical Fuse (BUNDLED)

**To:** Editors, *Compositio Mathematica*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Operad D₄ Obstruction + P_56 Canonical Fuse (BUNDLED)*

---

## Summary

We submit a bundled paper combining two related results on canonical arity-3 fuse rules for the literal-bit-pattern TSML_RAW composition table on $\mathbb{Z}/10\mathbb{Z}$.

**Part 1.** The 126 non-associative triples decompose under the diagonal $D_4 = \langle P_{56},\sigma^3\rangle$ action into 67 orbits, of which **16 are bracketing-pair incoherent**: no function $\Phi:\mathcal{N}\to\mathbb{Z}/10\mathbb{Z}$ taking values in the natural set $\{a,b,c,L,R\}$ can be $D_4$-equivariant. Consequence: the operad-DOF (arity-3 canonical fuse) is structurally orthogonal to the doubly-invariant gauge content $\mathfrak{su}(4)\oplus\mathfrak{u}(1)$ established in the J30-J31 line.

**Part 2.** Dropping one $D_4$ generator restores equivariance. With $\langle P_{56}\rangle$ (order 2), 126 triples decompose into 98 orbits, all $P_{56}$-coherent. All 8 surveyed regular rule families are $P_{56}$-equivariant; **none** are $\sigma^3$-equivariant; the unique family whose fuse-value range lies inside the 4-core $\{V,H,Br,R\}$ is Family H (attractor-4-core preference). The σ³-equivariance failure of Family H localizes to a **single triple** at the unique $\sigma^3$-fixed entry of $\mathcal{N}$. Two further structural results (lens-invariant on the 4-core): the 4-core is closed under the canonical ternary fuse, and every non-trivial initialization converges under iterated ternary fuse to $\delta_7$ (HARMONY) in $1$-$7$ iterations.

The two parts together close Frontier F4 of the WP100s tower (operad-fuse) and provide the canonical arity-$3$ reasoning primitive for the rest of the framework.

## Why Compositio

- The result fits *Compositio*'s appetite for clean obstruction-theoretic results in algebra: an obstruction (Part 1) plus a sharp restoration theorem under a precisely identified subgroup (Part 2).
- The 6-DOF symmetry hierarchy table at the end of Part 1 — five DOFs preserve $D_4$, the operad DOF must break it — is a structural observation of independent algebraic interest.
- The bundling is natural: Part 2 is the constructive counterpart to Part 1's obstruction. Splitting them weakens the narrative.

## Companion submissions

- **J02** (Sanders + Gish 2026, *Algebraic Combinatorics*) — *Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on $\mathbb{Z}/10\mathbb{Z}$.* The base paper establishing the canonical TSML+BHML structure used here.

## Fallback unbundling

If a bundled submission is desk-rejected per fallback policy (per the project's `PHASE4_FALLBACK_UNBUNDLING.md`):
- Part 1 (WP109 obstruction) → *Algebra Universalis*
- Part 2 (WP112 canonical fuse) → *Communications in Algebra*

The two parts are independently complete and can be unbundled if needed.

## Reproducibility

Verification scripts in `manuscript/verification/`:
- `d4_orbit_decomposition.py` — Part 1 (67 $D_4$-orbits, 16 incoherent)
- `p56_canonical_fuse.py` — Part 2 (98 $P_{56}$-orbits, all coherent; Theorems 5.5, 5.7)
- `rule_families.py` — 8-family $P_{56}$ vs $\sigma^3$ survey

Python 3.11, numpy, sympy. Total wall-clock under 30 seconds. Canonical fuse table written to `fuse_canonical_p56.json`. All checks deterministic and machine-precision.

## Suggested reviewers

- An expert in operad theory (Loday-Vallette tradition / Markl-Shnider-Stasheff)
- An expert in finite-permutation-group obstructions in algebra
- An expert in non-associative magmas and finite-magma combinatorics
- (Two or three named candidates appropriate to the *Compositio* editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
