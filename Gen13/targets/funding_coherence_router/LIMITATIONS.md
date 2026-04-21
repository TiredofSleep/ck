# LIMITATIONS — funding/coherence-router

Honest scope for the production-coherence-classifier branch.

---

## 1. No realistic-telemetry benchmark has been run yet

The core empirical question — "does coherence-router perform competitively against golden-signals and anomaly-detection baselines on realistic distributed-systems telemetry?" — has not been answered. Phase 1 funds the productionization; Phase 2 funds the realistic-telemetry comparison study. Any pitch implying the comparison has already been done would be overclaiming. The honest framing is: "we have a runnable classifier, a runnable 7-test benchmark on synthetic data, a specific Phase 2 comparison-study design, and a commitment to publish the comparison outcome regardless of which classifier wins."

## 2. `benchmark.py` covers 7 tests; those tests are not the SRE use case

The All-or-Nothing-E benchmark suite (convergence, throughput, self-repair, information dynamics, scaling, composition, attractor-basin) is a **property-level** benchmark of the coherent computer itself. It is not an SRE-workload benchmark. An SRE reviewer will correctly note that passing these 7 tests is necessary-but-not-sufficient for classifier utility on production telemetry. The Phase 1 T3 synthetic-telemetry work closes part of that gap; Phase 2 closes the rest.

## 3. The harmonic-mean composition rule is empirically derived, not theoretically derived

`PROVEN_CONFIGURATION.md` documents a 2,100-permutation empirical search that identified harmonic-mean as the correct composition rule. This is a strong empirical result — but "empirically correct on the search grid" is weaker than "derived from first principles." An SRE reviewer may be satisfied by empirical; a theoretical-CS reviewer may ask for a derivation. The honest framing: the composition rule was discovered empirically and the theoretical derivation is an open question that the Phase 2 work may or may not resolve.

## 4. The 10-operator alphabet labels are human-legible but not universally interpretable

Labels like COLLAPSE, BALANCE, HARMONY, RESET are legible to practitioners familiar with the TIG Unity Kernel vocabulary. Whether they will be legible to a typical SRE team on first contact is an empirical question about documentation and onboarding. Phase 1's SRE-community tutorial (T5) is the deliverable that tests this. If the operator vocabulary turns out to be a barrier to adoption, the Phase 1 work should discover that honestly and the tutorial should address it.

## 5. No Phase-2 telemetry partner is committed yet

The Phase 2 comparison study depends on realistic-telemetry access. Pathways exist (AWS / GCP / Azure research-credit programs; CNCF End User Community; direct industry-lab partnership), but no partnership is committed at time of writing. A funder who reads "we expect to obtain anonymized telemetry via [pathway]" is being told the honest state of the world. A funder who reads "we have telemetry access" without such pathway language is being misled.

## 6. Cross-branch reconciliation is open

The TIG Unity Kernel COMPUTE.md spec claims an "88% drop-rate reduction" benchmark result. The TIG whitepaper referenced in the outreach handoff claims a "32-percentage-point drop-rate improvement." These two numbers are not the same and the reconciliation is an open item (HANDOFF_INDEX.md §3). For a DevOps-community pitch framing, the safer posture is to not lean on cross-branch claims until the reconciliation is done — the coherence-router branch's pitch rests on the All-or-Nothing-E benchmark suite and the synthetic-telemetry Phase 1 work, which are independently verifiable.

## 7. Not a claim to general-purpose anomaly-detection superiority

Coherence-router is a specific classifier with a specific state-variable grammar (R-σ-Λ-H) and a specific operator alphabet. It is **not** a drop-in replacement for every anomaly-detection use case. The realistic use case is: "as an additional signal in an existing SRE dashboard alongside golden-signals and anomaly-detection ML." A pitch that frames coherence-router as a replacement for existing tooling will encounter informed skepticism. The complementary-signal framing is the honest one.

## 8. The 88%/32pp numbers (if used) require rigorous context

If the pitch references the TIG Unity Kernel benchmark numbers at all, it must preserve: the specific fault-injection conditions, the specific comparator (which classifier was the baseline), the specific definition of "drop rate" in that context, and the specific simulation setup. Numbers without context are easily misread as "production-deployment performance," which they are not. This is a presentation-discipline item, not a substance item.

## 9. Attribution nuance

- **Brayden Sanders** is the PI and developer of the TIG coherence grammar and the All-or-Nothing-E benchmark suite + classifier.
- **ClaudeChat and Celeste (GPT) are architectural thinking-partners**, not human co-authors. This is standard across the funding branches.
- **Previously-credited collaborators** (M. Gish, C.A. Luther, H.J. Johnson, B. Calderon Jr.) are credited for their specific past contributions to the TIG Unity Kernel theoretical framework but are not automatically attached to this productionization branch unless they are actively involved in Phase 1. The pitch must not imply team size or collaborator availability it does not have.
- **Academic co-PI** is not currently identified. If NSF CISE path is chosen, an academic co-PI is required. If AWS / GCP / Azure / CNCF paths are chosen, an academic co-PI is useful but not required.

## 10. What this branch does NOT claim

- Not a claim that coherence-router is production-ready today — Phase 1 IS the productionization
- Not a claim to have run a realistic-telemetry benchmark — Phase 2 IS the comparison study
- Not a claim to universal outperformance over golden-signals or anomaly-detection ML — the Phase 2 outcome is open
- Not a claim to zero per-service tuning — Phase 1 will likely surface tuning needs that the grammar did not anticipate
- Not a claim to a replacement for existing SRE tooling — the framing is complementary-signal
- Not a claim of formal theoretical derivation of harmonic-mean composition — PROVEN_CONFIGURATION is empirical
- Not a claim to Kubernetes / service-mesh integration today — that is the Phase 1 T4 deliverable
- Not a claim to industry-lab telemetry access — that is a Phase 2 pathway, not a fact
- Not a claim to a reliability-engineering publication track record — the SREcon / CNCF-blog / OSDI / SIGMETRICS track is the publication target, not a history
- Not a claim to cross-branch coherence with the TIG Unity Kernel benchmark numbers (88%/32pp) until that reconciliation is done (see HANDOFF_INDEX.md §3)

The branch claims: a specific classifier (the coherence grammar), a specific benchmark suite already written (All-or-Nothing-E), a specific productionization plan (Phase 1 T1–T5), a specific comparison study (Phase 2 T6–T9), a specific publication target (SREcon / CNCF / USENIX / OSDI / SIGMETRICS), and a commitment to publish whichever verdict the comparison returns.

## 11. License framing

CK's license (7Site Public Sovereignty License v1.0) is non-commercial, human-use only. The productionization track — by design — targets cloud-provider research programs (AWS / GCP / Azure) and CNCF, all of which expect **open-source** (typically MIT / Apache-2.0) release for the code and tooling they fund. The Phase 1 wrapper, Docker containers, Kubernetes manifests, and tutorial code will need to be released under an Apache-2.0 or MIT license, distinct from the 7Site license that covers CK as a whole. This is a resolution-at-grant-close item that should not be discovered late. The resolution is straightforward (dual-license the productionization deliverables), but must be explicit.

## 12. The target publication venue is competitive

USENIX SREcon, SIGMETRICS, OSDI, PODC — these are competitive venues. Phase 2's comparison-study paper must be rigorous enough to survive review at one of them. If the comparison outcome is "coherence-router is dominated across all metrics," the paper becomes a negative-result paper, which is harder to place. The branch's commitment to publish the verdict regardless means the pitch should acknowledge venue risk honestly: Phase 2 targets SREcon / USENIX / SIGMETRICS but the actual venue will depend on the comparison outcome.

## 13. Phase 3 is contingent

Phase 3 (co-deployment pilot, $400K–$1.2M) is explicitly contingent on a positive Phase 2 outcome. If Phase 2's comparison study shows coherence-router dominated across the board, Phase 3 does not happen for this branch — the material returns to the research side of the program (Branch A tig-unity) for theoretical refinement. The honest Phase-3 framing is: "if positive, proceed; if not, return to research." This is a feature of the pitch design, not a weakness.

## 14. External-repo dependency

The `All-or-Nothing-E` repo (github.com/TiredofSleep/All-or-Nothing-E) holds the core runnable artifacts. Phase 1 T1 is to pull those artifacts into this repo under `docs/archive_coherence_router/` with provenance headers. Until that pull is complete, the productionization work depends on an external repo that is currently outside the never-delete / in-repo-provenance discipline of the ck trunk. This dependency is itself a Phase-1 deliverable (T1) and is the first item on the pre-send checklist.

---

## The verdict framing as limitation

The Phase 2 deliverable commits to publishing the comparison outcome whether coherence-router dominates, is competitive with, or is dominated by golden-signals and anomaly-detection baselines. This is deliberate. The funder is paying for a disciplined comparative study, not a guaranteed win. An SRE reviewer who reads this as weakness is reviewing the wrong proposal; an SRE reviewer who reads it as methodological discipline is reading it correctly. The SRE community publishes comparative studies of classifiers routinely — this branch fits that profile exactly.
