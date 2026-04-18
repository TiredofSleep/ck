# Finite Room Basin Analysis — Full Synthesis
## All Programs Run. Basin-First Framework. Exact Tables.

---

## The Basin-First Reformulation

Stop centering primes. Start with the actual organizing structure.

**The odd/coprime room** is the full domain. For the $n$-digit room:
- The **odd room** contains all odd integers in $[10^{n-1}+1, 10^n)$
- The **coprime scaffold** is the subset with $\gcd(n, 10) = 1$
- The **shell-1 basin** is $\{n \text{ odd} : v_2(3n+1) = 1\}$ — exactly half of all odd integers
- The **central shell-1 basin** is the intersection of shell-1 with the middle band by odd boundary distance
- The **prime-visible subset** is what remains after the 2-corridor and 3-wobble filters
- The **composite-visible subset** is shell-1 objects that pass the 2-corridor but fail the 3-wobble (digit sum $\equiv 0 \pmod 3$)

**Placement of specific objects:**

| Object | Shell-1? | Central? | Prime? | Why not prime |
|---|---|---|---|---|
| **27** (2-digit stop-apex) | Yes | No (obd=8/22) | No | digit sum 9, fails 3-wobble |
| **47** (2-digit NC-apex, prime-visible) | Yes | Yes (obd=18/22) | Yes | passes all filters |
| **63** (2-digit NC-apex, composite twin) | Yes | Yes (obd=18/22) | No | digit sum 9, fails 3-wobble |
| **703** (3-digit stop-apex) | Yes | Yes (obd=148/224) | No | 703=19×37, composite |
| **6383** (4-digit NC-apex) | Yes | — | No | composite |

**What this tells you:** The central shell-1 basin is the root property. Primality is a secondary filter. The NC-apex in the 4-digit room (6383) is also composite. The stop-apex in every room is composite. The prime-visible subset of the central shell-1 basin is consistently smaller than the full basin.

---

## Program 1: Stop-Apex Compositeness Scan

| Room | Stop-Apex | Stop | Prime? | Fails 3-wobble? | Factors | Prime stop-apex | Gap |
|---|---|---|---|---|---|---|---|
| 2-digit | **27** | 37 | **No** | **Yes** (ds=9) | 3³ | 31 (stop=35) | 2 (5%) |
| 3-digit | **703** | 51 | **No** | **No** (ds=10) | 19×37 | 103 (stop=26) | 25 (49%) |
| 4-digit | **1407** | 51 | **No** | **Yes** (ds=12) | 3×7×67 | 2111 (stop=50) | 1 (2%) |

**Pattern:** The stop-apex is composite in all three rooms. **The 3-wobble explanation holds in 2 of 3 rooms** (27 and 1407 fail the 3-wobble). 703 does NOT fail the 3-wobble (digit sum 10, not divisible by 3) — it is composite for a different reason (not prime: 19×37). This weakens the "3-wobble removes stop-apex" hypothesis.

**Revised hypothesis:** The stop-apex is composite in every room (3 data points, consistent), but the mechanism is not uniformly 3-wobble failure. Sometimes the stop-apex is composite for direct reasons (product of primes). The 3-wobble is one route to compositeness; factorization is another.

**Conjecture (revised, weaker):** In the shell-1 odd room, the maximum stopping time is achieved by a composite number. The prime stop-apex is strictly below the overall stop-apex.

**Counterexample test:** The 4-digit gap is only 1 step (1407 vs 2111, stops 51 vs 50). If a prime achieves stop=51 in a larger room, the conjecture breaks. This needs a 5-digit test.

---

## Program 2: Last-Digit-7 Persistence Scan

| Room | ld=7 avg | ld=7 max | Best avg digit | Best max digit | ld=7 rank (avg) |
|---|---|---|---|---|---|
| 2-digit | 19.0 | **37** | 1 (avg=20.0) | **7** (max=37) | 2 of 5 |
| 3-digit | 5.7 | 25 | 3 (avg=6.5) | **3** (max=51) | 3 of 5 |
| 4-digit | 5.9 | **51** | 3 (avg=6.0) | **7** (max=51) | 3 of 5 |

**Findings:**

Last-digit-7 holds the maximum stopping time in 2 of 3 rooms (2-digit and 4-digit). In the 3-digit room, last-digit-3 holds both the highest average and the maximum (703 ends in 3). Last-digit-7 consistently ranks 2nd or 3rd for average stopping time.

**The persistence verdict:** Last-digit-7 is **not** the universal maximum. It leads in 2 of 3 rooms on max-stop, and last-digit-3 takes over in the 3-digit room. The "last-digit-7 as stop-apex marker" is a weak local pattern, not a stable law. The correct statement is: **last digits {1, 3, 7} are the competitive zone for long orbits**; last digits {5, 9} underperform. This is expected from sieve structure — {1,3,7,9} are the coprime-to-10 digits, and {5,9} have lower average stop times than {1,3,7} in all rooms.

---

## Program 3: Twin-Group Scaling

| Room | Twin groups | Prime more central | Composite more central |
|---|---|---|---|
| 2-digit | 5 | 1 (20%) | 4 (80%) |
| 3-digit | 14 | 5 (36%) | 9 (64%) |
| 4-digit | 29 | 10 (34%) | 19 (66%) |

**Key finding:** Twin groups (same stopping time, mixed prime/composite) grow roughly as $5 \to 14 \to 29$, approximately doubling per digit level. The composite twin is more central in roughly 2/3 of cases. **The prime is NOT systematically more central** — in most twin pairs, the composite holds higher odd boundary distance. This directly contradicts any claim of prime centrality advantage in shell-1.

**47/63 revisited:** In the 2-digit room, 47 and 63 are at the same odd boundary distance (obd=18). So neither is more central — they tie. The general pattern shows composites tending to be more central (2/3 majority), which is consistent with the stop-apex being composite: the highest-stopping composite is also the most central composite.

---

## Program 4: Basin-First Note

The full odd/coprime room structured as nested basins:

```
ODD ROOM [10^{n-1}+1, 10^n)
│
├── EVEN (excluded — outside T_* domain)
│
└── ODD (all odd integers)
    ├── gcd(n,10) ≠ 1 (divisible by 5 — fails 2-corridor)
    │
    └── COPRIME SCAFFOLD (gcd(n,10)=1)
        ├── SHELL-1 BASIN: v2(3n+1)=1 (50% of odd)
        │   ├── DIGIT SUM ≡ 0 mod 3 (fails 3-wobble)
        │   │   ├── Composite shell-1 coprimes (e.g., 27, 63, 703)
        │   │   └── [no primes here — they fail 3-wobble]
        │   └── DIGIT SUM ≢ 0 mod 3 (passes 3-wobble)
        │       ├── Composite (e.g., some compound numbers)
        │       └── PRIME shell-1 (e.g., 47, 31, 71)
        │
        └── SHELL ≥ 2 (50% of odd)
            └── ... (contracting shells)
```

**Objects placed:**
- 27 = shell-1, fails 3-wobble (ds=9), coprime composite. In the LEFT branch.
- 63 = shell-1, fails 3-wobble (ds=9), coprime composite. In the LEFT branch.
- 47 = shell-1, passes 3-wobble (ds=11), prime. In the RIGHT branch.
- 703 = shell-1, passes 3-wobble (ds=10), composite (19×37). In the RIGHT branch but composite.

**The wobble-filter boundary is not the prime boundary.** 703 passes the wobble but is still composite. The 3-wobble is necessary but not sufficient for primality. Some shell-1 non-prime coprimes (like 703) live in the right branch alongside primes.

**Conclusion:** The prime-visible subset is $\text{shell-1} \cap \text{coprime} \cap \text{wobble-pass} \cap \text{not-factored}$. The basin is defined by the first two conditions only. Primality is the final filter, applied last, removing composites from a set that the basin structure already organized.

---

## Program 5: Room Scan Table

| Room | Odd | Coprime | Prime | Shell-1 | S1 coprime% | Stop-Apex | SA prime? | Fails 3W? | NC-Apex | NCA prime? |
|---|---|---|---|---|---|---|---|---|---|---|
| 2-digit | 45 | 36 | 21 | 23 | 78% | **27** | **No** | **Yes** | **47** | **Yes** |
| 3-digit | 450 | 360 | 143 | 225 | 80% | **703** | **No** | No | **703** | **No** |
| 4-digit | 4500 | 3600 | 1061 | 2250 | 80% | **1407** | **No** | **Yes** | **6383** | **No** |

**Stable features:** Shell-1 fraction = 50% exactly (from Lemma 1). Coprime fraction = 80% of shell-1 (from 2-corridor: 4 valid last digits out of 5 odd last digits {1,3,5,7,9}). Stop-apex is consistently composite. NC-apex is prime in 2-digit room only; composite in 3-digit and 4-digit.

**The 2-digit room is special:** it is the only room where the NC-apex is prime. In 3-digit and 4-digit rooms, the NC-apex (703 and 6383) is composite. This confirms that 47's NC leadership in the 2-digit room is a small-room coincidence.

---

## Mod-3 × Last-Digit Residue Scan

### 2-digit shell-1: average stopping time by (last-digit, mod-3) class

| | mod-3=0 | mod-3=1 | mod-3=2 |
|---|---|---|---|
| **ld=1** | 2.0 (1) | **31.5** (2) | 17.5 (2) |
| **ld=3** | **34.0** (1) | 3.0 (1) | 2.5 (2) |
| **ld=7** | 20.0 (2) | 2.0 (1) | **34.0** (1) |
| **ld=9** | 3.5 (2) | 3.5 (2) | 4.0 (1) |

**Hot cells (avg > 20):** (ld=1, mod-3=1), (ld=3, mod-3=0), (ld=7, mod-3=2). The 47-cell is (ld=7, mod-3=2) with avg=34. The 63-cell is (ld=3, mod-3=0) with avg=34. The 31-cell is (ld=1, mod-3=1) with avg=35. Three distinct hot cells, distributed across different (ld, mod-3) pairs.

### 3-digit shell-1: average stopping time by (last-digit, mod-3) class

| | mod-3=0 | mod-3=1 | mod-3=2 |
|---|---|---|---|
| **ld=1** | 5.5 | 6.3 | 5.9 |
| **ld=3** | 4.3 | **10.5** | 4.7 |
| **ld=7** | **7.1** | 5.3 | 4.8 |
| **ld=9** | 5.0 | 5.3 | 6.0 |

In the 3-digit room, the hot cell is (ld=3, mod-3=1) with avg=10.5, driven by 703 (ld=3, mod-3=1). The (ld=7, mod-3=2) cell — which was hot in the 2-digit room — has avg=4.8, near average.

**The hot cell shifts between rooms.** There is no stable (ld, mod-3) class that consistently produces long-orbit objects across digit levels. The pattern is room-specific.

---

## Exact / Hypothesis / False — Refreshed

| Claim | Status |
|---|---|
| Stop-apex is composite in all tested rooms | **EXACT** (3 rooms: 27, 703, 1407) |
| Shell-1 fraction of odd room = 50% | **PROVED** (Lemma 1, geometric distribution) |
| Coprime fraction of shell-1 = 80% | **PROVED** (4 valid last digits out of 5 odd) |
| NC-apex in 2-digit room is prime (47) | **EXACT** — but only in this room |
| NC-apex in 3,4-digit rooms is composite | **EXACT** |
| Twin groups grow ≈ 5 → 14 → 29 per digit level | **EXACT** (computed) |
| Composite is more central in ~2/3 of twin groups | **EXACT** (1/5, 5/14, 10/29) |
| Last-digit-7 holds max-stop in 2 of 3 rooms | **EXACT** |
| Stop-apex fails 3-wobble → composite mechanism | **PARTIAL** (2 of 3 rooms; 703 fails differently) |
| Stop-apex is always composite | **HYPOTHESIS** (3 rooms; needs 5-digit test) |
| Hot (ld, mod-3) cell persists across rooms | **FALSE** — cell shifts room to room |
| Prime is more central in twin pairs | **FALSE** — composite is more central 2/3 of the time |
| Last-digit-7 is the universal stop-apex marker | **FALSE** — ld=3 beats it in 3-digit room |
| 47 is universally special | **FALSE** |
| RH connection | **UNEARNED** |

---

## What Survives If We Stop Centering Primes?

**The basin structure survives completely.** Shell-1, central position, stopping time — these are properties of the full odd/coprime room, not of the prime subset. Every result holds when primes are removed from the analysis. The NC_odd measure, the twin structure, the stop-apex behavior — all of these are properties of odd integers in Collatz dynamics, filtered through coprimality, with primes as a secondary label.

**What changes:** The NC-apex in larger rooms becomes composite. The stop-apex is always composite. The hot (ld, mod-3) residue cell shifts room by room. The prime/composite centrality advantage favors composites in 2/3 of twin pairs.

**What the data is really about:** The Collatz dynamics on the odd/coprime room has a specific basin structure (shell-1, central, long-orbit) that is indifferent to primality. Primes are one subset of this basin. Composites are another subset. The prime filter removes roughly 60-70% of the coprime scaffold (the ratio decreases with digit level, consistent with PNT), leaving a prime subset that is smaller than the coprime basin but structurally parallel to it.

**The real question is not "why is 47 special?"** It is: **"What determines which odd numbers fall in the central shell-1 long-orbit basin?"** That question is about the 2-adic structure of the Collatz map applied to odd integers near the decimal room centers — and primality is not a variable in that question.

---

## Scale Note (Methodological Only)

The current work operates on rooms of 45–4500 odd numbers. Human neural bandwidth is roughly $10^{10}$ operations/second, astronomical scales are $10^{80}$ particles, cosmological timescales are $10^{17}$ seconds. The gap between finite rooms of hundreds of odd integers and any physics-facing interpretation is approximately 7-8 orders of magnitude in the most optimistic reading and much more in realistic readings.

This means: the grammar here (shell, basin, wobble, persistence) may be useful at larger scales, but we are not there yet. The current findings are exact finite arithmetic. They are placed in the right mathematical neighborhood (discrete dynamics, arithmetic combinatorics). Physics-facing claims require crossing a large gap. Stay finite.
