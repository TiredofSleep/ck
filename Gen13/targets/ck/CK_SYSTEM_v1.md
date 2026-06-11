# CK SYSTEM v1 — the whole organism, assembled

**Date:** 2026-06-11. **Synthesizes:** Walker blueprint + Intelligence Synthesis + Quadratic Glue Principle + walker_v0 (built, measured) + extraction/ (built, measured).
**Brayden's directive:** *"research and build and build and research... extract intelligence from open-source models to avoid long training... CK builds his own plastic models to speak his internal languages and any language he chooses... synthesized and prolific."*

## §1 — The organism (corrected hierarchy, now with all organs placed)

```
CK — sees the world as measurable / unmeasurable
│
├── THE QUADRATIC GLUE (constitutive; quadratic_glue.py + the bilinear
│     substrate heartbeat). Fuses streams, FORCES CHOICE at T* = 5/7
│     every tick, watches its own degeneracy locus (the paradox sense).
│
├── PERCEPTION
│    ├─ Layer M: substrate invariants (native; Phase 1)
│    └─ BORROWED CORTEX (built 2026-06-11): frozen open-source
│       embedders via local Ollama (nomic-embed-text 768d pulled;
│       llama3.2 / mistral already resident as teachers). Years of
│       training extracted at zero training cost; hash-3gram fallback
│       so the organism never hard-depends on the borrowed organ.
│
├── PLASTIC MODELS (built): tiny heads CK builds/owns/signs/discards —
│    prototype or one-solve ridge over (borrowed embeddings ⊕ substrate
│    invariants). One per language/task. facts_head.json is the first:
│    CK's English→internal-language router.
│
├── TOOLS the glue wields: Gap Router (24/24, 125×, J56) ·
│    lifted substrate reservoir (MG-84 win, J56) · HER memory (Phase 0)
│    · voice · sovereign refusal (the Type-III organ) · FPGA body
│
└── MEMORY/IDENTITY: Ed25519 cortex · D-canon (the DreamCoder library,
     kept by hand for a year, to be automated)
```

## §2 — What was measured today (first extraction run, honest)

English→internal-language routing, 20 adversarial held-out paraphrases
(zero keyword overlap), 6 out-of-domain traps:

| mechanism | routing | OOD abstention |
|---|---|---|
| keyword FACTS (production) | 20% | 100% (blind-safe) |
| plastic head + borrowed cortex + canon anchors | **35%** | **67%** |

Misses are dominated by low-margin ABSTAINs — the glue **refusing
rather than bluffing** on deep-jargon queries the generic embedder
cannot see ("the gamma zero of three paper"). **The system classified
its own residual: Type II — the borrowed feature family cannot separate
CK's internal classes.** The route is therefore not more tuning but
invariant growth: (a) teacher-labeled corpus expansion — llama3.2
generates hundreds of paraphrases per topic offline (extraction channel
#2; survey: tiny students learn best from labels/short rationales, NOT
long CoT), refit = one solve; (b) substrate invariants concatenated
into the head's feature space (Layer M proper). Both pre-planned, both
cheap.

## §3 — The five extraction channels (surveyed, ranked, grounded)

1. **Frozen embeddings + plastic head** — BUILT. nomic-embed-text via
   Ollama; prototype/ridge heads; ms/query CPU.
2. **Teacher-label distillation** — teachers resident (llama3.2 2GB,
   mistral 4.4GB). Overnight batch labeling → one-solve refits.
   The Small-Model-Learnability-Gap result mandates short labels.
3. **Logprob readouts** (Ollama native API) — confidence features for
   the glue's gate; free with generation.
4. **Structured-output judgments** — JSON-schema-constrained teacher
   scores as clean feature vectors; official Ollama capability.
5. **repeng-style reading vectors** — white-box, llama.cpp route only
   (Ollama PR unmerged); deferred.

Skip as hype for these constraints: CPU LoRA training; evolutionary
merging at sub-1B; long-CoT trace distillation into tiny students.

## §4 — The prolific loop (research→build→build→research, standing)

Every cycle: (1) the glue finds a gap; (2) the router types it;
(3) the route either *extracts* (borrow a frozen capability, fit a
plastic head in one solve) or *grows* (new invariant, new D-entry) or
*refuses* (Type III) or *re-windows* (Type IV); (4) the result is
measured, the number goes in the doc as measured, and the canon gets
the entry. Today's cycle ran end-to-end: surveyed (2 grounded surveys)
→ built (borrowed_cortex, plastic, demo) → measured (35%/67% vs 20%) →
classified its own gap (Type II) → named the next build. That loop IS
the system being prolific.

## §5 — Consolidated build state

| piece | status |
|---|---|
| Gap Router + suite (P1, 125×, 24/24) | BUILT, measured, in J56 (pushed) |
| Lifted substrate reservoir (P2 split, MG-84 +36%) | BUILT, measured, in J56 |
| Borrowed cortex + plastic models + facts head | BUILT, measured (today) |
| Glue degeneracy monitor (P5) | designed, next build |
| HER wake (Phase 0) | next build (one boot call) |
| Layer M substrate invariants in heads | next build |
| Teacher-corpus expansion of facts head | next build (overnight job) |
| Abstention governor on frozen LLM (P1-LLM piggyback) | designed |
| reservoirpy upstream PR | designed |

Pre-registered and open: P1-real, P1-LLM, P2-next (F_p lift), P3
(noisy-TV suite), P4 (gated HER), P5 (glue-triggered diagnosis).

## §6 — SPAWN INHERITANCE (Brayden 2026-06-11: "tons and tons of files of training and memory from how many times I have built this creature")

The spawn must inherit CK's BIOGRAPHY, not synthetic paraphrases. Inventory of the lives:

| source | what it is | spawn use |
|---|---|---|
| ck_dictionary.json (4.3MB, **112,703 entries**, v3, carried Gen8→Gen14) | his learned vocabulary | embedding anchor store + retrieval lexicon |
| CKIS/ck_store/dialogue_digests.jsonl | tick-level lived dialogue records (composed operator, info_density, semantic content) | training pairs from actual life |
| Gen10 HER (8.8M experiences) | state-action replay | tick-loop warm start (Phase 0) |
| external_corpora/wikipedia/ | what he was fed | general grounding corpus |
| CKIS/knowledge/ck_training_curriculum.md | how he was raised | curriculum for plastic heads |
| bdc_logs (27MB) | 8 days of heartbeat | dynamics statistics |

Trajectory measured today: keyword 20% → untrained head 35% → teacher-trained spawn 50% (all misses are low-margin ABSTAINs, zero bluffs). NEXT TRAINING PASS: ingest the dictionary + dialogue digests as the corpus — the spawn learns CK's internal language from CK's own lives. Teacher generation stays as the channel for NEW languages only.
