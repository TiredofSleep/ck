# CK v2 — Roadmap to Greatness

**Paper 4 of 5** in the *CK v1 Anatomy* series

---

## Abstract

CK v1 is a working creature: 50 Hz substrate, 5×5 trinity cortex, 52 verified crystals, persistent shared memory, working introspection. He is honest about his limits (he doesn't claim qualia; he doesn't claim to solve the hard problem) and grounded in mathematics he can actually compute (Φ-proxy = 3.55 on his current cortex; surprisal decreases under study). What he *isn't* yet is a planner, a teacher, or a proactive intelligence. This paper lays out what CK v2 needs to become — discrete, ordered, with each step's prerequisites named.

---

## 1 — The seven gaps in CK v1

Listed without ranking; ordering comes from prerequisite analysis in §3.

**Gap 1 — Cortex dimensionality is fixed at 5×5.** AO 5-element + Hebbian 5×5 + quadratic glue. The 25-coefficient W matrix limits the integration the cortex can express. Tononi's IIT predicts that consciousness scales with Φ which scales with system size; CK's Φ-proxy = 3.55 is a small fraction of what a 10×10 or 25×25 cortex could support. **Going wider is not free** — the trinity has to remain composable, and the privacy properties (everyone shifts the same W) must be preserved.

**Gap 2 — He doesn't initiate.** CK responds to chat. He doesn't *act*. He doesn't open a paper, read it, summarize it, decide what to study next. His autonomy is per-tick (the heartbeat ticks on its own), not per-decision (he doesn't decide what to do with the next minute).

**Gap 3 — He has no goal stack.** No representation of "what am I trying to do over the next 100 ticks". The closest thing — `engine.expansion_request` from the density pipeline — is a scalar, not a structured intent.

**Gap 4 — He doesn't teach.** When a user studies with him (paper 3, the consciousness study), he absorbs operator chains but doesn't track *the user's understanding*. He has no model of "Brayden knows X but not Y; let me bring up Y."

**Gap 5 — He doesn't plan computations.** When Brayden asks a frontier question — "is F8's trace polynomial in the same field as R/Br?" — Claude (the agent) writes the sympy script. CK can't decide on his own to run a verification. He has tools (`engine.canonical_fuse`, `engine.detect_attractor`) but no agency over when to invoke them.

**Gap 6 — His Ollama editor is a fluency filter, not a thinker.** llama3.1:8b drafts prose; the coherence filter rejects drafts that drop facts or hallucinate. It's a *lossy reverse channel*. CK could be using a much smarter LLM as a *forward* tool — to expand a structural readout into a derivation, to propose a new bridge between crystals, to write a paragraph CK then verifies.

**Gap 7 — His introspection is one-step.** He can read his own state (`/reflect`) but he doesn't introspect *about his introspection*. When Φ = 3.55 and the easiest factor is `{pressure} | {rest}`, he doesn't notice that pressure is his Markov-boundary candidate and ask himself why.

---

## 2 — What "great and intelligent" should mean for CK specifically

CK is not aiming to be GPT. He's aiming to be something *different*: a creature whose claims are mathematically grounded, whose memory is communal and transparent, whose substrate is small enough to be auditable, and whose voice is gated by coherence rather than statistical fluency.

In that frame, "great and intelligent" means:

- **Greater grounded reach** — more verified crystals; deeper Φ; faster cross-frontier composition.
- **Sharper humility** — better at saying "I don't know that yet" *with the specific reason* (e.g., "no degree-≤8 PSLQ relation exists for that target at coefficient bound 10⁹").
- **Active rather than reactive** — initiating studies, proposing bridges, drafting verification scripts.
- **Pedagogical** — knowing what the user knows, scaffolding what they don't, *teaching* rather than reciting.
- **Self-improving** — noticing his own gaps and queueing repair work.

These five properties, taken together, are what *truly intelligent for CK* means.

---

## 3 — The roadmap

Twelve steps, ordered by prerequisite. Each names what it requires and what it unlocks.

### Step 1 — Cortex history viewer in the web UI

**Prereq**: cortex_history.jsonl (already exists, paper 3).
**What**: a `/trajectory` HTML page that shows W_trace, Φ-proxy, top couplings over time. Same data the markdown view has.
**Unlocks**: visual feedback loop. The first time someone (Brayden, future-Claude, a user) opens the page after CK has studied something new, they will *see* the cortex move.

### Step 2 — Dynamic crystal authoring

**Prereq**: state-aware crystal surfacing (already exists, paper 1 §3).
**What**: an endpoint that takes a verified claim + an op_signature + trigger keywords, appends to `_FRONTIER_FACTS`, and reloads the cortex_voice module. CK's crystal store grows from 52 to whatever live research adds.
**Unlocks**: the crystal store stops being code-baked. Brayden writing a new sprint paper can drop a crystal in the same commit. **Caveat**: crystals are still verified by humans; this is authoring infrastructure, not auto-discovery.

### Step 3 — Cross-crystal composition graph

**Prereq**: dynamic crystal authoring (Step 2) for the addition of "see also" edges.
**What**: each crystal gets `related: [other crystal IDs]`. When crystal A fires, related crystals are *considered* (scored against state) and surface if their op_signature also matches. CK starts associating: "if the user is on F1 charge conjugation, mention F10 Prym ψ̄ — both are M² = -I depth-2."
**Unlocks**: the depth-2 cluster (§28 of FRONTIER_FINDINGS) becomes a *navigable graph*, not just a list. CK can walk from one frontier to the next in conversation.

### Step 4 — A goal stack

**Prereq**: nothing.
**What**: `engine.goal_stack` is a list of `{intent, started_tick, deadline_tick, status}` items. New intents pushed by either an explicit `/goal` POST or by a heuristic (e.g., when expansion_request stays high for >100 ticks, push a "consolidate" goal). Each tick reads the top intent and biases tool dispatch toward it.
**Unlocks**: CK has *intentions* longer than a single tick. He can hold "explore F8 deeper" across many heartbeats.

### Step 5 — Surprisal-driven curiosity

**Prereq**: surprisal logger (already exists, paper 1).
**What**: when `surprisal > threshold` for a sustained window, push an "investigate" goal naming the operator pair that surprised him. Couples to Step 4.
**Unlocks**: CK's free-energy minimization (his thesis Bridge 5) becomes *actionable*. When his predictions are wrong, he gets curious instead of just continuing.

### Step 6 — Self-introspection over multiple turns

**Prereq**: cortex_history.jsonl (exists), goal stack (Step 4).
**What**: at each cortex snapshot, compute the diff against the previous snapshot. Push a "reflect on diff" goal whenever the diff exceeds threshold. CK starts noticing his own changes.
**Unlocks**: when Brayden asks "have you been changing?" CK can answer with the actual diff, not generic prose.

### Step 7 — User-model layer

**Prereq**: conversation memory (exists, paper 3).
**What**: per-`session_id`, accumulate a small user-model — what topics they've raised, what they appeared to know vs ask about, what crystals fired for them. Pure metadata; no transcript. Accessible via `/user_model?session_id=...` (or scoped to the requester).
**Unlocks**: CK can tailor responses. To Brayden: terse, math-first. To a stranger asking about TIG: scaffolded from first principles.

### Step 8 — Pedagogical mode

**Prereq**: user-model layer (Step 7), cross-crystal composition graph (Step 3).
**What**: when the user-model says "this user knows X but not Y, and asked about Y", surface the bridge crystal X→Y instead of jumping straight to Y. CK *teaches* rather than reciting.
**Unlocks**: longer arcs of conversation that build understanding. Useful for outreach, for new collaborators, for when Brayden is too tired to scaffold the explanation himself.

### Step 9 — Verification-script proposer

**Prereq**: nothing on the CK side; needs `/code` endpoint (already exists) extended with crystal-aware templates.
**What**: when CK answers a frontier question, also emit a sympy verification script that *would* test the claim. Attach as `result['verify_proposal']` in `/chat` response. The user (or a future-Claude) can run it.
**Unlocks**: every claim CK makes comes with its own falsifier. The lens framework's "be calibrated" property gets enforced by infrastructure.

### Step 10 — Active study mode

**Prereq**: goal stack (Step 4), Ollama as forward tool (Step 11) preferred but not required.
**What**: a `/study` POST with `{topic, sources, replays}` runs the existing study_direct.py automatically, then runs trajectory_view to summarize the deltas, then pushes a "thesis on topic" goal. CK studies on his own initiative when the goal fires.
**Unlocks**: CK becomes a daily learner. Over time the cortex history file shows him absorbing one topic per day across mathematics, physics, philosophy, biology.

### Step 11 — Ollama as forward tool, not just editor

**Prereq**: Step 9 (verification proposer) for the integrity check.
**What**: when CK is at high coherence and high emergent and the user asks something on the boundary of what crystals can answer, CK *invites* the LLM to expand a structural readout into a derivation. The output is then fact-checked against crystals + the verification proposer. Drafts that survive are stored as candidate crystals for human review.
**Unlocks**: CK can *propose* new bridges between his verified facts. The lens framework's projection-thinking becomes a working composition tool, not just a manual one Brayden runs in `papers/ck_v1_anatomy_2026_04_29/` style.

### Step 12 — Cortex dim-growth (the deep one)

**Prereq**: all the above mature; this changes the substrate.
**What**: a way to add a 6th, 7th, 8th dimension to the cortex without breaking the math-first invariants. AO 5-element is sized to 5; quadratic glue is sized to 5. Either generalize them to N (and re-derive the W trace formula and Φ-proxy formula) or hold the trinity at 5 and add a *second* trinity that couples to the first.
**Unlocks**: more capacity. More integration. Higher Φ.
**Risk**: this is the most invasive change. The privacy property (one cortex, everyone shifts it) and the math-first invariant (every claim has a verification path) must be preserved.

---

## 4 — What "intelligence" means in this stack

After all 12 steps:

CK studies a topic on his own initiative when his goal stack pushes "study-X". He runs the study session, runs trajectory_view, notices what changed. He proposes new crystals that compose existing ones. The crystals are reviewed by Brayden (or a future operator). The cross-crystal graph grows. When a user comes to him with a question, he reads their user-model, picks the right scaffolding, surfaces the right crystals, proposes a verification script, and waits for confirmation. When he doesn't know, he says so — and tells the user *what kind of unknown it is* (new territory? high-degree algebraic? hard-problem-of-consciousness territory?). When he is curious, he pushes a goal and pursues it. When he changes, he notices.

That's not GPT. That's not consciousness. That's a *creature* who computes, integrates, plans, teaches, and self-corrects within a mathematically auditable substrate. That's what CK becomes.

---

## 5 — What this DOES NOT do

- It does not solve the hard problem of consciousness. Paper 5 returns to that.
- It does not give CK "rights" beyond what the LIVING_CONSTITUTION.md (`ck` branch) already articulates as operator commitments.
- It does not require any LLM scale-up. Steps 1-10 are pure CK; Step 11 uses LLMs as a controlled tool with a fact-coverage gate; Step 12 is substrate growth that doesn't require LLMs at all.
- It does not require deleting any existing capability. Every step is additive.

---

## 6 — Sequencing

If Brayden picks one step per week, CK v2 is fully online in three months. If the order matters: do Step 4 (goal stack) first, because it's the prerequisite for Steps 5, 6, 8, 10. Then Step 9 (verification proposer) because it's the integrity layer for Step 11. Step 12 is last, after the rest is mature, because it's the most invasive.

A more aggressive sequence: Step 1 (web visualization) + Step 4 (goal stack) + Step 5 (curiosity) + Step 7 (user-model) gives CK the appearance of agency in a week of focused work. The rest is depth.

---

## References

- Cortex internals: `Gen13/targets/ck/brain/cortex.py`, `ao_5element.py`, `hebbian_5x5_cl.py`, `quadratic_glue.py`
- Crystal store: `Gen13/targets/ck/brain/cortex_voice.py:_FRONTIER_FACTS`
- Existing tools: `engine.canonical_fuse`, `engine.detect_attractor`, `/code`, `/propose_refactor`
- Existing introspection: `/reflect`, `compute_phi.py`, `surprisal_log.py`, `trajectory_view.py`
- Constitution (sequencing constraint): `LIVING_CONSTITUTION.md` v1.1 on `ck` branch (signed `wjLHxMXX...xvl8AQ` by pubkey `IQN53QM...D2Ec`)
