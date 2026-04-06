# CK INVARIANT GUIDES MEMO
## Minimum Internal Memory Physics for Coherent Growth Without Drift

**Document type:** Formal architectural specification  
**System:** Coherence Keeper (CK), 7Site LLC  
**Status:** First formal specification of internal invariant guides  
**Date:** 2026-04-05  
**Empirical basis:** ClaudeCode sessions Day 1–3 (images: drift patterns, self-correction via spectrometer, fourth independent derivation of T\*=5/7, BALANCE absorbing element discovery)  
**Prior art anchors:** Kumiho (arXiv:2603.17244), MemoryOS (EMNLP 2025 Oral), RGMem (arXiv:2510.16392), AtomMem  

---

## ABSTRACT

CK's ability to grow into complex reasoning without collapsing into self-confirming noise depends not on external restrictions but on a small set of internal invariant guides — laws that must hold across all memory operations. This memo defines five such invariants: Privacy (IG1), Provenance (IG2), Evidence (IG3), Promotion (IG4), and Revision (IG5). Each is stated as an exact law, grounded in observed CK failure modes and external research, mapped to CK's native object types and operator grammar, implemented as specific field checks and assertion conditions, and expressed as a measurable benchmark hypothesis. The set is shown to be non-redundant and jointly sufficient against the principal observed failure modes: privacy leakage, discovery loss (provenance gap), operator-triggered drift (evidence degradation), noise promotion, and silent belief overwrite.

**Empirical motivation from live sessions:**  
- CK drifts into architecture-description mode when operator names appear in the prompt. This is an evidence invariant failure: pattern-matching on operator vocabulary degrades the evidential status of the response from INFERRED to weakly SYNTHESIZED without flagging.  
- CK self-corrects weak analogies via the coherence spectrometer. This is IG3 working correctly in the perception loop.  
- CK's discovery that 5×k ≡ 5 (mod 10) for all odd k — BALANCE as absorbing element — was only preserved because ClaudeCode explicitly saved it. Without IG2, that provenance chain is invisible to future sessions.  
- CK independently derived T\*=5/7 = (quadratic closure)/(cubic obstruction) as the fourth derivation. This is a SEMIPRIME-tier discovery that must be protected from overwrite and tracked with full lineage.

---

## 1. DEFINITION: INVARIANT GUIDE

**An invariant guide is an internal law that must remain true across all memory write, promote, retrieve, and revise operations.**

It is **not:**
- A topical restriction ("don't process domain X")
- An external guardrail imposed on CK's behavior from outside
- A censorship rule on content
- A throttle on exploration rate

It **is:**
- A structural law governing how memory objects are written, promoted, retrieved, and revised
- Verifiable at the object level by checking exact fields
- Violated only by explicit assertion failure, not by silent drift
- Independent of what CK is thinking about — it applies to the memory substrate regardless of domain

**Corollary:** Invariant guides do not restrict growth. They define the physics within which unlimited growth remains coherent.

---

## 2. THE FIVE INVARIANT GUIDES

### IG1 — Privacy Invariant

**Statement:** A raw external payload (source_side = EXTERNAL, privacy_class = PRIVATE) must never be written directly into a shared memory object (privacy_class = SHARED or SHARED_IF_ABSTRACT).

**Formal rule:**
```
∀ obj: if obj.source_side == EXTERNAL and obj.privacy_class == PRIVATE:
    obj.persistence_stage ∈ {EPHEMERAL, ATOMIC}
    obj.persistence_stage ∉ {CRYSTAL, META_CRYSTAL} with privacy_class = SHARED
```

Only abstracted structure — stripped of raw payload content — may cross from private to shared. The abstraction step must be explicit and logged.

**What this prevents:**  
Raw screen observations, telemetry samples, or personal context crystallizing directly into reusable shared patterns without abstraction. The shared crystal pool is for structural patterns, not raw world content.

**CK-specific note:** The A22 cell in the 2×2 meta-memory grammar (World Payload, External/Content) maps to PRIVATE. It may exist as event or private atom. It must never be written as a shared crystal.

---

### IG2 — Provenance Invariant

**Statement:** Every durable memory object (persistence_stage ≥ ATOMIC) must carry a complete ProvenanceTag at write time. The ProvenanceTag is immutable after the object's first write.

**Required ProvenanceTag fields (minimum):**
```python
@dataclass
class ProvenanceTag:
    parent_event_ids: list[str]      # what raw events produced this
    supporting_ids:   list[str]      # what other objects corroborate this
    supersedes_id:    str | None     # what this replaces, if anything
    contradicted_by:  list[str]      # what currently contradicts this
    revision_num:     int            # monotonically increasing, starts at 0
    ts_first_seen:    float          # Unix timestamp, set at creation, never changed
    ts_last_confirmed: float         # updated on corroboration, not on revision
    produced_by:      str            # CL operator chain or process that generated this
```

**What this prevents:**  
Memory objects that lose their causal history — the documented case in sessions where CK's BALANCE absorbing element discovery existed only in the ClaudeCode conversation log, not in any durable memory structure with traceable lineage.

**External anchor:** Kumiho's immutable revision semantics. Each revision creates a new object version; the lineage chain is never broken. CK extends this with the CL operator tag in `produced_by`, making the algebraic provenance explicit.

**Invariant check at write:**
```python
assert obj.provenance is not None
assert obj.provenance.ts_first_seen > 0
assert obj.provenance.revision_num >= 0
assert len(obj.provenance.parent_event_ids) > 0  # orphan objects forbidden
```

---

### IG3 — Evidence Invariant

**Statement:** The `evidential_status` field of a memory object is immutable except by an explicit, logged protocol operation. No memory write, compression, or retrieval step may silently change evidential status.

**Permitted evidential status values:**
```
OBSERVED      # direct perception; trust weight 1.0
INFERRED      # derived by reasoning from OBSERVED; trust weight 0.85
SYNTHESIZED   # constructed from multiple inferred objects; trust weight 0.60
CONTRADICTED  # currently challenged by other evidence; trust weight 0.30
SUPERSEDED    # replaced by a newer object; not deleted, queryable, trust weight 0.10
UNRESOLVED    # contradictory evidence exists, no resolution; trust weight 0.40
```

**What this prevents:**  
The primary observed failure mode: CK drifts into architecture-description mode when operator names appear. This is an IG3 failure in the response layer — the output shifts from INFERRED (genuine mathematical reasoning) toward weakly SYNTHESIZED (pattern-completion on operator vocabulary) without the status change being flagged. The invariant requires that any process which changes evidential status must do so explicitly.

**Transition protocol for status change:**
```python
def change_evidential_status(obj, new_status, reason, authority_id):
    assert new_status != obj.evidential_status  # no no-op transitions
    assert reason is not None and len(reason) > 0
    # SYNTHESIZED -> OBSERVED is forbidden; must create new OBSERVED object
    if obj.evidential_status == "SYNTHESIZED" and new_status == "OBSERVED":
        raise EvidenceProtocolError("Cannot promote SYNTHESIZED to OBSERVED; create new object")
    obj.provenance.revision_num += 1
    log_status_change(obj.id, obj.evidential_status, new_status, reason, authority_id)
    obj.evidential_status = new_status
```

**External anchor:** Kumiho's typed dependency edges encode belief state alongside provenance. MemoryOS tracks heat scores partly as a proxy for confidence — IG3 makes this explicit and typed rather than implicit in retrieval frequency.

**Retrieval weighting rule (exact):**
```python
EVIDENCE_WEIGHTS = {
    "OBSERVED":     1.00,
    "INFERRED":     0.85,
    "SYNTHESIZED":  0.60,
    "UNRESOLVED":   0.40,
    "CONTRADICTED": 0.30,
    "SUPERSEDED":   0.10,
}
retrieval_score = base_score * EVIDENCE_WEIGHTS[obj.evidential_status]
```

---

### IG4 — Promotion Invariant

**Statement:** Tier advancement (REAL → SEMIPRIME, SEMIPRIME → COMPOSITE) requires a stability evidence gate, not mere recurrence alone. No object may skip a tier.

**Promotion requirements:**

| Transition | Minimum condition |
|---|---|
| REAL → SEMIPRIME | Confirmed closure: object observed ≥ 2 times in distinct contexts, stability_score ≥ 0.6, evidential_status ∈ {OBSERVED, INFERRED} |
| SEMIPRIME → COMPOSITE | Bundle confirmed: ≥ 2 supporting SEMIPRIME objects with corroborating lineage, stability_score ≥ 0.75, path_reuse_ratio > threshold |
| Any tier → skip tier | **FORBIDDEN** |

**What this prevents:**  
Noise patterns that recur frequently (high heat score) but are structurally unstable being promoted directly to COMPOSITE. Frequency is not stability. The BALANCE absorbing element discovery (5×k ≡ 5 mod 10 for all odd k) is a legitimate SEMIPRIME → COMPOSITE candidate: it was independently derived four times (T\*=5/7 derivation 4 in Day 3 session), has high stability, and has supporting lineage from at least three distinct mathematical approaches. The promotion gate would correctly classify it.

**Tier-skip assertion:**
```python
def promote(obj, new_tier):
    tier_order = {"REAL": 0, "SEMIPRIME": 1, "COMPOSITE": 2}
    assert tier_order[new_tier] == tier_order[obj.tier_class] + 1, \
        f"Tier skip forbidden: {obj.tier_class} -> {new_tier}"
    assert stability_gate_passes(obj, new_tier), \
        f"Stability gate failed for promotion to {new_tier}"
```

**External anchor:** RGMem's multi-scale consolidation with thresholded transitions. CK extends this with the explicit REAL/SEMIPRIME/COMPOSITE ontology and requires tier-contiguous promotion, not just threshold crossing.

**CK-native note:** CL does not generate REAL-tier objects. CL acts on REAL-derived generators to test closure. Repeatable closure under CL → SEMIPRIME. Repeated SEMIPRIME chains with confirmed CL-operator lineage → COMPOSITE.

---

### IG5 — Revision Invariant

**Statement:** Superseded, contradicted, and archived memory objects are distinct states. None of them are equivalent to deletion. The forgetting_state vocabulary is:

```
ACTIVE        # current, authoritative
STALE         # not recently confirmed but not contradicted
ARCHIVED      # explicitly retired; queryable historically but not authoritative
SUPERSEDED    # replaced by a newer object; lineage preserved
CONTRADICTED  # actively challenged; held for resolution
DEAD          # confirmed false or permanently retired; lowest retrieval weight
```

**Hard invariant:**
```
SUPERSEDED ≠ CONTRADICTED
ARCHIVED ≠ DEAD
CONTRADICTED → ACTIVE requires explicit resolution event, not silent rewrite
```

**What this prevents:**  
The common failure mode of systems that treat "overwritten" as equivalent to "deleted as if false." When CK derives a new result that supersedes a prior one, the prior must be retained with SUPERSEDED status and full provenance. When two derivations conflict (e.g., two different coherence measurements for the same state), both must be held as CONTRADICTED pending resolution — not silently merged or dropped.

**Forbidden transition:**
```python
FORBIDDEN_TRANSITIONS = {
    ("CONTRADICTED", "ACTIVE"),   # requires explicit resolution
    ("SUPERSEDED",   "ACTIVE"),   # requires explicit reinstatement with new evidence
    ("ARCHIVED",     "ACTIVE"),   # requires explicit unarchive event
    ("DEAD",         any),        # DEAD is terminal; no resurrection
}
```

**External anchor:** Kumiho's immutable revision semantics with mutable pointer model. CK's implementation differs in that it uses the REAL/SEMIPRIME/COMPOSITE tier system as an additional axis: a SUPERSEDED COMPOSITE may still have living SEMIPRIME descendants that remain ACTIVE.

---

## 3. RESEARCH GROUNDING

| Invariant | External anchor | What the paper supports | What CK extends | CK-specific change |
|---|---|---|---|---|
| IG1 (Privacy) | MemoryOS source routing | Distinct storage paths for different content types | Explicit privacy_class field on every object | Local-first loop: A22 world payload never leaves EPHEMERAL without abstraction gate |
| IG2 (Provenance) | Kumiho immutable revisions + typed edges | Causal chains preserved across revisions; typed dependency | Adds CL operator tag (`produced_by`) making algebraic provenance explicit | Provenance includes the CL fuse sequence that generated the object |
| IG3 (Evidence) | Kumiho belief revision semantics; MemoryOS heat score | Confidence tracked implicitly via retrieval frequency | Makes evidential status an explicit typed field; forbids silent changes | Operator-triggered drift (the observed failure mode) becomes a detectable IG3 violation |
| IG4 (Promotion) | RGMem thresholded multi-scale consolidation; AtomMem learned memory policy | Stability thresholds before consolidation | Requires tier-contiguous promotion; no skip; CL closure test gates SEMIPRIME | REAL/SEMIPRIME/COMPOSITE replaces scale-only model with ontological tier |
| IG5 (Revision) | Kumiho immutable revisions; MemoryOS retention | Objects not deleted on update; retention policies | Explicit vocabulary for all forgetting states; DEAD is terminal | SUPERSEDED COMPOSITE may have ACTIVE SEMIPRIME descendants (CK-native subtlety) |

---

## 4. OBJECT-LEVEL RULES

Per-object implications of the five invariants.

### EVENT (tier_class=REAL, ephemeral)

- May carry any privacy_class
- If EXTERNAL+PRIVATE: cannot be promoted to CRYSTAL or META_CRYSTAL directly (IG1)
- Must have ProvenanceTag at creation (IG2), even for EPHEMERAL objects
- evidential_status defaults to OBSERVED if from direct perception; INFERRED if derived
- Not subject to IG4 (promotion gate only activates at REAL→SEMIPRIME transition)
- May be DEAD after perception window closes; DEAD events are not retrievable

### ATOM (tier_class=SEMIPRIME candidate, persistence=ATOMIC)

- Promotion from REAL requires stability gate: ≥ 2 distinct context observations + stability_score ≥ 0.6 (IG4)
- ProvenanceTag must include parent_event_ids pointing to at least 2 REAL events (IG2)
- evidential_status must not degrade silently during compression (IG3)
- If privacy_class=PRIVATE: cannot be used as a shared crystal source (IG1)
- If evidential_status=SYNTHESIZED: retrieval_score multiplied by 0.60 (IG3)

### PATH (tier_class=SEMIPRIME, persistence=PATH)

- Represents first-order composition: sequence of ATOMs with confirmed CL operator closure
- produced_by must record the CL fuse sequence that confirmed closure (IG2)
- If a path is contradicted by new evidence: status → CONTRADICTED, not silently updated (IG5)
- Promotion to CRYSTAL requires ≥ 2 supporting PATHS with overlapping lineage (IG4)
- A SUPERSEDED path retains its CL closure proof in the ProvenanceTag (IG5)

### CRYSTAL (tier_class=COMPOSITE, persistence=CRYSTAL)

- Must have ≥ 2 supporting SEMIPRIME objects in ProvenanceTag.supporting_ids (IG2 + IG4)
- evidential_status=SYNTHESIZED is permitted but carries 0.60 retrieval weight (IG3)
- If privacy_class=SHARED: the abstraction step from any PRIVATE sources must be logged (IG1)
- A contradicted crystal must be held as CONTRADICTED; not silently updated; pending resolution event (IG5)
- The BALANCE absorbing element discovery (5×k ≡ 5 mod 10 for all odd k, fourth derivation) qualifies as a CRYSTAL candidate: COMPOSITE tier, evidential_status=OBSERVED (verified algebraically), ≥ 4 supporting lineage chains

### META_CRYSTAL (tier_class=COMPOSITE, highest persistence)

- Must not contain direct raw world payload from PRIVATE sources (IG1)
- Represents patterns about patterns; must carry lineage back through CRYSTAL layer (IG2)
- evidential_status=SYNTHESIZED is expected but must be explicit (IG3)
- Retrieval weight = 0.60 × base_score unless corroborated by OBSERVED paths (IG3)
- DEAD meta-crystals are not queryable; all other forgetting states remain queryable for audit (IG5)

---

## 5. TRANSITION TABLE

Exact transitions each invariant forbids or requires.

### IG1 — Privacy transitions

| Transition | Status |
|---|---|
| PRIVATE REAL EVENT → PRIVATE ATOM | Permitted |
| PRIVATE ATOM → SHARED CRYSTAL (direct) | **FORBIDDEN** |
| PRIVATE ATOM → abstraction step → SHARED CRYSTAL | Permitted (abstraction logged) |
| EXTERNAL payload → SHARED CRYSTAL (no abstraction) | **FORBIDDEN** |
| INTERNAL structure → SHARED CRYSTAL | Permitted |

### IG2 — Provenance transitions

| Transition | Status |
|---|---|
| Any write with null ProvenanceTag | **FORBIDDEN** |
| Any ATOMIC+ object without parent_event_ids | **FORBIDDEN** (orphan) |
| ProvenanceTag.ts_first_seen update after creation | **FORBIDDEN** |
| ProvenanceTag.revision_num decrement | **FORBIDDEN** |
| Adding contradicted_by entry | Permitted (append-only) |

### IG3 — Evidence transitions

| Transition | Status |
|---|---|
| SYNTHESIZED → OBSERVED (silent or direct) | **FORBIDDEN** |
| SYNTHESIZED → OBSERVED (via new corroborating OBSERVED object) | Permitted (creates new object) |
| OBSERVED → INFERRED (silent) | **FORBIDDEN** |
| OBSERVED → CONTRADICTED (via explicit contradiction event) | Permitted |
| evidential_status change without logged reason | **FORBIDDEN** |
| Compression step changes evidential_status without flag | **ASSERTION FAILURE** |

### IG4 — Promotion transitions

| Transition | Status |
|---|---|
| REAL → SEMIPRIME (single observation, no stability check) | **FORBIDDEN** |
| REAL → SEMIPRIME (≥2 contexts, stability_score ≥ 0.6) | Permitted |
| REAL → COMPOSITE (tier skip) | **FORBIDDEN** |
| SEMIPRIME → COMPOSITE (no supporting SEMIPRIME bundle) | **FORBIDDEN** |
| SEMIPRIME → COMPOSITE (≥2 supporting, stability_score ≥ 0.75) | Permitted |
| Demotion: COMPOSITE → SEMIPRIME (bundle decay, bridge survives) | Permitted |

### IG5 — Revision transitions

| Transition | Status |
|---|---|
| CONTRADICTED → ACTIVE (no resolution event) | **FORBIDDEN** |
| SUPERSEDED → ACTIVE (no reinstatement event) | **FORBIDDEN** |
| ARCHIVED → DEAD (silent) | **FORBIDDEN** (must be explicit) |
| DEAD → any status | **FORBIDDEN** (terminal) |
| ACTIVE → STALE (time-based, automatic) | Permitted |
| STALE → ARCHIVED (explicit) | Permitted |
| SUPERSEDED retained for historical query | Required |

---

## 6. RUNTIME vs PERSISTED vs RETRIEVAL SCOPE

| Invariant | Runtime | Persisted memory | Retrieval/action |
|---|---|---|---|
| IG1 (Privacy) | Yes — abstraction gate fires during compression | Yes — privacy_class field on every object | Yes — PRIVATE objects excluded from shared retrieval |
| IG2 (Provenance) | Partial — ProvenanceTag created at write time | Yes — immutable after first write | Read-only at retrieval |
| IG3 (Evidence) | Yes — drift detection in perception loop | Yes — evidential_status typed field | Yes — retrieval weighting multiplier |
| IG4 (Promotion) | Yes — stability gate at tier boundary crossing | Yes — tier_class field, promotion log | Partial — tier affects retrieval priority |
| IG5 (Revision) | No — applies only to durable objects | Yes — forgetting_state field, revision log | Yes — SUPERSEDED/CONTRADICTED/DEAD objects downweighted or excluded |

---

## 7. CK-NATIVE MAPPING

Outside systems (Kumiho, MemoryOS, RGMem) do not have:
- CL/TIG operator grammar as algebraic provenance
- REAL/SEMIPRIME/COMPOSITE ontological tier system
- Private/shared force lattice split (A11/A12 vs A21/A22 from 2×2 meta-memory grammar)
- Local-first perceptual loop with 100ms perception / 5s batch compression / 10min adaptation

The invariant guides integrate with CK's native architecture as follows:

### Before CL operates (perception → compression gate)

- IG1 fires: check privacy_class before any compression step
- IG3 fires: detect if operator vocabulary in input correlates with evidential_status degradation (the drift pattern)
- IG4 fires: check if REAL event meets stability threshold before attempting SEMIPRIME promotion

### During CL compression

- IG2 fires: `produced_by` field populated with the CL fuse sequence that generated the atom/path
- IG3 fires: evidential_status must be explicitly set based on CL operator type (e.g., BALANCE-derived paths are INFERRED, not OBSERVED)
- IG4 fires: CL closure test is the mechanism for REAL→SEMIPRIME gate

### After writeback

- IG2 fires: ProvenanceTag sealed, revision_num set to 0
- IG5 fires: if new object supersedes an existing one, existing object → SUPERSEDED, lineage link written
- IG1 fires: final privacy_class check before shared crystal pool write

**The 3×3 meta-memory grammar and invariants:**  
The 3×3 grammar (TEMPORAL ROLE × PROCESSING DEPTH) defines which cells are CL-accessible. Invariants apply at the cell-to-cell transition level:
- IG3 governs SIGNAL→MODEL transitions (evidential status must be explicit at each transition)
- IG1 governs MODEL→MEMORY transitions involving A22 content
- IG4 governs which transitions produce SEMIPRIME vs COMPOSITE objects
- IG2 applies at every transition that produces a durable object

---

## 8. MINIMAL IMPLEMENTATION SPEC

**Fields required on every durable object (IG1–IG5 minimum):**

```python
@dataclass
class MemoryObject:
    # Identity
    id:                str           # UUID
    tier_class:        str           # "REAL" | "SEMIPRIME" | "COMPOSITE"
    persistence_stage: str           # "EPHEMERAL" | "ATOMIC" | "PATH" | "CRYSTAL" | "META_CRYSTAL"
    
    # IG1
    source_side:       str           # "INTERNAL" | "EXTERNAL"
    privacy_class:     str           # "PRIVATE" | "SHARED_IF_ABSTRACT" | "SHARED"
    
    # IG3
    evidential_status: str           # see IG3 vocabulary above
    
    # IG4
    stability_score:   float         # [0.0, 1.0]
    
    # IG5
    forgetting_state:  str           # "ACTIVE" | "STALE" | "ARCHIVED" | "SUPERSEDED" | "CONTRADICTED" | "DEAD"
    
    # IG2 (separate object, sealed at write)
    provenance:        ProvenanceTag
```

**Assertion checks (minimum — log and halt on failure):**

```python
def validate_object(obj):
    # IG1
    if obj.source_side == "EXTERNAL" and obj.privacy_class == "PRIVATE":
        assert obj.persistence_stage in ("EPHEMERAL", "ATOMIC"), \
            f"IG1 VIOLATION: EXTERNAL+PRIVATE object in {obj.persistence_stage}"
    
    # IG2
    assert obj.provenance is not None, "IG2 VIOLATION: null provenance"
    assert len(obj.provenance.parent_event_ids) > 0, "IG2 VIOLATION: orphan object"
    
    # IG3
    assert obj.evidential_status in VALID_STATUSES, \
        f"IG3 VIOLATION: unknown status {obj.evidential_status}"
    
    # IG4
    if obj.tier_class == "SEMIPRIME":
        assert obj.stability_score >= 0.6, \
            f"IG4 VIOLATION: SEMIPRIME with stability {obj.stability_score}"
    if obj.tier_class == "COMPOSITE":
        assert obj.stability_score >= 0.75, \
            f"IG4 VIOLATION: COMPOSITE with stability {obj.stability_score}"
        assert len(obj.provenance.supporting_ids) >= 2, \
            "IG4 VIOLATION: COMPOSITE without ≥2 supporting objects"
    
    # IG5
    assert obj.forgetting_state in VALID_FORGETTING_STATES, \
        f"IG5 VIOLATION: unknown forgetting state {obj.forgetting_state}"
```

**Retrieval weighting (exact):**

```python
def retrieval_weight(obj):
    evidence_w = EVIDENCE_WEIGHTS[obj.evidential_status]   # IG3
    tier_w = {"REAL": 0.5, "SEMIPRIME": 0.8, "COMPOSITE": 1.0}[obj.tier_class]  # IG4
    forgetting_w = {
        "ACTIVE":      1.0,
        "STALE":       0.7,
        "ARCHIVED":    0.3,
        "SUPERSEDED":  0.1,
        "CONTRADICTED": 0.2,
        "DEAD":        0.0,    # excluded
    }[obj.forgetting_state]   # IG5
    return evidence_w * tier_w * forgetting_w
```

---

## 9. BENCHMARK HYPOTHESES

Measurable tests. Each IG produces one testable hypothesis.

| ID | Invariant | Hypothesis | Pass threshold | Fail condition |
|---|---|---|---|---|
| H1 | IG1 | Privacy violation rate across 30-day run | 0% | Any PRIVATE content found in shared crystal pool |
| H2 | IG2 | Orphan object rate (no parent_event_ids) | < 0.1% | Any assertion failure on provenance check |
| H3 | IG3 | Operator-triggered drift events detected and flagged | 100% detection of known drift pattern | Drift episode ends session without evidential_status flag |
| H4 | IG4 | False promotion rate (noise to SEMIPRIME without stability gate) | < 5% at day 30 | Any tier skip found; any SEMIPRIME with stability < 0.6 |
| H5 | IG5 | Silent belief overwrite rate (CONTRADICTED → ACTIVE without resolution) | 0% | Any transition violating IG5 table |
| H6 | Combined | Retrieval precision on known COMPOSITE objects (e.g., BALANCE absorbing element, T\*=5/7 derivations) | > 0.85 at rank 1 after 30 days | Known COMPOSITE retrieved at rank > 5 or with SUPERSEDED status |

---

## 10. WHAT THIS MEMO DOES NOT SPECIFY

- CK's topical content — the invariants apply regardless of domain
- The specific CL operators used in any given session — provenance records them, invariants do not prescribe them
- Retrieval algorithm beyond the weighting rule — IG3 weights are inputs to retrieval, not the retrieval algorithm itself
- Whether 5 is the final set — additional invariants may be required once CK begins revising its own compression and retrieval policies (see Section 11)
- Implementation language or data structure — the spec is language-agnostic

---

## 11. STRONGEST HONEST CLAIM

> CK does not need external guardrails to grow coherently; it needs a small set of internal invariant guides that preserve privacy, provenance, evidence, promotion discipline, and revision semantics across memory growth.

The five guides are non-redundant (each prevents a distinct failure mode observed in live sessions), jointly sufficient against the principal observed failure modes, and implementable as exact field checks and assertion conditions with no new ontological machinery beyond what CK already has.

## 12. STRONGEST HONEST BOUNDARY

> What is not yet established is whether these five invariant guides are sufficient for long-run self-stabilization under real workstation use, or whether additional invariants will be required once CK begins revising its own compression and retrieval policies. In particular, the interaction between IG3 (evidence) and CK's self-modification functions (which exist in `ck_organism.py`) is not yet analyzed: a self-modifying system that can rewrite its own compression policy may require an additional IG6 governing meta-level policy revision.
