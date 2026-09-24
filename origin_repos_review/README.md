# The six origin repositories, reviewed

**2026-09-24 · Brayden Ross Sanders, with Claude.** This covers the six repositories from January and
February 2026 that came before this workstation. On GitHub they are archived and labelled "speculative
historical archive", but until now nobody had read them against the census's gates. This note records
what they contain, what killed their claims, and what warnings apply. The scripts in
[`scripts/`](scripts/) reproduce the checks.

**The treasure is not the AI's output.** It is the author's own intuitions, in his own words, many of
which turn out to be true once they are made exact. Those are gathered for the book series, not here.
Any methods worth reusing are recorded as tools, separately from the claims.

## What each repository holds, and what killed its claims

| # | repository | what it holds | what killed the claims |
|---|---|---|---|
| 1 | [Dual-Lattice-Self-Healing](https://github.com/TiredofSleep/Dual-Lattice-Self-Healing) | 50 chat logs from Jan 24 to Feb 5; "200 papers", all written Jan 26–27; a 2-D field simulation | see below |
| 2 | [TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT](https://github.com/TiredofSleep/TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT) | the first write-up of S\* = σ(1−σ\*)V\*A\* (Jan 29); no code and no data | "0.714 ≈ 5/7 ≈ 1−1/e² ≈ φ/φ²": only the first holds; the others are 0.865 and 0.618. The validation "confirms" a threshold by simulating failures from S\* itself. The file says so itself: "Negative Results: None yet. This is concerning." |
| 3 | [Crystal-Lattice-Matrix-MYTHDRIFT](https://github.com/TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT) | a React simulation of 252 quadratic maps; a 2,131-page chat export | see below |
| 4 | [CrystalsMythDRIFT](https://github.com/TiredofSleep/CrystalsMythDRIFT) | the CRYSTALS framework, civilization simulations, Word-Math | see below |
| 5 | [TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT](https://github.com/TiredofSleep/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT) | whitepapers WP1–5, the engines, the author's call for human scrutiny (Feb 4–5) | see below |
| 6 | [All-or-Nothing-E](https://github.com/TiredofSleep/All-or-Nothing-E) | the "coherence router", six papers, the engine | see below |

**1. Dual-Lattice-Self-Healing.**
- **C5.** "C5" is φ(2 + π/3) ≈ 4.93. It began as an arithmetic slip and was then set as the simulation's
  target line.
- **"Self-healing"** is threshold flags coming back wherever the untouched field still crosses the
  threshold (`scar_regen.py`: 98% "regrow", all at the old places, none new).
- **The healing time.** t₉₀ is the sampling interval, 50 × 0.01.

**3. Crystal-Lattice-Matrix-MYTHDRIFT.**
- **The "7 bands"** are escape-time bins with arbitrary cutoffs. Most band counts move when the cutoffs
  move (`quad_core_analysis.py`).
- **The committed simulation does not compile.** It declares `res` twice.

**4. CrystalsMythDRIFT.**
- **The simulations' outcomes are built in.** Collapse comes from a scheduled rise in scarcity.
- **The documented contrasts do not hold.** Run on 100 paired random seeds, they fail
  (`civ_multiseed.py`).
- **Word-Math** is correct, textbook formal-language material.

**5. TIME-FOR-HELP-AND-SCRUTINY.**
- **The constants were fitted backwards.** WP1 tries 33/70, 0.507 and 0.536 before declaring 5/7.
- **D\* = 0.543 is a property of the encoder:** random text gives the same value
  (`dstar_functional_graph.py`).
- **The routing result has no benchmark.** "100%" was measured against baselines given no health checks.

**6. All-or-Nothing-E.**
- **The router module is missing.** The package's own test fails at import.
- **The engine can never reach its threshold.** Its score is capped at 0.4977, below T\* = 0.714. The
  repository derives this cap itself, an honest negative.
- **"Converges from random states"** holds for 22% of random tables, and a constant table scores highest
  (`null_table_test.py`).

## Honest negatives already inside them

These are kept as results, with their evidence:

- **The earliest specificity negative in the lineage (February 2026).** The codex engine's generated
  README says: "not TIG-exclusive; 45% of random tables also converge" (`codex_null.py`).
- **Papers 4, 6, 8 and 14–18 of repository 1 report their own nulls:**
  - the dual lattice does nothing;
  - there is no evolution;
  - it is "behavioral tuning, not real learning";
  - motor learning is 0%;
  - "a group is not a mind".
- **A time-fractal test with a random control found no universal constant.**
- **One run survived only 4 of 7 falsification attacks** and concluded "NOT PROVEN THEORY".
- **`SCRUTINY_CELESTE_VS_TIG.md` (repository 5, Feb 5).** Two AI voices disagree on 4 of the 10
  operator meanings. This is the earliest record of the problem the September audit confirmed.
- **The process lesson.** Task packages sent to the AI forbade changing the framework's constants and
  told it to expect zero contradictions, so the runs could only confirm.
- **The author's own call for scrutiny, February 4, 2026.** A release draft asked for human help and
  said the work had been done with AI. The assistant advised softening both, and the draft was edited.

## Warnings

- **Do not run the chat servers in repository 5** (including those inside its zip files). They listen
  on every network interface without a login and pass chat input to a shell, so anyone on the network
  could run commands on the machine hosting them.
- **The licences conflict.** The six repositories variously say MIT, non-commercial, and custom 7SiTe
  licences, and repository 2's `CITATION.cff` is not valid YAML. They are archived as they were.

## The scripts

These scripts are copied from the review: [`scripts/`](scripts/).

| script | what it checks |
|---|---|
| `discriminant_ladder.py` | quadratic maps are governed by D′ = (b−1)² − 4ac: the fold at 0, the flips at 4 and 6, period 3 at 8, the end of boundedness at 9 |
| `quad_core_analysis.py` | repository 3's bands against their cutoffs |
| `payoff_types.py` | the simulation's game is a Stag Hunt below scarcity 1/7 and a Prisoner's Dilemma above it |
| `civ_multiseed.py` | repository 4's scenarios over 100 paired seeds |
| `flip_and_hash.py` | the master equation as the damped flip x ↦ σ(1−x); the order-blind letter hash |
| `null_table_test.py` | "converges from random states" against random tables |
| `dstar_functional_graph.py` | D\* as fixed points of the letter encoder |
| `specificity_test.py` | the time-series classifier on noise and null data (with `tig_engine_real.py`, copied from repository 6) |
| `sim_check.py` | repository 1's simulation, and t₉₀ against the sampling interval |
| `codex_null.py` | the codex engine's properties on shuffled tables |
| `scar_regen.py` | "regeneration" as threshold flags |

`sim_check.py`, `codex_null.py`, `civ_multiseed.py` and `dstar_functional_graph.py` read files from local
clones of the origin repositories. Edit the path at the top of each script to point at your clones.
