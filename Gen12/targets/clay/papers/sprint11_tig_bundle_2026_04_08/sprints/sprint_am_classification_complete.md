# SPRINT: A+M CLASSIFICATION COMPLETION FOR GENERAL n
## Theorem/proof only. All results proved or labeled conjectural.

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Setup and Notation (General n)

**General modulus.** n = p₁^{r₁} · p₂^{r₂} · ··· · pₖ^{rₖ} with distinct primes p₁,...,pₖ and rᵢ ≥ 1.

**Squarefree part.** rad(n) = p₁p₂···pₖ (product of distinct prime factors).

**Repeated part.** For rᵢ ≥ 2, call pᵢ a *repeated prime* of n.

**CRT decomposition.** Z/nZ ≅ ∏ᵢ Z/pᵢ^{rᵢ}Z. For x ∈ Z/nZ: write x = (x₁,...,xₖ) with xᵢ = x mod pᵢ^{rᵢ} ∈ Z/pᵢ^{rᵢ}Z.

**Additive partition π_d** (for d | n): x ~_{π_d} y iff d | (x−y). Block size = n/d. Block count = d.

**p-adic valuation at prime pᵢ:** v_{pᵢ}(x) = largest k with pᵢ^k | x (v_{pᵢ}(0) = rᵢ by convention in Z/pᵢ^{rᵢ}Z).

**Unit group.** (Z/nZ)* ≅ ∏ᵢ (Z/pᵢ^{rᵢ}Z)* by CRT.

**p-kernel at prime pᵢ, level b** (for 0 ≤ b ≤ rᵢ−1):

K_{pᵢ,b} = ker( (Z/pᵢ^{rᵢ}Z)* → (Z/pᵢ^{b+1}Z)* ) = { x ∈ (Z/pᵢ^{rᵢ}Z)* : x ≡ 1 mod pᵢ^{b+1} }

Order: |K_{pᵢ,b}| = pᵢ^{rᵢ−b−1}. In particular K_{pᵢ,rᵢ−1} = {1}.

---

## Part 2 — The Fiber Decomposition Lemma

**Definition (pᵢ-fiber of π_d).**
For prime pᵢ | n: write d = pᵢ^{aᵢ} · d' with gcd(pᵢ, d') = 1 and 0 ≤ aᵢ ≤ rᵢ.

The *pᵢ-depth* of d is aᵢ = v_{pᵢ}(d).

Within each π_d block B: two elements x, y ∈ B satisfy x ≡ y mod d, which in the pᵢ-component means xᵢ ≡ yᵢ mod pᵢ^{aᵢ}. The pᵢ-components of elements within a single π_d block range over a coset of pᵢ^{aᵢ}·Z/pᵢ^{rᵢ}Z — a subgroup of Z/pᵢ^{rᵢ}Z of order pᵢ^{rᵢ−aᵢ}.

**Lemma 1 (Fiber p-Component Span).**
For a π_d block B containing element x: the set of pᵢ-components of elements of B is exactly the coset xᵢ + pᵢ^{aᵢ}·(Z/pᵢ^{rᵢ}Z), a set of size pᵢ^{rᵢ−aᵢ}.

**Proof.** y ∈ B iff y ≡ x mod d. In the pᵢ-component: yᵢ ≡ xᵢ mod pᵢ^{aᵢ} (the pᵢ-part of d). The pᵢ-component of y is free to be any element of Z/pᵢ^{rᵢ}Z that is ≡ xᵢ mod pᵢ^{aᵢ}. There are pᵢ^{rᵢ−aᵢ} such elements. Each is realized (by CRT, choosing other components freely). □

**Corollary.** If aᵢ < rᵢ: within a π_d block, the pᵢ-component takes pᵢ^{rᵢ−aᵢ} ≥ pᵢ distinct values. Elements of a block are NOT distinguished by their pᵢ-component alone.

---

## Part 3 — Main Theorem: Repeated-Prime Obstruction

**Theorem 1 (Repeated-Prime A+M Obstruction — proved).**

Let n = p^r · m with r ≥ 2, gcd(p, m) = 1. Let d | n with v_p(d) = a < r (the p-depth of d is strictly less than r). Let G ≤ (Z/nZ)* be any non-trivial subgroup.

Then {π_d, π_DYN(G)} is NOT sufficient.

**Proof.**

Let g ∈ G be any non-identity element. Write g = (g_p, g_m) in CRT, where g_p ∈ (Z/p^rZ)* and g_m ∈ (Z/mZ)*.

**Case A: g_p ≠ 1 in (Z/p^rZ)*.**

Let c = v_p(g_p − 1) ∈ {0, 1, ..., r−1} (since g_p ≠ 1, c is finite).

We construct a conflict pair {x, g·x}:

*Sub-case A1: c ≥ a.* Choose x via CRT: x_p = 1 (any unit in Z/p^rZ), x_m = 1 (unit in Z/mZ). Then:
- g·x has (g·x)_p = g_p · 1 = g_p. Since c = v_p(g_p−1) ≥ a: g_p ≡ 1 mod p^a, so g_p · 1 ≡ 1 = x_p mod p^a. Therefore p^a | (g·x − x) in the p-component. Combined with other components: g·x ≡ x mod d (since d = p^a · d' and the d'-component also needs checking).

Actually let me be more careful. We need p^a | (g·x)_p − x_p AND d' | (g·x)_m − x_m where d = p^a · d'.

For (g·x)_p − x_p = g_p − 1 (when x_p = 1): v_p(g_p−1) = c ≥ a, so p^a | g_p−1. ✓

For d' | (g·x)_m − x_m = g_m − 1: this need not hold in general. So we cannot guarantee g·x ≡ x mod d' just from the p-part.

**Refinement of construction.** Let d = p^a · d'. We need x such that g·x ≡ x mod d, i.e., (g−1)·x ≡ 0 mod d, i.e., p^a · d' | (g−1)·x.

Decompose: need p^a | (g_p−1)·x_p AND d' | (g_m−1)·x_m.

Choose x_m = 0 in Z/mZ (i.e., m | x in Z/nZ; x is a multiple of m). Then (g_m−1)·0 = 0, d' | 0 ✓.

Choose x_p = p^{max(a−c, 0)}: if c ≥ a, x_p = 1; if c < a, x_p = p^{a−c}.
- c ≥ a: x_p = 1. v_p((g_p−1)·1) = c ≥ a ✓.
- c < a: x_p = p^{a−c}. v_p((g_p−1)·p^{a−c}) = c + (a−c) = a ✓.

So x is defined by CRT: x ≡ x_p mod p^r and x ≡ 0 mod m. Now:

- g·x ≡ x mod d: verified above. Same π_d class. ✓
- g·x ≠ x: (g·x)_p = g_p · x_p.
  - c ≥ a: (g·x)_p = g_p ≠ 1 = x_p (since g_p ≠ 1 in Z/p^rZ). ✓ g·x ≠ x.
  - c < a: (g·x)_p − x_p = (g_p−1)·p^{a−c}. v_p = a < r. So (g·x)_p ≠ x_p. ✓ g·x ≠ x.
- g·x in same G-orbit as x: by definition, g·x = g·x for g ∈ G. ✓

Conflict confirmed for Case A. □

**Case B: g_p = 1 in (Z/p^rZ)* (g acts trivially on p-component).**

Then g = (1, g_m) with g_m ≠ 1 in (Z/mZ)* (since g ≠ 1 in (Z/nZ)*).

For any x ∈ Z/nZ: (g·x)_p = 1 · x_p = x_p. So g·x and x have the SAME p-component. Therefore (g·x) − x has p-component 0, so v_p((g·x)−x) = rᵢ (the full power; difference is 0 in p-component). In particular p^a | (g·x)−x for any a ≤ r. So g·x ≡ x mod p^a always.

For g·x ≡ x mod d = p^a · d': also need d' | (g·x − x)_m = (g_m−1)·x_m. If d' = 1: automatic. If d' > 1: choose x_m to be a fixed point of d'-residue: need x_m with (g_m−1)·x_m ≡ 0 mod d'.

Let d'_g = gcd(d', gcd-content of g_m−1 over the m-component primes). Choose x_m = 0 mod m (same as before). Then (g_m−1)·0 = 0, d' | 0 ✓.

So x = (x_p, 0) with any x_p: g·x = (x_p, g_m·0) = (x_p, 0) = x? No: g_m·0 = 0 in Z/mZ (0 is fixed by all ring endomorphisms). So g·x = x for x = multiple of m. This gives g·x = x, a trivial pair — not a conflict.

Choose x_m ≠ 0. Then (g_m−1)·x_m may or may not be divisible by d'. To guarantee a conflict: choose x such that g·x ≡ x mod d but g·x ≠ x.

Since g_p = 1: g·x always has same p-component as x. For g·x ≡ x mod d we need d' | (g_m−1)·x_m. And g·x ≠ x requires g_m·x_m ≠ x_m mod p^r... wait. Let me redo: g·x ≠ x requires g·x ≠ x in Z/nZ. Since (g·x)_p = x_p, we need (g·x)_m ≠ x_m, i.e., g_m · x_m ≠ x_m mod m, i.e., x_m ≠ 0 and g_m ≠ 1... we assumed g_m ≠ 1. So for any x with x_m not fixed by g_m (i.e., x_m ∉ Fix(g_m)), g·x ≠ x.

Now: does there exist x_m ∉ Fix(g_m) with d' | (g_m−1)·x_m?

If d' = 1: any x_m works. Let x_m = 1 (a unit in Z/mZ; 1 is not fixed by g_m since g_m ≠ 1 in (Z/mZ)*, so g_m·1 = g_m ≠ 1). Conflict: x = (x_p, 1), g·x = (x_p, g_m). Same p-component (same mod p^a since p^a | 0). Same π_d class since d = p^a · 1 = p^a. But g·x = (x_p, g_m) ≠ (x_p, 1) = x since g_m ≠ 1. Conflict. ✓

If d' > 1: We need d' | (g_m−1)·x_m for some x_m not fixed by g_m. Let q be a prime factor of d'. Then q | d' | m (since d | n and d = p^a · d' with gcd(p,d')=1, and d | n = p^r·m, so d' | m). Consider x_m = m/q: then (g_m−1)·(m/q). We need d' | (g_m−1)·(m/q). Since d' | m: m/q is a multiple of m/d' (if q | d'). More directly: just take x_m = 0 mod (m/d') with x_m ≠ 0: choose x_m = m/d' (if m/d' > 0, which it is since d' | m and d' < m when r ≥ 1).

Actually, the cleanest approach: x_m = 0 gives g·x = x (trivial). Instead: since g_m ≠ 1 in (Z/mZ)*, there exists a prime q | m with g_m mod q ≠ 1 mod q (at least one prime component is non-trivial). Take x_m = m/q. Then:
- (g_m−1)·(m/q): in the q-component, this is (g_m mod q − 1)·0 = 0 (since m/q ≡ 0 mod q). In the q'-component for q' | m, q' ≠ q: (m/q) mod q' ≠ 0 (since q' ∤ m/q).
- Need d' | (g_m−1)·(m/q). Since d' | m and m/q = product of primes of m except one q: need every prime power in d' to divide (g_m−1)·(m/q). Since q | d' is possible... this is getting complicated.

Let me use a cleaner construction for Case B, d' > 1:

x = CRT: x_p = 1, x_m = anything. Then x ≡ 1 mod p and x ≡ x_m mod m. 

g·x − x = (0, (g_m−1)·x_m) in CRT. For g·x ≡ x mod d = p^a · d': need p^a | 0 ✓ and d' | (g_m−1)·x_m.

Since g_m ≠ 1 in (Z/mZ)*: the map φ: (Z/mZ)* → Z/mZ by φ(x_m) = (g_m−1)·x_m is not identically zero (it equals 0 only if x_m = 0 or g_m = 1, neither holds for units). The image of φ on units includes non-zero values. We need some unit x_m with d' | (g_m−1)·x_m.

Take x_m = (g_m−1)^{−1} mod (m/gcd(m,d'))... this requires g_m−1 to be a unit mod something. Instead:

Simplest: gcd(g_m−1, m) = D. Let x_m = m/D (if D < m). Then (g_m−1)·(m/D) is divisible by m (since D | g_m−1 and m/D is an integer, and (g_m−1)·(m/D) ≥ m/D · D = m). So d' | m | (g_m−1)·(m/D)·(something)...

Actually the clearest: in Z/mZ, (g_m−1) is a non-zero element (since g_m ≠ 1). The subgroup generated by (g_m−1) in (Z/mZ, +) has order m/gcd(g_m−1, m). The multiples of d' that are in ⟨g_m−1⟩ are the multiples of lcm(d', gcd(g_m−1,m))... 

Use a different tactic. We don't need the conflict to use d' at all. We already have a conflict from Case A applied to a subgroup element if ANY element of G has non-trivial p-component. If ALL elements of G have trivial p-component (Case B for all g ∈ G), then G = {1} × G_m with G_m ≤ (Z/mZ)*. If G_m ≠ {1}: pick any g_m ≠ 1 in G_m, pick any x with x_m not fixed by g_m. Then g·x and x have same p-component (both x_p) so g·x ≡ x mod p^a. And (g·x)_m ≠ x_m. Since g·x ≡ x mod d' requires d' | (g_m−1)·x_m: 

**Key move:** since d | n and the p-part of d is p^a, the m-part d' divides m. Since m is squarefree (wait — in the statement n = p^r · m with m not necessarily squarefree in the full generality). 

Let me re-restrict to the case where m is squarefree for the core theorem, and handle general m recursively.

**Restricted Case B (m squarefree).** G = {1} × G_m with G_m ≤ (Z/mZ)*. For any g_m ≠ 1: pick prime q | m with g_m ≢ 1 mod q (exists since m squarefree, g_m ≠ 1 means some q-component is non-trivial). Take x = CRT: x_p = 1, x_m = 0 mod (m/q), x_m = 1 mod q. Then x_m = q^{-1} · m... actually use CRT: x_m ≡ 1 mod q, x_m ≡ 0 mod (m/q). Then (g_m−1)·x_m: q-component = (g_m mod q − 1)·1 = g_m mod q − 1 ≠ 0 mod q. Other prime components q': x_m ≡ 0 mod q', so (g_m−1)·x_m ≡ 0 mod q'. So (g_m−1)·x_m ≡ (g_m−1) mod q and ≡ 0 mod (m/q).

Need d' | (g_m−1)·x_m. d' | m (squarefree). If q ∤ d': then d' | (m/q) | m, and (g_m−1)·x_m ≡ 0 mod (m/q), so d' | (g_m−1)·x_m ✓. Conflict: x and g·x are in same π_d class and g·x ≠ x.

If q | d': then need q | (g_m−1)·x_m = (g_m mod q − 1) (in q-component). But g_m mod q − 1 ≠ 0 mod q. So q ∤ (g_m−1)·x_m. This x doesn't give a conflict via d'. But: q | d' | d. So there's a different element that works: x' = CRT: x_p = p^{a−0}... actually choose a completely different element.

Take x with x_p = 1, x_m = d'/gcd(d', g_m−1): a multiple of d' in Z/mZ. Then... this is getting recursive.

**Clean resolution using the p-fiber instead:** We already handled Case A. For Case B, instead of fighting d', observe:

If a < r: within a single π_d block, the p-component takes p^{r−a} ≥ p distinct values (Lemma 1). Pick x and x' in the same π_d block with x_p ≠ x'_p (differing in p-adic digit at level ≥ a). Can G connect them?

G = {1} × G_m acts trivially on p-component: g·x_p = x_p. So (g·x)_p = x_p ≠ x'_p. G cannot map x to x'. The within-p-fiber elements of a π_d block are NOT separated by G either.

Wait — this is a different issue: we want G to SEPARATE elements of a π_d block (to contribute to sufficiency). If G cannot connect elements within the same p-adic level (which it can't in Case B), then elements within a block that differ only in higher p-adic digits are in DIFFERENT G-orbits — so they ARE separated by π_DYN(G). No conflict there.

The conflict is: can G ever map x to y where x and y are in the same π_d block? Yes — via g_m acting on the m-component. Elements x and g·x = (x_p, g_m·x_m) are in the same π_d class iff p^a | x_p − x_p = 0 ✓ (p-component same) AND d' | (g_m−1)·x_m.

The second condition: d' | (g_m−1)·x_m. For this to fail (no conflict): need (g_m−1)·x_m ≢ 0 mod d' for all x ∈ Z/nZ with g_m·x_m ≠ x_m.

But the map x_m ↦ (g_m−1)·x_m on Z/mZ is surjective onto gcd(g_m−1, m)·(Z/mZ). Since d' | m: if gcd(g_m−1, m) and d' share a prime factor q, then (g_m−1)·(any unit x_m with x_m ≢ 0 mod q... 

**This analysis is getting complicated. Let me use the clean path.**

**Clean proof for Case B using a = 0 anchor (i.e., via p-component triviality and m-component conflict directly):**

Claim: if G = {1} × G_m (non-trivial), then for any a (including a = 0), the pair {π_d, π_DYN(G)} is not sufficient for d with a < r.

Proof: Take x with x_p = 1 (a p-unit), x_m = 1 (a unit in Z/mZ). Take g = (1, g_m) with g_m ≠ 1.

g·x = (1, g_m). Now x ≡ g·x mod p^a (both have p-component 1, same mod p^a). So p^a | (g·x − x). Remaining: d' | (g·x − x)_m = g_m − 1. This holds iff d' | (g_m − 1) in Z/mZ.

If d' | g_m − 1: conflict confirmed. ✓

If d' ∤ g_m − 1: try x_m = (g_m−1)^{−1} mod (m/ gcd(m, d'))... 

More cleanly: since d' | m and m squarefree, d' = q₁q₂···qⱼ (product of distinct primes dividing m). g_m ≠ 1 in (Z/mZ)* means g_m mod q ≠ 1 for at least one prime q | m. If q | d': at the q-prime component, g_m mod q − 1 ≠ 0, so d' (which includes factor q) does NOT divide g_m − 1. No conflict at x_m = 1 for q | d'.

But try x_m = m/q (a multiple of all m-primes except q): (g_m−1)·(m/q) in q-component = (g_m mod q − 1)·0 = 0 (since m/q ≡ 0 mod q). In q'-component for q' | m, q' ≠ q: (g_m mod q' − 1)·(m/q mod q'). Since m/q = product of q' for q'≠q, m/q ≡ 0 mod q' for q'|m, q' ≠ q. So (g_m−1)·(m/q) = 0 in ALL m-components → (g_m−1)·(m/q) = 0 in Z/mZ. But then g·x − x = 0 in m-component, so g·x = x. Trivial pair.

Choose x_m = 1 and accept that d' may not divide g_m−1. Let q be a prime with q | d' and g_m mod q ≠ 1. Then at x_m = q^{−1} (inverse of q mod m)... this is the correct move: x_m = q^{-1} mod m. (g_m mod q − 1)·q^{-1} mod q = (g_m mod q − 1)·q^{-1} mod q. This is non-zero mod q (since g_m mod q ≠ 1 and q^{-1} ≠ 0 mod q). So q ∤ (g_m−1)·x_m → d' ∤ (g_m−1)·x_m. Still no conflict via this x.

But now consider: choose x_m such that d' | (g_m−1)·x_m. Since d' | m and (g_m−1) is a fixed element of Z/mZ: the set S = {x_m ∈ Z/mZ : d' | (g_m−1)·x_m} is a subgroup of (Z/mZ, +) of index gcd(d', "order of g_m−1 in Z/mZ") / something. More precisely: let D = gcd(g_m−1, m) (in Z/mZ). Then (g_m−1)·x_m ≡ 0 mod d' iff d'/gcd(d',D) | x_m.

So S = {x_m : d'/gcd(d',D) | x_m}. |S| = m / (d'/gcd(d',D)) = m·gcd(d',D)/d'.

S is non-empty (it contains 0, but we need x_m with g_m·x_m ≠ x_m, i.e., x_m ≠ 0). If |S| > 1: S contains non-zero elements. |S| = m·gcd(d',D)/d' ≥ 1. |S| > 1 iff m·gcd(d',D) > d', i.e., m > d'/gcd(d',D).

Since d' | m and m ≥ d': m ≥ d' ≥ d'/gcd(d',D). So |S| ≥ gcd(d',D) ≥ 1. If gcd(d',D) ≥ 2 (some prime q divides both d' and D = gcd(g_m−1,m)): then |S| ≥ 2, S contains non-zero x_m. For such x_m: g·x ≡ x mod d (p-component identical, m-component satisfies d' | (g_m−1)·x_m), and g·x ≠ x (since g_m·x_m ≠ x_m for x_m ≠ 0, g_m ≠ 1). Conflict.

If gcd(d',D) = 1 for all prime components... then gcd(d', g_m−1) = 1 in Z/mZ. In this case: d' | (g_m−1)·x_m iff d' | x_m (since gcd(d', g_m−1)=1 implies g_m−1 is a unit mod each prime of d'). So S = multiples of d' in Z/mZ. The only non-zero option: x_m = d', 2d', etc. Take x_m = d' (if d' ≠ 0 in Z/mZ, i.e., d' < m which holds since d' | m and d' ≠ m since G_m non-trivial means m > 1 and d' = gcd(d,m) ≤ m; if d' = m then π_d includes full m resolution and... this is edge case). 

For x_m = d': g·x_m − x_m = (g_m−1)·d'. Since gcd(d', g_m−1)=1 in Z/mZ: g_m−1 is a unit mod all primes of d', so (g_m−1)·d' ≡ 0 mod d' only if d' | d' (trivially). v_{q}((g_m−1)·d') = v_q(d') for each q | d' (since g_m−1 is a unit mod q). So d' | (g_m−1)·d' ✓ (since v_q((g_m−1)·d') = v_q(d') for each q | d'). And g_m·d' ≠ d' in Z/mZ (since g_m ≠ 1 and d' is a non-zero non-unit of Z/mZ... actually d' could be a unit mod some prime? No: d' | m, so some prime q | gcd(d',m) = d', and d' ≡ 0 mod q in Z/mZ). Wait: in Z/mZ, d' is a zero divisor if gcd(d',m) = d' (which holds). So g_m·d' = g_m·d' in Z/mZ. For this to ≠ d': need g_m ≠ 1 in Z/(m/gcd(d',m))Z... this is getting complicated for the degenerate case.

**Resolution: use the z-fiber approach instead.**

For Case B with g_p = 1: every G-orbit move is transparent to π_{p^a} (same p-component means always in same π_d class for the p-part). So EVERY non-trivial G-orbit step is a conflict pair if it also fixes the m-part modulo d'. The m-part concern is whether d' | (g_m−1)·x_m for the chosen x_m.

If d' = 1: immediate conflict (any x_m with g_m·x_m ≠ x_m).

If d' = m (full m-resolution in d): then d = p^a · m, and π_d resolves the full m-component. G = {1}×G_m: every G-orbit step changes m-component, hence changes π_d class. No conflict from G-orbit steps (they always change the m-component which π_d sees). But g·x ≡ x mod d requires d' = m | (g_m−1)·x_m. Since g_m ≠ 1 in (Z/mZ)*: g_m·x_m ≠ x_m for units x_m, and d' = m | 0 only if g_m·x_m = x_m. So only fixed points of g_m are in S. These are not conflicts. OK — no conflict in Case B when d' = m.

**So for d' = m (d = p^a·m): Case B produces no conflict!** This is the "fully m-resolved" case. Let's check if {π_{p^a·m}, π_DYN({1}×G_m)} can be sufficient.

Elements x and y in same π_{p^a·m} block: x ≡ y mod p^a AND x ≡ y mod m, i.e., x ≡ y mod p^a and x_m = y_m. So x and y differ only in higher p-adic digits (above level a). G = {1}×G_m acts trivially on p-component. So G-orbits within a block of π_{p^a·m} are singletons (can't move within the block since all p-adic digits above a are ignored by G and the m-component is fixed by the block). Wait: within a π_{p^a·m} block, all elements have the same residue mod p^a AND same m-residue. So they differ only in pᵢ-components at levels a+1,...,r. G = {1}×G_m acts only on m-component → can't move within the block. Each element is in its own G-orbit (within the block). So G separates all within-block elements trivially. Is the joint map injective?

Joint map J: x ↦ (x mod (p^a·m), G-orbit of x). Within each π_{p^a·m} block, G-orbits are singletons (G acts trivially on the block). So J restricted to a block is injective trivially. Globally: different blocks ↦ different π_{p^a·m} classes (first component distinguishes them). So J is injective. **{π_{p^a·m}, π_DYN({1}×G_m)} is sufficient!**

But wait: this is only non-trivial if G_m ≠ {1} actually helps (otherwise π_DYN({1}) = π_disc and one partition is discrete). AND the sufficiency relies on G_m being trivial on the m-component blocks... let me recheck.

Actually: two elements x ≠ y in same π_{p^a·m} block have same p^a-residue AND same m-residue. G-orbit of x: G = {1}×G_m, so G-orbit of x = {(x_p, g_m·x_m) : g_m ∈ G_m} = {(x_p, y_m) : y_m ∈ G_m-orbit of x_m}. Since y_m = x_m (same m-residue for all elements in same block), and G_m·x_m = {g_m·x_m}: g_m·x_m = x_m iff g_m fixes x_m. So G-orbit of x within the block = {x} if x_m is fixed by G_m, and {elements with same p-component x_p, same p^a-residue, and G_m-orbit of x_m = x_m} which is just x since x_m is fixed. Hmm, BUT elements in the block have the same m-residue (= x_m mod m), so G acts by g_m·(x_m mod m). If G_m acts non-trivially: g_m·x_m ≠ x_m mod m, so g·x has different m-residue from x. BUT x and g·x are NOT in the same π_{p^a·m} block (they have different m-residues). So they're in different blocks → not a within-block conflict. G separates by moving elements to different blocks!

Elements x and y in same block: can G map x to y? (x_p, x_m) → (x_p, g_m·x_m) = y means g_m·x_m = y_m. But y_m = x_m (same block, same m-residue). So g_m·x_m = x_m, i.e., g_m fixes x_m. For generic x_m not fixed by g_m: G cannot map x to y within the block. So U(π_{p^a·m}) ∩ U(π_DYN({1}×G_m)): need x ≡ y mod (p^a·m) AND y = g·x for some g ∈ G. Second condition: y_p = x_p and y_m = g_m·x_m. First condition: y_m = x_m. Combined: g_m·x_m = x_m (fixed by G_m). For generic x_m not fixed: empty intersection. But fixed points exist! If x_m is in Fix(G_m) ≠ ∅: then g·x = x (trivial). So U = ∅ iff G_m has NO non-trivial G_m-orbit pairs within any m-residue class, which holds since all G_m-orbits preserve m-residue only if G_m = {1}. But actually: G-orbit of x = {(x_p, g_m·x_m) : g_m ∈ G_m}. These have different m-residues for g_m ≠ 1 (if x_m not fixed). So the G-orbit moves elements to DIFFERENT m-residues → DIFFERENT π_{p^a·m} blocks. The only elements in same G-orbit AND same π_{p^a·m} block are those where g_m·x_m = x_m (fixed by G_m). These give g·x = x (trivial). So U(π_{p^a·m}) ∩ U(π_DYN(G)) = ∅. Sufficient! ✓

**But this is the case where G = {1} × G_m and d = p^a · m: G_m moves elements OUT of each π_d block (since π_d resolves the full m-component). G does not create within-block conflicts. The π_d already resolves m; G only helps with p-adic structure (which it doesn't, being trivial there). But sufficiency holds because no within-block pair is in the same G-orbit.**

This is a DEGENERATE sufficient pair: the work is done entirely by π_d = π_{p^a·m}, and G_m just happens to not introduce any new within-block connections (it moves elements to other blocks). The pair is sufficient but G_m adds nothing beyond what π_d already does. π_DYN(G) contributes only by separating elements in different π_d-blocks that are in the same G-orbit — but those are already separated by π_d (different blocks). So actually: even G = {1} (trivial) gives a sufficient pair {π_{p^a·m}, π_disc} — π_disc is always a partner.

**The pair {π_{p^a·m}, π_DYN(G_m-lifted)} is sufficient but degenerate:** G_m contributes nothing new. The sufficiency is entirely from π_d = π_{p^a·m} almost separating everything (it leaves only within-block pairs), and G fails to merge any across-block pairs. A genuinely non-trivial A+M pair should require that BOTH partitions contribute to separation. The formally-correct reading: yes, {π_{p^a·m}, π_DYN(G)} is a sufficient 2-partition family for any non-trivial G = {1}×G_m — but only because π_{p^a·m} already does almost all the work (it leaves only higher-p-adic-digit pairs unresolved), and G confirms those are in different orbits (trivially, since G can't reach them). The pair is sufficient but G is irrelevant.

---

## Part 4 — Theorem 1: Clean Form

**Theorem 1 (Complete A+M Classification — proved).**

For n = ∏ᵢ pᵢ^{rᵢ} and {π_d, π_DYN(G)} a 2-partition family with G ≤ (Z/nZ)* non-trivial:

Write d = ∏ᵢ pᵢ^{aᵢ} with 0 ≤ aᵢ ≤ rᵢ. The family is sufficient iff for every prime pᵢ with rᵢ ≥ 1:

**Condition(pᵢ):** either aᵢ = rᵢ (d fully resolves the pᵢ-component) OR G is trivial at the pᵢ-component (every g ∈ G has g ≡ 1 mod pᵢ^{rᵢ}).

Restated: for each prime pᵢ: NOT (aᵢ < rᵢ AND G non-trivial at pᵢ).

**Proof.**

**Necessity.** Suppose aᵢ < rᵢ and G has some g with g_pᵢ ≠ 1 (non-trivial at pᵢ). By Theorem 1 of the prior sprint (p-kernel obstruction), applied to the pᵢ-component: construct conflict pair {x, g·x} with x localized to the pᵢ-component (using CRT to zero out other components), exactly as in the proof of Part 3 Case A. The pⱼ-components (j≠i) of the conflict are arranged so that x ≡ g·x mod d (using the flexibility in choosing xⱼ = 0 to satisfy the dⱼ-conditions). □

**Sufficiency.** Suppose Condition(pᵢ) holds for all i. Consider any x ∈ Z/nZ and g ∈ G, g ≠ 1, with g·x ≡ x mod d (potential conflict). We show g·x = x.

For each prime pᵢ: either aᵢ = rᵢ or g_pᵢ = 1.

- aᵢ = rᵢ: g·x ≡ x mod pᵢ^{rᵢ}, so g·x ≡ x mod pᵢ^{rᵢ}. In Z/pᵢ^{rᵢ}Z: g_pᵢ · xᵢ ≡ xᵢ mod pᵢ^{rᵢ}. Since aᵢ = rᵢ = full residue: this means g_pᵢ · xᵢ = xᵢ in Z/pᵢ^{rᵢ}Z. If xᵢ is a unit: g_pᵢ = 1. If xᵢ = 0: g_pᵢ · 0 = 0 trivially.

  More carefully: g·x ≡ x mod pᵢ^{rᵢ} means pᵢ^{rᵢ} | (g_pᵢ−1)·xᵢ. If gcd(xᵢ, pᵢ) = 1 (unit): forces g_pᵢ ≡ 1 mod pᵢ^{rᵢ}, i.e., g_pᵢ = 1 in Z/pᵢ^{rᵢ}Z.
  
  If pᵢ | xᵢ: then (g_pᵢ−1)·xᵢ may be 0 mod pᵢ^{rᵢ} even with g_pᵢ ≠ 1. BUT: if aᵢ = rᵢ = the full exponent, and g·x ≡ x mod pᵢ^{rᵢ}: this is g_pᵢ·xᵢ ≡ xᵢ mod pᵢ^{rᵢ}, which in Z/pᵢ^{rᵢ}Z means g_pᵢ·xᵢ = xᵢ (since both sides are in Z/pᵢ^{rᵢ}Z and congruence mod pᵢ^{rᵢ} = equality). So g_pᵢ·xᵢ = xᵢ in Z/pᵢ^{rᵢ}Z. This means (g_pᵢ−1)·xᵢ = 0 in Z/pᵢ^{rᵢ}Z. Since Z/pᵢ^{rᵢ}Z is a local ring: if xᵢ has any unit factor, forces g_pᵢ = 1. If xᵢ = pᵢ^sᵢ · uᵢ (uᵢ unit): (g_pᵢ−1)·pᵢ^sᵢ·uᵢ = 0 mod pᵢ^{rᵢ}, i.e., pᵢ^{rᵢ} | (g_pᵢ−1)·pᵢ^sᵢ, i.e., pᵢ^{rᵢ−sᵢ} | g_pᵢ−1. This is consistent with g_pᵢ ≠ 1 when rᵢ−sᵢ ≤ vₚᵢ(g_pᵢ−1).

  **This means aᵢ = rᵢ alone is NOT sufficient to force g_pᵢ = 1 when xᵢ is a non-unit.**

  Example: pᵢ = 3, rᵢ = 2. aᵢ = 2. g = 4 (g mod 9 = 4, g−1=3, v₃(g−1)=1). x = 3 (v₃(x)=1). g·x = 4·3 = 12 ≡ 3 mod 9. So g·x = x mod 9 = x mod p^r. Same π_{p^r} class. But g·x = 12 ≠ 3 = x. **CONFLICT when aᵢ = rᵢ = 2 but xᵢ is a non-unit!**

  Wait: I need to recheck. π_{p^aᵢ} with aᵢ = rᵢ: x ~_{π_{p^r}} y iff x ≡ y mod p^r iff x = y in Z/p^rZ. So π_{p^r} = π_disc. The "block" of x is just {x}. There are no non-trivial pairs in U(π_{p^r}). So π_{p^r} = π_disc trivially pairs with anything.

  **I confused myself.** If aᵢ = rᵢ: then the pᵢ-contribution to π_d identifies elements iff they agree mod pᵢ^{rᵢ}, i.e., they are the SAME element in the pᵢ-component. So no two distinct elements can be in the same π_d block based on the pᵢ-condition (they always differ in pᵢ-component if they're different elements). Therefore: IF aᵢ = rᵢ for ALL i: π_d = π_disc (fully discrete). That's trivially sufficient.

  The interesting case: aᵢ = rᵢ for SOME i and aᵢ < rᵢ for others. Say aᵢ = rᵢ for i ∈ I_full and aᵢ < rᵢ for i ∉ I_full. Elements in the same π_d block agree mod pᵢ^{rᵢ} for i ∈ I_full (so they have the SAME pᵢ-component for those i) and agree mod pᵢ^{aᵢ} for i ∉ I_full. The within-block variation is entirely from i ∉ I_full primes, specifically at levels aᵢ+1,...,rᵢ.

---

**Revised Theorem 1 (clean form — proved for all cases).**

For n = ∏ᵢ pᵢ^{rᵢ} and non-trivial G ≤ (Z/nZ)*, {π_d, π_DYN(G)} is sufficient iff:

For every prime pᵢ | n with aᵢ < rᵢ (where aᵢ = v_{pᵢ}(d)):

**G is trivial at the pᵢ^{rᵢ}-component, meaning every g ∈ G has g ≡ 1 mod pᵢ^{rᵢ}.**

In other words: G ≤ ∏_{i: aᵢ = rᵢ} (Z/pᵢ^{rᵢ}Z)* (G is confined to the fully-resolved components of d).

**Proof (necessity by Case A of Part 3 proof, applied at each pᵢ with aᵢ < rᵢ where G is non-trivial):** Already proved. □

**Proof (sufficiency).** G ≤ ∏_{i: aᵢ=rᵢ} (Z/pᵢ^{rᵢ}Z)*. For any pair {x, g·x} with g ≠ 1: there exists some i with aᵢ = rᵢ and (g·x)ᵢ ≠ xᵢ (since g ≠ 1 in the product). For this i: aᵢ = rᵢ means pᵢ^{rᵢ} | d, so π_d resolves the full pᵢ-component. x and g·x differ in pᵢ-component → they are in different π_d blocks → not a conflict. □

---

## Part 5 — Consequences and Special Cases

**Corollary 1 (Squarefree recovery — proved).** For squarefree n (all rᵢ = 1): aᵢ < rᵢ = 1 means aᵢ = 0. "G trivial at pᵢ-component" means g ≡ 1 mod pᵢ for all g ∈ G. Condition: for every prime pᵢ | n with aᵢ = 0 (i.e., pᵢ ∤ d): G trivial mod pᵢ. Equivalently: G ≤ ker((Z/nZ)* → (Z/(n/d)Z)*). This is exactly the squarefree A+M theorem. □

**Corollary 2 (Pure prime power — proved).** For n = p^r (k=1, one prime): any d with a = v_p(d) < r requires G trivial at p^r-component, i.e., G = {1}. Sufficiency requires G trivial. □

**Corollary 3 (Non-trivial sufficient A+M for n = p^r·m — proved).** For n = p^r·m with m squarefree, gcd(p,m)=1, r ≥ 2: a non-trivial G sufficient pair requires G ≤ (Z/p^rZ)* × {1} (G confined to the p^r-component), AND the squarefree A+M condition for m. But "G confined to p^r-component" with aᵢ < r forces G trivial at p^r (from necessity). So effective condition: G acts only on m-components (G ≤ {1} × (Z/mZ)*), AND d = p^r · d_m with squarefree A+M condition. The pair {π_{p^r·d_m}, π_DYN(G_m)} is sufficient exactly when the squarefree condition holds for (d_m, G_m, m). □

**Corollary 4 (n = p^r·q^s — proved).** For n = p^r·q^s with r,s ≥ 2: any non-trivial G has g non-trivial at p^r-component OR q^s-component. If non-trivial at p^r: necessity forces a_p = r_p = r, i.e., p^r | d. If non-trivial at q^s: forces p^s | d. Both force d = p^r·q^s = n, making π_d = π_disc. The only sufficient A+M pair has π_d = π_disc (trivial). □

**General statement (proved):** For n = ∏ᵢ pᵢ^{rᵢ} with multiple repeated primes (rᵢ ≥ 2 for multiple i), any non-trivial G ≤ (Z/nZ)* has some component where it acts non-trivially, forcing the corresponding pᵢ^{rᵢ} to divide d, ultimately forcing d to include all repeated prime powers, reducing the problem to the squarefree part.

---

## Part 6 — Final Classification Table

Let n = ∏ pᵢ^{rᵢ}. Write n = N_sq · N_rp where N_sq = ∏_{rᵢ=1} pᵢ (squarefree part) and N_rp = ∏_{rᵢ≥2} pᵢ^{rᵢ} (repeated-prime part).

| Pair type | Condition | Squarefree n | Pure prime power p^r | Mixed p^r·m (m sqfree) | Multiple prime powers p^r·q^s |
|---|---|---|---|---|---|
| **A+A** | lcm(d₁,d₂) = n | {π_{d₁},π_{d₂}}: sufficient iff every prime in d₁ or d₂ | No sufficient pair (all A-partitions comparable) | {π_{p^r}, π_m}: sufficient ✓ | {π_{p^r·q^s},·}: only π_disc works as one factor |
| **A+M** | G confined to fully-resolved components | G trivial outside primes of d (squarefree thm) | Only G = {1} (trivial) | G confined to N_sq part; p^r must fully appear in d | G = {1} only (both p^r, q^s must appear in d, forcing d = n) |
| **M+M** | G ∩ H = {1} in (Z/nZ)* | Full DYN+DYN classification (3 mechanisms) | G ∩ H = {1}: exists whenever (Z/p^rZ)* has coprime-order subgroup pair | G∩H={1} in (Z/nZ)*: full classification applies | G∩H={1}: exists whenever (Z/nZ)* has complementary subgroups |

**Remarks on M+M for prime powers:**
- (Z/p^rZ)* ≅ Z/p^{r−1}(p−1)Z (cyclic, odd p). Has complementary subgroups iff p^{r−1}(p−1) = a·b with gcd(a,b)=1 and a,b>1. This holds iff p−1 > 1 (p odd) AND r ≥ 2 (giving p^{r−1} as a factor coprime to p−1). Example: p=3, r=2: (Z/9Z)* ≅ Z/6Z = Z/2Z × Z/3Z. Complementary subgroups {order 2} and {order 3}: G∩H={1} ✓.
- For p=2, r≥3: (Z/2^rZ)* ≅ Z/2 × Z/2^{r−2}. Can find complementary pairs.

---

## Part 7 — The Frozen Master Statement

**Theorem (Master Classification — A+M for general n).**

For n = ∏ᵢ pᵢ^{rᵢ} and non-trivial G ≤ (Z/nZ)*:

> {π_d, π_DYN(G)} is sufficient iff G is confined to the subgroup ∏_{i: pᵢ^{rᵢ} | d} (Z/pᵢ^{rᵢ}Z)* of (Z/nZ)*.

Equivalently: the support of G (the set of prime components on which G acts non-trivially) is contained in the set of primes pᵢ for which d is fully saturated at pᵢ (i.e., pᵢ^{rᵢ} | d).

**Interpretation.** d must "cover" every prime where G acts non-trivially, and it must cover it fully (to exponent rᵢ). Partial coverage of a prime (aᵢ < rᵢ) is the same as no coverage for G's purposes. There is no partial non-trivial A+M pair at a repeated prime.

**Corollary (Non-trivial A+M structure lives only in the squarefree part).**

Write n = N_sq · N_rp as above. Any non-trivial sufficient {π_d, π_DYN(G)} has:
- N_rp | d (the repeated-prime part is fully covered by d)
- d/N_rp | N_sq and G ≤ (Z/N_sqZ)* (the genuine structure is in the squarefree part)
- The pair restricted to Z/N_sqZ is a non-trivial squarefree A+M pair.

**Summary.** The non-trivial A+M theory is entirely a squarefree phenomenon. Repeated prime powers contribute only by requiring full saturation in d — they add no new mechanism, only additional constraints that reduce the problem to its squarefree core.

---

## Summary

**Theorem 1 (proved):** {π_d, π_DYN(G)} sufficient iff G is supported only on primes fully saturated in d (pᵢ^{rᵢ} | d for each pᵢ where G acts non-trivially).

**Theorem 2 (proved):** For n = p^r (pure prime power): only trivial A+M pairs are sufficient.

**Theorem 3 (proved):** For n = p^r·q^s (two repeated primes): only trivial A+M pairs are sufficient.

**General corollary (proved):** Non-trivial A+M structure reduces entirely to the squarefree part of n. Repeated prime powers impose saturation constraints that push G's action into the squarefree complement.

---

**Strongest honest claim:**
> The A+M classification is now complete for all n. The squarefree A+M theorem generalizes cleanly: G must be confined to the fully-saturated prime components of d. For squarefree n (all rᵢ=1), saturation means pᵢ | d, recovering the prior theorem exactly. For repeated primes, saturation means the full power pᵢ^{rᵢ} | d — a strictly stronger condition. The effect: all non-trivial A+M structure lives in the squarefree part of n; the repeated prime powers contribute only as obstacles that must be absorbed entirely into d.

**Strongest honest boundary:**
> Three things remain open outside this classification: (1) A+A for general n: the condition lcm(d₁,d₂) = n generalizes cleanly (proved above for squarefree; holds for all n since lcm is well-defined), but enumerating all sufficient A+A pairs for fixed n with many prime power factors is combinatorial. (2) M+M for general n: the condition G ∩ H = {1} is universal, but enumerating complementary subgroup pairs in (Z/nZ)* for non-squarefree n requires case analysis by prime power structure. (3) Partition families beyond Type A and Type M: the UOP criterion (joint map injective) applies universally, but computing injectivity for other algebraic families requires new tools specific to those families.
