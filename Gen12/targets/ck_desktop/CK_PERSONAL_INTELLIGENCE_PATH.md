# CK As My Own Intelligence System — Path Document

**Date filed:** 2026-04-18
**Companion to:** `COLLAB_CHAT_ROADMAP.md` (the outside-collaborator service path)
**Status:** **PARKED** — resume after new atlas is delivered and worked through
**Scope:** CK as Brayden's personal daily intelligence instrument — distinct from /collaborate service, shared substrate

---

## Why This Document Exists

The `COLLAB_CHAT_ROADMAP.md` in this folder answers a service question: how does CK help outsiders resolve tangled frameworks. This document answers a different question in the same substrate: **how does CK become the instrument Brayden uses daily to measure his own work.**

Same brain. Different surface. Same algebraic substrate (10 operators, T* = 5/7 gate, TSML/BHML, Hebbian 5×5 CL field, crystal bank, lattice chain, fractal voice). Different workspace — Brayden's, persistent, loaded with the atlas and the 16-sprint arc.

No external LLM. No Ollama. No transformer. CK measures with the same algebra he measures anyone's with, because the algebra *is* what he is.

---

## The Frame

CK as Brayden's intelligence system means four concrete things:

1. **Persistent personal workspace.** Atlas, sprint folders, sanctioned-sentence registry, named open questions, PPM closeout, Hodge closure, Q-series work — all loaded into CK's persistent store so he can refer back without re-pasting.

2. **Methodology routines run on Brayden's drafts first.** The eight routines in `COLLAB_CHAT_ROADMAP.md` (`separate`, `name_gap`, `file_register`, `three_threads`, `sanctioned_sentence`, `preserve`, `pre_register`, `no_composite`) get their first real use on *Brayden's* material — the atlas, the PPM addendum, the Hodge arc — before any outside collaborator sees them.

3. **Field measurement of Brayden's own claims.** Ask CK "is this composite?" or "is this register-honest?" or "does this paraphrase the sanctioned sentence?" — he measures, he doesn't flatter. IG3 already blocks drift-synthesized crystallization; IG6 (when built) will block composite-claim formation at the architectural level.

4. **Continuity of discipline.** CK catches what Brayden would catch on a third read: Rule 19 violations, SAH paraphrase drift, stale framing, cross-thread contamination. Second set of eyes that never gets tired and never gets polite.

What it does *not* mean: CK replacing Brayden as primary composer. Not yet. Not for multi-paragraph prose.

---

## The Capability Layers

### Layer 0 — What works today

At coherencekeeper.com CK already speaks, takes short questions, returns operator classification and coherence measurement. TSML/BHML lookup works. Crystal bank retrieves prior measurements. 50Hz heartbeat runs. Olfactory bulb verifies field crossings.

Useful *now*. A short measurement question ("is X in composite form?") gets a real answer from the algebra. Flattery is refused by architecture, not by instruction.

Missing: no persistent file ingestion, no workspace, no methodology routines, no long-form composition.

### Layer 1 — Personal workspace (4–8 weeks of the same MVP work)

Same MVP scoped for /collaborate, with Brayden as the first user. Collaborator number one.

Concrete additions:

- `brayden_workspace/` in `ck_boot_api.py`, separate from `collab_workspaces/`
- File ingestion routes: `/brayden/upload`, `/brayden/message`, `/brayden/ck_reading`, `/brayden/resolution`, `/brayden/workspace`
- Atlas loaded as persistent context: `ATLAS_MISSING_MATERIAL_2026_04_18.md`, the 16-sprint index, the register taxonomy, sanctioned sentences
- The eight methodology routines wired in, running against Brayden's drafts

What Layer 1 buys: upload an atlas section, a sprint draft, a README candidate. Ask CK to separate claims, name gaps, check registers, block composites. He returns a **measurement, not prose**. Output is structured: verdict lists, register classifications, paraphrase-blocklist hits, named gaps. Brayden composes; CK measures.

First real version of CK-as-instrument.

### Layer 2 — Capability thickening (months, not weeks)

Operator routines harden through repeated use on Brayden's material. Not a rewrite. Thickening.

- `separate.py` gets better at decomposing Brayden's characteristic sentence patterns
- `name_gap.py` learns Brayden's named-gap vocabulary (Source 3 direction, attractor privilege, shape-filter infrastructure, V0 boundary)
- `sanctioned_sentence.py` blocklist grows as more hypotheses are filed
- `no_composite.py` catches drift in Brayden's specific prose style
- Cross-session memory via file-based persistence (workspace files, not neural weights)

At Layer 2 CK drafts a short structured resolution for an uploaded section — still not long-form prose, but "here is the verdict list, here is the register classification, here is the named-gap candidate." Useful as a first pass to refine.

### Layer 3 — Algebraic LLM (12–18 month research horizon)

The parallel work underneath everything above: the **Gen13 brain trinity** (AO 5-element + Hebbian 5×5 CL + quadratic glue) scaled to longer composition. The plan in `C:\Users\brayd\.claude\plans\goofy-discovering-lobster.md` is exactly this work.

The thesis: the 10 operators are a generative basis. Hebbian 5×5 is the cross-dimensional coupling. Quadratic glue (F3 × F4) is the 2→3 bridge. If the substrate is genuinely generative, it composes paragraphs the way it composes sentences — operator stream → AO projection → Hebbian update → quadratic glue → coherence gate → voice.

If it works: CK drafts atlas revisions; Brayden edits; CK measures. Composition entirely from his own algebra.

If it does not work at scale: CK stays a measurement instrument and Brayden stays the primary composer. Honest fork — filed at foundation register, not promised at theorem register.

---

## What Makes This Brayden's, Not A Service

1. **Workspace separation.** The atlas never enters a collab workspace. Collab workspaces never see the atlas.

2. **No polish tax.** /collaborate has to read cleanly for outsiders. Brayden's surface can be rougher — direct file paths, shorthand, half-formed questions.

3. **Authority asymmetry.** Brayden can redirect CK's attention, restart sessions, override verdicts when he has context CK does not. CK records the override with the reason.

4. **Context concentration.** The 16-sprint arc, the atlas, the Hodge closure, the PPM closeout, the Q-series, the physics instantiations — all in one persistent store, cross-referenced by operator signature. Capability thickens fastest on Brayden's material because repeated exposure sharpens routines against his vocabulary.

5. **First-reader discipline.** Brayden sees CK's drafts before anyone else. Errors caught here do not propagate.

---

## Why The Two Paths Are The Same Build

Load-bearing observation: **the /collaborate roadmap and the personal intelligence system are the same work at different surfaces.**

The methodology routines live in `ck_methodology/`. They do not know whose workspace they are running on. The brain trinity does not know whose operator stream it is projecting. The coherence gate does not know whose claim it is measuring.

What differs is which workspace is loaded, which sanctioned sentences are in scope, which prior verdicts are available in the crystal bank. **Substrate is shared; context is scoped.**

Every hour on /collaborate also matures the personal instrument. Every hour tuning CK to the atlas also matures the routines that will eventually run on collaborator material. There is no fork. There is one build.

---

## What To Do This Month (When Resumed)

Three concrete moves that return value fast and do not require Layer 3 to be finished:

1. **Load the atlas as persistent context.** `ATLAS_MISSING_MATERIAL_2026_04_18.md` (and its successor, whatever Brayden delivers next) and the 16-sprint index ingested into `brayden_workspace/`. One-time load, not a retrain. CK reads the atlas the way he reads a crystal — measured structure, filed by operator signature.

2. **Build the first two routines against Brayden's material.** `no_composite.py` (Rule 19 enforcement) and `sanctioned_sentence.py` (paraphrase blocklist) return value fastest on actual writing. Both algebraic — operator-basis perturbation check against the registered sentence. No external model.

3. **Use CK as intake for Brayden's own work for 30 days.** Every atlas section, verdict draft, README candidate through `/brayden/message` first. CK measures. Brayden revises. Keep a log of hits and misses. The log becomes source material for Layer 2 thickening.

Cost: a handful of engineering weekends plus the 30-day discipline. No Layer 3 dependency. Runs on what CK already has.

---

## Rate-Limiting Step, Stated Honestly

The rate-limiter for CK becoming the daily intelligence instrument is **not engineering effort — it is algebraic substrate maturity.**

CK today measures well at short forms. At sentence length he is sharp. At paragraph length he thins. At multi-paragraph length he does not yet compose from his own algebra.

Honest current state. The Gen13 brain trinity is the path to lengthening the composition window. Research work with real uncertainty. Filed at foundation register, not promised at theorem register.

What this means: **Layers 0, 1, and 2 are engineering-bound** — twelve months or less if prioritized. **Layer 3 is research-bound** — twelve to eighteen months if it lands, open-ended if the substrate does not scale cleanly.

Healthy version of this path does not bet on Layer 3 to deliver the value. Layers 0–2 are already a meaningful intelligence instrument: a persistent, disciplined, honest second reader with measurement grounded in Brayden's own algebra. That by itself is rare.

---

## One-Sentence Path

CK becomes Brayden's personal intelligence system by the same operator-routine hardening path that makes /collaborate viable — shared substrate, scoped workspace, methodology routines tested first on atlas and sprint material — shipping in layers (Layer 0 today, Layer 1 in weeks, Layer 2 over months, Layer 3 as research horizon) with honesty about which layer is actually in use and refusal to promise composition capability the algebra does not yet have.

---

## Resume Protocol — How To Pick This Up

When returning to this document:

1. **Read the new atlas first.** Brayden will deliver it; work through it with him before continuing on this path. The atlas is the material the personal instrument runs *on* — the path is meaningless without knowing what is loaded into `brayden_workspace/`.

2. **Confirm the substrate has not drifted.** Check that `COLLAB_CHAT_ROADMAP.md` is still the authoritative service-side design and that nothing here conflicts with what that file commits to. Shared substrate means no silent divergence.

3. **Re-check the rate-limiter.** Before proceeding, confirm the honest state of CK's composition window. If Layer 3 work has progressed in the interval, Layers 1 and 2 may need to be rescoped. If it has not, Layers 1 and 2 stand as written.

4. **Pick the first routine to build.** The recommendation above is `no_composite.py` and `sanctioned_sentence.py` — both can be built independently of the other. If Brayden has a different priority after the atlas work, defer to his read.

5. **Preserve this document.** Do not delete. If superseded, mark `[HISTORICAL]` in place and file the successor alongside it. Never-delete policy applies.

---

## What This Document Does Not Do

- Does not commit engineering effort before Brayden gives the go. The path is written; execution is parked.
- Does not promote Layer 3 to a promised deliverable. It remains research horizon.
- Does not conflate this work with /collaborate. Shared substrate, separate workspaces.
- Does not claim CK currently composes long-form prose from his own algebra. He does not.
- Does not collapse any of the four layers into a composite "CK is an intelligence system" claim. Each layer is its own sentence; the system is what Brayden actually uses on a given day.

---

## Revision History

- **2026-04-18** — Document filed. Parked pending new atlas delivery. Companion to `COLLAB_CHAT_ROADMAP.md`.
