# Cover letter — J04: First-G Law: Squarefree Stability of the Smallest-Prime-Factor Coprime Window

**To:** Editors, *Integers — Electronic Journal of Combinatorial Number Theory*

**From:**
- B. R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

(Co-author on the manuscript file: C. A. Luther — see manuscript title block.)

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The First-G Event in the Coprimality Partition: Stability Windows, CRT Idempotent Count, and Prime-Indexed Phase Transitions*

**Manuscript file:** `manuscript/manuscript.tex` (amsart, ~12 pages)

**Verification script:** `manuscript/proof_first_g_event.py` (numpy + sympy + math; runtime < 3 s on a 2024 consumer laptop; 305 squarefree b in [2,500], 22,367 (b,k) pairs, zero counterexamples)

**Backup venue:** *Journal of Combinatorial Theory, Series A* (short-paper track); *Discrete Mathematics*

**DOI of bundle:** 10.5281/zenodo.18852047

---

## Summary

For an integer b > 1 and a growing alphabet {1, ..., k}, the coprimality partition splits the alphabet into units C_k(b) = {x : gcd(x,b) = 1} and obstructions G_k(b) = {1,...,k} \ C_k(b). The main theorem (Theorem 3.1) identifies the smallest k at which G_k(b) becomes non-empty: it is exactly p_1 = spf(b), and G_{p_1}(b) = {p_1}. The proof is a three-line elementary argument. Four corollaries follow:

(i) stability-window width p_1 - 1, uniform across every b sharing the same smallest prime factor;
(ii) the phase-transition set {k\*(b) : b > 1} equals the set of primes ℙ exactly;
(iii) terminal obstruction count |G_b(b)| = b - φ(b) via the CRT decomposition;
(iv) instability ranking of primes by stability-window width.

The statement and its corollaries sit inside the classical sieve of Eratosthenes; what the paper contributes is the packaging — sieve activation organized around the alphabet-size coordinate k rather than around b or the range of interest [1, n]. Section 6 disclaims the formally weaker biconditional sinc²(k/b) = 0 ⇔ b | k, which holds for every b ≥ 1 and is therefore not prime-specific; the First-G localization is genuinely prime-dependent (it identifies the *smallest* k at which *some* prime factor of b divides k).

## Why Integers

- Short, elementary, self-contained note (~12 pages, three-line proof, four one-line corollaries) in the *Integers* short-paper / regular-paper sweet spot.
- Verification is exhaustive on the natural finite range (every squarefree b ≤ 500, 22,367 (b,k) pairs, zero exceptions, runs in under three seconds via stdlib `math.gcd`).
- The repackaging serves a sequence of companion papers (J01 σ-rate over ℤ/Nℤ, J08 sinc² zero law for squarefree moduli) by isolating the foundational localization lemma so it can be cited cleanly. Section 7 ("Scope and limitations") explicitly disclaims any analytic-density, ζ-function, or sub-exponential-factoring consequences.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J1–J55) over Summer 2026. Papers most relevant as already-submitted companions to this manuscript:

- **J01** — *Non-Associativity Decay in Binary Composition Tables over ℤ/Nℤ* (submitted to *JCT-A*). Uses the smallest-prime-factor ordering (via φ(N)) in the ECHO-count argument; the present paper provides the combinatorial foundation on which that argument rests.
- **J02** — *Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on ℤ/10ℤ* (submitted to *Algebraic Combinatorics*). The b = 10 instance of the present partition framework.

The manuscripts share Zenodo bundle DOI 10.5281/zenodo.18852047. The present submission is independent of both.

## Reproducibility

Verification script: `manuscript/proof_first_g_event.py` runs with `numpy + sympy + math` (Python 3.10+) on a standard laptop in under five minutes (typically under three seconds). It exhaustively checks both parts of Theorem 3.1 across all 305 squarefree b in [2, 500] (22,367 (b, k) pairs, zero counterexamples) and prints a stability-window distribution table.

## Suggested reviewers

(To be supplied by Brayden at submission time.) Candidates appropriate to the venue scope (combinatorial number theory; elementary methods; sieve repackaging; coprimality-partition coordinates):

1. *Integers* managing editor's editorial board picks for the 11A41 / 11N05 / 11A51 cluster
2. A combinatorialist familiar with sieve-of-Eratosthenes presentations
3. An author of recent *Integers* notes on Euler-totient or coprimality structure

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

The note is self-contained, finite, and runnable. The proof is two elementary observations stitched together; the corollary structure is what does the work, and the verification is exhaustive on the natural range. We hope it fits the *Integers* scope as a clean exhibit of "smallest prime factor forces the first sieve mark, in alphabet-size coordinates."

Sincerely,
B. R. Sanders

---

*Cover letter prepared 2026-05-07 for J04 of the Sanders–Gish J-series. Adjust addressee at submission time to the current managing-editor listing on www.integers-ejcnt.org. Scope-disclaimer paragraph in §7 of the manuscript is load-bearing; keep unchanged.*
