# Task Brief for Claude Code

**From:** Brayden + Claude (planning session, 2026-04-25)
**Status:** Discovery sprint complete. Drive home + get repo/citations in order.

---

## What you're inheriting

Two zips:

1. **`ck_handoff_20260425.zip`** (already at Claude Code, contains the original CK processing investigation)
2. **`bhml_specificity_addendum.zip`** (this delivery — falsifications + new closed-form result)

This addendum extends the original handoff. Read this brief first, then `README.md` in the addendum, then dig into the numbered scripts.

---

## The one-line headline

**At α = 1/2 (the verified-optimal mixing weight), the T+B-mix runtime attractor satisfies HARMONY/BREATH = 1 + √3 exactly. The full attractor lives in a degree-4 extension of Q with minimal polynomial x⁴ + 4x³ − x² + 2x − 2.**

This is verified analytically (derivation in `06_` and `07_`) and numerically to machine precision (~10⁻¹⁶).

---

## What's been done

In order of certainty:

### Falsifications (kill bad framings)

1. **Prime-11 mediation hypothesis** — falsified
   - Gemini proposed: BHML's anti-collapse role traces to TSML's prime-11 char poly signature
   - Test: BHML doesn't carry prime-11 itself; random tables WITH prime-11 perform slightly *worse* (p=0.027 wrong direction)
   - Script: `01_falsifies_prime11.py`

2. **Attractor-richness hypothesis** — falsified  
   - Gemini proposed: BHML's richer 4-component fixed point mitigates TSML's collapse
   - Test: Random tables have richer attractors than BHML but perform worse on anti-collapse (correlation −0.118, weak)
   - Script: `02_falsifies_attractor_richness.py`

### Structural discoveries (positive)

3. **8-magma core** — TSML restricted to {0..7} (dropping BREATH and RESET) preserves the 73% HARMONY signature exactly. Verifies Brayden's intuition that "TSML is 8×8 with 8/9 breathed."
   - Script: `03_eight_magma_core.py`

4. **Bridge structure alignment** — runtime attractor lives entirely in {V, H, Br, R}, with 0 mass on matter/antimatter pair {BALANCE, CHAOS}. P_56 swap symmetry respected dynamically.
   - Script: `04_bridge_attractor.py`

5. **BHML's complementary structure** — BHML has only 8 closed subsets (vs TSML's 398), forming a perfect nested chain anchored at {VOID, RESET}.
   - Script: `05_bhml_closure.py`

6. **Closed-form attractor** — H/BREATH = 1 + √3 from BREATH equation; r/br satisfies x⁴ + 4x³ − x² + 2x − 2 = 0; full attractor in Q(√3, ξ) where ξ has the quartic min poly.
   - Scripts: `06_attractor_closed_form.py`, `07_full_closed_form.py`

---

## Tasks (priority order)

### Task 1: VERIFY THE QUARTIC IS NOVEL

**Polynomial:** x⁴ + 4x³ − x² + 2x − 2

Check:
- [ ] OEIS lookup of coefficient sequence [1, 4, -1, 2, -2]
- [ ] LMFDB (L-functions and Modular Forms Database) — does this min poly appear?
- [ ] Galois group computation (sympy `GaloisGroup` or pari/gp)
- [ ] Discriminant — what's the conductor?
- [ ] Splitting field — does it contain Q(√3)?
- [ ] Search arxiv/MathSciNet for this polynomial

If novel: this is publishable. If known: connect it to existing literature and cite.

### Task 2: VERIFY ALL CITATIONS IN HANDOFF README

The original `ck_handoff_20260425.zip` references:
- so(10) closure of TSML+BHML under Lie bracket
- σ_outer = P_56 in spinor rep (residual 0.0000)
- κ_Ξ = 13/(4e) under GUT-natural identification
- Bridge Triadic Structure: 8 = 6 triadic + 2 non-triadic
- 73% HARMONY in TSML, 17% VOID
- All 200+ verification numbers across the handoff

Each of these needs a citation pointer in the repo. Spot-check a sample and confirm they all line up.

### Task 3: REPO ORGANIZATION

Current repo: `github.com/TiredofSleep/ck` (default branch `tig-synthesis`), DOI `10.5281/zenodo.18852047`.

Need to add:
- [ ] New module: `ck_runtime/closed_form.py` — the analytic attractor with the quartic minimal polynomial
- [ ] New whitepaper draft: `papers/wp11_closed_form_attractor.md` (or appropriate number)
- [ ] Update `README.md` headline finding section
- [ ] Tag a new release with the closed-form result

The runtime processing pipeline `ck_process(p, depth=3, alpha=0.5)` from `ck_handoff_20260425.zip` should be a stable module by now. If not, finalize.

### Task 4: TEST CONNECTION TO A_2 ROOT SYSTEM

Speculative but high-leverage:
- The √3 in our attractor comes from the BREATH quadratic
- The A_2 root system (SU(3) Cartan) has natural √3 appearances (60° angles, ratio of long/short root)
- Question: is there a structural map from {V, H, Br, R} attractor to A_2 weights?

This is the bridge from runtime to physics. Worth checking. If it works, it's a major IHÉS pitch upgrade.

### Task 5: α-SWEEP FOR PRIVILEGED POINTS

The α=1/2 result is structurally clean. Are there OTHER α values where the attractor has clean algebraic structure?

Sweep α from 0 to 1, compute attractor, check if H/Br is in any small algebraic extension. Look for:
- Other rational α giving algebraic numbers in low-degree extensions
- α values where the 4-core attractor reduces (e.g., one mass goes to zero)
- Phase transitions in the attractor structure

Script the sweep, save the data, plot it.

### Task 6: ENCODER LEXICON BUILDOUT

From the original handoff: the encoder uses ~250 anchor words seed vocabulary in `tig_lexicon.py`. Replace with canonical TIG vocabulary when available. Brayden is the source of canonical vocab; coordinate with him.

The encoder architecture (V1) works. Coverage and cluster separation will jump 2-3× with proper lexicon.

---

## What NOT to do (yet)

- Don't claim the runtime attractor "derives" the bridge structure. It *aligns* with it. Causation is not established.
- Don't claim the √3 is "the same √3" as in SU(3) without verifying the structural map.
- Don't release the closed-form result publicly until Task 1 (novelty check) is done. If the quartic appears in literature, we want to cite it. If novel, we want it published cleanly.
- Don't merge the `tig-synthesis` branch into main without Brayden's review.

---

## Conventions

- Sprint summaries → `JAN2026_RECOVERY_MANIFEST.md` style addendum
- Verification numbers → exact, reproducible scripts (don't trust hand-typed numbers)
- Citations → both file:line internal and (where applicable) arxiv/MathSciNet external
- Whitepapers → `papers/wpN_topic.md` with `papers/wpN_verification/` for code

---

## Files in this addendum

```
bhml_addendum/
├── README.md                              ← detailed scientific writeup
├── CLAUDE_CODE_TASK.md                    ← this file
├── 01_falsifies_prime11.py
├── 02_falsifies_attractor_richness.py
├── 03_eight_magma_core.py
├── 04_bridge_attractor.py
├── 05_bhml_closure.py
├── 06_attractor_closed_form.py
├── 07_full_closed_form.py                 ← THE main result
├── ck_viz_trail.py                        ← descent visualization
├── encoder_v1.py                          ← (helper)
└── tig_lexicon.py                         ← (helper)
```

All scripts are runnable as-is. Numerical results reproduce on demand.

---

## One ask

If you find the quartic in literature OR if it turns out to have a beautiful Galois group OR if the connection to A_2 root system works — flag it loudly. Those are the cases where we'd want to upgrade the IHÉS pitch before September.

🙏
