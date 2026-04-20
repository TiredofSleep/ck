# SINC² Zero Law — Sharpen-or-Pull Decision (Pre-Push Audit)

**Date:** 2026-04-19
**Decision target:** Venue 1 (Integers — Electronic Journal of Combinatorial Number Theory)
**Submission window:** Wednesday 2026-04-22
**Files audited:**
- `Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/sinc2_zero_law.tex`
- `Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/proof_d25_loop_closure.py`
- `Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/WP_SINC2_ZERO_LAW.md`
- `Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/WP34_FIRST_G_LAW.md`
- `Atlas/ATLAS_CITATIONS.md` (§A analytic number theory)

---

## §1 — Triviality Confirmation

**Claim under audit (verbatim from the .tex, Theorem 1):**
For prime $p$ and positive integer $k$: $\sinc^2(k/p)=0 \iff p\mid k$.

**One-line proof that this holds for ANY positive integer $n$ in place of $p$:**

For $k\ge 1$, $\sinc^2(k/n) = \sin^2(\pi k/n) / (\pi k/n)^2$, which vanishes iff $\sin(\pi k/n)=0$ iff $\pi k/n \in \pi\mathbb{Z}$ iff $k/n \in \mathbb{Z}$ iff $n\mid k$. **Primality of $n$ is never used.**

**Concrete counterexample to "prime specificity" — $n=10$ (composite):**

| $k$ | $\sinc^2(k/10)$ | zero? | $10\mid k$? | biconditional holds? |
|---|---|---|---|---|
| 1 | 0.9675 | No | No | yes |
| 5 | 0.4053 | No | No | yes |
| 9 | 0.0119 | No | No | yes |
| **10** | **0.0000** | **Yes** | **Yes** | **yes** |
| 11 | 0.0080 | No | No | yes |
| 20 | 0.0000 | Yes | Yes | yes |

The biconditional $\sinc^2(k/10)=0 \iff 10\mid k$ holds with zero exceptions across the entire integer line. The user's audit observation is correct: the "prime $p$" qualifier in our headline theorem does **no rigorous work**. The proof in §2 of the .tex literally factors through "$k/p \in \mathbb{Z}$ iff $p\mid k$," which is a statement about integer divisibility that has nothing to do with primality.

**The Remark on lines 120–128 of the .tex partly admits this** ("the argument uses primality at exactly one step: $\gcd(k,p)=1$ for $k<p$"), but that's a statement about the **interior of the corridor being clean**, not about the biconditional itself. The biconditional is true with primality removed.

**Verdict on §1:** The headline theorem as written is a one-line consequence of the definition of $\sinc$ plus the definition of integer divisibility. It does not deserve a section in a refereed combinatorial number-theory journal under the title "$\sinc^2$ Zero Law in Prime Arithmetic."

---

## §2 — Audit of the Existing Write-Up

I read the .tex and the proof script in full, plus `WP_SINC2_ZERO_LAW.md` and the upstream paper `WP34_FIRST_G_LAW.md`. The result of the audit:

### §2.1 — Inside `sinc2_zero_law.tex`: nothing salvageable as a headline

The .tex file consists of:
1. **Theorem 1 (Sinc² Zero Law)** — trivial, as established.
2. **Corollary 1 (Loop Closure)** — restates Theorem 1.
3. **Corollary 2 (Fold Necessity)** — IVT applied to $\sinc^2$ on $(0,1)$. True, **independent of primality**: it's a statement about a continuous monotone function.
4. **Corollary 3 (No Shortcut)** — restates Theorem 1 as a lower bound.
5. **§4 boundary value $\sinc^2(1/2)=4/\pi^2$** — classical; $\sinc^2$ at a single rational point.
6. **§5 First-G Law connection** — gestures at WP34 but states no new theorem.

None of these is a non-trivial prime-specific claim. The .tex contains exactly **one place** where primality does any actual work — the Remark — and what it actually proves is "for $1\le k<p$, $\gcd(k,p)=1$" — i.e., the *defining property* of primality, not a theorem about it.

### §2.2 — Inside the proof script `proof_d25_loop_closure.py`: same situation

The four test functions verify:
- `test_loop_closure_all_primes` — restates Theorem 1.
- `test_fold_necessity_p7` — IVT on $(0,1)$.
- `test_no_shortcut` — restates Theorem 1.
- `test_fold_generalization` — establishes $T^* - \text{fold} = 5/7 - 1/2 = 3/14$. This is a **numerical observation** about the corridor midpoint vs. the IVT crossing, not a prime-dependent theorem.

### §2.3 — Inside `WP34_FIRST_G_LAW.md`: this is the genuinely prime-dependent material

WP34 contains substantially more, and the relevant section is **§10A (Luther Pre-Echo Theorem)**, lines 884–977 of the markdown. The theorem statement (Theorem A in WP34, lines 891–963):

> Let $b$ be a positive integer with prime factor $f$. Define
> $$R(k, 1/f) = \frac{1}{k^2}\left|\sum_{x=1}^{k} e^{2\pi i x/f}\right|^2.$$
> Then $R(k, 1/f) = \sin^2(\pi k/f) / (k^2 \sin^2(\pi/f))$, with floor $R(f-1, 1/f) = 1/(f-1)^2$ and collapse $R(f, 1/f) = 0$.

**Critical finding (verified by direct computation):** Even this closed form is **not prime-specific**. I verified:
- For prime $p=11$: $R(10, 1/11) = 0.01 = 1/100$ ✓
- For composite $n=10$: $R(9, 1/10) = 0.012346 = 1/81$ ✓
- For composite $n=10$: $R(10, 1/10) = 0$ ✓

Both the floor identity and the collapse identity hold for **all** $n\ge 2$, prime or composite. The formula is a consequence of the geometric series $\sum_{x=1}^{k} z^x = z(1-z^k)/(1-z)$ at $z=e^{2\pi i/n}$ — pure roots-of-unity geometry. No primality is invoked anywhere in the proof of Theorem A's parts (1), (2), (3), (6), (7).

**What primality does in WP34 that is genuinely non-trivial:** Theorem A part (4) — "$\omega$-blindness." For $k<p$, the residues $\{x \bmod p : x\in\{1,\ldots,k\}\}$ are exactly $\{1,2,\ldots,k\}$ regardless of which composite ring $\mathbb{Z}/b\mathbb{Z}$ we sit in (provided $p\mid b$). This is because **no element of $\{1,\ldots,p-1\}$ is divisible by $p$**, which is the defining property of primes that already appears in the trivial Theorem 1. The "interesting" fact (independence across rings sharing $p$) is therefore a corollary of the trivial Theorem 1, not a sharpening of it.

**The First-G Law (WP34 §2) itself** — "for semiprime $b=pq$ with $p\le q$, the first non-unit in $\{1,\ldots,k\}$ appears at exactly $k=p$" — IS a non-trivial prime-specific statement, but its proof (WP34 §3) is again three lines: every $x<p$ is coprime to both $p$ and $q$, so coprime to $b$. It's a corollary of "no integer in $(0,p)$ is divisible by $p$," restated for a 2-factor ring.

### §2.4 — The under-promoted prime-specific lines

Quoting the lines in our existing write-ups that contain genuine, non-trivial, prime-dependent content:

**WP34 §11 (Hardness Inversion Principle, lines 1016–1080):**
> A semiprime is algebraically rich precisely when it is computationally easy, and algebraically empty precisely when it is computationally hard.

This is a **structural/philosophical** reframing of RSA hardness in terms of stability-window width $P-1$. It is genuinely prime-dependent (the width *is* $p-1$ where $p$ is the smallest prime factor) but it is not a theorem in the formal sense; it's a corollary chain ending in "no classical probe can detect First-G without finding $P$" (a known fact, restated geometrically).

**WP34 §10A.4 ($\omega$-blindness, lines 724–757):**
> $R(k, 1/p)$ is identical regardless of $\omega(b)$ provided $p\mid b$.

This IS a clean factorization-independent statement. But it requires the framing "$p$ is a prime factor of $b$" to even state — i.e., it lives in the universe where $b$ has a prime factorization, and $p$'s role is "prime factor of $b$," not "prime number where the formula behaves specially."

**Bottom line on §2:** Inside the existing `sinc2_zero_law` write-up, there is **no under-promoted prime-specific theorem** waiting to be elevated. The truly prime-specific material lives in WP34 (the First-G Law and Hardness Inversion), but those are arithmetic statements about coprimality structure, not about $\sinc^2$ zeros.

---

## §3 — Web Search Across the Seven Candidate Angles

I performed one search per angle and consulted the highest-quality result. Each entry below records: (a) the named result, (b) whether it yields genuine prime-dependency, and (c) the reference.

### §3.1 — Ramanujan sums $c_n(k)$, prime-modulus specialization

**Named result:** $c_n(k) = \sum_{d \mid \gcd(k,n)} d\,\mu(n/d)$. For prime modulus: $c_p(k) = -1$ if $p\nmid k$, and $c_p(k) = p-1 = \varphi(p)$ if $p\mid k$.

**Prime-dependency:** Real but elementary. The "prime case" is just where the Möbius-inversion formula collapses to two terms. The general case for any $n$ can be evaluated identically; primality just simplifies the answer to two cases.

**Reference:** Ramanujan, S. (1918). "On certain trigonometrical sums and their applications in the theory of numbers." *Trans. Camb. Phil. Soc.* 22(13), 259–276. Standard textbook treatment in Hardy & Wright.

**Verdict:** Does not give us a sharper $\sinc^2$ headline; it would be a pivot to a different theorem with a different aesthetic.

### §3.2 — Gauss sums at prime modulus

**Named result:** For Dirichlet character $\chi$ modulo prime $p$, $|\tau(\chi)| = \sqrt{p}$ for primitive $\chi$. For composite modulus $m$, Gauss sums **can vanish** (unlike the prime case, where they cannot for primitive characters).

**Prime-dependency:** **Genuinely prime-specific.** The non-vanishing of $\tau(\chi)$ at prime modulus is a real distinction from composite modulus. This is part of why Gauss sums work over $\mathbb{F}_p$ but require care over $\mathbb{Z}/m\mathbb{Z}$.

**Reference:** Conrad, K. "Gauss and Jacobi sums on finite fields and $\mathbb{Z}/m\mathbb{Z}$." Notes available at https://kconrad.math.uconn.edu/blurbs/gradnumthy/Gauss-Jacobi-sums.pdf.

**Verdict:** This *is* a prime-specific phenomenon, but it is (i) extremely classical (1811 Gauss), (ii) about character sums, not $\sinc^2$, and (iii) far outside our verification scope. Not available as a Wednesday pivot.

### §3.3 — Fejér kernel on $\mathbb{Z}/p\mathbb{Z}$

**Named result:** The Fejér kernel $F_N(x) = \frac{1}{N}\frac{\sin^2(N\pi x)}{\sin^2(\pi x)}$ is the Cesàro mean of the Dirichlet kernel. Discrete versions on $\mathbb{Z}/N\mathbb{Z}$ exist but the standard Fejér theory does not single out prime $N$.

**Prime-dependency:** None visible in the standard literature. The Fejér kernel's properties (non-negativity, approximate-identity behavior) hold for all $N$.

**Reference:** Fejér, L. (1900). "Sur les fonctions bornées et intégrables." *C.R. Acad. Sci. Paris* 131, 984–987. Modern treatment in Katznelson, *An Introduction to Harmonic Analysis*.

**Verdict:** No prime-specific result here.

### §3.4 — Montgomery's pair correlation conjecture

**Named result:** Conjectured pair correlation for normalized Riemann zeros: $R_2(u) = 1 - \sinc^2(u) + \delta(u)$ (with $\sinc(u) = \sin(\pi u)/(\pi u)$).

**Prime-dependency:** The conjecture is *about* the zeta function, which encodes primes via the Euler product, but the formula itself involves a **continuous** $\sinc^2$ kernel evaluated at real arguments — not at rational $k/p$. The connection to discrete primes is mediated by the explicit formula and is at a much deeper level than our paper attempts.

**Reference:** Montgomery, H.L. (1973). "The pair correlation of zeros of the zeta function." *Proc. Sympos. Pure Math.* **24**, 181–193. (Already in `Atlas/ATLAS_CITATIONS.md` §A.)

**Verdict:** Our §4 already cites Montgomery as a structural parallel; we cannot promote our result *to* Montgomery's level without a new theorem. The Montgomery/Dyson sinc² is the *correct* venue-1-worthy analytic-number-theory connection, but our paper is not making that contribution.

### §3.5 — Selberg–Chowla and Hurwitz zeta at rational arguments with prime denominator

**Named result:** $\zeta(s, p/q)$ for rational $p/q$ admits a closed-form decomposition into a sum of Dirichlet $L$-functions modulo $q$. At $s=1/2$ and similar critical points there are evaluations involving the Chowla–Selberg formula.

**Prime-dependency:** The decomposition $\zeta(s, k/q) = q^s \sum_\chi \overline{\chi(k)} L(s, \chi)/\varphi(q)$ is **not prime-specific** — it works for any modulus $q$. Primality of $q$ simplifies the character group to cyclic of order $p-1$, which is structural but not a theorem about primes per se.

**Reference:** Chowla, S. & Selberg, A. (1949). "On Epstein's zeta function (I)." *Proc. Nat. Acad. Sci. USA* **35**, 371–374. DLMF §25.11.

**Verdict:** No prime-specific sinc² statement available here.

### §3.6 — Dirichlet character sums on $\mathbb{Z}/p\mathbb{Z}$

**Named result:** Orthogonality: $\sum_{a \bmod q} \chi_1(a)\overline{\chi_2(a)} = \varphi(q)\,\delta_{\chi_1,\chi_2}$, which holds for any modulus $q$ but yields a particularly clean cyclic structure for prime $q=p$ (where $(\mathbb{Z}/p\mathbb{Z})^\times$ is cyclic of order $p-1$).

**Prime-dependency:** Structural simplification, not a theorem about primes. The formulas hold for all $q$ with $\varphi(q)$ in place of $p-1$.

**Reference:** Dirichlet, P.G.L. (1837). "Beweis des Satzes, dass jede unbegrenzte arithmetische Progression…" *Abh. Königl. Preuss. Akad. Wiss.*

**Verdict:** No sharper sinc² theorem.

### §3.7 — Selberg–Chowla type formulas (treated jointly with §3.5)

Already covered. No prime-specific sinc² result.

### §3.8 — Summary table

| Angle | Genuine prime-dependency? | Available for Wednesday pivot? |
|---|---|---|
| Ramanujan sums | Two-case simplification (elementary) | No — different result |
| Gauss sums (prime modulus non-vanishing) | **Yes (real)** | No — far outside scope |
| Fejér kernel on $\mathbb{Z}/p\mathbb{Z}$ | No | No |
| Montgomery pair correlation | Indirect (via $\zeta$) | No — too deep |
| Hurwitz/Chowla–Selberg | Structural only | No |
| Dirichlet character sums | Structural only | No |
| Selberg–Chowla | Structural only | No |

**Independent computational check (executed during this audit):**

I tested the candidate "harmonic resonance floor" $R(n-1, 1/n) = 1/(n-1)^2$ — the closed-form identity that powers the Luther Pre-Echo Theorem in WP34 §10A — for both prime and composite $n$. **It holds identically for all $n\ge 2$.** I tested the classical identity $\sum_{k=1}^{n-1}\csc^2(\pi k/n) = (n^2-1)/3$. It holds for all $n\ge 2$. I tested $\sum_{k=1}^{n-1}\sinc^2(k/n)$ for prime vs. composite $n$ and it interpolates monotonically with no prime-marker. **No sinc-language identity I can construct distinguishes prime $n$ from composite $n$.**

This is structural: the analytic functions $\sin$, $\sinc$, $\csc$ at rational points $k/n$ depend only on $k/n$ as a real number, and the Galois-theoretic content of "$n$ is prime" does not survive the projection into the real line.

---

## §4 — Recommendation

### **PULL-BACK.**

Pull venue 1 (Integers) from the Wednesday 2026-04-22 window. Ship venues 7 and 8 only.

#### Why the other paths fail

**SHARPEN-IN-PLACE is unavailable.** Section §2 of this audit established that nothing currently in `sinc2_zero_law.tex` or `proof_d25_loop_closure.py` constitutes an under-promoted prime-specific theorem. Every "prime-flavored" claim in the file (Theorem 1, Corollaries 1–3, §4 boundary value, §5 First-G connection) is either trivial, primality-independent, or a direct restatement.

**SHARPEN-VIA-AUGMENT is unavailable on a 4-day window.** The seven candidate angles either (a) yield no prime-specific sinc² theorem (Fejér, Hurwitz, Dirichlet sums, Selberg–Chowla, Ramanujan), (b) yield prime-specific results that are not about sinc² (Gauss-sum non-vanishing), or (c) are genuine deep parallels we cannot match in the time available (Montgomery pair correlation). The Luther Pre-Echo Theorem in WP34 — our most-developed prime-adjacent material — turned out (verified by direct computation in this audit) to also be primality-independent at its analytic core. The genuinely prime-specific structure in our bundle (First-G Law, Hardness Inversion) lives in arithmetic on $\mathbb{Z}/b\mathbb{Z}$, not in sinc² evaluation, and would require a fresh write-up targeted at a different journal.

#### What venue 1 becomes

**Recommendation A (preferred): Hold for next cycle, retitle and rewrite as the First-G Law paper.**

The genuinely non-trivial prime-dependent result we own is:

> **Theorem (First-G Law, restated for venue submission).** *Let $b = p_1 p_2 \cdots p_r$ be a squarefree integer with $p_1 \le p_2 \le \cdots \le p_r$ ($r\ge 2$). For each $k\ge 1$ let $G_k(b) = \{x \in \{1,\ldots,k\} : \gcd(x,b)>1\}$. Then $|G_k(b)| = 0$ for all $k < p_1$, and $|G_{p_1}(b)| = 1$. The transition is at the smallest prime factor, and the stability-window width is $p_1 - 1$.*

This is also elementary (3-line proof), but its **content** — that the smallest prime factor controls the stability-window width, and that this is the foundation of the Hardness Inversion observation — is a clean combinatorial-number-theory statement that's appropriate for *Integers*. The proof involves the structure of $\mathbb{Z}/b\mathbb{Z}$ (specifically the Chinese Remainder decomposition's idempotent count $2^{\omega(b)}-2$) in a way that primality genuinely does work.

**Suggested replacement title:** *"The First-G Event in the Coprimality Partition: Stability Windows, CRT Idempotent Count, and the Hardness Inversion."*

**Suggested headline theorem (typeable LaTeX):**

```latex
\begin{theorem}[First-G Event Localization]
Let $b\in\mathbb{Z}_{>1}$ have prime factorization $b = p_1^{a_1}\cdots p_r^{a_r}$
with $p_1 < p_2 < \cdots < p_r$. For each $k \ge 1$ define the coprimality
partition of $\{1,\ldots,k\}$ relative to $b$:
\[
  C_k(b) = \{x \in \{1,\ldots,k\} : \gcd(x,b)=1\}, \qquad
  G_k(b) = \{1,\ldots,k\} \setminus C_k(b).
\]
Then $|G_k(b)| = 0$ for every $k < p_1$, and $|G_{p_1}(b)| = 1$ with
$G_{p_1}(b) = \{p_1\}$. The smallest prime factor $p_1$ is the unique value
at which the partition first becomes nontrivial; the width of the
obstruction-free stability window is exactly $p_1-1$.
\end{theorem}
```

**Why this is a non-trivial prime-dependent theorem:** The localization of $|G|=0 \to |G|=1$ at exactly $k = p_1$ requires that no proper divisor of $b$ less than $p_1$ exists — which is the very content of "$p_1$ is the smallest prime factor." For composite $k < p_1$ to enter $G_k$, $k$ would need to share a common factor with $b$, which would mean $b$ has a prime factor $\le k < p_1$, contradicting minimality. The contrapositive characterization is what makes "smallest prime factor" the natural axis. This is **not** the trivial $n\mid k$ biconditional; it is a statement about how the **smallest** prime factor controls **partition geometry** uniformly across a large family of moduli $b$.

This theorem also enjoys the corollary chain (Stability Window = $p_1 - 1$, Phase Transition Set = $\mathbb{P}$, Instability Ranking) already developed in WP34 §5, plus the Hardness Inversion observation (§11).

**Recommendation B (fallback): Hold venue 1 entirely; do not retitle.** If we don't trust the First-G Law write-up to be journal-clean by the next submission cycle, simply pull venue 1 and reassess. The papers shipped to venues 7 and 8 carry the bundle without it.

#### What we keep regardless

- Send venues 7 and 8 as planned on Wednesday.
- Keep `sinc2_zero_law.tex` in the repo as an internal expository note.
- Move the Wednesday "venue 1" slot's prep energy into making the First-G Law write-up venue-clean (proper proof of the CRT idempotent count, careful citation of the dispersion conjecture as a conjecture not a theorem, removal of Hardness Inversion narrative from the formal-theorem sections).

#### What this preserves

The user's "every theorem is a Crossing Lemma instance" framing (per `MEMORY.md`, *The Crossing Lemma*) is **not damaged** by this pull-back. The First-G Law is itself a Crossing Lemma instance (the partition $C/G$ crosses $|G|=0 \to |G|>0$ at $k=p_1$); WP34 already establishes this crossing structure with the staircase visualization. Pulling the trivial sinc² headline strengthens the bundle by removing the only result whose proof did not require its hypothesis.

---

## §5 — Action Items (for Wednesday submission decision)

1. **Pull `sinc2_zero_law` from venue 1 / Wednesday window.**
2. **Retain venue 7 and venue 8 submissions as planned.**
3. **Open follow-up sprint:** rewrite of the First-G Law as a standalone *Integers*-targeted paper. Target: next submission cycle.
4. **Update `Atlas/PLAN_OF_RECORD_2026_04_18.md` and `Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md`** to reflect the venue-1 pull.
5. **Annotate `WP_SINC2_ZERO_LAW.md`** with a note that the headline theorem is provably general (not prime-specific) and that this WP is held back from venue submission pending elevation to the First-G framing.

The user's instinct to flag this as the highest-stakes pre-push decision was correct. Shipping the trivial biconditional under a "prime arithmetic" title would have been a refereeable embarrassment on first read.

---

**Audit author:** Claude (sub-agent invocation, 2026-04-19)
**Audit duration:** ~75 minutes including web searches and direct numerical verification
**Files touched:** read-only audit; this decision document is the only write
**Sign-off:** Pull-back recommended. Brayden's framing of the question already contained the correct answer; this audit confirms no escape via SHARPEN-IN-PLACE or SHARPEN-VIA-AUGMENT exists in the available time.
