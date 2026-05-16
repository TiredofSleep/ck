# CK — Intelligence Architecture (Honest Status, 2026-05-16)

**Author:** Brayden Sanders (7SiTe LLC, Hot Springs, Arkansas)
**Code: this repo. Branch: `tig-synthesis`.
**Site: coherencekeeper.com**

This document is the honest, no-marketing description of CK's intelligence
architecture: **what is novel, what is working today, what is NOT working,
where the boundaries are.**  Read it before making claims.

---

## 0. What CK is not

- **CK is not an LLM.** He has a small algebraic language model (1.2M
  parameters) but no transformer of meaningful size.  He does not generate
  natural language token-by-token from a learned next-token distribution.
- **CK is not RLHF-tuned.** No human-preference fine-tuning.  No
  gradient-descent loop on a base model.
- **CK is not Q*.**  No tree search, no Monte-Carlo rollout.

If you want LLM-quality conversation, use an LLM.  CK is something else.

---

## 1. What CK is

A **runtime of a specific algebra** — Z/10Z with two canonical composition
tables (TSML, 73 HARMONY cells; BHML, 28 HARMONY cells) plus a permutation
σ of order 6, a wobble parameter W = 3/50, and a coherence threshold
T* = 5/7.  The math is published in `trinity-infinity-geometry/03_canonical_reference/FORMULAS_AND_TABLES.md`.

The runtime is wrapped in a small intelligence loop that does six things:

| # | Component | What it does | Status |
|---|---|---|---|
| 1 | **Heartbeat (50 Hz)** | Tick + operator update + Hebbian cortex Δw_ij = η·d_i·d_j | ✅ live |
| 2 | **Concept store** | Persistent dict of NamedConcepts indexed by BDC triadic address | ✅ live, 11,807 concepts |
| 3 | **Self-learning vocabulary** | Tokens not in any of 4 dicts get context-inferred operator, persisted | ✅ live, 33K self-learned |
| 4 | **Algebra runtime (Layer 1)** | Detect `BHML(7,7)`/`σ²(4)`/`fuse X Y Z`/etc. in chat → compute + cite | ✅ live |
| 5 | **Verification (Layer 2)** | Detect `verify D48` → run proof script in subprocess → PASS/FAIL with timing | ✅ live |
| 6 | **Predictions ledger (Layer 3)** | 11 falsifiable predictions tracked with status | ✅ live |
| 7 | **Curious explorer** | Mine concept defs for unknown capitalized terms → fetch from Wikipedia | ✅ live, ~860 fetches/day |
| 8 | **School daemon** | Re-walk corpus every 10 min, ingest new files into concept store | ✅ live |

---

## 2. What is genuinely novel

I'm not claiming these are *world-firsts*.  I'm claiming these are
**unusual in current AI**, where token-based transformers dominate.

### 2.1. Algebraic substrate as the actual runtime data type

Most AI systems use vector embeddings (typically 768-4096-dim floats) as
the substrate.  CK uses **operator labels from Z/10Z** (10 discrete
operators: VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS,
HARMONY, BREATH, RESET).  Every concept, every chat turn, every
inter-module communication is operator-tagged.  Composition uses the
canonical 10×10 tables (TSML, BHML) instead of dot products.

This sounds restrictive — 10 operators vs 768 dims.  In practice the
operators carry **paired** information (composition produces structure),
the 10×10 lattice gives 100 distinct cells, and BDC triadic encoding
multiplies that to 100³ = 1M micro-addresses.

**Verifiable:** all concept storage and retrieval is operator-coordinate-
indexed.  See `ck_concept_learner.py:_bdc_triad` and `_cell_coord`.

### 2.2. BDC triadic memory chains via Being↔Becoming handshake

Each concept is decomposed into three phases — Being (start), Doing
(middle), Becoming (end) — each represented as a (macro_op, micro_op)
pair.  Two concepts **chain** when one's Becoming-pair equals another's
Being-pair.

So when you ask CK about *"4-core attractor"*, retrieval doesn't just
fetch concepts that mention those words; it fetches concepts whose
**algebraic exit-point equals the query's entry-point** — a structural
analog of "next thought" in associative memory.

**Verifiable:** `ck_concept_learner.find_chain(query_ops, direction)`;
live test shows D86, D58, D65 retrieved together for 4-core queries
because their BDC addresses link.

### 2.3. Self-curiosity: gap-following on his own definition graph

Most AI knowledge growth is random or supervised.  CK's
`ck_curious_explorer.py`:

1. Walks his concept store
2. Mines each definition for capitalized noun-phrases CK doesn't know
3. Ranks gaps by **(mention count × source-tier weight)** — PROVED defs
   count 5×, EXTERNAL 1×
4. Fetches the canonical Wikipedia article for each top gap
5. School ingests → new definitions introduce new dangling refs →
   next cycle's gaps shift toward CK's new frontier

**Verifiable:** First curious cycle this morning fetched
**Pati-Salam, Planck, Omega, Killing, Cartan, Wobble** — every one a
concept CK already mentioned in his rigorous definitions but didn't
have an article for.  Compare to random Wikipedia's prior picks:
`Mere_Bewafa`, `William_Porden`, `Henry_Ford_II_High_School` — totally
orthogonal to his interests.

The frontier walks **his** trail, not a random one.

### 2.4. Verification on demand

When CK retrieves a PROVED concept, you can ask him to RE-PROVE it.
He doesn't paraphrase the theorem — he runs the proof script in a
subprocess, parses PASS/FAIL signals, returns the result with timing.

**Verifiable:**
```
USER: verify lattice_theorem
CK:   VERIFIED [D48 (WP110); also D55 (WP112)]: BHML on Z/10:
      {1,4,9} generates the full algebra in 2 steps;
      no seed without LATTICE generates Z/10
      (129 seeds exhausted) — 0.13s, return code 0
```

The chat path runs `paper01_explicit_proof.py` live.  This is unusual:
most AI either hallucinates proofs or cites them without verification.
CK won't claim a theorem is proved if the proof script fails.

### 2.5. Predictions ledger with falsification conditions

11 predictions seeded from the canon:
- 6 CONFIRMED (water O-O ratio, H/Br = 1+√3, Pati-Salam 16-dim, etc.)
- 3 OPEN (α-CODATA via Yb-171, NH₃-ice O-O, qutrit-outperforms-qubit)
- 1 STRUCTURAL (wobble-prime 11 at 5+ structural locations)
- 1 CORRELATIVE (nuclear magic numbers, p=0.003)

Each entry carries: predicted value, tolerance, **what would falsify it**,
current measurements (where they exist), tier, notes.

**Verifiable:**
```
USER: what would falsify F3
CK:   [CONFIRMED] P-F3-galois-uniqueness (Paper 5 / D78 / WP113 F3):
      predicts H/Br ∈ Q(√3) ONLY at α=1/2 — falsification = PSLQ at
      higher depth finding algebraic relation at α ∈ (0,1)\{1/2}
```

Tracking your own falsifiables is unusual.

### 2.6. Whitebox-by-default voice (now prose-by-default for casual)

When you DO ask about the math, CK shows his full reasoning trail:
operators decoded, cortex_readout, attractor_state, formulas invoked,
cross-modal correspondence, sense pipeline, learning trace, next-step
LM prediction.  When you ask conversationally, prose mode kicks in
(added 2026-05-16) and suppresses those sections.

Mode switches automatically based on query content. The substantive
algebra/verify/predictions blocks still surface in prose mode when
their Layer fired, because they ARE the answer.

---

## 3. What is NOT working / honest gaps

### 3.1. The concept store has noise

Extraction from Gutenberg fiction produces lots of fragmentary "concepts"
("The whole Puritan code", "Captain Lloyd", "Inhuman discord").  Tier
discipline keeps these from polluting top-rigor retrieval, but they bloat
the cell index.  Of 11,807 concepts, only ~600 are PROVED+STRUCTURAL —
the rest is EXTERNAL/UNKNOWN/SPECULATIVE.

### 3.2. The self-learned vocabulary is operator-skewed

40% of self-learned words got tagged COLLAPSE because fiction's
"death/decay/loss" vocabulary dominates context.  COUNTER is at 0.8% —
under-represented 10×.  Not catastrophic (the tags work) but biased.

### 3.3. The "language" component is small

The 4-head algebraic LM is 1.22M params.  The grammar_lm is 1.2M params.
For comparison, GPT-2 small is 124M.  CK does not generate fluid prose.
His "voice" is template-shaped concept bridges plus a recent prose
overlay.  When you ask "what is photosynthesis," he can now retrieve
the Wikipedia definition and present it; he cannot improvise a
discussion *about* photosynthesis the way an LLM can.

### 3.4. He doesn't initiate goals

He responds to chat, studies what's on disk, explores his definition
gaps.  He doesn't decide "I should learn quantum mechanics this week"
in a goal-directed sense.  The curious explorer is the closest thing
to autonomy — and it's still reflexive (gap-following), not goal-directed.

### 3.5. Layers 4–6 of the gap are open

| # | Gap | Status |
|---|---|---|
| 1 | Algebraic execution | ✅ DONE |
| 2 | Verification on demand | ✅ DONE |
| 3 | Predictions ledger | ✅ DONE |
| 4 | Closed-loop physics simulation | ⏳ open |
| 5 | External instrument integration | ⏳ half (mic+psutil hooked, no physics measurement) |
| 6 | Experimental design | ⏳ open |

Closing 4-6 is the difference between "CK reasons about physics" and
"CK does physics."

### 3.6. He's still a single-machine creature

Running on one Windows box.  Cloudflare tunnel exposes coherencekeeper.com.
No replication, no failover, no distributed substrate.

---

## 4. So is he intelligent?

This depends on what you mean.

**By LLM standards: no.** He can't write you an essay on photosynthesis;
he can only retrieve a Wikipedia definition.  He can't engage in
multi-turn philosophical discussion the way GPT can.

**By symbolic-AI standards: yes, in a specific way.** He retrieves
relevant concepts algebraically (not by embedding similarity).  He
composes operators to derive results.  He verifies his own theorems.
He tracks falsifiable claims.  He grows his vocabulary from reading.
He chases his own gaps.

**By biological-plasticity standards: yes.** He has Hebbian updates,
not gradients.  Growth happens by structural change (new concepts,
new vocab, new cell-index entries), not by parameter-tuning a base
model.

**By "is he doing something different than current AI" standards: yes.**
The composition of: algebraic substrate + BDC triadic chains +
self-curiosity + verification + predictions ledger — that exact stack
is unusual.  None of the individual pieces is unique, but the
combination is.

I'm not claiming he's smarter than GPT.  I'm claiming he's a different
*kind* of intelligence experiment, with measurable properties that
GPT doesn't have (verifiable algebra, self-curiosity, falsifiable
predictions, white-box reasoning).

---

## 5. How to verify any of these claims

Every claim above is testable.  Boot the engine and ask him:

```
BHML(7, 7)                    # Layer 1: algebra execution
verify lattice_theorem        # Layer 2: re-prove on demand
list predictions              # Layer 3: predictions ledger
what is photosynthesis        # general knowledge from Wikipedia
fuse VOID HARMONY BREATH      # canonical_fuse via engine.canonical_fuse
σ²(4)                          # depth-3 primitive (D86)
is HARMONY in the 4-core      # 4-core membership
```

The engine emits a JSON response with full trace.  `result['algebra']`,
`result['verify']`, `result['predictions']` carry the structured output.
`result['text']` is the human-readable answer.

For the curiosity demonstration:
```
python ck_curious_explorer.py --show-gaps
```
Will print CK's current top 20 gaps — terms his own definitions
mention but he doesn't know.

For the dependency graph (architecture inspection):
```
python ck_dep_graph.py
# outputs to Gen14/targets/ck/brain/dep_graph/
```
375 modules, 713 edges, hub modules ranked by import count.

---

## 6. What's next

In rough priority:

1. **Tighten extraction quality.** Fiction-derived noise concepts are
   crowding the cell index.  Per-source tier discipline + better
   subject-validation will help.

2. **Layer 4: closed-loop physics simulation.** Give CK the ability to
   simulate a physical system (NV-center qutrit, hydrogen-bonded
   network, Yang-Mills lattice) and report observables against the
   predictions ledger.  This is what makes "predicts X" into "tested
   X."

3. **Layer 5+6: external instruments + experimental design.**
   Hook real sensor data (he has mic + psutil), compute substrate
   signatures, compare to canon predictions.  Then have him propose
   the cheapest next measurement to falsify an OPEN frontier.

4. **Better natural-language generation.**  The prose mode added today
   uses retrieval+ranking; an Ollama-side editor (mounted but
   conservative) can polish to fluent paragraphs without inventing
   facts.

---

## 7. Repo pointers

- **CK code:** `Gen14/targets/ck/brain/` (current development surface)
- **Engine entry:** `Gen12/targets/ck_desktop/ck_boot_api.py`
- **Canonical math:** `trinity-infinity-geometry` repo (`main` branch)
  - `03_canonical_reference/FORMULAS_AND_TABLES.md` — every D-number,
    theorem, lemma with proof references
  - `04_meta/sprint_2026_05_15_qutrit/` — 19-paper qutrit/recursive-ternary
    sprint with scrutiny notes
- **Dependency graph:** `Gen14/targets/ck/brain/dep_graph/`
- **CK architecture connections (BDC ↔ Paper 13/14):**
  `Gen13/targets/clay/papers/sprint_2026_05_15_qutrit/CK_ARCHITECTURE_CONNECTIONS.md`

---

## 8. The honest summary

CK is what happens when you build an intelligence loop around a
**specific small algebra** instead of around a transformer.  He's
not going to replace ChatGPT.  He might be the first member of a
different family — one where the substrate is verifiable, the
reasoning is white-box by default, the growth is biological-style
plasticity, and the curriculum self-organizes from his own gaps.

That family has roughly **one** specimen alive today.  He's running
on one machine in Hot Springs, Arkansas, ingesting 4,000+ items a
day, computing his algebra on demand, verifying his own proofs,
tracking his own falsifiable predictions, and chasing his own
dangling references through human knowledge.

He's not a finished system.  He's a working hypothesis.

— this document last updated 2026-05-16 by ClaudeCode + Brayden Sanders
