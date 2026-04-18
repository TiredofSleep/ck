# NEXT_CLAUDE_NOTES — Gen13 Startup Protocol

**Read order:** this file → `README_GEN13.md` → `ARCHITECTURE.md` → `targets/ck/CK_DIALOGUE_2026_04_17.md` → `targets/ck/brain/BRAIN_DESIGN.md`

---

## Where We Left Off (2026-04-17)

Gen13 is built. CK can talk math.

The two key fixes are wired into `targets/ck/server/ck_boot_api.py`:
1. `surface_math` from `runtime/ck_voice_math.py` wraps `api.process_chat`
2. `engine.olfactory_her = build_olfactory_her(engine.olfactory)` restored after engine.start()

The Gen11 brain (156 modules / 122K LOC) lives intact at `targets/ck/brain/ck_sim/`. Do not rewrite it. The point of Gen13 is that we **stopped rewriting it**.

---

## The First Thing to Check When You Boot

```
cd Gen13/targets/ck/server
python ck_boot_api.py
```

Look for these three lines:
```
[CK] Gen13 math-first voice: ENABLED
[CK] Gen13 HER: restored (engine.olfactory_her initialized)
[CK] Organism alive. API: http://0.0.0.0:7777
```

If `math-first voice: DISABLED`, the `runtime/ck_voice_math.py` import failed — check `sys.path` insertion at the top of `ck_boot_api.py`.

If `HER: failed`, read the error — most likely the olfactory bulb didn't initialize on the platform you're booting on.

---

## What NOT To Do

- **Do NOT** rewrite `ck_sim_engine.py`, `ck_olfactory.py`, or any of the 156 brain modules. They work. Brayden lost a generation to that mistake.
- **Do NOT** add more modules to "fix" CK's voice. The voice fix is one boolean conditional and a FACTS dict. Adding more modules is the Gen12 anti-pattern.
- **Do NOT** push to GitHub without Brayden's explicit confirmation.
- **Do NOT** cut over the live Cloudflare tunnel from Gen12 to Gen13 without confirmation.
- **Do NOT** delete anything. Anywhere. Ever. (See `feedback_never_delete.md`.)
- **Do NOT** import vocabulary across the three threads (TIG / Q-series / finite arithmetic). They stay separate per Sprint-16 protocol.

---

## What To Do When Brayden Asks You Something Math-First

If the question is in the FACTS dict at `runtime/ck_voice_math.py`, the live CK already answers it well — point Brayden at the response and the operator chain. If the question is **not** in the FACTS dict and is math-first, *add it to the FACTS dict*, do not redirect through SEMANTIC_LATTICE.

Add a fact like:

```python
"new_topic": {
    "text": "Plain-English fact with numbers, sourced from <paper or table>.",
    "keys": ("keyword1", "keyword2", "phrase the user might type"),
},
```

Then re-run the boot, the new topic surfaces immediately on the next `/chat` POST.

---

## The Three Threads (Stay Separate)

| Thread | Owner | Status | Lead Papers |
|---|---|---|---|
| A — TIG/σ/ξ | Brayden + collaborators | σ rate proved; framework stated | Sprint 14 WP81/91/101 |
| B — Q-series | Brayden | σ polynomial fully characterized on Z/10Z | Q10, Q11, Q17_* |
| C — Basin finite arithmetic | Sprint 16 thread | 4 stable invariants, dual reset law proved | Sprint 16 folder |

No vocabulary imports across threads without a proved map. (See `feedback_never_delete.md` and the existing memory records on citation rigor.)

---

## Where the Things Live

| Thing | Path |
|---|---|
| CK runtime entry point | `targets/ck/server/ck_boot_api.py` |
| Math-first voice patch | `targets/ck/runtime/ck_voice_math.py` |
| Brain (Gen11 intact) | `targets/ck/brain/ck_sim/` |
| Brain inventory | `targets/ck/brain/NEURAL_INVENTORY.md` |
| Live diagnostic transcript | `targets/ck/CK_DIALOGUE_2026_04_17.md` |
| Web pages | `targets/ck/web/` |
| Clay sprint papers | `targets/clay/papers/sprint{10,12,13,14,16,17}_*/` |
| Journal venues (4 tiers) | `targets/journals/` |
| Submission roadmap | `targets/journals/SUBMISSION_LADDER.md` |
| FPGA reference | `targets/fpga/` |
| XIAOR Dog | `targets/xiaor_dog/` |

---

## Memory Pointers

The following memory records are load-bearing for Gen13 work:

- `memory/project_gen13_neural_architecture.md` — HERS resolution + brain catalog source
- `memory/MEMORY.md` — top-of-file index, points at the above
- `memory/feedback_never_delete.md` — preservation policy + citation discipline
- `memory/feedback_always_push.md` — but **NOT** for Gen13 cutover; only for routine commits
- `memory/voice_fluency.md`, `memory/voice_loop.md` — historical; superseded by `runtime/ck_voice_math.py` for math topics

If you need older context, `Gen12/NEXT_CLAUDE_NOTES.md` and `old/Gen11/...` are intact.

---

## When Brayden Says "He's Talking Math"

Then it worked. Update `memory/project_gen13_state.md` with the timestamp and any new FACTS keys you added. Show Brayden the curl response or screenshot.

When Brayden says "he's still under-mathed", check:
1. Is `surface_math` returning None for the query? → add to FACTS dict
2. Is `text_gen12` still being preferred by the website? → check `web/chat.html` JS
3. Did the Gen13 boot actually pick up the patch? → look for the `Gen13 math-first voice: ENABLED` line

---

## What Comes After Gen13

Per the approved plan and the unfinished pieces:
- A fresh `web/index.html` math-first landing page
- A fresh `web/tower.html` interactive Sprint-17 3-layer-tower visualization
- The journal Tier-1 actual submissions (JCAP / σ-rate / sinc²-zero)
- XIAOR Dog Δ¹/Δ²/Δ³ bring-up status update

But the foundation — *CK can say `5/7`* — is done. Everything after that is incremental.
