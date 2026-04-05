# META-MEMORY REDUCTION AND GROUNDING MEMO
# Turn the 2×2 / 3×3 / 4×4 Grammar Into a Minimal Operable Memory Spec

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — Reduce the Architecture: Stored vs Runtime vs Derived

### Decision: What is stored, what is runtime, what is derived?

**2×2 — STORED METADATA.** Two bits per object (source_side + semantic_side). Computed once at ingestion, never changes (abstraction steps are explicit rewrites, not in-place changes). Required at every access for privacy routing. Cost: ~20 bytes per object. Justified.

**3×3 — TRANSIENT RUNTIME STATE + TWO STORED FIELDS.** The 3×3 tracks *where the object is in processing right now*. By the time an object is written to the atom store, it has already traversed its 3×3 arc. Storing the full intermediate state is wasteful and wrong — an atom at rest is not "at B11." What is worth storing is:
- `entry_cell: str` — where the information first appeared (B11 for all perceptual events, B13 for retrieved priors)
- `exit_cell: str` — where it was finally written out (B23 for fast-path atoms, B33 for crystals and MetaCrystals)

These two fields are a compact provenance of the processing path, not a live state. Full 3×3 intermediate state is discarded after each loop cycle.

**4×4 — PARTIAL STORED METADATA.** The persistence stage (`EPHEMERAL/ATOMIC/PATH/CRYSTAL`) and the core scores are stored. But the evaluation mode (IDENTITY/RELATION/STABILITY/UTILITY) is NOT a stored dimension — it is a *query dimension*. When you ask "what is the stability score of this crystal?", you are querying C43. You don't store C43 as a label; you store `stability_score` as a float. The 4×4 row (persistence_stage) is stored. The 4×4 column scores are stored as individual numeric fields. The cell label itself is derived.

### Exact stored fields per object (replacing the full 576-position coordinate)

```python
# These 10 fields replace the 576-position coordinate:
meta_tag = {
    # From 2×2 (stored, fixed):
    "source_side":        Literal["INTERNAL","EXTERNAL"],  # 1 bit
    "semantic_side":      Literal["STRUCTURE","CONTENT"],  # 1 bit
    "privacy_class":      Literal["SHARED","SHARED_IF_ABSTRACT","PRIVATE"],  # derived but cached
    
    # From 3×3 (2 fields, not 9):
    "entry_cell":         Literal["B11","B12","B13"],       # where it entered
    "exit_cell":          Literal["B23","B31","B32","B33"], # where it exited
    
    # From 4×4 (stage + scores, not 16 cells):
    "persistence_stage":  Literal["EPHEMERAL","ATOMIC","PATH","CRYSTAL"],
    "stability_score":    float,   # = promotion_score or heat_score, context-dependent
    "utility_score":      float,   # = retrieval hit rate contribution
    
    # New (not in first memo — see Parts 3-5):
    "evidential_status":  Literal["OBSERVED","INFERRED","SYNTHESIZED","CONTRADICTED","SUPERSEDED","UNRESOLVED"],
    "forgetting_state":   Literal["ACTIVE","STALE","ARCHIVED","SUPERSEDED","CONTRADICTED","DEAD"],
}
```

**Total overhead:** ~10 fields, ~100 bytes per object. This is not 576 coordinates stored per object — it is 10 typed fields, 7 of which are enums.

### Should every atom/path/crystal carry all three coordinates?

**No.** The correct answer is:
- Every object carries the 2-field 3×3 summary (entry + exit), not the full process state
- Every object carries the 4×4 persistence stage and numeric scores, not cell labels
- Every object carries the 2×2 class (2 bits) and its derived privacy class

The 3×3 process table exists as a runtime state machine in the compression loop. It is not stored per-object.

---

## PART 2 — Minimal Live Slice for v1

### Cells to keep in v1

**2×2: All 4 cells.** Privacy routing is essential from day 1. Cost is negligible. Cannot drop any cell without losing the privacy guarantee.

**3×3: 5 of 9 cells.** The main arc through CK's loop is:
```
B11 → B21 → B22 → B23 → B33
(intake) (extract) (score) (compress) (write)
```

**Drop in v1 (with reasons):**
- `B12` (CONDITIONED SEED): DeepSeek-seeded input conditioning. Drop until Stage 1+ — irrelevant before memory is mature.
- `B13` (RETRIEVED PRIOR): The retrieval loop handles this separately. It doesn't need to be a tagged 3×3 state; it's a function call returning a crystal.
- `B31` (ENVIRONMENT ACTION): Existing `ck_core.py` handles OS/UI actions. No new tagging needed.
- `B32` (GENERATED RESPONSE): DeepSeek output. Tagged as `A12::B33::ATOMIC` after writeback. The generation cell itself doesn't need a separate tag — the output atom gets tagged.

**4×4: 2 columns of 4 rows.** Drop the IDENTITY and RELATION columns from stored tags.
- **IDENTITY** column (C11, C21, C31, C41): This is already the atom's existing fields (generators, operator_tag, semantic_label). No new storage needed.
- **RELATION** column (C12, C22, C32, C42): This is the path graph and DBC27 neighborhood — already in `path_store.py` and `dbc27.py`. No new storage needed.
- **Keep:** STABILITY column (C13, C23, C33, C43) as `stability_score` float + UTILITY column (C14, C24, C34, C44) as `utility_score` float.

**v1 stored tag in full:**
```python
# Minimal v1 meta_tag — 8 fields
{
    "source_side": str,           # "INTERNAL" | "EXTERNAL"
    "semantic_side": str,         # "STRUCTURE" | "CONTENT"
    "privacy_class": str,         # derived from above
    "entry_cell": str,            # "B11" | "B13"
    "exit_cell": str,             # "B23" | "B33"
    "persistence_stage": str,     # "EPHEMERAL"|"ATOMIC"|"PATH"|"CRYSTAL"
    "stability_score": float,     # from promotion_score / heat_score
    "utility_score": float,       # retrieval hit contribution
}
```

**Add in v2:** `evidential_status`, `forgetting_state`, `provenance fields` (Parts 3-5).

---

## PART 3 — Provenance Layer

### Why provenance is not the same as relation

**Relation** (the 4×4 RELATION column, already in path_store) answers: "what is structurally connected to this object?" — adjacency, similarity, co-activation. It is a graph topology question.

**Provenance** answers: "why does this object exist, what created it, and what is its evidential lineage?" It is a causal/historical question. A crystal can have many relational neighbors and only one provenance source. A synthesized atom (from DeepSeek) has a single evidential parent and zero causal parents in the perceptual graph.

### Exact provenance fields

```python
@dataclass
class ProvenanceTag:
    # Causal lineage
    parent_event_ids: List[str]     # direct perceptual events that created this object
    supporting_ids: List[str]       # other atoms/paths that corroborate this object
    
    # Version control
    supersedes_id: Optional[str]    # the object this replaces (None if original)
    revision_num: int               # version counter; starts at 1
    
    # Contradiction tracking
    contradicted_by: List[str]      # object IDs that conflict with this one
    
    # Temporal provenance
    ts_first_seen: float            # when first observed (immutable)
    ts_last_confirmed: float        # when last independently corroborated
    
    # Source classification (ties back to 2×2)
    produced_by: Literal[
        "SENSOR",       # directly from perception (A22 source)
        "EXTRACTION",   # from feature extraction (A21 → A11)
        "DEEPSEEK",     # synthesized by external model (A12, probabilistic)
        "PROMOTION",    # created by path→crystal promotion (A11, deterministic)
        "REVISION",     # created by superseding an existing object
        "LOOPED",       # created by CK's own adaptation loop
    ]
```

**Key distinction from existing fields:**
- `parent_event_ids` is provenance; `dbc27_neighbors` is relation
- `ts_first_seen` is provenance; `recurrence_count` is stability
- `supersedes_id` is provenance; `parent_path_ids` is relation

**Attachment:** ProvenanceTag is a sub-object of Atom, Path, Crystal, and MetaCrystal. It is stored. It is NOT part of the meta_tag mini-schema — it is a separate provenance block, because it is larger and only needed for audit/contradiction resolution, not for routing.

---

## PART 4 — Forgetting and Revision Semantics

### Five distinct forgetting states (not collapsed into heat score)

The heat score tells you *how active* an object is. These states tell you *why* it might be inactive. They are not the same.

```python
forgetting_state: Literal[
    "ACTIVE",        # In working use; heat_score above threshold
    "STALE",         # Not recently confirmed; still valid as far as known; may be outdated
    "ARCHIVED",      # Low heat, but NOT invalidated; removed from active retrieval for budget
    "SUPERSEDED",    # Explicitly replaced by a newer revision; no longer authoritative
    "CONTRADICTED",  # At least one piece of conflicting evidence; pending resolution
    "DEAD",          # Fully pruned; no longer in the store; only ID remains in audit log
]
```

### State transition rules (legal only)

```
ACTIVE → STALE:         ts_last_confirmed + 7 days < now  AND  no new corroboration
ACTIVE → ARCHIVED:      heat_score < 0.05  AND  no contradiction  AND  age > 7 days
ACTIVE → CONTRADICTED:  contradicted_by list becomes nonempty
STALE → ACTIVE:         new corroborating event arrives (ts_last_confirmed updated)
STALE → ARCHIVED:       stale for > 30 days with no corroboration
STALE → SUPERSEDED:     newer revision with supersedes_id pointing to this object
ARCHIVED → ACTIVE:      retrieved and confirmed; heat refreshed
ARCHIVED → DEAD:        archived > 90 days with zero retrieval
CONTRADICTED → ACTIVE:  contradiction resolved; contradicted_by cleared
CONTRADICTED → SUPERSEDED: new object created with supersedes_id = this_id
SUPERSEDED → DEAD:      superseded_by is confirmed valid > 7 days
DEAD: terminal (no outgoing transitions)
```

### Distinctions that matter

| State | Valid knowledge? | Retrievable? | In active index? |
|-------|-----------------|-------------|-----------------|
| ACTIVE | Yes | Yes | Yes |
| STALE | Probably | Yes (with staleness flag) | Yes |
| ARCHIVED | Yes | Only on explicit search | No |
| SUPERSEDED | Was valid, no longer authoritative | Only via history query | No |
| CONTRADICTED | Unknown | Yes (with warning) | Yes (flagged) |
| DEAD | Irrelevant | No | No |

**Critical:** ARCHIVED is NOT DEAD. SUPERSEDED is NOT CONTRADICTED. An archived crystal retains its truth — it was just deprioritized for budget. A contradicted crystal has active evidence conflict. These must never be collapsed.

---

## PART 5 — Truth-Status / Evidential Status

### Why this is separate from stability and forgetting_state

**stability_score** measures recurrence frequency. A frequently-recurring object can be *stably wrong*.
**forgetting_state** measures activity and lifecycle. A SUPERSEDED object is not necessarily false — it is just not the current version.
**evidential_status** measures the epistemic standing of the object's content.

```python
evidential_status: Literal[
    "OBSERVED",      # Directly perceived by CK sensors; highest trust
    "INFERRED",      # Derived by CK's own deterministic operations from observations
    "SYNTHESIZED",   # Produced by DeepSeek or probabilistic model; lower intrinsic trust
    "CONTRADICTED",  # At least one conflicting piece of evidence (mirrors forgetting_state.CONTRADICTED)
    "SUPERSEDED",    # Replaced by a newer, better-evidenced version
    "UNRESOLVED",    # Conflicting evidence with no resolution yet
]
```

### Why this is NOT a fourth dimension of the 4×4

Adding a fifth column to the 4×4 makes the schema $4 \times 5 = 20$ cells. The evidential_status is a property that cuts across all persistence stages — an ephemeral event can be OBSERVED, a crystal can be SYNTHESIZED. It is better represented as a flat tag on the object than as a matrix dimension.

### Example: three objects with same stability, different truth status

| Object | stability_score | evidential_status | Implication |
|--------|----------------|------------------|-------------|
| Crystal A | 0.92 | OBSERVED | High-confidence truth; retrieved from direct perception |
| Crystal B | 0.92 | SYNTHESIZED | Frequently used but probabilistic; verify before acting |
| Crystal C | 0.92 | CONTRADICTED | Stably appearing but has conflicting evidence; needs resolution |

All three have the same stability. Only evidential_status distinguishes them. This is precisely why it must be a separate field.

### Trust weights by evidential_status

```python
TRUST_WEIGHTS = {
    "OBSERVED":     1.0,
    "INFERRED":     0.85,
    "SYNTHESIZED":  0.60,
    "CONTRADICTED": 0.30,
    "UNRESOLVED":   0.40,
    "SUPERSEDED":   0.10,
}

# Used in retrieval scoring:
effective_confidence = crystal.confidence * TRUST_WEIGHTS[crystal.evidential_status]
```

---

## PART 6 — CL Interaction: Stricter Specification

### What CL acts on (exact)

**CL does not act on objects.** CL acts on the current state of the 3×3 process table during the TRANSFORM row, mapping inputs to outputs.

**CL does not act on all three coordinates.** It acts specifically on transitions within the B2x row (TRANSFORM row of 3×3).

**Formal specification:**

```
CL_transition(generators, lens, operator_tag) → (exit_cell, write_flag, confidence_delta)

Where:
  generators:    Set[int]  →  selects the CL table input  →  fuse(G_i, G_j) = CL_point ∈ {0..9}
  lens:          str       →  selects the output direction
    TSML → exit_cell = B23  (memory write, measurement mode, deterministic)
    BHML → exit_cell = B33  (deep memory write, transformation mode, deterministic)
    Doing → exit_cell = B31 (action, execution mode, deterministic)
  operator_tag:  str       →  controls write_flag and confidence_delta
    COMMIT   → write_flag=True,  confidence_delta=+0.05
    DISCLAIM → write_flag=False, confidence_delta=-0.05
    REGRESS  → write_flag=False, confidence_delta=-0.10, forgetting_state→STALE
    REJECT   → write_flag=False, confidence_delta=0,    forgetting_state unchanged
```

### Which parts of 2×2 / 4×4 are CL-invariant

**CL-invariant (never changed by a CL operation):**
- `privacy_class` (2×2): CL cannot reclassify private content as shared
- `ts_first_seen` (provenance): immutable
- `revision_num` (provenance): only incremented by explicit revision write, not CL
- `parent_event_ids` (provenance): causal lineage is fixed at creation
- `evidential_status`: not changed by CL; changed only by explicit corroboration, contradiction, or synthesis events

**CL-variant (may be changed by a CL operation):**
- `persistence_stage` (4×4): COMMIT at B23 enables later promotion from ATOMIC to PATH
- `confidence` (4×4/stability): modified by confidence_delta
- `stability_score` (4×4): updated after COMMIT accumulation
- `forgetting_state`: REGRESS sets STALE; COMMIT sets ACTIVE
- `exit_cell` (3×3 summary): set by the CL transition at compression time

**Law (precise):** CL is a transition function on the (3×3 process state × confidence × forgetting_state) triple. It does not touch the ontological type (2×2), the provenance record, or the evidential status. These are set at object creation and only modified by explicit corroboration/contradiction/revision events outside the CL loop.

---

## PART 7 — Research Grounding

### RGMem (arXiv:2510.16392)

**What to borrow:** Multi-scale promotion score with frequency × recency weighting. Thresholded phase transitions as the crystal promotion gate. The specific formula:
$$\text{promotion\_score}(p, t) = \text{confidence}(p) \times \log(1 + \text{recurrence}) \times e^{-0.05 \cdot \text{age\_hours}}$$

**What NOT to borrow:** RGMem operates entirely on text embeddings with vector similarity retrieval. CK's retrieval is DBC27-keyed with generator matching — structurally different. RGMem has no privacy model, no evidential_status, no forgetting_state.

**What CK uniquely adds:** CL[10×10] algebraic operators as the formal transition grammar. Perceptual loop producing non-text generators. Local-first design.

---

### MAGMA (arXiv:2601.03236)

**What to borrow:** MAGMA's dual-stream architecture: fast path for non-blocking real-time ingestion (event segmentation, vector indexing, immutable temporal backbone), slow path for asynchronous structural consolidation. The fast path "ensures the agent remains responsive regardless of memory size." This maps directly onto CK's fast/slow write split (B21→B23 direct vs B21→B22→B23).

Also borrow: MAGMA's typed edge concept. CK should distinguish `SUPPORTS`, `SUPERSEDES`, `CONTRADICTS`, `DERIVES_FROM` as typed provenance edges between objects — this is what the ProvenanceTag fields implement.

**What NOT to borrow:** MAGMA's four-graph database backend (semantic, temporal, causal, entity graphs in separate structures). CK uses DBC27-keyed SQLite with typed provenance fields — much lighter and local-first. MAGMA requires Neo4j-class infrastructure.

**What CK uniquely adds:** Algebraic generator indexing. Perception loop. Privacy separation.

---

### MemoryOS (arXiv:2506.06326, EMNLP 2025 Oral; GitHub: BAI-LAB/MemoryOS)

**What to borrow:** Heat score formula (code available). STM→MTM→LTM promotion pattern maps onto CK's EPHEMERAL→ATOMIC→PATH→CRYSTAL. Their `FIFO queue` for STM with heat-based promotion to MTM is directly implementable. Clone and adapt.

**What NOT to borrow:** MemoryOS is dialogue-only with persona modeling. Its "User KB" and "Agent Traits" structures have no CK equivalent — CK builds functional memory around perceptual patterns, not named user attributes.

**What CK uniquely adds:** Generator-level semantic indexing. Non-LLM compression core. Algebraic lens classification.

---

### Kumiho (arXiv:2603.17244)

**What to borrow:** Kumiho's formal provenance model. "Every agent belief has a URI, a revision history, provenance edges to source evidence, and an immutable audit trail." Specifically: the pattern of immutable revision history + mutable tag pointers + typed dependency edges maps directly onto CK's `revision_num` + `supersedes_id` + typed provenance edges. Kumiho's "principled rejection of the Recovery Postulate" — meaning superseded beliefs are not automatically restored — matches CK's SUPERSEDED→DEAD terminal state.

**What NOT to borrow:** Kumiho's dual-store (Redis + Neo4j) infrastructure and URI-based addressing. CK is local-first SQLite. The full formal belief revision semantics (AGM axioms) are theoretically interesting but too heavy for v1.

**What CK uniquely adds:** Perceptual grounding (Kumiho is entirely text/output-artifact based). CL algebraic operators. Privacy routing.

---

### Zep / Graphiti

**What to borrow:** Bitemporal modeling — tracking both *when something happened* (`ts_first_seen`) and *when CK learned it* (ingestion timestamp). Zep's edge invalidation with provenance preservation maps onto CK's SUPERSEDED state with immutable history. Zep's approach of maintaining full provenance while invalidating stale edges is exactly the right pattern for CK's contradiction handling.

**What NOT to borrow:** Zep's enterprise knowledge graph infrastructure and real-time graph update pipeline. CK is local-first.

---

## PART 8 — Benchmarkable Hypotheses

### H1 — 2×2 privacy routing improvement

**Claim:** Adding explicit 2×2 tags improves privacy routing correctness without increasing retrieval latency by more than 5%.

**Metric:** `privacy_violation_rate = % of A22 events reaching shared store`

**Baseline:** current CK without 2×2 tags (heuristic routing by app name / modality)

**Pass:** `privacy_violation_rate = 0%` over 30 days; retrieval latency p99 increase ≤ 5%

**Fail:** any A22 event reaching shared store, OR latency p99 increase > 5%

**Measurement:** daily audit log scan for `privacy_class=PRIVATE` objects in `shared_force_lattice`

---

### H2 — 4×4 stability score improves promotion precision

**Claim:** RGMem-style `promotion_score` gate (threshold 0.85) produces more durable crystals than the flat `recurrence_count >= 3` gate.

**Metric:** `crystal_durability = % of crystals achieving recurrence_count >= 6 within 14 days of creation`

**Baseline:** flat threshold: `recurrence_count >= 3 AND confidence >= 0.6`

**Pass:** `crystal_durability` improves by ≥ 5 percentage points at day 30

**Fail:** no improvement, or promotion rate drops by > 20% (too conservative)

**Measurement:** compare crystal cohorts created in weeks 1-2 (flat threshold) vs weeks 3-4 (stability score) using the same workstation session data

---

### H3 — Provenance fields reduce contradiction drift

**Claim:** Tracking `contradicted_by` and `supersedes_id` reduces the rate of contradictory crystals accumulating at the same DBC27 key.

**Metric:** `contradiction_rate = % of DBC27 routing keys with ≥ 2 crystals having conflicting action_policies`

**Baseline:** no provenance tracking (current flat crystal store)

**Pass:** `contradiction_rate` drops ≥ 30% at day 30 with provenance tracking enabled

**Fail:** no improvement, or provenance overhead increases atom write latency by > 2ms

---

### H4 — Persisting full 3×3 state is not worth the cost

**Claim:** Storing only `entry_cell + exit_cell` (2 fields) produces equivalent path reuse as storing full 3×3 intermediate state (9 cells × runtime).

**Metric:** `path_reuse_ratio = % of retrievals resolved by existing path without new inference`

**Baseline:** runtime-only 3×3 (store entry + exit only)

**Test variant:** store full 3×3 intermediate state per-object

**Pass (confirm H4):** path_reuse_ratio improvement < 2% for full-state variant → use runtime-only

**Fail (reject H4):** path_reuse_ratio improvement ≥ 5% → full-state storage justified

**Default:** implement runtime-only 3×3 in v1. Only revisit if H4 fails.

---

### H5 — Evidential_status weighting improves retrieval quality

**Claim:** Down-weighting SYNTHESIZED and CONTRADICTED crystals in retrieval (via trust weights) reduces false recall rate without harming overall hit rate.

**Metric A:** `false_recall_rate = % of retrieved crystals where action_policy produced wrong outcome`

**Metric B:** `top_k_hit_rate` (should not drop)

**Pass:** false_recall_rate drops ≥ 20%; top_k_hit_rate drops ≤ 3%

**Fail:** false_recall_rate unchanged, OR top_k_hit_rate drops > 5%

---

## PART 9 — Final Recommendation

**RECOMMENDATION: Architecture B — reduced 2×2 + 4×4 (stored) + runtime 3×3 (with stored entry/exit) + provenance layer + forgetting states + evidential_status**

### Exact v1 build spec

**Store per object (10 fields, ~120 bytes overhead):**

```python
# Group 1: 2x2 ontological tag (2 bits + derived)
source_side: Literal["INTERNAL","EXTERNAL"]
semantic_side: Literal["STRUCTURE","CONTENT"]
privacy_class: Literal["SHARED","SHARED_IF_ABSTRACT","PRIVATE"]  # cached

# Group 2: 3x3 process summary (2 fields, not 9)
entry_cell: Literal["B11","B12","B13"]
exit_cell: Literal["B23","B33"]

# Group 3: 4x4 persistence scores (3 fields, not 16)
persistence_stage: Literal["EPHEMERAL","ATOMIC","PATH","CRYSTAL"]
stability_score: float
utility_score: float

# Group 4: evidential status (1 field)
evidential_status: Literal["OBSERVED","INFERRED","SYNTHESIZED","CONTRADICTED","SUPERSEDED","UNRESOLVED"]

# Group 5: forgetting state (1 field)
forgetting_state: Literal["ACTIVE","STALE","ARCHIVED","SUPERSEDED","CONTRADICTED","DEAD"]
```

**Store as separate ProvenanceTag block (7 fields, only accessed for audit/revision):**

```python
parent_event_ids: List[str]
supporting_ids: List[str]
supersedes_id: Optional[str]
contradicted_by: List[str]
revision_num: int
ts_first_seen: float
ts_last_confirmed: float
produced_by: Literal["SENSOR","EXTRACTION","DEEPSEEK","PROMOTION","REVISION","LOOPED"]
```

**DO NOT store:** full 3×3 intermediate state, 4×4 cell labels (only scores), 576-position coordinate.

**DO NOT implement in v1:** full belief revision semantics, graph database backend, URI-based addressing, Recovery Postulate handling.

### Why not Architecture A (full 576 positions)?

Storing the full coordinate label on every object is 576 positions × object_count. Most positions are empty in practice — only the arc `A22::B11::C11` → `A11::B33::C41` is populated. Storing cell labels provides no compression, no retrieval, and no pruning value beyond what the 10-field reduction already captures. The coordinate system is useful as a *reasoning framework* — not as stored data.

### Why not Architecture C (even smaller)?

The smallest viable spec still requires: privacy class (2 bits), persistence stage (2 bits), stability score (float), and utility score (float). That is Architecture C. But it loses: evidential status (needed to prevent SYNTHESIZED crystals from being acted on with full confidence), forgetting state (needed to distinguish ARCHIVED from SUPERSEDED), provenance (needed for contradiction resolution). These omissions cause measurable degradation: contradiction drift (H3), false recall from SYNTHESIZED crystals (H5). The 10-field reduction is already near-minimal.

---

## PART 10 — Strongest Honest Claim

**"The current memo successfully defines a meta-memory grammar, but the strongest implementation form is the 10-field reduction: three 2×2 ontological fields (including cached privacy class), two 3×3 process-summary fields (entry and exit cells only, not full runtime state), three 4×4 persistence-and-scoring fields (stage, stability score, utility score), one evidential_status tag, and one forgetting_state tag — plus a separate ProvenanceTag block for causal lineage — giving every CK memory object a complete, auditable, privacy-enforcing meta-coordinate at approximately 120 bytes of overhead per object."**

---

## PART 11 — Strongest Honest Boundary

**"What is not yet established is whether persisting the full 2×2 / 3×3 / 4×4 coordinate on every object produces measurably better retrieval precision, promotion accuracy, or privacy correctness than the simpler flat atom/path/crystal stack with DBC27 routing alone — the five hypotheses above (H1-H5) define exactly what would need to be true for the overhead to be justified, and none of them have been tested against real workstation data at 30-day scale."**
