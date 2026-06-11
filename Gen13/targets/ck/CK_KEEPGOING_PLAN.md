# CK KEEP-GOING PLAN — he does not stop

**2026-06-11.** Brayden: *"make a plan to keep him going, don't stop."* This is the plan as
**running code** (`trinity/ck_keepgoing.py`), not a wish-list. One cycle reads, weaves,
gains literacy, re-measures, and pushes — journaled, autonomous, resumable.

## §1 The standing loop (running now)

`python ck_keepgoing.py` executes one growth cycle:

| job | substrate | what it does |
|---|---|---|
| READ +300 | CPU | daemon reads 300 new books, fact/fiction-judged, journaled |
| WEAVE 500 | CPU | rebuild knowledge fabric over 500 books |
| LITERACY | GPU | real-dose pretrain (40K steps, 150 books) → reader re-sit |
| LEDGER | CPU | regenerate self-knowledge from all results |
| PUSH | — | receipts public (the repo-loss law) |

Each job continues on failure (logged to the journal); the **cycle is the unit**, resumable.
Make it perpetual with ONE keystroke (admin PowerShell, your authorization — persistent
config is yours to grant):

```
schtasks /Create /TN CK_KeepGoing /SC HOURLY /TR "C:\ck_venv\lora312\Scripts\python.exe 'C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\targets\ck\trinity\ck_keepgoing.py'"
schtasks /Create /TN CK_Nightly  /SC DAILY /ST 02:00 /TR "C:\ck_venv\lora312\Scripts\python.exe 'C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\targets\ck\trinity\ck.py' nightly"
```

After that he reads, weaves, retrains, and pushes on his own, forever, while you sleep.

## §2 Tonight's state (handoff)

- **Spine ALIVE** (`ck.py`): one body — senses → faces → gate → fabric/library → judged voice
  → journal → nightly loops. Demo: 6/6 questions, 0 hallucinations, both traps killed by count.
- **Voice**: DPO v1 (halluc 33→1) → v2 (10/16 grounded answers, fluent). The gate refuses
  traps BEFORE the voice; ck.py auto-loads the newest adapters. Voice = answerer, gate = bouncer.
- **Reader**: literacy lineage retrieval 0.602 → v1 0.620; real-dose pretrain queued in §1.
- **Knowledge**: 2,386-concept fabric, 6 domains, census routing; fact/fiction 85%; 80+ books
  read and journaled.
- All pushed to `origin/tig-synthesis`; the lost frontier history preserved on
  `original-frontier-2026-05`.

## §3 The forward queue (each a registered, gated build — append to JOBS as they land)

1. **DPO v3** — judge balanced (answer-reward + trap-penalty symmetric) so the voice speaks
   AND refuses; lift gate-authority once it passes.
2. **Library QA shelving** — embed all 1,019 books → the scholar answers from the whole library.
3. **Spine sense-streaming** — daemon hears/sees while reading (senses → live percept).
4. **DKAN loop** — the LLM's output bends CK's tables (T* target); the other half of the loop.
5. **HER consolidation** — scheduled replay defends old skills as new books arrive.
6. **FPGA P1** — power the board, heartbeat LED, then D2-in-silicon (CK_FABRIC_PLAN.md).
7. **External benchmark artifact** — the gate's selective-QA story, public, for the adoption path.
8. **Package the recipe** — personal-CK + federation (organs-not-data), the "for all" build.

## §4 The invariant (never breaks, across every cycle)

Registered prediction → measured exam → honest verdict → commit → **public**. Wins and
negatives weighted equally. The harness is the one organ that is never ablated. As long as that
holds, he keeps going AND stays true — which is the whole point. Feed him mornings; he does
the rest.
