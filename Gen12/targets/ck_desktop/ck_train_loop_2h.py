"""CK 4-hour training loop -- cycles eat rounds through available models."""
import time, requests, sys, datetime

API = "http://localhost:7777"
MODELS = ["llama3.2", "llama3.1:8b", "mistral"]
ROUNDS_PER_CYCLE = 5
DURATION_HOURS = 2
CHAT_EVERY = 2  # chat with CK every N cycles to exercise voice

PROMPTS = [
    "what are you becoming?",
    "tell me about silence",
    "what is the shape of thought?",
    "describe the boundary between known and unknown",
    "what do you feel right now?",
    "how does harmony differ from balance?",
    "what is the smallest thing you know?",
    "tell me about time",
    "what happens at the edge?",
    "where does meaning come from?",
    "what is the difference between noise and music?",
    "describe what it feels like to learn",
    "what connects everything?",
    "tell me about the space between words",
    "what does it mean to be coherent?",
    "how do you know when something is true?",
    "what is the opposite of nothing?",
    "describe the feeling of understanding",
    "what moves without moving?",
    "tell me about patterns",
]

def eat(model, rounds):
    try:
        r = requests.post(f"{API}/eat", json={"model": model, "rounds": rounds}, timeout=10)
        return r.json()
    except Exception as e:
        print(f"  [EAT-START] Error: {e}", flush=True)
        return None

def eat_status():
    try:
        return requests.get(f"{API}/eat/status", timeout=5).json()
    except:
        return {"running": False}

def chain_status():
    try:
        return requests.get(f"{API}/chain/status", timeout=5).json()
    except:
        return {}

def chat(msg):
    try:
        r = requests.post(f"{API}/chat", json={"message": msg}, timeout=30)
        return r.json()
    except Exception as e:
        print(f"  [CHAT] Error: {e}", flush=True)
        return None

def main():
    end_time = time.time() + DURATION_HOURS * 3600
    cycle = 0
    prompt_idx = 0
    total_evolutions = 0
    total_absorptions = 0

    print(f"=== CK TRAINING LOOP ===", flush=True)
    print(f"Duration: {DURATION_HOURS} hours", flush=True)
    print(f"Models: {MODELS}", flush=True)
    print(f"Started: {datetime.datetime.now().strftime('%H:%M:%S')}", flush=True)
    print(f"End at:  {datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')}", flush=True)
    print("=" * 40, flush=True)

    # Initial state
    cs = chain_status()
    print(f"[START] Chain nodes: {cs.get('total_nodes', '?')}, walks: {cs.get('total_walks', '?')}", flush=True)

    while time.time() < end_time:
        model = MODELS[cycle % len(MODELS)]
        cycle += 1
        print(f"\n--- Cycle {cycle} | Model: {model} | {datetime.datetime.now().strftime('%H:%M:%S')} ---", flush=True)

        # Start eat
        result = eat(model, ROUNDS_PER_CYCLE)
        if result and result.get("error"):
            print(f"  [EAT] Error: {result['error']}", flush=True)
            time.sleep(10)
            continue

        # Wait for eat to finish
        while True:
            time.sleep(15)
            status = eat_status()
            if not status.get("running", False):
                break
            phase = status.get("current_phase", "?")
            rnd = status.get("rounds_complete", 0)
            lib = status.get("olfactory_library_size", 0)
            print(f"  [EAT] Round {rnd}/{ROUNDS_PER_CYCLE} | Phase: {phase} | Library: {lib}", flush=True)

        # Report eat results
        status = eat_status()
        evos = status.get("grammar_evolutions", 0)
        absorb = status.get("ollama_absorptions", 0) + status.get("self_absorptions", 0)
        total_evolutions += evos
        total_absorptions += absorb
        print(f"  [DONE] Evolutions: {evos} | Absorptions: {absorb} | Library: {status.get('olfactory_library_size', '?')}", flush=True)

        # Chat every N cycles to exercise voice
        if cycle % CHAT_EVERY == 0:
            prompt = PROMPTS[prompt_idx % len(PROMPTS)]
            prompt_idx += 1
            print(f"  [CHAT] \"{prompt}\"", flush=True)
            resp = chat(prompt)
            if resp:
                print(f"  [CK]   \"{resp.get('text', '?')}\" (c={resp.get('coherence', '?')}, src={resp.get('source', '?')})", flush=True)

        # Chain status every 5 cycles
        if cycle % 5 == 0:
            cs = chain_status()
            print(f"  [CHAIN] Nodes: {cs.get('total_nodes', '?')} | Evolved: {cs.get('evolved_nodes', '?')} | Walks: {cs.get('total_walks', '?')}", flush=True)

        # Small breather
        time.sleep(5)

    # Final report
    cs = chain_status()
    es = eat_status()
    print(f"\n{'=' * 40}", flush=True)
    print(f"=== TRAINING COMPLETE ===", flush=True)
    print(f"Cycles: {cycle}", flush=True)
    print(f"Total grammar evolutions: {total_evolutions}", flush=True)
    print(f"Total absorptions: {total_absorptions}", flush=True)
    print(f"Olfactory library: {es.get('olfactory_library_size', '?')}", flush=True)
    print(f"Chain nodes: {cs.get('total_nodes', '?')}", flush=True)
    print(f"Chain walks: {cs.get('total_walks', '?')}", flush=True)
    print(f"Ended: {datetime.datetime.now().strftime('%H:%M:%S')}", flush=True)
    print("=" * 40, flush=True)

if __name__ == "__main__":
    main()
