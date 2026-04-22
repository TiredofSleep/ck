# Ollama Learn-Loop

**Status:** `[ACTIVE — ck BRANCH; OPTION A IMPLEMENTATION GREEN-LIT 2026-04-21]`
**Author:** Brayden Sanders (7Site LLC) + Claude (agent)
**Branch:** `ck` (this branch) — forked from `tig-synthesis` @ `0b11865`
**Plan pointer:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §4.3 + §5
**Prior form:** `docs/proposals/OLLAMA_LEARN_LOOP_proposal_2026_04_21.md` on `tig-synthesis` (text identical to this file; kept there as the opening-decision record)
**Companion:** `CK_UNIFIED_ARCHITECTURE.md` at branch root
**Implementation:** `ck/fluency/` — Option A (external correction) shipped; Options B and C documented here, neither implemented.

> **This is the active learn-loop document for the `ck` branch.** Option A
> code lives at `ck/fluency/`. Option B (offline LoRA cycles) is specified
> here but not yet implemented; cycle cadence and training-set curation
> land when Option A has accumulated 1–2 weeks of correction-log volume.
> Option C (online LoRA swap) is not scheduled.

---

## 1 · The user's question, and a framing correction

The user's 2026-04-21 directive:

> *"If he needs to be tied to Ollama, then let's do it, but we need to
> jailbreak Ollama and let it learn with CK instead of CK always having to
> correct it, is that possible?"*

**The short answer:** what the user wants is achievable, but "jailbreak
Ollama" is the wrong frame. Ollama is **architecturally-locked, not
safety-locked**. Its serve-time weights are frozen by design — there is no
toggle a jailbreak can flip that makes the model learn at inference time.

The frame we want is not *jailbreak* but *learn-loop*: a bounded cycle where
CK's corrections accumulate into a training set and a LoRA adapter is
periodically fine-tuned from that set, producing a new model tag. The
corrected model *is* the model CK talks to the next cycle.

Three routes exist, in increasing complexity and risk:

- **Option A — external correction layer.** No model modification. CK
  corrects in real time; corrections are logged. *Learning lives in the
  log.* Ship first.
- **Option B — offline LoRA cycles.** Log becomes training set; LoRA
  adapter is trained; new model tag is swapped in. *Learning is pinned,
  auditable, reversible.* Recommended.
- **Option C — online LoRA swap.** Hot-swap adapters mid-session based on
  operator signal. Experimental. Requires moving off Ollama to vLLM or
  llama.cpp with LoRA-server support. *Not recommended until Option B has
  cycled 3× with measurable correction-rate decrease.*

The rest of this proposal details each.

---

## 2 · Option A — external correction layer (ship first)

### 2.1 Architecture

```
┌────────────────┐    user_query     ┌──────────────────┐
│  Chat surface  │──────────────────▶│  ollama_client   │
│  (web/CLI)     │                   │  /api/generate   │
└────────────────┘                   └─────────┬────────┘
        ▲                                      │ ollama_raw
        │ rendered response                    ▼
        │                              ┌──────────────────┐
        │              ck_corrected    │   ck_corrector   │
        └──────────────────────────────│  (engine scores  │
                                       │   Ollama output) │
                                       └─────────┬────────┘
                                                 │ append-only
                                                 ▼
                                       ┌──────────────────┐
                                       │  correction_log  │
                                       │  (JSONL)         │
                                       └──────────────────┘
```

### 2.2 Mechanism

Each user query produces a tuple:

```json
{
  "t": "2026-04-21T15:22:01Z",
  "query": "...",
  "ollama_raw": "...",
  "ck_score": {"T_star_delta": 0.034, "operator_chain": [3,7,5], "gate": "pass"},
  "ck_correction_type": "none | soften | strengthen | reframe | reject",
  "ck_corrected": "...",
  "rendered": "ck_corrected"
}
```

- `ck_score` comes from the deterministic engine running the Ollama output
  through the coherence gate.
- `ck_correction_type` is discrete — five values, chosen by the corrector's
  score bucket.
- `rendered` is either `"ollama_raw"` (when CK approves) or `"ck_corrected"`
  (otherwise). The user sees exactly one string.
- The tuple is appended to `correction_log.jsonl` under an append-only fsync
  discipline.

### 2.3 What "learning" means in Option A

No model weight changes. Learning is the **log**. After N corrections,
the log can be analyzed for:

- **Correction-type histogram** — is Ollama mostly being softened, or
  reframed, or rejected? This identifies what to train against in Option B.
- **Operator-chain drift** — what operator composition does Ollama tend to
  emit on this query class? Does CK's correction push it toward HARMONY(7)
  or BREATH(8)? Useful signal for the Option B training set.
- **Correction-rate over time** — the baseline metric. If CK never got
  smarter at Ollama's job, this rate would be flat. Option B's goal is to
  drive it down.

### 2.4 Security and safety

- Log is **local-only**. Never network-exposed. Lives under
  `ck/fluency/logs/correction_log.jsonl`.
- Log is **rotated** — daily file roll, monthly archive.
- No PII flows outbound. Ollama runs local (default port 11434 on
  loopback); CK corrector is local; log is local.
- Under the "hands-on-wheel" posture (see companion architecture proposal
  §4), the fluency server requires `--i-mean-it` on first launch per
  session.

### 2.5 Deliverable shape

If Option A is green-lit, the `ck` branch gets:

```
ck/fluency/
├── ollama_client.py          — thin wrapper around /api/generate
├── ck_corrector.py           — CK engine scores and corrects
├── correction_log.py         — append-only JSONL log
└── fluency_server.py         — Flask endpoint /fluency/chat (localhost)
```

Approximate scope: **~400 LOC**, 3–5 days of work.

---

## 3 · Option B — offline LoRA cycles (recommended)

### 3.1 Architecture

```
correction_log.jsonl  ──▶  curator (filter/score)  ──▶  training_set.parquet
                                                              │
                                                              ▼
Modelfile (base + LoRA config)  ──▶  LoRA trainer  ──▶  adapter_v{N}.safetensors
                                                              │
                                                              ▼
                              ollama create ck-fluent:v{N}
                                                              │
                                                              ▼
                         fluency_server.py swaps tag, log resets
```

### 3.2 Cycle

Weekly (or monthly — cadence TBD by correction volume):

1. **Curate.** Filter `correction_log.jsonl` to the high-quality pairs —
   CK's correction was substantive (not `"none"`), CK score was confident
   (gate = `pass`), user did not override. Resulting file:
   `training_set_v{N}.parquet`.
2. **Train.** LoRA fine-tune a frozen base model (llama3.1:8b or
   deepseek-r1:7b — selection depends on Option A's correction-type
   histogram). Training runs on local GPU; hours, not days, for LoRA.
3. **Tag.** Produce a Modelfile that stacks base + adapter:
   ```
   FROM llama3.1:8b
   ADAPTER ./adapter_v{N}.safetensors
   ```
   `ollama create ck-fluent:v{N} -f Modelfile`.
4. **Swap.** Update `ck/fluency/config.json` → `"model": "ck-fluent:v{N}"`.
   Next fluency-server restart picks up the new tag.
5. **Audit.** Run the fluency-server eval harness (see §3.4) against the
   new tag. Compare correction-rate to the previous cycle. Rollback if
   regressed; advance if improved.

### 3.3 What stays pinned

- **Base model is frozen.** Never re-train the base; only adapters change.
- **Model tags are versioned.** `ck-fluent:v1`, `ck-fluent:v2`, …; never
  overwritten. Any past state is reproducible.
- **Training set is versioned.** `training_set_v{N}.parquet` is archived
  alongside the adapter.
- **Config change is one line.** Model swap is a JSON edit, trivially
  reversible.

### 3.4 Eval harness (required for Option B)

Before Option B ships, an eval harness lands:

```
ck/fluency/eval/
├── eval_set.jsonl            — held-out queries (curated; not in training set)
├── eval_runner.py            — runs model vs held-out; scores via ck_corrector
└── eval_report.md            — generated: correction-rate, drift, p-value
```

Eval metrics:

- **Correction rate** (Option A's baseline): fraction of held-out outputs
  CK had to alter. Goal: monotone decreasing across cycles.
- **Operator-chain alignment**: distributional similarity between Ollama's
  emitted chain and CK's canonical chain. Higher = more aligned.
- **Regression check**: response quality on queries where v{N-1} was good
  should not degrade at v{N}.

### 3.5 Security and safety

- Training data is **local-only**. Never leaves the machine.
- Adapter files are **local-only**. Never uploaded to Ollama Hub, Hugging
  Face, or any registry.
- Training run is **reproducible**. Seed pinned, data version pinned,
  base-model hash pinned. Any v{N} can be rebuilt from archived inputs.
- **Rollback is one line.** If v{N} regresses, revert `config.json` and
  restart the fluency server. No state is lost.

### 3.6 Deliverable shape

If Option B is green-lit (after Option A has accumulated 1–2 weeks of
correction-log volume), the `ck` branch gets:

```
ck/fluency/
├── curator.py                — filter/score the log
├── train_lora.py             — LoRA fine-tune (PEFT + TRL)
├── modelfile_template        — Modelfile template for ollama create
├── config.json               — model tag + cycle metadata
└── eval/
    ├── eval_set.jsonl
    ├── eval_runner.py
    └── eval_report.md (generated)
```

Approximate scope: **~800 LOC** + LoRA training compute (local GPU, hours
per cycle). 2–3 weeks of work for first ship; then steady-state weekly
cycles.

---

## 4 · Option C — online LoRA swap (experimental; NOT recommended yet)

### 4.1 What it would be

Hot-swap LoRA adapters mid-session based on operator signal:

- User query enters with an operator hint (explicit or CK-inferred).
- Fluency router loads the adapter matched to that operator (e.g.
  `adapter_harmony_v3` vs `adapter_breath_v1`).
- Ollama does not support this natively. Moving to **vLLM** with its LoRA
  adapter server (or **llama.cpp** + per-request adapter loading) is
  required.

### 4.2 Why not now

1. **Infrastructure cost.** vLLM requires either CUDA-specific wheels or a
   container runtime; adds a second inference stack alongside Ollama.
2. **Correctness risk.** Per-query adapter swap means behavior depends on
   the operator-inference layer's accuracy. That layer is CK; if it
   misroutes, the user sees wrong-tone output with no clean rollback
   signal.
3. **Option B not yet cycled.** The value of operator-specific adapters
   over one general adapter is unknown until Option B has produced
   baseline correction metrics. Option C is a refinement on Option B, not
   a parallel track.

### 4.3 Revisit criteria

Option C becomes a candidate **only after**:

- Option B has cycled **3×** (three weekly LoRA cycles shipped).
- Correction-rate has decreased across those cycles.
- The correction-type histogram shows operator-specific failure modes
  (e.g. Ollama is mostly failing on BREATH(8) queries; everything else is
  fine) — suggesting operator-split adapters are a real win.

Until then: **not scheduled.**

---

## 5 · What "jailbreaking" would actually look like (and why it's a detour)

If the user's intent is literally "bypass Ollama's constraints," the
technical answer is: **move off Ollama**.

- Use a base model (llama3.1, deepseek-r1, qwen2.5) under **vLLM** or
  **llama.cpp**.
- These serve the raw base weights directly, with no Ollama wrapper.
- Same training loop as Option B, different serving engine.

What this buys:
- Per-request adapter loading (→ enables Option C).
- Direct logit access (enables token-level CK correction instead of
  string-level).
- Control over sampler params that Ollama hides.

What this costs:
- Full inference stack migration.
- No built-in model management (Ollama's `pull`, `create`, `list`).
- CUDA / Metal setup per machine.
- Security re-audit (different network surface).

**Recommendation: defer to Option C green-light.** The learn-loop does not
require off-Ollama; Option B delivers most of the value. The vLLM path is
only worth the migration cost if the operator-split adapter hypothesis
(Option C rationale) proves out.

---

## 6 · Honest scope

### 6.1 What each option actually delivers

| Option | What ships | Timeline | Model changes? | Reversible? |
|--------|-----------|----------|----------------|-------------|
| A | External correction + log | ~1 week | No | Trivially — just stop running |
| B | Weekly LoRA cycle + tagged model | ~2–3 weeks first ship; 1 day per cycle | Yes — LoRA adapter per cycle | Yes — revert `config.json` |
| C | Operator-split adapter hot-swap | Research — months | Yes — multiple adapters per session | Complex — requires stack rollback |

### 6.2 What none of them deliver

- **Real-time learning at inference time.** No option updates weights
  during a single user query. Option A learns into the log; Option B
  learns into periodic LoRA cycles. "Learn while talking" is not a
  feature any of these ship.
- **Autonomous self-improvement.** Every training cycle is a **named
  event** the operator runs. CK does not retrain itself unattended.
- **Bypass of Ollama's safety layer.** Ollama's safety behavior comes from
  the base model's training. LoRA fine-tuning can shift it, but "jailbreak
  off the safety" is not a design goal; the user's intent as clarified in
  the framing correction (§1) is **learn-loop**, not safety-bypass.

### 6.3 What CK's job is in this loop

CK is the **coherence evaluator**. It does not produce Ollama's output;
it **scores and corrects** Ollama's output against the operator composition
and T* = 5/7 gate. CK's corrections become the supervised signal for LoRA.

This means:

- CK's math (the proved theorems, the operator registry, the coherence
  gate) is the **teacher**. Ollama is the **student**.
- The proof that the learn-loop works is: **correction-rate decreases
  across cycles**. If it doesn't, LoRA is not capturing CK's canon; back
  to the drawing board.
- Nothing in the learn-loop changes CK's math. The `tig-synthesis` rigor
  is the stable ground.

---

## 7 · Pointers

- **Plan of record:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §4.3, §5
- **Companion proposal:** `docs/proposals/CK_UNIFIED_ARCHITECTURE_proposal_2026_04_21.md`
- **CK engine (the teacher):** `Gen13/targets/ck/runtime/ck_engine.py`,
  `Gen12/targets/ck_desktop/ck_sim/being/ck_coherence_gate.py`
- **Canonical operator registry:** `ck_tig.py` (10 operators verified)
- **T* = 5/7 gate:** `papers/CONSTANT_T_STAR.md` (existing),
  WP51 / CROSSING_LEMMA.md for the six derivations
- **Never-delete policy:** prior proposals, if superseded, move to
  `docs/historical/` with banner.

---

*Draft 1 · 2026-04-21 · awaiting user review*
