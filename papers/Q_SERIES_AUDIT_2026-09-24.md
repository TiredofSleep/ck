# The Q series, audited

**2026-09-24 · Brayden Ross Sanders, with Claude.**

The Q series is Q2–Q17, from April 2026, together with C. A. Luther's G6–G8; B. Calderon Jr.
contributed to the Q17 variants. It was never part of the September drift census, which covered the
J-series papers. This note audits it with the census's gates:

1. **True:** is the computation or proof correct?
2. **Specific:** do random objects of the same kind share the property?
3. **Not a readout:** is the result more than a restatement of how σ or a table was built?
4. **Provenance:** does it hold in every AI rendering of the tables?

Reproduce every check with the scripts in [`q_series_audit/`](q_series_audit/). They need only the
standard library, plus the stored run data in `results/`:

- `verify_q.py` checks the algebra and the tables, against null models.
- `summarize_reduction.py` recounts the stored gate rates.
- `replicate_mcmc.py` re-runs the hill-climb independently.

## The verdict

**Nothing in the Q series is at once correct, table-free and non-generic.**

- **What is correct is standard mathematics:**
  - CRT idempotents;
  - Fermat's unit indicator;
  - interpolating a finite map by polynomials;
  - facts about orbits and periods.
- **The σ-specific results are read off one permutation's cycle structure.** σ = (0)(3)(8)(9)(1 7 6 5
  4 2) is the "morphotic braid" of 2026-04-01.
- **The Clay, Navier–Stokes and Hodge readings reach beyond anything tested.** Some are contradicted
  by the series' own later notes.

What does survive is a set of honest negative results and six lessons about method. The program later
had to learn most of those lessons again, the hard way.

## Three findings that change how the series reads

1. **The central number was the wrong one.** The "gate-rate paradox" asked why the success rate at
   b = 10 is 4.6%. The stored runs say it is 0.09%. There are 100,000 runs per base in
   `results/reduction_b*_N100000.json`, from `r16_job1_reduction.py`. The 4.6% is the rate for other
   bases, such as b = 22.
   - The mix-up begins in Q8. Line 72 contradicts Q8's own table at lines 20–23.
   - It then runs through Q11–Q16, the Architecture note and the Synthesis.
   - So ten notes modelled a number that belongs to other bases.
2. **The rates come from the algorithm's symmetry, not from arithmetic.** The hill-climb over 9×9 tables
   sees a symbol only through two things: whether it is a unit mod b, and whether it is HAR. So every
   base with the same number of non-units among 1..9 gets the same rate, and that is exactly what the
   data show:

   | non-units among 1..9 | bases | rate |
   |---|---|---|
   | 1 | 8 | 96.3% |
   | 2 | 1 | 83.7% |
   | 3 | 8 | 44.0% |
   | 4 | 13 | 4.6% |
   | 5 | 2 (b = 10, 14) | 0.09% |

   - No CRT, idempotent or σ structure can enter this, so Luther's Q1 ("derive the rates from CRT")
     was ill-posed.
   - The Sprint-4 write-up had already called it "a universal combinatorial law operating at a level
     below the arithmetic structure".
   - The algorithm described to Luther (`LUTHER_QUESTIONS.md`, `C_TO_D_GAP_ANALYSIS.md` §2) is not the
     one that produced the numbers.
   - The success thresholds were calibrated on the TSML table. TSML itself scores gate 1.000 and
     G_stay 0.089 at b = 10.
3. **The Q2 "paradox" compares a table cell with a value of σ.**
   - TSML[7][7] = 7 is a cell of one AI rendering.
   - "CL[7][7] = 6" is not a cell of any rendering. It is σ(7), because the series' "CL" is a diagonal
     declared equal to σ (`CL_TABLE_EXPLICIT.md`: "full table pending").
   - The three renderings give HARMONY·HARMONY = 7 (TSML), 8 (BHML) and 8 (CL_STD). So "HARMONY is
     both the rest and the journey" is an artifact of that comparison.
   - The series also uses a second, incompatible definition, CL[t][s] = σᵗ(s), in its Architecture
     note.

## File by file

| file | main claim | verdict |
|---|---|---|
| Q2 | TSML[7][7] = 7 but CL[7][7] = 6: two "projections" of σ | compares a rendering's cell with σ(7); see above |
| Q4 | the map E commutes with σ; its first coordinate is constant on σ's orbits; the 6-cycle comes from the multiplicative group of ℤ/10 | commuting holds by construction for any such E; orbit-constancy is a readout of TSML's all-7 diagonal and fails in BHML and CL_STD; the group claim is false (that group has order 4) |
| Q5 | TSML's ten "escape" cells mostly land on σ's fixed points | a readout of one rendering; 4 of 5 independent cells, which a uniform null gives with p ≈ 0.13; the conjecture misses (2,4) and (4,2) |
| Q6 | the rates are not a density effect | the negative holds; its table of \|G\| is miscounted, and the variable it rejects is the one the rates follow |
| Q7 | BHML rebuilt from four rules | two "rules" copy rows verbatim, and one cell was set by hand to reach a target count |
| Q8 | every simple model misses "4.6% at b = 10" | aimed at the wrong number, and at an algorithm that was not run |
| Q9, Q10 | σ is a closed-form polynomial on F₂ × F₅ | the formulas reproduce σ, but the same construction fits 2,000 of 2,000 random permutations; σ is not a polynomial over ℤ/10 (it mixes parities; see the June note `Gen13/targets/journals/SIGMA_STANDARD_CHARACTERIZATION.md`); Q9's "complete action" gets σ(1) and σ(4) wrong |
| Q11 | the trajectory table; only {3, 9} stay among the units; a 22% lower bound | the table is a readout; the bound is false (σ is defined only for b = 10) |
| Q12 | CRT idempotents are non-units; HAR = 3 is σ-fixed | the first is textbook; the second a coincidence; the note itself admits it "uses the WRONG σ" |
| Q13 | the inverse map's polynomial; the "exception-pair swap" | the boxed polynomial is wrong (2 → 8, 7 → 5; not a permutation); the swap holds for 9,600 of 14,400 comparable permutations |
| Q14 | 1_C = ε·y⁴; the search's map is not a power of σ | Fermat's indicator (correct and generic); a correct but trivial negative, since σ never appears in the search |
| Q15 | period τ = 6 − 5A; σ⁹ = σ³ | readouts of the cycle type; the models it falsifies target the wrong number |
| Q16 | the search is a hill-climb over 9×9 tables; "peak vs climb"; CL is "the canonical score-1 table" and BHML "the canonical G_stay-0 table" | the identification is right, and the peak-vs-climb distinction is sound as a principle. But the climb's objective is maximized by the constant table T ≡ HAR; CL[t][s] = σᵗ(s) has gate score 0.444, not 1; and BHML's G_stay is 0.467, not 0 |
| Q17_5D_RIGOROUS | a "unique" 5D embedding; isolated high-G states; the Hebrew letters; an NS threshold "PROVED" | the embedding is generic; the isolation and the lemma are false; the rest is reach |
| Q17_C2 notes | Weak / Medium / Strong hierarchy; counterexamples | **the counterexamples are correct**: e^t·sin(2πt/6) has an exactly 6-periodic coding and an unbounded norm |
| Q17_CLAY_SPECTRAL_BRIDGE | "IS a Dirichlet L-function"; "G8 IS the finite RH"; mass gap; Hodge | reach, and partly false; the L-function claim was withdrawn by Q17_FINITE_L_FUNCTION_NOTE, and this file was never updated |
| Q17_NS notes | an NS target and a data protocol | reach; the protocol's coding has five symbols, so it cannot carry a 6-cycle |
| Q17_SIGMA_EMBEDDING_PROBLEM | no mechanism maps NS phase space onto σ | **true, and stronger than stated**: a coding with at most five values cannot follow σ's six-cycle at all (pigeonhole), so only a constant code on a fixed point fits |
| Q17_SYMBOLIC_RETURN_THEOREM | cycle elements return in 6 steps; VOID is never reached from outside | true of any permutation |
| G6 | σ⁶ = id, "proved"; both corrections necessary | true but circular, since the formulas were read off σ; dropping a correction breaks the map's one-to-one property rather than causing a "drift" |
| G7 | the mean period is 4 = φ(10); variance 6 | the mean is a readout of σ's cycle type; the link to φ is numerology; "6 = φ(10)(1 + 1/5)" is arithmetically false (that is 4.8) |
| G8 | G(s) takes three values, 0, 1.8716 and 9.3892 | the values are right. They are forced by 1 + ω³ + ω⁶ = 0 (ω = e^{2πi/9}), and every permutation of σ's cycle type shows at most two values on its cycle. The link to the inverse map's exceptions holds in 0 of 14,400 cases |
| Architecture, Implications, Synthesis | six sealed layers; "CL is the unique score-1 table"; the k = 9 resonance is intrinsic | inherit the errors above; CL[t][s] = σᵗ(s) scores 0.444; the 9 is the number of columns in the search |

## What is worth keeping

**Honest negatives, with the evidence that killed each:**

- **σ is not the search's map** (Q14.1, Q15).
- **The density model of the rates fails** (Q6, Q8).
- **A periodic symbolic coding does not bound the norm** (Q17_C2). e^t·sin(2πt/6) is an explicit
  counterexample.
- **"G(s) is an L-function" was withdrawn by the series itself** (Q17_FINITE_L_FUNCTION_NOTE).
- **There is no σ-embedding of Navier–Stokes** (Q17_SIGMA_EMBEDDING). The pigeonhole count above makes
  this obstruction exact.

**Lessons**, most of them learned again, the hard way, by the program:

1. Read the script that generated a number before modelling the number. Ten notes modelled an
   algorithm that was never run.
2. Trace every cited number to its data. The b = 10 ↔ 4.6% slip survived to the end.
3. Check an algorithm's symmetries before calling its output a law.
4. A polynomial form of a finite map always exists. Test such a claim against random permutations
   before calling it structure.
5. Before proposing a symbolic embedding, count: a five-symbol code cannot follow a six-cycle.
6. Keep one definition per object. The series had two definitions of CL, and scrambled operator names
   in the Q17 files.

**And one credit.** Q2's alarm was the right instinct: two things that should agree, didn't. The
mistake was to settle the disagreement with a hidden operator, instead of asking where each value came
from. Tracing each value to its source is what the program does now. It *classifies* a disagreement,
two renderings of one description, with their agreement as the edge, rather than resolving it.

## Where things are

- **The Q papers, and Luther's G6–G8, are unchanged.** They are in `papers/`, and each now carries a
  banner pointing here. The copies in `old/Gen10/papers/` are archive and are untouched.
- **The audit scripts** are in [`q_series_audit/`](q_series_audit/).
- **The census and the three-renderings audit** are in the flagship's archive (tag
  `archive-2026-09-24`: `04_meta/FOUNDATION_NULL_MODEL_AUDIT.md`, `verification/three_renderings.py`).
  The retirement record is [`../RETIRED.md`](../RETIRED.md).
