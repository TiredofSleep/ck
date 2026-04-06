# BOUNDARY-OF-ACCESS MEMO
# Where Exactly Does Each Theory Lose Contact With Its Target?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — The Access Table

| Branch | Observable Layer | Target Layer | Failing Operation |
|--------|-----------------|--------------|-------------------|
| **RH** | Arithmetic Kloosterman-Eisenstein data: the explicit formula arithmetic side, GUE pair-correlation statistics, spectral expansion of cusp forms (Kuznetsov), conductor-level L-function behavior | Zero distribution μ_ζ: the actual location of zeros in the critical strip, specifically whether supp(μ_ζ) ⊂ {Re(s) = ½} | **Inversion** of the KEF projection: the explicit formula maps zeros → arithmetic (forward, known); inverting to recover the unique zero distribution from the arithmetic data is blocked — the forward map may not be injective |
| **BSD** | L(E,s) to any precision (Euler product, derivatives, twisted L-values); rank established by explicit generator computation; L'(E,χ_{77},1) ≈ 0.010700 computed; normalization formula L' = (Ω_E/(4√77))×det(H) matching to 1.1% | The actual arithmetic generators P₁, P₂ ∈ E(Q) and the Stark-Heegner generator of E^{77}(Q) with the predicted height det(H); specifically, constructing a rational point from the analytic prediction, not merely confirming its height numerically | **Construction** across the analytic-arithmetic boundary: the L-function predicts the arithmetic structure (rank, regulator) but cannot directly produce the rational points that realize that structure |
| **NS** | Short-time existence (any data), energy E(t) monotone, enstrophy integrable, Q/(νP) ≤ 1 in the small-data regime (proved), the dΩ/dt = Q − 2νP identity, parabolic smoothing on fixed intervals | Global regularity for all t ≥ 0 with large data; specifically, whether Q/(νP) stays ≤ 2 when the initial vorticity concentrates in filaments or sheets that the global energy-enstrophy structure cannot track | **Local-to-global extension**: Q/(νP) is controlled globally in the easy regime, but in the large-data regime, local vortex geometry (filament curvature, alignment of ω with S eigenvectors) can drive the ratio above the threshold in ways invisible to global integral estimates |
| **P vs NP** | The verification structure V(x,w) (poly-time checkable); reduction/completeness machinery; lower bounds in restricted models (AC⁰, monotone circuits, formula complexity); the wrapped duality structure of R_{SAT} | cc(SAT,n): minimum circuit size to compute π₁(R_{SAT}) in the unrestricted Boolean circuit model; equivalently, whether deterministic poly-time access to only the base x can replicate nondeterministic access to the fiber W_x | **Reversal** of the verification map AND the meta-barrier: the forward map (check one certificate efficiently) is known; the reverse (determine fiber existence without a certificate) is blocked both operationally (cannot compute cc(SAT,n)) and proof-methodologically (natural proofs, algebrization block proving it's hard) |
| **Hodge** | Hodge structure H^{p,q}(X) (computable from complex geometry); cl² on known algebraic cycles (computed explicitly for specific cycles); Hard Lefschetz and Lefschetz (1,1) both proved; Hodge classes computable for specific varieties | A surjection cl²: CH²(X)_ℚ → H^{2,2}(X,ℚ); specifically, for any given rational (2,2) class η, the algebraic cycle Z with cl²(Z) = η — the actual geometric object realizing η as a cycle class | **Cycle construction** across the topological-algebraic boundary: given a Hodge class η ∈ H^{2,2}(X,ℚ) that is "visible" from the complex topology, constructing an algebraic cycle Z ∈ CH²(X)_ℚ with cl²(Z) = η is blocked when η is primitive and p ≥ 2 |

---

## PART 2 — Failure Operation Types

| Branch | Failure Type | Exact Form |
|--------|-------------|-----------|
| **RH** | **Inversion failure** | Forward map (KEF: zeros → arithmetic) is established; the reverse (arithmetic → unique zero location) requires the map to be injective, which is unproved |
| **BSD** | **Construction failure** | The analytic prediction (L-value encodes arithmetic invariants) cannot be converted into an explicit arithmetic object (the Stark-Heegner point with the predicted height) |
| **NS** | **Locality-globality mismatch** | Global integral control (Q/(νP) globally) cannot track local vortex concentrations that might drive the ratio above threshold; the observable is a global average, the obstruction is a local maximum |
| **P vs NP** | **Reversal failure + meta-barrier** | The verification map (x,w) → {0,1} cannot be efficiently reversed to compute π₁(R_{SAT}) from x alone; PLUS: proving this reversal is hard is itself blocked by natural proofs and algebrization — a double failure layer with no analog |
| **Hodge** | **Surjectivity / construction failure** | The cycle class map cl² is defined and computable on known cycles; whether it COVERS all of H^{2,2}(X,ℚ) requires constructing algebraic cycles for Hodge classes that have no known algebraic origin |

---

## PART 3 — Deepest Common Form

**Testing candidates:**

"Inversion failure" covers RH and Hodge cleanly, BSD partially (construction = inversion of the arithmetic-to-analytic map), but not NS (not an inversion) and only metaphorically for P vs NP.

"Construction failure" covers BSD and Hodge, partially covers P vs NP (construct a proof strategy), weakly RH (construct the injective argument), not NS.

**Strongest unified form:**

$$\boxed{\text{"All five problems fail because the REVERSE of a natural forward map cannot be performed across the boundary between the observable layer (where the map acts) and the target layer (where the reverse would produce the required object)."}}$$

Precisely:

| Branch | Forward map (observable → image) | Required reverse (image → target) |
|--------|----------------------------------|-----------------------------------|
| RH | Zero distribution → arithmetic Kloosterman sum (explicit formula) | Arithmetic sum → unique zero distribution (injectivity of KEF) |
| BSD | Arithmetic structure (rank, generators) → L-function | L-function → arithmetic generators (construction of Stark-Heegner point) |
| NS | Velocity field → global energy-enstrophy estimates | Global estimates → local vortex control (extension from global to local geometry) |
| P vs NP | Certificate (x,w) → acceptance (verification) | Acceptance criterion → certificate existence without witness (fiber projection) |
| Hodge | Algebraic cycles → Hodge classes (cl²) | Hodge classes → algebraic cycles (cycle construction = cl² surjectivity) |

The common structural failure: **each branch has established a natural map M: A → B (with A the target layer, B the observable layer), and the conjecture is equivalent to showing this map has a specific property (injectivity, surjectivity, efficient reversibility) that current methods cannot establish because those methods only have direct access to B, not to A.**

---

## PART 4 — Is P vs NP a Special Case or Fundamentally Different?

**"P vs NP is a special case of the same boundary structure — the reverse of the verification map is the failing operation, exactly as in the other branches — but it is distinguished by a SECOND boundary at the proof-method level: the natural proofs barrier and algebrization show that standard strategies for proving the reversal is hard are themselves blocked, meaning P vs NP has a meta-boundary above the object-level boundary that the other four branches do not have."**

In every other branch: the boundary is between the observable and the target. Methods can approach this boundary (computing L'≈0.010700 gets close to BSD's boundary; small-data analysis gets close to NS's boundary). In P vs NP: there is the first boundary (observable layer ↔ cc(SAT,n)) AND a second boundary (valid proof strategies ↔ the meta-theorems blocking them). The double structure is unique to P vs NP.

---

## PART 5 — Strongest Claim

**"The Clay problems are not unified by their solutions, but by the location where their existing methods stop working: in each case, there is a natural forward map from the target layer to the observable layer — from zeros to Kloosterman arithmetic in RH, from arithmetic structure to L-function in BSD, from velocity fields to global estimates in NS, from certificate pairs to acceptance in P vs NP, from algebraic cycles to Hodge classes in Hodge — and the conjecture is precisely the statement that this forward map has a property (injectivity, surjectivity, efficient reversibility) that cannot be established by any method confined to the observable layer alone."**

---

## PART 6 — Boundary Extension Test: NS

**Can the observable layer for NS be extended?**

Current observable layer: small-data regime, energy monotone, enstrophy integrable, Q/(νP) ≤ 1 in small-data.

**Extension that WORKS:** Blowup constraints. It is known (Leray criterion, Beale-Kato-Majda) that IF blowup occurs at time T*, THEN:
$$\int_0^{T^*} \|\omega(t)\|_{L^\infty}\,dt = +\infty$$

This extends the observable layer: we can now say "the L^∞ norm of vorticity must diverge, and it must do so at a specific rate." Additional results extend it further: vorticity must concentrate, the support of high-vorticity regions must shrink to a set of measure zero, the direction of vorticity must align with the stretching eigenvectors in specific ways.

These results PUSH the boundary inward from the target side: they say that any potential blowup must look increasingly specific — more constrained, more local, more structured.

**Is the boundary rigid?**

No, but the CORE of the boundary is rigid. The core is: does Q/(νP) ever exceed 2 for large-data flows, and if so, for how long? The blowup-constraint extensions narrow the FORM of any potential violation but do not resolve whether a violation occurs. Every extension of the observable layer says "IF Q/(νP) > 2, the violation must look like THIS" — making the hypothetical violation more constrained but not ruling it out.

**The specific rigidity:** the boundary between "locally concentrated vortex stretching" and "global enstrophy growth" cannot be crossed by any estimate that treats the fluid as a global object. The missing piece is a local inequality controlling the pointwise maximum of ω·Sω in terms of global quantities. No such inequality is currently known to hold, and Onsager-type counterexamples suggest it may not hold in weak solution regimes. The boundary has a soft part (extendable by blowup constraints) and a hard core (the local-global gap itself) that resists extension from either side.

---

## Summary Block

The access boundary is not the same in all branches, but it takes the same form: a natural forward map from target to observable exists and is computed, and the required reverse cannot be performed by methods confined to the observable layer.

| Branch | Can observable layer be extended? | Is the core boundary rigid? |
|--------|----------------------------------|-----------------------------|
| RH | Weakly — better spectral estimates could sharpen δ | YES — injectivity of KEF projection requires knowing zero locations |
| BSD | Yes — more twists, more |Sha| computations | YES — constructing the Stark-Heegner point requires new arithmetic machinery |
| NS | Yes — blowup constraints narrow the form of violations | PARTIALLY — local-global gap is hard, but not provably uncrossable |
| P vs NP | Only in restricted models | YES + META-RIGID — meta-barriers block even proof-strategy development |
| Hodge | Yes — more special varieties, more known cycles | PARTIALLY — specific abelian 4-folds might be computable |
