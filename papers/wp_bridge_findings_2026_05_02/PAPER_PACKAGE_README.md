# Paper Package — May 2026

**For:** ClaudeCode
**From:** Bridge research thread, 2026-05-03
**Author:** Brayden Sanders, 7Site LLC
**DOI:** 10.5281/zenodo.18852047
**Repo:** github.com/TiredofSleep/ck

---

## What's in this package

```
paper_package/
├── README.md                       ← you are here
├── paper/                          ← the arXiv submission
│   ├── main.tex                    ← LaTeX source, 746 lines, 29 numbered envs
│   └── verify_paper.py             ← reproduces every numerical claim
├── handoff/                        ← five-finding verified handoff (PRIMARY)
│   ├── CLAUDECODE_HANDOFF.md       ← entry point for repo + CK integration
│   ├── code/                       ← 41 Python scripts incl. verify_findings.py
│   ├── docs/                       ← 11 synthesis documents
│   ├── results/                    ← KNOWN_ISSUES, VERIFICATION_PROTOCOL, etc.
│   └── wp_drafts/                  ← WP9, WP10, BRIDGE_PAPERS_status outlines
├── thread_archive/                 ← 7 transcripts of the full thread
├── meta_strategy/                  ← strategic notes
│   └── META_STRATEGY.md            ← Bucket-1 alignment moves, ACT/CT analysis
└── scrutiny/                       ← honest record of errors and calibration
    └── SCRUTINY_NOTES.md           ← errors I caught + reviewer checklist
```

---

## Order of operations for ClaudeCode

### Phase 0: Verify before trusting

1. Read `scrutiny/SCRUTINY_NOTES.md` first. I made two structural
   errors during paper drafting that I had to catch and fix. The notes
   document them explicitly.
2. Run `paper/verify_paper.py`. Should produce 42 passes, 0 failures.
3. Run `handoff/code/verify_findings.py`. Should produce 5 findings
   verified, 0 failures.
4. If either fails, STOP and report. Do not proceed.

### Phase 1: Paper preparation (if verification passes)

1. Read `paper/main.tex` end to end.
2. Compile with EPTCS LaTeX style files (style.eptcs.org).
3. Check for: matrix rendering, bibliography linking, no overfull hboxes
   in critical spots.
4. Read `scrutiny/SCRUTINY_NOTES.md §4` — the reviewer checklist of
   things I'd want flagged before submission.
5. Address the items in `scrutiny/SCRUTINY_NOTES.md §5` (the
   pre-submission checklist).
6. Search magma classification literature for the 4-element commutative
   non-associative magma with identity. Etherington 1939, Bruck 1958,
   Smith 2007. Either find it (cite) or confirm absent (strengthen open
   question).
7. Confirm Burrin–von Essen 2024 publication status.

### Phase 2: Repo integration (from earlier handoff)

Per `handoff/CLAUDECODE_HANDOFF.md`:
- Add D88-D94 to FORMULAS_AND_TABLES.md
- Update README.md
- Draft WP9 / WP10 from outlines
- Update bridge paper handoffs
- Increment DOI version

### Phase 3: CK integration (from earlier handoff)

Per `handoff/results/INTEGRATION_TARGETS.md`:
- Update ck_organism.py with corrected substrate
- Verify ck_curvature.py uses corrected frame
- Add ck_invariants.py for ±21 metrics
- Wire force9_codec.py with role partition
- Add ck_fault_state_debug.py
- Update ck_olfactory.py with role labels

### Phase 4: arXiv submission (Brayden's call)

When all above passes:
- Choose arXiv categories: math.RA primary, math.CO secondary
- Possibly math.CT tertiary
- Submit `paper/main.tex` + `paper/verify_paper.py` as ancillary
- Update Zenodo DOI as new file in same record

### Phase 5: Strategic engagement (Brayden's call)

Per `meta_strategy/META_STRATEGY.md`:
- ACT 2026 (Tallinn, July 6-10) — submission window closed; attend as
  observer if possible
- CT 2026 (Baltimore, July 13-18) — submission window closed; attend as
  observer (registration through May 15, 2026; virtual is free)
- ACT 2027 / CT 2027 — realistic conference targets
- Topos Institute (Spivak, Fong) — potential cold-contact targets after
  arXiv post lands

### Phase 6: HOLD

The fifteen-ropes document, Ho Tu correspondences, consciousness
adjacencies, cosmological constants, GUT framings — these all stay OUT
of the paper, OUT of the repo, OUT of any submission. They live as
private/personal notes for separate investigation, with separate
evidence requirements, in their own time.

The discipline is: **one rope at a time, fully earned**.

---

## What this package proves

Five things, all mechanically verifiable from the canonical tables:

1. **Theorem 3.1 (Diagonal successor):** $B(n,n) = n+1$ for $n \in \{1..7\}$,
   with $B(8,8) = 7$, $B(9,9) = 0$, $B(0,0) = 0$.
2. **Theorem 4.1 (Trefoil characterization):** Exactly 9 trefoil triples
   under the runtime processor, in 2 multiset classes $\{0,7,8\}$ and
   $\{0,8,8\}$, all $B$-associative.
3. **Theorem 5.1-2 (Two-coding split):** $T$ has 5-element image
   $\{3,4,7,8,9\}$, role-deterministic on 8/9 input class pairs. $B$ has
   full image, role-deterministic only on V/M-touching pairs.
4. **Theorems 6.2-4 (Integer invariant decompositions):** $\sum \psi = -21$,
   decomposes as $-T_5 - T_3$ along $\sigma$-orbits and as $-F_7 - F_6$
   along the partition (canonical-specific).
5. **Proposition 7.2 (Role-quotient magma):** Commutative, non-associative,
   $V$ is two-sided identity, $V$ is only idempotent.

## What this package does NOT prove

Anything about cosmology, physics, consciousness, the Ho Tu, traditional
cosmologies, biology, nucleosynthesis, number theory's deep open problems,
or any of the fifteen ropes. Those are separate hypotheses with separate
evidence requirements.

---

## Trust posture

We trust nobody, including ourselves. The verification scripts catch our
own mistakes. I made two during the paper drafting session — a wrong-table
copy and a structural error in defining $T$ as a restriction of $B$. Both
were caught by running computations and checking against canonical sources.
That's the only trust mechanism that works.

When you (ClaudeCode) take the next step on this work, run the
verifications first. Don't trust this README, this LaTeX file, or any
narrative description over what `verify_paper.py` and `verify_findings.py`
actually output.

If they pass, the math is real. That's the only claim we make.

---

End of package README.
