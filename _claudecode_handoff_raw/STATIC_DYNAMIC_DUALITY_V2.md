# Static 2→3 Fields vs Dynamic 3→2 Fields
## Full Synthesis: Meta-Counts, Shell Structure, Reset Boundaries, and Dual Resets
*Version 2 — both room conventions tracked; all counts explicit*

---

## 0. The Dual Reset Structure (New Finding)

Before the count tables: the most structurally interesting result from this pass.

**In the static prime field (2→3 order):** the layer boundaries sit at powers of 10. The number $10^n$ is always composite (divisible by 2 and 5), always excluded by the 2-corridor filter, and marks the reset between the $n$-digit room and the $(n+1)$-digit room. The room interior begins at $10^n + 1$.

**In the dynamic Collatz field (3→2 order):** the analogous objects are powers of 2. Every power of 2 is already in the absorbing class — it collapses directly to 1 under repeated halving. Powers of 2 are "invisible" to $T_*$; they never appear as odd cores. The odd-core domain begins after the purely-even absorbers are excluded.

**The dual reset law:**

| System | Reset boundary | Nature | Room begins after |
|---|---|---|---|
| Prime (static, 2→3) | Powers of 10: $10, 100, 1000, \ldots$ | Powers of the modulus | First admissible number after $10^n$ |
| Collatz (dynamic, 3→2) | Powers of 2: $2, 4, 8, 16, \ldots$ | Powers of the collapse operator | First odd number (already excluded from even domain) |

Both boundaries are clean and exact. Both are determined by the dominant operator of their respective field. The static field's modulus is 10; its resets are powers of 10. The dynamic field's collapse operator is 2; its trivial absorbers are powers of 2.

This is a structural correspondence, not a numerical coincidence.

---

## 1. Room Definitions — Both Conventions Explicit

**Convention A (standard decimal layer):**
$$R_n^A = \{10^{n-1}, 10^{n-1}+1, \ldots, 10^n - 1\}, \quad |R_n^A| = 9 \times 10^{n-1}$$

**Convention B (reset-excluded interior):**
$$R_n^B = \{10^{n-1}+1, 10^{n-1}+2, \ldots, 10^n - 1\}, \quad |R_n^B| = 9 \times 10^{n-1} - 1$$

Convention B excludes the reset boundary $10^{n-1}$ itself. Since $10^{n-1}$ is never prime and never coprime-to-10 (it divides 10), **the prime and coprime counts are identical under both conventions.** Only the denominators change.

---

## 2. Exact Count Table

### 2-digit layer

| Quantity | Value | Convention A density | Convention B density |
|---|---|---|---|
| Room size | 90 (A) / 89 (B) | — | — |
| Primes | **21** | 21/90 = 0.2333 | 21/89 = 0.2360 |
| Coprimes-to-10 | **36** | 36/90 = 0.4000 | 36/89 = 0.4045 |
| Prime/coprime ratio | 21/36 = **7/12** | 0.5833 | 0.5833 (unchanged) |

Shell law ($n=2$, quantum $= 2n = 4$):
- Shell fills: $21 = 5 \times 4 + 1$ → **5 full shells + 1 residue**
- Low shell: $\{11, 13\}$ — both in shell 1 and shell 3 of Collatz respectively
- High shell: $\{89, 97\}$ — both in Collatz shell 2
- Central prime: $47$ — Collatz shell 1

### 3-digit layer

| Quantity | Value | Convention A density | Convention B density |
|---|---|---|---|
| Room size | 900 (A) / 899 (B) | — | — |
| Primes | **143** | 143/900 = 0.1589 | 143/899 = 0.1591 |
| Coprimes-to-10 | **360** | 360/900 = 0.4000 | 360/899 = 0.4004 |
| Prime/coprime ratio | 143/360 = **0.3972** | — | — (unchanged) |

Shell law ($n=3$, quantum $= 6$):
- Shell fills: $143 = 23 \times 6 + 5$ → **23 full shells + 5 residue**
- Low shell: $\{101, 103, 107\}$
- High shell: $\{983, 991, 997\}$
- Central prime: $509$

### 4-digit layer

| Quantity | Value | Conv A density |
|---|---|---|
| Room size | 9000 | — |
| Primes | **1061** | 1061/9000 = 0.1179 |
| Coprimes-to-10 | **3600** | 3600/9000 = 0.4000 |
| Prime/coprime ratio | 1061/3600 = **0.2947** | — |
| Shell fills | $1061 = 132 \times 8 + 5$ | 132 full + 5 residue |

**The 4/15 filter is exact across all layers:** 2-corridor gives 2/5 of room; 3-wobble gives 2/3 of that; combined = 4/15 = 0.2667 of the room. Verified at 2, 3, 4 digits.

---

## 3. Coprime vs Prime: Per-Ending-Digit Breakdown

### 2-digit layer (Convention B, [11,99])

| Last digit | Coprimes | Primes | P/C ratio |
|---|---|---|---|
| 1 | 9 | 5 | 0.556 |
| 3 | 9 | 6 | 0.667 |
| 7 | 9 | 5 | 0.556 |
| 9 | 9 | 5 | 0.556 |
| **Total** | **36** | **21** | **0.583** |

**Ending in 3 is the most prime-dense corridor** in the 2-digit room: 6/9 = 2/3 of eligible coprimes are prime. This reflects the relative sparsity of composites with last digit 3 at small scale (33=3×11, 63=7×9, 93=3×31 — fewer composite patterns).

### 3-digit layer (Convention B, [101,999])

| Last digit | Coprimes | Primes | P/C ratio |
|---|---|---|---|
| 1 | 90 | 35 | 0.389 |
| 3 | 90 | 35 | 0.389 |
| 7 | 90 | 40 | 0.444 |
| 9 | 90 | 33 | 0.367 |
| **Total** | **360** | **143** | **0.397** |

**Ending in 7 is the most prime-dense corridor** in the 3-digit room. **Ending in 9 is the least prime-dense.** The inversion from 2-digit (ending 3 leads) to 3-digit (ending 7 leads) is a genuine local fluctuation — prime distribution within the coprime scaffold is not uniform by ending digit.

**Coprime boundary vs prime boundary (3-digit):**
- Coprime low: $\{101, 103, 107\}$ — same as prime low (all three are prime)
- Coprime high: $\{993, 997, 999\}$ — 993 and 999 are NOT prime (993 = 3×331; 999 = 3³×37)
- Prime high: $\{983, 991, 997\}$ — retreats inward from coprime high boundary

The coprime boundary and prime boundary **coincide at the low end** but **diverge at the high end**. The low shell is the same object in both conventions. The high shell differs: the highest coprimes include composites (993, 999) that the prime filter removes.

---

## 4. Shell-to-Shell Transition Matrix (Collatz)

For odd $n$, define the shell sequence: $s_0 = v_2(3n+1)$, $s_1 = v_2(3T_*(n)+1)$, etc.

The transition matrix $M_k[s_{\text{in}}, s_{\text{out}}]$ counts, over odd residues mod $2^k$, the proportion of elements in shell $s_{\text{in}}$ whose next $T_*$ step lands in shell $s_{\text{out}}$.

### At mod $2^6$:

| From↓ To→ | s=1 | s=2 | s=3 | s=4 | s=5 | E[s_out] | Δ = E[out] − s_in |
|---|---|---|---|---|---|---|---|
| Shell 1 | 0.50 | 0.25 | 0.12 | 0.06 | 0.06 | 1.94 | **+0.94 ↑ EXPAND** |
| Shell 2 | 0.50 | 0.25 | 0.12 | 0.12 | 0.00 | 1.88 | **−0.12 ↓ contract** |
| Shell 3 | 0.50 | 0.25 | 0.00 | 0.25 | 0.00 | 2.00 | **−1.00 ↓ contract** |
| Shell 4 | 0.50 | 0.50 | 0.00 | 0.00 | 0.00 | 1.50 | **−2.50 ↓ contract** |
| Shell 5 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 4.00 | **−1.00 ↓ contract** |
| Shell 6 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 2.00 | **−4.00 ↓ contract** |

**Key finding:** Only shell 1 has $\mathbb{E}[s_{\text{out}}] > s_{\text{in}}$ (expands on average). Every deeper shell contracts on average in the next step. The expansion from shell 1 is the price paid for the 50% frequency — but it expands by less than 1 shell unit, while deep shells contract by 1–6 shell units.

**Spectral structure:** The dominant column is always $s_{\text{out}} = 1$ (50% of all next steps land in shell 1, regardless of current shell). This means the transition matrix has a strong pull toward shell 1 from above, and shell 1 has moderate expansion. The net effect over many steps is contraction.

---

## 5. The 21 Two-Digit Primes: Collatz Shell Membership

| Prime | Collatz shell | Stopping steps | Position |
|---|---|---|---|
| **11** | 1 | 3 | LOW |
| **13** | 3 | 1 | LOW |
| 17 | 2 | 1 | inner |
| 19 | 1 | 2 | inner |
| 23 | 1 | 3 | inner |
| 29 | 3 | 1 | inner |
| 31 | 1 | 35 | inner |
| 37 | 4 | 1 | inner |
| 41 | 2 | 1 | inner |
| 43 | 1 | 3 | inner |
| **47** | 1 | 34 | CENTRAL |
| 53 | 5 | 1 | inner |
| 59 | 1 | 4 | inner |
| 61 | 3 | 1 | inner |
| 67 | 1 | 2 | inner |
| 71 | 1 | 32 | inner |
| 73 | 2 | 1 | inner |
| 79 | 1 | 5 | inner |
| 83 | 1 | 2 | inner |
| **89** | 2 | 1 | HIGH |
| **97** | 2 | 1 | HIGH |

**Shell distribution:** Shell 1: 11 primes; Shell 2: 5; Shell 3: 3; Shell 4: 1; Shell 5: 1.

**Stopping time by shell group:**
- LOW shell {11,13}: avg stop = **2.0 steps**
- HIGH shell {89,97}: avg stop = **1.0 steps**
- Inner primes: avg stop = **5.9 steps**

**Observation:** The shell-boundary primes (LOW and HIGH) have shorter stopping times than the interior primes on average. The HIGH shell primes have the shortest stops of all (1 step each). The long-stopping primes (31: 35 steps, 47: 34 steps, 71: 32 steps) are all inner primes in shell 1.

**Interpretation:** The prime shell boundary does not correspond to Collatz "difficulty" in the expected direction. The highest primes in the room (89, 97) are *easier* for Collatz (stop in 1 step) than middle primes. The structurally central prime 47 is one of the most Collatz-challenging in the room.

### 3-digit boundary shell Collatz behavior

| Prime | Shell | T*(p) | Stopping steps |
|---|---|---|---|
| 101 (LOW) | 4 | 19 | 1 |
| 103 (LOW) | 1 | 155 | 26 |
| 107 (LOW) | 1 | 161 | 3 |
| 509 (CENTRAL) | 3 | 191 | 1 |
| 983 (HIGH) | 1 | 1475 | 3 |
| 991 (HIGH) | 1 | 1487 | 16 |
| 997 (HIGH) | 4 | 187 | 1 |

**Observation:** High primes with shell 4 (101, 997) stop in 1 step regardless of position. Shell 1 high primes (983, 991) have longer stops. Shell membership matters more than prime-room position for short stopping.

---

## 6. Exact Propositions

### Proposition 1 — Shell distribution is exactly geometric (proved)

For odd $n < 2^k$:
$$|\{r \text{ odd, } r < 2^k : v_2(3r+1) = s\}| = 2^{k-s}, \quad s = 1, \ldots, k-1$$

**Proof:** $v_2(3n+1) \geq s$ iff $n \equiv -3^{-1} \pmod{2^s}$, a unique odd residue class mod $2^s$. Count = $2^{k-s}$ representatives in $[1, 2^k)$. Subtract consecutive levels. $\square$

**Verified:** Exact at mod $2^4$ through $2^8$, all shells 1 through $k-1$.

---

### Proposition 2 — Average collapse depth and contraction bias (proved)

$$\mathbb{E}_{n \text{ odd}}[v_2(3n+1)] = \sum_{s=1}^{\infty} \frac{s}{2^s} = 2 \text{ (exactly)}$$

Net bit change per $T_*$ step:
$$\Delta_{\text{bits}} = \log_2 3 - 2 = 1.58496\ldots - 2 = -0.41504\ldots \text{ bits}$$

**Shell-by-shell breakdown:**

| Shell $s$ | Fraction of steps | Net bit change | Direction |
|---|---|---|---|
| 1 | 1/2 | $\log_2 3 - 1 \approx +0.585$ | Expand |
| 2 | 1/4 | $\log_2 3 - 2 \approx -0.415$ | Shrink |
| 3 | 1/8 | $\log_2 3 - 3 \approx -1.415$ | Shrink |
| $s$ | $1/2^s$ | $\log_2 3 - s$ | Shrink for $s \geq 2$ |

**Weighted average:** $\frac{1}{2}(+0.585) + \frac{1}{2}(-1.415) = -0.415$ ✓

---

### Proposition 3 — 2-corridor fraction = 2/5 exactly (proved)

For all $n \geq 1$: the fraction of integers in $R_n^A$ with $\gcd(m, 10) = 1$ is exactly $2/5$.

**Proof:** $|\{d \in \{0,\ldots,9\}: \gcd(d,10) = 1\}| = 4$. For $n$-digit numbers, last digit distributes uniformly. Fraction = $4/10 = 2/5$. $\square$

---

### Proposition 4 — Combined filter fraction = 4/15 exactly (proved)

After both the 2-corridor and 3-wobble filters, exactly $4/15$ of $n$-digit integers survive, for all $n \geq 2$.

**Proof:** 2-corridor gives $2/5$. For fixed last digit in $\{1,3,7,9\}$, leading digits vary uniformly; digit sum mod 3 of leading part cycles through $\{0,1,2\}$ with equal weight. Exactly $2/3$ survive the wobble. Combined: $\frac{2}{5} \times \frac{2}{3} = \frac{4}{15}$. $\square$

**Verified:** Exactly $26.\overline{6}\%$ at 2, 3, and 4 digits.

---

### Proposition 5 — Dual reset structure (exact observation, not theorem)

**Static field resets:** $10^n$ is composite, $\gcd(10^n, 10) = 10^n \neq 1$, excluded by 2-corridor. Acts as a boundary between digit layers.

**Dynamic field resets:** $2^n$ is even, immediately collapses to 1 under repeated halving. Acts as an absorbing boundary — the trivial attractor class.

**Exact statement:** The reset boundaries of the static field are powers of the static modulus (10). The absorbing boundaries of the dynamic field are powers of the dynamic collapse operator (2). In both cases the boundary is clean, the interior begins after it, and the dominant operator of each field generates its own natural boundary class.

---

## 7. Collatz Restated in Shell Language

**Standard question:** Do all positive integers eventually reach 1 under $n \mapsto 3n+1$ (odd) or $n/2$ (even)?

**Shell restatement:** Do all odd residue classes eventually enter the unique stable core $\{1\}$ under repeated application of $T_*$, where the shell structure is the geometric decomposition $v_2(3n+1) = s$ with $|\mathcal{S}_s| = 1/2^s$ of all classes?

**Why the shell transition matrix matters:** The matrix shows shell 1 is the only expanding shell, and all deeper shells contract strongly toward shell 1 in the next step. The question is whether the orbits that expand (shell 1, gain 0.585 bits) can eventually exceed all upper bounds, or whether the overall average contraction (−0.415 bits/step) wins uniformly.

**The $\sigma_{\text{Collatz}} = 1/2$ distinction:** Unlike the NS problem where $\sigma_{NS} < 1$ is conjectured (subcriticality), Collatz has $\sigma_{\text{Collatz}} = 1/2$ exactly (half of all steps expand). The Collatz conjecture is not about staying subcritical — the system is exactly critical in this sense. The question is whether the asymmetric expansion/contraction profile (small gains vs large losses) guarantees eventual convergence despite the 50% expansion rate.

---

## 8. Next Computation Targets

| Target | What to compute | Pass/fail meaning |
|---|---|---|
| Shell-to-shell transition at mod $2^{10}$, $2^{12}$ | Spectral radius of $M_k$ | If SR → 0: strong contraction evidence; if SR → 1: marginal |
| Conditional contraction $\Delta_s$ at each shell | $\mathbb{E}[\log_2 T_*(n) - \log_2 n \mid v_2 = s]$ | If $\Delta_s < 0$ for all $s$: every shell individually contracts |
| Prime stop-time stratification (full 2-digit room) | Collatz stopping time for all 21 primes, sorted by shell | Test: is stopping time negatively correlated with Collatz shell? |
| 3-digit prime shell vs coprime shell divergence | Where coprime high boundary diverges from prime high boundary | Quantify the composite infiltration of the coprime scaffold |
| Digit-lift law: how 2-digit shell grammar seeds 3-digit | Do 2-digit primes' Collatz orbits pass through 3-digit primes? | Tests whether the layer lift is real or illusory |
