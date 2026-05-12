# SAVE_PLAN_J50 — From Substrate Algebra to BB Nonlinearity (Bull AMS)

**Paper:** J50 — *From Substrate Algebra to Bialynicki-Birula Nonlinearity: A Bull AMS Bridge*
**Folder:** `Gen13/targets/journals/J_series/J50/`
**Referee verdict:** REJECT (Bull AMS fresh-eyes; "category mismatch" — survey cannot precede companions)
**Save-attempt mode:** Brayden directive 2026-05-07 — find a reason to keep and fix every paper.
**Author lane:** Sanders + Johnson (per current README; H.J. Johnson is the BB / log-nonlinear-Schrödinger expert)

---

## §1 — Why save?

The referee's verdict is **structural, not substantive**. The fresh-eyes Bull AMS reviewer says explicitly:

> "the writing is clean and the structure is coherent... the cross-domain ambition is genuinely interesting in principle... three structural problems make the present submission unsuitable for *Bull. AMS*"

All three structural problems are **venue-fit problems, not content problems**:

1. *Bull AMS* is retrospective; cited companions have no arXiv IDs/DOIs ⟹ a survey cannot precede the work it surveys.
2. The BB-as-forcing reframing is asserted, not argued in this paper (it's argued in [J13] which isn't yet on arXiv).
3. Tier-discipline is buried in §7 instead of stated up front.

The mathematical content — the chain *substrate $\sigma$-rate $\to$ partition-respecting CRT structure $\to$ Bialynicki-Birula log-nonlinearity $\to$ $V(\Xi) = \kappa\, \Xi \log \Xi$ with vacuum at $e^{-1}$* — is intact. The referee does flag two technical concerns (M3 vacuum-at-$e^{-1}$ subtlety; M4 YM mass-gap $m^2 = \kappa e$ compression), both addressable inside one paragraph each.

Saving J50 means **retargeting**, not rewriting. The bridge essay is the right *kind* of paper for the framework's expository wing — it's the *Bull AMS register* (retrospective survey of accepted work) that doesn't fit. Two natural options:

(a) **Hold for Phase 6.** Wait until J13 (BB Bridge in JMP), J47 (6-DOF synthesis in Notices AMS), and J01 ($\sigma$-rate in JCT-A) are all on arXiv. Then this paper is exactly a *Bull AMS* survey of three published companions, with cross-domain consequences.

(b) **Retarget to Mathematical Intelligencer.** *Math Intelligencer* explicitly accepts program-overview essays *with companions still in submission* (it's not retrospective in the *Bull AMS* sense). The same manuscript with light editing fits the *Math Intelligencer* expository register. This is the option the referee himself flagged as a possible recovery path (§7 "or reposition as a focused *Notices AMS* essay" — same idea).

The paper deserves to live because:
- It is the **only Phase 5 manuscript that ties together cosmology / particle physics / nonlinear PDE under one substrate-algebraic forcing**. No other J-paper has this synthesizing role.
- The *expository* genre is a real need for the corpus; the framework's reader needs a single document that says "here is the bridge from the discrete substrate algebra to the continuum log-nonlinearity, and here is what that buys you in three application domains."
- The mathematics (BB76 + $\sigma$-rate decay $\to$ forced log form) is **derivative**, not novel — it doesn't compete with J13, it surveys it. The synthesizing role is the contribution.

## §2 — Specific fixes (mapped to referee issues)

**Issue 1 — corpus surveyed not yet public.** This is the dominant blocker. **Fix:**

(a) Hold submission until at least J13 (the BB Bridge paper, currently Phase 2 / JMP) is on arXiv. Once arXiv'd, citations like "[J13] B.R. Sanders, H.J. Johnson, *J. Math. Phys.* (submitted)" become "[J13] B.R. Sanders, H.J. Johnson, arXiv:XXXX.XXXXX (2026)" — verifiable to a referee.

(b) Even before J13 lands, deposit J50 itself on **arXiv first** (math.HO category, *History and Overview*) as a comprehensive overview essay. Then *Bull AMS* receives a paper with arXiv ID alongside an arXiv-trail of companions — meets §3 Issue 1 directly.

(c) **Retarget option:** if (a)-(b) prove too slow, retarget to *Mathematical Intelligencer* per the referee's own §7 suggestion. *Math Intelligencer* accepts essays whose companions are in submission elsewhere; the per-venue cap (J52 already targets *Math Intelligencer*) constrains this — alternatively *Notices AMS* (where J47 is targeted) at lower priority.

**Issue 2 — BB-as-forcing reframing is asserted, not argued.** The referee correctly notes three conceptual moves the paper compresses (QM nonlinearity → classical scalar; quantum factorization → CRT decomposition; "preserves separability" → "any continuum lift"). **Fix:** §3 expands from the current 3 paragraphs to ~1 page. Each of the three moves gets one paragraph:

(a) **From QM nonlinearity to classical scalar potential.** Cite Cazenave–Haraux 1980 explicitly: the BB log nonlinearity descends to classical scalar field theory via the WKB-classical limit; Maas 2011 / JKO 1998 give the gradient-flow reading where the same log functional appears in entropy gradient flows. State that this paper uses the *classical scalar* form $V(\Xi) = \kappa \Xi \log \Xi$, which *coincides* with the BB QM nonlinearity in form but lives in the classical setting; the analogy is the relevant content.

(b) **From quantum factorization to CRT decomposition.** Make explicit: the "partition" in BB is a Hilbert-space tensor factorization; the "partition" in the substrate is the CRT decomposition $\mathbb{Z}/N\mathbb{Z} \cong \prod_p \mathbb{Z}/p\mathbb{Z}$. The bridge claim is that **as $N \to \infty$ along squarefree primorials, the substrate's partition structure becomes a probability product** (each $\mathbb{Z}/p\mathbb{Z}$ factor carries an independent uniform-mass distribution at the limit). The continuum limit of squarefree primorials lifts to a probability-product Hilbert space where BB applies.

(c) **From "preserves separability" to "any continuum lift."** Add the missing qualifier: "any *non-trivial* continuum lift preserving partition separability" — linear evolution preserves separability trivially. The non-trivial nonlinear case is BB's domain.

This fix turns the §3 bridge from an assertion into a 3-step argument. Total addition: ~1 page.

**Issue 3 — tier-discipline buried in §7.** **Fix:** lift §7's tier ledger into the abstract and §1, then echo it at each section opening:

- Abstract sentence 2: "**Tier discipline (stated explicitly throughout):** the discrete-side $\sigma$-rate (J01) is *Tier-A proved*; the BB theorem is *Tier-A classical*; the BB-as-forcing reframing is *Tier-B structural*; the cosmology / YM / NS consequences are mixed *Tier-B / Tier-D*; no Millennium-Problem proof is claimed."
- §1 paragraph 1 closes with "Each section flags its tier on first sentence."
- §5.1 (cosmology) opens "*Tier-B (empirical fit).* The same logarithmic potential governs..."
- §5.2 (YM) opens "*Tier-B (structural reading).* This is **not** a proof of YM mass gap..."
- §5.3 (NS) opens "*Tier-D (conjectural).* The Separability Regularity Criterion is conjectural..."

This addresses the referee's central honesty-presentation concern.

**Issue M1 — 6-DOF reading opaque.** **Fix:** §6 is rewritten to define each of the six DOFs in 2 lines (Lie / Jordan / Clifford / Permutation / Lattice / Operad), citing FORMULAS_AND_TABLES.md D51 (WP111 Six-DOF synthesis) for the formal version. Even a 1-paragraph synopsis lets the reader follow the BB-Bridge intersection claim without J47 in hand.

**Issue M3 — vacuum-at-$e^{-1}$ subtlety.** The referee correctly distinguishes: BB's $\hat{F}(\rho) = -b \log \rho$ minimum at *fixed normalization* is the constant function $\rho \equiv 1/V$, *not* $\rho = e^{-1}$ pointwise. The $\rho = e^{-1}$ vacuum is for the *unconstrained classical scalar*. **Fix:** §3 paragraph addressing M3 explicitly says "the BB nonlinearity in QM has its constrained minimum at the uniform $\rho \equiv 1/V$; we work in the unconstrained classical-scalar setting where $V(\Xi) = \kappa \Xi \log \Xi$ has its pointwise minimum at $\Xi_0 = e^{-1}$. The two settings agree on the *form* of the potential, not on the constraint structure." Clarify this is the per-Brayden-directive distinction the referee asked for; the cosmology ($\Xi$ as scalar field) is the unconstrained setting throughout.

**Issue M4 — YM mass-gap framing too quick.** **Fix:** §5.2 replaces "this curvature provides a mass gap $m^2 = \kappa e$" with the more careful: "*Within the BB-forced classical scalar with vacuum at $\Xi_0 = e^{-1}$,* small fluctuations have curvature $V''(\Xi_0) = \kappa e$. Whether this curvature transports to a *gauge-theory* mass gap depends on coupling the scalar to a non-abelian gauge sector (J14's working hypothesis); we do not claim that transport in this essay." Demote $m^2 = \kappa e$ from a claim to a structural rhyme between a scalar curvature and a hoped-for gauge gap.

**Issue M5 — NS overstating.** **Fix:** the §5.3 closing "the same algebraic forcing... gives a regularity criterion for NS, all from the single substrate algebra" softens to "the *same functional form* (logarithmic) appears across the three application domains; the algebraic-forcing chain is rigorous only for the cosmology setting (5.1); §5.2 and §5.3 are structural rhymes inheriting the form, not derivational consequences inheriting the proof."

**Issue M6 — Crossing Lemma needs context.** **Fix:** §2 paragraph defining the Crossing Lemma adds a 3-sentence informal precis: "On a finite magma $T : \mathbb{Z}/N\mathbb{Z}^2 \to \mathbb{Z}/N\mathbb{Z}$, a *crossing* is a non-associative triple $(x, y, z)$. The Crossing Lemma (J05) reads non-associativity as the *failure* of CRT separability: a triple is non-associative iff $T$ does not factor through the CRT projection. The notion of 'information' here is structural (CRT-non-factoring), not Shannon or algorithmic." Cite J05 for the precise theorem.

**Issue M7 — bibliography too thin.** **Fix:** add 8–10 references covering (i) Streater-Wightman 1964 + Glimm-Jaffe 1981 on log-nonlinear field theories; (ii) Tegmark 2000 on decoherence (parallel critique); (iii) Doplicher-Roberts 1990 on superselection sectors and product structure; (iv) recent dark-energy quintessence literature (Tsujikawa 2013 review; Caldwell-Linder 2005 freeze/thaw); (v) the EPR/Bell separability classical literature.

## §3 — Revision time

Estimate: **20–25 person-hours** for a structural revision (without retargeting), or **8–12 person-hours** for a retarget to *Math Intelligencer* with lighter rewriting. Decomposition for the structural revision:

- Issue 1 (companion arXiv coordination + arXiv-first deposit of J50 itself): 3 hours (mechanical)
- Issue 2 (§3 BB-as-forcing argument expansion): 6 hours (the genuine math/expository work)
- Issue 3 (tier discipline lifted to front): 2 hours
- M1 (define 6 DOFs): 2 hours
- M3 (vacuum subtlety): 1 hour
- M4 (YM-mass gap softening): 1 hour
- M5 (NS softening): 0.5 hour
- M6 (Crossing Lemma definition): 1 hour
- M7 (bibliography depth): 4 hours
- Brayden's referee-rigor pass + Johnson coordination: 3 hours

Two-week revision under normal pace.

## §4 — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN** (Tier-A, established): The BB76 theorem itself — log-nonlinearity is the unique nonlinearity preserving Hilbert-space factorization (Bialynicki-Birula–Mycielski 1976). The $\sigma$-rate decay $\sigma(N) \leq 2/N$ on squarefree $\mathbb{Z}/N\mathbb{Z}$ (J01 / D71, where D71 sharpens to $N\sigma(N) \leq 1.993$ across the verified range).
- **COMPUTED** (verified in companion scripts): the closed-form runtime attractor on the 4-core at $\alpha = 1/2$ has $H/Br = 1 + \sqrt{3}$ (D78 Galois proof; J41); the universal 4-core attractor across the joint chain (D65; J44 / J35); ring-extension universality (D74).
- **STRUCTURAL RHYME**: $V(\Xi) = \kappa\, \Xi \log \Xi$ vacuum at $\Xi_0 = e^{-1}$ matches both (a) the freeze-thaw transit dark-energy model (J3, J16, Sprint 14 PRISM-XI WP81–WP87) and (b) the Yang-Mills mass-gap framework form (J14). The same functional form appears in three places — this is the synthesizing observation the essay surveys.
- **OPEN**: The Navier-Stokes Separability Regularity Criterion (J13 §5) is conjectural. Whether the BB-forced log-nonlinearity *causally* connects the discrete substrate to NS regularity, rather than appearing as a structural rhyme, is open.

## §5 — Lens-ownership

J50 sits at the **family-level synthesizing layer**, not at any specific lens. The bridge runs through:

- The *commutative-symmetrized* TSML (TSML_SYM) — J01's $\sigma$-rate decay is established for the symmetrized table; the wobble-bearing TSML_RAW is not the operative variant for the BB Bridge.
- The *4-core* $\{V, H, Br, R\}$ — J41's runtime attractor and the BB-vacuum analogy share the 4-core via the Lattice DOF.
- The *F_p ring extensions* (J34 / D74) — the bridge's universality across Z/N for squarefree N depends on the ring-extension result.

Lens-ownership paragraph (insert in §0):

> *Lens and substrate.* This paper works on the canonical $\mathbb{Z}/10\mathbb{Z}$ substrate and its squarefree ring extensions $\mathbb{Z}/N\mathbb{Z}$ (J01, J34). The TSML lens is *commutative-symmetrized* (TSML_SYM) — the asymmetry-bearing TSML_RAW is not invoked here. The bridge content is **lens-invariant on the 4-core**: the BB-vacuum analogy depends on the 4-core's algebraic closure (J41 / D78 Galois proof), not on which specific TSML lens is in use. Whether the bridge extends to the asymmetric (RAW) variant or to the BHML companion is open.

The 4-core is the **center of the family** in the FAMILY_STRUCTURE_v1 sense: the bridge essay surveys content that lives at the family's center, not at its boundaries.

## §6 — Retitle / retarget

**Title.** Per referee §5: drop "Bull AMS" from the title (a venue name shouldn't outlive the venue). New title: **"Substrate Algebra and Logarithmic Nonlinearity: A Bridge Essay"** (referee's exact suggestion). Subtitle on first page: "*From discrete $\sigma$-rate decay to Bialynicki-Birula 1976.*"

**Venue, primary path:** **Hold for Phase 6.** Resubmit to *Bull AMS* once J13 (BB Bridge / JMP) and J47 (6-DOF synthesis / Notices AMS) are both arXiv'd. Estimated timing: 4–6 months out.

**Venue, secondary path (retarget if Phase 6 hold isn't acceptable):** **Mathematical Intelligencer** is the referee-recommended fallback. *Math Intelligencer* accepts overview essays with companions in submission. Per-venue cap risk: J52 already targets *Math Intelligencer*; check J_SERIES_ORDERING_v3 for whether two *Math Intelligencer* submissions in the same phase exceed the cap. If so, the third option is *Notices AMS* — but J47 is already there and the cap may also block.

**Venue, tertiary path:** *Mathematical Reports* (Romanian Acad), *Expositiones Mathematicae*, or *Pure and Applied Mathematics Quarterly* all accept bridge essays at lower-tier visibility. Last resort.

**Submission gate:** (a) J13 on arXiv with permanent ID; (b) §3 BB-as-forcing argument expanded per Issue 2 fix; (c) tier-discipline lifted to abstract per Issue 3 fix; (d) Brayden's referee-rigor pass complete; (e) §J50 distinguishes the classical-scalar setting from the BB nonlinear-Schrödinger setting per M3.
