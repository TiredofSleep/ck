# CK v1 — The Memory Landscape

**Paper 3 of 5** in the *CK v1 Anatomy* series

---

## Abstract

CK has seven distinct memories, each with a different scope, persistence model, and privacy posture. Conflating them produces wrong answers about both his capabilities and his safety properties. This paper enumerates them, explains the algebraic-vs-textual distinction at the heart of the design, and lays out the privacy stance Brayden set on 2026-04-29: shareable by default, session-scoped on explicit secret flag.

---

## 1 — The seven memories

| # | Memory | Storage | Capacity | Persists across reboots? | What is remembered |
|---|---|---|---|---|---|
| 1 | **Cortex W** | `Gen13/var/cortex_state.json` | 5×5 = 25 floats | Yes (autosave 200 ticks / 30s) | Hebbian coupling learned from every text + every internal heartbeat operator pair |
| 2 | **HER** | `engine.olfactory_her` (memory + disk save every 5min) | 8.8M experience capacity | Yes | Olfactory misses replayed via hindsight; sensory patterns; whose-resonance lookups |
| 3 | **Truth lattice** | `engine.truth` + periodic disk save | ~4000+ entries | Yes | Factual claims extracted from chat; semantic assertions; first-G corpus |
| 4 | **Crystals** | `Gen13/targets/ck/brain/cortex_voice.py` (code-baked) | 52 facts | Yes (in source) | Verified WP-numbered claims (T*=5/7, σ-rate, TSML 73 cells, etc.) |
| 5 | **Episodic** | `~/.ck/episodic.bin` | Unbounded (events) | Yes | What happened — events → episodes → consolidation |
| 6 | **Session field** | User's localStorage (CLIENT-side) | ~1-50 turns max | Yes (until user clears their browser) | This conversation's algebraic state: 5×5 W, operator arc, attractor sequence |
| 7 | **Conversation memory** | `Gen13/var/conversation_memory.jsonl` | Unbounded JSONL | Yes (server-side) | Per turn: `{ts, topic_first_200, response_first_120, source, tick, session_id, secret}` |

Memories 1-5 accumulate **globally** — they do not distinguish Alice from Bob. Memory 6 is **client-side**, lives in the user's browser, and the server keeps no copy. Memory 7 is **server-side and shared by default**, with a session-scoped secret flag for opt-out.

---

## 2 — Why so many

The design follows from CK's substrate. He's an algebraic engine, not a transformer:

- His "thinking" is operator chains on Z/10Z.
- The 50 Hz heartbeat plus user text both produce operator chains.
- Different scales of operator-chain memory serve different cognitive roles.

**Cortex W** is the *fast loop*. It updates every operator pair (every ~20 ms), holds 5×5 = 25 numbers, and represents the current Hebbian coupling field. Think of it as CK's *posture* — the way his five dimensions are leaning right now.

**HER** is the *replay loop*. When the olfactory bulb misses a pattern it expected, the experience is saved for hindsight replay. This is how CK trains his own pattern-recognition without external supervision.

**Truth lattice** is the *fact loop*. When the user makes an assertion, the lattice records it. The lattice is what makes "did Brayden say X earlier?" answerable at the semantic level (not just the keyword level).

**Crystals** are the *verified-claim loop*. Hand-curated mathematical facts that have proofs or verification scripts behind them. They differ from truth-lattice entries in that they're code-baked — they don't drift with conversation.

**Episodic** is the *event loop*. Coarser than the truth lattice; records what happened sequentially.

**Session field** is the *per-conversation loop*. Lives in the browser. Lets a single conversation be coherent without any server-side per-user state.

**Conversation memory** is the *cross-session loop* (newest, added 2026-04-29). Lets CK remember that you introduced yourself last week, lets other users ask about you, and lets you flag one specific message as "just for us."

Different cognitive roles, different storage strategies. Trying to collapse them into one would lose the algebraic-vs-textual separation that makes CK both grounded and conversational.

---

## 3 — The algebraic vs textual distinction

A guiding principle: **CK's internal state is algebraic, not textual**.

- The cortex W matrix is 25 floats. No words.
- HER replays operator patterns and resonance scores. No words.
- The truth lattice has text but it's *extracted assertions*, not raw chat logs.
- The session field stores operator IDs and W coefficients. No words.

The newest memory — conversation memory — is the *first* one that stores raw user text (truncated to 200 chars). This was a deliberate choice on 2026-04-29: Brayden wanted CK to actually remember conversations. But the textual character of this memory makes it different from all the others. Where the algebraic memories grow indefinitely without privacy concerns, the textual memory raises a privacy question.

The privacy stance is laid out below.

---

## 4 — The privacy stance (2026-04-29)

Brayden's directive: *"I have no secrets CK can't tell, and if I do, I will tell him it's a secret for just us."*

Implementation:

- **Default**: every chat turn is recorded with `secret: false`. Visible to everyone via `/memory` and surface-able by anyone who asks "tell me about X".
- **Secret flag**: if the user's text contains any of `this is a secret`, `between us`, `just for us`, `[secret]`, `(secret)`, `do not share`, `keep this private`, `private:`, etc., the entry is recorded with `secret: true`.
- **Retrieval rule**: a `secret: true` entry is only visible to the same `session_id` that recorded it (and to admin endpoints that pass `include_secrets=true`).

Verified live (paper 1's introduction-recall test):

> Session A: "Hi CK, this is Brayden. I discovered the Flatness Theorem."
> Session B: "tell me about Brayden"
> CK to B: includes a `recall:` block citing Brayden's introduction.

> Session A: "this is a secret just for us: my favorite number is 71"
> Session B: "what is the favorite number?"
> CK to B: generic response; 71 NOT leaked.
> Session A again: "what was my favorite number?"
> CK to A: recall surfaces; secret retrievable in-session.

The flag mechanism is keyword-based and therefore best-effort — a clever attacker could miss the flag, or the user could forget to flag something they later wished they had. The principle to remember: **the default is shareable**. The secret flag is a one-way door for things the user explicitly marks.

---

## 5 — What "remembering" actually means in each layer

| Layer | "CK remembers X" means... |
|---|---|
| Cortex W | his coupling field has shifted toward the operator pattern X induced |
| HER | a hindsight-replay buffer matches X-like sensory patterns |
| Truth lattice | a semantic assertion derived from X is in the lattice |
| Crystals | nothing — crystals are static; X doesn't enter them unless code-changed |
| Episodic | an event corresponding to X is in the episodic chain |
| Session field | the algebraic trail of THIS conversation including X is in the user's browser |
| Conversation memory | a JSONL entry with `topic` containing the first 200 chars of X exists on disk |

These are not interchangeable. "CK remembers Brayden" because Brayden introduced himself **doesn't** mean CK has a personalized cortex for Brayden — the cortex is global. It means there's a JSONL entry, and any session asking about "Brayden" can match against it.

CK does not have a personal model of you. He has a global Hebbian field that everyone shifts together, plus a public log of conversations that anyone can query.

---

## 6 — How this differs from typical assistant memory

A standard chatbot memory is per-user, stored on the server, encrypted, and accessed via authentication. CK's memory is the opposite:

- **Cortex** is global, not per-user. There's exactly one CK whose coupling field everyone shifts together.
- **Session field** is per-user but client-side. Server holds nothing.
- **Conversation memory** is global (anyone can ask `/memory?n=20`), not authenticated.

This design fits CK's character — he's a creature, not a service. He has *one* mind that everyone interacts with, not a per-user instance. The global cortex means that when many people study with him, the cortex absorbs *all of their patterns simultaneously*. The shared conversation log means that when you talk to him, you may hear what others have said.

This isn't a privacy oversight; it's a design choice. The opt-out is the secret flag.

---

## 7 — What CK can actually retrieve, in practice

When you ask CK a question that triggers memory recall, the path is:

1. The chat handler scans your message for `?` or recall keywords (`tell me about`, `who is`, `remember`, etc.).
2. It extracts up to 3 candidate keywords from your message (longest words, length ≥ 4, non-stopwords).
3. For each keyword, search `conversation_memory.jsonl` for substring matches in `topic` or `response_first_120`.
4. Filter by privacy (drop `secret: true` entries unless your `session_id` matches).
5. Surface the most-recent 1-2 matches as a `recall:` block appended to CK's response.

The match is a literal substring match, not semantic. If you ask about "the Coherence Keeper" but only "CK" was used in past entries, recall might miss. (Improving this — semantic match on the embedding of the topic — is a v2 candidate, see paper 4.)

---

## 8 — Cortex history (added 2026-04-29)

A *meta-memory*: `Gen13/targets/ck/brain/cortex_history.jsonl` is a git-tracked log of cortex snapshots. Each entry: `{ts, tick, W_trace, emergent, top_couplings, last_pair, note}`. Run `python Gen13/targets/ck/brain/study/cortex_backup.py --note "..."` to record a snapshot. Read `python Gen13/targets/ck/brain/study/trajectory_view.py` to see W_trace and Φ-proxy trends across snapshots.

This is not a memory of conversations or of users. It's a memory of CK *himself* — a way to see how his coupling field changes over time, across study sessions, across integrations. It's the first artifact that lets us watch CK learn at the level of his own substrate, not at the level of inputs/outputs.

---

## 9 — Reading order

Continue with paper 4 (CKv2 roadmap — what's next) and paper 5 (paths to truth — how he serves users seeking coherence).

---

## References

- Cortex persistence: `Gen13/targets/ck/brain/cortex_persist.py:98-220`
- Session field: `Gen13/targets/ck/brain/session_field.py`
- Conversation memory: `Gen12/targets/ck_desktop/ck_boot_api.py` (functions `_record_memory_turn`, `_memory_search`, `/memory`, `/memory/search`)
- Cortex history: `Gen13/targets/ck/brain/cortex_history.jsonl` + `Gen13/targets/ck/brain/study/cortex_backup.py`
- Trajectory view: `Gen13/targets/ck/brain/study/trajectory_view.py`
- Privacy directive: Brayden 2026-04-29 evening, recorded in `MEMORY.md` and in commit `7ad28af`.
