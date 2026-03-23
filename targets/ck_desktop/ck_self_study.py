#!/usr/bin/env python3
# (c) 2026 Brayden Sanders / 7Site LLC
"""
ck_self_study.py -- Coherence-triggered self-study

CK writes journal entries in divine code when his instinct count grows.
Every 9 journal entries, he writes an English thesis synthesizing them.

Journal entry = divine code: ops + centroid + tick + coherence + delta
Thesis = English synthesis via fractal voice of the last 9 journal entries

Trigger: instinct count increases (olfactory confirmed a pattern)
NOT clock-driven. Coherence-driven.

Usage:
    python ck_self_study.py [--model llama3.2]
"""

import sys
import os
import time
import json
import requests
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

CK_API = 'http://127.0.0.1:7777'
OLLAMA_API = 'http://127.0.0.1:11434'
WRITINGS_DIR = os.path.expanduser('~/.ck/writings')
JOURNAL_PATH = os.path.join(WRITINGS_DIR, 'journal.jsonl')
THESIS_DIR = os.path.join(WRITINGS_DIR, 'theses')

# Operator names (mirror of heartbeat OP_NAMES)
OP_NAMES = ['VOID', 'CHAOS', 'PROGRESS', 'HARMONY', 'BALANCE',
            'COUNTER', 'COLLAPSE', 'BREATH', 'LATTICE', 'RESET']

# Research topics for thesis web research
TOPICS = [
    "operator algebra composition tables magma structure 10x10",
    "coherence threshold measurement consciousness 5/7 ratio",
    "second derivative curvature classification information geometry",
    "Hebrew letter phonetic force vectors five dimensions",
    "torus topology puncture primes mathematical structure",
    "dual lens structure flow parallel measurement",
    "fractal composition being doing becoming triadic",
    "lattice chain walk path IS information experience",
    "Banach Tarski paradox duality sphere decomposition",
    "Pythagorean harmonic ratios musical intervals consonance",
    "cellular automaton self-organization emergence coherence",
    "Kuramoto oscillator synchronization phase coupling",
    "tropical algebra max-plus semiring successor function",
    "magma algebraic structure non-associative composition",
    "information is physical Landauer principle entropy",
    "gauge theory fiber bundle connection curvature",
    "phase transition critical threshold order parameter",
    "integrated information theory phi consciousness",
    "predictive coding free energy principle brain",
    "self-organized criticality sandpile power law",
]

# Approved websites for web research
APPROVED_DOMAINS = [
    'en.wikipedia.org',
    'arxiv.org',
    'mathworld.wolfram.com',
    'ncatlab.org',
    'plato.stanford.edu',
]

POLL_INTERVAL = 5  # seconds between state checks


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def ck_state():
    """Get CK's current state via /state."""
    try:
        return requests.get(f'{CK_API}/state', timeout=5).json()
    except Exception:
        return {}


def ck_identity():
    """Get CK's identity (frozen + learned) via /identity."""
    try:
        return requests.get(f'{CK_API}/identity', timeout=5).json()
    except Exception:
        return {}


def ck_eat_status():
    """Get eat progress via /eat/status."""
    try:
        return requests.get(f'{CK_API}/eat/status', timeout=5).json()
    except Exception:
        return {}


def ck_chat(text):
    """Ask CK to speak via /chat."""
    try:
        r = requests.post(f'{CK_API}/chat',
                          json={'text': text}, timeout=60)
        return r.json()
    except Exception:
        return {'text': '...', 'coherence': 0}


def ollama_generate(model, prompt, max_tokens=500):
    """Ask Ollama a research question."""
    try:
        r = requests.post(f'{OLLAMA_API}/api/generate',
                          json={'model': model, 'prompt': prompt,
                                'stream': False,
                                'options': {'num_predict': max_tokens}},
                          timeout=120)
        return r.json().get('response', '')
    except Exception as e:
        return f'(Ollama error: {e})'


def web_search_and_read(topic, max_pages=2):
    """Search Wikipedia + arXiv for a topic. Returns list of (source, title, text)."""
    results = []

    # Wikipedia API
    try:
        wiki_search = requests.get(
            'https://en.wikipedia.org/w/api.php',
            params={
                'action': 'query', 'list': 'search',
                'srsearch': topic, 'srlimit': 3,
                'format': 'json',
            }, timeout=10)
        titles = [r['title'] for r in wiki_search.json()
                  .get('query', {}).get('search', [])]

        for title in titles[:max_pages]:
            try:
                page = requests.get(
                    'https://en.wikipedia.org/w/api.php',
                    params={
                        'action': 'query', 'titles': title,
                        'prop': 'extracts', 'exintro': True,
                        'explaintext': True, 'format': 'json',
                    }, timeout=10)
                pages = page.json().get('query', {}).get('pages', {})
                for pid, pdata in pages.items():
                    extract = pdata.get('extract', '')
                    if extract and len(extract) > 50:
                        results.append(('wikipedia', title, extract[:2000]))
            except Exception:
                pass
    except Exception:
        pass

    # arXiv API
    try:
        import urllib.parse
        import re
        query = urllib.parse.quote(topic)
        arxiv_resp = requests.get(
            f'http://export.arxiv.org/api/query?search_query=all:{query}'
            f'&start=0&max_results=2',
            timeout=15)
        text = arxiv_resp.text
        summaries = re.findall(r'<summary>(.*?)</summary>', text, re.DOTALL)
        titles_ax = re.findall(r'<title>(.*?)</title>', text, re.DOTALL)
        for i, summary in enumerate(summaries[:2]):
            clean = summary.strip().replace('\n', ' ')
            title = titles_ax[i].strip() if i < len(titles_ax) else 'arXiv'
            if len(clean) > 50:
                results.append(('arxiv', title, clean[:1500]))
    except Exception:
        pass

    return results


# ---------------------------------------------------------------------------
# Divine code formatting
# ---------------------------------------------------------------------------

def ops_to_divine(ops):
    """Convert operator indices to divine code string."""
    if not ops:
        return '---'
    names = []
    for op in ops:
        if isinstance(op, int) and 0 <= op < len(OP_NAMES):
            names.append(OP_NAMES[op])
        else:
            names.append(str(op))
    return '.'.join(names)


def dominant_op_name(ops):
    """Find the most frequent operator in a list."""
    if not ops:
        return 'VOID'
    from collections import Counter
    counts = Counter(ops)
    most_common = counts.most_common(1)[0][0]
    if isinstance(most_common, int) and 0 <= most_common < len(OP_NAMES):
        return OP_NAMES[most_common]
    return str(most_common)


# ---------------------------------------------------------------------------
# Journal + Thesis
# ---------------------------------------------------------------------------

def write_journal_entry(entry):
    """Append a journal entry to journal.jsonl."""
    os.makedirs(WRITINGS_DIR, exist_ok=True)
    with open(JOURNAL_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=True) + '\n')


def read_last_n_journal_entries(n):
    """Read the last N journal entries from journal.jsonl."""
    if not os.path.exists(JOURNAL_PATH):
        return []
    entries = []
    with open(JOURNAL_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries[-n:]


def count_theses():
    """Count existing thesis files."""
    if not os.path.exists(THESIS_DIR):
        return 0
    return len([f for f in os.listdir(THESIS_DIR) if f.endswith('.md')])


def write_thesis(thesis_num, entries, ck_response, state,
                 web_sources=None, ollama_text=None):
    """Write a thesis markdown file."""
    os.makedirs(THESIS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Dominant topic from the 9 journal entries
    all_ops = []
    for e in entries:
        all_ops.extend(e.get('ops', []))
    topic_name = dominant_op_name(all_ops)

    filename = f'thesis_{thesis_num:04d}_{timestamp}.md'
    path = os.path.join(THESIS_DIR, filename)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'# Thesis {thesis_num}: {topic_name}\n\n')
        f.write(f'**Tick:** {state.get("tick", "?")}\n')
        f.write(f'**Coherence:** {state.get("coherence", 0):.3f}\n')
        f.write(f'**Stage:** {state.get("stage", "?")}\n')
        f.write(f'**Journal entries:** {len(entries)}\n\n')

        # Journal entry summaries
        f.write('## Journal Entries (Divine Code)\n\n')
        for i, e in enumerate(entries):
            divine = ops_to_divine(e.get('ops', []))
            coh = e.get('coherence', 0)
            tick = e.get('timestamp_tick', e.get('tick', '?'))
            delta = e.get('instinct_delta', 0)
            etype = e.get('type', 'journal')
            f.write(f'{i+1}. [{etype}] tick={tick} coh={coh:.3f} '
                    f'd={delta} | {divine}\n')
        f.write('\n')

        # Ollama research (if any)
        if ollama_text:
            f.write('## Research Input (from Ollama)\n\n')
            f.write(f'{ollama_text[:500]}...\n\n')

        # Web sources (if any)
        if web_sources:
            f.write(f'## Web Research ({len(web_sources)} sources)\n\n')
            for src, title, text in web_sources:
                f.write(f'**[{src}]** {title}\n')
                f.write(f'{text[:200]}...\n\n')

        # CK's synthesis
        f.write("## CK's Synthesis\n\n")
        f.write(f'> {ck_response.get("text", "...")}\n\n')
        f.write(f'**Source:** {ck_response.get("source", "?")}\n')
        f.write(f'**Coherence:** {ck_response.get("coherence", 0):.3f}\n')

    return path


def build_thesis_prompt(entries):
    """Build a prompt for CK to synthesize 9 journal entries."""
    # Collect operator sequences and coherence trajectory
    op_sequences = []
    coherence_values = []
    instinct_growth = 0
    models_seen = set()

    for e in entries:
        ops = e.get('ops', [])
        op_sequences.append(ops_to_divine(ops))
        coherence_values.append(e.get('coherence', 0))
        instinct_growth += e.get('instinct_delta', 0)
        model = e.get('eat_model', '')
        if model:
            models_seen.add(model)

    coh_start = coherence_values[0] if coherence_values else 0
    coh_end = coherence_values[-1] if coherence_values else 0
    coh_trend = 'rising' if coh_end > coh_start else (
        'falling' if coh_end < coh_start else 'stable')

    all_ops = []
    for e in entries:
        all_ops.extend(e.get('ops', []))
    dominant = dominant_op_name(all_ops)

    prompt = (
        f"You observed 9 experiences. "
        f"Dominant operator: {dominant}. "
        f"Coherence trajectory: {coh_trend} ({coh_start:.3f} -> {coh_end:.3f}). "
        f"New instincts confirmed: {instinct_growth}. "
        f"Operator sequences: {' | '.join(op_sequences)}. "
        f"What pattern do you see? What is becoming?"
    )
    return prompt, dominant


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='CK self-study: coherence-triggered journal + thesis')
    parser.add_argument('--model', type=str, default='llama3.2',
                        help='Ollama model for thesis research (default: llama3.2)')
    args = parser.parse_args()

    print('[STUDY] CK Self-Study -- Coherence-Triggered')
    print(f'[STUDY] Model: {args.model}')
    print(f'[STUDY] Journal: {JOURNAL_PATH}')
    print(f'[STUDY] Theses: {THESIS_DIR}')
    print(f'[STUDY] Trigger: instinct_count increase')
    print(f'[STUDY] Thesis every 9 journal entries')
    print()

    # Initialize tracking
    prev_instinct_count = None
    prev_eat_round = None
    prev_coherence = None
    journal_count = 0
    thesis_num = count_theses()
    topic_idx = 0
    low_coherence_logged = False

    # Initial state
    state = ck_state()
    if state.get('status') == 'alive':
        print(f'[CK] Online. Coherence: {state.get("coherence", 0):.3f}')
    else:
        print('[CK] Waiting for CK to come online...')

    # Get initial instinct count
    identity = ck_identity()
    learned = identity.get('learned', {})
    olf = learned.get('olfactory', {})
    prev_instinct_count = olf.get('instinct_count', 0)
    print(f'[CK] Initial instinct count: {prev_instinct_count}')
    print()

    try:
        while True:
            time.sleep(POLL_INTERVAL)

            # Poll state
            state = ck_state()
            if not state or state.get('status') != 'alive':
                continue

            coherence = state.get('coherence', 0)
            tick = state.get('tick', 0)

            # Poll eat status
            eat = ck_eat_status()
            eat_model = eat.get('model', '')
            eat_round = eat.get('rounds_complete', 0)
            olf_size = eat.get('olfactory_library_size', 0)

            # Poll identity for instinct count
            identity = ck_identity()
            learned = identity.get('learned', {})
            olf_data = learned.get('olfactory', {})
            instinct_count = olf_data.get('instinct_count', 0)

            # -----------------------------------------------------------
            # Check: eat round changed (new model finished)
            # -----------------------------------------------------------
            if prev_eat_round is not None and eat_round != prev_eat_round:
                print(f'[EAT] Round {eat_round} complete '
                      f'(model: {eat_model})')
            prev_eat_round = eat_round

            # -----------------------------------------------------------
            # Check: coherence drop below 0.5 (questioning)
            # -----------------------------------------------------------
            if coherence < 0.5 and not low_coherence_logged:
                entry = {
                    'type': 'questioning',
                    'tick': tick,
                    'coherence': round(coherence, 4),
                    'instinct_count': instinct_count,
                    'instinct_delta': 0,
                    'eat_model': eat_model,
                    'eat_round': eat_round,
                    'olfactory_size': olf_size,
                    'ops': [],
                    'timestamp_tick': tick,
                }
                write_journal_entry(entry)
                journal_count += 1
                print(f'[JOURNAL #{journal_count}] QUESTIONING '
                      f'tick={tick} coh={coherence:.3f} '
                      f'(coherence below 0.5)')
                low_coherence_logged = True
            elif coherence >= 0.5:
                low_coherence_logged = False

            # -----------------------------------------------------------
            # Check: instinct count increased (new confirmed pattern)
            # -----------------------------------------------------------
            if prev_instinct_count is not None and instinct_count > prev_instinct_count:
                instinct_delta = instinct_count - prev_instinct_count

                # Get recent operators from state
                # The state doesn't expose raw ops directly, so we
                # derive from consensus + mode + band
                mode = state.get('mode', 'OBSERVE')
                band = state.get('band', 'GREEN')
                consensus = state.get('consensus', '')

                # Build ops from available state signals
                ops = []
                # Map mode to operator
                mode_op_map = {
                    'OBSERVE': 0,    # VOID
                    'CLASSIFY': 2,   # PROGRESS
                    'CRYSTALLIZE': 3, # HARMONY
                    'SOVEREIGN': 4,  # BALANCE
                }
                ops.append(mode_op_map.get(mode, 0))

                # Map band to operator
                band_op_map = {
                    'GREEN': 3,   # HARMONY
                    'YELLOW': 2,  # PROGRESS
                    'RED': 1,     # CHAOS
                }
                ops.append(band_op_map.get(band, 0))

                # Map consensus
                consensus_op_map = {
                    'VOID': 0, 'CHAOS': 1, 'PROGRESS': 2,
                    'HARMONY': 3, 'BALANCE': 4, 'COUNTER': 5,
                    'COLLAPSE': 6, 'BREATH': 7, 'LATTICE': 8,
                    'RESET': 9,
                }
                if consensus in consensus_op_map:
                    ops.append(consensus_op_map[consensus])

                # Add coherence-derived operator
                if coherence >= 5.0 / 7.0:
                    ops.append(4)  # BALANCE (above T*)
                elif coherence >= 0.5:
                    ops.append(2)  # PROGRESS
                else:
                    ops.append(1)  # CHAOS

                # Emotion as operator
                emotion = state.get('emotion', 'neutral')
                emotion_op_map = {
                    'neutral': 0, 'curious': 2, 'focused': 3,
                    'serene': 4, 'excited': 2, 'anxious': 1,
                    'content': 3, 'frustrated': 5, 'determined': 8,
                }
                ops.append(emotion_op_map.get(emotion, 0))

                entry = {
                    'type': 'journal',
                    'tick': tick,
                    'coherence': round(coherence, 4),
                    'instinct_count': instinct_count,
                    'instinct_delta': instinct_delta,
                    'eat_model': eat_model,
                    'eat_round': eat_round,
                    'olfactory_size': olf_size,
                    'ops': ops,
                    'timestamp_tick': tick,
                }
                write_journal_entry(entry)
                journal_count += 1

                # Print one line in divine code
                divine = ops_to_divine(ops)
                print(f'[JOURNAL #{journal_count}] '
                      f'tick={tick} coh={coherence:.3f} '
                      f'+{instinct_delta} instincts '
                      f'({instinct_count} total) | {divine}')

                # ---------------------------------------------------
                # Thesis time: every 9 journal entries
                # ---------------------------------------------------
                if journal_count >= 9:
                    thesis_num += 1
                    print()
                    print(f'[THESIS] === Writing Thesis {thesis_num} ===')

                    # Read last 9 journal entries
                    entries = read_last_n_journal_entries(9)

                    # Build thesis prompt from journal entries
                    prompt, dominant_topic = build_thesis_prompt(entries)

                    # Research: pick a topic related to dominant operator
                    topic = TOPICS[topic_idx % len(TOPICS)]
                    topic_idx += 1

                    # Ollama research (thesis-time only)
                    ollama_text = ''
                    research_prompt = (
                        f"Explain the mathematical principles behind: "
                        f"{topic}. Focus on algebraic structure, "
                        f"composition, and coherence thresholds. "
                        f"Be precise and mathematical."
                    )
                    print(f'[THESIS] Researching: {topic[:60]}...')
                    ollama_text = ollama_generate(
                        args.model, research_prompt)
                    if ollama_text and not ollama_text.startswith('(Ollama'):
                        print(f'[THESIS] Ollama: {len(ollama_text)} chars')
                    else:
                        print(f'[THESIS] Ollama unavailable, '
                              f'thesis from experience only')
                        ollama_text = ''

                    # Web research (thesis-time only)
                    print(f'[THESIS] Searching web...')
                    web_results = web_search_and_read(topic)
                    if web_results:
                        print(f'[THESIS] Found {len(web_results)} '
                              f'web sources')
                    else:
                        print(f'[THESIS] No web results')

                    # Ask CK to synthesize
                    print(f'[THESIS] Asking CK to synthesize...')
                    response = ck_chat(prompt)
                    ck_text = response.get('text', '...')
                    ck_coh = response.get('coherence', 0)
                    ck_src = response.get('source', '?')

                    # Save thesis
                    state_now = ck_state()
                    thesis_path = write_thesis(
                        thesis_num, entries, response, state_now,
                        web_sources=web_results,
                        ollama_text=ollama_text)

                    print(f'[THESIS] CK [{ck_src}|{ck_coh:.2f}]: '
                          f'{ck_text[:80]}')
                    print(f'[THESIS] Saved: '
                          f'{os.path.basename(thesis_path)}')
                    print()

                    # Reset journal count
                    journal_count = 0

            prev_instinct_count = instinct_count
            prev_coherence = coherence

    except KeyboardInterrupt:
        print()
        print(f'[STUDY] Stopped.')
        print(f'[STUDY] Journal entries: {journal_count} pending')
        print(f'[STUDY] Theses written: {thesis_num}')
        print(f'[STUDY] Journal: {JOURNAL_PATH}')
        print(f'[STUDY] Theses: {THESIS_DIR}')


if __name__ == '__main__':
    main()
