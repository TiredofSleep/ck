# Corridor Separation Lemma (Negative Form)
## W_BHML and Corridor Compression Are Formally Disconnected

*Brayden Ross Sanders / 7Site LLC & C. A. Luther*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*
*Status: CLOSED NEGATIVE RESULT. Do not relitigate.*

---

## Statement

**Corridor Separation Lemma.**
Let b = p×q be a semiprime, p < q prime. The corridor compression law — the
decay of R(k, p) from k=1 to k=p — is governed entirely by the sinc² field:

    R(k, p) = sin²(πk/p) / (k² sin²(π/p)) → sinc²(k/p)   as p → ∞.

The wobble constant W_BHML = 3/50 (proved Tier C, Z/10Z ring arithmetic) plays
**no role** in the corridor, either as:

1. A modulation factor inside the corridor (k ≤ p), or
2. A sidelobe frequency prediction past the gate (k > p).

These two claims were tested and falsified by direct computation.

---

## Evidence

### Claim 1 Falsified — Candidate formula R×sin²(πW·k/p)

The candidate Corridor(b,k) = R(m,b,k) × sin²(π × W_BHML × k/p):

| Test | Result |
|------|--------|
| Shape within corridor | sin²(πW·k/p) is **monotone** in [0,p]; maximum value 0.0351; no oscillation |
| Continuum limit | Corridor(t) → (3/50)² × sin²(πt) — a bell shape peaking at t=0.5, opposite to sinc² decay from t=0 |
| RMSE vs empirical | sinc²(k/p) outperforms by 0.482 RMSE across 16 worlds (0.077 vs 0.559) |
| Global test | sinc² wins 16/16 worlds |

**Kill condition met.** The candidate does not reproduce the sinc² envelope.

### Claim 2 Falsified — W_BHML sidelobe prediction

The prediction: first post-gate sidelobe of R(k,p) occurs at k ≈ p × 1/(2W_BHML) = p × 50/6 ≈ 8.33p.

| Test | sinc² prediction (t≈1.43) | W_BHML prediction (t≈8.33) | Winner |
|------|--------------------------|---------------------------|--------|
| p=3  | 1.43 (error 0.93)        | 8.33 (error 5.93)         | sinc² |
| p=5  | 1.43 (error 0.03)        | 8.33 (error 6.89)         | sinc² |
| p=7  | 1.43 (error 0.00)        | 8.33 (error 6.90)         | sinc² |
| p=11 | 1.43 (error 0.02)        | 8.33 (error 6.88)         | sinc² |
| p=13 | 1.43 (error 0.03)        | 8.33 (error 6.87)         | sinc² |
| All 14 primes tested | | | **sinc² wins 14/14** |

Mean first post-gate sidelobe: t ≈ 1.494. W_BHML prediction error: 6.84 corridor widths.

**Kill condition met.** W_BHML does not set the post-gate sidelobe frequency.

### Claim 3 Tested — W_BHML^n echo attenuation

Prediction: R(p+n, p) ≈ W_BHML^n × R(1, p). If W_BHML = 3/50 is the per-gate attenuation:

| p=5, n | R(p+n,p) | W^n × R(1) | Ratio |
|--------|----------|------------|-------|
| 1 | 0.0278 | 0.0600 | 0.46 |
| 2 | 0.0534 | 0.0036 | 14.8 |
| 3 | 0.0409 | 0.0002 | 189 |
| 4 | 0.0123 | 0.00001 | 953 |

Ratios diverge by orders of magnitude at each step. **W_BHML^n is not the echo attenuation law.**

---

## What Survives

The three-object separation is **intact**:

| Object | Formula | Status |
|--------|---------|--------|
| W_BHML | 3/50 — per-step C×D asymmetry in Z/10Z ring | **Tier C** — proved for Z/10Z |
| Wob(b,k) | 8/9 at k=9 — alphabet saturation | **Measured**, k-dependent |
| Corridor compression | sinc²(k/p) = R(k,p) | **Tier D** — D2 proved |

These three objects exist and are distinct. What does **not** exist is a formula pairing W_BHML with corridor compression. They are structurally separate.

---

## Why This Is Useful

This negative result does three things:

1. **Prevents re-litigation.** The corridor formula question is settled. Any future formula
   proposal must account for why the candidate failed both the shape test and the sidelobe
   test before claiming a corridor role for W_BHML.

2. **Clarifies the atlas.** The corridor compression is already Tier D (proved). No new
   algebraic form is needed to describe it. The corridor IS the sinc² field.

3. **Directs future work.** If W_BHML appears in a post-gate structure, the mechanism is
   not sidelobe frequency but something else entirely — perhaps the Montgomery dual
   R₂(t) = 1 − sinc²(t), where W_BHML might appear at R₂(3/50) = 1 − sinc²(3/50) ≈ 0.965.
   This is a Tier A structural analogy, not a tested claim.

---

## Formal Status

**A13 (Corridor Compression Model) — KILLED.**
*Date of death: March 31, 2026.*
*Kill conditions met: shape test failure across 16 worlds; sidelobe prediction fails 14/14 primes.*
*Three-object separation survives. Corridor compression belongs to Tier D (D2). W_BHML belongs to Tier C (C8). No formula connects them.*

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
