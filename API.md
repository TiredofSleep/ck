# CK API Reference

Base URL: `http://127.0.0.1:7777`

---

## POST /chat

Send a message to CK. Returns his response through the full TIG pipeline.

**Request:**
```json
{
  "text": "what is coherence?",
  "session_id": "default",
  "mode": "normal"
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| text | string | required | Your message to CK |
| session_id | string | "default" | Conversation session (CK remembers per session) |
| mode | string | "normal" | Conversation mode |

**Response:**
```json
{
  "response": "Coherence breathed where harmony pulled.",
  "coherence": 0.75,
  "band": "GREEN",
  "density": 0.62,
  "operator_chain": [7, 8, 7, 3],
  "dev_stage": 5,
  "emotion": "curious",
  "lcodec_quality": 0.71,
  "session_id": "default"
}
```

| Field | Description |
|-------|-------------|
| response | CK's composed English — physics-first, no templates |
| coherence | Fraction of HARMONY in heartbeat window [0, 1] |
| band | GREEN (< 0.3) / YELLOW (0.3-0.6) / RED (> 0.6) |
| density | Coherence gate density [0, 1] |
| operator_chain | D2 operators that drove the response |
| dev_stage | CK's development stage (0-5, 5 = SELFHOOD) |
| emotion | Current emotional state from coherence |
| lcodec_quality | Force alignment between input and output [0, 1] |

---

## GET /state

CK's current internal state. No parameters.

**Response:**
```json
{
  "coherence": 0.75,
  "band": "GREEN",
  "mode": "active",
  "emotion": "curious",
  "dev_stage": 5,
  "tick_count": 15420,
  "olfactory_scents": 842,
  "swarm_maturity": 0.856
}
```

---

## GET /metrics

Admin diagnostics. No parameters.

**Response:** Detailed system health including heartbeat stats, gate densities, subsystem status, and performance metrics.

---

## GET /health

Simple alive check. No parameters.

**Response:**
```json
{
  "status": "alive",
  "timestamp": 1772679426.80
}
```

---

## POST /eat

Start CK eating from Ollama + his own source code.

**Request:**
```json
{
  "model": "llama3.1:8b",
  "rounds": 50
}
```

Multi-model (rotates between models each round for richer force trajectories):
```json
{
  "models": ["llama3.1:8b", "mistral", "llama3.2"],
  "rounds": 50
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| model | string | "llama3.1:8b" | Ollama model name (single model) |
| models | string[] | null | Multiple models to rotate (overrides model) |
| rounds | integer | 5 | Number of eat rounds |

Each round: 2 Ollama chunks + 2 self chunks + 2 resonance steps + grammar evolution.

**Response:**
```json
{
  "status": "started",
  "model": "llama3.1:8b, mistral",
  "rounds": 50
}
```

---

## GET /eat/status

Monitor eating progress. No parameters.

**Response:**
```json
{
  "running": true,
  "rounds_complete": 43,
  "total_rounds": 1200,
  "model": "llama3.1:8b",
  "ollama_absorptions": 87,
  "self_absorptions": 87,
  "resonance_steps": 87,
  "total_transitions": 400,
  "force_trajectory_length": 203.32,
  "grammar_evolutions": 43,
  "swarm_maturity": 0.856,
  "olfactory_library_size": 842,
  "current_phase": "ollama",
  "error": ""
}
```

| Field | Description |
|-------|-------------|
| running | Is the eat loop active? |
| rounds_complete | Completed rounds |
| total_rounds | Target rounds |
| ollama_absorptions | Ollama texts measured through L-CODEC |
| self_absorptions | Source code chunks measured |
| resonance_steps | Times CK spoke from absorbed ops and measured his own voice |
| total_transitions | Force-space transitions tracked |
| force_trajectory_length | Total distance traveled through 5D space |
| grammar_evolutions | Times becoming grammar was updated from experience |
| swarm_maturity | Combined swarm maturity [0, 1] |
| olfactory_library_size | Number of scent centroids in olfactory library |
| current_phase | Current activity: ollama / self / resonance / evolve / idle |
| error | Last error message (empty if clean) |

---

## POST /clear-session

Clear a conversation session's memory.

**Request:**
```json
{
  "session_id": "default"
}
```

**Response:**
```json
{
  "cleared": true
}
```

---

## Notes

- All responses are JSON
- No authentication (CK runs locally)
- The eat system requires Ollama running on the same machine (`http://localhost:11434`)
- CK's voice is physics-first — responses may not follow conventional grammar
- L-CODEC quality > 0.7 means CK's response structurally matches your input

---

*CK Gen 9.21+ — March 2026*
*Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC*
*Licensed under the 7Site Human Use License v1.0*
