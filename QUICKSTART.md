# CK Quickstart

Get CK running in 5 minutes.

---

## Requirements

- **Python 3.10+**
- **Ollama** (for eating) — https://ollama.ai
- **GPU optional** (RTX 4070 or similar for full GPU acceleration)

## Install

```bash
cd Gen9/targets/ck_desktop
pip install flask numpy
```

Flask is the only dependency for API mode. Full GUI mode also needs:
```bash
pip install kivy sounddevice requests beautifulsoup4
```

## Boot (API Mode)

```bash
cd Gen9/targets/ck_desktop
python -B ck_boot_api.py
```

CK starts at `http://127.0.0.1:7777`. You'll see all subsystems initialize:
```
  [SIM] HeartBeat: 32-sample window, CL 10x10
  [SIM] D2: Q1.14 pipeline, 22 roots
  [SIM] Olfactory: 5x5 CL field convergence
  [SIM] L-CODEC v1: language measurement online
  [SIM] Eat v2: transition physics engine ready
  [SIM] ALL MODULES AWAKE
```

## Talk to CK

```bash
curl -X POST http://127.0.0.1:7777/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "hello"}'
```

Response includes CK's words, coherence data, operator chain, and more.

## Feed CK (Eat)

Install a model in Ollama first:
```bash
ollama pull llama3.1:8b
```

Then start eating:
```bash
curl -X POST http://127.0.0.1:7777/eat \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.1:8b", "rounds": 50}'
```

Monitor progress:
```bash
curl http://127.0.0.1:7777/eat/status
```

CK measures Ollama's output through L-CODEC (5D force vectors), tracks transitions, absorbs into his olfactory field, and evolves his grammar. No text is memorized — only force trajectories.

## Boot (GUI Mode)

```bash
cd Gen9/targets/ck_desktop
python -m ck_sim
```

Opens the Kivy GUI with interactive terminal.

## Data Locations

| What | Where |
|------|-------|
| Olfactory library | `~/.ck/olfactory/` |
| Swarm experience | `~/.ck/ck_experience.json` |
| Lattice chain | `~/.ck/lattice_chain/` |
| L-CODEC gauges | `~/.ck/lcodec/` |
| Eat voice journal | `~/.ck/eat_journal.jsonl` |

All data persists across restarts. Delete `~/.ck/` to reset CK to a blank state.

## Available Ollama Models

CK can eat any model. Tested with:
- `llama3.1:8b` (4.9 GB) — default, good balance
- `llama3.2` (2.0 GB) — faster, less diverse force trajectories
- `mistral` (4.4 GB) — different texture
- `mixtral:8x7b` (22 GB) — richest trajectories, slowest

## Architecture

See:
- `WHITEPAPER_1_TIG_ARCHITECTURE.md` — Full system architecture
- `WHITEPAPER_4_GIVING_MATH_A_VOICE.md` — Every formula documented
- `CL_TABLE_EXPLAINED.md` — The algebraic core explained

---

*CK Gen 9.21+ — March 2026*
*Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC*
*Licensed under the 7Site Human Use License v1.0*
