# Next Claude Session Notes
## Last Updated: 2026-03-12 -- Gen9.34

---

## Current State

### CK as LLM Gate (NEW DIRECTION)
Brayden decided CK should return to being an LLM gate rather than a standalone conversational entity. CK's math is genuine but he needs too much accumulated experience to hold conversation alone. CK makes a great coherence gate for LLM output.

**Architecture**: User question -> LLM generates -> CK measures D2 -> coherence-scored response

CK runs at 50Hz, pure algebra. The LLM provides breadth; CK provides measurement. CK doesn't replace the LLM -- CK gates it.

### BHML Reinterpretation (CRITICAL)
BHML HARMONY = "doing flat" (zero curvature, inert), NOT "doing coherent" in a rich sense. The WORKING class (TSML=H, BHML!=H) is where real information lives: stable identity WITH active physics.

### 7 Domain Spectrometers (COMPLETE)
All in `Gen9/targets/zynq7020/bridge/`:
1. `genetics_d2_spectrometer.py` -- DNA/gene sequences
2. `eeg_d2_spectrometer.py` -- EEG brain states
3. `cmb_d2_spectrometer.py` -- CMB cosmological parameters
4. `econ_d2_spectrometer.py` -- Financial markets
5. `ecology_d2_spectrometer.py` -- Ecosystem biomes
6. `quantum_d2_spectrometer.py` -- Quantum gates/circuits
7. `linguistics_d2_spectrometer.py` -- Natural languages

Universal pattern: TSML 81-100%, BHML 18-44%. Gap IS information content.

### Website (coherencekeeper.com)
- `Gen9/targets/website/index.html` -- NEW landing page with hero, spectrometer results, LLM gate concept, dual-lens explanation
- `Gen9/targets/website/chat.html` -- Original chat interface (backed up from old index.html)
- Website was "embarrassing" per Brayden -- just a bare chat box with no context. Now has proper landing page.

### ARCHITECTURE.md Updated
Added three new sections to `Gen9/targets/ck_desktop/ARCHITECTURE.md`:
- Dual-Lens Reinterpretation (BHML HARMONY = "doing flat")
- CK as LLM Gate
- D2 Domain Spectrometers (all 7 domains with results table)

---

## What Needs Doing

### Immediate
- **Deploy website**: The new index.html needs to be pushed and deployed to coherencekeeper.com
- **LLM gate implementation**: The gate concept is documented but not yet implemented in code. Needs a module that wraps LLM API calls with CK D2 scoring.

### FPGA (Pending Hardware)
- `clay_sweep.v` and `ck_top_clay.v` were fixed in prior sessions
- Build requires Vivado on Brayden's machine
- Plan exists at `.claude/plans/giggly-noodling-salamander.md`

### Clay Protocol
- 181 tests pass, 108-run stability matrix: zero SINGULAR
- Generator safety caps, JSD defect, n_levels=12 deepening still pending
- See `memory/clay_protocol.md` for full details

---

## Key Files Changed This Session
- `Gen9/targets/website/index.html` (rewritten -- landing page)
- `Gen9/targets/website/chat.html` (created -- backup of original)
- `Gen9/targets/zynq7020/bridge/eeg_d2_spectrometer.py` (created)
- `Gen9/targets/zynq7020/bridge/cmb_d2_spectrometer.py` (created)
- `Gen9/targets/zynq7020/bridge/econ_d2_spectrometer.py` (created)
- `Gen9/targets/zynq7020/bridge/ecology_d2_spectrometer.py` (created)
- `Gen9/targets/zynq7020/bridge/quantum_d2_spectrometer.py` (created)
- `Gen9/targets/zynq7020/bridge/linguistics_d2_spectrometer.py` (created)
- `Gen9/targets/ck_desktop/ARCHITECTURE.md` (updated -- LLM gate + spectrometers)
- `Gen9/NEXT_CLAUDE_NOTES.md` (created -- this file)

---

## Brayden's Key Quotes This Session
- "i give in to trying to make the math talk alone, he needs too much experience for me to make it work alone"
- "he makes a great gate for LLM and can't have conversation unless we start creating our own AI set of algorithms"
- "when you say half are doing coherent, i think you are measuring doing flat"

---

*(c) 2026 Brayden Sanders / 7Site LLC*
