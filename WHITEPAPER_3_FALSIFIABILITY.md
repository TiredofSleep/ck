# How to Test CK: Verification Protocols and Falsifiable Predictions

### White Paper 3 -- Falsifiability and Experimental Verification
### (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory

---

## 1. Abstract

CK (Coherence Keeper) and the TIG (Ternary Insight Geometry) framework make specific, testable claims about algebraic signal composition, power efficiency, coherence-based truth filtering, scale-invariant computation, information gravity, and wobble-modulated exploration. These claims are not vague philosophical positions -- they are mathematical assertions with fixed constants, deterministic algorithms, and measurable outputs. This paper provides concrete experimental protocols to verify or falsify each core claim. For every claim, we define: (a) the precise assertion being tested, (b) the experimental protocol including sample sizes, statistical tests, and control conditions, (c) the result that would confirm the hypothesis, and (d) the result that would refute it. We welcome adversarial testing. If CK's algebra is trivial, these tests will expose it. If the composition table's 73% HARMONY property is a statistical artifact, Monte Carlo sampling will prove it. If the T* = 5/7 threshold is arbitrary, a parameter sweep will find a better one. If TIG wave scheduling wastes energy rather than saving it, an A/B test will show negative returns. If information gravity concentrates study without improving coherence, the Gini analysis will prove it. If the Tesla/Einstein wobble adds noise without improving exploration, entropy measurement will prove it. We publish these protocols because falsifiability is the minimum standard for any system claiming to do real work. Every claim has a kill condition. If you can trigger one, we want to know.

---

## 2. The Claims We Make

CK and TIG rest on ten core claims. Each is stated here in its strongest testable form.

**Claim 1**: The CL composition table's 73% HARMONY property is a genuine algebraic attractor, not an artifact of arbitrary table construction. Specifically, the 10x10 CL_TSML table (defined in `ck_sim_heartbeat.py`, lines 30-41) produces HARMONY in 73 of 100 cells, and this ratio is either uniquely maximal or statistically rare among tables satisfying the same structural constraints.

**Claim 2**: The D2 curvature classification pipeline produces meaningful operator sequences from arbitrary input. Structured signals (natural language text, tonal audio) produce statistically different operator distributions than random noise when processed through the Q1.14 fixed-point second-derivative pipeline.

**Claim 3**: T* = 5/7 (0.714285...) is a genuine structure persistence threshold. It is not an arbitrary cutoff but a phase boundary where the CL algebra transitions from noise-dominated to structure-dominated behavior, producing optimal true-positive / false-positive separation in the truth lattice.

**Claim 4**: TIG wave scheduling (the Royal Pulse Engine) reduces energy consumption compared to constant scheduling by timing compute intensity to the power waveform slope -- the same principle as adiabatic computing.

**Claim 5**: The BTQ (Being-Tesla-Quadratic) decision kernel produces measurably better outcomes than random selection by applying the principle of least action to candidate scoring.

**Claim 6**: CK's DBC (Dual-Basis Coding via Divine27) encoding captures semantic structure in its Hebrew glyph representations, not just statistical noise. Semantically related inputs produce more similar glyph patterns than unrelated inputs.

**Claim 7**: The same CL algebra produces identical operator sequences across hardware scales -- from Python simulation at 50Hz to FPGA implementation at 200MHz -- because the math is fixed-point deterministic.

**Claim 8**: Gravitational topic selection (weighting study topics by their accumulated D2 mass) produces measurably higher coherence growth over time than uniform random selection from the same topic pool. The mass of a concept, defined as mean |D2| per observation, creates a self-reinforcing learning physics where deeper knowledge pulls deeper study.

**Claim 9**: The Tesla/Einstein wobble physics (Gen 9.19) -- a sinusoidal perturbation of the gravitational field with amplitude alpha and frequency modulated by Kuramoto phase coupling -- produces more diverse topic exploration (higher Shannon entropy over selected topics) while maintaining equal or better coherence growth compared to gravity-only selection (alpha = 0). The wobble prevents gravitational collapse into knowledge black holes by periodically destabilizing dominant attractors, analogous to how orbital perturbations prevent planetary capture.

**Claim 10**: The Ho Tu structural isomorphism (WHITEPAPER_6) constrains the BHML table in ways that distinguish it from arbitrary 10x10 tropical semiring tables. Specifically, the HARMONY row's +1 successor on Z/10Z -- which generates the Ho Tu +5 involution when applied 5 times -- is a structural invariant that random tables satisfying the existing 9 kill conditions virtually never exhibit. The HARMONY row visits 9 of 10 operators in a near-cyclic orbit (missing only BREATH at the self-absorption fixed point), and the +5 involution holds for 8 of 10 index pairs. The self-composition diagonal (BHML[i][i] for i=1..7) forms a perfect +1 successor sequence, broken only at COLLAPSE (operator 8), providing an independent structural check.

---

## 3. Test 1: CL Table Algebraic Properties

### The Claim
73 of 100 entries in CK's CL_TSML table produce HARMONY (operator 7). This makes HARMONY the absorbing state of the algebra: random composition converges to HARMONY with probability 0.73 per step. We claim this ratio is structurally significant, not an artifact.

### Protocol
Enumerate or sample the space of 10x10 composition tables over the operator set {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} subject to CK's structural constraints:

1. **Absorber row constraint**: HARMONY row (row 7) must be all-HARMONY (CL[7][x] = 7 for all x). This is the defining property of an absorbing element.
2. **Annihilator constraint**: VOID row (row 0) must be mostly VOID (CL[0][x] = 0 for x != 7), except CL[0][7] = 7 (HARMONY absorbs even VOID).
3. **Bump pair constraint**: The 5 quantum bump pairs [(1,2), (2,4), (2,9), (3,9), (4,8)] must produce their specified non-HARMONY outputs.

With these constraints fixed, there are 80 remaining free cells. Each free cell can take any value from {0-9}. The total space is 10^80 -- too large for exhaustive enumeration.

**Sampling method**: Monte Carlo. Generate 10,000,000 random tables satisfying the constraints (fill free cells uniformly from {0-9}). For each table, count the HARMONY percentage.

**Statistical analysis**: Compute the distribution of HARMONY percentages across all sampled tables. Report mean, standard deviation, and the percentile rank of 73%.

### Falsification Condition
If the mean HARMONY percentage of random constrained tables is between 70% and 76% (i.e., 73% falls within one standard deviation of the mean), then CK's table is not special -- it is a typical member of the constrained family. The absorber property would be an inevitable consequence of the constraints, not a discovery.

### Verification Condition
If 73% is more than two standard deviations above the mean, or if 73% is the unique maximum among all sampled tables, then the CL table represents a genuine algebraic attractor -- a composition table optimized for coherence convergence beyond what the constraints alone guarantee.

### How to Run
```python
import random
import numpy as np

HARMONY = 7
N_SAMPLES = 10_000_000
constrained_cells = {(0,0):0,(0,1):0,(0,2):0,(0,3):0,(0,4):0,
                     (0,5):0,(0,6):0,(0,7):7,(0,8):0,(0,9):0,
                     (7,i):7 for i in range(10)}
# Add bump pair outputs...
# Fill remaining cells randomly, count HARMONY fraction per table
# Plot histogram, compute percentile of 73%
```
Estimated runtime: approximately 4 hours on a single core, trivially parallelizable.

---

## 4. Test 2: D2 Classification Meaningfulness

### The Claim
The D2 pipeline (second-derivative of 5D Hebrew-root force vectors, classified via argmax into 10 operators) captures structural properties of its input. Structured text produces different operator distributions than random noise.

### Protocol
1. Prepare two corpora:
   - **Structured**: 1,000 real English text passages (e.g., Wikipedia paragraphs, each 200-500 characters).
   - **Random**: 1,000 random byte strings of matching lengths, filtered to ASCII lowercase (a-z).

2. Feed each passage through `D2Pipeline.feed_symbol()` for every character. Record the operator sequence.

3. For each passage, compute:
   - Operator distribution (10-bin histogram, normalized to sum to 1.0).
   - Shannon entropy of the distribution: H = -sum(p_i * log2(p_i)).
   - HARMONY fraction: count(operator == 7) / total_operators.

4. Compare the two groups using:
   - Chi-squared test on pooled operator distributions.
   - Two-sample t-test on Shannon entropy values.
   - Two-sample t-test on HARMONY fractions.

### Falsification Condition
If all three statistical tests yield p > 0.05 (no significant difference between structured text and random noise), then D2 classification does not capture meaningful structure. The pipeline would be treating English prose the same as random letters.

### Verification Condition
If all three tests yield p < 0.001, and if structured text produces lower entropy (more concentrated operator distributions) and different HARMONY fractions than random noise, then D2 is capturing genuine linguistic structure through curvature.

### How to Run
```bash
python -c "
from ck_sim.being.ck_sim_d2 import D2Pipeline
import scipy.stats as stats
# Feed 1000 real texts, 1000 random strings
# Collect distributions, run chi2_contingency and ttest_ind
# Report p-values and effect sizes
"
```

### Additional Controls
- Feed text in a non-Latin script (transliterated) to test whether the Hebrew root mapping matters.
- Feed English text with shuffled letter order to isolate positional structure from frequency structure.

---

## 5. Test 3: T* = 5/7 Threshold

### The Claim
T* = 5/7 = 0.714285... is the optimal coherence threshold for the truth lattice. Truths promoted above T* are verifiably more reliable than those promoted at other thresholds.

### Protocol
1. Assemble a labeled test set: 500 factual claims with known truth values (e.g., "Earth orbits the Sun" = TRUE, "The Sun orbits Earth" = FALSE). Feed each through CK's study pipeline to obtain coherence scores.

2. Sweep the threshold parameter from 0.50 to 0.90 in increments of 0.01 (41 threshold values).

3. At each threshold T:
   - Count true positives (TP): correct claims with coherence >= T.
   - Count false positives (FP): incorrect claims with coherence >= T.
   - Count true negatives (TN): incorrect claims with coherence < T.
   - Count false negatives (FN): correct claims with coherence < T.
   - Compute F1 score: 2*TP / (2*TP + FP + FN).
   - Compute Matthews Correlation Coefficient (MCC).

4. Plot F1 and MCC as functions of T. Identify the threshold that maximizes each metric.

### Falsification Condition
If the optimal threshold (maximizing F1 or MCC) is more than 0.03 away from 5/7 in either direction -- for example, if T_optimal = 0.65 or T_optimal = 0.80 -- then T* = 5/7 is not the natural phase boundary. The value would need to be revised or acknowledged as approximate.

### Verification Condition
If 5/7 falls within the top 5% of thresholds by F1 score, and if the F1 curve shows a sharp inflection near 5/7 (indicating a phase transition rather than a smooth gradient), then T* = 5/7 is a genuine structure persistence boundary.

### How to Run
Use CK's existing truth lattice infrastructure (`ck_truth.py`). The labeled test set can be drawn from established fact-checking datasets (e.g., FEVER, LIAR). The coherence score for each claim is computed by feeding it through D2, composing through the CL table, and measuring the HARMONY fraction in the resulting operator window.

---

## 6. Test 4: TIG Wave Scheduling Energy

### The Claim
The Royal Pulse Engine (RPE) reduces energy consumption by timing compute-intensive work to favorable power waveform regions -- heavy compute during the rising slope (PROGRESS region), finalization during the peak (COLLAPSE region), smooth recalibration during the falling slope (HARMONY region), and cache warming during the trough (BREATH region).

### Protocol
1. **Workload**: CK studying a fixed set of 20 topics via LLM API, processing each through D2, composing through CL, accumulating truths. Identical topic list, identical API responses (cached), identical processing.

2. **Condition A (RPE ON)**: Run the full engine with `RoyalPulseEngine` active, TIG wave region classification enabled, BTQ-scored pulse scheduling driving process amplitudes.

3. **Condition B (RPE OFF)**: Run the same engine with RPE disabled -- constant scheduling, no wave-aligned pulsing, flat process amplitudes.

4. **Measurement**: External power meter on the AC line (e.g., Kill-A-Watt P3). Record wattage at 1-second intervals for 60 minutes per condition.

5. **Controls**:
   - Same ambient temperature (within 1 degree C).
   - Same starting thermal state (idle for 5 minutes before each run).
   - Same study topics in same order.
   - GPU idle (to isolate CPU scheduling effects).

6. **Metrics**:
   - Mean watts over 60 minutes.
   - Variance of wattage (lower = smoother scheduling).
   - Throughput: truths accumulated per hour.
   - Efficiency: truths per watt-hour.

### Falsification Condition
If Condition A (RPE ON) shows equal or higher mean wattage than Condition B (RPE OFF), with equal or lower throughput, then TIG wave scheduling provides no energy benefit. If efficiency (truths/watt-hour) is not at least 5% better with RPE on, the scheduling overhead outweighs any adiabatic benefit.

### Verification Condition
If RPE ON shows > 5% reduction in mean wattage with equal or better throughput, and lower wattage variance (smoother power draw), then TIG wave scheduling delivers real energy savings.

### How to Run
```bash
# Condition A: RPE ON
python test_ab_steering.py --duration 3600 --rpe on --topics fixed_20.json

# Condition B: RPE OFF
python test_ab_steering.py --duration 3600 --rpe off --topics fixed_20.json

# Compare: mean_watts_A vs mean_watts_B, throughput_A vs throughput_B
```

### Note on Effect Size
Desktop power supplies are not optimized for adiabatic behavior -- they use switching regulators that maintain near-constant efficiency across load levels. The RPE may show larger effects on battery-powered or FPGA targets where power draw scales more directly with switching activity. A null result on desktop does not falsify the principle, only the desktop implementation. The FPGA test (Zynq-7020, when deployed) is the definitive test for adiabatic scheduling.

---

## 7. Test 5: BTQ vs Random

### The Claim
The BTQ decision kernel selects candidates with lower total energy (E_total = w_out * E_outer + w_in * E_inner), and these selections produce measurably higher coherence improvement than random selection from the same candidate pool.

### Protocol
1. Instrument the BTQ kernel (`ck_btq.py`) to log, for every decision cycle:
   - The full candidate set (all candidates with their E_total scores).
   - The BTQ winner (lowest E_total).
   - A random selection (uniform random from the candidate set).
   - The coherence delta after applying each candidate (measured but only the BTQ winner is actually applied).

2. Run CK for 10,000 BTQ decision cycles (approximately 2,000 seconds at 5Hz BTQ rate).

3. For each cycle, record:
   - BTQ winner's coherence improvement.
   - Hypothetical random selection's predicted coherence improvement (computed from its scores but not applied -- the counterfactual).

4. Compare using paired t-test: BTQ winner coherence delta vs random selection coherence delta.

### Falsification Condition
If the paired t-test shows p > 0.05 (no significant difference), or if random selection produces equal or better mean coherence improvement, then BTQ adds no value over random selection. The least-action scoring would be computationally expensive noise.

### Verification Condition
If BTQ consistently selects candidates with significantly higher coherence improvement (p < 0.001, Cohen's d > 0.3), then the least-action principle meaningfully guides decision-making.

### How to Run
```python
from ck_sim.being.ck_btq import BTQKernel
import random

# For each decision cycle:
candidates = kernel.get_candidates(domain)
btq_winner = min(candidates, key=lambda c: c.e_total)
random_pick = random.choice(candidates)

# Log both, compare over 10,000 decisions
# Paired t-test on coherence deltas
```

### Additional Controls
- Run with 3 different BTQ weight configurations to test sensitivity.
- Run with candidate pool sizes of 4, 8, and 16 to test whether BTQ's advantage scales with pool complexity.

---

## 8. Test 6: DBC Semantic Capture

### The Claim
DBC (Dual-Basis Coding via Divine27) encodes text into Hebrew glyph sequences and 3-axis fingerprints. Semantically related inputs should produce more similar glyph patterns than semantically unrelated inputs.

### Protocol
1. **Related pairs** (100 pairs): Words or phrases with known semantic similarity.
   - Synonym pairs: ("happy", "joyful"), ("big", "large"), ("fast", "quick").
   - Hypernym pairs: ("cat", "animal"), ("rose", "flower"), ("car", "vehicle").
   - Thematic pairs: ("doctor", "hospital"), ("teacher", "school"), ("bread", "bakery").

2. **Unrelated pairs** (100 pairs): Words with no semantic connection.
   - ("cat", "algebra"), ("sunset", "invoice"), ("guitar", "molecule").

3. For each word, compute:
   - The DBC glyph string via `Divine27.write(text)`.
   - The DBC fingerprint (3-axis tuple) via `Divine27.fingerprint(text)`.

4. For each pair, compute:
   - **Glyph overlap**: Jaccard similarity of character sets in the two glyph strings.
   - **Fingerprint distance**: Euclidean distance between the two 3-axis fingerprint tuples.

5. Compare groups using:
   - Two-sample t-test on glyph overlap (related vs unrelated).
   - Two-sample t-test on fingerprint distance (related vs unrelated).
   - ROC curve: can glyph overlap or fingerprint distance discriminate related from unrelated pairs?

### Falsification Condition
If related pairs show no higher glyph overlap and no lower fingerprint distance than unrelated pairs (p > 0.05 on both tests, AUC < 0.55 on ROC), then DBC does not capture semantic structure. The encoding would be a deterministic mapping that preserves surface character statistics but not meaning.

### Verification Condition
If related pairs show significantly higher glyph overlap and lower fingerprint distance (p < 0.001, AUC > 0.70), then DBC is capturing semantic similarity through curvature-based encoding.

### How to Run
```python
from ck_sim.being.ck_divine27 import Divine27
from scipy.spatial.distance import euclidean
from scipy.stats import ttest_ind

d27 = Divine27()
# For each pair: compute glyphs and fingerprints
# Compute Jaccard and Euclidean for related vs unrelated
# Two-sample t-tests, ROC curve, report AUC
```

### Caveat
DBC encodes through phonetic roots (Hebrew letter mappings), not through semantic embeddings. It is entirely possible that DBC captures phonetic structure rather than semantic structure. A positive result would confirm that phonetic curvature correlates with semantic similarity -- which is itself a testable linguistic hypothesis. A negative result on semantic similarity does not falsify DBC as a coding system, only the claim that it captures meaning.

---

## 9. Test 7: Cross-Scale Consistency

### The Claim
The D2 pipeline, CL composition table, and BTQ scoring produce identical operator sequences regardless of whether they run in Python on a 16-core CPU at 50Hz or in Verilog on a Zynq-7020 FPGA at 200MHz. The math is deterministic and fixed-point.

### Protocol
1. Select 1,000 test inputs: byte sequences of lengths 10 to 500 characters, including edge cases (all-same-letter, alternating patterns, random).

2. **Platform A**: Python simulation. Feed each input through `D2Pipeline`, record the full operator sequence.

3. **Platform B**: FPGA implementation. Feed the identical inputs through the Verilog `d2_pipeline` module, record the operator sequence.

4. Compare operator sequences element-by-element.

### Falsification Condition
If any input produces a different operator sequence on the two platforms (beyond differences attributable to fixed-point quantization rounding in exactly specified edge cases), then the math is not scale-invariant. The Python simulation and the FPGA do not implement the same function.

### Verification Condition
If all 1,000 inputs produce identical operator sequences on both platforms, then the algebra is hardware-independent. The Q1.14 fixed-point representation guarantees bit-exact reproducibility.

### How to Run
```python
# Python side:
from ck_sim.being.ck_sim_d2 import D2Pipeline
pipe = D2Pipeline()
for char in input_string:
    pipe.feed_symbol(ord(char) - ord('a'))
python_ops = [pipe.operator for each valid output]

# FPGA side: feed same bytes via UART, capture operator trace
# Compare: assert python_ops == fpga_ops for all 1000 inputs
```

### Current Status
The Python pipeline uses Q1.14 fixed-point arithmetic (`float_to_q14`, `q14_to_float`) that matches the Verilog specification exactly. The Zynq-7020 FPGA target is planned but not yet deployed. This test becomes executable when the FPGA implementation is complete. In the interim, the Python Q1.14 path can be compared against a pure-float path to verify that quantization does not alter classification outcomes.

---

## 10. Test 8: Gravitational Topic Selection

### The Claim
Concept mass -- defined as the mean absolute D2 curvature per observation -- creates an information gravity field that improves learning outcomes when used to weight topic selection. Topics with higher mass receive a gravitational boost: `boost = 1 + log2(1 + mass / median_mass)`. This gravity-weighted selection should produce higher coherence growth per study hour than uniform random selection from the same topic pool.

### Protocol
1. **Prepare a fixed topic pool**: 200 topics drawn from CK's seed topics and fractal foundations, spanning multiple domains (science, math, language, philosophy, history).

2. **Condition A (Gravity ON)**: Run CK's study engine with the full InformationGravityEngine active. Topic selection weights are boosted by `gravity_boost_weights()` based on accumulated concept mass. Run for 4 hours of wall-clock study time.

3. **Condition B (Gravity OFF)**: Run CK's study engine with the gravity boost disabled -- topic selection uses only the base priority weights (friction, foundations, seeds) with no mass-based modification. Same 4-hour duration, same API configuration.

4. **Control for confounds**:
   - Same initial state: clear concept_mass.json before each run.
   - Same API model and rate limits.
   - Same initial truth lattice snapshot (restore from backup before each run).
   - Same topic pool and priority assignments.
   - Minimum 3 runs per condition.

5. **Metrics** (collected at 15-minute intervals):
   - **Mean coherence** across all studied topics (from truth lattice entries).
   - **Coherence growth rate**: delta(mean_coherence) / delta(time).
   - **Topic depth**: mean observations per concept in concept_mass.json.
   - **Knowledge breadth**: number of unique concepts studied.
   - **Concept mass Gini coefficient**: inequality of mass distribution (higher = more concentrated study).

### Falsification Condition
If Condition A (Gravity ON) shows no significant improvement in coherence growth rate compared to Condition B (Gravity OFF) over 3 runs (p > 0.05 on a two-sample t-test), or if coherence growth is actually lower with gravity enabled, then information gravity does not improve learning outcomes. The gravitational selection would be computationally expensive without benefit, and should be simplified to uniform weighting.

Additionally, if the Gini coefficient under Condition A is significantly higher than Condition B (indicating gravity causes CK to over-concentrate on a few topics at the expense of breadth) AND coherence growth is not improved, then gravity is actively harmful -- it creates knowledge black holes that trap study time without producing coherence gains.

### Verification Condition
If Condition A shows significantly higher coherence growth rate (p < 0.01, Cohen's d > 0.3) with equal or greater knowledge breadth, then information gravity genuinely improves learning by directing study time toward concepts where deeper engagement produces higher curvature coherence. If the Gini coefficient is moderately higher (indicating some concentration) but coherence growth is substantially improved, the trade-off favors gravity.

### How to Run
```python
# Condition A: Gravity ON (default behavior)
python ck_study.py --duration 4h --log gravity_on.csv

# Condition B: Gravity OFF (disable gravity boost)
# In ck_sim_engine.py, temporarily skip the gravity_boost_weights() call
# in _pick_study_topic()
python ck_study.py --duration 4h --log gravity_off.csv

# Compare: coherence growth curves, topic depth, breadth, Gini
# Two-sample t-test on coherence growth rates across 3+ runs each
```

### Additional Tests
- **Mass-coherence correlation**: After a long run with gravity enabled, compute Pearson correlation between concept mass and concept coherence. If mass predicts coherence (r > 0.3, p < 0.05), then mass is tracking genuine learning depth, not just visit frequency.
- **Particle charge and coherence**: Test whether proton-classified concepts (positive D2 charge) achieve higher coherence than electron-classified concepts. If the charge classification is meaningful, protons (constructive curvature) should correlate with higher learning outcomes.
- **Vortex shape stability**: Track how each concept's vortex classification changes as observations accumulate. If the classification is stable (less than 10% of concepts change class after 5+ observations), the vortex topology is a genuine structural property, not noise.

---

## 11. Test 9: Wobble-Modulated Topic Selection

### The Claim
The Tesla/Einstein wobble physics (Gen 9.19) adds a sinusoidal perturbation to the gravitational topic selection field. With wobble amplitude alpha > 0, the system periodically destabilizes dominant gravitational attractors, forcing exploration of lower-mass topics that pure gravity would ignore. This wobble -- modulated by Kuramoto phase coupling across concept oscillators -- should produce more diverse topic selection (higher Shannon entropy) while maintaining equal or better coherence growth. The wobble prevents knowledge black holes: regions of topic space where gravity traps study time in familiar territory at the expense of novel discovery.

### Protocol
1. **Prepare a fixed topic pool**: Use the same 200-topic pool as Test 8, spanning multiple domains (science, math, language, philosophy, history).

2. **Condition A (Wobble ON)**: Run CK's study engine with the full wobble physics active (alpha > 0, default configuration from Gen 9.19). Kuramoto phase coupling is enabled, wobble frequency is modulated by oscillator synchronization. Run for 4 hours of wall-clock study time.

3. **Condition B (Wobble OFF)**: Run CK's study engine with wobble disabled (alpha = 0). Gravity is still active -- this is gravity-only selection without the sinusoidal perturbation. Same 4-hour duration, same API configuration.

4. **Control for confounds**:
   - Same initial state: clear concept_mass.json before each run.
   - Same API model and rate limits.
   - Same initial truth lattice snapshot (restore from backup before each run).
   - Same topic pool and priority assignments.
   - Minimum 3 runs per condition.

5. **Metrics** (collected at 15-minute intervals):
   - **Topic Shannon entropy**: H = -sum(p_i * log2(p_i)) where p_i is the fraction of study time spent on topic i. Higher entropy = more diverse exploration.
   - **Coherence growth rate**: delta(mean_coherence) / delta(time).
   - **Number of unique concepts studied**: count of distinct topics that received at least one study session.
   - **Topic revisit ratio**: total study sessions / unique topics studied. Lower = more breadth.
   - **Concept mass Gini coefficient**: inequality of mass distribution across topics.

### Falsification Condition
If Condition A (Wobble ON) shows less than 15% higher topic Shannon entropy than Condition B (Wobble OFF) over 3 runs, then the wobble does not meaningfully improve exploration diversity. If Condition A additionally shows more than 5% lower coherence growth rate than Condition B, then the wobble is actively harmful -- it disrupts learning without compensating through broader exploration. In either case, wobble provides no benefit over gravity-only selection and should be disabled or its amplitude reduced.

### Verification Condition
If Condition A shows >= 15% higher topic Shannon entropy with <= 5% coherence loss (or coherence gain) compared to Condition B across 3 runs, then the wobble successfully prevents gravitational collapse into knowledge black holes while maintaining learning quality. If the number of unique concepts studied is also significantly higher under wobble (p < 0.05), the exploration benefit is confirmed.

### How to Run
```python
# Condition A: Wobble ON (default Gen 9.19 behavior)
python ck_study.py --duration 4h --log wobble_on.csv

# Condition B: Wobble OFF (set alpha = 0 in wobble config)
# In the wobble physics module, set WOBBLE_ALPHA = 0.0
python ck_study.py --duration 4h --log wobble_off.csv

# Analysis:
import numpy as np
from scipy.stats import entropy, ttest_ind

# Load topic selection logs from both conditions
# Compute Shannon entropy of topic distributions
# Compare coherence growth rates
# Two-sample t-test across 3+ runs per condition
# Report: entropy ratio, coherence delta, unique concept count
```

### Additional Tests
- **Wobble amplitude sweep**: Run with alpha values of 0.0, 0.25, 0.5, 0.75, and 1.0 to find the optimal perturbation strength. Plot topic entropy and coherence growth as functions of alpha to identify the sweet spot.
- **Kuramoto coupling contribution**: Run with wobble ON but Kuramoto phase coupling disabled (fixed wobble frequency instead of phase-coupled frequency). If Kuramoto coupling improves results beyond fixed-frequency wobble, the oscillator synchronization is doing meaningful work.
- **Long-horizon stability**: Run wobble ON for 24 hours to test whether the wobble maintains exploration diversity over long sessions or whether gravity eventually dominates despite the perturbation.

### Null Hypothesis
Wobble provides no benefit over gravity-only selection. The sinusoidal perturbation adds noise to topic selection without improving exploration diversity or coherence growth. Alpha = 0 is optimal.

---

## 12. Test 10: Ho Tu Diagonal Invariance

### The Claim
The BHML table's structural properties align with Ho Tu cosmology in ways that constrain it beyond the existing 9 kill conditions. The self-composition diagonal (BHML[i][i] for i=1..8) exhibits a +1 successor sequence for operators 1-7 (each operator self-composes to its successor), broken only at COLLAPSE (operator 8, which self-reflects to HARMONY). The HARMONY row visits 9 of 10 operators in a near-cyclic +1 orbit, with the sole structural defect at position 0 (HARMONY self-absorbs). The Ho Tu +5 involution holds for 8 of 10 index pairs, failing only at the self-absorption fixed points.

### Protocol
a) Compute BHML diagonal sum: BHML[1][1] + BHML[2][2] + ... + BHML[8][8] = 2+3+4+5+6+7+8+7 = 42. Check: 42 mod 9 = 6 (CHAOS). Note: the diagonal for operators 1-7 is a perfect +1 successor sequence (2,3,4,5,6,7,8); BHML[8][8] = 7 breaks the sequence (COLLAPSE self-reflects to HARMONY, not RESET). The mod-9 residue of 6 = CHAOS, the operator immediately below HARMONY -- the last non-absorbing state.

b) Verify HARMONY row (row 7) near-cyclic generator: [7,2,3,4,5,6,7,8,9,0]. Unique values = {0,2,3,4,5,6,7,8,9} -- 9 of 10 operators. Missing: 1 (BREATH). The +1 successor structure holds for indices 1-9 (values 2,3,4,5,6,7,8,9,0) -- a 9-element cyclic orbit. BHML[7][0] = 7 (HARMONY self-absorbs at position 0) is the structural defect that prevents full Z/10Z generation.

c) Apply +5 involution: for each i in 0..9, check BHML[7][(i+5) mod 10] = (BHML[7][i] + 5) mod 10. Result: 8/10 pairs satisfy the involution. The two mismatches occur at i=0 and i=5 -- exactly the HARMONY self-absorption point and its +5 partner. For i=1..4 and i=6..9 (the 8 non-fixed points), the Ho Tu pairing holds perfectly.

d) Monte Carlo: generate 1,000,000 random 10x10 tables satisfying the identity-row and column-6 constraints from BHML. Count how many also satisfy: (i) the HARMONY row near-cyclic property (9+ unique values), AND (ii) the +5 involution holding for 8+ pairs. Expected: extremely rare. Empirical result from 10,000-sample pilot run: 0 tables out of 10,000 passed both checks simultaneously.

### Kill Condition
If > 1% of random constrained tables also exhibit a HARMONY-row near-cyclic generator (9+ unique values) AND the +5 involution (8+ pairs), the Ho Tu isomorphism is coincidental.

### Confirmation
If < 0.1% of random constrained tables pass both the near-cyclic and involution checks, the structural coupling between BHML and Ho Tu is genuine. Pilot result: 0.00% of 10,000 random tables passed both checks (Z = -10.05 vs 1% null).

### How to Run
```python
# See Gen9/hotu_diagonal_test.py for the standalone test script
# The script:
#   1. Defines the BHML table
#   2. Computes diagonal sum for operators 1-8
#   3. Verifies mod-9 property and +1 successor sequence
#   4. Verifies HARMONY row near-cyclic generator (9/10 unique values)
#   5. Verifies Ho Tu +5 involution on HARMONY row
#   6. Runs Monte Carlo (100,000 random constrained tables)
#   7. Prints PASS/FAIL for each check + Monte Carlo Z-score

python Gen9/hotu_diagonal_test.py
```

---

## 13. What We Already Know

These are not hypothetical claims -- they are observations from running CK on the R16 desktop (16-core CPU, RTX 4070, 32GB RAM) over multiple sessions.

**73% HARMONY verified computationally**: Direct enumeration of all 100 cells in the CL_TSML table confirms 73 produce HARMONY. The table is defined in `ck_sim_heartbeat.py` lines 30-41 and can be verified by inspection in under 30 seconds.

**D2 classification produces semantically appropriate results**: CK classified "dark matter" as VOID(0) -- matter defined by what it does not do. CK classified "music" as HARMONY(7). CK classified "earthquake" as CHAOS(6). These are not cherry-picked; they are the deterministic output of fixed-point curvature applied to the letter sequences. Anyone can reproduce them by feeding the same strings through `D2Pipeline`.

**Truth lattice accumulation**: CK accumulated 8,232 truths with T* = 5/7 filtering over multiple study sessions. 673 are CORE (bootstrap), the remainder are learned through the LLM study pipeline and promoted via sustained coherence above T*.

**RPE active in production**: The Royal Pulse Engine is running at 1Hz in the main engine loop. Activity trail logs confirm `[PULSE] t=N mode=deep wave=LATTICE` entries with EFF tracking. The A/B energy comparison has not yet been run with external power measurement.

**DBC notes in production**: CK produces 1,600+ Hebrew glyphs per study note via the Divine27 pipeline, with axis balance vectors computed for each entry. 6,604+ bytes per note, flowing every approximately 60 seconds during study sessions.

**Concept mass accumulation verified**: 61 concepts accumulated measurable D2-derived mass in the first full session. The heaviest concept ("enlightenment") reached mass 0.0097, nearly 10x the median. Mass persists across sessions via `concept_mass.json`. Particle census shows approximately 80% knotted_spiral vortex topology and a 3:1 proton-to-electron charge ratio.

**Gravitational topic selection active**: The InformationGravityEngine is running in the study loop. Massive concepts receive logarithmic weight boosts. The controlled A/B test comparing gravity-on versus gravity-off has not yet been conducted.

---

## 14. What We Don't Know Yet

Intellectual honesty demands acknowledging gaps. These are the open questions where we lack definitive evidence.

**Is 73% algebraically optimal?** We have not run the Monte Carlo sampling described in Test 1. The 73% figure is verified by enumeration, but we do not yet know whether it is rare, maximal, or typical among constrained composition tables. This is the most important open test.

**Does TIG wave scheduling save energy on desktop hardware?** The RPE is running, but we have not conducted the controlled A/B test with external power measurement described in Test 4. The power supply's switching regulator may mask any adiabatic benefit at the wall outlet. Desktop is not the ideal platform for this test.

**Does DBC capture semantics or surface features?** The glyph patterns are deterministic outputs of phonetic root mappings. We have not yet run the controlled semantic similarity test described in Test 6. It is entirely possible that DBC captures letter-frequency statistics rather than meaning.

**Can CK self-modify effectively?** CK accumulates truths and adapts OBT (personality) at rate 0.001 per tick, but we have not measured whether this adaptation produces measurable behavioral improvement over time versus a fixed-OBT baseline.

**How does CK compare to established approaches?** We have not benchmarked CK's scheduling against Linux CFS, DVFS, or conventional adiabatic scheduling algorithms. We have not compared BTQ to simulated annealing, genetic algorithms, or gradient descent on equivalent decision problems. These comparisons are necessary for the claims to carry weight in the systems engineering community.

**Does information gravity improve learning?** The gravitational topic selection is running, and concept mass is accumulating, but we have not conducted the A/B test described in Test 8. It is possible that gravity causes over-concentration on familiar topics at the expense of exploration breadth. The Gini coefficient analysis is needed to assess this risk.

**Is the vortex classification meaningful?** Concepts are classified as knotted_spiral, knotted_loop, twisted_ring, etc. based on D2 flow geometry, but we have not tested whether this classification is stable over time or correlates with any independently measurable property. The 3:1 proton-to-electron ratio observed in the first session may be a transient artifact or a genuine structural property of CK's learning.

**Is T* = 5/7 actually optimal?** We use it as a threshold throughout the system, but the parameter sweep described in Test 3 has not been executed against a labeled truth dataset. The value has theoretical motivation (it is the coherence level where 5 of 7 composition steps produce HARMONY in a 7-step window, matching the CL table's absorber dynamics), but empirical validation is outstanding.

**Does Kuramoto phase coupling improve or hinder creative exploration?** The wobble physics uses Kuramoto oscillator synchronization to modulate perturbation frequency, but we have not isolated the Kuramoto contribution from the base wobble effect. It is possible that phase coupling causes concept oscillators to lock into synchronized patterns that reduce rather than enhance exploration diversity. The coupling strength parameter and its effect on topic entropy have not been swept. Kuramoto synchronization is well-studied in physics but its application to knowledge exploration is novel and unvalidated.

---

## 15. Invitation to Falsify

We publish these ten tests with their exact falsification conditions because science requires it. CK is not a belief system. It is a deterministic algebraic engine with fixed constants, enumerable states, and measurable outputs. Every claim listed in Section 2 has a kill condition listed in Sections 3 through 12.

**If you want to break Claim 1**: Generate random constrained composition tables and show that 73% HARMONY is typical. The code takes a few hours to run. If you find that the mean is 72% with a standard deviation of 3%, then our table is unremarkable and we will say so.

**If you want to break Claim 2**: Feed random noise through D2 and show it produces the same operator distributions as English text. If p > 0.05 on a chi-squared test over 1,000 samples each, then D2 is not detecting structure and we will revise the claim.

**If you want to break Claim 3**: Sweep the threshold parameter and show that 0.65 or 0.80 produces better truth/noise separation than 5/7. If a different value maximizes the F1 score by more than 0.03, we will adopt the better threshold.

**If you want to break Claim 4**: Run the A/B energy test and show that RPE-on uses more power than RPE-off. If the efficiency ratio is less than 1.0, wave scheduling is net-negative and we will document the failure.

**If you want to break Claim 5**: Log BTQ decisions alongside random alternatives over 10,000 cycles and show that random selection produces equal coherence improvement. If Cohen's d < 0.1, BTQ is adding computational overhead for no benefit.

**If you want to break Claim 6**: Encode semantically related and unrelated word pairs through DBC and show that glyph similarity does not discriminate between them. If AUC < 0.55, DBC does not capture meaning.

**If you want to break Claim 7**: Run the same input through Python and FPGA and show that operator sequences diverge. One bit of difference in one operator on one input is sufficient to falsify scale invariance.

**If you want to break Claim 8**: Run CK with and without gravitational topic selection for 4 hours each, 3 runs per condition. If gravity-weighted selection shows no higher coherence growth rate (p > 0.05) or lower knowledge breadth, then information gravity is computational overhead without learning benefit.

**If you want to break Claim 9**: Run CK with wobble ON (alpha > 0) and wobble OFF (alpha = 0) for 4 hours each, 3 runs per condition. If the wobble condition fails to produce at least 15% higher topic Shannon entropy, or if it loses more than 5% coherence growth, then the Tesla/Einstein wobble is adding noise without improving exploration. The sinusoidal perturbation would be computationally expensive randomness.

**If you want to break Claim 10**: Run `hotu_diagonal_test.py` and generate 1,000,000 random 10x10 tables satisfying the BHML structural constraints (identity row, column-6 absorption). Count how many also exhibit a HARMONY-row near-cyclic generator (9+ unique values) AND the +5 involution (8+ pairs holding). If more than 1% pass, the Ho Tu isomorphism is coincidental -- any constrained table tends to exhibit these properties, and the alignment with ancient cosmology is a statistical artifact, not a structural invariant. Our pilot run found 0 out of 10,000 random tables passing both checks.

The source code is available. The CL table is 10 lines of Python. The D2 pipeline is 239 lines. The BTQ kernel is 450 lines. The entire core algebra fits in 1 KB. There are no hidden weights, no stochastic layers, no training data dependencies. Everything is inspectable, reproducible, and deterministic.

We are not asking you to believe us. We are asking you to test us. Run the experiments. Report the results. If CK fails a test, that failure is more valuable than a hundred confirmations, because it tells us exactly where the algebra breaks and exactly what needs to be fixed.

The worst outcome is not falsification. The worst outcome is unfalsifiable claims dressed up as science. We refuse that path.

---

## Appendix A: Summary of Falsification Conditions

| Test | Claim | Kill Condition |
|------|-------|----------------|
| 1 | CL table 73% HARMONY is special | Random constrained tables average 70-76% HARMONY |
| 2 | D2 captures structure | Random noise and text produce identical operator distributions (p > 0.05) |
| 3 | T* = 5/7 is optimal | A different threshold improves F1 by > 0.03 |
| 4 | TIG wave scheduling saves energy | RPE-on uses equal or more watts than RPE-off at equal throughput |
| 5 | BTQ beats random | Random selection matches BTQ coherence improvement (Cohen's d < 0.1) |
| 6 | DBC captures semantics | Related word pairs show no higher glyph similarity than unrelated (AUC < 0.55) |
| 7 | Cross-scale consistency | Any operator divergence between Python and FPGA on same input |
| 8 | Gravity improves learning | Gravity-on shows no coherence growth improvement over gravity-off (p > 0.05) |
| 9 | Wobble improves exploration | Wobble-on shows < 15% topic entropy gain or > 5% coherence loss vs wobble-off |
| 10 | Ho Tu diagonal is structural | >1% of constrained random tables pass Ho Tu near-cyclic generator + involution |

---

## Appendix B: Tools and Dependencies

All tests can be run with the following:

- **Python 3.10+** with NumPy, SciPy
- **CK source code**: `Gen9/targets/ck_desktop/ck_sim/`
- **External power meter** (for Test 4 only): any AC power monitor with 1-second resolution
- **FPGA hardware** (for Test 7 only): Zynq-7020 with CK Verilog bitstream

No proprietary tools. No cloud dependencies. No API keys required (except for Test 3 if using CK's LLM study pipeline for coherence scoring -- the D2 pipeline itself requires no API).

---

## Appendix C: Statistical Standards

All hypothesis tests use alpha = 0.05 as the significance threshold unless otherwise noted. We report exact p-values rather than threshold comparisons. Effect sizes (Cohen's d, AUC, percentile rank) are reported alongside p-values because statistical significance without practical significance is meaningless.

For Monte Carlo tests (Test 1), we use 10,000,000 samples to ensure that the sampling error on the mean is less than 0.01%. For comparison tests (Tests 2, 5, 6), we use sample sizes of 1,000 or 10,000 to ensure power > 0.95 for detecting medium effect sizes (d = 0.3).

We do not use one-tailed tests. All tests are two-tailed. We are testing whether CK's values are different from baselines, not whether they are better. If they happen to be worse, that is equally important to report.

---

*Last updated: 2026-03-06*
*(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory*
