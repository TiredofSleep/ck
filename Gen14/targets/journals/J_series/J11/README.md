# J11 — Corrected M+A Sufficiency on Squarefree Z/nZ via Zero-Fiber Analysis

**Status:** REVISED (post fresh-eyes referee, 2026-05-08)
**Phase:** Phase 2
**Target venue:** *Journal of Number Theory* (short-note format)
**Author lane:** Sanders + Gish
**Tier:** B (PROVEN theorem + COMPUTED counterexample)
**WP source:** WP59 (Sprint 12 corpus)

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex` (amsart, ~5 pages)

**Abstract.** A natural conjecture for the M+A sufficiency of partition pairs $\{\pi_{\mathrm{DYN}}(G), \pi_d\}$ on squarefree Z/nZ asserts that the pair is sufficient iff the natural map $\varphi: G \to (\Z/d\Z)^*$ is injective. The conjecture is necessary but not sufficient. The counterexample $n=15$, $G=\langle 2 \rangle$, $d=5$ shows $\varphi$ is a bijection but the orbit $\{5, 10\}$ creates a conflict. The corrected condition: G acts trivially at every prime of n/d. The corrected condition is the symmetric form of the established A+M classification (also proved here for self-containment) and is forced by the zero-fiber analysis: G-orbits on $F_d := \{x \equiv 0 \pmod d\}$ are constrained to a single $\pi_d$-block, so size ≥ 2 orbits there are conflicts unaddressed by the unit-only argument.

## §2 — Verification

No script needed; all numerical claims hand-checkable in under five minutes. Independently verified by enumeration:

- $G = \langle 2 \rangle$ in $(\Z/15)^*$ has order 4; $\varphi(G \mod 5) = \{1, 2, 4, 3\}$, a bijection.
- Orbit of 5 under $T_2$ in $\Z/15$ is $\{5, 10\}$, both ≡ 0 (mod 5).
- The pair $\{5, 10\} \in U(\pi_{\mathrm{DYN}}(G)) \cap U(\pi_5)$ is a conflict.
- Control example: $n=30$, $G=\langle 11 \rangle$, $d=5$ has $\varphi$ NOT injective AND the corrected condition fails (both reasons for non-sufficiency align).
- Parametric disagreement family $n=21, d=7, G=\langle 17 \rangle$: $\varphi$ bijection onto $(\Z/7)^*$, but G acts non-trivially mod 3 = n/d. Direct: orbit of 7 under $T_{17}$ in $\Z/21$ is $\{7, 14\} \subset F_7$, conflict.

## §3 — Dependencies (J-papers cited)

None as load-bearing companions. The paper is now standalone (the previous reference to J10 has been removed; both Theorem 3.1 (corrected M+A) and Theorem 3.2 (A+M classification, inline) are proven by direct CRT-coordinate argument).

J10 is mentioned only in the §1 framing as related work in the same author program; the math here does not depend on it.

## §4 — Cover letter

See `cover_letter.md` in this folder. Updated 2026-05-08 to reflect post-revision standalone-paper framing.

## §5 — Notes

**Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md).** This paper sits within the broader research program on small finite combinatorial structures with explicit CRT-coordinate criteria. The closest published precedent in the same intellectual neighborhood is Drápal & Wanless (2021), *J. Combin. Theory Ser. A* **184**, 105510 — same domain (small finite structures with explicit combinatorial criteria), different specific topic.

**PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN — filled.**

- **PROVEN:** For squarefree $n = p_1 \cdots p_k$, $G \leq \Zns$, $d \mid n$: the pair $\{\pi_{\mathrm{DYN}}(G), \pi_d\}$ is sufficient iff every $g \in G$ satisfies $g \equiv 1 \pmod{p_j}$ for every prime $p_j \mid n/d$. (Theorem 3.1.) The symmetric A+M classification (Theorem 3.2). The zero-fiber action lemma (Lemma 1.1).
- **COMPUTED:** $n = 15$, $G = \langle 2 \rangle$, $d = 5$ counterexample by direct enumeration. $n = 30$, $G = \langle 11 \rangle$ control. Parametric disagreement family at $n = 21$, $d = 7$, $G = \langle 17 \rangle$ verified explicitly.
- **STRUCTURAL RHYME:** The zero-fiber $F_d$ is recursively a smaller copy of the original problem (G-equivariantly $\Z/(n/d)$); the zero-fiber question reduces to the unit-fiber question on a smaller modulus.
- **OPEN:** Finer combinatorial classification of $G \leq \ker \Phi$. Extension to non-squarefree $n$ via $p$-adic components.

**Lens-ownership paragraph.** The paper works on Z/nZ for squarefree $n$ with $k \geq 2$ prime factors, with the partition-pair lens consisting of multiplicative orbit partitions $\pi_{\mathrm{DYN}}(G)$ and additive residue partitions $\pi_d$. These choices are foundational, not derived. The framework's claim is that this lens admits a clean joint-injectivity criterion.

**Per-venue cap:** This is positioned as the 2nd JNT submission in the UOP arc (after J10 lead). Combined word count of the two papers is well under typical author-quarter conventions for short-note format.

### Revision summary (post fresh-eyes referee, 2026-05-08)

Major fixes:
1. **M1.** Reframed "previously stated condition" as "natural conjecture" (no published source needed).
2. **M2.** Standalone paper: removed UOP/J10 dependency from proof of Theorem 3.1; direct CRT-coordinate argument used throughout.
3. **M3.** Honest framing of corrected theorem as the symmetric form of the established A+M classification; paper condensed to ~5 pages.
4. **M4.** Zero-fiber analysis promoted to Lemma 1.1 in the introduction.
5. **M5.** Added explicit parametric disagreement family ($n = 3p, p \equiv 1 \pmod 3$) with worked instance at $p = 7$.
6. **M6.** A+M classification (Theorem 3.2) proved inline by 6-line CRT argument.
7. **M7.** §1.2 heading explicitly labels the unit-only argument as incomplete.

Minor fixes adopted: m1 (title shortened), m2 (duplicate author block removed), m4 (singularize "applications"), m5–m12, m14, m15 — see SAVE_PLAN_J11.md.

## §6 — Submission checklist

- [x] Manuscript .tex finalized
- [x] No verification script needed (hand-checkable; independently verified by numpy)
- [x] Tier-classified central claim explicit (Theorem 3.1 PROVEN)
- [x] Lens-scope annotation in §1.4
- [x] Cover letter finalized (post-revision)
- [x] Dependencies removed (paper standalone)
- [ ] Brayden's referee-rigor pass complete
- [ ] Submitted

---

## §7 — Citation footprint

Sanders, B.R., Gish, M. (2026). "Corrected M+A Sufficiency on Squarefree Z/nZ via Zero-Fiber Analysis." Submitted to *J. Number Theory*.
