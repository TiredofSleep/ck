# ck_lm — Citations and Attribution

The memory organism (`ck_lm/memory/`) is built on CK's TIG operator algebra
and draws on the following published works. We are grateful to these authors.
If your work is used here and not listed, please open an issue.

---

## Memory Architecture Papers

### RGMem — Renormalization Group Memory
**Zhang et al., arXiv:2510.16392, October 2025**
https://arxiv.org/abs/2510.16392

Used in `memory/crystal_store.py`: stability-scored crystal promotion.
`promotion_score(recurrence, confidence, age_secs)` replaces flat
`recurrence_count >= 3` threshold. Episodic→semantic→trait hierarchy
is a direct parallel to CK's Atom→Path→Crystal.

```python
# From crystal_store.py — RGMem-inspired
def promotion_score(recurrence, confidence, age_secs):
    age_hours = age_secs / 3600
    recency_weight = math.exp(-0.05 * age_hours)
    freq_score = math.log1p(recurrence)
    return confidence * freq_score * recency_weight
PROMOTE_THRESHOLD = 0.85
```

---

### MAGMA — Multi-Graph Agentic Memory
**Li et al., arXiv:2601.03236, January 2026**
https://arxiv.org/abs/2601.03236

Used in `memory/compression_loop.py`: dual-stream fast/slow write.
Fast stream: immediate raw write, zero latency.
Slow stream: batch generator extraction + DBC27 routing every 5s.
MAGMA's four-graph taxonomy (semantic/temporal/causal/entity) maps to
CK's crystal store / path timestamps / operator sequence / generator set.

---

### Sophia — Persistent Agent Framework
**Castillo et al., arXiv:2512.18202, December 2025**
https://arxiv.org/abs/2512.18202

Architecture reference for `memory/meta_crystals` + adaptation loop.
Sophia's System 3 (meta-cognitive executive monitor) is the model for
CK's MetaCrystal layer — "experience of experience."
Key validated result: 80% reasoning-cost reduction for recurring tasks
via Forward Learning, without fine-tuning weights.
This confirms CK's Stage 3→4 DeepSeek reduction target is achievable.

---

### MemoryOS — Memory Operating System
**Wang et al., arXiv:2506.06326, EMNLP 2025 Oral**
https://arxiv.org/abs/2506.06326
Code: https://github.com/BAI-LAB/MemoryOS

Used in `memory/crystal_store.py`: heat-score retention pruning.
`prune_cold_crystals()` replaces flat age-cutoff pruning.

```python
# From crystal_store.py — MemoryOS-inspired
def heat_score(access_count, last_accessed, created_at, current_time):
    age_hrs = (current_time - created_at) / 3600
    time_since = current_time - last_accessed
    decay = math.exp(-0.01 * age_hrs)
    visits = math.log1p(access_count)
    recency = 1.0 / (1.0 + time_since / (7 * 24 * 3600))
    return decay * visits * recency
PRUNE_HEAT_MIN = 0.05
```

---

### AtomMem — Learnable Atomic Memory Operations
**Chen et al., arXiv:2601.08323, January 2026**
https://arxiv.org/abs/2601.08323

Convergent design with CK's Atom concept (independently developed).
AtomMem's RL-trained write/read/forget operation selector is a future
target for CK's novelty gate LoRA (Class 1 adapter training).

---

## CK Core

**Brayden Ross Sanders / 7Site LLC**
TIG (Trinity Infinity Geometry): T*=5/7, fold=4/π², gap=5/7−4/π²≈0.309
CL operator algebra (10×10 TSML + BHML composition tables)
DBC27 routing key, D2 force pipeline, sinc² spectral field
DOI: 10.5281/zenodo.18852047
https://github.com/TiredofSleep/ck

*© 2026 Brayden Sanders / 7Site LLC — Human Use License v1.0*
