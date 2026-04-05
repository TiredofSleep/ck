# CASE-B NAILDOWN MEMO
# Which Branchwise r-Formulas Are Real, Which Are Surrogates, Which Need Demotion?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## OUTCOME SUMMARY

| Branch | r-status BEFORE | r-status AFTER | Movement |
|--------|----------------|----------------|----------|
| RH | Exact intrinsic | **Exact intrinsic** | Confirmed |
| NS | Surrogate B | **UPGRADED: Intrinsic A** | ↑ |
| BSD | Direct approx. | **Explicit surrogate B** | Clarified |
| Hodge | Provisional B | **DEMOTED: Analogy only C** | ↓ |
| YM weak | Proxy B | **Proxy only** | Confirmed low |
| P vs NP | Structural limit | **DEMOTED: Unknown encoded as zero** | ↓ |
| YM excited | Structural limit | **DEMOTED: Unknown encoded as zero** | ↓ |

---

## PART 1 — Frozen State

| Property | Value |
|---------|-------|
| Universal skeleton | $f(x) = \mathrm{sinc}^2(r(x))$ for $f \leq 1$; $f = 1/\mathrm{sinc}^2(r)$ for $f > 1$ |
| $\mathrm{fold}$ | $4/\pi^2 = \mathrm{sinc}^2(1/2)$ |
| $T^*$ | $5/7 = \mathrm{sinc}^2(r_{T^*})$, $r_{T^*} = 0.3144$ |
| RH exact | $r = \mathrm{Re}(s)$ |
| BSD approx | $r \approx 1 - 2\varepsilon$ (incoming claim) |
| NS surrogate | $r = 1 - Q/(2\nu P)$ (incoming claim) |
| Hodge provisional | $r = n/8$ coverage-fraction schema |
| YM weak proxy | $r \approx 1/(1+g^2 N)$ |
| P vs NP, YM excited | $r = 0$ (incoming: structural limit) |

---

## PART 2 — BSD Hardening

### Exact formula test

From the BSD data:
- $L'_{\mathrm{obs}} = 0.0106998338$
- $L'_{\mathrm{pred}} = \Omega_E/(4\sqrt{77}) \times \det(H) = 0.0108165$
- Normalization residual: $\varepsilon = |L'_{\mathrm{obs}} - L'_{\mathrm{pred}}|/L'_{\mathrm{pred}} = 1.079\% = 0.010787$
- Inferred $r = 0.97646$, so $1-r = \delta = 0.02354$

**The correct small-$\delta$ approximation** for $r$ near 1:

$$\mathrm{sinc}^2(r) = \left(\frac{\sin\pi\delta}{\pi(1-\delta)}\right)^2 \approx \delta^2 \quad \text{for } \delta = 1-r \ll 1$$

Therefore: $f \approx \delta^2 = (1-r)^2$, and the exact inversion gives:

$$r_{\mathrm{BSD}} \approx 1 - \sqrt{f}$$

Check: $r = 1 - \sqrt{5.8 \times 10^{-4}} = 1 - 0.02408 = 0.97592$ vs actual $0.97646$ (error $0.0006$).

### Was $r = 1 - 2\varepsilon$ correct?

**No. It was a coincidental fit.** The ratio $(1-r)/\varepsilon = 2.18$, not exactly 2. The correct structural relationship is $r = 1 - \sqrt{f}$. The connection between $f$ and $\varepsilon$ requires a separate formula $f_{\mathrm{BSD}} = g(\varepsilon)$ that the current BSD theory does not provide.

### Is $\varepsilon$ probe-independent?

**YES.** The normalization residual $\varepsilon = |L'_{\mathrm{obs}} - L'_{\mathrm{pred}}|/L'_{\mathrm{pred}}$ is computed from actual $L$-function values and BSD period data — not from probe count.

### What about the factor $\sqrt{f/\varepsilon^2} = 2.233$?

This is $\sqrt{f}/\varepsilon = \sqrt{5.8 \times 10^{-4}}/0.010787 = 2.233$. It is NOT derivable from BSD theory alone. It would require knowing how the defect value $f_{\mathrm{BSD}}$ maps to the normalized $L$-function residual $\varepsilon$ — a relationship not established in the current framework.

### BSD overflow (rank mismatch, $f=1.300$)

$r = 0.2787$ (from $1/\mathrm{sinc}^2(0.2787) = 1.300$). The rank-mismatch case (analytic rank $\neq$ algebraic rank) corresponds to $r < r_{T^*}$ — a genuine structural gap. No explicit intrinsic formula for $r$ at this escape is currently derivable.

### BSD verdict

**Explicit surrogate (B).** $\varepsilon$ is intrinsic and probe-independent. The relationship $f = g(\varepsilon)$ is not known. The formula $r = 1-\sqrt{f}$ is the exact sinc² inversion for the resolved case, but it inverts the probe output — it does not derive $r$ from BSD invariants directly.

---

## PART 3 — Hodge Hardening

### Can $n$ be made explicit from A_* data?

Four tests, all failing:

| Test | Formula | Result for A_* | Status |
|------|---------|---------------|--------|
| **1.** $n$ = number of accessible obstruction directions | $n = \dim(\text{algebraic} \cap W_*)$ | $n = 0 \Rightarrow r = 0$ | **IMPOSSIBLE** |
| **2.** $n$ = dim of algebraically covered subspace in $W_*$ | Same as test 1 | $n = 0 \Rightarrow r = 0$ | **IMPOSSIBLE** |
| **3.** $n$ = weighted block coverage $(\lambda_{B_1}+\ldots)/\lambda_{\mathrm{total}}$ | First $k$ blocks / total | $r \in \{0.009, 0.053, 0.272, 1.0\}$ for $k=1,2,3,4$ | None match $r \approx 0.38$ |
| **4.** $n$ = $Q$-weighted single block | $\lambda_{B_1}/\lambda_{\mathrm{total}}$ or $1 - \lambda_{B_4}/\lambda_{\mathrm{total}}$ | $0.009$ or $0.272$ | **Neither matches** |

**Root cause:** The labels "analytic_only" and "known_transcendental" refer to abstract Hodge problem sub-cases (instances of the conjecture for classes of varieties), NOT to the A_* testbed computation. For A_* specifically, the algebraic coverage of $W_*$ is exactly zero — which would give $r = 0$, contradicting the probe-assigned values of $0.377$ and $0.321$.

**Conclusion:** The Hodge formula $r = n/8$ requires a meta-level count of which abstract Hodge sub-cases are resolved, which is not computable from the A_* cohomology data.

### Hodge verdict: DEMOTE TO ANALOGY ONLY (C) for the A_* testbed

The formula $r = n/8$ describes a useful coverage schema for the abstract Hodge landscape but is not derivable from the computed invariants of any specific Weil 4-fold. For A_*, the only honest value is $r_{\mathrm{alg}} = 0$ (zero algebraic coverage of $W_*$), which maps to $f = 1$ — the escaped regime. The "analytic_only" and "known_transcendental" labels encode prior Hodge knowledge not present in the A_* computation.

---

## PART 4 — NS Hardening

### Is the formula $r_{\mathrm{NS}} = 1 - Q/(2\nu P)$ intrinsic?

**Derivation from governing equation:**

The NS enstrophy evolution is:

$$\frac{d\Omega}{dt} = Q - 2\nu P$$

where $Q$ = vortex-stretching term, $\nu$ = viscosity, $P$ = palinstrophy. The critical threshold is $Q/(\nu P) = 2$:

$$\frac{d\Omega}{dt} < 0 \iff Q/(\nu P) < 2 \quad \text{(resolved: enstrophy decays)}$$

Setting $r = 1 - Q/(2\nu P)$:

| $Q/(\nu P)$ | $r$ | Classification |
|------------|-----|---------------|
| $0$ (zero vortex-stretching) | $1$ | RESOLVED (deep) |
| $1$ | $\mathbf{1/2}$ | **Fold boundary** $= \mathrm{sinc}^2(1/2) = 4/\pi^2$ |
| $2$ | $0$ | Escaped threshold |
| $> 2$ | $< 0$ | Overflow (needs extension) |

**Critical alignment:** $r = 1/2$ corresponds exactly to $Q/(\nu P) = 1$ — half the NS threshold. The fold threshold $4/\pi^2 = \mathrm{sinc}^2(1/2)$ aligns with half the enstrophy escape threshold. This is derived, not fitted.

**Five upgrade tests:**

| Test | Status |
|------|--------|
| Formula derived from governing equation | ✓ YES |
| Threshold 2 algebraically exact (from $d\Omega/dt = Q - 2\nu P$) | ✓ YES |
| $r \in [0,1]$ in resolved regime ($Q/\nu P \leq 2$) | ✓ YES |
| Small-data shell: $Q/\nu P \ll 1 \Rightarrow r \approx 1$ (RESOLVED) | ✓ YES |
| Probe-independent ($Q/\nu P$ is a flow quantity) | ✓ YES |

### NS verdict: **UPGRADE TO INTRINSIC (A)**

$r_{\mathrm{NS}} = 1 - Q/(2\nu P)$ is the second fully intrinsic branch coordinate after RH. It is derived from the governing enstrophy equation, has an algebraically exact threshold, and requires no finite probe count.

---

## PART 5 — YM Weak Hardening

### Is $r \approx 1/(1+g^2 N)$ derived or guessed?

**Key diagnosis:** the formula $1/(1+g^2 N)$ is a Padé approximant of $e^{-g^2 N}$ at leading order. Both give $r \to 1$ as $g^2 N \to 0$ and $r \to 0$ as $g^2 N \to \infty$. At the specific weak-coupling value that gives $r = 0.9924$, the coupling $g^2 N = 1/r - 1 = 1/0.9924 - 1 = 0.00766$.

**Three tests:**

1. **What exact object has coupling $g^2 N = 0.00766$?** NOT STATED. The YM_weak_coupling object is labeled but not given a specific coupling value in the probe data.

2. **Why $1/(1+g^2 N)$ vs $e^{-g^2 N}$ vs other monotone forms?** No derivation from YM spectral theory distinguishes these forms at this level of data.

3. **Can the formula be derived from the perturbative mass-gap picture?** The YM spectral gap involves the running coupling, but the specific formula $1/(1+g^2 N)$ is not the standard perturbative expression — it is shape-matched.

### YM verdict: **PROXY ONLY (remains)**

The formula has correct qualitative behavior but is not derived from YM theory. No upgrade is justified.

---

## PART 6 — P vs NP and YM Excited Demotion

### P vs NP ($r = 0$, $f = 1.000$)

**Demotion test:**

Does any P vs NP invariant actually give $r = 0$?
- The superpolynomial lower bound $\mathrm{cc}(\mathrm{SAT},n)$ is unproved
- No known invariant of the P vs NP problem takes the value $0$ in a meaningful sense
- The freeze at $f = 1.000$ is the sinc² model hitting its ceiling

**Verdict: OPTION C — "unknown" encoded as zero.**

The defect value $1.000$ encodes: "no structural coverage of this branch is currently established within the probe framework." It is not a coordinate value derived from the circuit complexity of SAT.

### YM excited ($r = 0$, $f = 1.000$)

**Demotion test:**

The non-perturbative YM regime has no weak-coupling expansion accessible. The formula $r = 1/(1+g^2 N)$ gives $r \to 0$ as $g^2 N \to \infty$, which is the correct qualitative limit. But:
- The specific value $r = 0$ (not $r = 0.001$ or $r = 0.1$) is not derived
- It is the ceiling of the probe model, not a computed invariant

**Verdict: OPTION C — "unknown" encoded as zero.**

**Both demoted.** $r = 0$ for these two objects is probe saturation, not a real invariant. The fact that both freeze at exactly $f = 1.000$ (not $f = 0.95$ or $f = 1.05$) reflects that the probe model assigns maximum defect to objects with zero recoverable structure — not that these objects have a computable coordinate $r = 0$.

---

## PART 7 — Shared Schema Audit

### Schema: $r(x) = \varphi(\mathrm{coverage\_fraction}(x))$

**Test 1 — Is it a theorem pattern?**

NO. The three recovered intrinsic/explicit formulas have entirely different justifications:
- RH: $r = \mathrm{Re}(s)$ — a geometric coordinate in the critical strip
- NS: $r = 1 - Q/(2\nu P)$ — a rescaled ratio from the governing enstrophy equation
- BSD: $r = 1 - \sqrt{f_{\mathrm{BSD}}}$ — a probe output inversion (NOT intrinsic)

There is no common theorem that generates these from a single principle. The "coverage fraction" language is a post-hoc description, not a derivation.

**Test 2 — Is it a useful organizing schema?**

YES, with limits. The schema captures that: (a) all recoverable $r$ formulas are monotone in some branch measure, (b) $r = 1/2$ (the fold) is the universal midpoint in every branch where $r$ is defined, and (c) $r = 0$ corresponds to the extreme-hardness limit in every branch. These alignments are real and useful.

**Test 3 — Is it a dangerous over-compression?**

PARTIALLY. For three branches (Hodge, P vs NP, YM excited), the schema produced no computable formula and led to either analogy or demotion. Treating the schema as a theorem would over-read it.

**Final verdict: Option 2 — useful organizing schema, explicitly NOT a theorem.**

---

## PART 8 — Final Six-Branch Table

| Branch | Current formula for $r$ | Status | Nail strength | Next exact task |
|--------|------------------------|--------|---------------|----------------|
| **RH** | $r = \mathrm{Re}(s)$ | **Intrinsic (A)** | **Hard** | None: formula is complete |
| **NS** | $r = 1 - Q/(2\nu P)$ | **Intrinsic (A)** | **Hard** | Verify overflow formula for $Q/\nu P > 2$ |
| **BSD** | $r = 1 - \sqrt{f_{\mathrm{BSD}}}$ | **Explicit surrogate (B)** | **Medium** | Find explicit $f_{\mathrm{BSD}}(\varepsilon)$ formula from BSD theory |
| **Hodge** | $r = n/8$ schema (non-computable from A_*) | **Analogy only (C)** | **Weak** | Define $n$ from abstract Hodge sub-case coverage, independent of A_* |
| **P vs NP** | $r = 0$ (unknown encoded as zero) | **Structural limit** | **None** | Demoted: no formula possible until circuit lower bounds exist |
| **YM** | $r \approx 1/(1+g^2 N)$ (weak, shape fit); $r=0$ (excited, demoted) | **Proxy (B-)** | **Weak** | Derive $r$ from YM spectral gap formula, not coupling proxy |

**Hard nails: RH, NS.** Medium nail: BSD. Demoted/analogy: Hodge, YM, P vs NP.

---

## PART 9 — Strongest Honest Claim

**"The CASE B result is now nailed down to the statement that exactly two branches — RH and NS — have fully intrinsic, probe-independent formulas for $r(x)$: $r_{\mathrm{RH}} = \mathrm{Re}(s)$ derived from the critical-strip geometry, and $r_{\mathrm{NS}} = 1 - Q/(2\nu P)$ derived from the enstrophy evolution equation; BSD has an explicit surrogate $r = 1 - \sqrt{f_{\mathrm{BSD}}}$ (a probe-output inversion, not an intrinsic derivation); Hodge is demoted to analogy only because no formula for $r$ is computable from the A_* cohomology data; and P vs NP and YM excited are demoted to unknown-encoding because their $r = 0$ values are probe saturation ceilings, not derived coordinates."**

---

## PART 10 — Strongest Honest Boundary

**"What is still not established is whether the branchwise coordinate $r(x)$ for BSD can be expressed as an explicit function of the normalized $L$-function residual $\varepsilon$ without knowing the defect value $f$ first — that is, whether $f_{\mathrm{BSD}} = g(\varepsilon)$ for some function $g$ derivable from BSD theory alone — which is the exact gap between the BSD surrogate status and full intrinsic status; and whether the fold alignment $r = 1/2$ for all three intrinsic/surrogate branches (RH: $\mathrm{Re}(s) = 1/2$; NS: $Q/\nu P = 1$; BSD: approximate) reflects a genuine universal half-structure principle or is a coincidence of the sinc² parameterization."**

---

## Collaborator Paragraph

The naildown produced two clean results and two clean demotions. NS is upgraded to fully intrinsic: $r_{\mathrm{NS}} = 1 - Q/(2\nu P)$ is derived from $d\Omega/dt = Q - 2\nu P$, has algebraically exact threshold $Q/\nu P = 2$, and places the fold boundary exactly at $Q/\nu P = 1$ (half the NS escape threshold) — this is not fitted, it is algebraically forced. BSD is clarified: the earlier "factor 2" claim ($r = 1-2\varepsilon$) was a coincidental fit; the correct small-$\delta$ approximation gives $r = 1-\sqrt{f}$ (probe-output inversion), and $\varepsilon$ is intrinsic but the map $\varepsilon \mapsto f$ is not established from BSD theory. Hodge is demoted: all four tests for making $n$ explicit from A_* data fail (algebraic coverage on A_* is exactly 0, giving $r = 0$, wrong), and the labels "analytic_only" / "known_transcendental" refer to abstract Hodge sub-cases not computable from A_*. P vs NP and YM excited are demoted: $r=0$ is probe saturation encoding "unknown," not a derived coordinate. The shared coverage schema is not a theorem — it is a useful organizing description that RH and NS support with genuine derivations, while the other branches do not.
