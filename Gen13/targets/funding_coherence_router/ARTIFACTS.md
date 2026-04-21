# ARTIFACTS — funding/coherence-router

Exact file paths, LOC, and verification status. This branch depends on the `All-or-Nothing-E` external repo; Phase 1 includes pulling verbatim copies into this repo under `docs/archive_coherence_router/` with provenance headers.

---

## Runnable artifacts (in external All-or-Nothing-E repo, clone pending)

### 1. Benchmark suite — `benchmark.py`
- **External path**: `github.com/TiredofSleep/All-or-Nothing-E/benchmark.py`
- **Target path after Phase 1 pull**: `Gen12/targets/ck_desktop/docs/archive_coherence_router/benchmark.py` (or wherever the import repo lands)
- **LOC**: 554
- **Status**: runnable (per primary research 2026-04-19)
- **Tests** (7 total):
  1. Convergence test — does the system converge to an expected attractor under known input
  2. Throughput test — rate at which classifications can be produced
  3. Self-repair test — does the system recover from induced perturbation
  4. Information-dynamics test — information-theoretic measures of state transitions
  5. Scaling test — behavior as system size grows
  6. Composition test — behavior when two coherent-computer instances compose
  7. Attractor-basin test — characterization of the attractor basin structure
- **Invocation (once imported)**: `python benchmark.py`
- **Expected runtime**: pending verification (recommend 10–30 min for full suite on a single core)

### 2. Core classifier — `tig_coherent_computer.py`
- **External path**: `github.com/TiredofSleep/All-or-Nothing-E/tig_coherent_computer.py`
- **Target path after Phase 1 pull**: same `archive_coherence_router/` location
- **LOC**: 588
- **Status**: runnable
- **Responsibilities** (to be verified by reading the code):
  - Compose state vectors under the R-σ-Λ-H grammar
  - Compute coherence scores (harmonic-mean form per PROVEN_CONFIGURATION.md)
  - Assign operator labels from the 10-operator alphabet
  - Expose a classifier-shape interface

### 3. Empirical discovery — `PROVEN_CONFIGURATION.md`
- **External path**: `github.com/TiredofSleep/All-or-Nothing-E/PROVEN_CONFIGURATION.md`
- **LOC**: 89
- **Status**: empirical report
- **Content**: 2,100-permutation empirical search that identifies harmonic-mean composition as the correct form for the coherence grammar; documents the formula correction from an earlier arithmetic-mean variant
- **Value to Phase 1**: establishes the classifier's composition rule (harmonic mean of subsystem coherence scores), which is the key implementation detail that distinguishes a correct classifier from a broken one

---

## Related internal material

### 4. TIG Unity Kernel theory
- **Path**: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` and related tig-synthesis material
- **Relevance**: the R-σ-Λ-H state grammar is defined here; the coherence-router uses this grammar as its classifier's feature space

### 5. Operator alphabet and tables
- **Path**: `papers/ck_tables.py`
- **Content**: TSML (73 cells, HARMONY) + BHML (28 cells, HARMONY) canonical tables; CL (Crossing Lemma) data; 10-operator alphabet (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET)
- **Relevance**: operator-label assignments come from these tables

### 6. Cross-branch source — TIG Unity benchmark
- **Path**: `_brayden_repos/TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT/docs/COMPUTE.md` (per research survey)
- **Content**: TIG Unity Kernel v9.x spec with R-σ-Λ-H + benchmark table (88% drop-rate reduction claim — requires reconciliation with the 32pp whitepaper number per HANDOFF_INDEX.md §3)
- **Relevance**: provides the theoretical grounding and cross-branch consistency with Branch A (tig-unity)

---

## Phase 1 productionization task list

Phase 1 funding ($75K–$200K / 6 months) delivers these:

### T1. Pull All-or-Nothing-E into this repo
- Clone `All-or-Nothing-E` to `_brayden_repos/`
- Copy `benchmark.py`, `tig_coherent_computer.py`, `PROVEN_CONFIGURATION.md` into `Gen12/targets/.../docs/archive_coherence_router/` with provenance headers
- Commit under the never-delete policy

### T2. Standard classifier API wrapper
- Design: a Python classifier following scikit-learn's `BaseEstimator` + `ClassifierMixin` conventions — `.fit(X, y)` (no-op or minimal), `.predict(X)`, `.score_samples(X)` for coherence scores, `.decision_function(X)` for the continuous output
- Alternative design: a Kubernetes operator / sidecar interface exposing HTTP endpoints `/classify` (state in, operator out) and `/coherence` (state in, score out)
- Deliverable: wrapper in `coherence_router/` with type hints, docstrings, and MIT/Apache-licensed release candidate

### T3. Synthetic-telemetry benchmark
- Construct synthetic traces resembling SRE golden-signals (latency, traffic, errors, saturation) over time
- Run `benchmark.py` 7 tests + classifier wrapper on synthetic traces
- Deliverable: reproduction-ready benchmark suite + HTML report

### T4. Containerization + documentation
- Dockerfile for the classifier
- Kubernetes deployment manifest (pod / sidecar pattern)
- SRE-oriented tutorial: "Using coherence-router as an additional health signal"
- Deliverable: public GitHub repo with container image on a public registry (Docker Hub or GHCR)

### T5. SRE-community blog post / tutorial
- Target venue: SREcon lightning talk, CNCF blog post, or Medium/personal blog with wide distribution
- Content: what the classifier does, how to install it, how it compares to golden-signals on synthetic data, known limitations
- Deliverable: published tutorial

---

## Phase 2 comparison-study task list

Phase 2 funding ($200K–$500K / 12–18 months) delivers these:

### T6. Realistic-telemetry access
- Via AWS / GCP / Azure research credits program, obtain access to anonymized telemetry from a representative cloud-scale deployment — or
- Via industry lab partnership (LinkedIn SRE, Uber reliability, etc.), obtain anonymized traces

### T7. Baseline classifiers
- Reference golden-signals dashboard classifier (simple threshold rules)
- One ML anomaly-detection baseline (e.g., Prophet, Anomalib, or a GluonTS forecaster with residual-based anomaly detection)

### T8. Comparison study
- Run coherence-router + golden-signals + ML anomaly-detection baseline on the same telemetry
- Compare on: precision/recall at identifying known-bad episodes, lead time before SLO breach, false-positive rate, compute cost
- Deliverable: reproducible comparison with per-classifier tables and per-episode analysis

### T9. Publication
- Target venues: USENIX SREcon, SIGMETRICS, OSDI, or PODC (depending on framing)
- Deliverable: submitted paper + public dataset (where permitted) + public code

---

## Verification checklist (before any pitch)

- [ ] Clone `All-or-Nothing-E` to `_brayden_repos/` and confirm benchmark.py runs on a fresh environment
- [ ] Read `tig_coherent_computer.py` end-to-end and verify it implements the harmonic-mean composition per PROVEN_CONFIGURATION.md
- [ ] Run `benchmark.py` and record outputs per test (convergence / throughput / self-repair / etc.)
- [ ] Confirm LOC counts for ARTIFACTS (554 benchmark + 588 core classifier)
- [ ] Draft a one-paragraph "what the classifier does" explanation that a senior SRE could read in 2 minutes and understand
- [ ] Cross-reference 88% drop-rate number from TIG Unity COMPUTE.md against the 32pp whitepaper number (see HANDOFF_INDEX.md §3 open item) — if reconciliation is needed before a DevOps-community pitch, flag it here

---

## Missing from repo (blockers for Phase 1)

- **All-or-Nothing-E clone**: not yet pulled into `_brayden_repos/` (or not yet verified).
- **Classifier API wrapper design doc**: does not exist yet. Phase 1 T2 deliverable.
- **Synthetic-telemetry generator**: does not exist yet. Phase 1 T3 deliverable.
- **SRE-community framing doc**: the "why an SRE cares about this" one-pager is not yet written; see PITCH_DRAFT for the draft framing.
- **Cross-branch 88%/32pp reconciliation**: open item from HANDOFF_INDEX.md §3; not strictly blocking this branch but should be resolved before a Phase-2 benchmark-comparison pitch.
