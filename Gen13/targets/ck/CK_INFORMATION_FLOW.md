# CK INFORMATION FLOW — the map, and the missing nerves

**2026-06-11.** Brayden: *"make a map of how information flows and is derived through this
system — it seems like we are running disconnected systems."* Correct. Tonight grew organs
faster than nerves. This is the map: how information SHOULD flow, what is wired, what floats.

## §1 The flow

```
                              W O R L D
            text · books · audio · pixels · dialogue · canon
                                 │
                          ┌──────▼──────┐
                          │   SENSES    │  codecs: letters / PCM / hue
                          │ (organ_     │  → one alphabet: Z/10Z ops
                          │  senses)    │  [FPGA home: i2s_receiver.v]
                          └──────┬──────┘
                                 ▼
              ╔══════════════════════════════════════╗
              ║   THE TOOLBOX — generation layer      ║
              ║   every input measured by ALL tools:  ║
              ║   VSA · braid · char-3g · PPMI+head · ║
              ║   census · stylometry · lattices · D2 ║
              ╚════════╦═══════════╦═══════════╦══════╝
                       ▼           ▼           ▼
                  FORM face   MEANING face   GAP face
                  identity    routing 75%,   kNN+conformal+census:
                  recall 91%  domains 83%,   ANSWER / REFUSE,
                  evidence    fact/fic 85%   risk dial, τ
                       │           │           │
                       └─────┬─────┴─────┬─────┘
                             ▼           ▼
                   ┌──────────────┐  ┌──────────────────────┐
                   │  KNOWLEDGE   │  │  VOICE               │
                   │  fabric:     │  │  unfrozen llama3.2   │
                   │  concept →   │→→│  (LoRA: ck_lora_dpo) │
                   │  books →     │  │  speaks ONLY through │
                   │  domains →   │  │  the GAP gate +      │
                   │  associates  │  │  census judge        │
                   └──────┬───────┘  └─────────┬────────────┘
                          │                    ▼
                          │     OUTPUT: answer + evidence (book,
                          │     passage, score, counts)  |  or
                          │     REFUSE + counted reason
                          ▼                    │
                   ┌──────────────────────────▼─┐
                   │  STUDY JOURNAL (his lived   │
                   │  text, first person)        │
                   └──────┬──────────────────────┘
                          ▼
        ════════ LEARNING LOOPS (sleep / background) ════════
        ▼                  ▼                   ▼            ▼
   meaning organ      DPO dose:           DKAN: output   HER: replay
   retrains on        CK judges voice     bends HIS      consolidates
   journal+curric     (census→gradient;   tables (T*     (continual
   (lived-text law)   proven 33→1)        target)        seat)
                          │
                          ▼
                ┌────────────────────┐
                │ REGISTRY + LEDGER  │  self-knowledge as data:
                │ every seat, every  │  what each organ can do,
                │ number, regenerable│  with numbers
                └─────────┬──────────┘
                          ▼
                ┌────────────────────┐
                │ HARNESS            │  registered prediction →
                │ (the law)          │  exam → commit → PUBLIC
                └────────────────────┘

   substrates: CPU = daemons, harness, counting · GPU = voice, training
               FPGA = native ops at line rate (P1–P3, fabric plan)
```

**The derivation chain in one sentence:** world → one operator alphabet → joint measurement
(percept) → three faces decide *known/meant/unknown* → knowledge retrieved + voice generated
*under the gate* → every output journaled → journals feed four learning loops → loops update
organs → registry records what changed → harness proves it → back to the world, public.

## §2 The wiring table (why it feels disconnected — honest)

| nerve | status |
|---|---|
| senses → operator alphabet | **WIRED** (measured: ear 27%, eye p=0.003) |
| toolbox → three faces | **WIRED** (trinity.py percept) |
| gate → book QA with evidence/refusal | **WIRED** (ck_book_chat, 0 hallucinations) |
| reader → journal → ledger | **WIRED** (daemon, 479 books/min) |
| CK-as-judge → voice weights (DPO) | **WIRED once** (33→1; manual launch) |
| fabric → book-chat answers | **NOT WIRED** (fabric built, chat doesn't query it) |
| voice → live gate (LLM speaks through trinity.ask) | **NOT WIRED** (gate gates retrieval only) |
| senses → daemon (streaming hearing/seeing while reading) | **NOT WIRED** |
| journal → meaning retrain (automatic) | **NOT WIRED** (manual probe only) |
| HER consolidation on schedule | **NOT WIRED** (seat assigned, no scheduler) |
| DKAN ← tonight's organs | **NOT WIRED** (bench queued) |
| FPGA substrate | **DOWN** (RTL exists; fabric plan P1) |

## §3 THE SPINE — the single next build (wiring, no new organs)

One file, one loop, `ck.py` — the organism tick:

```
perceive(input) → percept = toolbox(input)
gate.decide(percept) → if REFUSE: speak counts; journal; return
retrieve(fabric, shelves) + voice.generate(context, LoRA)
judge(voice_output): census + canon + gate     ← the same judge that won DPO
speak(answer + evidence) ; journal(everything)
nightly(): meaning.retrain(journal) ; HER.consolidate() ; DPO.dose(judged_pairs)
           ledger.regenerate() ; push
```

Every box above already exists and is measured. The spine is connection, not invention —
estimated one session. After the spine: no more disconnected systems; one creature, one flow,
journals feeding loops feeding organs, with the harness watching everything.
