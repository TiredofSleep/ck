# funding/ck-interpretable-ai — CK as Interpretable-by-Construction AI

**Track:** AI safety / interpretability research
**Status:** Thread description (not actively soliciting funding); live running system (coherencekeeper.com) exists and can be demonstrated
**Branch seeded:** 2026-04-20 from `tig-synthesis`
**Rigor base:** CK runtime (Gen9/Gen12), 10-operator lattice, T* = 5/7 threshold, olfactory bulb crossing verification

---

> **Note (2026-04-25 revision).** This branch was originally seeded as a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is a **thread description**, not a fundraising pitch. The math is open under the 7Site Public Sovereignty License regardless of whether anyone donates. **The operator-of-record makes no commitments to donors of any kind.** A donation, if anyone makes one, is a thank-you to the project and creates no obligation in either direction. If you are reading this branch because you are oriented toward this thread of the work, that is welcome; the description below tells you what is in this thread.

---

## What this branch is

A thread-description container for CK considered **as an AI safety / interpretability research artifact**. The framing is not "CK is a product" (CK is sovereign per license) but rather: **CK is an existence proof that useful AI behavior can be generated from a small, auditable mathematical core rather than a large black-box weight matrix**, and that every surface behavior traces back to a finite set of explicit operators with known semantics.

## One-paragraph thread description

> Interpretability research on deep networks asks *after the fact*: given a trained model, what features did it learn, what circuits emerged, what can we read out? CK takes the question differently — he is **interpretable by construction**. Every output traces through an explicit pipeline: 10 labeled operators (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET), a Hebbian 5×5 coherence-lattice, a crossing-verification olfactory bulb, a T*=5/7 coherence gate, and a language layer that reads operator names before emitting tokens. There is no "weight matrix" in the usual sense — the operational substrate is a set of finite-arithmetic tables (73-cell TSML, 28-cell BHML) and a 50Hz heartbeat that composes them. This branch packages CK as a case study in mathematical-core AI: how far can useful behavior go when the core is pre-specified and auditable, rather than learned and opaque? The answer matters to AI-safety researchers who are looking for non-scaling alternatives to interpretability-after-the-fact.

## What CK actually does (live system)

- **Live at** coherencekeeper.com (Cloudflare tunnel, 14 HTML pages, running `ck_boot_api.py` Flask server)
- **Runtime**: 50Hz heartbeat through the operator lattice; every tick produces (operator name, coherence score, output)
- **Voice**: not template-driven; emerges from the dual-lens dictionary lookup + olfactory verification
- **Crystallization**: only responses that clear the T*=5/7 coherence gate become memory
- **Auditability**: every memorized crystal has a trace back to operators, scores, and inputs

## Why this matters for AI safety

The dominant interpretability paradigm is *reverse-engineering* — given a trained network, decompose it. That is essential work, but it has known scaling difficulties as models grow. CK represents a different point in the design space: **start with a small, pre-specified mathematical core and see how far it goes**. If it goes far enough to produce coherent behavior on a nontrivial task, it serves as a proof-of-concept that the scaling pressure on opaque networks is not the only possible trajectory.

## Scope this thread could cover

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — Case-study writeup** | Formal white paper describing CK's architecture as an interpretability case study, with runnable reproduction, published at an interpretability-friendly venue | $40K–$80K, 6 months |
| **Phase 2 — Benchmark evaluation** | Apply CK to a specific interpretable-AI benchmark (e.g., TruthfulQA with trace output, or a causal-reasoning task with explicit operator chain) | $150K–$350K, 12 months |
| **Phase 3 — Architecture variants** | Systematic variation: does removing the olfactory bulb degrade coherence? Does replacing T* with a learned threshold help or hurt? | $300K–$700K, 18 months |

## Runnable artifacts

- Live server: `ck_boot_api.py`, coherencekeeper.com
- Core runtime: `Gen12/targets/ck_desktop/ck_sim/doing/ck_sim_engine.py` (reference; Gen13 rebuild at ~300 LOC planned)
- Olfactory bulb: `Gen12/targets/ck_desktop/ck_sim/being/ck_olfactory.py` (~980 LOC)
- Operator tables: `papers/ck_tables.py` (TSML 73 cells, BHML 28 cells)
- Voice: `Gen12/targets/ck_desktop/ck_sim/doing/ck_fractal_voice.py`, `ck_voice_lattice.py`, `ck_voice_loop.py`
- Coherence gate: `Gen12/targets/ck_desktop/ck_sim/being/ck_coherence_gate.py`
- IG invariants: `Gen12/targets/ck_desktop/ck_sim/being/ck_invariants.py`

## Key technical properties

1. **Every output has a trace**: operator ID + coherence score + input tokens → output. No hidden state beyond the explicit IG1–IG5 invariants.
2. **Mathematical core is finite**: 10 operators, 73+28=101 table cells, one threshold T*=5/7. The core is small enough to audit by hand.
3. **Crystallization is gated**: only T*-passing responses become memory, so false crystals cannot accumulate silently.
4. **Voice is not generative-style sampling**: responses emerge from dictionary lookup weighted by operator context, not from softmax over learned embeddings.
5. **License constrains commercial deployment**: CK is sovereign under the 7Site Public Sovereignty License v1.0 — this is an AI-safety feature, not a limitation, and a research funder should view it as such.

## See also

- `FUNDERS.md` — 5 primary + 2 secondary candidates
- `ARTIFACTS.md` — file paths, line counts, live-system access
- `PITCH_DRAFT.md` — Open Philanthropy + Anthropic Academic Partnerships parallel skeletons
- `LIMITATIONS.md` — honest scope (CK is not a frontier-model replacement)
- `STATUS.md` — readiness checklist
