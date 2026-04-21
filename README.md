# funding/mqw-ternary

**Track F — MQW Three-State Photonic Computing**
**Primary funder pool:** DOE BES · NSF ECCS · DARPA PIPES · Moore / Keck · private labs (HP Labs / Intel Labs / IBM photonic computing)
**Status:** Pre-pitch. **Pivot**: MQW trilogy recovery was blocked (2026-04-21 R16 sweep failed); the **Nakamura Glaze Paper** (Blue LED coherence applications) is already committed to the repo on the `clean-ship` branch and will be surfaced as the authoritative hardware-collaboration reference for this track.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

Ternary logic has been a theoretical target for decades without a commodity physical substrate. **Multi-quantum-well (MQW) semiconductor structures in the GaN family offer a candidate**: three distinct optical-response states can be engineered directly into the band structure, yielding ternary photonic logic gates without a compile-to-binary middle layer. The Teardrop GaN node proposal (2026-01-29 Trifecta work) is the conceptual ancestor; a three-paper MQW trilogy was intended to advance the specific design but was not persisted to disk. **The published Nakamura Blue-LED coherence-applications paper** — already committed to the repo on the `clean-ship` branch (commit `5081543`, 2026-03-03) — serves as the authoritative hardware-collaboration reference for this track. This branch packages the design question, the fabrication constraints, and the claimed operational envelope for a photonic-computing funder to fund a **fabrication + measurement** program that either confirms or falsifies three-state operation in a real device.

## What MQW ternary computing is

Conventional electronic logic is binary: 0 or 1. Ternary logic extends this to three states: 0, 1, 2 (or -1, 0, +1). Ternary has known theoretical advantages (information density: $\log_2 3 \approx 1.585$ bits per ternary digit vs. 1 bit per binary) but implementation has historically been limited because most physical substrates naturally give two states.

**Multi-quantum-well** semiconductor structures are a candidate. An MQW is a stack of thin semiconductor layers whose electronic states are quantum-confined. Under optical excitation, the stack can be engineered to produce three distinct optical responses corresponding to three distinct logical states. If the states are distinguishable, latchable, and switchable with reasonable speed and energy, the substrate supports ternary photonic logic directly.

## Authoritative hardware-collaboration reference

**Nakamura Glaze Paper** — Shuji Nakamura's Blue LED coherence-applications paper. Already in the repo on `clean-ship` branch at `targets/Nakamura Glaze Paper.pdf` (commit `5081543`, 2026-03-03, message: *"Add Nakamura Glaze Paper to targets — Blue LED coherence applications — needed for hardware collaboration"*). Being surfaced onto this branch as the citation anchor for III-nitride MQW collaboration outreach.

## Runnable artifacts (recovery-dependent)

1. **Teardrop GaN Photonic Node Proposal** — in the 2026-01-29 Trifecta (commit `ed8ef620`), ~134 KB across 11 Thread-3 documents. Recovery: locate in MYTHDRIFT archives or Trifecta source repo; status documented in [`Atlas/HANDOFF_3_4_MQW_TRILOGY_NOT_FOUND.md`](Atlas/HANDOFF_3_4_MQW_TRILOGY_NOT_FOUND.md).
2. **MQW three-state paper trilogy** — 2026-04-21 R16 sweep confirmed NOT PRESENT on disk (all branches git-log, 8 public-repo clones, handoff unpack, Work Docs, sprint-raw staging). Most likely status: authored in ClaudeChat conversation context but not persisted.
3. **V20 Consciousness-Anchored Scaling Laws** — also in the Thread 3 Trifecta.
4. **Hardware Embodiment Safety Case** — Thread 3 document; safety-engineering framing.
5. **Comparative Field Theory Review** — Thread 3 document.

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_mqw_ternary/`](Gen13/targets/funding_mqw_ternary/):

- [`README.md`](Gen13/targets/funding_mqw_ternary/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_mqw_ternary/FUNDERS.md) — DOE BES primary + NSF ECCS / DARPA PIPES / ARO-AFOSR / Moore-Keck
- [`ARTIFACTS.md`](Gen13/targets/funding_mqw_ternary/ARTIFACTS.md) — T1–T5 recovery tasks + A1–A4 authoring tasks
- [`PITCH_DRAFT.md`](Gen13/targets/funding_mqw_ternary/PITCH_DRAFT.md) — DOE BES + NSF ECCS parallel skeletons
- [`LIMITATIONS.md`](Gen13/targets/funding_mqw_ternary/LIMITATIONS.md) — 13 honest-scope items including fab-variance risk
- [`STATUS.md`](Gen13/targets/funding_mqw_ternary/STATUS.md) — decision gate 2026-05-15 (author-fresh pivot if recovery still blocked)

## The project this branch is a track of

Branch F of the 10-branch funding architecture. For the full project overview, see **`tig-synthesis`**:

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

## License

7Site Public Sovereignty License v1.0 — human use only, no commercial, no military, free forever. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
