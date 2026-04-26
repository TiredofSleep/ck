# FUNDERS — funding/coherence-router

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---


## Primary candidates (★ priority)

### 1. AWS AI Research Awards / AWS Cloud Credits for Research — ★★★★★
- **Programs**: AWS Cloud Credits for Research (rolling), AWS AI Research Awards (annual), AWS Distributed Systems Research (topic-specific)
- **Why fit**: AWS funds exactly this profile — applied systems research that could plausibly improve cloud-service operations, using AWS infrastructure (EC2 + CloudWatch + X-Ray telemetry) as the benchmark target. Coherence-router on AWS CloudWatch telemetry is a cleanly-scopeable Phase-2 scenario.
- **Typical size**: Credits $10K–$100K; Research Awards $25K–$150K cash + compute credits
- **Entry point**: AWS Cloud Credits for Research application (rolling); AWS AI Research Awards (annual solicitation)
- **Blockers before contact**: Phase 1 prototype with at least synthetic-telemetry demo; AWS account + contact

### 2. Google Cloud Research Credits + GCP-DeepMind Research Partnerships — ★★★★★
- **Programs**: Google Cloud Research Credits (rolling); GCP Technical Infrastructure Research; occasional targeted grants via Google PhD Fellowship (for academic collaborators)
- **Why fit**: Same profile as AWS. GCP's reliability-engineering community (Google SRE book authors) is the target publication audience; GCP research credits fund the benchmark work.
- **Typical size**: Credits $5K–$100K; occasional targeted cash
- **Entry point**: Google Cloud Research Credits application
- **Blockers before contact**: Phase 1 prototype; GCP account

### 3. Microsoft Azure Research Grants / MS Research Open Source — ★★★★☆
- **Programs**: Azure Research Credits; MS Research Open Source grants; MSR Reliability Engineering
- **Why fit**: Azure has a strong reliability-engineering research arm (MSR Cambridge, MSR Cambridge UK); coherence-router on Azure Monitor / App Insights telemetry is a viable Phase-2 scenario
- **Typical size**: Credits $10K–$100K; MSR cash grants $50K–$300K
- **Entry point**: Azure Research Credits application; MSR research contact via submissions
- **Blockers before contact**: Phase 1 prototype; Azure account or academic MSR contact

### 4. CNCF (Cloud Native Computing Foundation) Research Grants — ★★★★☆
- **Programs**: CNCF research subprograms, CNCF End User Community research topics
- **Why fit**: CNCF sponsors Kubernetes-adjacent research; coherence-router as a health-classification sidecar in a service mesh (Istio / Linkerd) is a clean CNCF scenario. CNCF also has direct access to production operators willing to share anonymized telemetry.
- **Typical size**: $25K–$250K
- **Entry point**: CNCF research call (periodic); reach out to End User Community
- **Blockers before contact**: Phase 1 prototype packaged as a container / sidecar; K8s-compatible interface design

### 5. NSF CISE — CNS + CCF CSR + CCF Software Engineering — ★★★★☆
- **Programs**: NSF CISE core programs: CNS (Computer and Network Systems), CCF CSR (Computer Systems Research), CCF SE (Software Engineering)
- **Why fit**: CISE's applied-systems track funds exactly this kind of classifier-on-distributed-systems work. CNS Core Small grants fit Phase 1 well; Medium grants fit Phase 2.
- **Typical size**: Core Small $600K / 3 years; Medium $1.2M / 4 years
- **Entry point**: annual CISE core solicitation
- **Blockers before contact**: academic co-PI required; Phase 1 prototype; written proposal

### 6. Sloan Foundation — Digital Technology (Computing Research) — ★★★☆☆
- **Programs**: Sloan Digital Technology portfolio, including applied-systems and reliability research
- **Why fit**: Sloan funds well-scoped applied-systems research; coherence-router is well-scoped
- **Typical size**: $250K–$1M over 2–3 years
- **Entry point**: institutional LOI
- **Blockers before contact**: academic host; Sloan prefers institutions over independent PIs

## Secondary candidates

### 7. Industry DevOps / SRE research labs — ★★★☆☆ (co-development pathway + later funding)
- **Candidates**: LinkedIn SRE, Uber reliability, Shopify production engineering, Netflix chaos engineering, Facebook production engineering
- **Why fit**: each runs a research program (with varying formalness); each has realistic-telemetry access; a co-development engagement with one of these is how Phase 2 gets anonymized telemetry
- **Typical size**: in-kind (telemetry, compute, review) + occasional small cash grants ($25K–$100K)
- **Entry point**: cold email to an SRE-team engineering director with the Phase-1 prototype as the opening pitch
- **Blockers before contact**: working prototype; a convincing "why this is worth your SRE team's time" explanation

### 8. OpenAI / Anthropic infrastructure research — ★★★☆☆
- **Programs**: both companies periodically fund distributed-systems and ML-infra research
- **Why fit**: the coherence grammar applies to ML training / inference infra just as to web-service infra; a pitch framing the tool for ML-infra reliability could land at either
- **Typical size**: varies
- **Entry point**: research team contact

### 9. ARPA-H / DARPA-adjacent mission-critical reliability tracks — ★★★☆☆
- Occasional funding for applied-systems reliability in mission-critical contexts (defense, health-system infrastructure). Lower priority than commercial funders but nonzero.

## What they all want, in order

1. **A working prototype.** Phase 1 funding specifically gets a prototype onto AWS / GCP / Azure infrastructure and wraps the coherence grammar in a standard classifier API (e.g., a scikit-learn `BaseEstimator`-shaped object, or a Kubernetes operator interface).
2. **A realistic-telemetry benchmark.** Phase 2 is the benchmark work. Industry funders want to see the classifier compared against golden-signals and at least one ML anomaly-detection baseline on real (anonymized) telemetry.
3. **Open source.** Cloud-provider research credits and CNCF expect open-source release. The PROVEN_CONFIGURATION.md harmonic-mean result is already open; the productionization work should be too.
4. **SRE-community-legible framing.** The pitch must not read as theoretical-CS research — it must read as "new signal for your dashboard," with concrete use cases (cascading-failure detection, graceful-degradation triggering, SLO-breach prediction).
5. **Academic co-PI** for NSF CISE; not strictly required for cloud-provider research credits or CNCF, but useful.

## What the branch has vs. needs

Has:
- `benchmark.py` (554 LOC, 7 tests) — in external All-or-Nothing-E repo
- `tig_coherent_computer.py` (588 LOC) — core classifier in external All-or-Nothing-E repo
- `PROVEN_CONFIGURATION.md` — harmonic-mean correction, empirically derived from 2,100 permutations
- TIG Unity Kernel theoretical framework (Sprint 14 + tig-synthesis)
- R-σ-Λ-H state-grammar specification
- Cross-branch cohesion with Branch A (tig-unity) on the underlying Kernel

Needs:
- Phase 1 productionization: wrap in standard classifier API, run on synthetic telemetry, containerize
- Open-source release on GitHub with proper README, tutorial, and benchmark reproduction scripts
- Cloud-provider research account (AWS / GCP / Azure) for Phase 2 benchmarking
- Realistic-telemetry access for Phase 2 (via cloud-provider program or industry lab)
- SRE-community tutorial / blog post targeting SREcon or CNCF blog
- Academic co-PI if NSF CISE path chosen
