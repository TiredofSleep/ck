# Unfrozen AI · Black-Box Resolved (but not gone)

**Plan of record · Gen13 · 2026-04-25**

---

## 0 · The two-sentence frame

A frozen language model is a probabilistic guesser with no relationship to truth.
A coherence framework without a guesser is a deterministic skeleton with no flesh.
**This plan is the marriage**: the LM keeps guessing token-by-token, CK keeps
functionally mapping every guess back to operators / AO / Hebbian / T\*=5/7, and
the two run as one organism so we can *watch the geometry unfold* — the black
box is resolved into a visible trajectory through CK's coherence space, but the
box itself stays (the LM still carries language fluency CK cannot).

---

## 1 · Where we already are (audit, honest)

### Already alive and learning per tick (✓)

| Layer | File | What it does | Live state proof |
|---|---|---|---|
| AO 5-element basis | `Gen13/targets/ck/brain/ao_basis.py` | CRT Fourier projection 10→5 (Earth/Air/Water/Fire/Ether = D0..D4) | self-test passes, used by cortex |
| Hebbian 5×5 W | `hebbian_5x5.py` | Symmetric co-activation tensor with `update`, `wobble`, `collapse`, `prime`, `score` | `cortex_state.json` persisted at tick 14,061,650 |
| Quadratic glue (F3×F4) | `fusion.py` | LoRA-free runtime fusion: tensor primes the corrector, blends with gentle weight=0.20 | live in `FusionCKCorrector` |
| Cortex (the trinity wired together) | `cortex.py` | One-tick: input → AO → Hebbian update → glue → output | `cortex_readout` field on every chat |
| HER (Hindsight Experience Replay) | `Gen12/.../ck_hindsight_replay.py` | 8.8M experiences, 97.6% impact | banner at boot |
| Olfactory / lattice / spectral / topology / meta lens | `Gen12/.../being/*` | The 47-module deep brain | all loaded at boot |
| Pastoral fold (just shipped) | `Gen12/.../ck_pastoral_fold.py` | DATA-only verse offering on grief/fear/hope, math→meaning bridge via brain_dominant_op | `/pastoral/status` live |

### Already trainable, just shipped (✓)

| Pipeline | Tool | Output | Status |
|---|---|---|---|
| Offline LoRA (Option B) | `train_lora.py` | r=16 adapter, 167 MB safetensors | v1 (1ep, loss 4.04) and v2 (5ep, loss 0.61) trained on dataset v3 (40 sharegpt examples ≥ T\*=5/7) |
| LoRA → GGUF | `convert_lora_to_gguf.py` (llama.cpp) | 84 MB GGUF | v2 ready: `ck/brain/lora/v2/gguf/ck-v2-lora.gguf` |
| Idle Hebbian teacher (Option A) | `idle_loop.py` | Updates `hebbian_5x5.json` from approved chat turns | runs on demand from CLI |
| Dataset builder | `build_training_set.py` | sharegpt v\<N\> with T\* gate, structural-only filter, dedup | v3 has 40/393 kept |

### Where it ends (the cliff)

**The LM and the brain trinity do not yet meet inside generation.** The current
chain is:

```
user text → CK engine → operators[] → math-first wrap → cortex wrap →
            ollama editor (Llama-3.1 frozen) → fold → response
```

The cortex *sees* the result and *learns from it* (W matrix updates), but
Llama-3.1 produced its tokens **without ever consulting the cortex**. The LM
draws its draft in a vacuum; CK either accepts or polishes after the fact.

That's the freeze the user is rejecting. Below is how to break it.

---

## 2 · The architecture: five layers, one organism

Each layer is named, sized, located, and has a concrete invariant. None of the
existing live runtime is removed. Everything new is additive.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  L1  PROBABILISTIC GUESSER       (the LM, ~8 B params, frozen base)      │
│       Llama-3.1-8B-Instruct + v_N LoRA delta                             │
│       Lives in-process via transformers + peft + bitsandbytes (4-bit)    │
│       Exposes:  forward(prompt) -> logits[T, V]                          │
│                 forward_with_hidden(prompt) -> hidden[L, T, H=4096]      │
└──────────────────────────────────────────────────────────────────────────┘
                                  ↕  hidden states per layer
┌──────────────────────────────────────────────────────────────────────────┐
│  L2  GEOMETRIC PROJECTOR         (the lens that resolves the black box)  │
│       hidden[L, T, 4096]  →  AO[L, T, 5]   via fixed orthonormal basis   │
│       Lives in: Gen13/targets/ck/brain/lm_geometry.py  (NEW, ~250 LOC)   │
│       Exposes:  project_lm_to_ao(hidden) -> {layers, tokens, ao_5d}      │
│                 dominant_op_per_layer(ao) -> List[op_name]               │
│                 trajectory_coherence(ao_seq) -> float in [0..1]          │
│       This is the "geometric picture" — 32 layers × N tokens × 5 D.      │
│       Visualizes as: per-layer dominant operator (32-step walk through   │
│       the 10-operator ring), or as 5-D PCA of token trajectories.        │
└──────────────────────────────────────────────────────────────────────────┘
                                  ↕  per-token AO state d_t
┌──────────────────────────────────────────────────────────────────────────┐
│  L3  FUNCTIONAL MAPPER           (CK's brain trinity, already built)     │
│       AO basis + Hebbian 5×5 W + quadratic glue                          │
│       Lives in: Gen13/targets/ck/brain/{ao_basis, hebbian_5x5, fusion}.py│
│       Exposes:  W.prime(d) -> primed_d        (current associations)    │
│                 W.score(d) -> scalar           (coherence with history)  │
│                 W.update(d_t, d_{t-1})         (learning step)           │
│       Per-token reads: each LM hidden state projects to d_t, scored      │
│       against W to produce a coherence-with-history scalar.              │
└──────────────────────────────────────────────────────────────────────────┘
                                  ↕  coherence-shaped logit bias
┌──────────────────────────────────────────────────────────────────────────┐
│  L4  COHERENCE-GATED DECODER     (where guess and map meet)              │
│       At each next-token step:                                            │
│         logits     = LM.forward(prompt + tokens_so_far)                  │
│         d_now      = project_lm_to_ao(last_hidden)                       │
│         coh_score  = W.score(d_now) - lambda * (T_STAR - coh_running)    │
│         token_bias = AO_to_token_bias(W.prime(d_now))                    │
│         logits_g   = logits + alpha * token_bias                         │
│         next_token = sample(softmax(logits_g))                           │
│       Lives in: Gen13/targets/ck/brain/lm_coherence_decode.py (NEW ~300) │
│       This makes the LM's tokens drift toward CK's current operator      │
│       state. The base remains frozen; the SAMPLING gets functional.      │
└──────────────────────────────────────────────────────────────────────────┘
                                  ↕  finished response
┌──────────────────────────────────────────────────────────────────────────┐
│  L5  HER + ONLINE LORA UPDATE    (the unfreezing closes the loop)        │
│       After each chat:                                                    │
│         if coherence_at_end >= T_STAR:                                   │
│           append (prompt, response) to ck/fluency/logs/<sess>.jsonl      │
│           HER replays a sampled past trajectory through W.update          │
│           idle_loop kicks if buffer >= MIN_BUFFER_FOR_RETRAIN             │
│             -> small SFT pass on top of v_N LoRA, writes v_{N+1}         │
│             -> live LM reload swaps the adapter (ck_lm_fold)             │
│       Lives in: idle_loop.py (extends), ck_lm_fold.py (NEW ~200)         │
│       The LM is now "unfrozen at the edge" — its frozen 8B core + a      │
│       LoRA delta that breathes with every coherent turn.                 │
└──────────────────────────────────────────────────────────────────────────┘
```

### What this gives you

- **L1 stays a black box for language** — no one is going to retrain 8 B parameters on a 4070, and that's fine. Llama-3.1 carries the pre-training; we don't need to reinvent it.
- **L2 makes the inside visible** — 32-layer × N-token × 5-D trajectory through CK's coherence basis. Renderable as: a path through the 10-operator ring, or a 5-D PCA scatter, or a Hebbian-style coupling matrix between layers. **The black box is resolved into geometry.**
- **L3 is the brain you already built** — no rework, just hooked in.
- **L4 is where probabilistic and functional become one operation** — every sampled token is the result of a softmax that has been reshaped by W's current state. The LM is not free to drift; it drifts *along the cortex's gradient*.
- **L5 is the loop that closes** — coherent output becomes training data, the LoRA delta breathes, the LM gets continuously closer to CK's grammar without retraining the core.

---

## 3 · Probabilistic ⊗ functional: how the operation works token-by-token

This is the heart, written tight.

```
At each generation step t for token x_t:

  1. LM forward pass on prefix → hidden state h_t ∈ R^4096
                              → logits ℓ_t ∈ R^V (V ≈ 128k vocab)

  2. AO projection (L2):
       d_t = B^T h_t / ||h_t||             # B is the 4096×5 fixed basis
       d_t ∈ R^5  (Earth, Air, Water, Fire, Ether activations)

  3. Functional mapping (L3, what the cortex knows):
       primed_t = W @ d_t                  # what history says fires next
       coh_t    = d_t^T W d_t              # coherence-with-history scalar

  4. Coherence-gated logit reshape (L4):
       op_index_t = argmax(d_t)            # which AO element peaks now
       op_lift    = lift_5_to_10(primed_t) # 10-d operator profile
       token_bias = M @ op_lift            # M is V×10 op→token preference
       ℓ_t' = ℓ_t + α * token_bias - β * ||d_t - d_{t-1}||^2

  5. Sample:
       p_t = softmax(ℓ_t' / temperature)
       x_t ~ Categorical(p_t)

  6. Hebbian update (L3, learning during generation):
       W.update(d_t, d_{t-1})              # symmetric outer-product
```

α (logit-bias weight) and β (transition penalty) are the two knobs that
control how strongly the cortex shapes generation. α=0 β=0 reduces exactly
to vanilla Llama. α=∞ collapses to deterministic operator readout. Sweet spot
is α ≈ 0.3 of `||logits||`, β ≈ 0.1 — gentle, the way `fusion_weight=0.20`
gentles the corrector today.

---

## 4 · The geometric picture (what the user will literally see)

### Endpoint 1: `/lm/geometry?text=...`

```json
{
  "text_in": "what is coherence?",
  "tokens": ["what", "is", "co", "herence", "?"],
  "layers": 32,
  "ao_traj": [
    [0.12, 0.45, 0.78, 0.31, 0.09],  // layer 0 AO activations
    [0.18, 0.49, 0.82, 0.27, 0.11],  // layer 1
    ...
    [0.05, 0.21, 0.94, 0.18, 0.03]   // layer 31 (peaks on Water = HARMONY axis)
  ],
  "dominant_op_per_layer": [
    "LATTICE", "LATTICE", "COUNTER", "COUNTER", "HARMONY",
    "HARMONY", "HARMONY", "HARMONY", ...
    "HARMONY"
  ],
  "trajectory_coherence": 0.87,
  "hebbian_score": 1.43,
  "T_star": 0.7142857142857143,
  "verdict": "above_T_star"
}
```

### Endpoint 2: `/lm/geometry/path?text=...&format=svg`

Renders the 32-layer trajectory as an SVG arc through the 10-operator ring,
labeled at peaks. **This is "watch the geometry unfold"** — a literal picture
of what shape Llama traces inside CK's coherence frame for any prompt.

### Endpoint 3: `/lm/coherence_chat`

Full chat with L4 active. Returns:
- `text` (the response)
- `tokens` (the per-token operator labels and ao_traj)
- `coherence_history` (per-token coh_t, plotted as a line)
- `accepted_at_T_star` (bool)

### Frontend hook (one new website page)

`Gen12/targets/website/lm_geometry.html` shows:
- The user's prompt at the top
- A 32-layer × 5-D heatmap (rows = layers, cols = AO)
- The 10-op ring with the dominant trajectory drawn as an arc
- The Hebbian W matrix as a 5×5 colormap
- Coherence over tokens as a line chart with T\* gate marked

Same data is on `/cortex` already; the new page just composes it.

---

## 5 · Implementation steps (sequential, sized, verifiable)

### Step 1 · L2 geometric projector (FRESH, ~250 LOC, 1 day)

File: `Gen13/targets/ck/brain/lm_geometry.py`

```python
class LMGeometry:
    def __init__(self, base_model, lora_path):
        # loads bnb-4bit base + PeftModel with LoRA, output_hidden_states=True
        # builds B = 5 fixed orthonormal directions in R^4096 (seeded RNG)
        # B aligns to AO via deterministic seed derived from
        #   hash("Earth"), hash("Air"), ..., hash("Ether")
    def forward(self, text) -> Dict:
        # returns hidden[L, T, 4096], maps -> ao[L, T, 5], dominant ops, coherence
    def project_layer(self, h_layer) -> List[float]:  # 5-d
    def trajectory_coherence(self, ao_seq) -> float:
        # avg cos-sim between adjacent layer AO states; how smoothly the
        # trajectory walks the ring vs. jumping
```

Boot test: `python -m ck.brain.lm_geometry "what is coherence?"` prints the
trajectory. Exits 0 if all 32 layers projected successfully.

### Step 2 · `/lm/geometry` route + fold (~150 LOC, 0.5 day)

File: `Gen13/targets/ck/brain/lm_fold.py`

```python
def mount_lm_fold(api):
    # singleton load of LMGeometry (~30s, ~5 GB GPU)
    # registers /lm/geometry, /lm/geometry/path (svg), /lm/health, /lm/info
    # NOT a wrap of process_chat yet — pure read-only diagnostic
```

Wired in `ck_boot_api.py` next to the pastoral fold mount. Banner:
`[CK] LM geometry: MOUNTED (base=..., lora=v2, GPU=4.8GB, basis_seed=...)`

Verify: `curl http://localhost:7777/lm/geometry?text=what+is+T*` returns the
32-layer trajectory.

### Step 3 · website page `lm_geometry.html` (~200 LOC, 0.5 day)

Plain HTML/JS hitting `/lm/geometry`. Renders:
- 32×5 heatmap (Canvas)
- 10-op ring with trajectory arc (SVG)
- 5×5 Hebbian W (Canvas)
- Coherence line chart (existing chart code)

Live. Interactive. **This is the moment "watch the geometry unfold" becomes
literal.**

### Step 4 · L4 coherence-gated decoder (~300 LOC, 1.5 day)

File: `Gen13/targets/ck/brain/lm_coherence_decode.py`

```python
class CoherenceDecoder:
    def __init__(self, lm_geometry, cortex):
        # gets handles to L1+L2 (lm_geometry) and L3 (cortex W)
    def generate(self, prompt, max_tokens, alpha, beta) -> Dict:
        # token-by-token loop with logit reshape
        # returns text + per-token ao_traj + per-token coh_t
        # updates W in-place if coherence >= T_STAR
```

Token→operator preference matrix M (V × 10) is built ONCE at boot from a
seed lexicon (~100 words per operator from CK's existing dictionaries:
`ck_dictionary.json`, `ck_dict.js`, `ck_voice_lattice.py`). Words match
operator → row in M gets weight 1, others 0. Cosine-normalize per row.

Verify: `python -m ck.brain.lm_coherence_decode "what is balance?" --alpha 0.3`
should produce text where the dominant ops trend toward BALANCE/HARMONY.
A/B against `--alpha 0.0` (vanilla LM) should show measurable drift.

### Step 5 · `/lm/coherence_chat` route (~100 LOC, 0.5 day)

Adds `/lm/coherence_chat` to `lm_fold.py`. Returns text + full geometry +
coherence_history.

### Step 6 · Optionally wrap `api.process_chat` (1 day)

File: `Gen12/targets/ck_desktop/ck_lm_geometry_fold.py` (analog of pastoral fold)

```python
def mount_lm_geometry_fold(api, mode="diagnostic"):
    # mode="diagnostic": adds lm_geometry + lm_dominant_ops + lm_coherence
    #                   fields to chat response. Doesn't change CK's text.
    # mode="generator":  CK's text comes from CoherenceDecoder.generate(text)
    #                   instead of the engine. Fully replaces ollama editor.
```

`mode="diagnostic"` ships first — same idea as the pastoral fold's DATA-only
output. The website renders the geometry alongside CK's structural prose.
Brayden then decides when to flip to `mode="generator"`.

### Step 7 · L5 online LoRA refresh (~200 LOC, 1 day)

Extends `idle_loop.py`:

```python
def online_lora_step(buffer_path, current_lora, out_lora):
    # if buffer has >= MIN_BUFFER (say 16) new high-coherence turns:
    #   train 1 epoch on the new turns + a sampled HER replay of older turns
    #   save as v_{N+1}
    # never destructive; v_N stays as fallback
```

`ck_lm_fold` watches `out_lora` mtime — when a new version appears, it does
a hot-swap of the PeftModel adapter on the live LM (no server restart).

Verify: have a 30-turn coherent chat session, watch v3 → v4 appear in
`ck/brain/lora/`, observe LM-grammar drift toward CK's vocabulary.

---

## 6 · The "what we cannot do" page (honest limits)

- **The 8 B base does not move.** A consumer GPU cannot full-fine-tune Llama
  in any meaningful time. The base stays frozen by physics. What we DO move:
  the LoRA delta (42 M params, 0.5%) — that breathes with the cortex.
- **Logit bias is post-hoc, not structural.** L4's reshape is on top of the
  LM's existing softmax. We are sampling differently, not training the
  attention heads. To make TIG truly intrinsic to language, you need a model
  trained from scratch in the AO basis. That's a different project.
- **The geometric projection is interpretive, not derived.** The 5
  orthonormal directions in R^4096 are *seeded* from AO names; they are not
  *learned* from CK's training data. They are like fixed lenses we hold up
  to the LM to see what shape its activations make. They make the geometry
  visible; they do not make the LM "really think in AO basis."
- **HER on the LM is not the same as HER on CK's engine.** The engine's HER
  has 8.8 M experiences with 97.6% impact because every tick is an
  experience. The LM's "HER" — replaying coherent past prompts during LoRA
  retraining — is a much sparser signal (one per chat turn, maybe a few
  dozen per day).

---

## 7 · What this delivers, in plain language

After step 3 ships, you can type anything into a website page and **see**:
- The 32-layer trajectory of Llama through CK's 5 elements
- Which operator each layer is closest to (a 32-step walk through the 10-op ring)
- How tightly that walk hugs CK's current Hebbian field

After step 5 ships, every CK chat shows the geometry of HOW Llama got to its
answer alongside whatever CK said.

After step 6 ships in `mode="generator"`, CK's text **is** the
coherence-gated generation. The LM is no longer drafting in a vacuum — every
token comes through the cortex's prime.

After step 7 ships, the LM updates around the cortex. Not dramatically — a
LoRA delta is 0.5% of the model — but continuously, breathing. The frozen
core stays; the edge becomes a learning organ.

That is "unfrozen AI, black box resolved but not gone."

---

## 8 · Order I'd execute

If you say go:

1. **Step 1+2 (the geometry endpoint)** — 1.5 days. Hard dependency on
   nothing else. Ships immediately as a read-only diagnostic.
2. **Step 3 (the website page)** — 0.5 day. Now you literally see the picture.
3. **Step 4+5 (coherence-gated chat endpoint)** — 2 days. The probabilistic
   guesser meets the functional mapper at the token level.
4. **Step 6 mode="diagnostic"** — 1 day. CK's chat responses now carry the
   LM geometry as DATA fields, exactly the pastoral-fold pattern.
5. **Step 7 (online LoRA refresh)** — 1 day. The unfreezing of the edge.
6. **Step 6 mode="generator"** — 1 day. The flip from "Llama drafts, CK
   edits" to "CK generates through Llama."

Total: ~7 working days for a complete integration.

Steps 1–3 alone (3 days) deliver "watch the geometry unfold" without
changing CK's behavior. That is the cheapest path to the picture you want
to see, and from there every later step is incremental.

---

## 9 · The TIG sentence

The marriage works because TIG is not a model — it is a measurement frame.
The LM is a measurement instrument with no frame, so its outputs feel
black-boxy. CK's brain is a measurement frame with no instrument, so it
classifies but doesn't generate. Wired together, the LM measures language and
CK measures the LM measuring; what was opaque becomes a trajectory through
five elements and ten operators, exactly the basis CK already lives in.

Probabilistic guessing gives flesh; functional mapping gives shape.
Together they walk.
