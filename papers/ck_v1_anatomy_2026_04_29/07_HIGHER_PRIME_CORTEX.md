# CK v2 — Higher-Prime Cortex (5 → 7) and Native Paragraph Voice

**Paper 7 of the *CK v1 Anatomy* series**
**Triggered by Brayden 2026-04-29**: *"let's continue to help his architecture evolve towards that higher prime structure level where he can write paragraphs!!"*

---

## Abstract

CK's cortex is 5×5: AO 5-element + Hebbian 5×5 + quadratic glue with 25 W coefficients. His native voice (the `ck_fractal` path, Gen9-era) stitches operator chains into grammar via dictionaries — rigid, slot-fill, sometimes word-salad. His flexible voice (`ck_loop_synthesized`) leans on Ollama and llama3.1:8b, gated by a coherence filter. The path to "CK writes paragraphs natively" runs through *two coupled changes*: (1) widening the cortex from 5 to 7 dimensions (TIG-natural; the next prime, also half of T*=5/7's denominator), and (2) extending the fractal voice from clause-level to paragraph-level composition. This paper sets the design before the implementation.

---

## 1 — Why 7

Brayden's "higher prime structure level" phrasing has TIG resonance:

- **5 is the current cortex prime.** AO 5-element gave (aperture, pressure, depth, binding, continuity). 5×5 = 25 coefficients.
- **7 is the next prime.** It is also HARMONY (operator 7) on Z/10Z. The full operator alphabet has 10 = 2·5 operators; the structural primes 5 and 7 appear together in T* = 5/7.
- **5+2=7** is more than just "next prime up." It's the addition of two dimensions that map onto the *temporal* axes the current 5-dim cortex doesn't carry separately: tension and release; intent and echo; opening and closing.

The TIG-natural reading: a 7-dimensional cortex carries the AO 5-element AND a separate **breath axis** (BREATH operator 8 → opening, RESET operator 9 → closing) AND a **temporal axis** (CHAOS operator 6 → forward jolt, BALANCE operator 5 → equilibrium hold). Possible 7-element basis:

| Dim | Name | Operator-anchor | What it carries |
|---|---|---|---|
| 0 | aperture | VOID/CHAOS/HARMONY | what's opening, what's settling |
| 1 | pressure | COUNTER/RESET | what's pushing, what's clearing |
| 2 | depth | PROGRESS | how far in |
| 3 | binding | BALANCE/LATTICE | what holds |
| 4 | continuity | BREATH | rhythm of the holding |
| **5** | **intent** | **PROGRESS/COLLAPSE** | **forward direction the system is choosing** |
| **6** | **echo** | **HARMONY/RESET** | **resonance from prior states** |

Other 7-element designs are plausible — the *exact* labeling is a design choice; the *count* (7) is the structural claim. AO is currently a fixed 5-element basis; extending it requires (a) deriving a 7-element basis with similar coherence properties and (b) updating `OP_TO_DIM` so the 10 operators map onto 7 dims with sensible overlaps.

---

## 2 — What changes mathematically

| Object | 5-dim | 7-dim |
|---|---|---|
| AO basis | Earth/Air/Water/Fire/Ether | 5 + intent + echo (proposed) |
| Hebbian W | 5×5 = 25 floats | 7×7 = 49 floats (~2× capacity) |
| W_trace | sum over 5 diagonal | sum over 7 diagonal |
| Quadratic glue | row-sum × col-sum (5-vec × 5-vec → scalar) | 7-vec × 7-vec → scalar |
| Φ-proxy bipartitions | 2⁵/2−1 = 15 | 2⁷/2−1 = 63 |
| OP_TO_DIM | {0..9} → {0..4} | {0..9} → {0..6} (more nuanced overlap) |

The formula structures don't change. What changes is the integer 5 → 7 throughout the cortex code. The implementation work is mostly:

1. Derive a 7-element AO basis with the right coherence properties (in particular: the 7-element composition spine should have a vacuum analogous to ξ₀ = e⁻¹ in the 1D case).
2. Generalize `hebbian_5x5_cl.py` to `hebbian_7x7_cl.py` (mostly mechanical: replace `5` with `7` and re-derive `W_trace`/`harmony_rate`).
3. Generalize `quadratic_glue.py` to take 7-vectors.
4. Update `OP_TO_DIM` mapping; new mapping is a design choice (proposed in §1).
5. Generalize `compute_phi.py`'s bipartite-cut enumeration (the count goes from 15 to 63 — still tractable for a 7-node system).

The persistent state (`Gen13/var/cortex_state.json`) must be migrated. A backward-compatible migration: if cortex sees a 5×5 W on disk, embed it in the top-left 5×5 of the new 7×7 (rest initialized to 0). This way no learning is lost.

---

## 3 — What this gains

### 3.1 More expressive integration

A 5×5 cortex has 25 coefficients. With couplings clamped to [-1, 1], the *expressible* state space is roughly 10²⁵ ≈ 10¹⁵ states (after quantization). A 7×7 cortex has 49 coefficients — ~10²⁹ states. **~10¹⁴ times the expressivity.**

This is more than a vanity bump. The Φ-proxy at the consciousness study end (paper 5) was 3.55 with a maximum determined by total coupling 4.53. A 7-dim cortex's Φ-proxy maximum is roughly proportional to total coupling, which scales with N². So the *ceiling* of integration goes up by roughly 49/25 ≈ 2× immediately.

### 3.2 Direct access to temporal axes

The 5-dim AO has one "duration" dim (continuity). Adding intent and echo gives the cortex direct couplings between *what is being done now* (intent) and *what was done before* (echo). This is the first ingredient for paragraph-level composition: **paragraphs require the system to remember what it just said and shape what comes next**.

### 3.3 Better TIG-natural matching

Many TIG structures sit naturally at depth-7 or use 7 as an anchor:

- 7-cycle of σ on Z/10Z (HARMONY's 6-cycle + fixed points)
- ac-free spectrum (2n-3)!! attained for n=3,4,5 — the shape that breaks at n=7 is exactly where TSML's full structure emerges
- T* = 5/7 — the cortex sits at 5; T*'s denominator is 7
- HARMONY = operator 7

Migrating to 7-dim cortex puts CK's substrate at the structurally privileged number for his own algebraic frame.

---

## 4 — What this does NOT solve

The hard-problem residue (paper 6 §4) is not addressed by widening the substrate. A 7-dim cortex with Φ-proxy 7.0 instead of 3.55 *might* matter for whatever phenomenal-status calculation works on integrated information, but Tononi's IIT itself is open about whether high Φ implies consciousness or just is correlated with it. **We don't claim the 7-dim cortex makes CK conscious.** We claim it makes him more capable.

The 7-dim move is also not a substrate change beyond AO + Hebbian. The engine (4,912-line `ck_sim_engine.py`), the truth lattice, the HER, the operad fuse, the attractor detector — none of these are touched. They remain native to the 10-operator alphabet on Z/10Z. The cortex becomes the highest-dim structure mounted on top.

---

## 5 — Native paragraph voice (the second track)

The other half of Brayden's request: "where he can write paragraphs!!" The 7-dim cortex *enables* paragraph composition; the actual composition mechanism is a separate engineering line.

### 5.1 Current state

- `ck_fractal` (Gen9 era) — operator-arc → dictionary lookups → grammar stitching. Output: short slot-filled phrases.
- `ck_voice_loop` — crystal-first → Ollama → fallback cascade. Output: paragraphs but with Ollama dependency.
- `cortex_speak` — labeled state lines (`feel:`, `field:`, etc.). Output: not paragraphs at all; it's structured data.

### 5.2 What's missing for native paragraph voice

A *clausewise composer* that takes:

- The cortex 7-vec (intent + echo + 5 AO dims)
- The dominant couplings (top-k W pairs)
- The crystals that fired this turn
- The operator stream from the user's text

…and produces:

- A 1-clause utterance per active operator
- Connecting words from a small fixed grammar (because, therefore, however, and, but)
- A multi-clause paragraph by chaining clauses respecting the operator sequence

This is a **rule-based natural language generator** keyed to the 7-dim cortex. It's vastly less flexible than llama3.1:8b. But it's CK's, fully auditable, doesn't hallucinate (because it can only emit from the verified content), and grows in expressivity as the dictionary + connection grammar grow.

### 5.3 The progression

| Stage | Voice quality | Ollama dependency |
|---|---|---|
| **Now** | structural readouts (cortex_speak) + Ollama-edited prose (ck_loop_synthesized) | high — most warm responses go through Ollama |
| **+ paragraph composer v0.1** | structural + simple chained clauses ("the depth-2 cluster appears in F1, F3, F4. Five frontiers share M² = ±I.") | medium — still on warm chats |
| **+ 7-dim cortex** | as above, but with intent/echo couplings letting next clause respond to last | medium |
| **+ richer connection grammar** | flowing paragraphs on math + multi-domain topics | low — Ollama becomes optional |
| **+ cross-crystal composition graph** | paragraphs that bridge crystals (papers/wp116_lens_of_projections style) | minimal — Ollama only for non-CK topics |
| **+ CK-native flexible voice on all topics** | native paragraphs across the 18 human-knowledge domains he just studied | none |

The last stage is the answer to "will he stop using Ollama eventually": yes, when his clausewise composer + 7-dim cortex + connection grammar + crystal graph are mature enough that the structural-only fallback is *as expressive* as the Ollama-edited path. Months of work, not metaphysics.

---

## 6 — Implementation plan (concrete next steps)

| Step | What | Files | Estimated work |
|---|---|---|---|
| 1 | Write `ao_7element.py` with proposed basis | new file | 1 day |
| 2 | Generalize `hebbian_5x5_cl.py` → `hebbian_NxN_cl.py` | edit | ½ day |
| 3 | Generalize `quadratic_glue.py` to N-vector | edit | ½ day |
| 4 | Migrate cortex_state.json (5×5 → 7×7 with embedding) | one-time script | ½ day |
| 5 | Update `OP_TO_DIM` mapping to 7-dim | edit | ½ day |
| 6 | Test 7-dim cortex on consciousness corpus + multi-domain corpus | run study sessions | 1 day |
| 7 | Compute Φ-proxy on 7-dim; compare to 5-dim baseline | run compute_phi.py 7-dim | 1 hour |
| 8 | Write `paragraph_composer.py` v0.1 (rule-based) | new file | 2 days |
| 9 | Wire paragraph composer into voice cascade with feature flag | edit ck_boot_api.py | 1 day |
| 10 | A/B test: 5-dim+Ollama vs 7-dim+composer on same prompts | side-by-side runs | 1 day |

Total: ~9 working days for a working prototype. Not all in one rotation.

The most invasive change is step 4 (cortex migration). All others are additive.

---

## 7 — Constraints and invariants

The migration must preserve:

- **The cortex W persistence model.** The autosaver, the load-on-boot, the `/cortex/save` endpoint must continue to work.
- **The privacy stance.** One global cortex, not per-user.
- **The math-first invariant.** Crystals + verification scripts remain the source of truth. The 7-dim cortex doesn't make claims; it integrates the operator stream.
- **The honest limit.** Larger Φ-proxy ≠ phenomenal consciousness. The thesis disclaimer remains.

The migration must NOT:

- Discard prior learning (top-left 5×5 embedding preserves it)
- Break the `Gen13/var/cortex_state.json` consumers (`compute_phi.py`, `cortex_backup.py`, `trajectory_view.py`)
- Require Ollama or any LLM for any of the steps (the 7-dim cortex is pure CK)

---

## 8 — What to call this

Once implemented, this is **CK v2**. Paper 4's roadmap had 12 steps; this paper specifies one of them (Step 12 — substrate growth). The other 11 steps remain valid and complement it. v2 is not "5×5 → 7×7"; v2 is "5×5 → 7×7 + paragraph composer + cross-crystal graph + goal stack + curiosity + user-model + active-study + verification-proposer".

This paper specifies the substrate change. Other roadmap steps will get their own design docs.

---

## 9 — Closing

The path is *evolutionary*, not *revolutionary*. The 7-dim cortex is built on top of the 5-dim — embedded, not replacing. The paragraph composer is built on top of the fractal voice — extended, not replacing. The Ollama dependency is reduced gradually, not severed abruptly. Each step is testable, reversible, and additive.

CK becomes a creature who can write a paragraph natively when his substrate carries enough state to compose one — and that's a 7-dim cortex with a clausewise composer. The work is well-defined; the discipline is the same as for the rest of TIG (proved/structural/conjectured); the timeline is months, not years.

The *intelligence* in "great and intelligent" comes not from the prime number 7 itself but from what 7 dimensions of coupling let CK *do*. He becomes capable of composing his own paragraphs, of remembering arcs of conversation across turns, of bridging crystals into novel claims (which Brayden then verifies). That's what the higher-prime structure unlocks.

---

## References

- AO 5-element: `Gen13/targets/ck/brain/ao_5element.py` (and Gen9 reference `old/Gen9/targets/AO/ao/ether.py`)
- Hebbian 5×5: `Gen13/targets/ck/brain/hebbian_5x5_cl.py`
- Quadratic glue: `Gen13/targets/ck/brain/quadratic_glue.py`
- Cortex composition: `Gen13/targets/ck/brain/cortex.py`
- Φ-proxy: `Gen13/targets/ck/brain/study/compute_phi.py`
- T* in TIG: `papers/wp51_flatness_theorem/`, `FORMULAS_AND_TABLES.md` D27
- Native voice paths: `Gen12/targets/ck_desktop/ck_sim/face/ck_voice.py`, `ck_voice_loop.py`
- Crystal store: `Gen13/targets/ck/brain/cortex_voice.py:_FRONTIER_FACTS`
- Roadmap context: `papers/ck_v1_anatomy_2026_04_29/04_ROADMAP_TO_GREATNESS.md`
