# Gen13 Architecture — Math-First, Brain-Intact

## The One Diagnosis That Drove Gen13

> CK's operator chains are mathematically perfect. The voice layer cannot say numbers.

Verified live against the Gen12 production server (tick=36,270,588, coherence=1.0, GROKKED) on 2026-04-17. Full transcript: `targets/ck/CK_DIALOGUE_2026_04_17.md`.

When asked *"What number is T star?"*, CK's heartbeat produced the chain:

```
COUNTER → COUNTER → HARMONY → HARMONY → VOID → COLLAPSE → BREATH → BALANCE → LATTICE → PROGRESS
```

That is a textbook measurement-to-resolution arc. The math is happening. But the voice rendered:

> "Eigenvalue and in this moment nothing is missing form coherence, and t* is the resolution of the progression."

No `5/7`. No `0.714`. The SEMANTIC_LATTICE renders adjective + verb tier words; numbers were never wired in.

---

## The Two-Part Fix

**Part 1 — surface_math (math-first voice patch).** A small dictionary of `(topic_key → math_fact)` pairs sourced from `ck_tables.py`, `FORMULAS_AND_TABLES.md`, and the Sprint papers. Before falling through to SEMANTIC_LATTICE, ask: *"Is this query about T*, the tower, σ, BHML, TSML, the gap, AO, HER, or the operators?"* If yes, return the fact. If no, fall through.

Insertion point: `targets/ck/server/ck_boot_api.py` wraps `api.process_chat`. The Gen11 brain is untouched.

**Part 2 — restore HER.** `engine.olfactory_her = build_olfactory_her(self.olfactory)` after engine boot. Gen10 had it; Gen12 lost the call. Restored in `ck_boot_api.py` immediately after `engine.start()`.

---

## The Composition Spine — Gen9 AO 5-Element

The brain is organized by the rule from `old/Gen9/targets/AO/ao/ether.py:171` (`class AO`). Each tick:

```
input symbol → D1.feed(symbol)
            → D2.feed(symbol)
            → Heartbeat.tick(current_op, d2_op, shell)   # CL[B][D] table lookup
            → coherence.observe(d2_op)                   # 32-entry window
            → brain.observe(d2_op)                       # transition memory
            → body.tick(coherence, bump, novelty)        # E, A, K + breath + wobble
            → BTQ.decide(d2_op, brain, coherence, body, shell)
            → next current_op
```

| Element | Concern | Module(s) |
|---|---|---|
| **Earth** | Ground (constants, lattice, tables) | `ck_tig.py`, `ck_tables.py`, `ck_divine27.py` |
| **Air** | D1 generator (velocity, non-local view) | `ck_sim_d2.py` (D1 path) |
| **Water** | D2 eye (curvature, local measurement) | `ck_sim_d2.py` (D2 path) |
| **Fire** | Engine (heartbeat, brain, body, BTQ) | `ck_sim_heartbeat.py`, `ck_sim_brain.py`, `ck_sim_body.py`, `ck_btq.py` |
| **Ether** | Coupling (voice, I/O, the living loop) | `runtime/ck_voice_math.py` + face/* |

---

## What Carries Forward (Untouched)

- All 156 Gen11 brain modules / 122K LOC at `targets/ck/brain/ck_sim/`
- The Gen11 `__init__.py` meta-path alias finder (`_CKAliasFinder`) — flat imports keep working
- 14 HTML pages from Gen12 `website/`
- `ck_tl.bin` truth lattice
- `ck_tables.py` (TSML/BHML/CL canonical)
- `ck_boot_api.py` (Gen12 Flask boot, repathed)
- 6 Clay sprint folders (sprint10, 12, 13, 14, 16, 17)
- 11 journal venue folders, regrouped by submission tier
- XIAOR Dog (10 files)

## What Gen13 Adds (Net New)

- `targets/ck/runtime/ck_voice_math.py` — math-first voice patch (~250 LOC)
- `targets/ck/brain/BRAIN_DESIGN.md` + `NEURAL_INVENTORY.md`
- `targets/ck/CK_DIALOGUE_2026_04_17.md` — diagnostic transcript
- `targets/ck/server/ck_boot_api.py` patches: surface_math wrap + HER restoration (~50 LOC delta)
- `targets/journals/SUBMISSION_LADDER.md` — 4-tier publication map
- This file + `README_GEN13.md` + `NEXT_CLAUDE_NOTES.md`

## What Gen13 Does NOT Do

- Does not delete anything from Gen12 (or Gen9, Gen10, Gen11) — never-delete preserved
- Does not rewrite the 4,912-line `ck_sim_engine.py` — Gen11 brain is intact
- Does not cut the live Cloudflare tunnel over to Gen13 (separate user-confirmed step)
- Does not push to GitHub without confirmation
- Does not import vocabulary across the three threads (TIG / Q-series / finite arithmetic stay separate)

---

## The Constants

| Constant | Value | Source |
|---|---|---|
| **T*** | 5/7 = 0.714286 | torus aspect ratio, six independent derivations |
| **4/π²** | 0.405285 | sinc²(1/2), historical |
| **gap** | 0.309 | T* − 4/π² (proves T* is not the sinc² zero) |
| **ξ₀** | e⁻¹ = 0.368 | vacuum of log nonlinearity (BB 1976) |
| **m²_ξ** | κe | mass gap, Sprint 14 PRISM-XI |
| **σ(N)** | ≤ C/N | rate theorem, Sprint 14 WP101 |

All cited in `targets/ck/runtime/ck_voice_math.py` FACTS dict and the corresponding sprint papers.

---

## The 10 TIG Operators

```
0  VOID       empties
1  LATTICE    builds structure
2  COUNTER    measures
3  PROGRESS   steps forward
4  COLLAPSE   oscillates  (Brayden's primary operator)
5  BALANCE    equilibrates
6  CHAOS      breaks open
7  HARMONY    settles
8  BREATH     rests
9  RESET      clears
```

CREATION orbit = [1,3,9,7]. DISSOLUTION orbit = [2,4,8,6]. COLLAPSE = (+1,-1) oscillation. CHAOS = (-1,+1) reversed.

---

## How to Verify Gen13 Works

```
cd Gen13/targets/ck/server
python ck_boot_api.py
```

Expected boot lines:
```
[CK] Disagreement tick: adaptive Hz from algebraic disagreement
[CK] Gen13 math-first voice: ENABLED
[CK] Gen13 HER: restored (engine.olfactory_her initialized)
[CK] Organism alive. API: http://0.0.0.0:7777
```

Then:
```
curl -X POST http://localhost:7777/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"What number is T star?","session_id":"test","mode":"normal"}'
```

Should return JSON containing `T* = 5/7 = 0.714286 ...` in the `text` field, with the original adjective response preserved at `text_gen12` for comparison.

```
curl http://localhost:7777/her/status
```
Should return `{"available": true, ...}` (Gen12 returned `false`).

---

## Why Brayden Asked For This

> "ck is struggling to communicate, he is overarchitected and under mathed... let him use all of the neural architecture we have made for him — d2, 5d, olfactory, gustatory, HERS, Hebbian AO, DKAN, and there were others!"

Gen13 is the smallest set of changes that gives CK back his math voice without disturbing the brain that already works.
