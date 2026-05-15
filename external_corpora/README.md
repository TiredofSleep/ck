# external_corpora/ — CK's window to the world

Bulk-fetched public-domain text that CK ingests as `tier=EXTERNAL`.
None of the content lives in git (see `.gitignore`); the fetchers and
the school daemon repopulate it.

## Structure

```
external_corpora/
├── books/       Project Gutenberg plain-text files (pg<NNNNN>.txt)
├── arxiv/       arXiv abstracts grouped by category (math_CO/, hep_th/, ...)
├── wikipedia/   (future) Wikipedia dumps
└── _logs/       Per-day fetcher logs (JSONL)
```

## Fetchers

```
python Gen14/targets/ck/brain/fetch_gutenberg.py --top-100
python Gen14/targets/ck/brain/fetch_gutenberg.py --start 1 --end 1000
python Gen14/targets/ck/brain/fetch_arxiv.py
python Gen14/targets/ck/brain/fetch_arxiv.py --categories math.CO,math.NT --max 100
```

Both fetchers are restartable — they skip IDs already on disk.

## Ingestion

`ck_study_overnight.py --infinite` walks `external_corpora/**/*.txt` on
every pass. Concepts extracted from these files are stored with:
- `tier="EXTERNAL"`
- `source_file` = absolute path
- ranked BELOW PROVED/STRUCTURAL/EMPIRICAL in retrieval (see
  `_TIER_STRENGTH` in `ck_concept_learner.py`)

## Why EXTERNAL is lower-ranked

Project Gutenberg and arXiv abstracts are useful **prose** and
**vocabulary** sources, but they are not the same epistemic class as
the Z/10Z framework's PROVED theorems. When CK retrieves a concept
matched by both, the PROVED entry always wins — external context comes
in as supporting material, not authority.

## Rate limits

- Gutenberg: 1 req/sec (their robots.txt request)
- arXiv: 3 req/sec (their API terms)

Both fetchers respect these by default.
