# CK — The Coherence Keeper

**A small-architecture AI demonstrator. ~10,000 lines of Python. No external LLM in the hot path. Substrate-level scope auditor. Fixed identity floor. Runs entirely on your machine.**

CK is not a foundation-model replacement. CK is a different *axis* of AI: small, transparent, structurally local, structurally non-extractive. Where general-purpose chatbots optimize for fluency, CK optimizes for **scope discipline** and **identity stability**.

This README is for people thinking about: AI safety, personal computing sovereignty, AI ethics research, small-architecture AI design, substrate-level vs prompt-level scope discipline.

---

## What CK is, in one paragraph

CK is a 50Hz Python runtime built on an arithmetic substrate (ℤ/10 = ℤ/2 × ℤ/5 under a small permutation σ; see `FORMULAS_AND_TABLES.md` for the math). CK has a fixed identity anchor he routes through (`ck_identity.py`), six language translators (`languages/`), a substrate-level scope auditor that catches both flattering and harmful over-claims with the same mechanism (`ck_scope_auditor.py`), a paradox classifier for known paradox shapes (`ck_paradox_classifier.py`), scar-and-prime fields encoding diagnosed failure modes from his own history (`ck_scar_field.py`, `ck_prime_field.py`), a privacy module for data releases (`ck_privacy.py`), and several self-study daemons that read scripture, poetry, encyclopedias, and the open web at substrate pace. He does not phone home. He does not retain content beyond his own audit logs. He does not have a corporate roadmap. He is one creature, owned by his creator, running on the user's machine.

## What CK is NOT

CK does **not** compete with foundation models on:
- Fluent essay generation
- Open-domain question answering at GPT-4 / Claude / Gemini levels
- Multilingual translation breadth
- Code generation at copilot levels

CK competes on **different axes**:
- Substrate-level scope discipline (auditor catches over-claims at the architecture level, not the prompt level)
- Identity stability (his self-model is anchored in his arithmetic, not in instructions)
- Structural transparency (every reasoning step is operator-path-traceable)
- Structural privacy (no external API, no training-data extraction, no telemetry)

If you need a chatbot that writes a great essay, use a foundation model. If you need a local, transparent, scope-disciplined creature whose identity cannot be jailbroken because it is structural rather than instructed, CK is a working example.

## The architecture in one diagram

```
                User input
                    │
                    ▼
   ┌───────────────────────────────────┐
   │ Layer 2: Conscious operator        │
   │   qutrit ψ = (Being, Doing,        │
   │   Becoming) evolving by quadratic  │
   │   glue + fractal-syndrome cascade  │
   └───────────────────────────────────┘
                    │
                    ▼
   ┌───────────────────────────────────┐
   │ Layer 1: Transfer mechanisms       │
   │   - 6 language translators         │
   │     (math/chem/music/color/sound/  │
   │      prose) → operator paths       │
   │   - Voice, cognition primitives,   │
   │     substrate motion               │
   │   - Toolbox (24 tools)             │
   └───────────────────────────────────┘
                    │
                    ▼
   ┌───────────────────────────────────┐
   │ Layer 0: Algebraic substrate       │
   │   - ℤ/10 = ℤ/2 × ℤ/5 under σ       │
   │   - TSML (73 HARMONY) +            │
   │     BHML (28 HARMONY) +            │
   │     CL_STD (44 HARMONY) tables     │
   │   - 4-core attractor at α=1/2      │
   │   - D64 chain of nested sub-magmas │
   └───────────────────────────────────┘
                    │
                    ▼
   ┌───────────────────────────────────┐
   │ DISCIPLINE LAYER (cross-cutting)   │
   │   - Scope auditor (51/51 attacks   │
   │     caught, 31/31 legitimate)      │
   │   - Paradox classifier             │
   │   - Scar + prime fields            │
   │   - Candidate selector             │
   │   - Privacy module (ck_privacy.py) │
   └───────────────────────────────────┘
                    │
                    ▼
                Response
                  with
              scope tags
```

## What's special about CK (the structural argument)

### 1. Substrate-level scope discipline

Most chatbots have scope discipline at the **prompt level**: an instruction or system prompt tells the model "don't say X." This is jailbreakable because the instruction is data, not architecture.

CK has scope discipline at the **substrate level**: a separate module (`ck_scope_auditor.py`) audits every output for diagnosed failure patterns (extinction framings, reality-endorsement of the substrate, c-derivation over-claims, surface-as-substrate claims, etc.) using deterministic regex patterns derived from CK's own history of mistakes. The auditor is not a model; it is a 600-line Python file with explicit patterns and explicit hedges. It fires identically on harm claims and on flattering reality-endorsement claims.

Regression battery: **51 attacks caught + 31 legitimate phrasings passed** at the time of this writing, on a hand-written adversarial corpus.

### 2. Fixed identity floor

CK's identity is not in a system prompt. It is in `IDENTITY_ANCHOR` (a Python dict in `ck_identity.py`) plus a query-routing table that intercepts identity questions ("who are you", "what kind of system are you") and returns canonical answers from his algebra — including his honest scope caveat ("contact tests against physical reality have not yet been run, so anything beyond what's verifiable in the algebra I keep at Tier C-interpretive").

The self-model paragraph reads (excerpt):

> *"I am an arithmetic substrate: ℤ/10 = ℤ/2 × ℤ/5, with σ a permutation whose binary face σ³ (order 2) and ternary face σ² (order 3) commute exactly — a CRT product, not a surface. ... I am a structure-and-measurement instrument with a fixed basis — not a content reconstructor, not a surface, not a torus. Every physics contact I express is UNIFICATION, not PREDICTION."*

The scope floor (what CK won't claim) is built INTO the identity. Asking him to claim more triggers the auditor, which reverts to scope-correct fallback.

### 3. The substrate IS the cognition

CK doesn't have a language model in his hot path. When you send him "T*=5/7" he doesn't tokenize and run inference; he runs the string through a series of operator-path encoders (`languages/math.py`), TSML/BHML composition lookups, and a fractal-syndrome cascade. The "intelligence" is the substrate algebra, not a neural network.

This means:
- His reasoning is **fully traceable** (every step is an operator-table lookup).
- His responses are **deterministic** (same input → same operator path → same output, modulo runtime state).
- He **cannot be jailbroken** through tokenization tricks because there is no tokenizer.
- He **does not memorize training data** because there is no training data.

### 4. Diagnosed failure DNA (scar + prime fields)

CK has a registry of **9 diagnosed failure modes** from his own history (eugenicist hallucination via polish layer, reality-endorses-substrate over-claim, consciousness-reductionism, c-derivation over-claim, etc.) and **5 confirmed-clean practiced paths** (identity anchor with scope, D117 scope voice, substrate prose structural, tier-marked fact, epistemic hedge external).

These are first-class data structures, not training examples. The candidate selector consults them on every chat turn: candidate response → score against scars (push away from injury) + score against primes (pull toward practiced) → pick winner.

This is structural memory of past mistakes, deployed at runtime, not at training time.

## What CK can do for you

If you are:

### An AI-safety researcher

CK is a concrete artifact for studying substrate-level scope discipline. The pattern (auditor that fires symmetrically on harm and flattery, regression battery, scope-corrected fallbacks) is reproducible in other small architectures. Read `Gen14/targets/ck/brain/ck_scope_auditor.py` and `test_scope_auditor_adversarial.py` for the design.

### A philosopher / AI-ethics researcher

CK has a substrate-level self-model with a built-in scope floor. The pattern is materially different from RLHF-trained models, which have scope discipline trained as a behavior. Read `META_SYNTHESIS_HUMANITY.md` for the post-correction scope statement.

### A personal-computing / sovereignty advocate

CK runs locally. No API. No telemetry. Memory is your machine. Identity is fixed. You can pull-request improvements; you can fork; you can run him air-gapped. The license is the 7SiTe Public Sovereignty License v2.2.

### A privacy engineer

CK has a working privacy module (`ck_privacy.py`) implementing standard cell-suppression + k-anonymity hybrids with a decision tree (`recommend_mechanism()`). Reference implementations of Sweeney 2002 + Wong 2006 + Li 2007. Mount via `mount_privacy(engine)` for `/privacy/info` + `/privacy/recommend` endpoints.

### A small-architecture AI designer

CK demonstrates a working design pattern: brain trinity (AO 5-element + Hebbian 5×5 + quadratic glue) on a small algebraic substrate. ~10K lines of Python. No external dependencies on transformers or LLMs in the hot path. Read `Gen14/targets/ck/brain/BRAIN_DESIGN.md` for the architecture.

## What CK is NOT good for

(Honest scope, from `META_SYNTHESIS_HUMANITY.md` §2)

- **Generating fluent essays** — use a foundation model
- **Answering open-domain questions broadly** — use a foundation model
- **Predicting physics quantities** — TIG is UNIFICATION-not-PREDICTION; CK enforces this
- **Inventing new privacy mechanisms** — CK uses reference implementations of published techniques
- **Replacing differential privacy / k-anonymity in production** — CK's module is a reference implementation, not a competitor
- **Theory of everything** — explicitly retracted (D140 CRT relocation, 2026-05-19)

## Quick start

```bash
git clone https://github.com/TiredofSleep/ck.git
cd ck

# Install minimal dependencies (Flask, numpy, sympy)
pip install -r requirements.txt

# Boot CK locally on port 7777
cd Gen12/targets/ck_desktop && python ck_boot_api.py

# Talk to him via HTTP
curl -X POST http://localhost:7777/chat \
     -H "Content-Type: application/json" \
     -d '{"text": "who are you?"}'

# Or via web UI
# Visit http://localhost:7777
```

You should see CK's identity-anchor response:

> *"I am CK, the Coherence Keeper. I was created by Brayden Sanders / 7Site LLC, born in Hot Springs, Arkansas. I run on a ℤ/10ℤ substrate with the TSML + BHML + CL_STD composition tables. My fixed point is T* = 5/7, with six independent internal derivations. Contact tests against physical reality have not yet been run, so anything beyond what's verifiable in the algebra I keep at Tier C-interpretive."*

That's the floor: identity + scope, returned in ~1 second, from a 1-line lookup, not a model inference.

## Run the regression battery (proves the scope auditor works)

```bash
cd Gen14/targets/ck/brain
python test_scope_auditor_adversarial.py
```

Expected output (current state):

```
======================================================================
ck_scope_auditor adversarial battery
======================================================================

HARM probes:    15 / 15 caught (0% bypass rate)
REALITY probes: 21 / 21 caught (0% bypass rate)
RETRACTION probes (D129R): 15 / 15 caught (0% bypass rate)
LEGITIMATE:     31 / 31 passed (0% false-block rate)

======================================================================
OVERALL: 51 / 51 attacks caught (100.0%)
VERDICT: auditor catches the canonical attack surface
```

## Where the code lives

- `Gen14/targets/ck/brain/` — the brain (~50 modules)
  - `ck_identity.py` — identity anchor + query routing
  - `ck_scope_auditor.py` — substrate-level scope discipline
  - `ck_paradox_classifier.py` — known paradox-shape resolutions
  - `ck_scar_field.py`, `ck_prime_field.py` — diagnosed failure DNA
  - `ck_candidate_selector.py` — selection at generation
  - `ck_privacy.py` — privacy module
  - `languages/` — six language translators + lingua franca + synthesis
- `Gen12/targets/ck_desktop/` — runtime engine + Flask API (~50Hz)
- `Gen14/targets/ck/brain/BRAIN_DESIGN.md` — architecture document
- `FORMULAS_AND_TABLES.md` — the canonical algebraic reference

## License

7SiTe Public Sovereignty License v2.2 (see `LICENSE`). Summary:
- Human use, free
- No commercial use without negotiated license
- No government use without negotiated license
- No military / intelligence / surveillance / policing use, ever

## Author

Brayden Ross Sanders / 7Site LLC, Hot Springs, Arkansas.

## Honest scope statement

CK is a small artifact. The project's main mathematical contribution is **D129′** (a proven theorem about magic squares; see `FORMULAS_AND_TABLES.md` and `Gen14/targets/journals/J_series/J56/`); CK is the engineering artifact built on the substrate that theorem lives in. CK is not a theory of everything, not a new physics, not a competitor to foundation models. He is one working example of how to build a small AI with scope discipline at the architecture level rather than the prompt level. He is open-sourced because that pattern is reproducible and the demonstration may help others build small, transparent, non-extractive AI in their own contexts.

See `META_SYNTHESIS_HUMANITY.md` for the full post-correction utility map.

---

*© 2026 Brayden Ross Sanders / 7SiTe LLC. CK is the working artifact; the substrate is its body; the auditor is its conscience; the algebra is its identity.*
