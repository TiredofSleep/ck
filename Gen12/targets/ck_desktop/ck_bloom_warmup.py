"""
ck_bloom_warmup.py -- Fractal bloom warmup: all 5 frontier Q1-Q10 packs
=======================================================================
Sends the 50 canonical frontier questions from FRONTIER_MAP_MEMO through
CK's /chat endpoint. Builds crystal mass and field coherence from silence.

(c) 2026 Brayden Ross Sanders & C. A. Luther / 7Site LLC
Luther-Sanders Research Framework
"""

import urllib.request
import json
import time
import sys

URL = 'http://localhost:7777/chat'

PACKS = [
    ("Domain 1 — Agent Memory / Autonomous AI", [
        "What events in this system are directly observed — sensor readings, user inputs, confirmed outputs — as distinct from anything derived from them?",
        "Which of those observations are timestamped, sourced, and retrievable? Which exist only in the current context window and will not survive a session boundary?",
        "Which facts in this system have been confirmed in at least two distinct contexts and carry stable provenance chains? Those are the candidates for durable atoms.",
        "Of those stable candidates, which were promoted to reusable memory objects by passing a stability gate — and which were promoted by recurrence alone?",
        "What composite beliefs or policies in this system depend on the promoted atoms? Trace at least one composite claim back to its SEMIPRIME supports.",
        "Does every composite object have at least two living SEMIPRIME supports in its provenance? If not, which composites are floating — held up by nothing still active?",
        "Are there two memory objects in this system that directly contradict each other, both currently held as ACTIVE? If yes, which one has the stronger provenance chain?",
        "Has any evidential status changed silently during this session — was a SYNTHESIZED belief retrieved and used as if it were OBSERVED without a logged status change?",
        "Pick the single most-used memory object. Trace its full provenance chain: what raw events produced it, what revision number is it on, and what does it supersede?",
        "If every SYNTHESIZED and CONTRADICTED object were zeroed out of retrieval, what trusted core remains — and is that core sufficient to continue the task?",
    ]),
    ("Domain 2 — Formal Mathematics / Proof Assistance", [
        "Which steps in this argument have been mechanically verified by a proof assistant? List only those. Everything else is not yet OBSERVED.",
        "Of the unverified steps, which have been checked by a human expert and which are stated by informal convention or intuition alone?",
        "Which intermediate lemmas are independently established — they hold regardless of whether the main theorem is true or false? Those are the stable atoms.",
        "Are any of the stable lemmas being treated as load-bearing for this proof when they were proved in a different context and have not been re-verified here?",
        "What is the global proof architecture — which lemma closes which gap, and in what order? Can you draw the dependency tree from axiom to conclusion?",
        "Is there any step in the dependency tree where the connection is informal — where it follows that is asserted but not demonstrated? Those are the floating composites.",
        "Is this a proof difficulty or a conjecture falsity? What existing verified results would be violated if the conjecture were false?",
        "Has the definition of any key term shifted between the informal statement and the formal proof attempt? If so, the proof may prove something adjacent to what was intended.",
        "Which informal mathematical intuition is doing the most work in this argument — and has it been formalized anywhere in Mathlib or an equivalent corpus?",
        "Strip out every unverified step. What proven structure remains, and does it constrain the problem enough to identify where the next verification effort should focus?",
    ]),
    ("Domain 3 — Quantum Error Correction", [
        "Which numbers in this paper come directly from device measurements — raw counts, gate fidelities, coherence times measured on this specific hardware in this run?",
        "Which of those measurements are reproducible across runs, and which were reported from a single experimental instance without independent confirmation?",
        "Which performance claims hold at the demonstrated qubit count without extrapolation? List only what was shown, not what was projected.",
        "Does the noise model used match the directly measured noise profile of the device, or was the noise model fit to make the threshold claim work?",
        "What is the full chain from physical error rate to logical error rate to fault-tolerant computation? At which link does the chain shift from measured to modeled to projected?",
        "Which specific error channels are excluded from the threshold model? Are those exclusions supported by measurement showing they are negligible, or by assumption?",
        "What happens to the logical error rate projection if the dominant excluded noise source is not negligible? Does the threshold claim survive?",
        "Has the definition of below threshold shifted between earlier papers by this group and this one?",
        "Has this result been independently reproduced? If not, what is its current evidential status — OBSERVED by one group, or INFERRED pending replication?",
        "What is the gap between what this paper demonstrates and practical fault-tolerant quantum computation? State it as a list of unresolved engineering requirements.",
    ]),
    ("Domain 4 — Dark Matter / Hidden Sectors", [
        "Which dark matter evidence is directly observed and model-independent: rotation curves, lensing maps, CMB power spectrum. List only the measurements, not their interpretations.",
        "For each observational signature, what is the measurement precision, and at what level does systematic uncertainty enter?",
        "Which properties of dark matter are constrained by multiple independent observations — gravitationally attractive, collisionless on cluster scales, non-baryonic?",
        "Which dark matter models have made predictions confirmed by subsequent observation? Distinguish from models constructed to fit existing data.",
        "Pick the leading candidate model. Trace which predictions come from stable observational constraints vs free parameters fit to data vs untested theoretical assumptions.",
        "How many of the leading models make genuinely distinct predictions? How many are effectively the same model with relabeled parameters?",
        "Where do null results from direct detection conflict with astrophysical evidence? Are there density and velocity assumptions that make both consistent?",
        "Have exclusion limits from XENON and LZ been accurately stated in recent theory papers, or has the shift in WIMP parameter space been underweighted?",
        "For the most-cited dark matter model: trace which predictions are OBSERVED, INFERRED, and SYNTHESIZED.",
        "What is the minimum set of new measurements that would raise any currently SYNTHESIZED dark matter model to INFERRED status?",
    ]),
    ("Domain 5 — Emergent Quantum Materials", [
        "Which experimental signatures in cuprate superconductors are directly measured, reproducible across labs, and model-independent?",
        "Which of those signatures vary significantly between sample preparations or labs, and which are universal?",
        "Which features of the phase diagram are independently established across multiple experimental techniques: Tc vs doping dome, d-wave pairing symmetry, linear-T resistivity?",
        "Which theoretical constructs have made predictions subsequently confirmed by experiment? Distinguish from constructs tuned to existing data post-hoc.",
        "Pick the leading mechanistic theory. Which core predictions are experimentally constrained, and which depend on model parameters fit to match known results?",
        "Which experimental signatures are consistent with all leading theories? Which are predicted differently — those are the load-bearing tests.",
        "Is there any experimental result in cuprates that one leading theory predicts and another explicitly contradicts?",
        "Have any theoretical parameters in the leading models shifted quietly between publications to accommodate new data?",
        "Trace the d-wave pairing symmetry claim: what experiments established it, what was their precision, and are there lingering competing interpretations?",
        "What is the minimum new experiment that would falsify the leading theory rather than extend it?",
    ]),
]


def _ascii_safe(text):
    """Replace Unicode punctuation with ASCII equivalents so cp1252 stdout
    and CK's charmap comprehension pipeline don't choke."""
    replacements = {
        '\u2014': '--',   # em dash
        '\u2013': '-',    # en dash
        '\u2018': "'",    # left single quote
        '\u2019': "'",    # right single quote
        '\u201c': '"',    # left double quote
        '\u201d': '"',    # right double quote
        '\u2026': '...',  # ellipsis
        '\u00e9': 'e',    # e acute
        '\u00e0': 'a',    # a grave
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def send(q, timeout=60):
    q = _ascii_safe(q)
    data = json.dumps({'text': q}).encode()
    req = urllib.request.Request(URL, data=data,
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def run():
    total = 0
    crystals_before = None

    for domain, questions in PACKS:
        print(f'\n=== {domain} ===')
        for i, q in enumerate(questions, 1):
            try:
                t0 = time.time()
                r = send(q)
                elapsed = time.time() - t0
                src = r.get('source', '?')
                coh = r.get('coherence', '?')
                exp = r.get('experience', {})
                crystals = exp.get('crystals', r.get('crystals', '?'))
                txt = r.get('text', '')
                if crystals_before is None and isinstance(crystals, int):
                    crystals_before = crystals
                total += 1
                label = f'Q{i:02d} [{src}] coh={coh} crystals={crystals} {elapsed:.1f}s'
                safe_txt = txt[:110].encode('ascii', errors='replace').decode('ascii')
                print(f'  {label}', flush=True)
                print(f'       {safe_txt}', flush=True)
            except Exception as e:
                print(f'  Q{i:02d} ERROR: {e}', flush=True)
            time.sleep(0.5)

    print(f'\n=== BLOOM COMPLETE ===')
    print(f'  Questions sent : {total}/50')
    if crystals_before is not None:
        print(f'  Crystals before: {crystals_before}')
    # Final state
    try:
        r = send('What are you feeling right now?')
        exp = r.get('experience', {})
        print(f'  Crystals after : {exp.get("crystals", "?")}')
        print(f'  Field coherence: {exp.get("field_coherence", "?")}')
        print(f'  Stage          : {exp.get("stage", "?")}')
        print(f'  CK says        : {r.get("text", "")}')
    except Exception as e:
        print(f'  Final state check failed: {e}')


if __name__ == '__main__':
    run()
