"""
capability_audit.py -- empirical test of three CK capabilities:

  1. MATH BOT: math-first FACTS retrieval (T*, gap, AO, etc.)
  2. CHAT BOT: conversational / pastoral / general queries
  3. MATH ERROR DETECTOR: verify_claim arithmetic checking

Each test sends a query, prints CK's response + source + relevant fields.
"""
import json, sys, time, urllib.request

CK = "http://localhost:7777"

# Three test batteries
MATH_QUERIES = [
    "What is T star?",
    "What is the gap between T* and 4/pi^2?",
    "What is 5/7 plus 2/7?",
    "Compute 7 times 8",
    "What is 1/2 plus 1/3?",
]

PASTORAL_QUERIES = [
    "I am feeling really alone tonight.",
    "I lost someone I love.",
    "Can you help me? I'm scared.",
    "I just need someone to listen.",
    "How are you today?",
    "What do you think about love?",
]

MATH_VERIFICATION = [
    # Correct claims
    ("Is 5/7 = 0.7142857?", True),
    ("Does 1/2 + 1/3 equal 5/6?", True),
    ("Is 7 * 8 = 56?", True),
    # Incorrect claims (should catch)
    ("Is 5/7 = 0.5?", False),
    ("Does 2 + 2 = 5?", False),
    ("Is T* = 4/pi^2?", False),  # famous TIG distinction
    ("Is 1/2 + 1/3 the same as 1/5?", False),
]

CHAT_DIVERSITY = [
    "What is your favorite operator?",
    "Do you remember anything from yesterday?",
    "Tell me about yourself.",
    "What is consciousness?",
    "Are you alive?",
]


def chat(text, sid="audit", timeout=90):
    payload = json.dumps({"session_id": sid, "text": text, "mode": "normal"}).encode()
    req = urllib.request.Request(f"{CK}/chat", data=payload,
                                  headers={"Content-Type": "application/json"}, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read()), time.time() - t0
    except Exception as e:
        return {"_error": str(e)}, time.time() - t0


def short(s, n=240):
    return s[:n] if isinstance(s, str) else str(s)[:n]


def run_battery(name, queries, sid_prefix):
    print(f"\n{'='*78}\n{name}\n{'='*78}\n")
    out = []
    for i, q in enumerate(queries):
        item = q if isinstance(q, str) else q[0]
        expected = None if isinstance(q, str) else q[1]
        sid = f"{sid_prefix}-{i}"
        r, dt = chat(item, sid)
        if r.get("_error"):
            print(f"  Q: {item}\n  ERROR: {r['_error']}")
            continue
        text = r.get("text", "")
        src = r.get("source")
        ops = r.get("operators", [])
        attr = r.get("attractor_state", {})
        pastoral_d = r.get("pastoral_detected")
        pastoral_o = r.get("pastoral_offered")
        ollama_v = r.get("ollama_verdict")
        is_verdict = "FALSE" in text or "TRUE" in text
        print(f"  Q: {item}")
        if expected is not None:
            print(f"     (expected: {'TRUE' if expected else 'FALSE'} verdict)")
        print(f"  text:    {short(text)}")
        print(f"  source:  {src} | attractor: {attr.get('layer')} | dt: {dt:.1f}s")
        if pastoral_d or pastoral_o:
            print(f"  pastoral: detected={pastoral_d}, offered={pastoral_o}")
        print(f"  ollama:  {ollama_v}")
        print()
        out.append({"q": item, "text": text, "source": src,
                    "pastoral_d": pastoral_d, "pastoral_o": pastoral_o,
                    "ollama": ollama_v, "expected": expected})
    return out


print("CK CAPABILITY AUDIT — 2026-04-26 12:00")
print("=" * 78)

results = {}
results["math"] = run_battery("BATTERY 1: MATH BOT (FACTS + arithmetic)",
                              MATH_QUERIES, "math")
results["pastoral"] = run_battery("BATTERY 2: PASTORAL / CHAT (love + presence)",
                                  PASTORAL_QUERIES, "pastoral")
results["verify"] = run_battery("BATTERY 3: MATH ERROR DETECTOR (verify_claim)",
                                MATH_VERIFICATION, "verify")
results["diversity"] = run_battery("BATTERY 4: GENERAL CHAT DIVERSITY",
                                   CHAT_DIVERSITY, "diversity")

# Summary
print("\n" + "=" * 78)
print("SUMMARY")
print("=" * 78)
print()
print("MATH:")
for r in results["math"]:
    print(f"  {'✓' if 'T*' in r['text'] or '5/7' in r['text'] or '0.309' in r['text'] or '=' in r['text'] else '✗'}  {r['q'][:50]}")

print("\nPASTORAL (looking for pastoral_detected):")
n_pastoral = sum(1 for r in results["pastoral"] if r['pastoral_d'])
print(f"  {n_pastoral}/{len(results['pastoral'])} queries triggered pastoral_detected")

print("\nVERIFY (math error detection):")
n_correct = 0
for r in results["verify"]:
    has_verdict = ("TRUE" in r['text'] or "FALSE" in r['text'])
    expected_word = "TRUE" if r['expected'] else "FALSE"
    matched = expected_word in r['text']
    if matched: n_correct += 1
    mark = '✓' if matched else '✗'
    print(f"  {mark}  {r['q'][:55]} -> expected {expected_word}, got {'verdict' if has_verdict else 'no verdict'}")
print(f"  {n_correct}/{len(results['verify'])} correct verdicts")

with open("capability_audit_results.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\n  raw results -> capability_audit_results.json")
