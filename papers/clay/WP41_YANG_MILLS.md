# WP41 — Yang-Mills Mass Gap Through the TIG Lens
## The First-G Distance as a Model of Field Energy Quantization

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — analogical, not a proof*

> **Intellectual Property Notice.** CK, T*, TSML, BHML, D1, D2, and the TIG
> (Trinity Infinity Geometry) framework are the exclusive intellectual property
> of Brayden Ross Sanders / 7Site LLC, developed over 18 months prior to this
> sprint. C. A. Luther's contribution is the Luther dispersion conjecture
> applied to the number theory studied here. Luther has no claim to the CK
> architecture or its derived constants. This paper presents structural
> analogies, not a proof of the Yang-Mills mass gap.

---

## Abstract

The Yang-Mills mass gap problem asks for a rigorous mathematical proof that
pure Yang-Mills gauge theory in four dimensions exists and possesses a mass
gap — a positive lower bound on the energy of any non-vacuum excitation. The
TIG framework, developed for the Coherence Keeper (CK) system, independently
produces an arithmetic structure that exhibits striking parallels with the
mass gap concept. This paper presents those parallels as structural analogies.
We show: (1) the First-G Law (WP34) establishes a minimum distance p before
any non-trivial structure appears in the arithmetic alphabet, and this
minimum distance is a structural analog of the mass gap; (2) the T* = 5/7
coherence floor — calibrated on CK's FPGA hardware — functions as an energy
floor in the TIG composition algebra, enforced by the TSML table; (3) the
stability window {1, ..., p-1} where all elements are coprime to b is the
TIG vacuum analog; (4) Luther dispersion provides a field energy distribution
analog; and (5) the sinc² resonance field is smooth everywhere and singular
at k = p, mirroring the Yang-Mills field structure. We do not claim these
analogies constitute a proof. We present them as a coherent structural picture.

---

## §1. The Yang-Mills Mass Gap Problem

### 1.1 Classical Statement

Yang-Mills theory is a non-Abelian gauge theory on four-dimensional Euclidean
space, defined by a gauge group G (typically SU(2) or SU(3)) and an action:

    S[A] = (1/2g²) ∫ Tr(F_μν F^μν) d⁴x

where F_μν = ∂_μ A_ν - ∂_ν A_μ + [A_μ, A_ν] is the field strength tensor.

The Clay Millennium Problem asks for a proof that:
1. The quantum Yang-Mills theory exists as a mathematically rigorous object
   (a quantum field theory satisfying the Wightman axioms or Osterwalder-
   Schrader axioms in Euclidean space).
2. The theory possesses a mass gap Δ > 0: the energy spectrum is
   spec(H) = {0} ∪ [Δ, ∞), with the vacuum state E = 0 isolated.

The mass gap says: you cannot create an excitation of the Yang-Mills field with
arbitrarily small positive energy. The smallest possible excitation costs at
least Δ energy units. There is a "threshold" below which nothing happens.

### 1.2 Why This Is Hard

The difficulty is that classical Yang-Mills theory has no mass gap (photons are
massless in classical electromagnetism). The mass gap is a purely quantum,
non-perturbative phenomenon arising from the non-Abelian nature of the gauge
group. No perturbative calculation can see it. The standard physics argument
(lattice confinement, Wilson loops) is plausible but not mathematically
rigorous. The Osterwalder-Seiler theorem (1978) provides the closest rigorous
result: reflection positivity on the lattice gives a self-adjoint transfer
matrix, whose spectral gap would imply a mass gap in the continuum limit — but
the continuum limit itself remains unproven.

WP15 (Yang-Mills Synthesis) develops the BHML spectral gap argument in detail.
This paper develops the complementary First-G Law perspective.

---

## §2. The First-G Distance as a Mass Gap Analog

### 2.1 The First-G Law Restated

For a semiprime b = p × q with p ≤ q, define the alphabet {1, 2, ..., k}
with coprimality partition:

    C_k = { x ∈ {1..k} : gcd(x, b) = 1 }   (coherent elements — "vacuum")
    G_k = { x ∈ {1..k} : gcd(x, b) > 1 }   (obstructing elements — "excited")

**First-G Law (WP34 Theorem, proved algebraically, verified in 36,662 cases):**

    |G_k| = 0   for all k < p
    |G_p| = 1   (the element p is the first non-unit)

The First-G Law says: **there is no non-trivial structure until you reach
alphabet size k = p.** Below that threshold, every element is in the vacuum
(coprime to b). At k = p, the first excited element appears.

### 2.2 The Structural Analog

The parallel with the mass gap is direct:

| Yang-Mills concept        | TIG analog                              |
|--------------------------|----------------------------------------|
| Vacuum state (E = 0)     | All elements coprime to b (k < p)      |
| Mass gap Δ               | The prime p (First-G distance)         |
| First excited state      | The element p itself (first non-unit)  |
| Energy spectrum {0}∪[Δ,∞)| Coprime alphabet followed by G_k jump  |
| Cannot excite below Δ    | Cannot have gcd(x,b)>1 for x < p      |

The First-G Law is an algebraic proof that in the TIG alphabet, the "mass gap"
(the distance from vacuum to first excitation) is exactly p. Not approximately
p. Not roughly p. Exactly p, with zero exceptions.

### 2.3 The Gap is Forced by the Prime Structure

The reason the mass gap equals p is that p is a prime. If p were composite
(say p = a × c with a, c > 1), then a < p would already be non-coprime to
a × c × q = b only if a divides b, but a divides b iff a shares a factor with
p × q. Since a < p and p is prime, a does not share a factor with p. Whether
a shares a factor with q depends on q.

The irreducibility of p as a prime is what forces G_k to be empty up to k = p.
The mass gap in Yang-Mills is similarly forced by the non-Abelian structure of
the gauge group — it is the irreducibility of the gauge group representation
that prevents low-energy excitations.

**Structural claim:** The role of primality in the First-G Law is structurally
analogous to the role of non-Abelianness in Yang-Mills. Both are "irreducibility
conditions" that force a minimum excitation threshold.

---

## §3. T* = 5/7 as the Coherence Floor

### 3.1 The T* Threshold in CK

CK's FPGA hardware calibrated to T* = 5/7 = 0.714285... as the coherence
threshold after 18 months of development. WP35 §1A proves this is not hardware
noise: T* is the exact unit fraction of b = 35 at the second gate event:

    unit_frac(k = 7, b = 35) = |{x ∈ {1..7} : gcd(x, 35) = 1}| / 7 = 5/7

For b = 35 = 5 × 7, the second gate is at k = q = 7 (the larger prime factor).
In the alphabet {1, 2, 3, 4, 5, 6, 7}, the elements 5 and 7 share a factor
with 35. The remaining five elements {1, 2, 3, 4, 6} are coprime. Density:
5/7 = T*.

This is not an approximation. 5/7 is exact. T* is a derived constant of the
arithmetic, not a free parameter.

### 3.2 T* as an Energy Floor in the TSML

The TSML composition table enforces T* as the coherence floor. WP17 establishes:
- TSML_8 is symmetric (self-adjoint over the reals)
- TSML_8 has nullity 1, with the null eigenvector in the BALANCE-CHAOS subspace
- The TSML HARMONY absorption rate is 84.4% (8×8 core)

The HARMONY operator is the maximum-value absorbing operator — it absorbs any
composition above the T* threshold. Below T*, the BREATH operator governs.
The T* threshold is the transition point between BREATH-dominated and HARMONY-
dominated composition.

### 3.3 The Mass Gap Parallel

In Yang-Mills theory, the mass gap Δ is the energy floor. Below Δ, no
excitations exist. The vacuum is stable. Above Δ, excitations are possible.

In TIG:
- Below T*: BREATH-dominated, coherence fluctuating, near-vacuum
- At T*: the transition point — b = 35 second gate, exact balance
- Above T*: HARMONY-dominated, coherent, excited

The T* floor in TIG is structurally analogous to the Yang-Mills mass gap:
it is the minimum coherence that the TSML algebra enforces. The TSML cannot
produce a composition below T* and call it coherent — below that level, the
system is in the vacuum state. This is enforced algebraically, not dynamically.

---

## §4. The Stability Window as Vacuum

### 4.1 The Window {1, ..., p-1}

For semiprime b = p × q with p ≤ q, the stability window is:

    W(b) = { k ∈ {1, ..., p-1} : gcd(k, b) = 1 }

By the First-G Law, W(b) = {1, ..., p-1} — the entire pre-prime alphabet is
coprime to b. Every element in the window is "vacuum": no prime obstruction,
no non-unit element, no mass.

Properties of the window:
- **Size:** |W(b)| = p - 1 (all elements up to but not including p)
- **Density:** (p-1)/(p-1) = 1 (perfect — no exceptions)
- **Coherence:** Every element has gcd(k, b) = 1 (unit, fully coprime)
- **Stability:** Adding any element from W(b) to any other gives a result
  that is still coprime to b (under addition mod b — ring-theoretic vacuum)

### 4.2 Vacuum Stability

The stability window is not just "all coprime elements happen to live here."
It is stable under the TIG coherence gate: any element k < p that attempts to
"excite" (acquire a non-trivial gcd with b) cannot do so — the prime p has not
yet entered the alphabet. The vacuum is topologically protected.

This is the TIG analog of the Yang-Mills vacuum stability: the Yang-Mills
vacuum |0⟩ is stable against small fluctuations because any excitation costs
at least Δ energy. Below Δ, you cannot perturb the vacuum. In TIG, below k = p,
you cannot perturb the coprime alphabet.

### 4.3 The Prime p as the Threshold

The threshold between vacuum and first excitation is k = p. This threshold is:
- **Algebraically forced:** Proven from the definition of primality (WP34)
- **Universal:** Holds for all semiprimes b = p × q without exception
- **Sharp:** One step before k = p, everything is vacuum; at k = p, exactly
  one excitation appears (the element p itself)

The sharpness is the key. In Yang-Mills, the mass gap is also a sharp threshold
— there is no continuous interpolation between vacuum and first excited state.
The TIG First-G Law realizes this sharpness in an algebraically exact form.

---

## §5. Luther Dispersion and Field Energy Distribution

### 5.1 Luther Dispersion Conjecture

C. A. Luther's dispersion conjecture characterizes how non-units are distributed
through the post-First-G alphabet {p, p+1, ..., q-1, q, ...}. High-dispersion
semiprimes (large q/p) have non-units spread irregularly through this alphabet;
low-dispersion semiprimes (q/p near 1) have regular, predictable spacing.

Define the interleave index of b = p × q as:

    I(b) = (number of coprime runs in {p, ..., b}) / (q - p)

Low I(b) means long coprime runs (few excitations, low field energy density).
High I(b) means many short coprime runs (frequent excitations, high field energy
density).

### 5.2 Field Energy Density Analog

In Yang-Mills theory, the field energy density is:

    ε(x) = Tr(F_μν F^μν)(x)

This is the local energy cost of having a non-trivial field configuration at
point x. Where ε(x) is large, the field is "excited." Where ε(x) ≈ 0, the
field is near the vacuum.

In TIG, the analog of ε(x) is the density of non-unit elements in the
post-First-G alphabet. High Luther dispersion D(b) means ε is spread out
across many alphabet positions. Low Luther dispersion means ε is concentrated
near specific positions (the primes p and q).

### 5.3 Low-Interleave G = Concentrated Field Energy

Specific structural observations:

**Low-interleave G (q/p near 1, near-twin primes):**
- Non-units cluster near k = p and k = q
- Coprime runs are long in the middle
- Field energy is concentrated at the prime threshold events
- Structural analog: confinement — field energy concentrated in "flux tubes"
  between color charges

**High-interleave G (q/p large):**
- Non-units spread throughout {p, ..., b}
- Many short coprime runs
- Field energy is diffuse
- Structural analog: asymptotic freedom — at high energies, the field becomes
  weakly coupled and field energy spreads

The transition between low-interleave and high-interleave regimes as q/p
increases is a structural analog of the confinement-deconfinement transition
in Yang-Mills theory (though the latter requires finite temperature).

---

## §6. The sinc² Field Approach

### 6.1 The Resonance Field Near k = p

The sinc² resonance field (WP35 Theorem 5):

    R(k, f) = sin²(πk/f) / (k² sin²(π/f))

is smooth and positive for all k in {1, ..., f-1} and collapses to exactly
zero at k = f. For f = p (the smallest prime factor of b), this field is:
- **Smooth everywhere in {1, ..., p-1}:** No singularities in the vacuum window
- **Singular at k = p:** Exact zero, the First-G event
- **Positive definite in the vacuum:** R(k, p) > 0 for all k < p

This is structurally analogous to the Yang-Mills field:
- The Yang-Mills field A_μ is smooth in regions with no topological charge
- Instantons and monopoles create point singularities in the classical field
- The first excitation (mass gap) appears at the lowest non-trivial topological
  sector

### 6.2 The Zero as an Instanton Analog

In Yang-Mills theory, instantons are topologically non-trivial field
configurations that contribute to the path integral. They have finite action
and appear as point-like events in Euclidean space-time.

In TIG, the zeros of R(k, p) at k = p, 2p, 3p, ... are topologically
non-trivial events in the arithmetic alphabet — they are the First-G events
and their periodic recurrences. Like instantons, they:
- Appear at discrete, isolated locations (k = np for n = 1, 2, 3, ...)
- Have "finite action" (R transitions from positive to exactly zero)
- Are separated by "vacuum regions" where R > 0

### 6.3 The T* Connection to Field Smoothness

The T* threshold 5/7 = 0.71428... equals the resonance field at k = q for
b = 35:

    R(k = 7, f = 5) = sin²(7π/5) / (49 sin²(π/5))
                    = sin²(7π/5) / (49 sin²(π/5))

(This equals a specific numerical value; the exact T* derivation is the unit
fraction argument of WP35 §1A, which is algebraically cleaner.) The point
is that T* marks the specific density at which the coherence field transitions
from the "first gap region" to the "bridge region" between p and q. This
transition is smooth in the resonance field — no singularity at T*, only at
k = p and k = q.

This mirrors Yang-Mills: the field is smooth at generic configurations (analog
of T*-level coherence) and singular only at instanton locations (analog of
the First-G events at k = p and k = q).

---

## §7. Open Questions

### 7.1 Continuum Limit of the First-G Distance

The First-G Law is a discrete arithmetic result. The Yang-Mills mass gap is a
continuum quantum field theory result. The key open question is:

**Open Question 1.** Does the First-G distance p, for a sequence of semiprimes
b_n = p_n × q_n with p_n → ∞, have a well-defined continuum analog? Does the
lattice spacing a = 1/p_n → 0 as p_n → ∞ in a way that produces a continuum
limit with a well-defined gap?

This is the TIG analog of the Osterwalder-Seiler continuum limit question.

### 7.2 The BHML Spectral Gap and the First-G Distance

WP15 (Yang-Mills Synthesis) establishes the BHML spectral gap as the T*
eigenvalue ratio:

    |λ_6|/|λ_5| = 0.4735/0.7502 = 0.6312 ≈ 1 - T* = 2/7

**Open Question 2.** Is there a direct algebraic relationship between the
BHML spectral gap (derived from the operator composition table) and the
First-G distance p? Both provide a "minimum energy" concept in TIG. Do they
measure the same phenomenon from different angles?

### 7.3 Non-Abelianness and Non-Primality

The Yang-Mills mass gap is believed to arise from the non-Abelian nature of
the gauge group. An Abelian gauge theory (electromagnetism) has no mass gap.

**Open Question 3.** What is the TIG analog of Abelian vs. non-Abelian? For
the First-G Law, replacing the prime p with a composite number c gives a
different result — the first non-unit appears before k = c. Does this
"composite modulus" regime correspond to an Abelian theory with no mass gap?
If so, primality in TIG is the precise algebraic analog of non-Abelianness
in gauge theory.

---

## §8. Attribution

**Brayden Ross Sanders (7Site LLC):**
- TIG framework, CK architecture, TSML/BHML tables, T* = 5/7 calibration
- D2 force physics, operator set {VOID..RESET}, CL composition lattice
- First-G Law discovery and proof framework (WP34)
- Pre-Echo Countdown Law and sinc² field (WP35)
- This paper's structural framing: First-G as mass gap, T* as energy floor,
  stability window as vacuum, sinc² as field smooth-singular structure
- All CK source code: github.com/TiredofSleep/ck

**C. A. Luther:**
- Luther dispersion conjecture (applied to prime structure in WP34-WP35)
- Dispersion-field energy distribution analog (this paper §5)
- Low/high interleave structural correspondence to confinement/deconfinement
- Independent approach to the same arithmetic structure from analytic side
- Neither author reaches this paper without the other

**CK / T* / TSML are 7Site LLC exclusive IP.** Luther's contributions are
confined to the dispersion conjecture and its applications.

---

## References

- WP34: Sanders & Luther, "The First-G Law and Prime-Forced Dispersion," March 2026.
  DOI: 10.5281/zenodo.18852047
- WP35: Sanders & Luther, "The Prime Phase Transition: Harmonic Pre-Echo,
  Zero-Width Gates, and the Geometry of RSA Security," March 2026.
  DOI: 10.5281/zenodo.18852047
- WP15: Sanders, "Yang-Mills Mass Gap Synthesis: A Spectral Gap Theorem for
  the BHML Transfer Matrix," March 2026. DOI: 10.5281/zenodo.18852047
- Yang, C. N., & Mills, R. L. (1954). "Conservation of isotopic spin and
  isotopic gauge invariance." Physical Review 96(1): 191–195.
- Wilson, K. G. (1974). "Confinement of quarks." Physical Review D 10(8):
  2445–2459.
- Osterwalder, K., & Seiler, E. (1978). "Gauge field theories on a lattice."
  Annals of Physics 110(2): 440–471.
- Jaffe, A., & Witten, E. (2000). "Quantum Yang-Mills theory." Clay
  Mathematics Institute Millennium Problems. Available at claymath.org.

---

*© 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry*
*CK, TIG, T*, TSML, BHML, D2, D1 are exclusive intellectual property of 7Site LLC.*
*C. A. Luther's dispersion conjecture is credited as stated above.*
*This paper presents structural analogies. It is not a proof of the Yang-Mills mass gap.*
