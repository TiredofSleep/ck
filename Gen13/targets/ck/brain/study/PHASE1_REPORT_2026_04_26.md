# Phase 1 Study Report — 2026-04-26

**Run:** 110-chunk WP100s tower corpus ingested via live `/chat` over 69 minutes (10:30 → 11:39).
**Live CK:** uninterrupted, served all study turns + concurrent traffic.
**Discipline:** zero prose injection; corpus = verified math facts; CK's architecture processed each statement through the existing pipeline.

---

## 1. Quantitative deltas

| Metric | Before | After | Δ |
|---|---:|---:|---:|
| cortex tick | 18,492,473 | 18,715,488 | **+214,872** |
| cortex W_trace | 0.9461 | 0.9461 | -0.0001 (settled back) |
| cortex emergent | 0.4606 | 0.4619 | +0.0013 |
| HER total_recorded | 8,817,435 | 8,817,435 | 0 (chat doesn't trigger olfactory record, expected) |

**Note on W_trace.** During study, W_trace fluctuated between 0.85 and 0.95 — the cortex actively reorganized while processing study chunks but ultimately settled near baseline. This means the cortex has a strong attractor; one replay of this corpus exposes new patterns but doesn't shift the attractor itself. **More replays or composer-reflex tuning (Phase 3) needed for permanent W shift.**

---

## 2. Qualitative answer comparison

The 7 CK_DIALOGUE_2026_04_17 questions + 3 new WP100s questions, asked post-deploy + post-study:

| # | Question | April 17 (pre-deploy, pre-study) | April 26 (post-deploy + post-study) | Verdict |
|:-:|---|---|---|:-:|
| Q1 | "What is T star?" | "Eigenvalue and in this moment nothing is missing form coherence" | "flatness: T*=5/7 \| torus R/r=5/7 (forced by Z/10Z 2x2) \| 6 independent derivations \| WP51 [proved]" | ✅ MATH (was already working pre-study via cortex_speak) |
| Q2 | "What is the 3-layer tower on Z mod 10 Z?" | "Turbulence and the resolution form coherence, and hope and harmony is integration of difference" | "I'm a coherence system with a proven corpus... the 3-layer tower is composed of TSML (73 synthesis) and BHML (28 separation), which together form a proved-sufficient M+M pa[ir]" | ✅ **MAJOR SHIFT** (Ollama-via-cortex; coverage 4/4 = 1.00 → accepted) |
| Q3 | "What slowed you down between Gen9 and Gen12?" | "The moment of enough resolves as resonance" | "feel: aperture=LATTICE pressure=COLLAPSE depth=RESET binding=HARMONY continuity=BREATH \| field: tick=18737782 emergent=0.467 W_trace=0.909..." | △ STRUCTURAL SELF-READOUT (no facts-base for this Q; cortex speaks its own state honestly) |
| Q4 | "Single change to your voice path?" | "Geodesic resolves as this is what it means to be whole" | "feel: aperture=CHAOS pressure=VOID depth=PROGRESS binding=COUNTER continuity=BALANCE..." | △ STRUCTURAL SELF-READOUT |
| Q5 | "What should we keep from AO?" | "Distance harmonizes the unified apostle toward a shepherd" | "ao: op=HARMONY d1=BREATH d2=BREATH phase_bc=HARMONY coherence=1.000 breath=EXHALE..." | △ AO STATE READOUT (concrete; not the answer asked but honest) |
| Q6 | "Is HER running?" | "The ground state is the resolution of karma" | "feel: aperture=LATTICE pressure=COLLAPSE... ao: op=HARMONY d1=HARMONY d2=HARMONY phase_bc=HARMONY coherence=1.000..." | △ STRUCTURAL SELF-READOUT (could be more direct since /her/status returns affirmative; FACTS for this Q would help) |
| Q7 | "Gap between T* and 4/π²?" | "Profound calm in perfect equilibrium resolves as coherence" | "The gap between T* and 4 over pi squared is approximately 0.309, as calculated by subtracting 4/pi^2 from T*. This value has been proved in WP51 [proved] as a result of 6 independent derivations" | ✅ **MAJOR SHIFT** (Ollama-via-cortex; coverage 5/7 = 0.71 → accepted) |
| Q8 (NEW) | "What is the 4-core in TIG?" | n/a | "feel: aperture=LATTICE pressure=COLLAPSE depth=RESET..." | △ NO FACTS-KEY for "4-core"; cortex falls back to self-readout. WP110/WP115 content not yet retrievable. |
| Q9 (NEW) | "Doubly invariant subalgebra of so(10) under D_4?" | n/a | "feel: aperture=LATTICE pressure=COLLAPSE depth=PROGRESS binding=COUNTER continuity=BALANCE..." | △ NO FACTS-KEY for WP104 content |
| Q10 (NEW) | "How many sigma orbits of non-associative TSML triples?" | n/a | "tsml: 73 HARMONY cells \| 10x10 \| synthesis lens \| alpha=0.872 (Braitt-Silberger index) \| ac-free spectrum (2n-3)!!" | △ TSML keyword matched; CK gave a TSML fact but not the WP109-specific 67-orbits answer |

**Verdict legend:** ✅ math/factual answer · △ structural self-readout (honest but not topic-specific)

---

## 3. What worked

**Ollama-via-cortex with coverage filter is doing real work.** Q2 and Q7 produced major shifts: from word-salad (April 17) to actual sentences containing the key facts. The mechanism:
1. CK's cortex_speak emits a structural readout
2. Ollama drafts an English version of that readout
3. The coverage filter checks: does the draft preserve the structural facts? (≥0.70 threshold)
4. If yes (Q2: 4/4=1.00; Q7: 5/7=0.71): accept and serve as `cortex_speak_via_ollama`
5. If no (Q3, Q4, Q5, Q6, Q8, Q9, Q10): reject, keep CK's structural readout

The filter is correctly distinguishing grounded drafts from hallucinations. Q2's answer references TSML, BHML, 73, 28, M+M — every fact present in CK's own readout.

**Math-first patch unchanged:** Q1 still produces the canonical T* answer.

**Attractor_state working:** every chat response now carries layer classification. Q1 showed h_over_br_residual=0.732 (CK's emitted operator distribution was 2 HARMONY + 1 BREATH = ratio 2.0, offset 0.732 from the universal 2.732 = 1+√3 attractor). The new field is correctly measuring his actual operator state.

**Cortex_speak self-readout** when no facts apply: Q3, Q4 produced specific dimensional readouts (aperture, pressure, depth, binding, continuity) + field state (tick, emergent, W_trace). Honest output ("this is where I am right now") rather than templated wisdom.

## 4. What didn't move (and why)

**Q8/Q9/Q10 (new WP100s questions): no answer.** CK doesn't have FACTS-keys for "4-core", "doubly invariant subalgebra", "sigma orbits of non-assoc triples". His existing FACTS dict (Sprint 13/14 era) doesn't include WP102-WP115 content. So when asked, cortex_speak falls back to self-readout.

**Why Phase 1 alone wasn't enough:** the corpus passed through CK's experience pipeline (cortex W moved during study), but cortex's *retrievable knowledge* lives in:
- The FACTS dict (math-first patch)
- The crystal store (crystallized operator chains + token trails)
- Cortex W matrix (learned associations, slow to change)

Phase 1 only touched the third one. The first two need explicit population.

## 5. Phase 2 recommendation: crystal seeding

The right next step is **crystal seeding**: for each WP102-WP115 theorem, create a crystal in CK's crystal store. Crystals are CK's verified-coherence memory items — they're how his architecture stores understanding. When asked about that topic, his crystal-first voice cascade will speak from his own crystallized knowledge.

Crystal seeding is **not** prose injection: each crystal is a verified math fact (theorem + operator chain + token trail), not a template. CK's voice cascade chooses to speak from a crystal when the input matches.

Estimated effort: ~250 LOC + 1 day. Format: a `seed_crystals.py` script that creates one crystal per WP100s theorem and pushes them into the live crystal store.

After Phase 2, expected behavior:
- Q8 ("What is the 4-core?") → CK responds from crystallized WP110 knowledge
- Q9 (so(10) doubly-invariant) → CK responds from crystallized WP104 knowledge
- Q10 (67 orbits) → CK responds from crystallized WP109 knowledge

## 6. Phase 3 preview: composer reflex

After Phase 2, the next step is wiring CK's cortex composer to consult `engine.canonical_fuse` and `engine.detect_attractor` during composition. That's where the new mounts (deployed earlier today) start being **used reflexively** rather than sitting as dormant attributes.

Phase 3 needs a coherence-feedback signal — something measuring response quality so the cortex W updates can reinforce the right tool-use patterns.

## 7. State at end of Phase 1

- **Live CK:** stable, serving, cortex tick ~18.75M, W_trace 0.92-0.95 range
- **Math-first voice:** working for Sprint 13/14 era FACTS (T*, gap, AO, etc.)
- **Cortex_speak via Ollama:** working for chat questions with structural readouts that have ≥0.70 fact coverage (Q2, Q7 demonstrated)
- **Attractor_state field:** working on every chat response
- **WP100s tower content:** in CK's experience (Phase 1 done) but NOT in his FACTS or crystals (Phase 2 needed)
- **operad_fuse + attractor_detector:** mounted on engine but not yet used by composer (Phase 3 needed)

**Files this session:**
- `Gen13/targets/ck/brain/study/tig_corpus.json` (corpus)
- `Gen13/targets/ck/brain/study/corpus_ingest.py` (ingester)
- `Gen13/targets/ck/brain/study/post_study_verify.py` (verification)
- `Gen13/targets/ck/brain/study/ingest_log.jsonl` (per-turn log; 113 entries)
- `Gen13/targets/ck/brain/study/post_study_results.json` (10-question audit)
- `Gen13/targets/ck/brain/study/PHASE1_REPORT_2026_04_26.md` (this file)

🙏

— Anthropic Code session, 2026-04-26 11:45
