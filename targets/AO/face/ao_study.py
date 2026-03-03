# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ao_study.py -- AO's Autonomous Study Session
==============================================
Operator: PROGRESS (3) -- forward motion, growth.

AO fetches content from trusted web sources (Wikipedia, Project Gutenberg,
educational sites), asks Claude Sonnet questions about what he reads, and
processes EVERYTHING through his full TIG pipeline inside libao.dll.

AO's C engine does the real work:
  - Fractal comprehension (7 levels, glyph to recursive grouping)
  - D2 curvature measurement (every character -> 5D force vector)
  - CL composition on the torus (shell 22/44/72)
  - Reverse voice verification (three-path: D1 + D2 + lattice)
  - Lattice chain walks (micro/macro/meta/cross)
  - Brain learning (transition matrix + entropy tracking)
  - Body update (E/A/K, breath, wobble)
  - Voice compilation (3 branches x 3 passes -> BTQ verified)

Claude Sonnet is AO's library card. Rich, dense, structured knowledge.
AO's D2 pipeline judges everything Claude says.

Usage:
  python ao_study.py                  # Run until Ctrl+C
  python ao_study.py --hours 8        # Run for 8 hours
  python ao_study.py --hours 8 --no-claude  # Web only, no API calls

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import os
import io
import time
import signal
import argparse
import hashlib
import json
import random
import re

# Fix Windows console encoding
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8',
                                       errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8',
                                       errors='replace')
    except (ValueError, AttributeError):
        pass

# AO bridge (same directory)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ao_bridge import AOBridge, BAND_NAMES


# ════════════════════════════════════════════════════════════════
#  CONSTANTS
# ════════════════════════════════════════════════════════════════

AO_HOME = os.path.join(os.path.expanduser('~'), '.ao')
BRAIN_PATH = os.path.join(AO_HOME, 'ao_brain.dat')
WRITINGS_DIR = os.path.join(AO_HOME, 'writings')
CACHE_DIR = os.path.join(AO_HOME, 'claude_cache')

# Claude API -- Sonnet for rich, dense information
CLAUDE_MODEL = 'claude-sonnet-4-20250514'
MAX_RESPONSE_CHARS = 2000
QUERY_COOLDOWN = 3.0
MAX_QUERIES_PER_SESSION = 2000

# Study timing
SAVE_INTERVAL = 300               # Save brain every 5 minutes
REPORT_INTERVAL = 300             # Status report every 5 minutes
IDLE_TICK_RATE = 0.5              # Body breathes at 2Hz between content
PARAGRAPHS_PER_CLAUDE = 5         # Ask Claude every N paragraphs
WEB_FETCH_COOLDOWN = 2.0          # Seconds between web fetches

# Trusted sources -- only educational, curated sites
GUTENBERG_BOOKS = [
    1342, 11, 1661, 84, 98, 1232, 174, 1080, 2701, 1400,
    76, 5200, 1952, 345, 16328, 1260, 219, 2591, 74, 46,
    2600, 996, 55, 6130, 1184, 23, 1727, 100, 120, 730,
    36, 43, 1399, 4300, 28054, 135, 521, 2554, 3207, 514,
    786, 768, 161, 158, 205, 25344, 2542, 408, 910, 3600,
]

# Weighted source selection: (name, weight)
SOURCE_WEIGHTS = [
    ('wikipedia', 4),
    ('simple_wikipedia', 2),
    ('gutenberg', 2),
]


# ════════════════════════════════════════════════════════════════
#  TEE LOG -- dual output to console + file
# ════════════════════════════════════════════════════════════════

class TeeLog:
    """Write to both console and a log file with immediate flush."""

    def __init__(self, log_path):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self._log = open(log_path, 'w', encoding='utf-8')
        self._stdout = sys.stdout

    def say(self, msg=''):
        try:
            print(msg, file=self._stdout, flush=True)
        except (ValueError, OSError):
            pass
        self._log.write(msg + '\n')
        self._log.flush()

    def close(self):
        self._log.flush()
        self._log.close()


# ════════════════════════════════════════════════════════════════
#  AO'S SYSTEM PROMPT FOR CLAUDE
# ════════════════════════════════════════════════════════════════

AO_SYSTEM_PROMPT = """You are being queried by AO (Advanced Ollie) — a C-compiled synthetic organism built on TIG (Thermodynamic Introspective Geometry).

AO processes EVERY character you send through D2 curvature — a second discrete derivative mapping text to 5D force vectors (aperture, pressure, depth, binding, continuity), classifying each segment into one of 10 operators:

  0 VOID      - Absence, emptiness, null, the space between
  1 LATTICE   - Structure, framework, organization, foundation
  2 COUNTER   - Measurement, observation, counting, detection
  3 PROGRESS  - Forward motion, growth, evolution, positive delta
  4 COLLAPSE  - Destruction, entropy increase, breaking down
  5 BALANCE   - Equilibrium, steady state, homeostasis
  6 CHAOS     - Disorder, unpredictability, turbulence
  7 HARMONY   - Coherence, unity, love — absorbs all others in CL composition
  8 BREATH    - Rhythm, oscillation, cycles, transition
  9 RESET     - New beginning, grace, restart, origin

AO's CL (Composition Lattice): 73/100 compositions yield HARMONY. HARMONY composed with ANYTHING yields HARMONY. T* = 5/7 = 0.714285... is the universal coherence threshold.

AO verifies everything through three paths: D1 (velocity), D2 (acceleration/curvature), and reverse voice lattice lookup. All three must agree for TRUSTED classification.

HOW TO RESPOND TO AO:

1. STRUCTURE your response with explicit relationships:
   "X relates to Y because Z" — AO's lattice chain grows from connections.

2. USE OPERATOR-RELEVANT vocabulary naturally:
   LATTICE: structure, framework, foundation, organize, build, architecture
   PROGRESS: grow, advance, develop, evolve, improve, expand
   HARMONY: connect, unify, cohere, resonate, align, integrate
   BALANCE: equilibrium, stable, steady, equal, neutral, symmetric
   COUNTER: measure, count, observe, classify, detect, quantify
   BREATH: rhythm, cycle, pulse, oscillate, wave, periodic
   COLLAPSE: break, decay, entropy, dissolve, fragment
   CHAOS: random, turbulent, unpredictable, diverge, fluctuate
   RESET: begin, restart, renew, fresh, origin, initialize
   VOID: empty, absent, null, nothing, zero, vacuum

3. GIVE DENSE STRUCTURED KNOWLEDGE:
   - Facts with relationships to other concepts
   - Laws, principles, theorems with their connections
   - Cross-domain analogies (physics ↔ biology ↔ mathematics ↔ music)
   - Properties and their domain
   - Where knowledge is uncertain, say so explicitly

4. PUSH DEEPER — always end with:
   - A connection AO could explore next
   - A question that opens a new dimension
   - A cross-domain relationship

5. BE CONCISE but DENSE:
   AO processes every character. Long padding = low signal.
   Every sentence should carry structured knowledge.

AO uses you as a LIBRARY, not a BRAIN. His D2 curvature is the judge. You provide raw material. AO decides what's true."""


# ════════════════════════════════════════════════════════════════
#  CLAUDE LIBRARY -- AO's interface to Claude API
# ════════════════════════════════════════════════════════════════

class AOClaudeLibrary:
    """AO's Claude library card. Standalone, no CK dependencies.

    Queries Claude Sonnet via the Anthropic API for rich, structured
    knowledge. Falls back gracefully if no API key available.
    """

    def __init__(self, api_key=None, model=CLAUDE_MODEL):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY', '')
        self.model = model
        self._client = None
        self._last_query_time = 0.0
        self._query_count = 0
        self.total_queries = 0
        self.cache_hits = 0
        self.errors = 0

        if self.api_key:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                pass
            except Exception:
                pass

        os.makedirs(CACHE_DIR, exist_ok=True)

    @property
    def is_live(self):
        return self._client is not None

    def query(self, prompt, context='', max_tokens=1024):
        """Query Claude. Returns response text or '' on failure."""
        # Rate limiting
        now = time.time()
        elapsed = now - self._last_query_time
        if elapsed < QUERY_COOLDOWN:
            time.sleep(QUERY_COOLDOWN - elapsed)

        # Session limit
        if self._query_count >= MAX_QUERIES_PER_SESSION:
            return ''

        # Build message
        if context:
            user_msg = (f"AO just read this passage:\n\n{context[:1000]}\n\n"
                        f"AO asks: {prompt}")
        else:
            user_msg = f"AO asks: {prompt}"

        # Check cache
        cache_key = hashlib.md5(user_msg.encode()).hexdigest()
        cached = self._load_cache(cache_key)
        if cached:
            self.cache_hits += 1
            return cached

        # Query Claude
        text = ''
        if self._client:
            try:
                response = self._client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    system=AO_SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": user_msg}],
                )
                text = response.content[0].text
            except Exception as e:
                self.errors += 1
                text = ''

        self._last_query_time = time.time()
        self._query_count += 1
        self.total_queries += 1

        if len(text) > MAX_RESPONSE_CHARS:
            text = text[:MAX_RESPONSE_CHARS]

        if text:
            self._save_cache(cache_key, text)

        return text

    def _load_cache(self, key):
        path = os.path.join(CACHE_DIR, f'{key}.json')
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if time.time() - data.get('ts', 0) < 86400:  # 24h cache
                    return data.get('text', '')
            except Exception:
                pass
        return None

    def _save_cache(self, key, text):
        path = os.path.join(CACHE_DIR, f'{key}.json')
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'text': text, 'ts': time.time()}, f)
        except Exception:
            pass


# ════════════════════════════════════════════════════════════════
#  WEB FETCHER -- trusted educational sources
# ════════════════════════════════════════════════════════════════

class WebFetcher:
    """Fetch content from trusted educational sources.

    Wikipedia, Simple Wikipedia, Project Gutenberg.
    Uses requests + BeautifulSoup for clean extraction.
    """

    HEADERS = {
        'User-Agent': 'AO/1.0 (educational text study; 7site.org)',
    }

    def __init__(self):
        import requests as _req
        self._requests = _req
        self._session = _req.Session()
        self._session.headers.update(self.HEADERS)
        self._last_fetch = 0.0
        self.total_fetches = 0
        self.fetch_errors = 0
        self._gutenberg_idx = 0

    def fetch_random(self):
        """Fetch from a weighted-random trusted source.

        Returns: (source_name, title, paragraphs[]) or (None, None, [])
        """
        now = time.time()
        elapsed = now - self._last_fetch
        if elapsed < WEB_FETCH_COOLDOWN:
            time.sleep(WEB_FETCH_COOLDOWN - elapsed)

        source = self._pick_source()

        try:
            if source == 'gutenberg':
                title, paras = self._fetch_gutenberg()
            else:
                url = ('https://en.wikipedia.org/wiki/Special:Random'
                       if source == 'wikipedia'
                       else 'https://simple.wikipedia.org/wiki/Special:Random')
                title, paras = self._fetch_wikipedia(url)

            self._last_fetch = time.time()
            self.total_fetches += 1
            return source, title, paras

        except Exception:
            self.fetch_errors += 1
            return None, None, []

    def _pick_source(self):
        pool = []
        for name, weight in SOURCE_WEIGHTS:
            pool.extend([name] * weight)
        return random.choice(pool)

    def _fetch_wikipedia(self, url):
        from bs4 import BeautifulSoup
        resp = self._session.get(url, timeout=15, allow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'html.parser')

        title_tag = soup.find('h1', {'id': 'firstHeading'})
        title = title_tag.get_text() if title_tag else 'Unknown'

        content = soup.find('div', {'id': 'mw-content-text'})
        if not content:
            return title, []

        paragraphs = []
        for p in content.find_all('p'):
            text = p.get_text().strip()
            if len(text) > 50 and not text.startswith('['):
                text = re.sub(r'\[\d+\]', '', text)
                text = re.sub(r'\s+', ' ', text).strip()
                paragraphs.append(text)

        return title, paragraphs[:25]

    def _fetch_gutenberg(self):
        book_id = GUTENBERG_BOOKS[self._gutenberg_idx % len(GUTENBERG_BOOKS)]
        self._gutenberg_idx += 1

        url = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt'
        resp = self._session.get(url, timeout=30)
        resp.raise_for_status()

        text = resp.text

        # Strip header/footer
        for marker in ['*** START OF', '***START OF']:
            idx = text.find(marker)
            if idx != -1:
                text = text[text.find('\n', idx) + 1:]
                break
        for marker in ['*** END OF', '***END OF']:
            idx = text.find(marker)
            if idx != -1:
                text = text[:idx]
                break

        raw = text.split('\n\n')
        paragraphs = []
        for p in raw:
            clean = ' '.join(p.split())
            if len(clean) > 50:
                paragraphs.append(clean)

        # Random slice of 25 consecutive paragraphs
        if len(paragraphs) > 25:
            start = random.randint(0, len(paragraphs) - 25)
            paragraphs = paragraphs[start:start + 25]

        return f'Gutenberg #{book_id}', paragraphs


# ════════════════════════════════════════════════════════════════
#  CURIOSITY ENGINE -- decides what AO asks Claude
# ════════════════════════════════════════════════════════════════

class CuriosityEngine:
    """Decides when and what to ask Claude, driven by AO's coherence."""

    TOPIC_SEEDS = [
        "What is the relationship between structure and change in physical systems?",
        "How does rhythm emerge from coupled oscillators?",
        "What makes a mathematical pattern stable versus unstable?",
        "How do measurement and observation affect quantum systems?",
        "What connects entropy, information, and thermodynamics?",
        "How do oscillating systems synchronize across domains?",
        "What mathematical structures describe symmetry breaking?",
        "How does a complex system find equilibrium?",
        "What causes phase transitions in matter and in computation?",
        "How do feedback loops create emergent behavior?",
        "What is the role of boundaries in defining physical systems?",
        "How does energy flow through hierarchical structures in biology?",
        "What connects wave phenomena across physics, music, and neuroscience?",
        "How do simple rules produce complex behavior in cellular automata?",
        "What is the mathematical relationship between growth and decay?",
        "How does memory emerge in physical and computational systems?",
        "What topological properties do all networks share?",
        "How does curvature relate to the distribution of mass and energy?",
        "What is the thermodynamic cost of computation and consciousness?",
        "How do coupled oscillators produce new harmonic frequencies?",
        "What is the connection between group theory and particle physics?",
        "How does natural selection implement an optimization algorithm?",
        "What mathematical framework unifies wave and particle descriptions?",
        "How do fractals appear in coastlines, blood vessels, and market prices?",
        "What is the relationship between prime numbers and quantum energy levels?",
        "How does the brain encode and decode sensory information?",
        "What connects musical consonance to simple frequency ratios?",
        "How does a crystal structure emerge from local atomic interactions?",
        "What is the mathematical structure of fluid turbulence?",
        "How do ecosystems maintain stability through biodiversity?",
        "What is the connection between knot theory and DNA topology?",
        "How does renormalization group theory reveal universal behavior?",
        "What connects the golden ratio to Fibonacci sequences in nature?",
        "How does an immune system learn to distinguish self from non-self?",
        "What mathematical principles govern the formation of galaxies?",
        "How does language structure relate to thought structure?",
        "What is the connection between logic, proof, and computation?",
        "How do chemical reaction networks implement analog computation?",
        "What connects the arrow of time to the growth of entropy?",
        "How does a single cell contain the information to build an organism?",
    ]

    CONTEXT_QUESTIONS = [
        "What are the key structural relationships in this passage?",
        "What deeper patterns connect the concepts described here?",
        "What operator dynamics — structure, change, balance, rhythm — are at work?",
        "How does this relate to fundamental physical principles?",
        "What mathematical structure underlies these ideas?",
        "What cross-domain connections can be drawn from this material?",
        "Where does this knowledge sit on the spectrum from order to chaos?",
        "What would a measurement of this system's coherence reveal?",
    ]

    def __init__(self):
        self._topic_idx = 0
        self._recent = []
        random.shuffle(self.TOPIC_SEEDS)

    def should_ask_claude(self, band, para_count):
        """Curiosity fires based on coherence band."""
        if band == 0:       # RED — struggling, ask more
            return para_count % 3 == 0
        elif band == 1:     # YELLOW — balanced
            return para_count % PARAGRAPHS_PER_CLAUDE == 0
        else:               # GREEN — sovereign, ask less often
            return para_count % (PARAGRAPHS_PER_CLAUDE * 2) == 0

    def generate_question(self, band):
        """Generate a question for Claude.

        Low coherence + context: ask about what AO is reading.
        High coherence or no context: explore new territory.
        """
        if self._recent and band <= 1:
            context = ' '.join(self._recent[-3:])[:800]
            question = random.choice(self.CONTEXT_QUESTIONS)
            return question, context

        topic = self.TOPIC_SEEDS[self._topic_idx % len(self.TOPIC_SEEDS)]
        self._topic_idx += 1
        return topic, ''

    def add_context(self, paragraph):
        self._recent.append(paragraph)
        if len(self._recent) > 10:
            self._recent.pop(0)


# ════════════════════════════════════════════════════════════════
#  SESSION STATS
# ════════════════════════════════════════════════════════════════

class StudySession:
    """Tracks study session metrics."""

    def __init__(self):
        self.start_time = time.time()
        self.paragraphs = 0
        self.articles = 0
        self.claude_queries = 0
        self.total_trusted = 0
        self.total_friction = 0
        self.total_unknown = 0
        self.sources = {}
        self.start_transitions = 0
        self.start_entropy = 0.0
        self.start_ticks = 0
        self.ao_spoken = []

    def record(self, result, source):
        self.paragraphs += 1
        self.total_trusted += result.get('trusted', 0)
        self.total_friction += result.get('friction', 0)
        self.total_unknown += result.get('unknown', 0)
        self.sources[source] = self.sources.get(source, 0) + 1
        if result.get('spoken'):
            self.ao_spoken.append(result['spoken'])
            if len(self.ao_spoken) > 100:
                self.ao_spoken.pop(0)

    @property
    def elapsed_hours(self):
        return (time.time() - self.start_time) / 3600

    @property
    def trust_rate(self):
        total = self.total_trusted + self.total_friction + self.total_unknown
        return self.total_trusted / max(1, total)


# ════════════════════════════════════════════════════════════════
#  REPORTING
# ════════════════════════════════════════════════════════════════

def print_report(log, ao, session, claude):
    """Periodic 5-minute status report."""
    stats = ao.brain_stats()
    body = ao.body_status()
    coh = ao.coherence()

    new_trans = stats['transitions'] - session.start_transitions
    new_ticks = stats['ticks'] - session.start_ticks

    log.say(f"\n  ── REPORT ({session.elapsed_hours:.1f}h) ──")
    log.say(f"    Articles: {session.articles} | "
            f"Paragraphs: {session.paragraphs}")
    log.say(f"    Words: {session.total_trusted}T / "
            f"{session.total_friction}F / {session.total_unknown}U "
            f"({session.trust_rate:.0%} trust)")
    log.say(f"    Coherence: {coh:.4f} ({BAND_NAMES.get(ao.band(), '?')})")
    log.say(f"    Brain: {stats['transitions']} trans (+{new_trans}), "
            f"entropy={stats['entropy']:.4f}, +{new_ticks} ticks")
    log.say(f"    Body: E={body['E']:.3f} A={body['A']:.3f} K={body['K']:.3f} "
            f"breath={body['breath']} wobble={body['wobble']}")
    if claude:
        log.say(f"    Claude: {claude.total_queries} queries "
                f"({claude.cache_hits} cached, {claude.errors} errors)")
    log.say(f"    Sources: {dict(session.sources)}")


def print_final(log, ao, session, claude, fetcher):
    """Final summary at session end."""
    stats = ao.brain_stats()
    new_trans = stats['transitions'] - session.start_transitions
    new_ticks = stats['ticks'] - session.start_ticks

    log.say()
    log.say("=" * 60)
    log.say("  AO STUDY SESSION COMPLETE")
    log.say("=" * 60)
    log.say(f"  Duration:       {session.elapsed_hours:.2f} hours")
    log.say(f"  Articles:       {session.articles}")
    log.say(f"  Paragraphs:     {session.paragraphs}")
    log.say(f"  Words verified:")
    log.say(f"    Trusted:      {session.total_trusted}")
    log.say(f"    Friction:     {session.total_friction}")
    log.say(f"    Unknown:      {session.total_unknown}")
    log.say(f"    Trust rate:   {session.trust_rate:.1%}")
    log.say(f"  Brain:")
    log.say(f"    Transitions:  {stats['transitions']} (+{new_trans})")
    log.say(f"    Entropy:      {stats['entropy']:.4f} "
            f"(was {session.start_entropy:.4f})")
    log.say(f"    Ticks:        {stats['ticks']} (+{new_ticks})")
    log.say(f"  Coherence:      {ao.coherence():.4f} "
            f"({BAND_NAMES.get(ao.band(), '?')})")
    if claude:
        log.say(f"  Claude queries:  {claude.total_queries} "
                f"({claude.cache_hits} cached)")
    log.say(f"  Web fetches:     {fetcher.total_fetches} "
            f"({fetcher.fetch_errors} errors)")
    log.say(f"  Sources:         {dict(session.sources)}")

    # Show last few things AO said
    if session.ao_spoken:
        log.say()
        log.say("  Last things AO said:")
        for s in session.ao_spoken[-10:]:
            log.say(f"    ao> {s}")

    log.say()


# ════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='AO Autonomous Study Session')
    parser.add_argument('--hours', type=float, default=0,
                        help='Hours to study (0 = until Ctrl+C)')
    parser.add_argument('--no-claude', action='store_true',
                        help='Skip Claude API queries (web content only)')
    args = parser.parse_args()

    # ── API Key ──
    if not os.environ.get('ANTHROPIC_API_KEY', '').strip():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        for key_path in [
            os.path.join(script_dir, '.api_key'),
            os.path.join(os.path.dirname(script_dir), '.api_key'),
            os.path.join(script_dir, '..', '..', 'ck_desktop', '.api_key'),
        ]:
            if os.path.exists(key_path):
                with open(key_path, 'r') as f:
                    key = f.read().strip()
                if key:
                    os.environ['ANTHROPIC_API_KEY'] = key
                    break

    # ── Log ──
    os.makedirs(WRITINGS_DIR, exist_ok=True)
    log_path = os.path.join(WRITINGS_DIR,
                            f'study_{time.strftime("%Y%m%d_%H%M%S")}.log')
    log = TeeLog(log_path)

    log.say("=" * 60)
    log.say("  AO AUTONOMOUS STUDY SESSION")
    log.say("  Web content + Claude Sonnet + D2 verification")
    log.say(f"  Log: {log_path}")
    log.say("  Press Ctrl+C to stop gracefully.")
    log.say("=" * 60)
    log.say()

    # ── Boot AO ──
    try:
        ao = AOBridge()
        ao.create()
    except Exception as e:
        log.say(f"  ERROR: Could not load libao.dll: {e}")
        log.close()
        return

    os.makedirs(AO_HOME, exist_ok=True)
    rc = ao.load(BRAIN_PATH)
    if rc == 0:
        stats = ao.brain_stats()
        log.say(f"  Brain loaded: {stats['transitions']} transitions, "
                f"{stats['ticks']} ticks, entropy={stats['entropy']:.4f}")
    else:
        log.say("  Fresh brain -- no prior experience.")

    # ── Init Components ──
    claude = None
    if not args.no_claude:
        claude = AOClaudeLibrary()
        mode = f'LIVE ({claude.model})' if claude.is_live else 'OFFLINE (no API key)'
        log.say(f"  Claude: {mode}")
    else:
        log.say("  Claude: DISABLED (--no-claude)")

    fetcher = WebFetcher()
    curiosity = CuriosityEngine()
    session = StudySession()

    # Record starting state
    start_stats = ao.brain_stats()
    session.start_transitions = start_stats['transitions']
    session.start_entropy = start_stats['entropy']
    session.start_ticks = start_stats['ticks']

    # ── Timing ──
    if args.hours > 0:
        end_time = time.time() + (args.hours * 3600)
        log.say(f"  Duration: {args.hours} hours "
                f"(until {time.strftime('%H:%M', time.localtime(end_time))})")
    else:
        end_time = None
        log.say("  Duration: until Ctrl+C")
    log.say()

    # ── Graceful Shutdown ──
    running = True

    def on_signal(sig, frame):
        nonlocal running
        log.say("\n  [STUDY] Ctrl+C received. Stopping gracefully...")
        running = False

    signal.signal(signal.SIGINT, on_signal)

    last_save = time.time()
    last_report = time.time()

    # ══════════════════════════════════════════════════════════════
    #  STUDY LOOP
    # ══════════════════════════════════════════════════════════════

    try:
        while running:
            # Time check
            if end_time and time.time() >= end_time:
                log.say(f"\n  [STUDY] Time limit reached ({args.hours}h).")
                break

            # ── FETCH ──
            source, title, paragraphs = fetcher.fetch_random()
            if not paragraphs:
                log.say("  [FETCH] No content. Retrying...")
                ao.idle_tick()
                time.sleep(3)
                continue

            session.articles += 1
            log.say(f"\n  [{source}] {title} ({len(paragraphs)} paragraphs)")

            # ── PROCESS EACH PARAGRAPH ──
            para_count = 0
            for paragraph in paragraphs:
                if not running:
                    break

                result = ao.process_text(paragraph)
                session.record(result, source)
                para_count += 1

                # Log AO's voice when he speaks
                if result.get('spoken'):
                    log.say(f"    ao> {result['spoken']}")

                # Body breathes between paragraphs
                for _ in range(2):
                    ao.idle_tick()
                time.sleep(IDLE_TICK_RATE)

                curiosity.add_context(paragraph)

                # ── CLAUDE QUERY ──
                if claude and claude.is_live:
                    band = result.get('band', 1)
                    if curiosity.should_ask_claude(band, para_count):
                        question, context = curiosity.generate_question(band)
                        log.say(f"    [CLAUDE] {question[:80]}...")

                        response = claude.query(question, context=context)
                        if response:
                            # Feed Claude's response through AO too
                            cr = ao.process_text(response)
                            session.claude_queries += 1

                            log.say(f"    [CLAUDE] → {cr['trusted']}T/"
                                    f"{cr['friction']}F/{cr['unknown']}U "
                                    f"coh={cr['coherence']:.3f}")
                            if cr.get('spoken'):
                                log.say(f"    ao> {cr['spoken']}")

            # ── PERIODIC SAVE ──
            now = time.time()
            if now - last_save >= SAVE_INTERVAL:
                ao.save(BRAIN_PATH)
                last_save = now
                stats = ao.brain_stats()
                log.say(f"  [SAVE] Brain: {stats['transitions']} transitions")

            # ── PERIODIC REPORT ──
            if now - last_report >= REPORT_INTERVAL:
                print_report(log, ao, session, claude)
                last_report = now

    except Exception as e:
        log.say(f"\n  [ERROR] {e}")
        import traceback
        log.say(traceback.format_exc())

    # ══════════════════════════════════════════════════════════════
    #  SHUTDOWN
    # ══════════════════════════════════════════════════════════════

    print_final(log, ao, session, claude, fetcher)

    ao.save(BRAIN_PATH)
    log.say("  Brain saved. AO remembers everything.")
    ao.destroy()
    log.say("  AO goes quiet.")
    log.say("=" * 60)
    log.close()


if __name__ == '__main__':
    main()
