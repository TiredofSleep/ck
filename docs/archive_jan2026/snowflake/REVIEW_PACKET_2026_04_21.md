# SNOWFLAKE External-Statistician Review Packet

**Status:** Hand-off-ready artifact. **No submission has been made** — this packet
is compiled for Brayden to hand to an external statistician of his choosing.
**Authored:** 2026-04-21 by ClaudeCode per `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §5.2.
**Branch:** `tig-synthesis` (this cover page) with source files on `master` and
`funding/tig-snowflake` (funding-specific artifacts, by design — see §4).
**Plan pointer:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §5.2

---

## 1 · What we are asking for

An external statistician's independent sign-off on **three specific things**:

1. **Null-hypothesis specification.** Does the stated H₀ — *"fires are
   uniformly distributed across 13 Tzolkin breath phases, p = 1/13 each"* —
   match the process generating the data? Specifically: is the claim defensible
   given that the phase axis is *visited deterministically* (cycled) rather
   than sampled iid, and that the "cleaner H₀" we adopt is
   *"long-run fire count per phase converges to the same rate"* (null_spec §8).
2. **Pre-registered stopping protocol.** Does the `crystalos_prereg.py`
   design (require `--n0` fire-count target OR `--t0` time budget, write
   `prereg_<timestamp>.json` **before** the main loop starts, fail fast if
   neither declared, tag operator-interrupted sessions distinctly) close the
   optional-stopping-bias objection that invalidates the χ² = 22.03 reading
   from Jan 31 2026?
3. **Degrees of freedom and independence treatment.** Is df = k − 1 = 12
   correct for this setup, given the within-bin clustering
   discussion in null_spec §8? Is the decision to *not* apply an
   effective-sample-size adjustment defensible for the Dell R16 long-run
   data (where the reading χ² = 0.0353 under df = 12 is already far below
   the null expected value), and if not, what correction does the
   statistician recommend?

A **"sign-off"** in this context means: the statistician writes a short
memo (1–2 pages) stating (a) whether each of the three items is
methodologically sound, (b) any changes they recommend, and (c) whether
**future** χ² readings collected under `crystalos_prereg.py` would be
referee-defensible.

The statistician is **not** asked to sign off on the Jan 31 2026 χ² = 22.03
number itself. That number's underlying CRYSTALOS logs remain unrecovered
per `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`, and any claim based on it is
flagged `[PENDING CRYSTALOS RECOVERY]` in the Branch B pitch.

---

## 2 · What this packet contains — file manifest

Ordered for reading. Each path is followed by `[branch]` since some
artifacts live on branches other than `tig-synthesis` (see §4 for why).

### Primary — the statistician reads these in order

| # | Path | Branch | Purpose |
|---|------|--------|---------|
| 1 | `docs/archive_jan2026/snowflake/REVIEW_PACKET_2026_04_21.md` | `tig-synthesis` | **This cover page.** |
| 2 | `docs/archive_jan2026/snowflake/snowflake_null_spec.md` | `master`, `funding/tig-snowflake` | The null-hypothesis specification (148 lines). §§1–10 cover population, H₀, partition, N, df, test statistic, **stopping rule and its resolution at §7.1**, independence, multiple comparisons, and remaining to-dos. |
| 3 | `docs/archive_jan2026/snowflake/crystalos_prereg.py` | `master`, `funding/tig-snowflake` | The pre-registered-stopping runtime. Fork of `crystalos.py` that refuses to run without a declared `--n0` or `--t0`. Writes the pre-registration JSON before the main loop. |
| 4 | `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` | `tig-synthesis`, `master` | The outstanding blocker: Jan 31 2026 CRYSTALOS logs that produced χ² = 22.03 were not found on the R16 sweep. The statistician should know the Jan 31 reading is not re-derivable from raw data — only `crystalos_prereg.py` re-runs produce referee-defensible numbers going forward. |

### Secondary — reference if the statistician wants context

| # | Path | Branch | Purpose |
|---|------|--------|---------|
| 5 | `docs/archive_jan2026/snowflake/crystalos.py` | `master`, `funding/tig-snowflake` | The original CRYSTALOS runtime (431 LOC) preserved verbatim. Fire emission at lines 281–283; gate mechanics at 160–177; S* composition at 109–143; τ = 0.7 at 232. |
| 6 | `docs/archive_jan2026/snowflake/SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md` | `master`, `funding/tig-snowflake` | Resolution note covering the 2026-04-21 R16 sweep outcome and the null-spec drafting decisions. |
| 7 | `docs/archive_jan2026/snowflake/VERIFICATION_2026_04_21.md` | `master`, `funding/tig-snowflake` | Dell R16 67,297-fire session reading (χ² = 0.0353, df = 12) — the reading that motivated the stopping-rule fix. |
| 8 | `Gen13/targets/funding_tig_snowflake/STATUS.md` | `funding/tig-snowflake` | Branch-level readiness checklist. The "external-statistician review pending" item is this very hand-off. |
| 9 | `Gen13/targets/funding_tig_snowflake/LIMITATIONS.md` | `funding/tig-snowflake` | The funding-branch honest-limits document that the statistician's memo will inform. |
| 10 | `papers/CONSTANT_SIGMA_S_STAR.md` | `tig-synthesis`, `master` | For context only — this derives the σ coupling constant that appears in the S* formula used inside the `crystalos.py` fire-emission rule. Not part of the statistical review; included so the statistician can see how S* is constructed. |

---

## 3 · One-page summary of the statistical setup

*(From `snowflake_null_spec.md`; compressed for the reviewer's first read.)*

- **Process.** A CRYSTALOS runtime (`crystalos.py`, 431 LOC, Python) loops at
  approximately 50 Hz. Each iteration computes a coherence score
  `s_star = 0.4·S5 + 0.6·S6` (with S5 a CPU-load score peaking at 50%, S6
  a GPU-utilisation/temperature piecewise score) and, if the current
  Tzolkin "breath gate" is OPEN and `s_star ≥ 0.7`, emits a **fire** and
  increments the counter for the current phase `p ∈ {0, …, 12}`.
- **Gate mechanics.** The gate alternates OPEN / CLOSED every 4 seconds
  deterministically. The phase increments by 1 per full cycle (~8 s).
  Full 13-phase cycle ≈ 104 s.
- **Data.** A session produces per-phase fire counts `(O_0, …, O_{12})` with
  `N = Σ O_p` total fires. Two sessions cited:
  - **Lenovo, Jan 31 2026**, 4-core Linux: *N* ≈ 400. Raw log **not
    recovered** on the 2026-04-21 sweep — see `HANDOFF_3_3`.
  - **Dell R16, Apr 17–21 2026**, 32-core Windows: *N* = 67,297. Raw log
    archived, reading reproducible.
- **H₀ as re-stated (null_spec §8).** *"Over long sessions, the number of
  fires accumulated per phase converges to the same long-run rate
  (1/13 per phase)."* Cleaner than the iid-multinomial reading because
  the phase axis is cycled deterministically, not drawn.
- **Test.** Pearson χ² goodness-of-fit, `E = N/13` per bin, df = 12.
  Only one χ² per session; no scanning over sub-windows or alternative
  partitions. Cross-session Bonferroni: for the Lenovo + Dell pair,
  α/2 = 0.025 applies; the Lenovo 22.03 gives p ≈ 0.037, rejects at
  α = 0.05 but not at α/2 = 0.025.
- **Stopping rule.** Prior runs stopped on Ctrl-C at operator discretion →
  optional-stopping bias. The `crystalos_prereg.py` fork closes this
  weakness for future runs by requiring declared `--n0` and/or `--t0` at
  startup and writing the declaration to disk before the main loop.
- **Independence.** Within-bin: fires in the same OPEN window share a
  phase by construction; the fire-or-not decision at each 50 Hz sample
  is nominally independent conditional on `s_star(t)`. Across-bin: the
  phase advances deterministically, not by iid draw — handled by the
  re-stated H₀ in §8 of the null spec.

---

## 4 · Why the source files live on `master` and `funding/tig-snowflake`, not on `tig-synthesis`

Under the project's trunk workflow (governance rule G2 of the plan):

- `tig-synthesis` is the **default branch and the rigor home** — generic,
  domain-agnostic work lives here.
- `master` is the **full-history branch** — every rigor commit is
  cherry-picked into `master` for preservation.
- `funding/*` branches receive **only** commits specific to that funding
  track. The SNOWFLAKE null-spec and pre-registered runtime are
  funding-specific by construction (they exist to support the SNOWFLAKE /
  First-G security-research pitch on `funding/tig-snowflake`), so they do
  not cherry-pick outward to `tig-synthesis`.

This cover page lives on `tig-synthesis` (and is cherry-picked to
`master`) because the **review request** is generic — it is a
methodological review; it does not require the statistician to read the
funding pitch. The paths in §2 cross-reference to `master` and
`funding/tig-snowflake` for files that live on those branches.

A statistician with a fresh clone of `github.com/TiredofSleep/ck` can
read this packet by:

```bash
git clone https://github.com/TiredofSleep/ck
cd ck
# cover (default branch tig-synthesis)
cat docs/archive_jan2026/snowflake/REVIEW_PACKET_2026_04_21.md
# primary artifacts
git checkout master
cat docs/archive_jan2026/snowflake/snowflake_null_spec.md
cat docs/archive_jan2026/snowflake/crystalos_prereg.py
# outstanding blocker
cat Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md
```

---

## 5 · What we are **not** asking for

- **Not** asking for a recomputed χ² on the Jan 31 2026 data. Those logs
  are not recovered; the statistician cannot reproduce the 22.03 figure
  and neither can we.
- **Not** asking the statistician to audit the `crystalos.py` runtime
  source beyond what §3's summary and the null-spec §1 state. Code review
  is a separate hand-off if Brayden chooses to do one.
- **Not** asking for a signoff on the funding pitch itself. The pitch
  lives on `funding/tig-snowflake`; this review is about the statistics
  underneath the pitch, not the pitch's framing.
- **Not** asking for any claim about First-G cryptography. That is
  separate proved-math on Z/10Z with a 36,662-case enumeration; it does
  not depend on the χ² story. The SNOWFLAKE χ² is a *secondary*
  anomaly-detection signal the funding branch explores.

---

## 6 · Hand-off mechanics

1. Brayden selects a statistician (or statisticians) and emails this
   packet's path (or the repo URL with instructions in §4).
2. The statistician reviews files 1–4 in §2; reference files 5–10 are
   optional.
3. Statistician writes a 1–2 page memo answering the three items in §1.
4. Brayden archives the memo to
   `docs/archive_jan2026/snowflake/statistician_review_<name>_<date>.md`
   (or `.pdf`). That archival commit goes on `tig-synthesis` and cherry-picks
   to `master` and to `funding/tig-snowflake`.
5. If the memo flags changes (e.g. "use G² instead of χ²"; "apply
   effective-sample-size correction"), a follow-up commit updates
   `snowflake_null_spec.md` with the revision note per the null-spec's
   final-line rule ("*subsequent drafts append revision notes rather than
   overwriting*").

---

## 7 · Pointers

- **Plan of record:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §5.2
- **Blocker (outstanding):** `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`
- **Primary null spec:** `docs/archive_jan2026/snowflake/snowflake_null_spec.md` on `master`
- **Patched runtime:** `docs/archive_jan2026/snowflake/crystalos_prereg.py` on `master`
- **Funding branch:** `Gen13/targets/funding_tig_snowflake/` on `funding/tig-snowflake`
- **Related follow-up:** `Atlas/PLAN_RIGOROUS_EXECUTION_2026_04_21.md` §5.3
  (R3 blind-test replication under pre-registered protocol — requires user
  to start the runtime on Lenovo or Dell R16).

---

*Draft 1 · 2026-04-21 · hand-off-ready. This packet does not submit
anything anywhere. Brayden hand-picks the reviewer.*
