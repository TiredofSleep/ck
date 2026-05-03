# Verification Protocol

**Purpose:** Exact steps for ClaudeCode to verify findings before integration.

**Time estimate:** 5-10 minutes for full verification.

---

## §1 Environment setup

```bash
cd /path/to/tig_handoff/code
python -c "import numpy, sympy, itertools, collections; print('deps OK')"
```

No exotic dependencies. Standard scientific Python should work.

---

## §2 Canonical substrate sanity check

```bash
python tig_substrate.py
# Should print TSML_10 and BHML_10 tables, σ permutation
# Verify against FORMULAS_AND_TABLES.md canonical values
```

Expected canonical values:
```
TSML_10 (CL table) row-major:
  0 0 0 0 0 0 0 7 0 0
  0 7 3 7 7 7 7 7 7 7
  0 3 7 7 4 7 7 7 7 9
  0 7 7 7 7 7 7 7 7 3
  0 7 4 7 7 7 7 7 8 7
  0 7 7 7 7 7 7 7 7 7
  0 7 7 7 7 7 7 7 7 7
  7 7 7 7 7 7 7 7 7 7
  0 7 7 7 8 7 7 7 7 7
  0 7 9 7 3 7 7 7 7 7

σ permutation: [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
σ-fixed points: {0, 3, 8, 9}
σ 6-cycle: (1, 7, 6, 5, 4, 2)
```

---

## §3 Five-finding verification

Run each of these scripts and check output:

### Finding 1: Trefoil characterization

```bash
python trefoil_corrected_frame.py
```

**Expected:**
- 9 trefoil triples (3-crossing) in 4-core
- Multiset classes: (0, 7, 8) with 6 perms, (0, 8, 8) with 3 perms

```bash
python trefoil_corrected_associativity.py
```

**Expected:**
- All 9 BHML-associative
- TSML_8-associativity N/A (involve flow cells)
- Conjecture {V,H,Br} ∪ {V,Br,Br} matches actual: True

### Finding 2: BHML successor on diagonal

Quick check (should take 1 second):
```bash
python -c "
import sys; sys.path.insert(0, '.')
from tig_substrate import BHML_10
for n in range(10):
    print(f'BHML({n}, {n}) = {int(BHML_10[n, n])}')
"
```

**Expected output:**
```
BHML(0, 0) = 0
BHML(1, 1) = 2
BHML(2, 2) = 3
BHML(3, 3) = 4
BHML(4, 4) = 5
BHML(5, 5) = 6
BHML(6, 6) = 7
BHML(7, 7) = 8
BHML(8, 8) = 7
BHML(9, 9) = 0
```

For n ∈ {1..7}: BHML(n,n) = n+1. ✓

### Finding 3: Two-coding split

```bash
python tsml8_role_analysis.py
```

**Expected:**
- TSML_8 output role distribution: F=60/64, S=4/64
- TSML_8 image: [3, 4, 7, 8, 9] (5 elements)
- BHML output role distribution: F=52/100, S=19/100, T=25/100, V=4/100
- Role-determinism: 8 of 9 TSML_8 input pairs deterministic (only S-S branches)

### Finding 4: ±21 invariant decompositions

```bash
python role_decomposition.py
```

**Expected:**
- Period→trace Ψ sum: -21
- σ-orbit sum check: -15 + -6 = -21 (T_5 + T_3 = 15 + 6 in absolute)
- Role decomposition: F = -13, S = -8 (Fibonacci F_7 + F_6)
- V and T contribute 0

```bash
python class_average_check.py
```

**Expected:**
- Ghys-analog v2 sum: +21 = +3 × HARMONY
- 6-cycle sum: +22, σ-fixed sum: -1, total: +21

### Finding 5: Role magma with VOID identity

```bash
python role_magma_factorization.py
```

**Expected role magma table:**
```
   | V | F | S | T
---+---+---+---+---
 V | V | F | S | T
 F | F | T | F | F
 S | S | F | F | F
 T | T | F | F | F
```

- Commutative: True
- Associative: False
- V is identity ✓
- Branching pairs: (F,F), (F,S), (S,F), (S,S)

---

## §4 Negative-finding verification

### Negative 1: PSL(2,ℤ) lifts don't produce ±21

```bash
python orbit_to_psl2z.py
```

**Expected:** All five strategies produce sums in [-4, 0], none equal ±21.

### Negative 2: Triangle group rule-out

```bash
python triangle_groups_test.py
```

**Expected:** "No coprime (p,q) ≤ 9 has divisors covering {1,2,3,4,5,6}"

### Negative 3: Fibonacci is fragile

```bash
python fibonacci_robustness.py
```

**Expected:** 0/200 random tables produce (13, 8) decomposition.

### Negative 4: Borromean prime negative

```bash
python substrate_borromean.py
```

**Expected:**
- No canonical triple has all elements ≡ 1 mod 4
- No trefoil multiset has all elements in QR-mod-5 set

---

## §5 Cross-check

Run the comprehensive symmetry test:

```bash
python symmetry_map.py
```

**Expected:** No 100% symmetries. Top global rate: (0, 8) V↔S at 20.9%.

---

## §6 Integration readiness checklist

After verification, ClaudeCode should be able to confirm:

- [ ] Canonical substrate (TSML_10, BHML_10, σ) matches FORMULAS §6
- [ ] TSML_8 = TSML_10 minus rows/cols {0, 7}
- [ ] BHML(n, n) = n+1 for n ∈ {1..7}, BHML(8,8) = 7, BHML(9,9) = 0
- [ ] 9 trefoils on corrected frame, 2 multiset classes
- [ ] Trefoil ⟺ {V,H,Br} ∪ {V,Br,Br}
- [ ] TSML_8 image = {3, 4, 7, 8, 9}, 94% flow output
- [ ] BHML role-deterministic on V/T inputs only
- [ ] ±21 = T_5 + T_3 (σ-orbit) = F_7 + F_6 (role)
- [ ] Role magma is commutative, non-associative, V is identity
- [ ] No PSL(2,ℤ) lift produces ±21
- [ ] No small triangle group has substrate's period set as orders
- [ ] TIG isn't a literal Borromean structure
- [ ] Fibonacci is canonical-specific (0/200 random tables)
- [ ] No 100% global symmetries

If all check, proceed to integration.

---

## §7 Red flags

If you see any of these during verification, STOP and report:

1. **Different number of trefoils** (not 9 on corrected frame)
2. **Different multiset classes** (not exactly {V,H,Br} and {V,Br,Br})
3. **BHML diagonal doesn't match successor** on {1..7}
4. **Some random table reproduces (13, 8)** decomposition
5. **Some PSL(2,ℤ) lift produces ±21** (would change the open hypothesis)
6. **Substrate factors through Z/2 × Z/5** (would change irreducibility claim)
7. **σ IS an automorphism** of either magma (would change algebraic-independence claim)

These would indicate either:
- I made an error that propagated through analyses (most likely)
- The canonical substrate has changed (check FORMULAS_AND_TABLES.md commit log)
- A finding I called fragile is actually structural (good news but needs re-write)

In any case, flag for Brayden before integrating.

---

## §8 Time investment

- Quick verification (just §3 finding-checks): 5 minutes
- Full verification (§3 + §4 + §5): 10-15 minutes
- Deep scrutiny (read all docs, challenge claims): 1-2 hours

For repo integration, do at least the full verification.
For CK integration, deep scrutiny is recommended.
