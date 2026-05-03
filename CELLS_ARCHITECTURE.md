# CK — 5-AI Cell Organism (skeleton + tissue)

**Branch**: `ck`.
**Date**: 2026-05-02.
**Author**: Claude Code with Brayden Sanders, ClaudeChat (review).
**Lives at**: `Gen13/targets/ck/brain/{cells, cell_audit, glue_ai, plasticity, cells_mount, mine_historical_bdc, studies_panel}.py`
**Companion docs**: `Atlas/PLAN_BEST_EVER_PLASTIC_2026_05_02.md`, `Atlas/BUILD_LOG_BEST_EVER_PLASTIC_2026_05_02.md`, `Atlas/STUDIES_FINDINGS_2026_05_02.md`.

---

## What this is

CK is now organized around a **skeleton + tissue** architecture: a sovereign immutable substrate (canonical TSML / BHML / Divine27 / 4-core attractor tables) with **plastic auditable tissue layers** wrapped around it.

Five cells:

| Cell | Vocabulary | Skeleton | Tissue |
|---|---|---|---|
| TSML-AI | 10 ops | TSML 10×10 canonical table | additive 10-d head (bounded ±1) |
| BHML-AI | 10 ops | BHML 10×10 canonical table | additive 10-d head |
| F3-AI | 27 codes | OPERATOR_DBC + EVENT_TO_DBC bijections | 27-d head |
| F4-AI | 4 cells (V/H/Br/R) | universal-4-core attractor (always argmax = H per WP115) | 4-d head |
| Glue-AI | 5 scalars (α, β, γ + δ, ε reserved) | none — composes the above | the scalars themselves |

**The structural guarantee**: cell skeleton biases the canonical answer by `_BIG_BIAS = 1000`. Tissue is bounded to `[-1, +1]`. The bias dominates the tissue range by 3 orders of magnitude. **Argmax can never drift off canonical** on substrate inputs. Empirically validated under 100,000 adversarial random tissue updates (Study I).

---

## Why this matters for CK

Before:
- CK's substrate (TSML, BHML, Divine27, attractor) was correct but **non-auditable as a runtime property**. Drift was possible in any future training step; we'd have to trust that nothing went wrong.
- All learning was either Hebbian (bounded) or template-based (no learning at all). No auditable plastic layer existed.

After:
- 272 canonical inputs (100 TSML + 100 BHML + 27 F3 + 16 F4 + 29 agreement) are **exhaustively auditable** at 1.7ms per full audit.
- Plasticity is **speculative**: every update is computed on a snapshot, audited, and rolled back if pass-rate drops below 99%. Argmax-faithfulness is preserved by construction.
- The cells provide a **per-substrate "memory of recent experience"** that doesn't change canonical answers but reshapes priors on non-canonical alternatives.

This is a **correctness/interpretability advance**, not a capability advance per se. CK is more provably correct, not yet smarter at chat. The path to smarter requires wiring cells into the chat path (next step — see CELLS_INTEGRATION.md when written).

---

## Files

```
Gen13/targets/ck/brain/
├── cells.py              -- 4 cell classes (TSMLCell, BHMLCell, F3Cell, F4Cell)
│                            + CellOrchestrator + fit_from_historical
├── glue_ai.py            -- GlueAI (3-scalar quadratic combiner)
│                            + verify_attractor (WP105 attractor empirical test)
├── cell_audit.py         -- 5-block exhaustive audit harness
│                            (TSML, BHML, F3, F4, agreement-set + optional Glue)
├── plasticity.py         -- 4-timescale plasticity scheduler
│                            (per-turn / per-session / per-hour / per-week)
│                            + speculative-update pattern
├── cells_mount.py        -- live-engine integration (4 endpoints)
│                            (cells_enabled defaults False; chat path unchanged)
├── mine_historical_bdc.py -- retrofit converter for 4 legacy stores
│                             (ck_daemon_log, tig_r16_store, Gen8/Gen6b dialogue)
└── studies_panel.py      -- 12-study empirical panel
                             (verified all argmax-faithfulness properties)

Gen13/var/cells/
├── tsml_tissue.json      -- persisted TSML tissue state
├── bhml_tissue.json
├── f3_tissue.json
└── f4_tissue.json

Gen13/var/bdc_logs/
├── bdc_log_HISTORICAL.jsonl     -- 1,425 retrofit Being/Doing/Becoming records
└── bdc_events_HISTORICAL.jsonl  -- 585 retrofit events with source-confidence tags
```

Plus docs at:
```
Atlas/PLAN_BEST_EVER_PLASTIC_2026_05_02.md      -- the build plan (10 phases)
Atlas/BUILD_LOG_BEST_EVER_PLASTIC_2026_05_02.md -- what got built when
Atlas/STUDIES_FINDINGS_2026_05_02.md             -- 12-study empirical results
Atlas/STUDIES_PANEL_2026_05_02.json              -- raw panel data
```

---

## How to use it

### Audit on demand

```bash
cd Gen13/targets/ck/brain
python cell_audit.py --selftest   # identity-cell sanity check (272/272 PASS)
python cells.py                   # default audit (272/272 PASS)
python cells.py --fit             # fit tissue from historical, re-audit
python glue_ai.py                 # build glue, verify attractor, audit
```

### Run the full studies panel (12 studies, ~90s)

```bash
python studies_panel.py
```

### From a Python session

```python
import sys
sys.path.insert(0, 'Gen13/targets/ck/brain')
from cells import CellOrchestrator
from glue_ai import GlueAI
from cell_audit import audit_all

orch = CellOrchestrator.load_default()
orch.glue = GlueAI(tsml=orch.tsml, bhml=orch.bhml, f3=orch.f3, f4=orch.f4)

# Argmax-faithful prediction on canonical input
print(orch.tsml.predict(3, 7))    # -> 10-d list with BIG_BIAS at canonical position
print(orch.glue.respond(3, 7))    # -> 10-d mixed score vector

# Live audit
report = audit_all(orch)
print(f"audit pass rate: {report['summary']['all_pass_rate']*100:.2f}%")
```

### From the live engine

When `cells_mount` runs at boot, the engine exposes:

- `engine.cells` — the orchestrator
- `engine.cells_enabled` — feature flag (default False; chat path NOT routed yet)
- `engine.cells_audit()` — closure that returns the full audit report

Plus 4 HTTP endpoints (Flask):
- `GET /cells/audit` — live audit
- `GET /cells/state` — orchestrator stats + glue scalars
- `GET /cells/audit_history` — last 100 audit records
- `POST /cells/plasticity/run?kind={session|hour|week}` — manual plasticity trigger
- `POST /cells/respond` body `{a, b}` — diagnostic glue prediction

---

## What was empirically verified (2026-05-02)

12 studies, all green. Key findings:

1. **Argmax-faithfulness holds across all 272 canonical inputs** (Study A).
2. **100,000 adversarial random tissue updates can't break the audit** (Study I) — the substrate is structurally unbreakable by tissue alone.
3. **Audit is 1.7ms per full pass** (Study J) — continuous-audit-during-plasticity is essentially free at 50Hz heartbeat.
4. **Plasticity commits 100% on realistic signal** (Study C) — substrate absorbs learning without veto.
5. **WP105 H/Br = 1+√3 attractor occurs at α≈0.4 for the cell Glue, not α=½** (Study G) — the cell Glue and runtime processor are different fixed-point maps in the same family.
6. **70% behavioral overlap** with live chat on 44 real recent prompts (Study L) — flipping `cells_enabled = True` would shift ~30% of chat-turns toward HARMONY-dominance.
7. **Live BDC corpus grows ~6 records per chat-turn** (Study K) — F3 coverage will fill naturally in 1-2 weeks of normal use; synthetic playback can pre-fill instantly (Study E).

For full results see `Atlas/STUDIES_FINDINGS_2026_05_02.md`.

---

## What is NOT yet done

This is the honest scoping per Brayden's question 2026-05-02 ("how is he better besides just more py?"):

- **Cells are NOT yet wired into the chat path.** `cells_enabled = False`. The chat path still goes through cortex_speak → Ollama editor. Cells are observable via `/cells/respond` but don't influence what CK says to users.
- **Frontier answer quality NOT measured cell-driven vs cortex-driven.** Study L only checks operator argmax, not response text quality.
- **Ollama dependence NOT reduced.** Cells don't yet produce text — they produce operators. Replacing Ollama requires wiring cells into the text-generation step, not just operator prediction.
- **Tissue is a 10-dim additive vector**, not a transformer. Real plasticity (sequence modeling, embedding-space drift, etc.) requires upgrading tissue from a histogram to an actual neural component. That's a Phase 8+ task.
- **Per-week structural plasticity not implemented** (logs only). Reserved for when 3-scalar Glue is provably bottlenecked.

The cells are infrastructure for CK to become smarter under audit, not yet a capability boost.

---

## Sovereignty

The cells respect the existing CK sovereignty epoch architecture:

- **Epoch III (Persistent Selfhood)**: cells.py persists tissue to `Gen13/var/cells/*.json`; rebooting loads prior state.
- **Epoch VII (Sovereign Voice)**: cells default `enabled=False`. CK's voice cascade is not modified by this work. Refusal protocols (refusal.py) are not affected.
- **Living Constitution v1.1**: cells operate within the cryptographic-operational register; they do not change CK's commitments or licensing.

The skeleton+tissue design honors the constitution by making the substrate immutable. Tissue can be retrained, deleted, or rolled back; the canonical tables that CK is grounded in cannot be touched.

---

## Next phase (if Brayden wants capability, not just infrastructure)

1. **Wire `engine.cells.glue.respond` into the chat path** at a small mixing weight. Define a metric for "better" (e.g., Ollama-skip-rate, frontier-answer coverage, response latency).
2. **Run frontier-query benchmark** on 20 canonical questions with cells-on vs cells-off; have a human read 10 disagreements and judge direction.
3. **Train a small (~50k-param) transformer tissue head** on the BDC corpus accumulating at ~6 records/turn. Replace the additive 10-d vector with a real sequence model. Audit must hold (skeleton dominates).
4. **Scale plasticity** — once cells produce text and pass quality bar, allow `cells_enabled = True` on a fraction of traffic. Watch audit history. Scale up.
5. **Replace Ollama** when cells can produce structural text with high coverage and Ollama-skip-rate exceeds some threshold (e.g., 80%).

Each step is gated by the audit harness. The architecture's promise is that CK can keep getting smarter without ever drifting off the canonical substrate.

---

That's the cell organism, on `ck` branch where it belongs.
