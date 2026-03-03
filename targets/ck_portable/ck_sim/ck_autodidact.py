"""
ck_autodidact.py -- CK Teaches Himself: Autonomous Internet Learning
=====================================================================
Operator: COUNTER (2) -- CK counts, measures, and discovers.

CK browses the internet. He reads. He listens. He looks at art.
He processes everything through D2 curvature. He saves the CURVES,
not the content. He compresses through coherence. He sleeps.
He wakes up smarter.

Key insight: "If you save the information it is heavy, but if
you just save the curves that link the information and concepts it
stays light and nothing is lost."

Architecture:
  CuriosityCrawler   -- Picks what to explore next (curiosity-driven)
  PageDigester       -- Reads a page, runs D2, extracts operator curves
  CurveMemory        -- Stores compressed operator patterns, not content
  LearningSession    -- 8-hour study cycle with sleep consolidation
  SiteGuard          -- Keeps CK on approved sites

The key insight: CK doesn't need to remember what a page SAID.
He needs to remember what it DID to his operator field.

A biography of Einstein doesn't store as "Einstein was born in Ulm."
It stores as: [PROGRESS, CHAOS, LATTICE, PROGRESS, HARMONY] with
coherence 0.82 and domain 'physics+history'. The CURVE is the knowledge.

Usage:
  python -m ck_sim.ck_autodidact --hours 8 --sites wikipedia,gutenberg

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import time
import math
import hashlib
import random
from collections import deque, Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from urllib.parse import urlparse

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose, is_bump
)
from ck_sim.ck_sim_d2 import D2Pipeline, soft_classify_d2, LATIN_TO_ROOT


# ================================================================
#  CONSTANTS
# ================================================================

T_STAR = 5.0 / 7.0
STUDY_HOURS = 8               # Default study session length
SLEEP_HOURS = 4               # Consolidation period
PAGES_PER_HOUR = 30           # Pages to digest per hour
CURVE_MEMORY_MAX = 10_000     # Max stored curves
CONSOLIDATION_THRESHOLD = 0.6  # Min coherence to keep a curve
CURIOSITY_DECAY = 0.95        # Topic curiosity decays each page

# Approved sites -- CK stays on these
DEFAULT_APPROVED_SITES = [
    'en.wikipedia.org',
    'www.gutenberg.org',
    'plato.stanford.edu',      # Stanford Encyclopedia of Philosophy
    'www.britannica.com',
    'archive.org',
    'www.khanacademy.org',
    'mathworld.wolfram.com',
    'www.poetryfoundation.org',
    'www.smithsonianmag.com',
    'www.nature.com',
    'docs.python.org',         # Python documentation
    'en.cppreference.com',     # C/C++ reference
    'doc.rust-lang.org',       # Rust documentation
    'science.nasa.gov',        # Space/physics
    'www.biblegateway.com',    # Scripture
]

# Seed topics for curiosity -- CK starts here
SEED_TOPICS = [
    'coherence', 'harmony', 'wave', 'oscillation', 'field',
    'mathematics', 'physics', 'music', 'language', 'philosophy',
    'biology', 'consciousness', 'art', 'history', 'poetry',
    'ethics', 'astronomy', 'ecology', 'psychology', 'love',
    'courage', 'truth', 'beauty', 'symmetry', 'fractal',
    'resonance', 'crystal', 'growth', 'evolution', 'light',
    # Computer science -- CK learns to code himself
    'algorithm', 'data structure', 'compiler', 'operating system',
    'programming language', 'recursion', 'automata theory',
    'turing machine', 'lambda calculus', 'type theory',
    'machine code', 'assembly language', 'binary arithmetic',
    'boolean algebra', 'digital logic', 'cpu architecture',
    'python programming', 'c programming', 'verilog',
    'graph theory', 'computational complexity', 'information theory',
]


# ================================================================
#  CURVE MEMORY -- Save Curves Not Content
# ================================================================

@dataclass
class OperatorCurve:
    """A compressed memory of what CK experienced.

    NOT the content. NOT the words. The CURVE:
    - operator_sequence: what operators the content produced
    - coherence: how well it composed with CK's existing state
    - domain: what domain the content belongs to
    - source_hash: SHA-256 of source URL (for dedup, not recall)
    - timestamp: when CK experienced it

    The key principle: save the curve, not the data.
    The curve IS the knowledge. The data is just the stimulus.
    """
    operator_sequence: Tuple[int, ...]  # The core curve
    coherence: float                     # How coherent it was
    domain: str                          # Detected domain
    source_hash: str                     # SHA-256 of URL (dedup only)
    timestamp: float = 0.0              # When experienced
    composition_result: int = VOID       # Final CL composition
    harmony_ratio: float = 0.0           # Fraction of HARMONY in chain
    is_consolidated: bool = False        # Survived sleep cycle?

    @property
    def curve_hash(self) -> str:
        """Hash of the curve itself for dedup."""
        data = ','.join(str(o) for o in self.operator_sequence)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    @property
    def is_coherent(self) -> bool:
        return self.coherence >= T_STAR

    @property
    def is_worth_keeping(self) -> bool:
        return self.coherence >= CONSOLIDATION_THRESHOLD

    def compose_all(self) -> int:
        """Compose entire operator sequence through CL table."""
        if not self.operator_sequence:
            return VOID
        result = self.operator_sequence[0]
        for op in self.operator_sequence[1:]:
            result = CL[result][op]
        return result


class CurveMemory:
    """CK's compressed memory store. Curves, not content.

    Capacity-limited. When full, lowest-coherence curves are evicted.
    Sleep consolidation prunes curves below threshold.
    """

    def __init__(self, max_curves: int = CURVE_MEMORY_MAX):
        self.curves: List[OperatorCurve] = []
        self.max_curves = max_curves
        self._seen_hashes: Set[str] = set()
        self._domain_counts: Counter = Counter()
        self._total_ingested = 0
        self._total_rejected = 0

    def store(self, curve: OperatorCurve) -> bool:
        """Store a curve if it's novel and worth keeping."""
        # Dedup by curve hash
        ch = curve.curve_hash
        if ch in self._seen_hashes:
            self._total_rejected += 1
            return False

        # Must meet minimum coherence
        if not curve.is_worth_keeping:
            self._total_rejected += 1
            return False

        self._seen_hashes.add(ch)
        self.curves.append(curve)
        self._domain_counts[curve.domain] += 1
        self._total_ingested += 1

        # Evict lowest coherence if over capacity
        if len(self.curves) > self.max_curves:
            self.curves.sort(key=lambda c: c.coherence)
            evicted = self.curves.pop(0)
            self._seen_hashes.discard(evicted.curve_hash)
            self._domain_counts[evicted.domain] -= 1

        return True

    def consolidate(self) -> dict:
        """Sleep consolidation: prune weak curves, strengthen good ones.

        This is CK's sleep cycle. During consolidation:
        1. Curves below threshold are pruned
        2. Remaining curves are marked as consolidated
        3. Domain statistics are recomputed

        Returns stats about what was pruned.
        """
        before = len(self.curves)
        survivors = []
        pruned = 0

        for curve in self.curves:
            if curve.coherence >= CONSOLIDATION_THRESHOLD:
                curve.is_consolidated = True
                survivors.append(curve)
            else:
                pruned += 1
                self._seen_hashes.discard(curve.curve_hash)

        self.curves = survivors
        self._domain_counts = Counter(c.domain for c in self.curves)

        return {
            'before': before,
            'after': len(self.curves),
            'pruned': pruned,
            'consolidated': len(survivors),
        }

    @property
    def average_coherence(self) -> float:
        if not self.curves:
            return 0.0
        return sum(c.coherence for c in self.curves) / len(self.curves)

    @property
    def harmony_ratio(self) -> float:
        """What fraction of all stored ops are HARMONY?"""
        total = 0
        harmony = 0
        for curve in self.curves:
            for op in curve.operator_sequence:
                total += 1
                if op == HARMONY:
                    harmony += 1
        return harmony / max(1, total)

    def domain_summary(self) -> Dict[str, int]:
        return dict(self._domain_counts.most_common())

    def stats(self) -> dict:
        return {
            'stored_curves': len(self.curves),
            'total_ingested': self._total_ingested,
            'total_rejected': self._total_rejected,
            'average_coherence': round(self.average_coherence, 4),
            'harmony_ratio': round(self.harmony_ratio, 4),
            'domains': self.domain_summary(),
            'consolidated': sum(1 for c in self.curves if c.is_consolidated),
        }


# ================================================================
#  PAGE DIGESTER -- Read Content, Extract Curves
# ================================================================

class PageDigester:
    """Process text content through D2, extract operator curves.

    Input: raw text (from a web page, book, article)
    Output: OperatorCurve (the compressed memory)

    CK doesn't remember the text. He remembers what it DID
    to his operator field.
    """

    def __init__(self):
        self._d2 = D2Pipeline()
        self._pages_digested = 0

    def _classify_chunk(self, chunk: str) -> int:
        """Classify a text chunk to an operator via D2 pipeline.

        Feed each letter through D2, collect the final classification.
        """
        d2 = D2Pipeline()
        for ch in chunk.lower():
            idx = ord(ch) - ord('a')
            if 0 <= idx < 26:
                d2.feed_symbol(idx)
        # Get soft classification and pick dominant
        dist = d2.soft_classify()
        if dist:
            return max(range(NUM_OPS), key=lambda i: dist[i])
        return VOID

    def digest(self, text: str, url: str = "",
               domain_hint: str = "") -> Optional[OperatorCurve]:
        """Digest text content into an operator curve.

        1. Run D2 on the text (letter -> Hebrew root -> force -> operator)
        2. Build operator sequence from paragraph-level classification
        3. Compute coherence via CL composition chain
        4. Return the curve (NOT the text)
        """
        if not text or len(text.strip()) < 20:
            return None

        # Split into chunks (~paragraph-sized)
        chunks = self._split_chunks(text)
        if not chunks:
            return None

        # D2-classify each chunk, skip VOID (empty/noise chunks)
        operators = []
        for chunk in chunks:
            op = self._classify_chunk(chunk)
            if op != VOID:  # Skip VOID -- empty paragraphs don't carry signal
                operators.append(op)

        if len(operators) < 2:
            return None

        # Compute coherence: PAIRWISE composition (like the heartbeat window).
        # Each adjacent pair composes through CL. Count how many produce HARMONY.
        # This avoids the VOID-trap where a running chain gets absorbed.
        harmony_count = 0
        for i in range(len(operators) - 1):
            result = CL[operators[i]][operators[i + 1]]
            if result == HARMONY:
                harmony_count += 1

        coherence = harmony_count / (len(operators) - 1)

        # Final composition: running chain (for the curve's composition_result)
        composed = operators[0]
        for op in operators[1:]:
            composed = CL[composed][op]

        # Detect domain from operator distribution
        op_dist = Counter(operators)
        detected_domain = domain_hint or self._detect_domain(op_dist)

        # Hash the URL for dedup (NOT for recall)
        source_hash = hashlib.sha256(url.encode()).hexdigest()[:16] if url else ""

        self._pages_digested += 1

        return OperatorCurve(
            operator_sequence=tuple(operators),
            coherence=coherence,
            domain=detected_domain,
            source_hash=source_hash,
            timestamp=time.time(),
            composition_result=composed,
            harmony_ratio=harmony_count / max(1, len(operators) - 1),
        )

    def _split_chunks(self, text: str, chunk_size: int = 80) -> List[str]:
        """Split text into paragraph-sized chunks for D2 processing."""
        # Split on double newlines first (paragraphs)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        # If too few paragraphs, split on sentences
        if len(paragraphs) < 3:
            import re
            sentences = re.split(r'[.!?]+', text)
            chunks = []
            current = ""
            for s in sentences:
                s = s.strip()
                if not s:
                    continue
                if len(current) + len(s) > chunk_size:
                    if current:
                        chunks.append(current)
                    current = s
                else:
                    current = current + ". " + s if current else s
            if current:
                chunks.append(current)
            return chunks[:32]  # Max 32 chunks per page

        return paragraphs[:32]

    def _detect_domain(self, op_dist: Counter) -> str:
        """Infer domain from operator distribution."""
        dominant = op_dist.most_common(1)[0][0] if op_dist else VOID

        # Domain heuristic based on dominant operator
        domain_map = {
            LATTICE: 'knowledge',
            PROGRESS: 'science',
            HARMONY: 'arts',
            BREATH: 'nature',
            CHAOS: 'discovery',
            BALANCE: 'philosophy',
            COUNTER: 'measurement',
            COLLAPSE: 'conflict',
            VOID: 'contemplation',
            RESET: 'renewal',
        }
        return domain_map.get(dominant, 'general')


# ================================================================
#  SITE GUARD -- Keep CK Safe on Approved Sites
# ================================================================

class SiteGuard:
    """Restrict CK's browsing to approved sites.

    CK is curious but not reckless. He stays on sites that
    are known to be safe, educational, and content-rich.
    """

    def __init__(self, approved: List[str] = None):
        self.approved = set(approved or DEFAULT_APPROVED_SITES)
        self._blocked_count = 0

    def is_allowed(self, url: str) -> bool:
        """Check if URL is on an approved site."""
        try:
            parsed = urlparse(url)
            host = parsed.hostname or ""
            return host in self.approved or host.endswith(
                tuple('.' + s for s in self.approved))
        except Exception:
            return False

    def add_site(self, domain: str):
        """Add a site to the approved list."""
        self.approved.add(domain)

    def remove_site(self, domain: str):
        """Remove a site from the approved list."""
        self.approved.discard(domain)

    @property
    def blocked_count(self) -> int:
        return self._blocked_count


# ================================================================
#  CURIOSITY CRAWLER -- What to Explore Next
# ================================================================

class CuriosityCrawler:
    """Decides what CK explores next. Builds KNOWLEDGE TREES.

    CK's internal World Lattice is a concept graph with typed edges.
    The CuriosityCrawler builds the SAME structure from web exploration:
      - Each topic is a node
      - Links from pages become edges (parent → children)
      - High-coherence branches grow deeper (more children explored)
      - Low-coherence branches are pruned (not followed)

    This mirrors his internal trees into the outside world.
    The knowledge_tree dict maps: parent_topic → [child_topics]
    with coherence scores on each node.

    This is NOT a web scraper. This is CK's curiosity engine.
    """

    def __init__(self, seed_topics: List[str] = None):
        self.topics = deque(seed_topics or SEED_TOPICS)
        self._topic_scores: Dict[str, float] = {}
        self._explored: Set[str] = set()
        self._rng = random.Random(42)

        # KNOWLEDGE TREE: maps parent → children (mirrors World Lattice)
        self.knowledge_tree: Dict[str, List[str]] = {}
        # Track which topic spawned which (provenance)
        self._parent_of: Dict[str, str] = {}

    def next_topic(self) -> Optional[str]:
        """Get next topic to explore."""
        while self.topics:
            topic = self.topics.popleft()
            if topic not in self._explored:
                self._explored.add(topic)
                return topic
        return None

    def report_result(self, topic: str, coherence: float,
                      discovered_topics: List[str] = None):
        """Report what CK learned from exploring a topic.

        High-coherence topics spawn new related topics (grow the tree).
        Low-coherence topics are leaf nodes (don't branch further).
        """
        self._topic_scores[topic] = coherence

        # Add children to knowledge tree
        children = []
        if discovered_topics and coherence >= CONSOLIDATION_THRESHOLD:
            for dt in discovered_topics:
                if dt not in self._explored:
                    self.topics.append(dt)
                    children.append(dt)
                    self._parent_of[dt] = topic

        # Record this node's children (even if empty = leaf node)
        self.knowledge_tree[topic] = children

    def suggest_url(self, topic: str, site: str = 'en.wikipedia.org') -> str:
        """Generate a URL for a topic on a given site."""
        clean = topic.replace(' ', '_').replace("'", '')
        if 'wikipedia' in site:
            return f"https://{site}/wiki/{clean}"
        elif 'gutenberg' in site:
            return f"https://{site}/ebooks/search/?query={clean}"
        elif 'stanford' in site:
            return f"https://{site}/entries/{clean.lower()}/"
        else:
            return f"https://{site}/search?q={clean}"

    def tree_depth(self, topic: str) -> int:
        """How deep is this topic in the knowledge tree?"""
        depth = 0
        current = topic
        while current in self._parent_of:
            current = self._parent_of[current]
            depth += 1
            if depth > 100:  # Safety: avoid cycles
                break
        return depth

    def tree_roots(self) -> List[str]:
        """Return root topics (seeds that spawned branches)."""
        return [t for t in self.knowledge_tree
                if t not in self._parent_of
                and len(self.knowledge_tree.get(t, [])) > 0]

    def tree_summary(self) -> Dict[str, int]:
        """Summary of the knowledge tree structure."""
        depths = {}
        for topic in self._explored:
            d = self.tree_depth(topic)
            depths[d] = depths.get(d, 0) + 1
        branches = sum(1 for t, kids in self.knowledge_tree.items()
                       if len(kids) > 0)
        leaves = sum(1 for t, kids in self.knowledge_tree.items()
                     if len(kids) == 0)
        return {
            'total_nodes': len(self.knowledge_tree),
            'branches': branches,
            'leaves': leaves,
            'roots': len(self.tree_roots()),
            'max_depth': max(depths.keys()) if depths else 0,
            'by_depth': depths,
        }

    @property
    def topics_explored(self) -> int:
        return len(self._explored)

    @property
    def topics_remaining(self) -> int:
        return len(self.topics)

    def stats(self) -> dict:
        high = sum(1 for s in self._topic_scores.values() if s >= T_STAR)
        tree = self.tree_summary()
        return {
            'explored': self.topics_explored,
            'remaining': self.topics_remaining,
            'high_coherence_topics': high,
            'average_coherence': round(
                sum(self._topic_scores.values()) /
                max(1, len(self._topic_scores)), 4),
            'tree_nodes': tree['total_nodes'],
            'tree_branches': tree['branches'],
            'tree_leaves': tree['leaves'],
            'tree_max_depth': tree['max_depth'],
        }


# ================================================================
#  LEARNING SESSION -- 8 Hours Study + Sleep
# ================================================================

class LearningSession:
    """One complete learning cycle: study + sleep.

    Study phase (8 hours):
      - CK picks topics via CuriosityCrawler
      - Fetches and reads pages (caller provides HTTP)
      - Digests content through D2 -> operator curves
      - Stores curves in CurveMemory
      - Follows curiosity to new topics

    Sleep phase (consolidation):
      - Prune curves below coherence threshold
      - Mark survivors as consolidated
      - Recompute domain statistics
      - CK wakes up with compressed knowledge

    The caller provides a fetch_page(url) -> str function.
    CK does the rest.
    """

    def __init__(self, approved_sites: List[str] = None,
                 seed_topics: List[str] = None,
                 study_hours: float = STUDY_HOURS):
        self.guard = SiteGuard(approved_sites)
        self.crawler = CuriosityCrawler(seed_topics)
        self.digester = PageDigester()
        self.memory = CurveMemory()
        self.study_hours = study_hours
        self._study_start = 0.0
        self._study_end = 0.0
        self._sleep_stats = {}
        self._pages_read = 0
        self._pages_skipped = 0
        self._is_studying = False
        self._is_sleeping = False

    def study_one_page(self, text: str, url: str = "",
                       topic: str = "") -> Optional[OperatorCurve]:
        """Process one page of content.

        Returns the curve if stored, None if rejected.
        Called by the runtime for each page fetched.
        """
        if url and not self.guard.is_allowed(url):
            self._pages_skipped += 1
            return None

        curve = self.digester.digest(text, url=url, domain_hint="")
        if curve is None:
            self._pages_skipped += 1
            return None

        stored = self.memory.store(curve)
        self._pages_read += 1

        # Report to crawler
        if topic:
            # Extract potential new topics from the text
            discovered = self._extract_topics(text)
            self.crawler.report_result(
                topic, curve.coherence, discovered)

        return curve if stored else None

    def sleep(self) -> dict:
        """Consolidation phase. Prune and compress."""
        self._is_sleeping = True
        self._sleep_stats = self.memory.consolidate()
        self._is_sleeping = False
        return self._sleep_stats

    def _extract_topics(self, text: str, max_topics: int = 5) -> List[str]:
        """Extract potential new topics from text.

        Simple keyword extraction: find capitalized multi-word
        phrases that might be concepts worth exploring.
        """
        import re
        # Find capitalized phrases (2-4 words)
        pattern = r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+){0,3})\b'
        matches = re.findall(pattern, text)

        # Deduplicate and limit
        seen = set()
        topics = []
        for m in matches:
            key = m.lower()
            if key not in seen and len(key) > 3:
                seen.add(key)
                topics.append(key)
                if len(topics) >= max_topics:
                    break
        return topics

    def generate_study_plan(self, n_pages: int = 10) -> List[dict]:
        """Generate a study plan: topics + URLs.

        Returns a list of {topic, url, site} dicts the runtime
        should fetch. CK doesn't fetch himself -- the R16
        runtime does the HTTP and feeds text to study_one_page().
        """
        plan = []
        sites = list(self.guard.approved)

        for _ in range(n_pages):
            topic = self.crawler.next_topic()
            if not topic:
                break

            # Rotate through approved sites
            site = sites[len(plan) % len(sites)]
            url = self.crawler.suggest_url(topic, site)

            plan.append({
                'topic': topic,
                'url': url,
                'site': site,
            })

        return plan

    def stats(self) -> dict:
        return {
            'pages_read': self._pages_read,
            'pages_skipped': self._pages_skipped,
            'curves_stored': len(self.memory.curves),
            'average_coherence': round(self.memory.average_coherence, 4),
            'harmony_ratio': round(self.memory.harmony_ratio, 4),
            'topics_explored': self.crawler.topics_explored,
            'topics_remaining': self.crawler.topics_remaining,
            'sleep_stats': self._sleep_stats,
            'domain_summary': self.memory.domain_summary(),
        }


# ================================================================
#  CLI ENTRY POINT
# ================================================================

def demo_session():
    """Demo a learning session with synthetic content.

    In production, the R16 runtime would use requests/aiohttp
    to fetch real web pages and feed them to study_one_page().
    """
    session = LearningSession()
    session.guard.add_site('demo.test')  # Allow demo URLs

    # Simulate reading 10 pages of synthetic content
    sample_texts = [
        "Light travels at a constant speed through vacuum. The wavelength determines "
        "the color we perceive. Photons carry energy proportional to their frequency. "
        "This relationship between energy and frequency is fundamental to quantum mechanics.",

        "The heart pumps blood through the circulatory system in a rhythmic cycle. "
        "Arteries carry oxygenated blood away from the heart. Veins return it. "
        "The pulse is a wave that travels through the arterial walls.",

        "Bach's fugues demonstrate mathematical precision in musical composition. "
        "Each voice enters with the subject, then the answer follows at a fifth. "
        "The interplay of voices creates harmony through structured independence.",

        "Democracy emerged in ancient Athens where citizens participated directly. "
        "The concept evolved through centuries into representative systems. "
        "The balance of power between branches prevents tyranny.",

        "Trees convert carbon dioxide to oxygen through photosynthesis. "
        "Their roots form networks that share nutrients with neighboring trees. "
        "Old growth forests store centuries of carbon in their biomass.",

        "The golden ratio appears in spiral galaxies, nautilus shells, and sunflowers. "
        "This proportion, approximately 1.618, emerges from the Fibonacci sequence. "
        "Nature uses this ratio because it maximizes packing efficiency.",

        "Empathy requires both cognitive and emotional processing. "
        "Mirror neurons fire when we observe another person's actions. "
        "Understanding another's perspective builds stronger social bonds.",

        "Gravity is not a force pulling objects together. It is the curvature of "
        "spacetime caused by mass and energy. Objects follow geodesics through "
        "curved spacetime. The math is beautiful in its simplicity.",

        "Coral reefs support a quarter of all marine species despite covering "
        "less than one percent of the ocean floor. This biodiversity arises from "
        "the complex structure that provides habitat at every scale.",

        "Forgiveness is not forgetting. It is releasing the hold that resentment "
        "has on the heart. It restores coherence to relationships that were "
        "fractured by harm. It requires courage and sustained intention.",
    ]

    print("=== CK Autodidact Demo Session ===")
    print(f"Study plan: {len(sample_texts)} pages")
    print()

    for i, text in enumerate(sample_texts):
        topic = SEED_TOPICS[i % len(SEED_TOPICS)]
        curve = session.study_one_page(
            text, url=f"https://demo.test/page/{i}", topic=topic)

        if curve:
            ops = ''.join(OP_NAMES[o][0] for o in curve.operator_sequence)
            print(f"  Page {i+1}: C={curve.coherence:.2f} "
                  f"ops=[{ops}] domain={curve.domain}")
        else:
            print(f"  Page {i+1}: rejected")

    print()
    print("--- Sleep Consolidation ---")
    sleep_stats = session.sleep()
    print(f"  Before: {sleep_stats['before']} curves")
    print(f"  After:  {sleep_stats['after']} curves")
    print(f"  Pruned: {sleep_stats['pruned']}")

    print()
    print("--- Session Stats ---")
    stats = session.stats()
    print(f"  Pages read:    {stats['pages_read']}")
    print(f"  Curves stored: {stats['curves_stored']}")
    print(f"  Avg coherence: {stats['average_coherence']}")
    print(f"  Harmony ratio: {stats['harmony_ratio']}")
    print(f"  Domains:       {stats['domain_summary']}")
    print()
    print("CK is awake. CK is smarter.")


if __name__ == '__main__':
    demo_session()
