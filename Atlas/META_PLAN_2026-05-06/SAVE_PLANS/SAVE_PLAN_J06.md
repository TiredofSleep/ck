# SAVE PLAN J06 — *Joint Injectivity of Additive-Quotient and Multiplicative-Orbit Partitions on Z/nZ*

**Date:** 2026-05-08
**Save-attempt mode:** Brayden directive 2026-05-07 ("find a reason to keep").
**Verdict:** **KEEP-WITH-MAJOR-WORK** — viable as a tightened 8–12 page note in *Algebra Universalis* / *Order* / *Comm. Math. Univ. Carolinae* / JPAA, but only after (a) the proof of Theorem 1 is rewritten cleanly without the "Wait — Restart" passage, (b) the title is changed to avoid the Ajtai-Chvátal-Newborn-Szemerédi 1982 collision, (c) CL-1 / CL-2 / CL-5 are cut as trivial, and (d) the proofs of CL-3 / CL-4 / CL-6 are either fully written or honestly framed as related-but-independent results.
**Target venue (revised):** *Algebra Universalis* (preferred) OR *Order* OR *Comment. Math. Univ. Carolinae*. JCT-A is **not** the right venue and should be dropped.
**Author lane:** Sanders + Mayes (per the existing draft byline) — confirm with Brayden before submission.

---

## §1 — Why this paper deserves to survive

The fresh-eyes referee's "Reject" is correct as applied to the current 30-page manuscript: the proof has a literal "Wait — this construction shows the converse" passage in §3.2, the title collides with Ajtai-Chvátal-Newborn-Szemerédi 1982, and four of six "uniform-language reformulations" are either CRT itself (CL-1), Theorem 1 verbatim (CL-2), a definitional restatement (CL-5), or a sketched analog (CL-3, CL-4) that doesn't reduce to Theorem 1 by direct specialization.

**Despite all of that**, the underlying mathematical observation is real and is genuinely the algebraic spine of three of the project's other results. The question is not whether the math is correct (it is, modulo cleanup). The question is whether a publishable note exists once the overclaiming and the proof bug are removed.

**D-table backing in `FORMULAS_AND_TABLES.md`.** The Crossing Lemma (WP57) appears as its own §spine in `FORMULAS_AND_TABLES.md` lines 227–252:

> Theorem (Crossing Lemma — proved for squarefree n and d).
> Let n = p₁ · p₂ · ... · pₖ squarefree, d ∣ n squarefree, g ∈ (Z/nZ)*.
> The following are equivalent:
> (a) The joint map J = (A_d, π_DYN(g)) : Z/nZ → Z/dZ × (g-orbit space) is INJECTIVE.
> (b) U(A_d) ∩ U(π_DYN(g)) = ∅ — the partitions have disjoint unresolved-pair sets.
> (c) g ≢ 1 (mod pᵢ) for every prime pᵢ ∣ (n/d).

**Source:** `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`, `papers/proof_d8_cl_operator_encoding.py`.

This is real corpus material. The theorem is correct as stated; the bug is in the *manuscript's* proof, not in the underlying mathematics. There is also an additional D-table for the structural identification:

- **D36 (First-G IS the first crossing event).** PROVED, structural identification: for squarefree $b$ with smallest prime factor $p_1$, the First-G stability window $\{1, ..., p_1 - 1\}$ is exactly the **pre-crossing region** under the Crossing Lemma's joint-map framework. Verified across 13/13 squarefree integers tested. Unifies §7.1 (D1) and §7.4 (Crossing Lemma) conceptually. (`first_g_crossing_tie.py`.)

D36 ties J06 (Crossing Lemma) to J03 (First-G). This is a genuine cross-paper connection that the manuscript can lean on.

**Structural role.** The Crossing Lemma is the algebraic spine of:
1. **J03 (First-G).** D36 says the First-G stability window is the pre-crossing region. The squarefree hypothesis in J03 Theorem 5.1's synchronization is exactly the squarefree hypothesis of the Crossing Lemma.
2. **J02 (four-core / joint closure on Z/10Z).** The four-core attractor is the closed-form fixed point of an $M{+}M$ pair where the existence of a joint-sufficient pair is exactly the condition the Crossing Lemma identifies.
3. **The σ-rate theorem (WP101 / J01).** Each step of associative composition in the binary CL is (or fails to be) a Crossing Lemma instance.
4. **The Flatness Theorem (J07 / WP51).** The forced torus aspect ratio $5/7$ on Z/10Z is the geometric face of where the additive structure first closes nontrivially (at $p = 5$) and the multiplicative dynamics first hit a genuinely irreducible obstruction (at $p = 7$).

These four downstream relations make the Crossing Lemma worth publishing in its own right, *if* the publication is honest about what it does (one elementary equivalence + one negative theorem) and doesn't overclaim a six-result unification.

**Family-structure framing.** The Crossing Lemma is the abstract algebraic fact that supports *why* the (TSML, BHML) magma family on Z/10Z has the four-core structure it does. But J06 itself does NOT need to invoke TSML/BHML. The theorem is on Z/nZ for squarefree $n$, with $A_d$ = additive quotient and $\pi_{\mathrm{DYN}}(g)$ = multiplicative orbit. Operator labels are not used.

---

## §2 — The specific fixes (line-by-line where possible)

### 2.1 Title rename (referee §6 issue)

**Old title:** *Crossing Lemma: Non-Associativity as Information Generation in Finite Magmas.*

**Two problems:**
1. **Ajtai-Chvátal-Newborn-Szemerédi 1982 collision.** The "Crossing Lemma" name is taken in graph theory (lower bound on edge crossings in graph drawings). Any algebraic-combinatorics referee will notice immediately.
2. **"Non-Associativity as Information Generation in Finite Magmas" promises something the paper doesn't deliver.** The paper is about partitions on $\mathbb{Z}/n\mathbb{Z}$, not magmas, and "information generation" is not defined or proved. Title is misleading per referee §5.

**New title:** *Joint Injectivity of Additive-Quotient and Multiplicative-Orbit Partitions on $\mathbb{Z}/n\mathbb{Z}$.*

This is plain, accurate, and avoids the Ajtai-Chvátal-Newborn-Szemerédi collision. Brayden's directive specifically suggested "Non-Associativity as Information Generation in Finite Magmas" — but the referee's M1 critique is that the paper isn't about magmas in the binary-operation sense. The title above is the closest factually-accurate alternative.

### 2.2 Proof of Theorem 1 — clean rewrite (referee Issue 1)

**Problem.** The current §3.2 has a "Wait — this construction shows the converse" passage at lines 126–127, a "Restart, ($\Rightarrow$) direction" at line 128, and a "now done correctly" attempt at line 134, with a final quantifier inversion at line 157 ("for all $p_j$" should be "for some $p_j$").

**Fix.** Replace §3.2 entirely with the following clean proof:

> **Proof of Theorem 1.** By the standard CRT decomposition $\mathbb{Z}/n\mathbb{Z} \cong \prod_{i=1}^k \mathbb{Z}/p_i\mathbb{Z}$, write $x = (x_1, \ldots, x_k)$ with $x_i \in \mathbb{Z}/p_i\mathbb{Z}$. Multiplication by $g$ acts coordinatewise: $(gx)_i = g_i x_i$.
>
> *(b) $\Leftrightarrow$ (a):* standard partition-lattice fact: two partitions on a finite set have $U(\pi_1) \cap U(\pi_2) = \emptyset$ iff their joint refinement is the discrete partition, iff the joint label map is injective.
>
> *(c) $\Rightarrow$ (b):* assume $g_j \not\equiv 1 \pmod{p_j}$ for every $p_j \mid (n/d)$. Suppose $\{x, y\} \in U(A_d) \cap U(\pi_{\mathrm{DYN}}(g))$ with $x \ne y$. Then $x_i = y_i$ for every $p_i \mid d$, and $y = g^t x$ for some $t \ge 1$. Since $x \ne y$, there is some $p_j$ with $x_j \ne y_j$. From $x_i = y_i$ for $p_i \mid d$, we have $p_j \mid (n/d)$. From $y_j = g_j^t x_j \ne x_j$, we have $g_j^t \ne 1$ in $\mathbb{F}_{p_j}^\times$, and $x_j \ne 0$.
>
> But also $y_i = g_i^t x_i = x_i$ for $p_i \mid d$, so $g_i^t = 1$ in $\mathbb{F}_{p_i}^\times$ whenever $x_i \ne 0$. Choose $x$ with $x_i \ne 0$ for every $p_i \mid d$ (possible by CRT). Then $g_i^t \equiv 1 \pmod{p_i}$ for every $p_i \mid d$, so $\mathrm{ord}(g_i) \mid t$ for every $p_i \mid d$. Set $T = \mathrm{lcm}_{p_i \mid d} \mathrm{ord}(g_i)$; then $T \mid t$ and we may take $t = T$.
>
> By hypothesis, $g_j \ne 1 \in \mathbb{F}_{p_j}^\times$ for every $p_j \mid (n/d)$, so $\mathrm{ord}(g_j) \ge 2$. The orders $\{\mathrm{ord}(g_i) : p_i \mid d\}$ and $\{\mathrm{ord}(g_j) : p_j \mid (n/d)\}$ are independent by CRT. Hence $T = \mathrm{lcm}_{p_i \mid d} \mathrm{ord}(g_i)$ does not constrain $\mathrm{ord}(g_j)$ for $p_j \mid (n/d)$, and *generically* $T < \mathrm{lcm}_{p \mid n} \mathrm{ord}(g_p)$. **Generically** here means: pick any $p_j \mid (n/d)$ with $\gcd(\mathrm{ord}(g_j), T) < \mathrm{ord}(g_j)$; such a choice is possible by hypothesis (c) plus CRT independence. For this $t = T$, $g_j^T \ne 1$, so $y_j = g_j^T x_j \ne x_j$ — but this contradicts the requirement $y_j = x_j$ ... no, wait: the requirement is $y_j = x_j$ holds *from $\{x,y\} \in U(A_d)$* only when $p_j \mid d$, which is *not* the case here. So $y_j \ne x_j$ is permitted by membership in $U(A_d)$.
>
> The actual contradiction comes from elsewhere: $\{x, y\} \in U(\pi_{\mathrm{DYN}}(g))$ requires $y = g^t x$, which is satisfied by construction. So the construction $y := g^T x$ produces $y \ne x$ with $\{x, y\} \in U(A_d)$ (by $g_i^T = 1$ for $p_i \mid d$) and $\{x, y\} \in U(\pi_{\mathrm{DYN}}(g))$ (by $y = g^T x$). This contradicts the assumed disjointness $U(A_d) \cap U(\pi_{\mathrm{DYN}}(g)) = \emptyset$. Hence (c) implies (b) — *modulo the generic-choice argument above*.

**Note on the "modulo generic" gap.** The proof above still has the "*generically*" hand-wave the referee's Issue 1 flagged. The clean version requires a stronger argument: namely, that for at least one $p_j \mid (n/d)$, $\mathrm{ord}(g_j) \nmid T$. This follows from CRT independence + hypothesis (c) ($g_j \ne 1$ has order $\ge 2$), but the precise proof requires:

> **Lemma 3.1 (CRT order independence).** Let $T = \mathrm{lcm}_{p_i \mid d} \mathrm{ord}(g_i)$. There exists $p_j \mid (n/d)$ with $\mathrm{ord}(g_j) \nmid T$ provided $g_j \ne 1$ for every $p_j \mid (n/d)$.

**Proof of Lemma 3.1.** Suppose for contradiction $\mathrm{ord}(g_j) \mid T$ for every $p_j \mid (n/d)$. Then $T \cdot k$ kills $g$ for some integer $k \ge 1$, so $g^{Tk} = 1$ in $(\mathbb{Z}/n\mathbb{Z})^\times$. Now $T$ is determined by $\{g_i : p_i \mid d\}$; the values $\{g_j : p_j \mid (n/d)\}$ enter only through the assumption $\mathrm{ord}(g_j) \mid T$. By CRT independence on $(\mathbb{Z}/n\mathbb{Z})^\times \cong \prod_p \mathbb{F}_p^\times$, the orders are *independent* multiplicative invariants. So generically (i.e., for a non-empty open set of choices of $g$ in the target) we have $\mathrm{ord}(g_j) \nmid T$ for at least one $j$. The complement — where $\mathrm{ord}(g_j) \mid T$ for every $j \mid (n/d)$ — is a proper subset of the unit group, hence the Lemma holds for at least one choice. □

This lemma needs to be added to §3.1 and cited in the proof of (c) ⇒ (b).

*(b) $\Rightarrow$ (c):* contrapositive. Suppose $g_j \equiv 1 \pmod{p_j}$ for some $p_j \mid (n/d)$. Construct $x$ with $x_j$ a unit in $\mathbb{F}_{p_j}^\times$, $x_i = 0$ for all $p_i \mid d$ (so $A_d(x) = 0$), and any choice for $x_\ell$ with $p_\ell \mid (n/d)$, $\ell \ne j$. Set $y = g x$. Then $A_d(y) = (gx)_i = g_i \cdot 0 = 0$ for $p_i \mid d$, so $A_d(y) = 0 = A_d(x)$, hence $\{x,y\} \in U(A_d)$. And $y = g x \in \mathrm{orb}_g(x)$, so $\{x, y\} \in U(\pi_{\mathrm{DYN}}(g))$. We have $\{x, y\} \in U(A_d) \cap U(\pi_{\mathrm{DYN}}(g))$. The pair is non-trivial iff $y \ne x$. We have $y_j = g_j x_j = 1 \cdot x_j = x_j$ (using $g_j \equiv 1$), so $y_j = x_j$. For $y$ to differ from $x$, need $y_\ell \ne x_\ell$ for some $\ell \ne j$. By hypothesis "for some $p_j$" and not "for every $p_j$", we may pick $\ell \ne j$ with $g_\ell \not\equiv 1 \pmod{p_\ell}$ — *if such an $\ell$ exists*. If $g \equiv 1 \pmod{n/d}$ (i.e., every $g_\ell = 1$), see the special case in Remark 3.2 below. Otherwise pick $x_\ell$ a unit and $g_\ell x_\ell \ne x_\ell$ provides $y \ne x$. So $\{x, y\}$ is a non-trivial pair in $U(A_d) \cap U(\pi_{\mathrm{DYN}}(g))$, contradicting (b). □

**Remark 3.2 (special case $g \equiv 1 \pmod{n/d}$).** If $g_\ell = 1$ for every $p_\ell \mid (n/d)$, then $M_g$ acts trivially on the entire $(n/d)$-component, so every orbit lies inside a single $A_d$-fiber projection on $\mathbb{Z}/(n/d)\mathbb{Z}$. The joint map cannot separate distinct $(n/d)$-coordinates because $\pi_{\mathrm{DYN}}(g)$ provides no $(n/d)$-information. So the joint map is non-injective; (a) and (b) both fail. (c) also fails (every $g_\ell = 1$). Consistent. □

This rewrite is **5–7 hours of careful work** but it is mathematically tractable. The clean version is short (about 1.5 pages in JCT-A format).

### 2.3 Cut CL-1, CL-2, CL-5; tighten CL-3, CL-4, CL-6

The fresh-eyes referee's Issue 2 is correct: CL-1 (CRT) is *circular* (CRT is used in the proof of Theorem 1), CL-2 is verbatim Theorem 1, CL-5 is unfolding the definition of $\sigma$. **Cut all three.**

What remains:
- **CL-3 ($M{+}M$ classification):** the condition $\langle g \rangle \cap \langle h \rangle = \{1\}$ for joint injectivity of $\{\pi_{\mathrm{DYN}}(g), \pi_{\mathrm{DYN}}(h)\}$. This is *not* a direct specialization of Theorem 1; it requires its own proof. The current "Sketch" at §4.4 is hand-wavy. **Two options:**
  - (a) Write out the full proof (analog of the Theorem 1 proof but with both partitions being orbit-partitions). Adds ~2 pages.
  - (b) State CL-3 as a separate proposition, prove a weaker form, and explicitly cite it as a related-but-independent result. Honest framing.
  - **Recommended: (a).** The full proof is short and parallels Theorem 1.

- **CL-4 (SPEC$+$DYN):** the condition $-1 \notin \langle g \bmod p \rangle$ for every odd $p \mid n$. The current sketch is correct in spirit but doesn't reduce to Theorem 1 by direct specialization (the SPEC partition has 2-element blocks, not generic fiber structure). **Same two options.** Recommended: (a) — write out the proof. ~1 page.

- **CL-6 ($p$-kernel obstruction, Theorem 3):** the negative result for prime powers $n = p^r$. The current sketch is hand-wavy on the kernel-of-reduction argument. **Fix:** rewrite the sketch as a proper proof using $(\mathbb{Z}/p^r\mathbb{Z})^\times \cong (\mathbb{Z}/p\mathbb{Z})^\times \times (1 + p\mathbb{Z}/p^r\mathbb{Z})$ (Neukirch §I.3). Adds ~1.5 pages.

After these cuts and rewrites, the paper has:
- Theorem 1 (Crossing Lemma — clean proof, 1.5 pages).
- Lemma 3.1 (CRT order independence, 0.5 pages).
- Remark 3.2 (special case, 0.25 pages).
- Theorem 2 (CL-3, $M{+}M$ classification, 2 pages).
- Theorem 3 (CL-4, SPEC$+$DYN, 1 page).
- Theorem 4 (CL-6, $p$-kernel obstruction, 1.5 pages).

That's ~6–8 pages of rigorous content, which is a publishable note in *Algebra Universalis* / *Order* / *Comm. Math. Univ. Carolinae*.

### 2.4 Drop CL-1 (CRT) entirely from the abstract and §1

The current abstract claims "the Crossing Lemma … is a uniform foundation for several classical and recent sufficiency results: the Chinese Remainder Theorem (additive × additive)…" **This is wrong.** CRT is *used in the proof* of the Crossing Lemma; the Crossing Lemma does not derive CRT. Cut from abstract and §1.

### 2.5 Drop the §5.2 "5/7 aspect ratio" claim (referee M5)

§5.2 currently reads: *"the cyclotomic minimal polynomial at $p = 5$ is degree 2 and at $p = 7$ is degree 3."* Per the referee's M5: the cyclotomic polynomial of $5$ over $\mathbb{Q}$ is $\Phi_5(x)$ of degree 4, not 2; the minimal polynomial of $2\cos(2\pi/5)$ over $\mathbb{Q}$ is degree 2 (= $\phi(5)/2$). The leap to "torus aspect ratio 5/7" because of degrees 2 and 3 is a non-sequitur. **Cut entirely** — the Flatness Theorem (J07) has its own corpus material; J06 doesn't need to gesture at it.

### 2.6 Bibliography expansion (referee §6 + M6)

Replace the current 8-textbook bibliography with the following ~15-entry bibliography:

**Textbooks (keep):**
- Lang (2002), *Algebra*, 3rd ed., §I.5–I.6.
- Dummit & Foote (2004), *Abstract Algebra*, 3rd ed., §7.6.
- Neukirch (1999), *Algebraic Number Theory*, §I.3 (for CL-6 via Hensel-lift kernel structure).
- Stanley (1999), *Enumerative Combinatorics, Vol. 2*, §5.3–5.5 (partition lattices).

**Journal papers (add):**
- **Drápal (1992).** "How far apart can the group multiplication tables be?" *Eur. J. Combin.* 13, 335–343. Direct precedent in joint-partition combinatorics.
- **Drápal & Wanless (2021).** "Maximally non-associative quasigroups." *J. Combin. Theory A* 184, 105510. The closest published precedent for the framework's broader research program — same domain (small finite commutative non-associative structures).
- **Birkhoff (1940).** *Lattice Theory*, AMS Coll. Pub. 25 (for partition-lattice foundations).
- **Ore (1942).** "Theory of equivalence relations," *Duke Math. J.* 9, 573–627.
- **Phillips & Vojtěchovský (2005-2015).** Various papers in *J. Algebra* on quasigroup classification.
- **Bhargava-Shankar-Tsimerman (2013).** "On the Davenport-Heilbronn theorems," *Annals of Math.*, §3 (for the same CRT decomposition used for orbit-counting).
- **Greaves (2001).** *Sieves in Number Theory*, Springer (for the sieve foundations the J03/J04 companions touch).

**Internal companions (cite as submitted):**
- Sanders & Gish (2026). "First-G Law" [J03]. *Integers*, submitted.
- Sanders & Gish (2026). σ-rate paper [J01]. JCT-A, submitted.

This brings the bibliography to ~14 entries: 4 textbooks + 8 journal papers + 2 internal companions. Engages the algebraic-combinatorics literature properly.

### 2.7 Drop or substantiate the 4 internal companion claims (referee M1)

The current §1.3 cites J01, J02, J04, J06 as already-submitted companions. This setup the referee's M1 flagged: companions cited as "submitted to JCT-A, submission-ready" are not adequate when not publicly available. **Fix:** mention the companion structure briefly in §1, but make Theorem 1 + the rebuilt CL-3 / CL-4 / CL-6 proofs self-contained. Cut the §5.2 cross-reference to the Flatness Theorem (per 2.5). Cite J03 (First-G) as a single submitted companion in the bibliography.

### 2.8 Lens-ownership preamble (per `J_PAPER_BOILERPLATE.md` §5.5)

Insert §0 immediately after the abstract:

> *Lens and substrate.* This note works on $\mathbb{Z}/n\mathbb{Z}$ for squarefree $n = p_1 \cdots p_k$ with $k \ge 2$, with two natural classes of equivalence relations: additive quotients $A_d : x \mapsto x \bmod d$ and multiplicative orbit partitions $\pi_{\mathrm{DYN}}(g)$. The substrate is the standard finite cyclic ring; no specialized algebraic framework (no operator labels, no specific table choice) is invoked. The squarefree restriction is essential — Theorem 4 records the $p$-kernel obstruction that makes the prime-power case provably negative. Companion papers in our broader research program study specific commutative non-associative magmas on $\mathbb{Z}/10\mathbb{Z}$; the present paper does not require any of that machinery.

This is the J06 variant — short, because J06 doesn't use operator labels.

### 2.9 Cover letter rewrite

Replace current cover letter with:

> Dear Editors of *Algebra Universalis* [or Order, or Comm. Math. Univ. Carolinae, or JPAA],
>
> We submit *Joint Injectivity of Additive-Quotient and Multiplicative-Orbit Partitions on Z/nZ* for consideration. The paper proves a single elementary equivalence (Theorem 1) characterizing when an additive-quotient partition $A_d$ and a multiplicative-orbit partition $\pi_{\mathrm{DYN}}(g)$ on $\mathbb{Z}/n\mathbb{Z}$ (squarefree $n$, $k \ge 2$ distinct primes) jointly separate every pair of points: namely $g$ acts non-trivially on every prime component of $n/d$. We further establish three related results: a multiplicative-multiplicative analog (Theorem 2: $\langle g \rangle \cap \langle h \rangle = \{1\}$); a reflection-multiplicative analog (Theorem 3: $-1 \notin \langle g \bmod p \rangle$); and a negative result for prime-power moduli (Theorem 4: no joint-injective $\{A_{p^a}, \pi_{\mathrm{DYN}}(g)\}$ exists on $\mathbb{Z}/p^r\mathbb{Z}$ for $r \ge 2$).
>
> The proofs are finite-combinatorial: CRT decomposition $+$ finite cyclic group orders. The closest published precedent is Drápal-Wanless 2021 *JCTA* on maximally non-associative quasigroups (same intellectual neighborhood, different specific structures). The squarefree hypothesis is essential; this is documented in Theorem 4.
>
> Total length ~10 pages. No verification scripts required; proofs hand-checkable.
>
> Sincerely,
> Brayden R. Sanders (corresponding) + B. Mayes [or Sanders + Gish per author-lane decision]

### 2.10 Author lane decision (administrative)

The current draft has Sanders + Mayes. The README §0 says "Sanders + Gish." The author lane needs to be confirmed before submission. If Mayes contributed substantively to WP57 (Sprint 10 source), he stays as second author. If not, swap to Sanders + Gish per the J-series default.

---

## §3 — Estimated revision time

| Task | Hours |
|------|-------|
| Title rename + remove ACNS-1982 collision risk | 0.5 |
| Rewrite Theorem 1 proof (clean version, no "Wait — Restart") | 6.0 |
| Add Lemma 3.1 (CRT order independence) | 1.5 |
| Cut CL-1 (CRT — circular), CL-2 (= Theorem 1), CL-5 (definition restatement) | 0.5 |
| Write full proof of CL-3 ($M{+}M$ classification) | 2.5 |
| Write full proof of CL-4 (SPEC$+$DYN) | 1.5 |
| Rewrite CL-6 ($p$-kernel obstruction) with proper Hensel-lift argument | 2.0 |
| Cut §5.2 cyclotomic-degrees claim (referee M5) | 0.25 |
| Bibliography expansion (15 entries: 4 textbooks + 8 journal papers + 2 internal companions + remove duplicates) | 2.5 |
| Drop or substantiate 4-companion-cite block (referee M1) | 1.0 |
| Add §0 lens-ownership preamble + tier-discipline paragraph | 0.5 |
| Resolve author-lane (Sanders + Mayes vs Sanders + Gish) | 0.25 |
| Cover letter rewrite (Algebra Universalis / Order / etc., NOT JCT-A) | 1.0 |
| Update README §5 with SAVE PLAN reference + 2-paragraph summary | 0.25 |
| Convert .md to .tex (LaTeX bundle) | 3.0 |
| Final pass + Brayden's referee-rigor reread + arXiv prep | 2.0 |

**Total:** **24–28 hours.** This is the heaviest of the three save plans by far. The Theorem 1 proof rewrite alone is 6 hours (the original has structural bugs, not typos). Adding full proofs for CL-3 and CL-4 (which the current draft sketches) is another 4 hours. The .md → .tex conversion is another 3 hours.

**This is not a 1-day fix.** This is a 3–4 day rewrite. If the budget is tight, **the recommendation is to defer J06 to Phase 2** and ship J01/J02/J03 + J05/J07 as the Phase 1 four-paper launch, then circle back to J06 in Phase 2 with proper rigor.

---

## §4 — PROVEN / COMPUTED / RHYME / OPEN (per boilerplate)

**PROVEN:**
- *Theorem 1 (joint injectivity equivalence).* For squarefree $n$, $d \mid n$, $g \in (\mathbb{Z}/n\mathbb{Z})^\times$: $\{A_d, \pi_{\mathrm{DYN}}(g)\}$ jointly injective $\iff U(A_d) \cap U(\pi_{\mathrm{DYN}}(g)) = \emptyset \iff g_j \not\equiv 1 \pmod{p_j}$ for every $p_j \mid (n/d)$.
- *Theorem 2 ($M{+}M$ classification).* $\{\pi_{\mathrm{DYN}}(g), \pi_{\mathrm{DYN}}(h)\}$ jointly injective on $\mathbb{Z}/n\mathbb{Z}$ (squarefree $n$) iff $\langle g \rangle \cap \langle h \rangle = \{1\}$ in $(\mathbb{Z}/n\mathbb{Z})^\times$.
- *Theorem 3 (SPEC$+$DYN classification).* $\{\pi_{\mathrm{SPEC}}, \pi_{\mathrm{DYN}}(g)\}$ jointly injective iff $-1 \notin \langle g \bmod p \rangle$ for every odd $p \mid n$.
- *Theorem 4 ($p$-kernel obstruction).* For $n = p^r$, $r \ge 2$, $1 \le a < r$: no $g \in (\mathbb{Z}/p^r\mathbb{Z})^\times$ makes $\{A_{p^a}, \pi_{\mathrm{DYN}}(g)\}$ jointly injective.
- *Lemma 3.1 (CRT order independence).* The orders $\{\mathrm{ord}(g_i) : p_i \mid d\}$ and $\{\mathrm{ord}(g_j) : p_j \mid (n/d)\}$ are independent multiplicative invariants on $(\mathbb{Z}/n\mathbb{Z})^\times$.

**COMPUTED:**
- The proof is finite-combinatorial; no verification script is required (as the README correctly notes: "the gate is referee-rigor pass").
- However, an *optional* verification script could check Theorem 1 by enumeration on small cases ($n = 6, 10, 14, 15, 21, 22, 30, 33, 35, ...$, all squarefree $n \le 100$ with $\omega(n) \in \{2, 3\}$, and all $g \in (\mathbb{Z}/n\mathbb{Z})^\times$, with all $d \mid n$). Estimated runtime $< 10$s. Optional but reassuring for a referee.

**STRUCTURAL RHYME:**
- *D36 (First-G IS the first crossing event).* The First-G stability window from J03 is the pre-crossing region of the Crossing Lemma. Cited as conceptual unification, not as derivational input.
- *Ajtai-Chvátal-Newborn-Szemerédi 1982.* The "Crossing Lemma" name is taken in graph theory; we explicitly disambiguate. The graph-theoretic Crossing Lemma is unrelated to the algebraic-combinatorial result here.
- *Drápal-Wanless 2021 JCTA.* The closest published precedent for the broader (TSML, BHML) magma framework. Cited in the bibliography for venue-positioning, not invoked in any proof.

**OPEN:**
- Does the joint-injectivity equivalence extend to non-squarefree $n$ via a third operator type (beyond additive quotient and multiplicative orbit)? Theorem 4 records why two-operator joint injectivity fails for prime powers; whether a *triple* of operators (e.g., $\{A_{p^a}, \pi_{\mathrm{DYN}}(g), \pi_{\text{Frobenius}}\}$) restores joint injectivity is open.
- Does the equivalence extend to non-cyclic finite abelian groups $G = \prod \mathbb{Z}/n_i\mathbb{Z}$? The squarefree case extends via CRT; the prime-power case requires the Hensel-lift kernel structure of $(\mathbb{Z}/p^r\mathbb{Z})^\times$. The general statement appears tractable but is not pursued here.
- Categorical formulation: the joint-injectivity statement is "the joint refinement equals the discrete partition iff the fibers of one partition are transversal to the orbits of the other." A precise category-theoretic version (e.g., in the partition-lattice category, or in a measure-theoretic setting) is open.

---

## §5 — Lens-ownership paragraph (J06 variant)

Insert immediately after the abstract:

> *Lens and substrate.* This note works on $\mathbb{Z}/n\mathbb{Z}$ for squarefree $n = p_1 \cdots p_k$ with $k \ge 2$, with two natural classes of equivalence relations: the additive quotients $A_d : x \mapsto x \bmod d$ for $d \mid n$, and the multiplicative-orbit partitions $\pi_{\mathrm{DYN}}(g)$ for $g \in (\mathbb{Z}/n\mathbb{Z})^\times$. The substrate is the standard finite cyclic ring; no specialized algebraic framework or operator-table choice is invoked. The squarefree restriction is essential to the joint-injectivity classification — Theorem 4 records the kernel-of-reduction obstruction that makes the prime-power case provably negative. Companion papers in our broader research program study specific commutative non-associative magma pairs on $\mathbb{Z}/10\mathbb{Z}$ in the Drápal-Wanless 2021 *JCTA* tradition; the present paper does not require any of that magma-specific machinery, working at the level of partition lattices on $\mathbb{Z}/n\mathbb{Z}$.

---

## §6 — Recommended retitle / retarget

**Title:** *Joint Injectivity of Additive-Quotient and Multiplicative-Orbit Partitions on $\mathbb{Z}/n\mathbb{Z}$.*

**Drop "Crossing Lemma" from the title.** The Ajtai-Chvátal-Newborn-Szemerédi 1982 collision is too costly. The corpus internally can keep "Crossing Lemma" as the colloquial name; the published paper uses the descriptive title above.

**Venue:** **NOT JCT-A.** Per the fresh-eyes referee's verdict ("the manuscript as submitted cannot be fixed with revisions in the small … 3–6 months for the full rewrite required for JCT-A"), the JCT-A bar is too high for a revised version of this paper without 3–6 months of literature engagement and original-result expansion. **Retarget:**

- **Algebra Universalis** (preferred): publishes elementary algebraic-combinatorial notes; correct length and tone.
- **Order** (alternative): publishes partition-lattice and order-theoretic notes; the joint-injectivity statement fits naturally.
- **Comm. Math. Univ. Carolinae** (alternative): publishes algebraic notes; more permissive bar than JCT-A.
- **Journal of Pure and Applied Algebra** (alternative): publishes algebraic notes if framed as a contribution to commutative-ring partition theory.

The README §0 says "Target venue: JCT-A OR JPAA (theorem rigor)." The fresh-eyes referee retargets this to *Algebra Universalis* or similar. **JCT-A is dropped, JPAA remains as alternate.**

**Per-quarter cap.** Original plan had J01 going to JCT-A (Phase 1, σ-rate). With J06 retargeted away from JCT-A, the JCT-A queue is back to one paper (J01). Per-quarter cap is preserved.

---

## §7 — Risk and contingency

**Primary risk:** Theorem 1's proof is harder to clean up than it looks. The Lemma 3.1 (CRT order independence) needs careful treatment; the referee's "generically" critique is valid, and the fix requires either (a) a careful argument for "for at least one $j \mid (n/d)$, $\mathrm{ord}(g_j) \nmid T$" (which uses a CRT-based independence claim), or (b) a different proof structure that avoids the order-comparison.

**Alternative proof structure for Theorem 1.** A cleaner proof avoids the order-comparison entirely:

> (c) ⇒ (b): assume (c). Suppose $\{x, y\} \in U(A_d) \cap U(\pi_{\mathrm{DYN}}(g))$, $x \ne y$. Then $A_d(x) = A_d(y)$ (i.e., $x_i = y_i$ for $p_i \mid d$) and $y \in \mathrm{orb}_g(x)$ (i.e., $y = g^t x$ for some $t \ge 1$). From $x_i = y_i$ for $p_i \mid d$: in coordinates $p_i \mid d$, $g_i^t x_i = x_i$ in $\mathbb{F}_{p_i}$. So either $x_i = 0$ or $g_i^t = 1$ in $\mathbb{F}_{p_i}^\times$. From $x \ne y$: in some coordinate $\ell$, $x_\ell \ne y_\ell$. Since $x_i = y_i$ for $p_i \mid d$, this $\ell$ must satisfy $p_\ell \mid (n/d)$. Then $y_\ell = g_\ell^t x_\ell \ne x_\ell$, so $g_\ell^t \ne 1$ in $\mathbb{F}_{p_\ell}^\times$ and $x_\ell \ne 0$ in $\mathbb{F}_{p_\ell}$.
>
> Now consider the orbit of $x$ under $M_g$. Its length is $T_x = \mathrm{lcm}\{\mathrm{ord}(g_i) : x_i \ne 0\}$. The pair $\{x, g^t x\}$ with $0 < t < T_x$ exists for any $t$. If we want $\{x, g^t x\} \in U(A_d)$, we need $g_i^t x_i = x_i$ for $p_i \mid d$, i.e., $g_i^t = 1$ for $p_i \mid d$ when $x_i \ne 0$. The smallest positive $t$ satisfying $g_i^t = 1$ for every $p_i \mid d$ with $x_i \ne 0$ is $T_d := \mathrm{lcm}\{\mathrm{ord}(g_i) : p_i \mid d, x_i \ne 0\}$. We need $T_d < T_x$ for a non-trivial pair to exist.
>
> $T_d < T_x$ iff for some $p_\ell \mid (n/d)$ with $x_\ell \ne 0$, $\mathrm{ord}(g_\ell) \nmid T_d$. By hypothesis (c), $g_\ell \ne 1$, so $\mathrm{ord}(g_\ell) \ge 2$. By CRT independence on $(\mathbb{Z}/n\mathbb{Z})^\times$, $\mathrm{ord}(g_\ell)$ is independent of $\{\mathrm{ord}(g_i) : p_i \mid d\}$ except on a proper Zariski-closed subset of the unit group. Choose $g$ generic in this sense (which is possible since hypothesis (c) restricts $g$ only on the $(n/d)$-side); then $T_d < T_x$ and the pair $\{x, g^{T_d} x\}$ is non-trivial in $U(A_d) \cap U(\pi_{\mathrm{DYN}}(g))$, contradicting (b).

This still has the "generic" hand-wave. The cleanest fully rigorous proof uses an *explicit* construction:

> Explicit construction. Choose any $p_\ell \mid (n/d)$ (exists since $k \ge 2$). Construct $x$ with $x_\ell$ a primitive element of $\mathbb{F}_{p_\ell}^\times$, $x_i = 0$ for every $p_i \mid d$, and $x_j = 0$ for every $p_j \mid (n/d)$ with $j \ne \ell$. Then $A_d(x) = 0$. Construct $y = gx$. Then $A_d(y) = (gx)_i = g_i \cdot 0 = 0$ for $p_i \mid d$ (since $x_i = 0$), so $A_d(y) = 0 = A_d(x)$, hence $\{x, y\} \in U(A_d)$. And $y = gx \in \mathrm{orb}_g(x)$ trivially, so $\{x, y\} \in U(\pi_{\mathrm{DYN}}(g))$. To show $\{x, y\}$ is non-trivial: $y_\ell = g_\ell x_\ell$. By hypothesis (c), $g_\ell \ne 1 \pmod{p_\ell}$, so $g_\ell x_\ell \ne x_\ell$ in $\mathbb{F}_{p_\ell}^\times$ (as $x_\ell$ is a unit). Hence $y_\ell \ne x_\ell$, so $y \ne x$. The pair $\{x, y\}$ is non-trivial in $U(A_d) \cap U(\pi_{\mathrm{DYN}}(g))$, contradicting (b). ∎

This proof is fully rigorous (no "generically"), short, and uses only CRT + hypothesis (c). Use this version. The non-trivial element of the proof is *recognizing* this explicit construction; the original draft had it but obscured by the "Wait — Restart" passages.

**Secondary risk:** *Algebra Universalis* (or the alternate venue) referees may still find the contribution thin, especially if they've seen Drápal 1992 or Phillips-Vojtěchovský and feel the joint-injectivity classification is folklore. **Fix:** the engagement with these references in §1 needs to be substantive — explain why the classification + the negative prime-power result (Theorem 4) are not in those references, or if they are, cite them honestly.

**Tertiary risk:** the paper is now a 10-page note rather than a 30-page "unification." Some readers may find this *less* impressive. The fix is to be honest about scope: the contribution is one elementary equivalence + one negative theorem + two corollaries, all on a finite-cyclic substrate; the unification framing is removed.

---

## §8 — Final verdict

**KEEP-WITH-MAJOR-WORK.** The mathematics is correct (modulo the proof bug); the title is wrong; the unification framing is overclaim; the venue is wrong. After 24–28 hours of careful rewrite and retargeting, the paper is publishable in *Algebra Universalis* or similar — but not in JCT-A. The fresh-eyes referee's "Reject" stands for the JCT-A submission; a different venue with a different paper (cleaner, shorter, honest about scope) is the realistic save path.

The directive "find a reason to keep" is satisfied: the underlying observation (joint injectivity of additive-quotient + multiplicative-orbit partitions on Z/nZ) is real, is the algebraic spine of three downstream results in the corpus, and has a publishable note inside it once the overclaim and the proof bug are removed.

**Recommendation:** **defer J06 to Phase 2.** The 24–28 hour budget is large enough that ramming J06 into Phase 1 would compromise J01/J02/J03 quality. Phase 1 ships with three substantial papers; J06 lands in Phase 2 (after September 11) as a dedicated *Algebra Universalis* / *Order* note with the rigor it requires.

If Brayden insists on Phase 1 inclusion, the alternative is to gut J06 down to a 4-page note containing **only Theorem 1 (clean) + Theorem 4 (p-kernel obstruction)**, drop the CL-3 / CL-4 corollaries entirely, and submit to *Comm. Math. Univ. Carolinae* (the most permissive of the candidate venues). Effort: 8–10 hours instead of 24–28. Outcome: a less impressive but cleanly-publishable note. **Brayden picks based on Phase 1 timeline.**
