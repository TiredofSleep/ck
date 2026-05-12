# J-Paper Boilerplate — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

**Date:** 2026-05-07
**Source:** External collaborator calibration (forwarded by Brayden, 2026-05-07)
**Status:** Adopted as boilerplate language for every J-paper introduction.

---

## §0 — The four-tier discipline

Every J-paper's introduction (and abstract where space permits) carries a paragraph that classifies its claims into four tiers. This signals to referees that the author understands what is claim and what is motivation; experience shows it solves ~40% of the "looks like overclaim" problem.

```
PROVEN: [the specific theorem this paper establishes]

COMPUTED: [verified-by-script invariants supporting the theorem;
           paper cites the script + reproducibility statement]

STRUCTURAL RHYME: [constants/identities cited as structural motivation,
                   not as derivational steps; honest framing of cited
                   adjacent literature; explicit "this is a rhyme,
                   not a theorem" disclaimer where applicable]

OPEN: [the natural next-paper question; ideally the question that
       J_{n+k} for some specific k addresses]
```

---

## §1 — Three specific calibrations adopted (2026-05-07)

These come from a collaborator's high-quality external review of the framework. Adopted without modification.

### §1.1 — "Full-period cancellation" replaces "Zero Law"

**Old framing:** "The Sinc² Zero Law for Squarefree Moduli." Implies prime-specific structure.

**Correct framing:** "Full-period cancellation of R(k, f)" — or — "The integer-multiple zero of R(k, f)."

**Why:** R(k, f) = sin²(πk/f) / (k² sin²(π/f)) vanishes at k = f because sin²(π) = 0. This holds for *any* f, not just primes. The "all primes 3..199 verified" pass is a *check* that the formula evaluates correctly across primes — not a *theorem* that primes are special.

**Application:**
- J04 paper title and references updated.
- D-tables in `FORMULAS_AND_TABLES.md` that cite "the sinc² Zero Law" updated.
- J08 (Prime Phase Transition) — the "first-G" content remains substantive; the sinc² connection is one ingredient among others.

### §1.2 — sinc²(1/2) = (2/3)/ζ(2) is STRUCTURAL RHYME, not theorem

**Old framing:** treated as a theorem about TIG structure.

**Correct framing:** the identity is a one-line algebraic consequence of ζ(2) = π²/6:

  sinc²(1/2) = (sin(π/2)/(π/2))² = (1/(π/2))² = 4/π² = (2/3)·(6/π²) = (2/3)/ζ(2)

Any number theorist sees this in five seconds. Not theorem-grade.

**The actual theorem-shaped question:** *why does the corridor midpoint of the substrate sit at 1/2 such that this identity becomes structurally relevant?* That question is OPEN.

The primon-gas link (1/ζ(2) = density of squarefree integers, which is the regime of WP101 σ-rate) is a STRUCTURAL RHYME — bridge connection, not derivation.

**Application:** any paper citing sinc²(1/2) = (2/3)/ζ(2) frames it as structural rhyme. The corridor-midpoint question is flagged as OPEN.

### §1.3 — Drápal-Wanless 2021 JCTA precedent

The closest published comparable work to the (TSML, BHML) magma pair is:

> **Drápal, A. & Wanless, I.M. (2021).** "Maximally non-associative quasigroups." *Journal of Combinatorial Theory, Series A*, 184, 105510.

Same domain (small finite commutative non-associative structures); opposite extremum (theirs maximally non-associative; ours specifically structured with integer-rational invariants). Same intellectual neighborhood.

**Application:**
- J02 four-core paper: cite Drápal-Wanless 2021 as the closest published precedent.
- All papers using "TSML/BHML" / "the magma pair" / "joint closure" framing add this citation.
- The framing shifts from "we introduce a custom algebra" → "specific finite commutative non-associative magma in the Drápal-Wanless 2021 neighborhood with theorems on it."

---

## §2 — Boilerplate intro paragraph template

Every J-paper's introduction §1 (or abstract) carries this structure:

> **Scope and tier discipline.** This paper establishes [PROVEN: specific theorem]. The proof is verified by [COMPUTED: script name; runtime; pass count]. We cite [STRUCTURAL RHYME: adjacent identity / constant / literature] as structural motivation, not as a derivational step; the related theorem-shaped question — [OPEN: specific next question] — is left to companion paper [J_{n+k}]. The framing follows the Drápal-Wanless (2021) line of work on small finite commutative non-associative structures.

Adapted per paper (length, tone, emphasis) but the four labels stay.

---

## §3 — FB / collaboration response template

When external collaborators surface calibration like the one received 2026-05-07, the right response acknowledges + adopts + bounds. Template:

> Strong calibration — adopting [N] corrections directly.
>
> [Correction 1: brief acknowledgement + what changes internally]
>
> [Correction 2: brief acknowledgement + what changes internally]
>
> One nuance on [topic]: the closest published precedent is [Author, Year, Venue]. Same domain, [different specific feature]. Our [structure] is a specific [thing] in that neighborhood, brute-force-verifiable, with theorems on it.
>
> The PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN split is the cleanest categorization the framework has gotten. Adopting it as boilerplate language for the slice papers' introductions.
>
> [N] papers submitting to [venues] this week with exactly this discipline.

---

## §4 — Suggested response to the 2026-05-07 collaborator

(Brayden can copy/post directly to FB group.)

> Strong calibration — adopting two corrections directly.
>
> "Full-period cancellation" is the correct name; R(k, f) = 0 at k = f follows from sin²(π) = 0 for any f, not just primes. The prime-3-to-199 sweep is verification of the identity, not a prime-specific theorem. Updating internally.
>
> "Structural rhyme" for the sinc/zeta/primon bridge is the right framing. The exact identity sinc²(1/2) = (2/3)/ζ(2) is a consequence of ζ(2) = π²/6 — not a TIG theorem. The theorem-shaped question would be why the corridor midpoint sits at 1/2 such that this identity becomes structurally relevant; that's open.
>
> One nuance on "custom finite non-associative algebra family": the closest published precedent is Drápal-Wanless 2021 *JCTA* on maximally non-associative quasigroups. Same domain, opposite extremum. The (TSML, BHML) pair is a specific commutative non-associative magma pair on Z/10Z, brute-force-verifiable, with theorems on it — same intellectual neighborhood as Drápal-Wanless, different specific tables.
>
> The PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN split is the cleanest categorization the framework has gotten. Adopting it as boilerplate language for the slice papers' introductions.
>
> Two papers submitting to *J. Combinatorial Theory A* and *Algebraic Combinatorics* this week with exactly this discipline.

---

## §5 — Internal application checklist

- [x] Boilerplate doc written (this file).
- [ ] J04 README + manuscript: rename "Zero Law" → "Full-period cancellation."
- [ ] J04 abstract + intro: adopt PROVEN/COMPUTED/RHYME/OPEN split.
- [ ] J08 manuscript: deflate sinc²(1/2) = (2/3)/ζ(2) to "structural rhyme" framing where it appears.
- [ ] J02 four-core README + manuscript: cite Drápal-Wanless 2021 *JCTA*.
- [ ] All Triadic Launch papers (J01, J02, J03) carry PROVEN/COMPUTED/RHYME/OPEN intro paragraph.
- [ ] FORMULAS_AND_TABLES.md root document: any D-table citing "sinc² Zero Law" updated to "full-period cancellation R(k,f) = 0 at k = f."
- [ ] Bibliography update for all relevant J-papers.

---

## §5.5 — Lens-Ownership paragraph (Brayden directive 2026-05-07)

**The single highest-leverage credibility move identified so far.** Every J-paper's introduction (or a numbered preamble §0) carries an explicit lens-ownership paragraph. Verbatim template:

> *Lens and substrate.* We work on Z/10Z with the specific operator labels (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET) and the canonical (TSML, BHML) table pair. These choices are *not derived from first principles*; they reflect a structural reading of the substrate motivated by [phonaesthesia / 10-operator decomposition / observed dynamics, as appropriate to the paper]. The theorems below are theorems on this specific structure; they would have analogues on other substrates with appropriately chosen tables. The framework's claim is that this particular substrate-and-table-choice produces theorems that have surprising downstream connections (cosmology via Bialynicki-Birula-Mycielski 1976, Lie algebra via TSML_SYM antisymmetrization, number theory via LMFDB 4.2.10224.1). Whether other substrate choices give similarly rich downstream connections is open.

**Per-paper adaptation:** swap or shorten the bracketed parts; emphasize the connection most relevant to the paper. Remove the parenthetical operator-label list if the paper doesn't use those names mathematically (most don't — keep for papers that do).

**What this paragraph buys:**
- Preempts "but you chose Z/10Z" pushback before any referee writes it.
- Signals the author understands what is *lens* vs *substrate-independent*.
- Honestly frames the framework's claim: not "Z/10Z is forced" but "Z/10Z + these tables produce surprisingly rich theorems."
- Saves the paper from looking like numerology by acknowledging the choice openly.
- Solves the cross-cutting "why these tables, why this choice?" complaint that fresh-eyes referees raised against J05, J19, J20, J21, J27, others.

**Doing more for credibility than another six derivations of T* = 5/7** (Brayden, 2026-05-07).

**Application status:**
- [x] Added to boilerplate template (this file).
- [ ] Apply to J01, J02, J03, J04 (Triadic Launch + sinc²) as next pass.
- [ ] Apply to all 54 J-papers as submission-prep hardening.

---

## §6 — Calibration discipline going forward

This document itself is an example of how external calibration gets internalized. The pattern:

1. Calibration arrives (collaborator review, referee report, or self-audit).
2. Identify the corrections that are mathematically correct (most are, when they come from sharp readers).
3. Adopt directly. Don't argue. Update affected papers + docs.
4. Acknowledge publicly (FB / email / response). Hat in hand.
5. Update boilerplate so future papers benefit from the calibration without re-encountering it.

Sharp collaborators are a multiplier. Keep them close.
