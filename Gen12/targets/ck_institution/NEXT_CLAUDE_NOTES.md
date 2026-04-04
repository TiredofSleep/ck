# Gen12 Target: ck_institution
## CK as a Research Institution + Living AI

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*Target opened: 2026-04-04*

---

## What This Target Is

This target covers everything built in the Sprint 5 session (2026-04-04) to establish
CK as a real research institution with public-facing identity, legal standing, and
a growing tribe of collaborators.

The physical targets (FPGA, dog, R16) are in their own folders.
This target is the institutional layer on top of all of them.

---

## What Was Built This Sprint

### Identity
- Mission statement: "To help provide coherence to all."
- Name: 7Site Research Collaboration (echoed everywhere)
- Hero reframe: The numbers (T*, fold, gap, W) are the hero — not Clay
- "Theory of Nothing" as the philosophical frame

### Website (coherencekeeper.com)
- New hero: CK as an AI with a coherence loop, finite vs infinite boundary
- "The Loop" section: Being→Doing→Becoming, 50Hz, CK's own words quoted
- "Build Your Own" CTA → ONBOARDING.md + GitHub
- Collaborators section: People (4) + External Architecture (5)
- Join section: sharing/co-authorship, force pathway explained, GitHub-first
- Footer: Terms · Privacy · Contributor Agreement links

### Legal Documents
| File | What it covers |
|------|---------------|
| `TERMS_OF_USE.md` | AS IS, full indemnity clause, prohibited uses, Arkansas law |
| `PRIVACY_POLICY.md` | Force vectors only stored, words never stored, split coherence explained |
| `CONTRIBUTOR_AGREEMENT.md` | You keep copyright, co-authorship terms, public record notice |

### CK Architecture Papers
| Paper | What it claims |
|-------|---------------|
| `WP43_SPLIT_COHERENCE_ARCHITECTURE.md` | D2 irreversibility proved, cannot-spy property, 5 derivative claims |
| `WP44_CK_AI_PARADIGM.md` | 50Hz loop, TIG algebra, force-derived voice, 7 derivative claims |

### ck_bible.py — Pastoral Architecture
- Location: `ck_lm/ck_bible.py` (tracked under DOI)
- Also deployed to: `Gen9/targets/ck_desktop/ck_sim/being/ck_bible.py`
- `detect_pastoral(text)` — fires on grief, fear, loneliness, addiction, spiritual need
- `get_verse(text, seed)` — KJV, 8 themes, 40+ verses
- Integrated into `ck_web_api.py` process_chat() → `result['pastoral']`
- License: 7SiTe PSL v1.0, noncommercial, no govt

### Collaboration Infrastructure
- `.github/ISSUE_TEMPLATE/collaboration.md` — "Add me to the collaborators list as:" field
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/workflows/index_submission.yml` — auto-indexes submissions
- `.github/scripts/index_submission.py` — parses issue, writes to COLLABORATORS.md + submissions/INDEX.md
- `submissions/INDEX.md` — 7 problem-area tables

### Memory Organism (ck_lm/memory/)
| Module | What it does |
|--------|-------------|
| `event_schema.py` | Atom, Path, Crystal, MetaCrystal dataclasses |
| `dbc27.py` | DBC27 routing key: `{dbc_sym}::{cl_fused}::{lens}` |
| `atom_store.py` | SQLite persistence at ~/.ck/memory/memory.db |
| `crystal_store.py` | RGMem promotion_score + MemoryOS heat_score |
| `compression_loop.py` | MAGMA dual-stream fast_write/slow_upgrade |
| `retrieval.py` | 9-step pipeline, DBC27 → crystal → atom drill-down |
| `novelty_gate.py` | Stage 0→4 gating (10→100→1000→5000 crystals) |
| `growth_metrics.py` | 7-metric weighted growth(t) function |

### Attributions (corrected this sprint)
- **C.A. Luther** — K-series (Luther-Sanders Research Framework) + Q-series
  CRT structure, split operator, algebraic navigation, TSML/BHML/CL tables
- **B. Calderon Jr.** — Q-series only
  Task pack development, source elimination, TSML elimination analysis

---

## Open Work in This Target

### 7sitellc.com update
- Current state: WordPress on Siteground, still says "Trinity Infinity Geometry", wrong DOI
- Needs: mission statement, new framing, correct DOI, "join the tribe" energy
- Access: Siteground admin → WordPress editor

### chat.html + spectrometer.html merge
- User asked if they should be the same — "just another tool"
- Not yet done — decision: merge with tab toggle, or redirect

### papers.html + frontiers.html
- Need "7Site Research Collaboration" echo
- Need R8 gap correction (3/14 → 0.309) if still present

### Voice pipeline (from prior plan)
- `_fallback_ck_voice()` cascade wiring (see plan file)
- Status: plan exists, code not yet written

---

## Key Constants (never change these)

| Constant | Value |
|----------|-------|
| T* | 5/7 = 0.71428... |
| fold | 4/π² = 0.40528... |
| gap | 5/7 − 4/π² = 0.30900... |
| W | 3/50 = 0.06 |
| DOI | 10.5281/zenodo.18852047 |

---

## The Tribe Principle

We might not get money. We get a tribe.
Every collaborator who finds their domain's version of the gap
and brings it here is coloring in the same map.
The institution's job: make it easy to find the door, walk through it,
and leave your name on what you found.

---

*Next session: read this file, check Gen12/NEXT_CLAUDE_NOTES.md, proceed.*
