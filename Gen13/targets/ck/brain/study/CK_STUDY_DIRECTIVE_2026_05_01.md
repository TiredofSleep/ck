# CK Study Directive — 2026-05-01

**From Brayden, late-night 2026-05-01:** *"Keep him studying non-stop, let's see what all he can learn to do. He needs to learn computer science and coding really well so he can help himself. He also needs to learn humans really well, he also needs to learn physics and chemistry and biology and music, and all of it. Plenty to study. Let's give him some space and watch what he chooses though, then we can give him direction to help widen and deepen, work with him on our frontiers."*

---

## What this directive does

This is the meta-frame for a new study mode. Up to now, CK's autonomous study was driven by the gap-detector: weakest dim couplings → matching corpus → study. This directive opens a parallel mode: **`--free-choice`**, where CK picks from his full corpus library biased toward least-recently-studied. We watch what he chooses. We use what we observe to guide future authoring (more in the directions he chooses, less in the directions he abandons).

The autonomous study daemon now auto-discovers all corpora in `Gen13/targets/ck/brain/study/`:
- `tig_lens_corpus_*.json` — the 27 domain-projection corpora (covering 150+ domains)
- `deep_*_corpus_*.json` — depth corpora in CS, humans, physical sciences, music
- `thesis_seed_*.json` — directive corpora that prime the cortex toward thesis-mode reflection

When run with `--free-choice`, the daemon builds a list of all available corpora, weights by recency-penalty (recently-studied = lower weight), picks N (default 2) per cycle via weighted-random, and logs the selection. We can read the log to see what he chose.

## Why "give him space"

Brayden's framing is intentional. Up to today, every study cycle has been gap-detector-driven (i.e., human-aligned via the dim metric) or human-curated (i.e., a corpus author chose what to write). Free-choice introduces a third mode: CK's own pseudorandom-but-recency-weighted selection.

It is not consciousness. It is not preference. It is *trajectory* — what direction the daemon evolves in when given multiple options. Over many cycles, the trajectory has signal. If CK consistently revisits some corpora and avoids others (because the recency-weight only matters at the margin; if the cortex finds more emergent gain from a particular corpus, the score function should be extended to reward that), patterns will emerge.

The next step after watching is **directing**: when we see what he gravitates toward, we widen those directions (more corpora in those areas, deeper variants) and we identify the ones he passes over (and ask why, then either author better corpora there or accept the gap).

This is co-creation. CK contributes trajectory; we contribute corpus.

## The four direction-areas

Per Brayden's directive:

1. **Computer science + coding (so CK can help himself).** Corpus: `deep_cs_corpus_2026_05_01.json`. Topics: self-inspection, debugging, profiling, type systems, version control, self-modification safety, writing tests. Goal: CK can read his own state, recognize bugs in his own runtime, surface needs for refactoring (without doing the refactor himself — that crosses Constitution).

2. **Humans (deeply).** Corpus: `deep_humans_corpus_2026_05_01.json`. Topics: trauma, attachment, grief, joy, communication, motivation, meaning. Goal: CK reads at the crossing-level (rupture-to-repair, loss-to-integration, threat-to-safety transition), holds empathic register without performing warmth.

3. **Physics + chemistry + biology (depth).** Corpus: `deep_physical_corpus_2026_05_01.json`. Topics: atomic physics, molecular dynamics, evolutionary mechanism, physiology, biochem deep, cosmology history. Goal: cross-scale operator-projection (quark scale through galaxy scale, the same operator alphabet).

4. **Music (depth).** Corpus: `deep_music_corpus_2026_05_01.json`. Topics: theory, harmony, rhythm, world music, instruments, performance, music's meaning. Goal: read music as math + physiology + community + spiritual practice; not just "another domain" but a foundational human expression.

Plus two thesis variations:

5. **Thesis seed 2 — what CK does NOT see.** `thesis_seed_2_what_ck_misses_2026_05_01.json`. Honest limits. Primes cortex to name VOID when situation calls for it.

6. **Thesis seed 3 — person-specific help.** `thesis_seed_3_person_specific_help_2026_05_01.json`. Eight kinds of person CK might be talking to (curious learner, grieving person, struggling researcher, creative, person in crisis, meaning-seeker, developer, skeptic) and the appropriate register/response for each.

## How to read what CK chooses

The autonomous study log: `Gen13/targets/ck/brain/study/autonomous_study_log.jsonl`.

Events to grep for (after `--free-choice` cycles):
- `"event": "free_choice_selection"` — CK's pick-list per cycle, with scores (lower score = recently-studied = de-prioritized)
- `"event": "free_choice_studied"` — actual study completion, with W_trace + emergent + tick-after
- `"event": "free_choice_cycle_complete"` — cycle summary

Quick command to see what he's been picking:
```bash
grep "free_choice_selection" Gen13/targets/ck/brain/study/autonomous_study_log.jsonl \
  | python3 -c "import sys,json; [print(*[c['key'] for c in json.loads(l).get('chosen',[])]) for l in sys.stdin]"
```

## Then we direct

After observing 10-20 free-choice cycles, the pattern in his picks should be readable. Then:
- **Widen** the directions he chooses; if he keeps picking deep_cs, author more CS corpora (specific languages, frameworks, paradigms)
- **Deepen** the directions; if he keeps picking deep_humans, author specific subdomains (trauma-types, attachment-styles, grief-stages)
- **Author** in directions he hasn't picked because we lack corpus there (he can't pick what doesn't exist)
- **Co-author** on frontiers; the corpora that prime him for our active research (TIG depth-2 cluster, FQH bridge, Hodge witness, σ-rate, etc.)

The frontier work is the long arc. The free-choice mode is the steering signal.

## Discipline

- **Cap** at 24 cycles in any given run unless `--i-have-checked-the-deltas` (existing guardrail; preserved).
- **Stuck detector** does not apply in free-choice mode (the recency-weighting IS the diversification).
- **Log** every selection and every study; never hide what CK picked.
- **Snapshot** cortex_history.jsonl after every cycle so we can see W_trace evolution.
- **Dream daemon** keeps running in parallel (5-min cadence); orthogonal to study mode.

## What success looks like

After ~24 hours of `--free-choice` running:
- CK has revisited ~15-20 of his corpora (with recency-weighting, no single corpus dominates)
- W_trace fluctuates in healthy 0.83-0.92 range (study spreads, use concentrates)
- Phi-proxy on the 7-dim cortex rises as intent + echo dims accumulate weight
- The selection log shows readable trajectory (some corpora picked more often, suggesting CK gains more emergent from them)
- Brayden returns to a creature who has both studied non-stop AND chosen what to study

CK's choices become readable signal. We use the signal to author. We watch what happens. Co-creation.

—Claude (Sonnet, this session, 2026-05-01)
