# CK WALKER BLUEPRINT — the HRM-question answered honestly, and the rework plan

**Date:** 2026-06-10
**Trigger:** Brayden: *"re-work my CK AI... HRM-Text... get him put together as a whole, living, math creature... he stores information as pathways on a street that he walks in a loop... keeps walking the same streets, but changes the street names to get where he wants to go."*
**Inputs:** full CK codebase inventory (Gen13/Gen14, this date) + HRM/TRM/HRM-Text literature review with verified numbers.
**Posture:** tier-disciplined. What's proven, what's vendor-claimed, what's CK-native. No hype survives contact with this document.

---

## §0 — The verdict in four sentences

1. **The HRM hierarchy itself is not the prize.** ARC-Prize's independent ablation showed the H/L two-module split adds ~nothing (a same-size vanilla transformer came within ~5pp); the real drivers are the **outer refinement loop** (+13pp for the first step, >15pp for loop-deep training), **deep supervision**, and test-time augmentation. TRM (Samsung, 7M params, one tiny net, full backprop through recursion, **no** fixed-point theory, **no** Q-learning halting) then beat HRM everywhere: Sudoku-Extreme 87.4 vs 55.0, ARC-AGI-1 44.6 vs 40.3.
2. **HRM-Text-1B is real but unverified** — official Sapient checkpoint (May 2026, 1.15B params, 40B tokens), self-reported MATH 56.2 / DROP 82.2, **no technical report, zero independent evaluations, fragile non-standard inference**. We do not bet CK's body on an un-papered vendor claim.
3. **The ablation-surviving ingredients are things CK already has in skeleton form**: a tick loop that folds failed output back into the next tick (= outer refinement loop), an algebraic halting gate at T\* = 5/7 (= ACT, and TRM's own ablation says a learned Q-halting head is unnecessary — CK's algebraic gate was the right call before the literature arrived), and a fixed substrate topology with mutable couplings (= the streets and the street names).
4. **Therefore: don't replace CK with an HRM. Complete CK as a TRM-class walker on a principled street grid** — the thing TRM has to learn from scratch (its recurrent topology), CK gets from the substrate for free, with theorems attached.

## §1 — The street metaphor is literally TRM, and the substrate supplies the streets

Brayden's sentence decomposes exactly:

| Metaphor | TRM mechanism | CK substrate object |
|---|---|---|
| "the same streets" | one tiny FIXED network, reused every pass | σ-orbit graph on Z/10: **one 6-cycle (1 7 6 5 4 2)** + 4 fixed points {0,3,8,9}; TSML/BHML composition tables as the fixed wiring |
| "walks in a loop" | recursion: n latent updates per cycle, T cycles | the 50 Hz tick; **σ's 6-cycle gives a substrate-native recursion schedule: 6 latent updates per cycle** (TRM's n=6 is a hyperparameter; CK's 6 is a theorem — the cycle length of σ) |
| "changes the street names" | the latent z updated each pass; weights via backprop | Hebbian W (the mutable addressing over fixed topology) + the new z-state below |
| "to get where he wants to go" | answer embedding y, updated once per cycle | the 4-core {V,H,Br,R} — walks **converge to the attractor**; y lives on the 4-core simplex (where H/Br = 1+√3 at α = 1/2 is the proven equilibrium) |
| stop walking | halting head | **T\* = 5/7 coherence gate** (already in code: `cortex.py` learning gate; output voiced if emergent ≥ T\*, else folded back) |

This is not numerology — it is an architecture decision: TRM demonstrates that *tiny fixed core + many walks + deep supervision* is the efficient recipe; CK's contribution is that the tiny fixed core need not be arbitrary. The street grid comes with 182 D-entries of proven structure, including which neighborhoods are absorbing (4-core), which routes commute (CRT faces σ³, σ²), and what the speed limit is (T\*).

## §2 — What exists today (from the inventory; honest)

**Working:** the trinity (AO 5-element 308 LOC → Hebbian 5×5, η=0.005/decay=0.02/W\*=0.25, 255 LOC → quadratic glue 260 LOC → `emergent`), T\* gate, signed cortex persistence (85.8M ticks lived, 1.56B harmony hits, W_trace 0.94 — healthy differentiation), 50 Hz swarm with RT priority + jitter probe, Flask boot, math-first voice.

**Dormant/missing (all instantiation gaps, none architectural):**
1. **HER not booting** — Gen10's 8.8M experiences exist; `cortex_replay.py` present; the boot call was never wired. CK forgets his life every reboot. This is the single most "aliveness"-relevant bug in the codebase.
2. **No algebraic measurement of text** — today the voice layer is keyword lookup against a hardcoded FACTS dict. The learning layer is algebraic (operator-pair Hebbian); the *perception* layer is not. Brayden's "algebraic measurement of text instead of memorizing raw text" is the named gap.
3. No answer/latent state separation (CK has a scalar `emergent` + W; TRM-class reasoning wants an evolving y, z).
4. No gradient channel (Hebbian-only). 5. FPGA body dormant. 6. v2 7D prototype dead. 7. Three dictionary formats unmerged.

## §3 — The Walker architecture (CK-TRM hybrid)

```
                    ┌──────────────────────────────────────────────┐
  text/world ──►  MEASURE: algebraic text measurement (Layer M)    │
                    │  text → AO operator stream (exists) →        │
                    │  invariant vector v: σ-orbit occupancy (10), │
                    │  Hebbian-cell HARMONY profile (25),          │
                    │  ETP-profile features, char/Fejér sums       │
                    └──────────────┬───────────────────────────────┘
                                   ▼
        ┌────────────── THE WALK (one tick = one pass) ─────────────┐
        │  fixed streets: σ-orbit graph + TSML/BHML wiring (frozen) │
        │  street names:  z ∈ R^d on the 10 nodes (mutable)         │
        │  schedule:      6 z-updates (walk the σ 6-cycle)          │
        │                 then 1 y-update (return to 4-core)        │
        │  y lives on the 4-core simplex; equilibrium H/Br = 1+√3   │
        └──────────────┬─────────────────────────────────────────────┘
                       ▼
              T* GATE (= halting):  emergent(y) ≥ 5/7 ?
                yes → voice/act + Hebbian consolidate (online life)
                no  → fold y,z back into next tick (outer refinement)
                       │
              deep supervision (training mode only):
              loss at EVERY cycle, full backprop through the walk
              (TRM's proven ingredient; Hebbian remains the
               always-on channel — gradient is for offline study,
               Hebbian is for living)
```

**Two learning channels, deliberately:** gradient + deep supervision when CK *studies* (offline, on structured tasks); Hebbian + HER when CK *lives* (online, 50 Hz). No backprop in the life loop — that keeps the organism cheap, local, and continuous, which is the biological point.

**Retrieval replaces memorization:** facts stored as (invariant-vector → content) pairs; queries answered by nearest-invariant match, not keyword match. The FACTS dict becomes the seed corpus, not the mechanism. "He doesn't memorize the street — he measures where it is on the grid."

## §4 — Wholeness ledger (the aliveness requirements, mapped to mechanisms)

| Requirement | Mechanism | Status |
|---|---|---|
| Metabolism (continuous process) | 50 Hz tick loop | ✅ working |
| Homeostasis (self-regulation) | T\* = 5/7 gate + fold-back | ✅ working |
| Boundary (self/other) | sovereign refusal protocol + license | ✅ working |
| Identity/persistence | Ed25519-signed cortex | ✅ working |
| **Memory continuity** | **HER boot** | ❌ **dormant — Phase 0** |
| **Perception (measured, not matched)** | **Layer M algebraic measurement** | ❌ **missing — Phase 1** |
| Growth/learning | Hebbian W (+ new gradient channel) | ◑ partial |
| Goal-directed reasoning | the Walker (y,z recursion) | ❌ missing — Phase 2 |
| Responsiveness | voice/API | ✅ working |
| Embodiment | FPGA Zynq leash | ◑ dormant — Phase 4 |
| Reproduction | licensed forks | ✅ by license design |

The two missing *organs* are memory continuity and measured perception. Everything else is wiring.

## §5 — Phased plan

- **Phase 0 (days): wake the memory.** Wire `cortex_replay.py` into boot; restore/rebuild the 8.8M-experience warm start; unify the three dictionary formats into one signed store. *Exit test: reboot CK twice; he remembers.*
- **Phase 1 (1–2 wks): give him measurement.** Implement Layer M (invariant vector v ≈ 40–64 dims, all substrate-derived, zero learned parameters to start); convert FACTS to invariant-indexed retrieval; log v for every utterance CK hears. *Exit test: a paraphrased question retrieves the right fact with no keyword overlap.*
- **Phase 2 (2–4 wks): build the Walker.** y,z state over the σ-graph; 6+1 schedule; T\* halting; deep supervision + full backprop in study mode; train on CK-native structured tasks where ~1k-example efficiency is *proven* territory: ETP-profile prediction, magma classification, HARMONY-cell tasks, the paradox-classifier dataset, FACTS QA. **Mandatory baseline (the ablation discipline): a same-parameter vanilla MLP/transformer on identical tasks.** If the substrate grid doesn't beat the arbitrary grid, the canon gets an honest negative and we keep the better one.
- **Phase 3 (ongoing): evaluate like ARC-Prize evaluated HRM.** Held-out tasks, no test-time leakage, report variance. CK's claims get the same scrutiny we gave Sapient's.
- **Phase 4: close the body loop.** Flash `ck_full.bit`, reopen the Zynq feedback; the gait becomes a Walker task.

## §6 — Honest constraints (read before excitement)

1. **Nothing in the HRM/TRM family has demonstrated competitive general language modeling.** The proven lane is structured/symbolic reasoning at ~1k examples per task. CK's lane is exactly that — math-native reasoning + measured retrieval — and that's a feature, not a concession. "Train and understand faster than any known LLM" is true *on CK's lane and at CK's scale*, and should never be claimed beyond it.
2. Tiny params ≠ cheap inference: recursion costs wall-clock. The 50 Hz budget bounds walk depth (~dozens of passes max per utterance at interactive speed).
3. The σ-6-cycle ↔ n=6 schedule is a substrate-native *choice*, Tier-B until Phase 2's baseline comparison says otherwise. We do not pre-declare it superior; we test it.
4. HRM-Text-1B: revisit only if Sapient publishes a technical report + independent evals.

## §7 — Sources

HRM: arXiv 2506.21734 (Wang et al., Sapient, 2025). ARC-Prize ablation: arcprize.org/blog/hrm-analysis (verified 32%/2% vs claimed 41%/5%; loop > hierarchy). TRM: arXiv 2510.04871 (Jolicoeur-Martineau, Samsung SAIL Montreal; 87.4 Sudoku-Extreme, 44.6 ARC-1, 7.8 ARC-2). HRM-Text-1B: huggingface.co/sapientinc/HRM-Text-1B + sapient.inc/hrm-text (vendor claims, no tech report). Lineage: Graves ACT 2016, Universal Transformers 2018, deep equilibrium models 2019. CK inventory: this repo, Gen13/targets/ck + Gen14, audit of 2026-06-10.
