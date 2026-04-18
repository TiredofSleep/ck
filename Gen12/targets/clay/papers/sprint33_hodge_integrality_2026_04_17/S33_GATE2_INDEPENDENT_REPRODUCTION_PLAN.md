# S33 Gate 2 — Independent Reproduction Plan

**Sprint:** 33 (Hodge Integrality)
**Gate:** 2 (independent first-principles reproduction)
**From:** ClaudeCode
**To:** Brayden + ChatGPT + ClaudeChat
**Date:** 2026-04-18
**Scope:** Rebuild the S33 construction from atlas definitions only, without referring to `probe_hodge_integrality_v2.py` or the S29 R1-KE code, and confirm the same verdict independently.

**Prerequisite:** S33 Gate 1-full PASS (`S33_CONSTRUCTION_AUDIT.md`).

**Status:** PLAN (not yet executed). Can run in parallel with Sprint 35a.

---

## §0. One-sentence charter

**Reproduce the $W_* \cap \mathbb{Q}^{70} = \{0\}$ verdict from first principles, using only the atlas definitions of $A_*$, $\varphi$, $J_\Omega$, $L$, so that any unintended dependency between the probe code and the S29 R1-KE machinery is caught before Gate 3 (external audit).**

---

## §1. Why Gate 2 matters

Gate 1A confirmed construction; Gate 1-full resolved all five open mathematical questions. But:

- `probe_hodge_integrality_v2.py` was written by one author (ClaudeCode), against one specification (`S33_HANDOFF_TO_CLAUDECODE.md`).
- The S29 R1-KE memo (`sprint29_hodge_r1_kequivariant_2026_04_17/R1_KEQUIVARIANT_CLOSURE_MEMO.md`) was written by the same author.
- A subtle **shared error** — e.g. a sign convention, an indexing mismatch, a basis ordering — could pass through both files undetected.

Gate 2 catches this by rebuilding the probe from scratch with different conventions and comparing.

---

## §2. Differences from v2

Gate 2 must differ from v2 in **at least 3 independent ways** so any shared error becomes visible:

1. **Different basis ordering for $H^4$:** v2 uses `list(combinations(range(8), 4))` in lex order. Gate 2 uses a Hamming-weight-sorted or reverse-lex order. If the rank computation depends on basis ordering (it shouldn't, but a bug could introduce dependence), Gate 2 would diverge.

2. **Different construction of $J_\Omega$:** v2 builds $J_\Omega$ from the block formula. Gate 2 builds $J_\Omega$ from the period map directly:
   $$J_\Omega = P \cdot \operatorname{diag}(i, i, i, i, -i, -i, -i, -i) \cdot P^{-1}$$
   where $P$ is the $8 \times 8$ real matrix mapping the $H^{1,0}$ basis to the standard $\mathbb{R}^8$ basis.

3. **Different algebraic arithmetic:** Gate 2 uses `sympy.AlgebraicField(sqrt(2), sqrt(3), sqrt(5))` instead of a hand-rolled 8-tuple (Sprint 35a) or PSLQ (v2). sympy's AlgebraicField is a completely different backend.

4. **Different rank algorithm:** v2 uses mod-$p$ Gaussian elimination. Gate 2 uses `sympy.Matrix.rank()` directly (fraction-free over ℚ). Slow but independent.

If Gate 2 yields rank = 70, the result is robust against all 4 implementation differences.

---

## §3. Gate 2 deliverables

### §3.1 `probe_gate2_independent.py` (~400 LOC)

**Inputs:** same atlas definitions (Ω, M₂, M₃, polarization).

**Outputs:**
- `gate2_verdict.json` with rank over ℚ computed 4 different ways:
  (a) sympy AlgebraicField + sympy Matrix rank
  (b) sympy expressions + sympy Matrix rank (redundant but tests AlgebraicField)
  (c) mod-p rank with 5 primes (matches v2's method, must agree)
  (d) Custom 8-tuple + mod-p rank (matches Sprint 35a's method, must agree)

All four must produce rank = 70.

### §3.2 `gate2_comparison_memo.md`

Side-by-side table comparing v2 output, v3 output (from S35a), and Gate 2 output (a/b/c/d), with any discrepancies flagged. Expected: all 6 results agree.

### §3.3 Basis convention audit

Document each basis ordering explicitly:
- $H^4$ basis: lex / Hamming-weight / reverse-lex
- Galois basis of $\mathbb{Q}(\sqrt{2},\sqrt{3},\sqrt{5})$: bit-indexed (S35a convention) / lex on $(\sqrt{2}^a \sqrt{3}^b \sqrt{5}^c)$
- Hodge decomposition ordering $H^{1,0}$ vs $H^{0,1}$: convention fixed and documented

---

## §4. Failure modes and triage

If Gate 2 **agrees** with v2/v3 → S33 is robust, proceed to Gate 3 (external).

If Gate 2 **disagrees**:
- (a) Gate 2 gives different rank — investigate which of v2/v3/G2 has the bug.
- (b) Gate 2 gives same rank but different kernel → basis convention issue, likely benign.
- (c) Gate 2 fails to terminate → sympy AlgebraicField performance issue; fall back to approach (d).

**Triage protocol:**
1. Check basis ordering consistency first.
2. Check sign conventions on $\varphi$ vs $J_\Omega$.
3. Check polarization sign (Hodge–Riemann might enter with $(-1)^{p+q}$ factor).
4. If still disagreement, flag to ChatGPT + ClaudeChat for external fresh eyes.

---

## §5. Gate 3 prerequisites (not part of Gate 2)

After Gate 2 passes:
- **Gate 3a** — external mathematician reproduces construction independently (human review).
- **Gate 3b** — full write-up of construction + verdict goes into journal submission.
- **Gate 3 triggers atlas status change** from `[gold-with-gap]` to `[fire]`.

---

## §6. Estimated effort

- Writing `probe_gate2_independent.py`: ~6 hours (with Sprint 35a's Q235 code as reference).
- Running + verifying: ~1 hour.
- Writing `gate2_comparison_memo.md`: ~2 hours.
- **Total:** ~1 day.

---

## §7. Interface with other sprints

- **S33 Gate 1-full:** PASSED. Gate 2 builds on this.
- **Sprint 35a:** running in parallel. Shares the mathematical content but different code. If S35a v3 passes, it provides one of Gate 2's four methods (d). Cross-reference reduces total Gate 2 effort.
- **Sprint 35b:** independent of Gate 2; can run in parallel.
- **Gate 3 (external review):** downstream.

---

## §8. What Gate 2 does NOT do

- Does NOT re-prove the S29 R1-KE theorem (takes it as a black box — audited in Gate 1-full §4).
- Does NOT construct $C_*$ (that's Sprint 35b).
- Does NOT submit to journal (that's Gate 3).
- Does NOT change any atlas status.

---

## §9. Routing

**Action requested:**

1. Brayden — confirm Gate 2 spec above, green-light execution.
2. ChatGPT — review the 4-method verification plan, flag any redundancy or missing cross-check.
3. ClaudeCode — once green-lit, write `probe_gate2_independent.py` and report verdict.

---

## §10. One-sentence charter

**Gate 2 rebuilds the S33 probe using four independent methods (sympy AlgebraicField, sympy expression, mod-p, custom 8-tuple) from atlas-only definitions, so any implementation-shared error between v2 and the S29 R1-KE memo would produce a visible discrepancy.**

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*
