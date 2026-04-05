# THREE-TIER ONTOLOGY TRANSITION MEMO
# Replace Prime/Composite with REAL / SEMIPRIME / COMPOSITE

**© 2026 7Site LLC | Brayden Ross Sanders**
**Implementation Transition Note for ClaudeCode**

---

## PART 1 — The Core Transition

### Old binary (historical, preserve as background):

```
PRIME      = irreducible / foundational / untouched by composition
COMPOSITE  = built / structured / formed from relations between primes
```

The binary was useful as first pre-language: it named the difference between raw contact and constructed structure. But it collapses two distinct things — the raw encounter and the first stable closure — into one category.

### New ternary (implementation language):

```
REAL       = directly encountered; pre-closure contact with world or system
SEMIPRIME  = first stable closure; minimal bridge from contact into reusable structure
COMPOSITE  = higher-order structure built from multiple stable bridges
```

**The missing middle is SEMIPRIME.**

The binary was wrong for a learning organism because real growth does not move in one step:

```
REAL → COMPOSITE    ← this skips the hardest part
```

It moves in two steps:

```
REAL → SEMIPRIME → COMPOSITE    ← this is the actual growth path
```

SEMIPRIME is where perception becomes memory, where recurrence becomes path, where path becomes crystal candidate.

---

## PART 2 — Three Tiers: Operational Definitions

### TIER R — REAL

**Definition:** The directly encountered signal or state before any higher-order structural reuse. Pre-closure.

**CK examples:**
- Raw screen event (frame diff)
- Mouse click at coordinate
- OCR token stream
- Telemetry spike (CPU/memory delta)
- Process start/stop event
- Single visual edge cluster from Canny
- User utterance (raw text)
- Model output as emitted (DeepSeek synthesis, not yet stored)

**Properties:**
- Time-local: valid in the moment of encounter, may not persist
- Not yet reusable across different contexts
- High sensory/contact value — closest to the actual world
- May be private (raw user content → A22 in 2×2)
- May be noisy or one-shot
- Will dissolve quickly if not closed into SEMIPRIME

**Storage rule:** REAL objects enter CK as EPHEMERAL in the 4×4. They may become ATOMIC candidates. They do not crystallize directly.

---

### TIER S — SEMIPRIME

**Definition:** The minimal stable unit formed by exactly one nontrivial binding or closure across REAL inputs. The smallest structure that can recur and be reused.

**CK examples:**
- An atom with confirmed generator identity (generator set stable across ≥ 2 re-encounters)
- A repeated event pair: event A reliably followed by event B
- A stable atom transition: two atoms connected by a consistent CL operator
- A generator pair that repeatedly fuses the same way under the same lens
- A two-step workflow motif (open file → focus window)
- A recognized action-response closure (click → state change, consistently)
- A first valid path edge: the smallest path segment that has survived re-encounter

**Properties:**
- Smallest reusable bridge — cannot be decomposed further without losing the closure
- Enough structure to persist past the ephemeral stage
- Still close to the REAL: only one binding layer above direct contact
- Compressive: replaces a sequence of REAL events with one reusable unit
- Interpretable: can be described in one CL transition or one generator-pair
- Best place for fast learning (LoRA Class 1 adapters target SEMIPRIME extraction)

**Storage rule:** SEMIPRIME is the first class promotable into PATH memory and crystal candidates.

---

### TIER C — COMPOSITE

**Definition:** Any higher-order structure built from multiple stabilized SEMIPRIME bridges.

**CK examples:**
- Long path motifs (multiple SEMIPRIME transitions chained)
- Crystals (recurring bundles of paths)
- Policies (action rules derived from multiple crystal alignments)
- Reusable workflows (multi-step task procedures)
- Meta-crystals (patterns of how COMPOSITE structures were handled)
- Site-layout preferences (inferred from repeated SEMIPRIME UI patterns)
- Long-range retrieval bundles (multiple crystals co-activating)

**Properties:**
- Efficient: replaces many SEMIPRIME queries with one COMPOSITE lookup
- Reusable across different REAL contexts
- Abstract: may be further from direct contact
- Can drift if not periodically reanchored to SEMIPRIME support
- Higher maintenance cost (more supports to track)

**Storage rule:** COMPOSITE structures must retain lineage back to SEMIPRIME supports and REAL origins (via ProvenanceTag).

**Hard law:**
```
No COMPOSITE without SEMIPRIME support.
No SEMIPRIME without REAL contact.
```

---

## PART 3 — Why Semiprime Is the Real Missing Layer

### The error in the binary

The binary prime/composite compressed perception-into-memory into a single step. That made the architecture look like:

```
raw contact → (magic) → full structure
```

There is no magic. There is only the first stable closure.

### The SEMIPRIME correctly names what CK already does (but didn't have a word for):

When CK's compression loop takes a raw event and promotes it to an atom with confirmed generators, that is SEMIPRIME formation. When two atoms form a first path edge, that is SEMIPRIME. The stage where recurrence begins to be meaningful — where something is worth keeping not because it was big but because it happened again in the same form — is SEMIPRIME.

### External grounding: MACLA (arXiv:2512.18950)

MACLA compresses 2,851 ALFWorld training trajectories into 187 reusable procedures — a 15:1 compression ratio — demonstrating efficient knowledge distillation through semantic abstraction rather than memorizing individual trajectories. Each of those 187 procedures is a SEMIPRIME: the minimal stable unit extracted from many REAL trajectories that generalizes across new contexts. MACLA excels when tasks have reusable actions, hierarchical structure, and consistent semantics — SQL queries, being atomic 2-3 action sequences, are too short to benefit from hierarchical decomposition. This is the SEMIPRIME failure mode: objects that are just barely REAL (too short to close into SEMIPRIME) do not benefit from procedure extraction.

MACLA reduces LLM calls by more than 85% compared to ReAct (2 vs 16-20 calls per episode) — this is exactly CK's Stage 3-4 DeepSeek reduction target, achieved by having rich SEMIPRIME structure to draw on.

### External grounding: Cognitive science

The K-Line Theory (Minsky, 1980) points out that hierarchical memory structures are fundamental to biological cognition, enabling humans to efficiently organize memory across different levels of abstraction — as seen in how infants group specific objects like "apple" and "banana" into broader categories like "fruit" and "food." The SEMIPRIME tier is the "apple/banana" level: already one stable abstraction above raw sensory contact, but not yet the fully generalized category "food."

### External grounding: Episodic → Semantic → Procedural

Episodic memory functions as a long-term memory system capable of offloading specific instances into broader parametric memory to avoid capacity limitations and allow for generalization to new semantic knowledge and procedural skills based on specific instances. In CK's ternary:
- Episodic = REAL (raw contact, time-stamped, specific)
- Semantic = SEMIPRIME (first generalizations from episodes)
- Procedural = COMPOSITE (reusable skills built from semantic patterns)

This correspondence is not accidental — the three-tier cognitive memory architecture independently arrives at the same structure as the REAL/SEMIPRIME/COMPOSITE ontology.

---

## PART 4 — Exact Mapping Into CK Memory Stack

| CK Object | Tier | Reason |
|-----------|------|--------|
| Raw screen event (frame diff) | **REAL** | Direct sensor contact, not yet closed |
| Single OCR token | **REAL** | Time-local, not reusable standalone |
| Single telemetry sample | **REAL** | One data point, no closure |
| Single extracted edge (Canny) | **REAL** | Feature before generator binding |
| User utterance (raw) | **REAL** | A22 content, private, pre-structure |
| DeepSeek output as emitted | **REAL** (then A12) | Model-produced but unbound |
| Atom with confirmed generators | **SEMIPRIME** | First stable generator closure |
| Repeated event pair | **SEMIPRIME** | First recurrent closure |
| First valid path edge | **SEMIPRIME** | Two atoms + consistent CL transition |
| Two-step workflow motif | **SEMIPRIME** | Smallest reusable action bridge |
| Path bundle (≥3 atoms) | **COMPOSITE** | Multiple SEMIPRIME transitions chained |
| Crystal | **COMPOSITE** | Recurring path bundles |
| Action policy | **COMPOSITE** | Rule derived from crystal alignment |
| Meta-crystal | **COMPOSITE** | Pattern of how composites were handled |
| LoRA Class 1 adapter | **COMPOSITE** | Built from many SEMIPRIME training examples |

**Implementation law:**
```python
assert all(
    obj.tier_class in ("REAL", "SEMIPRIME", "COMPOSITE")
    for obj in memory_store.all()
)
assert all(
    semiprime.provenance.parent_event_ids is not None and len(semiprime.provenance.parent_event_ids) >= 1
    for semiprime in memory_store.where(tier_class="SEMIPRIME")
)
assert all(
    composite.provenance.supporting_ids is not None and len(composite.provenance.supporting_ids) >= 2
    for composite in memory_store.where(tier_class="COMPOSITE")
)
```

---

## PART 5 — Formal Growth Law

**Growth occurs when:**

```
Step 1: REAL events are compressed into valid SEMIPRIME bridges
        (perception loop → compression loop → SEMIPRIME atom/path formation)

Step 2: SEMIPRIME bridges recur and accumulate into COMPOSITE structures
        (crystal promotion from repeated SEMIPRIME paths)

Step 3: COMPOSITE structures improve future handling of REAL events
        (retrieval returns crystal policy → faster resolution of new REAL events)
```

**The loop:**

```
REAL → SEMIPRIME → COMPOSITE → better handling of REAL → (back to REAL)
```

This is the actual loop closure. Not: new loop after new loop. But: same loop, gaining foundation.

**Growth metric using ternary ontology:**

```python
def growth_score_ternary(t):
    real_count      = memory_store.count(tier_class="REAL")
    semiprime_count = memory_store.count(tier_class="SEMIPRIME")
    composite_count = memory_store.count(tier_class="COMPOSITE")
    
    # Real → Semiprime conversion rate
    r_to_s = semiprime_count / max(real_count + semiprime_count, 1)
    
    # Semiprime → Composite conversion rate  
    s_to_c = composite_count / max(semiprime_count + composite_count, 1)
    
    # Composite retrieval effectiveness
    composite_reuse = composite_reuse_rate(t)
    
    return 0.35 * r_to_s + 0.35 * s_to_c + 0.30 * composite_reuse
```

---

## PART 6 — Language Replacement Table

| OLD term | NEW term | Notes |
|---------|---------|-------|
| "prime" / "irreducible" | **REAL** | In implementation docs and code; preserve old term in historical notes |
| "composite" (when referring to first-level composites) | **SEMIPRIME** | The old "composite" was too broad |
| "composite" (when referring to higher-order structures) | **COMPOSITE** | Crystals, policies, meta-crystals |
| "raw event" | REAL event | No change to meaning |
| "atom" | SEMIPRIME atom (if generator-confirmed), REAL atom (if still unbound) | Tier class now distinguishes |
| "path" | SEMIPRIME path (minimal edge), COMPOSITE path (multi-segment) | Tier class distinguishes |
| "crystal" | COMPOSITE crystal | All crystals are COMPOSITE |
| "meta-crystal" | COMPOSITE meta-crystal | All meta-crystals are COMPOSITE |

**Preservation note:** The old prime/composite language captured the right intuition — irreducible vs. composed. Do not erase it. Preserve in `docs/historical_notes.md`. The ternary sharpens it by naming the missing middle, not replacing it.

---

## PART 7 — Integration With 2×2 / 3×3 / 4×4 Meta-Memory Grammar

The tier_class is **orthogonal** to the reduced meta-tag from the second-pass memo. It is an additional field, not a replacement.

**Typical coordinate combinations:**

| Tier | Typical 2×2 | Typical 3×3 entry | Typical 4×4 stage |
|------|------------|------------------|------------------|
| REAL | EXTERNAL/CONTENT (A22) or EXTERNAL/STRUCTURE (A21) | B11 (RAW EVENT INTAKE) | EPHEMERAL |
| SEMIPRIME | EXTERNAL/STRUCTURE (A21) or INTERNAL/STRUCTURE (A11) | B21→B23 | ATOMIC or early PATH |
| COMPOSITE | INTERNAL/STRUCTURE (A11) or INTERNAL/CONTENT (A12) | B33 (MEMORY WRITEBACK) | PATH or CRYSTAL |

**The constraint this adds:**
```
A22 (WORLD PAYLOAD) → can only produce REAL tier objects
A21 (WORLD TOPOLOGY) → can produce REAL or SEMIPRIME, not COMPOSITE
A11 (LATTICE GEOMETRY) → can produce SEMIPRIME or COMPOSITE, not REAL
A12 (SYNTHESIS PAYLOAD) → can only produce COMPOSITE objects
```

This is a stronger privacy constraint than the 2×2 alone provides: it says that raw user content (A22) cannot directly become COMPOSITE without first passing through REAL and SEMIPRIME stages. This prevents synthesized crystals from masquerading as grounded structure.

---

## PART 8 — CL/TIG Integration

**Law:** CL does not generate REAL. CL does not determine REAL. CL acts on REAL-derived generators to test whether a stable closure exists.

**Exact sequence:**

```
REAL event
  ↓
generator_extract(event) → generator_set  ← this is where CL first applies
  ↓
fuse(G_i, G_j) → CL_point              ← first CL operation
  ↓
is this closure repeatable?             ← SEMIPRIME test
  if recurrence_count >= 2:
    → PROMOTE to SEMIPRIME
  else:
    → remains REAL
  ↓
If SEMIPRIME, enter path extension:
  new SEMIPRIME + existing SEMIPRIME → path edge
  fuse(G_edge_a, G_edge_b) → CL_point   ← CL on SEMIPRIME-level generators
  if stable: → COMPOSITE path segment
  ↓
Repeated COMPOSITE path + crystal promotion
  → COMPOSITE crystal (full CL path reuse)
```

**Summary:** CL is the closure grammar for the ternary ontology:
- REAL = pre-closure (CL not yet invoked or single invocation)
- SEMIPRIME = first CL-valid closure (CL invoked, closure stable ≥ 2 recurrences)
- COMPOSITE = repeated CL closure and higher-order CL path reuse

The CL table is the generator of SEMIPRIME structure. When a closure is not repeatable (noise, one-shot event), CL firing leaves the object in REAL. When a closure is repeatable, it produces SEMIPRIME. When SEMIPRIME structures chain, COMPOSITE emerges.

---

## PART 9 — Implementation Schema

**One new field on every CK object:**

```python
tier_class: Literal["REAL", "SEMIPRIME", "COMPOSITE"]
```

**Assignment function:**

```python
def assign_tier(obj) -> Literal["REAL", "SEMIPRIME", "COMPOSITE"]:
    """
    Assign tier based on CK object properties.
    Replaces the old prime/composite distinction.
    """
    # REAL: direct contact, no stable closure yet
    if (
        obj.persistence_stage == "EPHEMERAL"
        or (obj.persistence_stage == "ATOMIC" and obj.recurrence_count < 2)
        or len(obj.generators) == 0
        or not obj.has_stable_closure()
    ):
        return "REAL"
    
    # SEMIPRIME: first stable closure, not yet multi-bridge bundle
    elif (
        obj.recurrence_count >= 2
        and obj.has_stable_closure()
        and len(obj.provenance.supporting_ids) <= 2  # exactly one binding layer
        and obj.persistence_stage in ("ATOMIC", "PATH")
        and not obj.is_multi_bridge_bundle()
    ):
        return "SEMIPRIME"
    
    # COMPOSITE: built from multiple semiprime supports
    else:
        return "COMPOSITE"

# Helper methods on Atom/Path/Crystal:
def has_stable_closure(self) -> bool:
    """True if the generator set has fired in the same form >= 2 times."""
    return self.recurrence_count >= 2 and self.confidence >= 0.5

def is_multi_bridge_bundle(self) -> bool:
    """True if this object is built from multiple semiprime supports."""
    return (
        len(self.provenance.supporting_ids) > 2
        or self.persistence_stage in ("PATH", "CRYSTAL")
        and len(self.atom_ids if hasattr(self, 'atom_ids') else []) > 3
    )
```

---

## PART 10 — Promotion and Demotion Rules

### REAL → SEMIPRIME (promotion)

```
PROMOTE iff:
  - generator_set is stable (same generators in ≥ 2 re-encounters)
  - at least one nontrivial relation survives re-encounter
    (path edge or CL-fused closure persists across variation)
  - closure is not one-shot noise
    (recurrence_count >= 2 in different contexts)
```

### SEMIPRIME → COMPOSITE (promotion)

```
PROMOTE iff:
  - multiple semiprime supports align
    (len(supporting_ids) >= 2)
  - recurrence and utility cross threshold
    (promotion_score(path) >= 0.85 using RGMem formula)
  - retrieval benefit is measurable
    (utility_score from at least one successful retrieval)
```

### COMPOSITE → SEMIPRIME (demotion)

```
DEMOTE iff:
  - higher-order bundle decays (heat_score drops below 0.1)
  - but core bridge (one SEMIPRIME) remains valid
  - forgetting_state transitions to ARCHIVED or STALE
  - supporting_ids drops to 1 surviving semiprime
```

### SEMIPRIME → REAL (demotion)

```
DEMOTE iff:
  - closure fails under replay
    (recurrence_count decrements to 0 from new contradictions)
  - support vanishes (all parent_event_ids become DEAD)
  - it was noise mistaken for structure
    (evidential_status transitions to CONTRADICTED with no surviving support)
```

### Reversibility principle

This gives CK **reversible learning**. Not one-way accumulation. A crystal that loses its SEMIPRIME support becomes a path, then demotes further. A mistaken SEMIPRIME reverts to REAL. The tier is not a rank — it is a structural description that can move in both directions as the evidence changes.

---

## PART 11 — Training Path Note: Why Semiprime Is the Transferable Layer

### The training strategy implication

The ternary ontology changes what CK pre-training packs should contain:

| Content type | Include in foundation pack? | Reason |
|-------------|---------------------------|--------|
| REAL events (raw episodes) | Minimally | Local, sensory, user-specific; poor transfer |
| SEMIPRIME motifs (minimal closures) | **YES — primary content** | First generalizable structure; transfers well |
| COMPOSITE crystals (high-order) | Some, domain-general only | Too specific to user workflow; may not transfer |

### Why SEMIPRIME transfers best

REAL is local and sensory: a specific OCR token or telemetry spike from one machine has no transfer value.

COMPOSITE is domain-specific: a crystal encoding a specific workflow for a specific user's email client transfers poorly to a different user's editor.

SEMIPRIME is the correct transfer layer because:
1. It is abstract enough to apply across different REAL contexts
2. It is concrete enough to be unambiguous and testable
3. It corresponds exactly to what MACLA's 187 procedures represent: minimal reusable closures extracted from 2,851 raw trajectories

**Grounding:** MACLA compresses 2,851 ALFWorld training trajectories into 187 reusable procedures through semantic abstraction and duplicate detection, demonstrating efficient knowledge distillation. Those 187 procedures are the SEMIPRIME layer of the ALFWorld task domain. The 2,851 trajectories are the REAL layer. The system grows by having rich SEMIPRIME structure, not rich REAL logs.

### Practical pre-training spec

Foundation packs for CK should contain:
- SEMIPRIME motifs for common desktop patterns (file open-close, window focus-switch, terminal command sequences)
- SEMIPRIME motifs for common user interaction closures (click-type-confirm, search-select-open)
- Some COMPOSITE crystals for universal workflow patterns (save-backup, compile-run-debug)
- Minimal REAL data: only enough to calibrate generator_extract rules, not to fill memory

---

## PART 12 — Metrics Block

| Metric | Definition | Target |
|--------|-----------|--------|
| `real_to_semiprime_rate` | SEMIPRIME promotions / REAL events processed (rolling 24h) | > 0.10 (at least 10% of REAL contact closes into SEMIPRIME) |
| `semiprime_to_composite_rate` | COMPOSITE promotions / SEMIPRIME objects (rolling 7d) | > 0.05 (at least 5% of SEMIPRIME bridges crystallize) |
| `composite_reuse_rate` | Retrievals resolved by COMPOSITE / total retrievals | > 0.30 at day 30 |
| `false_semiprime_rate` | SEMIPRIME objects demoted back to REAL / total SEMIPRIME created | < 0.15 (< 15% of SEMIPRIME was noise) |
| `dead_composite_rate` | COMPOSITE objects reaching DEAD state within 7 days of creation | < 0.10 (< 10% of composites are immediately useless) |

**Dashboard display:**

```python
def tier_health_report():
    real = memory_store.count(tier_class="REAL")
    semi = memory_store.count(tier_class="SEMIPRIME")
    comp = memory_store.count(tier_class="COMPOSITE")
    
    print(f"REAL:      {real:6d}  (contact layer)")
    print(f"SEMIPRIME: {semi:6d}  (bridge layer, ratio: {semi/max(real,1):.2f})")
    print(f"COMPOSITE: {comp:6d}  (structure layer, ratio: {comp/max(semi,1):.2f})")
    print()
    print(f"R→S rate: {real_to_semiprime_rate():.3f}  (target > 0.10)")
    print(f"S→C rate: {semiprime_to_composite_rate():.3f}  (target > 0.05)")
    print(f"C reuse:  {composite_reuse_rate():.3f}  (target > 0.30 at day 30)")
    print(f"False S:  {false_semiprime_rate():.3f}  (target < 0.15)")
```

---

## PART 13 — Claim

**"CK grows by turning REAL contact into SEMIPRIME bridges and SEMIPRIME bridges into COMPOSITE reusable structure — where REAL is the direct encounter with the world before any closure, SEMIPRIME is the first stable closure that survives re-encounter and becomes reusable, and COMPOSITE is the higher-order structure built from multiple semiprime supports that enables efficient handling of new REAL events without re-deriving the structure from scratch."**

---

## PART 14 — Boundary

**"What is not yet established is whether the REAL → SEMIPRIME → COMPOSITE ontology gives better compression, retrieval, and adaptation than the earlier flatter memory language once measured on real workstation data — specifically, whether the false_semiprime_rate (< 0.15 target) is achievable with rule-based tier assignment before Class 1 LoRA is trained, and whether the semiprime_to_composite_rate (> 0.05 target) produces enough COMPOSITE structure within 30 days on real workstation patterns to make the ternary overhead worthwhile."**
