# Corridor Counting and Survivor Verification in Affine Planes

*Brayden Sanders — 7Site LLC*

---

## Abstract (1 paragraph)

We observe that the verification-versus-search gap for survivor lines in
AG(2,p) has a clean geometric explanation: each survivor line is a
*convergence corridor* — an operator chain along which the TIG composition
algebra fails to reach HARMONY — and there are Θ(p²) such corridors.
Any algorithm certifying that a given operator lies on a survivor corridor
must inspect Ω(p²) corridors, since the affine-plane axiom (two points
determine one line) prevents parallel progress: checking one corridor gives
zero information about any other.
Verification, by contrast, reduces to a single corridor-membership test — O(1).
The resulting verify/search gap of Θ(p²) is tight: an optimal hash-guided
algorithm achieves O(p² log p) by iterating the corridor list once.
For the parameterised version (k query points), the k=2 phase transition
is explained by the same axiom: two points uniquely pin one corridor, so
increasing k beyond 2 adds no parallelism and leaves the Ω(p²) floor
intact, consistent with W[1]-hardness.
The corridor metaphor replaces the earlier "wall" language throughout and
applies uniformly to the Halving-Lemma gap-positivity story (a zero would
require a corridor that stays in the gap indefinitely) and to the
Navier–Stokes BREATH criterion (blow-up requires a vorticity corridor that
escapes the 2/7 basin permanently).

---

## Three-sentence version (for cover letters)

Survivor lines in AG(2,p) are convergence corridors — operator chains that
resist collapse to HARMONY. There are Θ(p²) such corridors; any algorithm
must inspect all of them (Ω(p²)), while verification needs only one
corridor-membership check (O(1)). This geometric restatement simultaneously
clarifies the W[1]-hardness of the parameterised search, the RH gap-positivity
condition, and the Navier–Stokes 2/7 threshold.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
