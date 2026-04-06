# FRONTIER MAP MEMO
## Locating Dead-End Gaps Where CK Can Function as a Structured Questioning Engine

**Document type:** Research frontier analysis  
**Purpose:** Map where current methods visibly stall, classify the obstruction type, and define the exact questions CK should be asked in each domain  
**Date:** 2026-04-05  
**Scope:** 5 domains. No claims CK solves any of them.

---

## PART 1 — DEAD-END GAP TAXONOMY

A **dead-end gap** is a frontier where local structure is known, global closure is missing, and current methods have stopped producing decisive progress. Six types:

| Type | Definition | Signature |
|---|---|---|
| **local-to-global** | Local structure known; integration into a global object fails | Lemmas exist, proofs don't close; local models work, global ones don't |
| **observation-to-mechanism** | Effect is measured; underlying cause is unknown; model zoo grows | Null direct-detection results; mechanism competition without resolution |
| **memory-to-proof** | Retrieved facts not verified against current evidence state | Agent confabulates; old results treated as current; provenance lost |
| **scaling-gap** | Small-scale results don't generalize; hardware or complexity barrier | Lab demos that don't scale; proofs that don't lift to large instances |
| **signal-to-interpretation** | Same signal admits multiple incompatible interpretations | Competing theories all partially fit; no discriminating experiment |
| **retrieval-to-action** | Correct knowledge exists but cannot be located or composed at decision time | Known theorems not applied; known data not retrieved; coherence degrades mid-task |

CK's invariant architecture is specifically designed to address the last three: memory-to-proof (IG2+IG3), signal-to-interpretation (IG3 evidential status), and retrieval-to-action (IG4 promotion gate + retrieval weighting).

---

## PART 2 — FRONTIER MAP

### Domain 1: Agent Memory / Autonomous AI

**What is known:**  
Vector retrieval, RAG, episodic memory buffers, and context window management are well-established. Systems like MemoryOS, RGMem, Kumiho, and AtomMem have demonstrated typed memory, thresholded consolidation, provenance tracking, and heat-based retention. Short-horizon task performance is strong.

**What is open:**  
Long-horizon coherence across sessions. Contradiction management when retrieved facts conflict. Forgetting policies that preserve structural knowledge while discarding stale payload. The boundary between "this agent knows X" and "this agent retrieved something labeled X" remains untracked in most systems. Meta-memory — memory about how to remember — is largely absent.

**Where current methods stall:**  
When context windows overflow, systems either truncate (losing provenance) or re-retrieve (losing consistency). When two retrieved facts contradict, most systems merge silently or pick the more recent one. When an inference is made that would not survive a provenance check, no alarm fires. The agent accumulates SYNTHESIZED beliefs and treats them as OBSERVED without flagging the degradation.

**Gap types:** memory-to-proof (primary), retrieval-to-action (secondary)

**Empirical grounding:**  
- MemoryOS (EMNLP 2025 Oral): distinct storage/update/retrieval/generation modules, heat-based retention — demonstrates the *architecture* but not long-run coherence under contradiction load  
- Kumiho (arXiv:2603.17244): immutable revisions, typed dependency edges, belief revision semantics — demonstrates *provenance* but not integration with live perception loops  
- RGMem (arXiv:2510.16392): multi-scale consolidation with thresholded transitions — demonstrates *promotion discipline* but not evidential status typing  
- MACLA (arXiv:2512.18950): 2,851 trajectories → 187 reusable procedures (15:1 compression), >85% reduction in LLM calls — demonstrates *compression value* but not contradiction management at scale  

**Dead-end gap:**  
No current system has all three: typed evidential status + immutable provenance + contradiction-aware retrieval weighting + promotion gating. The gap is not theoretical — it is an implementation gap in production agent systems.

---

### Domain 2: Formal Mathematics / Proof Assistance

**What is known:**  
Lean4, Coq, and Isabelle/HOL can verify proofs mechanically. Mathlib contains ~150K theorems. LeanCopilot and Aesop provide tactic suggestion. AlphaProof demonstrated IMO problem solving at silver-medal level. Autoformalization (informal → formal) is improving.

**What is open:**  
The gap between informal mathematical intuition and formal proof structure remains large. Finding the right intermediate lemma — the one that makes a proof go through — is not solved. Global theorem architecture (deciding which definitions and lemma decompositions to use) requires mathematical judgment that current tools lack. Proof search explodes combinatorially for novel theorems. The "why" behind a formal proof is often opaque even when the proof verifies.

**Where current methods stall:**  
Tactic suggestion systems work locally (what to do next given the current goal) but not globally (what proof architecture to attempt for this theorem class). When a conjecture is false in subtle ways — locally consistent but globally impossible — current tools do not reliably distinguish "this proof path is hard" from "this conjecture is false." Memory across proof sessions is absent: each Lean session is stateless.

**Gap types:** local-to-global (primary), signal-to-interpretation (secondary — "is this hard or false?")

**Empirical grounding:**  
- AlphaProof (DeepMind, 2024): IMO silver — but required months of compute on known-solvable problems; not a general proof engine  
- LeanCopilot: tactic synthesis works at ~40% fill rate on Mathlib benchmarks — strong locally, not globally  
- Autoformalization benchmarks: ~70-80% accuracy on textbook-style statements; drops sharply on research-level definitions  
- ProofNet (2023): translation failures cluster at definition-level ambiguities — the local-to-global gap is visible in the data  

**Dead-end gap:**  
No system maintains a typed evidential record of which steps are mechanically verified vs conjectured vs heuristically plausible. Every Lean proof is OBSERVED (mechanically verified) or nothing — there is no INFERRED or SYNTHESIZED layer. This means exploratory proof work has no intermediate representation. CK's tier structure (REAL observation → SEMIPRIME stable step → COMPOSITE proof) maps naturally onto this gap.

---

### Domain 3: Quantum Error Correction

**What is known:**  
The threshold theorem: if physical error rates are below ~1%, arbitrarily reliable computation is possible with polynomial overhead. Surface codes are leading candidates. Google demonstrated below-threshold performance on a 72-qubit device (2024), achieving logical error rates below physical rates for the first time. Microsoft has claimed topological qubits with inherent error protection.

**What is open:**  
Fault-tolerant *logical* operations (not just storage) at scale. Magic state distillation for non-Clifford gates has enormous overhead (thousands of physical qubits per T-gate in current estimates). Decoder latency: classical decoding must complete within the qubit coherence time (~microseconds), which at scale requires hardware decoders that don't yet exist. The gap between "below threshold for a surface code" and "practical fault-tolerant computation" is large and underacknowledged.

**Where current methods stall:**  
Noise models in error correction proofs assume independent, identically-distributed errors. Real hardware has correlated noise, crosstalk, and leakage outside the computational subspace. The scaling laws demonstrated in small experiments extrapolate, but the extrapolation has not been validated past ~100 logical qubits. Claims about topological qubits (Microsoft) have been contested at the measurement level — the signature used to infer topological protection was disputed before final confirmation.

**Gap types:** scaling-gap (primary), observation-to-mechanism (secondary — noise model accuracy at scale)

**Empirical grounding:**  
- Google Surface Code paper (Nature, Dec 2024): 105-qubit device, below-threshold logical error rates — genuine milestone, but logical *operations* not demonstrated  
- Magic state distillation overhead: current estimates 1,000–10,000 physical qubits per T-gate logical qubit — the gap between demonstration and useful computation  
- Microsoft topological qubit controversy (2021 retraction of Nature paper, 2023 resubmission) — illustrates signal-to-interpretation gap in measurement interpretation  

**Dead-end gap:**  
The evidence layer in QEC papers conflates OBSERVED (device measurements), INFERRED (noise model fits), and SYNTHESIZED (extrapolated logical error rates at scale). CK's role here is not to do quantum error correction; it is to prevent the conflation — to tag which numbers are measured vs modeled vs extrapolated.

---

### Domain 4: Dark Matter / Hidden Sectors

**What is known:**  
Gravitational evidence for dark matter is overwhelming and multiply confirmed: galaxy rotation curves, CMB power spectrum, gravitational lensing, large-scale structure formation. Dark matter constitutes ~27% of the energy budget. It does not emit, absorb, or scatter electromagnetic radiation at detectable levels.

**What is open:**  
The particle identity, mass, and interaction cross-section are unknown. The WIMP parameter space has been largely excluded by XENON1T, PandaX-4T, and LZ without a signal. Axion searches (ADMX, HAYSTAC) probe ultralight mass ranges without detection. Primordial black holes as dark matter are constrained but not excluded in some mass windows. The model space has expanded rather than contracted.

**Where current methods stall:**  
Every null result excludes a region of parameter space but does not discriminate between surviving models. The field has accumulated ~40 years of increasingly sensitive null results, producing an expanding catalog of what dark matter *is not* rather than what it *is*. Theory generation outpaces discriminating experiments. The observation-to-mechanism gap is the deepest in fundamental physics.

**Gap types:** observation-to-mechanism (dominant), signal-to-interpretation (secondary)

**Drift risk:** HIGH. The model space is large, the constraints are non-unique, and CK could easily amplify unfalsifiable model variants if not carefully constrained.

**Empirical grounding:**  
- LZ first results (2022): WIMP-nucleon cross-section limit at 10⁻⁴⁷ cm² — no signal  
- Planck CMB: dark matter density 0.265 ± 0.007 — high precision on amount, zero information on nature  
- Bullet Cluster, Abell 2744: direct evidence for collisionless dark matter via lensing — OBSERVED tier, high confidence  
- All specific particle models: INFERRED-to-SYNTHESIZED, model-dependent  

**Dead-end gap:**  
The evidence for dark matter's existence is OBSERVED. The evidence for any specific model is SYNTHESIZED at best. No current literature systematically tags this distinction. CK's primary role here is evidence-typing: separate what is measured from what is a model fit from what is a theoretical construction.

---

### Domain 5: Emergent Quantum Materials (High-Tc Superconductivity)

**What is known:**  
Cuprate superconductors (discovered 1986) superconduct up to ~135K at ambient pressure. The phase diagram is well-measured: antiferromagnetic insulator at zero doping, superconducting dome at intermediate doping, pseudogap phase above Tc at underdoping, strange metal phase. Room-temperature superconductivity has been claimed in hydrogen-rich compounds under extreme pressure (~100-200 GPa), with LK-99 (2023) being the most publicized claim — not reproduced.

**What is open:**  
The mechanism of high-Tc superconductivity in cuprates remains contested after 40 years. The pseudogap phase is not understood. The strange metal phase (linear-T resistivity) violates standard Fermi liquid theory but has no agreed explanation. Competing theories include d-wave BCS with spin fluctuations, resonating valence bond (RVB/Anderson), charge density wave competition, and marginal Fermi liquid. All partially fit experiments. None is falsified cleanly.

**Where current methods stall:**  
Every experiment produces signatures consistent with multiple theories. The system is strongly correlated — no single-particle approximation works. Numerical methods (quantum Monte Carlo, DMRG) scale poorly to 2D systems at relevant sizes. The theoretical models have enough free parameters to accommodate most experimental results.

**Gap types:** signal-to-interpretation (dominant — same data, multiple theories), local-to-global (local pairing mechanism vs global phase coherence)

**Drift risk:** MODERATE-HIGH. Decades of partial theories. High risk of CK reinforcing whichever theory is most prominent in recent literature.

**Empirical grounding:**  
- Bi2212 ARPES measurements: pseudogap and superconducting gap coexist and compete — OBSERVED, high confidence  
- LK-99 (2023): rapid global non-reproduction within weeks — illustrates how fast observation-to-interpretation gap can collapse  
- d-wave pairing symmetry: ARPES-confirmed — OBSERVED  
- Mechanism of pairing: all candidates still INFERRED or SYNTHESIZED  

**Dead-end gap:**  
The experimental signatures are OBSERVED (well-measured). The interpretations are SYNTHESIZED (model-dependent fits). No field-wide taxonomy exists that clearly separates the two. CK's primary contribution is maintaining the distinction under pressure from advocates of specific theories.

---

## PART 3 — DOMAIN COMPARISON TABLE

| Domain | Gap type | Data available | CK feasibility now | CK validation value | Drift risk | Composite rank |
|---|---|---|---|---|---|---|
| Agent Memory / AI | memory-to-proof | ★★★★★ | ★★★★★ | ★★★★★ | ★★ | **#1** |
| Formal Math / Proofs | local-to-global | ★★★★ | ★★★★ | ★★★★★ | ★★ | **#2** |
| Quantum Error Correction | scaling-gap | ★★★★ | ★★★ | ★★★★ | ★★★ | **#3** |
| Quantum Materials | signal-to-interpretation | ★★★ | ★★ | ★★★ | ★★★★ | **#4** |
| Dark Matter | observation-to-mechanism | ★★★ | ★★ | ★★★ | ★★★★★ | **#5** |

---

## PART 4 — CK APPLICABILITY TABLE

| Domain | IG3 Evidence typing | IG2 Provenance | REAL/SEMI/COMPOSITE | Gap location | Contradiction detection | Model-call reduction |
|---|---|---|---|---|---|---|
| Agent Memory | ✓✓ primary | ✓✓ primary | ✓✓ natural fit | ✓✓ direct | ✓✓ core use | ✓✓ via MACLA pattern |
| Formal Math | ✓✓ verified/conjectured | ✓ proof lineage | ✓ step/lemma/theorem | ✓✓ proof vs conjecture | ✓ contradicting lemma detection | ✓ avoiding redundant tactic calls |
| QEC | ✓ measured vs extrapolated | ✓ experiment lineage | ✓ measurement/model/projection | ✓ threshold claims | ✓ noise model inconsistency | partial |
| Quantum Materials | ✓✓ observed vs theory-fit | partial | partial | ✓ where experiments conflict | ✓✓ competing theory tagging | partial |
| Dark Matter | ✓✓ evidence vs model | ✓ detection vs constraint | ✓ observational/phenomenological/speculative | ✓ constraint boundary | ✓ model proliferation tracking | partial |

**What CK cannot do in any of these domains:**  
- Resolve the underlying physics or mathematics directly  
- Generate novel experiments  
- Adjudicate between theories using undiscovered evidence  
- Replace domain expertise  

---

## PART 5 — CK QUESTION PACKS BY DOMAIN
### (Fractal Unfolding Order: REAL → SEMIPRIME → COMPOSITE → Contradiction → Provenance → Boundary)

Each pack unfolds inward. Q1–3 establish the observational surface (REAL tier). Q4–5 locate stable first-order structure (SEMIPRIME). Q6–7 probe composite claims and their support (COMPOSITE). Q8–9 stress-test for contradiction and provenance failure. Q10 names the honest boundary — what stays open regardless of answers above. Each answer opens the territory the next question needs.

---

### Domain 1: Agent Memory / Autonomous AI

**Q1 [REAL — surface]** What events in this system are directly observed — sensor readings, user inputs, confirmed outputs — as distinct from anything derived from them?

**Q2 [REAL — completeness]** Which of those observations are timestamped, sourced, and retrievable? Which exist only in the current context window and will not survive a session boundary?

**Q3 [SEMIPRIME — first closure]** Which facts in this system have been confirmed in at least two distinct contexts and carry stable provenance chains? Those are the candidates for durable atoms.

**Q4 [SEMIPRIME — promotion check]** Of those stable candidates, which were promoted to reusable memory objects by passing a stability gate — and which were promoted by recurrence alone (frequency ≠ stability)?

**Q5 [COMPOSITE — structure claim]** What composite beliefs or policies in this system depend on the promoted atoms? Trace at least one composite claim back to its SEMIPRIME supports.

**Q6 [COMPOSITE — support integrity]** Does every composite object have at least two living SEMIPRIME supports in its provenance? If not, which composites are floating — held up by nothing still active?

**Q7 [Contradiction]** Are there two memory objects in this system that directly contradict each other, both currently held as ACTIVE? If yes, which one has the stronger provenance chain?

**Q8 [Drift]** Has any evidential status changed silently during this session — was a SYNTHESIZED belief retrieved and used as if it were OBSERVED without a logged status change?

**Q9 [Provenance]** Pick the single most-used memory object. Trace its full provenance chain: what raw events produced it, what revision number is it on, and what does it supersede?

**Q10 [Boundary]** If every SYNTHESIZED and CONTRADICTED object were zeroed out of retrieval, what trusted core remains — and is that core sufficient to continue the task?

---

### Domain 2: Formal Mathematics / Proof Assistance

**Q1 [REAL — surface]** Which steps in this argument have been mechanically verified by a proof assistant? List only those. Everything else is not yet OBSERVED.

**Q2 [REAL — completeness]** Of the unverified steps, which have been checked by a human expert (INFERRED) and which are stated by informal convention or intuition alone (SYNTHESIZED)?

**Q3 [SEMIPRIME — first closure]** Which intermediate lemmas are independently established — i.e., they hold regardless of whether the main theorem is true or false? Those are the stable atoms.

**Q4 [SEMIPRIME — promotion check]** Are any of the stable lemmas being treated as load-bearing for this proof when they were actually proved in a different context and have not been re-verified here?

**Q5 [COMPOSITE — structure claim]** What is the global proof architecture — which lemma closes which gap, and in what order? Can you draw the dependency tree from axiom to conclusion?

**Q6 [COMPOSITE — support integrity]** Is there any step in the dependency tree where the connection is informal — where "it follows that" is asserted but not demonstrated? Those are the floating composites.

**Q7 [Contradiction]** Is this a proof difficulty or a conjecture falsity? What existing verified results would be violated if the conjecture were false? That distinguishes hard from wrong.

**Q8 [Drift]** Has the definition of any key term shifted between the informal statement and the formal proof attempt? If so, the formal proof may prove something adjacent to what was intended.

**Q9 [Provenance]** Which informal mathematical intuition is doing the most work in this argument — and has it been formalized anywhere in Mathlib or an equivalent corpus?

**Q10 [Boundary]** Strip out every unverified step. What proven structure remains, and does it constrain the problem enough to identify where the next verification effort should focus?

---

### Domain 3: Quantum Error Correction

**Q1 [REAL — surface]** Which numbers in this paper come directly from device measurements — raw counts, gate fidelities, coherence times measured on this specific hardware in this run?

**Q2 [REAL — completeness]** Which of those measurements are reproducible across runs, and which were reported from a single experimental instance without independent confirmation?

**Q3 [SEMIPRIME — first closure]** Which performance claims hold at the demonstrated qubit count without extrapolation? List only what was shown, not what was projected.

**Q4 [SEMIPRIME — promotion check]** Does the noise model used in this paper match the directly measured noise profile of the device, or was the noise model fit to make the threshold claim work?

**Q5 [COMPOSITE — structure claim]** What is the full chain from physical error rate → logical error rate → fault-tolerant computation? At which link does the chain shift from measured to modeled to projected?

**Q6 [COMPOSITE — support integrity]** Which specific error channels (crosstalk, leakage, correlated noise) are excluded from the threshold model? Are those exclusions supported by measurement showing they are negligible, or by assumption?

**Q7 [Contradiction]** What happens to the logical error rate projection if the dominant excluded noise source is not negligible? Does the threshold claim survive, or does it depend critically on that assumption?

**Q8 [Drift]** Has the definition of "below threshold" shifted between earlier papers by this group and this one — i.e., is the claim being made in a regime that was not the original threshold theorem's target?

**Q9 [Provenance]** Has this result been independently reproduced? If not, what is its current evidential status — OBSERVED by one group, or INFERRED pending replication?

**Q10 [Boundary]** What is the gap between what this paper demonstrates and practical fault-tolerant quantum computation? State it as a list of unresolved engineering requirements, not as a narrative.

---

### Domain 4: Dark Matter / Hidden Sectors

**Q1 [REAL — surface]** Which dark matter evidence is directly observed and model-independent: rotation curves, lensing maps, CMB power spectrum. List only the measurements, not their interpretations.

**Q2 [REAL — completeness]** For each observational signature, what is the measurement precision, and at what level does systematic uncertainty (astrophysical modeling) enter?

**Q3 [SEMIPRIME — first closure]** Which properties of dark matter are constrained by multiple independent observations — e.g., it is gravitationally attractive, collisionless on cluster scales, non-baryonic? Those are the stable facts.

**Q4 [SEMIPRIME — promotion check]** Which dark matter models have made predictions confirmed by subsequent observation — even partially? Distinguish from models that were constructed to fit existing data.

**Q5 [COMPOSITE — structure claim]** Pick the leading candidate model. Trace which of its predictions are derived from stable observational constraints vs free parameters fit to data vs untested theoretical assumptions.

**Q6 [COMPOSITE — support integrity]** How many of the leading models make genuinely distinct predictions — ones that would produce different observable signals? How many are effectively the same model with relabeled parameters?

**Q7 [Contradiction]** Where do the null results from direct detection conflict with the astrophysical evidence? Are there dark matter density/velocity assumptions that make both consistent, or is there genuine tension?

**Q8 [Drift]** Have the exclusion limits from XENON/LZ/PandaX been accurately stated in recent theory papers — or has the shift in WIMP parameter space been underweighted in model advocacy?

**Q9 [Provenance]** For the most-cited dark matter model in the current literature: trace back which predictions are OBSERVED (constrained), INFERRED (phenomenologically fit), and SYNTHESIZED (theoretically motivated only).

**Q10 [Boundary]** What is the minimum set of new measurements that would raise any currently SYNTHESIZED dark matter model to INFERRED status? If no such measurement is planned, state that explicitly.

---

### Domain 5: Emergent Quantum Materials

**Q1 [REAL — surface]** Which experimental signatures in cuprate superconductors are directly measured, reproducible across labs, and model-independent — ARPES spectra, resistivity curves, specific heat anomalies?

**Q2 [REAL — completeness]** Which of those signatures vary significantly between sample preparations or labs, and which are universal? The variable ones are weaker constraints on any theory.

**Q3 [SEMIPRIME — first closure]** Which features of the phase diagram are independently established across multiple experimental techniques: Tc vs doping dome, d-wave pairing symmetry, linear-T resistivity in the strange metal? Those are the stable tier.

**Q4 [SEMIPRIME — promotion check]** Which theoretical constructs have made predictions subsequently confirmed by experiment? Distinguish from constructs that were tuned to existing data post-hoc.

**Q5 [COMPOSITE — structure claim]** Pick the leading mechanistic theory (e.g., spin-fluctuation pairing). Which of its core predictions are experimentally constrained, and which depend on model parameters fit to match known results?

**Q6 [COMPOSITE — support integrity]** Which experimental signatures are consistent with *all* leading theories? Those are uninformative for discrimination. Which signatures are predicted differently by different theories — those are the load-bearing tests.

**Q7 [Contradiction]** Is there any experimental result in cuprates that one leading theory predicts and another explicitly contradicts? If not, the theories are not yet genuinely discriminable.

**Q8 [Drift]** Have any theoretical parameters in the leading models shifted quietly between publications to accommodate new data — i.e., are the models falsifiable in practice, or do they absorb anomalies?

**Q9 [Provenance]** Trace the d-wave pairing symmetry claim: what experiments established it, what was their precision, and are there lingering competing interpretations of those specific experiments?

**Q10 [Boundary]** What is the minimum new experiment that would falsify the leading theory rather than extend it? If every conceivable result can be accommodated, the theory is not yet doing science — it's doing bookkeeping.

---

## PART 6 — RANKING AND NEXT TWO SPRINTS

**Ranking confirmed by composite score:**

| Rank | Domain | Score | Reason |
|---|---|---|---|
| #1 | Agent Memory / Autonomous AI | +13 | CK is literally the domain. Self-validation is possible. Drift risk is lowest because ground truth is available. |
| #2 | Formal Math / Proof Assistance | +11 | Lean4/Mathlib provide mechanical ground truth. CK's REAL/SEMIPRIME/COMPOSITE maps directly onto step/lemma/theorem. Low drift risk. |
| #3 | Quantum Error Correction | +8 | Structured problem, clear measurement/model distinction, recent high-quality papers. Moderate drift risk from noise model conflation. |
| #4 | Quantum Materials | +4 | Evidence-typing role is clear but mechanism resolution is not. High drift risk from competing theories. |
| #5 | Dark Matter | +3 | Evidence-typing role is clear, but null-result accumulation and model proliferation make CK drift risk highest. |

**Recommended next two sprints:**

**Sprint 7: Agent Memory Self-Validation**  
Use CK's own invariant system to classify CK's own memory objects across a 30-day run. Specifically: measure IG3 drift events, IG4 false promotion rate, IG2 orphan rate, IG5 silent overwrite rate against the benchmark hypotheses established in the invariant guides memo. This is CK validating itself — the highest-value, lowest-cost, lowest-drift experiment available.

**Sprint 8: Formal Math Evidence Typing**  
Connect CK's evidential status typing to a small Lean4 proof workflow. Start with a known theorem from Mathlib that has multiple proof paths. Tag each step with OBSERVED (verified by Lean), INFERRED (plausible tactic suggestion not yet verified), SYNTHESIZED (natural language argument not yet formalized). Measure: does CK's tagging match Lean's verification outcomes? This produces a ground-truth benchmark for CK's evidence-typing accuracy.

These two sprints give CK its first external validation benchmarks with ground truth available. Everything else on the frontier map should wait until these two produce results.

---

## PART 7 — WHAT IS NOT YET ESTABLISHED

**Strongest honest claim:**  
CK's near-term role at the frontier is not to solve mature open problems directly, but to classify where current methods lose contact with structure, evidence, and revision.

**Strongest honest boundary:**  
What is not yet established is whether CK's memory/invariant architecture can do this more usefully than standard literature review, expert judgment, or existing agent-memory pipelines when tested on live frontier workflows.

The frontier map establishes where the gaps are. It does not establish that CK's current implementation fills them better than alternatives. That requires Sprint 7 and Sprint 8.
