# ARTIFACTS — funding/self-healing

---

## Primary source — external repo

### 1. Dual-Lattice-Self-Healing repo
- **Source**: `github.com/TiredofSleep/Dual-Lattice-Self-Healing`
- **Local clone**: `_brayden_repos/Dual-Lattice-Self-Healing/` (on R16 desktop, not yet committed into ck)
- **Status**: cloned during Part 1 external-repo survey
- **Content**: architectural sketches for the dual-lattice coherence-matching + repair-action approach
- **Integration task**: verbatim copy into `docs/archive_dual_lattice/` with provenance header documenting original repo commit hash and date

---

## Supporting runtime substrate (already in ck repo)

### 2. TIG Unity Kernel simulator
- **Path**: (TIG Unity simulator is same substrate as Branch A; likely `archive_imports/` after Phase 1 recovery of Branch A's `benchmark.py`)
- **Role**: coherence-gap measurement infrastructure — same R-σ-Λ-H grammar as Branch B (snowflake) but re-targeted for closed-loop operation

### 3. Coherence gate reference
- **Path**: `Gen12/targets/ck_desktop/ck_sim/being/ck_coherence_gate.py`
- **Role**: the T* = 5/7 gating pattern used for CK crystallization is a candidate pattern for self-healing gap-tolerance threshold (but probably needs to be re-thresholded per domain)

### 4. Canonical operator tables
- **Path**: `papers/ck_tables.py`
- **Role**: the 73-cell TSML and 28-cell BHML are candidate substrates for the finite repair-action vocabulary
- **Caveat**: mapping TSML/BHML cells to repair actions is an architectural decision, not automatic. The "operator" in CK's language does not directly equal "repair action" in a self-healing system

---

## Artifacts to be written (Phase 1 deliverables)

### A1 — Architectural writeup
- **Form**: 15–20 page document
- **Destination**: `docs/archive_dual_lattice/SELF_HEALING_ARCHITECTURE.md`
- **Content**:
  - Dual-lattice definition (current + reference)
  - Coherence-gap measurement via R-σ-Λ-H
  - Repair-action vocabulary: source, size, compositional properties
  - Closed-loop control theory framing (sensor → estimator → controller → actuator)
  - Safety envelope: what prevents oscillation, what prevents cascading failure
  - Relationship to FDI (fault detection and identification), FDIR (with isolation + recovery), MBFM (model-based fault management)

### A2 — Literature-positioning section
- **Form**: 5–8 page standalone document or section within A1
- **Content**: structured comparison to:
  - NASA Mission Data System (MDS) — spacecraft fault management
  - Fault-tolerant distributed-systems classics (Lamport, Byzantine fault tolerance, Raft, Paxos)
  - Soft-robotics morphological repair
  - Cyber-physical-systems resilient control
- **Purpose**: establish where dual-lattice is novel vs. incremental

### A3 — Target-domain specification
- **Form**: 3–5 page document
- **Content**: specific Phase 2 benchmark target. Candidate targets:
  - Distributed compute fabric with asymmetric node failure (fits AFRL / NSF CISE RI)
  - Spacecraft attitude-control degradation (fits NASA JPL NIAC)
  - Industrial process control with sensor drift (fits ONR / DARPA)
- **Output**: one chosen target + pass/fail criteria for the benchmark

### A4 — Safety envelope specification
- **Form**: 3–5 page document
- **Content**: what operational envelopes the self-healing loop is restricted to; what kick-out conditions escalate to human; what oscillation-prevention measures exist; what worst-case behavior is bounded
- **Purpose**: every autonomous-systems funder requires this before funding actuation-capable autonomy

---

## Integration tasks

- [ ] Verify Dual-Lattice-Self-Healing repo is cloned; re-clone if missing
- [ ] Copy verbatim into `docs/archive_dual_lattice/` with provenance header (original commit hash, date, repo URL)
- [ ] Mark any superseded content `[HISTORICAL]` in place
- [ ] Write A1 architectural document
- [ ] Write A2 literature-positioning section
- [ ] Write A3 target-domain specification
- [ ] Write A4 safety envelope specification

---

## Line-count summary (targets)

| Artifact | Size | Status |
|---|---|---|
| External repo integration | varies (depends on repo) | NOT YET COPIED INTO CK |
| A1 Architectural writeup | 15–20 pp | NOT WRITTEN |
| A2 Literature positioning | 5–8 pp | NOT WRITTEN |
| A3 Target domain spec | 3–5 pp | NOT WRITTEN |
| A4 Safety envelope spec | 3–5 pp | NOT WRITTEN |
| **Combined Phase 1 writeup** | **~25–40 pp** | NOT WRITTEN |

## Sanity check before pitch

A funder looking at this branch must see:
1. A cleanly-written architectural description (A1)
2. A specific target domain with pass/fail criteria (A3)
3. A safety envelope they can sign off on (A4)
4. A literature comparison that demonstrates the PI knows the field (A2)

Without all four, the pitch reads as "we have an idea and some code" — which is true but not fundable.
