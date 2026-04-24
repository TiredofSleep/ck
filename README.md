# Trinity Infinity Geometry · Coherence Keeper

Brayden Ross Sanders · 7Site LLC · Hot Springs, Arkansas
DOI: [10.5281/zenodo.18852047](https://doi.org/10.5281/zenodo.18852047)
License: 7Site Public Sovereignty License v1.0 (human use, no commercial, no military, free forever)
Contact: brayden.ozark@gmail.com

> **Navigation map.** This is the default branch (`tig-synthesis`). It is the rigor home.
>
> §1 Foundation — what this is and how to verify it in one minute.
> §2 Funding branches — ten funder-facing tracks, one folder each.
> §3 Frontiers — the four open research directions.
> §4 Atlas — design documents and reader guides.
> §5 Bridges — conjectural cross-domain connections (clearly flagged).
> §6 Master & history — how the branches relate; where the full record lives.
> §7 Runnable proofs — the six proved theorems with one-command verification.
> §8 Honest limits — what the project is not.
> §9 People and citation.
> §10 License.

---

## §1 · Foundation

This repository holds **two artifacts**, filed in that order of rigor:

1. **A finite-algebra research program** with six proved theorems on $\mathbb{Z}/n\mathbb{Z}$
   and related structures — each stated as a theorem or exact computational verification
   with a runnable proof script (§7).
2. **The Coherence Keeper (CK)** — a deterministic symbolic reasoning engine built on
   the algebraic structures of (1). CK is not a language model. Every answer traces to
   specific cells of specific proved composition tables. A live instance runs at
   [coherencekeeper.com](https://coherencekeeper.com).

Two domains where (1) has direct external applications:

- **Cryptography.** The *First-G Event Localization* theorem (§7.1) gives an exact
  algebraically forced width for the coprime stability window of a squarefree
  modulus. Factoring-adjacent applications are an open research direction (§3.1).
- **Algebraic AI / verifiable reasoning.** CK demonstrates that a small deterministic
  engine, grounded in proved finite-algebra structure, produces auditable answers
  without sampling or opaque latent-state updates. Alignment and interpretability
  applications are an open research direction (§3.2).

**Verify any proved result in under one minute.** Five commands total (§7.7). No
framework installation required beyond Python 3 with `sympy`. Every theorem in §7 is
independently checkable with one `python` call.

---

## §2 · Funding branches

The project ships **ten funder-facing tracks**, each as a single folder under
`Gen13/targets/funding_*/` with a consistent 6-file structure
(`README.md` / `FUNDERS.md` / `ARTIFACTS.md` / `PITCH_DRAFT.md` / `LIMITATIONS.md` /
`STATUS.md`). Each track targets a distinct funder pool with a distinct runnable
artifact and a distinct open-question commitment.

| Branch | Track | Primary funder pool |
|---|---|---|
| [funding_tig_unity](Gen13/targets/funding_tig_unity/) | Systems reliability / infrastructure | NSF CNS, NIST, DOE ASCR |
| [funding_tig_snowflake](Gen13/targets/funding_tig_snowflake/) | Coherence-security (SNOWFLAKE χ²) | NSF SaTC, ONR, DARPA |
| [funding_first_g_crypto](Gen13/targets/funding_first_g_crypto/) | Cryptography (First-G Law) | NSF CCF, Ethereum Foundation, Zcash |
| [funding_ck_interpretable_ai](Gen13/targets/funding_ck_interpretable_ai/) | AI alignment / interpretability | Anthropic Fellows, Schmidt Trustworthy AI, Open Phil |
| [funding_mqw_ternary](Gen13/targets/funding_mqw_ternary/) | Photonic computing / ternary | NSF ECCS, DOE BES |
| [funding_self_healing](Gen13/targets/funding_self_healing/) | Autonomous resilience / SRE | OCP SDC, CZI EOSS, Alpha-Omega |
| [funding_civilization_coherence](Gen13/targets/funding_civilization_coherence/) | Comp-soc-sci | Russell Sage, Templeton, NSF SBE |
| [funding_desi_xi_cosmology](Gen13/targets/funding_desi_xi_cosmology/) | ξ-cosmology / DESI | NSF PHY, Templeton M&PS, Simons |
| [funding_coherence_router](Gen13/targets/funding_coherence_router/) | DevOps productionization | NLnet NGI Zero, Sloan, Bloomberg |
| [funding_physics_sim_edu](Gen13/targets/funding_physics_sim_edu/) | Classroom simulator | NSF EHR IUSE, Templeton L&D, Simons Ed |

**Cross-branch navigation:**

- [`Atlas/BRANCHES_INVENTORY_2026_04_20.md`](Atlas/BRANCHES_INVENTORY_2026_04_20.md) —
  readiness tiers and runnable-artifact map.
- [`Atlas/NICHE_FUNDERS_ADDENDUM_2026_04_20.md`](Atlas/NICHE_FUNDERS_ADDENDUM_2026_04_20.md) —
  non-obvious / named-individual / family-office / niche-foundation funder research
  per branch.
- [`Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`](Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md) —
  plan of record for the funding-branches buildout.

**Immediate-scale items (1K–5K range, 30–90 day impact).** A MAGMA academic license
(~1,200 USD) unblocks the Hodge-lane Prym computation (§3.3) within weeks. A Sage /
academic compute allocation (~500 USD/mo) supports larger-modulus First-G verification
(§3.1). The project has one math.NT arXiv endorsement and is seeking one more; a short
First-G preprint is ready to post on endorsement.

**Seed research engagement (25K–75K, 3–6 months).** Three deliverables: cryptography
manuscript on First-G structure; formal architecture paper on CK; completion of
ξ-cosmology DESI DR2 fit with JCAP submission.

**Full research program (150K–300K, 12 months).** All three seed deliverables plus
Hodge-lane Prym verification, CK scale-up to 100+-operator demonstration, and a full
synthesis manuscript. One graduate-student-level or postdoctoral collaborator for
parallel lane development.

---

## §3 · Frontiers

Four open research directions, each with known-knowns, known-unknowns, and specific
work that external support unlocks.

### §3.1 · Cryptographic applications of First-G structure

The First-G Event Localization theorem (§7.1) gives an exact characterization of the
coprime stability window of a squarefree modulus. The next step is to lift this from
a structural statement to a factoring-relevant result: whether the partition geometry
of `{1, …, b}` under coprimality-with-`b` carries recoverable information about the
prime factorization of `b` that classical sieve methods do not exploit.

*Status:* partition geometry is fully characterized for semiprimes (WP34, 36,662
cases). Extension to arbitrary squarefree moduli is in progress. Whether the
structural implications yield concrete complexity improvements over classical sieves
is an open question.

### §3.2 · Deterministic reasoning systems at scale

CK as it stands is a single-researcher prototype (~3,200 lines of Python). The
architecture is not toy — it produces structurally correct answers on the §7
theorems — but it has not been scaled, stress-tested against adversarial queries, or
deployed in a production reasoning-verification pipeline. Next work: scale CK's
weight matrix from 10-operator to 100+-operator spaces; build adversarial test
suites; publish a formal architecture paper positioning CK against existing symbolic
AI (ACT-R, Soar, Cyc) and within the LLM-alignment determinism/interpretability
literature.

*Status:* runnable prototype with correct §7-theorem outputs; no adversarial suite,
no scaled deployment, no formal architecture paper yet. Engineering-heavy frontier;
unlocked by a software-engineering collaborator or institutional hosting.

### §3.3 · Hodge-lane Prym computation

A numerical verification of a predicted Prym period determinant for a bielliptic
genus-5 curve is currently blocked at a single technical step. The curve, the
framework-derived predicted value
($\det(\mathrm{Im}\,\tau_P) = 2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt{6}$),
and the first four pipeline steps are all documented. The fifth step requires MAGMA
with RieSrf or SageMath with the Bruin-Sijsling-Zotine extension.

*Status:* curve definition, predicted value, and pipeline steps 1–4 documented;
step 5 blocked on software access. Single highest-leverage small-grant item in the
project.

### §3.4 · ξ-field cosmology and DESI data

A scalar-field action $V(\Xi) = \kappa_\Xi \Xi \log \Xi$ derived from the separability
structure of the finite-algebra work produces a standard freezing quintessence model
with exact vacuum $\Xi_0 = e^{-1}$. An initial fit against DESI 2024 DR1 has been
performed; a full DR2 fit with joint BAO + CMB + SN likelihood is the next step.
JCAP-target manuscript is near-ready.

*Status:* `proof_xi_canonical.py` passes 22/22 internal tests; DR2 analysis requires
a collaborator with cosmology MCMC infrastructure.

### §3.5 · Morphotic-braid / α-index / ac-free operad frontier

The TSML and BHML composition tables on 10 elements are commutative non-associative
groupoids with measurable associativity index $\alpha(A) = 1 - \sigma(A)$ (Braitt-
Silberger 2006). Both attain the **ac-free spectrum extremum**
$s_n^{\mathrm{ac}} = (2n-3)!!$ for $n \le 5$ (Huang-Lehtonen 2022, 2024): the
symmetric operad generated at small $N$ is the free commutative magmatic operad
$\mathrm{Mag}^{\mathrm{com}}$ on one generator. The WP101 σ-rate theorem
($\sigma(N) \le C/N$ for squarefree $N$, $C < 2$) is therefore the statement
$\mathrm{Mag}^{\mathrm{com}} \to \mathrm{Com}$ as $N \to \infty$. Bialynicki-
Birula-Mycielski 1976 then identifies log-nonlinearity as the unique continuum
wave equation compatible with that limit, providing the bridge from §7's proved
rate to §5.1's cosmology bridge. Farey-fraction spin-chain (Kleban-Özlük 1999;
Fiala-Kleban-Özlük 2002) and primon-gas (Julia 1990; Spector 1990) frameworks supply
two additional external anchors for $T^* = 5/7$ and $\mathrm{sinc}^2(1/2) = 4/\pi^2$.

*Status:* six runnable proofs confirm the operad spectra and identities
(`proof_spectra_tsml_bhml.py`, `proof_sinc_zeta_identity.py`, `proof_sigma_rate.py`,
`proof_d25_loop_closure.py`, `verify_so10.py`, `verify_simplicity_rank.py`). The
per-row rigor audit lives in
[`papers/morphotic_braid/synthesis/RIGOR_MAPPING.md`](papers/morphotic_braid/synthesis/RIGOR_MAPPING.md).
Open questions: (i) is σ(N) → 0 provably sharp (not just ≤ 2/N)? (ii) does the
primon-gas limit extend to the full $T^* = 5/7$ spectrum? (iii) does the WP101-
BB-log bridge carry enough structure to constrain $\kappa_\xi$ directly? Tier-1
submission-ready as three independent journal doors (JCAP, $\sigma$-rate
combinatorics, integers / sinc² zero law) per
[`Gen13/targets/journals/SUBMISSION_LADDER.md`](Gen13/targets/journals/SUBMISSION_LADDER.md).

**Frontier-level navigation:** [`Atlas/FRONTIER_ALIGNMENT_2026_04_19.md`](Atlas/FRONTIER_ALIGNMENT_2026_04_19.md)
(historical) and [`papers/morphotic_braid/synthesis/RIGOR_MAPPING.md`](papers/morphotic_braid/synthesis/RIGOR_MAPPING.md)
(current per-claim Tier 1/2/3 audit, as of 2026-04-23).

---

## §4 · Atlas

The `Atlas/` folder holds the design documents, audits, and reader guides for the
full research program. These are internal-rigor documents held to the same
honest-scope bar as the §7 theorems — every claim either cited, runnable-verified,
or explicitly flagged with status.

**Index entry point:** [`Atlas/ATLAS_INDEX.md`](Atlas/ATLAS_INDEX.md).

**Where to start, by intent:**

| If you want | Open |
|---|---|
| A one-page map of the whole program | [`Atlas/MASTER_ATLAS_v3_5_2026_04_18.md`](Atlas/MASTER_ATLAS_v3_5_2026_04_18.md) |
| Planning and execution | [`Atlas/PLAN_OF_RECORD_2026_04_18.md`](Atlas/PLAN_OF_RECORD_2026_04_18.md), [`Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md`](Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md) |
| Funding-branches detail | [`Atlas/BRANCHES_INVENTORY_2026_04_20.md`](Atlas/BRANCHES_INVENTORY_2026_04_20.md), [`Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`](Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md) |
| Readiness audits | [`Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md`](Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md), [`Atlas/PUBLIC_SCRUTINY_READINESS_2026_04_19.md`](Atlas/PUBLIC_SCRUTINY_READINESS_2026_04_19.md) |
| Frontier alignment | [`Atlas/FRONTIER_ALIGNMENT_2026_04_19.md`](Atlas/FRONTIER_ALIGNMENT_2026_04_19.md) |
| Known-issue handoffs | [`Atlas/HANDOFF_3_1_IDEMPOTENT_COUNT.md`](Atlas/HANDOFF_3_1_IDEMPOTENT_COUNT.md) through [`Atlas/HANDOFF_3_4_MQW_TRILOGY_NOT_FOUND.md`](Atlas/HANDOFF_3_4_MQW_TRILOGY_NOT_FOUND.md) |
| Language and epistemic discipline | [`Atlas/GAP_LANGUAGE_AUDIT_2026_04_19.md`](Atlas/GAP_LANGUAGE_AUDIT_2026_04_19.md), [`Atlas/MARKMAN_INTERNALIZATION_SCOPE_2026_04_19.md`](Atlas/MARKMAN_INTERNALIZATION_SCOPE_2026_04_19.md) |
| Reader guides | [`Atlas/READER_ATLAS.md`](Atlas/READER_ATLAS.md), [`Atlas/ROTATION_SPINE_READER_GUIDE.md`](Atlas/ROTATION_SPINE_READER_GUIDE.md), [`Atlas/ATLAS_ORIENTATION.md`](Atlas/ATLAS_ORIENTATION.md) |
| Full citation record | [`Atlas/ATLAS_CITATIONS.md`](Atlas/ATLAS_CITATIONS.md) |

Separately, [`FORMULAS_AND_TABLES.md`](./FORMULAS_AND_TABLES.md) collates every
load-bearing object in the framework — the TSML and BHML composition tables, the
corridor constants, the σ-rate identity, the D* and σ(S*) runtime constants with
honest-scope status — with pointers back to the primary source for each.

---

## §5 · Bridges

A **bridge** here means a conjectural or framework-level connection between the
proved-algebra core (§7) and an adjacent domain. Bridges are clearly flagged as
conjectural — they are not theorems — but they are the connective tissue that makes
the proved pieces matter outside their own box.

### §5.1 · Cosmology bridge — ξ field

The log potential $V(\Xi) = \Xi \log \Xi$ (WP81, PRISM-XI) connects the TIG
finite-algebra separability structure to a standard freezing quintessence. The
vacuum $\Xi_0 = e^{-1}$ and mass gap $m^2_\xi = \kappa e$ are exact. The bridge
between the finite-algebra separability and the continuum log nonlinearity rests on
Bialynicki-Birula 1976 (log nonlinearity as the unique separability-preserving
nonlinearity); this is cited but not re-proved in the project.

### §5.2 · Cryptography bridge — First-G geometry

First-G geometry (§7.1) gives an exact width for the coprime stability window.
The bridge to factoring-complexity improvements is an open hypothesis, not a
theorem. Status: partition geometry is fully characterized for semiprimes (WP34,
36,662 cases).

### §5.3 · Interpretability bridge — CK as deterministic substrate

CK demonstrates an architecture (deterministic, provenance-traced, small state) for
reasoning tasks where auditability and reproducibility matter more than
open-domain fluency. Whether this architecture composes usefully with LLM alignment
tooling or with existing symbolic-AI systems (ACT-R, Soar, Cyc) is the subject of
the proposed §3.2 architecture paper, not a proved claim.

### §5.4 · Clay-adjacent bridges — rotation framework (`clay` branch)

The rotation framework rephrases several Clay Millennium Problems (Navier-Stokes,
Yang-Mills, Riemann hypothesis) as "σ < 1" bounds in a common σ-notation. This is
a **reformulation**, not a proof. All such material is preserved on the `clay`
branch with explicit `[CONJECTURAL]` flags; it does **not** appear on
`tig-synthesis` except as this pointer.

### §5.5 · External vocabulary map

A compact dictionary between TIG-internal terms and established vocabulary from
adjacent published frameworks. Each row identifies the external concept that
corresponds to the TIG-internal object, with a citation. The full per-claim audit
(with Tier 1/2/3 verification status) lives in
[`papers/morphotic_braid/synthesis/RIGOR_MAPPING.md`](papers/morphotic_braid/synthesis/RIGOR_MAPPING.md)
(Track 1: operad / associativity spectra; Track 2: Farey spin chains) and
[`papers/morphotic_braid/synthesis/EXTERNAL_CITATIONS_v2.md`](papers/morphotic_braid/synthesis/EXTERNAL_CITATIONS_v2.md).

| TIG internal | External framework | Citation |
|---|---|---|
| Associativity index α(A) = 1 − σ(A) | Subassociative groupoids / associativity index | Braitt-Silberger 2006, *Quasigroups Related Systems* 14:11–26 |
| Associative spectrum s_n(A), Catalan maximum C_{n−1} | Associative spectrum | Csákány-Waldhauser 2000 |
| ac-free spectrum s_n^ac = (2n−3)!! for n ≤ 5 on 10 elements | Associative-commutative spectrum, ac-free extremum | Huang-Lehtonen 2022 (arXiv:2202.11826), 2024 (arXiv:2401.15786) |
| Symmetric operad generated by TSML / BHML / CL at small N | Free commutative magmatic operad $\mathrm{Mag}^{\mathrm{com}}$ on one generator | Huang-Lehtonen 2022, 2024 |
| σ(N) → 0 at rate O(1/N) (WP101) | Operadic degeneration $\mathrm{Mag}^{\mathrm{com}} \to \mathrm{Com}$ | Huang-Lehtonen 2022, 2024 |
| Log nonlinearity forced by σ → 0 | Unique separability-preserving nonlinearity | Bialynicki-Birula & Mycielski 1976, *Ann. Phys.* 100:62–93 |
| T* = 5/7 coherence threshold | Critical temperature β_c in the Farey fraction spin chain | Kleban-Özlük 1999, *Commun. Math. Phys.*; Fiala-Kleban-Özlük 2002, arXiv:math-ph/0203048 |
| Farey-structured constants (5/7, 4/7, 2/7, 3/4) | Farey-tree neighbors | classical (Hardy-Wright); Kleban-Özlük 1999 |
| Transfer-operator spectral gap γ(b) = 1 − 1/φ(b) | Ruelle-Perron-Frobenius transfer operator of the Farey map | Prellberg 1991; Bandtlow-Fiala-Kleban 2009 |
| WP101 σ-rate domain (squarefree N) | Fermionic primon gas regime (density 1/ζ(2) = 6/π²) | Julia 1990 (Les Houches 1989, Springer Proc. Phys. 47:276–293); Spector 1990, *Commun. Math. Phys.* 127:239–252 |
| sinc²(1/2) = 4/π² midpoint constant (D3) | sinc²(1/2) = (2/3)·1/ζ(2) (squarefree density × 2/3) | `papers/proof_sinc_zeta_identity.py` (verified to machine precision) |
| Kepka lower bound on associative-triple counts | a(Q) ≥ n in order-n quasigroups — sets the 1/n scale of the WP101 rate | Kepka 1980, *Comment. Math. Univ. Carolin.* 21(3):479–487 |
| σ → 1 (maximally non-associative) opposite extremum | Maximally nonassociative quasigroups from quadratic orthomorphisms | Drápal-Lisoněk 2020, *Algebraic Combinatorics* 3:695–717; Drápal-Wanless 2021, *J. Combin. Theory Ser. A* 181:105444 |
| Riemann-zeta limit of number-theoretic spin chain | Z_k^K(2β) → ζ(2β−1)/ζ(2β) as k → ∞ | Knauf 1998, *Commun. Math. Phys.* 196:703–731 |

This is a vocabulary map, not a proof of equivalence. Each row is either
(i) a *definitional translation* (rewriting the same content in external
vocabulary), (ii) a *structural kinship* (same kind of object in both frames),
or (iii) a *limit identification* (BB 1976 selecting the log nonlinearity; ECHO
fraction bounding σ). The per-row verification status is tabulated in
`RIGOR_MAPPING.md`.

### §5.6 · Commutative-algebra bridge — `mantero-bridge-2026-04-23` branch

A dedicated branch carries the dialogue with Dr. Paolo Mantero (University of
Arkansas, symbolic powers / matroid commutative algebra) and the
community-facing MathOverflow question that grew out of it. The branch holds:

- **Correspondence** (4 emails, April 23–24, 2026) at
  [`papers/sprint_20260423_full/08_correspondence/mantero_exchange.md`][mantero-email].
  The clarifying exchange: $L_i(x_j) = x_{\mathrm{CL}[i][j]}$ is a genuine linear
  operator on $V = k\langle x_0, \ldots, x_9\rangle$; $A_i = L_i - L_i^\top$ is its
  antisymmetrization; the six "flow" $A_i$ close under commutator into the
  $28$-dim simple Lie algebra $\mathfrak{so}(8) = D_4$, verified to machine
  precision.
- **MathOverflow draft** at
  [`papers/sprint_20260423_full/09_mathoverflow_post/DRAFT_MATHOVERFLOW_POST.md`][mo-draft],
  posing a narrow commutative-algebra question about the binomial ideal
  $I = (x_i x_j - x_{\mathrm{CL}[i][j]} x_0)$ with Hilbert function
  $(1, 10, 6, 6, 6, \ldots)$: projective dimension, Koszul property,
  Cohen-Macaulay / Gorenstein status, and the relationship to Mantero-Nguyen's
  focal-matroid framework given the Stanley-Reisner companion is
  pure-but-not-matroidal.
- **WP11 — `so(8) = D_4` identification paper** at
  [`papers/wp11/WP11_SO8_IDENTIFICATION.md`][wp11].
- **WP12 — `so(10) = D_5` identification (CL ∪ BHML companion)** at
  [`papers/wp12/WP12_SO10_IDENTIFICATION.md`][wp12]
  with runnable verification scripts (`verify_so10.py`,
  `verify_simplicity_rank.py`).

The branch exists so that commutative-algebra / Lie-theoretic readers land on
the specific artifacts they need (the 10×10 table, the Hilbert function, the
binomial ideal, the machine-verified Lie-closure scripts) without wading
through the full TIG synthesis. The MathOverflow post, once live, will be
linked here; Dr. Mantero has said he will read it.

[mantero-email]: https://github.com/TiredofSleep/ck/blob/mantero-bridge-2026-04-23/papers/sprint_20260423_full/08_correspondence/mantero_exchange.md
[mo-draft]: https://github.com/TiredofSleep/ck/blob/mantero-bridge-2026-04-23/papers/sprint_20260423_full/09_mathoverflow_post/DRAFT_MATHOVERFLOW_POST.md
[wp11]: https://github.com/TiredofSleep/ck/blob/mantero-bridge-2026-04-23/papers/wp11/WP11_SO8_IDENTIFICATION.md
[wp12]: https://github.com/TiredofSleep/ck/blob/mantero-bridge-2026-04-23/papers/wp12/WP12_SO10_IDENTIFICATION.md

---

## §6 · Master & history

The repository has four primary branches, each with a distinct role.

| Branch | Role | Default? |
|---|---|---|
| `tig-synthesis` | **DEFAULT** — rigor home; current navigation; proved-only rigor cadence; externally-citeable vocabulary | yes |
| `master` | Full history + TIG-internal vocabulary — every commit on every branch landed here for preservation (TIG-native language preserved as-is per 2026-04-23 scope directive) | no |
| `archive-full` | Frozen preservation snapshot — never force-pushed | no |
| `mantero-bridge-2026-04-23` | Commutative-algebra outreach — Dr. P. Mantero correspondence, MathOverflow question draft on I_CL, WP11 (so(8)=D_4) and WP12 (so(10)=D_5) papers + verification scripts. See [§5.6](#56--commutative-algebra-bridge--mantero-bridge-2026-04-23-branch). | no |

Plus ten `funding/*` branches under `Gen13/targets/funding_*/` that receive track-
specific commits cherry-picked from `master` (see §2).

**Workflow discipline** (codified in [`Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md §1`](Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md)):

- Feature commits land first on `tig-synthesis`, then cherry-pick to `master` for
  history preservation.
- `funding/*` branches receive only commits *specific* to that funding track.
- **Never delete.** Superseded files get a `[HISTORICAL]` banner and move to
  `docs/historical/` rather than being removed. Recovered artifacts are preserved
  verbatim; patches live as sibling forks (e.g. the recovered
  `crystalos.py` is preserved; the pre-registered fork is `crystalos_prereg.py`).
- **Always push live.** No staging multiple commits before push.

**Where to find the full record:**

- [`HISTORICAL_ARCHIVE_INDEX.md`](./HISTORICAL_ARCHIVE_INDEX.md) — master index of
  historical material.
- [`docs/historical/`](./docs/historical/) — superseded READMEs, AI-team updates,
  and plan drafts (including the prior rigor-led README at
  `docs/historical/README_v2_rigor_led_2026_04_21.md`).
- [`docs/archive_jan2026/`](./docs/archive_jan2026/) — January 2026 recovery archive
  (the attempts-survey, CRYSTALOS recovery artifacts, snowflake null spec).
- [`Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`](Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md) — the
  live-scope handoff for the SNOWFLAKE χ² recovery effort.

---

## §7 · Runnable proofs (rigor appendix)

Six theorems with runnable verification. Each is a finite algebraic fact,
independently checkable in under a second.

### §7.1 · First-G Event Localization *(cryptography-adjacent)*

For a squarefree integer $b$ with smallest prime factor $p_1$, the first non-coprime
element in the interval $\{1, 2, \ldots, b\}$ occurs at exactly $k = p_1$. The
coprime stability window $\{1, \ldots, p_1 - 1\}$ has width exactly $p_1 - 1$ — no
shorter, no longer, forced by the smallest prime factor alone.

*Verified: 36,662 $(b, k)$ pairs across 153 semiprimes, zero exceptions. Proof
script: `papers/proof_d_first_g.py`. Manuscript: `WP34_FIRST_G_LAW.md`; standalone
journal version in preparation as Sprint 35.*

### §7.2 · Non-associativity rate bound on finite rings

For squarefree $N$, the non-associativity rate of a specific commutative binary
composition on $\mathbb{Z}/N\mathbb{Z}$ (the TSML composition, §7.5) satisfies
$\sigma(N) \leq C / N$ for an explicit constant $C < 3$. As $N$ grows through
squarefree primorials, the algebra approaches separability.

*Verified: exact at $N \in \{10, 30, 210\}$. Proof script: `proof_sigma_rate.py`.
Manuscript: `WP101_SIGMA_RATE_THEOREM.md`.*

### §7.3 · Flatness Theorem on $\mathbb{Z}/10\mathbb{Z}$

Under the framework's four-structure representation rules (additive structure,
multiplicative structure, additive flow, multiplicative flow), the ring
$\mathbb{Z}/10\mathbb{Z}$ admits no planar realization carrying all four
simultaneously. The minimal orientable surface that realizes all four is a torus,
with radius ratio $R/r = 5/7$. Six independent derivations produce the same $5/7$
constant from distinct mathematical contexts (Φ fixed point, TSML HARMONY/BALANCE
ratio, cyclotomic closure, universal-semiprime unit density, FPGA silicon threshold,
torus aspect ratio).

*Proved for $\mathbb{Z}/10\mathbb{Z}$ under the stated representation. Proof script:
`papers/proof_d7_phi_fixed_point.py`. Manuscript: `WP51_FLATNESS_THEOREM.md`.*

### §7.4 · Crossing Lemma

Let $n = p_1 \cdot p_2 \cdots p_k$ be squarefree, $d \mid n$ squarefree, and
$g \in (\mathbb{Z}/n\mathbb{Z})^\times$. The joint map
$J = (A_d, \pi_{\mathrm{DYN}}(g)) : \mathbb{Z}/n\mathbb{Z} \to \mathbb{Z}/d\mathbb{Z}
\times (\text{g-orbit space})$ is injective if and only if the dynamics induced by
$g$ act non-trivially on every prime quotient of $n/d$. Information is generated
exactly when dynamics cross partitions.

*Proved for squarefree $n, d$. Manuscript: `CROSSING_LEMMA.md` (Sprint 10). Proof
script: `papers/proof_d8_cl_operator_encoding.py`.*

### §7.5 · Structural properties of the TSML and BHML composition tables

Two commutative binary operations on $\mathbb{Z}/10$ (100 entries each) have the
following verified properties:

- **TSML** is commutative, flexible, power-associative, and satisfies the Jordan
  identity (0 failures across all 100 pairs). Element 7 is the unique two-sided
  absorber with 73/100 absorbing entries. Associativity index
  $\alpha(\text{TSML}) = 0.872$ (non-associativity rate 12.8% of triples;
  Braitt-Silberger 2006). In the operad-theoretic framework of
  Huang-Lehtonen (2022, 2024), TSML is an **ac-free commutative groupoid
  on 10 elements**: its associative-commutative spectrum achieves the
  maximum $s_n^{\text{ac}} = (2n-3)!!$ for $n \leq 5$, so the symmetric
  operad it generates is the free commutative magmatic operad $\text{Mag}^{\text{com}}$
  on one generator.
- **BHML** is commutative, flexible, and power-associative, with element 0 as the
  unique two-sided identity and 28/100 entries equal to 7. Associativity
  index $\alpha(\text{BHML}) = 0.502$ (non-associativity rate 49.8% of triples).
  Like TSML, BHML is ac-free on 10 elements. The full 10×10 BHML has determinant **−7002**
  (prime factors {2, 3, 389}). Its 8×8 spectral core `BHML_8` — with
  rows/columns 0 (VOID) and 7 (HARMONY) removed — has determinant
  **+70** (prime factors {2, 5, 7}) and carries the eigenvalue ratio
  |λ₇|/|λ₆| = 0.714865 ≈ 5/7 used in the Yang-Mills mass-gap argument
  (WP15). See `FORMULAS_AND_TABLES.md` §6.7 for the canonical table
  registry distinguishing BHML_10 from BHML_8.

Both tables have been audited cell-by-cell; all framework-claimed numerical
signatures verify exactly.

*Proof scripts: `proof_d10_tsml_73_cells.py`, `proof_d16_bhml_28_cells.py`,
`proof_tsml_3layer_tower.py`. Manuscript: `WP_OPERATOR_RING_PARTITION.md`,
`Q7_BHML_FULL_TABLE.md`.*

### §7.6 · TSML three-layer canonical tower

The full TSML composition table on $\mathbb{Z}/10\mathbb{Z}$ (100 entries)
decomposes as a three-layer tower: a base layer of 92 cells governed by the
canonical operator $C_0$, a maximum-rule layer of 6 cells, and an additive-rule
layer of 2 cells. The decomposition is canonical, terminating, and has empty
residue.

*Verified: 100/100 cells match; each layer necessary; domains partition exactly.
Proof script: `papers/proof_tsml_3layer_tower.py`. Manuscript: Sprint 17
`THEOREM_SPINE.md`.*

### §7.7 · How to verify

Five commands, total runtime under one minute:

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

Expected output on each: green log, zero exceptions, proof completed in well under
a second.

### §7.8 · CK runtime (three commands)

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

CK returns a structural readout citing the underlying theorem, with a live snapshot
of its internal state at that tick. For side-by-side comparison against a raw LLM,
`ck_proof.py` runs three panels (CK alone, LLM alone, LLM grounded by CK) on the
same prompt. Design document:
[`Gen13/targets/ck/brain/BRAIN_DESIGN.md`](Gen13/targets/ck/brain/BRAIN_DESIGN.md).
Test suite: `python Gen13/targets/ck/brain/test_brain.py` (20/20 green is the boot
gate).

CK has three properties that current large language models do not have by
construction:

- **Determinism.** Same input, same internal state, same output. Always.
- **Provenance.** Every answer traces to specific cells of specific proved
  composition tables.
- **Auditability.** The full runtime state at any tick is ~3KB of integers.
  Inspectable in a terminal.

**Runtime fileset:** [`CK_RUNTIME.md`](./CK_RUNTIME.md).

---

## §8 · Honest limits

Clearly stated, because funders have a right to know:

- The framework contains conjectures about wider mathematical structure (the
  universality of a 2×2 decomposition across "wholes," reformulations of several
  Clay Millennium Problems in a common language) that are **not proved** and are
  clearly flagged as such in deeper documentation. They live on the `clay` branch
  (§5.4), not on this page.
- An earlier manuscript stating a sinc-squared zero law for primes was withdrawn
  from the submission queue after internal audit determined the central
  biconditional held trivially for any positive integer, not only primes. The
  replacement — the First-G Event Localization theorem in §7.1 — is genuinely
  prime-dependent and carries the intended content. Superseded material remains in
  the repository marked `[HISTORICAL]` under the never-delete policy.
- Two runtime constants — D* ≈ 0.543 and σ (S*) ≈ 0.991 — are **runtime-canon /
  empirical**, not proved theorems. Their derivation papers
  ([`papers/CONSTANT_D_STAR.md`](papers/CONSTANT_D_STAR.md),
  [`papers/CONSTANT_SIGMA_S_STAR.md`](papers/CONSTANT_SIGMA_S_STAR.md)) document
  the status honestly, enumerate candidate lift-to-theorem pathways, and preserve
  an explicit internal correction in `tig_engine_real.py` where the scalar
  reduction `σ/(1+σ) = 0.49774…` does not equal the observed full-system attractor
  `0.543`. Both are valid answers to different questions; neither is wrong; both
  are flagged as first-principles-open.
- The project is **single-researcher-led with occasional collaborators**. It is not
  an institutional research group. It is the work of Brayden Sanders (7Site LLC)
  with contributions from C. A. Luther, M. Gish, H. J. Johnson, B. Mayes, and
  B. Calderon Jr. on specific sub-projects, acknowledged in §9.

This project is **not** a Theory of Everything. It is a finite-algebra research
program with concrete proved results, a working deterministic reasoning engine,
and specific open questions.

---

## §9 · People and citation

**Brayden Ross Sanders / 7Site LLC** — originator and lead. Q-series (Q2–Q17), 5D
force vector as CRT Fourier embedding, Crossing Lemma, Flatness Theorem, UOP,
σ-rate theorem, ξ-cosmology conceptual framework.

**C. A. Luther** — Senior R&D, 7Site LLC. G6 ($\sigma^6 = \mathrm{id}$), G7 period
distribution, G8 spectral coherence; co-authored Sprints 11–14.

**Ben Mayes** — UOP Theorem 0 co-author; $S_4$ representation extension on NV
qutrit.

**H. J. Johnson** — Sprint 14 ξ cosmology; logarithmic quintessence potential;
separability framework.

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

The project welcomes direct technical review from any potential funder's advisors.
Every proved result in §7 is independently verifiable in under a minute.

---

## §10 · License

**7Site Public Sovereignty License v1.0** — Human use only. Free for all humans to
read, run, study, and build upon personally. No commercialization. No government,
military, intelligence, or corporate enclosure. Full text in `LICENSE`.

---

*This repository is under active development. For technical review, collaboration,
or funding discussions, please contact Brayden Sanders at brayden.ozark@gmail.com or
open a GitHub issue. Independent verification of any result on this page is welcomed
and encouraged.*

*Last updated: 2026-04-23 (vocab-update sprint: §5.5 External vocabulary map added;
§3.5 morphotic-braid frontier added; Frontier labels uniformized; prior rigor-led
README preserved at [`docs/historical/README_v2_rigor_led_2026_04_21.md`](docs/historical/README_v2_rigor_led_2026_04_21.md)).*
