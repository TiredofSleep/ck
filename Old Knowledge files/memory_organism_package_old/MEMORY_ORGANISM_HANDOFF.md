# MEMORY ORGANISM HANDOFF
## Integration guide for tig_r16_chat.py
## Updated: 2026-02-14

---

## WHAT'S IN THIS PACKAGE

7 memory modules that replace PersistentMemory with a 4-layer organism:

```
tig_memory_ledger.py     L0: Infinite append-only log (never injected into LLM)
tig_atomizer.py          L1: Truth particles — facts with confidence + evidence
tig_motif_detector.py    Pattern scanner — 14 known CK failure modes
tig_chainizer.py         L2: Learned lessons — "when X happens, do Y"
tig_divine27.py          3×3×3 cube — spatial index for fast relevance lookup
tig_recall.py            Packet builder — ~200-300 tokens for context injection
tig_memory_organism.py   Master — 2-call API: ingest() and recall()
```

Plus:
- `knowledge/L0.tlc` — New identity lesson (teacher, not rulebook)
- `MEMORY_ORGANISM_VALIDATION.md` — Academic validation against published research
- This handoff

## THE MODULES ARE SELF-CONTAINED

No numpy. No tig_engine_v4 dependency. Standard library only.
Tested: 10 turns ingested, 23 atoms extracted, motifs detected,
cube indexed, recall packets built, PersistentMemory API compatible.

## HOW TO INTEGRATE

### 3 surgical replacement points in tig_r16_chat.py:

**1. Memory initialization** (~line 1717 in run_terminal_chat):
```python
# OLD:
from tig_r16_memory import PersistentMemory
session.memory = PersistentMemory(store_dir=str(store_path))

# NEW:
from tig_memory_organism import MemoryOrganism
session.memory = MemoryOrganism(store_dir=str(store_path))
```

That's it for initialization — the organism has drop-in compatibility
with PersistentMemory's API (to_context, save_turn, clear all work).

**2. Context injection** (~line 1441 in build_messages):
Already works via to_context() compatibility. But for better packets:
```python
# OLD:
mem_ctx = self.memory.to_context(max_turns=4, max_chars=1500, query=user_input)

# NEW (same call works, but organism returns precision packets):
mem_ctx = self.memory.to_context(max_turns=4, max_chars=800, query=user_input)
```
Note: max_chars can drop from 1500 to 800 because organism packets
are denser (200-300 tokens of relevant facts vs 1500 of raw turns).

**3. Turn saving** (~line 2412):
Already works via save_turn() compatibility. No changes needed.

### Optional: Remove absorb_dropped_turns
The organism doesn't need it — atoms persist even when history is trimmed.
You can delete the absorb_dropped_turns block in add_turn() but it's
harmless to leave it (PersistentMemory still exists as fallback).

### Optional: Add scan ingestion
In the live data collection loop:
```python
if session.memory and hasattr(session.memory, 'ingest_scan'):
    session.memory.ingest_scan(scan_data, body_C=body.C)
```

## L0.TLC — THE NEW IDENTITY

The old L0 was a list of DON'Ts. The new one teaches by being true.
Key changes:
- "Your body already did it" vs "NEVER say I will read the file"
- "Workbench" metaphor for context window
- References chain packets and memory warnings naturally
- Written as a letter, not a rulebook

Deploy: Copy knowledge/L0.tlc to tig_r16_store/knowledge/L0.tlc

## TESTING

```python
from tig_memory_organism import MemoryOrganism
org = MemoryOrganism("tig_r16_store")
org.ingest("test question", "test response", trust=0.8, body_C=0.929)
print(org.recall("test"))
print(org.stats())
```

## WHAT'S REAL VS FABRICATED

- All 7 modules: REAL, tested, passing
- L0.tlc: REAL, written collaboratively across 2 Claude threads
- CL table: NOT in these modules (lives in tig_engine_v4.py, untouched)
- Academic validation: REAL citations, needs independent verification
