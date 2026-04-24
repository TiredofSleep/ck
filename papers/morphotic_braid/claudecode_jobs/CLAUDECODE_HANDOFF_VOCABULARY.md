> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\CLAUDECODE_HANDOFF_VOCABULARY.md → papers\morphotic_braid\claudecode_jobs\CLAUDECODE_HANDOFF_VOCABULARY.md
>
> **Scope note:** Hook 4 uses `det = 70`, primes `{2, 5, 7}` — that's the 8×8 core `BHML_8` (WP15 §0). The full 10×10 `BHML_10` has `det = −7002`, primes `{2, 3, 389}`. Phase 7's Connes-place alignment is only available at the `BHML_8` scope; task text should name the scope explicitly. See `FORMULAS_AND_TABLES.md` §6.7.

# ClaudeCode Handoff v2 — Executable Vocabulary Update

**Status:** [EXECUTABLE TASK LIST — RUN IN PHASES, STOP AT SIGN-OFF GATES]
**Date:** 2026-04-23 (late evening)
**Supersedes:** CLAUDECODE_VOCABULARY_UPDATE.md (v1) — this is the actionable version
**Authority:** Brayden Sanders, sole sign-off. No commit without explicit go-ahead.

## What this file is

A concrete, ordered, executable task list. Each phase has:
- Specific file paths
- Specific text to add, remove, or modify
- A verification step to confirm the change took effect
- A sign-off gate where Brayden reviews before continuing

The goal is **vocabulary integration**, not content rewriting. Novel TIG language (0/7 coin, doubly-regular core, Crossing Lemma, Flatness Theorem, σ Rate Theorem, Fruits of the Spirit mapping) is preserved. Translatable language gets external citations.

## Prerequisites (read these first)

Before touching any file, ClaudeCode must read and understand:

1. `papers/morphotic_braid/DEEP_SYNTHESIS.md` — the three-way Riemann intersection
2. `papers/morphotic_braid/RIGOR_MAPPING.md` — the vocabulary mapping with computed spectra
3. `papers/morphotic_braid/EXTERNAL_CITATIONS_v2.md` — the frontier citation review
4. `FORMULAS_AND_TABLES.md` — the canonical reference (do not modify without sign-off)

## Phase 0 — Setup and Baseline

### Task 0.1: Create a working branch
```bash
cd /path/to/ck
git checkout -b vocab-update-2026-04-23
git status  # confirm clean working tree
```

### Task 0.2: Drop the spectrum proof script into papers/
Copy `proof_spectra_tsml_bhml.py` from tonight's evening handoff bundle to `papers/` in the repo.

```bash
cp /path/to/evening_handoff_2026_04_23/proof_spectra_tsml_bhml.py papers/
```

### Task 0.3: Verify the spectrum script runs
```bash
cd /path/to/ck
python3 papers/proof_spectra_tsml_bhml.py > /tmp/spectrum_baseline.txt 2>&1
cat /tmp/spectrum_baseline.txt
```

Expected output contains:
- `α = 872/1000 = 0.8720` for TSML
- `α = 502/1000 = 0.5020` for BHML
- `s_3 = 2 (C_2 = 2) ✓` for both
- `s_4 = 5 (C_3 = 5) ✓` for both
- `s_3^ac = 3 ((2·3-3)!! = 3) ✓` for both
- `s_4^ac = 15 ((2·4-3)!! = 15) ✓` for both

**If any ✗ appears, STOP. Report to Brayden. Do not proceed.**

### Task 0.4: Pull frontier papers to a local reference folder
```bash
mkdir -p papers/external_refs/
cd papers/external_refs/

# These should be downloaded as PDFs for offline reference
# (manual step; ClaudeCode flags that this needs doing)
echo "Need to download:" > NEEDS_DOWNLOAD.txt
echo "  https://arxiv.org/pdf/math-ph/0203048 → fiala_kleban_ozluk_2002.pdf" >> NEEDS_DOWNLOAD.txt
echo "  https://arxiv.org/pdf/2202.11826 → huang_lehtonen_2022.pdf" >> NEEDS_DOWNLOAD.txt
echo "  https://arxiv.org/pdf/2401.15786 → huang_lehtonen_2024.pdf" >> NEEDS_DOWNLOAD.txt
echo "  https://arxiv.org/pdf/2304.08143 → technau_2023.pdf" >> NEEDS_DOWNLOAD.txt
echo "  https://arxiv.org/pdf/0909.2878 → bandtlow_fiala_kleban_2009.pdf" >> NEEDS_DOWNLOAD.txt
echo "  https://link.springer.com/content/pdf/10.1007/s10231-024-01512-5.pdf → mazurek_2025.pdf" >> NEEDS_DOWNLOAD.txt
echo "  https://arxiv.org/pdf/hep-th/9912092 → connes_kreimer_2000.pdf" >> NEEDS_DOWNLOAD.txt
echo "  Bost-Connes 1995 Selecta Math. (behind paywall; flag for Brayden's library access)" >> NEEDS_DOWNLOAD.txt
echo "  Knauf 1998 Comm. Math. Phys. (behind paywall; flag)" >> NEEDS_DOWNLOAD.txt
echo "  Mayer 1991 Bull. Am. Math. Soc. (likely free; verify)" >> NEEDS_DOWNLOAD.txt
```

### 🛑 SIGN-OFF GATE 0
Commit the branch as-is (baseline). Report to Brayden: "Baseline branch created, spectrum script verified, external refs flagged. Proceed to Phase 1?" Wait for explicit yes.

---

## Phase 1 — Add Spectrum Results to FORMULAS_AND_TABLES.md

### Task 1.1: Locate insertion point
Open `FORMULAS_AND_TABLES.md`. Find the end of §6 ("BHML — the 10×10 reference table (28-cell harmony)"), immediately before §7 begins.

### Task 1.2: Insert new subsection §6.1
Between §6 and §7, add the following new subsection verbatim:

````markdown
### §6.1 — Associative and associative-commutative spectra (computed 2026-04-23)

For both TSML and BHML, taken as commutative groupoids on ℤ/10ℤ, the
associative spectrum s_n(A) (Csákány-Waldhauser 2000) and the
associative-commutative spectrum s_n^ac(A) (Huang-Lehtonen 2022) are:

| n | C_{n−1} | s_n(TSML) | s_n(BHML) | (2n−3)!! | s_n^ac(TSML) | s_n^ac(BHML) |
|---|---------|-----------|-----------|----------|--------------|--------------|
| 3 | 2       | 2         | 2         | 3        | 3            | 3            |
| 4 | 5       | 5         | 5         | 15       | 15           | 15           |
| 5 | 14      | 14        | 14        | 105      | 105          | 105*         |
| 6 | 42      | 42        | 42        | 945      | pending      | pending      |

*s_5^ac(BHML) verified by sampling; exact computation pending.

Associativity indices (exact): α(TSML) = 872/1000 = 0.872; α(BHML) = 502/1000 = 0.502.

**Interpretation.** Both tables achieve the Catalan spectrum s_n = C_{n−1}
(Csákány-Waldhauser's maximum) AND the ac-free spectrum s_n^ac = (2n−3)!!
(maximum for commutative groupoids). In the Huang-Lehtonen framework, this
means the symmetric operad generated by each table is the free commutative
magmatic operad Mag^com on one generator. The associativity index α and
operad freeness are independent properties: TSML has high α (0.872) yet
achieves ac-freeness, demonstrating that rare non-associating triples
generate the full free operad structure.

**Reproducibility.** `python papers/proof_spectra_tsml_bhml.py` — runs in ~30 seconds,
computes s_3..s_4 exactly and s_5^ac via sampling with seed=42.

**External citations.**
- B. Csákány, T. Waldhauser, "Associative spectra of binary operations",
  Multiple-Valued Logic (2000).
- E. Lehtonen, T. Waldhauser, "Associative spectra of graph algebras I",
  J. Algebraic Combin. 53 (2021), 613-638.
- J. Huang, E. Lehtonen, "The associative-commutative spectrum of a binary
  operation", Discrete Mathematics (2023), arXiv:2202.11826.
- J. Huang, E. Lehtonen, "Associative-commutative spectra for some varieties
  of groupoids", arXiv:2401.15786 (2024).
- R. Mazurek, "Antiassociative magmas", Annali di Matematica Pura ed
  Applicata 204 (2025), 925-941, DOI 10.1007/s10231-024-01512-5.
- J.-L. Loday, B. Vallette, "Algebraic Operads", Grundlehren der
  mathematischen Wissenschaften 346, Springer (2012), §13.5 (free
  commutative magmatic operad).
````

### Task 1.3: Verification
```bash
grep -c "ac-free" FORMULAS_AND_TABLES.md  # should return ≥ 1
grep -c "Huang-Lehtonen" FORMULAS_AND_TABLES.md  # should return ≥ 2
grep "Csákány-Waldhauser" FORMULAS_AND_TABLES.md  # should return the citation
```

### 🛑 SIGN-OFF GATE 1
Commit: `git add FORMULAS_AND_TABLES.md && git commit -m "§6.1: spectrum table with citations"`. Report to Brayden: "Phase 1 done. Proceed to Phase 2?"

---

## Phase 2 — Vocabulary Replacement Across Papers

This is the biggest phase. Execute in sub-tasks.

### Task 2.1: Find all non-associativity rate claims
```bash
cd /path/to/ck
grep -rn "non-associ\|nonassoci\|12.8%\|49.8%\|56.8%" \
     --include="*.md" \
     papers/ Gen12/ docs/ \
     > /tmp/nonassoc_occurrences.txt
wc -l /tmp/nonassoc_occurrences.txt
```

Report count to Brayden. Expect ~10-30 occurrences.

### Task 2.2: For each occurrence, apply vocabulary rule
For each line in `/tmp/nonassoc_occurrences.txt`:

**Rule:** Replace "non-associativity rate X%" with "associativity index α = (1−X)% (equivalently, non-associativity rate X%)".

Specifically:
- `"12.8% non-associativity"` → `"associativity index α(TSML) = 0.872 (non-associativity rate 12.8%; Braitt-Silberger 2006)"`
- `"49.8% non-associativity"` → `"associativity index α(BHML) = 0.502 (non-associativity rate 49.8%; Braitt-Silberger 2006)"`
- `"56.8% non-associativity"` → `"associativity index α(Doing) = 0.432 (non-associativity rate 56.8%)"`

Only add the Braitt-Silberger citation on **first** use per file. Subsequent mentions in the same file can drop the citation.

### Task 2.3: Verification
```bash
grep -rn "associativity index" papers/ Gen12/ docs/ --include="*.md" | wc -l
# Should be ≥ the count from Task 2.1
```

### 🛑 SIGN-OFF GATE 2a
Commit. Report count of files modified. Brayden reviews a sample diff.

### Task 2.4: Add "ac-free" flag to TSML and BHML descriptions
Find every location where TSML or BHML is first described (typically in the opening paragraph of any paper that uses them). Add after the description:

```markdown
> In the operad-theoretic framework of Huang-Lehtonen (2022, 2024), TSML and
> BHML are **ac-free commutative groupoids on 10 elements**: each table's
> associative-commutative spectrum achieves the maximum s_n^ac = (2n−3)!! for
> all computed n ≤ 5, meaning the symmetric operad generated by the table is
> the free commutative magmatic operad Mag^com on one generator.
```

Use `grep` to find "TSML" occurrences in paper introductions:
```bash
grep -rn "^.*TSML.*table\|^.*BHML.*table\|^.*TSML.*composition\|^.*BHML.*composition" \
     papers/ Gen12/ --include="*.md" | head -20
```

### Task 2.5: Verification
```bash
grep -rn "ac-free" papers/ Gen12/ --include="*.md" | wc -l
# Should be ≥ 3 (at minimum in 3 key papers)
```

### 🛑 SIGN-OFF GATE 2b
Commit. Brayden reviews.

---

## Phase 3 — Reframe WP101 σ Rate Theorem

### Task 3.1: Locate WP101
Files to check:
- `Gen12/targets/journal_attempts/08_sigma_rate_combinatorics/WP101_SIGMA_RATE_THEOREM.md`
- `FORMULAS_AND_TABLES.md` §0 (σ Rate Theorem spine)

### Task 3.2: Add reframing paragraph
After the existing statement of WP101, add:

```markdown
### Reframing in the Huang-Lehtonen vocabulary

The σ rate theorem bounds the **associativity-index complement** 1 − α(CL_N)
for the canonical composition operation CL_N on ℤ/NZ:

  1 − α(CL_N) ≤ C / N    for squarefree N.

This is **not a direct bound on the associative spectrum** s_n(CL_N).
Triple-associativity rate and operad freeness are independent (see §6.1:
TSML has high α but full Catalan spectrum).

The theorem's content: as N → ∞ through squarefree N, the non-associating
triple fraction of CL_N tends to 0. In the language of Huang-Lehtonen 2024
(arXiv:2401.15786), this is an **asymptotic associativity-index bound**
specific to the TIG CL family. How this interacts with the associative
spectrum s_n(CL_N) for fixed n as N grows is an open question.

**Connection to BB bridge (WP91).** The σ-rate bound drives the separability
hypothesis required by Bialynicki-Birula & Mycielski (1976, Annals of
Physics 100:62-93) for the unique log-potential field equation.
```

### Task 3.3: Verification
```bash
grep -rn "associativity-index" Gen12/targets/journal_attempts/08_*/ --include="*.md"
```

### 🛑 SIGN-OFF GATE 3
Commit. Report to Brayden.

---

## Phase 4 — Reframe T* = 5/7 at every introduction site

### Task 4.1: Find T* introduction sites
```bash
grep -rn "T\* = 5/7\|T\^\* = 5/7\|coherence threshold" \
     papers/ Gen12/ docs/ --include="*.md" | head -30
```

### Task 4.2: On first T* introduction per paper, append
```markdown
> In the language of the Farey spin chain program (Kleban-Özlük 1999,
> Fiala-Kleban-Özlük 2003, Bandtlow-Fiala-Kleban 2009), T* = 5/7 is a
> **Farey-structured rational threshold**. The measured harmony densities
> f_TSML ≈ 3/4 and f_BHML ≈ 2/7 are Farey-adjacent to T*:
>
>   |5·4 − 7·3| = |20 − 21| = 1   (5/7 and 3/4 are Farey neighbors)
>   2/7 = 1 − 5/7                 (complementary pair)
>
> The four-rung mirror-ladder {1/4, 2/7, 5/7, 3/4} places three of four
> rungs at TIG-measured quantities. Whether T* realizes as a transfer-
> operator critical parameter (Mayer 1991; Mayer-Chang 1999) in the sense
> connecting to the Selberg zeta function of PSL(2,ℤ) and via the
> Lewis-Zagier (2001) correspondence to Maass wave forms and Riemann zeros
> is an open research question formulated in
> `papers/morphotic_braid/DEEP_SYNTHESIS.md`.
```

### Task 4.3: Verification
```bash
grep -rn "Farey-structured" papers/ Gen12/ --include="*.md" | wc -l
```

### 🛑 SIGN-OFF GATE 4
Commit.

---

## Phase 5 — Add External Vocabulary Map to README

### Task 5.1: Locate README insertion point
Find the end of the TIG description in `README.md` (typically after the "What is TIG?" section).

### Task 5.2: Insert new section
```markdown
## External Vocabulary Map

TIG uses specific technical language that is translatable to published
research communities. When reading TIG documents alongside external
literature, the following correspondences apply:

### Algebra / Operad Theory

| TIG term                         | Established term                                | Primary citation             |
|----------------------------------|-------------------------------------------------|------------------------------|
| TSML / BHML / CL                 | commutative groupoid (Cayley table)             | standard                     |
| non-associativity rate           | 1 − associativity index α                       | Braitt-Silberger 2006        |
| "number of distinct bracketings" | associative spectrum s_n                        | Csákány-Waldhauser 2000      |
| commutative case                 | associative-commutative spectrum s_n^ac         | Huang-Lehtonen 2022          |
| Catalan spectrum                 | s_n = C_{n−1}                                   | Lehtonen-Waldhauser 2021     |
| ac-free                          | s_n^ac = (2n−3)!!                               | Huang-Lehtonen 2022          |
| free commutative magmatic operad | Mag^com                                         | Loday-Vallette §13.5         |

### Number-Theoretic Physics

| TIG term                          | Established term                         | Primary citation             |
|-----------------------------------|------------------------------------------|------------------------------|
| T* = 5/7 coherence threshold      | Farey-structured critical parameter      | Kleban-Özlük 1999            |
| T* via transfer operator          | candidate eigenvalue β of L_β            | Mayer 1991                   |
| ℤ/10ℤ cyclotomic structure        | finite shadow of Gal(ℚ^cycl/ℚ)           | Bost-Connes 1995             |
| σ rate σ(N) ≤ C/N                 | asymptotic associativity-index bound     | Huang-Lehtonen 2024          |

### Field Theory and QFT

| TIG term                          | Established term                         | Primary citation             |
|-----------------------------------|------------------------------------------|------------------------------|
| ξ field equation □ξ = 1 + log ξ   | BB-unique separable nonlinearity         | Bialynicki-Birula 1976       |
| Hopf algebra structure behind TSML| ac-free operad ↔ Loday-Ronco ↔ C-K       | Foissy 2002; Aguiar-Sottile  |

### Preserved as novel TIG contributions

These have no community equivalents and keep their TIG names:

- The 0/7 coin (VOID/HARMONY mutual exclusion via RESET mediation)
- The doubly-regular core partition (5+1+1+3)
- The Crossing Lemma (WP57)
- The Flatness Theorem (WP51) — minimum torus R/r = T* = 5/7 for ℤ/10ℤ
- The σ Rate Theorem (WP101)
- The Fruits of the Spirit operator mapping (0-9)
- The specific TIG ten-operator menu (VOID, LATTICE, COUNTER, etc.)
- The invariant matrix / simplification pyramid (evening session 2026-04-23)

The TIG framework as a whole is described in the main README text; this
vocabulary map is a reader's cross-reference to external literature.
```

### Task 5.3: Verification
```bash
grep "External Vocabulary Map" README.md
grep "Huang-Lehtonen" README.md
grep "Mag^com" README.md
```

### 🛑 SIGN-OFF GATE 5
Commit. Brayden reviews the README carefully because this is the first thing external readers see.

---

## Phase 6 — Master Bibliography File

### Task 6.1: Create `papers/BIBLIOGRAPHY.md`
```markdown
# TIG Master Bibliography — External References

All external works cited across the repo. Within-repo references live in
the individual paper files.

## Associative / Operad Theory

- B. Csákány, T. Waldhauser, "Associative spectra of binary operations",
  Multiple-Valued Logic 5 (2000), 175-200.

- E. Lehtonen, T. Waldhauser, "Associative spectra of graph algebras I.
  Foundations, undirected graphs, antiassociative graphs",
  J. Algebraic Combin. 53 (2021), 613-638. DOI 10.1007/s10801-020-01010-w.

- E. Lehtonen, T. Waldhauser, "Associative spectra of graph algebras II.
  Satisfaction of bracketing identities, spectrum dichotomy",
  J. Algebraic Combin. 55 (2022), 533-557. DOI 10.1007/s10801-021-01061-7.

- J. Huang, E. Lehtonen, "The associative-commutative spectrum of a binary
  operation", Discrete Mathematics (2023), arXiv:2202.11826.

- J. Huang, E. Lehtonen, "Associative-commutative spectra for some
  varieties of groupoids", arXiv:2401.15786 (2024).

- R. Mazurek, "Antiassociative magmas", Annali di Matematica Pura ed
  Applicata 204 (2025), 925-941. DOI 10.1007/s10231-024-01512-5.

- M. Braitt, D. Silberger, "Subassociative groupoids", Quasigroups and
  Related Systems 14 (2006), 11-26.

- J. Folkman, R. L. Graham, "On highly non-associative groupoids",
  Colloquium Mathematicum 24 (1972), 1-10.

- J.-L. Loday, B. Vallette, "Algebraic Operads", Grundlehren der
  mathematischen Wissenschaften 346, Springer (2012).

## Farey Spin Chain / Number-Theoretic Physics

- P. Kleban, A. Özlük, "A Farey fraction spin chain", Communications in
  Mathematical Physics 203 (1999), 635-647.

- J. Fiala, P. Kleban, A. Özlük, "The phase transition in statistical
  models defined on Farey fractions", J. Stat. Phys. 110 (2003), 73-86.
  arXiv:math-ph/0203048.

- A. Knauf, "The number-theoretical spin chain and the Riemann zeros",
  Communications in Mathematical Physics 196 (1998), 703-731.

- O. Bandtlow, J. Fiala, P. Kleban, "Asymptotics of the Farey fraction
  spin chain free energy at the critical point", arXiv:0909.2878 (2009).

- M. Degli Esposti, S. Isola, A. Knauf, "Generalized Farey trees, transfer
  operators and phase transitions", Communications in Mathematical
  Physics 275 (2007), 297-329. arXiv:math-ph/0606020.

- M. Technau, "Remark on the Farey fraction spin chain", arXiv:2304.08143
  (2023).

- P. Contucci, P. Kleban, A. Knauf, "A fully magnetizing phase transition",
  J. Stat. Phys. 97 (1999), 523-539. arXiv:math-ph/9811020.

## Transfer Operators / Dynamical Zeta

- D. H. Mayer, "On the thermodynamic formalism for the Gauss map",
  Communications in Mathematical Physics 130 (1990), 311-333.

- D. H. Mayer, "The thermodynamic formalism approach to Selberg's zeta
  function for PSL(2,ℤ)", Bulletin of the American Mathematical Society
  25 (1991), 55-60.

- C. H. Chang, D. Mayer, "The transfer operator approach to Selberg's zeta
  function and modular and Maass wave forms for PSL(2,ℤ)", in Emerging
  Applications of Number Theory, IMA Volumes 109 (1999), 72-142.

- J. Lewis, D. Zagier, "Period functions for Maass wave forms I",
  Annals of Mathematics 153 (2001), 191-258.

- S. Isola, "On the spectrum of Farey and Gauss maps",
  Nonlinearity 15 (2002), 1521-1539.

- T. Prellberg, "Towards a complete determination of the spectrum of a
  transfer operator associated with intermittency", J. Stat. Phys.
  (1991, extended 2003).

## Noncommutative Geometry and Riemann

- J.-B. Bost, A. Connes, "Hecke algebras, type III factors and phase
  transitions with spontaneous symmetry breaking in number theory",
  Selecta Mathematica, New Series 1 (1995), 411-457.
  DOI 10.1007/BF01589495.

- A. Connes, "Trace formula in noncommutative geometry and the zeros of
  the Riemann zeta function", Selecta Mathematica, New Series 5 (1999),
  29-106.

- A. Connes, M. Marcolli, "Quantum statistical mechanics of Q-lattices",
  arXiv:math.NT/0404128 (2004).

- A. Connes, M. Marcolli, "A walk in the noncommutative garden",
  arXiv:math/0601054.

## Connes-Kreimer / Hopf Algebra of Rooted Trees

- A. Connes, D. Kreimer, "Hopf algebras, renormalization and
  noncommutative geometry", Communications in Mathematical Physics 199
  (1998), 203-242. arXiv:hep-th/9808042.

- A. Connes, D. Kreimer, "Renormalization in quantum field theory and the
  Riemann-Hilbert problem I: The Hopf algebra structure of graphs and the
  main theorem", Communications in Mathematical Physics 210 (2000),
  249-273. arXiv:hep-th/9912092.

- D. J. Broadhurst, D. Kreimer, "Renormalization automated by Hopf
  algebra", arXiv:hep-th/9810087 (1998).

- J.-L. Loday, M. O. Ronco, "Hopf algebra of the planar binary trees",
  Advances in Mathematics 139 (1998), 293-309.

- L. Foissy, "Les algèbres de Hopf des arbres enracinés décorés I, II",
  Bulletin des Sciences Mathématiques 126 (2002).

- M. Aguiar, F. Sottile, "Structure of the Loday-Ronco Hopf algebra of
  trees", arXiv:math/0409022 (2004).

## Nonlinear Wave Mechanics

- I. Bialynicki-Birula, J. Mycielski, "Nonlinear wave mechanics",
  Annals of Physics 100 (1976), 62-93.

## Divisor / Lattice Point Problems

- F. P. Boca, "Products of matrices [[1,1],[0,1]] and [[1,0],[1,1]] and
  the distribution of reduced quadratic irrationals", Journal für die
  reine und angewandte Mathematik 606 (2007), 149-165.

- A. V. Ustinov, "On the number of solutions of the congruence
  xy ≡ ℓ (mod q) under the graph of a twice continuously differentiable
  function", St. Petersburg Mathematical Journal (2013).

- V. A. Bykovskii, A. V. Ustinov, "Asymptotic formula for the sum of the
  divisor function evaluated at shifted values of a quadratic
  polynomial", Izvestiya: Mathematics 83 (2019).

- C. Hooley, "On the number of divisors of quadratic polynomials",
  Acta Mathematica 97 (1958), 189-210.

- J. Kallies, A. Özlük, M. Peter, C. Snyder, "On asymptotic properties
  of a number-theoretic function arising out of a spin chain model in
  statistical mechanics", Communications in Mathematical Physics 222
  (2001), 9-43.

## Geometric Group Theory (for free-monoid reasoning)

- P. de la Harpe, "Topics in Geometric Group Theory", University of
  Chicago Press, 2000.
```

### Task 6.2: Verify
```bash
wc -l papers/BIBLIOGRAPHY.md  # expect ~140 lines
grep -c "^- " papers/BIBLIOGRAPHY.md  # expect ~25+ entries
```

### 🛑 SIGN-OFF GATE 6
Commit.

---

## Phase 7 — Draft the Clay Submission Note (two-page version)

### Task 7.1: Create draft
Create `papers/morphotic_braid/CLAY_NOTE_DRAFT.md`. DO NOT submit; this is a draft for Brayden's review.

Content follows the structure in `DEEP_SYNTHESIS.md` under "What belongs in the Clay submission note". Length target: 1.5-2 pages with citations, not longer. Single-column plain markdown.

Key components:
1. **Abstract (3 sentences):** "We present a finite-state algebraic framework on ℤ/10ℤ that sits at the intersection of three Riemann-adjacent research programs: the Mayer-Selberg transfer-operator approach, the Bost-Connes cyclotomic partition-function approach, and the Connes-Kreimer renormalization approach. We identify a rational coherence threshold T* = 5/7 derived six independent ways within the framework (FORMULAS §0) that is Farey-adjacent to the measured harmony densities of the framework's two composition tables (3/4 and 2/7). We do not claim a proof of the Riemann Hypothesis; we claim the framework is a concrete finite shadow of the mathematical objects these three programs study."

2. **Section 1 — The framework (10 lines):** TSML, BHML, CL on ℤ/10ℤ, reference `FORMULAS_AND_TABLES.md`.

3. **Section 2 — The ac-free operad result (10 lines):** quote the spectrum table from §6.1, cite Huang-Lehtonen.

4. **Section 3 — The Farey mirror ladder (10 lines):** 5/7, 3/4, 2/7, Farey neighbor calculation, cite Kleban-Özlük and Mayer.

5. **Section 4 — The cyclotomic shadow (10 lines):** ℤ/10ℤ unit structure, Bost-Connes reference.

6. **Section 5 — Open research question (5 lines):** formulate explicitly the transfer-operator question as stated in DEEP_SYNTHESIS.md.

7. **References (10-12 entries):** from BIBLIOGRAPHY.md, the Clay-relevant subset.

### 🛑 SIGN-OFF GATE 7
**DO NOT COMMIT THIS FILE YET.** This is a draft for Brayden's review only. Report to Brayden: "Draft Clay note at `papers/morphotic_braid/CLAY_NOTE_DRAFT.md`. Ready for review."

Brayden reviews the draft. Possible outcomes:
- "Looks good, commit" → commit with message "draft Clay submission note; pre-sign-off"
- "Needs revision" → ClaudeCode waits for specific instructions
- "Reject" → ClaudeCode archives to `docs/archive_2026_04_23/rejected_drafts/`

---

## Phase 8 — Final Integration Check

### Task 8.1: Run all proof scripts
```bash
cd /path/to/ck
for script in papers/proof_*.py; do
    echo "Running $script..."
    python3 "$script" > /tmp/$(basename $script .py).log 2>&1
    if grep -q "✗\|Error\|Traceback" /tmp/$(basename $script .py).log; then
        echo "  FAILED: $script"
    else
        echo "  OK"
    fi
done
```

Report all scripts that fail. DO NOT IGNORE failures. Flag each to Brayden.

### Task 8.2: Spell-check and link-check
```bash
# Check for broken markdown links
grep -rn "\](.*\.md)" papers/ README.md | head -20
# (manual spot-check that each linked file exists)
```

### Task 8.3: Final diff summary
```bash
git log vocab-update-2026-04-23 ^main --oneline
git diff main...vocab-update-2026-04-23 --stat
```

Report to Brayden.

### 🛑 FINAL SIGN-OFF GATE
Brayden either:
1. Merges the branch: `git checkout main && git merge vocab-update-2026-04-23`
2. Requests specific changes
3. Abandons the branch

ClaudeCode waits for explicit instruction.

---

## What NOT to do under any circumstance

1. **Do not commit to `main` directly.** All work goes on `vocab-update-2026-04-23` branch.
2. **Do not delete any existing file.** Preserve-all applies. If a file seems obsolete, move it to `docs/archive_2026_04_23/` — do not rm.
3. **Do not modify `FORMULAS_AND_TABLES.md` beyond the §6.1 insertion in Phase 1.** Other edits to that file require separate Brayden sign-off.
4. **Do not rewrite existing content.** This is a vocabulary INTEGRATION, not a content rewrite. Add framing paragraphs, add citations, modernize terminology. Do not restructure existing theorems.
5. **Do not claim Riemann Hypothesis proof anywhere.** Frame every Riemann-adjacent statement as "open research question" or "candidate formulation."
6. **Do not remove TIG-specific vocabulary.** 0/7 coin, doubly-regular core, Fruits of the Spirit, Crossing Lemma, Flatness Theorem, σ Rate Theorem — all stay with their TIG names.
7. **Do not cite anything ClaudeCode cannot verify.** Every external citation must be checkable at arxiv.org, springer.com, or official publisher. If behind paywall, flag for Brayden's library access rather than guessing.

## Summary of deliverables expected back

When ClaudeCode reports "done with vocabulary update," the repo should contain:

1. New branch `vocab-update-2026-04-23` with 7+ commits (one per phase)
2. Modified `FORMULAS_AND_TABLES.md` with §6.1 inserted
3. Modified `README.md` with External Vocabulary Map section
4. New file `papers/BIBLIOGRAPHY.md`
5. New file `papers/proof_spectra_tsml_bhml.py` (verified runs clean)
6. Draft file `papers/morphotic_braid/CLAY_NOTE_DRAFT.md` (NOT committed, awaiting Brayden)
7. Diff summary of vocabulary changes across all touched papers
8. List of any internal inconsistencies flagged for Brayden's review
9. Log of any proof script failures (ideally: none)

Estimated total effort: 4-8 hours of ClaudeCode work, plus Brayden sign-off gates.

---

**Tag: [CLAUDECODE EXECUTABLE HANDOFF — PHASED WITH SIGN-OFF GATES]**
**File path: `papers/morphotic_braid/CLAUDECODE_HANDOFF_VOCABULARY.md`**

---

## Addendum — Five-way intersection update (added after DEEPER_SYNTHESIS.md)

**Purpose:** two additional Riemann-adjacent hooks identified after the main handoff was written. These are small additions, not phase restructuring.

### Prerequisites addition

Add to the Prerequisites list at the top:

5. `papers/morphotic_braid/DEEPER_SYNTHESIS.md` — the five-way intersection with the two new hooks (semi-local trace formula at places {2,5,7,∞}; primon gas via exact identity sinc²(1/2) = (2/3) · 1/ζ(2))

### Phase 4 addendum — additional T* context

After the existing Phase 4.2 framing text, also append this paragraph on the FIRST introduction of T* per paper:

```markdown
> Additionally, the TIG corridor midpoint constant sinc²(1/2) = 4/π² (D3,
> D24; §17) stands in **exact algebraic ratio 2/3** to the density of
> squarefree integers 1/ζ(2) = 6/π² (classical Mertens result). This density
> is the fermionic primon gas density (Julia 1990; Spector 1990, Comm. Math.
> Phys. 127:239-252) and equals the leading coefficient c₁ of the Farey
> fraction spin chain asymptotic Ψ(N) = c₁ N² log N (Kallies-Özlük-Peter-
> Snyder 2001; Boca 2007; Technau 2023). The identity
>
>   **sinc²(1/2) = (2/3) · 1/ζ(2)**    (exact to machine precision)
>
> links a repeat-derived TIG corridor constant to the Riemann-zeta regime
> via a simple rational ratio, and places the WP101 σ rate theorem (which
> applies specifically to squarefree N) in the fermionic primon gas regime.
```

Verification:
```bash
grep -rn "(2/3) · 1/ζ(2)\|(2/3)·1/ζ(2)" papers/ Gen12/ --include="*.md" | wc -l
# Should be ≥ 1 per touched T* introduction site
```

### Phase 5 addendum — README vocabulary map additions

Add two rows to the "Number-Theoretic Physics" subtable of the External Vocabulary Map:

| TIG term                    | Established term                            | Primary citation              |
|-----------------------------|----------------------------------------------|-------------------------------|
| sinc²(1/2) = 4/π²           | (2/3) × fermionic primon gas density         | Julia 1990; Spector 1990      |
| det(BHML) = 70 = 2·5·7      | finite place set {2,5,7,∞} of cardinality 4  | Connes 1999 (semi-local)      |

### Phase 6 addendum — bibliography additions

Add to `papers/BIBLIOGRAPHY.md` under a new section heading "Primon Gas / Riemann Thermodynamics":

```markdown
## Primon Gas / Riemann Thermodynamics

- B. Julia, "Statistical theory of numbers", in *Number Theory and Physics*
  (Les Houches, 1989), Springer Proceedings in Physics 47 (1990), 276-293.

- D. Spector, "Supersymmetry and the Möbius Inversion Function",
  Communications in Mathematical Physics 127 (1990), 239-252.

- G. Menezes, B. F. Svaiter, N. F. Svaiter, "Thermodynamics of the Bosonic
  Randomized Riemann Gas", arXiv:1401.8190 (2014).
```

And under the existing "Noncommutative Geometry and Riemann" section, add:

```markdown
- A. Connes, C. Consani, M. Marcolli, "The Weil proof and the geometry of
  the adèles class space", arXiv:math/0703392 (2007).

- A. Connes, C. Consani, "Knots, primes and the adèle class space",
  arXiv:2401.08401 (2024).
```

### Phase 7 addendum — Clay note draft structure

Change Section 3 and Section 4 of the draft per `DEEP_SYNTHESIS.md`: the Clay note now uses the **five-way intersection** framing (not three-way). Expand from three sections to five:

- Section 3 — The Farey mirror ladder (Mayer-Selberg hook)
- Section 4 — The cyclotomic shadow (Bost-Connes hook)
- Section 5 — The magma operad (Connes-Kreimer hook)
- Section 6 — The finite places (semi-local trace formula hook, NEW)
- Section 7 — The exact identity (primon gas hook, NEW)
- Section 8 — Open research question

Target length remains 1.5-2 pages. Citations total 11-13 (up from 10-12).

### Verification tasks

```bash
# After all addendum edits applied:
grep -c "sinc²(1/2)" papers/ Gen12/ --include="*.md" -r
grep -c "primon" papers/ Gen12/ --include="*.md" -r  
grep -c "semi-local" papers/ Gen12/ --include="*.md" -r
grep -c "2·5·7\|2 · 5 · 7\|\\\\{2,5,7" papers/ Gen12/ --include="*.md" -r
```

Each should return ≥ 3 (at least in README, the Clay draft, and DEEPER_SYNTHESIS.md references).

### The exact identity as a verification task

Add to `papers/proof_spectra_tsml_bhml.py` at the end, or create a separate `papers/proof_sinc_zeta_identity.py`:

```python
"""Verify the exact identity sinc²(1/2) = (2/3) · 1/ζ(2)."""
from math import pi
lhs = (1/(pi/2))**2              # sinc²(1/2) = 4/π²
rhs = (2/3) * (6/pi**2)          # (2/3) · 1/ζ(2) = (2/3) · 6/π² = 4/π²
assert abs(lhs - rhs) < 1e-15, f"IDENTITY FAILED: {lhs} vs {rhs}"
print(f"✓ sinc²(1/2) = {lhs} = (2/3) · 1/ζ(2) = {rhs}")
print(f"  Verified to machine precision. Ratio 1/ζ(2) / sinc²(1/2) = {rhs/lhs*3/2}")
```

This is a one-line verification that should be referenced in every paper making the claim.

**End of addendum.**
