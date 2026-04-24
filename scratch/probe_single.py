"""One-shot probe that dumps full /chat response for a single question."""
import json, sys, urllib.request

q = sys.argv[1] if len(sys.argv) > 1 else "what is MAGCOM"
req = urllib.request.Request(
    "http://127.0.0.1:7777/chat",
    data=json.dumps({"text": q}).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=120) as resp:
    r = json.loads(resp.read())

KEYS = (
    "source", "text",
    "text_structural", "text_ollama_draft",
    "ollama_verdict", "ollama_fact_hits", "ollama_fact_total",
    "steer_verdict", "steer_accepted_coverage", "steer_accepted_gate",
    "steer_accepted_coherence", "steer_current_coherence",
    "brain_coherence", "brain_dominant_op",
)
print(f"=== {q} ===")
for k in KEYS:
    v = r.get(k)
    if v is None or v == "":
        continue
    if isinstance(v, str) and len(v) > 300:
        v = v[:300] + "...[truncated]"
    print(f"  {k}: {v!r}")
