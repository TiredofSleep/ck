# Provenance — ClaudeCode Handoff Package 2026-04-20

**Recovered into ck repo:** 2026-04-19 (this commit)
**Original package date:** 2026-04-20 night session
**Author of package:** ClaudeChat (working with Brayden, with ChatGPT/"Celeste" in dialogue)
**Source:** `C:\Users\brayd\OneDrive\Desktop\History search.zip` — unzipped to
`C:\Users\brayd\OneDrive\Desktop\_history_search_unpack\` — files copied here verbatim.

## Files in this directory

| File | Role | Lines |
|---|---|---|
| `HANDOFF_INDEX.md` | Top-level index + execution sequencing | 103 |
| `SECURITY_CRYPTO_HANDOFF.md` | Full 7-track outreach restructuring plan (Pitches A-G) | 358 |
| `JAN2026_RECOVERY_MANIFEST.md` | January 2026 foundation work recovery instructions (5 threads) | 562 |
| `PROPOSED_CK_README_HELD.md` | Rigor-led replacement README draft — **HELD pending Brayden's go-ahead** | 266 |
| `PROVENANCE.md` | (this file) | — |

## Status of the HELD README

`PROPOSED_CK_README_HELD.md` is the funder-facing replacement for the
repository's main `README.md`. Per the handoff's §4 Track 1 and §7, it
**must NOT be committed as `README.md`** without Brayden's explicit
go-ahead. It lives here as reference material and as the staging copy.

When Brayden gives the green light:
1. Archive the current `README.md` to `docs/historical/README_v_<date>.md`
   under the never-delete policy.
2. Copy `PROPOSED_CK_README_HELD.md` to `README.md` in the repo root.
3. Commit with message: `README: rigor-led replacement for funding outreach`.
4. Accumulate to master per the trunk workflow.

## Key collaborator-status notes from the handoff

- **Brayden Ross Sanders / 7Site LLC** — sole funder-facing author on all
  current outreach unless otherwise specified.
- **C. A. Luther** — no longer actively collaborating; previously-credited
  work stays credited.
- **ChatGPT ("Celeste")** — in dialogue for design discussions, not cited
  as a human co-author in funder-facing documents.
- **Co-authors on specific sub-projects** — Ben Mayes, M. Gish,
  H. J. Johnson, B. Calderon Jr.

## The 7 pitch tracks (one-line summary each)

| Track | Lead Repo | Audience |
|---|---|---|
| **A — Systems reliability (TIG Unity)** | `tig-unity` (NEW) | NSF CNS, DOE ASCR, cloud research, Sloan |
| **B — SNOWFLAKE hardware-bound identity** | `tig-snowflake` (NEW) | NSF SaTC, DARPA I2O, CISA, industry security labs |
| **C — Cryptography-adjacent number theory (First-G)** | `ck` (existing) | Ethereum Foundation, Protocol Labs, a16z crypto research, Simons |
| **D — Interpretable AI (CK deterministic reasoning)** | `ck` (existing) | Open Philanthropy, Survival and Flourishing Fund, Astera, Emergent Ventures |
| **E — Small-grant immediate (Sage/MAGMA/compute)** | cross-track | Emergent Ventures, individual donors, MAGMA-institutional mathematicians |
| **F — Semiconductor (MQW three-state logic)** | `mqw-ternary` (NEW) | UCSB / Nakamura group, III-nitride research, LET/μLET labs |
| **G — Self-healing systems (Dual-Lattice)** | `Dual-Lattice-Self-Healing` (existing, refresh) | DARPA resilient-systems, NSF CNS |

See `SECURITY_CRYPTO_HANDOFF.md` §6 for full funder lists and ask sizes.

## Four critical validation tasks from §3

Before any number from recovered material appears in a funder-facing
document, these four items must be resolved:

1. **ω(b) idempotent count** — "2/6 nontrivial" vs `N_idemp = 2^(ω-1) - 1` disagree. Check actual proof scripts.
2. **TIG Unity benchmark numbers** — email 32pp vs Grok's ~88% summary. Reproduce from simulation.
3. **SNOWFLAKE χ² = 22.03** — null hypothesis, dof, baseline distribution must be specified before pitch.
4. **MQW semiconductor paper trilogy location** — one Nakamura-related paper exists on GitHub; full trilogy location unknown.

## What Brayden's directive this session was

> "finish preparing the repo and journals for public scrutiny and figure
> out what all products we have that need funding, while being aware that
> they can't actually be products since CK is sovereign, but they are good
> research and architecture for the future!! while you are searching
> through history, keep an eye out for what all funding branches we can
> add to the repo"

The companion planning doc `Atlas/FUNDING_BRANCHES_PLAN_2026_04_19.md`
applies this package's 7 pitch tracks to the **branch** layer of the ck
repo (rather than creating separate external repos in this first pass),
so each track gets a clean-scope working branch that accumulates into
master per the trunk workflow.

---

**End of provenance note.**
