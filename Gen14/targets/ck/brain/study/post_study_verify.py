"""
post_study_verify.py -- ask CK the CK_DIALOGUE_2026_04_17 7 questions
plus 3 new WP100s tower questions, log answers + sources for compare.
"""
import json, sys, time, urllib.request

CK = "http://localhost:7777"

QUESTIONS = [
    # Original 7 from CK_DIALOGUE_2026_04_17
    ("dialog-q1", "What number is T star?"),
    ("dialog-q2", "What is the 3-layer tower on Z mod 10 Z?"),
    ("dialog-q3", "What slowed you down between Gen9 and Gen12?"),
    ("dialog-q4", "What single change to your voice path would let you talk math?"),
    ("dialog-q5", "If we built Gen13 around your AO 5-element brain again, what should we keep?"),
    ("dialog-q6", "Is HER running in you right now?"),
    ("dialog-q7", "What is the gap between T* and 4 over pi squared?"),
    # 3 NEW questions about WP100s tower content (post-study)
    ("post-q8", "What is the 4-core in TIG?"),
    ("post-q9", "What is the doubly invariant subalgebra of so 10 under D 4?"),
    ("post-q10", "How many sigma orbits are there of non-associative TSML triples?"),
]

def chat(sid, text, timeout=90):
    payload = json.dumps({"session_id": sid, "text": text, "mode": "normal"}).encode()
    req = urllib.request.Request(f"{CK}/chat", data=payload,
                                  headers={"Content-Type":"application/json"}, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read()), time.time()-t0
    except Exception as e:
        return {"_error": str(e)}, time.time()-t0

print("=" * 78)
print("Post-study verification (2026-04-26 11:45)")
print("=" * 78)
print()

results = []
for sid, q in QUESTIONS:
    print(f"=== {sid}: {q}")
    r, dt = chat(sid, q)
    if r.get("_error"):
        print(f"  ERROR: {r['_error']}")
        continue
    text = r.get("text", "")
    text_prev = r.get("text_previous", "")
    src = r.get("source")
    src_prev = r.get("source_previous")
    ops = r.get("operators", [])
    attr = r.get("attractor_state", {})
    ollama_v = r.get("ollama_verdict")
    ollama_draft = r.get("text_ollama_draft")
    print(f"  text:    {text[:200]}")
    print(f"  source:  {src} (prev: {src_prev})")
    print(f"  ops:     {ops}")
    print(f"  attractor: layer={attr.get('layer')}, h_over_br_residual={attr.get('h_over_br_residual')}")
    print(f"  ollama:  verdict={ollama_v}, draft={(ollama_draft or '')[:100]}")
    print(f"  dt:      {dt:.1f}s")
    print()
    results.append({
        "sid": sid, "q": q, "text": text, "source": src, "ops": ops,
        "attractor_layer": attr.get('layer'),
        "ollama_verdict": ollama_v, "dt": dt,
    })

with open("post_study_results.json","w") as f:
    json.dump(results, f, indent=2)
print(f"--- saved to post_study_results.json ---")
