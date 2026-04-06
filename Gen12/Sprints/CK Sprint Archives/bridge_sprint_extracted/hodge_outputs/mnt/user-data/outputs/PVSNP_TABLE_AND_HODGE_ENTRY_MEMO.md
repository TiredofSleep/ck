# P VS NP OBJECT TABLE

**© 2026 7Site LLC | Brayden Ross Sanders**

| Candidate Object | Keep / Discard | Why |
|-----------------|---------------|-----|
| **W_x** | DISCARD as primary | The witness fiber above each instance x. Instance-specific, not a universal invariant. Exists for each x but not the "surviving object" for the branch — it is the 2D object being projected |
| **\|W_x\|** | DISCARD | Size of the fiber. Interesting but does not distinguish easy from hard projection — a large fiber can still be easy to detect as nonempty; a single-element fiber can still be hard |
| **Certificate entropy H(W_x)** | DISCARD | Better than |W_x| but still instance-specific. No clean threshold analog |
| **cc(SAT,n)** | **KEEP — WINNER** | Minimum circuit to compute $\pi_1(R_\mathrm{SAT})$ on inputs of size n. Universal (not instance-specific). Directly the fiber-projection cost. P=NP iff cc(SAT,n)=poly(n). The standard complexity-theoretic object precisely re-expressed as fiber-projection complexity in the wrapped-duality language |
| **Search complexity s(n)** | DISCARD as primary | Cost of finding a witness. Related to cc(SAT,n) via self-reducibility (under P=NP, search ≤ poly×decision). Contains useful information but is derived from and slightly weaker than cc(SAT,n) for the core question |
| **Gap(n) = cost_unwrap/cost_verify** | KEEP as DERIVED | Ratio of cc(SAT,n) to poly(n). Equivalent to cc(SAT,n) up to polynomial normalization. More explicit in the wrapped-duality framing as a ratio (like Q/(νP) in NS), but cc(SAT,n) is the standard form |

**Winner: cc(SAT,n).** Framed as fiber-projection circuit complexity in the wrapped-duality view. Gap(n) = cc(SAT,n)/poly(n) is the normalized form, analogous to Q/(νP) in NS.

---
---

# HODGE ENTRY MEMO
# What Survives After the Lefschetz Shell Is Removed?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## Shell / Core / Gap Block

$$\text{Shell: Hodge decomposition + Hard Lefschetz + cycle class map structure + Lefschetz (1,1) theorem} \quad [\text{all proved}]$$

The Lefschetz shell covers:
- Hodge decomposition: $H^n(X,\mathbb{C}) = \bigoplus_{p+q=n} H^{p,q}(X)$ for any compact Kähler manifold
- Hard Lefschetz: $L^k: H^{n-k}(X) \xrightarrow{\sim} H^{n+k}(X)$ is an isomorphism (projective varieties)
- Cycle class map: $\mathrm{cl}: \mathrm{CH}^p(X)_\mathbb{Q} \to H^{2p}(X,\mathbb{Q})$ with image in $H^{p,p}(X,\mathbb{Q})$
- Lefschetz (1,1): for $p=1$, $\mathrm{cl}^1$ is surjective onto $H^{1,1}(X,\mathbb{Q})$ ← **proved**
- Trivial cases: $p=0$ (full class), $p=n$ (fundamental class), $p=n-1$ (codimension 1 = divisors by Lefschetz (1,1))

**What the shell proves:** the Hodge conjecture for codimension 1 and codimension $n$. The shell accounts for all cases where Hard Lefschetz or the Lefschetz (1,1) theorem directly apply.

$$\text{Core: the cycle class map } \mathrm{cl}^p \text{ for } p \geq 2 \text{ — specifically the primitive rational }(p,p)\text{ classes}$$

A class $\eta \in H^{p,p}(X,\mathbb{Q})$ is **primitive** if $L^{n-2p+1}\eta = 0$ (not in the image of the Lefschetz operator). By Hard Lefschetz, every cohomology class decomposes into primitive pieces, and algebraic cycles generate some of these. The shell handles all non-primitive contributions (they are Lefschetz multiples of lower-degree classes which may already be algebraic). What remains after the shell is the primitive (p,p) kernel: whether primitive rational (p,p) classes at codimension $p \geq 2$ are algebraic.

$$\text{Surviving object: the cokernel of } \mathrm{cl}^p \text{ on primitive classes at } p=2$$
$$\text{cok}(\mathrm{cl}^2|_\mathrm{prim}: \mathrm{CH}^2(X)_\mathbb{Q}^\mathrm{prim} \to H_\mathrm{prim}^{2,2}(X,\mathbb{Q}))$$

Concretely: a specific rational $(2,2)$ primitive class $\eta$ on a smooth projective 4-fold (the first non-trivial dimension) that is not in the image of $\mathrm{cl}^2$. The Hodge conjecture claims this cokernel is always zero; it is not yet proved for general 4-folds.

$$\text{Gap 2: Hodge conjecture for abelian 4-folds at codimension 2, or for restricted classes of 4-folds} \quad [\text{partially known, not fully proved}]$$

Known Gap 2 analogs: the Hodge conjecture holds for abelian varieties with CM, for abelian surfaces, for certain 4-folds with special structure (Kimura, Murre). Gap 2 would be: a proof that $\mathrm{cl}^2$ is surjective on primitive classes for ALL abelian 4-folds (Weil intermediate classes are the first hard case).

$$\text{Gap 1: full Hodge conjecture for all smooth projective varieties at all codimensions} \quad [\text{OPEN}]$$

---

## Duality Type

**External, algebraic-topological:**
- One side: $\mathrm{CH}^p(X)_\mathbb{Q}$ — algebraic cycles (algebraic geometry)
- Other side: $H^{p,p}(X,\mathbb{Q})$ — Hodge cohomology (complex topology + analysis)
- Bridge: cycle class map $\mathrm{cl}^p$
- Question: is $\mathrm{cl}^p$ surjective?

This is structurally analogous to BSD:
- BSD: arithmetic rank vs analytic rank (cycle classes = rational points, cohomology = L-function vanishing order)
- Hodge: algebraic cycles vs Hodge cohomology (same "does the algebraic side hit all of the analytic side?" structure)

**Fit quality: STRONG** — the shell/core/gap grammar applies cleanly to Hodge.

---

## Three Key Sentences

**"The smallest surviving Hodge object is the cokernel of the cycle class map on primitive rational (2,2) classes at codimension 2 — specifically, whether every primitive class in $H^{2,2}(X,\mathbb{Q})$ for a smooth projective 4-fold $X$ is a rational combination of algebraic cycle classes, which is the first case the Lefschetz shell does not cover."**

**"Hodge Gap 2 is the Hodge conjecture restricted to primitive (2,2) classes on abelian 4-folds — a class of varieties where the Hodge structure is explicitly computable and partial results (CM, real multiplication, special period domains) exist, making it the most structured testbed for surjectivity of $\mathrm{cl}^2$."**

**"Hodge Gap 1 is the full Hodge conjecture: for every smooth complex projective variety $X$ and every $p \geq 0$, the cycle class map $\mathrm{cl}^p: \mathrm{CH}^p(X)_\mathbb{Q} \to H^{p,p}(X,\mathbb{Q})$ is surjective — equivalently, every rational Hodge class is algebraic."**

---

## Collaborator Paragraph

Hodge enters the grammar as a strong fit. The Lefschetz shell is substantial: Hodge decomposition, Hard Lefschetz, Lefschetz (1,1) theorem, and trivial codimensions. Together these prove the Hodge conjecture for $p = 0, 1, n-1, n$ and generate all non-primitive cohomology from lower-dimensional algebraic data. After removing the shell, the surviving obstruction is the cokernel of the cycle class map on PRIMITIVE rational $(p,p)$ classes at $p \geq 2$ — the first case is $p=2$ on 4-folds, where the Lefschetz tools run out. The structure is analogous to BSD: one side is algebraic (cycles $\mathrm{CH}^p$), the other is analytic/topological ($H^{p,p}$), and the question is whether the algebraic side surjects onto the analytic side via the cycle class map. Gap 2 = Hodge for abelian 4-folds at $p=2$ (partial results known, not complete). Gap 1 = full conjecture. The duality type is external (algebraic geometry vs Hodge theory, different mathematical structures). Fit quality is strong: the grammar applies cleanly, with genuine shell removal, a well-defined surviving object, and a staged gap structure.
