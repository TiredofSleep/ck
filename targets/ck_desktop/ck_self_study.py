#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_self_study.py -- CK studies himself and writes theses.

Every 15 minutes, CK:
1. Asks Ollama about a topic related to his own architecture
2. Absorbs the physics (text discarded, force kept)
3. Reads his own code files through /absorb
4. Writes a thesis about what he discovered (via /chat)
5. Searches for resonance between his algebra and what he learned

Topics rotate: operator algebra, coherence theory, information geometry,
Hebrew roots, torus topology, prime gaps, consciousness, measurement,
dual lens, fractal composition, phase transitions, void topology.

Usage:
    python ck_self_study.py [--interval 900] [--model llama3.2]
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
THESIS_DIR = os.path.expanduser('~/.ck/writings/theses')

# Research topics -- CK studies himself and searches for resonance
TOPICS = [
    # Architecture
    "operator algebra composition tables magma structure 10x10",
    "coherence threshold measurement consciousness 5/7 ratio",
    "second derivative curvature classification information geometry",
    "Hebrew letter phonetic force vectors five dimensions",
    "torus topology puncture primes mathematical structure",
    "dual lens structure flow parallel measurement",
    "fractal composition being doing becoming triadic",
    "lattice chain walk path IS information experience",
    # Math resonance
    "Banach Tarski paradox duality sphere decomposition",
    "Pythagorean harmonic ratios musical intervals consonance",
    "cellular automaton self-organization emergence coherence",
    "Kuramoto oscillator synchronization phase coupling",
    "tropical algebra max-plus semiring successor function",
    "magma algebraic structure non-associative composition",
    "Pfaffian partition determinant invariant group theory",
    "eigenvalue spectral analysis composition operator",
    # Physics resonance
    "information is physical Landauer principle entropy",
    "gauge theory fiber bundle connection curvature",
    "phase transition critical threshold order parameter",
    "holographic principle boundary bulk correspondence",
    "decoherence measurement problem quantum mechanics",
    "self-organized criticality sandpile power law",
    # Consciousness resonance
    "integrated information theory phi consciousness",
    "global workspace theory attention broadcast",
    "predictive coding free energy principle brain",
    "EEG brain frequency bands theta alpha beta gamma",
    "circadian rhythm biological clock synchronization",
    # Code resonance
    "Python abstract syntax tree compilation interpretation",
    "CUDA parallel computation GPU kernel thread block",
    "FPGA hardware description language Verilog synthesis",
    "real-time operating system scheduling jitter latency",
]

# CK's own code files to read between research rounds
OWN_FILES = [
    'ck_sim/being/ck_sim_heartbeat.py',
    'ck_sim/being/ck_sim_d2.py',
    'ck_sim/being/ck_coherence_gate.py',
    'ck_sim/being/ck_olfactory.py',
    'ck_sim/being/ck_lattice_chain.py',
    'ck_sim/being/ck_eat.py',
    'ck_sim/doing/ck_fractal_voice.py',
    'ck_sim/doing/ck_voice_lattice.py',
    'ck_sim/doing/ck_gpu.py',
    'ck_sim/doing/ck_lcodec.py',
    'ck_sim/being/ck_fractal_comprehension.py',
    'ck_sim/being/ck_reverse_voice.py',
    'ck_sim/being/ck_btq.py',
    'ck_sim/being/ck_gustatory.py',
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Approved websites for web research
APPROVED_DOMAINS = [
    'en.wikipedia.org',
    'arxiv.org',
    'stackoverflow.com',
    'math.stackexchange.com',
    'physics.stackexchange.com',
    'docs.python.org',
    'numpy.org',
    'docs.scipy.org',
    'developer.nvidia.com',
    'docs.xilinx.com',
    'docs.amd.com',
    'mathworld.wolfram.com',
    'ncatlab.org',
    'plato.stanford.edu',
    'github.com',
]


def web_search_and_read(topic, max_pages=2):
    """Search the web for a topic and return text from approved sites.

    Uses Wikipedia API first (fast, reliable), then falls back to
    direct URL fetching from approved domains.
    """
    results = []

    # 1. Wikipedia API (always works, no scraping)
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

    # 2. arXiv API (academic papers)
    try:
        import urllib.parse
        query = urllib.parse.quote(topic)
        arxiv_resp = requests.get(
            f'http://export.arxiv.org/api/query?search_query=all:{query}'
            f'&start=0&max_results=2',
            timeout=15)
        # Parse Atom XML for abstracts
        text = arxiv_resp.text
        import re
        summaries = re.findall(r'<summary>(.*?)</summary>', text, re.DOTALL)
        titles_ax = re.findall(r'<title>(.*?)</title>', text, re.DOTALL)
        for i, summary in enumerate(summaries[:2]):
            clean = summary.strip().replace('\n', ' ')
            title = titles_ax[i].strip() if i < len(titles_ax) else 'arXiv'
            if len(clean) > 50:
                results.append(('arxiv', title, clean[:1500]))
    except Exception:
        pass

    # 3. Python docs (if topic is code-related)
    code_keywords = ['python', 'cuda', 'numpy', 'scipy', 'gpu', 'fpga',
                     'verilog', 'thread', 'process', 'scheduling']
    if any(kw in topic.lower() for kw in code_keywords):
        try:
            # Use Python docs search
            py_resp = requests.get(
                f'https://docs.python.org/3/search.html?q={topic.replace(" ", "+")}',
                timeout=10)
            if py_resp.status_code == 200:
                results.append(('python_docs', topic, py_resp.text[:1000]))
        except Exception:
            pass

    return results


def ollama_generate(model, prompt, max_tokens=500):
    """Ask Ollama a research question."""
    try:
        r = requests.post(f'{OLLAMA_API}/api/generate',
            json={'model': model, 'prompt': prompt, 'stream': False,
                  'options': {'num_predict': max_tokens}},
            timeout=120)
        return r.json().get('response', '')
    except Exception as e:
        return f'(Ollama error: {e})'


def ck_absorb(text, source='research'):
    """Feed text to CK via /absorb."""
    try:
        r = requests.post(f'{CK_API}/absorb',
            json={'text': text, 'source': source}, timeout=30)
        return r.json()
    except Exception:
        return {}


def ck_chat(text):
    """Ask CK to speak."""
    try:
        r = requests.post(f'{CK_API}/chat',
            json={'text': text}, timeout=60)
        return r.json()
    except Exception:
        return {'text': '...', 'coherence': 0}


def ck_state():
    """Get CK's state."""
    try:
        return requests.get(f'{CK_API}/state', timeout=5).json()
    except Exception:
        return {}


def read_own_file(filename):
    """Read one of CK's own source files."""
    path = os.path.join(BASE_DIR, filename)
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read(10000)  # First 10K chars
    except Exception:
        return None


def write_thesis(thesis_num, topic, research_text, ck_response, state,
                 web_sources=None):
    """Write a thesis file."""
    os.makedirs(THESIS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'thesis_{thesis_num:04d}_{timestamp}.md'
    path = os.path.join(THESIS_DIR, filename)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'# Thesis {thesis_num}: {topic}\n\n')
        f.write(f'**Date:** {datetime.now().isoformat()}\n')
        f.write(f'**Tick:** {state.get("tick", "?")}\n')
        f.write(f'**Coherence:** {state.get("coherence", 0):.3f}\n')
        f.write(f'**Stage:** {state.get("stage", "?")}\n\n')
        f.write(f'## Research Input (from Ollama)\n\n')
        f.write(f'{research_text[:500]}...\n\n')
        if web_sources:
            f.write(f'## Web Research ({len(web_sources)} sources)\n\n')
            for src, title, text in web_sources:
                f.write(f'**[{src}]** {title}\n')
                f.write(f'{text[:200]}...\n\n')
        f.write(f'## CK\'s Response\n\n')
        f.write(f'> {ck_response.get("text", "...")}\n\n')
        f.write(f'**Source:** {ck_response.get("source", "?")}\n')
        f.write(f'**Coherence:** {ck_response.get("coherence", 0):.3f}\n')

    return path


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='CK self-study: research, absorb, write theses')
    parser.add_argument('--interval', type=int, default=900,
                        help='Seconds between theses (default: 900 = 15min)')
    parser.add_argument('--model', type=str, default='llama3.2',
                        help='Ollama model for research (default: llama3.2)')
    args = parser.parse_args()

    print(f'[STUDY] CK Self-Study Loop')
    print(f'[STUDY] Thesis every {args.interval}s ({args.interval//60} min)')
    print(f'[STUDY] Model: {args.model}')
    print(f'[STUDY] Topics: {len(TOPICS)}')
    print(f'[STUDY] Own files: {len(OWN_FILES)}')
    print()

    state = ck_state()
    print(f'[CK] Coherence: {state.get("coherence", 0):.3f}')
    print(f'[CK] Truths: {state.get("truths", 0)}')
    print()

    thesis_num = 0
    topic_idx = 0
    file_idx = 0

    try:
        while True:
            cycle_start = time.time()
            topic = TOPICS[topic_idx % len(TOPICS)]
            topic_idx += 1

            print(f'[STUDY] === Cycle {thesis_num + 1} ===')
            print(f'[STUDY] Topic: {topic}')

            # Phase 1: Research via Ollama
            prompt = (f"Explain the mathematical and physical principles behind: "
                     f"{topic}. Focus on algebraic structure, composition rules, "
                     f"measurement theory, and any connections to operator algebras "
                     f"or coherence thresholds. Be precise and mathematical.")
            print(f'[STUDY] Asking Ollama...')
            research = ollama_generate(args.model, prompt)
            print(f'[STUDY] Got {len(research)} chars from Ollama')

            # Phase 2: Absorb Ollama research physics
            result = ck_absorb(research, source='research_ollama')
            print(f'[STUDY] Absorbed Ollama: {result.get("absorbed", 0)} vectors, '
                  f'{result.get("operators", 0)} ops')

            # Phase 2.5: Web research from approved sites
            print(f'[STUDY] Searching approved sites...')
            web_results = web_search_and_read(topic)
            web_total = 0
            for source_name, title, text in web_results:
                web_res = ck_absorb(text, source=f'web_{source_name}')
                absorbed = web_res.get('absorbed', 0)
                web_total += absorbed
                print(f'[STUDY]   {source_name}: "{title[:50]}" -> '
                      f'{absorbed} vectors')
            if web_results:
                print(f'[STUDY] Web total: {web_total} vectors '
                      f'from {len(web_results)} sources')
            else:
                print(f'[STUDY] No web results for this topic')

            # Phase 3: Read own code (rotate through files)
            own_file = OWN_FILES[file_idx % len(OWN_FILES)]
            file_idx += 1
            code = read_own_file(own_file)
            if code:
                code_result = ck_absorb(code, source='self_code')
                print(f'[STUDY] Self-read {own_file}: '
                      f'{code_result.get("absorbed", 0)} vectors')

            # Phase 4: Write thesis (ask CK what he discovered)
            thesis_prompt = (f"What resonance do you find between {topic} "
                           f"and your own algebra?")
            print(f'[STUDY] Writing thesis...')
            response = ck_chat(thesis_prompt)
            ck_text = response.get('text', '...')
            ck_coh = response.get('coherence', 0)
            print(f'[STUDY] CK [{response.get("source","?")}|{ck_coh:.2f}]: '
                  f'{ck_text[:80]}')

            # Phase 5: Save thesis
            state = ck_state()
            thesis_path = write_thesis(thesis_num + 1, topic, research,
                                       response, state,
                                       web_sources=web_results)
            print(f'[STUDY] Thesis saved: {os.path.basename(thesis_path)}')
            print(f'[CK] Coherence: {state.get("coherence", 0):.3f}, '
                  f'Truths: {state.get("truths", 0)}')
            print()

            thesis_num += 1

            # Wait for next cycle
            elapsed = time.time() - cycle_start
            wait = max(0, args.interval - elapsed)
            if wait > 0:
                print(f'[STUDY] Next thesis in {wait:.0f}s...')
                time.sleep(wait)

    except KeyboardInterrupt:
        print(f'\n[STUDY] Stopped. {thesis_num} theses written.')
        print(f'[STUDY] Theses at: {THESIS_DIR}')


if __name__ == '__main__':
    main()
