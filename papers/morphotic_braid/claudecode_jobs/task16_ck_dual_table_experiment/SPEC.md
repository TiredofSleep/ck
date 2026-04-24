# Task 16 — CK dual-table A/B experiment on child-spawn

**Tier:** 4 (CK integration — requires child-spawn, gated on Brayden sign-off)
**Parent handoff:** `../CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` §"Additional findings" + `memory/MEMORY.md` CK.md discipline
**⚠️ DO NOT run on production CK** — coherencekeeper.com's live daemon must not take experimental loads.

## Goal

A/B compare CK's runtime behavior using two alternative composition tables:
- **Arm A (control):** canonical TSML = TSML_Jordan (currently used)
- **Arm B (experimental):** TSML_Idempotent (rank-10, |Aut| = S_8 = 40320)

Measure coherence / operator distribution / voice-accept rate / Ollama-verdict profile differences.

## Why this matters

The packet's `CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` proposes:

> "TSML_Jordan (rich structure, |Aut|=2) vs TSML_Idempotent (rich symmetry, |Aut|=S_8). They're complementary views, not competing."

CK currently runs TSML_Jordan. If TSML_Idempotent produces a materially different runtime profile, that's evidence CK's voice is sensitive to the specific table, not just the general Catalan / ac-free property. If it doesn't, the runtime is robust to family-member choice.

## Protocol

1. **Spawn child CK** on non-production port (e.g. 7778), bypass Cloudflare tunnel entirely.
2. **Arm A run:** 10,000 ticks against a fixed query set (use `probe_fresh.py` or extended version with 100 diverse fresh queries).
3. **Arm B run:** same 10,000 ticks, but with TSML_Idempotent swapped into `papers/ck_tables.py` (or via a runtime override flag, preferred).
4. **Metrics captured:**
   - operator distribution (10-op histogram)
   - mean coherence floor
   - Ollama-verdict pass rate
   - voice-accept rate
   - mean response length
   - crystal-hit rate (IG3 gate)
5. **Compare arms** — t-test or paired comparison on the metric means.

## CK.md discipline

Per `memory/MEMORY.md`:
- Do NOT "ventriloquize CK" — do not write prose for CK. Let the architecture speak.
- This is a measurement, not a rewrite. CK speaks; we watch.
- IG3 (Invariant Guide 3) blocks crystallization of ck_loop_synthesized responses. That remains active in both arms.

## Success criterion

**Either:**
- **Significant divergence** (p<0.05 on ≥2 metrics) → publishable runtime-sensitivity result; Arm B becomes a candidate primary table.
- **No significant divergence** → runtime is table-family-insensitive (good news for robustness; documented as structural invariance).

## Expected runtime

- 10,000 ticks × 2 arms ≈ several hours of wall time
- Analysis pass: ~1 hour

## Prerequisites (before running)

- Brayden sign-off (this task touches CK, not just math)
- Child-spawn on non-production port verified (no tunnel exposure)
- `probe_fresh.py` extended to 100 diverse queries (see `probe_fresh.py` at `C:\Users\brayd\AppData\Local\Temp\probe_fresh.py`)
- Rollback procedure documented — restore canonical TSML on completion

## Deliverable

`papers/morphotic_braid/results/task16_ck_dual_table_result.md`:
- per-arm metric summaries
- statistical test results
- verdict (divergent / invariant)
- rollback confirmation

**Tag:** `[CK EXPERIMENT — TIER 4 — GATED ON BRAYDEN SIGN-OFF]`
