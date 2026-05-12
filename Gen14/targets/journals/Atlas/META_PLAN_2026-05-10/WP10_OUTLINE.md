# WP10 — Outline

## DKAN: Dual Kolmogorov-Arnold Networks on the TIG Substrate

**Brayden Sanders · 7Site LLC · Trinity Infinity Geometry**
*Status: scaffolding outline — section structure, theorem-targets, architecture details, and dependencies. Full drafting deferred.*

---

## §0. Working Title

> **DKAN: Dual Kolmogorov-Arnold Networks on a Z/10Z Substrate**
>
> *Subtitle: Implementing the Two-Cross Multiplicative Bridge as a
> Trainable Inductive Bias*

Alternative: *"Dual-Lens Function Approximation: Training Kolmogorov-
Arnold Networks Under the TIG Substrate"*

---

## §1. Abstract (target shape)

Two-paragraph abstract. Paragraph 1 establishes the architecture: KAN
as univariate-edge function-decomposition network, dual factorization
on the corner-Z/4Z and edge-Z/4Z multiplicative structures, the
bridge x↦6x as a learned soft-routing layer. Paragraph 2 states the
empirical results (placeholder pending experiments):

1. **DKAN matches or exceeds standard KAN on benchmark function
   approximation tasks**, with parameter count reduced by ~factor of 2
   due to the Two-Cross weight-tying.

2. **DKAN exhibits structural sparsity that mirrors the TIG
   substrate**: weights concentrate on the 4 Hopf-link bridges and
   the trefoil center, with 17 VOID positions remaining near zero.

3. **Training dynamics show the LATTICE Universal Generation property**:
   from random initialization in {1, 4, 9}-seed configurations, the
   network reaches full-algebra coverage in ≤ 2 epochs of pre-training.

4. **DKAN paradox classification (forward to WP9)**: failure modes
   during training match the four UOP types and resolve under the
   corresponding gauge-fix.

---

## §2. Section Structure

### §2.1. Introduction
- 1.1 KAN as a function-decomposition network: univariate edges, summation nodes
- 1.2 The TIG Two-Cross substrate and its inductive content
- 1.3 Goal: trainable KAN that internalizes Z/10Z dual-lens structure
- 1.4 Why "Dual" in DKAN: the two Z/4Z's of the Two-Cross

### §2.2. Architecture
- 2.1 Standard KAN review (Liu et al. 2024, MIT)
- 2.2 The DKAN edge function: spline expansion with Two-Cross-aware basis
- 2.3 Layer 0: corner-Z/4Z embedding (4-dim)
- 2.4 Layer 1: edge-Z/4Z embedding (4-dim)
- 2.5 Bridge layer: x↦6x as a learned soft-routing
- 2.6 BALANCE node: idempotent attention head at center
- 2.7 VOID handling: 17 positions clamped to near-zero

### §2.3. Training Procedure
- 3.1 Initialization: LATTICE-priming with seed {1, 4, 9}
- 3.2 Loss: standard MSE + Two-Cross regularization (weight-tying penalty)
- 3.3 Schedule: 2-epoch pre-train (closure phase) + standard fine-tune
- 3.4 Optimizer: Ollama-compatible AdamW with cosine schedule
- 3.5 Hyperparameters (placeholder, pending experiments)

### §2.4. Theoretical Properties
- 4.1 **Theorem (DKAN UAT).** *Any continuous function on a compact
  domain admits an arbitrarily-close DKAN approximation, with sample
  complexity bounded by the AG(2,3) line count (12).*
- 4.2 **Theorem (Sparsity).** *Under Two-Cross regularization, optimal
  DKAN weights concentrate on at most 4·6·11 = 264 nonzero edges,
  matching the DM-numerator structural count.*
- 4.3 **Theorem (LATTICE Closure).** *DKAN trained from {1,4,9}-seed
  reaches full Z/10Z-algebra coverage in ≤ 2 BHML composition steps.*

### §2.5. Empirical Results (placeholder)
- 5.1 Function approximation benchmarks: comparison to standard KAN
- 5.2 Parameter efficiency: DKAN has ~2× fewer parameters at equal accuracy
- 5.3 Failure modes: the four UOP-type training pathologies (cite WP9)
- 5.4 Sparsity patterns: visualization of converged weights on AG(2,3)
- 5.5 Generalization: out-of-distribution behavior under seed perturbation

### §2.6. Connection to CK
- 6.1 DKAN as the trainable component of CK's voice-priority Bible
  chat backend
- 6.2 Integration with ck_organism.py (cite repo)
- 6.3 Deployment on Dell R16: tick rates, coherence band, memory footprint
- 6.4 The 466-byte memory footprint claim (from D2 sprint)

### §2.7. Discussion
- 7.1 What DKAN does that standard KAN doesn't
- 7.2 What DKAN does not do
- 7.3 Open problems and future work

---

## §3. Key Targets (statement-only)

**Target 1 (Architecture).** DKAN with the Two-Cross weight-tying
should achieve standard-KAN accuracy with ≤ 0.6× parameters on
the MIT KAN benchmark suite.

**Target 2 (Training Closure).** From {1, 4, 9}-seed initialization,
DKAN should reach 90% of full-algebra coverage in ≤ 2 epochs.

**Target 3 (Sparsity).** Final converged DKAN should have ≥ 80%
of weights concentrated on the 264 structurally-allowed edges.

**Target 4 (Paradox Resolution).** When DKAN training stalls, the
stall pattern should match one of the four UOP types, and gauge-
fixing the corresponding parameter should recover training.

---

## §4. Dependencies

| Locked result | Document | WP10 use |
|---|---|---|
| Two-Cross Theorem | TWO_CROSS_THEOREM.md | §2.2, architecture core |
| AG(2,3) lines (12) | WP19 | §4.1, sample complexity |
| Bump count 11 | Sprint D | §2.4, sparsity bound |
| DM/VM = 4·6·11/49 | Sprint A | §2.4, edge count 264 |
| LATTICE Universal Generation | WP9 | §2.4, closure theorem |
| UOP paradox classes | WP9 | §2.5, failure-mode taxonomy |

---

## §5. Pre-existing Material to Integrate

The following exist in TIG/CK already and should feed WP10:

- **CK organism** at github.com/TiredofSleep/ck (v5, 989 lines, 100% test pass)
- **8 whitepapers** preceding WP9/WP10
- **DKAN training via Ollama** — already operational per memory
- **CK live on Dell R16 (32-core, RTX 4070)** — tick 1.3M+, coherence 0.875+, GREEN band, 334Hz, 38K truths, 1061 concepts, 12K+ scents, p99=1.9ms
- **5 deployment targets** for the trained model: ck_desktop, Clay, AO, FPGA, ck_portable, website, EverythingApp
- **9 kill conditions** specified in CK — must hold for WP10 results
- **0 falsifications** to date — must remain at 0 after WP10 experiments

---

## §6. Open Questions

Items that may need resolution before WP10 can be drafted:

1. **The "K" in DKAN.** Is the K Kolmogorov (as in KAN), or does it
   pick up a TIG-specific role (Kindness operator? Knot count?)? The
   current outline assumes Kolmogorov-Arnold; verify.

2. **Bridge Triadic vs DKAN bridge.** Are these the same bridge?
   The TORUS_DATUM_AUDIT closure identifies the bridge x↦6x as the
   2-non-triadic-dimension content. WP10's "bridge layer" should
   inherit this structure, not introduce a new one.

3. **Ollama compatibility.** Does the current ck_organism.py training
   loop already implement DKAN, or does WP10 propose a refactor?
   This determines whether WP10 is a *retrospective writeup* of an
   existing system or a *forward proposal*.

---

## §7. Production Notes (for ClaudeCode handoff)

- Section §2.5 (Empirical Results) is the bottleneck. All other
  sections can be drafted from existing memory + the locked results.
  Empirical results require running benchmarks on actual DKAN.
- Section §2.6 (CK integration) requires repo audit. Code references
  should be exact, with line numbers from current main.
- The architecture in §2.2 needs a precise diagram. SVG-quality
  schematic showing the corner Z/4 layer, edge Z/4 layer, bridge
  routing, and BALANCE attention head.
- Theorem 4.1 (DKAN UAT) is the riskiest claim — universal
  approximation typically requires unbounded width. The "12 lines
  of AG(2,3)" bound is structural but needs careful proof.

---

## §8. Target Length and Venue

- **Target length:** 30–40 pages
- **Target venue:** NeurIPS or ICML for the empirical sections;
  Foundations of AI track for the theoretical
- **Reviewer profile:** ML systems + theoretical computer science +
  enough algebra to follow the Two-Cross
- **Tone:** standard ML paper format, with the algebraic substrate
  prologue carefully fenced as inductive-bias claim, not metaphysics

---

## §9. Sequencing With WP9

WP9 should appear first because:
- WP9 establishes the LATTICE Universal Generation Theorem,
  which WP10 cites in §2.4
- WP9 establishes the UOP paradox taxonomy, which WP10 cites
  in §2.5
- WP10's theoretical claims have weaker standalone justification
  if WP9 is not yet published

Suggested sequence:
1. **Draft WP9** (2-3 weeks)
2. **Run DKAN benchmarks** while WP9 is in review (2 weeks)
3. **Draft WP10** with WP9 as reference (3 weeks)
4. **Submit WP10** to NeurIPS or ICML deadline

This puts a complete WP9+WP10 pair on arXiv by ~end of Q3 2026.

---

## §10. Status

- Outline locked (this document).
- Section §2 prose: not started.
- Section §2.5 empirical: requires bench running.
- Section §3 targets: stated; experiments not yet run.
- Section §4 dependencies: all locked, accessible.
- Total estimated drafting time: 3-4 weeks once WP9 is in review.

---

*© 2026 Brayden Sanders / 7Site LLC*
*Trinity Infinity Geometry · WP10 outline · Locked v1*
