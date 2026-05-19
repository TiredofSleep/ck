# J56 — The Odd Magic Square Law (D129′)

**Target venue**: *Mathematics Magazine* (Mathematical Association of America)
**Alternative venues**: *American Mathematical Monthly* (problem section), *Journal of Recreational Mathematics*, *Mathematical Gazette*
**Status**: Ready for submission
**Author**: Brayden Ross Sanders / 7Site LLC

## Summary

A 5-page paper proving that the canonical odd-order Siamese magic square satisfies three structural identities (magic constant, median center, complement-orbit tiers) as corollaries of a single property: the construction is center-point symmetric. Generalizes the classical observations about Lo Shu to every odd $n$.

## Why this venue

*Mathematics Magazine* publishes accessible expositions of new mathematics aimed at undergraduates and instructors. The paper fits because:
- The proof requires only elementary point-reflection symmetry.
- Lo Shu is a cultural-mathematical icon in K-12 and recreational math literature.
- The verification script is 15 lines and runs in under a second.

## Theorem statement (one sentence)

For the canonical Siamese odd-order magic square of order $n$ with symbols $\{1, \ldots, n^2\}$:
- magic constant $= n(n^2+1)/2$
- center cell $= (n^2+1)/2$
- cell-tiers $=$ self-complement orbits under $s \mapsto n^2+1-s$.

All three identities follow from center-point symmetry of the Siamese construction.

## Files

- `manuscript.tex` — the LaTeX source
- `cover_letter.md` — submission cover letter
- `README.md` — this file

## Verification

Reference implementation at `papers/proof_d129_odd_magic_square_law.py`. Run with:

```bash
python papers/proof_d129_odd_magic_square_law.py
```

Verified at $n = 3, 5, 7, 9, 11, 13$ — all three identities hold exactly at every tested $n$.

## Submission process

1. Compile `manuscript.tex` with `pdflatex` (no special packages needed beyond standard `amsmath`/`amsthm`/`amssymb`/`hyperref`/`geometry`).
2. Submit via the Mathematics Magazine online portal: <https://www.maa.org/press/periodicals/mathematics-magazine>
3. Include cover letter as the journal's online submission system supports.
4. Attach the verification script as supplementary material.

## Expected timeline

- Submission to first decision: ~3 months (MAA journals typically reply faster than research journals)
- Revision cycle: ~4-6 weeks
- Acceptance to publication: ~6-12 months depending on issue scheduling

## Related canon entries

- **D129′** in `FORMULAS_AND_TABLES.md` — the canonical statement of the theorem
- `papers/proof_d129_odd_magic_square_law.py` — the verification script
- `META_SYNTHESIS_HUMANITY.md` §1.1 — the help-humanity scope

## Honest scope reminder

This is a small theorem. It generalizes Lo Shu's structure but does not unlock new mathematics. Its value is pedagogical and cultural-bridging: a clean example of how informal pattern-noticing becomes formal mathematics. The paper makes no broader claims and does not require the reader to share any worldview.
