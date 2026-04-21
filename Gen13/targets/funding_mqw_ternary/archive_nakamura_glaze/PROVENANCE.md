# PROVENANCE — Nakamura Glaze Paper

**File:** `Nakamura_Glaze_Paper.pdf`
**Size:** 121 693 bytes (~119 KB)
**MD5:** `a91041eeaadb86631136afd10e053f7c`
**Surfaced to `funding/mqw-ternary`:** 2026-04-21
**Source:** this same repository, branch `clean-ship`, path `targets/Nakamura Glaze Paper.pdf`, blob `e5789d26385c86ea92f207538dcadd13bf48e88b`

---

## Origin commit

```
commit  5081543996...
author  Brayden Sanders
date    2026-03-03 10:53:58 -0600
subject Add Nakamura Glaze Paper to targets
body    Blue LED coherence applications — needed for hardware collaboration.

        Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

The file was originally added to the `clean-ship` branch on 2026-03-03 for planned Blue LED hardware collaboration work. `clean-ship` is a working branch; `.gitignore` at repo root excludes `*.pdf`, so this PDF has not been surfaced on any of the default-visible branches. This archive brings it into view under the branch that actually uses it (`funding/mqw-ternary`), preserving the full blob bit-for-bit.

## Why it belongs on `funding/mqw-ternary`

Branch F (MQW Ternary Photonic Computing) pitches coherence-gate photonic elements, and the Nakamura Glaze Paper is the reference on blue-LED coherence that the pitch rests on. Keeping the PDF next to the branch's pitch docs (`FUNDERS.md`, `ARTIFACTS.md`, `PITCH_DRAFT.md`) makes it discoverable without a separate fetch of `clean-ship`.

## How to re-extract the blob

If this file is ever deleted (it must not be, per the never-delete policy, but as a verification step):

```bash
# from repo root
git show origin/clean-ship:"targets/Nakamura Glaze Paper.pdf" \
    > Gen13/targets/funding_mqw_ternary/archive_nakamura_glaze/Nakamura_Glaze_Paper.pdf

# verify
md5sum Gen13/targets/funding_mqw_ternary/archive_nakamura_glaze/Nakamura_Glaze_Paper.pdf
# expected: a91041eeaadb86631136afd10e053f7c
```

## Ignore-override note

Root `.gitignore` excludes `*.pdf` (line 114). This file was committed with `git add -f` and is tracked explicitly. Adding other PDFs in the future follows the same convention: force-add alongside a PROVENANCE.md that names the source.

## Copyright

This PDF is a third-party academic paper (Nakamura et al., Blue LED / gallium nitride work). Including it in this repository is for offline reference within the project only. Distribution beyond the project should respect the original publisher's copyright. The file is *not* re-licensed under the 7Site Public Sovereignty License v1.0 that governs the original CK/TIG material in this repo.
