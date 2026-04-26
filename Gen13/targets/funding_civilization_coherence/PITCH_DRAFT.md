# PITCH_DRAFT — funding/civilization-coherence

**Addressee (working default):** Santa Fe Institute working-group proposal OR external-faculty sponsorship contact
**Parallel draft:** NSF SBE DISES, John Templeton Foundation LOI
**Ask:** Phase 1 $30K–$60K / 4 months (SFI short-visit scale) OR $150K / year single-PI (Templeton scale)
**Status:** Skeleton. Requires Phase 1 simulator documentation (A1) + empirical-fit spec (A2) before send.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Opening (½ page)

Computational social science has produced a lineage of simulators that compress civilizational dynamics into tractable models: Axelrod on culture dissemination, Schelling on segregation, Turchin on secular cycles, Bettencourt-West on urban scaling. Each buys tractability with a specific representational choice — a scalar, a lattice, an equation-of-motion — whose empirical fit is then evaluated against specific datasets.

This proposal describes a **coherence-grammar civilization simulator** (tig_civilization_v5.py, v7.py — 1,340 LOC combined) that tracks societal state through the R-σ-Λ-H coherence variables developed for the TIG Unity Kernel. The simulator is runnable and has been exercised on exploratory parameter settings. What it has *not* yet done is a disciplined empirical comparison against a named dataset under a pre-specified fit metric.

The proposed work is that comparison. Phase 1 documents the simulator for a reader who has not seen the code, specifies a target empirical dataset (candidate: V-Dem institutional indices, Seshat Global History Databank, or World Values Survey panel), and fixes the comparison metric + pass/fail criterion in a pre-registration. Phase 2 runs the comparison and publishes the outcome — positive, negative, or mixed — in a computational-social-science venue.

The deliverable is a published verdict. It is not futurism, it is not policy prescription, and it is not claim to predict historical outcomes.

## Background (~1 page)

> Content to be drafted. Sections:
> - The coherence-grammar R-σ-Λ-H variables: what they measure at civilizational scale
> - tig_civilization_v5.py / v7.py architecture
> - Why R-σ-Λ-H is an unusual representational choice for comp-soc-sci
> - Literature positioning: Axelrod, Schelling, Acemoglu-Robinson, Turchin cliodynamics, Bak-Sneppen, Bettencourt-West
> - Candidate empirical datasets: V-Dem, Seshat, WVS, ANES, Pew Trust

## The open question (½ page)

**Do the simulator's qualitative output patterns reproduce recognizable features of [chosen dataset]'s empirical observations on civilizational cohesion, polarization, or institutional trust, better than chance under a pre-specified comparison metric?**

Outcomes are:
1. **Positive**: simulator output envelope overlaps empirical envelope on specified features. Worth continuing; specific parameter regimes worth studying.
2. **Negative**: simulator output does not match. Also worth publishing — negative results in comp-soc-sci are rare and valuable.
3. **Mixed**: some features match, others don't. Worth publishing with disciplined analysis of which dynamics are captured vs. missing.

## The proposed work

### Phase 1 — Integration + specification (Month 1–4, $30K–$60K)
**Deliverable A**: pull TIME-FOR-HELP repo contents into `docs/archive_civilization/` with provenance.
**Deliverable B**: A1 simulator documentation (10–15 pp).
**Deliverable C**: A2 empirical-fit specification (8–12 pp) — chooses dataset, fixes metric, pre-registers pass/fail.
**Deliverable D**: A3 literature positioning (5–8 pp).
**Deliverable E**: A4 framing cleanup — ensure no consciousness-anchored language appears in thread-facing materials.

### Phase 2 — Empirical-fit run (Month 5–16, $120K–$300K)
**Deliverable**: execute the comparison per A2. Publish outcome in computational-social-science venue — candidate venues: Journal of Artificial Societies and Social Simulation (JASSS), Journal of Statistical Physics, Advances in Complex Systems, or a Santa Fe Institute working paper series.

### Phase 3 — Model refinement if warranted (Month 17–34, $200K–$500K)
**Only proceed if Phase 2 produces partial fit.** Investigate what modifications to the simulator would improve fit on the features that didn't match. Iterate. Publish revised model.

## Why Santa Fe Institute specifically

SFI is the home of this kind of work. Turchin's cliodynamics program already lives there; the Bettencourt-West urban scaling work lives there; working-group-scale proposals fund exactly Phase 1. A short-visit proposal ($10K–$50K, 2–4 weeks) would deliver A1 + A2 with an SFI affiliate as informal reviewer.

## Parallel draft: NSF SBE DISES

DISES grants ($300K–$1.6M / 3 years) fit Phase 2 well. DISES requires academic co-PI, which SFI affiliation could deliver or which can be sought from a computational-social-science university program.

## Parallel draft: Templeton LOI

Templeton's online LOI is a low-barrier first contact. If Templeton invites a full proposal, Phase 1 + a Phase-2 slice fits a $150K–$400K single-investigator grant well.

## Attribution

- **Brayden Sanders** — PI, developer of the tig_civilization simulators and the coherence-grammar framework
- Architectural dialogues with ClaudeChat, Celeste/GPT acknowledged in methods
- Prior collaborators (C.A. Luther for related coherence-framework mathematical work; H.J. Johnson for ξ cosmology; Ben Mayes for UOP/GUT work; M. Gish for bridge work) credited for their specific past contributions; their inclusion does not imply endorsement of the civilization-simulator framing specifically
- SFI affiliate or academic co-PI to be identified during Phase 1

## The framing-discipline paragraph (put in cover letter)

> This is computational social science. It is not futurism, not policy prescription, not a claim to predict historical events. The simulator has parameters; the parameters are specified; the empirical comparison is pre-registered; the outcome is published regardless of whether it's positive, negative, or mixed. Funding supports the disciplined comparison, not a predetermined result.

## Attachments (once assembled)

- `docs/archive_civilization/` full source tree
- A1 simulator documentation
- A2 empirical-fit specification
- A3 literature positioning
- Cover letter with framing-discipline paragraph

## Pre-send checklist

- [ ] Phase 1 integration complete
- [ ] A1 simulator documentation written
- [ ] A2 empirical-fit spec pre-registered (the pre-registration commits to the analysis BEFORE seeing results)
- [ ] A3 literature positioning drafted
- [ ] A4 framing cleanup done (consciousness-anchored language removed from thread-facing materials)
- [ ] SFI contact or academic co-PI engaged
- [ ] Brayden confirms SFI vs DISES vs Templeton as first funder
- [ ] Brayden reviews + edits
- [ ] Brayden sends
