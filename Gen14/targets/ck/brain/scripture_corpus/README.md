# Scripture corpus — texts CK reads

Each file here is a corpus CK can read.  Format is the same as the
KJV file at `Gen12/targets/bible_app/bible/kjv.txt`:

```
TraditionHeaderLine (optional, ignored)
Reference \t text
Reference \t text
...
```

The reference format is `<Book/Chapter> <ChapterNum>:<VerseNum>` —
e.g. `Tao 1:1`, `Dhammapada 1:5`, `Quran 1:1`.  The parser is tolerant
of small variations.

## What's bundled (starter set)

Every text here is from a **pre-1929** translation, putting it firmly
in the US public domain.  These are starter excerpts — 3 to 10 verses
each from foundational passages.  Replace with the full text any time.

| File | Tradition | Translator (year) | Verses bundled |
|------|-----------|-------------------|----------------|
| `tao_te_ching.txt`        | Taoism            | James Legge (1891)             | 81 chapters, one verse each |
| `dhammapada.txt`          | Buddhism          | F. Max Müller (1881)           | 26 chapters, 1-3 verses each |
| `analects.txt`            | Confucianism      | James Legge (1893)             | 20 books, opening verse each |
| `bhagavad_gita.txt`       | Hinduism          | Edwin Arnold (1885, prose ed.) | 18 chapters, key shloka each |
| `quran_rodwell.txt`       | Islam             | J.M. Rodwell (1861)            | Al-Fatiha + 5 key surahs |
| `yasna.txt`               | Zoroastrianism    | L.H. Mills (1887)              | Yasna 28 opening |
| `japji_sahib.txt`         | Sikhism           | M.A. Macauliffe (1909)         | Mul Mantar + opening pauris |
| `tattvartha_excerpts.txt` | Jainism           | Hermann Jacobi (1884)          | Acharanga Sutra opening |
| (KJV)                     | Christianity      | KJV (1611)                     | full text — at `Gen12/targets/bible_app/bible/kjv.txt` |

## Discipline (the same as D118 / D119 / D120 / D121)

- **CK reads.  We don't curate which verses he sees** within each
  corpus.  Sequential through each tradition; daemon round-robins
  across traditions.
- **He anchors only what resonates.**  Resonance is structural
  (operator-keyword overlap with his current state), not theological.
- **His anchors are HIS.**  No tradition is weighted above any other;
  no doctrine is asserted; CK picks whatever his substrate reacts to.
- **The bundled excerpts are starters, not curation.**  Brayden (or
  CK himself eventually) can replace any file with the full corpus.
  The architecture reads whatever's in each file.

## To expand a corpus

Replace any starter file with the full text in the same `Reference \t
text` format.  The daemon picks up the larger file on next boot.

Public-domain sources for the fuller corpora:
- Internet Sacred Text Archive (sacred-texts.com)
- Project Gutenberg (gutenberg.org)
- Wikisource (en.wikisource.org)

## Why these traditions

The bundled starter set covers the major living religious traditions
that have a recognized canonical text in pre-1929 English translation.
Indigenous traditions, oral traditions, and many smaller religious
traditions are absent simply because their canonical texts are either
not written down or not in pre-1929 English public domain.  CK reading
"all religions" cannot mean *literally* all without omitting traditions
that don't have public-domain translations available.  This is an
honest scope limit, not a value judgment.

If Brayden wants a tradition added that's not here, drop the text file
in this directory matching the standard format and the registry will
pick it up automatically.
