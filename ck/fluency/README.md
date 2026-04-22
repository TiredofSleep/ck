# ck/fluency — CK Ollama Learn-Loop (Option A)

Status: `[ACTIVE — ck BRANCH; OPTION A SCAFFOLDING 2026-04-21]`

This directory is the implementation of the Ollama learn-loop Option A
design described at `ck/OLLAMA_LEARN_LOOP.md` §2.  CK acts as the
**deterministic teacher** for a local Ollama model, with learning
captured in an append-only JSONL log rather than by modifying model
weights.

---

## What's here

| File | Role |
|---|---|
| `ollama_client.py` | Loopback-only urllib wrapper around `/api/generate`. |
| `ck_corrector.py` | Deterministic scorer + 5-way classifier against T\* = 5/7. |
| `correction_log.py` | Append-only, fsynced, daily-rotated JSONL log. |
| `fluency_server.py` | Flask endpoint `/fluency/chat` with `--i-mean-it` gate. |
| `eval/eval_set.jsonl` | 20 curated cases for regression checks. |
| `eval/eval_runner.py` | Runs the eval set, reports type / flag / dominant-op hits. |
| `logs/` | Created on first write. Contents are git-ignored. |

Launch wrapper: `scripts/START_FLUENCY_SERVER.bat` (G6 hands-on-wheel).

---

## The math the loop uses

The teacher layer implements five concrete math pieces from CK's corpus
(see `ck/brain/MATH_IN_CK.md` for the full map):

1. **T\* = 5/7** (`Fraction(5, 7)`) — the crystal gate. Every response
   is compared against this rational.
2. **10-operator registry** — `VOID LATTICE COUNTER PROGRESS COLLAPSE
   BALANCE CHAOS HARMONY BREATH RESET`, with regex detectors.
3. **Coherence scalar** — weighted activation sum squashed to `[0, 1]`
   (constructive = +1, disruptive = −1, neutral = 0).
4. **Crossing Lemma / COLLAPSE / CHAOS detectors** — self-contradiction
   (word + "not word" in one sentence) and topic drift (Jaccard < 0.05
   between adjacent sentences) are diagnosed as their own operators.
5. **UOP 5-way classification** — `none / soften / strengthen / reframe
   / reject` based on dominant operator × coherence vs T\*.

The correction is **never written as prose in CK's voice** — per
`memory/feedback_dont_ventriloquize_ck.md` HARD RULE. What the user sees
is Ollama raw + a deterministic annotation block that names the problem.

---

## Running

### Prereqs

1. Ollama serving locally: `ollama serve` (leave this in a window).
2. Model pulled once: `ollama pull llama3.1:8b`.
3. Python env with Flask: `pip install flask`.

### Self-tests (no Ollama needed)

Each module has a self-test that runs independently:

```powershell
python ck\fluency\correction_log.py   # exercises the log primitive
python ck\fluency\ollama_client.py    # probes reachability; prints pong if live
python ck\fluency\ck_corrector.py     # prints classification for 6 samples
```

### Eval set (no Ollama needed)

```powershell
python ck\fluency\eval\eval_runner.py
python ck\fluency\eval\eval_runner.py --verbose
python ck\fluency\eval\eval_runner.py --strict
```

Current green state: **20/20 flag match, 19/20 strict type match, 20/20
dominant-op match** (green threshold: ≥ 16/20 flag match per
`OLLAMA_LEARN_LOOP.md` §2.3).

### The server

Preferred launcher (hands-on-wheel):

```powershell
scripts\START_FLUENCY_SERVER.bat
```

Direct (for developers):

```powershell
python -m ck.fluency.fluency_server --i-mean-it --host 127.0.0.1 --port 7778
```

`--i-mean-it` is **required**. Without it the server refuses to start.
This is the G6 guard that prevents accidental boot.

### Endpoints

| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/health` | — | `{ok, ollama_reachable, model, T_star}` |
| POST | `/fluency/chat` | `{query, model?, temperature?, system?}` | see below |
| GET | `/fluency/stats` | — | today's per-correction-type counts |

`/fluency/chat` response:

```json
{
  "ok": true,
  "ollama_raw": "…",
  "ck_correction_type": "none|soften|strengthen|reframe|reject",
  "coherence": 0.xxx,
  "dominant_op": "HARMONY",
  "rendered": "ollama raw (plus annotation if correction_type != none)",
  "annotation": "[CK-PASS] dominant=HARMONY coherence=0.750 gate=0.7143 — approved",
  "rationale": "coherence 0.750 >= T*=0.7143; gate passes",
  "model_tag": "llama3.1:8b",
  "elapsed_ms": 9730,
  "T_star": "5/7"
}
```

### Example request

```powershell
curl -s -X POST http://127.0.0.1:7778/fluency/chat `
     -H "Content-Type: application/json" `
     -d "{\"query\":\"explain the crystal gate\"}"
```

---

## Scope limits (hard)

These are lifted verbatim from `ck/CK_UNIFIED_ARCHITECTURE.md` §3.4 and
`ck/OLLAMA_LEARN_LOOP.md` §6:

- **Loopback only.** `OllamaClient.__init__` raises `ValueError` for any
  host not starting with `http://localhost` or `http://127.0.0.1`. The
  server refuses any `--host` other than `127.0.0.1` or `localhost`.
- **No model modification.** Option A does not fine-tune, LoRA, or
  alter the Ollama model in any way. The ‘learning’ is the log.
- **No autostart.** No service, no scheduled task, no tray icon. You
  start it, you stop it.
- **No outbound calls.** The server talks only to Ollama (local) and the
  log (local filesystem).
- **No tunnel cutover.** The production Cloudflare tunnel at
  `coherencekeeper.com` is not touched by anything in this directory.
- **No deletion.** The log is append-only with fsync per write.
  Daily-rotated; old days are never rewritten.

Option B (LoRA-consolidation cycles) and Option C (experimental fusion)
remain on paper in `ck/OLLAMA_LEARN_LOOP.md` §§3–4. Neither is
implemented here.

---

## Log format

Each `/fluency/chat` call appends one JSONL line under
`ck/fluency/logs/corrections_YYYY_MM_DD.jsonl` (UTC-rotated, fsynced):

```json
{
  "t": "2026-04-21T19:33:12+00:00",
  "query": "…",
  "ollama_raw": "…",
  "ck_score": {
    "coherence": 0.75,
    "dominant_op": "HARMONY",
    "operator_profile": {"VOID": 0.0, "LATTICE": 0.5, "…": "…"}
  },
  "ck_correction_type": "none",
  "ck_corrected": "…rendered string…",
  "rendered": "ollama_raw+annotation",
  "model_tag": "llama3.1:8b",
  "elapsed_ms": 9730
}
```

Reading yesterday's log:

```python
from ck.fluency.correction_log import CorrectionLog
from datetime import datetime, timezone, timedelta

log = CorrectionLog()
yesterday = datetime.now(timezone.utc) - timedelta(days=1)
rows = log.read_day(yesterday)
print(len(rows), "interactions yesterday")
```

---

## How this connects back to CK

The log is the interface between the fluency loop and CK's Hebbian 5×5
memory. In a future pass (`ck/brain/hebbian_5x5_cl.py`), the idle loop
will read the log, decompose each entry's operator profile into the
5-element AO basis, and strengthen the 5×5 tensor links that co-fired.
That's how Ollama's output *teaches* CK without ever touching the
model's weights.

Cross-refs:
- Architecture: `ck/CK_UNIFIED_ARCHITECTURE.md`
- Design: `ck/OLLAMA_LEARN_LOOP.md`
- Math map: `ck/brain/MATH_IN_CK.md`
- Governance: `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §4 (G-rules)
- Canon T\*: `papers/CONSTANT_T_STAR.md` on `tig-synthesis` branch
