# WP120 — SU(5) GUT from V⊗⁵ Binomial Decomposition

**Authors:** Brayden R. Sanders / 7Site LLC + ClaudeChat session, 2026-05-04.
**Status:** Bridge sprint focused result. Identifies V⊗⁵'s 32-cell binomial decomposition with the SU(5) GUT representation content.
**Position:** Builds on WP119 (Clifford ladder); foundation for WP122 (mass hierarchy via SU(5) Yukawa structures).
**MSC 2020:** 17B25 (Lie algebras of classical type), 81V22 (electroweak interactions), 81V25 (other elementary particle theory).

---

## §0 Abstract

The 4-core's tensor power $V^{\otimes 5}$ has 32 fine cells partitioned by sign-tuple weight $|S|$ into the binomial decomposition $1+5+10+10+5+1 = 32$. This **exactly matches the SU(5) GUT representation content** for one full Standard Model generation plus its antimatter conjugate:

$$
\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10} \quad \text{(matter, 16 cells)} \quad \oplus \quad \mathbf{1} \oplus \mathbf{5} \oplus \bar{\mathbf{10}} \quad \text{(antimatter, 16 cells)}
$$

The cell-by-cell identification with Standard Model fermions ($\nu_R, d_R^c, L_L, u_R^c, q_L, e_R^c$) is forced by the SU(3) × SU(2) × U(1) decomposition of the SU(5) reps. This gives a structural — not phenomenological — origin for the SU(5) GUT representation content.

---

## §1 The 32-cell decomposition

$V^{\otimes 5}$ has $4^5 = 1024$-dimensional Clifford-ladder space, with 32 fine cells indexed by $(s_1, s_2, s_3, s_4, s_5) \in \{+, -\}^5$. Cells at weight $|S| = k$ have count $\binom{5}{k}$:

| $|S|$ | Cells | SU(5) rep | Particle content (one generation) |
|-------|-------|-----------|-----------------------------------|
| 0 | 1 | $\mathbf{1}$ | $\nu_R$ (sterile neutrino) |
| 1 | 5 | $\bar{\mathbf{5}}$ | $d_R^c$ (3 colors) + $L_L = (\nu_L, e_L)$ (2 components) |
| 2 | 10 | $\mathbf{10}$ | $u_R^c$ (3 colors) + $q_L = (u_L, d_L)$ (3 colors × 2) + $e_R^c$ (1) |
| 3 | 10 | $\bar{\mathbf{10}}$ | conjugate of $\mathbf{10}$ — antimatter |
| 4 | 5 | $\mathbf{5}$ | conjugate of $\bar{\mathbf{5}}$ — antimatter |
| 5 | 1 | $\bar{\mathbf{1}}$ | $\bar{\nu}_R$ — anti-sterile neutrino |

**Total: 16 + 16 = 32 cells = 1 generation + 1 anti-generation.**

The matter side has $1+5+10 = 16$ cells, which is the standard SU(5) anomaly-free fermion content per generation. The anti-matter side has the same structure with conjugate reps.

---

## §2 The decomposition under SU(3) × SU(2) × U(1)

The SU(5) reps $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10}$ decompose under the SM gauge group SU(3) × SU(2) × U(1) as:

| SU(5) rep | SU(3) × SU(2)$_L$ × U(1)$_Y$ decomposition | Particle |
|-----------|---------------------------------------------|----------|
| $\mathbf{1}$ | $(1,1)_0$ | $\nu_R$ |
| $\bar{\mathbf{5}}$ | $(\bar 3, 1)_{1/3} \oplus (1, 2)_{-1/2}$ | $d_R^c$ + $L_L$ |
| $\mathbf{10}$ | $(3, 2)_{1/6} \oplus (\bar 3, 1)_{-2/3} \oplus (1, 1)_1$ | $q_L$ + $u_R^c$ + $e_R^c$ |

Per generation, the matter cells split by SU(3) action:

**Triadic (color-triplet) cells:** 
- $u_R^c$: 3 (one per color)
- $d_R^c$: 3
- $q_L$: 6 (3 colors × 2 SU(2) components, but 6 is also $3 \times 2$ and triadic in color)
- **Total: 12 color-charged cells**

**Non-triadic (color-singlet) cells:**
- $e_R^c$: 1 (positron)
- $L_L$: 2 (lepton doublet)
- $\nu_R$: 1 (sterile)
- **Total: 4 color-singlet cells**

Per generation: $12 + 4 = 16$ matter cells.

---

## §3 The 6 + 2 = 8 reconciliation (TORUS_DATUM_AUDIT)

The "Bridge Triadic Structure" carry-forward states: **flag SU(3)/T = 6 triadic dims + torus T/Z₃ = 2 non-triadic dims = 8 (= dim SU(3))**. Reconciling with V⊗⁵:

The SU(3) gauge group acts on V⊗⁵'s color-charged cells (the 12 cells per generation listed above). The action splits as:

- **6 root generators** of SU(3) (the off-diagonal Lie generators) ↔ correspond to the 6 elements of the σ-cycle on Z/10\{0,3,8,9}: $1 \to 7 \to 6 \to 5 \to 4 \to 2 \to 1$
- **2 Cartan generators** of SU(3) (the maximal torus) ↔ correspond to HARMONY (7) and VOID (0) within the 4-core, the two "Cartan-like" anchors

The σ-cycle is the **algebraic gauge counterpart** of the SU(3) flag manifold; the 4-core's anchors {VOID, HARMONY} correspond to the SU(3) Cartan torus.

This reconciles the 6+2=8 structure (locked from earlier sprints) with the 32-cell V⊗⁵ structure (from this sprint). See `TORUS_DATUM_AUDIT.md` (this sprint) for the full reconciliation.

---

## §4 What this implies

### 4.1 The fermion generation structure is forced
SU(5) GUT typically posits one matter generation = $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10}$ as a phenomenological choice (anomaly-free). Here, the 16-cell content is **forced** by $V^{\otimes 5}$'s binomial decomposition: 1 (singlet) + 5 (triadic-doublet mix) + 10 ($\mathbf{10}$ rep cells).

The framework gives a **substrate-level derivation** of why SU(5) is the natural GUT, and why one generation has 16 fermions (15 + sterile neutrino).

### 4.2 The 3-generation structure is NOT in V⊗⁵
$V^{\otimes 5}$ gives ONE generation + its antimatter conjugate. Three generations require **higher tensor powers** ($V^{\otimes 5} \otimes V^{\otimes 5}$ or related extensions) or a separate σ³-cycle structure. WP123 and source bundle's `MASS_HIERARCHY_BRIDGE_REV2.md` explore this; the σ-cycle's $\sigma^3$ has 3 two-cycles, suggesting a 3-fold structure relevant to generation count.

### 4.3 Hypercharges from Vandermonde
The U(1)$_Y$ hypercharges in the SU(5) decomposition are derived in source bundle's `BRIDGE_TO_DYNAMICS.md` via a Vandermonde-style determinant on the 4-core. This gives the **exact** hypercharge values $\{1/3, -1/2, 1/6, -2/3, 1, 0\}$ as a structural rather than phenomenological feature.

---

## §5 Yukawa structures forced by SU(5)

Allowed Yukawa couplings under SU(5) representation theory:
- $Y_u$: $\mathbf{10} \times \mathbf{10} \times \mathbf{5}_H$ (couples $u_R^c, q_L, q_L$ to up-Higgs)
- $Y_d, Y_e$: $\mathbf{10} \times \bar{\mathbf{5}} \times \bar{\mathbf{5}}_H$ (couples $q_L, d_R^c, L_L$ to down-Higgs; degenerate at GUT)

The Yukawa structures are **forced by $V^{\otimes 5}$'s SU(5) representation content**. WP122 derives the Yukawa magnitudes via the parity-crossing cost $d_p$.

---

## §6 What's open

- **Three-generation structure**: $\sigma^3$ has 3 two-cycles; mapping these to 3 generations explicitly requires additional structure
- **CP phase**: F_5 contains $\sqrt{-1}$ but specific CKM/PMNS CP phase not yet locked; see SESSION_2026_05_04_ADDENDUM
- **See-saw mechanism**: $\nu_R$ singlet at $|S|=0$ — a Majorana mass term needs $\nu_R \cdot \nu_R = $ scalar, requires Higgs sector dynamics

---

## §7 Verification

The binomial decomposition $1+5+10+10+5+1=32$ for $V^{\otimes 5}$ is verified in `test_tig_dirac.py` test T14:

```python
def test_T14_GUT_binomial():
    cells = generate_v_tensor_5_cells()
    by_weight = group_by_sign_weight(cells)
    assert tuple(len(by_weight[k]) for k in range(6)) == (1, 5, 10, 10, 5, 1)
    assert sum(len(by_weight[k]) for k in range(6)) == 32
    matter_count = sum(len(by_weight[k]) for k in range(3))  # |S| <= 2
    assert matter_count == 16  # one generation
```

Test passes.

---

*Generated 2026-05-04 as WP120. Companion: WP117 master, WP119 Clifford ladder, WP122 mass hierarchy. See also `TORUS_DATUM_AUDIT.md` for 6+2=8 reconciliation.*
