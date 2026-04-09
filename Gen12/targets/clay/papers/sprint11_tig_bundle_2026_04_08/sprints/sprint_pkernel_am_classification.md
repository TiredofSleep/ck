# SPRINT: p-KERNEL A+M CLASSIFICATION FOR PRIME POWERS
*UOP / map language. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Setup: Additive Partitions and p-Kernel Filtration

**System.** Z/p^rZ for prime p and r ≥ 2. Elements {0,1,...,p^r−1}.

**p-adic valuation.** For x ∈ Z/p^rZ: v_p(x) = largest k with p^k | x. Set v_p(0) = r (convention).

**Definition 1 (Level-a additive partition).**
For 1 ≤ a ≤ r:

π_{p^a}: x ~_{p^a} y iff p^a | (x−y) iff x ≡ y mod p^a

Block of x: x + p^a·Z/p^rZ = {x, x+p^a, x+2p^a, ..., x+(p^{r−a}−1)p^a}. Block size = p^{r−a}. Block count = p^a.

**Chain of additive partitions (proved):**
π_triv ≥ π_p ≥ π_{p²} ≥ ... ≥ π_{p^r} = π_disc

Each step: π_{p^a} ≥ π_{p^{a+1}} (coarser to finer). Every pair is comparable. No two additive partitions of Z/p^rZ are incompatible.

**Consequence.** No sufficient 2-partition family exists within the Type-A family alone for Z/p^rZ: meet of any two additive partitions = the finer one = π_{p^{\max(a₁,a₂)}} ≠ π_disc unless max(a₁,a₂) = r, which means one partition is already π_disc.

---

**Definition 2 (p-kernel filtration).**
For 0 ≤ b ≤ r−1: define the level-b kernel subgroup of (Z/p^rZ)*:

K_b = ker( (Z/p^rZ)* → (Z/p^{b+1}Z)* ) = { x ∈ (Z/p^rZ)* : x ≡ 1 mod p^{b+1} }

Properties:
- K_0 = ker(→ (Z/pZ)*) = { x : x ≡ 1 mod p } = S_p from prior sprint. |K_0| = p^{r−1}.
- K_b ⊃ K_{b+1}: each is a subgroup of the next.
- K_{r−1} = {1}: trivial.
- K_b / K_{b+1} ≅ Z/pZ for each b = 0,...,r−2.
- (Z/p^rZ)* / K_0 ≅ (Z/pZ)* ≅ Z/(p−1)Z.
- Full filtration: (Z/p^rZ)* ⊃ K_0 ⊃ K_1 ⊃ ... ⊃ K_{r−1} = {1}.

This is the p-adic filtration of the unit group. K_b consists of elements that look like 1 in the first b+1 p-adic digits.

For odd prime p: (Z/p^rZ)* ≅ Z/p^{r−1}Z × Z/(p−1)Z (decomposition as cyclic × cyclic, with K_0 ≅ Z/p^{r−1}Z being the p-primary part).

---

**Definition 3 (Action level of a subgroup G on Z/p^rZ).**

G ≤ (Z/p^rZ)*. The *action level* of G is the largest integer ℓ(G) ≥ 0 such that G contains an element NOT in K_{ℓ(G)−1}. Equivalently:

ℓ(G) = min{ b : G ∩ K_b = G ∩ K_{b+1} } = the smallest b at which G stabilizes in the filtration.

Or equivalently: ℓ(G) = max{ b : G ⊄ K_{b−1} } (the deepest level where G is not yet confined).

The key quantity: v_p(ord(G)) — the p-adic valuation of |G|.

**For G with |G| = p^s · m (gcd(p,m)=1):**
G ∩ K_0 has order p^s (the p-Sylow part of G). The Sylow p-subgroup of G is a subgroup of K_0 ≅ Z/p^{r−1}Z, hence cyclic of order p^s (s ≤ r−1).

---

## Part 2 — The A+M Injectivity Condition

**Joint map.** J = (f_{p^a}, f_G): Z/p^rZ → Z/p^aZ × G-orbit-space.

**J-injectivity failure.** Pair {x, g·x} with g ∈ G, g ≠ 1, and f_{p^a}(x) = f_{p^a}(g·x), i.e., x ≡ g·x mod p^a, i.e., p^a | (g−1)·x.

**Condition:** p^a | (g−1)·x.

Write v_p(g−1) = c (g ≡ 1 mod p^c but g ≢ 1 mod p^{c+1}; c ∈ {0,...,r−1} for g ≠ 1; c = r means g = 1 trivially). Note: g ≡ 1 mod p^c exactly when g ∈ K_{c−1} \ K_c (using K_{−1} = (Z/p^rZ)* convention).

Then v_p((g−1)·x) = v_p(g−1) + v_p(x) = c + v_p(x).

The condition p^a | (g−1)·x becomes: c + v_p(x) ≥ a, i.e., v_p(x) ≥ a − c.

**Conflict pair exists iff:** ∃g ∈ G with g ≠ 1 and v_p(g−1) = c, and ∃x ≠ 0 with v_p(x) = a−c (or v_p(x) ≥ a−c and g·x ≠ x in Z/p^rZ). Specifically: if a − c ≤ r−1 (i.e., a − c is a valid valuation level), choose x = p^{a−c}. Then v_p(x) = a−c, so v_p((g−1)x) = c + (a−c) = a. Check g·x ≠ x: g·x − x = (g−1)·x, v_p((g−1)x) = a, so (g−1)x ≡ 0 mod p^a but ≢ 0 mod p^{a+1} (if c < r and a−c < r). So g·x ≡ x mod p^a (same π_{p^a} class) but g·x ≠ x (since v_p(g·x − x) = a < r). Conflict.

**Condition for NO conflict:** For every g ∈ G, g ≠ 1: no x ∈ Z/p^rZ with x ≠ 0 satisfies v_p(x) ≥ a − v_p(g−1) while also g·x ≠ x.

Let c = v_p(g−1). Conflict iff a − c ≤ r − 1 and x = p^{a−c} is a valid element with g·p^{a−c} ≠ p^{a−c}. The second condition: g·p^{a−c} − p^{a−c} = (g−1)·p^{a−c}, v_p = c+(a−c) = a < r, so yes, g·p^{a−c} ≠ p^{a−c} (since the difference has valuation a < r, hence is non-zero in Z/p^rZ).

This conflict is avoided only if: for all g ≠ 1 in G: v_p(g−1) < a − (r−1) = a − r + 1, i.e., v_p(g−1) ≤ a − r. But v_p(g−1) ≥ 0 always. So this requires a − r ≥ 0, i.e., a ≥ r. But a ≤ r, so a = r — meaning π_{p^r} = π_disc. Trivial.

**Intermediate conclusion:** For any 1 ≤ a ≤ r−1 (non-discrete additive partition) and any non-trivial G: there ALWAYS exists a conflict via the p-kernel mechanism, UNLESS the specific element x = p^{a−c} does not exist in Z/p^rZ or g fixes it.

**Correction to the intermediate conclusion:** g·p^{a−c} = g·p^{a−c} mod p^r. Since g is a unit (gcd(g,p)=1), and p^{a−c} is not a unit (for a−c ≥ 1), we need to verify g·p^{a−c} ≢ p^{a−c} mod p^{a+1}. We have: g ≡ 1 + t·p^c mod p^{c+1} with p ∤ t (since v_p(g−1) = c exactly). Then g·p^{a−c} ≡ (1+tp^c)·p^{a−c} = p^{a−c} + tp^a mod p^{a+1}. So g·p^{a−c} − p^{a−c} ≡ tp^a mod p^{a+1} with p ∤ t. Hence g·p^{a−c} ≢ p^{a−c} mod p^{a+1}, but both ≡ p^{a−c} mod p^a. ✓ Confirmed conflict.

---

## Part 3 — Main Theorem for p^r

**Theorem 1 (p-Kernel A+M Obstruction — proved).**

For n = p^r, 1 ≤ a ≤ r−1, and G ≤ (Z/p^rZ)*:

**{π_{p^a}, π_DYN(G)} is sufficient iff G = {1}.**

*That is: no non-trivial A+M sufficient pair exists for Z/p^rZ over any non-discrete additive partition.*

**Proof.**

Let G ≠ {1}. Pick any non-identity g ∈ G. Let c = v_p(g−1) ∈ {0,...,r−1}.

Set x = p^{max(a−c, 0)} · u for any unit u (to make x non-zero). Optimally take the simplest case:

**Sub-case c ≥ a:** Then v_p(g−1) = c ≥ a, so v_p((g−1)·1) = c ≥ a, so p^a | (g−1)·1, meaning g·1 ≡ 1 mod p^a. But g is a unit so g·1 = g ≡ 1 mod p^a. Meanwhile g ≠ 1 in Z/p^rZ. So the pair {1, g}: 1 ≡ g mod p^a (same π_{p^a} class) AND both in the same G-orbit. Conflict.

**Sub-case c < a:** Take x = p^{a−c}. Then x ≠ 0 (since a−c < r) and v_p(x) = a−c.
g·x − x = (g−1)·p^{a−c}. v_p((g−1)·p^{a−c}) = c + (a−c) = a.
So g·x ≡ x mod p^a but g·x ≢ x mod p^{a+1} (since v_p(g·x−x) = a). g·x ≠ x. The pair {x, g·x}: same π_{p^a} class, same G-orbit. Conflict.

In both sub-cases, a conflict exists. Therefore G ≠ {1} implies not sufficient. □

**Corollary.** For n = p^r (single prime power), the only sufficient A+M pair is {π_disc, π} for any π — trivial. Every non-trivial A+M 2-partition family for n = p^r is insufficient.

---

## Part 4 — Sharp Threshold: Which a Relative to r?

The impossibility of Theorem 1 holds for ALL 1 ≤ a ≤ r−1 regardless of the relationship between a and r. There is no threshold.

**Why no threshold exists:** The proof uses only that a−c ≥ 0 (for sub-case c < a) or c ≥ a (for sub-case c ≥ a). One of these always holds. The key is that for any non-trivial G, some element g has some c = v_p(g−1) ∈ {0,...,r−1}, and that c is always either ≥ a or < a. Both cases yield a conflict.

**The clean way to see it.** For Z/p^rZ, the ONLY additive partition with no conflict against any non-trivial G is π_disc. The chain π_p ≥ π_{p²} ≥ ... ≥ π_{p^{r−1}} all fail. There is no "sufficiently fine" non-discrete additive partition that pairs with a non-trivial G.

**Comparison to squarefree.** For squarefree n = p₁···pₖ and d = p₁···pⱼ (j < k): π_d is not discrete, but the orbit partition of G focused on primes {p₁,...,pⱼ} does not act on the {p_{j+1},...,pₖ} fiber. There, elements with aᵢ = 0 for pᵢ | d are in different mod-d residues from each other — actually wait, multiples of d form one residue class. So the "zero fiber" of π_d is {x : p₁ | x and p₂ | x ...and pⱼ | x} = {multiples of d}. In squarefree n, within this zero fiber, distinct elements still differ in at least one prime coordinate among {p_{j+1},...,pₖ}. G focused on {p₁,...,pⱼ} fixes all these coordinates (acts trivially on them), hence SEPARATES elements within the zero fiber. This is exactly what makes squarefree work: within-fiber separation is free.

In Z/p^rZ: within each π_{p^a} fiber, elements differ only in higher p-adic digits. G acting on Z/p^rZ as a unit group cannot "ignore" higher p-adic digits without ignoring the entire action. There is no analog of "focused generator" for the single-prime case — all generators affect the same variable.

---

## Part 5 — Concrete Cases

### n = 9 = 3²

Additive partitions: π_3 (3 blocks of size 3: {0,3,6},{1,4,7},{2,5,8}) and π_9 = π_disc.

**{π_3, π_DYN(G)}: never sufficient for G ≠ {1} (Theorem 1).**

Verify g=2 (primitive root, order 6):
- c = v_3(2−1) = v_3(1) = 0. Sub-case c < a=1. x = 3^{1−0} = 3. g·3 = 6. 3 ≡ 6 mod 3? Yes (both ≡ 0 mod 3). Same π_3 class. 3 ≠ 6. Conflict ✓.

Verify g=4 (order 3, g ∈ K_0 = {1,4,7}):
- c = v_3(4−1) = v_3(3) = 1 = a. Sub-case c ≥ a. g·1 = 4. 1 ≡ 4 mod 3? Yes (both ≡ 1 mod 3). Same π_3 class. 1 ≠ 4. Conflict ✓.

### n = 25 = 5²

(Z/25Z)* ≅ Z/20Z. K_0 = {1,6,11,16,21} ≅ Z/5Z (order 5).

**{π_5, π_DYN(G)}: never sufficient for G ≠ {1}.**

Verify g=2 (order 20, primitive root mod 25):
- c = v_5(2−1) = v_5(1) = 0 < a=1. x = 5. g·5 = 10. 5 ≡ 10 mod 5? Yes. Conflict ✓.

Verify g=6 ∈ K_0 (6−1=5, c = v_5(5) = 1 = a):
- Sub-case c ≥ a. g·1 = 6. 1 ≡ 6 mod 5? Yes (both ≡ 1 mod 5). 1 ≠ 6. Conflict ✓.

### n = 27 = 3³

Additive levels: π_3, π_9, π_27=π_disc.

(Z/27Z)* ≅ Z/18Z. K_0 = {x : x≡1 mod 3} (order 9). K_1 = {x : x≡1 mod 9} (order 3). K_2 = {1}.

**{π_3, π_DYN(G)} for a=1:** Never sufficient (Theorem 1). For g with c=v_3(g−1)=2 (g≡1 mod 9, g≢1 mod 27; e.g., g=10): x=3^{1−0}... wait, c=2 ≥ a=1 (sub-case c≥a). g·1 = 10. 1≡10 mod 3? Yes (both ≡ 1 mod 3). 1≠10. Conflict ✓.

**{π_9, π_DYN(G)} for a=2:** Never sufficient (Theorem 1). For g=2 (c=0 < a=2): x=3^{2−0}=9. g·9=18. 9≡18 mod 9? Yes (both ≡ 0 mod 9). 9≠18. Conflict ✓.

### n = 49 = 7²

(Z/49Z)* ≅ Z/42Z. K_0 = {x:x≡1 mod 7} (order 7).

**{π_7, π_DYN(G)} never sufficient.** For g=3 (primitive root mod 49, c=0): x=7. 3·7=21. 7≡21 mod 7? Yes. Conflict ✓.

### n = 125 = 5³

Additive levels: π_5, π_25, π_125=π_disc.

**{π_5, π_DYN(G)}: never sufficient** (c<a=1, x=5; or c≥1 via K_0 elements). ✓
**{π_25, π_DYN(G)}: never sufficient** (c<a=2, x=25; or c=1, x=5; or c=2 via K_1). ✓

---

## Part 6 — Mixed Cases: n = p^r · q (Partial, Labeled)

**Setup.** n = p^r · q with p ≠ q prime. CRT: Z/nZ ≅ Z/p^rZ × Z/qZ.

**Additive partitions:**
- π_{p^a}: x ≡ y mod p^a (ignores q-coordinate).
- π_q: x ≡ y mod q (ignores p-coordinate).
- π_{p^a · q}: x ≡ y mod p^a AND x ≡ y mod q (both).

**A+A sufficient pair.** {π_{p^r}, π_q} = {π_disc on p-side, residue mod q}: π_{p^r} = partition by x mod p^r (p^r classes of size q), π_q = partition by x mod q (q classes of size p^r). Joint map: x ↦ (x mod p^r, x mod q). Injective iff lcm(p^r, q) = p^r·q = n. Since gcd(p^r,q)=1: lcm = p^r·q ✓. **Sufficient.** □ (A+A theorem holds unchanged for p^r·q.)

**A+M sufficient pair attempt.** {π_{p^a}, π_DYN(G)} for G ≤ (Z/nZ)* ≅ (Z/p^rZ)* × (Z/qZ)*.

**New question:** does the obstruction from Z/p^rZ extend to Z/p^r·qZ?

**Partial answer (proved):** If G has non-trivial projection onto (Z/p^rZ)* (i.e., G is not trivial at the p^r component), then the p-kernel obstruction still applies within the p-component fiber.

Specifically: fix q-coordinate = 0 (elements x = q·m for m ∈ Z/p^rZ). These elements are a copy of Z/p^rZ inside Z/nZ. The restriction of π_{p^a} to this copy is π_{p^a} on Z/p^rZ. The restriction of π_DYN(G) to this copy is the orbit partition of (G mod p^r) on Z/p^rZ.

By Theorem 1: if G mod p^r ≠ {1}, the restricted pair is insufficient on the copy — hence the full pair is insufficient.

**Theorem 2 (p-kernel obstruction persists in p^r·q — partial, proved for the p-fiber).**
For n = p^r·q and G ≤ (Z/nZ)* with G mod p^r ≠ {1}:

{π_{p^a}, π_DYN(G)} is NOT sufficient for 1 ≤ a ≤ r−1.

**Proof.** Choose x = q · p^{a−c} where c = v_p(g_p − 1) for some g ∈ G with g_p = g mod p^r ≠ 1. Then x ≡ 0 mod q (so π_q class of 0 mod q is not relevant here), and x has v_p(x) = a−c in the p-component. By the same proof as Theorem 1: g·x ≡ x mod p^a but g·x ≠ x. {x, g·x} are in the same π_{p^a} class and same G-orbit. Conflict. □

**What's NOT yet proved:** Whether G with G mod p^r = {1} (G acts trivially on p-component, non-trivially on q-component) can pair with π_{p^a} to give a sufficient family.

**Partial result for G mod p^r = {1}:**
If G ≤ {1} × (Z/qZ)* (G acts only on q-coordinate), then π_DYN(G) resolves distinctions in the q-coordinate but not the p-coordinate. π_{p^a} resolves distinctions in the first a p-adic digits. Two elements x, y with x ≡ y mod p^a can differ in:
(i) higher p-adic digits (level > a), or
(ii) q-digit.

For (i): G acting trivially on p-component cannot resolve higher p-adic digit differences within the same π_{p^a} class. So G cannot separate elements that agree mod p^a but differ in higher p-adic digits.

**Theorem 3 (proved).** For n = p^r·q and G = {1} × H with H ≤ (Z/qZ)*:
{π_{p^a}, π_DYN(G)} is NOT sufficient for a < r.

**Proof.** Elements x = 1 and x' = 1 + p^a: both ≡ 1 mod p^a (same π_{p^a} class), both ≡ 1 mod q (since p^a < p^r·q). G acts on q-coordinate only. 1 mod q = 1 mod q, (1+p^a) mod q: these are generally different mod q, so G might separate them. But: elements x = 0 and x' = p^a: x ≡ 0 mod q, x' ≡ p^a mod q. If p^a ≢ 0 mod q (true since gcd(p,q)=1), x and x' are in different q-residue classes. But wait — we need them in the same G-orbit. G acts as ×h on q-coordinate and trivially on p-coordinate. For g·0 = 0 and g·p^a = p^a (since G fixes the p-component, both elements are fixed in p-component; the q-component of 0 is 0 and g·0's q-component is h·0 = 0; and p^a's q-component is p^a mod q and g·p^a's q-component is h·(p^a mod q)). If h·(p^a mod q) ≠ p^a mod q (h acts non-trivially), then g·p^a ≠ p^a in q-component, so different π_{p^a}... wait, π_{p^a} doesn't see the q-component. Let me redo:

π_{p^a} identifies elements iff they agree in p-adic digit up to a. Elements 0 and p^a: 0 mod p^a = 0, p^a mod p^a = 0. Same π_{p^a} class. ✓

G-orbit of 0: G = {1}×H, so g·0 = h·0 = 0 (since h is a unit, h·0 = 0 mod q in the q-component, and 0 in the p-component). So 0 is a fixed point of all G elements. Orbit {0}.

G-orbit of p^a: p-component is p^a (fixed by G). q-component is p^a mod q. G acts as h on q-component: orbit = {p^a mod p^r, h^k·(p^a mod q) : k ≥ 0} in CRT. If H acts non-trivially on p^a mod q: orbit contains multiple elements with p-component = p^a but different q-components. None of these elements are equal to p^a itself (unless h·(p^a mod q) = p^a mod q, meaning p^a mod q is fixed). But 0 is NOT in this orbit (p-component 0 ≠ p^a). So 0 is not in same G-orbit as p^a.

Therefore {0, p^a} are NOT a conflict: they are in the same π_{p^a} class but in DIFFERENT G-orbits (orbit of 0 = {0}, orbit of p^a contains elements with p-component p^a). NO conflict here.

**Revised analysis:** We need elements x, g·x in same π_{p^a} class. π_{p^a} identifies x ≡ y mod p^a. Elements x and x + kp^a (k = 1,...,p^{r−a}−1) are in same class. Can G connect them?

g·(x + kp^a) = g·x + g·(kp^a). In CRT: g acts trivially on p-component (G = {1}×H), so p-component of g·(x+kp^a) = x+kp^a (p-component). q-component of g·(x+kp^a) = h·(x+kp^a mod q). So g·(x+kp^a) has p-component x+kp^a. For this to equal x (the original element in the same π_{p^a} class): p-component x+kp^a must equal x — only if k=0. Contradiction. So G = {1}×H can NEVER map x to x+kp^a for k ≠ 0.

**Correction to Theorem 3 attempt:** When G = {1}×H (acting trivially on p-component), no two elements differing only in higher p-adic digits are in the same G-orbit. So within-p-class conflicts don't arise from G. But ARE there conflicts at all?

Conflict: x and g·x in same π_{p^a} class means x ≡ g·x mod p^a, i.e., p^a | (g·x − x) = (g−1)·x. Since G acts trivially on p-component: (g−1)·x in CRT = (1−1, h−1)·(x_p, x_q) = (0, (h−1)·x_q). So (g−1)·x has p-component 0, which means p^a | 0 — always true. And q-component (h−1)·x_q. So g·x ≡ x mod p^a always (p-component unchanged, so p-adic congruence trivially satisfied).

Therefore: g·x and x are ALWAYS in the same π_{p^a} class for G = {1}×H. AND g·x ≠ x whenever h·x_q ≠ x_q. So EVERY non-trivial G-orbit move creates a π_{p^a} conflict: ALL G-orbit pairs (x, g·x) with g non-trivial are also π_{p^a}-equivalent.

**Revised Theorem 3 (proved).**
For n = p^r·q and G = {1}×H with H ≤ (Z/qZ)* non-trivial: {π_{p^a}, π_DYN(G)} is NOT sufficient for any a ≤ r (including a = r).

**Proof.** G acting trivially on p-component means g·x and x ALWAYS agree on p-component, hence always agree mod p^a. Any G-orbit pair is a π_{p^a} conflict. □

**Key insight.** For A+M sufficiency with π_{p^a} (a < r), we need G to "act on" the p-component — specifically, G must be able to distinguish elements within π_{p^a} classes by changing their p-adic digits above level a. But we showed (Theorem 1, Theorem 2): any non-trivial action on the p-component creates a within-π_{p^a}-class conflict via the p-kernel. This is a genuine fork: G cannot act on the p-component without creating conflicts, and G not acting on the p-component means it acts only on other coordinates and therefore cannot help with higher-level p-adic separation.

**Theorem 4 (proved — complete A+M impossibility for p^r components).**
For any n = p^r · m (m squarefree, gcd(p,m)=1, r ≥ 1) and any 1 ≤ a ≤ r:
{π_{p^a}, π_DYN(G)} is NOT sufficient for any non-trivial G ≤ (Z/nZ)*.

**Proof.**
Two cases by how G projects:

**Case 1: G mod p^r ≠ {1}.** Theorem 2 applies (conflict from non-trivial p-component action).

**Case 2: G mod p^r = {1}.** G acts trivially on p-component. For any g ∈ G and any x ∈ Z/nZ: g·x and x have the same p-component. Therefore p^a | (g·x − x) always (p-component difference = 0). So g·x ≡ x mod p^a always. All G-orbit pairs are π_{p^a}-equivalent. If G has any non-trivial orbit (g·x ≠ x for some x), that orbit pair is a conflict. Since G non-trivial: ∃g ≠ 1 in G, ∃x with g·x ≠ x. Conflict. □

---

## Part 7 — The Right Replacement for the Squarefree Support Condition

**Squarefree support condition (Theorem 4, prior arc):** For squarefree n and π_d:

> G acts trivially outside primes of d ⟺ G ≤ ker( (Z/nZ)* → (Z/(n/d)Z)* )

This worked because in squarefree n, the additive partition π_d is "blind" to primes of n/d but "sharp" on primes of d — meaning elements within a π_d fiber (same d-residue) are uniquely distinguished by their (n/d)-coordinates, and G trivial on (n/d) means G doesn't move elements to other (n/d)-positions, hence doesn't create within-fiber conflicts.

**Prime-power obstruction — why squarefree reasoning fails:** In Z/p^rZ, within a π_{p^a}-fiber, elements differ in their (p^r/p^a) = p^{r−a} multiple structure. This is NOT an independent coordinate — it is a higher-order digit in the SAME p-adic expansion. There is no "other prime" to be the unit group of. Any multiplicative action on Z/p^rZ must operate via the SINGLE unit group (Z/p^rZ)*, and that group acts non-trivially on within-fiber elements via the p-kernel.

**The correct replacement statement (Theorem 4):** For prime-power n = p^r:

> No non-trivial multiplicative orbit partition can complement any non-discrete additive partition.

In the squarefree language: there is no valid "support confinement" condition because there is no complement coordinate system. The squarefree support condition requires a second independent variable; the prime-power setting has only one.

**For n = p^r · m (mixed):** A+M sufficiency requires:
- The additive partition must be π_{p^a} for some a ≤ r (or a product partition).
- G must act trivially on the p-component (Case 2 above) — but this makes π_{p^a} trivially unresolvable.
- OR G acts non-trivially on the p-component — Theorem 2 gives conflict.
- Conclusion: π_{p^a} cannot be used as one half of an A+M sufficient pair when p^r | n.

**Valid A+M sufficient pair for n = p^r·m:** Use π_{p^r} (= residue mod p^r, the "fully resolved p-component") and DYN of G focused on m-component. Then: π_{p^r} identifies x ≡ y mod p^r, and G (trivial on p-component, non-trivial on m-component) separates elements within π_{p^r}-fibers by their m-residue. Joint map: x ↦ (x mod p^r, G-orbit of x_m). This is exactly the squarefree A+M theorem applied to the m-component! Sufficient iff G is supported on m-primes (squarefree conditions apply to the m-part).

---

## Part 8 — Complete Statement for Mixed n = p^r · m

**Theorem 5 (A+M for n = p^r · m — proved).**
Let n = p^r · m with m squarefree, gcd(p,m) = 1, r ≥ 1. For G ≤ (Z/nZ)* and d | n:

**{π_d, π_DYN(G)} is sufficient iff:**
1. p^r | d (the additive partition fully resolves the p-component), AND
2. G mod (p^r component) = {1} (G acts trivially on the p-component), AND
3. The squarefree A+M condition holds for (d/p^r, G mod m, m): G acts trivially on primes of m/(d/p^r).

**Simplified:** Decompose d = p^r · d_m with d_m | m. Then condition becomes: (i) the p^r factor is fully used (p^r | d), and (ii) G is focused on primes of d_m within the m-component (squarefree theorem applies to (d_m, G_m, m)).

**Proof.**
The CRT decomposition Z/nZ ≅ Z/p^rZ × Z/mZ splits all structures. Joint map J = (f_d, f_G).

If p^r ∤ d: by Theorem 4, the p-component is not fully resolved by π_d, and any G creates a conflict. Not sufficient.

If p^r | d: π_d resolves the full p-component (x mod p^r determines x mod d restricted to p-part). Within each π_d fiber, elements differ only in m-coordinates (the p-component is fixed). G must separate these: G acting trivially on p (required to avoid Theorem 2 conflicts) must act sufficiently on m to separate all m-coordinate pairs within each d_m fiber. This is exactly the squarefree condition. □

---

## Part 9 — Test Cases for n = 18, 50, 75

### n = 18 = 2 · 3²

Decompose: p = 3, r = 2, m = 2. p^r = 9, m = 2 squarefree.

By Theorem 5: valid A+M sufficient pairs require 9 | d (i.e., d ∈ {9, 18}).

d = 9: π_9 = residue mod 9 (9 classes of size 2; {0,9},{1,10},...,{8,17}). d_m = 18/9 = 2 = m. Need G_m trivial on primes of m/d_m = 2/2 = 1 (empty). Condition: G_m can be anything in (Z/2Z)* = {1}. So G_m = {1} (only option). G = {1}×{1} = trivial? Then π_DYN({1}) = π_disc. Trivially sufficient (one partition is π_disc).

d = 9, G non-trivial in (Z/18Z)* ≅ (Z/9Z)* × (Z/2Z)*: G = {1}×{1,−1 mod 2} but (Z/2Z)* = {1}, so no non-trivial G. G = something from (Z/9Z)*: this violates condition (ii) (G must be trivial on p-component = trivial mod 9). So only G = {1}.

Conclusion: for n = 18, no non-trivial A+M sufficient pair exists with d < 18. □

Actually — let's check if {π_9, π_DYN(G)} is sufficient for G focused on m=2:

(Z/18Z)* = {1,5,7,11,13,17}. Elements trivial mod 9: need g ≡ 1 mod 9. Only g = 1, g = 10 (10 ≡ 1 mod 9, gcd(10,18)=2 — not a unit). So only g = 1 is trivial mod 9 among units. π_DYN({1}) = π_disc. Trivially sufficient but trivial.

Sufficient non-trivial pair: by A+A, {π_9, π_2}: joint map x ↦ (x mod 9, x mod 2). Injective iff lcm(9,2)=18=n. ✓ {π_9, π_2} is sufficient.

Is π_2 a Type-A partition? Yes: f_2(x) = x mod 2. Blocks: even={0,2,4,...,16}, odd={1,3,...,17}. A+A case, not A+M.

### n = 50 = 2 · 5²

p = 5, r = 2, m = 2. p^r = 25.

Valid A+M: d must have 25 | d. d ∈ {25, 50}.

d = 25: π_25 = residue mod 25 (25 classes of size 2). G trivial mod 25. (Z/50Z)* ≅ (Z/25Z)* × (Z/2Z)* ≅ Z/20Z × {1}. Elements trivial mod 25: only g = 1. Trivial only.

A+A sufficient: {π_25, π_2}: lcm(25,2)=50=n. ✓

### n = 75 = 3 · 5²

p = 5, r = 2, m = 3. p^r = 25.

Valid A+M: d with 25 | d. d ∈ {25, 75}.

d = 25: π_25 (25 classes of size 3). G trivial mod 25, acting on (Z/3Z)* component. (Z/75Z)* ≅ (Z/25Z)* × (Z/3Z)*. G ≤ {1} × (Z/3Z)*: G = {1} × {1} (trivial) or G = {1} × {1,2} = {1, 26 mod 75}. Check: 26 mod 25 = 1 ✓ (trivial on 25), 26 mod 3 = 2 (non-trivial on 3). G = {1,26}.

{π_25, π_DYN({1,26})}: Check sufficiency. π_25 classes: {x, x+25, x+50} for x = 0,...,24. G orbit of x: {x, 26x mod 75}. Since 26 ≡ 1 mod 25: 26x mod 75 has same mod-25 residue as x. 26x mod 3 = 2x mod 3. So orbit of x = {x, 26x = x+25(some adjustment)...} let me compute: 26·1=26, 26·26=676≡676-9·75=676-675=1. So orbit {1,26}. 1 mod 25=1, 26 mod 25=1. Same π_25 class. CONFLICT. Not sufficient.

Wait — I need to recheck Theorem 5 condition (iii): squarefree condition on (d/p^r, G_m, m) = (25/25=1, {1,2 mod 3}, 3). d_m = d/p^r = 1. G_m = (Z/3Z)* = {1,2}. Squarefree condition: G_m trivial on primes of m/d_m = 3/1 = 3. G_m trivial mod 3 means G_m = {1}. But G_m = {1,2}. NOT trivial. Condition fails. Consistent with conflict found.

For sufficiency: need G_m trivial mod 3 (i.e., G_m = {1}) → G = {1}. Trivial.

A+A sufficient: {π_25, π_3}: lcm(25,3)=75=n. ✓

---

## Part 10 — Classification Summary

**Theorem 1 (proved):** For n = p^r: {π_{p^a}, π_DYN(G)} sufficient iff G = {1} (trivial).

**Theorem 4 (proved):** For n = p^r · m: {π_{p^a}, π_DYN(G)} sufficient iff G trivial on p-component (p^r | d forced) AND squarefree condition holds for m-component.

**Theorem 5 (proved):** Complete A+M condition for n = p^r · m: requires p^r | d.

**Table:**

| n | Type | A+A sufficient pair | A+M non-trivial pair | M+M sufficient pair |
|---|---|---|---|---|
| p^r (single) | pure prime power | None (all comparable) | None (Thm 1) | {DYN(G), DYN(H)}, G∩H={1} |
| p^r · q | mixed | {π_{p^r}, π_q} ✓ | Need G trivial on p^r, then squarefree (Thm 5) | G∩H={1} in (Z/nZ)* |
| n = 9 = 3² | pure | None | None | {DYN({1,4,7}), DYN({1,8})} ✓ |
| n = 18 = 2·3² | mixed | {π_9, π_2} ✓ | Only trivial | {DYN(G), DYN(H)}, G∩H={1} |
| n = 50 = 2·5² | mixed | {π_25, π_2} ✓ | Only trivial | G∩H={1} |
| n = 75 = 3·5² | mixed | {π_25, π_3} ✓ | Only trivial | G∩H={1} |

---

## Summary

**Strongest honest claim:**
> For any n = p^r · m (m squarefree): the A+M sufficient pair condition requires the additive component to fully resolve the prime-power part (p^r | d). Any attempt to use a "partial" additive partition π_{p^a} (a < r) at a prime-power component creates a p-kernel conflict that no orbit partition can avoid. The squarefree A+M theorem (G trivial on primes of n/d) survives exactly for the squarefree substructure m — the prime-power part p^r contributes only via its fully-resolved additive partition π_{p^r}. The M+M theorem (G∩H={1}) holds unchanged for all n.

**Strongest honest boundary:**
> Theorem 5 gives the complete A+M classification for n = p^r · m when G is restricted to the ({1}×m-part)×(trivial on p^r) form. The case where G has non-trivial action on BOTH the p^r and m components is handled by Theorem 2 (p-kernel conflict from p-component action). Together Theorems 2 and 5 cover all cases. The remaining open problem: complete A+M classification for n = p^r · q^s (two prime powers, neither squarefree). Each prime-power component requires its own fully-resolved additive partition, suggesting the generalization: d must satisfy p^r | d for every prime power p^r | n — but this forces d = n (π_disc), leaving only trivial cases. This would mean: **for n with any repeated prime factor, no non-trivial A+M sufficient pair exists at all.**

**Conjectured general statement (not yet proved for n = p^r·q^s):**
{π_d, π_DYN(G)} sufficient iff for every prime p with p^r || n (p^r | n, p^{r+1} ∤ n): p^r | d. Combined with squarefree A+M conditions on the squarefree part of n/d. For n = p^r·q^s: requires both p^r | d and q^s | d, forcing d = p^r·q^s = n. Only trivial sufficient A+M pairs.
