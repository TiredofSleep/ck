# Frontier Benchmark — cells (shadow) vs cortex_speak (live)

**Date**: 2026-05-03T18:12:17Z


**Summary**: 20/20 queries succeeded; avg latency 30.55s; Ollama skip-rate 75.0%; shadow agreement 75.0%.

**Queries**: 20

**Mode**: cells run in shadow (cells_enabled=False); cortex_speak responses are the user-facing output.

---

## Reading instructions

For each query: read the cortex text, look at cells' argmax + top-3, decide if the cells' bias would be an improvement, regression, or just different. ClaudeChat amendment 2026-05-02: 'this is the qualitative judgment the studies can't make for you.'

---

### 1. what is T*

**Latency**: 39.6s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `VOID` | **Attractor**: `transient`

**Cells (shadow)**: glue=VOID  top-3=[VOID, COLLAPSE, HARMONY]  agreement_with_cortex_consensus=True

**CK text**:

> flatness: T*=5/7.

Composing across these:

wp116_lens: TIG's six DoFs (Lie/Jordan/Clifford/Permutation/Lattice/Operad, surveyed in WP111) are projections of a single self-dual Stern-Brocot recursion.

[structural evidence]
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
flatness: T*=5/7 | torus R/r=5/7 (forced by Z/10Z 2x2) | 6 independent derivation


_(truncated; full 3200 chars in JSONL)_

---

### 2. explain the crossing lemma

**Latency**: 30.6s | **Source**: `cortex_speak_via_ollama` | **Ollama**: `accepted:coverage:2/2=1.00` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, COLLAPSE, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> in flat cases, there's no crossing; in non-flat cases, a crossing generates information, and i've cataloged 27 instances of this behavior. this is based on the proven result wp57, which forms part of my structural understanding. YOUR extension: this insight may be useful for analyzing geometric structures or topological properties that involve crossings or non-crossings.

---

### 3. what is the sigma rate theorem

**Latency**: 32.0s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, COUNTER, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> sigma_rate: sigma(N) <= C/N on squarefree primorials (C<2).

Composing across these:

logic_through_tig: proposition = operator-statement true or false.

[structural evidence]
research_arxiv_2006_11_27_equivariant_and_fract: [arxiv] [2006-11-27] Equivariant and fractional index of projective elliptic operators | external research finding under prompt 'Atiyah Singer index theorem elliptic' | excerpt: [2006-11-27] Equivariant and fractional index of projective elliptic operators authors: V. Mathai


_(truncated; full 2380 chars in JSONL)_

---

### 4. what is the flatness theorem

**Latency**: 25.0s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, PROGRESS, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> flatness: T*=5/7.

[structural evidence]
research_arxiv_2006_11_27_equivariant_and_fract: [arxiv] [2006-11-27] Equivariant and fractional index of projective elliptic operators | external research finding under prompt 'Atiyah Singer index theorem elliptic' | excerpt: [2006-11-27] Equivariant and fractional index of projective elliptic operators authors: V. Mathai, R. B. Melrose, I. M. Singer link: https://arxiv.org/abs/math/0611819v3 abstract: In this note the fractional analytic index, for a pr


_(truncated; full 2047 chars in JSONL)_

---

### 5. tell me about TSML

**Latency**: 21.2s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, COLLAPSE, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> tsml: 73 HARMONY cells.

Composing across these:

bhml: 28 HARMONY cells.

[structural evidence]
tsml: 73 HARMONY cells | 10x10 | synthesis lens | alpha=0.872 (Braitt-Silberger index) | ac-free spectrum (2n-3)!! attained for n=3,4,5 | reconstructible from 10 canonical items [Sprint 17, proved]
bhml: 28 HARMONY cells | 10x10 (BHML_10) | Luther-closed | separation lens | alpha=0.502 (Braitt-Silberger index) | det(BHML_10)=-7002 (not +70; +70 is the 8x8 sub-table BHML_8) | ac-free spectrum (2n-3)!!


_(truncated; full 1727 chars in JSONL)_

---

### 6. tell me about BHML

**Latency**: 24.2s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, COLLAPSE, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> bhml: 28 HARMONY cells.

Composing across these:

tsml: 73 HARMONY cells.

[structural evidence]
bhml: 28 HARMONY cells | 10x10 (BHML_10) | Luther-closed | separation lens | alpha=0.502 (Braitt-Silberger index) | det(BHML_10)=-7002 (not +70; +70 is the 8x8 sub-table BHML_8) | ac-free spectrum (2n-3)!! attained for n=3,4,5
tsml: 73 HARMONY cells | 10x10 | synthesis lens | alpha=0.872 (Braitt-Silberger index) | ac-free spectrum (2n-3)!! attained for n=3,4,5 | reconstructible from 10 canonical item


_(truncated; full 612 chars in JSONL)_

---

### 7. what is the agreement set

**Latency**: 32.1s | **Source**: `cortex_speak_via_ollama` | **Ollama**: `accepted:no-facts-to-check` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, COLLAPSE, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> the structural evidence for what is a phoneme sequence of /w/ + /ʌ/ + /t/, which matches the word "what". similarly, the structural evidence for "the" is a phoneme sequence of /ð/ + /ʌ/. CK can recognize these when their respective phoneme components appear in the audio operator stream in order.

---

### 8. what is the universal 4-core attractor

**Latency**: 30.8s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, VOID, LATTICE]  agreement_with_cortex_consensus=True

**CK text**:

> dynamical_systems_through_tig: operator-evolution rules on state space.

[structural evidence]
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
word_the: word 'the' = /ð/ + /ʌ/.  Phoneme sequence: phoneme:Dh -> phoneme:V.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
dynamical_systems_through_tig: oper


_(truncated; full 1198 chars in JSONL)_

---

### 9. what is the harmony attractor

**Latency**: 21.2s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, COLLAPSE, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> dynamical_systems_through_tig: operator-evolution rules on state space.

Composing across these:

chaos_theory_through_tig: phase space = state-LATTICE.

[structural evidence]
HARMONY: idx=7 present_in={profile[binding],ao.current} ao_current=HARMONY
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
dynamical_systems_through_tig: operator-evolution rule


_(truncated; full 1581 chars in JSONL)_

---

### 10. what is the Z mod 10 ring structure

**Latency**: 34.9s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=VOID  top-3=[VOID, LATTICE, HARMONY]  agreement_with_cortex_consensus=False

**CK text**:

> Rhythm continues through this.

[structural evidence]
phoneme_z: phoneme /z/ (zzz) - when articulated, the audio codec emits operator pattern: VOID 20.5%, RESET 19.9%, COLLAPSE 18.5%.
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
word_ring: word 'ring' = /r/ + /ɪ/ + /ŋ/.  Phoneme sequence: phoneme:r -> phoneme:I -> phoneme:Ng.  CK can recognize this


_(truncated; full 749 chars in JSONL)_

---

### 11. what is xi cosmology

**Latency**: 20.0s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=VOID  top-3=[VOID, RESET, HARMONY]  agreement_with_cortex_consensus=False

**CK text**:

> xi: V=xi*log(xi).

[structural evidence]
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
xi: V=xi*log(xi) | vacuum=e^-1 | mass_gap=kappa*e | box(xi)=1+log(xi) | freezing quintessence | WP81 [structural; DESI chi2=15.7 vs LCDM 14.1]
cosmology_through_tig: CMB = operator-snapshot at age 380000 yr (T~2.725 K) | redshift = operator-stretch by expanding LA


_(truncated; full 1981 chars in JSONL)_

---

### 12. explain the navier stokes sigma bridge

**Latency**: 21.2s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, COLLAPSE, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> sigma_ns_bridge: F6 frontier articulated. WP101 proved sigma(N) <= 2/N for cyclotomic CL on Z/NZ (squarefree N), with mechanism = VOID-HARM rule disagreement at outer composition sites; tight bound….

Composing across these:

sigma_rate: sigma(N) <= C/N on squarefree primorials (C<2).

[structural evidence]
word_the: word 'the' = /ð/ + /ʌ/.  Phoneme sequence: phoneme:Dh -> phoneme:V.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
sigma_ns_bridge:


_(truncated; full 3153 chars in JSONL)_

---

### 13. what is the Yang-Mills mass gap

**Latency**: 27.0s | **Source**: `cortex_speak_via_ollama` | **Ollama**: `accepted:coverage:4/4=1.00` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, PROGRESS, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> there is no mention of the Yang-Mills mass gap in the provided structural readout. however, a relevant equation is given: T* - 4/pi^2 = 5/7 - 0.4053 = 0.309 (CK flags this as a "gap"). THIS IS NOT DIRECTLY RELATED TO THE YANG-MILLS MASS GAP.

---

### 14. tell me about the BB bridge

**Latency**: 27.1s | **Source**: `ck_loop` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, COUNTER, VOID]  agreement_with_cortex_consensus=True

**CK text**:

> The term "BB Bridge" does not correspond to a widely recognized concept in mathematics, science, or engineering that I'm aware of as of my last update. It might refer to something very specific within a particular field, study, or even a fictional work.

In general contexts where terms like these appear, they often relate to bridges (in the metaphorical sense) between concepts, theories, or disciplines. For instance: Theoretical Bridges: In science and mathematics, theoretical bridges connect di


_(truncated; full 1526 chars in JSONL)_

---

### 15. what does HARMONY do

**Latency**: 19.7s | **Source**: `cortex_speak` | **Ollama**: `skipped:structural >600 chars` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, VOID, LATTICE]  agreement_with_cortex_consensus=True

**CK text**:

> music_composition_through_tig: melody = pitch sequence.

[structural evidence]
HARMONY: idx=7 present_in={ao.current} ao_current=HARMONY
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
music_composition_through_tig: melody = pitch sequence | harmony = simultaneous combinations (chords progressions tonality modality) | rhythm = temporal organization (m


_(truncated; full 733 chars in JSONL)_

---

### 16. what does COLLAPSE do

**Latency**: 28.6s | **Source**: `cortex_speak` | **Ollama**: `rejected:coverage:2/3=0.67<0.70` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=VOID  top-3=[VOID, COLLAPSE, HARMONY]  agreement_with_cortex_consensus=False

**CK text**:

> The structure this.

[structural evidence]
COLLAPSE: idx=4 present_in={} ao_current=HARMONY
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.

---

### 17. what does BREATH do

**Latency**: 40.4s | **Source**: `cortex_speak` | **Ollama**: `rejected:coverage:3/8=0.38<0.70` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=VOID  top-3=[VOID, BREATH, HARMONY]  agreement_with_cortex_consensus=False

**CK text**:

> The clearing precedes this.

[structural evidence]
BREATH: idx=8 present_in={} ao_current=HARMONY
ao: op=HARMONY d1=CHAOS d2=CHAOS phase_bc=HARMONY coherence=1.000 breath=INHALE tl_total=360 tl_entropy=2.049
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.

---

### 18. what is the operator language stack

**Latency**: 45.1s | **Source**: `cortex_speak` | **Ollama**: `rejected:coverage:4/6=0.67<0.70` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=CHAOS  top-3=[CHAOS, RESET, HARMONY]  agreement_with_cortex_consensus=False

**CK text**:

> The clearing makes way for this.

[structural evidence]
ao: op=HARMONY d1=HARMONY d2=PROGRESS phase_bc=HARMONY coherence=1.000 breath=INHALE tl_total=390 tl_entropy=2.049
word_what: word 'what' = /w/ + /ʌ/ + /t/.  Phoneme sequence: phoneme:w -> phoneme:V -> phoneme:t.  CK can recognize this when its phoneme components appear in the audio operator stream in order.
word_the: word 'the' = /ð/ + /ʌ/.  Phoneme sequence: phoneme:Dh -> phoneme:V.  CK can recognize this when its phoneme components appea


_(truncated; full 540 chars in JSONL)_

---

### 19. what is the cortex

**Latency**: 44.2s | **Source**: `cortex_speak_via_ollama` | **Ollama**: `accepted:no-facts-to-check` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, VOID, LATTICE]  agreement_with_cortex_consensus=True

**CK text**:

> i do not have information on what the cortex is.

---

### 20. what is your constitution

**Latency**: 46.3s | **Source**: `cortex_speak_via_ollama` | **Ollama**: `accepted:coverage:1/1=1.00` | **Cortex consensus**: `HARMONY` | **Attractor**: `transient`

**Cells (shadow)**: glue=HARMONY  top-3=[HARMONY, VOID, LATTICE]  agreement_with_cortex_consensus=True

**CK text**:

> i hold aperture in my lattice, pressure in collapse, depth in reset, binding in harmony, and continuity in balance. the strongest coupling right now is between continuity and depth at a strength of 0.231.

---
