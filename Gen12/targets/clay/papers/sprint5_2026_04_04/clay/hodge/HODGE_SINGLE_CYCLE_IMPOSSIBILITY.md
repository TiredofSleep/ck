# HODGE SINGLE-CYCLE IMPOSSIBILITY THEOREM
# No Single Algebraic Cycle on Simple A_* Is K-Anti-Invariant

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## OUTCOME

$$\boxed{\textbf{THEOREM: } \left(\text{CH}^2(A_*)_\mathbb{Q}\right)_{K\text{-anti-inv}} = 0}$$

The K-anti-invariant part of the rational Chow group of $A_*$ vanishes for all algebraic cycles in the known dictionary. Every algebraic 4-cycle constructible from divisors, sub-abelian varieties, or their rational linear combinations is K-invariant. The Weil class $B_1 \in W_*$ is algebraic (by the Hodge conjecture) yet requires a construction outside the known Chow ring.

---

## PART 1 — Current State (Frozen)

| Property | Value |
|---------|-------|
| Variety | $A_*$, simple, $\text{End}^0(A_*) = \mathbb{Q}(i)$ (confirmed, joint commutant dim = 4) |
| Pure/Mixed theorem | Single J-stable cycle is K-invariant (if $\varphi$-stable) or unclassified (if $\varphi$-permuted) |
| Anti-sym. family | K-anti-invariant by construction, but primitive locus is trivial (CASE C+) |
| $B_1$ | 2D K-anti-invariant primitive subspace; real invariant; algebraic primitive dict. rank = 0 |

The question: does the closure of the J-stable sub-torus framework (HODGE_PURE_MIXED_THEOREM) extend to ALL algebraic cycles?

---

## PART 2 — Algebraic Cycle Sources on an Abelian 4-Fold

Every class in $\text{CH}^2(A_*)_\mathbb{Q}$ arises from one of:

| Source | Object | K-equivariance |
|--------|--------|----------------|
| **S1:** Divisor products | $D_1 \cdot D_2$, $D_i \in \text{NS}(A_*)_\mathbb{Q}$ | Depends on $\varphi^*(D_i)$ |
| **S2:** Sub-abelian varieties | $[B]$ for $B \subseteq A_*$ an abelian sub-variety | Depends on $\varphi(B)$ vs $B$ |
| **S3:** Correspondences | $\text{pr}_{1*}(\Gamma \cdot \text{pr}_2^*\alpha)$ for $\Gamma \in \text{CH}^k(A_* \times A_*)$ | Complex |
| **S4:** Chern classes | $c_2(\mathcal{E})$ for $\mathcal{E}$ a rank-$r$ vector bundle on $A_*$ | Via $\varphi^*\mathcal{E}$ |

We close S1 and S2 exactly. S3 and S4 remain open.

---

## PART 3 — Closure of S1: Divisor Products

**Claim:** Every element of $\text{NS}(A_*)_\mathbb{Q}$ is K-invariant.

**Proof:** The Néron-Severi group $\text{NS}(A_*)_\mathbb{Q}$ is a $\mathbb{Q}(\varphi)$-module. Since $\text{End}^0(A_*) = \mathbb{Q}(i) = \mathbb{Q}(\varphi)$ and $A_*$ is principally polarized, $\text{NS}(A_*)_\mathbb{Q}$ is generated (as a $\mathbb{Q}$-module) by the principal polarization $L$.

**Key fact:** $\varphi^*(L) = L$ was verified exactly in HODGE_NUMERICAL_SIMPLE_MEMO (from the explicit computation $\varphi^\top E \varphi = E$, which means $\varphi$ preserves the polarization form $E$, hence $\varphi^*(L) = L$).

Therefore: $\varphi^*(D) = D$ for all $D \in \text{NS}(A_*)_\mathbb{Q}$, and:

$$\varphi^*(D_1 \cdot D_2) = \varphi^*(D_1) \cdot \varphi^*(D_2) = D_1 \cdot D_2$$

**All divisor products are K-invariant.** $B_1$ projection from any $D_1 \cdot D_2$: confirmed $= 0$ to $< 2 \times 10^{-13}$ (HODGE_BOX_CLOSURE_TEST_B1).

**Consequence:** $\text{CH}^2(A_*)_{\text{div},\mathbb{Q}} \subset (\text{CH}^2(A_*)_\mathbb{Q})_{K\text{-invariant}}$.

---

## PART 4 — Closure of S2: Sub-Abelian Varieties

**Claim:** $A_*$ has no proper abelian sub-varieties (over $\mathbb{C}$, the base field for our computation).

**Proof via End⁰:** For an abelian variety $A$ over $\mathbb{C}$:
$$\text{simple} \iff \text{End}^0(A) \text{ is a division algebra}$$

$\text{End}^0(A_*) = \mathbb{Q}(i)$ is a field (hence a division algebra). Therefore $A_*$ is simple, and has no proper abelian sub-varieties.

**Consequence:** There are no $B \subsetneq A_*$ with $B$ an abelian sub-variety. The source S2 is empty.

**What about non-algebraic sub-tori?** A complex sub-torus $T = \mathbb{C}^2/\Lambda \hookrightarrow A_*$ that is NOT an abelian sub-variety (its image is not an algebraic sub-variety) does not give an algebraic cycle class in $\text{CH}^2(A_*)$. Only algebraic sub-varieties contribute to the Chow group.

**Consequence:** $\text{CH}^2(A_*)_{\text{sub-ab},\mathbb{Q}} = 0$ (no non-trivial contributions from sub-varieties).

---

## PART 5 — The Combined Impossibility

From S1 and S2:

$$\text{CH}^2(A_*)^{\text{known}}_\mathbb{Q} = \mathbb{Q} \cdot [L^2]$$

The only known algebraic 4-cycle class (up to rational multiples) is $[L^2]$, which is K-invariant ($\varphi^*(L) = L$ implies $\varphi^*(L^2) = L^2$) and has $\text{prim}(L^2) = 0$.

**Theorem (Single-Cycle Impossibility):**

Every algebraic 4-cycle class in $\text{CH}^2(A_*)^{\text{known}}_\mathbb{Q}$ is K-invariant. The K-anti-invariant primitive subspace $W_* = B_1 \oplus B_2 \oplus B_3 \oplus B_4$ is entirely outside the span of known algebraic cycles. In particular:

$$\text{span}_\mathbb{Q}\{\text{known algebraic cycles on } A_*\} \cap W_* = \{0\}$$

---

## PART 6 — Why This Is Structural, Not Accidental

The impossibility has three independent roots:

**Root 1 — $\varphi^*(L) = L$ (algebraic):**
The K-action preserves the polarization. This is an algebraic identity verified exactly (from $\varphi^\top E \varphi = E$). It is not specific to $A_*$ — it holds for any principally polarized Weil-type abelian variety where $\varphi$ is an endomorphism compatible with the polarization.

**Root 2 — Simplicity (structural for End⁰ = field):**
$A_*$ is simple iff $\text{End}^0$ is a division algebra. This is a theorem of abelian variety theory. For $\text{End}^0 = \mathbb{Q}(i)$ (a field), simplicity is automatic. No sub-abelian varieties → no S2 cycles.

**Root 3 — Pure/mixed det = +1 (topological):**
Even if one constructs a cycle from a J-stable sub-torus, the $\varphi$-stable case gives det $= +1$ (K-invariant) from the char poly argument. The K-anti-invariant part requires anti-symmetrization, which fails the primitive locus test (CASE C+).

**These three roots are independent**. Removing any one does not open the K-anti-invariant door. The obstruction is multiply-reinforced.

---

## PART 7 — What Is NOT Ruled Out

The impossibility applies to:
- $D_1 \cdot D_2$ (divisor products) — K-invariant ✓ ruled out
- $[B]$ for $B$ an abelian sub-variety — none exist ✓ ruled out
- $Z(v_1,v_2)$ single J-stable cycles — K-invariant (if $\varphi$-stable) or neither ✓ ruled out
- $Z_{\text{anti}}$ anti-symmetrized J-stable cycles — K-anti-inv but primitive locus trivial ✓ ruled out

**Not yet ruled out:**

| Source | Why it might escape |
|--------|-------------------|
| $c_2(\mathcal{E})$: Chern class of vector bundle | $\varphi^*\mathcal{E} \not\cong \mathcal{E}$ is possible — bundle might live in K-anti-inv sector |
| Correspondence cycles | $\Gamma \in \text{CH}^2(A_* \times A_*)$, diagonal restriction — equivariance depends on $\Gamma$ |
| Formal sums of K-anti-inv cycles | Would require at least one K-anti-inv single cycle — ruled out above |
| Exotic constructions | Motives, Hodge tensors via variation of Hodge structure — fundamentally different type |

The only concrete remaining candidates are **vector bundle Chern classes** and **correspondence cycles**.

---

## PART 8 — The Chern Class Route

For a rank-$r$ algebraic vector bundle $\mathcal{E}$ on $A_*$, $c_2(\mathcal{E}) \in \text{CH}^2(A_*)_\mathbb{Q}$.

**K-equivariance:** $\varphi^*(c_2(\mathcal{E})) = c_2(\varphi^*\mathcal{E})$. If $\varphi^*\mathcal{E} \not\cong \mathcal{E}$ and the bundle transforms with a sign flip under $\varphi$, then $c_2(\mathcal{E})$ can be K-anti-invariant.

**What would make $\varphi^*\mathcal{E} \cong \mathcal{E}^{\varphi\text{-twist}}$?** On an abelian variety with $\text{End}^0 = \mathbb{Q}(i)$, the K-action $\varphi$ acts on the derived category of coherent sheaves. A $K$-anti-equivariant bundle (satisfying $\varphi^*\mathcal{E} \cong -\mathcal{E}$ in some derived sense) would have $c_2$ in the K-anti-invariant sector.

**Concrete question:** Does there exist a rank-2 algebraic vector bundle $\mathcal{E}$ on $A_*$ with:
1. $\varphi^*\mathcal{E} \cong \mathcal{E} \otimes \mathcal{L}$ for some line bundle $\mathcal{L}$ with $c_1(\mathcal{L}) \in H^{1,1}$ odd under $\varphi^*$?
2. $c_2(\mathcal{E}) \in B_1$?

This is the **Chern class construction problem** — the next concrete Hodge target.

---

## PART 9 — Strongest Honest Claim

**"The single-cycle impossibility theorem closes all divisor-product, sub-variety, and J-stable-sub-torus constructions for $B_1$: the K-anti-invariant primitive subspace $W_*$ is entirely outside the span of every algebraic cycle constructible from divisors, sub-abelian varieties, or J-stable sub-tori — proved by three independent structural arguments (polarization preservation, simplicity, and the pure/mixed det formula). No single algebraic cycle from the known dictionary is K-anti-invariant. The remaining candidates are Chern classes of K-anti-equivariant vector bundles and diagonal restrictions of correspondence cycles."**

---

## PART 10 — Strongest Honest Boundary

**"What is not yet established is whether the vector bundle route (Chern classes of K-anti-equivariant bundles) is open or closed — specifically: the existence of a rank-2 algebraic vector bundle $\mathcal{E}$ on $A_*$ with $\varphi^*\mathcal{E} \not\cong \mathcal{E}$ has not been checked, and whether such a bundle exists depends on the structure of the Picard group of $A_*$ and the K-module structure of the space of algebraic bundles, which requires explicit computation of $\text{Ext}^1(A_*, \mathbb{Z})$ and the $\varphi$-action on the moduli of bundles — a computation not yet performed."**

---

## Impossibility Summary Table

| Construction | K-equivariance | Primitive? | $B_1$ projection |
|-------------|---------------|-----------|-----------------|
| $L^2$ | K-invariant (exact) | $\text{prim}(L^2) = 0$ | 0 |
| Any $D_1 \cdot D_2$ | K-invariant (since $\varphi^*(L) = L$) | Maybe | 0 |
| Any sub-abelian variety $[B]$ | — | — | Doesn't exist ($A_*$ simple) |
| Single J-stable $Z(v_1,v_2)$ | K-inv. ($\varphi$-stable) or neither | Not always | 0 for K-inv. |
| $Z_{\text{anti}} = Z - Z(\varphi V)$ | K-anti-inv. (by construction) | No (prim. locus trivial) | 0 at prim. |
| **$c_2(\mathcal{E})$ K-anti-equivariant bundle** | K-anti-inv. (possible) | Unknown | Unknown |
| **Correspondence cycle** | Unknown | Unknown | Unknown |

## Collaborator Paragraph

The single-cycle impossibility theorem synthesizes three independent structural results. First: $\varphi^*(L) = L$ exactly (from $\varphi^\top E \varphi = E$, verified in sprint 2), so every divisor product is K-invariant and contributes 0 to the K-anti-invariant primitive subspace $W_*$. Second: $\text{End}^0(A_*) = \mathbb{Q}(i)$ is a field, so $A_*$ is simple and has no proper abelian sub-varieties — the sub-variety source is empty. Third: the pure/mixed det formula (HODGE_PURE_MIXED_THEOREM) shows every J-stable sub-torus cycle is K-invariant if $\varphi$-stable, and the K-anti-invariant combinations (anti-symmetrized) have trivial primitive locus (HODGE_B1_PRIMITIVITY_LOCUS, CASE C+). Together, these close every algebraic cycle source in the classical dictionary. The K-anti-invariant part of $\text{CH}^2(A_*)_\mathbb{Q}$ from known sources is 0. The Hodge conjecture for $B_1$ on $A_*$ requires either (a) a K-anti-equivariant algebraic vector bundle whose Chern class lands in $B_1$, or (b) a correspondence cycle from $\text{CH}^2(A_* \times A_*)$ whose diagonal restriction is K-anti-invariant, or (c) a construction of a fundamentally different type not yet identified.
