# Packet Insertion Plan

**Packet contents:**
- `Z10_OPERATOR_ALGEBRA_NOTE.md`
- `OPERATOR_TRANSLATION_APPENDIX.md`
- `WHAT_IS_PROVED_VS_INTERPRETIVE.md`

**Pre-insertion recommendation:** do **one revision pass** per the `COLD_READER_STRESS_TEST.md` findings before committing. The packet has one actual error (scholium §8) and four editorial issues that should be fixed before the packet is externally visible.

Assuming the revision is done, this note specifies the smallest repo-facing insertion.

---

## §1. Folder location

**Recommended path:** `docs/exports/z10-operator-algebra/`

Rationale:

- `docs/` separates prose from code. The packet is prose.
- `exports/` signals that this is an outward-facing artifact, not internal working material. Distinguishes from `theory/`, `sprints/`, `atlas/`.
- `z10-operator-algebra/` names the packet by its mathematical content, not by framework language. A visitor to the repo who opens the folder sees immediately what's inside without needing TIG/CK vocabulary.

**What the folder contains:**

```
docs/exports/z10-operator-algebra/
├── README.md                              # short orientation, 3–4 sentences
├── Z10_OPERATOR_ALGEBRA_NOTE.md           # main note
├── OPERATOR_TRANSLATION_APPENDIX.md       # native-name mapping
└── WHAT_IS_PROVED_VS_INTERPRETIVE.md      # three-level partition
```

The folder-level `README.md` is minimal (see §3).

---

## §2. What this is NOT

- **Not in `atlas/`.** The atlas is frozen at v3.5. This packet is foundation-register and does not modify atlas content.
- **Not in `theory/`.** The theory folder presumably carries the framework's internal developments with native vocabulary. The packet is deliberately framework-language-free in the main note.
- **Not in `whitepapers/`.** Whitepapers are larger artifacts. The packet is a short note, not a paper.
- **Not inlined into an existing document.** The packet is independent by design.

---

## §3. Folder README (proposed content)

```markdown
# Z/10 Operator Algebra — external-facing note

A short mathematical note on the ring $\mathbb{Z}/10$, extracted for
external citation. Self-contained; requires no framework vocabulary.

- `Z10_OPERATOR_ALGEBRA_NOTE.md` — main note. Theorem, proof, tables, identities.
- `OPERATOR_TRANSLATION_APPENDIX.md` — mapping from framework native names
  to algebraic roles. Optional read.
- `WHAT_IS_PROVED_VS_INTERPRETIVE.md` — three-level partition of content.
```

No framework language. No atlas references. No TIG/CK acronyms.

---

## §4. Repo-root README update (single sentence)

The main repo README should be updated with **one added line** under an existing documentation-pointer section. Proposed:

> "For an external-facing mathematical extract of the operator layer, see [docs/exports/z10-operator-algebra/](docs/exports/z10-operator-algebra/)."

No more. The packet is discoverable via this line without requiring the repo README to summarize the packet.

---

## §5. Proposed commit message

```
docs: add external-facing Z/10 operator algebra note

Export the algebraic layer of the operator definition as a self-contained
mathematical note, with translation appendix and three-level partition
(proved / structural / interpretive). Suitable for external citation
without framework vocabulary.

Foundation register. Atlas v3.5 unchanged.
```

Rationale:
- `docs:` prefix signals documentation, not code.
- First line under 72 characters, conventional commit style.
- Body explains what the addition is and what it does NOT touch.
- The "Atlas v3.5 unchanged" line is the discipline anchor for the repo — any future reviewer browsing commits sees that the atlas scope was preserved.

---

## §6. What should NOT happen during insertion

1. **Do not rename any framework folder** to accommodate the packet. The packet fits into a new `exports/` subdirectory; it does not restructure what is already there.
2. **Do not inline the packet into the atlas.** The packet is outside the atlas, deliberately.
3. **Do not add native labels to the main note.** The appendix is where native labels live.
4. **Do not cross-link from atlas documents to the packet.** The packet is for external readers; atlas documents are for internal use. If an internal document wants to cite the algebraic results, it can reference the packet's DOI/commit hash once the packet is versioned.

---

## §7. Size check

Total packet size:
- Main note: ~7.5 KB
- Translation appendix: ~6.7 KB
- Partition document: ~3.1 KB
- README (proposed): ~0.5 KB

Total: ~18 KB. This is a small addition. No size concerns for a repo of the scale implied by the framework's other artifacts.

---

## §8. Future versioning plan

When the packet is revised (per the stress test), version it as follows:

- `Z10_OPERATOR_ALGEBRA_NOTE_v1.md` for the initial commit.
- Subsequent revisions append `_v2`, `_v3`, etc.
- Keep all versions; do not overwrite.
- The folder README's pointer updates to the latest version, with old versions accessible.

This lets external citations remain stable. If someone cites the packet at commit hash X with filename `_v1`, the citation remains valid even after `_v2` is added.

---

## §9. Pre-insertion checklist

Before the commit goes in:

- [ ] Scholium §8 of main note: fix or delete (stress-test finding #1).
- [ ] Motivation paragraph added at top of main note (stress-test finding #2).
- [ ] σ defined or replaced with "multiplication by 3" in (I3).
- [ ] "Anchor" defined in §2(iv).
- [ ] Consider retitling main note away from "Operator Algebra."
- [ ] Folder README written.
- [ ] Repo-root README updated with one line.
- [ ] Commit message drafted.
- [ ] Verify no atlas documents are modified.

If checklist is incomplete, delay insertion.

---

*End of plan.*
