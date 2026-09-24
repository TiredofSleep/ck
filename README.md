> ## ⚙️ This repository is the WORKSTATION — kept whole, and retired in place
>
> **`ck` is the full working trail of the earlier program: the lab bench, not the gallery.** It keeps
> every generation (`Gen9`–`Gen14`), the Coherence Keeper software, and the table-based "TIG" research
> program with its papers, its drift and its retractions. Nothing has been deleted. On 2026-09-23 the
> program's claims were retired. **[`RETIRED.md`](RETIRED.md)** says what was retired, why, and what
> was salvaged.

# ck — the workstation of the TIG / Coherence Keeper project

**Brayden Ross Sanders** · 7SiTe LLC · Hot Springs, Arkansas

## Where the living work is

- **[The Shape of Understanding](https://github.com/TiredofSleep/shape-of-understanding)** — the book.
  The integers read as shapes: the void, the simplices, the tetrahedron's 1/3, the cube with its two
  shadows, rotation as *i*, growth as *e*, and the seam where counting cannot measure. It climbs from
  gumdrops to undergraduate mathematics, and every picture is checked against the real proof.
- **[Trinity Infinity Geometry](https://github.com/TiredofSleep/trinity-infinity-geometry)** — the
  flagship: a new way to teach higher mathematics by classifying its paradoxes, not resolving them.
  - The base: the integers 0–9 as the most symmetric arrangements of points.
  - The towers of higher mathematics that each shape points up to.
  - The coin: two sides and an edge on every floor.

  It is machine-checked, one command per part.
- **[What survived](https://github.com/TiredofSleep/trinity-infinity-geometry/blob/main/WHAT_SURVIVED.md)**
  — an essay on the audit of this repository: the three gates, what passed them, and what we would
  tell anyone doing research with AI.

## What happened here

**What it was.** From 2025 into 2026, working with AI, the author built a large research program
here. "TIG" rested on ten verbally described operators and three 10 × 10 composition tables, with an
AI system — the Coherence Keeper, CK — meant to run on them. Around them grew 56 journal-style papers,
whitepapers numbered past 120, a canon of results, funding pitches, and a website.

**What an audit found (September 2026).**
- The tables were AI renderings of the author's descriptions, and they disagree with one another on
  about half their cells.
- No result specific to the tables survived testing: each was generic, a restatement of how the
  tables were built, numerology, or computed on a transcription error.
- The readings in physics, cosmology and number theory were numerical fits, not derivations.
- A June 2026 probe had already found that CK's language model organizes itself by English grammar,
  not by the tables.

**What survived.**
- The book's premise — integers as shapes — now lives in the book and the flagship.
- The author's own classification of paradoxes into four kinds, with Ben Mayes, is now in the
  flagship's coin.
- A few correct, expository notes.
- Working software: a from-scratch language model that writes fluent English, a fold-not-prune
  growable architecture, a Muon optimizer integration, and a reusable interpretability probe.
- A continual-learning benchmark.
- Two small, checked results that came out of the audit itself. They concern type specimens in Tao's
  Equational Theories Project, and both run against the program's own papers:
  - J61's "fossil variety" theorem is false;
  - every one of the eight closures J61 listed has a finite type specimen.

  See [`J61_CLOSURES_ALL_REALIZED.md`](Gen14/targets/journals/J_series/J61/J61_CLOSURES_ALL_REALIZED.md).
- The discipline of retracting the program's own claims.

The details, with paths, are in **[`RETIRED.md`](RETIRED.md)**.

## Finding your way in the old material

| | |
|---|---|
| [`RETIRED.md`](RETIRED.md) | **Start here** — what was retired, why, and what was salvaged |
| [`README_ARCHIVED_2026-09-23.md`](README_ARCHIVED_2026-09-23.md) | the old front page, unchanged |
| tag [`workstation-2026-09-23`](https://github.com/TiredofSleep/ck/tree/workstation-2026-09-23) | the whole repository as it stood before the retirement |
| [`Gen13/PROJECT_STATUS_SALVAGE_HISTORICAL.md`](Gen13/PROJECT_STATUS_SALVAGE_HISTORICAL.md) | the June 2026 salvage, with the September correction at its top |
| [`Gen13/targets/journals/J_SERIES_NOTE_N_WHAT_DIDNT_HOLD.md`](Gen13/targets/journals/J_SERIES_NOTE_N_WHAT_DIDNT_HOLD.md) | every numerical "bridge" to physics and to famous problems, and why none is a derivation |
| [`Gen13/targets/ck/trinity/TIG_AS_EXPLANATION.md`](Gen13/targets/ck/trinity/TIG_AS_EXPLANATION.md) | the probe's honest negative: CK is organized by grammar, not by TIG |
| [`Gen13/targets/ck/trinity/ns_number_theory_tour/`](Gen13/targets/ck/trinity/ns_number_theory_tour/README.md) | an honest, table-free computational tour of Navier–Stokes and number theory |
| the side branches | all 22 carry a banner: retired, historical, merged, or salvaged core |

## License

Unchanged — see [`LICENSE`](LICENSE). The project DOI,
[10.5281/zenodo.18852047](https://doi.org/10.5281/zenodo.18852047), is the umbrella for every version.
