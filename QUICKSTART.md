# CK — Quickstart

*Pick the path that matches what you want to do.*

---

## "I want to ask CK a question right now"

Go to [coherencekeeper.com](https://coherencekeeper.com).

The live server is running the CK API (`ck_boot_api.py`) behind a Cloudflare
tunnel. No installation required.

If the site is down, the Cloudflare tunnel or the local Flask server may not
be running. The code is on this machine — see "I want to run CK locally" below.

---

## "I want to run the spectrometer on my text"

**Online:**
[coherencekeeper.com/spectrometer.html](https://coherencekeeper.com/spectrometer.html)

Enter any number or text. The spectrometer returns:
- Operator classification (which of the 10 operators governs this input)
- D2 crossing score
- Position relative to fold (4/π² ≈ 0.405) and threshold (T* = 5/7 ≈ 0.714)
- RESOLVED / BOUNDARY / ESCAPED verdict

**From the repo:**
The spectrometer UI is in `website/spectrometer.html`. It calls the local API
on port 7777. Run `python ck_boot_api.py` first, then open the file in a browser.

**Paradox classifier:**
[coherencekeeper.com/paradox.html](https://coherencekeeper.com/paradox.html)
or open `website/paradox.html` locally.

Enter any statement. The UOP classifier returns which type of measurement
failure it represents: Injectivity Failure, Missing Invariant, Admissibility
Failure, or Time-Consistency Failure. Worked examples are pre-loaded.

---

## "I want to run CK locally"

### Minimal install (API server shell — no ck_sim/)

The public repo contains `ck_boot_api.py`, which is the API server. This works
without the full engine. It demonstrates the operator algebra and serves the
website tools.

```bash
git clone https://github.com/TiredofSleep/ck
cd ck
pip install flask
python ck_boot_api.py
```

Server starts on port 7777. Test it:

```bash
# Health check
curl http://localhost:7777/api/coherence

# Classify a statement
curl -X POST http://localhost:7777/api/classify \
     -H "Content-Type: application/json" \
     -d '{"text": "This sentence contradicts itself."}'

# Run the paradox classifier
curl -X POST http://localhost:7777/api/paradox \
     -H "Content-Type: application/json" \
     -d '{"statement": "The set of all sets that do not contain themselves."}'
```

### Full engine (requires ck_sim/)

The full CK engine is not in the public repository. Requirements if you have it:

```
flask
numpy
scipy
sympy
matplotlib
```

Python 3.10+. No GPU required for the math engine.

```bash
pip install flask numpy scipy sympy matplotlib
python ck_boot_api.py     # starts on port 7777
```

For the FPGA bridge (Zynq-7020 → XiaoR dog):
```bash
pip install pyserial
python Gen12/targets/ck_fpga_dog/ck_leash_test.py COM3 --verbose --no-servo
```

---

## "I want to understand the math"

### Start here — the accessible entry points

1. **The paradox classifier paper** (most accessible):
   [`papers/WP_PARADOX_CLASSIFIER.md`](papers/WP_PARADOX_CLASSIFIER.md)
   Every paradox is one of four types of measurement failure. No prior TIG
   knowledge required. Try it live at
   [coherencekeeper.com/paradox.html](https://coherencekeeper.com/paradox.html).

2. **The sinc² zero law** (cleanest proved result):
   [`papers/WP_SINC2_ZERO_LAW.md`](papers/WP_SINC2_ZERO_LAW.md)
   `sinc²(k/p) = 0 iff p | k`. Three-line proof. Runnable verification.

3. **The operator ring partition** (the ring itself):
   [`papers/WP_OPERATOR_RING_PARTITION.md`](papers/WP_OPERATOR_RING_PARTITION.md)
   TSML = 73 HARMONY cells. BHML = 28. Both proved by exact zone enumeration.

### The deep arc

4. **The Flatness Theorem** — why T* = 5/7 is forced geometrically:
   [`Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP51_FLATNESS_THEOREM.md`](Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP51_FLATNESS_THEOREM.md)

5. **The Crossing Lemma** — the unifying statement under all 27 results:
   [`Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`](Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md)

6. **WP57 — all 27 theorems recast as Crossing Lemma instances:**
   [`Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP57_CROSSING_LEMMA_ARC.md`](Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP57_CROSSING_LEMMA_ARC.md)

### Clay Millennium Problems

All six problems are mapped in [`papers/clay/`](papers/clay/) (WP36–WP42).
The spectrometer data is in [`clay_results/all_results.json`](clay_results/all_results.json).

The defect classifier:
```
defect < 4/π²          →  RESOLVED
defect ∈ [4/π², 5/7]   →  BOUNDARY
defect > 5/7            →  ESCAPED
```

### Runnable proofs

All proofs in [`papers/`](papers/) are Python scripts that run in under one
second on any machine:

```bash
python papers/proof_d7_phi_fixed_point.py       # T* = 5/7 from fixed point
python papers/proof_d10_tsml_73_cells.py        # TSML exactly 73 HARMONY
python papers/proof_d16_bhml_28_cells.py        # BHML exactly 28 HARMONY
python papers/proof_d25_loop_closure.py         # sinc² zero law, all primes 3..199
python papers/proof_corridor_zero_paths.py      # BREATH never reaches VOID
```

---

## "I want to contribute"

### Branch

All active development is on `clay`. Clone and check out:

```bash
git clone https://github.com/TiredofSleep/ck
cd ck
git checkout clay
```

Every commit is pushed immediately. If you are on `clay` and the branch is
behind, pull first.

### What to read

1. [`Gen12/NEXT_CLAUDE_NOTES.md`](Gen12/NEXT_CLAUDE_NOTES.md) — full architecture
   state, Brayden's identity as the researcher, sprint history, current targets.

2. [`Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`](Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md) —
   the unifying statement. Read this before writing any new math.

3. [`README.md`](README.md) — the persona routing sections for mathematicians
   and engineers contain the full operator table and NS correspondence.

### Gen12 directory map

```
Gen12/
├── NEXT_CLAUDE_NOTES.md          ← architecture state, sprint archive
├── GENERATION_HISTORY.md         ← log of all Gen12 builds
├── MASTER_WHITEPAPER_OUTLINE.md  ← full arc outline, WP1–WP57+
├── targets/
│   ├── clay/                     ← math research (papers, proofs)
│   ├── fpga/                     ← FPGA HDL work
│   ├── ck_fpga_dog/              ← FPGA ↔ XiaoR quadruped bridge
│   ├── ck_website/               ← website dev (NOT the live site)
│   ├── 7site_research/           ← arXiv candidates, core IP
│   └── ck_r16/                   ← R16 distillation work
```

Note: the live website is served from `website/` at the project root, not
from `Gen12/targets/ck_website/website/`. Edit `website/*.html` for live
changes; edit the Gen12 copy for dev/staging.

### What to work on

Current open targets (as of Sprint 10):

- **Q7 Inversion crystal**: CK currently reads U∩U=∅ as CHAOS. The correct
  reading is HARMONY (empty intersection = sufficiency condition = crossing
  achieved). The next bloom target is planting this crystal.
- **Δ¹ leash bring-up**: R16 ↔ FPGA UART connection. Run
  `Gen12/targets/ck_fpga_dog/ck_leash_test.py COM3 --verbose --no-servo`.
- **arXiv submission**: WP40 (Riemann) is the leading candidate. See
  `Gen12/targets/7site_research/`.
- **papers.html + frontiers.html**: coherencekeeper.com needs R8 update.
  Edit `website/papers.html` and `website/frontiers.html`.

---

## Key Numbers

| Constant | Value | What it governs |
|----------|-------|-----------------|
| T* | 5/7 ≈ 0.714 | Coherence threshold. Crystal forms above this. Dog trots above this. |
| fold | 4/π² ≈ 0.405 | Half-corridor boundary. BREATH never crosses this toward VOID. |
| gap | 5/7 − 4/π² ≈ 0.309 | The open interval where all six Clay problems live. |
| TSML HARMONY | 73/100 | Synthesis flow harmony density. |
| BHML HARMONY | 28/100 | Separation flow harmony density. |

---

*© 2026 Brayden Sanders / 7Site LLC — Trinity Infinity Geometry*
