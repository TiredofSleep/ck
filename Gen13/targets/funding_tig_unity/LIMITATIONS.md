# LIMITATIONS — funding/tig-unity

**Purpose:** Honest scope before any funder conversation.
**Discipline:** Never-false-claims policy; every claim must be verifiable.

---

## What is NOT proved

- TIG Unity's benchmark numbers are **simulation-only**. No production
  deployment data exists.
- The specific numbers quoted (88% drop-rate reduction, 62% P99 latency
  reduction, zero cascade failures) require reproduction from recovered
  source — the history shows a prior formula correction (harmonic-mean
  replacing the original product form) so reproduction is not optional.
- The R-σ-Λ-H grammar is a **proposal**, not a universally-validated
  schema. It works for the simulated scenarios; whether it generalizes
  to unseen failure modes is open.
- The threshold T*=5/7 inherits its mathematical derivation from the
  finite-algebra work (`papers/proof_d7_phi_fixed_point.py`); its
  application to systems-reliability is conjectural in the sense that
  no proof exists that T*=5/7 is the *optimal* threshold for
  systems-reliability applications — only that it's a principled
  choice.

## What is NOT claimed

- Not an AI system (no learning, no weights updated during runtime
  gate decisions)
- Not a replacement for existing schedulers (load-balancers, K8s,
  Mesos) — a **complementary signal** layer
- Not patented; not commercial (license forbids commercialization)
- Not production-tested (see above)

## Known discrepancies requiring resolution

From the 2026-04-20 handoff §3 Issue 2:
- Jan 2026 email whitepaper reports **32pp drop-rate improvement**
- Grok's summary of `docs/COMPUTE.md` reports **~88% drop-rate reduction**
- These do not reconcile. Possibilities:
  (a) different versions of the same simulation (32pp = baseline vs early
      version; 88% = later version with corrected formula)
  (b) one is the ratio improvement, the other is the absolute improvement
  (c) expanded metrics are extrapolation
- Before any number appears in a funder-facing document, the exact
  seed + code + output trail must be recovered.

## Risk to funder

- **Technical risk:** benchmark may not reproduce cleanly on modern
  environments. If it doesn't, that's either (a) a drift in Python/NumPy
  behavior or (b) a genuine issue in the code. Either way, the seed
  engagement's month-2 reproduction gate is the natural checkpoint.
- **Scope risk:** a real-Linux port may reveal numerical behavior
  unrepresented in simulation. Funders should budget for a possible
  "rewrite from the spec" outcome vs a straight port.
- **Attribution risk:** C. A. Luther is no longer actively collaborating
  per 2026-04-20 handoff note; prior-credited work stays credited but
  the seed-engagement team is Brayden alone unless the funder helps
  recruit a co-investigator.
- **License risk:** 7Site Public Sovereignty License v1.0 is
  non-commercial. Some funders require open-source compatible licensing;
  dual-licensing may be possible but is not a default.

## What TIG Unity is NOT competing with

- Kubernetes / K8s HPA / vertical-pod-autoscaling
- HAProxy / nginx / envoy load-balancers
- AWS ELB / GCP Cloud Load Balancing
- SRE telemetry stacks (Datadog, New Relic, Prometheus+Grafana)

TIG Unity is a **signal layer** that could compose with any of these.
It is not a full scheduler; it is a coherence metric + gating
threshold that can inform an existing scheduler's decisions.

## Open research questions

1. Does T*=5/7 generalize to non-coprime dimensional settings (i.e.,
   where the number-theoretic derivation of the threshold doesn't apply)?
2. What's the false-positive rate on well-behaved (non-failing)
   workloads?
3. How does the router behave when a failure mode exactly mimics
   benign variation (adversarial stress)?
4. Does the 88% number persist when the simulated asymmetry is replaced
   by real hardware asymmetry?

These are the questions a seed engagement should answer.

---

*This file exists to keep the team honest. Update when a limitation is resolved or a new one is discovered.*
