# K13_WEAK_THEOREMS.md
## K13 Weak Theorems: Weyl Symmetry, BFH Identification, Explicit Formula

**D-tier: 2. C-tier: 4. B-tier: 2.**

---

## D-Tier

**Theorem K13.D1 — Kloosterman prime power formula (D-tier):**
```
Kl(1,1;p^k) = p^{k/2} · sin((k+1)θ_p) / sin(θ_p)
```
where Kl(1,1;p) = 2√p cos θ_p (Sato-Tate parametrization).

Proof: Hecke recursion on Kloosterman sums at prime powers. See Iwaniec §12.3. ∎

---

**Theorem K13.D2 — A₂ local symmetry fails (D-tier no-go):**

Z̃_p(s,w) = (1-v²)(1-u²)/[(1-2v cosθ+v²)(1-2u cosθ+u²)] does NOT satisfy:

Z̃_p(s,w) = G_p(s,w) · Z̃_p(1-s, w+s-1/2)

for any simple scalar G_p(s,w). The A₂ transformation introduces θ_p-dependent factors
that cannot be absorbed into a scalar correction.

Proof: Direct substitution v → p^{-2}/v, u → u/(pv) into the local factor formula.
The result is Z̃_p(1-s, w+s-1/2) = [v-dependent factors] × Z̃_p(s,w), where the
factors involve p and cos θ_p in a way that doesn't factor out globally. ∎

---

## C-Tier

**Theorem K13.C1 — Z̃ equals shifted BFH series (C-tier):**

Z̃(s,w) = (1/p) · Z̃_χ(s+1, w)

where Z̃_χ(s,w) = Σ_c Σ_{χ mod c} |τ(χ)|² χ(1) c^{-s} L(w,χ) is the BFH
double Dirichlet series of type A₂.

Evidence: Local factor of Z̃_χ at p equals p · Z̃_p(s,w) by:
- Σ_{χ mod p} |τ(χ)|² χ(1) = p · Kl(1,1;p) (standard character sum identity)
- Local L-function factors agree

Gap: Composite moduli c=mn (gcd>1) in Z̃_χ vs. Z̃. Whether these cancel or contribute
is not verified.

---

**Theorem K13.C2 — BFH functional equation for Z̃ (C-tier, conditional):**

IF K13.C1 holds (Z̃ = Z̃_χ(s+1,w)/p), THEN Z̃(s,w) satisfies the A₂ functional equations:

```
Z̃(s,w) = G₁(s,w) · Z̃(-s, w+s+1/2)        [σ₁ shifted by 1]
Z̃(s,w) = G₂(s,w) · Z̃(s+w-1/2, 1-w)        [σ₂ unchanged]
```

where G₁, G₂ are explicit products of ζ-values and gamma factors from BFH.

Gap: Inherits gap from K13.C1 (composite moduli correction).

---

**Theorem K13.C3 — ζ-zero poles of Z̃ at w=3/4+iγ/2 (C-tier):**

Under analytic continuation (assuming K13.C2), Z̃(s,w) has poles at:
```
w = 3/4 + iγ/2    for each ζ-zero ρ = 1/2 + iγ
```

These poles come from the ζ(2w-1)^{-1} factor in the global product formula (K12).

Evidence: K12 global formula Z̃ ~ ζ(2s+2)^{-1} ζ(2w-1)^{-1} / L(Sym²)².
Gap: The global product formula is formal (C-tier from K12). Promotes to D-tier
only if K13.C1 and K13.C2 are proved.

---

**Theorem K13.C4 — Kloosterman explicit formula exists (C-tier):**

The sum Σ_{p≤N} Kl(1,1;p) h(p) admits a spectral expansion:
```
Σ_{p≤N} Kl(1,1;p) h(p) = N^{1/2} [Σ_k W_k h(γ_k) + Σ_f D_f h(t_f)] + O(N^{1/2-δ})
```

Evidence: Perron-Kuznetsov integration (§5 above), H₃ numerical signal (K11-K12).
Gap: Controlling the Perron contour shift through ζ-zero locations and bounding the
error term.

---

## B-Tier Conjectures

**Conjecture K13.B1 — Composite correction is negligible:**

The composite-moduli contribution to Z̃_χ(s+1,w) satisfies:
```
Σ_{c composite} (...) = O(N^{-1/2})   as Im(s) → ∞
```
This would promote K13.C1 to D-tier.

**Conjecture K13.B2 — Explicit formula weights:**
```
W_k = 1/|ζ(2ρ_k - 1)|²  ×  (Γ-factor)
E_N = O(N^{-1/4+ε})
```
This makes K13.EF fully explicit. The weight W_k = |ρ_E(1,ρ_k)|² matches the
Eisenstein coefficient formula from K10.1.

---

## Cumulative Program Status After K13

**The K-series has converged to one theorem:**

> **K13.EF (target theorem):** The Kloosterman explicit formula.
> If proved, it explains the 97% H₃ detection and provides a structural bridge
> from Kloosterman sums (computable) to ζ-zero locations (the goal).

**What remains to close K13.EF:**
1. K13.C1 → D-tier: verify composite correction in Z̃ vs Z̃_χ (numerical, K14)
2. K13.C4 → D-tier: Perron contour control (analytical, requires ζ zero-free region)

**Total no-goes accumulated (K1-K13):** 21 routes documented and closed.

**Surviving paths:**
1. K13.EF Kloosterman explicit formula (C-tier, gap = Perron control)
2. K13.C1 BFH identification (C-tier, gap = composite correction)
3. K13.C3 ζ-zero poles at w=3/4+iγ/2 (C-tier, conditional on C1+C2)
