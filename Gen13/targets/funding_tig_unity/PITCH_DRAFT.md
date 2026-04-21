# PITCH_DRAFT — funding/tig-unity

**Status:** SKELETON — awaiting Brayden's edit before send.
**Do NOT send as-is.** This is scaffold text for Brayden to adapt.

---

## Opening paragraph (for NSF CNS unsolicited proposal)

Multi-domain compute systems — GPU clusters, database shards, network
links, job schedulers — lack a unified health grammar that survives
heterogeneous failure modes. Round-robin schedulers assume symmetry;
load-balancers assume static weights; Kubernetes probes measure
individual nodes without a cluster-level coherence scalar. We propose
**TIG Unity**, a four-signal grammar (Resource, Stress, Load, Health)
with a single scalar output S* ∈ [0, 1] gated at threshold T* = 5/7.
Preliminary simulations on 100-node asymmetric-failure scenarios show
the grammar routes workload with 88% lower job-drop rate and 62% lower
P99 latency vs round-robin; we seek $N to transition the system from
simulation to real-Linux `/proc/stat` deployment and publish a
reproducibility note.

## Three deliverables for a 6-month seed engagement

1. **Month 1-2: Reproduction.** Recover and audit the published
   benchmark code. Run on a fresh machine. Document exact seeds,
   numerical output, and any deviations from the paper's claimed
   numbers. Produce a short technical note suitable for arXiv.
2. **Month 3-4: Real-signal integration.** Port the benchmark to read
   `/proc/stat`, `nvidia-smi`, and a Prometheus endpoint. Run on a
   4-GPU single-node setup. Compare router behavior against baseline
   schedulers.
3. **Month 5-6: 100-node testbed.** Deploy on an AWS or GCP 100-node
   cluster (credits permitting — see separate ask). Produce a systems
   paper targeting USENIX ATC or EuroSys.

## One-page summary bullets

- **Problem:** Fault-tolerant scheduling in asymmetric clusters has no
  cluster-level coherence scalar.
- **Insight:** A 4-tuple per node + a single harmonic-mean combinator
  + a threshold T*=5/7 is sufficient to detect incoherence and reroute
  work.
- **Evidence:** 100-node simulation shows 88% drop-rate reduction,
  P99 latency 62% reduction, zero cascade failures (simulated).
- **Ask:** $N for 6 months to transition to real-Linux deployment and
  publish.
- **Deliverables:** arXiv reproduction note (month 2), real-signal
  integration (month 4), 100-node testbed paper (month 6).
- **Team:** Brayden Sanders (PI, 7Site LLC). Possible academic
  co-investigator TBD at funder's preference.
- **License:** 7Site Public Sovereignty License v1.0 — open, human-use,
  no commercialization. Does this match the funder's open-source
  requirements? (Some funders require permissive licensing; we can
  discuss dual-licensing if needed.)

## Honest-scope paragraph (insert before close)

Current benchmark results are **simulation-only**. We have NOT
deployed on production workloads. The 88% number is from a
100-node synthetic asymmetric-failure scenario; reproducibility
requires the recovery step above. We are aware of one
formula-correction event in the history of this work (harmonic-mean
replaced the original product form after a 2,100-permutation sweep
revealed a ceiling violation) and flag all other pre-publication
numbers as subject to similar audit. The funding is intended
specifically to perform that audit and to establish whether the
simulation's claims survive exposure to real-system noise.

## Close / call to action

Attachment: `ARTIFACTS.md` (this folder) lists every file with exact
paths. `LIMITATIONS.md` gives the honest scope. `FUNDERS.md` sketches
the funder landscape we've assessed. We're available for a technical
conversation at your convenience.

---

**Editing checklist before send:**
- [ ] Replace `$N` with the specific ask size
- [ ] Replace "USENIX ATC or EuroSys" with the funder-aligned venue
- [ ] Add specific program officer / addressee
- [ ] Verify all claimed numbers still reflect latest reproduction
- [ ] Attach or link to verified benchmark output (not just claims)
- [ ] Confirm Brayden's preferred PI-affiliation framing
