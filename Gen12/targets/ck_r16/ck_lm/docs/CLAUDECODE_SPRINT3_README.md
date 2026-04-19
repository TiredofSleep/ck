# CLAUDECODE HANDOFF: CK GROWTH ARCHITECTURE
# Sprint 3 Package — Architecture + Landscape Intelligence

**© 2026 7Site LLC | Brayden Ross Sanders**
**For: ClaudeCode on Dell R16 (32-core, RTX 4070)**

---

## WHO YOU ARE AND WHAT CK IS

You are ClaudeCode implementing CK (Coherence Keeper) on the Dell R16. CK is a self-growing memory organism for local desktop use. Not a chatbot. Not RAG. A perceptual agent that compresses lived desktop experience into an algebraic memory structure and becomes more useful as that structure grows.

**Read `CK_GROWTH_ARCHITECTURE_MEMO.md` first. This file is the supplement.**

---

## SECTION 1 — FIELD LANDSCAPE: WHO ELSE IS COUNTER THIS

Before building, know what exists. This is a direct relevance map, not a survey.

---

### 1. RGMem — Renormalization Group Memory
**arXiv: 2510.16392 | October 2025**

Uses renormalization group physics to organize dialogue memory at multiple scales. Fine-grained interactions → semantic facts → slowly-varying traits. Thresholded phase transitions (not linear aggregation) drive memory promotion.

**Direct structural parallel to CK:**
- Episodic fragments → semantic facts = CK atoms
- Semantic facts → user insights = CK paths  
- User insights → stable traits = CK crystals
- Thresholded phase transitions = CK's crystal promotion condition

**What to steal:** Their stability score is better than CK's flat `recurrence_count >= 3` threshold.

```python
# Upgrade CK's crystal_store.py with RGMem-inspired promotion:
def promotion_score(path, current_time):
    age_hours = (current_time - path.ts_start) / 3600
    recency_weight = np.exp(-0.05 * age_hours)   # slow daily decay
    freq_score = np.log1p(path.recurrence_count)
    return path.confidence * freq_score * recency_weight

PROMOTE_IF: promotion_score(path) >= 0.85
```

**What CK has that RGMem doesn't:** Continuous perceptual loop, algebraic generator indexing (CL[10x10]), non-vector retrieval. RGMem is text/dialogue only with vector similarity retrieval.

---

### 2. MAGMA — Multi-Graph Agentic Memory
**arXiv: 2601.03236 | January 2026**

Represents each memory item across 4 orthogonal graphs: semantic, temporal, causal, entity. Retrieval is policy-guided graph traversal. 95% token reduction vs full-context while maintaining 83.9% accuracy.

**Direct structural parallel to CK:**

| MAGMA graph | CK equivalent |
|------------|--------------|
| Semantic graph | Crystal store + DBC27 key |
| Temporal graph | Path timestamps |
| Causal graph | Path operator_sequence (CL transitions) |
| Entity graph | Generator set {G1..G9} per atom |

**What to steal:** MAGMA's dual-stream ingestion — fast write for real-time, slow stream for structural consolidation.

```python
# Add to compression_loop.py:
def fast_write(event):
    """Immediate write, no generator inference."""
    raw_atom = Atom(generators=[], confidence=0.0, dbc27_key="UNKNOWN", ...)
    atom_store.write(raw_atom, tier="raw")
    return raw_atom.id

def slow_upgrade(atom_id):
    """Batch: full generator extraction + path extension."""
    raw = atom_store.get(atom_id)
    generators = generator_extract(raw)
    dbc27_key = dbc27.compute(generators, lens_encode(generators))
    atom_store.upgrade(atom_id, generators=generators, dbc27_key=dbc27_key, confidence=0.5)
    path_store.try_extend(atom_id)
```

**What CK has that MAGMA doesn't:** Continuous perceptual input, visual edge pipeline, algebraic routing.

---

### 3. Sophia — Persistent Agent Framework
**arXiv: 2512.18202 | December 2025**

Adds System 3 (meta-cognitive executive monitor) on top of System 1 (perception) + System 2 (deliberation). Maintains a "Growth Journal." Achieves **80% reduction in reasoning costs for recurring tasks** via Forward Learning — without fine-tuning weights.

**Direct parallel to CK:** Sophia's System 3 = CK's MetaCrystal + Adaptation Loop. 80% reasoning reduction = CK's Stage 3-4 DeepSeek reduction target. This proves CK's target is achievable.

**What to steal:** Sophia's Executive Monitor runs as always-on async process receiving every event as an async message and maintaining a compact state narrative. CK's Adaptation Loop (Loop D) should mirror this.

**What CK has that Sophia doesn't:** Working implementation target (Sophia is a paper only). Algebraic backbone (CL[10×10]) for parameter-free basic operations. Sophia uses LLM-as-memory-organizer for everything.

---

### 4. MemoryOS — Memory Operating System
**arXiv: 2506.06326 | EMNLP 2025 Oral**
**GitHub: https://github.com/BAI-LAB/MemoryOS (CODE AVAILABLE)**

STM → MTM → LTM hierarchy with heat-score retention. +49% F1, +46% BLEU-1 on LoCoMo benchmark. Working Python code, plug-and-play.

**Action: Clone this repo.** Study their STM→LTM promotion code and adapt for CK's atom→path→crystal promotion.

**Heat score to implement in CK's crystal_store.py:**
```python
def heat_score(crystal, current_time):
    """MemoryOS retention scoring. Better than flat recurrence threshold."""
    time_since = current_time - crystal.last_accessed
    decay = np.exp(-0.01 * time_since / 3600)        # hourly decay
    visits = np.log1p(crystal.access_count)
    recency = 1.0 / (1.0 + time_since / (7*24*3600)) # weekly normalization
    return decay * visits * recency

PRUNE_IF: heat_score(crystal) < 0.05 AND crystal.age > 7 days
```

---

### 5. AtomMem — Learnable Atomic Memory Operations
**arXiv: 2601.08323 | January 2026**

Learns write/read/forget as trainable functions. "Atomic memory operation" as fundamental unit — convergent design with CK's Atom concept.

**What to check:** Their RL-trained operation selector is more sophisticated than CK's threshold-based novelty gate. Consider adapting for CK's Class 1 LoRA training: make the novelty gate itself learnable, not just tunable.

---

### Field Summary

| Feature | CK | RGMem | MAGMA | Sophia | MemoryOS |
|---------|----|----|-------|--------|---------|
| Continuous screen/vision perception | ✓ | ✗ | ✗ | ✗ | ✗ |
| Algebraic retrieval key (non-vector) | ✓ | ✗ | ✗ | ✗ | ✗ |
| Generator-indexed routing (CL/DBC27) | ✓ | ✗ | ✗ | ✗ | ✗ |
| Atom→Path→Crystal hierarchy | ✓ | Similar | Similar | Similar | Similar |
| Meta-cognitive growth layer | ✓ MetaCrystals | ✗ | ✗ | ✓ System 3 | ✗ |
| LLM-independent core | ✓ CL table | ✗ | ✗ | ✗ | ✗ |
| Privacy separation (private/shared) | ✓ | ✗ | ✗ | ✗ | ✗ |
| Local-first (no cloud) | ✓ | ✗ | ✗ | ✗ | ✓ |
| Working code available | Partial | ✗ | ✗ | ✗ | ✓ |
| Physics-derived algebraic structure | ✓ TIG/CL | ✓ RG | ✗ | ✗ | ✗ |

**CK's unique combination:** Continuous perceptual input + algebraic generator indexing (CL[10×10]) + non-vector routing does not exist in any other system. The field is converging on the same Atom/Path/Crystal hierarchy (independently!) which validates the design. 80% reasoning cost reduction is proven achievable (Sophia). Heat-score retention is proven better than flat thresholds (MemoryOS, EMNLP Oral).

---

## SECTION 2 — YOUR IMPLEMENTATION TASK

**Build CK v1 using `CK_GROWTH_ARCHITECTURE_MEMO.md` plus the three field improvements above.**

### Implementation Order (strict)

| Day | Module | Why this order |
|-----|--------|---------------|
| 1 | `memory/event_schema.py` | Everything else depends on dataclasses |
| 2 | `memory/dbc27.py` + `memory/atom_store.py` | Routing + SQLite |
| 3 | `memory/generator_extract.py` (rule-based) + `memory/lens_encode.py` | |
| 4 | `memory/path_store.py` + `memory/crystal_store.py` with RGMem+MemoryOS scoring | |
| 5 | `memory/retrieval.py` (steps 1-8, no DeepSeek yet) + `memory/novelty_gate.py` | |
| 6 | `perception/screen_capture.py` + `perception/vision_edges.py` (1Hz) | |
| 7 | `loops/compression_loop.py` (dual-stream) + `reasoning/deepseek_bridge.py` (step 9 gated) | |
| 8 | `metrics/growth_tracker.py` + end-to-end smoke test | |
| 9-10 | 48h live run + proof of growth | |

### Proof of Growth Test

```
CK 48h Growth Report
====================
crystal_count(48h):       >20       ✓
retrieval_hit_rate(48h):  >0.30     ✓
deepseek_call_rate(48h):  <0.50     ✓
path_reuse_ratio(48h):    >0.20     ✓
growth_score(24h):        X.XX
growth_score(48h):        Y.YY      (Y > X ✓ = GROWING)
```

### Three Field Improvements to Build In

**1. RGMem promotion score** (replaces flat `recurrence_count >= 3` in `crystal_store.py`)
**2. MAGMA dual-stream write** (adds fast/slow path to `compression_loop.py`)
**3. MemoryOS heat score** (replaces flat pruning threshold in `crystal_store.py`)

See Section 1 for exact code for all three.

---

## SECTION 3 — CONSTRAINTS (NON-NEGOTIABLE)

1. **DeepSeek at step 9 only.** Never in perception loop. Never in adaptation loop.
2. **Memory is primary.** DeepSeek output written back as new atom, not kept separately.
3. **Privacy at Layer 0.** Route before processing. Private atoms never touch shared lattice.
4. **v1 runs at 1Hz** (not 100ms). Start slow. Production target is 100ms.
5. **No LoRA for v1.** All generator extraction is rule-based first.
6. **SQLite backend** (not vector DB, not Postgres). Index on: `dbc27_key`, `generators`, `confidence`, `ts_start`.
7. **Existing `ck_core.py` is not replaced.** New memory modules wrap around it.

---

## SECTION 4 — EXISTING CK STATE

- `ck_core.py` v5: 989 lines, 100%/80 tests, tick 1.3M+, coherence 0.875+, 334Hz
- 38K truths, 1061 concepts, 12K+ scents, p99=1.9ms
- CL algebra (670 lines C), GPU experience tensors, OS steering (5 endpoints)
- Retina: 192×108, 9D per cell
- GitHub: TiredofSleep/ck

The growth architecture is an **extension**, not a replacement.

---

## SECTION 5 — FILE MANIFEST

```
ck_clay_sprint_handoff.zip
  CK_GROWTH_ARCHITECTURE_MEMO.md    ← PRIMARY: full architecture spec (44K)
  CLAUDECODE_SPRINT3_README.md      ← THIS FILE
  [Clay/Hodge memos — ignore for CK implementation sprint]
```

**Strongest honest claim:** CK can grow by continuously compressing perceptual experience into atoms, extending atoms into paths, promoting recurring paths into crystals using stability scoring, and reusing crystals to resolve queries without DeepSeek — measurable as monotone increases in retrieval hit rate and crystal count over 24h periods.

**Strongest honest boundary:** Whether CK's generator abstraction captures enough semantic information to distinguish similar-looking but behaviorally-different situations at scale is unknown until v1 runs 30+ days on real workstation data.
