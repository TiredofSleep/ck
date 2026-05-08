# SAVE_PLAN_J07 — Flatness Theorem + T*=5/7 (JPAA → retarget)

**Date:** 2026-05-07
**Status:** SAVE possible — but only by retitling, retargeting, and replacing Appendix A with a *different* derivation that the corpus actually has. The original "six derivations" appendix does not survive.
**Referee:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J07_JPAA_FreshEyes.md` (Reject; Issues 1, 2, 3 all critical)

---

## §1 — Why save?

Two structural facts make J07 worth saving rather than dropping.

**(a) D-table backing for the actual structural statement.** The referee's central correct objection is that the manuscript jumps from cyclotomic facts to "torus aspect ratio 5/7" without a constructed torus. But the corpus *does* have a clean structural statement near this neighborhood: the 4-core $\{V, H, Br, R\}$ on $\mathbb{Z}/10\mathbb{Z}$ is jointly closed under TSML and BHML (D48), and its runtime attractor at $\alpha_M = 1/2$ admits the *Galois-proven* algebraic relation $H/Br = 1+\sqrt{3}$ via BR-factor cancellation (D78). This is a *theorem* — sympy-symbolic proof, exact, in $\mathbb{Q}(\sqrt{3})$, Galois group $\mathbb{Z}/2\mathbb{Z}$. The 5/7 in the original manuscript is not the structural anchor; the anchor is the 4-core attractor at $\alpha = 1/2$. J07's salvage turns on replacing the 5/7 narrative with the 4-core / 1+√3 narrative.

**(b) Structural role per FAMILY_STRUCTURE_v1.md.** The Family Structure document identifies the 4-core at $\alpha_M = 1/2$ as **the algebraic center of the TIG family** (§2.1, "the unit circle is to U(1)"). Five independent structural facts converge on the same 4-element set: D48 (joint closure), D49 (symbolic normalizer Z_T = Z_B), D78 (Galois-forced 1+√3), D74 (universal across ring extensions), D65 (universal across joint-chain shells of size ≥ 4). J07's flatness setup — four structures on $\mathbb{Z}/n\mathbb{Z}$ — naturally lands in this neighborhood *if* the conclusion is restated as "the four-structure 2×2 forces a curved configuration whose center is the 4-core at $\alpha = 1/2$" rather than "the torus aspect ratio is 5/7." That is a defensible algebraic-geometry-of-finite-rings statement; the 5/7 framing is not.

The honest read: **the original J07 paper does not survive at JPAA.** A retitled, retargeted, restructured paper using the same setup and replacing Appendix A can survive. The save is real but not free.

---

## §2 — Specific fixes (line by line against the referee report)

### Issue 1 (no torus construction) — **CANNOT FULLY FIX**, must retreat

The referee's Issue 1 demands: "(a) explicit construction of a torus, (b) computation of two characteristic invariants R(T), r(T) from the algebra, (c) a theorem proving R/r = 5/7 for n = 10." The corpus does not have these. There is no constructed torus, no metric, no curvature computation. The retreat:

- **Drop the "torus aspect ratio = 5/7" claim entirely.** Remove §4 ("The Aspect Ratio R/r = T* = 5/7"), §6 (Riemann zeros / curvature), and Appendix A in their current form.
- **Reframe the paper around the Flatness Theorem itself** (Theorems 1 and 2 — the four-structure flatness obstruction and the two-circles-force-T² statement). These survive *with corrections* (see Issue 2 fix below).
- **Replace Appendix A with a new "structural center" appendix** built on D48 + D78: the 4-core is the joint-closure of TSML+BHML on $\mathbb{Z}/10\mathbb{Z}$ (D48); its attractor at $\alpha_M = 1/2$ has the Galois-proven relation $H/Br = 1+\sqrt{3}$ in $\mathbb{Q}(\sqrt{3})$ (D78). The new appendix doesn't claim 5/7 — it claims the algebraic center of the configuration is the 4-core / 1+√3 pair, and supplies the theorem.

### Issue 2 (geometric incoherence: R < r self-intersection) — **DELETE**

The referee correctly identifies that R/r = 5/7 < 1 with R < r means a self-intersecting spindle torus, and the manuscript's retreat to "abstract torus" is incoherent. With the 5/7 narrative dropped (Issue 1 fix), this entire critique vanishes. §5 ("The Seven Internal Zeros") and §6.3 (gap-as-prime-territory) go with it.

### Issue 3 (six derivations don't survive) — **DELETE Appendix A; replace**

- D3 = D6 in substance. **Confirmed; delete both.**
- D4 admits not-actually-derived. **Delete.**
- D5 has a factual error (5/7 is not a convergent of π). **Delete.**
- D1, D2 cite internal documents. **Don't cite internally; include only what survives standalone.**

The new Appendix A (per Issue 1 fix above) contains *one* clean structural result with proof: D78. No "six derivations" enumeration.

### M1 (incompatibility-of-factor-partitions proof needed) — **INLINE the 3-line argument**

The referee gives the proof verbatim ("for n=10, the partition by classes mod 2 is $\{\{0,2,4,6,8\},\{1,3,5,7,9\}\}$ and the partition by classes mod 5 is $\{\{0,5\},\{1,6\},\{2,7\},\{3,8\},\{4,9\}\}$, and neither refines the other"). Add this as a 3-line proof in §1.2.

### M2 (Theorem 2 conflates two claims; M-Flow is not free) — **REWRITE Theorem 2**

The current proof of Theorem 2 says "two independently closed S¹'s force T² = S¹ × S¹." The referee correctly notes this needs the actions to be free, and M-Flow has fixed points (0, 5 fixed by every unit). Two repairs:

- **Restate** as: the *configuration space* of pairs (additive position, multiplicative position) carries two commuting circle actions that are free *off the fixed locus*; that configuration space is what the four structures jointly inhabit. Be explicit that the underlying $\mathbb{Z}/n\mathbb{Z}$ itself is *not* the torus.
- **Or**, more honestly, demote Theorem 2 from "torus is forced" to "the configuration space of (A-Flow phase, M-Flow phase) is naturally a quotient of $S^1 \times S^1$ with the M-Flow fixed points identified." This is correct, weaker, and survives referee scrutiny.

### M3 (PROVED label over-applied) — **AUDIT every PROVED label**

After Issues 1-2 fixes, the surviving "PROVED" claims are:
- Theorem 1 (flatness obstruction) — PROVED *after* M1 fix (3-line argument inlined).
- Theorem 2 (configuration-space topology) — PROVED *after* M2 fix (rewritten as quotient claim).
- D48 + D78 in the new appendix — PROVED at sympy precision (in `papers/wp110_4core_fusion_closure/` and `papers/wp113_alpha_uniqueness/verification/f3_galois_alpha_uniqueness.py`).
- All other "PROVED" labels in the original §6, §A.4 — DELETED with the Issue 1-2 fixes.

### M4 (delete §6.2 Riemann zeta) — **DELETE entire §6**

Referee correctly notes the "5/7 → 1/2 under s ↔ 1−s" mapping is false (5/7 → 2/7). §6.2 is decorative + factually wrong. §6.1 (twin primes) and §6.3 (prime gap) are also out of scope for the retargeted paper. Delete all of §6.

### M5 (gap-prime-territory empirical claim) — **DELETE** (in §6 deletion)

### M6 (delete §7 CK applications) — **DELETE entire §7**

Out of scope for a math paper. The CK runtime application belongs in a separate venue or as an applications-section in a system paper.

### M7 (conjectures need separation) — **DELETE Conjectures A.1, A.2, A.3** along with Appendix A

The new Appendix A built on D48 + D78 has its own (single) open question: does the 4-core / 1+√3 structure extend to other commutative-magma pairs on $\mathbb{Z}/n\mathbb{Z}$ beyond TSML/BHML? That is the natural OPEN question per the boilerplate.

### M8 (author block) — Settled. Sanders + Gish (per Brayden directive in `AUTHOR_LANES_v2.md`).

### M9 (bibliography) — **CULL TO ACTUAL CITATIONS**

Drop Bialynicki-Birula, Russell, Gödel, Tarski, Banach-Tarski, Quine, Zermelo, the analytic-number-theory list. Keep:
- Lang (cyclotomic), Hardy-Wright, Stanley (lattice theory), Dummit-Foote, Birkhoff (lattice theory), Ore (equivalence relations).
- **Add Drápal-Wanless (2021), JCT-A 184, 105510** as the closest published precedent (per FAMILY_STRUCTURE_v1.md).
- Keep J02 (4-core paper, Algebraic Combinatorics) and J33 (closed-form attractor + α-PSLQ) as companions — both supply the technical D48/D78 results the new Appendix A cites.

### m1-m9 (minor fixes) — **APPLY DIRECTLY**

m1 (Fejér kernel attribution): add Apostol citation, drop "First-G law" name.
m2 (sinc² zero biconditional): drop the "iff p prime" phrasing (true for any p ≥ 2).
m3 (sixth-derivation remark): deleted with Appendix A.
m4 (§5 "7 zeros"): deleted with §5.
m5 (zeta poles): deleted with §6.
m6 (deg A_p notation): include φ(p)/2 formula in §1.4.
m7 ("globally obstructed prime"): deleted with the 5/7 narrative.
m8 ("PROVED for n=10"): handled in M3 audit.
m9 (companion arXiv IDs): supply arXiv IDs at submission time.

---

## §3 — Estimated revision time

**4–6 weeks** of focused work. The bulk:

- **1 week:** rewrite the introduction around the new structural-center claim; rewrite Theorems 1 and 2 with proofs; inline the M1 partition-incompatibility proof and the M2 configuration-space rewrite.
- **2 weeks:** write the new Appendix A from D48 + D78. Inline the 4-core joint-closure verification (16 + 16 in-core, 0 + 0 spillover under TSML and BHML) and the Galois-proof BR-factor cancellation argument. Cite J02 (4-core paper) and J33 (α-uniqueness PSLQ) as companions; lift the symbolic 1+√3 derivation from `f3_galois_alpha_uniqueness.py`.
- **1 week:** delete §5, §6, §7, original Appendix A; cull bibliography; align with Drápal-Wanless 2021 framing.
- **1–2 weeks:** Brayden's referee-rigor pass; M. Gish review; final pass.

This is faster than the referee's "Path A" (6–12 months to construct a real torus and prove R/r = 5/7) because the save *abandons* the torus-aspect-ratio claim. It is slower than the referee's "Path B" (2–4 weeks for a small honest note in *INTEGERS*) because the save preserves the four-structure flatness obstruction as a stand-alone result with the 4-core / 1+√3 attractor as its algebraic center.

---

## §4 — Updated PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

**PROVEN:**
- The four structures on $\mathbb{Z}/n\mathbb{Z}$ (squarefree, $k \geq 2$ primes) — A-Struct, M-Struct, A-Flow, M-Flow — cannot be simultaneously embedded in a flat 2D surface (Theorem 1, with the M1 fix inlined).
- The 4-core $\{V, H, Br, R\} = \{0, 7, 8, 9\}$ on $\mathbb{Z}/10\mathbb{Z}$ is jointly closed under TSML and BHML (D48; 16 + 16 in-core, 0 + 0 spillover, verified at machine precision).
- At mixing weight $\alpha_M = 1/2$, the runtime attractor on the 4-core admits the Galois-proven algebraic relation $H/Br = 1+\sqrt{3}$ in $\mathbb{Q}(\sqrt{3})$, with $H/Br$ satisfying $x^2 - 2x - 2 = 0$ (D78; sympy-exact symbolic proof via BR-factor cancellation).

**COMPUTED:**
- 4-core joint-closure verification: 16 + 16 in-core triples under TSML and BHML, verified by enumeration (`papers/wp110_4core_fusion_closure/`).
- Galois proof of 1+√3 forcing at $\alpha = 1/2$: `papers/wp113_alpha_uniqueness/verification/f3_galois_alpha_uniqueness.py` (sympy-symbolic).
- Universal 4-core attractor at $\alpha = 1/2$: 76–81 iterations to convergence at 50-digit mpmath precision across 7 boundary initial conditions (D58).

**STRUCTURAL RHYME:**
- The cyclotomic facts $\deg_\mathbb{Q} A_5 = 2$ and $\deg_\mathbb{Q} A_7 = 3$ are correct standard results (Lang, Washington), cited as background motivation for the four-structure setup. **Not as a derivation of any aspect ratio.** The referee's correct objection that the leap from these to "R/r = 5/7" is unsupported is acknowledged: the save replaces that derivation with the 4-core / 1+√3 structural-center claim.
- The Drápal-Wanless 2021 *JCT-A* 184, 105510 paper on maximally non-associative quasigroups is the closest published precedent; same domain (small finite commutative non-associative magmas), opposite extremum (theirs maximally non-associative; ours rationally-structured at α = 1/2).

**OPEN:**
- Does the four-structure flatness obstruction extend to general (non-squarefree) $\mathbb{Z}/n\mathbb{Z}$? The current proof uses the squarefree-CRT factorization explicitly.
- Does the 4-core / 1+√3 algebraic center generalize to other commutative-magma pairs $(T, B)$ on $\mathbb{Z}/n\mathbb{Z}$ satisfying the FAMILY_STRUCTURE membership criteria, or is it specific to TSML/BHML?
- The torus aspect ratio question — is there a metric/Riemannian construction on the configuration space giving a well-defined R/r, and if so, what determines its value? **This is left open**, no longer claimed.

---

## §5 — Updated lens-ownership paragraph

> *Lens and substrate.* This paper works on $\mathbb{Z}/10\mathbb{Z}$ (with the squarefree generalization to $\mathbb{Z}/n\mathbb{Z}$ for general squarefree $n$ in §1 — Theorem 1) using the canonical TSML and BHML composition tables in the appendix's structural-center derivation. These choices are not derived from first principles; they reflect a structural reading of the substrate motivated by the 10-operator decomposition of the ring's algebraic structure (additive cycle, multiplicative orbit, lattice/flow role partition). Theorem 1 (the flatness obstruction on the four structures) holds for any squarefree $\mathbb{Z}/n\mathbb{Z}$ with $k \geq 2$ distinct prime factors and is substrate-independent in this sense. The structural-center derivation in Appendix A (the 4-core / 1+√3 result) is specific to the canonical (TSML, BHML) pair on $\mathbb{Z}/10\mathbb{Z}$; analogous theorems on other substrate-and-table choices are open. The framework's claim is that this particular substrate-and-table choice produces theorems that have surprising downstream connections (Drápal-Wanless 2021 JCT-A neighborhood; Galois extensions in $\mathbb{Q}(\sqrt{3})$; LMFDB 4.2.10224.1 in companion paper J33). Whether other substrate choices give similarly rich downstream connections is open.

---

## §6 — Recommended retitle / retarget

**Old title:** "Flatness Theorem: The Forced 2x2 Torus on Z/10Z" (with T*=5/7 appendix).
**New title (recommended):** "A Flatness Obstruction on Squarefree $\mathbb{Z}/n\mathbb{Z}$: Four Algebraic Structures and the 4-Core Algebraic Center."

**Old venue:** *Journal of Pure and Applied Algebra* (referee verdict: REJECT; structural problems; Path A would take 6-12 months to build the actual torus).
**New venue (recommended):** *Algebraic Combinatorics* OR *Discrete Mathematics*. Rationale:
- *Algebraic Combinatorics* is the venue J02 (4-core paper) is going to. J07 retitled is a natural companion: J02 proves the 4-core's joint-closure structure on the joint-chain; J07 frames the broader four-structure context in which the 4-core is the algebraic center. Same intellectual neighborhood (Drápal-Wanless 2021 was published in *JCT-A*, with *Algebraic Combinatorics* as the natural home for follow-up work).
- *Discrete Mathematics* if *Algebraic Combinatorics* declines the bundle: the lattice-theoretic content (partition-lattice incompatibility, joint-closure structure) fits naturally there.

**Backup venue (Path B):** if neither *Algebraic Combinatorics* nor *Discrete Mathematics* accepts, the referee's Path B is available — strip everything except the corrected Theorem 1 (flatness obstruction) and submit as a 4-6 page note to *INTEGERS* or *Math. Magazine*. In that compressed form the paper is honest, small, and clearly stated. The 4-core / 1+√3 structural-center material would move to J02 or J33's companion sections.

**Author block:** Sanders + Gish (per AUTHOR_LANES_v2.md).

**T*=5/7 narrative future:** the corpus claim that T*=5/7 is structurally forced does not survive in J07's revised form. **The save explicitly abandons that narrative for J07.** If T*=5/7 is to be claimed elsewhere, it must be derived rigorously in a separate paper (the referee's Path A — 6-12 months work to construct the torus). J13's referee report (J13_ActaArith_FreshEyes.md) confirms that the standalone J13 attempt at the 5/7 derivation also fails (wrong minimal polynomial of $A_7$; arithmetic error in rational-root test). For the J-series corpus going forward: T*=5/7 should be cited *only* in papers that use it as a coherence threshold value (its operational role in CK runtime), not as an algebraic theorem.
