# Cover letter — J11: Corrected M+A Sufficiency on Squarefree Z/nZ via Zero-Fiber Analysis

**To:** Editors, *Journal of Number Theory*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Corrected M+A Sufficiency on Squarefree Z/nZ via Zero-Fiber Analysis*

---

## Summary

We submit a short note (~5 pages) correcting a natural-conjecture condition for M+A sufficiency of partition pairs on squarefree Z/nZ. The natural conjecture — that the pair $\{\pi_{\mathrm{DYN}}(G), \pi_d\}$ is sufficient iff the natural map $\varphi: G \to (\Z/d\Z)^*$ is injective — is necessary but not sufficient. It tracks unit-element conflicts but misses zero-fiber conflicts: pairs $\{x, g \cdot x\}$ where $x \equiv 0 \pmod d$ and $g$ acts non-trivially on a prime of $n/d$.

We give the explicit counterexample $n = 15$, $G = \langle 2 \rangle$, $d = 5$, where $\varphi$ is a bijection $G \to (\Z/5)^*$ but the orbit $\{5, 10\}$ creates a conflict in $U(\pi_{\mathrm{DYN}}(G)) \cap U(\pi_5)$. The corrected condition: $G$ acts trivially at every prime of $n/d$, equivalently every $g \in G$ satisfies $g \equiv 1 \pmod{p_j}$ for $p_j \mid n/d$. The corrected condition is the symmetric form of the established A+M classification (also proved here inline for self-containment) and is forced by the zero-fiber analysis: G-orbits on $F_d := \{x : x \equiv 0 \pmod d\}$ are constrained to a single $\pi_d$-block, so size-≥-2 orbits there are conflicts unaddressed by the unit-only argument.

The paper closes with a parametric disagreement family ($n = 3p$ for primes $p \equiv 1 \pmod 3$) where the natural conjecture and corrected condition disagree on infinitely many examples; the smallest instance is $n = 21, d = 7, G = \langle 17 \rangle$, verified by direct enumeration.

## Why JNT

The substance of the paper is a partition-lattice / CRT-coordinate analysis on $(\Z/n)^*$, squarely in the combinatorial number theory corner of JNT's scope. JNT does publish papers on the structure of $(\Z/n)^*$ and related orbit-counting questions; the present paper is in the "natural conjecture → counterexample → corrected theorem → structural reason" genre that fits short-note format particularly well.

## Standalone scope

This paper is now standalone. The proof of the corrected theorem uses only direct CRT-coordinate arguments (no dependency on companion submissions). The companion papers in the broader UOP arc (J10, J12) are mentioned only for context, not as load-bearing references.

## Closest published precedent

The paper sits in the same intellectual neighborhood as Drápal & Wanless (2021), *J. Combin. Theory Ser. A* **184**, 105510, on small finite combinatorial structures with explicit CRT-coordinate criteria — same domain, different specific topic.

## Reproducibility

The counterexample is self-checking: list $G = \{1, 2, 4, 8\}$ mod 15, compute the orbit of 5 under $T_2$, observe both elements share residue 0 mod 5. Hand-checkable in under five minutes; we have additionally verified by independent numpy enumeration.

## Suggested reviewers

- A specialist in finite ring theory and the partition lattice.
- A specialist in algebraic number theory with squarefree CRT structure expertise.
- A specialist in the orthogonality theory of finite groups.

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
