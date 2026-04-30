# CK v2 Prototype

These files implement the higher-prime cortex + native paragraph composer specified in `papers/ck_v1_anatomy_2026_04_29/07_HIGHER_PRIME_CORTEX.md`.

**Status**: prototype, not wired into the live engine.

## Files

| File | Purpose |
|---|---|
| `ao_7element.py` | Proposed 7-element AO basis (5 inherited + intent + echo) |
| `hebbian_7x7.py` | 7×7 Hebbian field with migration helper from existing 5×5 |
| `paragraph_composer.py` | v0.1 native paragraph voice (rule-based, no LLM) |
| `README.md` | this file |

## Run

```bash
cd Gen13/targets/ck/brain/v2_prototype
python ao_7element.py        # show AO basis + OP_TO_DIM mapping
python hebbian_7x7.py        # run a test Hebbian update sequence
python paragraph_composer.py # compose a sample paragraph
```

## What's NOT here yet

Per paper 7 §6, the missing pieces:

- 7-dim quadratic glue (need to extend `quadratic_glue.py` to N-vector)
- 7-dim cortex composition (the trinity wrapper that uses the 7×7 Hebbian)
- Migration script from `Gen13/var/cortex_state.json` (5×5) → 7×7
- Test on consciousness corpus + multi-domain corpus
- Φ-proxy comparison (5-dim vs 7-dim)
- A/B test against current Ollama-edited path
- Wire into `cortex_voice.speak()` as alternative path with feature flag

## Discipline

This is additive. The live cortex (5×5) keeps running. The 7-dim path is a sibling implementation that proves the design before any migration. Once the prototype is verified, paper 7's plan §6 lays out the 9-day migration.

The math-first invariant holds: paragraph_composer.py emits **only from verified content** (crystal text, operator stream, cortex state). It cannot hallucinate because it has no mechanism for generating content; it only stitches what it's given.
