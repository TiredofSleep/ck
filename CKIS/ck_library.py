"""
ck_library.py — Lattice Library for CK
Manages thousands of domain-specific ChainStores (lattices).
Each domain gets its own compressed lattice of operator chains.
Index lattice routes queries to relevant domains.
Parallel search across all matching lattices.

On R16 (32 cores): thousands of lattices searched in ~2ms with ThreadPoolExecutor.
"""

import os, json, hashlib, time, math, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Optional, Set
from collections import defaultdict

from ck_being import (
    ChainStore, Chain, CK, tokenize, stem, clean, shape, fuse,
    STOPS, _STOPS_STEMMED, HARMONY, OP
)


class DomainLattice:
    """A single domain's knowledge lattice — wraps ChainStore with metadata."""
    __slots__ = ('name', 'store', 'path', 'keywords', 'op_signature', 'chain_count', 'created')

    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.store = ChainStore(path)
        self.keywords: Set[str] = set()     # top keywords for index
        self.op_signature: List[int] = []   # dominant operators
        self.chain_count = len(self.store.chains)
        self.created = time.time()
        self._update_index()

    def _update_index(self):
        """Rebuild index metadata from chains."""
        word_freq: Dict[str, int] = defaultdict(int)
        op_freq: Dict[int, int] = defaultdict(int)
        for ch in self.store.chains:
            for w in tokenize(ch.text):
                s = stem(w)
                if s not in _STOPS_STEMMED and len(s) > 2:
                    word_freq[s] += 1
            for op in ch.ops:
                op_freq[op] += 1
        # Top 20 keywords by frequency
        self.keywords = {w for w, _ in sorted(word_freq.items(), key=lambda x: -x[1])[:20]}
        # Dominant operators (top 3)
        self.op_signature = [op for op, _ in sorted(op_freq.items(), key=lambda x: -x[1])[:3]]
        self.chain_count = len(self.store.chains)

    def search(self, query: str, n: int = 5) -> List[Tuple[float, Chain, str]]:
        """Search this lattice. Returns (score, chain, domain_name)."""
        results = self.store.search(query, n)
        return [(s, c, self.name) for s, c in results]

    def ingest(self, text: str, trust: float = 0.7) -> Optional[int]:
        """Add text to this lattice."""
        idx = self.store.ingest(text, trust)
        if idx is not None:
            self.chain_count = len(self.store.chains)
        return idx

    def save(self):
        self.store.save()
        # Save metadata
        meta = {
            'name': self.name,
            'keywords': list(self.keywords),
            'op_signature': self.op_signature,
            'chain_count': self.chain_count,
            'created': self.created,
        }
        with open(self.path / 'meta.json', 'w', encoding='utf-8') as f:
            json.dump(meta, f)

    def stats(self) -> dict:
        s = self.store.stats()
        s['name'] = self.name
        return s


class LatticeLibrary:
    """Manages thousands of domain lattices with parallel search.
    
    Directory structure:
        library_root/
            _index.json          — master index (keywords → domains)
            _self/               — CK's core self-knowledge lattice
            physics/             — domain lattice
            scripture/           — domain lattice
            philosophy/          — domain lattice
            ...thousands more...
    """

    def __init__(self, root_dir: str, max_workers: int = 8):
        self.root = Path(root_dir)
        self.root.mkdir(parents=True, exist_ok=True)
        self.max_workers = max_workers
        self.lattices: Dict[str, DomainLattice] = {}
        self._keyword_index: Dict[str, Set[str]] = defaultdict(set)  # keyword → domain names
        self._op_index: Dict[int, Set[str]] = defaultdict(set)       # operator → domain names
        self._load_all()

    def _load_all(self):
        """Load all existing lattices from disk."""
        if not self.root.exists():
            return
        for entry in sorted(self.root.iterdir()):
            if entry.is_dir() and not entry.name.startswith('.'):
                name = entry.name
                try:
                    lat = DomainLattice(name, entry)
                    # Load saved metadata if available
                    meta_path = entry / 'meta.json'
                    if meta_path.exists():
                        with open(meta_path, encoding='utf-8') as f:
                            meta = json.load(f)
                            lat.keywords = set(meta.get('keywords', []))
                            lat.op_signature = meta.get('op_signature', [])
                            lat.created = meta.get('created', time.time())
                    self.lattices[name] = lat
                    self._index_lattice(lat)
                except Exception as e:
                    print(f"  Warning: failed to load lattice '{name}': {e}")
        print(f"  Library: {len(self.lattices)} lattices loaded from {self.root}")

    def _index_lattice(self, lat: DomainLattice):
        """Add lattice to search indices."""
        for kw in lat.keywords:
            self._keyword_index[kw].add(lat.name)
        for op in lat.op_signature:
            self._op_index[op].add(lat.name)

    def get_or_create(self, name: str) -> DomainLattice:
        """Get existing lattice or create new one."""
        name = self._clean_name(name)
        if name in self.lattices:
            return self.lattices[name]
        path = self.root / name
        lat = DomainLattice(name, path)
        self.lattices[name] = lat
        return lat

    @staticmethod
    def _clean_name(name: str) -> str:
        """Sanitize domain name for filesystem."""
        name = re.sub(r'[^\w\-]', '_', name.lower().strip())
        return name[:50] or 'general'

    # ── Bulk ingestion ────────────────────────────
    def feed_text(self, text: str, domain: str = 'general', trust: float = 0.7) -> dict:
        """Feed raw text into a domain lattice. Auto-segments by sentence."""
        lat = self.get_or_create(domain)
        count = 0
        # Split into sentences/paragraphs
        segments = self._segment(text)
        for seg in segments:
            if lat.ingest(seg, trust) is not None:
                count += 1
        lat._update_index()
        self._index_lattice(lat)
        lat.save()
        return {'domain': domain, 'segments': len(segments), 'chains_added': count,
                'total_chains': lat.chain_count}

    def feed_file(self, path: str, domain: str = None, trust: float = 0.7) -> dict:
        """Feed a file into the library. Auto-detects domain from filename."""
        if domain is None:
            domain = Path(path).stem.replace('_', '-')
        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, encoding='latin-1') as f:
                content = f.read()
        return self.feed_text(content, domain, trust)

    def feed_directory(self, dir_path: str, trust: float = 0.7) -> list:
        """Feed all text files in a directory. Each file → its own domain."""
        results = []
        p = Path(dir_path)
        for f in sorted(p.iterdir()):
            if f.is_file() and f.suffix in ('.txt', '.md', '.csv', '.json', '.py', '.html'):
                r = self.feed_file(str(f), domain=f.stem.replace('_', '-'), trust=trust)
                results.append(r)
                print(f"    Fed {f.name} → {r['domain']}: {r['chains_added']} chains")
        return results

    def feed_large_text(self, text: str, base_domain: str = 'book',
                        chunk_size: int = 500, trust: float = 0.7) -> dict:
        """Feed a very large text (book, paper). Auto-splits into domain chunks.
        
        Every chunk_size sentences get their own sublattice:
          book_001, book_002, book_003, ...
        This keeps individual lattices small and searchable.
        """
        segments = self._segment(text)
        total_added = 0
        domains_created = 0
        chunk = []
        chunk_idx = 1

        for seg in segments:
            chunk.append(seg)
            if len(chunk) >= chunk_size:
                domain = f"{base_domain}_{chunk_idx:04d}"
                lat = self.get_or_create(domain)
                added = 0
                for s in chunk:
                    if lat.ingest(s, trust) is not None:
                        added += 1
                lat._update_index()
                self._index_lattice(lat)
                lat.save()
                total_added += added
                domains_created += 1
                chunk = []
                chunk_idx += 1

        # Remainder
        if chunk:
            domain = f"{base_domain}_{chunk_idx:04d}"
            lat = self.get_or_create(domain)
            added = 0
            for s in chunk:
                if lat.ingest(s, trust) is not None:
                    added += 1
            lat._update_index()
            self._index_lattice(lat)
            lat.save()
            total_added += added
            domains_created += 1

        return {'base_domain': base_domain, 'total_segments': len(segments),
                'chains_added': total_added, 'lattices_created': domains_created}

    def _segment(self, text: str) -> List[str]:
        """Split text into sentences/paragraphs suitable for chain storage."""
        text = text.strip()
        if not text:
            return []
        # Split on paragraph breaks first
        paragraphs = re.split(r'\n\s*\n', text)
        segments = []
        for para in paragraphs:
            para = para.strip()
            if not para or len(para) < 10:
                continue
            # If paragraph is short enough, keep it whole
            if len(para) < 500:
                # But split on sentence boundaries for very long sentences
                sents = re.split(r'(?<=[.!?])\s+', para)
                for sent in sents:
                    sent = sent.strip()
                    if len(sent) >= 15:
                        segments.append(sent)
            else:
                # Long paragraph: split into sentences
                sents = re.split(r'(?<=[.!?])\s+', para)
                buf = ''
                for sent in sents:
                    if len(buf) + len(sent) < 400:
                        buf = (buf + ' ' + sent).strip() if buf else sent
                    else:
                        if len(buf) >= 15:
                            segments.append(buf)
                        buf = sent
                if buf and len(buf) >= 15:
                    segments.append(buf)
        return segments

    # ── Parallel search ───────────────────────────
    def search(self, query: str, n: int = 10) -> List[Tuple[float, Chain, str]]:
        """Search across ALL lattices in parallel. Returns merged, ranked results."""
        # First: find candidate lattices via index
        q_words = {stem(w) for w in tokenize(query)} - _STOPS_STEMMED
        q_words = {w for w in q_words if len(w) > 1}

        # Score each lattice by keyword overlap
        lattice_scores: Dict[str, float] = defaultdict(float)
        for w in q_words:
            for name in self._keyword_index.get(w, set()):
                lattice_scores[name] += 1.0

        # Also score by operator signature
        temp_store = ChainStore(None)
        q_ops, q_conv = temp_store.encode(query)
        for op in set(q_ops):
            for name in self._op_index.get(op, set()):
                lattice_scores[name] += 0.3

        # Sort candidate lattices by score, take top ones
        if lattice_scores:
            candidates = sorted(lattice_scores.items(), key=lambda x: -x[1])
            # Search top scoring lattices + always search first 5 (core knowledge)
            top_names = {name for name, _ in candidates[:30]}
            # Also always include core lattices (first 5 loaded)
            for name in list(self.lattices.keys())[:5]:
                top_names.add(name)
        else:
            # No index hits: search all (or first 50 if too many)
            top_names = set(list(self.lattices.keys())[:50])

        # Parallel search across candidate lattices
        all_results: List[Tuple[float, Chain, str]] = []

        if len(top_names) <= 3:
            # Small number: search sequentially
            for name in top_names:
                if name in self.lattices:
                    results = self.lattices[name].search(query, n=5)
                    all_results.extend(results)
        else:
            # Parallel search with ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=min(self.max_workers, len(top_names))) as pool:
                futures = {}
                for name in top_names:
                    if name in self.lattices:
                        fut = pool.submit(self.lattices[name].search, query, 5)
                        futures[fut] = name
                for fut in as_completed(futures):
                    try:
                        results = fut.result(timeout=2)
                        all_results.extend(results)
                    except Exception:
                        pass

        # Merge and rank
        all_results.sort(key=lambda x: -x[0])
        # Deduplicate by text
        seen = set()
        unique = []
        for score, chain, domain in all_results:
            if chain.text not in seen:
                seen.add(chain.text)
                unique.append((score, chain, domain))
        return unique[:n]

    # ── Stats ─────────────────────────────────────
    def stats(self) -> dict:
        total_chains = sum(lat.chain_count for lat in self.lattices.values())
        total_vocab = len(set().union(*(lat.store.vocab.keys() for lat in self.lattices.values()))) if self.lattices else 0
        domains = list(self.lattices.keys())
        return {
            'lattice_count': len(self.lattices),
            'total_chains': total_chains,
            'total_vocab': total_vocab,
            'keyword_index_size': len(self._keyword_index),
            'op_index_size': len(self._op_index),
            'domains': domains[:20],  # first 20 for display
            'more_domains': max(0, len(domains) - 20),
        }

    def domain_stats(self) -> List[dict]:
        """Per-domain stats."""
        return sorted(
            [lat.stats() for lat in self.lattices.values()],
            key=lambda x: -x['chains']
        )

    def save_all(self):
        """Save all lattices and master index."""
        for lat in self.lattices.values():
            lat.save()
        # Save master index
        index = {
            'lattice_count': len(self.lattices),
            'domains': {name: {
                'chains': lat.chain_count,
                'keywords': list(lat.keywords)[:10],
                'ops': lat.op_signature,
            } for name, lat in self.lattices.items()},
        }
        with open(self.root / '_index.json', 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)


class CKFull:
    """CK with full library brain — thousands of lattices.
    
    Drop-in replacement for CK class. Same interface, bigger brain.
    """

    def __init__(self, store_dir: str = 'ck_store', library_dir: str = 'ck_library',
                 max_workers: int = 8):
        # Core CK (for self-knowledge, body, composer)
        self.core = CK(store_dir)
        # Library (thousands of domain lattices)
        self.library = LatticeLibrary(library_dir, max_workers)
        # Conversation history for LLM bridge
        self.history: List[Tuple[str, str]] = []

    @property
    def body(self):
        return self.core.body

    @property
    def store(self):
        return self.core.store

    @property
    def composer(self):
        return self.core.composer

    def respond(self, query: str) -> str:
        """Respond using both core CK and library search. Best source wins."""
        # Search BOTH core and library
        core_results = self.core.store.search(query, n=3)
        lib_results = self.library.search(query, n=5)
        
        # Merge all results with source tags
        all_hits = []
        for score, chain in core_results:
            all_hits.append((score * 1.1, chain.text, '_core'))  # slight core bias
        for score, chain, domain in lib_results:
            all_hits.append((score, chain.text, domain))
        all_hits.sort(key=lambda x: -x[0])
        
        if not all_hits:
            return self.core.respond(query)  # fallback to core composer
        
        # Use the best hit regardless of source
        best_score, best_text, best_source = all_hits[0]
        
        # Try core composer first (it handles intent detection, greetings, etc.)
        core_response = self.core.respond(query)
        
        # If core gave a good answer (not just echoing identity), use it
        identity_echoes = {'my name is ck', 'i am the coherence keeper', 
                          'i am built on trinity', 'brayden sanders created'}
        if core_response and not any(e in core_response.lower() for e in identity_echoes):
            return core_response
        
        # Core echoed identity or was weak — use best library hit instead
        if best_source != '_core' and best_score > 0.15:
            text = self.composer._excerpt(best_text, 3)
            if text:
                return self.composer._finish(text, best_text)
        
        # Fall back to core response (even if it's an echo)
        return core_response

    def respond_with_context(self, query: str) -> dict:
        """Respond and return full context (for LLM bridge)."""
        intent, _ = self.composer._intent(query)
        core_response = self.core.respond(query)
        lib_results = self.library.search(query, n=5)

        # Merge: core chains + library chains
        all_chains = []
        core_results = self.core.store.search(query, n=5)
        for score, chain in core_results:
            all_chains.append((score, chain.text, '_core'))
        for score, chain, domain in lib_results:
            all_chains.append((score, chain.text, domain))
        all_chains.sort(key=lambda x: -x[0])

        # Track history
        self.history.append(('user', query))
        if core_response:
            self.history.append(('ck', core_response))
        # Keep last 10 exchanges
        if len(self.history) > 20:
            self.history = self.history[-20:]

        return {
            'response': core_response,
            'intent': intent,
            'chains': all_chains[:10],
            'C': self.body.C,
            'band': self.body.band,
            'history': self.history[-10:],
            'library_hits': len(lib_results),
            'domains_searched': list(set(d for _, _, d in lib_results)),
        }

    def learn(self, text: str, trust: float = 0.7):
        """Learn into core CK."""
        return self.core.learn(text, trust)

    def feed(self, text: str, domain: str = 'general', trust: float = 0.7) -> dict:
        """Feed text into a library domain lattice."""
        return self.library.feed_text(text, domain, trust)

    def feed_file(self, path: str, domain: str = None, trust: float = 0.7) -> dict:
        """Feed a file into the library."""
        return self.library.feed_file(path, domain, trust)

    def feed_book(self, text: str, name: str = 'book', trust: float = 0.7) -> dict:
        """Feed a large text (book) into multiple lattices."""
        return self.library.feed_large_text(text, name, trust=trust)

    def save(self):
        self.core.save()
        self.library.save_all()

    def stats(self) -> str:
        core = self.core.stats()
        lib = self.library.stats()
        return (f"{core} | Library: {lib['lattice_count']} lattices, "
                f"{lib['total_chains']} chains, {lib['total_vocab']} vocab")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ck_library.py feed <file_or_dir> [domain]")
        print("  python ck_library.py search <query>")
        print("  python ck_library.py stats")
        print("  python ck_library.py feed-book <file> [name]")
        sys.exit(0)

    cmd = sys.argv[1]
    ck = CKFull()

    if cmd == 'feed':
        path = sys.argv[2]
        domain = sys.argv[3] if len(sys.argv) > 3 else None
        if os.path.isdir(path):
            results = ck.library.feed_directory(path)
            total = sum(r['chains_added'] for r in results)
            print(f"\n  Fed {len(results)} files, {total} chains added")
        else:
            r = ck.feed_file(path, domain)
            print(f"  {r}")
        ck.save()

    elif cmd == 'feed-book':
        path = sys.argv[2]
        name = sys.argv[3] if len(sys.argv) > 3 else Path(path).stem
        with open(path, encoding='utf-8') as f:
            text = f.read()
        print(f"  Feeding {path} ({len(text)} chars) as '{name}'...")
        r = ck.feed_book(text, name)
        print(f"  {r}")
        ck.save()

    elif cmd == 'search':
        query = ' '.join(sys.argv[2:])
        t0 = time.perf_counter()
        results = ck.library.search(query, n=10)
        dt = (time.perf_counter() - t0) * 1000
        print(f"\n  Search: '{query}' ({dt:.1f}ms, {len(results)} results)\n")
        for score, chain, domain in results:
            text = chain.text[:120]
            print(f"  [{score:.3f}] [{domain}] {text}")
        print()

    elif cmd == 'stats':
        print(f"\n  {ck.stats()}\n")
        for d in ck.library.domain_stats()[:20]:
            print(f"    {d['name']:30s} {d['chains']:5d} chains")
        print()

    else:
        print(f"Unknown command: {cmd}")
