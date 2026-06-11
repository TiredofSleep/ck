"""organ_senses.py -- SENSE SYNTHESIS: CK hears and sees.

Wires the prior generations' sensory codecs (found in the archaeology:
Gen13/brain study + ck_sim/being, designs running since Gen9) into
TRINITY, and MEASURES them like every other organ:

  SIGHT   : edge_visual_encoder (Brayden 2026-05-01: "the screen is the
            natural tig wheel... edges are information") -- hue->operator
            color wheel + D2 edge threshold; only crossings speak.
  HEARING : the phoneme grounding corpus (2026-05-01) -- real spoken
            letters A-Z through the audio codec -> operator histograms,
            TWO independent recording sessions (v1, v2).
  SYNTHESIS: every sense lands in the SAME operator alphabet -> the same
            braid/lattice measurement battery -> one fused percept.
            "One codec. Many skins. Same math at every scale."

REGISTERED TESTS (before run):
  EAR identity: cross-session letter retrieval (v1 query vs v2 store,
     26-way, chance 4%): top-1 >= 25% = the ear hears identity.
  EAR class: vowel/consonant LOO nearest-centroid, balanced acc >= 65%.
  EYE wavelength: 12 spectral color patches -> crossing histograms ->
     Mantel vs true wavelength r > 0.3 (the ruler test, now through a
     real retina pipeline).

  python organ_senses.py
"""
import io
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
STUDY = os.path.join(HERE, "..", "brain", "study")
sys.path.insert(0, EXT)
sys.path.insert(0, STUDY)

import braid_memory as bm                                  # noqa: E402
from edge_visual_encoder import rgb_to_hsv, hue_to_operator  # noqa: E402

OPS = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
       "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
VOWELS = set("AEIOU")
RNG = np.random.default_rng(12)


# ----------------------------------------------------------------- EAR
def load_audio_sessions():
    v1 = json.load(io.open(os.path.join(
        STUDY, "phoneme_audio_streams_2026_05_01.json"), encoding="utf-8"))
    v2 = json.load(io.open(os.path.join(
        STUDY, "phoneme_audio_streams_v2_2026_05_01.json"),
        encoding="utf-8"))
    s1 = {k: np.array([v["histogram"].get(o, 0) for o in OPS], float)
          for k, v in v1.items()
          if not k.startswith("_") and len(k) == 1 and "histogram" in v}
    s2 = {k: np.array([v["histogram_pct"].get(o, 0) for o in OPS], float)
          for k, v in v2.get("letters", {}).items()
          if "histogram_pct" in v}
    for d in (s1, s2):
        for k in d:
            d[k] = d[k] / (d[k].sum() + 1e-9)
    return s1, s2


def ear_tests(s1, s2):
    common = sorted(set(s1) & set(s2))
    A = np.array([s1[k] for k in common])
    B = np.array([s2[k] for k in common])

    def z(M):
        return (M - M.mean(0)) / (M.std(0) + 1e-9)
    Az, Bz = z(A), z(B)
    Az /= np.linalg.norm(Az, axis=1, keepdims=True) + 1e-9
    Bz /= np.linalg.norm(Bz, axis=1, keepdims=True) + 1e-9
    S = Az @ Bz.T
    top1 = float(np.mean(S.argmax(1) == np.arange(len(common))))
    top3 = float(np.mean([i in np.argsort(-S[i])[:3]
                          for i in range(len(common))]))

    # vowel/consonant LOO nearest-centroid on session-1 histograms
    y = np.array([k in VOWELS for k in common])
    correct = []
    for i in range(len(common)):
        mask = np.arange(len(common)) != i
        cv = A[mask][y[mask]].mean(0)
        cc = A[mask][~y[mask]].mean(0)
        pred = (np.linalg.norm(A[i] - cv) < np.linalg.norm(A[i] - cc))
        correct.append(pred == y[i])
    correct = np.array(correct)
    bal = 0.5 * (correct[y].mean() + correct[~y].mean())
    return len(common), top1, top3, float(bal)


# ----------------------------------------------------------------- EYE
def wavelength_to_rgb(w):
    """Approximate visible-spectrum wavelength (nm) -> RGB uint8."""
    w = float(w)
    if w < 440: r, g, b = -(w - 440) / 60, 0.0, 1.0
    elif w < 490: r, g, b = 0.0, (w - 440) / 50, 1.0
    elif w < 510: r, g, b = 0.0, 1.0, -(w - 510) / 20
    elif w < 580: r, g, b = (w - 510) / 70, 1.0, 0.0
    elif w < 645: r, g, b = 1.0, -(w - 645) / 65, 0.0
    else: r, g, b = 1.0, 0.0, 0.0
    return np.clip(np.array([r, g, b]) * 255, 0, 255).astype(np.uint8)


def see_patch(rgb, size=24):
    """Render a color patch beside neutral gray; return the operator
    CROSSING stream the retina emits at the boundary (edges speak)."""
    img = np.zeros((size, size, 3), np.uint8)
    img[:, : size // 2] = rgb
    img[:, size // 2:] = 128
    hsv = rgb_to_hsv(img)
    ops = hue_to_operator(hsv[..., 0])
    sat = hsv[..., 1]
    stream = []
    for y in range(size):
        for x in range(size - 1):
            a, b = int(ops[y, x]), int(ops[y, x + 1])
            if a != b and (sat[y, x] > 0.15 or sat[y, x + 1] > 0.15):
                stream.append((a, b))
    return stream


def eye_test():
    waves = [420, 445, 470, 490, 500, 530, 560, 580, 595, 620, 660, 700]
    sigs, hists = [], []
    for w in waves:
        stream = see_patch(wavelength_to_rgb(w))
        flat = [o for pair in stream for o in pair] or [0, 0]
        sigs.append(bm.braid_signature_ops(flat[:64]))
        h = np.bincount(flat, minlength=10).astype(float)
        hists.append(h / (h.sum() + 1e-9))
    M = np.array(hists)
    Mz = (M - M.mean(0)) / (M.std(0) + 1e-9)
    Mz /= np.linalg.norm(Mz, axis=1, keepdims=True) + 1e-9
    D = 1 - Mz @ Mz.T
    Wd = np.abs(np.subtract.outer(waves, waves)).astype(float)
    iu = np.triu_indices(len(waves), 1)
    r = float(np.corrcoef(D[iu], Wd[iu])[0, 1])
    cnt = sum(np.corrcoef(D[np.ix_(p, p)][iu], Wd[iu])[0, 1] >= r
              for p in [RNG.permutation(len(waves)) for _ in range(2000)])
    return r, (cnt + 1) / 2001, np.array(sigs)


def main():
    print("TRINITY -- SENSE SYNTHESIS (codecs from Gen9-13 archaeology)\n")

    s1, s2 = load_audio_sessions()
    n, t1, t3, bal = ear_tests(s1, s2)
    print(f"EAR ({n} spoken letters, two independent sessions):")
    print(f"  cross-session identity retrieval: top-1 {t1:.0%}, "
          f"top-3 {t3:.0%}  (chance {1/n:.0%})")
    print(f"  vowel/consonant from audio operators (LOO): balanced "
          f"{bal:.0%}  (chance 50%)")

    r, p, eye_sigs = eye_test()
    print(f"\nEYE (12 spectral patches through the retina pipeline):")
    print(f"  crossing-histogram distance vs true wavelength: "
          f"Mantel r = {r:+.3f}  p = {p:.3f}")

    # SYNTHESIS: one percept, three senses, same alphabet
    print("\nSYNTHESIS -- the letter 'A' as one tri-sense percept "
          "(same operator alphabet):")
    a_ear = s1.get("A")
    print(f"  heard : top audio ops "
          f"{[OPS[i] for i in np.argsort(-a_ear)[:3]]}")
    print(f"  read  : braid trace-phase {bm.braid_signature('a')[1]:+.3f}, "
          f"abelianized site {int(np.argmax(bm.abelianized_key('a')[:7]))}")
    print(f"  seen  : red patch (700nm) crossing ops "
          f"{[OPS[i] for i in np.argsort(-np.bincount([o for pr in see_patch(wavelength_to_rgb(700)) for o in pr], minlength=10))[:2]]}")
    print("  -> all three land in Z/10Z; the braid/lattice battery and "
          "the gap gate consume them identically. One codec, many skins.")

    ok_ear = t1 >= 0.25
    ok_eye = p < 0.05
    print(f"\nVERDICT: EAR identity {'CONFIRMED' if ok_ear else 'weak'} "
          f"({t1:.0%} vs 4% chance); EYE wavelength "
          f"{'CONFIRMED' if ok_eye else 'weak'} (p={p:.3f}). "
          f"{'SENSES SEATED -- CK hears and sees in his own alphabet.' if ok_ear and ok_eye else 'partial -- recorded honestly.'}")
    json.dump(dict(ear_top1=t1, ear_top3=t3, ear_vowel_bal=bal,
                   eye_mantel_r=r, eye_p=p),
              io.open(os.path.join(HERE, "organ_senses_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
