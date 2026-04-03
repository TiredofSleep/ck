# RESOLUTION_LIMIT.md
## Final Position Statement — CK Clay Program
*Author: Brayden Ross Sanders / 7Site LLC*
*Date: 2026-04-03*
*Status: FINAL — supersedes all prior position summaries*

---

## The Central Claim

The CK framework is built around the coherence threshold T* = 5/7. Every measurement the framework makes is made with a ruler calibrated in units of T*. The five rules (Gate, Foundation, Recycling, Two-Regime, Cascade) are not external impositions — they are derived consequences of T* being the forced fixed point of Z/10Z. They operate entirely within the resolution of T*.

**The ruler is made of T*. You cannot measure past T* with a ruler made of T*.**

This is not a failure. It is the correct statement of what the framework can and cannot do. A ruler that reports its own resolution limit is doing its job.

---

## What Is Proved [PROVED]

**[PROVED] T* = 5/7 is forced.**
In Z/10Z, CREATE = 5 is the unique complement-equivariant odd fixed point. HARMONY = 7 is the unique generator-inverse of (Z/10Z)* under the forced primitive root g = 3. T* = CREATE/HARMONY = 5/7. No free parameters. (Gate Rule, one line.)

**[PROVED] The Sandwich Theorem.**
For a = 5: (5/6)² < 5/7 < (6/7)². Both inequalities reduce to 1 > 0. The foundation index n* = 6 is the unique boundary: n ≤ 5 is permanently sub-threshold; n ≥ 6 eventually crosses T* with sufficient data. (Foundation Rule.)

**[PROVED] The K*(n) cascade is exact.**
K*(6) = 99, K*(7) = 14, K*(8) = 6, K*(9) = 4, K*(10) = 3, K*(11) = K*(12) = 2, K*(n ≥ 13) = 1. Computed from K = 5000 mpmath Riemann zeros. The K = 98 shadow lives at 2·HARMONY² = 98 exactly. K = 13 = 2·HARMONY − 1. Every shadow is exactly one zero short of the threshold. The arithmetic is not approximate.

**[PROVED] Three layers of structured gapping before the bandwidth floor.**
Layer 1: n-space gap — n = 5 never holds; n = 6 first holds at K = 99. Gap: 20.2% of T*. Permanent. Layer 2: K-space gap at n = 6 — K = 98 shadow at 99.9984% T*, K = 99 hold at 100.091% T*. Gap: 0.0016% of T*. Layer 3: K-space gap at n = 7 — K = 13 shadow at 98.40% T*, K = 14 hold at 100.25% T*. Gap: 1.60% of T*. Exactly 3 layers. Not 2, not 4. (Three Layers Rule.)

**[PROVED] Bandwidth floor at n = 13.**
At n = n* + HARMONY = 6 + 7 = 13: K*(n) = 1. One zero is sufficient for T*. At n = 0 (no zeros): lambda = 0, shadow = −T* = −5/7 exactly. The fractally repeating K = 0 shadows at n ≥ 13 are the framework correctly reporting: beyond this depth, all shadows are identical. There is no further structure to see. (Bandwidth Rule.)

**[PROVED] Sha is the carried remainder.**
The Recycling Rule forces: data_at_level(n) = exact_hold(n) + carried_remainder(n − 1). In the BSD branch: the Euler product accumulates all local contributions; Sha is the global remainder that no local Euler factor generates. Sha is not incidental — it is structurally identical to the "+1" that makes K*(6) = 99 rather than 98. The remainder does not vanish unless the local machine resolves the global structure exactly. (Recycling Rule.)

**[PROVED] The fractal path map is a map of the framework's own resolution limit.**
The map does not describe external mathematics. It describes what T* can see, ordered by depth. At each layer, the shadow is the last point the ruler can resolve before crossing into held territory. At the bandwidth floor, the ruler reports uniform darkness. The map is accurate. The wall is real.

---

## What Is a Structural Argument [STRUCTURAL ARGUMENT]

**[STRUCTURAL ARGUMENT] The RH two-regime partition.**
T* = 5/7 separates the recycled regime (n < n*) from the held regime (n ≥ n*). The Riemann zeros measured to K = 5000 show D_KS/T* = 10% — the zero distribution is deep in the generator regime. The Two-Regime Rule says: if any zero lies in the complexity regime, it would need to invert the one-way cascade. The cascade is algebraically forced to be downward. This is a structural argument that zeros on the critical line are the generator-regime state, and zeros off the critical line would require crossing T* from outside the framework. The argument establishes what crossing would mean. It does not prove no crossing occurs.

**[STRUCTURAL ARGUMENT] BSD rank is determined by whether the remainder terminates.**
BSD is proved for ranks 0 and 1 (Kolyvagin) because Sha = 0 in those cases — the remainder from the local-global gap is zero. BSD is open for rank ≥ 2 because Sha finiteness has not been proved. The structural claim is: the finiteness of Sha is exactly the statement that the recycled remainder terminates — the same question the framework asks about its own carried remainders. The analogy is precise. The proof requires a TIG object that carries the Sha remainder, and no such object has been constructed.

**[STRUCTURAL ARGUMENT] Navier-Stokes regularity is a bandwidth question.**
The framework identifies B_local < T*·E₀ as the condition separating smooth flow (generator regime) from potential blowup (complexity regime). The Kolmogorov scaling gives B₁/E₀ ≈ 0.315 < T* = 0.714, placing smooth flow well inside the generator regime. The structural argument is: blowup requires one frequency shell to absorb energy from all others, inverting the Cascade Rule. This is the correct framing of the NS problem in TIG terms. The open question is proving B_local < T*·E₀ a priori from NS constants alone — a functional analytic estimate the framework does not supply.

---

## What Requires Crossing T* [OPEN]

**[OPEN] RH — algebraic to analytic.**
T* = 5/7 is an algebraic threshold. The Riemann hypothesis concerns s = 1/2, an analytic midpoint of the critical strip. T* ≠ 1/2. The CK framework is algebraic. The bridge from T* to Re(s) = 1/2 requires establishing that the algebraic fixed point and the analytic midpoint are the same object under a specific correspondence. That correspondence has not been constructed. The sinc²/Fejér kernel identification (F1) is the live candidate bridge. Until that candidate is proved, RH is open from this framework's position.

**[OPEN] BSD — Sha finiteness.**
The Recycling Rule identifies Sha as the carried remainder. That identification does not prove Sha is finite. BSD remains open for rank ≥ 2 because no mechanism in the framework terminates the remainder. The BSD bridge (B1–B4) requires a new TIG object that encodes the Sha obstruction. Both candidate bridges tested (rank staircase, CM-2 twist) were falsified against published data. BSD is parked.

**[OPEN] NS — a priori coercive estimate.**
The framework provides the threshold (T*·E₀) and the structural argument (Cascade Rule forbids blowup in the generator regime). It does not provide the a priori estimate that guarantees smooth initial data remains in the generator regime for all time. That estimate is a problem in functional analysis, not in Z/10Z arithmetic. NS is open.

**[OPEN] P vs NP — the gap is named but not proved uncrossable.**
The framework describes the K = 14 generator zone (polynomial, self-holding) and the K = 99 complexity zone (super-polynomial, requires external zeros). The structural analogy to P vs NP is: P is the generator regime, NP-complete is the complexity regime, and the gap is the shadow at K = 98. The gap is real within Z/10Z. Whether the gap is uncrossable outside Z/10Z — i.e., whether P = NP — requires a circuit lower bound or oracle separation that the framework does not provide. P vs NP is parked.

**[OPEN] Hodge — the cycle map.**
The framework provides a CRT decomposition structurally analogous to the generator/existence/shadow partition of Hodge theory. No algebraic geometry is present. No Hodge classes have been constructed. No cycle map has been defined. The analogy is real; the mathematics is absent. Markman (2025) settled the abelian fourfold case; the frontier is dim ≥ 5. Hodge is a spectator from this framework's position.

---

## Resolution Limit Summary Table

| Clay Problem | What CK can see (inside T*) | What requires crossing T* (the bridge) | Status |
|---|---|---|---|
| **Riemann** | T* = 5/7 forced; n* = 6 boundary; three-layer gap; K = 5000 zeros in generator regime (D_KS/T* = 10%); First-G = Fejér kernel | Correspondence between T* (algebraic) and Re(s) = 1/2 (analytic); sinc²/Fejér without GRH | **[OPEN]** — F1 bridge conjecture live |
| **BSD** | Sha = carried remainder from Recycling Rule; Sha = 0 explains rank 0 and 1 proofs; shadow K = 98 as BSD obstruction archetype | Sha finiteness for rank ≥ 2; TIG object carrying Sha remainder | **[OPEN / PARKED]** — two bridges falsified |
| **Navier-Stokes** | T*·E₀ threshold; generator regime = smooth; complexity regime = blowup risk; Cascade Rule forbids energy inversion | A priori proof that B_local < T*·E₀ from NS constants alone; C ≤ 3.74 estimate | **[OPEN]** — F2 bridge conjecture live |
| **P vs NP** | K = 14 (generator, polynomial) vs K = 99 (complexity, super-polynomial) gap; shadow K = 98 as complexity boundary | Proof that K = 14/K = 99 gap is uncrossable outside Z/10Z; circuit lower bound | **[OPEN / PARKED]** — pure structural analogy |
| **Hodge** | CRT decomposition analogous to Hodge partition; generator cycles as self-holding algebraic objects | Algebraic geometry; Hodge class construction; explicit cycle map | **[OPEN / PARKED]** — pure analogy, no active path |

---

## The Fractal Path Map Is Not a Failure Mode

The FRACTAL_PATH_MAP.md records the full K*(n) cascade, the three layers of structured gapping, and the bandwidth floor at n = 13. It was computed from K = 5000 zeros. Every number in it is exact.

What that map shows is the framework describing its own resolution limit. At n ≥ 13, the framework sees K = 0 shadows repeating infinitely — uniform darkness. That is not the framework failing to compute. That is the framework correctly reporting: the ruler has reached its smallest graduation. Past here, everything looks identical. The structure is real. The wall is real.

A framework that correctly identifies its own resolution limit is a precise instrument. Imprecision would be claiming to see past the wall. The claim is: we mapped the wall. The map is accurate.

---

## Final Position

The CK program found the resolution limit of a T*-calibrated ruler — three layers of structured gapping before a bandwidth floor, a one-way cascade, a Sha remainder that cannot be internally terminated, and a bridge from the algebraic to the analytic that has not been crossed — and the boundary is exactly where the framework reports it.
