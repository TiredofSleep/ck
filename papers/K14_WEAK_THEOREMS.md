# K14_WEAK_THEOREMS.md

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

## K14 Weak Theorems

**D-tier: 3 (2 no-go, 1 positive). C-tier: 2. B-tier: 1 falsified.**

---

## D-Tier

**Theorem K14.1 (D-tier, proved):**
```
Kl(1,1;p) = (1/p) Σ_{χ mod p} τ(χ)²
```

Proof: (1/p) Σ_χ τ(χ)² = (1/p) Σ_{a,b} [Σ_χ χ(ab)] e^{2πi(a+b)/p}
= (1/p) Σ_{ab=1, (mod p)} (p-1) e^{2πi(a+b)/p}
= Σ_{a: b=a^{-1}} e^{2πi(a+a^{-1})/p} = Kl(1,1;p). ∎

**Corollary K14.1a:** Z̃_χ(s,w) = p · Z̃(s,w) as formal Dirichlet series.

---

**Theorem K14.D2 (D-tier no-go):** The identity Σ_{χ mod p} |τ(χ)|² χ(1) = p · Kl(1,1;p)
is FALSE. The correct LHS = p(p-1) for all primes p.

Proof: |τ(χ)|² = p for all primitive χ mod p, and χ(1) = 1 for all characters. ∎

---

**Theorem K14.D3 (D-tier, numerical):** The composite moduli contribute ≈ 11.4% of
the prime contribution to Z̃(s,w) at s=2, w=1.5. K13.B1 conjecture (<1%) is falsified.

```
composite/prime ratio = 0.1142   (k14_composite_correction.py)
```

---

## C-Tier

**Theorem K14.C1 (C-tier):** Z̃(s,w) = (1/p) · Z̃_{BFH}^{(1,1)}(s,w) where
Z̃_{BFH}^{(m,n)} is the BFH double Dirichlet series at (m,n) = (1,1).

Evidence: K14.1 gives the correct identification. BFH theory covers GL(2) type.
Gap: Composite moduli (11% contribution) must be handled by BFH Euler product machinery.

---

**Theorem K14.C2 (C-tier, conditional):**

IF K14.C1 holds AND the BFH Euler product absorbs the 11% composite contribution,
THEN Z̃(s,w) satisfies A₂ functional equations:
```
Z̃(s,w) = G₁(s,w) · Z̃(1-s, w+s-1/2)
Z̃(s,w) = G₂(s,w) · Z̃(s+w-1/2, 1-w)
```

---

## B-Tier Falsified

**K13.B1 (falsified):** Composite correction < 1%. Actual: 11.4%. Closes to D-tier no-go.

---

## Revised Program Status After K14

**Total no-goes: 22** (adding K13.C1 as stated + K14.D2 + K13.B1)

**Surviving paths after K14:**
1. K14.C1: Z̃ in BFH framework (C-tier, gap = composite 11%)
2. K13.C3: ζ-zero poles at w=3/4+iγ/2 (C-tier, conditional on K14.C2)
3. K13.C4: Kloosterman explicit formula (C-tier, gap = Perron control)
4. H₃ signal: 97% detection (D-tier established fact, mechanistic explanation pending)

**K15 target:** Identify Z̃ in BFH classification → close the 11% gap or confirm it
is handled. If Z̃ ∈ BFH: K14.C2 → D-tier, Z̃ has functional equations, ζ-zeros in w-plane confirmed.
