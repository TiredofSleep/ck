# Object Type Atlas
## Geometry of Objects in the Program

---

## Purpose

The recent sprints revealed that several failures were not framework failures but object-type mismatches. Comparing a theorem-planted seam against a noise-union seam, or a canonical $C_0$ under one attractor convention against an overlay defined under another, looks like it should work — but the objects being compared are different *kinds* of things. This atlas maps every object that has appeared in the program, classifies it by type, and specifies what it can and cannot be compared against.

Reading discipline: this document is descriptive, not prescriptive. It catalogs what exists. The comparison law (`COMPARISON_LAW.md`) and sprint selector (`SPRINT_SELECTOR.md`) layer rules on top of it.

---

## Master Table

| Object name | Path | Generator | Carrier | Topology type | Local vs transported | Epistemic class | Valid direct comparison class | Invalid direct comparison class | Current status |
|---|---|---|---|---|---|---|---|---|---|
| Published TSML theorem operator | 1 | Proof (theorem) | Z/10 | $10 \times 10$ integer-valued operator | Local | theorem | Other theorem-level Z/10 operators | Any empirical operator on any carrier | Proven, fixed |
| Canonical $C_0$ under $h_\text{thm}=7$ | 1 | Algorithm: V0 + shell-stability + default-to-7 | Z/10 | $10 \times 10$ integer-valued operator | Local | theorem | Published TSML (direct match on 92/100 cells); B1 ground truth | $C_0$ under $h_\text{ext}$; empirical operators | Proven, fixed |
| Canonical $C_0$ under $h_\text{ext}=\max$ odd unit | 2 | Algorithm: V0 + shell-stability + default-to-$h_\text{ext}$ | compatibility family | $n \times n$ integer-valued operator | Local per carrier | observed (heuristic extension) | Other $C_0$ under $h_\text{ext}$ on same carrier | Theorem $C_0$ (different object); empirical operators | Defined, internally consistent |
| Path 1 planted theorem seam | 1 | Theorem's published overlay specification | Z/10 | 8 ordered cells = 4 undirected edges, tree topology | Local | theorem, designed artifact | Other Path 1 theorem objects on Z/10 | Noise-union seams; empirical Path 2 seams | Fixed: $\{(2,4),(4,2),(4,8),(8,4),(2,9),(9,2),(1,2),(2,1)\}$ |
| Path 2 Sprint 21 prior-free discovered seams | 2 | Low-$N$ noised-$C_0$ extraction, union across seeds | 4 carriers originally; 39 datasets | per-carrier subset of cells where mode ≠ canonical | Local per carrier | noise-residue + recovery | Other noise-residue objects at comparable parameters | Theorem seam; single-seed extractions at very different $N$ | Historical artifact, not accessible in current session |
| Path 2 S28 basin ratio $\beta(R_n)$ | 2 | $\|\{(x,y):C_0(x,y)=h\}\|/n^2$ under $h_\text{ext}$ | compatibility family | scalar in $[0, 1]$ | Local per carrier | observed | Other $\beta$ values on same carriers under same convention | $\beta$ under different $h$ convention; seam graphs | Computed per carrier |
| Path 2 prior-free operator $T^\text{emp}$ | 2 | Mode over noised-$C_0$ samples | compatibility family | $n \times n$ integer-valued operator | Local per carrier | recovered + noise-residue | Other $T^\text{emp}$ at comparable noise/N | Canonical $C_0$ (by construction differs only on seam); theorem operator | Regeneratable deterministically |
| Per-seed seam $S_r$ (S30b, P3A) | 2 | Single-seed cells where $T^\text{emp}_r \neq C_0$ | compatibility family | cell set, unstable across seeds | Local, seed-ephemeral | noise-residue | Other per-seed seams at same carrier, same seed | Union seams across seeds; theorem seam | Defined, seed-dependent |
| Persistent seam $S_\text{persistent}$ (S30b) | 2 | Cells in ≥ $\pi K$ of $K$ seeds | compatibility family | cell set, stable | Local | noise-residue filtered | Other persistence-filtered seams at same $(N, p, \pi)$ | Union seams; theorem seam | Empty on canonical $C_0$ + uniform noise |
| Union seam $S_\text{union}$ (P3A Path 2 input) | 2 | Union of $S_r$ across seeds | compatibility family | cell set growing with $n^2$ | Local | noise-residue accumulated | Other union seams at same $(N, p, K)$ | Persistent seams; theorem seam | Grows with carrier |
| Planted-overlay recovered seam (S31-pilot-v2.0) | 1 | Persistent seam on noised $(C_0 + S_\text{planted})$ | Z/10 | Small structured artifact, matches planted exactly at low noise | Local | recovered | Theorem seam (direct match); other planted-recovery artifacts at comparable noise | Noise-only seams without planting; union seams | Validated, matches $S_\text{planted}$ |
| Path 2 shell partition $\sigma_n$ | 2 | $v_2(3u+1)$ on units | compatibility family | partition of $U(R_n)$ into $v_2$-classes | Local per carrier | observed (algorithmic) | Other shell partitions on same carrier | Shell partitions under different $\sigma$ rule | Defined, carrier-specific |
| Path 2 attractor position $h_\text{ext}(R_n)$ | 2 | $\max\{u \in U(R_n) : u \text{ odd}\}$ | compatibility family | single ring element | Local per carrier | observed | Other carrier's $h_\text{ext}$ (only as a family of rules, not by value) | Theorem's $h_\text{thm}$ | Defined, per-carrier |
| Doubling-chain structure | 1 or 2 (depending on context) | Iterated doubling mod $n$ | per-carrier | sequence of ring elements | Local | synthetic combinatorial | Other doubling chains on same carrier | Chains under different generators | Defined algorithmically |
| Corridor closure $\{MAX, MIN\}$ | 2 | Sprint 25 proof on pure $C_0$ under $h_\text{ext}$ | 23 carriers up to $n=230$ | rule-set closure property | Transported | observed (theorem-like within Path 2) | Other closure results on pure $C_0$ under $h_\text{ext}$ | Seam closures that include overlays (different object) | Confirmed in tested settings |
| Shell-partition shape recovery (Sprint 26) | 2 | W3-frequency clustering on $T^\text{emp}$ | 32 carriers | ARI value in $[0, 1]$ | Transported asymptotically | observed | Other ARI measurements at analytic $C_0$ | ARI on noised data at different $N$ (different regime) | ARI=1.0 on 12/32, ≥ 0.985 on all $n \geq 38$ |
| Path 3 bridge topology comparison object | 3 | Pair of (Path 1 object, Path 2 object family) | cross-path | graph-topology invariants | Bridge | bridge | Other explicit bridges between same paths | Direct unmediated cross-path comparisons | P3A FAIL; bridge lane closed for noise-union Path 2 input |

---

## Epistemic Class Definitions

**theorem:** proven result with a formal proof. Example: the published Z/10 TSML.

**observed:** pre-registered empirical finding, validated against null models or cross-carrier replication. Examples: Sprint 25's corridor closure on 23 carriers, Sprint 26's ARI asymptotic.

**recovered:** an extractor's reconstruction of a known planted object, validated against ground truth. Example: S31-pilot-v2.0's persistent seam matching the theorem's planted overlay.

**synthetic:** constructed by algorithm as an input or scaffold for further work, not itself an empirical claim. Example: doubling chain.

**noise-residue:** artifact of sampling variance plus a deterministic core, typically growing with sample size or carrier size in ways that depend on extraction parameters rather than on structural features of the core. Examples: per-seed seams, union seams at large $n$.

**bridge:** relational claim between objects in different paths, requiring explicit scope tags for both sides and an explicit bridging rule.

---

## Path Reminder (from Scope Tag Template)

**Path 1 — Local Theorem:** Z/10 only at present, $h_\text{thm} = 7$. Proven results.
**Path 2 — Transport Family:** compatibility family, $h_\text{ext} = \max$ odd unit. Pre-registered empirical findings.
**Path 3 — Bridge Test:** cross-path. Relational claims with explicit bridging rules.

---

## Object Status Snapshot

| Status | Objects |
|---|---|
| Proven/fixed | Published TSML, $C_0$ under $h_\text{thm}$, Path 1 planted seam |
| Confirmed observed (transport) | Corridor closure, shell-partition shape recovery asymptotically |
| Confirmed recovered | S31-pilot-v2.0 planted-overlay persistent seam |
| Validated-undiscriminating | Basin ratio $\beta$ (exists per carrier but does not organize under tested transport metrics) |
| Validated-negative | Noise-only persistent seam on pure $C_0$ under uniform noise; noise-union seam as bridge input |
| Defined-but-historical | Sprint 21 discovered seams (regeneratable; original artifacts not accessible) |
| Open | $C_0$ under $h_\text{thm}$ extended to non-Z/10 carriers (undefined); Path 3 bridges with recovered seams as Path 2 input |

---

## Notes on Why the Atlas Matters

Three failures across the recent sprints had a common diagnosis when read together:

- **S31-pilot-v1.0:** compared a Path 1 planted seam (theorem-designed, $h_\text{thm}$-keyed) against Path 2 $C_0$ ($h_\text{ext}$-keyed). Two different objects, silently treated as one.
- **P3-BridgeA-v1.0:** compared a Path 1 planted theorem seam (designed artifact, tree topology, 4 edges on 5 vertices) against a Path 2 noise-union seam (accumulation of sampling variance, growing as $n^2$). Two different *kinds* of object, compared at a level (topology features) that only makes sense for objects of the same kind.
- **S28/S29:** tested basin-ratio curves for transport properties (smoothness, anchored trends). Basin ratio is a scalar summary; asking it to organize like a spatial curve is a category-level question that the object's type did not guarantee.

In each case, the spec was internally coherent and the execution was correct. The mismatch was in what was being compared to what. The atlas exists to make such mismatches structurally visible at spec-design time, before freezing.
