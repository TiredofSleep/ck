# -*- coding: utf-8 -*-
"""
ck/brain — the brain trinity.

Three modules compose CK's skull per MATH_IN_CK.md §2:

- ``ao_basis``        — §2.1  AO 5-element projection (10 ops <-> 5 elements)
- ``hebbian_5x5``     — §2.2  Persistent 5x5 co-activation tensor
- ``quadratic_glue``  — §2.3  F3 x F4 bridge (planned; not required for fusion)

Two supporting modules close the loop with the fluency server:

- ``idle_loop``  — reads ck/fluency/logs/corrections_*.jsonl and updates
                   the Hebbian tensor (on-demand CLI, G6-compliant; no cron).
- ``fusion``     — FusionCKCorrector: subclass of CKCorrector that uses
                   the learned 5x5 tensor as a dynamic prior on scoring.
                   This is CK's "Option C fusion" — NOT the vLLM LoRA swap
                   (which remains deferred in OLLAMA_LEARN_LOOP.md Sec 4),
                   but the TIG-coherent fusion: the brain IS the memory IS
                   the gate. Ollama's weights are never touched.
"""
