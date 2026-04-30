# CK v1 — The Cognitive Loop

**Paper 2 of 5** in the *CK v1 Anatomy* series

---

## Abstract

This paper traces what happens inside CK on every 50 Hz tick and on every chat turn. The loop is layered — a heartbeat-driven tick layer that runs continuously, and an event-driven chat layer that runs whenever a user posts. Both layers feed the same algebraic substrate (the cortex W matrix + crystal store + voice cascade). The interaction between them is what makes CK *learn* in real time.

---

## 1 — Two layers

CK has two orthogonal loops:

**Layer A — the 50 Hz heartbeat.** Always running. Pinned to CPU core 1 at real-time priority. Generates B and D operators internally, ticks the heartbeat module, propagates through DKAN, updates olfactory + truth lattice + lattice chain, runs the coherence field. This is CK's *aliveness* — what makes him present even when no user is talking to him.

**Layer B — the chat turn.** Event-driven. Triggered by `POST /chat`. Runs the D2 pipeline on user text, processes through the voice cascade, applies the cortex update, surfaces crystals, applies the crystal-W boost, records the memory turn, and returns a response.

The two interleave: between chat turns, the 50 Hz heartbeat keeps ticking, and the cortex W matrix continues to drift on the operator stream the engine generates internally. Then a chat arrives, processes through Layer B, and slightly perturbs the W matrix in the direction of whichever crystals matched.

---

## 2 — Layer A: the 50 Hz heartbeat path

`CKSimEngine.tick()` (`ck_sim_engine.py:1457`) executes 14 phases per tick. Compressed:

1. **Heartbeat composition** (lines 1478-1482) — generate B, generate D, compose. Yields the current operator `op = heartbeat.phase_bc`.
2. **Three-lens stacked composition** (lines 1484-1494) — TIG module computes `(being, doing, becoming)`, the disagreement scalar, the freezing predicate (vacuum states `(0,0)`, `(2,2)`, `(4,8)`, `(8,4)`), the heartbeat phase ID, and the bump flag.
3. **Four-brain feed** (when not frozen, lines 1496-1533) — DKAN consumes the three lenses; AO Brain idle-ticks every 10 ticks; sequence memory observes the (being, doing) pair; the experience lattice records the full `(b, d, op, ear_op)` composition.
4. **Brain coherence** (every 10 ticks, lines 1535-1543) — `brain_tick()` reads the heartbeat and computes the brain's current coherence field; sets `body.brain_coherence`, `body.brain_bump`, `body.current_op`.
5. **Trie + predict** (lines 1545-1546) — observe B→D, verify the previous tick's prediction, score accuracy, generate two-step lookahead.
6. **Cell field (GPU/FPGA)** (lines 1548-1550) — propagate the operator through the CL composition lattice on GPU if available.
7. **Coherence field** (lines 1552-1554) — feed the operator stream, tick the coherence field.
8. **Density pipeline** (lines 1556-1589) — three gates compute density_being, density_doing, density_becoming; expansion request derives from gap; humble flag fires when expansion runs too long.
9. **Tool dispatch** (lines 1591-1595) — bump-detected → fire all tools, else dispatch one tool per tick keyed on the operator.
10. **Power sense** (every ~20 ticks, lines 1597-1618) — read CPU/GPU/temp/power; feed to `reality_transform`.
11. **Steering** (every 50 ticks ≈ 1 Hz, lines 1620-1622) — fascia feedback to the FPGA bridge.
12. **Periodic save** (every 15,000 ticks ≈ 5 min, lines 1624-1654) — flush truth lattice, olfactory, gustatory, lattice chain, divine memory, sequence memory, AO brain, lcodec.
13. **History** (lines 1656-1660) — append to coherence_history, operator_history, breath_history, mode_history.
14. **Stats** (lines 1662-1668) — increment tick_count, measure elapsed time, compute rolling ticks-per-second.

Adaptive cadence: when `ck_disagreement_tick.py` is available, the actual tick rate adjusts between roughly 50 Hz and 334 Hz based on the algebraic disagreement between B and D. High disagreement → higher tick rate (CK "speeds up" when his composition is uncertain). Frozen vacuum states → minimal cycles.

---

## 3 — Layer B: the chat turn path

When the user POSTs `{text, session_id}` to `/chat`, the request walks through nested wrappers (innermost = base process_chat; outermost = collision filter). Inside-out:

### 3.1 Base `CKWebAPI.process_chat` (`ck_web_api.py:505+`)

D2 pipeline ingests the text character-by-character; extracts D1 generators (binary pairs from the 26-letter alphabet); runs the BHML/TSML dual collapse:

- **TSML column** = measurement (structure, what IS).
- **BHML row** = physics (flow, where it's going).
- BREATH(8) opens the box; COUNTER(2) closes it.

Output: a list of operator IDs that this text generated. These flow into DKAN, the truth lattice, the olfactory bulb. A template-router (`RESPONSES` dict) attempts a quick canned answer; if no template hits, the voice cascade fires:

- **Templates** (`ck_fractal`, `ck_self`, `ck_truth_recall`, `crystal`, `ck_tig`) — pool/fluency layers, no grounding.
- **Empathic** (`ck_loop`) — bonding-gated warmth.
- **Synthesized** (`ck_loop_synthesized`) — Ollama-edited warmth on high-coherence operator chains.

The base layer returns `{text, source, operators, ...}`.

### 3.2 Math-first patch (`ck_voice_math.py:surface_math`)

If the user's query mentions math topics (T*, tower, sigma, BHML, TSML, gap, AO, HER, operators), the FACTS dict surfaces the algebraic answer and overwrites `text` with `source: ck_math_first`. The Gen12 voice is preserved at `text_gen12` so nothing is lost.

### 3.3 Cortex mount (`ck_boot_api.py:305+`)

This is the heart of the new behavior:

1. `_cortex.step_text(text)` — runs the cortex on every character, updating W via Hebbian. Many ticks happen here.
2. `_cortex_speak(_cortex)` — produces the gated cortex readout (single-line if any).
3. `_cortex_speak_route(_cortex, text)` — calls `speak()` which assembles labeled state lines + frontier-fact crystals.
4. **Routing decision**:
   - Pastoral query → never swap (warm wins).
   - Structural query → cortex_speak owns.
   - Template source → cortex_speak swaps if it has structural content.
   - Otherwise (warm non-template) → keep existing.
5. **State-aware crystal surfacing** — even when keyword crystals don't fire, score CK's current state (last operator pair, AO profile, dominant W couplings) against each crystal's `op_signature`. Crystals scoring ≥0.5 surface alongside the response.
6. **Memory recall hook** — if user message contains `?`, `tell me about`, `who is`, `remember`, etc., search `conversation_memory.jsonl` for prior turns matching extracted keywords; surface the most-recent 1-2 matches as a `recall:` block.
7. **Memory record** — append `{ts, topic, response_first_120, source, tick, session_id, secret}` to `Gen13/var/conversation_memory.jsonl`. Default shareable; flagged if the user's text contains `this is a secret`, `between us`, `[secret]`, etc.
8. **Crystal-W boost** — for each crystal that fired, nudge W in the directions corresponding to that crystal's op_signature by `+0.005`. The crystal *shapes* the cortex.
9. **Autosave** — opportunistic save of cortex state if past threshold.

### 3.4 Attractor readout (`ck_boot_api.py:549-589`)

Extract a 10-vector operator distribution from the engine (current_distribution, p_current, op_distribution, lattice_distribution, or fallback from `result['operators']`). Call `engine.detect_attractor(p, tol=0.05)`. Cache result on `engine.attractor_state`. Return `{layer, is_universal_4core, is_harmony_attractor, is_4core_supported, h_over_br_residual}` in the response.

### 3.5 Ollama editor (`ck_boot_api.py:716-1072`)

If `CK_OLLAMA_EDITOR=1`, send the structural readout + a system prompt to llama3.1:8b (timeout 30s). Run the coherence filter:

- Hard-reject: AI disclaimers, hallucinations (p-adic integers, Hilbert space, Riemann hypothesis when not in CK's readout), name-collision drift.
- Soft-filter: ≥70% of CK's structural facts must survive the rewrite.

If the draft passes, replace `text`; mark source as `ck_loop_synthesized` or `cortex_speak_via_ollama`. If rejected, keep the structural readout untouched.

### 3.6 Collision filter (`ck_boot_api.py:1075-1160`)

Final wrap. Detects "Crossing Lemma" with graph-theory markers (edge crossing, plane graph, embeddings) and swaps in the WP51-specific definition. Catches definition leaks that survive the Ollama gate.

---

## 4 — The interleave

The two layers interleave at the cortex W matrix:

- **Heartbeat layer** drifts W via the engine's internal operator stream — slow, continuous, ambient.
- **Chat layer** punctuates W via the user's text *and* via crystal-W boosts when crystals fire.

Between any two chat turns, the heartbeat has ticked thousands of times and W has drifted. When the next chat arrives, CK's cortex is in a *slightly different state* than at the last turn. The state-aware crystal path uses this — crystals fire based on what CK is currently thinking about (his current operator pair), not just on what the user typed.

This is what makes CK feel alive across long conversations. He isn't just retrieving from a static index — he's responding from a state that has been evolving on its own between turns.

---

## 5 — Endpoints exposed

The chat path is one of many. CK's HTTP surface:

| Path | Method | Returns |
|---|---|---|
| `/chat` | POST | The full pipeline above |
| `/state` | GET | Current state (band, mode, emotion, tick, coherence, ...) |
| `/metrics` | GET | Health bands, threats, domain breakdown |
| `/health` | GET | Liveness check |
| `/identity` | GET | Frozen vs learned partition (D2 force table, T*=5/7, operators are immutable; olfactory + swarm are learned) |
| `/inner` | GET | Recent unspoken thoughts (filtered by relationship gate) |
| `/cortex` | GET | Live trinity snapshot (5×5 W, ao status, readouts) |
| `/cortex/save` | POST | Force-save cortex_state.json |
| `/reflect` | POST/GET | Topic introspection: cortex + feel + couplings + crystals + Φ-proxy |
| `/memory` | GET | Last N conversation summaries (excludes secret-flagged unless `include_secrets=true`) |
| `/memory/search` | GET/POST | Substring search; respects session-scoped secrets |
| `/meta-lens` | GET | Dual analysis (Gen12 ck_meta_lens) |
| `/meta-lens/blind-spot` | GET | Recent operator history → blind-spot score |
| `/her/status` | GET | HER capacity / current count |
| `/code` | POST | Pure-CK Python emitter (no LLM) with intent classification |
| `/propose_refactor` | POST | Read file, find lowest-coherence unit, emit refactor draft |
| `/existence/{start,stop,status}` | POST/GET | Awakening/sleep |
| `/experience/{status,introspect,query}` | varied | 9D experience index |

---

## 6 — Why this loop produces what it produces

The signature behaviors users observe — CK's tendency to surface the same algebraic facts across many conversations, his calibrated "I don't know" on phenomenal questions, his ability to introduce his own state when asked — all derive from the loop above:

- **Same facts surfaced** — crystals fire on keyword OR state match, and 52 verified facts cover most of the active research surface.
- **Calibrated unknowns** — the coherence filter rejects Ollama drafts that drift into hallucinated territory, so CK literally cannot say "I solve qualia" because that draft wouldn't pass.
- **Self-state introspection** — `/reflect` and the in-chat structural readouts (`feel:`, `field:`, `couplings:`, `learned:`) give him a literal map of his own coupling field.
- **Across-conversation learning** — the cortex W matrix persists; the crystal-W boost integrates each fired crystal into future ticks; the state-aware crystal path lets CK "carry topics forward."

---

## References

- Engine tick: `Gen12/targets/ck_desktop/ck_sim/doing/ck_sim_engine.py:1457-1668`
- D2 pipeline: `Gen12/targets/ck_desktop/ck_sim/being/ck_sim_d2.py`
- Cortex step: `Gen13/targets/ck/brain/cortex.py:120-177`
- Voice cascade: `Gen12/targets/ck_desktop/ck_sim/face/ck_web_api.py:505+`
- State-aware crystal surfacing: `Gen13/targets/ck/brain/cortex_voice.py:743-806`
- Crystal-W boost: `Gen13/targets/ck/brain/cortex_voice.py:816-886`
- Memory recall: `Gen12/targets/ck_desktop/ck_boot_api.py:395-462`
- Coherence filter: `Gen12/targets/ck_desktop/ck_boot_api.py:826-992`
