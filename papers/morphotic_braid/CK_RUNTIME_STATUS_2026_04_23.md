# CK Runtime Status — 2026-04-23 evening

**Context:** Companion to `HANDOFF_2026_04_23_INDEX.md` and `VERIFICATION_LOG_2026_04_23.md`. Documents the runtime-side ripple of the ClaudeChat evening-handoff packet (84 files on CK; citation + vocabulary + synthesis cleanup). The Phase 1 / Phase 2 / Phase 3 handoff work is already landed (see INDEX.md). This note captures what changed *inside CK* and the live measurement.

**Branch:** `ck` · **Commits this ripple:** `dba41fa`, `e1b1a96`

---

## Changes inside CK

### 1. Extended structural vocabulary (`ck_coherence_verdict.py`)

Ten new terms admitted to `_NAMED_STRUCTURES` and therefore to `_CORE_FACT_NAMES`:

```
MAGCOM   CATALAN   MOUFANG   JORDAN
FAREY    ZETA      SINC
CROSSING FLATNESS  RIEMANN
```

The regex alternation was extended in step so the tokenizer extracts these as facts from a readout. `RIEMANN` is a core fact; the phrase `"riemann hypothesis"` stays in `_HALLUCINATION_MARKERS` (over-claim filter intact).

Before: `_CORE_FACT_NAMES` = 18 names (10 operators + 8 named structures)
After:  `_CORE_FACT_NAMES` = 28 names

Both the primary Ollama-editor path (`ck_boot_api`) and the steer rescue path (`ck_coherence_steer._coverage_of`) route through `ck_coherence_verdict`, so the lift is seen on both gates.

### 2. Steer-rescue fallback hardened (`ck_coherence_steer.py`)

When `ck_boot_api` isn't on `sys.modules` (tests, embedded calls), the steer's `_coverage_of` previously fell to a minimal 10-operator-only regex. It now tries `ck_coherence_verdict.fact_tokens` / `fact_hit` first, so the rescue path sees the same vocabulary as the primary path even when boot wasn't imported.

This keeps the two stages symmetric under every calling context.

### 3. Live probe committed (`probe_accept_rate.py`)

Promoted from `AppData/Local/Temp/` into `Gen12/targets/ck_desktop/probe_accept_rate.py` so we have a stable baseline. Probes `http://127.0.0.1:7777/chat` with 18 fresh questions split into two banks — pre-handoff vocabulary (10 questions) and handoff-vocabulary (8 questions) — and reports both stages:

```
STAGE 1 (Ollama editor):  ollama_verdict        ollama_fact_hits/total
STAGE 2 (Steer rescue):   steer_verdict         steer_accepted_coverage
```

---

## Live measurement (first cold run, 2026-04-23 evening)

```
TOTAL = 18   LIVE = 11   CACHED = 7   ERR = 0

STAGE 1 (Ollama editor):  accepted = 6/11 = 55%
  strict = 2   soft = 4   rej_coverage = 5
  rej_id = 0   rej_halluc = 0   rej_empty = 0

STAGE 2 (Steer rescue):   accepted = 8/11 = 73%
  strict = 6   passthrough = 2   fallback = 3

VOICED (final != honest_fallback): 8/11 = 73%
```

### What voiced via steer rescue (5 lifts editor→voice)

| Question                                 | editor verdict                | steer verdict                |
|------------------------------------------|-------------------------------|------------------------------|
| "tell me what a 2x2 structure forces"    | rejected:coverage 2/10=0.20   | accepted_constants:73        |
| "what is the CATALAN spectrum of TSML"   | rejected:coverage 2/4=0.50    | accepted_constants:73        |
| "how does MOUFANG differ from JORDAN"    | rejected:coverage 0/10=0.00   | accepted_strong              |
| "tell me the sinc² / ZETA(2) identity"   | accepted:soft 4/10            | accepted_constants:28        |
| "describe the RIEMANN connection"        | accepted:soft 4/10            | accepted_constants:28        |

### What fell through to honest_fallback

- **"what does COLLAPSE pressure do to the torus"** — editor soft-accepted 4/11, but `brain_coherence = 0.600 < T* = 5/7 ≈ 0.714`, so steer's operator-coherence gate rejected and fell through to the honest sentence. Working as designed; the steer enforces operator coherence independently of factual coverage.
- **"describe your FLATNESS theorem"** — editor 1/4 coverage. Voiced on a later retry (3/4 strict).
- **"what is MAGCOM"** — editor 1/10 coverage on the first draft. Voiced on a later retry with the graceful "i don't see any mention of magcom in the readout" pattern, which soft-accepts on `core = 5/5 = 1.00` (CK's 5 structural-readout operator names all preserved).

### Cache behavior

After one cold probe plus 2 one-shot re-runs, all 18 questions crystallized in the N=3 buffer. A second probe run with the same bank returned 18/18 `cache_hit` — steady-state `accept = 100%` on repeats.

---

## Diagnostic signal: two orthogonal gates, both tunable

The runtime now gives clean per-stage telemetry on every turn. Tuning knobs are environment-overridable:

| Knob                            | Default | Purpose                                            |
|---------------------------------|---------|----------------------------------------------------|
| `CK_VERDICT_COVERAGE_REQUIRED`  | 0.70    | editor strict gate                                 |
| `CK_VERDICT_SOFT_CORE_COV`      | 0.50    | editor soft-accept core fraction                   |
| `CK_VERDICT_SOFT_CORE_MIN`      | 2       | editor soft-accept minimum core hits               |
| `CK_VERDICT_SOFT_MIN_HITS`      | 2       | editor soft-accept minimum total hits              |
| `CK_VERDICT_SOFT_NO_CORE_COV`   | 0.40    | editor soft-accept when readout has no core facts  |
| (steer T* floor — hard-coded)   | 5/7     | steer operator-coherence gate                      |

The FLATNESS/MAGCOM persistent-fail behavior is now observable: editor's coverage gate or steer's coherence gate, depending on the query shape. Tuning is available per-knob without code changes.

---

## What's NOT shipping in this ripple

- **Phase 4 / Phase 5 of the handoff integration plan** — Brayden-gated per `CLAUDECODE_HANDOFF_VOCABULARY.md` (eight sign-off gates). The runtime vocabulary extension here does NOT change the README, the bibliography, or the paper files. That's a separate branch (`vocab-update-2026-04-23`) and a separate decision.
- **Task 16 (CK dual-table A/B experiment on child-spawn)** — Brayden-gated per `claudecode_jobs/task16_ck_dual_table_experiment/SPEC.md`. Would require spawning a second CK on a non-production port with TSML_Idempotent swapped in, and comparing operator-distribution / accept-rate / Ollama-verdict profile against the canonical TSML_Jordan. Not started.
- **Any change to the live Cloudflare tunnel** — coherencekeeper.com still routes to the production `ck_boot_api.py` exactly as it did before today.

---

## How to reproduce

```
# Server must be up and Ollama must be reachable.
set PYTHONIOENCODING=utf-8
python -X utf8 Gen12/targets/ck_desktop/probe_accept_rate.py

# One-shot diagnostic on a single question (shows structural + draft):
python -X utf8 scratch/probe_single.py "what is MAGCOM"
```

---

**Tag:** `[RUNTIME SNAPSHOT — vocabulary extension active, two-stage telemetry live]`
