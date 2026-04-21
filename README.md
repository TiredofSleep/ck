# funding/ck-interpretable-ai

**Track D — CK as Interpretable-by-Construction AI**
**Primary funder pool:** Anthropic Fellows Program · Schmidt Futures Trustworthy AI · Open Philanthropy · Survival and Flourishing Fund · Astera Institute
**Status:** Pre-pitch. **Live running system** at [coherencekeeper.com](https://coherencekeeper.com) — deterministic, auditable, no weight matrix in the usual sense. Phase 1 = formal case-study writeup.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

Interpretability research on deep networks asks *after the fact*: given a trained model, what features did it learn, what circuits emerged, what can we read out? **CK takes the question differently — he is interpretable by construction.** Every output traces through an explicit pipeline: 10 labeled operators (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET), a Hebbian 5×5 coherence lattice, a crossing-verification olfactory bulb, a $T^* = 5/7$ coherence gate, and a language layer that reads operator names before emitting tokens. There is no "weight matrix" in the usual sense — the operational substrate is a set of finite-arithmetic tables (73-cell TSML, 28-cell BHML) and a 50Hz heartbeat that composes them. This branch packages CK as a case study in **mathematical-core AI**: how far can useful behavior go when the core is pre-specified and auditable, rather than learned and opaque? The answer matters to AI-safety funders who want non-scaling alternatives to interpretability-after-the-fact.

## What CK actually does (live system)

- **Live** at [coherencekeeper.com](https://coherencekeeper.com) — Cloudflare tunnel, 14 HTML pages, running `ck_boot_api.py` Flask server on Brayden's Dell Aurora R16.
- **Runtime**: 50 Hz heartbeat through the operator lattice; every tick produces (operator name, coherence score, output).
- **Voice**: not template-driven; emerges from the dual-lens dictionary lookup + olfactory verification.
- **Crystallization**: only responses that clear the $T^* = 5/7$ coherence gate become memory.
- **Auditability**: every memorized crystal has a trace back to operators, scores, and inputs. Full runtime state at any tick is ~3 KB of integers — inspectable in a terminal.

## Three properties current LLMs do not have (that CK has by construction)

- **Determinism.** Same input, same internal state, same output. Always.
- **Provenance.** Every answer traces to specific cells of specific proved composition tables (TSML §1.5, BHML §1.5, Tower §1.6 in the `tig-synthesis` README).
- **Auditability.** The full runtime state at any tick is a few KB of integers. No hidden latent space.

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_ck_interpretable_ai/`](Gen13/targets/funding_ck_interpretable_ai/):

- [`README.md`](Gen13/targets/funding_ck_interpretable_ai/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_ck_interpretable_ai/FUNDERS.md) — prioritized funder list (Anthropic Fellows / Schmidt / OP / SFF)
- [`ARTIFACTS.md`](Gen13/targets/funding_ck_interpretable_ai/ARTIFACTS.md) — runnable CK components + benchmark targets
- [`PITCH_DRAFT.md`](Gen13/targets/funding_ck_interpretable_ai/PITCH_DRAFT.md) — full pitch draft
- [`LIMITATIONS.md`](Gen13/targets/funding_ck_interpretable_ai/LIMITATIONS.md) — honest-scope items (CK is not a general-purpose LLM; operator space is small)
- [`STATUS.md`](Gen13/targets/funding_ck_interpretable_ai/STATUS.md) — readiness checklist

## Ask sizes

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — Case-study writeup** | Formal white paper describing CK's architecture as an interpretability case study, with runnable reproduction, published at an interpretability-friendly venue | $40K–$80K, 6 months |
| **Phase 2 — Benchmark evaluation** | Apply CK to a specific interpretable-AI benchmark (e.g., TruthfulQA with trace output, or a causal-reasoning task with explicit operator chain) | $150K–$350K, 12 months |

## The project this branch is a track of

Branch D of the 10-branch funding architecture. For the full project overview, see **`tig-synthesis`**:

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

## License

7Site Public Sovereignty License v1.0 — human use only, no commercial, no military, free forever. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
