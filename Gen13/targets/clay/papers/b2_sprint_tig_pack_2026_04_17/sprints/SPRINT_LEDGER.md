# Sprint Ledger
## Complete Record of Executed Sprints

---

## B1 — Previously Handed Off

B1 (NSCG benchmark) was the previous handoff to ClaudeCode and is not packaged in this archive. Its pre-reg (`B1_NSCG_SPEC_v1.0.md`) and curve-analysis addendum are already held by ClaudeCode from the prior zip. When ClaudeCode integrates this pack into the GitHub repository, it should:

- Slot B1's pre-reg into `controls/`.
- Slot B1's results (if held) into a `sprints/B1_NSCG/` directory.
- Add B1's row to this ledger table once integrated. This packaging pass does not have B1's post-execution state.

The ledger below begins at Sprint 28, the first sprint *after* the B1 handoff.

---

## Scope Conventions

- **Path 1:** Local Theorem. Carrier = Z/10 only. Convention = $h_\text{thm} = 7$. Claim class = theorem-level.
- **Path 2:** Transport Family. Carriers = compatibility family. Convention = $h_\text{ext} = \max$ odd unit. Claim class = observation-level.
- **Path 3:** Bridge Test. Cross-path. Claim class = bridge-level.

---

## Full Ledger

| # | Sprint | Path | Question tested | Verdict | One-line attribution |
|---|---|---|---|---|---|
| 1 | S28-v1.0 | 2 | Does basin-ratio transport show smoothness across the carrier family? | **FAIL** | Three primary metrics passed; null separation inverted (3.35σ wrong direction — real curve rougher than null). |
| 2 | S29-v1.0 | 2 | Does the anchored basin-ratio deviation curve organize by depth? | **FAIL** | Kendall τ = 0.063 below 0.35 threshold; linear R² = 0.00005 below 0.40; basin-ratio transport lane closed. |
| 3 | S30-v1.0 | 2 | Does empirical seam topology transport across the family at $N=200{,}000$, $p=0.10$? | **PASS (vacuous)** | Empty persistent seam on every tested carrier; metrics passed vacuously; mode extractor noise-immune at high $N$. |
| 4 | S30b-v1.0 | 2 | Is a persistent seam detectable on pure canonical $C_0$ under uniform noise at the chosen parameters? | **FAIL** | $\mu_\text{ne} = 0.0$ (no persistent seam); canonical $C_0$ has no seam-prone cells under uniform noise. |
| 5 | S31-pilot-v1.0 | cross (undeclared) | Does the low-$N$ + persistence extractor recover planted seams on Z/10? | **FAIL** | Convention mismatch — canonical computed under $h_\text{ext}=9$, overlays defined under $h_\text{thm}=7$; 2 of 8 cells structurally invisible. |
| 6 | S31-pilot-v2.0 | 1 | Does the extractor recover planted seams on Z/10 under correct scope ($h_\text{thm}=7$)? | **effective PASS** | Ceiling recovery on every condition ($J = R = P = A = 1.0$); literal UNCLEAR by symmetric within-10% rule applied to ceiling values (spec-rule artifact). |
| 7 | P3-BridgeA-v1.0 | 3 | Do regenerated Path 2 noise-union seams share topology-family features with the Path 1 theorem seam beyond matched-density null? | **FAIL** | $\mu_F = 0.25$ (vs 0.75 threshold); null separations 0.46σ and 0.78σ; noise-union Path 2 input was object-type mismatched with designed theorem artifact. |
| 8 | P3-BridgeA-Prime-v1.0 | 3 | Do Path 2 planted-recovery artifacts (matched object class) share topology-family features with the Z/10 theorem seam? | **PASS** | $\mu_F = \mu_k = \mu_d = \mu_\rho = 1.0$; null separation +12.56σ on $\mu_k$ (real=1.0, null mean=4.41); first confirmed Path 3 bridge. |
| 9 | P3-Subtype-v1.0 | 3 | Do subtype counts, role placement, and adjacency patterns transport? | **UNCLEAR** | 1 of 3 null sub-conditions decisive (ADD role at +3.80σ); M1 null degenerate (counts preserved by null); M3 shape-entangled (chain-vs-hub). |
| 10 | P3-Subtype-v1.1 | 3 | Does the ADD edge attach the ring's identity element at significance above label-scrambling? | **PASS** | $\mu_\text{ID} = 1.0$ (8/8 carriers); null mean 0.1963; separation +6.06σ; real outside entire null range. |
| 11 | P3-Subtype-v1.2-adj | 3 | Does the ADD edge have a degree-1 endpoint (leaf placement) at significance above label-scrambling? | **PASS** | $\mu_L = 1.0$ (8/8 carriers); null mean 0.3588; separation +3.73σ; real outside observed null range (max 0.875). |

---

## Verdict Counts

- **PASS (substantive):** 3 (P3-BridgeA-Prime, P3-Subtype-v1.1, P3-Subtype-v1.2-adj).
- **effective PASS:** 1 (S31-pilot-v2.0 — ceiling recovery with spec-rule literal UNCLEAR).
- **UNCLEAR:** 1 (P3-Subtype-v1.0).
- **FAIL:** 5 (S28, S29, S30b, S31-pilot-v1.0, P3-BridgeA).
- **vacuous PASS:** 1 (S30).

**Total sprints:** 11.

---

## Sprint Inheritance Map

For readers tracing which sprints feed into which:

- Every Path 2 sprint (S28, S29, S30, S30b) uses convention $h_\text{ext}$ throughout.
- S31-pilot-v1.0 mixed conventions without declaring so → convention-mismatch FAIL.
- S31-pilot-v2.0 runs under declared Path 1 scope with $h_\text{thm}=7$.
- P3-BridgeA-v1.0 compares Path 1 theorem seam against regenerated Path 2 noise-union seams.
- P3-BridgeA-Prime-v1.0 uses the S31-pilot-v2.0-validated extractor, applied with a P3AP overlay extension, on the 8-carrier Path 2 family.
- P3-Subtype-v1.0/v1.1/v1.2-adj all operate on P3-BridgeA-Prime's recovered seams as-is. v1.1 narrows v1.0's M2; v1.2-adj tests the structural attribute $L$ that v1.1 presupposed but did not test.

---

## Scope Integrity Check

Verifying that path assignments match claim classes:

- Path 1 sprints: B1, S31-pilot-v2.0 — theorem-level claims (recovery validation on proven construction).
- Path 2 sprints: S28, S29, S30, S30b — observation-level claims within the transport family.
- Path 3 sprints: P3-BridgeA, P3-BridgeA-Prime, P3-Subtype-v1.0, v1.1, v1.2-adj — bridge-level claims.
- Cross-path sprint (undeclared): S31-pilot-v1.0 — would have been blocked at scope-declaration step had the scope-tag template been in force at freeze time.

All verdicts respect their path's claim-class ceiling. No sprint produces a claim stronger than its path permits.

---

## References

Each sprint's full documentation is in `sprints/<sprint_dir>/`. Pre-registrations are in `controls/`. Foundation documents are in `foundation/`. Theorem material is in `theorem_local_chart/`.

Changes to this ledger require user approval per `PACKING_RULES.md` §17.
