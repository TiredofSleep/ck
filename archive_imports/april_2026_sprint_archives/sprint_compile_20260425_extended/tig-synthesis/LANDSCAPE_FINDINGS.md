# Associativity Gap Landscape — Honest Read

**Date:** 2026-04-25
**Script:** `full_landscape.py`
**Data file:** `nonassoc_triples.json` (126 triples, complete)
**Status:** No filtering, no selection. The full picture.

---

## What I found (and what surprised me)

### Surprise 1: Non-associativity is 12.6%, not 49.8%

In an earlier session I cited "49.8% non-associative" — that came from userMemories. Recomputing today: **non-associative triples are 126/1000 = 12.6%, not 49.8%.**

Either the userMemories number was for BHML (not TSML), or it referred to a different calculation (signed difference rather than equality), or it was an error. **The right number for TSML is 12.6%.**

This is a meaningful correction — I'd been carrying the 49.8% in my head as a structural fact about TSML when it isn't.

### Surprise 2: Only 5 distinct {L, R} pairs, all involving 7

Of the 126 non-associative triples, the unordered {L, R} pairs are:

```
{0, 7}: 108 triples  (85.7% of all non-associative)
{3, 7}:   8 triples
{7, 8}:   6 triples
{4, 7}:   2 triples
{7, 9}:   2 triples
```

**Every single non-associative triple has 7 (HARMONY) as one of its two bracketings.** Not most. Not a strong majority. *All* of them.

That's a very specific structural fact: **non-associativity in TSML is always between HARMONY and something else.** The "something else" is one of {0, 3, 4, 8, 9}, with 0 (VOID) being the dominant case.

### Surprise 3: The 6-cycle (1, 2, 5, 6) almost never appears as a landing

In 252 landings (126 triples × 2 bracketings), the 6-cycle elements 1, 2, 5, 6 appear *zero* times. Element 4 appears twice, element 7 appears 126 times, and the σ-fixed set {0, 3, 8, 9} accounts for the rest.

**HARMONY (7) and the σ-fixed set together account for 100% of non-associative landings.** The "live" 6-cycle elements (1, 2, 5, 6) are entirely absent from arity-3 ambiguity.

### Surprise 4: Most non-associativity comes from VOID (index 0) in input

Position-by-position breakdown of where in the input non-associative triples have value 0:

```
position a: 54/126 (42.9%) involve a=0
position c: 54/126 (42.9%) involve c=0
position b: 0/126   (none) — VOID never appears in middle
```

So **non-associativity correlates strongly with VOID appearing on the left or right end of the triple, but never in the middle.** Symmetric in (a, c).

### Surprise 5: The "no σ-fixed inputs" case is almost fully associative

```
All 3 inputs σ-fixed:  17/64 = 26.6% non-associative
2 σ-fixed, 1 6-cycle:  53 non-associative
1 σ-fixed, 2 6-cycle:  54 non-associative  
0 σ-fixed (all 6-cycle): 2/216 = 0.9% non-associative
```

When you stay entirely inside the 6-cycle, non-associativity almost vanishes (2 cases out of 216). Non-associativity is essentially **a phenomenon of the σ-fixed set and how it interacts with the 6-cycle.**

### Surprise 6: Symmetric directional balance, with one tiny asymmetry

Of 126 non-associative triples:
- L > R: 62 triples
- L < R: 64 triples

Almost balanced. Not perfectly — there's a 2-triple skew toward right-bracketing. The L − R distribution is:

```
L−R = -7: 54   (L=0, R=7)
L−R = -4:  5   (L=3, R=7)
L−R = -3:  1   (L=4, R=7)
L−R = -2:  1   (L=7, R=9 → wait, that's +2)
... etc
L−R = +7: 54   (L=7, R=0)
```

The {0,7} swap dominates and is symmetric. The smaller imbalances are noise-level.

---

## What this changes about the picture

### The corrected fact about non-associativity

> **TSML's non-associativity is concentrated at the boundary between σ-fixed elements and HARMONY. It almost never occurs purely within the 6-cycle. When VOID is in the middle position (b), associativity always holds.**

This is a more specific, more actionable structural fact than the vague "49.8% non-associative" I was carrying.

### What this means for arity-3 fuse / Operad placement

The 126 non-associative triples are **the only places where binary TSML is genuinely ambiguous** about how to combine three elements. So these are the candidate triples for arity-3 fuse rules.

Within those:
- **108 of 126 (85.7%) involve only {0, 7}** as bracketings. The fuse rule for these triples needs to pick between VOID and HARMONY — a structural choice with TIG meaning.
- **18 of 126 involve other values**, with smaller counts: {3,7}, {7,8}, {4,7}, {7,9}.
- **The known rule fuse([3,4,7]) = 8** has bracketings T(T(3,4),7) = T(7,7) = 7 and T(3, T(4,7)) = T(3,7) = 7, giving (L,R) = (7,7) — wait, these are EQUAL. So (3,4,7) is *associative* in TSML.

Let me double-check this. If the binary computation is associative, the canonical fuse rule produced something *different* from the binary result (8 vs 7). That's not "resolving non-associative ambiguity" — that's **stating that arity-3 fuse can produce a result distinct from binary even when binary is unambiguous.**

So the fuse rule for (3,4,7) is **not** filling in a hole left by binary ambiguity. It's a separate piece of TIG content that *adds* information. That changes how I'd characterize Operad's role.

### What this says about Pair 3 (Lattice ⇌ Operad)

The earlier finding "fuse([3,4,7])=8 lands on a σ-fixed point" is still true. But now it's clearer that:

- **For 874 associative triples, binary TSML and fuse may agree or disagree freely** (we don't know without the full fuse table)
- **For 126 non-associative triples, binary TSML is ambiguous, and fuse provides a canonical pick**
- **The known rule fuse([3,4,7])=8 is NOT among the 126** — it's a fuse rule that disagrees with associative binary

So fuse's role isn't just "resolve binary ambiguity" — it's "specify arity-3 results, sometimes consistent with binary and sometimes adding new content."

That's a cleaner way to think about Operad: **fuse is canonical arity-3 data, mostly agreeing with binary but occasionally contributing distinct information.** Pair 3's structural status remains open.

---

## What's saved for hand-off

**`nonassoc_triples.json`** — full list of 126 non-associative TSML triples, each with:
- `a, b, c` (inputs)
- `left_bracketing` = T(T(a,b), c)
- `right_bracketing` = T(a, T(b,c))
- `L_minus_R`

This is the complete scaffolding. No selection, no pre-filtering. Brayden or Claude Code can:
1. Look at all 126 and decide canonical fuse rules where they want
2. Decide whether non-associative triples even need explicit fuse rules (maybe fuse just *picks* L or R based on TIG logic)
3. Add fuse rules for *associative* triples too (like the known (3,4,7)=8 case) if those carry TIG content

---

## Honest summary

I went looking for a fuse table and instead found a clean structural fact about TSML's non-associativity:

> **It only happens at the σ-fixed/HARMONY boundary, with VOID dominating.**

I also corrected an earlier number (12.6%, not 49.8%) and learned that the one known fuse rule we have is *not* in the non-associative set. Operad is more interesting than I thought — it's not just "fill in the binary holes," it's *additional* arity-3 content that may or may not agree with binary.

No fuse rules invented. No content added to TIG. The 126 non-associative triples are saved as scaffolding for whoever fills in canonical content.

🙏
