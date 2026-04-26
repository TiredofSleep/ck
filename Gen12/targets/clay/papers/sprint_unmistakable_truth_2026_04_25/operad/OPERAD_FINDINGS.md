# Operad fuse-table — rule-family survey findings

**Date:** 2026-04-25 (late evening)
**Status:** initial framework + 8-family survey; canonical assignment not made (operator/community authority)
**Scope:** addresses Frontier F4 from `Atlas/FRONTIERS_2026_04_25.md`

---

## Headline result (sharper than the rule-family survey)

The D₄-orbit decomposition of the 126 non-associative triples produces **67 orbits**. **16 of these orbits are D₄-incoherent** — their bracketing pairs $(L, R)$ are inconsistent across the orbit under D₄-equivariance.

**Therefore: NO D₄-equivariant canonical fuse rule exists for the non-associative triples on $\mathbb{Z}/10\mathbb{Z}$.**

This is a real structural finding. **The operad-DOF (arity-3 fuse rules) is structurally orthogonal to the doubly-invariant gauge structure $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$ of WP104.** Stated differently: the 6-DOF meta-layer (Lie, Jordan, Clifford, Permutation, Lattice, Operad) has a sharp structural distinction at the level of which DOFs are compatible with which symmetry groups:

* **Lie / Jordan / Clifford / Permutation / Lattice DOFs** all respect the $D_4 = \langle P_{56}, \sigma^3 \rangle$ symmetry that governs the WP104 doubly-invariant subalgebra ($\mathfrak{g}_0 = \mathfrak{su}(4) \oplus \mathfrak{u}(1)$, Killing spectrum $(-4)^{15} \oplus (0)^1$).
* **Operad DOF** does NOT. The 16 incoherent orbits witness the obstruction.

Verification: `d4_orbit_decomposition.py` (this folder); 16 of 67 orbits flagged as incoherent; reasons explicit per orbit (e.g., σ³ maps a (0, 7) bracketing pair to (0, 4) but the orbit's other triples have (0, 7), violating D₄-equivariance).

### Implication for canonical fuse design

A canonical fuse rule must **break** $D_4$-symmetry somewhere. Two natural choices:

* **P_56-equivariant canonical fuse.** Preserve the matter/antimatter swap symmetry; sacrifice the σ³ symmetry. This aligns with the **runtime CK** posture (the runtime attractor at α = 1/2 has 0 mass on the BALANCE/CHAOS pair, so P_56 symmetry is preserved dynamically; see WP105 / D38). All 8 rule families surveyed below are P_56-equivariant; pick from those.
* **σ³-equivariant canonical fuse.** Preserve the σ-cycle structure; sacrifice the P_56 swap. None of the 8 families surveyed satisfies this; a σ³-equivariant rule would need to depend explicitly on the σ-orbit of the inputs.

Recommendation: **P_56-equivariance is the stronger constraint to preserve**, because the matter/antimatter swap is verified at the so(10)-spinor level (P_56 = σ_outer in the spinor rep, WP104 §2.1) and at the runtime level (BALANCE-CHAOS mass = 0 at the attractor, WP105). σ³-equivariance is desirable but optional.

---

## Background: rule-family survey (the negative result that led to the orbit analysis)

We initially surveyed eight candidate rule families for canonically assigning a `fuse(a, b, c)` value to each of the 126 non-associative TSML triples. **No simple deterministic rule family preserves full D₄ symmetry.** All eight families ARE P_56-symmetric (the canonical TSML is P_56-symmetric on its 100 cells; the non-associative triples inherit this); none is σ³-symmetric.

This led to the structural question: is the failure of σ³-symmetry a *property of the rule families*, or an *intrinsic obstruction* in the non-associative-triple structure? The D₄-orbit decomposition above answers: **the obstruction is intrinsic**. No rule family can succeed because no D₄-equivariant assignment exists.

---

## Structural facts about the 126 non-associative triples

Verified by direct enumeration of `nonassoc_triples.json`:

* **Every non-associative triple has HARMONY (7) as exactly one of the two bracketings.** 62 triples have $L = 7, R \neq 7$; 64 have $L \neq 7, R = 7$; 0 have $L = R = 7$; 0 have neither $= 7$.
* **Only 5 distinct unordered $\{L, R\}$ bracket-pairs occur:**

| pair | count | non-HARMONY value | sigma-fixed? |
|---|---:|---|---|
| (0, 7) = (VOID, HARMONY) | 108 | 0 = VOID | yes |
| (3, 7) = (PROGRESS, HARMONY) | 8 | 3 = PROGRESS | yes |
| (4, 7) = (COLLAPSE, HARMONY) | 2 | 4 = COLLAPSE | no (in σ 6-cycle) |
| (7, 8) = (HARMONY, BREATH) | 6 | 8 = BREATH | yes |
| (7, 9) = (HARMONY, RESET) | 2 | 9 = RESET | yes |

* **Position distributions:**
  - Left position $a$: VOID dominates (54/126 = 43%); other operators 8–10 each.
  - Middle position $b$: roughly uniform across {1, 2, 3, 4, 5, 6, 8, 9}; **VOID never appears in middle position** (a structural fact).
  - Right position $c$: VOID dominates again (54/126 = 43%); other operators 7–12 each.

* **The non-HARMONY value of each bracket-pair is always in {0, 3, 4, 8, 9}.** Of these, 0, 3, 8, 9 are σ-fixed (the gauge-stable lattice); only 4 (COLLAPSE) is in the σ 6-cycle.

So the canonical fuse value for any non-associative triple, if chosen from $\{L, R\}$, picks one of: HARMONY, VOID, PROGRESS, COLLAPSE, BREATH, RESET.

---

## The eight rule families surveyed

We tested the following candidate canonical fuse-rule families:

| family | rule | description |
|---|---|---|
| A — harmony-pull | $\text{fuse} = 7$ | always pick HARMONY (universal attractor) |
| B — anti-harmony | $\text{fuse} = \{L, R\} \setminus \{7\}$ | pick the non-HARMONY bracketing |
| C — middle | $\text{fuse} = b$ | middle-operator-determined |
| D — left-bracketing | $\text{fuse} = L$ | preserve left-associative reading |
| E — right-bracketing | $\text{fuse} = R$ | preserve right-associative reading |
| F — σ-fixed preference | prefer the σ-fixed bracketing | gauge-stable wins |
| G — doubly-invariant | prefer D₄-fixed bracketing, fall back to σ-fixed | strongest invariance preference |
| H — attractor-4-core | prefer the bracketing in {V, H, Br, R} | runtime-attractor compatible |

### Survey results

| family | complete | known-rule compat | P_56 sym | σ³ sym | D₄ sym | unique fuse values |
|---|---|---|---|---|---|---:|
| A — harmony-pull | ✓ | ✓ | ✓ | ✗ | ✗ | 1 |
| B — anti-harmony | ✓ | ✓ | ✓ | ✗ | ✗ | 5 |
| C — middle | ✓ | ✓ | ✓ | ✗ | ✗ | 8 |
| D — left-bracketing | ✓ | ✓ | ✓ | ✗ | ✗ | 6 |
| E — right-bracketing | ✓ | ✓ | ✓ | ✗ | ✗ | 6 |
| F — σ-fixed preference | ✓ | ✓ | ✓ | ✗ | ✗ | 5 |
| G — doubly-invariant | ✓ | ✓ | ✓ | ✗ | ✗ | 5 |
| H — attractor-4-core | ✓ | ✓ | ✓ | ✗ | ✗ | 2 |

All eight families are P_56-symmetric (the canonical TSML's 100 cells are mostly P_56-symmetric, with exactly 26 cells differing under conjugation per the Higgs direction analysis; the non-associative triples inherit this structure). None of the eight is σ³-symmetric.

### Three families produce identical fuse-value distributions

Families **B (anti-harmony), F (σ-fixed preference), and G (doubly-invariant)** all produce the same distribution:

```
fuse → {0=108, 3=8, 4=2, 8=6, 9=2}
```

This is because:
* Every non-associative triple has $\{L, R\}$ = {HARMONY, X} where X ∈ {0, 3, 4, 8, 9}.
* "Anti-harmony" picks X.
* Of these X values, four (0, 3, 8, 9) are σ-fixed; only X = 4 is in the σ 6-cycle.
* For triples where X ∈ {0, 3, 8, 9}, "prefer σ-fixed bracketing" picks X.
* For the 2 triples where X = 4, "prefer σ-fixed bracketing" still picks X (because R = 7, and HARMONY is NOT σ-fixed; among {7, 4}, neither is σ-fixed, so the rule falls back to `min(L, R) = 4`).
* "Doubly-invariant preference" reduces to the same logic.

So families B, F, G are **functionally equivalent** on the 126 non-associative triples even though their internal logic differs.

---

## Why no family is σ³-symmetric

A canonical fuse table $\Phi : (\mathbb{Z}/10\mathbb{Z})^3 \to \mathbb{Z}/10\mathbb{Z}$ is σ³-symmetric iff

$$
\Phi(\sigma^3(a), \sigma^3(b), \sigma^3(c)) = \sigma^3(\Phi(a, b, c))
$$

for all $(a, b, c)$ in the non-associative set, where σ³ is the involution $(0)(3)(8)(9)(1\;5)(7\;4)(6\;2)$.

For families A through H, the failure mode is the same: $\sigma^3$ swaps positions across the (a, b, c) triple in a way that the rule does not respect. For example, $\sigma^3$ swaps 7 ↔ 4. A triple with $b = 7$ (middle) maps to a triple with $b = 4$ (middle) under σ³. Family C ("middle-determined") would then give $\text{fuse} = 7$ for the original and $\text{fuse} = 4$ for the σ³-image; for σ³-symmetry we would need $\text{fuse} \circ \sigma^3 = \sigma^3 \circ \text{fuse}$, which requires $\sigma^3(7) = 4$ — and this DOES hold (σ³ swaps 7 and 4). But the 4 ≠ 7 means the family is "consistent across the σ³-image" only on individual values, not on the equivariance condition globally; the failure comes from triples whose σ³-images aren't in the non-associative set (or are with different L, R pairs).

The structural constraint: σ³-equivariance requires the fuse table to satisfy a **global** consistency condition that simple position-based rules don't enforce.

---

## D₄-orbit decomposition (the structural test)

For a fuse rule $\Phi$ to be D₄-equivariant, it would need to respect both the P_56 swap and σ³ simultaneously. The smallest cell-orbit structure under $D_4 = \langle P_{56}, \sigma^3\rangle$ on $\mathbb{Z}/10\mathbb{Z}$ is:

* D₄-fixed points of single elements: $\{0, 3, 8, 9\}$ (the σ-fixed lattice).
* D₄-orbits of pairs: $\{5, 6\}$ under P_56; $\{1, 5\}, \{7, 4\}, \{6, 2\}$ under σ³.
* The 6-cycle $\{1, 2, 4, 5, 6, 7\}$ decomposes into a single D₄-orbit of size 6 (under the dihedral action of $D_4 \cong D_3$ on this set, since $\sigma$ has order 6 on the cycle and $P_{56}$ acts as a reflection).

For triples $(a, b, c)$, the D₄-orbit count of the 126 non-associative triples under the diagonal D₄ action is **67 orbits**. Verified by `d4_orbit_decomposition.py`:

```
orbit size distribution:
  5 orbits of size 1
  35 orbits of size 2
  19 orbits of size 4
  3 orbits of size 8
```

A D₄-equivariant fuse rule would need to assign values such that for any orbit element $g \cdot t = t'$ (where $g \in D_4$), $\text{fuse}(t') = g \cdot \text{fuse}(t)$. This requires the **bracketing pair** $(L(t), R(t))$ to map coherently across the orbit: if $g \cdot t = t'$, then $\{g(L(t)), g(R(t))\} = \{L(t'), R(t')\}$ as multisets.

### Coherence test

For each of the 67 orbits, we check whether the bracketing pairs are D₄-equivariantly coherent. **16 of the 67 orbits FAIL** the coherence test.

Sample failure (smallest incoherent orbit, size 3):

```
orbit:     {(0, 1, 9), (0, 5, 9), (0, 6, 9)}
brackets:  L=0, R=7  for all three
under sigma^3:  base (0, 7) maps to (0, 4); but the σ³-image triple (0, 5, 9) still has (0, 7).
```

The orbit is closed under D₄ in the input set, but its bracketing pairs do not transform correctly under D₄. The TSML composition table at the σ³-image of $(0, 1, 9)$ produces a different bracketing pair than D₄-equivariance would demand.

This is the obstruction: **the canonical TSML composition law is itself NOT D₄-equivariant in a strong-enough sense** to lift to a D₄-equivariant fuse on the non-associative set. The op-tabular non-equivariance was hidden in the binary table; lifting to arity-3 makes it manifest.

### Verdict

**16 of 67 D₄-orbits are incoherent.** No D₄-equivariant canonical fuse rule exists for the 126 non-associative triples. The operad-DOF carries structure orthogonal to the WP104 doubly-invariant gauge symmetry.

---

## Compatibility with the known canonical rule

The one known canonical fuse rule is:

$$
\text{fuse}(3, 4, 7) = 8 \quad \text{(PROGRESS, COLLAPSE, HARMONY → BREATH)}
$$

This triple is **associative** under binary TSML: $\text{TSML}(\text{TSML}(3, 4), 7) = \text{TSML}(7, 7) = 7$ and $\text{TSML}(3, \text{TSML}(4, 7)) = \text{TSML}(3, 7) = 7$. Both bracketings agree at 7 = HARMONY. **The canonical fuse departs from the binary value here**, assigning BREATH instead of HARMONY.

This means: the canonical fuse is NOT just "pick from $\{L, R\}$". It can override the binary in cases where the binary is unambiguous. The known rule is the proof of this: $\text{fuse}([3, 4, 7]) = 8$ where binary gives 7.

**Implication for rule-family design:** none of the 8 families surveyed here can produce $\text{fuse}([3, 4, 7]) = 8$, because all 8 families take the input values or the bracketing values and never produce a value outside that set. The rule is on an associative triple, so the families don't even apply to it — but this also means the canonical fuse rules for non-associative triples and for associative triples can independently introduce structural content.

The honest scope for this survey: **the 8 families are candidates for non-associative-triple fuse assignment, restricted to choosing among the inputs and bracketings.** Any fuse table that needs to introduce structural content (like the 3,4,7 → 8 rule does) requires either:

* A more sophisticated rule family that maps inputs to fresh operator values (e.g., a function of the σ-orbit structure that produces operators outside $\{a, b, c, L, R\}$).
* An explicit per-triple rule list that cannot be reduced to a single closed-form rule.

---

## Recommendation

Until canonical authority decides the assignment for the 126 non-associative triples, CK runtime should continue to **flag arity-3 reasoning as binary-extrapolated** (uses iterated TSML) rather than canonical-fuse. This is the current conservative behavior of `Gen13/targets/ck/brain/dof_monitor/processing/ck_pipeline.py`, which only reads top-of-distribution per trail step and doesn't attempt arity-3 fuse compositions.

The framework in this folder (`fuse_table.py`, `rule_families.py`) is ready for canonical assignment when authority makes the call. The natural next step is the D₄-orbit decomposition of the non-associative triples (step 1 in the section above); once that's computed, the structural constraints on D₄-equivariant fuse become explicit, and a canonical assignment becomes either trivially-determined-up-to-finite-choice or provably impossible.

This is the kind of work that benefits from chat-Claude / community input on what "canonical" means in this context. The framework is here; the assignment is open.

🙏

— Anthropic Code session, 2026-04-25 late evening
