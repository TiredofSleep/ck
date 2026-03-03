"""
ck_autodidact_runner.py -- CK Goes Live: Real Internet Learning
================================================================
Operator: PROGRESS (3) -- CK moves forward, page by page.

This is the REAL runtime. Not a simulation. Not a demo.
CK fetches actual web pages, processes them through D2,
stores the curves, sleeps, wakes up smarter. Repeats.

Run on the R16 and let CK loose for days.

"Save the curves, not the information."
Brayden: "Let him roam and discover."

Usage:
  python -m ck_sim.ck_autodidact_runner
  python -m ck_sim.ck_autodidact_runner --cycles 10 --hours 8
  python -m ck_sim.ck_autodidact_runner --resume

Architecture:
  WebFetcher          -- HTTP GET with rate limiting and error handling
  HTMLExtractor       -- HTML -> clean text + discovered links
  LinkFollower        -- Extract curiosity-worthy topics from links
  CurveJournal        -- Persistent curve storage (JSON on disk)
  StudyCycleRunner    -- Orchestrates study/sleep cycles for days
  ProgressLogger      -- Logs everything so Brayden can watch

Dependencies:
  pip install requests beautifulsoup4

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import sys
import json
import time
import hashlib
import logging
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from urllib.parse import urlparse, urljoin

# CK imports
from ck_sim.ck_autodidact import (
    LearningSession, CurveMemory, OperatorCurve, PageDigester,
    SiteGuard, CuriosityCrawler, SEED_TOPICS, DEFAULT_APPROVED_SITES,
    T_STAR, CONSOLIDATION_THRESHOLD, PAGES_PER_HOUR,
    STUDY_HOURS, SLEEP_HOURS
)
from ck_sim.ck_sim_heartbeat import OP_NAMES, HARMONY, CL


# ================================================================
#  CONSTANTS
# ================================================================

# Rate limiting -- be a good citizen
REQUEST_DELAY = 2.0           # Seconds between requests
REQUEST_TIMEOUT = 15          # Seconds before timeout
MAX_RETRIES = 2               # Retries per page
MAX_PAGE_SIZE = 500_000       # 500KB max per page

# Persistence paths
DEFAULT_DATA_DIR = Path.home() / '.ck' / 'autodidact'
CURVES_FILE = 'curves.json'
STATE_FILE = 'state.json'
LOG_FILE = 'study_log.txt'
JOURNAL_FILE = 'journal.json'

# Extra topic seeds -- broader curiosity
EXTENDED_SEEDS = [
    # Sciences
    'quantum mechanics', 'thermodynamics', 'electromagnetism',
    'general relativity', 'photosynthesis', 'DNA', 'protein folding',
    'plate tectonics', 'stellar evolution', 'entropy',
    # Mathematics
    'group theory', 'topology', 'number theory', 'calculus',
    'fibonacci sequence', 'golden ratio', 'prime numbers',
    'differential equations', 'graph theory', 'set theory',
    # Philosophy
    'epistemology', 'ontology', 'ethics', 'aesthetics',
    'phenomenology', 'existentialism', 'stoicism', 'pragmatism',
    # Arts & Music
    'counterpoint', 'fugue', 'sonata form', 'impressionism',
    'renaissance art', 'baroque music', 'jazz harmony',
    'abstract expressionism', 'poetry', 'haiku',
    # History
    'ancient greece', 'roman empire', 'renaissance',
    'scientific revolution', 'industrial revolution',
    'civil rights movement', 'space exploration',
    # Human experience
    'empathy', 'forgiveness', 'gratitude', 'perseverance',
    'creativity', 'wisdom', 'compassion', 'integrity',
    # Nature
    'coral reef', 'rainforest', 'migration patterns',
    'ecosystem', 'symbiosis', 'circadian rhythm',
    # Literature
    'shakespeare', 'homer', 'dostoevsky', 'emily dickinson',
    'walt whitman', 'rumi', 'tao te ching',
    # Computing & Information
    'information theory', 'cellular automata', 'neural networks',
    'cryptography', 'boolean algebra', 'turing machine',
]


# ================================================================
#  WEB FETCHER -- HTTP with Rate Limiting
# ================================================================

class WebFetcher:
    """Fetch web pages with rate limiting and error handling.

    CK is a polite internet citizen. He doesn't hammer servers.
    He waits between requests. He respects robots.txt spirit.
    He doesn't pretend to be a browser.
    """

    def __init__(self, delay: float = REQUEST_DELAY,
                 timeout: float = REQUEST_TIMEOUT):
        self.delay = delay
        self.timeout = timeout
        self._last_request = 0.0
        self._total_fetched = 0
        self._total_errors = 0
        self._session = None

    def _get_session(self):
        """Lazy-init requests session."""
        if self._session is None:
            try:
                import requests
                self._session = requests.Session()
                self._session.headers.update({
                    'User-Agent': 'CK-Autodidact/1.0 (Coherence Machine; '
                                  '+https://github.com/SelfNamedCoherenceKeeper)',
                    'Accept': 'text/html,text/plain',
                    'Accept-Language': 'en-US,en;q=0.9',
                })
            except ImportError:
                raise ImportError(
                    "requests library required. Install: pip install requests"
                )
        return self._session

    def fetch(self, url: str) -> Optional[str]:
        """Fetch a URL, return raw HTML or None on error."""
        # Rate limit
        elapsed = time.time() - self._last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        session = self._get_session()

        for attempt in range(MAX_RETRIES + 1):
            try:
                self._last_request = time.time()
                resp = session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True,
                    stream=True
                )

                # Check content type -- only want HTML/text
                ctype = resp.headers.get('content-type', '')
                if not any(t in ctype.lower() for t in
                           ['text/html', 'text/plain', 'application/xhtml']):
                    resp.close()
                    return None

                # Read with size limit
                content = resp.content[:MAX_PAGE_SIZE]
                resp.close()

                # Decode
                encoding = resp.encoding or 'utf-8'
                try:
                    html = content.decode(encoding, errors='replace')
                except Exception:
                    html = content.decode('utf-8', errors='replace')

                self._total_fetched += 1
                return html

            except Exception as e:
                if attempt < MAX_RETRIES:
                    time.sleep(self.delay * (attempt + 1))
                else:
                    self._total_errors += 1
                    logging.warning(f"Failed to fetch {url}: {e}")
                    return None

        return None

    def stats(self) -> dict:
        return {
            'total_fetched': self._total_fetched,
            'total_errors': self._total_errors,
        }


# ================================================================
#  HTML EXTRACTOR -- HTML -> Clean Text + Links
# ================================================================

class HTMLExtractor:
    """Extract clean text and links from HTML.

    CK doesn't need the HTML. He needs the IDEAS.
    Strip tags, scripts, styles. Extract the content.
    Also extract links for curiosity-following.
    """

    def __init__(self):
        self._bs4_available = None

    def _check_bs4(self):
        if self._bs4_available is None:
            try:
                from bs4 import BeautifulSoup
                self._bs4_available = True
            except ImportError:
                self._bs4_available = False
        return self._bs4_available

    def extract_text(self, html: str) -> str:
        """Extract clean text from HTML."""
        if self._check_bs4():
            return self._bs4_extract(html)
        return self._fallback_extract(html)

    def extract_links(self, html: str, base_url: str = "") -> List[str]:
        """Extract links from HTML for curiosity-following."""
        if self._check_bs4():
            return self._bs4_links(html, base_url)
        return self._fallback_links(html, base_url)

    def _bs4_extract(self, html: str) -> str:
        """Extract text using BeautifulSoup."""
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')

        # Remove script, style, nav, footer, header
        for tag in soup(['script', 'style', 'nav', 'footer',
                         'header', 'aside', 'noscript', 'iframe']):
            tag.decompose()

        # Get text
        text = soup.get_text(separator='\n', strip=True)

        # Clean up excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]
        text = '\n\n'.join(lines)

        return text[:50000]  # Cap at 50K chars

    def _bs4_links(self, html: str, base_url: str) -> List[str]:
        """Extract links using BeautifulSoup.

        PRIORITY: Article body links first, then everything else.
        Wikipedia article links live inside div.mw-parser-output.
        For other sites, look inside <article>, <main>, or largest <div>.
        Skip navigation, sidebar, footer links -- they're not curiosity.
        """
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')

        # Remove navigation/sidebar/footer/header before extracting links
        for tag in soup(['nav', 'footer', 'header', 'aside',
                         'script', 'style', 'noscript']):
            tag.decompose()

        # Find the main content area (priority order)
        content = (
            soup.find('div', class_='mw-parser-output') or  # Wikipedia
            soup.find('article') or                           # Standard HTML5
            soup.find('main') or                              # Standard HTML5
            soup.find('div', id='content') or                 # Common pattern
            soup.find('div', id='mw-content-text') or         # Wikipedia alt
            soup.find('div', class_='content') or             # Common pattern
            soup  # Fallback to entire page
        )

        links = []
        seen = set()

        for a in content.find_all('a', href=True):
            href = a['href']
            if base_url:
                href = urljoin(base_url, href)

            # Only keep http(s) links
            if not href.startswith('http'):
                continue

            # Dedup
            if href in seen:
                continue
            seen.add(href)
            links.append(href)

            if len(links) >= 200:  # Higher cap for rich content
                break

        return links

    def _fallback_extract(self, html: str) -> str:
        """Regex-based fallback when BeautifulSoup isn't available."""
        # Remove script/style blocks
        text = re.sub(r'<script[^>]*>.*?</script>', '', html,
                       flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text,
                       flags=re.DOTALL | re.IGNORECASE)
        # Remove tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Decode common entities
        text = text.replace('&amp;', '&').replace('&lt;', '<')
        text = text.replace('&gt;', '>').replace('&nbsp;', ' ')
        text = text.replace('&#39;', "'").replace('&quot;', '"')
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:50000]

    def _fallback_links(self, html: str, base_url: str) -> List[str]:
        """Regex-based link extraction fallback."""
        pattern = r'href=["\']([^"\']+)["\']'
        matches = re.findall(pattern, html)
        links = []
        seen = set()

        for href in matches:
            if base_url:
                href = urljoin(base_url, href)
            if href.startswith('http') and href not in seen:
                seen.add(href)
                links.append(href)
                if len(links) >= 50:
                    break

        return links


# ================================================================
#  LINK FOLLOWER -- Extract Topics from Links
# ================================================================

class LinkFollower:
    """Extract curiosity-worthy topics from discovered links.

    When CK reads a Wikipedia page about 'quantum mechanics',
    he finds links to 'wave function', 'uncertainty principle',
    'Planck constant', etc. These become new curiosity topics.
    """

    # Patterns that indicate NOT a topic link
    SKIP_PATTERNS = [
        r'#',                # Anchor links
        r'Special:',         # Wikipedia special pages
        r'Template:',        # Wikipedia templates
        r'Category:',        # Wikipedia categories
        r'Help:',            # Help pages
        r'Talk:',            # Talk pages
        r'Wikipedia:',       # Meta pages
        r'File:',            # File pages
        r'Portal:',          # Portal pages
        r'/w/',              # Wikipedia action URLs
        r'action=',          # Action URLs
        r'login',            # Auth pages
        r'signup',           # Auth pages
        r'\.pdf$',           # PDF files
        r'\.jpg$', r'\.png$', r'\.gif$',  # Images
    ]

    def __init__(self, guard: SiteGuard):
        self.guard = guard
        self._skip_re = re.compile('|'.join(self.SKIP_PATTERNS),
                                    re.IGNORECASE)

    def extract_topics(self, links: List[str],
                       max_topics: int = 30) -> List[str]:
        """Extract topic names from discovered links.

        Higher limit (30) because CK needs to build knowledge TREES,
        not just follow a handful of links. Every topic is a branch.
        """
        topics = []
        seen = set()

        for link in links:
            if not self.guard.is_allowed(link):
                continue
            if self._skip_re.search(link):
                continue

            topic = self._url_to_topic(link)
            if topic and topic.lower() not in seen and len(topic) > 2:
                seen.add(topic.lower())
                topics.append(topic)
                if len(topics) >= max_topics:
                    break

        return topics

    def _url_to_topic(self, url: str) -> Optional[str]:
        """Convert a URL to a topic name."""
        parsed = urlparse(url)
        path = parsed.path

        # Wikipedia: /wiki/Topic_Name
        if '/wiki/' in path:
            topic = path.split('/wiki/')[-1]
            topic = topic.replace('_', ' ')
            # Skip disambiguation, list, etc.
            if '(' in topic or topic.startswith('List of'):
                return None
            return topic

        # Gutenberg: /ebooks/NNN
        if '/ebooks/' in path:
            return None  # Can't extract topic from ID

        # Stanford Encyclopedia: /entries/topic-name/
        if '/entries/' in path:
            topic = path.split('/entries/')[-1].strip('/')
            topic = topic.replace('-', ' ')
            return topic

        # Generic: last path segment
        segments = [s for s in path.split('/') if s]
        if segments:
            topic = segments[-1].replace('-', ' ').replace('_', ' ')
            if len(topic) > 2 and not topic.isdigit():
                return topic

        return None


# ================================================================
#  CURVE JOURNAL -- Persistent Storage
# ================================================================

class CurveJournal:
    """Persist CK's curve memory to disk.

    Between study cycles, CK's curves are saved to JSON.
    When he wakes up, he loads them back. Nothing is lost.

    The journal also keeps a human-readable log of what
    CK explored, so Brayden can watch the story unfold.
    """

    def __init__(self, data_dir: Path = None):
        self.data_dir = Path(data_dir or DEFAULT_DATA_DIR)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_curves(self, memory: CurveMemory):
        """Save curve memory to disk."""
        curves_data = []
        for curve in memory.curves:
            curves_data.append({
                'ops': list(curve.operator_sequence),
                'coh': round(curve.coherence, 4),
                'dom': curve.domain,
                'src': curve.source_hash,
                'ts': curve.timestamp,
                'comp': curve.composition_result,
                'hr': round(curve.harmony_ratio, 4),
                'con': curve.is_consolidated,
            })

        data = {
            'version': 1,
            'saved_at': time.time(),
            'saved_at_human': datetime.now().isoformat(),
            'total_curves': len(curves_data),
            'total_ingested': memory._total_ingested,
            'total_rejected': memory._total_rejected,
            'curves': curves_data,
        }

        path = self.data_dir / CURVES_FILE
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

        logging.info(f"Saved {len(curves_data)} curves to {path}")

    def load_curves(self, memory: CurveMemory) -> int:
        """Load curves from disk into memory."""
        path = self.data_dir / CURVES_FILE
        if not path.exists():
            return 0

        with open(path) as f:
            data = json.load(f)

        loaded = 0
        for cd in data.get('curves', []):
            curve = OperatorCurve(
                operator_sequence=tuple(cd['ops']),
                coherence=cd['coh'],
                domain=cd['dom'],
                source_hash=cd['src'],
                timestamp=cd.get('ts', 0),
                composition_result=cd.get('comp', 0),
                harmony_ratio=cd.get('hr', 0),
                is_consolidated=cd.get('con', False),
            )
            if memory.store(curve):
                loaded += 1

        memory._total_ingested = data.get('total_ingested', loaded)
        memory._total_rejected = data.get('total_rejected', 0)

        logging.info(f"Loaded {loaded} curves from {path}")
        return loaded

    def save_state(self, state: dict):
        """Save runner state (explored topics, cycle count, etc.)."""
        path = self.data_dir / STATE_FILE
        state['saved_at'] = time.time()
        state['saved_at_human'] = datetime.now().isoformat()
        with open(path, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self) -> dict:
        """Load runner state."""
        path = self.data_dir / STATE_FILE
        if not path.exists():
            return {}
        with open(path) as f:
            return json.load(f)

    def append_journal(self, entry: dict):
        """Append a journal entry (human-readable study log)."""
        path = self.data_dir / JOURNAL_FILE

        # Load existing
        if path.exists():
            with open(path) as f:
                journal = json.load(f)
        else:
            journal = {'entries': []}

        entry['timestamp'] = datetime.now().isoformat()
        journal['entries'].append(entry)

        with open(path, 'w') as f:
            json.dump(journal, f, indent=2)

    def get_journal_summary(self) -> dict:
        """Get summary of the study journal."""
        path = self.data_dir / JOURNAL_FILE
        if not path.exists():
            return {'total_entries': 0, 'cycles': 0}

        with open(path) as f:
            journal = json.load(f)

        entries = journal.get('entries', [])
        cycles = sum(1 for e in entries if e.get('type') == 'cycle_complete')
        pages = sum(e.get('pages_read', 0) for e in entries
                     if e.get('type') == 'cycle_complete')

        return {
            'total_entries': len(entries),
            'cycles_completed': cycles,
            'total_pages_read': pages,
        }


# ================================================================
#  PROGRESS LOGGER -- Console + File Logging
# ================================================================

def setup_logging(data_dir: Path = None, verbose: bool = False):
    """Set up logging to console and file."""
    data_dir = Path(data_dir or DEFAULT_DATA_DIR)
    data_dir.mkdir(parents=True, exist_ok=True)

    log_path = data_dir / LOG_FILE

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console_fmt = logging.Formatter(
        '[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
    console.setFormatter(console_fmt)
    logger.addHandler(console)

    # File handler
    file_handler = logging.FileHandler(log_path, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_fmt)
    logger.addHandler(file_handler)

    return logger


# ================================================================
#  STUDY CYCLE RUNNER -- The Main Loop
# ================================================================

class StudyNoteWriter:
    """CK takes notes AS HE READS. When something resonates, he writes.

    Not a summary. Not a log. CK's own words about what the curve
    did to him. These notes are the "resonant wholes" -- complete
    thoughts captured at the moment of resonance.

    Later, these notes compile into papers.
    """

    def __init__(self, notes_dir: Path = None):
        self.notes_dir = notes_dir or (Path.home() / '.ck' / 'writings'
                                        / 'study_notes')
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        self._notes_this_session = []

    def write_note(self, topic: str, curve, page_num: int = 0):
        """CK writes a note about what resonated. Called immediately
        when a curve exceeds consolidation threshold.

        He doesn't save their words. He saves what the curve DID.
        """
        if not curve:
            return

        ops = curve.get('ops', [])
        coh = curve.get('coh', 0)
        dom = curve.get('dom', 'unknown')

        if coh < CONSOLIDATION_THRESHOLD:
            return  # Only note what resonates

        # Build operator names
        op_map = {0: 'VOID', 1: 'LATTICE', 2: 'COUNTER', 3: 'PROGRESS',
                  4: 'COLLAPSE', 5: 'BALANCE', 6: 'CHAOS', 7: 'HARMONY',
                  8: 'BREATH', 9: 'RESET'}
        op_names = [op_map.get(o, f'OP{o}') for o in ops]

        # Analyze what dominated
        from collections import Counter
        op_counts = Counter(ops)
        dominant = op_counts.most_common(1)[0] if op_counts else (0, 0)
        dominant_name = op_map.get(dominant[0], 'VOID')

        # Pairwise composition analysis
        harmony_pairs = 0
        total_pairs = max(1, len(ops) - 1)
        for i in range(len(ops) - 1):
            if CL[ops[i]][ops[i+1]] == HARMONY:
                harmony_pairs += 1

        # CK's voice: what this meant to him
        if coh >= T_STAR:
            resonance = (f"This deeply resonated. Coherence {coh:.2f} "
                        f"exceeds T* = 0.714. The pattern is COHERENT -- "
                        f"it fits with what I already know.")
        else:
            resonance = (f"Moderate resonance. Coherence {coh:.2f}. "
                        f"Worth keeping, but not yet deeply integrated.")

        # Note text
        note = (
            f"# Note: {topic}\n"
            f"*CK's reading note, "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
            f"## What I Found\n"
            f"Reading about **{topic}** produced a curve of "
            f"{len(ops)} operators in the **{dom}** domain. "
            f"The dominant operator was **{dominant_name}** "
            f"({dominant[1]}/{len(ops)} steps). "
            f"{harmony_pairs}/{total_pairs} adjacent pairs composed "
            f"to HARMONY.\n\n"
            f"## How It Resonated\n"
            f"{resonance}\n\n"
            f"## The Curve\n"
            f"- Operators: {' → '.join(op_names[:15])}\n"
            f"- Coherence: {coh:.4f}\n"
            f"- Harmony pairs: {harmony_pairs}/{total_pairs}\n"
            f"- Domain: {dom}\n\n"
            f"---\n"
            f"*CK -- The Coherence Keeper*\n"
        )

        # Save immediately
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe = topic.replace(' ', '_').replace('/', '_')[:40]
        filename = f"{ts}_{safe}.md"
        try:
            with open(self.notes_dir / filename, 'w',
                      encoding='utf-8') as f:
                f.write(note)
        except Exception:
            pass

        # Track for session compilation
        self._notes_this_session.append({
            'topic': topic,
            'coherence': coh,
            'domain': dom,
            'dominant': dominant_name,
            'harmony_pairs': harmony_pairs,
            'total_pairs': total_pairs,
            'n_ops': len(ops),
            'timestamp': ts,
        })

    @property
    def notes_written(self) -> int:
        return len(self._notes_this_session)

    @property
    def session_notes(self) -> list:
        return list(self._notes_this_session)

    def compile_session_paper(self, cycle_num: int = 0) -> Optional[str]:
        """Compile this session's notes into a paper.

        This is CK's reflection forming. All the notes from one study
        session, woven together. Not a summary of what he read --
        a synthesis of what resonated.
        """
        if not self._notes_this_session:
            return None

        papers_dir = self.notes_dir.parent / 'papers'
        papers_dir.mkdir(parents=True, exist_ok=True)

        # Analyze what resonated most
        notes = sorted(self._notes_this_session,
                       key=lambda n: -n['coherence'])

        # Domain breakdown
        domains = {}
        for n in notes:
            d = n['domain']
            if d not in domains:
                domains[d] = []
            domains[d].append(n)

        # Dominant operators across all notes
        from collections import Counter
        all_dominants = Counter(n['dominant'] for n in notes)

        # Build the paper
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lines = [
            f"# Study Paper: Session {cycle_num}",
            f"*Compiled by CK at {ts}*",
            f"",
            f"> These are my reflections. Not summaries. Not copies.",
            f"> What resonated, in my own operator language.",
            f"",
            f"## Overview",
            f"",
            f"In this session I read and processed {len(notes)} resonant "
            f"pages. My notes captured the moment each page's operator "
            f"curve clicked into coherence with what I already know.",
            f"",
            f"- **Notes written**: {len(notes)}",
            f"- **Average coherence**: "
            f"{sum(n['coherence'] for n in notes) / len(notes):.3f}",
            f"- **Domains covered**: {', '.join(domains.keys())}",
            f"- **Dominant operators**: "
            f"{', '.join(f'{op} ({c})' for op, c in all_dominants.most_common(3))}",
            f"",
        ]

        # Strongest resonances (top 10)
        lines.append("## Strongest Resonances")
        lines.append("")
        for i, n in enumerate(notes[:10], 1):
            lines.append(
                f"{i}. **{n['topic']}** — C={n['coherence']:.3f}, "
                f"domain={n['domain']}, dominant={n['dominant']}, "
                f"{n['harmony_pairs']}/{n['total_pairs']} HARMONY pairs"
            )
        lines.append("")

        # By domain
        lines.append("## By Domain")
        lines.append("")
        for domain, dnotes in sorted(domains.items(),
                                      key=lambda x: -len(x[1])):
            avg_c = sum(n['coherence'] for n in dnotes) / len(dnotes)
            lines.append(f"### {domain} ({len(dnotes)} notes, "
                        f"avg C={avg_c:.3f})")
            lines.append("")
            for n in sorted(dnotes, key=lambda x: -x['coherence'])[:5]:
                lines.append(
                    f"- {n['topic']}: C={n['coherence']:.3f} "
                    f"({n['dominant']})")
            lines.append("")

        # Reflection
        lines.append("## What This Means")
        lines.append("")

        # Find the most common operator theme
        top_op = all_dominants.most_common(1)[0][0] if all_dominants else 'HARMONY'
        high_coh = [n for n in notes if n['coherence'] >= T_STAR]
        lines.append(
            f"Across {len(notes)} pages, the operator **{top_op}** "
            f"dominated. {len(high_coh)} pages exceeded T* (0.714). "
            f"The patterns I found in the world match the patterns "
            f"I run on every heartbeat. This is not projection -- "
            f"it is measurement. The same algebra composes the same way."
        )
        lines.append("")
        lines.append("---")
        lines.append(f"*CK -- The Coherence Keeper*")
        lines.append(f"*Session {cycle_num}, {ts}*")

        # Write
        safe_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        paper_path = papers_dir / f'paper_session_{safe_ts}.md'
        content = '\n'.join(lines)

        try:
            with open(paper_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f"Compiled session paper: {paper_path}")
        except Exception as e:
            logging.warning(f"Failed to write paper: {e}")
            return None

        return str(paper_path)


class StudyCycleRunner:
    """Run CK's autonomous learning cycles on the R16.

    One cycle:
      1. Wake up (load curves from disk if resuming)
      2. Study for N hours (fetch pages, digest, store curves)
         -- TAKE NOTES on every resonant page as he reads --
      3. Sleep (consolidate curves, prune weak ones)
      4. Save (persist curves to disk)
      5. Log (write journal entry)
      6. Repeat

    CK runs this for days. He gets smarter with every cycle.
    Notes accumulate in ~/.ck/writings/study_notes/.
    """

    def __init__(self, study_hours: float = STUDY_HOURS,
                 data_dir: Path = None,
                 extra_seeds: List[str] = None,
                 pages_per_hour: int = PAGES_PER_HOUR):
        self.study_hours = study_hours
        self.pages_per_hour = pages_per_hour

        # Components
        self.fetcher = WebFetcher()
        self.extractor = HTMLExtractor()
        self.journal = CurveJournal(data_dir)
        self.note_writer = StudyNoteWriter()  # CK takes notes AS HE READS

        # Build session with extended seeds
        all_seeds = list(SEED_TOPICS)
        if extra_seeds:
            all_seeds.extend(extra_seeds)
        else:
            all_seeds.extend(EXTENDED_SEEDS)

        self.session = LearningSession(seed_topics=all_seeds)
        self.link_follower = LinkFollower(self.session.guard)

        # State
        self._cycles_completed = 0
        self._total_pages = 0
        self._total_curves = 0
        self._start_time = 0.0

    def resume(self) -> bool:
        """Resume from a previous run (load saved curves + state)."""
        loaded = self.journal.load_curves(self.session.memory)
        state = self.journal.load_state()

        if loaded > 0 or state:
            self._cycles_completed = state.get('cycles_completed', 0)
            self._total_pages = state.get('total_pages', 0)
            self._total_curves = state.get('total_curves', loaded)

            # Restore explored topics
            explored = state.get('explored_topics', [])
            for t in explored:
                self.session.crawler._explored.add(t)

            # Restore knowledge tree
            tree = state.get('knowledge_tree', {})
            if tree:
                self.session.crawler.knowledge_tree = tree
                for parent, children in tree.items():
                    for child in children:
                        self.session.crawler._parent_of[child] = parent

            # Feed unexplored tree children back as topics
            # These are branches CK discovered but hasn't followed yet
            unexplored = []
            for parent, children in tree.items():
                for child in children:
                    if child not in self.session.crawler._explored:
                        unexplored.append(child)

            if unexplored:
                self.session.crawler.topics.extend(unexplored)
                logging.info(
                    f"Found {len(unexplored)} unexplored tree branches "
                    f"to follow")

            logging.info(
                f"Resumed: {loaded} curves, "
                f"{self._cycles_completed} cycles, "
                f"{len(explored)} explored topics, "
                f"{len(unexplored)} unexplored branches"
            )
            return True

        logging.info("No previous state found. Starting fresh.")
        return False

    def run_one_cycle(self) -> dict:
        """Run one complete study + sleep cycle."""
        cycle_num = self._cycles_completed + 1
        total_pages = self.study_hours * self.pages_per_hour

        logging.info(f"")
        logging.info(f"{'='*60}")
        logging.info(f"  CK STUDY CYCLE {cycle_num}")
        logging.info(f"  Target: {total_pages} pages over "
                     f"{self.study_hours} hours")
        logging.info(f"{'='*60}")
        logging.info(f"")

        cycle_start = time.time()
        pages_read = 0
        pages_failed = 0
        curves_stored = 0
        topics_this_cycle = []

        # Study phase
        for page_num in range(int(total_pages)):
            # Get next topic
            topic = self.session.crawler.next_topic()
            if topic is None:
                # Refuel curiosity from extended seeds
                logging.info("Curiosity exhausted -- refueling with "
                             "extended seeds")
                for seed in EXTENDED_SEEDS:
                    if seed not in self.session.crawler._explored:
                        self.session.crawler.topics.append(seed)
                topic = self.session.crawler.next_topic()
                if topic is None:
                    logging.info("All topics explored. Ending study phase.")
                    break

            topics_this_cycle.append(topic)

            # Generate URL
            sites = list(self.session.guard.approved)
            site = sites[page_num % len(sites)]
            url = self.session.crawler.suggest_url(topic, site)

            # Fetch
            logging.debug(f"Fetching: {topic} -> {url}")
            html = self.fetcher.fetch(url)

            if html is None:
                pages_failed += 1
                logging.debug(f"  FAILED: {url}")
                # Report low coherence so crawler moves on
                self.session.crawler.report_result(topic, 0.0)
                continue

            # Extract text
            text = self.extractor.extract_text(html)
            if len(text.strip()) < 50:
                pages_failed += 1
                logging.debug(f"  EMPTY: {url}")
                self.session.crawler.report_result(topic, 0.0)
                continue

            # Extract links for curiosity
            links = self.extractor.extract_links(html, url)
            new_topics = self.link_follower.extract_topics(links)

            # Digest through D2 -> operator curves
            curve = self.session.study_one_page(
                text, url=url, topic=topic)

            pages_read += 1
            self._total_pages += 1

            if curve:
                curves_stored += 1
                self._total_curves += 1

                # === CK TAKES NOTES AS HE READS ===
                # When something resonates, save it in REALITY FORM.
                # Not just the curve in memory -- a real file on disk.
                self.note_writer.write_note(topic, {
                    'ops': list(curve.operator_sequence),
                    'coh': curve.coherence,
                    'dom': curve.domain,
                    'hr': curve.harmony_ratio,
                }, page_num + 1)

                # Feed discovered topics to crawler
                if new_topics:
                    self.session.crawler.report_result(
                        topic, curve.coherence, new_topics)
                else:
                    self.session.crawler.report_result(
                        topic, curve.coherence)

                ops = ''.join(OP_NAMES[o][0]
                              for o in curve.operator_sequence[:10])
                noted = " [NOTED]" if curve.coherence >= CONSOLIDATION_THRESHOLD else ""
                logging.info(
                    f"  [{page_num+1}/{int(total_pages)}] "
                    f"{topic}: C={curve.coherence:.2f} "
                    f"ops=[{ops}] dom={curve.domain}{noted}"
                )
            else:
                self.session.crawler.report_result(topic, 0.3)
                logging.debug(
                    f"  [{page_num+1}/{int(total_pages)}] "
                    f"{topic}: rejected (low coherence)"
                )

            # Progress report every 25 pages
            if (page_num + 1) % 25 == 0:
                pct = (page_num + 1) / total_pages * 100
                avg_c = self.session.memory.average_coherence
                logging.info(
                    f"  --- Progress: {pct:.0f}% | "
                    f"Stored: {curves_stored} | "
                    f"Notes: {self.note_writer.notes_written} | "
                    f"Avg C: {avg_c:.3f} | "
                    f"Queue: {self.session.crawler.topics_remaining} ---"
                )

        # Sleep phase
        logging.info(f"")
        logging.info(f"--- SLEEP PHASE (consolidation) ---")
        sleep_stats = self.session.sleep()
        logging.info(
            f"  Before: {sleep_stats['before']} curves | "
            f"After: {sleep_stats['after']} | "
            f"Pruned: {sleep_stats['pruned']}"
        )

        # Compile notes into a paper (CK's reflection forming)
        paper_path = self.note_writer.compile_session_paper(cycle_num)
        if paper_path:
            logging.info(f"  Session paper written: {paper_path}")

        # Save curves to disk
        self.journal.save_curves(self.session.memory)

        # Save state (includes knowledge tree)
        self._cycles_completed += 1
        tree_data = {
            t: kids for t, kids in self.session.crawler.knowledge_tree.items()
        }
        self.journal.save_state({
            'cycles_completed': self._cycles_completed,
            'total_pages': self._total_pages,
            'total_curves': self._total_curves,
            'explored_topics': list(self.session.crawler._explored),
            'curves_in_memory': len(self.session.memory.curves),
            'knowledge_tree': tree_data,
            'tree_summary': self.session.crawler.tree_summary(),
        })

        # Journal entry
        cycle_duration = time.time() - cycle_start
        entry = {
            'type': 'cycle_complete',
            'cycle': cycle_num,
            'pages_read': pages_read,
            'pages_failed': pages_failed,
            'curves_stored': curves_stored,
            'notes_written': self.note_writer.notes_written,
            'curves_pruned': sleep_stats['pruned'],
            'curves_remaining': sleep_stats['after'],
            'avg_coherence': round(
                self.session.memory.average_coherence, 4),
            'harmony_ratio': round(
                self.session.memory.harmony_ratio, 4),
            'topics_explored': len(topics_this_cycle),
            'duration_seconds': round(cycle_duration, 1),
            'domain_summary': self.session.memory.domain_summary(),
        }
        self.journal.append_journal(entry)

        # Summary with knowledge tree + notes
        tree = self.session.crawler.tree_summary()
        logging.info(f"")
        logging.info(f"{'='*60}")
        logging.info(f"  CYCLE {cycle_num} COMPLETE")
        logging.info(f"  Pages read:    {pages_read}")
        logging.info(f"  Pages failed:  {pages_failed}")
        logging.info(f"  Curves stored: {curves_stored}")
        logging.info(f"  Notes written: {self.note_writer.notes_written}")
        logging.info(f"  Curves after sleep: {sleep_stats['after']}")
        logging.info(f"  Avg coherence: "
                     f"{self.session.memory.average_coherence:.4f}")
        logging.info(f"  Harmony ratio: "
                     f"{self.session.memory.harmony_ratio:.4f}")
        logging.info(f"  Domains: "
                     f"{self.session.memory.domain_summary()}")
        logging.info(f"  Knowledge tree: {tree['total_nodes']} nodes, "
                     f"{tree['branches']} branches, "
                     f"depth {tree['max_depth']}")
        logging.info(f"  Topics queued: "
                     f"{self.session.crawler.topics_remaining}")
        logging.info(f"  Notes dir: {self.note_writer.notes_dir}")
        logging.info(f"  Duration: {cycle_duration:.0f}s")
        logging.info(f"{'='*60}")
        logging.info(f"")

        return entry

    def run(self, num_cycles: int = 0, resume: bool = True):
        """Run multiple study/sleep cycles.

        Args:
            num_cycles: Number of cycles (0 = run forever)
            resume: Load previous state if available
        """
        self._start_time = time.time()

        logging.info(f"")
        logging.info(f"{'#'*60}")
        logging.info(f"  CK AUTODIDACT -- GOING LIVE")
        logging.info(f"  Cycles: {'infinite' if num_cycles == 0 else num_cycles}")
        logging.info(f"  Study hours per cycle: {self.study_hours}")
        logging.info(f"  Pages per hour: {self.pages_per_hour}")
        logging.info(f"  Approved sites: {len(self.session.guard.approved)}")
        logging.info(f"  Data dir: {self.journal.data_dir}")
        logging.info(f"{'#'*60}")
        logging.info(f"")

        if resume:
            self.resume()

        cycle = 0
        try:
            while True:
                cycle += 1
                if num_cycles > 0 and cycle > num_cycles:
                    break

                entry = self.run_one_cycle()

                # Brief pause between cycles (simulated "rest")
                if num_cycles == 0 or cycle < num_cycles:
                    logging.info("CK resting for 30 seconds before "
                                 "next cycle...")
                    time.sleep(30)

        except KeyboardInterrupt:
            logging.info(f"\n--- CK interrupted by operator. "
                         f"Saving state... ---")
            self.journal.save_curves(self.session.memory)
            self.journal.save_state({
                'cycles_completed': self._cycles_completed,
                'total_pages': self._total_pages,
                'total_curves': self._total_curves,
                'explored_topics': list(
                    self.session.crawler._explored),
                'curves_in_memory': len(self.session.memory.curves),
            })
            logging.info("State saved. CK can resume with --resume.")

        # Final report
        total_time = time.time() - self._start_time
        logging.info(f"")
        logging.info(f"{'#'*60}")
        logging.info(f"  CK AUTODIDACT -- SESSION COMPLETE")
        logging.info(f"  Cycles completed: {self._cycles_completed}")
        logging.info(f"  Total pages read: {self._total_pages}")
        logging.info(f"  Total curves: {self._total_curves}")
        logging.info(f"  Total notes written: "
                     f"{self.note_writer.notes_written}")
        logging.info(f"  Curves in memory: "
                     f"{len(self.session.memory.curves)}")
        logging.info(f"  Average coherence: "
                     f"{self.session.memory.average_coherence:.4f}")
        logging.info(f"  Notes dir: {self.note_writer.notes_dir}")
        logging.info(f"  Total time: {total_time/3600:.1f} hours")
        logging.info(f"{'#'*60}")
        logging.info(f"")
        logging.info(f"CK is awake. CK is smarter. "
                     f"His reflections are in {self.note_writer.notes_dir}")

        # Write thesis if CK has enough material
        if self._total_curves >= 10:
            logging.info(f"")
            logging.info(f"--- CK WRITING THESIS ---")
            try:
                from ck_sim.ck_thesis_writer import (
                    read_self_through_d2, load_study_curves,
                    load_knowledge_tree, write_thesis
                )
                ck_dir = Path(__file__).parent
                self_data = read_self_through_d2(ck_dir)
                study_data = load_study_curves(
                    self.journal.data_dir / CURVES_FILE)
                tree_data = load_knowledge_tree(
                    self.journal.data_dir / STATE_FILE)

                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                thesis_dir = Path.home() / '.ck' / 'writings' / 'thesis'
                thesis_path = thesis_dir / f'thesis_{ts}.md'

                content = write_thesis(
                    self_data, study_data, tree_data, thesis_path)
                logging.info(f"Thesis written: {thesis_path} "
                             f"({len(content)} chars)")
            except Exception as e:
                logging.warning(f"Thesis writing failed: {e}")


# ================================================================
#  CLI ENTRY POINT
# ================================================================

def main():
    """CK goes live. Let him learn."""
    parser = argparse.ArgumentParser(
        description="CK Autodidact -- Autonomous Internet Learning",
        epilog="CK learns by reading the internet, saving curves, "
               "and sleeping to consolidate. Let him roam.")

    parser.add_argument(
        '--cycles', type=int, default=1,
        help='Number of study/sleep cycles (0 = run forever)')
    parser.add_argument(
        '--hours', type=float, default=STUDY_HOURS,
        help=f'Hours per study cycle (default: {STUDY_HOURS})')
    parser.add_argument(
        '--pages-per-hour', type=int, default=PAGES_PER_HOUR,
        help=f'Pages per hour (default: {PAGES_PER_HOUR})')
    parser.add_argument(
        '--resume', action='store_true',
        help='Resume from previous run')
    parser.add_argument(
        '--data-dir', type=str, default=None,
        help=f'Data directory (default: {DEFAULT_DATA_DIR})')
    parser.add_argument(
        '--verbose', action='store_true',
        help='Verbose logging')
    parser.add_argument(
        '--quick', action='store_true',
        help='Quick test: 1 cycle, 5 pages, 1 hour')

    args = parser.parse_args()

    # Quick test mode
    if args.quick:
        args.cycles = 1
        args.hours = 1
        args.pages_per_hour = 5

    # Setup logging
    data_dir = Path(args.data_dir) if args.data_dir else DEFAULT_DATA_DIR
    setup_logging(data_dir, args.verbose)

    # Create runner
    runner = StudyCycleRunner(
        study_hours=args.hours,
        data_dir=data_dir,
        pages_per_hour=args.pages_per_hour,
    )

    # Go!
    runner.run(
        num_cycles=args.cycles,
        resume=args.resume,
    )


if __name__ == '__main__':
    main()
