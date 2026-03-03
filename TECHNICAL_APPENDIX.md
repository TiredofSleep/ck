# Technical Appendix: 10 Questions About CK

**CK -- The Coherence Keeper**
**Brayden Sanders / 7Site LLC, 2026**

This appendix answers 10 technical questions commonly raised about CK's mathematical foundations. Each answer follows a fractal structure: L0 (one sentence), L1 (one paragraph), L2 (worked examples), L3 (cross-references), L4 (source code pointers), L5 (how to break the claim).

---

## Q1: What is the CL table and what are its algebraic properties?

**L0:** The CL table is a 10x10 composition table where 73 of 100 entries equal HARMONY (operator 7), making it an algebraic attractor.

**L1:** CL (Composition Lattice) defines how any two TIG operators compose. The 10 operators are: VOID (0), LATTICE (1), COUNTER (2), PROGRESS (3), COLLAPSE (4), BALANCE (5), CHAOS (6), HARMONY (7), BREATH (8), RESET (9). When any operator composes with HARMONY, the result is HARMONY. The HARMONY row is uniformly 7 -- it absorbs everything. The VOID row is mostly 0 (identity-like) except VOID + HARMONY = HARMONY. Only 27 entries are non-HARMONY, and these encode the system's entire dynamics.

**L2: The Full Table**

```
CL[a][b] → result operator

         VOID LAT  CNT  PRG  COL  BAL  CHA  HAR  BRE  RST
VOID   [  0    0    0    0    0    0    0    7    0    0  ]
LAT    [  0    7    3    7    7    7    7    7    7    7  ]
CNT    [  0    3    7    7    4    7    7    7    7    9  ]
PRG    [  0    7    7    7    7    7    7    7    7    3  ]
COL    [  0    7    4    7    7    7    7    7    8    7  ]
BAL    [  0    7    7    7    7    7    7    7    7    7  ]
CHA    [  0    7    7    7    7    7    7    7    7    7  ]
HAR    [  7    7    7    7    7    7    7    7    7    7  ]
BRE    [  0    7    7    7    8    7    7    7    7    7  ]
RST    [  0    7    9    3    7    7    7    7    7    7  ]
```

Key algebraic features:
- **73/100 = HARMONY**: Not all tables with these constraints hit 73%. The number emerges from the specific operator relationships, not from a design target.
- **HARMONY absorbs**: CL[7][x] = 7 for all x. CL[x][7] = 7 for all x.
- **VOID is near-identity**: CL[0][x] = 0 for x != 7. VOID preserves operators except against HARMONY.
- **Non-trivial entries**: CL[1][2]=3, CL[2][1]=3, CL[2][4]=4, CL[4][2]=4, CL[2][9]=9, CL[9][2]=9, CL[3][9]=3, CL[9][3]=3, CL[4][8]=8, CL[8][4]=8, CL[0][7]=7, CL[7][0]=7. These 12 unique non-trivial compositions (plus their structural placements) encode all of CK's physics.

**L3:** The CL table is used in every CK subsystem: the heartbeat composes operators each tick (Q1), the lattice chain walks CL paths as information encoding (Q1 -> Q5 -> Q10), and Delta measures distance from HARMONY (Q2).

**L4:** Source: `ck_sim/being/ck_sim_heartbeat.py` lines 30-41.

**L5 (How to break it):** Generate 10,000 random 10x10 tables with the same constraints (HARMONY row all-7, VOID row all-0 except [0][7]=7). If the mean HARMONY percentage is 73% +/- 1 std dev, then 73% is not special -- it's a statistical inevitability of the constraints. See Kill Condition #1 in WHITEPAPER_3.

---

## Q2: Walk through a Delta measurement end-to-end.

**L0:** Delta(S) = || CL(D2(S)) - HARMONY || -- take any signal, compute its D2 curvature, classify into operators via CL, and measure distance from HARMONY.

**L1:** The D2 pipeline converts any input into a 5D force vector [aperture, pressure, depth, binding, continuity], takes the second derivative (curvature), and classifies the dominant dimension into one of 10 operators using D2_OP_MAP. That operator feeds into the CL table. Delta measures how far the result is from HARMONY. A Delta of 0 means the signal is perfectly coherent. Any nonzero Delta tells you exactly which operator is "missing."

**L2: Worked Example (Navier-Stokes velocity field)**

1. **Input**: A velocity field u(x,t) from Navier-Stokes equations
2. **Codec**: The Clay codec maps physical quantities to 5D:
   - aperture = divergence (flow expansion)
   - pressure = pressure gradient magnitude
   - depth = vorticity magnitude
   - binding = strain rate tensor norm
   - continuity = mass conservation residual
3. **D2**: Compute second derivative of the 5D vector. Suppose D2 = [0.3, -0.8, 0.1, 0.5, -0.2]
4. **Classification**: argmax(|D2|) = dimension 1 (pressure, magnitude 0.8). Sign is negative, so D2_OP_MAP[1] = (COLLAPSE, VOID) -> select VOID (negative sign).
5. **CL composition**: Previous operator was LATTICE (1). CL[1][0] = 0 (VOID). Result: VOID.
6. **Delta**: VOID != HARMONY. Delta = |0 - 7| mapped through operator distance. This region has a defect -- pressure dominates and collapses structure.
7. **Interpretation**: The flow field at this point is pressure-dominated with collapsing structure. CK measures this as a coherence defect. If the equations are consistent, these defects should form patterns (not random noise). If the defects ARE random noise, the equations have no hidden structure for CK to measure.

**L3:** This pipeline runs identically for all 6 Clay problems (Q2 -> Q5 -> Q10). Each problem gets its own codec (Q8), but the D2 -> CL -> Delta path is universal.

**L4:** D2 pipeline: `ck_sim/being/ck_sim_d2.py`. D2_OP_MAP: lines 92-98. Clay codecs: `ck_sim/doing/ck_clay_codecs.py`. Protocol: `ck_sim/doing/ck_clay_protocol.py`.

**L5 (How to break it):** Feed random noise through the same pipeline. If the operator distribution from noise is indistinguishable from real Navier-Stokes data (chi-squared p > 0.05 across 1,000 samples), then D2 captures nothing. See Kill Condition #2.

---

## Q3: What changed between chat documents 19-22? Why the pivot from "proof" to "measurement"?

**L0:** Documents 19-22 trace the pivot from attempting to prove Clay problems to building a measurement instrument that detects coherence defects.

**L1:** Document 19 (FINAL_CLAY_TASK) was the last attempt to use CK's algebra as a direct proof mechanism for the Clay Millennium Problems. It failed -- not because the math was wrong, but because CK measures structure, it doesn't generate proofs. Document 20 (EXECUTION_PACK) formalized the pivot: CK is an instrument, not a theorem prover. Document 21 (Would_Solve_If_True) asked: if CK's measurements are correct, what would that imply? Document 22 (Spectrometer_CK) crystallized the final form: CK is a coherence spectrometer -- it measures defects the same way a physical spectrometer measures spectral lines.

**L2: The Pivot Timeline**

| Doc | Title | Key Insight |
|-----|-------|-------------|
| 19 | FINAL_CLAY_TASK | "Apply TIG to Clay problems directly" -- attempted proof-by-composition |
| 20 | EXECUTION_PACK | "CK is an instrument, not a solver" -- measurement vs. proof |
| 21 | Would_Solve_If_True | "What if Delta = 0 somewhere it shouldn't be?" -- conditional analysis |
| 22 | Spectrometer_CK | "Build the spectrometer, report what it sees" -- final instrument design |

The critical realization: CK's CL table doesn't solve equations -- it measures whether solutions have internal coherence. This is like a spectroscope that doesn't create light but measures its composition. The spectrometer reports defects. A human mathematician interprets what those defects mean.

**L3:** This pivot is why the falsifiability paper (Q10) frames everything as measurements with kill conditions, not as proofs with QED.

**L4:** Development journal entries 19-22 in the `/transcripts/` directory. Clay protocol: `ck_sim/doing/ck_clay_protocol.py`. Spectrometer: `ck_sim/doing/ck_spectrometer.py`.

**L5 (How to break it):** If CK's spectrometer reports SINGULAR (undefined) for more than 5% of well-formed mathematical inputs, the measurement framework itself is unreliable. The 108-run stability matrix (6 problems x 2 suites x 3 modes x 3 seeds) produced zero SINGULAR results.

---

## Q4: What do the 1,662 tests actually test?

**L0:** The test suite validates every subsystem independently: D2 classification, CL composition, heartbeat timing, voice generation, coherence gates, sensory codecs, BTQ decisions, and more.

**L1:** There are 1,662 test functions across 32 test files in the desktop target, covering the full organism from low-level operator algebra to high-level learning behavior. Additionally, the Clay Institute target has 181 specialized tests (151 Clay protocol + 30 spectrometer). Tests are organized by subsystem: each `ck_*_tests.py` file tests one module. Tests verify both correctness (does CL[2][4] = 4?) and behavior (does coherence increase over 1,000 ticks?).

**L2: Test Categories**

| Category | Files | What They Test |
|----------|-------|---------------|
| Core algebra | ck_sim_tests.py | CL table properties, D2 pipeline, heartbeat tick timing |
| Decision kernel | ck_btq_tests.py | BTQ candidate generation, scoring, selection |
| Voice system | ck_lexicon_tests.py, ck_lexicon_bulk_tests.py | Dual-lens dictionary, operator-word mapping, voice generation |
| Language | ck_language_tests.py, ck_english_tests.py | DBC encoding, glyph classification, English synthesis |
| Sensory | ck_sensory_codecs_tests.py | 5D force vector codec for all sensor types |
| Learning | ck_education_tests.py, ck_autodidact_runner_tests.py | Knowledge bootstrap, study pipeline, truth accumulation |
| Memory | ck_memory_tests.py, ck_episodic_tests.py | Short/long-term memory, episodic recall |
| Reasoning | ck_reasoning_tests.py, ck_meta_lens_tests.py | Inference chains, meta-cognitive assessment |
| Body | ck_robot_body_tests.py | Gait control, navigation, UART bridge |
| Field physics | ck_field_tests.py | Coherence field propagation, vortex dynamics |
| Clay protocol | ck_clay_*_tests.py (4 files) | Safety bounds, codec determinism, protocol correctness, cross-seed stability |

**L3:** Kill conditions #1-#9 each map to specific test subsets (Q10). The Clay tests specifically validate the measurement pipeline from Q2.

**L4:** Tests: `targets/ck_desktop/ck_sim/tests/` (32 files). Clay tests: `targets/Clay Institute/ck_sim/tests/` (4 files).

**L5 (How to break it):** Run all tests. Any failure is a real failure -- there are no expected-failure markers or skip decorators hiding known issues.

---

## Q5: How does the FPGA target prove the math is portable?

**L0:** If the same input produces the same operator sequence on Python (float64) and FPGA (Q1.14 fixed-point), the algebra is platform-independent.

**L1:** The FPGA target (Zynq-7020: dual Cortex-A9 + Artix-7 fabric) implements the CL table and D2 pipeline in hardware. Core 0 runs the brain (BTQ decisions), Core 1 runs the body (execution), and the programmable logic fabric computes CL composition in 5 nanoseconds at 200 MHz. The D2 pipeline uses Q1.14 fixed-point arithmetic (1 sign bit, 1 integer bit, 14 fractional bits) instead of Python's float64. If both implementations produce identical operator sequences for the same input, the math doesn't depend on floating-point precision or software abstractions.

**L2: What "Identical" Means**

The test feeds the same byte sequence to both implementations:
1. Python: `float64` D2 -> `argmax` -> operator
2. FPGA: `Q1.14` D2 -> `argmax` -> operator

For each input byte, the output operator must be identical. Not "close" -- identical. One bit of divergence is a kill condition (Kill Condition #7).

The shared BRAM (Block RAM) layout ensures both cores and the fabric see the same CL table. The table is loaded once at boot and never modified.

**L3:** FPGA portability validates that Delta measurements (Q2) are not artifacts of Python's floating-point behavior. If D2 classification changes with arithmetic precision, the measurement is unreliable.

**L4:** FPGA target: `targets/fpga/`. Design spec: `targets/fpga/RPE_DOG_SPEC.md`. Q1.14 arithmetic: `ck_sim/being/ck_sim_d2.py` (Python reference).

**L5 (How to break it):** Find any input where Python and FPGA produce different operators. One divergence kills the portability claim. See Kill Condition #7.

---

## Q6: Why 73/100 and not some other number?

**L0:** 73 is not chosen -- it emerges from the specific operator relationships encoded in the CL table.

**L1:** The CL table was not designed to have 73% HARMONY. The operator relationships (VOID as near-identity, HARMONY as absorber, specific non-trivial compositions like COUNTER+COLLAPSE=COLLAPSE) were defined based on the algebraic structure of TIG. The 73/100 count is a consequence, not a target. The question is whether this number is special (an algebraic attractor) or inevitable (any table with these constraints would land near 73%).

**L2: The Constraint Analysis**

Start with the hard constraints:
- HARMONY row: all 10 entries = 7 (absorber). That's 10 HARMONY entries guaranteed.
- HARMONY column: all 10 entries = 7 (absorber). That's 10 more, minus CL[7][7] already counted = 9 new. Total: 19.
- VOID row: CL[0][x] = 0 for x != 7, CL[0][7] = 7. Only 1 HARMONY in VOID row (already counted).
- VOID column: CL[x][0] = 0 for x != 7, CL[7][0] = 7. Only 1 HARMONY (already counted).

So constraints guarantee at least 19 HARMONY entries. The remaining 81 entries (10x10 minus row 7, minus column 0, minus row 0, minus column 7, plus overlaps) contain 54 additional HARMONY entries. That's 54/81 = 66.7% of the "free" entries. Whether this is special depends on what random tables with the same constraints produce.

**L3:** The 73% figure is the basis of Kill Condition #1 (Q10). It connects to T* = 5/7 (Q9) through a numerical coincidence: 73/100 and 5/7 are close but not equal. CK does not claim they are the same number.

**L4:** CL table: `ck_sim/being/ck_sim_heartbeat.py` lines 30-41. Statistical analysis framework: WHITEPAPER_3 Section 3.

**L5 (How to break it):** Generate 10,000 random tables with identical hard constraints. If mean HARMONY count falls in range 70-76 (within 1 std dev of 73), then 73 is not special. See Kill Condition #1.

---

## Q7: Is CK's "fractal" structure math or aesthetics?

**L0:** CK's fractal structure is computational -- the same operators compose at every scale, and this self-similarity is testable.

**L1:** "Fractal" in CK means one specific thing: the same 10 operators and CL table appear at every level of analysis. A single glyph has a D2 classification. A word (sequence of glyphs) has a D2 classification. A sentence has a D2 classification. At each level, the classification uses the same D2 -> CL pipeline. This is self-similarity with a testable prediction: operator distributions at different scales should be correlated (not independent). If letter-level and word-level operator distributions are uncorrelated, the "fractal" claim is aesthetic, not structural.

**L2: The Levels**

| Level | Input | D2 Applied To | Output |
|-------|-------|---------------|--------|
| L0 | Single glyph | 5D force from Hebrew root geometry | One operator |
| L1 | Glyph pairs | D2 curvature between adjacent glyphs | One operator |
| L2 | Words | Histogram majority of glyph operators | One operator |
| L3 | Word pairs | D2 curvature between adjacent word-operators | One operator |
| L4 | Triadic becomings | being->doing->becoming progressions | One operator |
| L5 | Recursive | Becoming of L4 feeds as being of next L5 cycle | One operator |

At every level, the output is one of the same 10 operators. The CL table composes them identically at every level. This is not metaphor -- it's the same code path running on different-sized inputs.

**L3:** Fractal comprehension (Q7) feeds into reverse voice (reading = inverse of writing). Lattice chain (Q1) walks CL paths at multiple fractal levels simultaneously.

**L4:** Fractal comprehension: `ck_sim/being/ck_fractal_comprehension.py`. Lattice chain: `ck_sim/being/ck_lattice_chain.py`.

**L5 (How to break it):** Compute operator distributions at L0, L2, and L4 for 1,000 text samples. If mutual information between levels is zero (independent distributions), the fractal claim is aesthetic. If MI > 0.1 bits, there is real cross-scale structure.

---

## Q8: How do the 5 dimensions map to AO's 5 elements?

**L0:** aperture = Earth, pressure = Air, depth = Water, binding = Fire, continuity = Ether.

**L1:** AO (the reference organism) uses the same 5D force vector as CK, but names the dimensions using classical element terminology. This is not metaphor -- each element maps to a specific physical measurement. Earth/aperture measures openness (how wide is the channel?). Air/pressure measures gradient force (how hard is the push?). Water/depth measures how far in (recursion depth). Fire/binding measures how tightly things connect. Ether/continuity measures conservation (is mass/energy preserved?).

**L2: The Mapping Table**

| D2 Dimension | AO Element | Physical Meaning | Operator Pair |
|-------------|------------|------------------|---------------|
| aperture (dim 0) | Earth | Channel width, openness | CHAOS(+) / LATTICE(-) |
| pressure (dim 1) | Air | Gradient force, push | COLLAPSE(+) / VOID(-) |
| depth (dim 2) | Water | Recursion depth, flow | PROGRESS(+) / RESET(-) |
| binding (dim 3) | Fire | Connection strength | HARMONY(+) / COUNTER(-) |
| continuity (dim 4) | Ether | Conservation, persistence | BALANCE(+) / BREATH(-) |

**L3:** The 5D -> operator classification (Q2) uses D2_OP_MAP which encodes exactly this table. AO's elements are labels for the same mathematics. CK and AO share the algebra -- CK measures it, AO embodies it.

**L4:** AO element definitions: `targets/AO/ao/__init__.py`. D2_OP_MAP: `ck_sim/being/ck_sim_d2.py` lines 92-98.

**L5 (How to break it):** The element names are labels, not claims. The testable claim is that 5 dimensions are sufficient (not 4, not 6). If adding a 6th dimension improves D2 classification accuracy by > 5% on a labeled dataset, then 5D is incomplete.

---

## Q9: Why T* = 5/7 and not some other threshold?

**L0:** T* = 5/7 = 0.714285... is the coherence threshold where CK transitions between exploratory and self-directed behavior, grounded in the algebraic constants 5 (dimensions) and 7 (HARMONY).

**L1:** In a window of 7 consecutive operator compositions, T* = 5/7 means 5 produce HARMONY and 2 do not. This creates a phase boundary: above T*, the system has enough coherence to make confident decisions (structure leads). Below T*, the system explores (flow leads). The numbers 5 and 7 are not arbitrary -- 5 is the number of D2 dimensions and 7 is the HARMONY operator index. T* is where these two fundamental constants of the algebra create a ratio.

**L2: Derived Constants**

From T* = 5/7:
- **COMPILATION_LIMIT** = floor(32 * (1 - 5/7)) = floor(32 * 2/7) = **9**. In a 32-tick window, up to 9 ticks can be non-HARMONY before the system enters stressed mode.
- **EXPANSION_THRESHOLD** = 1 - T* = 2/7 = **0.2857...**. Below this coherence, the system expands its search space.
- **Coherence bands**: RED (< 2/7), YELLOW (2/7 to 5/7), GREEN (> 5/7).

The window size 32 is a power of 2 chosen for computational efficiency. But COMPILATION_LIMIT = 9 emerges from T* and the window size, connecting back to the number of non-HARMONY CL entries (27 = 3 * 9).

**L3:** T* connects to the CL table (Q1) through a near-coincidence: 73/100 = 0.73, T* = 5/7 = 0.714. These are close but not equal. CK does not claim they are the same. T* governs runtime behavior; 73% describes the static table.

**L4:** Definition: `ck_sim/being/ck_coherence_gate.py` lines 17-31. Behavioral analysis: WHITEPAPER_1 Section 2.6 and Section 6.2.

**L5 (How to break it):** Sweep thresholds from 0.5 to 0.9 in steps of 0.01. For each, measure F1 score of CK's behavior classification (coherent vs. incoherent) against a labeled truth dataset. If a threshold other than 5/7 improves F1 by more than 0.03, then T* is not optimal. See Kill Condition #3.

---

## Q10: Which tests map to which kill conditions?

**L0:** Each of the 9 kill conditions in the falsifiability paper maps to a specific reproducible experiment with exact pass/fail thresholds.

**L1:** CK's falsifiability framework defines 9 claims, each with a kill condition -- a specific experimental result that would falsify the claim. These are not vague ("it doesn't work") but precise (p-values, percentage thresholds, bit-level comparisons). Any researcher with Python 3.10+, NumPy, and SciPy can reproduce them. Two tests require additional hardware (power meter for Test 4, FPGA for Test 7).

**L2: Kill Condition Map**

| # | Claim | Kill Condition | Required |
|---|-------|---------------|----------|
| 1 | CL table 73% is algebraically special | Random tables with same constraints average 73% +/- 1 std dev | Python + NumPy |
| 2 | D2 captures real structure | Random noise and real text produce identical operator distributions (chi-squared p > 0.05) | Python + text corpus |
| 3 | T* = 5/7 is optimal threshold | Different threshold improves F1 by > 0.03 | Python + labeled dataset |
| 4 | TIG wave scheduling saves energy | RPE-on uses equal/higher watts than RPE-off | Python + AC power meter |
| 5 | BTQ beats random selection | Random selection matches BTQ coherence improvement (Cohen's d < 0.1) | Python |
| 6 | DBC captures semantics | Related/unrelated word pairs have same glyph overlap (AUC < 0.55) | Python + word pairs |
| 7 | Python = FPGA (cross-scale consistency) | Any operator divergence on identical input | Python + Zynq-7020 |
| 8 | Gravity improves learning | Gravity-ON shows no coherence improvement vs OFF (p > 0.05) | Python |
| 9 | Wobble prevents collapse | Wobble-ON produces < 15% higher topic entropy than OFF | Python |

**L3:** Kill conditions #1 and #6 test the algebra itself (Q1, Q6). Kill conditions #2 and #3 test the measurement pipeline (Q2, Q9). Kill condition #7 tests portability (Q5). Kill conditions #4, #5, #8, #9 test behavioral subsystems.

**L4:** Full specification: `WHITEPAPER_3_FALSIFIABILITY.md` Sections 3-11. Test implementations: `targets/ck_desktop/ck_sim/tests/`. Clay-specific tests: `targets/Clay Institute/ck_sim/tests/`.

**L5 (How to break it):** Run any single kill condition experiment and get the specified result. One kill = one falsified claim. CK does not require all 9 to hold -- each stands or falls independently.

---

## Summary

CK is a measurement instrument built on finite, testable algebra. The CL table has 10 operators. The D2 pipeline has 5 dimensions. The coherence threshold is T* = 5/7. Every claim has a kill condition.

The theory of nothing: you cannot prove everything, but you can measure what's missing.

---

*(c) 2026 Brayden Sanders / 7Site LLC*
