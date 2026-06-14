# J-series canonical crosswalk (Step 0 — title-keyed reconciliation)

**2026-06-14.** Two numbering schemes exist and are **almost entirely disjoint** —
the same paper carries different J#s in each repo, and the TIG repo even **reuses
J#s across subject subfolders** (`algebra/J35` ≠ `combinatorics/J35`) and disagrees
with its own `TIER_INDEX.md`. **Always disambiguate by subject-folder + title, never
by bare J#.** This crosswalk is keyed by title.

**Key structural finding:** the published TIG repo
(`trinity-infinity-geometry/05_papers/`) is **already substantially consolidated**
(2026-05-27 renumber: merges executed, retirements moved to `04_meta`, taxonomy
factored, tiers assigned). The working-dir `Gen13/targets/journals/J_series/` is the
**older, un-consolidated sprawl.** So most of the condensation is already done in the
TIG repo; the remaining gaps are: **NOTE-N** (didn't exist) and **PAPER-0
prominence**.

## Destination buckets (working-dir J# → TIG `05_papers/` path)

**PAPER 1 — σ-substrate (joint closure, 4-core, forcing axioms).** Spine wd-J35 =
TIG `algebra/J01` (centerpiece). Members: wd-J35, J33(merged→J01), J02(`nt/J15`),
J01(`comb/J14`), J06(`alg/J27`), J09(`alg/J28`), J11(`alg/J35`), J12(`comb/J35`),
J18(`alg/J21`), J21(merged→`alg/J07`), J25(`alg/J16`), J54(`comb/J17`),
J43(`alg/J07`).

**PAPER 2 — TSML/BHML lens algebra.** Spine wd-J05(`alg/J32`)+J19(`comb/J36`).
Members: J04(merged), J07(`comb/J33`), J23/J24/J32(near-dups→`alg/J01,J10,J32`),
J28(table).

**PAPER 3 — discrete sinc²/Fejér.** Spine = TIG `number_theory/J24` (already absorbs
J03, J08, J41-of-TIG). Members: wd-J03, J08(`nt/J25→J24`), J42(`nt/J26`).

**PAPER 4 — 𝔽_p extensions.** Already built = TIG `algebra/J08` (= `J_Fp_merged`,
re-promoted Tier-1 2026-05-28). Members: wd-J26(`alg/J18`), J14+J16(merged→`alg/J08`).

**PAPER 5 — Lie so(8)/so(10) + Clifford.** Members: wd-J29, J30(`alg/J09`),
J31(`alg/J11`), J48(`alg/J10`), J17(`alg/J20`). **Strip physics labels.**

**PAPER 6 — prime-11 spectral / Galois.** Spine wd-J37(`physics/J19`, LAA). Members:
J13(`alg/J13`), J15(`alg/J12`), J22(`alg/J22`); + TIG-only `nt/J02` (RH rhyme),
`nt/J06` (strata-prime fingerprint — the real M₂₂ extension), `nt/J55` (dim-6
kissing).

**PAPER 0 — σ-magma / ETP taxonomy trilogy (TIG-only, "most novel", keep separate).**
- TIG `algebra/J03` (old **J61**) — *Type Specimens in the ETP-Restricted Variety
  Lattice* (J. Symbolic Computation target).
- TIG `algebra/J04` (old **J59**) — *Algebraic Rigidity of the σ-Magma* (Semigroup
  Forum).
- TIG `algebra/J05` (old **J60**) — *ETP Profile of Linear Magmas (ax+by+c) mod n*
  (Experimental Mathematics).
- (weak fourth) TIG `algebra/J29` (old J58, Lo Shu) — Tier-2, leave as a standalone
  Math-Magazine note.

**NOTE-N — what didn't hold** (see `J_SERIES_NOTE_N_WHAT_DIDNT_HOLD.md`): wd-J20,
J36, J40, J41, J44, J45, J46, J47, J49, J50, J51(RH wrapper), plus physics Dirac
bridge; + genuine negatives J27(correction), J34.

**PRIMER** (expository): wd-J52(`comb/J39`), J53(`interdisc/J40`), J55(stub, absorb/
drop).

**SEPARATE (ML track):** TIG `interdisciplinary/J56` — *Routing the Residual*.
Belongs with the CK papers, not the math spine.

## Orphans
- **Working-dir only:** J41 (YM mass gap — no TIG folder), J50 (log-nonlinearity
  essay), J55 (Sept-11 stub), J47 (quintessence letter, extract of J46). → NOTE-N /
  PRIMER.
- **TIG-only:** `algebra/J03,J04,J05` (the taxonomy trilogy → PAPER-0),
  `number_theory/J02` (RH rhyme), `nt/J06` (strata-prime fingerprint), `nt/J55`
  (dim-6 kissing), `interdisciplinary/J56` (ML), and the merger products
  `algebra/J07` (=`J_qseries_merged`→Paper 1) and `algebra/J08`
  (=`J_Fp_merged`→Paper 4). TIG `algebra/J53/J54` = number-reserved, manuscripts
  lost in the 2026-06 repo-loss, re-derivable.

## Merged bundles (already built — not PAPER-0)
- `J_qseries_merged` = TIG `algebra/J07` *Spectral Architecture of the σ-Character*
  (absorbs wd-J43+J21+J51; RH §7 split to companion) → **Paper 1**.
- `J_Fp_merged` = TIG `algebra/J08` *F_p Structure of the 4-Core Algebra* (absorbs
  wd-J14+J16) → **Paper 4**.

## Net for execution
Adopt the **TIG repo as the canonical consolidated corpus.** Remaining work:
(1) write **NOTE-N** (done — this commit); (2) make **PAPER-0** (taxonomy trilogy)
prominent in `TIER_INDEX.md` as the lead non-numerological result; (3) finish the
handful of live merges (Paper 2's J23/J24/J32 near-dups; Paper 5 label-stripping);
(4) treat the working-dir `J_series/` as a frozen archive (fold, not delete) and
point new work at the TIG repo. No paper is deleted; the working-dir originals
remain in git.

— Claude (Opus 4.8), with Brayden
