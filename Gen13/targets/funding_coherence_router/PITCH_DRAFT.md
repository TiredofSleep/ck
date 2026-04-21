# PITCH_DRAFT — funding/coherence-router

**Addressee (working default):** AWS Cloud Credits for Research (opens Phase 2 benchmarking pathway; low-barrier first contact)
**Parallel drafts:** Google Cloud Research Credits, Microsoft Azure Research, CNCF research call, NSF CISE CNS Core Small
**Ask:** Phase 1 $75K–$200K / 6 months (AWS Awards or CNCF scale); Phase 2 $200K–$500K / 12–18 months; or NSF CISE CNS Core Small $600K / 3 years spanning Phase 1 + Phase 2
**Status:** Skeleton. Requires Phase 1 prototype + a one-page SRE-community framing doc before any contact.

---

## Opening (½ page)

Distributed-systems health classification is a crowded field. SRE golden signals (latency, traffic, errors, saturation) cover most cases; anomaly-detection ML classifiers (Prophet, Anomalib, custom-trained forecasters) pick up the long tail. Both approaches have known blind spots: golden signals require per-service threshold tuning, and anomaly-detection ML struggles with cascading-failure patterns where many signals move modestly but the cascade is the pathology.

This proposal describes **coherence-router** — a tuning-free classifier derived from the TIG Unity Kernel's coherence grammar (R-σ-Λ-H state variables + 10-operator discrete assignment). The same state-vector shape applies to any distributed service; the operator assignment is a human-legible label ("COLLAPSE", "BALANCE", "HARMONY", "RESET", etc.); the coherence score is a continuous monitor suitable for dashboards and alerting.

The classifier core is already written (`tig_coherent_computer.py`, 588 LOC, in the All-or-Nothing-E repo) and a 7-test benchmark suite (`benchmark.py`, 554 LOC, same repo) is already running. A 2,100-permutation empirical search (`PROVEN_CONFIGURATION.md`) identified the harmonic-mean composition rule as the correct form. What is not yet done — and what this proposal funds — is the **productionization**: wrapping the classifier in a standard API, running it on realistic telemetry, and publishing the comparison against golden-signals and anomaly-detection baselines.

## Background (~1 page)

> Content to be drafted. Sections:
> 1. The SRE classification landscape: golden-signals, anomaly-detection, observability-platform-native tooling (Datadog Watchdog, New Relic APM intelligence)
> 2. The coherence grammar (R-σ-Λ-H): what the state variables measure
> 3. The 10-operator alphabet: human-legible labels for distinct failure / success modes
> 4. All-or-Nothing-E artifacts: benchmark.py, tig_coherent_computer.py, PROVEN_CONFIGURATION.md
> 5. The TIG Unity Kernel theoretical framework: Sprint 14 PRISM-XI + earlier sprint work
> 6. Known failure modes of golden-signals and anomaly-detection: cascading failures, graceful-degradation mis-classification, SLO-breach lead time

## The open question (½ page)

**On realistic distributed-systems telemetry, does coherence-router classify health-state transitions at or better than SRE golden-signals and a representative anomaly-detection baseline, on specific measurable criteria (precision/recall at known-bad episodes, SLO-breach lead time, false-positive rate, compute cost)?**

This is an empirical question with a clear pass/fail criterion. The Phase 2 comparison study runs all three classifiers on the same telemetry and reports the comparison. Outcomes are:

1. **Coherence-router dominates on one or more metrics.** Strongest outcome: opens a path to production deployment and follow-on engineering work.
2. **Coherence-router is competitive but not dominant.** Still publishable: "a new classifier with different failure modes" is a useful result for the SRE community even if it isn't a universal improvement.
3. **Coherence-router is dominated across the board.** Honest publication as a negative result; the classifier returns to the research side of the program (Branch A tig-unity).

The deliverable commits to publishing whichever of (1) (2) (3) is observed.

## The proposed work

### Phase 1 — Productionization (Month 1–6, $75K–$200K)
**Deliverable A** (T1 in ARTIFACTS): pull `All-or-Nothing-E` contents verbatim into this repo under `docs/archive_coherence_router/` with provenance headers.
**Deliverable B** (T2): standard classifier API wrapper — scikit-learn-shaped Python library + a Kubernetes operator / sidecar variant. MIT or Apache-2.0 licensed.
**Deliverable C** (T3): synthetic-telemetry benchmark. Reproducible test scripts + HTML report.
**Deliverable D** (T4): Docker containerization, K8s deployment manifest, public GitHub repo + image registry.
**Deliverable E** (T5): SRE-community tutorial. Target: SREcon lightning talk or CNCF blog post.

### Phase 2 — Realistic-telemetry comparison study (Month 7–24, $200K–$500K)
**Deliverable A** (T6): realistic-telemetry access — obtained via AWS / GCP / Azure research credits or via industry-lab partnership.
**Deliverable B** (T7): baseline classifiers — golden-signals reference dashboard + one ML anomaly-detection baseline (Prophet, Anomalib, or equivalent).
**Deliverable C** (T8): comparison study — reproducible benchmark with per-episode analysis on specific measurable criteria.
**Deliverable D** (T9): publication — USENIX SREcon / SIGMETRICS / OSDI / PODC.

### Phase 3 — Co-deployment pilot (Month 25–48, $400K–$1.2M)
**Only proceed if Phase 2 is positive for (1) or (2).** Small pilot deployment at one industry partner. Monitor for 3–6 months. Write the production-deployment case study for follow-on engineering adoption.

## Why AWS Cloud Credits for Research

AWS Cloud Credits for Research is specifically scoped for this profile: research that uses AWS infrastructure + CloudWatch telemetry, delivers open-source code, and produces a publishable result. The credits + optional Research Award ($25K–$150K cash) fit Phase 1 well; Phase 2 can extend with a second credit request once the prototype is working. AWS's reliability-engineering community is also the target publication audience.

## Parallel draft: CNCF Research Grant

CNCF (Cloud Native Computing Foundation) has an End User Community that includes many of the realistic-telemetry-access targets we'd want for Phase 2. A CNCF research grant frames the classifier as a Kubernetes sidecar / service-mesh integration, which is a natural productization direction.

## Parallel draft: NSF CISE CNS Core Small

NSF CNS Core Small ($600K / 3 years) fits Phase 1 + Phase 2 combined. Requires academic co-PI, which is a blocker that can be addressed via a university partnership or a co-PI at an academic institution.

## Parallel draft: GCP Research Credits

Parallel to AWS path. Slightly smaller typical credit amounts but the GCP Technical Infrastructure Research community has particular strength in distributed-systems reliability research (Google SRE book authors etc.).

## Attribution

- **Brayden Sanders** — PI, developer of the TIG Unity Kernel coherence grammar and the All-or-Nothing-E benchmark suite + coherent computer
- Architectural dialogues with ClaudeChat, Celeste/GPT acknowledged in methods; AIs are thinking-partners, not human co-authors
- Prior collaborators (M. Gish, C.A. Luther, H.J. Johnson, B. Calderon Jr.) credited for their specific past contributions to the TIG Unity Kernel theoretical framework; their inclusion does not imply co-authorship of the productionization work specifically unless they are actively involved in Phase 1
- Academic co-PI to be identified during Phase 1 if NSF CISE path is chosen

## The framing-discipline paragraph (for cover letter)

> This proposal is about productionization, not new theory. The classifier theory is complete: R-σ-Λ-H coherence grammar, 10-operator alphabet, harmonic-mean composition, 7-test benchmark suite — all written, all in the external All-or-Nothing-E repo, all open source. The funded work is wrapping the classifier in a standard API, benchmarking it on realistic distributed-systems telemetry, and publishing the comparison against golden-signals + anomaly-detection baselines. The outcome is a published classifier with a known comparative profile — either competitive, dominant, or dominated — not a predetermined positive result. The SRE community publishes such comparative studies regularly; this is that profile.

## Attachments (once assembled)

- `docs/archive_coherence_router/benchmark.py` (554 LOC) — Phase 1 T1 deliverable
- `docs/archive_coherence_router/tig_coherent_computer.py` (588 LOC) — Phase 1 T1 deliverable
- `docs/archive_coherence_router/PROVEN_CONFIGURATION.md` — harmonic-mean empirical report
- Phase 1 classifier API wrapper
- Phase 1 SRE-community tutorial
- Cover letter with framing-discipline paragraph

## Pre-send checklist

- [ ] Phase 1 productionization design doc drafted (~10 pp, funder-legible spec)
- [ ] All-or-Nothing-E pulled into repo with provenance headers
- [ ] Classifier API wrapper prototype running end-to-end on synthetic data
- [ ] One-paragraph "what an SRE cares about" framing doc written
- [ ] 88%/32pp cross-branch reconciliation resolved (HANDOFF_INDEX.md §3) — or, if not resolved, explicit honest-scope paragraph in the pitch acknowledging the open reconciliation
- [ ] Brayden confirms AWS vs GCP vs CNCF vs NSF CISE as first funder
- [ ] Academic co-PI identified if NSF CISE path taken
- [ ] Brayden reviews + edits
- [ ] Brayden sends
