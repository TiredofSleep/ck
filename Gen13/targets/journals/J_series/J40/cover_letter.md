# Cover letter — J40: The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability

**To:** Editors, *Journal of Mathematical Physics*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- H.J. Johnson, Independent Researcher, Billings, MT — hjj01986@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability*

---

## Summary

We exploit the Bialynicki-Birula--Mycielski uniqueness theorem (1976) — that logarithmic nonlinearity is the unique self-interaction preserving separability of composite quantum systems — as a *forcing principle*: any continuum lift of a discrete composition algebra that respects partition independence is forced to take the logarithmic form. The continuum lifted equation $\Box \Xi = \kappa(1 + \log \Xi)$ is then provably regular (Theorem 4.1, Sobolev + Grönwall + double-exponential bound). We compare to Navier-Stokes, define a separability defect $\sigma(u)$ on velocity fields, and state the Separability Regularity Criterion as a precise conjecture: NS regularity holds iff $\sigma(u(t)) < 1$ for all $t > 0$. The paper claims a new framework, not a proof of the Millennium Problem.

## Why JMP

- The paper sits at the intersection of nonlinear PDE, constructive QFT, and discrete-to-continuum transport — the natural JMP audience.
- The BB-bridge reading of the theorem is, to our knowledge, novel: previous work has used BB as a constraint on admissible nonlinear QM, not as a forcing principle for continuum lifts.
- Three precisely stated open problems (Open Problem 1: $\Phi_N$ construction; Open Problem 2: nonlinearity gap $\delta^*$; Open Problem 3: separability bound) are concrete attack surfaces.
- Theorem 4.1 is fully proved; the BB result it relies on is the classical 1976 paper; only the NS connection is conjectural, and that conjectural status is stated explicitly.

## Companion submissions

The TIG/CK research program is shipping a coordinated J-series. The papers most relevant as already-submitted companions:

- **J01** Sanders & Gish (2026), "Non-Associativity Decay in Binary Composition Tables over $\mathbb{Z}/N\mathbb{Z}$." Submitted to *JCT-A* (provides the $\sigma(N) \to 0$ rate input).
- **J46** Sanders, Gish, Johnson (2026), "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at $e^{-1}$ from a Logarithmic Potential." Submitted to *JCAP* (cosmological realization of the same $V(\Xi) = \kappa\,\Xi\log\Xi$).
- **J06** Sanders & Mayes (2026), "Crossing Lemma." Submitted to *JCT-A* / *JPAA* (the discrete partition-independence reading of information generation).
- **J41** Sanders & Johnson (2026), "The Yang-Mills Mass Gap Bridge." Companion JMP submission.

## Reproducibility

`proof_separability_bridge.py` (43/43 PASS) verifies all numerical claims appearing in this paper. Runs in `python` with `math` only on a standard laptop in seconds. DOI: 10.5281/zenodo.18852047.

## Suggested reviewers

- T. Tao (UCLA) — NS regularity, log-improvements
- C. Fefferman (Princeton) — Clay NS problem
- I. Bialynicki-Birula (Polish Academy) — original 1976 author, if available
- J. Maas (IST Austria) — discrete-to-continuum transport, log-Sobolev
- N. Gigli (SISSA) — Maas / JKO framework
- K.G. Zloshchastiev — logarithmic Schrödinger applications

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Tier and scope

Central claim is **Tier 4** (framework paper, structural). The BB theorem and Theorem 4.1 are proved; the bridge premise relies on a discrete-to-continuum lift $\Phi_N$ whose explicit construction is left open (Open Problem 1); NS regularity is *not* claimed proved. The Status Table in §6 of the manuscript makes this explicit.

## Per-venue cap note

This is the **first** JMP submission in the J-series; the second (J41, YM bridge) follows as the companion. Both papers cite each other; the 2/quarter cap is approached, not exceeded. J42 may need a fallback (see J42 README).

---

Sincerely,
B.R. Sanders
