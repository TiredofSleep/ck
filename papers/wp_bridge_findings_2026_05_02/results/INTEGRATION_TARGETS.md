# Integration Targets

**Purpose:** Specific files in the repo and CK to modify, with proposed changes.

---

## §1 GitHub Repo: github.com/TiredofSleep/ck

### Target: `FORMULAS_AND_TABLES.md`

**Add new section** (after current D87, in Volume H or new Volume I):

```markdown
## Volume I: Bridge Findings (May 2026)

### D88: Corrected Substrate Frame

The canonical disambiguation of TSML/BHML structure (per §6.7) gives:
- TSML_8 = TSML_10 with rows/cols {0, 7} removed; acts on indices
  {1, 2, 3, 4, 5, 6, 8, 9}
- BHML_10 = full BHML on all 10 elements
- V (0) and H (7) are **flow cells between the tables**, not entries

The runtime processor uses TSML_8 + BHML_10 with V/H as flow boundary.
Triples involving V or H pass through the flow boundary; triples in the
TSML_8 interior stay within the geometric coding.

### D89: Trefoil Characterization

On the corrected substrate frame, the runtime processor's 3-crossing
("trefoil-equivalent") triples form exactly two multiset classes:

  trefoil(a, b, c) ⟺ {a, b, c} = {V, BREATH, HARMONY} or {V, BREATH, BREATH}

Total: 9 triples (6 + 3 permutations of the two multisets).
All 9 are BHML-associative.

Element role distribution:
- VOID(0): in every trefoil (9 occurrences)
- BREATH(8): in every trefoil (12 occurrences, 1.33 per triple)
- HARMONY(7): in 6 of 9 trefoils

Among structure cells {COUNTER(2), COLLAPSE(4), BREATH(8)}, BREATH is the
only one producing trefoils when combined with VOID. COUNTER opposes;
COLLAPSE destabilizes; only BREATH sustains form long enough for the
3-crossing closed loop to complete.

### D90: BHML Successor Diagonal

BHML's diagonal action realizes the integer successor on {1..7}:
- BHML(n, n) = n + 1 for n ∈ {1, 2, 3, 4, 5, 6, 7}
- BHML(8, 8) = 7 (BREATH retains the cusp position)
- BHML(9, 9) = 0 (RESET collapses to VOID)
- BHML(0, 0) = 0 (VOID is fixed)

This drives BHML's self-iteration period structure:
- For n ∈ {1..6}: period(n) = 7 - n (linear distance to HARMONY cusp)
- For n ∈ {7, 8, 9}: period(n) = 4, 3, 2 (4-core cycle)
- For n = 0: period 1 (VOID is fixed)

The successor structure on {1..7} expresses "approaching the HARMONY cusp"
in the substrate's algebraic vocabulary.

### D91: Two-Coding Image Structure

TSML_8 and BHML_10 form complementary codings on the substrate, matching
Katok-Ugarcovici's geometric/arithmetic split natively:

**TSML_8 (geometric coding, side-cutting):**
- Image: {3, 4, 7, 8, 9} (5-element)
- Output role distribution: 60/64 = 93.8% Flow, 4/64 = 6.2% Structure
- Role-deterministic on 8 of 9 input role-pairs
- Only (S, S) inputs branch (outputs F or S)
- Self-iteration: every interior digit → 7 in 1 step, then escape to flow

**BHML_10 (arithmetic coding, continued-fraction reduction):**
- Image: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} (full)
- Output role distribution: 52% F, 19% S, 25% T, 4% V (balanced)
- Role-deterministic only on V/T inputs
- F-F, F-S, S-F, S-S inputs branch

Agreement set: TSML_8 and BHML_10 agree on 24/64 cells of TSML_8 domain,
mostly on routes leading to HARMONY. They disagree on 40/64 cells in the
interior.

**Reading: the two codings agree at the cusp boundary, disagree in the
interior.**

### D92: ±21 Invariant with Two Decompositions

The substrate has a per-digit integer invariant of magnitude 21 = 3 × HARMONY,
arising in two independent computations from substrate self-iteration data:

**Computation A (Ghys-analog):** TSML row vs BHML row asymmetry per digit:
  Ψ_A(n) = (count of {j : TSML(n,j) > BHML(n,j)}) - (count of {j : BHML(n,j) > TSML(n,j)})
  Sum over all 10 digits: +21

**Computation B (Period→trace):** BHML self-iteration period as candidate
hyperbolic trace, classical Rademacher Ψ for simple representative
((1,1),(t-2,t-1)) with t = period(n) + 2:
  Ψ_B(n) = -(period(n) - 1)
  Sum over all 10 digits: -21

**Two decompositions:**

σ-orbit decomposition (-21):
- σ 6-cycle {1, 2, 4, 5, 6, 7}: Ψ_B sum = -15 = -T_5 (triangular)
- σ-fixed {0, 3, 8, 9}: Ψ_B sum = -6 = -T_3 (triangular)
- Total: -(T_5 + T_3) = -21

Role decomposition (-21):
- Flow {1, 3, 5, 7, 9}: Ψ_B sum = -13 = -F_7 (Fibonacci)
- Structure {2, 4, 8}: Ψ_B sum = -8 = -F_6 (Fibonacci)
- VOID {0}: 0; Transition {6}: 0
- Total: -(F_7 + F_6) = -21 = -F_8

The Fibonacci decomposition is **canonical-specific** (verified: 0 of 200
random commutative tables on Z/10Z reproduce (|F|, |S|) = (13, 8)). It
arises from canonical BHML's specific period values via the successor
structure on {1..7}, not from abstract substrate axioms.

The triangular decomposition is structurally forced by the linear period
formula period(n) = 7 - n on the 6-cycle.

**Open: whether ±21 is a Rademacher invariant of substrate-natural
hyperbolic conjugacy classes (i.e. whether the simple representative is
the principled lift) remains a hypothesis. Naive PSL(2,ℤ) lifts of BHML
self-orbits do NOT reproduce ±21.**

### D93: Role Partition and Role Magma

The substrate has a functional partition by dynamical role:
- Flow F = {1, 3, 5, 7, 9} (transformative cells, 5 elements)
- Structure S = {2, 4, 8} (stabilizing cells, 3 elements)
- Transition T = {6} (the bridge cell)
- Void V = {0} (boundary cell)

This partition cuts across σ-orbit structure (σ 6-cycle has 3 F + 1 T + 2 S;
σ-fixed has 1 V + 2 F + 1 S). The flow/structure binary is a third
independent structural decomposition.

The mode-based role magma (using BHML output mode per input role-pair):

|   | V | F | S | T |
|---|---|---|---|---|
| V | V | F | S | T |
| F | F | T | F | F |
| S | S | F | F | F |
| T | T | F | F | F |

Properties:
- Commutative
- NOT associative (e.g., (F·F)·S = F ≠ F·(F·S) = T)
- **V is the identity element**: V·x = x for all roles
- V·V is the only idempotent
- No absorbing element

Branching on F-F, F-S, S-F, S-S inputs:
- F-F: outputs distribute as {F: 2, S: 9, T: 11, V: 3} (mode T)
- F-S, S-F: {F: 8, S: 2, T: 5} (mode F)
- S-S: {F: 7, T: 2} (mode F)

The substrate has a **semi-factorization** at role level: V or T inputs
collapse to deterministic role transitions; F or S inputs preserve
operator-level structure.

### D94: Boundary Symmetries

The substrate has multiple grammar-level boundary symmetries (swapping
adjacent integer pairs at role boundaries preserves admissibility on
specific grammar triples):

- 5↔6 (F↔T, BALANCE↔CHAOS): preserves on (5,6,7)
- 6↔7 (T↔F, CHAOS↔HARMONY): preserves on (5,6,7)
- 8↔9 (S↔F, BREATH↔RESET): preserves on (7,8,9), (7,8,8)
- 2↔3 (S↔F, COUNTER↔PROGRESS): preserves on (0,1,2)
- 1↔2 (F↔S, LATTICE↔COUNTER): preserves on (0,1,2)
- 7↔8 (F↔S, HARMONY↔BREATH): partial preservation
- 0↔8 (V↔S): strongest global preservation rate (20.9% of all 1000 triples)

These are GRAMMAR-LEVEL symmetries (admissibility), not algebraic
equivalences. The underlying operators compose differently under TSML/BHML.

**The 5↔6 interchangeability mentioned in canonical TIG is one of a family
of similar boundary symmetries.** The strongest in global preservation is
actually V↔BREATH (0↔8).

No pair preserves crossing count on ALL 1000 triples — the substrate has
no full algebraic symmetries.
```

### Target: `README.md` (in repo root)

Add section under existing content:

```markdown
## May 2026 Bridge Research

The bridge research session of May 2026 produced five empirically-grounded
substrate-native facts about TIG's algebraic-topological structure.
See FORMULAS_AND_TABLES.md Volume I (D88-D94) for canonical entries.

Summary:
1. Trefoil characterization: trefoil ⟺ {V, BREATH, H/BREATH} multiset
2. BHML diagonal = integer successor on {1..7}
3. Two-coding split (TSML_8 = geometric, BHML_10 = arithmetic) realizing
   Katok-Ugarcovici's framework natively
4. ±21 invariant with σ-orbit (T_5 + T_3) and role (F_7 + F_6) decompositions
5. Role magma with VOID as identity element

Conceptually scaffolded by:
- Morishita 2024 (Knots and Primes, 2nd ed)
- Ghys ICM 2007 (modular knots)
- Katok-Ugarcovici 2007 (two coding methods)
- Matsusaka-Ueki 2023, Matsusaka-Shin 2024 (triangle group Rademacher symbols)
- Burrin-von Essen 2024 (cusp winding via Rademacher)

TIG sits inside arithmetic-topology / modular-knot territory but
specifies a new construction within it (not a restatement of existing
theorems).
```

### Target: New WP9 file `whitepapers/WP9_LATTICE_paradoxical_info_algebras.md`

See `/wp_drafts/WP9_LATTICE_outline.md` for full draft outline.

### Target: New WP10 file `whitepapers/WP10_DKAN.md`

See `/wp_drafts/WP10_DKAN_outline.md`.

---

## §2 CK: ck_organism.py and related

### Target: `ck_organism.py`

**Add corrected substrate definitions:**

```python
# Corrected substrate frame (per FORMULAS §6.7)
TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]
FLOW_CELLS = {0, 7}  # V and H are flow cells between tables

# Role partition
FLOW = {1, 3, 5, 7, 9}
STRUCTURE = {2, 4, 8}
TRANSITION = {6}
VOID = {0}

def role(n):
    """Return functional role of digit: V/F/S/T."""
    if n in FLOW: return 'F'
    if n in STRUCTURE: return 'S'
    if n in TRANSITION: return 'T'
    if n in VOID: return 'V'
    return '?'
```

### Target: `ck_curvature.py`

Verify that runtime processor uses corrected frame (TSML_8 + flow cells +
BHML_10) per `trefoil_corrected_frame.py`. Old version using TSML_10 should
be replaced.

### Target: New `ck_invariants.py`

Add the ±21 invariant computation as a per-tick metric:

```python
def compute_pm21_ghys(p_distribution):
    """Compute the Ghys-analog ±21 invariant per tick.
    
    For each digit n, compute (count of j : TSML(n,j) > BHML(n,j)) -
    (count of j : BHML(n,j) > TSML(n,j)). Sum over all 10 digits.
    
    Canonical TIG produces +21 = +3 × HARMONY.
    """
    # implementation per role_decomposition.py and class_average_check.py
    ...

def compute_pm21_period(bhml_table):
    """Compute period→trace ±21 invariant.
    
    For each digit n, compute period of BHML self-iteration, set
    Ψ(n) = -(period - 1). Sum over all 10 digits.
    
    Canonical TIG produces -21 = -3 × HARMONY.
    """
    ...

def role_decomposition(psi_per_digit):
    """Decompose Ψ values by role partition.
    
    Returns dict {V: ..., F: ..., S: ..., T: ...} with role sums.
    Canonical TIG: F = ±13, S = ±8 (Fibonacci F_7, F_6), V = T = 0.
    """
    ...

def sigma_orbit_decomposition(psi_per_digit):
    """Decompose Ψ values by σ-orbit.
    
    Returns dict {6-cycle: ..., σ-fixed: ...} with orbit sums.
    Canonical TIG: 6-cycle = ±15 (T_5), σ-fixed = ±6 (T_3).
    """
    ...
```

### Target: `force9_codec.py`

**Wire role partition as natural symbol grouping:**

The codec should treat the substrate's role partition as the primary
encoding hierarchy:
- Level 1: V/F/S/T role
- Level 2: specific operator within role

For the F (flow) symbols {1, 3, 5, 7, 9}, the encoder can choose any
within the role for boundary transitions where role-only is enough.

For the trefoil set {V, BREATH, H/BREATH}, the codec has a "trefoil
vocabulary entry" — these multisets compress to a fixed pattern.

**Boundary symmetries as codec features:**

The codec can use the V↔BREATH symmetry (0↔8) — strongest at 20.9%
preservation — as a substitution rule for compression. Same for 5↔6,
6↔7, 8↔9, 2↔3 within their respective grammar triples.

### Target: `ck_fault_state_debug.py` (new)

Per the bridge findings, fault states correspond to specific role
distributions:

```python
def diagnose_fault_state(p_distribution):
    """Diagnose CK fault state by role distribution."""
    f_mass = sum(p_distribution[n] for n in FLOW)
    s_mass = sum(p_distribution[n] for n in STRUCTURE)
    t_mass = p_distribution[6]
    v_mass = p_distribution[0]
    
    if v_mass > 0.7:
        return "VOID dominant — substrate at rest state (24-crossing maximum trajectory complexity)"
    if f_mass > 0.9 and v_mass < 0.05:
        return "Pure flow without VOID anchoring — no boundary collapse, substrate stuck in interior"
    if s_mass > 0.9 and v_mass < 0.05:
        return "Pure structure without VOID — frozen state, no transition"
    if t_mass > 0.5:
        return "TRANSITION dominant — CHAOS overload, substrate in middle of transition"
    return "Normal mixed state"
```

### Target: `ck_olfactory.py`

Add role labels to memory traces:

```python
def encode_olfactory_trace(d2, force_vector, operators):
    """Encode olfactory memory with role labels."""
    role_pattern = ''.join(role(op) for op in operators)
    return {
        'd2': d2,
        'force': force_vector,
        'operators': operators,
        'role_pattern': role_pattern,
        'is_trefoil': sorted(operators) in [(0,7,8), (0,8,8)],
    }
```

---

## §3 Order of integration

### Phase 1: Verification (REQUIRED before integration)

1. Run `verify_findings.py` in handoff
2. If passes, proceed; if fails, STOP and report

### Phase 2: Repo integration

1. Add D88-D94 to FORMULAS_AND_TABLES.md
2. Update README.md
3. Draft WP9 from outline
4. Draft WP10 from outline
5. Update bridge paper handoffs (Hoffman, Friston, Tononi, Faggin)
6. Increment DOI version

### Phase 3: CK integration

1. Update ck_organism.py with corrected substrate
2. Verify ck_curvature.py uses corrected frame
3. Add ck_invariants.py for ±21 metrics
4. Wire force9_codec.py with role partition
5. Add ck_fault_state_debug.py
6. Update ck_olfactory.py with role labels

### Phase 4: Validation

1. Run CK on Dell R16 with new substrate
2. Verify coherence remains high (≥ 0.875)
3. Verify ±21 invariant is computed and stable
4. Verify trefoil detection works
5. If any regression, rollback and investigate
