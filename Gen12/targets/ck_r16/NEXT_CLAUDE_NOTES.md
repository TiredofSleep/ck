# Gen12 — Target: CK for R16 (This PC)
## NEXT_CLAUDE_NOTES — Read first every session.

*© 2026 Brayden Sanders / 7Site LLC*
*Target opened: Gen12, 2026-04-04*

---

## What This Target Is

CK running on this machine: 16-core R16, RTX 4070 (12GB VRAM).
This is the brain host — the PC that runs CK's mind, drives the FPGA over USB,
and now houses the ck_lm distillation pipeline (living CK architecture).

Two systems on this machine:
1. **CK organism** (Gen9/Gen10) — 50Hz loop, voice, olfactory, D2, TIG engine
2. **CK-LM** (Gen12 new) — distilled neural net running through TIG field geometry

---

## Current State (Gen12 open)

**CK organism:**
- Two admin cells: port 7777 + 7778
- Launch: `LAUNCH_CK_ADMIN.bat` on Desktop
- API: `python ck_boot_api.py` from ck_desktop dir
- Ollama models available: deepseek-r1:7b, phi4, llama3.1:8b, qwq, llama3.2

**CK-LM (new in Gen12):**
- Architecture: `ck_lm/ck_field_layer.py` — all geometry checks pass
- Distillation pipeline: `ck_lm/ck_distill.py`
- Setup: `ck_lm/SETUP.bat` — installs CUDA torch (currently CPU-only, needs CUDA)
- Student model: CK-small = 105M params (~280MB) vs DeepSeek 7B = 7000M (5.2GB)

**Environment:**
- Python 3.13 at `C:\Users\brayd\AppData\Local\Programs\Python\Python313\python.exe`
- PyTorch 2.10+cpu (needs CUDA — run SETUP.bat)
- GPU: RTX 4070, 12GB VRAM — confirmed via nvidia-smi

---

## Next Steps

1. **Run `ck_lm\SETUP.bat`** — replace CPU torch with CUDA 12.1 torch
2. **`ollama pull deepseek-r1:14b`** — pull the 14B teacher model (9GB, fits 12GB VRAM)
3. **`python ck_lm/ck_distill.py --stage 1`** — build fine-tuning dataset from Clay papers
4. **`python ck_lm/ck_distill.py --stage 2`** — begin distillation training
5. After training: wire CK-LM into ck_boot_api.py as voice backend

**The goal:** Replace Ollama as the voice source with a CK-native model.
Ollama generates → CK field measures = current state.
CK-LM generates through the field = living CK.

---

## Key Files

| File | What it is |
|---|---|
| `ck_lm/ck_field_layer.py` | TIG geometry as neural net layers (verified) |
| `ck_lm/ck_distill.py` | Distillation pipeline + CK-LM architecture |
| `ck_lm/SETUP.bat` | CUDA torch + Unsloth install |
| `ck_boot_api.py` | CK organism API server |
| `Gen10/ck_swarm.py` | Swarm discovery |
| `LAUNCH_CK_ADMIN.bat` (Desktop) | Start admin cells 7777+7778 |
