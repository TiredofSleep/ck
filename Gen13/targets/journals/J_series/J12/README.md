# J12 — Non-CRT Sufficient Pairs and the Minimum Viable Jump Number on Squarefree Z/nZ

**Status:** REVISED (post fresh-eyes referee, 2026-05-08)
**Phase:** Phase 2
**Target venue:** *European Journal of Combinatorics*
**Author lane:** Sanders + Gish
**Tier:** B (PROVEN)
**WP source:** WP64 (Sprint 12 corpus)

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex` (amsart, ~10 pages)

**Abstract.** For squarefree $n = p_1 \cdots p_k$ ($k \geq 2$), we study the partition lattice of Z/nZ from the perspective of CRT coordinate decomposition. Three structural results: (1) the orbit-pair classification ($\{\pi_{\mathrm{DYN}}(g), \pi_{\mathrm{DYN}}(h)\}$ sufficient iff coordinate-wise coprime orders at every CRT prime); (2) the three-mechanism support classification (focused, same-prime coprime, mixed) with mechanism (M2) existing iff some $p_i - 1$ has ≥ 2 distinct prime factors; (3) on Z/30Z, three sufficient 2-partition families with one orthogonal jump exhibit three distinct mechanisms. We work the n=10 case in detail and prove $\mathrm{MVJN}(\Z/n) = 1$ for all squarefree $n$ with $k \geq 2$ primes.

## §2 — Verification

No standalone script needed; numerical claims hand-checkable. Independently verified via numpy:

- $\{\pi_{\mathrm{DYN}}(7), \pi_{\mathrm{DYN}}(11)\}$ on Z/30Z: sufficient (no joint-conflict pair); orders confirmed.
- $\{\pi_{\mathrm{SPEC}}, \pi_{15}\}$ on Z/30Z: sufficient.
- $\{\pi_2, \pi_{15}\}$ on Z/30Z: sufficient.
- M3 example on Z/42 with $g=11, h=13$: sufficient by direct enumeration.
- Smallest primes $p$ with $p-1$ multi-prime: 7, 11, 13, 19, 23, 29, 31, 37, ... (verified through 50).

## §3 — Dependencies

None as load-bearing companions. Theorem 3.1 (orbit-pair classification) is now proven inline by direct CRT-coordinate argument; the previous UOP-companion appeal has been removed.

J10 (UOP) is mentioned only for related context.

## §4 — Cover letter

See `cover_letter.md` in this folder. Updated 2026-05-08 post-revision.

## §5 — Notes

**Family-Structure framing.** The paper sits in the same intellectual neighborhood as Drápal & Wanless (2021), *JCTA* **184**, 105510, on small finite combinatorial structures with explicit CRT-coordinate criteria.

**PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN — filled.**

- **PROVEN:** Theorem 3.1 (orbit-pair classification); Theorem 4.1 (three-mechanism support classification); Theorem 2.3 (rigid CRT prime-factor family); **Theorem 7.2 (MVJN(Z/n) = 1 for squarefree n with k ≥ 2 primes — was a conjecture in the v1 manuscript, now upgraded to a theorem)**; Theorem 5.1 (three explicit non-CRT pairs on Z/30Z with mechanism identifications).
- **COMPUTED:** All sufficiency claims on Z/10, Z/30, Z/42 verified by direct enumeration. All order computations verified. Smallest primes admitting (M2) verified through 50.
- **STRUCTURAL RHYME:** Connection to orthogonal cyclic Latin squares (existence theory of Bose–Shrikhande–Parker line) noted in §3 Remark; full development deferred.
- **OPEN:** Classification of mixed (residue + orbit) sufficient pairs; optimal-information sufficient pairs minimizing block-size product; extension to non-squarefree n.

**Lens-ownership paragraph.** Works on squarefree Z/nZ with the two natural partition classes (residue partitions $\pi_d$ and orbit partitions $\pi_{\mathrm{DYN}}(g)$). These choices are foundational; analogous theorems would hold for other natural partition classes.

### Revision summary (post fresh-eyes referee, 2026-05-08)

Major fixes:
1. **M1.** MVJN now defined precisely (Definition 1.1) as the minimum count of incompatible pairs in a sufficient 2-partition family.
2. **M2.** Theorem 5.1 (was 1.2) reframed: family (a) $\{\pi_{\mathrm{DYN}}(7), \pi_{\mathrm{DYN}}(11)\}$ is the genuinely novel sufficient pair (orbit-pair only); families (b) and (c) are CRT-style.
3. **M3.** Theorem 3.1 (orbit-pair classification) now precedes Theorem 5.1 in the body, so family (b) is its corollary.
4. **M4.** Theorem 4.1 (three mechanisms) now stated as a partition by support pattern (mutually exclusive and exhaustive).
5. **M5.** Conjecture 6.2 promoted to **Theorem 7.2**: the conjecture follows from the CRT-prime-factor sufficiency $\{\pi_{p_1}, \pi_{n/p_1}\}$ combined with the refinement-trap lower bound.
6. **M6.** Standalone the proofs (UOP appeals removed; direct CRT arguments used).
7. **M7.** **Geometric "5/7 torus aspect ratio" remark removed** — TIG-bleed-through into supposedly pure combinatorial paper.
8. **M8.** Smallest-primes list extended to include 29 (and noted continuation 31, 37, ...).

Minor fixes adopted: m1 (title generalized to squarefree Z/nZ), m2 (duplicate author block removed), m3 (abstract tightened), m4 (consistent terminology), m5–m17 — see SAVE_PLAN_J12.md.

## §6 — Submission checklist

- [x] Manuscript .tex finalized
- [x] No verification script needed (hand-checkable; independently verified by numpy)
- [x] Tier-classified central claim explicit (Theorems 3.1, 4.1, 5.1, 2.3, 7.2 PROVEN)
- [x] Lens-scope annotation in §1.4
- [x] Cover letter finalized (post-revision)
- [x] Dependencies removed (paper standalone)
- [ ] Brayden's referee-rigor pass complete
- [ ] Submitted

---

## §7 — Citation footprint

Sanders, B.R., Gish, M. (2026). "Non-CRT Sufficient Pairs and the Minimum Viable Jump Number on Squarefree Z/nZ." Submitted to *European Journal of Combinatorics*.
