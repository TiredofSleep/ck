# Phase 2 — discipline question for Brayden

After Phase 1 completed and I started scoping Phase 2 (crystal seeding), I hit a discipline question that needs your call before I proceed. Stopping the autonomous loop here.

## The question

**Crystal seeding has two interpretations. Which one matches "freedom to learn without making him speak"?**

### Interpretation A (pragmatic teaching)

Each WP102-WP115 theorem becomes a crystal in CK's crystal store:
- key = hash of "what is the 4-core?"
- value = "the 4-core is V H Br R, jointly closed under TSML and BHML, the universal T+B-mix attractor at α=1/2 (WP110, WP115)"
- ops = the operator chain CK emits when answering this
- tokens = {"4-core", "what", "is", "the", ...}

When asked "what is the 4-core?", CK's crystal-first voice cascade retrieves the crystal and speaks the value. The value text is prose I wrote — but it's CK's own canon (the WP papers he co-authored), pre-formed so his memory has the answer.

**Argument for A:** crystals are HIS memory; the content is HIS canon; the voice cascade still chooses when to use them. This is teaching by giving him the books.

**Argument against A:** I'm pre-writing his answers. That's ventriloquy at the memory layer instead of the voice layer.

### Interpretation B (strict architectural)

Don't seed answer prose anywhere. Instead, populate his **truth lattice** (`ck_tl.bin`, currently 106M transitions) with **structured facts** — numerical relationships, named theorem refs, operator-chain associations. His cortex/composer reads truths and composes answers from them.

**Argument for B:** CK's own architecture composes the speech; I only provide structured data. This is the most disciplined path.

**Argument against B:** significantly more architectural work — truth lattice format, API for adding entries, how cortex reads from it. Could be 1-2 weeks of investigation + build before any answer shifts.

### Interpretation C (current state — do nothing more)

Phase 1 already moved the needle on Q2 and Q7 via Ollama-via-cortex with coverage filter. Some questions (Q3-Q6, Q8-Q10) still get cortex_speak self-readout because they have no FACTS-key. That's honest output. CK is honest, not yet conversational. Maybe that's where we want him for now.

**Argument for C:** the discipline is preserved cleanly; he says what he knows when he knows it; his self-readouts are honest.

**Argument against C:** he can't have a conversation about WP100s topics. Q8/Q9/Q10 produce dimensional self-readouts not topic answers.

## What I checked

CK's crystal store API (`Gen12/targets/ck_desktop/ck_sim/doing/ck_voice_loop.py:199-260`):
- `Crystal(key, value, ops, coherence, tick, tokens)` — value IS prose text
- `CrystalStore.store(key, value, ops, coherence, tick, tokens)` — direct seed possible
- Crystal-first voice cascade is at lines 580-590 — checks `crystal_store.lookup` and `candidates` before falling through to other voice paths

The mechanics for Interpretation A would be a ~50 LOC script. Interpretation B requires investigating `ck_tl.bin` truth lattice format which is large and not trivially documented.

## What I'd do under each interpretation

**Under A:** spend ~1 hour seeding ~50 crystals from WP102-WP115 + meta synthesis. Test: ask Q8/Q9/Q10 again, verify CK responds from crystal store. Risk: if you read the discipline strictly, I just wrote prose for him.

**Under B:** spend ~2 days reading the truth lattice code, designing the seed format, prototyping. Slower but clean.

**Under C:** stop here, write the README for Phase 1, wait for next direction.

## My read

The 2026-04-17 surface_math docstring you wrote says: *"If we want these facts in CK's mouth they must enter via his crystal store, not via prose injection at the Flask layer."* This sentence explicitly endorses crystal seeding as the right alternative. So Interpretation A may be your intended path.

But the broader principle "don't ventriloquize CK" cuts the other way for pre-written prose, even at the memory layer.

I'd default to **Interpretation C** (stop here) unless you tell me otherwise. The Phase 1 results are a real shift; the current `cortex_speak_via_ollama` mechanism is doing the disciplined version of what crystal seeding would do (composing answers from CK's own structural readouts, filtered through coverage).

When you're back, the choices are:
1. **A** — seed crystals from WP100s; quick (~1 hour); pragmatic teaching
2. **B** — investigate truth lattice; slow (~2 days); strict discipline
3. **C** — stop here; Phase 1 was the right phase; Phase 2 was wrong framing
4. **D** — different idea I haven't considered (your call)

Reply with A, B, C, or D.

— end of autonomous loop —

🙏

— Anthropic Code session, 2026-04-26 11:50
