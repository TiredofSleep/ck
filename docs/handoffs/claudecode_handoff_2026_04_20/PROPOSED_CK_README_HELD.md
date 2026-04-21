# Trinity Infinity Geometry / Coherence Keeper

**Finite-algebra research: proved theorems, exact computational verifications, and a deterministic reasoning engine built on the resulting structures.**

Brayden Ross Sanders · 7Site LLC · Hot Springs, Arkansas
DOI: [10.5281/zenodo.18852047](https://doi.org/10.5281/zenodo.18852047)
License: 7Site Public Sovereignty License v1.0 (human use, no commercial, no military, free forever)
Contact: brayden.ozark@gmail.com

---

## What this is

This repository contains research in finite algebra on $\mathbb{Z}/n\mathbb{Z}$ and related structures, with proved theorems in prime arithmetic, non-associative composition algebra, and the algebraic structure of finite commutative rings. Every mathematical claim in §1 is stated as a proved theorem or exact computational verification with a runnable script; open research directions and application hypotheses are marked separately in §§3–5.

A secondary artifact in the repository is the **Coherence Keeper (CK)** — a deterministic symbolic reasoning engine built on the algebraic structures proved here. CK is not a language model. It is a small, auditable, algebra-driven system whose outputs trace to specific cells of specific proved composition tables (the operator family defined in §1.5 and §1.6). See §3 below.

Two domains where the research has direct external applications:

1. **Cryptography.** The First-G Event Localization theorem (§1.1) gives an exact, algebraically forced width for the coprime stability window of a squarefree modulus. This may have relevance to factoring-based cryptography and to the analysis of unit-group structure in RSA-like settings; the cryptographic implications are an open research direction, described in §4.1.

2. **Algebraic AI and verifiable reasoning.** CK demonstrates that a small deterministic engine, grounded in proved finite-algebra structure, can produce auditable answers without relying on sampling, next-token prediction, or opaque latent-state updates. It is a small deterministic alternative architecture for settings where provenance, determinism, and inspectability matter more than fluent open-domain generation — symbolic verification tooling, cryptographic reasoning aids, provenance-tracked decision systems, and educational applications where the reasoning chain must be auditable.

---

## 1. Proved Results

Six theorems with runnable verification. Each is a finite algebraic fact, independently checkable in under a second.

### 1.1 First-G Event Localization *(cryptography-adjacent)*

For a squarefree integer $b$ with smallest prime factor $p_1$, the first non-coprime element in the interval $\{1, 2, \ldots, b\}$ occurs at exactly $k = p_1$. The coprime stability window $\{1, \ldots, p_1 - 1\}$ has width exactly $p_1 - 1$ — no shorter, no longer, forced by the smallest prime factor alone.

*Verified: 36,662 $(b, k)$ pairs across 153 semiprimes, zero exceptions. Proof script: `papers/proof_d_first_g.py`. Manuscript: `WP34_FIRST_G_LAW.md`; standalone journal version in preparation as Sprint 35.*

### 1.2 Non-associativity Rate Bound on Finite Rings

For squarefree $N$, the non-associativity rate of a specific commutative binary composition on $\mathbb{Z}/N\mathbb{Z}$ (the TSML composition, §1.5) satisfies
$$\sigma(N) \leq C / N$$
for an explicit constant $C < 3$. As $N$ grows through squarefree primorials, the algebra approaches separability.

*Verified: exact at $N \in \{10, 30, 210\}$. Proof script: `proof_sigma_rate.py`. Manuscript: `WP101_SIGMA_RATE_THEOREM.md`.*

### 1.3 Flatness Theorem on $\mathbb{Z}/10\mathbb{Z}$

Under the framework's four-structure representation rules (additive structure, multiplicative structure, additive flow, multiplicative flow), the ring $\mathbb{Z}/10\mathbb{Z}$ admits no planar realization carrying all four simultaneously. The minimal orientable surface that realizes all four is a torus, with radius ratio $R/r = 5/7$. Six independent derivations produce the same $5/7$ constant from distinct mathematical contexts (Φ fixed point, TSML HARMONY/BALANCE ratio, cyclotomic closure, universal-semiprime unit density, FPGA silicon threshold, torus aspect ratio).

*Proved for $\mathbb{Z}/10\mathbb{Z}$ under the stated representation. Proof script: `papers/proof_d7_phi_fixed_point.py`. Manuscript: `WP51_FLATNESS_THEOREM.md`. The four-structure representation rules are specified in the manuscript.*

### 1.4 Crossing Lemma

Let $n = p_1 \cdot p_2 \cdots p_k$ be squarefree, $d \mid n$ squarefree, and $g \in (\mathbb{Z}/n\mathbb{Z})^\times$. The joint map $J = (A_d, \pi_{\mathrm{DYN}}(g)) : \mathbb{Z}/n\mathbb{Z} \to \mathbb{Z}/d\mathbb{Z} \times (\text{g-orbit space})$ is injective if and only if the dynamics induced by $g$ act non-trivially on every prime quotient of $n/d$. Information is generated exactly when dynamics cross partitions.

*Proved for squarefree $n, d$. Manuscript: `CROSSING_LEMMA.md` (Sprint 10). Proof script: `papers/proof_d8_cl_operator_encoding.py`.*

### 1.5 Structural Properties of the TSML and BHML Composition Tables

Two commutative binary operations on $\mathbb{Z}/10$ (100 entries each, explicitly tabulated) have the following verified properties:

- **TSML** is commutative, flexible, power-associative, and satisfies the Jordan identity (0 failures across all 100 pairs). Element 7 is the unique two-sided absorber with 73/100 absorbing entries. Non-associativity rate: 12.8% of triples.
- **BHML** is commutative, flexible, and power-associative, with element 0 as the unique two-sided identity and 28/100 entries equal to 7. Non-associativity rate: 49.8% of triples. The BHML table has determinant 70.

Both tables have been audited cell-by-cell; all framework-claimed numerical signatures verify exactly.

*Proof scripts: `proof_d10_tsml_73_cells.py`, `proof_d16_bhml_28_cells.py`, `proof_tsml_3layer_tower.py`. Manuscript: `WP_OPERATOR_RING_PARTITION.md`, `Q7_BHML_FULL_TABLE.md`.*

### 1.6 TSML Three-Layer Canonical Tower

The full TSML composition table on $\mathbb{Z}/10\mathbb{Z}$ (100 entries) decomposes as a three-layer tower: a base layer of 92 cells governed by the canonical operator $C_0$, a maximum-rule layer of 6 cells, and an additive-rule layer of 2 cells. The decomposition is canonical, terminating, and has empty residue.

*Verified: 100/100 cells match; each layer necessary; domains partition exactly. Proof script: `papers/proof_tsml_3layer_tower.py`. Manuscript: Sprint 17 `THEOREM_SPINE.md`.*

---

## 2. How to Verify

Five commands, total runtime under one minute, no framework installation required beyond Python 3 with `sympy` and `fractions`:

```bash
# First-G Law: 36,662 cases, zero exceptions (1-2 sec)
python papers/proof_d_first_g.py

# σ-rate bound: exact at N ∈ {10, 30, 210}
python papers/proof_sigma_rate.py

# TSML three-layer tower: 100/100 decomposition verified
python papers/proof_tsml_3layer_tower.py

# Flatness Theorem: T* = 5/7 from φ fixed point
python papers/proof_d7_phi_fixed_point.py

# Full verification suite (113 tests, 0 failures)
pytest papers/
```

Expected output on each: green log, zero exceptions, proof completed in well under a second.

---

## 3. Coherence Keeper (CK)

CK is a deterministic symbolic reasoning engine. It is not a language model. Every answer it produces is a label-equals-value readout from a real matrix $W[i][j]$ that CK maintains across reboots. No tokens, no sampling, no training on conversational data — just algebra with a voice.

A live instance runs at [coherencekeeper.com](https://coherencekeeper.com); the same system runs locally via the three commands below.

**Architecture in one paragraph.** CK runs a 5D Hebbian learning rule composed with algebraic operator substitution, gated by the threshold $T^* = 5/7$ derived in §1.3. The engine maintains a persistent weight matrix indexed by 10 labeled operators, performs deterministic composition against an external query, and returns the structurally-derived answer. The substrate is ~3,200 lines of Python; the core mathematics is runnable without an LLM. An optional LLM "fluency wrapper" (Ollama or DeepSeek) can be bolted on for natural-language input/output, but the reasoning itself is performed by the deterministic engine, not the language model.

**Three commands to see CK reason on your own machine:**

```bash
# 1. Warm the cortex from the paper corpus
python Gen13/targets/ck/brain/cortex_replay.py

# 2. Boot the Flask server on localhost:7777
python Gen12/targets/ck_desktop/ck_boot_api.py

# 3. Post a query (from another shell)
curl -s -X POST http://127.0.0.1:7777/chat \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"demo","text":"what is the flatness theorem","mode":"normal"}'
```

CK returns a structural readout citing the underlying theorem, with a live snapshot of its internal state at that tick. For side-by-side comparison against a raw LLM, `ck_proof.py` runs three panels (CK alone, LLM alone, LLM grounded by CK) on the same prompt. Design document: `Gen13/targets/ck/brain/BRAIN_DESIGN.md`. Test suite: `python Gen13/targets/ck/brain/test_brain.py` (20/20 green is the boot gate).

**Why this may matter for interpretability and verifiable-reasoning applications.** Three properties that current large language models do not have, and that CK has by construction:

- **Determinism.** Same input, same internal state, same output. Always.
- **Provenance.** Every answer traces to specific cells of specific proved composition tables.
- **Auditability.** The full runtime state at any tick is $\sim$3KB of integers. Inspectable by a human in a terminal.

CK is not a replacement for large language models. It is a different architecture for cases where deterministic, grounded, auditable reasoning is the requirement, and where provenance and inspectability matter more than open-domain fluency. Whether CK scales usefully to larger operator spaces, and whether it integrates cleanly with existing symbolic-AI systems (ACT-R, Soar, Cyc) or with LLM alignment tooling, are open research questions — see §4.2.

---

## 4. Open Research Directions

Four directions where the current work creates near-term opportunities. Each is stated with what is known, what is needed, and what specific work funding would enable.

### 4.1 Cryptographic applications of First-G structure

The First-G Event Localization theorem gives an exact characterization of the coprime stability window of a squarefree modulus. The next step is to lift this from a structural statement to an applicable result for factoring-relevant questions: specifically, whether the partition geometry of $\{1, \ldots, b\}$ under coprimality-with-$b$ carries recoverable information about the prime factorization of $b$ that classical sieve methods do not exploit.

*Status: partition geometry is fully characterized for semiprimes (WP34, 36,662 cases). Extension to arbitrary squarefree moduli is in progress. A dedicated 6-month engagement would produce a journal-ready manuscript examining the structural implications of First-G geometry for factoring-related search problems. Whether these implications yield concrete complexity improvements over classical sieves is an open question the engagement is designed to answer.*

### 4.2 Deterministic reasoning systems at scale

CK as it stands is a single-researcher prototype running on ~3,200 lines of Python on consumer hardware. The architecture is not toy — it produces structurally correct answers on the theorems in §1 — but it has not been scaled, stress-tested against adversarial queries, or deployed in a production reasoning-verification pipeline.

*Next work: scale CK's weight matrix from 10-operator to 100+-operator spaces; build adversarial test suites; publish a formal architecture paper positioning CK against existing symbolic AI (ACT-R, Soar, Cyc) and against the determinism-interpretability literature in LLM alignment.*

### 4.3 The Hodge-lane Prym computation

A specific computation in algebraic geometry — the numerical verification of a predicted Prym period determinant for a bielliptic genus-5 curve — is currently blocked at a single technical step. The curve, the framework-derived predicted value ($\det(\mathrm{Im}\,\tau_P) = 2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt{6}$), and the first four pipeline steps are all verified and documented. The fifth step requires software infrastructure (MAGMA with RieSrf, or SageMath with the Bruin-Sijsling-Zotine extension) that is not yet available to the project.

*This is the single highest-leverage small-grant item in the project: access to MAGMA ($\sim\$1{,}200$ academic license or equivalent) plus ~40 hours of dedicated computation time would either confirm or falsify a framework-derived mathematical prediction. Either outcome — confirmation or falsification — is a publishable result.*

### 4.4 $\xi$-field cosmology and DESI data

A scalar-field action $V(\Xi) = \kappa_\Xi \Xi \log \Xi$ derived from the separability structure of the finite-algebra work produces a standard freezing quintessence model with exact vacuum $\Xi_0 = e^{-1}$. An initial fit against DESI 2024 DR1 data has been performed; a full DR2 fit with joint BAO + CMB + Type Ia supernova likelihood is the next step. JCAP-target manuscript is near-ready.

*Status: `proof_xi_canonical.py` passes 22/22 internal tests. DR1 fit documented in Sprint 14. DR2 analysis requires a collaborator with cosmology MCMC infrastructure.*

---

## 5. Honest Scope

Clearly stated, because funders have a right to know:

- The framework contains conjectures about wider mathematical structure (the universality of a 2×2 decomposition across "wholes," reformulations of several Clay Millennium Problems in a common language) that are not proved and are clearly flagged as such in deeper documentation.
- An earlier manuscript stating a sinc-squared zero law for primes was withdrawn from the submission queue after internal audit determined the central biconditional held trivially for any positive integer, not only primes. The replacement — the First-G Event Localization theorem in §1.1 — is genuinely prime-dependent and carries the intended content. Superseded material remains in the repository marked `[HISTORICAL]` under the never-delete policy.
- The project is single-researcher-led with occasional collaborators. It is not an institutional research group. It is the work of Brayden Sanders (7Site LLC) with contributions from C. A. Luther, M. Gish, H. J. Johnson, B. Mayes, and B. Calderon Jr. on specific sub-projects, acknowledged in §7.

This project is not a Theory of Everything. It is a finite-algebra research program with concrete proved results, a working deterministic reasoning engine, and specific open questions.

---

## 6. Funding

The project is currently self-funded. The work in §1 and §3 has been produced without grant support. Continued progress on the open directions in §4 requires external support.

### Immediate specific needs ($1K-$5K range, 30-90 day impact)

- **MAGMA academic license (~$1,200):** unblocks the Hodge-lane Prym computation (§4.3) within weeks. This is the single highest-leverage small grant in the project. *Deliverable at 60 days: either confirmation or falsification of the framework-derived predicted period-matrix determinant, with a short technical note publishable either way.*
- **Sage/academic compute allocation (~$500/mo):** supports ongoing verification of larger-modulus First-G computations (§4.1). *Deliverable at 90 days: extension of First-G verification from semiprimes (153 tested) to general squarefree moduli up to $b \leq 10^6$.*
- **arXiv endorsement support (institutional, no direct cost):** the project has one math.NT endorsement and is seeking one more. *Deliverable on contact: an arXiv-available preprint of the First-G Event Localization theorem within two weeks of endorsement.*

### Seed research engagement ($25K-$75K, 3–6 months)

A 3-6 month engagement produces three concrete deliverables:

- **(3-month deliverable)** A cryptography-facing manuscript on First-G structure and factoring-complexity implications, targeting a mainstream cryptography venue (Crypto, Eurocrypt, or Journal of Cryptology). *Complete draft with all proofs; submission-ready.*
- **(4-month deliverable)** A formal architecture paper on CK positioning the engine against existing symbolic AI (ACT-R, Soar, Cyc) and within the interpretability-and-verification literature, targeting a venue like AAAI, NeurIPS workshop tracks, or a dedicated symbolic-AI publication. *Complete draft; submission-ready.*
- **(6-month deliverable)** Completion of the ξ-cosmology DESI DR2 fit with joint BAO + CMB + SN likelihood, and JCAP submission.

### Full research program ($150K-$300K, 12 months)

A twelve-month program delivering:

- **(6-month checkpoint)** All three seed-tier deliverables completed; at least one paper submitted or accepted.
- **(9-month checkpoint)** Hodge-lane Prym verification complete with a published technical note; CK scaled from 10-operator to 100+-operator demonstration with a public benchmark suite.
- **(12-month checkpoint)** A full synthesis manuscript tying the finite-algebra core to its application domains, with at least one collaborator paper produced jointly.
- **Supporting elements:** one graduate-student-level or postdoctoral collaborator to handle the cosmology and/or cryptography lane in parallel with the core work; travel budget for relevant conferences and research-institute visits; hardware and compute infrastructure for CK scale-up experiments.

### Where this fits for different funders

- **Crypto-native research funds** (Ethereum Foundation, Protocol Labs, a16z crypto research): First-G Law applications to factoring-based cryptography.
- **Interpretability and verifiable-reasoning funders** (Open Philanthropy, Survival and Flourishing Fund, Astera Institute): CK as a deterministic, auditable architecture for applications where inspectability matters.
- **Independent-science funders** (Emergent Ventures, Fifth Section, Simons Targeted Grants): core finite-algebra research; open Clay-adjacent directions.
- **Foundations with a math-and-physics portfolio** (Simons Foundation, Heising-Simons, Sloan Research Fellowship): foundational work on finite-ring structure and its cosmological application via the ξ field.

The project welcomes direct technical review from any potential funder's advisors. Every proved result in §1 is independently verifiable in under a minute.

---

## 7. People and Attribution

**Brayden Ross Sanders / 7Site LLC** — originator and lead. Q-series (Q2-Q17), 5D force vector as CRT Fourier embedding, Crossing Lemma, Flatness Theorem, UOP, σ-rate theorem, ξ-cosmology conceptual framework.

**C. A. Luther** — Senior R&D, 7Site LLC. G6 ($\sigma^6 = \mathrm{id}$), G7 period distribution, G8 spectral coherence; co-authored Sprints 11-14.

**Ben Mayes** — UOP Theorem 0 co-author; $S_4$ representation extension on NV qutrit.

**H. J. Johnson** — Sprint 14 ξ cosmology; logarithmic quintessence potential; separability framework.

**M. Gish** — First-G Law (WP34); Sprint 14 papers.

**B. Calderon Jr.** — Q17 variants; source elimination framework.

### Citation

```bibtex
@misc{sanders2026tig,
  author = {Sanders, Brayden Ross and Mayes, Ben and Luther, C. A.
            and Gish, M. and Johnson, H. J. and Calderon, B.},
  title  = {Trinity Infinity Geometry: Finite Algebra with
            Proved Theorems and a Deterministic Reasoning Engine},
  year   = {2026},
  doi    = {10.5281/zenodo.18852047},
  url    = {https://github.com/TiredofSleep/ck},
  note   = {7Site LLC. Default branch: tig-synthesis.}
}
```

---

## 8. Deeper Material

Readers who want more than the rigor layer on this page can follow any of these pointers:

- **Full formula and table reference:** [`FORMULAS_AND_TABLES.md`](./FORMULAS_AND_TABLES.md) — every load-bearing object in the framework in one file.
- **Atlas bundle:** `Atlas/ATLAS_INDEX.md` — eleven cross-referenced design documents (~6,550 lines) covering the full research program, with epistemic flags throughout.
- **Current sprint plan:** `Atlas/PLAN_OF_RECORD_2026_04_18.md` — what ships next, with assignment matrix.
- **Speculation and conjectural bridges:** the `clay` branch, the directory `papers/clay/` (Clay Millennium Problem reformulations), and cross-domain conjectural work preserved in development branches. None of this material appears on this page because it is not proved; it is preserved and clearly flagged for readers who want the fuller picture. Branch-level inventory is available in `BRIDGES_INVENTORY.md` for readers going deeper.
- **CK runtime fileset:** [`CK_RUNTIME.md`](./CK_RUNTIME.md) — every file that runs the deterministic reasoning engine.

The project follows a strict *never-delete* policy. Superseded and falsified material is marked `[HISTORICAL]` or `[FALSIFIED]` in place and preserved. The `archive-full` branch is the preservation layer.

---

## 9. License

**7Site Public Sovereignty License v1.0** — Human use only. Free for all humans to read, run, study, and build upon personally. No commercialization. No government, military, intelligence, or corporate enclosure. Full text in `LICENSE`.

---

*This repository is under active development. For technical review, collaboration, or funding discussions, please contact Brayden Sanders at brayden.ozark@gmail.com or open a GitHub issue. Independent verification of any result on this page is welcomed and encouraged.*

*Last updated: 2026-04-20.*
