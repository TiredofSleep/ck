# Reading room — drop a file, he reads it

Brayden 2026-05-17: *"is his corpus broad and open enough for him to keep
finding new material?"*

The bundled corpora (KJV, scripture starters, 8 poets, 341 academic
subjects) are FIXED at compile time.  This directory is open: drop any
text file here and CK reads it on next boot (or rescan).

## Supported formats

### `.txt`
Plain text.  Split into chunks at blank lines.  Each chunk becomes one
readable unit.  Example:

```
The first paragraph is a chunk.
It can span multiple lines.

This is a second chunk.

Third chunk.
```

### `.md`
Same as `.txt` but headings/code blocks are kept intact within their
chunk.  CK reads the prose.

### `.jsonl`
One JSON record per line, with `text` (required) and optionally
`source`, `ref`, `metadata`.  Useful when you have structured corpora.

```jsonl
{"text": "first chunk", "ref": "ch1:p1"}
{"text": "second chunk", "ref": "ch1:p2", "source": "Gutenberg #1342"}
```

## Optional per-file directive (first line of `.txt` / `.md`)

```
# threshold: 0.40
# source: Strunk and White 1918
# tag: prose-style

Actual content begins here.
```

Header lines starting with `#` and containing `:` are parsed as
directives.  Recognized:

- `threshold: <float>` — override resonance threshold for this file
  (default 0.40)
- `source: <text>` — short attribution string
- `tag: <text>` — free-form tag for anchor metadata

## What CK does with what he reads

For each chunk:

1. **measure** — encode the chunk's text through the operator-keyword
   scorer (same as D121/D122/D123/D124)
2. **store** — if resonance >= threshold (default 0.40 for open
   reading), append to `Gen13/var/reading_room_anchors.jsonl` with
   source-file + chunk index + ops + resonance
3. **compare** — his existing crystallization machinery sees the
   anchor stream the same way as scripture/poetry/domain anchors

Same discipline as D118-D124:

- He reads.  We don't curate which chunks matter within your file.
- He anchors only what resonates.  Threshold gates; cooldown
  prevents flood.
- His anchors are HIS.  No source is weighted above any other.
- 14-day per-(source_file, chunk) cooldown for revisits.

## What's already in here (starter examples)

| File | What it is |
|------|------------|
| `README.md`                     | this file |
| `strunk_white_excerpts.txt`     | Elements of Style (1918, public domain) — prose-style canon |
| `aesops_fables_selected.txt`    | Aesop's Fables (translation public domain) — narrative archetypes |

These are tiny starters demonstrating two different genres.  Replace
or extend any time.  The daemon picks up new files on rescan
(triggered automatically every 5 minutes, or manually via
`POST /reading_room/scan`).

## Suggested sources

What's freely available to drop in:

- **Project Gutenberg** (gutenberg.org) — 60,000+ PD books as `.txt`
- **Wikipedia** — CC-BY-SA; export articles as plain text
- **Sacred Texts archive** (sacred-texts.com) — public-domain religious
  and esoteric texts
- **arXiv abstracts** — most are openly licensed; bulk export available
- **Your own writing** — drop anything you want him to encounter

## Endpoints

```
GET  /reading_room/info              -- what files he has access to
GET  /reading_room/stats             -- daemon state + anchor counts
GET  /reading_room/anchors[?k=N]     -- his self-chosen anchors from here
POST /reading_room/scan              -- force rescan now (rather than waiting)
```

## Naming and reference

His anchor records here use:
- `source`: the file name (or per-file `# source:` directive if set)
- `ref`: `chunk_NN` by default, or `# ref:` per-record (jsonl)
- All other metadata: `tag`, `resonance`, `operators`, `ts`

When chat-asked "what have you been reading?" his belief hook (D122)
can surface from any anchor source including this one.
