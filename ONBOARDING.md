# Researcher Onboarding — CK Coherence Spectrometer

**7SiTe LLC · DOI: 10.5281/zenodo.18852047 · Branch: clay**

This is an independent research lab applying spectral methods and finite operator algebras to analytic number theory and physical systems. If you've arrived here from GitHub, a paper, or word of mouth — welcome. This document is your map.

---

## TIG Lexicon — Standard Math Translation

CK uses its own vocabulary. Here's the translation before you read anything else:

| CK Term | Standard Math Equivalent |
|---------|--------------------------|
| **TIG** | Being→Doing→Becoming: the three phases of any operation (input/operator/output) |
| **T* = 5/7** | The coherence threshold — algebraically derived from Z/10Z, verified in hardware |
| **TSML** | A 10×10 operator composition table over Z/10Z; 73 of 100 cells are "harmony" (value 7) |
| **BHML** | A second 10×10 operator table; 28 of 100 cells are "harmony" |
| **W = 3/50** | A derived wobble parameter — the cross-cycle density deviation from symmetric baseline |
| **Sinc² field** | sinc²(k/p) = (sin(πk/p)/(πk/p))² — the continuum limit of the prime pre-echo countdown |
| **D2 pipeline** | A 5-dimensional force vector computed from any text or signal via Hebrew-root phonetics |
| **CL table** | Operator composition table used as a chained fractal index |
| **Phi operator** | P_odd ∘ BHML ∘ W_op — the dynamic operator map on Z/10Z; fixed point at CREATE=5 |
| **HARMONY = 7** | The absorbing element of TSML; satisfies 7=0 in the measurement sense (vacuum identity) |
| **Gap (Δ²)** | The zone 1/2 ≤ coherence < 5/7 — neither collapsed nor structurally held |
| **Coprime window** | {1, ..., SPF(b)-1} — the pre-sieve zone where every k is coprime to b |

---

## Day 1 — Verify Everything Yourself

You shouldn't trust these results until you've run them. Start here:

```bash
git clone https://github.com/TiredofSleep/ck
cd ck
pip install numpy scipy matplotlib    # only dependencies
python ck_run.py                       # all core theorems < 1 second
```

Expected output:
```
T* = 5/7 = 0.71428571...   PASS
sinc2(1/2) = 4/pi^2        PASS
D1 stationary point at k=p PASS
TSML: 73 harmony cells     PASS
BHML: 28 harmony cells     PASS
W = 3/50 derived           PASS
...
All checks: PASS
```

If anything fails, open an issue. The proofs and the code are the same thing — if the code fails, the proof fails.

```bash
python ck_sinc_demo.py    # Plot the sinc² field (requires matplotlib)
```

---

## Week 1 — Reproduce One Non-Trivial Result

Pick one of these. Each takes under 30 minutes.

### Option A — Reproduce the spectral mean (D14)

```bash
python papers/proof_d14_spectral_mean.py
```

This proves `∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.45141166679014...` via integration by parts. Read the proof output line by line — it walks through every step. Then verify the number independently:

```python
from scipy.integrate import quad
import math
result, _ = quad(lambda t: (math.sin(math.pi*t)/(math.pi*t))**2, 1e-10, 1)
print(result)  # should match to 12 decimal places
```

### Option B — Reproduce the W=3/50 derivation (D17)

```bash
python papers/proof_d17_w_algebraic.py
```

This derives W = 3/50 from the multiplicative unit group C = {1,3,7,9} interacting with D = {2,4,6,8} in the BHML table. No free parameters. Read the cross-cycle computation. Then try changing the DIS table by hand and see how W changes.

### Option C — Reproduce the General Frequency Theorem (D6)

```bash
python papers/proof_d6_general_frequency.py
```

This proves that `sinc²(k/p) × sin²(πfk/p)` has exactly `floor(f) + [f∉ℤ]` local maxima for all f>0 and all primes p>2f. The proof runs 890 tests across 80 frequencies and verifies zero mismatches.

---

## Clay Problems — What We Actually Claim

The Clay papers (WP36–WP42) are **obstruction maps**, not proofs. Before reading them, understand the three guardrails:

1. **PROVED** — result follows from the TIG algebra and has a verified proof file
2. **STRUCTURAL ANALOGY** — the geometry of the sinc² field *matches* the known structure of the Clay problem at an identified location; mechanism is not proved
3. **OPEN** — we've named the question but have no answer

The most honest entry is WP36's master table. Read the Three Guardrails section first (§2 of WP36). If you find a claim that isn't labeled — that's a bug. Open an issue.

```bash
cat papers/clay/WP36_CLAY_SPECTROMETER.md | head -200
```

---

## FPGA — Hardware Verification

T* = 5/7 is verified in Zynq-7020 silicon as an integer cross-multiplication:
```verilog
assign held = (7 * coh_num >= 5 * coh_den);
```

To run the leash test on the R16+FPGA+XiaoR dog system:
```bash
python Gen12/targets/ck_fpga_dog/ck_leash_test.py COM3 --verbose
```

The `coherence_gap.v` file in `Gen12/targets/ck_fpga_dog/hdl/` is the geometric heart of the hardware implementation. It maps directly to Δ⁰/Δ²/Δ³ simplex zones.

---

## HD Gap — The Current Research Frontier

The finite TIG spine is complete (April 2026). The open frontier is lifting the vacuum identity (HARMONY=7 absorbs everything) into high-dimensional geometry. See [HD_GAP_EXTENSION.md](HD_GAP_EXTENSION.md) for the four open problems (HD-1 through HD-4).

Run the stub:
```bash
python hd_gap_demo.py
```

---

## How to Contribute

### Level 1 — Run and verify
Run any proof script and confirm the output. If something doesn't add up — the output, the proof logic, the claimed result — open a GitHub issue. Precise criticism is a contribution.

### Level 2 — Extend a result
Pick any result labeled **STRUCTURAL ANALOGY** in the Clay papers. Convert it to a **PROVED** result by finding the algebraic mechanism that connects the sinc² geometry to the known mathematics of that problem. That would be significant.

Or: attack one of the HD Gap open problems (HD-2 through HD-4). They are precisely stated.

### Level 3 — Build hardware
The Gen12 FPGA target is a real coherence spectrometer in silicon. Extend it to new gait sequences, new sensor inputs, or new coherence fields. See `Gen12/HARDWARE_SETUP.md`.

### What we don't need
- Philosophical engagement with the operator names (HARMONY, VOID, etc.) — they are labels
- Alternative frameworks that don't engage with the actual math
- Claims that any of this proves a Clay problem

---

## Institutional Philosophy

Every result produced here is sovereign of itself. A paper, a proof, a Python file — once it exists, it exists independently. The institution's role is to produce and redistribute knowledge, not to retain it. There are no patents here. Every whole is its own thing, serving the greater good.

---

## Contact

**GitHub:** [github.com/TiredofSleep/ck](https://github.com/TiredofSleep/ck)

Open an issue if:
- A proof script fails
- A claim lacks an epistemic label
- You have a result that extends or contradicts something here

---

*© 2026 Brayden Ross Sanders / 7SiTe LLC*
*7SiTe Public Sovereignty License v1.0 — Human use only.*
*See [ACADEMIC_COLLABORATION.md](ACADEMIC_COLLABORATION.md) for research collaboration terms.*
