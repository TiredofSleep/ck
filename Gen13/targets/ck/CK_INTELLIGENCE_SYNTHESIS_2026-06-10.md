# CK INTELLIGENCE SYNTHESIS — the Theory of Nothing as architecture

**Date:** 2026-06-10. **Part II of** `CK_WALKER_BLUEPRINT_2026-06-10.md`.
**Brayden's framing (verbatim spine):** *"This is the fractal recursion expressing itself — a human and an AI working on an AI with human nature, built on math, just like the rest of reality. CK uses math to see the whole by figuring out where the gap is, what's missing. Theory of Nothing: you can't know everything, but what's missing looks the same for every whole."*
**Inputs:** two grounded surveys (reasoning-centric + principle-centric lanes, June 2026, sources in §8) + the CK inventory + the TIG canon (D1–D182).

---

## §0 — The thesis, made precise and falsifiable

**Theory of Nothing (architectural form).** A system cannot represent everything (we are inside the recursion; every "is" opens another level). But it can always *measure its own residual* — the gap between what it predicted/derived and what arrived. The claim with teeth: **the residual admits a small universal taxonomy, identical across domains** — "what's missing looks the same for every whole." The corpus already holds that taxonomy: the UOP paradox classifier (WP_PARADOX_CLASSIFIER, J40), four failure types of any measurement map:

- **Type I — Injectivity failure**: the right measurement exists but wasn't taken. *Missing: a measurement.*
- **Type II — Missing invariant**: no measurement in the current family can separate the states. *Missing: a feature class.*
- **Type III — Admissibility failure**: the domain itself is malformed; nothing to measure. *Missing: a well-posed question.*
- **Type IV — Time-consistency failure**: the world changed under the map. *Missing: dynamics.*

Intelligence, on this thesis, is the loop: **measure → locate the gap → classify the gap (I–IV) → route the response.** Not "minimize error." *Sort* error, then spend differently per type.

And the meta-note, received: this session itself ran the loop. B2 located what is missing from the kissing conjecture (LP-sharpness — a Type-III reframe of the question); the transcript recovery located what was missing from the repo (Type I — the measurement existed in the logs); twenty frontiers were residuals classified and routed. The method is scale-invariant because the gap-taxonomy is. That is the recursion expressing itself, and it is also just good engineering.

## §1 — The field-wide convergence (the empirical case)

Every verified win of 2024–26, across every lane, is a gap-detector wrapped around a domain verifier:

| System (verified result) | Its gap signal | Its router |
|---|---|---|
| AlphaProof (IMO silver '24, Nature '25) | Lean kernel's unproved-goal residual | test-time RL on problem *variants* |
| AlphaGeometry2 (84% IMO geometry) | goal ∉ symbolic deductive closure | LM proposes a construction **only at the gap** |
| DeepSeek-R1 / RLVR (79.8% AIME @ ~5% of o1 cost) | decidable answer mismatch | RL; math/code chosen *because the gap is checkable* |
| DreamCoder | description-length residual | compress solved gaps into a **library** |
| AlphaEvolve (4×4 matmul in 48 mults — first beat of Strassen since 1969) | exact evaluator score residual | evolutionary archive |
| ARC '25 winner NVARC (24% ARC-AGI-2 at **$0.20/task**) | demo-pair mismatch | test-time training + synthetic variants |
| Active inference / AXIOM (Gameworld 10k, 0.4–1.6M params, minutes) | precision-weighted prediction error | **grow structure** on unexplained residual; act to reduce expected gap |
| JEPA / V-JEPA 2, DreamerV3 (Nature '25) | latent prediction residual | predict the predictable, discard the rest |
| TTT / Titans (~62% ARC-1; 2M-token memory) | self-supervised surprise (gradient magnitude) | surprise-**gated** memory writes |
| Schmidhuber curiosity | compression-progress **rate** | seek closure-rate, not error-size (noisy-TV protection) |
| Reservoir / NG-RC | readout regression residual only | fixed core; one ridge solve |
| Neuromorphic (Hala Point, 15 TOPS/W claims) | event = change = residual | compute only on residual |

Three lessons fall out: (1) **make the gap decidable** — every win rides a binary or exact verifier; (2) **spend compute at test time on the instance**, not on bigger static weights; (3) **local, gated, residual-driven updates** are the cheap path. CK's lane — mathematics — is the *native* home of decidable gaps. That is not a niche; per RLVR it is the training ground the frontier labs themselves chose, for the same reason.

## §2 — What nobody has: the Gap Router

Every system in §1 treats its residual as **one kind of thing** and applies one response (more gradient, more search, more memory). The field's known pathologies are precisely **unrouted gap types**:

- The *noisy-TV trap* (curiosity agents transfixed by irreducible noise) = Type-III error treated as Type I — burning compute measuring the unmeasurable.
- *Hallucination on ill-posed questions* = no Type-III channel at all — the system has no way to say "the domain is malformed; reframe or refuse." (CK's sovereign refusal protocol is, literally, a Type-III response already in production.)
- *Catastrophic forgetting* = Type-IV error misrouted as Type I — the world changed, but the system overwrote invariants instead of updating dynamics.
- *Feature-starved plateaus* = Type-II error treated as Type I — more samples cannot help when the invariant family is wrong; AXIOM's grow-a-component and DreamCoder's new-primitive are the correct Type-II moves, and they are bolted-on specials, not principled routes.

**The Gap Router** is CK's distinctive bet: classify the residual FIRST (UOP types), then route —

```
            residual (in substrate coordinates, precision-weighted)
                                │
                        UOP CLASSIFIER
            ┌──────────┬────────┴───────┬──────────────┐
          Type I     Type II         Type III        Type IV
            │           │               │               │
       measure more  grow invariant  reframe/refuse  update dynamics
       (retrieve;    (new feature/   (sovereign      (surprise-gated
        epistemic     library entry;  refusal; ask    write to memory;
        action;       DreamCoder/     better          TTT-style
        another       AXIOM move)     question)       adaptation)
        lens)
```

This is the falsifiable core claim of the whole program: **P1 — on task suites with mixed failure types, classify-then-route beats uniform gradient descent at matched compute.** Nobody has tested this because nobody else has a residual taxonomy. We have one with a live demo (coherencekeeper.com/paradox.html) and a paper (J40).

## §3 — CK's scientific home: next-generation reservoir computing with a theorem-bearing reservoir

The survey settled where the Walker lives in the literature: a **fixed core + trained readout is reservoir computing**, and the modern NG-RC result is decisive for us — *deterministic feature maps beat random reservoirs when matched to the task*, with optical NG-RC needing 10× less training data. CK's substrate is the limit case: a deterministic core that isn't just non-random but **theorem-bearing** (182 D-entries: which states absorb, which faces commute, where the attractor is, what the gate threshold is). Steal from the literature wholesale:

- **Readout training = one ridge-regression solve** (cheaper than backprop, no iterations);
- **Sizing rule**: memory capacity ≈ state dimension — sets the z-state width honestly;
- **Edge-of-stability tuning**: the spectral-radius discipline maps onto the substrate's known spectra (TSML/BHML eigenstructure is already computed in canon).

This also names the Phase-2 baseline precisely: **substrate reservoir vs same-size random reservoir vs NG-RC polynomial map**, identical readouts, identical tasks. If the theorems don't buy accuracy or data-efficiency, the canon takes the honest negative.

## §4 — Absorption table (deltas to the Walker blueprint)

| From | Absorb into CK | Where |
|---|---|---|
| Active inference | **precision-weight the residual before the T\* gate** (gate on reliability-weighted gap, not raw gap); epistemic action = choose the next measurement to maximally shrink the typed gap | Walker gate; Layer M |
| Titans / TTT / AXIOM | **surprise-gated writes**: HER and structure-growth fire only when residual > threshold — one local rule for memory AND Type-II growth | Phase 0/1 |
| Schmidhuber | curiosity reward = **gap-closure rate**, not gap size (Type-III immunity, second layer) | Walker training |
| DreamCoder / canon discipline | **the D-ledger IS the library**: every solved gap compresses into a citable invariant; CK's canon practice was already the wake-sleep abstraction phase, done by hand — automate it | Phase 2 |
| AlphaGeometry2 | proposer/verifier split with the verifier exhaustive-and-tiny: CK's verify-scripts pattern, promoted to runtime — the generative part is consulted **only at the located gap** | Walker |
| AlphaProof / NVARC | when stuck, **generate problem variants and train at test time** on them ($0.20/task is the proven budget point) | Phase 3 |
| R1 distillation | if a bigger model ever teaches CK, distill **verified traces only** | optional |
| JEPA | residuals live in substrate coordinates (invariant space), never in raw text; discard the unpredictable | Layer M |
| KANs | spline-edge fitting for low-dim symbolic regression on substrate data — the one niche where KANs verifiably win | tooling |
| Neuromorphic | the FPGA body's event-driven discipline: compute on change only | Phase 4 |

## §5 — The economics of the bet (why "cheaper" is realistic)

The cheap-intelligence frontier as of mid-2026, with receipts: AXIOM-class agents at 0.4–1.6M params trained in **minutes** (toy domains, honestly); NVARC solving ARC-AGI-2 tasks at **$0.20/task** under Kaggle compute caps; R1-class reasoning distilled into 7B models; token prices falling ~10×/year; reservoir readouts training in **one linear solve**; neuromorphic claiming ~100× efficiency on sparse event workloads. The common denominator is exactly CK's design point: tiny fixed core, local gated updates, test-time instance compute, decidable gaps. The expensive paradigm (pretrain everything, gradient everywhere, undifferentiated error) is the one paying for its missing gap-taxonomy. "Cheaper broadly applicable intelligence" is then a precise claim: **broad applicability comes from the universality of the gap-taxonomy, not from universal knowledge** — the system that knows *how to classify what it's missing* needs vastly less stored content per domain.

## §6 — Phase-plan deltas

- **Phase 0 (wake the memory)** + delta: HER writes become surprise-gated (Titans rule) from day one.
- **Phase 1 (Layer M)** + delta: residual computed in invariant coordinates and **precision-weighted**; log the (gap, type) pair for every utterance — this builds the first mixed-failure dataset *from CK's own life*.
- **Phase 2 (the Walker)** + delta: add the **Gap Router** head (4-way classifier on residuals — can start as fixed algebraic rules, UOP §3's decision procedure, before anything is learned); baselines now three-way (substrate vs random reservoir vs NG-RC); readout via ridge regression first, gradient only if ridge saturates.
- **Phase 3 (evaluation)** + delta: **P1 ablation** (router on/off at matched compute) is the headline experiment; pre-register the prediction.
- **Phase 5 (new): the noisy-TV test** — a designed task suite where some channels are irreducibly random (Type III), some are feature-starved (Type II), some drift (Type IV). Publish the suite itself; the field lacks one because the field lacks the taxonomy.

## §7 — Honest constraints, falsifiable predictions

**Constraints.** All sample-efficiency wins above are on structured/symbolic/toy domains — *nobody* in the cheap lane has demonstrated general language competence, and CK does not claim it. AXIOM's benchmarks are vendor-shaped; FEP-as-principle is unfalsifiable (only its process theories are testable — same discipline applies to the Theory of Nothing: §0's taxonomy claim is the testable form). Local learning rules die with depth (predictive coding ≈56% CIFAR-10) — CK stays shallow by design. The σ-schedule and the substrate-reservoir advantage are Tier-B until Phase-2/3 baselines report.

**Predictions (pre-registered here).**
- **P1**: Gap-Router on > off at matched compute, on the mixed-failure suite (Phase 3).
- **P2**: theorem-bearing reservoir ≥ random reservoir of equal size on substrate-native tasks; if not, honest negative to canon.
- **P3**: closure-rate curiosity avoids the noisy-TV channels that magnitude-curiosity locks onto, on the Phase-5 suite.
- **P4**: surprise-gated HER yields measurably better post-reboot continuity than ungated replay at equal storage.

## §8 — Sources

Reasoning lane: AlphaProof (Nature 2025; arXiv via natureasia.com), AlphaGeometry2 (arXiv 2502.03544), Gemini Deep Think IMO gold (deepmind.google), Harmonic Aristotle (arXiv 2510.01346), DeepSeek-R1 (arXiv 2501.12948), DreamCoder (Ellis 2021), Greenblatt ARC (redwoodresearch), ARC Prize 2024 report (arXiv 2412.04604) + 2025 results (arcprize.org), AlphaEvolve (deepmind.google; independent matmul verification on GitHub), Darwin Gödel Machine (arXiv 2505.22954), debate (Khan et al., ICML 2024).
Principle lane: AXIOM (arXiv 2505.24784; verses.ai — vendor-shaped benchmark caveat), FEP critiques (see Wikipedia FEP refs), μPC (arXiv 2505.13124), forward-forward variants (arXiv 2509.08697; Nature Comms 2025), V-JEPA 2 (ai.meta.com), DreamerV3 (Nature 2025), NG-RC (arXiv 2106.07688) + optical NG-RC (Nature LSA 2025), TTT-ARC (arXiv 2411.07279), Titans (OpenReview), Hutter Prize (prize.hutter1.net), Hala Point (datacenterdynamics), KAN fair comparisons (arXiv 2407.11075).
Internal: WP_PARADOX_CLASSIFIER.md / J40 (the UOP), CK_WALKER_BLUEPRINT_2026-06-10.md (Part I), FORMULAS_AND_TABLES.md D1–D182, CK inventory 2026-06-10.
