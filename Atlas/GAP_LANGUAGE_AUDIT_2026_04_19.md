# Gap-Language Audit: Tier-1 Submissions (Sprint 34)

**Date:** 2026-04-19
**Auditor:** Claude (per Brayden directive: every word we choose is defined by us rigorously or by previous rigor)
**Submission window:** Wednesday 2026-04-22
**Files audited:**

1. `Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/sinc2_zero_law.tex`
2. `Gen13/targets/journals/tier1_submit_now/jcap_xi_cosmology/jcap_xi_cosmology.tex`
3. `Gen13/targets/journals/tier1_submit_now/sigma_rate/sigma_rate_theorem.tex`

**Suspicious-word checklist applied:** corridor, gap, hold, shell, bridge, collapse, flow, cascade, opens, obstruction, plus TIG-framing leaks (TIG, crystal, crossing, harmony, coherence keeper).

---

## File 1: sinc2_zero_law.tex

### TOP-OF-FILE FINDING — TRIVIALITY IN MAIN THEOREM

**The "p prime" hypothesis in Theorem 1 (line 97-103) is vacuous in the biconditional as written.**

The theorem states:
> Let $p$ be prime and $k$ a positive integer. Then $\sinc^2(k/p)=0 \iff p\mid k$.
> Within $k\in\{1,\dots,p\}$ the unique zero is at $k=p$.

Both clauses are true for ANY positive integer $n$ replacing $p$:
- The biconditional `sinc²(k/n) = 0 ⟺ n|k` reduces to `sin(πk/n) = 0 ⟺ πk/n ∈ πℤ ⟺ n|k`. No primality needed.
- "Within $k \in \{1,\dots,n\}$ the unique zero is at $k=n$" follows from the same fact: the only multiple of $n$ in $\{1,\dots,n\}$ is $n$ itself, regardless of whether $n$ is prime, composite, or 1.

**Where primality actually does work in the manuscript:**
- Line 114-115 (proof body): "since $p$ is prime and $1 \le k < p$, we have $\gcd(k,p)=1$." Primality is used to justify coprimality of every interior $k$ with $p$. But coprimality is *stronger than necessary* for the zero conclusion (which only requires non-divisibility), and the proof itself even acknowledges this implicitly when it writes "so $p \nmid k$". The non-divisibility step is the operative one; coprimality is a free side-product of primality.
- Line 120-128 (remark): the remark is honest and admits the point — "What primality contributes is that no proper divisor of $p$ lies strictly between $1$ and $p$, so the corridor's interior is clean." This is a coprimality/structural statement, not a zero-detection statement.

**Recommended fixes (escalation order):**
1. **Minimum:** Restate Theorem 1 with general $n$, then add a corollary specializing to primes that says exactly what primality buys you (every interior $k$ is a unit mod $p$ — a coprimality statement, not a zero statement).
2. **Better:** Reframe the paper around the *coprimality* structure that primality genuinely provides. The phrase "no proper divisor of $p$ lies strictly between $1$ and $p$" in line 127 is the actual content. Build the theorem around that. The current theorem statement reads as a number-theoretic claim but the math is purely trigonometric.
3. **Best (if Brayden wants the prime emphasis):** Replace the biconditional formulation with the *unit-detection* formulation: "for prime $p$, $\sinc^2(k/p)$ takes the value $0$ at exactly one point in $\{1,\dots,p\}$, and at every other point the argument $k/p$ is a unit fraction in lowest terms." Then primality is doing the work (forcing reducedness).

This is a referee-bait issue. *Integers* referees in particular will notice immediately. **Must fix before Wednesday.**

### Per-occurrence table (sinc² paper)

| Line | Word | Context snippet | Classification | Fix |
|---|---|---|---|---|
| 43 (keywords) | corridor | `\keywords{sinc function, prime arithmetic, corridor, loop closure, ...}` | **DROP** as keyword. Not a defined object. | Remove from keyword list. Replace with `arithmetic progression` or `lattice`. |
| 56 (abstract) | corridor | "Within the corridor $k\in\{1,\dots,p\}$ the unique zero..." | **STRUCTURAL SHORTHAND** (pinned to a set in same sentence) | Acceptable since the set is named inline; consider replacing with "interval" or "arithmetic window" for venue fit. Integers readers will read "corridor" as imported terminology. |
| 59 (abstract) | loop closure | "*loop closure* (the corridor closes exactly once, at the prime)" | **STRUCTURAL SHORTHAND** (Corollary 1 below makes it precise — the unique zero of $\sinc^2$ on the set) | OK: italicized as a named result (Corollary 1) and immediately re-stated formally. Keep but ensure the corollary statement (line 133-137) is what the reader sees as the definition. |
| 60 (abstract) | crossing | "*fold necessity* (a unique amplitude crossing occurs in the interior...)" | **STRUCTURAL SHORTHAND** (pinned to "amplitude crossing" — refers to the IVT crossing of $1/2$ in Corollary 2) | OK in body since Corollary 2 makes it formal; **flag for TIG-leak risk**: the bare word "crossing" in mathematical context near the abstract is the kind of thing reviewers may grep. Consider replacing with "intersection point" or "level crossing of $1/2$". |
| 62 (abstract) | no-shortcut | "the *no-shortcut lemma* (the path from the corridor entrance to its zero has length exactly $p-1$)" | **STRUCTURAL SHORTHAND** for Corollary 3 | OK; Corollary 3 makes it formal. |
| 91 (setup) | corridor | "we study the values $\sinc^2(k/p)$ along the rational corridor $\{1/p, 2/p, \dots\}$" | **STRUCTURAL SHORTHAND** (pinned to a set inline) | OK; the word is doing structural-naming work and the set is given. |
| 102 (theorem) | $k\in\{1,\dots,p\}$ | "Within $k\in\{1,\dots,p\}$ the unique zero is at $k=p$." | n/a — fully typed | OK but see TRIVIALITY note above: this clause is true for any positive integer $p$. |
| 127 (remark) | corridor | "so the corridor's interior is clean" | **HEURISTIC/MOTIVATION** (in remark, after the formal proof) | OK as remark commentary. |
| 134 (Cor 1) | corridor | "The corridor $\{1/p,2/p,\dots,p/p\}$ is nonzero on..." | **DEFINED OBJECT** (the set is given inline) | OK. |
| 136 (Cor 1 statement) | closes / closure | "The corridor closes exactly once." | **STRUCTURAL SHORTHAND** for "$\sinc^2 = 0$ at exactly one point of the corridor" | Marginally OK. Consider rephrasing: "$\sinc^2$ vanishes at exactly one point of the corridor." The word "closes" is doing metaphorical work. |
| 141 (Cor 1 proof) | crossing | "begins in positive territory and terminates at zero, giving one crossing at the prime itself" | **HEURISTIC/MOTIVATION** (proof is informal restatement of Theorem 1) | The word "crossing" here is loose — "crossing" of what level? Replace with "...giving exactly one zero, at $k=p$." |
| 146 (Cor 2 statement) | fold | "there exists a unique $x^{*}\in(0,1)$ — the *fold* — where $\sinc^2(x^{*})=1/2$" | **DEFINED OBJECT** (defined inline, in italics, immediately) | OK. |
| 169 (Cor 2 proof) | fold crosses | "so the fold crosses between $k=3$ and $k=4$" | **STRUCTURAL SHORTHAND** for "$x^*$ lies between $3/7$ and $4/7$" | Marginally OK. The verb "crosses" between two integers is sloppy; the fold is a real number, not something that traverses. Suggest: "so $x^* \in (3/7, 4/7)$." |
| 180-181 (Cor 3 proof) | path / length | "any path from the corridor entrance to the $\sinc^2$ null has length at least $p-1$" | **DROP** in proof step: "path" and "length" are not defined objects. The result IS just Theorem 1 restated. | Replace with: "By Theorem 1, the only zero of $\sinc^2(k/p)$ for $k\in\{1,\dots,p\}$ occurs at $k=p$; in particular, no $k\in\{1,\dots,p-1\}$ is a zero." Drop "path" and "length" — these read as TIG-framing leaks. |
| 196 (Sec 4) | gate | "the first sidelobe of a rectangular spectral gate" | **DEFINED OBJECT** (standard signal-processing terminology) | OK; "spectral gate" = window/aperture in DSP literature. |
| 202 (Sec 4) | spectral partition | "$\sinc^2(u)$ and $R_2(u)$ sum to unity --- a complete spectral partition" | **STRUCTURAL SHORTHAND** (the partition IS the equation $\sinc^2 + R_2 = 1$) | OK; the equation immediately precedes. |
| 246 (Sec 7) | bridge | "beyond the Montgomery bridge observation in Section..." | **HEURISTIC/MOTIVATION** (in scope-limits section) | Marginally OK. "Bridge" reads as informal. Suggest: "beyond the Montgomery pair-correlation identity in Section 4." |

### sinc² file: counts & DROP backlog

| Classification | Count |
|---|---|
| DEFINED OBJECT | 4 |
| STRUCTURAL SHORTHAND | 7 |
| HEURISTIC/MOTIVATION | 2 |
| DROP | 2 (line 43 keyword; lines 180-181 "path"/"length" in Cor 3 proof) |

**DROP edit backlog:**
1. Line 43 — remove `corridor` from `\keywords{...}` list. Replace with `arithmetic progression` or omit.
2. Lines 180-181 — replace the proof of Corollary 3 with: "By Theorem~\ref{thm:main}, the only zero of $\sinc^2(k/p)$ for $k \in \{1,\dots,p\}$ is $k=p$. Hence no $k \in \{1,\dots,p-1\}$ is a zero." Drop the words "path" and "length"; they are not defined.

**Plus the TRIVIALITY at the top of this section — this is the highest-priority fix.** Without it, a referee can dispose of the paper in one page.

### sinc² file: rigor verdict
The math is correct; the framing is the problem. Two specific edits (the TRIVIALITY restatement and the Cor 3 proof rewrite) put it in shape. The paper otherwise reads cleanly for *Integers*.

---

## File 2: jcap_xi_cosmology.tex

### Per-occurrence table (xi cosmology paper)

| Line | Word | Context snippet | Classification | Fix |
|---|---|---|---|---|
| 78 (abstract) | drives | "drives a freezing quintessence history" | **HEURISTIC** in abstract (verb of motion) | OK in abstract. |
| 79 (abstract) | freezing | "freezing quintessence history" | **DEFINED OBJECT** (standard cosmology term, see Caldwell-Linder 2005 in the field; also defined operationally by Prop 7 (ii) at line 299: "$w_\Xi \to -1^+$ near the vacuum in slow roll: freezing quintessence") | OK; the term has a literature meaning AND is pinned to Prop 7 in this paper. Recommend adding one inline citation to a freezing-vs-thawing review (Caldwell-Linder 2005) at the abstract. |
| 117 (intro) | rolls | "the field rolls toward infinity" | **DEFINED OBJECT** (standard cosmology — slow-roll dynamics) | OK. |
| 129 (intro) | settles | "exactly as the field settles at its vacuum" | **HEURISTIC** in intro | OK; standard usage. |
| 132 (intro) | forbidding phantom crossing | "...forbidding phantom crossing." | **STRUCTURAL SHORTHAND** (pinned to Prop 7 (iv) at line 301: "$w_\Xi \ge -1$ on-shell: no phantom crossing") | OK. |
| 134 (intro) | delimit what is formal | "we state the canonical action and delimit what is formal and what is interpretive" | n/a — methodological framing | OK. |
| 178 (Sec 2 remark) | substrate | "substrate-level interpretations" | **HEURISTIC/MOTIVATION** (in remark; explicitly deferred and disclaimed) | OK; the remark is doing the right work — explicitly labeling what is and isn't claimed. |
| 196-198 (Sec 3.1) | Box, EL eqn | $\Box\Xi=1+\log\Xi$ | n/a — fully typed | OK. |
| 218-220 (Sec 3.3) | Setting $\Box\Xi = 0$ | vacuum derivation | n/a — fully typed | OK. |
| 247 (Sec 3.4) | $m_\Xi^{2}=\kappa_\Xi e$ | mass formula | n/a — fully typed | OK. |
| 261-262 (Sec 3.5) | "globally bounded below" | "The total energy density $\rho_\Xi=\tfrac{1}{2}\kappa_\Xi\dot\Xi^{2}+V(\Xi)$ is likewise bounded below, giving global stability for $\Xi>0$" | **DEFINED OBJECT** (energy density typed, bound made explicit at line 257-258) | OK. |
| 284 (Sec 4.1) | $\boxed{\;\ddot\Xi+3H\dot\Xi=1+\log\Xi\;}$ | FRW EOM | n/a — fully typed | OK. |
| 297-302 (Prop 7) | freezing, stiff, phantom crossing | enumeration of EoS regimes | **DEFINED OBJECT** for each (each clause is given operationally with $\dot\Xi$, $\Xi$ conditions explicit) | OK. |
| 313 (Prop 7 proof) | "sign-changing locus in $\rho_\Xi$, which does not cross within a cosmologically relevant range" | clause about $\rho_\Xi$ | **STRUCTURAL SHORTHAND** (refers to the locus where $\rho_\Xi=0$, but "cross within a cosmologically relevant range" is hand-wavy) | **Flag.** Either define "cosmologically relevant range" by giving the redshift band, or excise the parenthetical. Suggest: "...away from a sign-changing locus in $\rho_\Xi$, which numerical integration in §6.2 confirms does not occur for $z \le z_i \approx 20$." Otherwise reads as a hand-wave. |
| 318-322 (Sec 4.3) | rolls, drives, settles | late-time attractor narrative | **HEURISTIC** (in narrative paragraph, conclusion follows from Prop 7(i) cited explicitly) | OK. |
| 337 (Sec 5) | "relaxes dynamically" | "the field therefore relaxes dynamically to the configuration of maximum Gibbs entropy" | **HEURISTIC** (intuitive verb in expository sentence) | OK. |
| 341-353 (Sec 5 remark) | "structurally distinguished" | BBM uniqueness remark | n/a — explicitly disclaims as motivation, not derivation | OK; very well-handled (the remark itself flags the gap between the theorem's hypothesis and what's claimed here). |
| 354 (Sec 5 remark heading) | "Information-theoretic precedents" | "Entropic approaches to dark energy in the holographic sense..." | **HEURISTIC** in remark, with citations | OK. |
| 371 (Sec 6.1) | "freezing attractor" | "The freezing attractor derived above..." | **STRUCTURAL SHORTHAND** (pinned to §4.3 "late-time attractor" + Prop 7) | OK. |
| 396 (Sec 6.2) | "monotone freezing" | "The corresponding $w(z)$ trajectory is monotone freezing" | **DEFINED OBJECT** (operationally defined by F2 in line 420: "monotone approach $w(z)\to-1$ from above"), AND visible in the table | OK. |
| 419-422 (F1-F4) | falsification list | each criterion typed | **DEFINED OBJECT** for each | OK; the F1-F4 enumeration is exemplary rigor. |
| 436 (Sec 6.4) | "minimal theory" | "the effective fifth-force coupling between $\Xi$ and SM matter is of order..." | **DEFINED OBJECT** (the action of Eq 2 is "minimal", excluding direct-matter couplings as enumerated at line 440) | OK. |
| 510-525 (Sec 7) | scope/limits enumeration | each negative claim typed | **DEFINED OBJECT** (best-practice scope statement) | Exemplary. |

**TIG-leak scan (xi cosmology):** zero hits. No mention of corridor, gap, hold, shell, bridge, collapse, flow, cascade, opens, obstruction, TIG, crystal, crossing, harmony, coherence keeper. The word "freezing" occurs but is the standard cosmology term (Caldwell-Linder 2005), not a TIG term.

### xi cosmology file: counts & DROP backlog

| Classification | Count |
|---|---|
| DEFINED OBJECT | 9 |
| STRUCTURAL SHORTHAND | 4 |
| HEURISTIC/MOTIVATION | 6 |
| DROP | 0 |

**DROP edit backlog:** None outright. ONE flag for tightening:
1. Line 313 — "cosmologically relevant range" is hand-wavy. Either give a redshift bound or cite the §6.2 numerical integration explicitly.

### xi cosmology file: rigor verdict
**Cleanest of the three.** Authors have already practiced the discipline Brayden is enforcing — every term is either typed, explicitly cited, or labeled as motivation/scope-limit. The §7 Scope-and-Limitations section is a model for the other two papers. **Submit-ready modulo line 313.**

---

## File 3: sigma_rate_theorem.tex

### Per-occurrence table (sigma rate paper)

| Line | Word | Context snippet | Classification | Fix |
|---|---|---|---|---|
| 38-42 (macros) | $\HARM, \VOID, \ECHO, \DIS, \CL$ | macro definitions | n/a (macros) | These macros bake TIG-derived names into the LaTeX. Operationally fine since each is **defined formally** in Definition 1 (line 144-159). However: $\HARM$ and $\VOID$ are TIG operator names from the CK 10-operator system. They do rigorous work here (each is a named rule of $\CL_N$) but a *Journal of Combinatorial Theory* referee will read "$\HARM$" and ask "why this name?" Consider renaming to neutral letters $T$ (top-absorbing), $Z$ (zero-absorbing), $E$ (echo) for the journal version. **Not a rigor failure, but a venue-fit risk.** |
| 67 (keywords) | "spectral gap" | keyword | **DEFINED OBJECT** (standard term in Markov chain theory) | OK. |
| 76 (abstract) | "absorbing rules" | "three absorbing rules" | **STRUCTURAL SHORTHAND** (pinned to Definition 1) | OK. |
| 78 (abstract) | $\ECHO$ rule statement | "$a+b\equiv a\cdot b\pmod N$" | n/a — fully typed | OK. |
| 89 (abstract) | "triples involving at least one $\ECHO$ composition have density $\le 3/N$" | abstract claim | **DEFINED OBJECT** (matches Theorem 1) | OK. |
| 92-96 (abstract) | "Bialynicki-Birula-Mycielski uniqueness theorem... identifies the logarithmic nonlinearity as the unique separability-preserving continuum limit" | structural corollary advertisement | **STRUCTURAL SHORTHAND** (pinned to Corollary 2 + remark on hypothesis) | OK; the abstract correctly flags "additional hypothesis (separability)". |
| 109-110 (intro) | "two absorbing classes ($\HARM$, $\VOID$) and one arithmetic class ($\ECHO$)" | intro framing | **STRUCTURAL SHORTHAND** (defined in §2) | OK. |
| 115-117 (intro) | $\sigma(N)$ definition (Eq 1) | typed equation | n/a | OK. |
| 124-129 (intro) | "places the family inside the domain of Bialynicki-Birula-Mycielski" | bridging language | **STRUCTURAL SHORTHAND** (Corollary 2) | The verb "places" is informal but pointer is to Cor 2. OK. |
| 130-135 (intro) | "Wasserstein gradient structures are recovered from discrete Markov chains carrying a spectral gap" | literature framing | **HEURISTIC/MOTIVATION** in intro | OK. |
| 132 (intro) | "spectral gap" | as above | **DEFINED OBJECT** (standard) | OK. |
| 134 (intro) | "ECHO layer forms a reversible Markov chain with an explicit absorbing-state mass" | intro framing | **STRUCTURAL SHORTHAND** but the chain itself is **NOT** constructed in the paper. This is a forward-pointer to material not present. | **Flag.** Either remove the sentence or make the construction explicit (probably out of scope for this paper — recommend remove). The phrase "absorbing-state mass" is undefined in this manuscript. |
| 144-159 (Def 1) | $\CL_N$ piecewise definition | typed | n/a — DEFINED OBJECT | OK. |
| 162-166 (Eq 4) | $\DIS, \ECHO$ as functions | typed | n/a | OK. |
| 175-202 (Lemma 1) | $\ECHO$ count | proof of $\varphi(N)+1$ | n/a — almost fully typed BUT see issue below | **Issue.** The proof is muddled around the $(0,0)$ and $(1,1)$ pairs. Lines 188-201 walk through "doubly trivial" and acknowledge "the count is $\varphi(N)$ in the strict enumeration or $\varphi(N)+1$ when $(0,0)$ is counted as a separate absorbing pair." This ambiguity in a Lemma is bad — a referee will object. **Fix:** state the lemma cleanly with a single, definite count, OR rephrase as a bound: "there are at most $\varphi(N)+1$ solutions" and prove only that. The current proof tries to have it both ways. The numerical verification at line 199-201 (giving 4, 8, 48 for $N=10,30,210$) confirms $\varphi(N)$ in the strict count. Recommend: state lemma as "**exactly $\varphi(N)$ solutions with $a,b \ne 0, N-1$**" and prove that single statement. |
| 205-211 (Cor 1) | $\rho_N \le 1/N$ | typed bound | n/a | OK; uses Lemma 1 cleanly. |
| 216-225 (Theorem 1 statement) | rate bound | typed | n/a — DEFINED OBJECT | OK. |
| 219 (Thm 1) | "absolute constant $C<3$" | the constant C | **DEFINED OBJECT** (asserted with a strict bound) | OK as stated. But see line 247-251: the proof produces $C=2$ via a clean union bound, then claims "A slightly finer analysis (tracking the third-argument $\ECHO$ possibility...) sharpens the factor 2 to a constant $C<3$ that does not depend on $N$; we work with the conservative bound $C=3$ below." This is **backward**: if union bound gives $C=2$ and the "finer analysis" gives a *bigger* constant ($<3$), the finer analysis is *worse*, not sharper. **Either the prose is wrong or the logic is wrong.** Strongly suspect: the factor 2 is the union over two intermediates, but a *third* possibility (re-bracketing on the right) adds a third $\ECHO$ event, giving $3 \times \rho_N \le 3/N$. So the finer analysis loosens the bound from 2 to 3, not the other way around. The text as written is contradictory ("sharpens" but to a worse bound). **Fix:** rewrite line 248-252 as: "Allowing for the third $\ECHO$ possibility (the outer composition $\CL_N(\CL_N(a,b),c)$) yields the conservative bound $C=3$; the union over only the two inner intermediates gives $C=2$, and we work with $C=3$ below for safety. Numerical evidence (§6) suggests the true constant is below 2." |
| 235-242 (Thm 1 proof) | "absorbing element", "any further composition... returns ... on both sides" | proof of associativity on $\ECHO$-free triples | **DEFINED OBJECT** (uses absorbing rules of Def 1) | OK. |
| 240-242 (Thm 1 proof) | "the two bracketings agree, and the triple contributes $0$" | proof step | n/a — typed | OK. |
| 243 (Thm 1 proof) | "We obtain an over-count by observing that every non-associative triple..." | proof step | n/a — typed | OK. |
| 247 (Thm 1 proof) | union bound | typed | n/a | OK. |
| 257-260 (remark) | "$\sigma(10)=0.128$, $\sigma(30)=0.058$..." | numerical | DEFINED OBJECT | OK. |
| 265-277 (Cor 2 statement) | BBM corollary | typed | n/a | The hypothesis "Assume the limiting operator is separable on product states" is an explicit additional assumption, properly flagged. OK. |
| 274 (Cor 2) | $\xi$ (limiting scalar field) | "the limiting scalar field $\xi$" | **STRUCTURAL SHORTHAND** but the limit field $\xi$ is **not constructed** in the paper. The corollary says "extended to a family of nonlinear wave operators via the usual discrete-continuum embedding of finite rings" but no embedding is made explicit. | **Flag.** This is the weakest point of the paper. The phrase "the usual discrete-continuum embedding of finite rings" is hand-wavy — there is no single canonical such embedding from $\ZN$-valued composition tables to scalar wave equations. The authors should EITHER cite a specific embedding from the literature OR explicitly state it as a hypothesis/conjecture rather than as a corollary. **Recommend:** demote Cor 2 to a "Conjecture" or "Heuristic statement" and rewrite the body to make the missing-embedding hypothesis explicit. As a "Corollary" of Theorem 1, it overclaims — Theorem 1 is a finite combinatorial bound and Cor 2 is a continuum-limit field-theory statement; the bridge is non-trivial. |
| 280-287 (Cor 2 proof) | "Matching the scale constants... yields (Eq 5)" | proof step | **DROP** in proof: "matching the scale constants" is undefined in this manuscript. | The proof of Cor 2 is essentially a re-citation of BBM 1976 with a hand-wave. If the corollary stands, the proof needs to make the matching explicit OR cite a specific previous derivation. Otherwise the proof reads as gestural. Tied to the previous flag — recommend demoting Cor 2 entirely. |
| 289-297 (Cor 2 remark) | scope-of-corollary remark | n/a — explicit scope statement | OK; the remark *itself* admits the issue. But best practice would be to demote the corollary and keep this remark as the honest framing. |
| 322-335 (§7 Scope) | enumeration of non-claims | typed | DEFINED OBJECT | Exemplary. |

**TIG-leak scan (sigma rate):** Operator names $\HARM, \VOID, \ECHO$ are TIG-derived (HARMONY, VOID, ECHO from the 10-operator system per memory). They are *operationally defined* in Def 1 so they do rigorous work, but they are also the most visible TIG-framing leak in any of the three papers. **Recommendation:** for journal version, rename to neutral symbols ($T$ for top, $Z$ for zero, $E$ for echo). The rigor doesn't change; the venue-fit risk goes away.

### sigma rate file: counts & DROP backlog

| Classification | Count |
|---|---|
| DEFINED OBJECT | 9 |
| STRUCTURAL SHORTHAND | 5 |
| HEURISTIC/MOTIVATION | 1 |
| DROP | 1 (line 280-287 "matching the scale constants" — undefined in proof of Cor 2) |

**DROP edit backlog:**
1. Lines 134 — remove the sentence "and our $\CL_N$ model gives an elementary family whose ECHO layer forms a reversible Markov chain with an explicit absorbing-state mass" (the chain construction is not in the paper).
2. Lines 188-201 — clean up Lemma 1 to state and prove a single, unambiguous count.
3. Lines 247-252 — fix the contradictory "sharpens to $C<3$" wording in Theorem 1 proof.
4. Lines 265-297 — demote Corollary 2 to a Conjecture/Remark, OR construct the embedding rigorously. As written, the corollary overclaims and the proof gestures. Recommend demotion: the rate theorem stands on its own as a clean combinatorial result.
5. (Venue fit, not rigor:) rename $\HARM, \VOID, \ECHO$ to $T, Z, E$ for *Journal of Combinatorial Theory*.

### sigma rate file: rigor verdict
**Most work needed before Wednesday.** The combinatorial core (Theorem 1) is sound and elegant once Lemma 1 is cleaned up. The continuum corollary (Cor 2) is the soft underbelly — it is a structural advertisement, not a derivation, and the proof admits as much. Either demote it or build the missing bridge. The TIG-named operator macros are the most visible framing leak across all three papers.

---

## Cross-file summary

**Overall rigor health:** The xi cosmology paper sets the standard the other two should meet. Its §7 Scope-and-Limitations section enumerates exactly what the paper does and does *not* claim, with citations and with explicit demotion of the BBM uniqueness theorem from "derivation" to "structural motivation." The other two papers each have a *single dominant rigor gap* that must be closed before Wednesday.

**Cleanest:** `jcap_xi_cosmology.tex`. Zero TIG-framing leaks, no DROP-class words, one minor flag (line 313, "cosmologically relevant range"). **Submit-ready modulo a one-line tightening.**

**Most work needed:** `sigma_rate_theorem.tex`. Five issues: (1) Lemma 1's ambiguous count needs cleanup; (2) Theorem 1 proof has a self-contradictory "sharpens to $C<3$" sentence; (3) Corollary 2 overclaims and its proof gestures; (4) the abstract and intro forward-reference a "reversible Markov chain" construction not in the paper; (5) the TIG-derived macro names ($\HARM, \VOID, \ECHO$) are the most visible framing leak in any of the three submissions. Items (1)-(3) are rigor failures and must be fixed; (4) is a stray sentence to delete; (5) is venue-fit, not rigor.

**Highest-priority single fix across all three:** the `sinc²` paper's TRIVIALITY in Theorem 1 — primality is *vacuous in the biconditional as written*. An *Integers* referee will catch this in one read. Restate the theorem in terms of general $n$, then add a proper corollary that uses primality to derive coprimality of every interior $k$ (which is the actual content primality contributes). Without this fix, the sinc² paper is trivially refutable on submission.

**Brayden's principle applied:** "every word we choose is defined by us rigorously or by previous rigor." The audit found 22 DEFINED OBJECTs (typed and pinned), 16 STRUCTURAL SHORTHAND uses (acceptable when pinned to a formal statement on the same or facing page), 9 HEURISTIC/MOTIVATION uses (acceptable when in remarks, abstracts, introductions — and most are), and 3 DROP-class words across all three papers. The cleanest paper has zero DROPs; the most-impacted paper has one DROP plus four rigor issues. The principle is mostly met; the remaining gaps are concrete and addressable in 2-4 hours of editing per paper.

**Recommendation for Wednesday:**
- **Submit `jcap_xi_cosmology.tex`** after fixing line 313.
- **Submit `sinc2_zero_law.tex`** ONLY after restating Theorem 1 to remove the primality triviality and rewriting the Cor 3 proof. Otherwise hold.
- **Hold `sigma_rate_theorem.tex`** until Lemma 1, Theorem 1's "$C<3$" wording, and Corollary 2's framing are fixed. The combinatorial result is good but the manuscript currently overpromises in the BBM corollary and is internally inconsistent in the constant-$C$ analysis. Consider splitting Cor 2 off as a separate note ("a structural conjecture") so the rate theorem can ship clean.

---

*End of audit. No .tex files were modified.*
