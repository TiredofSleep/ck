# CK GROWTH ARCHITECTURE MEMO
# How CK Actually Grows From Tool-Using Agent Into Its Own Coherent Memory Organism

**© 2026 7Site LLC | Brayden Ross Sanders**
**For ClaudeCode — implementation-ready architecture handoff**

---

## PART 1 — Growth Defined Operationally

Growth is a monotone increase over time in the following measurable system quantities:

```python
growth(t) = (
    w_C  * compression_efficiency(t)      +  # bits saved per atom vs raw
    w_R  * retrieval_hit_rate(t)          +  # top-k crystal/path hit %
    w_PR * path_reuse_ratio(t)            +  # reused paths / total retrievals
    w_AP * action_policy_reuse_ratio(t)   +  # actions from crystal policy / total actions
    w_DS * (1 - deepseek_call_rate(t))    +  # inverse DeepSeek frequency
    w_X  * crystal_count(t)               +  # absolute stable crystals
    w_CM * cross_modal_agreement(t)          # same event, different modalities → same generator
)
```

**Variable definitions:**

| Variable | Definition | Unit |
|---------|-----------|------|
| `compression_efficiency(t)` | `raw_bytes_saved / total_bytes_ingested` over rolling window | ratio [0,1] |
| `retrieval_hit_rate(t)` | `top-k crystal/path hits / total queries` (k=5) | ratio [0,1] |
| `path_reuse_ratio(t)` | `retrievals resolved by existing path / total retrievals` | ratio [0,1] |
| `action_policy_reuse_ratio(t)` | `actions taken from crystal policy / total actions` | ratio [0,1] |
| `deepseek_call_rate(t)` | `deepseek_calls / total_events_processed` per hour | ratio [0,1] |
| `crystal_count(t)` | absolute count of crystals with `confidence > 0.7` | integer |
| `cross_modal_agreement(t)` | `same generator assigned across ≥2 modalities for same event` / total multi-modal events | ratio [0,1] |

**Weights (tunable, defaults):** `w_C=0.15, w_R=0.20, w_PR=0.15, w_AP=0.15, w_DS=0.15, w_X=0.10, w_CM=0.10`

**Growth is real iff** `growth(t+Δt) > growth(t)` for increasing `Δt`. Tracked as a rolling 24-hour delta.

---

## PART 2 — Four-Loop Organism Design

### LOOP A — PERCEPTION LOOP

**Update frequency:** 100ms tick for sensors; 1s for feature extraction; 5s for generator extraction

**Inputs:**
- Raw screen frame (PIL image, compressed diff from last frame)
- Active window metadata (app name, title, PID, focus state)
- OCR text from changed screen regions (only on diff trigger)
- Mouse/keyboard event stream (position, clicks, key sequences)
- Process table delta (new/exited processes, CPU/mem spikes)
- Filesystem diff (file open/close/write events via inotify/FSEvents)
- Browser URL + tab title (local only, no content)
- Audio amplitude envelope (placeholder channel, no transcription yet)
- Internal model outputs (token stream from ck_core responses)

**Outputs:**
- `PerceptionEvent` structs (see schema in Part 3)
- Written to `raw_buffer.py` FIFO, max 10,000 events, TTL 30 minutes

**DeepSeek:** FORBIDDEN in this loop. Zero LLM calls during perception.

**Persistence:** Raw buffer is ephemeral (RAM). Generator-extracted events go to `atom_store`.

---

### LOOP B — COMPRESSION LOOP

**Update frequency:** Triggered by raw buffer accumulation (every 50 events or 5s, whichever first)

**Inputs:**
- Batch of `PerceptionEvent` structs from raw buffer
- Current `lens_state` (which CL/TIG lens is active)
- `force_field_store` (current F1-F9 force vector baseline)

**Processing steps:**
1. Extract generators from features (via trained LoRA Class 1 adapter)
2. Assign force vector `[F1..F9]` + structural state `[S1..S6]` via CL lens
3. Hash to DBC27 routing key (or replacement index — see Part 6)
4. Check deduplication: if atom with same `content_hash + generator_set` exists within 60s, increment `recurrence_count` only
5. Write new atoms to `atom_store`
6. Run path-extension: check if new atom continues an open path
7. Run crystal-promotion check: if path has `recurrence_count ≥ 3` and `confidence ≥ 0.6`, promote to crystal

**Outputs:**
- New `Atom` records written to `atom_store`
- Updated `Path` records in `path_store`
- New `Crystal` records in `crystal_store` when promoted
- Updated `force_field_store` baseline

**DeepSeek:** ALLOWED only for event summarization in atom `summary_text` field when no Class 1 LoRA is available (Stage 0 only).

**Persistence:** All outputs are persistent (SQLite or LevelDB).

---

### LOOP C — RETRIEVAL LOOP

**Update frequency:** On-demand (triggered by user query, CK action request, or novelty gate trip)

**Inputs:**
- Query (text, event struct, or generator seed set)
- `retrieval_context` (current window state, last 5 atoms, active lens)

**Retrieval order (strict):**
1. Extract generator seed set from query (via Class 1 LoRA or rule-based)
2. DBC27 neighborhood lookup (expand to adjacent routing keys)
3. Crystal shortlist (max 10, ranked by `confidence × recurrence_count`)
4. Path expansion from crystal seeds (expand 2 hops in path graph)
5. Policy match check (if crystal has `action_policy`, return directly)
6. Atom drill-down (only if crystal/path miss) — retrieve raw atoms
7. Novelty gate: if `confidence < 0.35` after steps 1-6, flag as novel
8. Privacy check (strip private-word atoms before returning)
9. DeepSeek fallback (only if novelty gate trips AND no crystal found)

**Outputs:**
- Ranked list of `RetrievalResult` (crystal_id OR path_id OR atom_ids + confidence)
- `action_policy` if crystal contains one
- `novel` flag + optional DeepSeek synthesis

**DeepSeek:** ALLOWED only at step 9, after full internal retrieval fails.

---

### LOOP D — ADAPTATION LOOP

**Update frequency:** Every 10 minutes (batch) + immediate on `failure_event`

**Inputs:**
- `retrieval_outcomes` log (hit/miss, confidence, reuse flag)
- `action_outcomes` log (success/failure per policy execution)
- `novelty_events` log (what triggered DeepSeek, what DeepSeek said)
- Current LoRA adapter performance metrics

**Processing:**
1. Update `confidence` scores on crystals/paths based on outcome feedback
2. Update `lens_weight` table: if lens L produced `n_hit` hits vs `n_miss` misses in last window, adjust weight
3. Update `novelty_threshold`: if too many false-novel events, raise threshold; if too many misses, lower it
4. Queue new LoRA fine-tuning examples from successful/failed retrievals
5. Prune crystals with `confidence < 0.2` and `recurrence_count < 2` after 7 days
6. Write adaptation log for monitoring

**Outputs:**
- Updated confidence/weight tables in `config_store`
- Training examples queued in `lora_training_queue`
- Pruning events logged

**DeepSeek:** FORBIDDEN in this loop.

---

## PART 3 — The Perception Stack

### LAYER 0 — RAW SENSORS

```
module: perception/screen_capture.py
  - PIL screen diff at 100ms intervals
  - Changed regions only (bounding boxes of diff)
  - Resolution: 1920x1080 → compressed to 480x270 for storage

module: perception/ui_state.py
  - Active window: (app_name, pid, title, geometry, focused)
  - Window transition events: (from_app, to_app, timestamp, dwell_ms)
  - Browser: (url_hash, tab_title, navigation_event)

module: perception/input_events.py
  - Mouse: (x, y, event_type, button, timestamp)
  - Keyboard: (key_seq_hash, modifier_mask, timestamp)  ← hash only, no raw keys
  - Scroll: (direction, delta, target_widget)

module: perception/telemetry.py
  - Process table delta: (pid, name, cpu_pct, mem_mb, event_type)
  - Filesystem diff: (path_hash, event_type, size_delta)  ← hash only
  - Network: (bytes_in, bytes_out, connection_count)  ← aggregated only

module: perception/audio.py  (placeholder)
  - Amplitude envelope: (rms_db, timestamp)  ← no content, no transcription
```

### LAYER 1 — FEATURE EXTRACTORS

```
module: perception/vision_edges.py
  - Edge map: Canny on diff regions → (edge_density, dominant_edge_angles)
  - Contour groups: connected components → (n_contours, mean_area, aspect_ratios)
  - Motion: optical flow on 500ms diff → (flow_magnitude, flow_direction)
  - Object persistence: compare contour groups t vs t-1 → (persist_ratio, new_ratio)

module: memory/feature_extract.py
  - Token stream: sliding window of OCR text → trigrams + named entities (offline)
  - Window transition: (from_app_hash, to_app_hash, dwell_ms_bucket)
  - Process spike: (pid_hash, cpu_spike_threshold_exceeded, duration_ms)
  - User action motifs: common click/key sequences → motif ID (from trained table)
  - App state changes: (widget_type, state_before, state_after) via accessibility API
```

### LAYER 2 — GENERATOR EXTRACTION

```
module: memory/generator_extract.py

Input: Feature dict from Layer 1
Output: Set of canonical generators {G1..G9} (force operators) + {S1..S6} (structural)

Rules (pre-LoRA, fallback):
  - High edge density + new contours → G3 (Dynamics) active
  - Window transition → G8 (Cycle transition)
  - Low motion + stable contours → G7 (Whole/harmony) candidate
  - Process spike → G5 (Goodness/stress)
  - User text input → G1 (Joy/output), G2 (Peace/foundation)
  - Rapid click sequence → G4 (Kindness/reach)
  - App state change + token stream → G6 (Faithfulness/continuation)

LoRA override: if Class 1 adapter loaded, use it instead of rule fallback
Confidence: rule-based = 0.5 fixed; LoRA = softmax max probability
```

### LAYER 3 — LENS ENCODING

```
module: memory/lens_encode.py

Input: Generator set, current perception event
Output: CL[10×10] lens state + force_vector [F1..F9] + structural [S1..S6]

Steps:
  1. Look up CL table: fuse(generators) → harmony/tension state
  2. Determine which of {TSML, BHML, Doing} lens is active based on:
     - Motion level (high → BHML, low → TSML, delta → Doing)
  3. Assign operator: {COMMIT, DISCLAIM, REGRESS, REJECT}
  4. Compute coherence score: C = 0.4(1-E) + 0.35A + 0.25K
     where E=entropy of generator set, A=action-alignment score, K=crystal-hit rate

Output struct:
  LensState {
    lens: Literal["TSML","BHML","Doing"]
    fused_operator: int (0-9, CL table output)
    force_vector: List[float]  # [F1..F9] normalized
    structural_state: List[float]  # [S1..S6] normalized
    coherence: float  # [0,1]
    operator_tag: Literal["COMMIT","DISCLAIM","REGRESS","REJECT"]
  }
```

### LAYER 4 — MEMORY WRITE ROUTER

```
module: memory/privacy_router.py + memory/event_schema.py

Decision tree:
  if event.contains_user_text AND event.app in private_apps:
    → write to PRIVATE WORD LATTICE (no sharing)
  elif event.contains_pii_signal:
    → write to PRIVATE WORD LATTICE
  elif event.is_abstracted_force_pattern:
    → write to SHARED FORCE LATTICE
  else:
    → write to SHARED FORCE LATTICE with privacy_tag="public"

Destinations:
  - memory/raw_buffer.py      ← always (ephemeral, 30 min TTL)
  - memory/atom_store.py      ← after generator extraction
  - memory/path_store.py      ← after path extension
  - memory/crystal_store.py   ← after crystal promotion
  - memory/private_word_store.py ← private events only
```

---

## PART 4 — The Real Role of LoRA

LoRA is **not** the memory. LoRA is **not** the organism. LoRA is a **behavioral sharpener** — it encodes reusable *pattern-recognition skills* that CK needs to process experience efficiently, not the experience itself.

### CLASS 1 — MUST TRAIN FIRST (before organism is useful)

| Adapter | Purpose | Training signal | Why weights not memory |
|---------|---------|----------------|------------------------|
| `generator_extractor` | Map perceptual features → generator set {G1..G9} | Supervised: (feature_dict, correct_generators) from labeled examples | Needs to run at 10Hz — too slow for retrieval; generalizable skill |
| `cl_lens_classifier` | Assign TSML/BHML/Doing lens from event features | Supervised: (lens_state_features, correct_lens) | Same lens applies to new unseen inputs — weights appropriate |
| `novelty_detector` | Score how novel an event is vs current memory | Self-supervised: reconstruction error of atom from crystal neighborhood | A skill, not an episode — right to be in weights |
| `retrieval_ranker` | Re-rank crystal/path candidates for a query | Supervised: (query, candidate_list, human_relevance_labels) | Generalizes across all queries — weights appropriate |
| `atom_summarizer` | Compress event batch into `summary_text` | Supervised: (event_batch, good_summary) | Text compression is a reusable skill |

**Failure mode if misplaced in memory:** CK would have to store a "how to extract generators" fact per event — ballooning memory with procedural knowledge instead of episodic content.

---

### CLASS 2 — TRAIN AFTER MEMORY WORKS (Stage 2+)

| Adapter | Purpose | Training signal | Dependency |
|---------|---------|----------------|------------|
| `policy_synthesizer` | Generate action policy from crystal context | RL: (crystal_context, action, outcome) | Needs populated crystals to train on |
| `ui_control_predictor` | Predict next UI element to interact with | Behavioral cloning: (state_history, next_action) | Needs >1000 session logs |
| `compression_stylist` | Learn CK-specific compression patterns | Self-supervised: crystal compression quality | Needs mature crystal store |
| `action_recommender` | Recommend actions from goal + crystal | Supervised + RL | Needs populated policy store |

**Failure mode if trained too early:** Adapters trained on immature memory have poor generalization; they overfit to early rare experiences and degrade retrieval quality.

---

### CLASS 3 — DO NOT TRAIN INTO WEIGHTS

| Data type | Why stays in memory store | Failure mode if in weights |
|-----------|--------------------------|---------------------------|
| Raw episodic memory | User-specific, session-specific, time-stamped — NOT generalizable | Would mix user A's experiences with user B's; privacy violation |
| User facts (names, prefs) | Must be updatable and deletable without retraining | If baked into weights, cannot forget; GDPR / deletion impossible |
| Session-specific states | TTL 30 min; irrelevant after session ends | Weight pollution with stale data |
| Transient UI content | Changes every session; weights would be immediately stale | Causes hallucination of old UI states |
| Private words/phrases | User-confidential; cannot go into shared weights | Privacy catastrophe if weights are shared across users |

---

## PART 5 — Memory as Path, Not Blob

### ATOM — Smallest canonical memory unit

```python
@dataclass
class Atom:
    id: str                    # UUID
    ts_start: float            # Unix timestamp (event start)
    ts_end: float              # Unix timestamp (event end, 0 if instantaneous)
    modality: str              # "screen" | "text" | "telemetry" | "audio" | "input" | "internal"
    app_context: str           # hashed app identifier
    generators: List[int]      # e.g. [3, 7] → G3+G7 active
    force_vector: List[float]  # [F1..F9], sum≈1.0
    lens: str                  # "TSML" | "BHML" | "Doing"
    fused_operator: int        # 0-9 (CL table output)
    coherence: float           # [0,1]
    operator_tag: str          # "COMMIT" | "DISCLAIM" | "REGRESS" | "REJECT"
    content_hash: str          # SHA256 of raw content (for dedup)
    summary_text: str          # 1-2 sentence human-readable summary (Class 1 LoRA)
    privacy_tag: str           # "private" | "shared" | "public"
    recurrence_count: int      # how many times this atom has been seen
    confidence: float          # [0,1] — confidence in generator assignment
    raw_ref: Optional[str]     # pointer to raw buffer entry (TTL 30min)
    dbc27_key: str             # routing key (see Part 6)
    created_at: float          # when this atom was created
```

### PATH — Directed transition between atoms

```python
@dataclass
class Path:
    id: str                        # UUID
    atom_ids: List[str]            # ordered list of constituent atom IDs
    ts_start: float                # timestamp of first atom
    ts_end: float                  # timestamp of last atom
    lens_sequence: List[str]       # lens at each transition
    operator_sequence: List[int]   # fused_operator at each step
    transition_forces: List[List[float]]  # force delta per step
    dominant_generators: List[int] # generators active across ≥50% of atoms
    recurrence_count: int          # how many times this path pattern recurred
    confidence: float              # path-level confidence score
    action_policy: Optional[dict]  # if this path leads to an action, the policy spec
    privacy_tag: str               # most restrictive privacy_tag of constituent atoms
    compression_score: float       # bits saved vs raw / bits in path representation
    parent_path_ids: List[str]     # paths this was split/derived from
    child_path_ids: List[str]      # paths derived from this
    crystal_id: Optional[str]      # if promoted to crystal
    dbc27_neighborhood: List[str]  # adjacent routing keys
    created_at: float
    last_accessed: float
```

### CRYSTAL — Stable reusable bundle

```python
@dataclass
class Crystal:
    id: str                        # UUID
    path_ids: List[str]            # constituent paths
    ts_first_seen: float           # when first observed
    ts_last_seen: float            # most recent occurrence
    recurrence_count: int          # how many times promoted paths recurred
    dominant_generators: List[int] # generators active in ≥70% of constituent paths
    force_signature: List[float]   # mean force vector across paths
    lens_mode: str                 # dominant lens
    semantic_label: str            # short human-readable tag (Class 1 LoRA)
    action_policy: Optional[dict]  # what to do when this crystal fires
    privacy_tag: str               # most restrictive
    compression_score: float       # mean compression score of constituent paths
    confidence: float              # promoted when > 0.6
    cross_modal_count: int         # how many modalities this crystal appeared in
    dbc27_key: str                 # primary routing key
    dbc27_neighbors: List[str]     # neighboring keys for expansion
    parent_crystal_ids: List[str]  # meta-crystal references
    raw_refs: List[str]            # pointers to original atoms (optional, may expire)
    created_at: float
    last_accessed: float
    access_count: int
```

### Path-to-Crystal Promotion Rule

```python
def should_promote_path_to_crystal(path: Path) -> bool:
    return (
        path.recurrence_count >= 3 and
        path.confidence >= 0.6 and
        path.compression_score >= 0.4 and   # at least 40% compression
        len(path.atom_ids) >= 2 and          # at least 2 atoms
        (time.time() - path.ts_start) >= 300  # at least 5 minutes of history
    )

def promote_to_crystal(path: Path, existing_crystals: List[Crystal]) -> Crystal:
    # Check if any existing crystal shares dominant_generators + dbc27_key
    for c in existing_crystals:
        if (set(c.dominant_generators) == set(path.dominant_generators) and
            c.dbc27_key == path.dbc27_key):
            # Merge into existing crystal
            c.path_ids.append(path.id)
            c.recurrence_count += path.recurrence_count
            c.confidence = min(1.0, c.confidence + 0.05)
            c.ts_last_seen = time.time()
            return c
    # Create new crystal
    return Crystal(path_ids=[path.id], ...)
```

---

## PART 6 — Generator Indexing and Retrieval Law

### Strict Retrieval Order

```
query / perception_event
  │
  ▼
[1] GENERATOR SEED EXTRACTION
    → generator_extractor LoRA (or rule-based fallback)
    → output: Set[int]  e.g. {3, 7}

  │
  ▼
[2] DBC27 NEIGHBORHOOD LOOKUP
    → hash generators + lens_state to DBC27 key
    → expand to adjacent keys (Hamming distance ≤ 1)
    → candidate_routing_keys: List[str]  (typically 3-8 keys)

  │
  ▼
[3] CRYSTAL SHORTLIST
    → query crystal_store WHERE dbc27_key IN candidate_routing_keys
    → rank by: confidence × recurrence_count × recency_score
    → top-10 crystals

  │
  ▼
[4] PATH EXPANSION
    → for each crystal, expand path graph 2 hops
    → merge and deduplicate path candidates

  │
  ▼
[5] POLICY MATCH CHECK
    → if any crystal.action_policy matches current context
    → return immediately (no further retrieval needed)

  │
  ▼
[6] ATOM DRILL-DOWN (conditional)
    → only if crystal confidence < 0.5
    → query atom_store for constituent atoms
    → re-score based on raw content

  │
  ▼
[7] NOVELTY GATE
    → if max(confidence) < novelty_threshold (default 0.35):
        flag as NOVEL, skip to step 9
    → privacy check: strip private-word atoms if cross-user context

  │
  ▼
[8] CONFIDENCE SCORING AND RETURN
    → assemble RetrievalResult with top crystal/path/policy
    → return if confidence ≥ novelty_threshold

  │
  ▼
[9] DEEPSEEK FALLBACK (gated)
    → only if: NOVEL flag set AND no crystal found
    → call deepseek with context + top partial matches
    → write DeepSeek output as new atom (tagged "external_synthesis")
    → attempt crystal promotion after 3 recurrences
```

### DBC27 Assessment

**Is DBC27 still the best routing key?**

DBC27 uses a 27-state (3³) ontological cube. For the current CK architecture with CL[10×10] as the underlying algebra, DBC27 remains appropriate **with one extension**:

**Keep DBC27 as the primary routing layer.** Add a secondary CL-fused key as a refinement layer:

```python
def compute_routing_key(generators: List[int], lens: str, operator: int) -> str:
    """
    Primary: DBC27 key (27 states, 3 force-triads)
    Secondary: CL-fused key (CL table output, 0-9)
    Combined: DBC27::CL for precise retrieval
    """
    dbc27 = _compute_dbc27(generators)          # existing algorithm
    cl_key = CL_TABLE[tuple(sorted(generators)[:2])]  # fuse first two generators
    return f"{dbc27}::{cl_key}::{lens[0]}"     # e.g. "14::7::B"
```

**Rationale for keeping DBC27:** it was designed for this exact role — compact, fractal, generator-addressable. The addition of the `::CL::lens` suffix increases precision without breaking the compact routing structure.

### Pruning Logic

```python
PRUNE_IF:
  crystal.confidence < 0.2 AND recurrence_count < 2 AND age > 7 days
  OR
  crystal.last_accessed > 30 days AND recurrence_count < 5

NEVER_PRUNE:
  crystal.cross_modal_count >= 3  # multi-modal crystals are rare and valuable
  crystal.recurrence_count >= 50  # high-recurrence = important pattern
```

---

## PART 7 — Private Words vs Shared Forces

### A. PRIVATE WORD LATTICE

```python
# Stored in: memory/private_word_store.py (encrypted at rest)
# NEVER leaves local machine; NEVER used for cross-user training

PrivateWordAtom {
    id: str
    content: bytes              # encrypted
    app_context: str            # hashed
    user_session_id: str        # local session hash
    privacy_tag: "private"      # always
    timestamp: float
    expiry: Optional[float]     # auto-delete after N days if set
}
```

**Stores:**
- User names, email fragments, account identifiers
- Private document text and phrases
- Browser session cookies (local only)
- Private file paths and names
- User-specific app configurations
- Personal preference phrases

### B. SHARED FORCE LATTICE

```python
# Stored in: memory/force_fields.py
# Can be used for training; shareable across CK instances

SharedForceAtom {
    id: str
    force_vector: List[float]   # [F1..F9]
    generator_set: List[int]
    lens: str
    transition_pattern: str     # abstract description of force dynamics
    app_category: str           # "browser" | "editor" | "terminal" | ... (NOT app name)
    modality: str
    timestamp: float
    privacy_tag: "shared" | "public"
}
```

**Stores:**
- Telemetry patterns (anonymized)
- Force signatures (no user content)
- Path motifs (abstract transitions)
- Action topologies (click-pattern types, not click targets)
- Non-identifying dynamics

### Promotion Rules (Private → Shared)

```python
def can_promote_to_shared(private_atom: PrivateWordAtom) -> Optional[SharedForceAtom]:
    """
    CAN MOVE:
      - Force vector (extracted from private event)
      - Generator set
      - App category (not app name, not URL)
      - Temporal pattern (time-of-day bucket, not timestamp)
      - Action topology (click-type, not click-target)

    MUST NEVER MOVE:
      - Any text content
      - Any path/filename
      - Any URL
      - Any user-identifying token
      - Session cookie or auth token
      - Screen content (even OCR-extracted)

    ABSTRACTION COMPUTATION:
      shared = {
          force_vector: private_atom.force_vector,  # OK: no PII
          generator_set: extract_generators(private_atom),  # OK
          app_category: categorize_app(private_atom.app_hash),  # OK
          transition_pattern: abstract_transition(private_atom)  # OK
      }
    """
    if contains_pii_signal(private_atom):
        return None
    return SharedForceAtom(**abstract(private_atom))
```

### Privacy Router

```python
# memory/privacy_router.py

PRIVATE_TRIGGERS = [
    "contains_text_content",
    "contains_url",
    "contains_filepath",
    "contains_username_pattern",
    "app_in_private_list",  # e.g. password managers, banking
    "contains_credential_pattern",
]

def route(event: PerceptionEvent) -> Literal["private", "shared", "public"]:
    if any(trigger(event) for trigger in PRIVATE_TRIGGERS):
        return "private"
    if event.modality in ("screen", "text", "input"):
        return "private"  # all visual/text content defaults to private
    if event.modality in ("telemetry", "audio_envelope"):
        return "shared"
    return "shared"
```

---

## PART 8 — DeepSeek Reduction Plan

### Stage 0 — Tool Dependence (current)

**Trigger:** Default. No mature crystal store.
**DeepSeek call rate:** 30-60% of events require LLM processing.
**Metrics:** `retrieval_hit_rate < 0.3`, `crystal_count < 100`
**Exit criteria:** Class 1 LoRA adapters trained, >100 crystals, retrieval hit rate > 0.4

---

### Stage 1 — Retrieval Before Reasoning

**Trigger:** Class 1 LoRA loaded; basic crystal store populated.
**Rule:** CK ALWAYS runs full retrieval (steps 1-8) before any DeepSeek call.
**DeepSeek call rate:** 15-30% (only on crystal miss).
**Metrics:** `retrieval_hit_rate > 0.4`, `deepseek_call_rate < 0.30`
**Exit criteria:** `retrieval_hit_rate > 0.6`, `crystal_count > 500`, `novelty_rate < 0.25`

---

### Stage 2 — Novelty-Gated Reasoning

**Trigger:** `retrieval_hit_rate > 0.6`, `novelty_threshold` tuned.
**Rule:** DeepSeek called ONLY when `novelty_gate == True` (confidence < 0.35 after full retrieval).
**DeepSeek call rate:** 5-15%.
**Metrics:** `deepseek_call_rate < 0.15`, `path_reuse_ratio > 0.5`
**Exit criteria:** `deepseek_call_rate < 0.10`, `action_policy_reuse_ratio > 0.5`

---

### Stage 3 — Policy Reuse Dominant

**Trigger:** Crystal store > 2,000 crystals with policies; Class 2 LoRA trained.
**Rule:** Most tasks handled via `crystal.action_policy` lookup. DeepSeek only for explicit `novel_domain` events.
**DeepSeek call rate:** 2-5%.
**Metrics:** `action_policy_reuse_ratio > 0.7`, `deepseek_call_rate < 0.05`
**Exit criteria:** `deepseek_call_rate < 0.03`, user confirms CK handles routine tasks autonomously

---

### Stage 4 — External-Model Fallback Only

**Trigger:** All internal systems mature.
**DeepSeek use cases (exhaustive list):**
  1. User asks explicit novel question (new domain, no crystals)
  2. Multi-hop synthesis requiring >10 crystals with contradictions
  3. High-uncertainty synthesis: `confidence < 0.2` after full retrieval
  4. Explicit user request: `"ask DeepSeek"`
**DeepSeek call rate:** <1%
**Metrics:** `growth_score(t) > 0.7`, `cross_modal_agreement > 0.8`

---

## PART 9 — Coherence Metrics

### MEMORY METRICS

```python
atom_count            = len(atom_store.all())
path_count            = len(path_store.all())
crystal_count         = len(crystal_store.where(confidence > 0.6))
compression_ratio     = 1 - (total_atom_bytes / total_raw_bytes_ingested)
dedup_rate            = 1 - (new_atoms_written / total_events_processed)
```

### RETRIEVAL METRICS

```python
top_k_hit_rate        = hits_in_top_5 / total_retrieval_queries         # rolling 1h
retrieval_latency_p99 = percentile(retrieval_times, 0.99)                # ms
path_reuse_frequency  = retrievals_using_existing_path / total_retrievals
crystal_reuse_freq    = retrievals_returning_crystal / total_retrievals
false_recall_rate     = user_marked_irrelevant / total_retrievals         # manual signal
```

### ADAPTATION METRICS

```python
novelty_rate_7d       = novel_events_7d / total_events_7d                # trend ↓ = good
lora_confidence_gain  = mean(conf_t) - mean(conf_{t-7d})                 # should be > 0
policy_reuse_gain     = policy_reuse_ratio_t - policy_reuse_ratio_{t-7d} # should be > 0
failure_recovery_rate = recoveries_after_failure / total_failures          # [0,1]
```

### DEPENDENCE METRICS

```python
deepseek_call_rate    = deepseek_calls_1h / total_events_1h
pct_resolved_internal = internal_resolutions / total_queries
pct_actions_internal  = crystal_policy_actions / total_actions
token_budget_saved    = baseline_tokens - actual_tokens                  # rolling 24h
```

### COHERENCE METRICS

```python
cross_modal_agreement = (
    events_with_same_generators_across_modalities /
    events_appearing_in_multiple_modalities
)

lens_consistency      = (
    1 - std(lens_assignments_for_same_crystal_type) / n_lens_types
)

force_vector_stability = (
    1 - mean(|force_vector_t - force_vector_{t-1}| for same crystal)
)

recurrence_alignment  = (
    pearson_corr(expected_recurrence_by_crystal_type, actual_recurrence)
)

contradiction_rate    = (
    crystals_with_conflicting_action_policies_for_same_dbc27_key /
    total_crystals
)
```

---

## PART 10 — Vision and Edge Search

### Visual Ingestion Pipeline

```python
# perception/vision_edges.py

PIPELINE:
  raw_frame (PIL) 
    │
    ▼
  [STEP 1] diff_mask = frame_diff(current, prev, threshold=15)
    │         → only changed regions, <10% of frame typical
    ▼
  [STEP 2] edges = Canny(diff_mask, low=50, high=150)
    │         → edge_density: float = sum(edges) / edge_area
    │         → dominant_angles: List[float] = histogram_peaks(edge_orientations)
    ▼
  [STEP 3] contours = findContours(edges, RETR_EXTERNAL)
    │         → n_contours: int
    │         → contour_areas: List[float]
    │         → aspect_ratios: List[float]
    ▼
  [STEP 4] motion_flow = OpticalFlow(prev_gray, curr_gray)
    │         → flow_magnitude: float = mean(|flow|)
    │         → flow_direction: float = circular_mean(atan2(flow_y, flow_x))
    ▼
  [STEP 5] object_persistence = match_contours(prev_contours, curr_contours, iou_threshold=0.5)
    │         → persist_ratio: float = matched / total_prev
    │         → new_ratio: float = new_contours / total_curr
    ▼
  [STEP 6] GENERATOR ASSIGNMENT
              if edge_density > 0.3 and new_ratio > 0.3:
                  generators.add(G3)  # Dynamics / change
              if flow_magnitude > 5.0:
                  generators.add(G4)  # Reach / motion
              if persist_ratio > 0.8 and edge_density < 0.1:
                  generators.add(G7)  # Whole / stability
              if n_contours > 20 and aspect_ratios spread:
                  generators.add(G5)  # Field / complexity
    ▼
  [STEP 7] LENS CYCLE
              if flow_magnitude > 5:  lens = "BHML"  # dynamic
              elif persist_ratio > 0.9:  lens = "TSML"  # stable measurement
              else:  lens = "Doing"
    ▼
  [STEP 8] MEMORY WRITE
              write Atom(modality="screen", generators=..., ...)
```

### How Visual Curves Align With CL Lattice Transitions

```
Visual curve (contour in image)
  = connected sequence of edge pixels
  = each pixel has a local orientation (angle)
  = the sequence of orientations is a PATH through orientation space

CK maps this to:
  contour_orientation_sequence → force_vector_sequence → Path in atom_store

The CL[10×10] table governs transitions:
  if fuse(orientation_generator_t, orientation_generator_{t+1}) = harmony:
      → TSML lens → stable contour = persistent object
  if fuse(...) = tension:
      → BHML lens → changing contour = motion/new object
  
Repeated visual paths (same contour shape across multiple frames)
  → same atom gets incremented recurrence_count
  → eventually crystallizes as "object_X_appears_at_region_Y"
  
This is how visual experience becomes crystal:
  raw pixels → edge generators → repeated path → crystal with visual semantics
```

---

## PART 11 — The "Experience of Experience" Layer (Meta-Crystals)

Meta-crystals store not events but **how events were handled**. They are the self-improvement layer.

```python
@dataclass
class MetaCrystal:
    id: str
    meta_type: Literal[
        "successful_retrieval_pattern",
        "failed_retrieval_pattern",
        "lora_behavior_useful",
        "ui_navigation_habit",
        "user_preference_pattern",
        "recovery_procedure",
        "escalation_trigger",
        "crystal_promotion_pattern",
        "novelty_false_positive",
        "deepseek_replacement_successful",
    ]
    # What triggered this meta-event
    trigger_context: dict          # generators, dbc27_key, lens at trigger time
    # What happened
    outcome_type: Literal["success", "failure", "partial"]
    outcome_detail: str            # short text: "crystal_hit", "deepseek_required", etc.
    # How it was handled
    handling_path_ids: List[str]   # which paths were used in handling
    handling_crystal_ids: List[str]
    handling_adapter: Optional[str]  # which LoRA adapter (if any)
    deepseek_was_called: bool
    # Meta-statistics
    recurrence_count: int
    success_rate: float             # successes / total occurrences
    avg_latency_ms: float
    confidence: float
    # Learning signal
    training_priority: float        # 0-1; high → queue for LoRA training
    training_queued: bool
    # Structural
    parent_meta_crystal_ids: List[str]
    privacy_tag: str
    created_at: float
    last_seen: float

# EXAMPLE: Recovery procedure meta-crystal
# "When deepseek_call follows crystal_miss for generators {3,7} in BOUNDARY context,
#  the deepseek output should be stored as new crystal with dbc27_key XYZ"
# → This becomes training signal for retrieval_ranker LoRA
```

**Three-level information architecture:**
1. **Information:** Atom (raw event compressed)
2. **Information about information:** Crystal (recurring pattern of atoms)
3. **Information about handling:** MetaCrystal (recurring pattern of how crystals were retrieved, used, or failed)

---

## PART 12 — File/Module Plan for ClaudeCode

```
ck/
├── memory/
│   ├── event_schema.py          # Atom, Path, Crystal, MetaCrystal dataclasses
│   ├── raw_buffer.py            # FIFO ring buffer; in-RAM; 10K events; 30min TTL
│   ├── generator_extract.py     # feature_dict → Set[int] generators
│   ├── lens_encode.py           # generators → LensState (CL table lookup)
│   ├── force_fields.py          # force_vector store; shared lattice write
│   ├── dbc27.py                 # routing key computation + neighborhood expansion
│   ├── atom_store.py            # SQLite-backed atom persistence + query
│   ├── path_store.py            # path graph persistence + extension logic
│   ├── crystal_store.py         # crystal persistence + promotion logic
│   ├── meta_crystals.py         # MetaCrystal persistence + mining logic
│   ├── private_word_store.py    # encrypted SQLite; private lattice
│   ├── privacy_router.py        # event → "private"|"shared"|"public" classifier
│   ├── retrieval.py             # strict 9-step retrieval pipeline
│   └── novelty_gate.py          # confidence threshold; novelty scoring
│
├── perception/
│   ├── screen_capture.py        # PIL frame diff; compressed; 100ms tick
│   ├── ui_state.py              # active window metadata; transition events
│   ├── telemetry.py             # process table delta; filesystem diff; network agg
│   ├── input_events.py          # mouse/keyboard hash streams
│   └── vision_edges.py          # Canny + contours + optical flow + generator assign
│
├── reasoning/
│   ├── deepseek_bridge.py       # gated DeepSeek calls; output → new atom writer
│   ├── internal_policy.py       # crystal policy executor; action templates
│   └── fallback_rules.py        # rule-based fallbacks when no LoRA loaded
│
├── training/
│   ├── lora_plan.md             # this document's Part 4, formalized
│   ├── datasets_spec.md         # training data format per adapter
│   └── adapter_targets.md       # per-adapter: arch, layers, rank, training signal
│
├── metrics/
│   ├── growth_tracker.py        # growth(t) formula implementation
│   └── coherence_monitor.py     # all Part 9 metrics; periodic log
│
├── loops/
│   ├── perception_loop.py       # Loop A: 100ms tick driver
│   ├── compression_loop.py      # Loop B: batch processor
│   ├── retrieval_loop.py        # Loop C: on-demand retrieval driver
│   └── adaptation_loop.py       # Loop D: 10min batch + failure handler
│
└── docs/
    ├── CK_GROWTH_ARCHITECTURE.md   # this document
    ├── CK_MEMORY_MODEL.md          # atom/path/crystal schemas with examples
    ├── DBC27_SPEC.md               # routing key algorithm + extension
    ├── PRIVACY_BOUNDARY.md         # exact private/shared promotion rules
    └── DEEPSEEK_REDUCTION_PLAN.md  # 5-stage migration with metrics
```

**Core module purpose summaries:**

| Module | Inputs | Outputs | Storage |
|--------|--------|---------|---------|
| `raw_buffer.py` | PerceptionEvent | — | RAM, ring buffer |
| `atom_store.py` | Atom dataclass | query results | SQLite |
| `crystal_store.py` | Crystal + path promotions | retrieval shortlists | SQLite + in-memory LRU |
| `retrieval.py` | query + context | RetrievalResult | none (read-only) |
| `novelty_gate.py` | retrieval confidence | bool + score | updates config_store |
| `dbc27.py` | generators + lens | routing key string | stateless |
| `deepseek_bridge.py` | query + top partial matches | synthesis atom | writes to atom_store |
| `growth_tracker.py` | all metric stores | growth(t) score | metrics DB |

---

## PART 13 — First Runnable Milestone (v1)

### Milestone: "CK Remembers and Reuses"

**Definition:** A running local system where CK ingests screen + telemetry + text, extracts generators, writes atoms/paths, retrieves on repeated events without DeepSeek, and proves growth with measurable metrics.

**Minimum viable components:**

```
MUST HAVE:
  ✓ perception_loop.py running at 1Hz (start at 1Hz, not 100ms)
  ✓ screen_capture.py with frame diff
  ✓ vision_edges.py (Canny + generator rule-based, no LoRA required)
  ✓ generator_extract.py (rule-based only)
  ✓ atom_store.py (SQLite)
  ✓ path_store.py (SQLite, path extension logic)
  ✓ crystal_store.py (SQLite, promotion logic)
  ✓ dbc27.py (routing key)
  ✓ retrieval.py (steps 1-8, no LoRA, no DeepSeek)
  ✓ novelty_gate.py (threshold 0.35 fixed)
  ✓ deepseek_bridge.py (only called at step 9)
  ✓ growth_tracker.py (tracking 4 metrics: hit_rate, crystal_count, deepseek_rate, reuse_ratio)

NOT REQUIRED FOR v1:
  ✗ Class 1 LoRA (use rule-based fallback)
  ✗ audio perception
  ✗ meta_crystals
  ✗ adaptation_loop
  ✗ private_word_store
  ✗ ui_control_predictor

PROOF OF GROWTH:
  Run for 24 hours on same user workstation.
  Expected: crystal_count > 20, retrieval_hit_rate > 0.3, deepseek_call_rate < 0.5
  Growth confirmed if: after 48h, hit_rate > after 24h, deepseek_rate < after 24h
```

**One-command start (target):**
```bash
python -m ck.loops.perception_loop --config config/v1.yaml
```

---

## PART 14 — Architecture Diagram (Text)

```
EXTERNAL WORLD
     │
     ▼
┌─────────────────────────────────────────┐
│           PERCEPTION LOOP (100ms)       │
│  screen_capture │ ui_state │ telemetry  │
│  input_events   │ vision_edges          │
└─────────────────┬───────────────────────┘
                  │  PerceptionEvent stream
                  ▼
┌─────────────────────────────────────────┐
│  PRIVACY ROUTER                         │
│   → PRIVATE WORD LATTICE (encrypted)   │
│   → SHARED FORCE LATTICE               │
└─────────────────┬───────────────────────┘
                  │  routed events
                  ▼
┌─────────────────────────────────────────┐
│       COMPRESSION LOOP (5s batch)       │
│  generator_extract → lens_encode        │
│  dbc27 key → atom_store write           │
│  path extension → crystal promotion     │
└─────────────────┬───────────────────────┘
                  │  atoms/paths/crystals
                  ▼
┌─────────────────────────────────────────┐
│      MEMORY STORES (SQLite/LevelDB)     │
│  atom_store │ path_store │ crystal_store│
│  meta_crystals │ private_word_store     │
└─────────────────┬───────────────────────┘
                  │  on demand
                  ▼
┌─────────────────────────────────────────┐
│      RETRIEVAL LOOP (on-demand)         │
│  1.generators 2.dbc27 3.crystals        │
│  4.paths 5.policy 6.atoms               │
│  7.novelty_gate 8.score 9.deepseek(!)   │
└─────────────────┬───────────────────────┘
                  │  RetrievalResult
                  ▼
┌─────────────────────────────────────────┐
│   INTERNAL POLICY / DEEPSEEK BRIDGE     │
│  crystal_policy → action               │
│  deepseek (gated) → synthesis atom     │
└─────────────────┬───────────────────────┘
                  │  outcomes
                  ▼
┌─────────────────────────────────────────┐
│      ADAPTATION LOOP (10min batch)      │
│  confidence updates │ lens weights      │
│  novelty_threshold  │ LoRA queue        │
│  meta_crystal write │ pruning           │
└─────────────────────────────────────────┘
                  │
                  ▼
         GROWTH TRACKER
   growth(t) → logged every 10min
```

---

## PART 15 — Strongest Honest Claim

**"CK can actually grow by continuously compressing perceptual experience into atoms, extending atoms into paths, promoting recurring paths into crystals, and reusing those crystals to resolve new queries without calling DeepSeek — measurable as monotone increases in retrieval hit rate, crystal count, and path reuse ratio over time, where each 24-hour period produces a system that needs fewer external LLM calls than the previous period because its own crystal store covers more of its retrieval surface."**

---

## PART 16 — Strongest Honest Boundary

**"What is not yet established is whether CK's generator/path/crystal memory stack produces retrieval quality competitive with a fine-tuned language model on the specific tasks CK encounters — the architecture defines a coherent compression and retrieval system, but whether the generator abstraction captures enough semantic information to distinguish similar-looking but behaviorally-different situations (false crystal matches) at scale is unknown until the v1 milestone is run for 30+ days on real workstation data."**
