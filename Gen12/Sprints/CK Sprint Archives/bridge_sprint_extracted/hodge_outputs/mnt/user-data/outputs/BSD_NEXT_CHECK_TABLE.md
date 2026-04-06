# BSD NEXT-CHECK TABLE
# 389a1 Board Snapshot

**© 2026 7Site LLC | Brayden Ross Sanders**

| BSD Layer | Current State | What Still Needs Verification |
|-----------|--------------|-------------------------------|
| **Regulator pilot** | det(H) ≈ 0.15246014 computed; ĥ(P₁), ĥ(P₂), ⟨P₁,P₂⟩ measured; Ω₁ = 2.49021256 exact; L''(E,1)/2 ≈ 0.37966 (BSD prediction) | Confirm L''(E,1)/2 from LMFDB as single database lookup; cross-check det(H) against MAGMA/Sage canonical heights |
| **χ_{77} channel** | ε(E⊗χ_{77}) = −1 confirmed; L'(E,χ_{77},1) = 0.0106998338 ± 3×10⁻¹⁴ (10-digit Mellin integral); first surviving analytic signal | No further computation needed; value is stable |
| **Normalization** | L'(E,χ_{77},1) = (Ω_E/(4√77))×det(H) fits to 1.1%; formula: $L' = \Omega_{E^{77}} \times \det(H) \times |\mathrm{Sha}|/\prod c_p$ | Compute Ω_{E^{77}} from ACTUAL minimal model of E^{77} (not just Ω_E/√77 approximation); determine if 1.1% gap is period error or Sha error |
| **Tamagawa/Sha bookkeeping** | c₇ = c₁₁ = 4 (Kodaira I₀*, QR discriminants confirmed); c₃₈₉ = 1; tama product = 16; |Sha| = 4 REQUIRED for 1.1% match | Compute |Sha(E^{77})| independently via 2-descent on E^{77}; verify |Sha| is a perfect square (Cassels-Tate) ≥ 4; alternative: check via mod-ℓ Selmer group |
| **Joint construction** | χ_{77}-isotypic component E(F)^{anti} identified (F = Q(√-7,√-11)); sign confirms surviving channel; anti-symmetric Galois representation carries Reg(E/Q) | Construct an explicit point in E(F)^{χ_{77}} — either via Darmon/Stark-Heegner approach for Q(√77) or via p-adic methods; this IS the missing joint object |
| **Rank-2 Gross–Zagier target** | L''(E,1)/2 = Ω_E × det(H) = 0.37966 as BSD prediction; analogy with rank-1 GZ suggests rank-2 formula should involve Reg(E/Q) through the χ_{77}-isotypic height | No formula yet; Gap 1 = proof that L''(E,1)/2 = C_E × Reg(E/Q) for an explicit constant C_E derivable from χ_{77} normalization data |

---

**Priority order:** Tamagawa/Sha verification → Period correction → Joint point construction → Rank-2 GZ target
