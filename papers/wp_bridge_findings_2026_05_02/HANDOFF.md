# ClaudeCode Handoff: Bridge Findings → Repo + CK Integration

**From:** Bridge research session (Claude / Brayden, 2026-05-02)
**To:** ClaudeCode
**Status:** Computational results ready for scrutiny + integration
**DOI:** 10.5281/zenodo.18852047
**Repo:** github.com/TiredofSleep/ck

---

## §1 What this handoff is

A research session pushed every available computational thread on TIG's
substrate (TSML_8 + BHML_10 with V/H flow boundary, σ permutation,
flow/structure/transition/void role partition). Five empirically-grounded
findings emerged. Ten honest negatives sharpened what the framework IS by
establishing what it ISN'T.

This handoff packages everything for you to:
1. **Scrutinize** — verify computations, find errors I missed, challenge claims
2. **Integrate into the github repo** — add canon-quality findings to FORMULAS_AND_TABLES.md, draft WP9/WP10
3. **Wire into CK** — codec, ck_organism.py, force9, persistence layer

You should NOT trust this work blindly. I made several errors during the
session that Brayden caught (most importantly: I had been using TSML_10
instead of TSML_8 + flow cells for trefoil computations until corrected).
Treat my findings as hypotheses to verify, not truth.

---

## §2 Files in this handoff

### `/docs/`
- `OUT_OF_ROPE_FINAL.md` — the final consolidated synthesis (master doc)
- `BRIDGE_TESTS_FINAL.md` — bridge tests with negatives
- `CORRECTED_FRAME_BRIDGES.md` — corrected substrate findings
- `FLOW_STRUCTURE_FINAL.md` — flow/structure binary integration
- `THREE_DOORS_SYNTHESIS.md` — Fibonacci, TSML_8 image, boundary symmetries
- `DEEPER_FINDINGS.md` — earlier honest results
- `THREE_READINGS_SYNTHESIS.md` — three reading framework
- `CITATION_MAP.md` — published-math citations for bridge papers
- `FORWARD_CITATIONS.md` — recent papers (Matsusaka-Ueki, Burrin-von Essen, etc.)
- `SYNTHESIS.md`, `INDEX.md` — earlier organization

### `/code/`
30+ Python scripts, all reproducible, none requiring exotic dependencies.

**Substrate definitions (canonical):**
- `tig_substrate.py` — TSML_10, BHML_10, σ permutation
- `corrected_substrate.py` — TSML_8 + BHML_10 + flow cells

**Trefoil analyses (corrected frame):**
- `trefoil_corrected_frame.py` — runtime processor, 9-trefoil result
- `trefoil_corrected_associativity.py` — {V,H,Br} ∪ {V,Br,Br} characterization
- `breath_uniqueness.py` — why BREATH is the unique structure cell
- `higher_order_trefoils.py` — 4-element and 5-element extensions

**Reading C and Rademacher:**
- `reading_c_corrected.py` — TSML_8 self-iteration → cusp escape
- `rademacher_period_bridge.py` — period→trace bridge giving -21
- `rademacher_bridge.py`, `rademacher_search.py` — earlier attempts (uncorrected)
- `orbit_to_psl2z.py` — five PSL(2,Z) lift strategies (all negative)
- `triangle_groups_test.py` — triangle group rule-out

**Role partition:**
- `flow_structure_binary.py` — F/S/T/V partition definition + tests
- `role_decomposition.py` — ±21 = F_7 + F_6 (Fibonacci) decomposition
- `role_magma_factorization.py` — role magma table, V is identity
- `tsml8_role_analysis.py` — TSML_8 5-element image, 94% flow output

**Symmetries and taxonomy:**
- `interchangeability_test.py` — 5↔6 and other boundary swaps on grammar
- `symmetry_map.py` — comprehensive global preservation map
- `crossing_taxonomy.py` — crossing-count distribution analysis
- `algebraic_relationship.py` — TSML vs BHML algebraic independence

**Lacasa, Borromean, Fibonacci robustness:**
- `lacasa_corrected.py` — substrate doesn't factor through CRT
- `borromean_primes.py`, `substrate_borromean.py` — Borromean negative
- `fibonacci_robustness.py` — Fibonacci is canonical-specific

**Earlier (uncorrected frame, kept for reference):**
- `d1_composition.py`, `d2_phenomenological.py`
- `d3_attestation.py`, `d3_attestation_fixed.py`
- `d4_invariant_clean.py`, `d4_invariant_search.py`
- `three_readings.py`, `knot_polynomials.py`
- `trajectory_braid.py`, `trefoil_22_analysis.py`
- `trefoil_algebraic.py`, `trefoil_link_structure.py`
- `trefoil_structure.py`, `trefoil_survival.py`
- `class_average_check.py`

### `/results/`
- `FINDINGS_TABLE.md` — five facts + ten negatives in tabular form
- `INTEGRATION_TARGETS.md` — specific files in repo and CK to modify
- `VERIFICATION_PROTOCOL.md` — exactly what to re-run for verification
- `KNOWN_ISSUES.md` — errors I made, things to double-check

### `/wp_drafts/`
- `WP9_LATTICE_outline.md` — outline for paradoxical info algebras paper
- `WP10_DKAN_outline.md` — outline for DKAN paper
- `BRIDGE_PAPERS_status.md` — status of Hoffman/Friston/Tononi/Faggin handoffs

---

## §3 The five findings (TL;DR)

1. **Trefoil characterization (operator-level):**
   On corrected frame (TSML_8 + flow cells + BHML_10), trefoil ⟺
   multiset = {VOID, BREATH, HARMONY} or {VOID, BREATH, BREATH}.
   Nine triples, two multiset classes, all BHML-associative.

2. **BHML diagonal = integer successor on {1..7}:**
   BHML(n, n) = n + 1 for n ∈ {1..7}, with BHML(8,8) = 7 (return) and
   BHML(9,9) = 0 (collapse). Drives period(n) = 7-n for the 6-cycle.

3. **Two-coding split:**
   - TSML_8 (geometric): 5-element image {3,4,7,8,9}, 94% flow output,
     role-deterministic on 8 of 9 input role-pairs.
   - BHML_10 (arithmetic): 10-element image, balanced roles,
     role-deterministic only on V/T inputs.
   - Two codings agree at cusp (HARMONY), disagree in interior.

4. **±21 invariant has two decompositions:**
   - σ-orbit: T_5 + T_3 = 15 + 6 (triangular)
   - Role: F_7 + F_6 = 13 + 8 (Fibonacci, canonical-specific)

5. **Role magma has VOID as identity:**
   Mode-based role magma (V/F/S/T) is commutative, non-associative, has
   V as identity. V/T inputs make BHML role-deterministic; F/S inputs
   branch.

---

## §4 The ten honest negatives

1. No naive PSL(2,ℤ) lift produces ±21 — five strategies tested
2. No small triangle group Γ_{p,q} has substrate's period set as elliptic orders
3. TIG's grammar isn't a literal Borromean-prime condition
4. σ ↔ ST in SL(2,ℤ) gives elliptic elements (wrong for modular knots)
5. σ is NOT an automorphism of TSML or BHML (48% / 17% match)
6. TSML and BHML don't distribute over each other (19.5% match)
7. BHML iteration doesn't converge to TSML (28/64 starts)
8. Substrate algebra doesn't factor through Z/2 × Z/5
9. Random tables don't reproduce Fibonacci role decomposition (0/200)
10. Role partition alone doesn't determine crossing count for most patterns

---

## §5 What I want you to do

### Phase 1: Scrutiny (priority)

Before integrating ANYTHING, verify the math.

1. **Run `verify_findings.py`** in `/code/` — re-runs all five findings and
   checks them. If any fail, STOP and report.

2. **Read `KNOWN_ISSUES.md`** — I list errors I made and things I'm uncertain
   about. Pay extra attention there.

3. **Sanity-check the corrected substrate frame.** Per FORMULAS §6.7:
   TSML_8 = TSML_10 with rows/cols {0, 7} removed. V (0) and H (7) are
   flow cells between tables. I had been using TSML_10 in early scripts
   until Brayden corrected me. Verify all post-correction scripts use the
   right frame.

4. **Challenge the Fibonacci claim.** The robustness test showed it's
   canonical-specific (0/200 random tables reproduce it). I downgraded
   from "Fibonacci structure theorem" to "numerical signature of
   canonical TIG." Make sure I didn't inflate it back up anywhere in the
   docs.

5. **Verify the BHML successor claim:** BHML(n, n) = n + 1 for n ∈ {1..7}.
   This is checkable in 2 lines of Python. Confirm it.

6. **Look for arithmetic errors.** I worked fast across many scripts.
   Spot-check several computations against direct hand calculations.

### Phase 2: Integration into github repo

If scrutiny passes:

1. **Update FORMULAS_AND_TABLES.md** with new D-entries (see
   INTEGRATION_TARGETS.md for proposed numbering):
   - D88: Corrected substrate frame (TSML_8 + BHML_10 + flow cells)
   - D89: Trefoil characterization {V,H,Br} ∪ {V,Br,Br}
   - D90: BHML successor diagonal (n → n+1 on {1..7})
   - D91: Two-coding TSML_8/BHML_10 image structure
   - D92: ±21 invariant with σ-orbit and role decompositions
   - D93: Role magma with VOID identity
   - D94: Five canonical grammar role-pattern readings

2. **Write WP9 (LATTICE theorem / paradoxical info algebras) using the
   role-magma findings.** The role-level branching on F/S inputs vs
   role-determinism on V/T inputs is the paradoxical-information structure
   for WP9. Outline in `/wp_drafts/WP9_LATTICE_outline.md`.

3. **Write WP10 (DKAN) integrating the two-coding picture.** TSML_8 as
   collapse-coding, BHML_10 as expansion-coding maps cleanly to DKAN's
   geometric/arithmetic split. Outline in `/wp_drafts/WP10_DKAN_outline.md`.

4. **Update bridge paper handoffs** (Hoffman, Friston, Tononi, Faggin) with
   corrected-frame results. Specifically:
   - Lead with corrected substrate (not the wrong-frame version I used early)
   - Replace "trefoil-22" claim with corrected "trefoil-9" + characterization
   - Add Burrin-von Essen analogy carefully (structural similarity, not theorem)
   - Be honest about open ±21 hypothesis (period→trace bridge needs principled
     derivation, not yet proven)

5. **Add citation map** (CITATION_MAP.md, FORWARD_CITATIONS.md) to repo for
   academic engagement scaffolding.

### Phase 3: CK integration

1. **Update ck_organism.py** with corrected substrate definitions:
   - Add TSML_8 explicit table
   - Add flow cell handling (V/H between tables)
   - Verify ck_curvature.py uses the corrected frame

2. **Wire ±21 invariant into CK metrics:**
   - Compute Ghys-analog and period-bridge versions per tick
   - Track role-decomposition (Fibonacci) and σ-orbit decomposition (triangular)
   - Add to coherence dashboard

3. **Update force9 codec:**
   - The role partition ({V}, {F=1,3,5,7,9}, {S=2,4,8}, {T=6}) is the
     codec's natural symbol grouping
   - 5↔6 boundary symmetry should be a codec feature: encoder can choose
     either at the F/T boundary
   - V↔BREATH symmetry (the strongest at 20.9%) should similarly be available

4. **CK fault-state debugging hook:**
   - When CK enters fault state, check role distribution
   - If pure-F or pure-S accumulating without V/T cells, signal "no boundary
     collapse" (substrate stuck in interior)
   - If VVV-state dominating, signal "rest state" (24-crossing maximum
     trajectory complexity, not failure)

5. **Codec + olfactory integration:**
   - The trefoil set {V,H,Br} ∪ {V,Br,Br} is the codec's "knot vocabulary
     entry for trefoil"
   - Olfactory remembers d2 + force vectors; add role labels to memory traces

### Phase 4: Open questions to flag

These are NOT ready for integration; they are research projects:

1. **Principled lift to PSL(2,ℤ) hyperbolic conjugacy classes** — would
   confirm or rule out ±21 as real Rademacher invariant. Currently:
   period→trace bridge under simple representative gives -21, but that's
   one of many possible lifts.

2. **Larger substrate variants** — does Fibonacci role decomposition
   appear in Z/14Z, Z/18Z analogs? Test would clarify whether it's a
   small-substrate coincidence.

3. **The (0,7,7,9) anomaly** — at 4-element level this multiset is a
   trefoil-equivalent without BREATH. The "trefoil = needs BREATH" rule
   is 3-element-specific. Investigate further.

4. **Burrin-von Essen explicit Fuchsian-group lift** — substrate's BHML
   period structure structurally analogous to their cusp winding, but the
   embedding in a Fuchsian group is unproven.

---

## §6 Tone for integration

When you write into the repo, be honest like the synthesis docs are honest:

- **Don't overclaim.** Where I had to demote claims (Fibonacci is fragile,
  not structural; 5↔6 is one of many partial symmetries; ±21 modular
  interpretation is hypothesis), keep them demoted.

- **Don't inflate.** Brayden has been explicit about wanting accurate
  representation, not over-decoration.

- **Cite carefully.** The literature scaffolds the framework; it doesn't
  prove its theorems. Phrases like "structurally analogous to" and
  "conceptually scaffolded by" are accurate. Phrases like "matches" or
  "satisfies the [theorem]" are usually not.

- **Preserve the negatives.** The ten honest negatives sharpen what TIG
  IS by establishing what it ISN'T. They belong in the docs.

---

## §7 If something breaks

If you find:
- A computation that doesn't reproduce → check if I used wrong frame
  (TSML_10 vs TSML_8) or wrong bridge variant
- A claim that contradicts substrate axioms → flag it for Brayden, don't
  paper over
- A finding that depends on a Reading A heuristic (the (p,q) winding
  assignments I had) → those were stripped per Brayden's instruction;
  any remaining traces need cleanup
- A numerical coincidence I claimed was structural → verify with random
  tables before integrating

---

## §8 Critical context

Brayden has been building this for ~2 years independently, recently
dissolved a 3-person team to go solo. He's planning IHÉS / Institut Henri
Poincaré presentation. Daughter's birthday Sept 11, Oxford Clay conference
12 days later. The mathematics needs to hold up to mathematician scrutiny.

His posture: "hat in hand," choosing to observe rather than dominate. He
identifies as the LATTICE — the framework that enables without controlling.
This means the integration into the repo and CK should be PRECISE and
HONEST, never decorative or self-aggrandizing. If the math is real, it
will show. If a finding is fragile, say so.

The bridge research stands inside arithmetic-topology / modular-knot
territory. Morishita 2024 (2nd ed), Ghys ICM 2007, Katok-Ugarcovici 2007,
Matsusaka-Ueki 2023, Burrin-von Essen 2024 are the intellectual
neighborhood. TIG is a specific construction within that territory, not a
restatement of any of those theorems.

---

## §9 Order of operations

```
1. Read this document fully.
2. Read OUT_OF_ROPE_FINAL.md (master synthesis).
3. Read KNOWN_ISSUES.md and VERIFICATION_PROTOCOL.md.
4. Run verify_findings.py.
5. If pass: proceed to integration.
   If fail: STOP, report, do not integrate.
6. Phase 2 (repo) before Phase 3 (CK) — repo is canonical.
7. Update INDEX.md and SYNTHESIS.md if new findings warrant.
8. Tag DOI version increment if substantial canonical changes.
```

---

## §10 What this is NOT

- NOT a finished bridge paper. The bridge papers themselves still need to
  be written (handoffs are plans).
- NOT proof that ±21 is a Rademacher invariant. That's a hypothesis with
  one supporting lift (period→trace under simple representative).
- NOT a literal arithmetic-topology Borromean-prime structure on TIG.
  Verified empirically that it's not.
- NOT exhaustive of substrate properties. Open questions remain (variants,
  larger substrates, principled lifts).
- NOT to be trusted blindly. Verify before integrating.

---

End of master handoff document.
