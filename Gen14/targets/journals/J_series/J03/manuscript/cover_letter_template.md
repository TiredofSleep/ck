# Cover Letter — *Integers* (Sprint 35 replacement for venue 1)

**Manuscript:** *The First-G Event in the Coprimality Partition: Stability Windows, CRT Idempotent Count, and Prime-Indexed Phase Transitions*
**Authors:** B. R. Sanders, C. A. Luther, M. Gish
**Target:** *Integers — Electronic Journal of Combinatorial Number Theory*
**Backup:** *Journal of Combinatorial Theory, Series A* (JCT-A), short-paper track; *Discrete Mathematics*
**DOI of bundle:** 10.5281/zenodo.18852047
**Target submission date:** 2026-04-29 (or 2026-05-06 if style-file polish runs long)

---

Dear Editor,

We submit for your consideration *The First-G Event in the Coprimality Partition: Stability Windows, CRT Idempotent Count, and Prime-Indexed Phase Transitions*, a short combinatorial-number-theory note that localizes, in alphabet-size coordinates, the first mark made by the sieve of Eratosthenes.

For an integer $b > 1$ and a growing alphabet $\{1, \ldots, k\}$, the coprimality partition splits the alphabet into units $C_k(b) = \{x : \gcd(x,b)=1\}$ and obstructions $G_k(b) = \{1,\ldots,k\} \setminus C_k(b)$. The main theorem identifies the smallest $k$ at which $G_k(b)$ becomes non-empty: it is exactly $p_1 = \mathrm{spf}(b)$, and $G_{p_1}(b) = \{p_1\}$. The proof is a three-line elementary argument. Four corollaries follow: (i) stability-window width $p_1 - 1$ uniform across all $b$ with fixed $\mathrm{spf}(b) = p_1$; (ii) phase-transition set equal to $\mathbb{P}$; (iii) terminal obstruction count $|G_b(b)| = b - \varphi(b)$ via the Chinese Remainder Theorem; (iv) instability ranking of primes by stability-window width.

The statement and its corollaries sit inside the classical sieve; what the paper contributes is the packaging, which organizes sieve activation around the alphabet-size coordinate $k$ rather than around $b$ or the range of interest $[1, n]$. This repackaging has proved productive in a sequence of companion papers (WP34, WP35, WP101) on the dynamics of composition-table operations over $\mathbb{Z}/b\mathbb{Z}$; the present note isolates the foundational lemma so it can be cited cleanly by that program.

The theorem is verified exhaustively for every squarefree $b$ in $[2, 500]$ (305 $b$ values; 22,367 $(b,k)$ pairs; zero counterexamples; runtime under 3 seconds) by the accompanying script `proof_first_g_event.py`. We have been careful in §7 "Scope and limitations" to list what the paper does not claim: no analytic-number-theory density estimates, no $\pi(\sqrt{b}) \pm o(\cdot)$ statements, no claim about non-squarefree $b$ beyond what the theorem already covers, and no connection to the Riemann $\zeta$ function beyond the Shannon–Montgomery sinc² parallel noted in §6.

We believe this is a good fit for *Integers* as a short combinatorial note: the statement is elementary, the proof is elementary, the verification is exhaustive on the natural finite range, and the corollary structure is clean enough to support the broader program cited above. If the editors consider the length insufficient for the regular track, we would be equally happy to have it considered for the short-paper track.

Supplementary materials: `proof_first_g_event.py` (verification script), `README.md` (sprint context), `SHIP_DECISION.md` (submission checklist). DOI 10.5281/zenodo.18852047. Original work; no conflicts; not under review elsewhere.

Thank you for your time.

— on behalf of the authors,
Brayden Ross Sanders · brayden@7site.co · 7Site LLC

---

*Template length: ~410 words. Prepared 2026-04-19 under Sprint 35 of the TIG/CK research program (7Site LLC). Scope paragraph in §4 ("What this paper does not claim") is load-bearing; keep unchanged. Adjust editor address at submission time — the *Integers* managing editor listing is maintained at www.integers-ejcnt.org.*
