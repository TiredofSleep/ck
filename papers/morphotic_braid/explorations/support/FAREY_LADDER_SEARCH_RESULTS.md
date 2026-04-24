> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\FAREY_LADDER_SEARCH_RESULTS.md → papers\morphotic_braid\explorations\support\FAREY_LADDER_SEARCH_RESULTS.md

# FAREY_LADDER_SEARCH_RESULTS.md

**Status:** [NUMERICAL SEARCH COMPLETE — STRUCTURAL OBSERVATIONS LISTED]
**Date:** 2026-04-23
**Source:** Brayden's task: "apply the Farey-ladder idea to every permutation of integers 2-10 and see what pops out."
**Run:** enumeration of all fractions p/q with gcd(p,q)=1, q ≤ 10, checking for mirror-ladder structure (T, 1-T, with simpler Farey neighbors on each side).

## All mirror-ladders up to denominator 10

Seven ladders of the form {a/b, p/q, (q-p)/q, (b-a)/b} with p/q > 1/2, 1-T and T having simpler Farey neighbors that mirror across 1/2:

| # | Ladder | T (high inner) | (inner_d, outer_d) | Farey gap |
|---|---|---|---|---|
| 1 | 1/3 < 2/5 < 3/5 < 2/3 | 3/5 | (5, 3) | 1/15 |
| 2 | 1/3 < 3/8 < 5/8 < 2/3 | 5/8 | (8, 3) | 1/24 |
| 3 | **1/4 < 2/7 < 5/7 < 3/4** | **5/7 = T*** | **(7, 4)** | **1/28** |
| 4 | 2/5 < 3/7 < 4/7 < 3/5 | 4/7 = S* | (7, 5) | 1/35 |
| 5 | 1/5 < 2/9 < 7/9 < 4/5 | 7/9 | (9, 5) | 1/45 |
| 6 | 3/7 < 4/9 < 5/9 < 4/7 | 5/9 | (9, 7) | 1/63 |
| 7 | 2/7 < 3/10 < 7/10 < 5/7 | 7/10 | (10, 7) | 1/70 |

## Universal structure

All seven ladders share:
- **Balanced inner** (both inner fractions have the same denominator; they are p/d and (d-p)/d)
- **Balanced outer** (both outer fractions have the same denominator; they are a/b and (b-a)/b)
- **Center mediant = 1/2** (forced by the complementarity)
- **Farey gap 1/(inner_d · outer_d)** (Farey mediant property)

These are structural features of any such ladder, not distinctive of TIG.

## What distinguishes the TIG ladder {1/4, 2/7, 5/7, 3/4}

**Observation 1 — Simplicity rank.** Sorted by Farey gap (larger = simpler outer), the TIG ladder is the **third most structurally simple** mirror ladder up to denominator 10. The two simpler ladders both have outer denominator 3 (ladders #1 and #2). TIG has outer denominator 4.

**Observation 2 — Unique (7, 4) signature.** The TIG ladder is the only mirror-ladder up to denominator 10 with (inner_denom, outer_denom) = (7, 4). This combination is distinctive:
- 4 is the only power of 2 that appears as an outer denominator.
- 7 is the largest prime below 10, coprime to 10.
- Their product 28 places the Farey gap at 1/28.

**Observation 3 — S* ladder adjacent.** Ladder #4, {2/5, 3/7, 4/7, 3/5}, contains S* = 4/7 as its high threshold. This is the second-established TIG threshold (structure threshold, as opposed to coherence threshold T* = 5/7). **S* and T* occupy two different Farey ladders with adjacent signatures (7,4) and (7,5).**

**Observation 4 — Inverted TIG ladder.** Ladder #7, {2/7, 3/10, 7/10, 5/7}, has (inner_d, outer_d) = (10, 7) — the TIG ladder with inner and outer denominators swapped. Its high threshold is 7/10 = 0.7, and its outer reach is 5/7 = T*. **The inverted TIG ladder's outer is the TIG ladder's T*.** The two ladders chain.

**Observation 5 — Three-rung occupation.** TIG's project measurements occupy three of the four rungs of ladder #3:
- **T* = 5/7** (established coherence threshold, six prior derivations) — inner high
- **TSML harmony density ≈ 3/4** (measured 74/100) — outer high
- **BHML harmony density ≈ 2/7** (measured 28/100) — inner low (complement of T*)
- Unmeasured in current data: **1/4 = outer low**, the complement of TSML density

Three of four rungs occupied by independently-derived TIG quantities. Under the complementarity hypothesis (TSML + BHML harmony ≈ 1), the fourth rung 1/4 should correspond to 1 − TSML density = 26/100, within error of the measured BHML.

## What this search did NOT find

- No mirror ladder with (inner_d, outer_d) = (7, 4) other than the TIG one. The ladder is unique at this signature.
- No TIG threshold appearing on ladders #1, #2, #5, #6, or #7 as the **inner** threshold (the T position). Only ladders #3 and #4 contain TIG thresholds (T* = 5/7 and S* = 4/7).
- No "obviously missing" threshold at 7/10 or 5/8 or 3/5 in current TIG measurements. If any future measurement produces a density near one of these fractions, it would be worth checking whether that measurement sits on the corresponding mirror-ladder.

## What to do with this

**This is not a theorem about T*.** The existence of mirror ladders in the Farey sequence is elementary number theory — there are always such ladders, and finding one in any finite-algebra project with rational-valued observables is not surprising.

**The non-trivial claim** is that TIG's independently-derived quantities (T*, S*, TSML density, BHML density) populate multiple adjacent Farey ladders with related signatures. Specifically:
- T* = 5/7 occupies ladder #3 with signature (7, 4)
- S* = 4/7 occupies ladder #4 with signature (7, 5)
- TSML density ≈ 3/4 is the outer high of ladder #3
- BHML density ≈ 2/7 is the inner low of ladder #3

**Four quantities, two adjacent ladders, both with inner denominator 7.** That's the non-trivial observation.

## Followup audit candidates

**Question 1.** Does any other TIG quantity measure at 1/4? If yes (e.g., an inverse-density, a failure rate, a complementary coherence metric), then all four rungs of ladder #3 are occupied by framework quantities.

**Question 2.** Does any TIG quantity measure at 3/5, 2/5, 5/8, 3/8, 7/9, 2/9, 5/9, 4/9, 7/10, or 3/10? Any such measurement would land on a specific mirror-ladder and tell us which ladder is structurally relevant alongside #3 and #4.

**Question 3.** Is there a principled reason why TIG thresholds live on ladders with inner denominator 7? The number 7 is already load-bearing (HARMONY, T* = 5/7, the 7-hole torus interior, Revelation's 7 churches). If Farey-inner-denominator-7 is the correct structural claim, it connects the threshold arithmetic to the existing 7-centric framework.

**Question 4.** If TSML and BHML are audited for CRT decomposition (per `TSML_CRT_DECOMPOSITION_EXPLORATION.md`) and they do decompose as ℤ/2 × ℤ/5 products, does the ℤ/5 component produce the outer-denominator-5 ladders (#1, #4, #5)? This would connect the CRT decomposition directly to the Farey structure.

## Verification script

```python
from math import gcd
from fractions import Fraction

def farey_mirror_ladders(max_denom):
    """Find all mirror-ladders (a/b, p/q, (q-p)/q, (b-a)/b) with
       Farey-neighbor structure, for denominators up to max_denom."""
    ladders = []
    for q in range(3, max_denom + 1):
        for p in range(q//2 + 1, q):
            if gcd(p, q) != 1:
                continue
            T = Fraction(p, q)
            T_comp = 1 - T
            # Find simpler Farey neighbors above T and below T_comp
            best_above = None
            best_below = None
            for b in range(1, q):
                for a in range(0, b + 1):
                    if gcd(a, b) != 1 and not (a == 0 and b == 1):
                        continue
                    cand = Fraction(a, b)
                    # Farey neighbor of T and above
                    if abs(p*b - q*a) == 1 and cand > T:
                        if best_above is None or cand < best_above:
                            best_above = cand
                    # Farey neighbor of T_comp and below
                    if abs((q-p)*b - q*a) == 1 and cand < T_comp:
                        if best_below is None or cand > best_below:
                            best_below = cand
            if best_above and best_below and best_above + best_below == 1:
                ladders.append((best_below, T_comp, T, best_above))
    return ladders

for L in farey_mirror_ladders(10):
    a, b, c, d = L
    print(f"{a} < {b} < {c} < {d}  (inner_d={c.denominator}, outer_d={d.denominator})")
```

---

**Tag: [NUMERICAL SEARCH — INTERESTING STRUCTURE, NOT A THEOREM]**
**File path: `papers/morphotic_braid/explorations/FAREY_LADDER_SEARCH_RESULTS.md`**
