# Findings: markov_binary_cl.py run

**Date:** 2026-04-27
**Script:** `markov_binary_cl.py` (Sprint 15 — Blockers 1A + 1B)
**Status:** Ran clean, no exceptions. Output captured in `markov_binary_cl_output.txt`.

---

## Summary

Three substantive findings worth flagging:

1. **σ values claimed in WP101 / sigma_rate_theorem.tex are reproduced exactly.** σ(10) = 0.128, σ(30) = 0.058, σ(210) = 0.009. These anchor numbers hold up.

2. **The conjectured tight constant C = 2 is approached from below as N grows.** N·σ(N) values: 1.28, 1.73, 1.96 for N = 10, 30, 210. Trend is consistent with C = 2 in the limit. Not yet proved, but numerically supported.

3. **The binary CL construction does NOT reproduce TSML.** This is the most important finding to flag. The script's verification block attempts to show `binary_CL[Z/10Z] = TSML` and gets **17/100 matches**, with 83 mismatches. The binary construction picks element 9 as harmony (highest-curvature unit), while TSML uses element 7. These are different tables.

   The fact that they coincidentally have the same σ value at N=10 (both 0.128) is structural coincidence, not identity.

---

## Detailed findings

### Option A: Universal Markov properties (N=10)

| Table          | Gap   | DB  | sigma | H/Hmax  | Attractor | Frac |
|----------------|-------|-----|-------|---------|-----------|------|
| TSML           | 0.100 | 0   | 0.128 | -0.000  | 7         | 0.73 |
| BHML           | 0.659 | 70  | 0.498 | 0.836   | 7         | 0.28 |
| ADD (a+b)%10   | 1.000 | 0   | 0.000 | 1.000   | 1         | 0.10 |
| MUL (a*b)%10   | 0.200 | 0   | 0.000 | -0.000  | 0         | 0.27 |
| DIS \|add-mul\|| 0.500 | 20  | 0.300 | 0.386   | 1         | 0.33 |
| D2 (curvature) | 0.718 | 16  | 0.554 | 0.599   | 0         | 0.49 |

**Observations:**

- TSML σ = 0.128 matches the paper's reported value. Anchor confirmed.
- BHML σ = 0.498 is **substantially higher** than TSML's. BHML does not satisfy the σ-rate theorem in the same way — it's nearly 50% non-associative. This is consistent with BHML being a different kind of object than the binary CL family.
- ADD and MUL are exactly associative (σ = 0), as expected for (Z/10Z, +) and (Z/10Z, ·).
- The "H/Hmax = -0.000" entries are floating-point display of values very close to zero, occurring when the stationary distribution concentrates entirely on one state.

### Option B: Binary CL construction

**Z/10Z verification:** Binary CL with harmony = 9 (highest-curvature unit) matches TSML in only **17/100 entries**. The 83 mismatches arise from:

- **Harmony choice**: TSML uses element 7 as harmony; binary CL picks element 9. This causes most default-rule entries to differ (TSML returns 7, binary returns 9).
- **ECHO outputs**: TSML's ECHO rule fires at different (a,b) pairs than the binary construction's. For example, TSML[2,2] = 7 (default), but binary[2,2] = 4 (ECHO since DIS=0, returns (2+2)%10 = 4).
- **Boundary handling**: TSML[0,7] = 7 (because 7 is harmony), but binary[0,7] = 0 (VOID rule precedes harmony rule for harmony ≠ 9).

**Conclusion:** Binary CL ≠ TSML on Z/10Z. They are distinct tables in the same family.

### Convergence table

| N    | Harmony | σ(N)     | Gap     | Harmony frac | ECHO | DB violations |
|------|---------|----------|---------|--------------|------|---------------|
| 10   | 9       | 0.128    | 0.1000  | 0.800        | 3    | 0             |
| 30   | 29      | 0.0578   | 0.0333  | 0.929        | 7    | 0             |
| 210  | 209     | 0.009336 | 0.0048  | 0.9895       | 47   | 0             |

**Key observations:**

- **N · σ(N):** 1.28, 1.73, 1.96 — trending toward 2 from below.
- **ECHO post-priority count = φ(N) − 1:** The script reports 3, 7, 47 for N = 10, 30, 210. The paper's Lemma 4.1 gives φ(N) = 4, 8, 48 (pre-priority). The off-by-one is exactly the (0,0) pair being intercepted by VOID before ECHO fires. **This matches the paper's remark about pre-priority vs post-priority counts.**
- **Spectral gap ~ 1/N:** 0.1, 0.033, 0.0048 ≈ 1/10, 1/30, 1/210. The chain mixes more slowly as N grows because the harmony attractor dominates more strongly.
- **Detailed balance:** Holds (DB violations = 0) for all binary CL tables. This is a non-trivial property; not all absorbing chains satisfy it.

---

## Implications for the σ-rate paper (#08)

These findings reinforce three points from my earlier review:

**1. Issue 4 from the review (pre-priority vs post-priority φ(N) count) is real and shows up empirically.** The script's ECHO column gives post-priority counts (3, 7, 47), which differ from φ(N) (4, 8, 48). The paper uses the pre-priority count for its bound, which is correct but slightly loose. The remark in the paper acknowledges this implicitly; making it explicit (Issue 4 in the review) would help.

**2. Issue 1 from the review (proof gap) — the data is consistent with σ ≤ 2/N.** The N·σ(N) values approach 2 from below, never exceeding. The proved bound σ ≤ 3/N has substantial margin. The conjectured σ ≤ 2/N is supported numerically across the tested range. Whichever way the proof gets tightened (recovering 2/N rigorously or conceding 4/N), the data does not falsify the rate.

**3. New issue — TSML vs binary CL distinction.** The paper's framing ("the binary CL on Z/NZ") is consistent with reading the σ-rate theorem as a result about a *family* parameterized by (N, harmony choice). TSML is one member of this family at N=10 with a specific harmony choice (= 7). The script's "verification" block attempts to show binary CL with harmony = 9 reproduces TSML and fails (17/100). 

If the paper anywhere implies that TSML is *the* binary CL on Z/10Z (rather than *a* specific instance of the family), that should be tightened. The σ-rate theorem holds for the family; TSML's individual σ value happens to coincide with the harmony=9 binary CL's σ at N=10, but they are structurally distinct tables.

**Recommendation:** Add a sentence to §2 of the manuscript explicitly noting that the binary CL family is parameterized by harmony choice, and that TSML corresponds to one specific choice within this family.

---

## Files

```
/home/claude/markov_binary_cl.py             — script as provided
/home/claude/markov_binary_cl_output.txt     — full console output
/mnt/user-data/outputs/markov_binary_cl_findings.md  — this document
```

🙏

---

*Computational verification by chat-Claude (Anthropic conversational session, 2026-04-27).*
*Author retains all scientific judgments.*
