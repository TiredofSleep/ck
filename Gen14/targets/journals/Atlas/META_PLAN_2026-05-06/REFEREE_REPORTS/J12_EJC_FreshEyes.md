# Referee Report: J12 / European Journal of Combinatorics

**Manuscript:** "Coordinate Coverage on $\mathbb{Z}/10\mathbb{Z}$: Non-CRT Sufficient Pairs and the Minimum Viable Jump Number"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** European Journal of Combinatorics
**Reviewer:** External referee (anonymous, fresh eyes)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

For squarefree $n = p_1 \cdots p_k$ ($k \geq 2$), the authors study the partition lattice of $\mathbb{Z}/n\mathbb{Z}$ and partition pairs that *separate* (their meet is the discrete partition $\pi_{\mathrm{disc}}$). The setup uses two natural classes of partitions:

- *Residue partitions* $\pi_d$ for $d \mid n$, with blocks $\{x : x \equiv c \pmod d\}$.
- *Orbit (DYN) partitions* $\pi_{\mathrm{DYN}}(g)$ for $g \in (\mathbb{Z}/n\mathbb{Z})^{\times}$, with blocks the multiplicative orbits of $T_g(x) = gx$.

A pair $\{\pi_1,\pi_2\}$ is *sufficient* when $\pi_1 \wedge \pi_2 = \pi_{\mathrm{disc}}$. Two partitions form an *orthogonal jump* when neither refines the other. The *Minimum Viable Jump Number* $\mathrm{MVJN}(\mathbb{Z}/n\mathbb{Z})$ is defined as the smallest number of orthogonal jumps in any sufficient family.

The paper proves four theorems:

**Theorem 1.1 (Rigidity of CRT prime-factor family).** For squarefree $n$ with $k \geq 2$ primes, every minimal sufficient family among $\{\pi_{p_1},\ldots,\pi_{p_k}\}$ has length $k$ and contributes exactly $k - 1$ orthogonal jumps.

**Theorem 1.2 (Non-CRT pairs on $\mathbb{Z}/30\mathbb{Z}$).** Three sufficient $2$-partition families on $\mathbb{Z}/30\mathbb{Z}$ exist with exactly one orthogonal jump:
- (a) $\{\pi_{\mathrm{SPEC}},\pi_{15}\}$ (residue + reflection),
- (b) $\{\pi_{\mathrm{DYN}}(7),\pi_{\mathrm{DYN}}(11)\}$ (orbit + orbit),
- (c) $\{\pi_2,\pi_{15}\}$ (residue + residue).

In particular $\mathrm{MVJN}(\mathbb{Z}/30\mathbb{Z}) = 1$.

**Theorem 1.3 (Orbit-pair classification).** For $g, h \in (\mathbb{Z}/n\mathbb{Z})^{\times}$ with squarefree $n$, the pair $\{\pi_{\mathrm{DYN}}(g),\pi_{\mathrm{DYN}}(h)\}$ is sufficient iff $\langle g\rangle \cap \langle h\rangle = \{1\}$, equivalently $\gcd(\mathrm{ord}_{p_i}(g),\mathrm{ord}_{p_i}(h)) = 1$ at every prime $p_i \mid n$.

**Theorem 1.4 (Three mechanisms).** Sufficient $\{\pi_{\mathrm{DYN}}(g),\pi_{\mathrm{DYN}}(h)\}$ pairs arise via three mechanisms:
- (M1) focused on distinct primes;
- (M2) same-prime coprime orders, existing at $p_i$ iff $p_i - 1$ has $\geq 2$ distinct prime factors (smallest such primes: $7, 11, 13, 19, 23$);
- (M3) mixed (each of $g, h$ acts non-trivially at multiple primes).

A detailed worked example for $n = 10$ is given (§5), including the partition lattice $\pi_{\mathrm{SPEC}} \leq \pi_{\mathrm{UG}} \leq \pi_{\mathrm{CRT}_2}$ with $\pi_{\mathrm{CRT}_5}$ pairwise incompatible. The conjecture $\mathrm{MVJN}(\mathbb{Z}/n\mathbb{Z}) = 1$ for all squarefree $n \geq 6$ is stated and supported by explicit verification at $n \in \{6,10,14,15,21,22,26,30,33,34,35,38,39,42\}$.

I have verified each numerical claim by independent enumeration; all are correct. (See §5 below.)

---

## 2. Decision recommendation

**Minor revisions.**

This is the strongest paper in the J10/J11/J12 cluster from a *European Journal of Combinatorics* perspective. The combinatorial content is substantive:

1. Theorem 1.3 (orbit-pair classification) gives a clean, explicit, CRT-coordinate-by-coordinate criterion for two cyclic-action partitions to separate. This is well-motivated, well-stated, well-proved.
2. Theorem 1.4 (three mechanisms) is a structural result that distinguishes the "mod-$p$ obstruction" landscape into three regimes, with the $p_i - 1$ prime-factorization condition being a genuine number-theoretic-flavored combinatorial criterion.
3. Theorem 1.2 (non-CRT pairs on $\mathbb{Z}/30\mathbb{Z}$) is a concrete, verifiable result that establishes $\mathrm{MVJN}(\mathbb{Z}/30\mathbb{Z}) = 1$ and exhibits three different *mechanisms* for achieving this minimum.
4. The detailed $n = 10$ worked example (§5) is a model presentation.

The paper does have several issues that should be addressed before camera-ready, but none are fatal. The combinatorial substance is well-suited to *European Journal of Combinatorics*, and the result is, in my view, novel and interesting.

---

## 3. Major comments

### M1. The MVJN definition has an inconsistency.

The "minimum viable jump number" is defined two different ways in the paper:

- §1 (line 67): "the smallest number of orthogonal jumps in any sufficient family of partitions of $\mathbb{Z}/n\mathbb{Z}$."
- §6 (line 240): "For any family of *proper* partitions ($\pi \neq \pi_{\mathrm{disc}}$, $\pi \neq \pi_{\mathrm{triv}}$), at least one orthogonal jump must occur for the meet to reach $\pi_{\mathrm{disc}}$."

The §1 definition is a global minimum; the §6 lower bound interprets "jump" relative to a *family* (i.e., the family must contain at least one pair of incomparable partitions). This is the standard meaning, but the precise count of "jumps" needs to be defined.

For example: in the family $\{\pi_2, \pi_3, \pi_5\}$ on $\mathbb{Z}/30\mathbb{Z}$ (length 3, sufficient via Theorem D), how many "jumps" are there? Three pairs $\{\pi_2,\pi_3\}, \{\pi_2,\pi_5\}, \{\pi_3,\pi_5\}$ are all pairwise incomparable, so the answer could be:
- 3 (count of incomparable pairs), or
- 2 (length minus one, as in Theorem 1.1's $k - 1$), or
- some other notion.

§1.1 says "Two partitions are *incompatible* (an *orthogonal jump*) when neither refines the other." So an orthogonal jump is a *pair* of incomparable partitions. But then "number of orthogonal jumps in a family" should be the number of incomparable pairs, not $k - 1$.

Theorem 1.1 says the prime-factor family has "exactly $k - 1$ orthogonal jumps" — this matches the *transitions* in a sequential ordering of the family, but not the count of incomparable pairs (which would be $\binom{k}{2}$, all of them by Lemma 3.1).

**Recommended fix.** Define MVJN precisely. Two natural choices:

- $\mathrm{MVJN}_{\mathrm{trans}}$: minimum, over sufficient families $\mathcal F$ ordered as a chain $\pi_1, \pi_2, \ldots, \pi_m$, of the number of consecutive transitions $i \to i+1$ that are orthogonal jumps. (This gives $k - 1$ for the prime-factor family in Theorem 1.1.)
- $\mathrm{MVJN}_{\mathrm{pairs}}$: minimum, over sufficient families $\mathcal F$, of the number of unordered incomparable pairs. (This gives $\binom{k}{2}$ for the prime-factor family.)

The paper's results are clearer under $\mathrm{MVJN}_{\mathrm{trans}}$, and this is presumably the intended definition. State it precisely in §1.

Alternatively, since the paper's positive results all involve $2$-element families, define MVJN as: "the minimum number of orthogonal jumps in any sufficient family of size 2", which collapses the issue (every $2$-family has $0$ or $1$ jump).

### M2. Theorem 1.2 (the $\mathbb{Z}/30\mathbb{Z}$ result) needs a clearer "what's new" framing.

Family (c) $\{\pi_2,\pi_{15}\}$ is the CRT pair $\{\pi_{p_1}, \pi_{p_2 p_3}\}$ — i.e., it is the standard CRT decomposition for $30 = 2 \cdot 15$, treating $\pi_{15}$ as a single residue partition that encodes the joint mod-3 and mod-5 information. This is *not* a deep result — it is a restatement of the CRT, and the paper acknowledges this implicitly (line 153). The remark at line 158 makes the framing explicit:

> "Family (a) and family (c) both have a residue partition $\pi_{15}$ that encodes both the mod-3 and mod-5 CRT coordinates simultaneously..."

Similarly, family (a) uses $\pi_{\mathrm{SPEC}}$ to resolve mod-2 and $\pi_{15}$ to resolve mod-3, mod-5 jointly. This is also a CRT-flavored decomposition.

The genuinely surprising family is (b): $\{\pi_{\mathrm{DYN}}(7),\pi_{\mathrm{DYN}}(11)\}$. Here both partitions are orbit partitions, neither is a residue partition, and the mechanism is the coordinate-wise coprime-order condition (Theorem 1.3). This is the result that does not reduce to CRT in an obvious way and is the heart of the paper.

**Recommended fix.** Reframe §4 to highlight family (b) as the "novel" sufficient pair, with families (a) and (c) as "CRT-style" pairs that decompose differently. This sharpens the message and makes the connection to Theorem 1.3 (orbit-pair classification) more direct.

### M3. The relationship between Theorems 1.2(b) and 1.3 should be made explicit earlier.

Theorem 1.2(b) is a special case of Theorem 1.3 with $g = 7$, $h = 11$, $n = 30$. The paper's order of presentation is:
- §4: Theorem 1.2 (concrete claim with three families, including (b)).
- §5: Theorem 1.3 (general orbit-pair classification).

A reader encountering §4 first sees only the verification "compute the orbits, check no overlap" without the structural understanding that Theorem 1.3 provides. Reordering or cross-referencing would help.

**Recommended fix.** Either (i) move Theorem 1.3 earlier so that Theorem 1.2(b) is presented as its corollary, or (ii) at the start of §4(b)'s proof, reference Theorem 1.3 explicitly: "By Theorem 1.3 (proved below), it suffices to verify the coordinate-wise coprime-order condition...".

### M4. The "three mechanisms" classification (Theorem 1.4) is interesting but underexplored.

Theorem 1.4 asserts:
- (M1) "focused on distinct primes": $g$ acts non-trivially only at $p_i$, $h$ only at $p_{\ell}$, $i \neq \ell$.
- (M2) "same-prime coprime orders": $g, h$ both act only at $p_i$, with coprime orders.
- (M3) "mixed": each acts at multiple primes.

The paper proves existence of each mechanism. But the classification raises natural questions:

- Is every sufficient orbit-pair *exactly* one of (M1), (M2), (M3)? Or do these mechanisms overlap?
- For (M3), what is the smallest $n$ where (M3) but not (M1) or (M2) is achievable? The paper gives $n = 42$.
- Is there a *fourth* mechanism, perhaps involving cyclic subgroups generated by elements of mixed type?

**Recommended fix.** Add a remark or proposition clarifying:
- The three mechanisms are *not* mutually exclusive (e.g., $g, h$ both focused on different primes but with extra trivial action at other primes counts as (M1)), but they are exhaustive (every sufficient orbit-pair fits at least one).
- Or, conversely, they are the three "pure" types and a general sufficient pair may be a "hybrid".

State the classification more precisely. As written, the theorem says "the following three mechanisms produce sufficient pairs", which is an existence statement, not a classification.

### M5. The conjecture $\mathrm{MVJN}(\mathbb{Z}/n\mathbb{Z}) = 1$ is interesting but needs more support.

Conjecture 6.2: $\mathrm{MVJN}(\mathbb{Z}/n\mathbb{Z}) = 1$ for every squarefree $n \geq 6$.

The paper supports this by explicit verification at 14 values of $n$ (line 247). But the claim "we have verified the conjecture for $n = 6, 10, 14, ...$" is not made precise (which sufficient pair was found at each $n$? Was the verification by enumeration of all pairs, or by exhibition of one pair?).

For each verified $n$, the paper presumably constructed a sufficient $2$-partition family. If so, document the construction systematically. Specifically:

- For $n = pq$ (two primes): take $\{\pi_p, \pi_q\}$, which is sufficient by CRT. This is a 1-jump family.
- For $n = pqr$ (three primes): take $\{\pi_p, \pi_{qr}\}$ if $\pi_{qr}$ resolves mod-$q$ and mod-$r$. By Theorem D this is sufficient with 1 jump.
- For $n = p_1 p_2 \cdots p_k$ ($k \geq 2$): take $\{\pi_{p_1}, \pi_{p_2 \cdots p_k}\}$. By Theorem D, $\mathrm{lcm}(p_1, p_2 \cdots p_k) = n$, sufficient. Always 1 jump (Lemma 3.1 implies pairwise incomparability).

This argument actually *proves* the conjecture for all squarefree $n \geq 6$ (and $n = pq$ for $p < q$ primes with $pq \geq 6$, e.g., $n = 6, 10, 14, 15, \ldots$). What am I missing?

Let me re-read the conjecture statement: "$\mathrm{MVJN}(\mathbb{Z}/n\mathbb{Z}) = 1$" — this is the *minimum* over sufficient families. The minimum is at most 1 (by the construction $\{\pi_{p_1}, \pi_{n/p_1}\}$). It is at least 1 (by Theorem 6.1, the refinement-trap lower bound). So the minimum is exactly 1, for every squarefree $n$ with $k \geq 2$.

If MVJN is the count-of-jumps in a $2$-partition family (which is at most 1), the conjecture is trivially true.

The conjecture only makes sense if MVJN is defined more carefully, perhaps:
- MVJN = minimum, over all sufficient families *of any size*, of the count of incomparable pairs.

Under this definition, the family $\{\pi_{p_1}, \pi_{n/p_1}\}$ has size 2 and 1 incomparable pair, achieving MVJN $\leq 1$. So this gives MVJN $\leq 1$. Combined with MVJN $\geq 1$ (Theorem 6.1 generalized to all families), this proves MVJN $= 1$.

So the conjecture is *not* open — it follows from the family $\{\pi_{p_1}, \pi_{n/p_1}\}$ being sufficient (Theorem D) and the refinement-trap lower bound (Theorem 6.1).

**Recommended fix.** Either (i) prove the conjecture (it appears to follow from the existing theorems), or (ii) state more carefully what MVJN means and why the construction $\{\pi_{p_1}, \pi_{n/p_1}\}$ does *not* directly establish MVJN $= 1$. Currently the conjecture as stated appears to be a theorem.

### M6. The companion-paper dependence should be made standalone.

The proofs of Theorems 1.3 and 1.4 begin by invoking "the Universal Orthogonality Principle" of the J10 companion paper (line 164). As I noted in the J11 referee report, the UOP is a partition-lattice tautology and the actual proofs in this paper (Theorem 1.3 at line 164–171) are self-contained CRT arguments. The UOP appeal is a stylistic gesture and could be removed.

Moreover, the companion citation is to a paper currently in submission to JNT. EJC will (and should) require that any cited result either:
- be from a *published* paper (DOI, arXiv ID, MathSciNet), or
- be proved inline in the present paper, or
- be cited as "in preparation" with the understanding that the citation may need updating before publication.

The cleanest approach: prove Theorem 1.3 inline (the proof is short — see line 164–171, which is essentially complete), removing the dependence on J10. Similarly for Theorem 1.4.

**Recommended fix.** Make J12 standalone. Cite J10 only for context, not for load-bearing results. The proofs in J12 are short enough to stand on their own.

### M7. The "geometric interpretation" remark (line 230) is out of place.

§5.4 ends with:
> "Two independent CRT directions cannot be embedded in a single $S^1$ continuously (since $\pi_1(S^1) = \mathbb{Z}$ admits no surjection to $\mathbb{Z}^2$). The natural ambient embedding for the joint $(\pi_{\mathrm{CRT}_2}, \pi_{\mathrm{CRT}_5})$ data is the torus $T^2 = S^1 \times S^1$. The companion paper of Sanders–Gish (*Flatness Theorem*) gives a structural argument that the minimum-curvature ambient for the four simultaneous structures on $\mathbb{Z}/10\mathbb{Z}$ is a torus with aspect ratio $5/7$."

This remark is jarring in an EJC paper. The fundamental-group argument is correct but not motivated by the partition-lattice content of the paper, and the reference to "$5/7$ torus aspect ratio" is opaque without the *Flatness Theorem* paper in hand. EJC readers will not have that paper.

**Recommended fix.** Either (i) remove the remark, or (ii) replace with a one-line note: "An external observation: the joint data of the two CRT decompositions has natural ambient geometry $T^2 = S^1 \times S^1$." Drop the "$5/7$" reference unless it can be motivated within the present paper.

### M8. Theorem 1.4's "smallest primes" list (line 97) is slightly underspecified.

The statement: "Mechanism (M2) exists at $p_i$ iff $p_i - 1$ has at least two distinct prime factors. The smallest such primes are $7, 11, 13, 19, 23$."

I verified: $p = 7, 11, 13, 19, 23$ all have $p - 1$ with $\geq 2$ distinct prime factors. The list omits $p = 17$ ($16 = 2^4$, only one distinct prime factor — correctly omitted). The list also omits $p = 29$? Let me check: $29 - 1 = 28 = 2^2 \cdot 7$, two distinct primes. So 29 should be in the list. The list says "the smallest such primes are $7, 11, 13, 19, 23$" — implicitly the first five. State this explicitly.

**Recommended fix.** Reword as "The smallest five such primes are $7, 11, 13, 19, 23$" or "The smallest such primes start $7, 11, 13, 19, 23, \ldots$".

---

## 4. Minor comments

### m1. (Title line 34–35) "Coordinate Coverage on $\mathbb{Z}/10\mathbb{Z}$: Non-CRT Sufficient Pairs and the Minimum Viable Jump Number" — clear. Note that the paper's content is *not* mainly about $\mathbb{Z}/10\mathbb{Z}$ — that's just the worked example in §5. The main results (Theorems 1.1–1.4) are about general squarefree $n$. Consider retitling: "Non-CRT Sufficient Pairs and the Minimum Viable Jump Number on Squarefree $\mathbb{Z}/n\mathbb{Z}$" with $n = 10$ as a worked example.

### m2. (Author block lines 37–42) Same duplicated-author block as J10/J11. Remove.

### m3. (Abstract, lines 49–50) The abstract is dense and lists all four theorems plus the conjecture. Consider tightening to: "We prove a coordinate-wise coprime-order classification of orbit pairs (Theorem 1.3), exhibit three structural mechanisms for sufficient orbit pairs (Theorem 1.4), and establish $\mathrm{MVJN}(\mathbb{Z}/30\mathbb{Z}) = 1$ via three explicit families (Theorem 1.2). The CRT prime-factor family is shown to be rigid (Theorem 1.1), and we conjecture $\mathrm{MVJN}(\mathbb{Z}/n\mathbb{Z}) = 1$ for all squarefree $n \geq 6$." (Cuts about half the abstract length without losing content.)

### m4. (§1.1 line 60) "Two partitions are *incompatible* (an *orthogonal jump*) when neither refines the other." — the terminology *incompatible* and *orthogonal jump* are introduced as synonyms; pick one and use it consistently. (See M3 of the J10 report for concerns about "orthogonal".)

### m5. (Lemma 3.1 proof, line 113) "Suppose $\pi_{p_i} \leq \pi_{p_j}$..." — should be "Suppose $\pi_{p_i} \leq \pi_{p_j}$ for contradiction." Add the contradiction signal.

### m6. (Lemma 3.1 proof, line 113) "Each $\pi_{p_i}$-block has size $n/p_i$..." — correct. Note: the proof shows the block contains $\geq p_j$ elements with distinct mod-$p_j$ residues; the right framing is: since $\gcd(p_i,p_j) = 1$ and the block's elements form an arithmetic progression with common difference $p_i$, the block surjects to $\mathbb{Z}/p_j\mathbb{Z}$ (and has at least one element in every $\pi_{p_j}$-block).

### m7. (Theorem 3.2 / "Full meet = discrete") The proof is correct. The statement could be sharper: $\bigwedge_{i=1}^k \pi_{p_i} = \pi_{\mathrm{disc}}$, *and* this is the minimum number of factor partitions needed. State as "exactly $k$ factor partitions are needed".

### m8. (§4(a) proof line 137) "From these, $2a \equiv 15 \pmod{30}$, which has no solution (gcd $2 \nmid 15$)." — the gcd argument: $\gcd(2,30) = 2$, and $2 \mid 15$ is false, so $2a \equiv 15 \pmod{30}$ has no solution. The notation "gcd $2 \nmid 15$" is informal; rewrite as "since $\gcd(2,30) = 2$ does not divide $15$, no solution exists."

### m9. (§4(b) proof line 144–148) The orders are correctly computed. Check $7^2 = 49 \equiv 19 \pmod{30}$, $7^3 = 7 \cdot 19 = 133 \equiv 13 \pmod{30}$, $7^4 = 7 \cdot 13 = 91 \equiv 1 \pmod{30}$. So $\mathrm{ord}_{30}(7) = 4$. Verify: $\mathrm{ord}_2(7) = \mathrm{ord}_2(1) = 1$ ✓, $\mathrm{ord}_3(7) = \mathrm{ord}_3(1) = 1$ ✓, $\mathrm{ord}_5(7) = \mathrm{ord}_5(2) = 4$ ✓ (since $2,4,3,1$). The orbit $\{1,7,19,13\}$ has size 4. ✓

For 11: $11^2 = 121 \equiv 1 \pmod{30}$, so $\mathrm{ord}_{30}(11) = 2$. Verify: $\mathrm{ord}_2(11) = \mathrm{ord}_2(1) = 1$ ✓, $\mathrm{ord}_3(11) = \mathrm{ord}_3(2) = 2$ ✓, $\mathrm{ord}_5(11) = \mathrm{ord}_5(1) = 1$ ✓. Orbit $\{1,11\}$ has size 2. ✓

Coordinate-wise gcds: $(1,1), (1,2), (4,1)$; gcds $(1,1,1)$, all 1. Sufficient by Theorem 1.3. ✓

### m10. (§5 line 192) "$\pi_{\mathrm{DYN}} = \pi_{\mathrm{UG}}$" — the equality is for the specific $g = 3$. State $\pi_{\mathrm{DYN}}(3) = \pi_{\mathrm{UG}}$. (The paper does state this in Lemma 5.1.)

### m11. (§5 Lemma 5.1 proof, line 203) "$1 \to 3 \to 9 \to 7 \to 1$" — verify: $T_3(1) = 3, T_3(3) = 9, T_3(9) = 27 \equiv 7 \pmod{10}, T_3(7) = 21 \equiv 1 \pmod{10}$. ✓ "$2 \to 6 \to 8 \to 4 \to 2$" — verify: $T_3(2) = 6, T_3(6) = 18 \equiv 8 \pmod{10}, T_3(8) = 24 \equiv 4 \pmod{10}, T_3(4) = 12 \equiv 2 \pmod{10}$. ✓

### m12. (§5 Proposition 5.2(b)) "$\pi_{\mathrm{CRT}_5}$ is incompatible with each of $\pi_{\mathrm{CRT}_2}$, $\pi_{\mathrm{UG}}$, and $\pi_{\mathrm{SPEC}}$." — verify $\pi_{\mathrm{CRT}_5}$ vs. $\pi_{\mathrm{SPEC}}$: $\pi_{\mathrm{CRT}_5}$-block $\{0,5\}$ has $0$ in $\pi_{\mathrm{SPEC}}$-singleton $\{0\}$, $5$ in $\pi_{\mathrm{SPEC}}$-singleton $\{5\}$ — different blocks. $\pi_{\mathrm{SPEC}}$-block $\{1,9\}$ has $1 \bmod 5 = 1$, $9 \bmod 5 = 4$ — different $\pi_{\mathrm{CRT}_5}$-blocks. So neither refines the other. Verified.

### m13. (§6 Theorem 6.1 proof, line 240) "A family of pairwise comparable partitions $\pi_1 \leq \pi_2 \leq \cdots \leq \pi_m$ has meet equal to its finest element $\pi_1$." — correct. The conclusion is that the family must contain $\pi_{\mathrm{disc}}$, hence cannot consist only of "proper" partitions.

This is essentially the refinement trap (J10's Theorem 7.1). State the connection.

### m14. (§7 open questions, items (a)–(d)) Items (a) and (b) are the substantive open problems; (c) and (d) are extensions. Reorder if (a) and (b) are the priority questions.

### m15. (References) Bibliography is appropriately tight (8 entries, all standard textbooks plus the J10 and Flatness Theorem companions). The Flatness Theorem citation (line 300) is not used elsewhere in the paper except in the §5.4 geometric remark. If the geometric remark is removed (M7), drop the citation.

### m16. (Notation) The paper uses $\pi_{\DYN}$, $\pi_{\SPEC}$, $\pi_{\UG}$, $\pi_{\CRT_p}$ — clear macros are defined. The use of $\pi_{\CRT_p}$ for what is in fact $\pi_p$ (residue mod $p$) is slightly unusual; consider just $\pi_p$ throughout.

### m17. (§4 family (b), the orbit table) Checking: $\pi_{\mathrm{DYN}}(7)$ orbits on $\mathbb{Z}/30\mathbb{Z}$ — $\{0\}, \{1,7,13,19\}, \{2,8,14,26\}$? Let me verify $\{2,8,14,26\}$: $T_7(2) = 14, T_7(14) = 98 \equiv 8 \pmod{30}, T_7(8) = 56 \equiv 26 \pmod{30}, T_7(26) = 182 \equiv 2 \pmod{30}$. Orbit $\{2, 14, 8, 26\}$ ✓. The orbit $\{3,9,21,27\}$: $T_7(3) = 21, T_7(21) = 147 \equiv 27, T_7(27) = 189 \equiv 9, T_7(9) = 63 \equiv 3$. Orbit $\{3,21,27,9\}$ ✓. All orbits as listed are correct.

---

## 5. Specific verifications performed

I have independently verified:

1. $\pi_{\mathrm{DYN}}(7)$ on $\mathbb{Z}/30\mathbb{Z}$: orbits $\{0\}, \{1,7,13,19\}, \{2,8,14,26\}, \{3,9,21,27\}, \{4,16,22,28\}, \{5\}, \{6,12,18,24\}, \{10\}, \{11,17,23,29\}, \{15\}, \{20\}, \{25\}$. All confirmed.
2. $\pi_{\mathrm{DYN}}(11)$ on $\mathbb{Z}/30\mathbb{Z}$: orbits $\{0\}, \{1,11\}, \{2,22\}, \{3\}, \{4,14\}, \{5,25\}, \{6\}, \{7,17\}, \{8,28\}, \{9\}, \{10,20\}, \{12\}, \{13,23\}, \{15\}, \{16,26\}, \{18\}, \{19,29\}, \{21\}, \{24\}, \{27\}$. All confirmed.
3. $U(\pi_{\mathrm{DYN}}(7)) \cap U(\pi_{\mathrm{DYN}}(11)) = \emptyset$: verified by direct enumeration. Sufficient.
4. $\mathrm{ord}_2(7) = \mathrm{ord}_3(7) = 1, \mathrm{ord}_5(7) = 4$; $\mathrm{ord}_2(11) = \mathrm{ord}_5(11) = 1, \mathrm{ord}_3(11) = 2$. Coordinate-wise gcds $(1,1,1)$. Confirmed.
5. $U(\pi_{\mathrm{SPEC}}) \cap U(\pi_{15}) = \emptyset$ on $\mathbb{Z}/30\mathbb{Z}$: confirmed.
6. $U(\pi_2) \cap U(\pi_{15}) = \emptyset$ on $\mathbb{Z}/30\mathbb{Z}$: confirmed.
7. $\pi_{\mathrm{DYN}}(3)$ on $\mathbb{Z}/10\mathbb{Z}$: orbits $\{0\}, \{1,3,7,9\}, \{2,4,6,8\}, \{5\}$. Confirmed equals $\pi_{\mathrm{UG}}$.
8. $\pi_{\mathrm{SPEC}}$ on $\mathbb{Z}/10\mathbb{Z}$: $\{0\}, \{1,9\}, \{2,8\}, \{3,7\}, \{4,6\}, \{5\}$. Confirmed.
9. (M3) example: $n = 42, g = 11, h = 13$. $\mathrm{ord}_2(11) = \mathrm{ord}_2(13) = 1$; $\mathrm{ord}_3(11) = 2, \mathrm{ord}_3(13) = 1$; $\mathrm{ord}_7(11) = 3, \mathrm{ord}_7(13) = 2$. Coordinate-wise gcds $(1,1,1)$. Direct enumeration: $U(\pi_{\mathrm{DYN}}(11)) \cap U(\pi_{\mathrm{DYN}}(13)) = \emptyset$ on $\mathbb{Z}/42\mathbb{Z}$. Confirmed.
10. Smallest primes $p$ with $p - 1$ having $\geq 2$ distinct prime factors: $7 (6 = 2 \cdot 3), 11 (10 = 2 \cdot 5), 13 (12 = 2^2 \cdot 3), 19 (18 = 2 \cdot 3^2), 23 (22 = 2 \cdot 11), 29 (28 = 2^2 \cdot 7), \ldots$ — the paper lists 5; 29 also qualifies and is omitted. Either include 29 or rephrase as "first five".

---

## 6. Question to the authors

### Q1. Is the conjecture MVJN($\mathbb{Z}/n\mathbb{Z}$) = 1 actually open, or does it follow from existing results?

As I noted in M5, the family $\{\pi_{p_1}, \pi_{n/p_1}\}$ is sufficient by Theorem D ($\mathrm{lcm} = n$) and contributes 1 jump (incomparable by Lemma 3.1 generalized). Combined with the refinement-trap lower bound, this gives MVJN $= 1$ for all squarefree $n$ with $k \geq 2$. Where is the open content?

If the conjecture is meant in a different sense (e.g., minimum over families of *unbounded* size, where adding more partitions could reduce the jump count to 0), please clarify. Otherwise, the conjecture is a theorem.

### Q2. Does Theorem 1.4 give an exhaustive classification?

Are mechanisms (M1), (M2), (M3) mutually exclusive? Are there other mechanisms? Specifically: a sufficient orbit-pair $\{\pi_{\mathrm{DYN}}(g),\pi_{\mathrm{DYN}}(h)\}$ where one of $g, h$ acts at a single prime and the other at multiple — is this (M1) or (M3) or a hybrid?

A clean classification statement would be: every sufficient orbit-pair is uniquely characterized by the "support patterns" $(\mathrm{supp}_g, \mathrm{supp}_h)$ where $\mathrm{supp}_g = \{p_i : g_i \neq 1\}$. The conditions for sufficiency depend only on these supports and the orders at each prime in the union.

### Q3. What is the relationship between Theorem 1.3 (orbit-pair) and the established theory of orthogonal Latin squares?

Two cyclic orbit partitions $\pi_{\mathrm{DYN}}(g), \pi_{\mathrm{DYN}}(h)$ on $\mathbb{Z}/n\mathbb{Z}$ being sufficient is closely related to the existence of pairs of orthogonal Latin squares of side $n$ (where $n = pq$, etc.). The cyclic case is well-studied (Bose–Shrikhande–Parker, Mullin–Stinson, etc.). Is Theorem 1.3 a known result in disguise?

Specifically: a Latin square based on $g$-action (each row $i$ has entries $g^j i$ for $j = 0, \ldots, n-1$) — when are two such squares orthogonal? The condition is closely related to coprime-order at each prime. This connection should be discussed.

### Q4. What is the smallest $n$ for which mechanism (M3) is the only mechanism available?

For $n = 30$, all three mechanisms are available (the three families in Theorem 1.2). For $n = 42$ (the (M3) example), is (M1) also available? Let's see: $42 = 2 \cdot 3 \cdot 7$. (M1) needs $g$ acting only at $p$, $h$ only at $q$, distinct primes. $g$ generator of $(\Z/3)^\times$ extended trivially: $g$ has $g_3$ a generator, $g_2 = g_7 = 1$. The smallest such $g$ in $(\Z/42\Z)^\times$ — solve $g \equiv 2 \pmod 3, g \equiv 1 \pmod 2, g \equiv 1 \pmod 7$. By CRT, $g = 29$. So (M1) on $\Z/42\Z$ uses $g = 29, h = $ generator of $(\Z/7)^\times$ extended trivially: $h \equiv 3 \pmod 7, h \equiv 1 \pmod 2, h \equiv 1 \pmod 3$ — by CRT, $h = 31$. Check: $\{\pi_{\mathrm{DYN}}(29), \pi_{\mathrm{DYN}}(31)\}$ would be sufficient via (M1).

So $n = 42$ admits (M1). What is the smallest $n$ admitting (M3) but not (M1) or (M2)? This is a natural follow-up question.

---

## 7. Originality and significance for EJC

### Originality.

The paper makes three original contributions:

1. The orbit-pair classification (Theorem 1.3): a clean, explicit, CRT-coordinate criterion for two cyclic-action partitions to separate. The criterion "coordinate-wise gcd of orders is 1 at every prime" is a nice combinatorial statement. I am not aware of this exact result in the prior literature on partition lattices of $\mathbb{Z}/n\mathbb{Z}$, though it is closely related to the theory of orthogonal cyclic Latin squares (Q3).

2. The three-mechanism classification (Theorem 1.4): the distinction between focused, same-prime-coprime, and mixed mechanisms is a useful structural insight. The "$p_i - 1$ has $\geq 2$ distinct prime factors" condition is a concrete number-theoretic constraint that emerges from the combinatorics.

3. The non-CRT sufficient pairs on $\mathbb{Z}/30\mathbb{Z}$ (Theorem 1.2): three explicit families with one orthogonal jump, demonstrating that the prime-factor family is *not* the minimum-jump sufficient family.

### Significance for EJC.

EJC publishes work on:
- Combinatorial structures (graphs, designs, codes, polytopes).
- Algebraic combinatorics (group actions, posets, matroids).
- Combinatorial number theory.

The paper fits well in the second and third categories. The partition-lattice framework on $\mathbb{Z}/n\mathbb{Z}$ with cyclic actions is a natural EJC topic. The level of generality (squarefree $n$, $k \geq 2$ primes, two natural classes of partitions) is appropriate.

The bar at EJC is met: the result is novel, the proof is clean, the worked examples are concrete, and the open questions are well-posed.

---

## 8. Reproducibility

All numerical claims are verifiable by hand or by trivial computer enumeration. I have run independent enumerations on $\mathbb{Z}/10\mathbb{Z}, \mathbb{Z}/30\mathbb{Z}, \mathbb{Z}/42\mathbb{Z}$ to confirm:
- All orbits in §4 and §5 are correct.
- All sufficiency claims hold by direct intersection-empty check.
- All order computations are correct.

No code is supplied with the paper, but none is needed; the verifications are within range of a calculator or 5-line Python script.

---

## 9. Final remarks

This is the strongest paper in the J10/J11/J12 cluster. The combinatorial content is substantive, the worked examples are concrete, the structural classifications are clean, and the venue (EJC) is appropriate. The mathematics is correct.

The recommended decision is **Minor revisions**, with the expectation that:

1. MVJN is precisely defined (M1).
2. The conjecture in §6 is either proved (since it appears to follow from existing results) or its open content is clarified (M5).
3. Theorem 1.2 is reframed to highlight family (b) as the genuinely novel sufficient pair (M2).
4. The proofs of Theorems 1.3 and 1.4 are made standalone, removing the J10 dependency (M6).
5. The geometric remark in §5.4 is removed or trimmed (M7).
6. The "smallest primes" list is corrected to include 29 or rephrased (M8).
7. Minor exposition fixes per §4 above.
8. The connection to orthogonal Latin squares is discussed (Q3).

After these revisions, the paper would be a clean and substantial contribution to EJC.

---

**Estimated revision effort:** 10–18 person-hours. Most of the work is consolidating proofs to standalone, tightening §4 framing, and discussing the orthogonal-Latin-squares connection. The mathematics is settled.

**Reviewer's confidence:** High. I have read the paper end-to-end, verified all computational claims by independent enumeration, and re-derived the proofs.
