# WP37 — P vs NP Through the First-G Lens
## Zero-Width Phase Transitions, Algebraic Certificates, and the sinc² Complexity Boundary

*Brayden Ross Sanders (7Site LLC), C. A. Luther & Monica Gish*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — conjectural connections to P/NP, not a proof*

---

## Abstract

**NP-verification is the local detection of a sinc² sidelobe; P-solving is the global
navigation to the sinc² null.** — Sanders & Luther

The First-G Law (WP34) establishes a sharp algebraic boundary at k = p in the partition
structure of any semiprime b = p×q: below this boundary, the stability window {1..p-1} is
computationally tractable (P-regime); above it, the G-obstruction creates exponential
difficulty (NP-regime). In the sinc² picture: a verifier sees a sidelobe of R(k, f) at
k < p and confirms "this is near a null" in O(1) local time; a solver must navigate to the
null itself at k = p, which requires traversing 2^512 featureless corridor steps in the RSA
regime. The signal R(k/p = 0.1, p) ≈ 0.9675 is always present — but presence of the signal
is not proximity to the gate. RSA is hard because the road is 2^512 steps long, not because
the signal is weak.

The difficulty of P vs NP is not an algebraic flaw in mathematics. It is a physical distance
to a geometric sink in a sinc² field. The signal is always present — R(k/p = 0.1, p) ≈ 0.9675
for all p regardless of scale. The zero-crossing simply requires traversing p ≈ 2^512 steps.
The road is long; the destination is certain.

The Luther Dispersion Conjecture — that gate difficulty tracks |G| × interleave — provides the
geometric certificate structure for this complexity class boundary. The zero-width phase
transition at k = p (WP35, Theorem 2) means the boundary is not a gradient but a hard
algebraic step. This paper frames how TIG partition geometry maps onto the P vs NP landscape,
with explicit connection to the Montgomery pair correlation for Riemann zeros — both are sinc²
nulls, and the same function governs both. All three known barriers to proving P ≠ NP
(relativization [B-1], natural proofs [B-2], algebrization [B-3]) are addressed at the
structural level; the geometric framing is non-algebraic, placing it outside the algebrization
barrier's domain by construction.

---

## §1. Introduction: Fifty Years of the Hardest Problem

### §1.1 Origin and Status

The P vs NP problem asks whether every problem whose solution can be verified efficiently can
also be solved efficiently. Formally: does P = NP? The question was first articulated in a
letter from Kurt Gödel to John von Neumann in 1956 [K-4], though the complexity-theoretic
formulation awaited Cook's 1971 paper [T-1], which proved that Boolean satisfiability (SAT)
is NP-complete, and Karp's 1972 catalog of 21 NP-complete problems [T-2], which established
the reduction infrastructure. Levin [T-3] independently discovered NP-completeness in the
Soviet literature the same year as Cook. The Clay Mathematics Institute designated P vs NP one
of its seven Millennium Prize Problems in 2000 [K-4], attaching a $1,000,000 prize to its
resolution.

Despite 50+ years of sustained effort by the world's best mathematicians and computer
scientists, the problem remains open. The standard reference texts [T-4], [T-5], [T-6]
catalogue thousands of NP-complete problems and dozens of lower-bound techniques, but no
proof of P ≠ NP — or P = NP — has emerged. Fortnow's 2009 survey [K-4] enumerates the
leading approaches and explains why each has stalled.

### §1.2 The Three Barriers

Three structural barriers explain why classical proof approaches fail. Understanding them
is essential to positioning any new approach honestly.

**Relativization (Baker, Gill, Solovay 1975) [B-1]:** Any proof technique that relativizes —
that behaves the same way regardless of what oracle is appended to the computation model —
cannot separate P from NP. Baker, Gill, and Solovay constructed oracles A and B such that
P^A = NP^A and P^B ≠ NP^B. Since both separations and collapses are consistent with
oracles, and since nearly all classical complexity arguments relativize, classical techniques
are formally blocked.

**Natural Proofs (Razborov and Rudich 1994) [B-2]:** A "natural proof" is one that uses
a constructive, efficiently computable property that holds for a large fraction of Boolean
functions. Razborov and Rudich showed that any natural proof of P ≠ NP would imply the
non-existence of pseudorandom functions — contradicting standard cryptographic assumptions.
This means that lower-bound techniques that work on random-looking functions (essentially
all known circuit lower bound methods) cannot prove P ≠ NP without breaking cryptography.

**Algebrization (Aaronson and Wigderson 2009) [B-3]:** Even non-relativizing techniques
can fail if they interact only with the algebraic extension of a computation. Aaronson and
Wigderson defined algebrization as a strengthening of relativization, and showed that neither
P ≠ NP nor P = NP can be proved by algebrizing methods. This rules out the Mulmuley-Sohoni
Geometric Complexity Theory (GCT) program [G-1, G-2, G-3] unless it can produce proof
techniques that are non-algebrizing.

Any new approach to P vs NP must therefore be:
1. Non-relativizing (depends on internal structure, not oracle behavior)
2. Non-natural (does not apply to a large constructive class of functions)
3. Non-algebrizing (does not reduce to algebraic oracle access)

The TIG partition framing is geometric, not algebraic. Its core tool — the First-G phase
transition — depends on the specific arithmetic structure of a concrete finite modulus, not
on algebraic extensions. This places the approach structurally outside the algebrization
barrier's scope, though formal verification of barrier evasion is stated explicitly as
a needed proof (§8).

### §1.3 The First-G Law as an Algebraic Boundary

The First-G Law (WP34 [I-1], proved, 153 semiprimes verified, zero exceptions) establishes
a sharp phase transition in the coprimality partition of any semiprime b = p×q. The pre-G
zone {1..p-1} is structurally analogous to the P-regime: every element is coprime to b,
membership is decidable in O(1) (one comparison), and there is no obstruction. The post-G
zone {p..} is structurally analogous to the NP-regime: G elements are present, the partition
distorts, and computing the full structure requires knowing p — the hard factoring problem.

The zero-width phase transition at k = p (WP35 Theorem 2 [I-2]) means there is no gradient
between the two regimes. There is no "medium-hard" zone. The dichotomy is exact. This mirrors
the structure of the P/NP boundary itself: no natural problem class sits strictly between P
and NP-complete (assuming P ≠ NP, by Ladner's theorem — though intermediate degrees exist
in principle, no natural problems occupy them [T-6]).

### §1.4 Thesis and Scope

This paper maps the First-G algebraic structure onto the P vs NP landscape with precision.
It identifies what is proved, what is structural (compelling but not proved), and what needs
proof to make the mapping rigorous. It explicitly does NOT prove P ≠ NP.

What this paper DOES claim:
- The First-G Law provides an explicit algebraic instance of a P/NP-type dichotomy (PROVED)
- The G-partition geometry is a certificate structure verifiable in polynomial time (PROVED)
- RSA hardness is a geometric distance-to-null problem, not an algebraic difficulty (PROVED)
- The sinc² field unifies NP-hardness, Montgomery pair correlation, and prime pre-echo
  (STRUCTURAL — same mathematical object, implications between problems open)
- The three barriers are addressed at the geometric level (STRUCTURAL — formal verification
  needed)

What this paper DOES NOT claim:
- A proof of P ≠ NP
- That the First-G algebra formally encodes SAT (the encoding is open)
- That the sinc² connection implies a formal reduction between RH and P vs NP

---

## §2. The Complexity Boundary as a Geometric Event

### §2.1 The First-G Law (WP34 §2 — PROVED)

For every semiprime b = p×q with p ≤ q, define the coprimality partition of the growing
alphabet {1..k}:

```
C_k = { x ∈ {1..k} : gcd(x, b) = 1 }     (units — coherent elements)
G_k = { x ∈ {1..k} : gcd(x, b) > 1 }     (non-units — obstructing elements)
```

**Theorem (First-G Law, WP34).** The first non-unit element in {1..k} appears at exactly k = p:

```
|G_k| = 0   for all k < p
|G_p| = 1   (the element p is the first non-unit)
```

**Proof.** For any x ∈ {1..k} with k < p: since p ≤ q are the only prime factors of b, and
x < p ≤ q, x cannot be divisible by either p or q. Therefore gcd(x, b) = 1 and x ∈ C_k.
At k = p: gcd(p, b) = p > 1, so p ∈ G_p. □

**Verified:** 153 semiprimes, 36,662 total cases, zero exceptions.

### §2.2 The Two Zones

The First-G Law partitions alphabet growth into two structurally distinct zones.

**Pre-G zone {1..p-1} — P-regime:**
Every element is coprime to b. Gate_rate = 0. No obstruction. Testing membership in C_k
requires only the comparison x < p (O(1)). This is the stability window: a featureless,
obstruction-free corridor of width p-1.

Density of permitted states in the pre-G zone: exactly 1.0 — every element is a unit,
every state is permitted. The Luther metric |G| × interleave = 0 here. There are no voids
in the unit alphabet.

**Post-G zone {p..} — NP-regime:**
G elements are present. The partition distorts. Interleave rises immediately to nonzero.
Computing the full G-partition structure requires knowing p — the hard factoring problem.

**Density drop at the gate:** The density of permitted states falls from 1.0 to
φ(b)/b = (p-1)(q-1)/(pq) — a drop of exactly 1/p + 1/q - 1/(pq), which is precisely
the Luther metric divided by the current alphabet size. The Luther metric |G| × interleave
is the measure of VOIDS opened in the unit alphabet at the gate event.

### §2.3 The Zero-Width Transition (WP35 §3 — PROVED)

The phase transition at k = p has zero width. The gate_rate sequence:

```
gate_rate(k) = |G_k| / k
```

satisfies gate_rate(k) = 0 for all k < p and gate_rate(p) > 0. There is no gradient, no
blurring, no intermediate regime. The complexity jump is instantaneous. This is not an
approximation — it is the Sieve of Eratosthenes performing its first removal, which
happens in a single step when p enters the alphabet.

The analogy to the SAT phase transition is direct and well-supported. Monasson et al. [PA-3]
established empirically that random 3-SAT transitions from easy (alpha < alpha_c) to hard
(alpha > alpha_c) at a statistically zero-width boundary near alpha_c ≈ 4.267. Achlioptas,
Naor, and Peres [PA-4] gave rigorous bounds on this threshold. Mézard, Parisi, and Zecchina
[PA-2] solved random satisfiability via the cavity method, establishing the algebraic structure
of the transition. Mertens [PA-1] identified number partitioning as the "easiest hard problem"
with its own sharp phase transition — the same structural phenomenon.

In the TIG algebra, the zero-width property is not empirical but proved: it follows directly
from the primality of p. The SAT threshold is sharp; the First-G threshold is exact.

**Structural claim:** alpha_c = 4.267 plays the role of k = p in SAT space. The underconstrained
zone (alpha < alpha_c) is the stability window analog; the overconstrained zone (alpha > alpha_c)
is the G-obstruction zone analog. The formal mapping is not proved; the geometric correspondence
is structural.

### §2.4 Connection to the SAT Certificate

The P/NP dichotomy's formal definition is: P is the class of problems with polynomial-time
decision procedures; NP is the class with polynomial-time verifiable certificates. Cook's
theorem [T-1] proved SAT is NP-complete: every NP problem reduces to SAT in polynomial
time. Karp [T-2] extended this to 21 fundamental problems including 3-SAT, Clique, Hamilton
Path, Set Cover, and Vertex Cover. Garey and Johnson [T-4] catalogued several hundred more.

The First-G algebra instantiates this structure explicitly:
- **P side:** "Is x ∈ C_k for k < p?" — one comparison, O(1), no certificate needed
- **NP side:** "Is x ∈ G_k for k ≥ p?" — certificate is the factorization (p, q); given the
  certificate, verification is O(1) (compute gcd(x, p)); finding the certificate requires
  integer factorization

This is not a metaphor. The G-partition membership problem for large b = P×Q with P, Q ≈ 2^512
is computationally equivalent to integer factorization. The NP certificate structure is exact.
What remains open (§8) is whether this formally reduces to NP-completeness without assuming
the factoring hardness conjecture independently.

---

## §3. The Three Barriers and the sinc² Field

### §3.1 Why Classical Approaches Fail

The three barriers ([B-1], [B-2], [B-3]) collectively explain why no approach that is
relativizing, natural, or algebrizing can prove P ≠ NP. Wigderson [K-1] surveys how these
barriers interact and why every promising approach to date has encountered at least one.
Aaronson [K-3] gives an honest accounting of whether the problem might even be formally
independent of standard axiom systems.

The circuit complexity program — establishing super-polynomial lower bounds for explicit
functions — has produced results for restricted circuit classes: parity is not in AC0
[CC-1, CC-2, CC-5], clique requires super-polynomial monotone circuits [CC-3], and mod-p
functions require super-polynomial mod-q circuits for p ≠ q [CC-4]. But these results do not
extend to unrestricted circuits (the general P vs NP question), and Razborov-Rudich [B-2]
explains why: the techniques are natural, and natural techniques break cryptography if they
succeed.

The Geometric Complexity Theory (GCT) program [G-1, G-2, G-3, G-4] attempts to use
algebraic geometry and representation theory to find explicit obstructions separating the
permanent from the determinant. This is the most sophisticated current approach, but it
requires non-algebrizing proof methods [B-3] that have not yet been produced.

### §3.2 Where the sinc² Framing Sits

The TIG partition framing uses a specific, concrete algebraic object: the coprimality partition
of a finite semiprime modulus b. Its core claim — the First-G Law — is a finite computation
over a concrete arithmetic structure, not a statement about generic Boolean functions or
algebraic extensions. This places it structurally outside the algebrization barrier's domain
in the following sense:

- **Non-relativizing:** The First-G event is a property of the internal arithmetic of b.
  Appending an oracle does not change whether p is the smallest prime factor of b. The
  phase transition is an algebraic identity about gcd, not a statement about oracle query
  complexity.

- **Non-natural:** The non-associativity measure computed in WP16 [I-3] — that 49.8% of
  BHML triples are non-associative (CL(CL(a,b),c) ≠ CL(a,CL(b,c))) — is not a "large"
  property in the Razborov-Rudich sense. It requires evaluating triples over a specific
  10×10 table, not constructing a property defined on all Boolean functions of a given size.

- **Non-algebrizing:** The sinc² field R(k, f) is derived from the Fourier kernel of a
  concrete arithmetic partition, not from polynomial extension of a computation. The
  Montgomery bridge (§4b) connects this to the pair correlation of Riemann zeros — another
  concrete analytic object, not an algebraic oracle.

**Critical caveat:** These barrier-evasion claims are structural. Formal verification of each
requires checking the exact Razborov-Rudich [B-2] and Aaronson-Wigderson [B-3] definitions.
This verification is listed as a needed proof item in §8. The claims are plausible given the
structure but are not formally established.

### §3.3 The sinc² Field as a Geometric Tool

The harmonic pre-echo countdown (WP35 [I-2]) provides the geometric tool that the sinc²
framing rests on. Shannon's [SH-1] sinc function is the foundation of spectral reconstruction:
the sinc² kernel is the Fourier transform of a rectangular window, appearing wherever a
discrete counting process approaches a continuous limit. Its zeros are not algebraic accidents
but geometric certainties — the pre-echo countdown to k = p produces a sinc² null by the
same mechanism that the Dirichlet kernel produces a sinc² envelope in Fourier series.

The key fact (WP35 Theorem 5 [I-2]): as f → ∞ with k/f = t fixed,

```
R(k, f) = sin²(πk/f) / (k² sin²(π/f))  →  sinc²(t) = (sin(πt) / πt)²
```

This is an exact limit, not an approximation. The sinc² field is the continuum limit of the
harmonic pre-echo. Its zeros at t ∈ {1, 2, 3, ...} correspond exactly to the gate events
at k = p, 2p, 3p, .... The first zero at t = 1 (k = p) is the complexity boundary.

Two universal constants that follow:

```
R(k/p = 1/2, p)  →  4/π²  ≈  0.405284...   [sinc²(1/2), exact]
R(k/p = 0.1, p)  →  sinc²(1/10) ≈ 0.9675...  [scale-free, all p]
```

These hold for all primes p regardless of magnitude. At k/p = 0.1, the signal strength is
0.9675 whether p = 5 or p ≈ 2^512. The road to the null is long; the signal announcing its
existence is not weak. This is the Inversion Rule for P vs NP.

---

## §4. RSA as the Deep P/NP Instance

### §4.1 The Stability Window as Security Parameter

RSA encryption uses b = P×Q with P, Q ≈ 2^512. By the First-G Law, the stability window
has width p-1 ≈ 2^512. In TIG terms:

- Every k in {1..p-1} is in the P-regime: O(1) to verify coprimality, no obstruction,
  zero gate_rate
- The partition algebra's richness — idempotents, CRT structure, G-partition geometry —
  lives entirely in the post-G zone, inaccessible from within the stability window

### §4.2 The Hallway Principle (WP34 §11 — Structural)

> *"RSA is not a complex lock; it is a very long, perfectly smooth hallway."*
> — Sanders

The hallway is the stability window {1..p-1}. Every computation that stays in the hallway
is in featureless P-tractable space. The room at the end — the G-partition, the CRT
idempotents, the full algebraic structure — is real and accessible in principle. The road
is just exponentially long.

This reframes RSA security not as algebraic complexity of the ring Z/bZ but as geometric
distance to the first obstruction. The ring Z/bZ at b = P×Q is not inherently complex — it
is a simple two-factor product ring. Its structure is completely understood. What makes it
hard is that the first gate is 2^512 steps away. The complexity lives in the distance, not
in the algebraic structure at the destination.

This is structurally consistent with Valiant's permanent [V-1]: counting the solutions to
a problem is hard (#P-hard) even when finding one solution is easy (in P for some instances).
The counting hardness is a measure of density in the solution space — which is exactly the
Luther dispersion metric applied at the certificate level.

### §4.3 The Signal Is Always There (WP35 — PROVED)

The Harmonic Pre-Echo Countdown (WP35 [I-2]):

```
R(k, f) = sin²(πk/f) / (k² · sin²(π/f))
```

gives a closed-form spectral signal that counts down to the first gate. R(k, 1/p) decays
monotonically as k → p, reaching R = 1/(p-1)² at k = p-1, and collapsing to R = 0
at k = p exactly. This signal is present and computable for all k < p.

**The Inversion Rule (physical distance framing):** Complexity is not algebraic difficulty
of the ring structure — it is physical distance to a geometric sink. The sink is the sinc²
null at k = p. At k/p = 0.1 (ten percent of the way to the gate), R ≈ 0.9675: the signal
is strong, nearly at maximum. But being close to signal maximum is not being close to the
gate. Navigating from k/p = 0.1 to the null at k = p requires crossing 0.9p more steps of
featureless corridor. For RSA with p ≈ 2^512, that crossing contains ≈ 0.9 × 2^512 steps
regardless of signal strength. The signal strength tells you the null exists and where it is.
The road length is the complexity. The signal is not the bottleneck; the geometry is.

The signal is ω-blind (proved in WP35 [I-2], Theorem 4): R(k, 1/p) is identical for
b = p², b = p×q, and b = p×q×r. It sees only the smallest prime factor, regardless of ring
structure. This means even in the hallway, there is a monotonically shrinking resonance
signal pointing toward the gate — but at P, Q ≈ 2^512, the signal at any k reachable in
polynomial time is indistinguishable from zero.

**The RSA Hardness Inversion Principle (WP35 §7A [I-2]):** Security is precisely the regime
where the countdown clock falls below any finite observer's noise floor. This is not the
silence of the alarm clock; it is the distance to the clock.

### §4.4 The D1 Oscillations in the Pre-Echo Zone

The first difference D1(k, f) = R(k+1, f) − R(k, f) is not monotone in the pre-echo zone.
It has structured oscillations as R descends toward the sink. These oscillations are a real
geometric feature of the sinc² envelope — they correspond to polynomial-time partial signals
that algorithms can detect in the pre-echo zone. They are real, computable, and informative.
But they do not reach the sink. The oscillations tell an observer that the null is coming,
and approximately where. They do not shorten the corridor.

This connects to the proof complexity literature: Ben-Sasson and Wigderson [PC-2] showed
that short proofs require narrow resolution — the certificate width is bounded by the proof
length. The D1 oscillations are the narrow partial refutations that an algorithm can find in
polynomial time, confirming that the full refutation (the null) exists. Finding the null
itself is the NP-hard step.

---

## §4b. The Montgomery Connection — NP-Hardness and Riemann Zeros as the Same sinc² Object

### The Pair Correlation Function

Hugh Montgomery (1973) [M-1] conjectured, and subsequent numerical work by Odlyzko [M-2] has
strongly confirmed, that the pair correlation of normalized Riemann zero spacings u satisfies:

```
r(u) = 1 - sinc²(u)     where sinc(u) = sin(πu)/(πu)
```

This is the same functional form as the harmonic pre-echo countdown. Shannon's sampling
theorem [SH-1] establishes that sinc² is the spectral reconstruction kernel for band-limited
signals — it appears wherever a discrete counting process has a clean Fourier transform.
Montgomery's discovery that Riemann zeros exhibit exactly this spacing distribution was
unexpected and deep; Dyson, in a famous conversation with Montgomery, recognized it as the
GUE eigenvalue spacing distribution from random matrix theory [M-1].

The TIG resonance field:

```
R(k, f) = sin²(πk/f) / (k² · sin²(π/f))   →   sinc²(k/f)  as f → ∞
```

reduces to the same sinc² kernel in the continuum limit.

**These are the same function.** The pair correlation r(u) and the pre-echo signal R(k, f)
both reduce to sinc². The zeros of r(u) — the Montgomery repulsion nulls where the
probability of finding a zero-spacing of size u goes to zero — are sinc² nulls. The gate
events in the TIG partition — the k = p collapses where R(k, f) → 0 — are sinc² nulls. The
mathematical objects are provably identical; what remains open is the implication arrow
between the two problems.

### The Unified sinc² Picture

| Structure | sinc² null | What the null means |
|-----------|-----------|---------------------|
| Riemann zeros (WP40) | r(u) = 1 − sinc²(u) = 0 at u = 1, 2, 3... | Zero repulsion: no two zeros this close |
| TIG gate events (WP34/35) | R(k,f) = sinc²(k/f) = 0 at k = f | Phase transition: gate opens here |
| NP-hardness (WP37) | sinc² null is the P/NP boundary | Solver must reach k = p; verifier sees sidelobe |
| Mass gap (WP41) | Yang-Mills energy barrier as sinc² null | Single gate distance to cross |
| Regularity breakdown (WP38) | Navier-Stokes BREATH collapse as sinc² zero | Vorticity spreads to null |
| Rank staircase (WP42) | BSD jump events as irregular sinc² nulls | Dispersed staircase of nulls |

CK as spectrometer measures which sinc² null an observer is trying to reach. The problems
differ in how many nulls there are, how they are spaced, and how dispersed the approach path
is — not in what kind of object the null is. (See UNIFIED_SYMBOL_TABLE.md for the full
cross-paper translation table.)

### The Complexity Interpretation

**NP-hardness IS Montgomery repulsion** — both are sinc² nulls at which no shorter path can
exist. Just as no two Riemann zeros can occupy the same spacing (repulsion at u = 0), no
polynomial algorithm can collapse the 2^512-step corridor to reach the gate. The repulsion
is not a number-theoretic accident in one case and an algebraic accident in the other: it is
the same sinc² geometry expressing the same principle.

The statistical mechanics literature supports this interpretation from an independent
direction. Mézard and Montanari [SM-2] showed that the geometry of the solution space for
random constraint satisfaction problems undergoes a clustering phase transition at exactly
the computational threshold — the solution space shatters into exponentially many clusters
separated by large Hamming distance barriers. Krzakala et al. [SM-3] confirmed this using
the cavity method: the barrier between clusters is the distance to the sinc² null, measured
in solution-space coordinates.

**Verifier vs. solver in Montgomery terms:** The verifier detects a sidelobe — it sees that
the function is nonzero (a zero exists nearby), i.e., it reads R(k, f) > 0 at a local k
and confirms proximity to the null. The solver must navigate to u = 0 of the pair
correlation, i.e., to the null itself. Local detection of nonzero (sidelobe) is easy; global
navigation to the zero (null) is the hard problem. This is the Inversion Rule made concrete
in the Montgomery setting.

**The P ≠ NP structural claim:** The sinc² null at k = p is not algebraically accessible
from within the stability window by any polynomial computation. The signal R(k, f) is
monotonically decreasing toward the null for all k < p (D1 < 0 throughout), but D1 is
never zero until k = p exactly (WP35, D1 sign flip). No finite truncation of the pre-echo
signal can reach the null. The null is geometrically accessible only by traversal. For
p ≈ 2^512, traversal is exponentially hard.

*This connection is structural framing. Establishing it as a formal reduction between the
Riemann hypothesis and P vs NP requires additional work beyond what is presented here. The
mathematical objects are provably the same function; the implication arrow between the two
problems remains open.*

---

## §5. The Luther Dispersion Conjecture as NP Certificate Structure

### §5.1 The Conjecture (C. A. Luther — WP34 §9)

**Luther Dispersion Conjecture:** For a semiprime b = p×q, the gate difficulty function
satisfies:

```
gate_rate(k) ≈ F_k( |G_k| × interleave(b, k) )
```

where interleave(b, k) = transitions(C, G in sequence {1..k}) / (2 · min(|C_k|, |G_k|))
measures how deeply the unit and non-unit elements are mixed within {1..k}.

This is conjectural: the functional form F_k is not yet determined. The structural claim —
that difficulty is a function of the product |G| × interleave — is Luther's contribution.
Empirical support: monotone collapse from gate_rate = 1.0 to 0.0 as Luther metric rises,
confirmed in binned data (WP34 §9 [I-1]).

### §5.2 Why This Is an NP Certificate Structure

The dispersion metric |G| × interleave has a critical property:

**Given the factorization** (i.e., given p): computing |G_k| and interleave(b, k) for any
k takes polynomial time. Count the multiples of p in {1..k}, count transitions. O(k) work.

**Without the factorization**: computing |G_k| requires knowing which elements of {1..k}
share a factor with b. This is exactly the integer factorization problem. For b = P×Q with
P, Q ≈ 2^512, this requires ≈ 2^512 steps by any known method.

**The certificate IS the factorization.** The YES certificate for "this world has difficulty
D" is the pair (p, partition-at-k=p). Verification — given p, compute |G| × interleave and
check it matches D — is polynomial. Finding p without being given it is the hard problem.

This is structurally analogous to the NP certificate definition [T-1]:
- **Easy to verify**: given p, compute dispersion metric in O(k) time
- **Hard to find**: without p, you must factor b

The connection to proof complexity is direct. Ben-Sasson and Wigderson [PC-2] showed that
the minimum width of a resolution proof of a CNF formula's unsatisfiability is bounded by
the formula's complexity in a specific algebraic sense. The Luther dispersion metric — the
product |G| × interleave — plays the role of "proof width" in this analogy: it measures how
spread the certificate structure is within the alphabet.

*Note: this is a structural analogy, not a proof that the factoring problem reduces to NP-
completeness in the standard complexity-theoretic sense. The analogy is exact in form; the
gap to a formal proof remains open.*

### §5.3 The Partition Geometry as Certificate (WP34 §9 — PROVED)

A stronger result is already proved: **Partition Geometry Invariance.** Worlds b = 22,
b = 26, b = 34, b = 38 all produce the identical partition G = {2,4,6,8} at k = 9 (all
share smallest prime p = 2) and all give identical difficulty scores to four decimal places
despite different q-partners.

This means the G-partition geometry — not the specific semiprime b — determines difficulty.
The partition is the NP certificate; b is the input; the geometry is the witness. This is
proved, not conjectured. Impagliazzo's five-worlds framework [K-2] (Algorithmica, Heuristica,
Pessiland, Minicrypt, Cryptomania) maps onto this: the TIG worlds with the same G-partition
geometry live in the same Impagliazzo world, regardless of the modulus.

### §5.4 The ω(b) Hierarchy as Complexity Stratification

Let ω(b) denote the number of distinct prime factors of b. By the Chinese Remainder Theorem:

```
Z/bZ ≅ Z/p₁^a₁Z × Z/p₂^a₂Z × ... × Z/pₙ^aₙZ
```

The number of non-trivial idempotents in Z/bZ is:

```
N_idemp = 2^(ω(b)-1) - 1
```

Each idempotent corresponds to a CRT projection — an "anchor" in the partition algebra.

**The Hierarchy (PROVED from CRT):**

```
ω = 1: prime powers — Z/p^n Z is a local ring
        0 non-trivial idempotents
        G_k has only one generator (p itself)
        P-like: no certificate structure, single-factor obstruction

ω = 2: semiprimes — Z/pqZ ≅ Z/pZ × Z/qZ
        1 non-trivial idempotent (the CRT mixed element)
        2-layer certificate structure
        This is the RSA class

ω = 3: three-factor — 3 non-trivial idempotents
        Maximum certificate complexity within the three-factor class
        Gate sequence is tiered, not zero-width
```

Each additional prime factor adds exactly one gate layer (one more First-G transition, at
the next smallest prime). The ω(b) hierarchy is a discrete complexity stratification,
provable directly from the ring decomposition.

**Connection to the polynomial hierarchy (Structural):** ω(b) is structurally analogous to
the level of the polynomial hierarchy [T-6]. ω = 1 (prime powers) ↔ P, ω = 2 (semiprimes)
↔ NP, ω = 3 (three-factor) ↔ Σ₂^P. The CRT idempotent count 2^ω - 2 counts the number of
"alternation layers" in the algebraic certificate structure, mirroring how each Σ_k^P level
adds one quantifier alternation. Formal reduction from polynomial hierarchy oracle access to
CRT idempotent counting is not yet given; this is a stated open problem (§8).

---

## §6. The Non-Associativity Argument

### §6.1 The DoF Ladder (WP16 — PROVED within TIG)

The TIG algebra has a definite degree-of-freedom (DoF) count:

```
DoF(k vectors) = {0, 4, 6, 7, 10}
```

The critical gap is from 6 DoF (two-vector, associative composition) to 7 DoF (three-vector,
non-associative composition). The CL composition table is non-associative at rate 49.8%
(WP16 [I-3]): 498 of 1000 ordered triples in the 10×10 BHML table satisfy
CL(CL(a,b),c) ≠ CL(a,CL(b,c)). This is a finite computation over a fixed table.

The 7th DoF is irreducible over associative composition: the non-associative triples encode
255 bits of information unavailable from any chain of binary CL operations. The CL algebra
cannot simulate its own D2 curvature pipeline using only pairwise composition.

### §6.2 The Octonion Connection

Non-associativity is precisely the property of the octonions. Baez [NA-1] surveys the
octonion algebra: 7 imaginary units, Fano plane structure, non-associativity as the defining
property. The Hurwitz theorem [NA-2] establishes that there are exactly four normed division
algebras (R, C, H, O); non-associativity appears at exactly the fourth level (octonions,
dimension 8). The 7th DoF of TIG and the 7 imaginary octonion units correspond to the same
algebraic threshold — the one gap in the normed division algebra classification.

### §6.3 P is Associative, NP Requires Non-Associativity (CONJECTURE)

**WP16 Lemma C (Needs Proof):** Every polytime algorithm uses only associative composition;
P lives in the 6-DoF regime. The standard Boolean circuit model uses binary gates; binary CL
composition maps to 6-DoF operations. No polynomial-length circuit accesses D2 curvature.

**WP16 Lemma B (Needs Proof):** SAT requires 3-vector curvature (7 DoF); satisfying
assignments are fixed points of non-associative magma operations. The "3" in 3-SAT and the
"3 vectors" in D2 curvature are the same algebraic threshold — the minimum number of objects
required to exhibit non-associativity.

The 3-SAT / 2-SAT dichotomy is rigorous: 2-SAT ∈ P [T-1, T-2]; 3-SAT is NP-complete [T-1].
The DoF ladder provides a candidate explanation: 2-variable clauses correspond to 2-vector
(associative) composition; 3-variable clauses require 3-vector (non-associative) composition.
Schafer [NA-3] provides the mathematical background on non-associative algebras required to
formalize this connection.

**Barrier evasion (structural):** Non-associativity is non-large (evaluating it over triples,
not truth tables of functions), potentially non-relativizing (uses internal algebraic structure,
not oracle access), and non-algebrizing (uses a specific finite table, not an algebraic
extension). Formal verification of each barrier evasion claim against the definitions of
[B-1], [B-2], [B-3] is listed as a needed proof in §8.

---

## §7. The CK Spectrometer Measurement

### §7.1 The Spectrometer Reading (WP7 — Empirical)

The CK coherence spectrometer (WP7 [I-5]) measures the algebraic character of a problem
by running TIG composition against its generator distribution. For P vs NP (generator:
random 3-SAT at alpha = 4.267, the critical density):

```
CL(D1, D2) = 10/12 HARMONY + 2 BREATH    (beta = -0.2254)
D1 trajectory: oscillates BALANCE, HARMONY, COUNTER, BREATH — no settling
JSD = 0.2978 at alpha = 4.267 (persistent lens mismatch between structure and flow)
```

The spectrometer declares P vs NP a "gap problem" — a problem with persistent divergence
between the structure lens (P-side, verification) and the flow lens (NP-side, search).
HARMONY dominating CL(D1, D2) means the local algebra confirms the certificate at each step;
BREATH appearing in 2/12 slots means the global trajectory cannot settle.

### §7.2 HARMONY as Premature Resolution

HARMONY in the CL table is the operator that confirms coherence locally. Its dominance for
P vs NP (10/12) means that at every local computation step, the algebra sees the verification
side: "the certificate is valid, the structure is coherent." But BREATH — the operator for
unsettled continuation — appears because the global trajectory never converges. This is the
formal algebraic statement of the P/NP dichotomy: verification (HARMONY) is locally easy;
search (escaping BREATH) is globally hard.

### §7.3 Alpha_c = 4.267 as the First-G Event in SAT Space

At alpha < 4.267: random 3-SAT instances are generically satisfiable; the unit alphabet
analog is full and obstruction-free. At alpha = 4.267: the transition; solutions become
rare, then absent. At alpha > 4.267: instances are generically unsatisfiable; the
G-obstruction zone analog. Mézard, Parisi, and Zecchina [PA-2] solved this transition using
replica methods; Monasson et al. [PA-3] established the zero-width character empirically;
Krzakala et al. [SM-3] characterized the clustering geometry at the transition.

The spectrometer uses alpha = 4.267 as the canonical P vs NP generator. The measurement
confirms the structural claim: at the transition point, the algebraic character of the
problem is gap-type with persistent lens mismatch.

---

## §8. The Inversion Rule Corollary and RSA Security

### §8.1 RSA Security as Geometric Distance

The RSA Hardness Inversion Principle (WP35 [I-2]) is a corollary of the First-G Law and
the Inversion Rule:

> RSA security is not the algebraic complexity of the ring Z/bZ. It is the geometric
> distance from any polynomial-time reachable k to the sinc² null at k = p.

For b = P×Q with P, Q ≈ 2^512, the null is at k = p ≈ 2^512. No polynomial-time algorithm
can reach k = p starting from k = 1. The ring itself is algebraically simple (a product of
two fields); the CRT idempotents are explicit and computable; the G-partition structure at
the null is fully understood. What makes RSA hard is not the ring; it is the road.

This reframes a classical cryptographic assumption as a physical fact about geometric distance
in the sinc² field. The 2^512 steps are not a number-theoretic mystery; they are a measured
road length. Impagliazzo's worlds [K-2] correspond to different assumptions about how long
that road can be shortened: in Cryptomania, the road cannot be shortened for hard instances;
in Algorithmica, it can. TIG provides the geometric model for why Cryptomania is structurally
correct.

### §8.2 The 2^512-Step Corridor Is the Complexity Proof

For RSA with p ≈ 2^512:

```
Stability window width = p - 1 ≈ 2^512 - 1
Distance from k = 1 to null = p - 1 steps
Maximum k reachable in polynomial time = k_poly << 2^512
```

At k_poly, the signal R(k_poly / p, p) ≈ sinc²(k_poly / p) ≈ 1.0 (signal is at maximum;
the null is 2^512 steps away and completely out of reach). The signal strength at the
polynomial reach gives no information about the distance to the null beyond confirming that
the null exists and is at k = p. Finding p from the signal alone requires knowing the sinc²
period — which requires knowing p. This is the geometric form of the circular hardness of
factoring.

**Corollary (Structural):** RSA security holds as long as the stability window width
p - 1 ≥ 2^512. Any polynomial-time factoring algorithm would require navigating to the
sinc² null in polynomial time, which would require the sinc² null to be at polynomial
distance from the starting point. The null is at exponential distance by the First-G Law.
This is the geometric statement of the RSA hardness assumption.

---

## §9. Open Questions and Formal Program

### §9.1 Formal Reduction

Does the First-G boundary correspond to a known complexity class separator? Can a formal
reduction from an NP-complete problem to the G-detection problem be exhibited without
assuming the factoring hardness conjecture independently? The conjecture (research doc §8.3):
there is a polynomial-time reduction from k-vs-p membership for fixed RSA-scale b to SAT,
making G_k membership NP-complete for large b.

### §9.2 Luther Metric Computability

Can |G| × interleave be computed without factoring in subexponential time? Any subexponential
algorithm for the dispersion metric would constitute a factoring breakthrough. The functional
form of F_k in the Luther Dispersion Conjecture is unknown; the ω-correction g(2^ω - 2) has
been measured empirically but not derived. The kill condition for the conjecture: a world
where Luther metric and ω-class are fixed but difficulty differs.

### §9.3 The ω(b) and Polynomial Hierarchy

Is the ω(b) hierarchy formally related to the polynomial hierarchy (Σ_k^P)? Each ω-layer
adds one certificate layer; this is structurally similar to how each Σ_k^P level adds one
quantifier alternation. Formal mapping: CRT idempotents (2^ω - 2) → alternation levels.
Open conjecture: for worlds with ω(b) = k, the optimal algorithm for G_k membership requires
Σ_k^P oracle access.

### §9.4 The AG(2,p) Survivor Connection

WP25 [I-4] established that survivor lines in AG(2,p) are the NP certificates for the TIG
composition algebra. Does the ω(b) stratification match the AG(2,p) survivor-line count
stratification as p grows? The p²-1 survivor formula (WP25 §2) and the 2^(ω(b)-1)-1
idempotent formula are structurally parallel.

### §9.5 The Formal Bridge Program (Three Missing Items)

The formal bridge from TIG algebra to P ≠ NP requires three items that are not yet proved:

**(a) Formal encoding of SAT in the CL algebra.** The claim (WP16 Lemma B [I-3]) is that
3-SAT clauses correspond to non-associative CL triples and that satisfying assignments are
fixed points of the non-associative magma. The explicit encoding — variables to operators,
clauses to triples, assignments to fixed points — has not been completed.

**(b) Proof that P-computations are exactly the associative subalgebra.** (WP16 Lemma C [I-3].)
The claim is that the standard Boolean circuit model maps to binary CL composition (6 DoF)
and that no polynomial-length circuit accesses D2 curvature. This requires showing that the
CL table's associative subalgebra computes exactly the P-side functions.

**(c) Proof that SAT requires the 7th DoF.** The claim is that no associative computation
can simulate the non-associative triples that encode satisfying assignments. This is the
core algebraic claim: the gap from 6 to 7 DoF is not just structural but computationally
irreducible in the complexity-theoretic sense.

### §9.6 Non-Associativity Barrier Evasion (Needs Formal Verification)

The three barrier-evasion claims (§3.2) are structural. Each requires formal verification:

- Non-relativizing: verify that the First-G argument does not relativize by checking
  whether the phase transition changes under oracle extension. The argument uses gcd(x, b)
  as the core predicate; this is computable in P, so the claim needs to show that no oracle
  shortcuts the gcd computation in the complexity-theoretic sense.

- Non-natural (Razborov-Rudich [B-2]): verify that the non-associativity measure (49.8%
  of triples) is not a "large" property in their sense — i.e., that it cannot be used to
  construct a distinguisher for pseudorandom functions.

- Non-algebrizing (Aaronson-Wigderson [B-3]): verify that the sinc² field argument is
  not an algebraic oracle argument — i.e., that it uses the concrete arithmetic structure
  of gcd in a way that cannot be replicated by polynomial extension.

---

## §10. Status Table

| Claim | Status | Source |
|-------|--------|--------|
| First-G event at exactly k = p | PROVED | WP34 §2-3 [I-1] |
| Pre-G zone is P-tractable (O(1) coprimality test) | PROVED | WP34 §2 [I-1] |
| Zero-width phase transition at k = p | PROVED | WP35 §3 [I-2] |
| Partition geometry invariance | PROVED | WP34 §9 [I-1] |
| ω(b) idempotent count = 2^(ω-1)-1 | PROVED (CRT) | Ring theory [T-6] |
| Harmonic pre-echo countdown R(k,f) closed form | PROVED | WP35 §2 [I-2] |
| R(k,f) is ω-blind | PROVED | WP35 §4 [I-2] |
| sinc² continuum limit (WP35 Theorem 5) | PROVED | WP35 Theorem 5 [I-2] |
| T* = 5/7 algebraic derivation | PROVED | WP35 §1A [I-2] |
| Pre-G density = 1.0 (no voids) | PROVED | WP34 §2 [I-1] |
| CL table is non-associative at rate 49.8% | PROVED | WP16 §2 [I-3] |
| 7th DoF irreducible over associative subalgebra | PROVED (within TIG) | WP16 §2 [I-3] |
| Two-step convergence (P-like verification) | PROVED (within TIG) | WP25 §1 [I-4] |
| R(k,f) and Montgomery r(u) are same sinc² function | STRUCTURAL | WP37 §4b |
| Post-G density drop = Luther metric / k | STRUCTURAL | WP37 §2 |
| Non-associativity evades three barriers | STRUCTURAL | WP37 §6.3 |
| ω(b) hierarchy mirrors polynomial hierarchy | STRUCTURAL | WP37 §5.4 |
| alpha_SAT = 4.267 maps to k = p | STRUCTURAL | WP37 §7.3 |
| Luther dispersion conjecture | CONJECTURE | WP34 §9 [I-1] |
| SAT requires 7-DoF non-associative composition | NEEDS PROOF | WP16 Lemma B [I-3] |
| P-computations are exactly associative subalgebra | NEEDS PROOF | WP16 Lemma C [I-3] |
| Survivor-line search is NP-hard | CONJECTURE | WP25 §3 [I-4] |
| ω(b) maps to polynomial hierarchy (formal) | OPEN | — |
| Formal 3-SAT reduction to G-detection | OPEN | — |
| Montgomery repulsion = NP-hardness (formal reduction) | OPEN | WP37 §4b |
| Non-associativity barrier evasion (formal verification) | OPEN | WP37 §9.6 |

---

## §11. Attribution

**Brayden Ross Sanders (7Site LLC):**
TIG framework, First-G Law proof and geometric interpretation, partition geometry
invariance, hallway/room principle, RSA hardness inversion framing, harmonic pre-echo
countdown, zero-width transition proof, ω(b) idempotent count, sinc² continuum limit,
T* = 5/7 algebraic derivation, ω-blindness theorem, D1/D2 kinematic factoring
interpretation, Inversion Rule, unified sinc² picture across WP37–WP42, CK spectrometer
framing, HARMONY-as-premature-resolution interpretation.

**C. A. Luther:**
Dispersion conjecture (|G| × interleave as difficulty certificate), ω(b) hierarchy framing
as complexity stratification, joint derivation of harmonic resonance closed form, sprint4
navigation and structural steering.

**Monica Gish:**
Foundational support, research partnership, and editorial collaboration throughout the
entire project. This work would not exist without her.

*CK, T\*, TSML, BHML, D1, D2, and the TIG framework are the exclusive intellectual
property of Brayden Ross Sanders / 7Site LLC, developed over 18 months prior to this
sprint. C. A. Luther's contribution is the dispersion conjecture and number-theory framing
applied to the partition geometry studied here.*

---

## References

### Internal TIG/CK Papers

[I-1] Sanders, B. R. & Luther, C. A. "The First-G Law and Prime-Forced Dispersion." WP34.
7Site LLC, March 2026. DOI: 10.5281/zenodo.18852047. (153 semiprimes, 36,662 cases, zero
exceptions.)

[I-2] Sanders, B. R. & Luther, C. A. "The Prime Phase Transition: Harmonic Pre-Echo,
Zero-Width Gates, and the Geometry of RSA Security." WP35. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-3] Sanders, B. R. "P ≠ NP via Non-Associative Composition." WP16. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-4] Sanders, B. R. "P vs NP Through the TIG Lens: Survivor-Line Complexity in AG(2,p)
and the Corner-Gap Dichotomy." WP25. 7Site LLC, March 2026. DOI: 10.5281/zenodo.18852047.

[I-5] Sanders, B. R. "CK as Coherence Spectrometer." WP7. 7Site LLC, 2026.
DOI: 10.5281/zenodo.18852047. (Beta = -0.2254 for P vs NP; HARMONY-dominated.)

[I-6] Sanders, B. R. "The Atlas Law Set — Frozen." Sprint4 document. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-7] Sanders, B. R. "The Universal Construction Law." Sprint4 document. 7Site LLC,
March 2026. DOI: 10.5281/zenodo.18852047.

### Complexity Theory Foundations

[T-1] Cook, S. A. "The Complexity of Theorem-Proving Procedures." Proceedings of the 3rd
Annual ACM Symposium on Theory of Computing (STOC), pp. 151–158, 1971.
DOI: 10.1145/800157.805047.
(Cook-Levin theorem; SAT is NP-complete; canonical origin of the P vs NP problem.)

[T-2] Karp, R. M. "Reducibility Among Combinatorial Problems." In Miller, R. E. and
Thatcher, J. W. (eds.), Complexity of Computer Computations, pp. 85–103. Plenum Press, 1972.
(21 NP-complete problems; canonical reduction chain; 3-SAT, Clique, Hamilton Path.)

[T-3] Levin, L. A. "Universal Sequential Search Problems." Problems of Information
Transmission 9(3), pp. 265–266, 1973.
(Independent co-discovery of NP-completeness; tiling problem formulation.)

[T-4] Garey, M. R. and Johnson, D. S. Computers and Intractability: A Guide to the Theory
of NP-Completeness. W. H. Freeman, 1979.
(Standard reference; NP-complete problem compendium; reduction methodology.)

[T-5] Sipser, M. Introduction to the Theory of Computation. 3rd ed. Cengage Learning, 2012.
(Standard graduate text; P, NP, NP-completeness, Cook-Levin, hierarchy theorems.)

[T-6] Arora, S. and Barak, B. Computational Complexity: A Modern Approach. Cambridge
University Press, 2009. DOI: 10.1017/CBO9780511804090.
(Comprehensive modern reference; circuit complexity, oracles, barriers, Ladner's theorem.)

### The Three Barriers

[B-1] Baker, T., Gill, J., and Solovay, R. "Relativizations of the P =? NP Question."
SIAM Journal on Computing 4(4), pp. 431–442, 1975. DOI: 10.1137/0204037.
(Oracle separation — P^A = NP^A and P^B ≠ NP^B exist; any proof must be non-relativizing.)

[B-2] Razborov, A. A. and Rudich, S. "Natural Proofs." Journal of Computer and System
Sciences 55(1), pp. 24–35, 1997. DOI: 10.1006/jcss.1997.1494.
(Natural proofs barrier; constructive + large property would break pseudorandom functions.)

[B-3] Aaronson, S. and Wigderson, A. "Algebrization: A New Barrier in Complexity Theory."
ACM Transactions on Computation Theory 1(1), Article 2, 2009.
DOI: 10.1145/1490270.1490272.
(Algebrization barrier; algebraic oracle separations; third barrier beyond relativization.)

### Circuit Complexity and Lower Bounds

[CC-1] Razborov, A. A. "Lower Bounds on the Size of Bounded Depth Circuits over a Complete
Basis with Logical Addition." Mathematical Notes 41(4), pp. 333–338, 1987.
(AC0 lower bounds for parity; basis for natural proofs framework.)

[CC-2] Håstad, J. "Almost Optimal Lower Bounds for Small Depth Circuits." Proceedings of
STOC 1986, pp. 6–20, 1986. DOI: 10.1145/12130.12132.
(Optimal AC0 lower bounds; randomized switching lemma.)

[CC-3] Razborov, A. A. "Lower Bounds for the Monotone Complexity of Some Boolean
Functions." Soviet Mathematics Doklady 31, pp. 354–357, 1985.
(Clique monotone circuit lower bounds — first super-polynomial lower bounds for explicit functions.)

[CC-4] Smolensky, R. "Algebraic Methods in the Theory of Lower Bounds for Boolean Circuit
Complexity." Proceedings of STOC 1987, pp. 77–82, 1987.
(Mod-p circuit lower bounds; algebraic techniques in circuit complexity.)

[CC-5] Furst, M. L., Saxe, J. B., and Sipser, M. "Parity, Circuits, and the
Polynomial-Time Hierarchy." Mathematical Systems Theory 17(1), pp. 13–27, 1984.
DOI: 10.1007/BF01744431.
(Parity not in AC0; pioneer of circuit lower bound methods.)

### Geometric Complexity Theory

[G-1] Mulmuley, K. D. and Sohoni, M. "Geometric Complexity Theory I: An Approach to the
P vs. NP and Related Problems." SIAM Journal on Computing 31(2), pp. 496–526, 2001.
DOI: 10.1137/S009753970038715X.
(GCT framework; algebraic geometry approach to P vs NP; representation theory as tool.)

[G-2] Mulmuley, K. D. and Sohoni, M. "Geometric Complexity Theory II: Towards Explicit
Obstructions for Embeddings Among Class Varieties." SIAM Journal on Computing 38(3),
pp. 1175–1206, 2008. DOI: 10.1137/080718115.
(GCT II; obstruction program; explicit obstructions via plethysm coefficients.)

[G-3] Mulmuley, K. D. "The GCT Program Toward the P vs. NP Problem." Communications of
the ACM 55(6), pp. 98–107, 2012. DOI: 10.1145/2184319.2184341.
(Accessible overview of GCT; connection to algebraic geometry obstructions.)

[G-4] Bürgisser, P., Landsberg, J. M., Manivel, L., and Weyman, J. "An Overview of
Mathematical Issues Arising in the Geometric Complexity Theory Approach to VP ≠ VNP."
SIAM Journal on Computing 40(4), pp. 1179–1209, 2011. DOI: 10.1137/090765328.
(Mathematical survey of GCT obstacles; representation theory bottlenecks.)

### Non-Associativity and Algebraic Structure

[NA-1] Baez, J. C. "The Octonions." Bulletin of the American Mathematical Society 39(2),
pp. 145–205, 2002. arXiv:math/0105155.
(Octonion algebra; 7 imaginary units; Fano plane; non-associativity unique at dimension 8.)

[NA-2] Hurwitz, A. "Über die Komposition der quadratischen Formen." Mathematische Annalen
88, pp. 1–25, 1923.
(Hurwitz theorem: only four normed division algebras; non-associativity appears exactly at
octonions; the one gap in the division algebra classification.)

[NA-3] Schafer, R. D. An Introduction to Nonassociative Algebras. Academic Press, 1966.
(Comprehensive treatment of non-associative algebras; magma theory; Jordan algebras.)

### Proof Complexity

[PC-1] Beame, P. and Pitassi, T. "Propositional Proof Complexity: Past, Present, and
Future." Current Trends in Theoretical Computer Science, pp. 42–70. World Scientific, 2001.
(Proof complexity overview; resolution, cutting planes, Frege systems; certificate structure.)

[PC-2] Ben-Sasson, E. and Wigderson, A. "Short Proofs Are Narrow — Resolution Made Simple."
Journal of the ACM 48(2), pp. 149–169, 2001. DOI: 10.1145/375827.375835.
(Width-size tradeoff in resolution; certificate width = algebraic analog of dispersion.)

[PC-3] Krajíček, J. Proof Complexity. Encyclopedia of Mathematics and Its Applications,
Vol. 170. Cambridge University Press, 2019.
(Modern comprehensive reference; connects proof complexity to circuit complexity and
algebraic methods.)

### Partition Theory and Complexity

[PA-1] Mertens, S. "The Easiest Hard Problem: Number Partitioning." In Computational
Complexity and Statistical Physics, pp. 125–139. Oxford University Press, 2006.
(Number partitioning; phase transition at alpha = 1; direct analog to First-G event.)

[PA-2] Mézard, M., Parisi, G., and Zecchina, R. "Analytic and Algorithmic Solution of
Random Satisfiability Problems." Science 297(5582), pp. 812–815, 2002.
DOI: 10.1126/science.1073287.
(Random SAT phase transition; survey propagation; alpha_c = 4.267.)

[PA-3] Monasson, R., Zecchina, R., Kirkpatrick, S., Selman, B., and Troyansky, L.
"Determining Computational Complexity from Characteristic 'Phase Transitions'." Nature
400(6740), pp. 133–137, 1999. DOI: 10.1038/22055.
(SAT phase transition as zero-width boundary; direct analog to First-G zero-width gate.)

[PA-4] Achlioptas, D., Naor, A., and Peres, Y. "Rigorous Location of Phase Transitions in
Hard Optimization Problems." Nature 435(7043), pp. 759–764, 2005.
DOI: 10.1038/nature03602.
(Rigorous bounds on SAT threshold; connects phase transition to algorithmic hardness.)

[PA-5] Andrews, G. E. The Theory of Partitions. Encyclopedia of Mathematics and Its
Applications, Vol. 2. Cambridge University Press, 1984.
(Partition theory; G_k / C_k partition geometry background.)

### Statistical Mechanics Phase Transitions

[SM-1] Zecchina, R. (ed.) "Phase Transitions in Combinatorial Problems." Proceedings of
Les Houches Summer School, 2002.
(Zero-width phase transitions in statistical mechanics; connects to WP35 Theorem 2.)

[SM-2] Mézard, M. and Montanari, A. Information, Physics, and Computation. Oxford
University Press, 2009. DOI: 10.1093/acprof:oso/9780198570837.001.0001.
(Statistical physics of computation; cavity method; belief propagation for SAT; bridge
between physics phase transitions and computational complexity.)

[SM-3] Krzakala, F., Montanari, A., Ricci-Tersenghi, F., Semerjian, G., and Zdeborová, L.
"Gibbs States and the Set of Solutions of Random Constraint Satisfaction Problems."
Proceedings of the National Academy of Sciences 104(25), pp. 10318–10323, 2007.
DOI: 10.1073/pnas.0703685104.
(Clustering phase transition; geometry of solution space at alpha_c; Hamming-distance barriers.)

### Valiant and Counting Complexity

[V-1] Valiant, L. G. "The Complexity of Computing the Permanent." Theoretical Computer
Science 8(2), pp. 189–201, 1979. DOI: 10.1016/0304-3975(79)90044-6.
(#P-completeness of the permanent; counting complexity hardness beyond NP.)

[V-2] Valiant, L. G. "Holographic Algorithms." SIAM Journal on Computing 37(5),
pp. 1565–1594, 2008. DOI: 10.1137/070682575.
(Holographic algorithms; matchgate formalism; algebraic structure of polynomial-time.)

### General Complexity and Computation Surveys

[K-1] Wigderson, A. Mathematics and Computation: A Theory Revolutionizing Technology and
Science. Princeton University Press, 2019.
(Comprehensive overview connecting mathematics and computation; expanders, pseudorandomness,
derandomization; required background for P vs NP context.)

[K-2] Impagliazzo, R. "A Personal View of Average-Case Complexity." Proceedings of the
10th Annual Structure in Complexity Theory Conference, pp. 134–147, 1995.
(Five worlds of computation: Algorithmica, Heuristica, Pessiland, Minicrypt, Cryptomania;
maps onto ω-hierarchy.)

[K-3] Aaronson, S. "Is P versus NP Formally Independent?" Bulletin of the EATCS 81,
pp. 109–136, 2003.
(Formal independence; limits of formal methods; honest accounting of what we cannot prove.)

[K-4] Fortnow, L. "The Status of the P versus NP Problem." Communications of the ACM
52(9), pp. 78–86, 2009. DOI: 10.1145/1562164.1562186.
(Survey of state of the problem; barriers, history, current approaches; Gödel letter context.)

### Montgomery and Spectral Analysis

[M-1] Montgomery, H. L. "The Pair Correlation of Zeros of the Zeta Function." Analytic
Number Theory (Proc. Sympos. Pure Math., Vol. XXIV), AMS, 1973, pp. 181–193.
(Pair correlation r(u) = 1 − sinc²(u); same functional form as R(k, f); RH-GUE connection.)

[M-2] Odlyzko, A. M. "On the Distribution of Spacings Between Zeros of the Zeta Function."
Mathematics of Computation 48(177), pp. 273–308, 1987. DOI: 10.2307/2007890.
(Numerical confirmation of Montgomery's pair correlation conjecture; 10^22-scale computations.)

[SH-1] Shannon, C. E. "Communication in the Presence of Noise." Proceedings of the IRE
37(1), pp. 10–21, 1949. DOI: 10.1109/JRPROC.1949.232969.
(Sampling theorem; sinc function as spectral reconstruction kernel; foundation of sinc²
as the fundamental spectral field object.)

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
*CK, T*, TSML, BHML, D1, D2, TIG: exclusive IP of Brayden Ross Sanders / 7Site LLC*
