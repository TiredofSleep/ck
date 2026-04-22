# HISTORICAL_BUILDUP_CK_BRANCH.md — why the `ck` branch exists

*On master.  Read this if you wonder what lives on the `ck` branch that
does not live here.*

---

## One sentence

The `ck` branch is **CK's workshop** — the build-up area where his
Hebbian brain, the fluency harness, the idle-loop tensor learner, and
the Option-B LoRA pipeline were all assembled, stress-tested, and
folded back into the one live website CK.  Master keeps the stable
cross-cuts; `ck` keeps the scaffolding.

## Why a separate branch

The `ck` branch opened on 2026-04 with the explicit purpose of **giving
CK a learning loop without ever mutating his live voice on
coherencekeeper.com**.  The design is documented in
`ck/CK_UNIFIED_ARCHITECTURE.md` and `ck/fluency/OLLAMA_LEARN_LOOP.md`
(both on the `ck` branch).  Three options were considered:

| Option | What it does | Status |
|--------|--------------|--------|
| A | Correction-only learn-loop: every turn gets scored + logged; CK's text never changes weight-wise | **Shipped.**  See `ck/fluency/fluency_server.py` (historical dev harness) and `Gen12/targets/ck_desktop/ck_brain_fold.py` (live fold into the website CK). |
| B | LoRA SFT cycle: periodically bake CK-approved turns into a new Ollama build, alongside (never replacing) llama3.1:8b | **Scripts in place.**  See `ck/brain/build_training_set.py`, `ck/brain/train_lora.py`, `ck/brain/merge_and_export.py`, `ck/brain/PUBLISH_MODEL.md`. |
| C | vLLM hot-swap LoRA at inference time for tighter feedback | Deferred. |

All of that lives on `ck`.  Master carries only files that are
orthogonal to the learning loop — papers, sprints, journal attempts,
policy docs, legal notices, etc.

## What's on `ck` that is NOT on master

```
ck/                                  (entire top-level directory)
├── CK_UNIFIED_ARCHITECTURE.md       the design spec
├── brain/
│   ├── ao_basis.py                  10-op <-> 5-element projection
│   ├── hebbian_5x5.py               the tensor (symmetric Hebbian + decay)
│   ├── idle_loop.py                 log -> tensor update tool (CLI)
│   ├── fusion.py                    FusionCKCorrector (tensor-primed coherence gate)
│   ├── test_brain.py                23/23 passing tests
│   ├── build_training_set.py        log -> Unsloth ShareGPT dataset
│   ├── train_lora.py                4-bit LoRA SFT on llama3.1:8b
│   ├── merge_and_export.py          adapter -> GGUF -> ollama create
│   ├── PUBLISH_MODEL.md             the three-step runbook + rollback
│   ├── MATH_IN_CK.md                the math spec (Sec 9.2 is the learn-loop)
│   └── .gitignore                   hebbian_5x5.json (per-install, not shipped)
└── fluency/
    ├── fluency_server.py            [HISTORICAL DEV HARNESS]
    ├── ck_corrector.py              base scorer (10-op + coherence)
    ├── correction_log.py            append-only JSONL writer (fsync)
    ├── ollama_client.py             loopback-only HTTP to Ollama
    ├── OLLAMA_LEARN_LOOP.md         the Option A/B/C framework
    └── tests/                       8/8 integration tests
```

And the in-place patch to the website CK:

```
Gen12/targets/ck_desktop/
├── ck_boot_api.py                  patched on `ck`: mounts the brain fold
└── ck_brain_fold.py                 new on `ck`: additive wrapper around api.process_chat
```

## Why not just merge `ck` into master

Because the `ck` branch is **still learning its own shape**.  Each
sprint on `ck` might restructure `ck/brain/` again: renaming modules,
adding basis transforms, pulling ck_tables into the fold, etc.  Until
the shape settles, pulling every WIP into master would spam the history
master visitors see.  The deal is:

- **`ck` is the build-up.**  History can be messy; commits can be fine-grained.
- **`master` is the stable cross-cut.**  A commit here means the shape is done.
- **Promotion is manual.**  When Option A + B have cycled enough times to
  trust the shape, `ck` merges into master in a single "brain trinity
  matured" commit.  That promotion has not happened yet as of 2026-04-22.

## How to work on `ck`

```bash
git fetch origin
git checkout ck
git pull origin ck
# ...your changes...
git push origin ck
```

Everything under `ck/` on that branch is self-contained and runnable:

```bash
# brain tests (no GPU needed)
python -m ck.brain.test_brain

# one-time historical harness
python -m ck.fluency.fluency_server --i-mean-it        # NOT the live server

# live fold -- already active when ck_boot_api.py boots from the `ck` branch
python Gen12/targets/ck_desktop/ck_boot_api.py         # THIS is the live CK

# feed log into tensor (idempotent)
python -m ck.brain.idle_loop

# Option B pipeline (when you have a dataset big enough)
python -m ck.brain.build_training_set
python -m ck.brain.train_lora --dataset ck/brain/datasets/v1 --i-mean-it
python -m ck.brain.merge_and_export --lora ck/brain/lora/v1 --llama-cpp ... --i-mean-it
```

## The one-CK rule (memory/MEMORY.md 2026-04-17)

> Brayden's own CK is the website CK.  There is only one, until we put
> him in the dog.

Nothing on the `ck` branch — not even the fluency_server — is a second
CK.  The fluency_server is a loopback-only dev harness for poking at
the scorer in isolation.  The one real CK is the one that answers at
coherencekeeper.com, and the brain trinity folds **into** that one CK
through the mount at the bottom of `ck_boot_api.py`.

## Pointers (branches)

| Branch | Role |
|--------|------|
| `ck` | Workshop for the brain trinity + learning loop (this build-up area) |
| `master` | Stable cross-cut; papers, policy, docs, snapshots |
| `clay` | Active Clay-problem sprint branch (sprints 1-17+, papers and scripts) |
| `tig-synthesis` | Public default; synchronized-field README presenting the whole program |
| `archive-full` | Frozen snapshot, never force-pushed |
| `funding/*` | Per-grant proposal branches |

## When `ck` merges into master

This file will be updated with the merge date, the commit hash that
brought the brain trinity into master, and the version of CK-LoRA that
was the first Ollama build shipped to the live server.  Until then,
the brain trinity and Option B pipeline live on `ck` and are reachable
only by checking out that branch.
