# funding/coherence-router

**Track J — Production Coherence Classifier for DevOps / SRE**
**Primary funder pool:** NLnet NGI Zero · Sloan · Bloomberg Philanthropies · CNCF research · AWS/GCP/Azure research credits · industry DevOps/SRE labs
**Status:** Pre-pitch. Runnable artifacts (`benchmark.py` 554 LOC + `tig_coherent_computer.py` 588 LOC + `PROVEN_CONFIGURATION.md`) recovered into [`Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/`](Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/). Phase 1 T1 **complete**.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

Distributed-systems health classification — *"is this service healthy right now?"* — is normally done with SRE golden signals (latency, traffic, errors, saturation) plus anomaly-detection ML classifiers. These work but require per-service tuning and have known blind spots around cascading failures and information-dynamics anomalies. **The TIG coherence grammar** (R-σ-Λ-H variables + 10-operator discrete assignment) **is a tuning-free alternative**: the same state-vector shape applies across services, the operator assignment is a human-legible label (e.g., "COLLAPSE", "RESET"), and the coherence score is a continuous monitor. The All-or-Nothing-E artifact already contains a 554-LOC benchmark suite covering convergence, throughput, self-repair, information dynamics, scaling, composition, and attractor-basin behavior. **The funder-facing ask is to productionize this as a standard-interface classifier**, run it on realistic telemetry (e.g., anonymized SRE traces from a cloud-scale operator), and publish the comparison against golden-signals and anomaly-detection baselines.

## Runnable artifacts (recovered 2026-04-21)

1. **`benchmark.py`** (~554 LOC) — 7-benchmark suite: convergence test, throughput test, self-repair test (50% chaos injection), information-dynamics test, scaling test, composition-depth test, attractor-basin test. Location: [`Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/benchmark.py`](Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/benchmark.py).
2. **`tig_coherent_computer.py`** (~588 LOC) — core composition + coherence computation + attractor-basin analysis. Location: [`Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/tig_coherent_computer.py`](Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/tig_coherent_computer.py).
3. **`PROVEN_CONFIGURATION.md`** — 2,100-permutation empirical discovery that **harmonic-mean composition** (not arithmetic-mean) is the correct composition form. 89 LOC markdown. Documents the formula correction from an earlier arithmetic-mean variant.
4. **Source repo** (snapshot, provenance-tagged): `github.com/TiredofSleep/All-or-Nothing-E` — now preserved under `archive_all_or_nothing_e/` with a `PROVENANCE.md` header per the never-delete policy.
5. **Cross-branch grounding**: TIG Unity Kernel spec in `TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT/docs/COMPUTE.md` provides the theoretical base.

## Where this differs from Branch A (tig-unity)

Branch A (`funding/tig-unity`) targets the **infrastructure-reliability research community** (NSF CNS / DOE ASCR / Sloan) with a framing of "TIG Unity Kernel for compute-health research." **Branch J targets the DevOps / SRE practitioner community** (AWS/GCP/Azure research credits, CNCF, industry labs) with a framing of "coherence-router as a production classifier." The two are complementary: Branch A funds the research side, Branch J funds the productionization side. If both succeed, research outputs feed productization outputs and vice-versa.

## Where this differs from Branch D (ck-interpretable-ai)

Branch D funds CK as an **interpretability research artifact** (AI safety funders: Anthropic Fellows, Schmidt, Open Phil, SFF). Branch J funds the **applied productionization** of the same underlying coherence math into a DevOps tool. No overlap in funder pool, no overlap in deliverable shape.

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_coherence_router/`](Gen13/targets/funding_coherence_router/):

- [`README.md`](Gen13/targets/funding_coherence_router/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_coherence_router/FUNDERS.md) — prioritized funder list (NLnet / Sloan / Bloomberg / CNCF / cloud research programs)
- [`ARTIFACTS.md`](Gen13/targets/funding_coherence_router/ARTIFACTS.md) — archive pull + productionization plan
- [`PITCH_DRAFT.md`](Gen13/targets/funding_coherence_router/PITCH_DRAFT.md) — full pitch draft
- [`LIMITATIONS.md`](Gen13/targets/funding_coherence_router/LIMITATIONS.md) — honest-scope items
- [`STATUS.md`](Gen13/targets/funding_coherence_router/STATUS.md) — readiness checklist (Phase 1 T1 complete 2026-04-21)
- [`archive_all_or_nothing_e/`](Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/) — the recovered 45-file external-repo bundle with provenance headers

## The project this branch is a track of

Branch J of the 10-branch funding architecture. For the full project overview, see **`tig-synthesis`**:

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

## License

7Site Public Sovereignty License v1.0 — human use only, no commercial, no military, free forever. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
