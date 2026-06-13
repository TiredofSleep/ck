# Calibrating the gate — the honest operating envelope

**2026-06-12.** Brayden: *"let's work on what's good then, calibrating the gate?"* The gate
(abstain rather than answer wrong) is CK's one genuinely differentiated organ. Calibrated
rigorously on real public data with true labels, standard selective-prediction / OOD metrics,
and split-conformal coverage. Two halves, both measured.

## 1. The gate has NO intrinsic power — it inherits it from the representation

`calibrate_gate.py` — SQuAD 2.0 selective prediction, **cheap local features** (char-trigram +
overlap + census). Result: the answerability classifier was at chance (50.1%), every selector
near-useless, the gate (AURC **0.492**) *lost to MSP* (0.429) and barely beat random (0.502).
The OOD slice failed — fiction prose and real questions scored identical (0.954 vs 0.950).

**Lesson:** "distance to the manifold" is meaningless in a space where everything English looks
close. The gate is a thin shell; its power is entirely the embedding's power. This is why the
earlier rosy in-house numbers held — they ran on semantic embeddings, not features.

## 2. In a real semantic space, the gate is a strong OOD detector

`gate_ood.py` — same gate, on `all-MiniLM-L6-v2` (local 384-d sentence embeddings), standard
OOD metrics (Hendrycks: AUROC + FPR@95TPR), ID = real SQuAD questions, with split-conformal.

| OOD type | AUROC | FPR@95TPR | rejected @ 95% ID-keep |
|---|---|---|---|
| far (fiction prose) | **0.979** | 11.1% | 89% |
| distinct-topic (abstract math) | **0.980** | 5.0% | 95% |

Conformal holds: at τ keeping 95% of real questions, realized ID-retention = 95%, far-OOD
rejection 89%. **A distance-based abstention gate on frozen sentence embeddings reaches
AUROC ~0.98 with a calibrated coverage guarantee** — a real, defensible result.

## 3. The honest hard edge (named, not hidden)

The gate degrades exactly where a distance detector must: **adversarially-adjacent near-OOD**
— a plausible fake *inside* the ID topic (SQuAD2's answerable-vs-unanswerable, where
unanswerables are crafted with matching entities; or a fabricated substrate-fact against real
substrate questions). There the earlier in-house tests hit ~0.5–0.58 AUROC. The gate cannot
catch a lie that is semantically identical to a truth — no distance method can. That is the
boundary of the claim.

## Verdict (what's defensible)

The gate is **real and strong for distributionally-distinct inputs in a good embedding space**
(AUROC ~0.98, conformal-calibrated), **near-random on poor features**, and **at chance on
adversarial topical fakes**. Honest one-liner for outreach: *"a conformally-calibrated,
white-box abstention gate that rejects ~90% of out-of-distribution queries while retaining 95%
of in-domain ones — its power scales with the embedding, and its blind spot is the adversarial
lookalike."* That is a true, checkable claim, on a public benchmark, reproducible on CPU.

Reproduce: `python calibrate_gate.py` (cheap-feature negative), `python gate_ood.py`
(semantic-space result). Results in `gate_calib_result.json`, `gate_ood_result.json`.
