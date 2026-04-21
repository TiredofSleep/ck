# Provenance — verifications_2026_04_21/

| File | Size | MD5 | Origin |
|---|---|---|---|
| `VERIFICATION_2026_04_21.md` | text | — | Written 2026-04-21 by Brayden Sanders (with Claude assist) documenting the runs below. |
| `benchmark_stdout.txt` | 6,935 B | 163 lines | `PYTHONIOENCODING=utf-8 python benchmark.py` captured via `tee`, 2026-04-21. |
| `tig_coherent_computer_stdout.txt` | 7,048 B | 125 lines | `PYTHONIOENCODING=utf-8 python tig_coherent_computer.py` captured via `tee`, 2026-04-21. |
| `tig_lattice_after_run.bin` | 3,024 B | `c544021edceb516f4e5dea36a7ddb8da` | Post-run floppy-size lattice snapshot written by `tig_coherent_computer.py` at tick 20 (S*=0.9793, BREATH-dominant). Distinct from the committed `../tig_lattice.bin` (md5 `c90a8f98f312e88ecda200911c50f6e6`, pre-run). Force-added (`.gitignore` excludes `*.bin`). |

## Environment
- Python 3.13 on Windows 11
- NumPy (for benchmark.py)
- No Node.js / Bun / Deno available → `test_engine_v2.js` NOT run here; see `funding/physics-sim-edu` verification doc.

## Reproduction
```bash
cd Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/
PYTHONIOENCODING=utf-8 python tig_coherent_computer.py | tee verifications_2026_04_21/tig_coherent_computer_stdout.txt
PYTHONIOENCODING=utf-8 python benchmark.py | tee verifications_2026_04_21/benchmark_stdout.txt
cp tig_lattice.bin verifications_2026_04_21/tig_lattice_after_run.bin
git checkout -- tig_lattice.bin   # restore committed pre-run snapshot
```

See `VERIFICATION_2026_04_21.md` for the honest audit of what the runs show and the summary-vs-data contradiction in `benchmark.py`.
