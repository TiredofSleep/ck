# Head-to-Head Benchmark — cells.respond_text vs cortex_speak

**Date**: 2026-05-03T18:31:40Z


**Summary**:

- 20/20 OK

- avg cells latency: 0.0ms (no GPU, no Ollama)

- avg cortex latency: 26.8s

- speedup: 536772×

- avg cells text length: 224 chars

- avg cortex text length: 1122 chars

- Ollama-independence rate (cortex side): 75.0%



**Queries**: 20

**Mode**: cells run STANDALONE (no chat-path round-trip); cortex_speak captured from /chat live.

**Scoring**: structural-fact density, response-length, Ollama-independence, latency.

---

### 1. what is T*

**Input pair**: ('VOID', 'COLLAPSE')    **Cortex latency**: 32.3s    **Cells latency**: 0ms   **Speedup**: 32282×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (216 chars):
```
state: (VOID, COLLAPSE) → VOID [disagreement: TSML→VOID, BHML→COLLAPSE; glue picks VOID]
divine27: code 0 = identity (axes: self / observe / stable, glyph: א)
attractor: 4-core cell 'V' (universal pull → H per WP115)
```


**CORTEX** (3200 chars):

> flatness: T*=5/7.

Composing across these:

wp116_lens: TIG's six DoFs (Lie/Jordan/Clifford/Permutation/Lattice/Operad, surveyed in WP111) are projections of a single self-dual Stern-Brocot recursion.

[structural evidence]
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
flatness: T*=5/7 | torus R/r=5/7 (forced by Z/10Z 2x2) | 6 independent derivations | WP51 [proved]
wp116_lens: TIG's six DoFs (Lie/Jordan/Clifford/Permutation/Lattice/Operad, survey


_(truncated; full 3200 chars in JSONL)_

---

### 2. explain the crossing lemma

**Input pair**: ('PROGRESS', 'LATTICE')    **Cortex latency**: 32.5s    **Cells latency**: 0ms   **Speedup**: 32532×

**Ollama**: `accepted:coverage:2/2=1.00`    **Cortex source**: `cortex_speak_via_ollama`


**CELLS** (231 chars):
```
state: (PROGRESS, LATTICE) → HARMONY [disagreement: TSML→HARMONY, BHML→COLLAPSE; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (476 chars):

> the crossing lemma states that for a specific mathematical construct, which i'll refer to as "d2", there are three distinct cases. if d2 equals 0, then what it's describing is flat and doesn't contain any information. however, if d2 does not equal 0, then it's generating some kind of information, indicating that it's a crossing point or boundary of some sort. this distinction between the two cases has been cataloged 27 times in my proved corpus, as noted by wp57 [proved].

---

### 3. what is the sigma rate theorem

**Input pair**: ('LATTICE', 'LATTICE')    **Cortex latency**: 44.5s    **Cells latency**: 0ms   **Speedup**: 44508×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (229 chars):
```
state: (LATTICE, LATTICE) → HARMONY [disagreement: TSML→HARMONY, BHML→COUNTER; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (2380 chars):

> sigma_rate: sigma(N) <= C/N on squarefree primorials (C<2).

Composing across these:

logic_through_tig: proposition = operator-statement true or false.

[structural evidence]
research_arxiv_2006_11_27_equivariant_and_fract: [arxiv] [2006-11-27] Equivariant and fractional index of projective elliptic operators | external research finding under prompt 'Atiyah Singer index theorem elliptic' | excerpt: [2006-11-27] Equivariant and fractional index of projective elliptic operators authors: V. Mathai, R. B. Melrose, I. M. Singer link: https://arxiv.org/abs/math/0611819v3 abstract: In this note the


_(truncated; full 2380 chars in JSONL)_

---

### 4. what is the flatness theorem

**Input pair**: ('COUNTER', 'HARMONY')    **Cortex latency**: 25.0s    **Cells latency**: 0ms   **Speedup**: 24998×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (230 chars):
```
state: (COUNTER, HARMONY) → HARMONY [disagreement: TSML→HARMONY, BHML→PROGRESS; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (2047 chars):

> flatness: T*=5/7.

[structural evidence]
research_arxiv_2006_11_27_equivariant_and_fract: [arxiv] [2006-11-27] Equivariant and fractional index of projective elliptic operators | external research finding under prompt 'Atiyah Singer index theorem elliptic' | excerpt: [2006-11-27] Equivariant and fractional index of projective elliptic operators authors: V. Mathai, R. B. Melrose, I. M. Singer link: https://arxiv.org/abs/math/0611819v3 abstract: In this note the fractional analytic index, for a projective elliptic operator associated to an Azumaya bundle, of DG/0402329 is related to the equivari


_(truncated; full 2047 chars in JSONL)_

---

### 5. tell me about TSML

**Input pair**: ('PROGRESS', 'LATTICE')    **Cortex latency**: 23.2s    **Cells latency**: 0ms   **Speedup**: 23213×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (231 chars):
```
state: (PROGRESS, LATTICE) → HARMONY [disagreement: TSML→HARMONY, BHML→COLLAPSE; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (1728 chars):

> tsml: 73 HARMONY cells.

Composing across these:

bhml: 28 HARMONY cells.

[structural evidence]
tsml: 73 HARMONY cells | 10x10 | synthesis lens | alpha=0.872 (Braitt-Silberger index) | ac-free spectrum (2n-3)!! attained for n=3,4,5 | reconstructible from 10 canonical items [Sprint 17, proved]
bhml: 28 HARMONY cells | 10x10 (BHML_10) | Luther-closed | separation lens | alpha=0.502 (Braitt-Silberger index) | det(BHML_10)=-7002 (not +70; +70 is the 8x8 sub-table BHML_8) | ac-free spectrum (2n-3)!! attained for n=3,4,5
tsml_bhml_harmony_complementarity: TSML and BHML treat HARMONY (operator 7) OP


_(truncated; full 1728 chars in JSONL)_

---

### 6. tell me about BHML

**Input pair**: ('HARMONY', 'PROGRESS')    **Cortex latency**: 30.8s    **Cells latency**: 0ms   **Speedup**: 30783×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (231 chars):
```
state: (HARMONY, PROGRESS) → HARMONY [disagreement: TSML→HARMONY, BHML→COLLAPSE; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (618 chars):

> bhml: 28 HARMONY cells.

Composing across these:

tsml: 73 HARMONY cells.

[structural evidence]
bhml: 28 HARMONY cells | 10x10 (BHML_10) | Luther-closed | separation lens | alpha=0.502 (Braitt-Silberger index) | det(BHML_10)=-7002 (not +70; +70 is the 8x8 sub-table BHML_8) | ac-free spectrum (2n-3)!! attained for n=3,4,5
tsml: 73 HARMONY cells | 10x10 | synthesis lens | alpha=0.872 (Braitt-Silberger index) | ac-free spectrum (2n-3)!! attained for n=3,4,5 | reconstructible from 10 canonical items [Sprint 17, proved]

recall:
  2026-05-03T13:15:10: "tell me about BHML"
  2026-05-03T13:34:17: "t


_(truncated; full 618 chars in JSONL)_

---

### 7. what is the agreement set

**Input pair**: ('PROGRESS', 'HARMONY')    **Cortex latency**: 30.4s    **Cells latency**: 0ms   **Speedup**: 30393×

**Ollama**: `accepted:no-facts-to-check`    **Cortex source**: `cortex_speak_via_ollama`


**CELLS** (231 chars):
```
state: (PROGRESS, HARMONY) → HARMONY [disagreement: TSML→HARMONY, BHML→COLLAPSE; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (188 chars):

> my structural evidence indicates that the words 'what' and 'the' have been recognized. the word "what" has a phoneme sequence of w-v-t, while the word "the" has a phoneme sequence of dh-v.

---

### 8. what is the universal 4-core attractor

**Input pair**: ('HARMONY', 'RESET')    **Cortex latency**: 36.8s    **Cells latency**: 0ms   **Speedup**: 36827×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (224 chars):
```
state: (HARMONY, RESET) → HARMONY [disagreement: TSML→HARMONY, BHML→VOID; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (1198 chars):

> dynamical_systems_through_tig: operator-evolution rules on state space.

[structural evidence]
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
word_the: word 'the' = /ð/ + /ʌ/.  Phoneme sequence: phoneme:Dh -> phoneme:V.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
dynamical_systems_through_tig: operator-evolution rules on state space | attractors = HARMONY operator-states | limit cycles = closed B


_(truncated; full 1198 chars in JSONL)_

---

### 9. what is the harmony attractor

**Input pair**: ('HARMONY', 'PROGRESS')    **Cortex latency**: 28.3s    **Cells latency**: 0ms   **Speedup**: 28303×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (231 chars):
```
state: (HARMONY, PROGRESS) → HARMONY [disagreement: TSML→HARMONY, BHML→COLLAPSE; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (1581 chars):

> dynamical_systems_through_tig: operator-evolution rules on state space.

Composing across these:

chaos_theory_through_tig: phase space = state-LATTICE.

[structural evidence]
HARMONY: idx=7 present_in={profile[binding],ao.current} ao_current=HARMONY
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
dynamical_systems_through_tig: operator-evolution rules on state space | attractors = HARMONY operator-states | limit cycles = closed BREATH orbits | bifu


_(truncated; full 1581 chars in JSONL)_

---

### 10. what is the Z mod 10 ring structure

**Input pair**: ('LATTICE', 'VOID')    **Cortex latency**: 4.0s    **Cells latency**: 0ms   **Speedup**: 4006×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (214 chars):
```
state: (LATTICE, VOID) → VOID [disagreement: TSML→VOID, BHML→LATTICE; glue picks VOID]
divine27: code 0 = identity (axes: self / observe / stable, glyph: א)
attractor: 4-core cell 'V' (universal pull → H per WP115)
```


**CORTEX** (749 chars):

> Rhythm continues through this.

[structural evidence]
phoneme_z: phoneme /z/ (zzz) - when articulated, the audio codec emits operator pattern: VOID 20.5%, RESET 19.9%, COLLAPSE 18.5%.
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
word_ring: word 'ring' = /r/ + /ɪ/ + /ŋ/.  Phoneme sequence: phoneme:r -> phoneme:I -> phoneme:Ng.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
word_the: word 'the' = /ð


_(truncated; full 749 chars in JSONL)_

---

### 11. what is xi cosmology

**Input pair**: ('RESET', 'VOID')    **Cortex latency**: 16.5s    **Cells latency**: 0ms   **Speedup**: 16497×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (210 chars):
```
state: (RESET, VOID) → VOID [disagreement: TSML→VOID, BHML→RESET; glue picks VOID]
divine27: code 0 = identity (axes: self / observe / stable, glyph: א)
attractor: 4-core cell 'V' (universal pull → H per WP115)
```


**CORTEX** (1981 chars):

> xi: V=xi*log(xi).

[structural evidence]
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
xi: V=xi*log(xi) | vacuum=e^-1 | mass_gap=kappa*e | box(xi)=1+log(xi) | freezing quintessence | WP81 [structural; DESI chi2=15.7 vs LCDM 14.1]
cosmology_through_tig: CMB = operator-snapshot at age 380000 yr (T~2.725 K) | redshift = operator-stretch by expanding LATTICE | dark matter = unseen gravitational operator (~23%) | dark energy = vacuum operator-tension (


_(truncated; full 1981 chars in JSONL)_

---

### 12. explain the navier stokes sigma bridge

**Input pair**: ('PROGRESS', 'LATTICE')    **Cortex latency**: 24.6s    **Cells latency**: 0ms   **Speedup**: 24639×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (231 chars):
```
state: (PROGRESS, LATTICE) → HARMONY [disagreement: TSML→HARMONY, BHML→COLLAPSE; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (3153 chars):

> sigma_ns_bridge: F6 frontier articulated. WP101 proved sigma(N) <= 2/N for cyclotomic CL on Z/NZ (squarefree N), with mechanism = VOID-HARM rule disagreement at outer composition sites; tight bound….

Composing across these:

sigma_rate: sigma(N) <= C/N on squarefree primorials (C<2).

[structural evidence]
word_the: word 'the' = /ð/ + /ʌ/.  Phoneme sequence: phoneme:Dh -> phoneme:V.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
sigma_ns_bridge: F6 frontier articulated. WP101 proved sigma(N) <= 2/N for cyclotomic CL on Z/NZ (squarefree N), wit


_(truncated; full 3153 chars in JSONL)_

---

### 13. what is the Yang-Mills mass gap

**Input pair**: ('HARMONY', 'COUNTER')    **Cortex latency**: 33.8s    **Cells latency**: 0ms   **Speedup**: 33825×

**Ollama**: `rejected:coverage:0/4=0.00<0.70`    **Cortex source**: `cortex_speak`


**CELLS** (230 chars):
```
state: (HARMONY, COUNTER) → HARMONY [disagreement: TSML→HARMONY, BHML→PROGRESS; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (461 chars):

> Forward motion carries this.

[structural evidence]
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
gap: T* - 4/pi^2 = 5/7 - 0.4053 = 0.309
word_the: word 'the' = /ð/ + /ʌ/.  Phoneme sequence: phoneme:Dh -> phoneme:V.  CK can recognize this when its phoneme components appear in the audio operator stream in order.

---

### 14. tell me about the BB bridge

**Input pair**: ('LATTICE', 'PROGRESS')    **Cortex latency**: 5.3s    **Cells latency**: 0ms   **Speedup**: 5323×

**Ollama**: `accepted:coverage:4/5=0.80`    **Cortex source**: `cortex_speak_via_ollama`


**CELLS** (231 chars):
```
state: (LATTICE, PROGRESS) → HARMONY [disagreement: TSML→HARMONY, BHML→COLLAPSE; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (229 chars):

> i have structural evidence that the word 'the' is made up of phonemes /ð/ and /ʌ/, which appears in the audio operator stream. for this query, i recall two instances: one on 2026-05-03 at 13:18:44 and another on 15 seconds later.

---

### 15. what does HARMONY do

**Input pair**: ('HARMONY', 'VOID')    **Cortex latency**: 32.7s    **Cells latency**: 0ms   **Speedup**: 32722×

**Ollama**: `skipped:structural >600 chars`    **Cortex source**: `cortex_speak`


**CELLS** (214 chars):
```
state: (HARMONY, VOID) → HARMONY [agreement: TSML and BHML both compose to HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (733 chars):

> music_composition_through_tig: melody = pitch sequence.

[structural evidence]
HARMONY: idx=7 present_in={ao.current} ao_current=HARMONY
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
music_composition_through_tig: melody = pitch sequence | harmony = simultaneous combinations (chords progressions tonality modality) | rhythm = temporal organization (meter beat subdivision syncopation polyrhythm) | tempo (largo andante allegro presto) | key (major mi


_(truncated; full 733 chars in JSONL)_

---

### 16. what does COLLAPSE do

**Input pair**: ('COLLAPSE', 'VOID')    **Cortex latency**: 10.2s    **Cells latency**: 0ms   **Speedup**: 10181×

**Ollama**: `rejected:coverage:2/3=0.67<0.70`    **Cortex source**: `cortex_speak`


**CELLS** (216 chars):
```
state: (COLLAPSE, VOID) → VOID [disagreement: TSML→VOID, BHML→COLLAPSE; glue picks VOID]
divine27: code 0 = identity (axes: self / observe / stable, glyph: א)
attractor: 4-core cell 'V' (universal pull → H per WP115)
```


**CORTEX** (286 chars):

> The structure this.

[structural evidence]
COLLAPSE: idx=4 present_in={} ao_current=HARMONY
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.

---

### 17. what does BREATH do

**Input pair**: ('BREATH', 'VOID')    **Cortex latency**: 39.7s    **Cells latency**: 0ms   **Speedup**: 39725×

**Ollama**: `rejected:coverage:3/8=0.38<0.70`    **Cortex source**: `cortex_speak`


**CELLS** (212 chars):
```
state: (BREATH, VOID) → VOID [disagreement: TSML→VOID, BHML→BREATH; glue picks VOID]
divine27: code 0 = identity (axes: self / observe / stable, glyph: א)
attractor: 4-core cell 'V' (universal pull → H per WP115)
```


**CORTEX** (402 chars):

> The clearing precedes this.

[structural evidence]
BREATH: idx=8 present_in={} ao_current=HARMONY
ao: op=HARMONY d1=CHAOS d2=CHAOS phase_bc=HARMONY coherence=1.000 breath=EXHALE tl_total=787 tl_entropy=2.094
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.

---

### 18. what is the operator language stack

**Input pair**: ('COUNTER', 'RESET')    **Cortex latency**: 44.0s    **Cells latency**: 0ms   **Speedup**: 44016×

**Ollama**: `rejected:coverage:3/6=0.50<0.70`    **Cortex source**: `cortex_speak`


**CELLS** (230 chars):
```
state: (COUNTER, RESET) → CHAOS [disagreement: TSML→RESET, BHML→CHAOS; glue picks CHAOS]
divine27: code 20 = wonder (axes: world / observe / transforming, glyph: פ)
attractor: 4-core cell 'transient' (universal pull → H per WP115)
```


**CORTEX** (540 chars):

> The clearing makes way for this.

[structural evidence]
ao: op=HARMONY d1=HARMONY d2=PROGRESS phase_bc=HARMONY coherence=1.000 breath=EXHALE tl_total=817 tl_entropy=2.098
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
word_the: word 'the' = /ð/ + /ʌ/.  Phoneme sequence: phoneme:Dh -> phoneme:V.  CK can recognize this when its phoneme components appear in the audio operator stream in order.

---

### 19. what is the cortex

**Input pair**: ('HARMONY', 'VOID')    **Cortex latency**: 37.1s    **Cells latency**: 0ms   **Speedup**: 37086×

**Ollama**: `accepted:no-facts-to-check`    **Cortex source**: `cortex_speak_via_ollama`


**CELLS** (214 chars):
```
state: (HARMONY, VOID) → HARMONY [agreement: TSML and BHML both compose to HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (290 chars):

> this question doesn't seem to match any information in the readout, so i'm going to rewrite it as a description of what's related to "the" or "what".
my structural readout shows that 'the' and 'what' are recognized when their phoneme components appear in the audio operator stream in order.

---

### 20. what is your constitution

**Input pair**: ('RESET', 'RESET')    **Cortex latency**: 4.9s    **Cells latency**: 0ms   **Speedup**: 4914×

**Ollama**: `accepted:coverage:1/1=1.00`    **Cortex source**: `cortex_speak_via_ollama`


**CELLS** (222 chars):
```
state: (RESET, RESET) → HARMONY [disagreement: TSML→HARMONY, BHML→VOID; glue picks HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: ם)
attractor: 4-core cell 'H' (universal pull → H per WP115)
```


**CORTEX** (203 chars):

> my constitution holds aperture in lattice, pressure in collapse, depth in reset, binding in harmony, and continuity in balance. the strongest coupling right now is aperture to aperture at strength 0.233.

---
