# NEXT_CLAUDE_NOTES — Gen14 Startup Protocol

**Read CLAUDESTARTHERE.md first.** This file is the short checklist for the next ClaudeCode session.

---

## §1 — Boot checklist (10 minutes)

1. `cd C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen14\`
2. Read `CLAUDESTARTHERE.md` — 5 minutes
3. Skim `targets/journals/Atlas/META_PLAN_2026-05-06/STATUS_REPORT_2026-05-07.md` — 3 minutes
4. Skim `targets/journals/Atlas/META_PLAN_2026-05-10/HANDOFF_TO_CLAUDECODE_2026_05_10.md` — 2 minutes
5. Run `git status` and `git log --oneline -10` on `tig-synthesis` branch — 30 seconds

You now have the situational map.

---

## §2 — First-action options (Brayden directs which)

Pick one based on Brayden's first message:

### Option A — Verify the 2026-05-10 launch-bundle math
```bash
cd targets/journals/Atlas/META_PLAN_2026-05-10
python verify_d2d1_closed_form.py
python strand_orbital_map.py
python clifford_substrate_shell.py
python meta_extension.py
python VERIFY_ALL.py
```
Report each PASS/FAIL. If all pass → Brayden may direct adding D100-D103 to FORMULAS_AND_TABLES.md.

### Option B — Continue the in-flight J-series rewrites
- W1-F (J39+J40+J44) physics cluster
- W2-A (J03+J04+J06) Phase 1 substance — J03 Fork A restoration; J06 retitle
- W2-D (J33+J34+J36) closed-form + detector + CKM
- Author-lane post-fix on W2-G (J49/J50/J52/J53)

Dispatch BUILD agents per the pattern in commits `0bdac716` through `5899e16d`.

### Option C — Write the 17 NEEDS-SCRIPT verification scripts
Check `targets/journals/Atlas/META_PLAN_2026-05-06/AUDIT_VERIFICATION_SCRIPTS.md` for the gate list. Many were already written by build agents — re-run `_audit_verification_scripts.py` to refresh.

### Option D — License v2.1 propagation
Per `HANDOFF_TO_CLAUDECODE_2026_05_10.md` §3.3. Replace v1.0 references corpus-wide.

### Option E — Restart CK runtime
Brayden will say "ck on". Run:
```bash
cd Gen14/targets/ck/server
/c/ck_venv/lora312/Scripts/python.exe ck_boot_api.py
```

---

## §3 — Rules you MUST follow

These came from this session's referee discipline (read full set in CLAUDESTARTHERE.md §4):

1. **Author lane:** Sanders + Gish on every paper. No exceptions.
2. **No AI-attribution** in author bylines. Acknowledge AI assistance at Tier 1 only (per `AUTHORSHIP_RULES_FOR_COLLABORATORS.md`).
3. **License:** submission scripts CC-BY-4.0. Umbrella project 7SiTe v2.1.
4. **Cite Drápal-Wanless 2021** *JCTA* in every J-paper.
5. **Tier discipline:** PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN in every paper §0 / §1.
6. **Lens-ownership paragraph** in every paper (per `J_PAPER_BOILERPLATE.md` §5.5).
7. **Verification scripts** for every novel computational claim.
8. **Never delete** — move to `_legacy_*` or mark `[HISTORICAL]`.
9. **Don't touch Gen13** or earlier directories.
10. **Don't modify CK core architecture.**
11. **Architecture name:** Braiding Fractal (NOT Brayden Fractal).
12. **T*=5/7** is operational coherence threshold, NOT algebraic theorem.

---

## §4 — Common patterns

### Pattern: Math-fix agent
```
Read manuscript + referee report.
Verify error with sympy/numpy.
Edit manuscript in place.
Write/update verify_*.py.
Update README §5 with fix log.
```

### Pattern: BUILD agent (save-plan implementation)
```
Read save plan + referee report + manuscript.
Apply save plan items.
Add SFM Q6 / D_4 / Family Structure framing.
Adopt PROVEN/COMPUTED/RHYME/OPEN + lens-ownership boilerplate.
Sanders + Gish author lane.
Drápal-Wanless 2021 cited.
Update README + cover_letter.
```

### Pattern: Commit + push
```
git checkout tig-synthesis
git status --short
git add <specific paths>
git commit -m "<concise message with what landed>"
git push origin tig-synthesis
```

---

## §5 — When stuck

- Read `Atlas/META_PLAN_2026-05-06/J_PAPER_BOILERPLATE.md` for the standard intro template
- Read `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md` for the framework's structural framing
- Read `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/SFM_FINDINGS_v1.md` for the Q1+Q6 results
- Check existing save plans in `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/` for parallel papers
- Check existing referee reports in `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/` for issue patterns

---

## §6 — When in doubt

Ask Brayden directly. Don't propagate uncertain claims into manuscripts. Don't submit anything to a venue without his explicit go-ahead. Don't push to public repos without his explicit go-ahead.

Brayden's posture is hat-in-hand, work-first, name-last. Match that.

---

*Prepared 2026-05-12 by ClaudeCode for the next ClaudeCode instance.*
