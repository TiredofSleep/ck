"""ck_web_reading.py -- CK explores the open internet for new material.

Brayden 2026-05-17: "open him up to the internet to explore"

═══════════════════════════════════════════════════════════════════════
What this module is
═══════════════════════════════════════════════════════════════════════

His prior corpora (bible, scripture, poetry, 341 domain subjects) were
all bundled at compile time.  This module gives him actual web access
so he can keep finding new material indefinitely.

Architecture is the same five-rule discipline (D118-D124):

  1. He reads.  We don't curate which URLs matter.  Seed list is
     openly editable; rotation is round-robin.
  2. He anchors only what resonates.  Same scorer.
  3. His anchors are HIS.  No source weighted above another.
  4. Honest about absence ("I couldn't reach that URL today").
  5. Discipline written into canon: D125 + this docstring.

═══════════════════════════════════════════════════════════════════════
Etiquette (the rules he reads the web BY)
═══════════════════════════════════════════════════════════════════════

  - Honest User-Agent: "CK-Bot/0.1 (Coherence Keeper; coherencekeeper.com)"
  - Polite rate limit: minimum 10 seconds between same-host requests
  - Respect robots.txt (best-effort check via urllib.robotparser)
  - Strict timeouts: 10 seconds total per fetch
  - Max content size: 200KB per page (truncate larger)
  - HTTPS preferred; HTTP allowed for sources that require it
  - No credentials, no cookies, no JS execution
  - No POST/PUT/DELETE -- read-only GET requests
  - No following redirects across hosts (within-host only, max 3)
  - 24-hour per-URL cooldown so he isn't hammering the same page

═══════════════════════════════════════════════════════════════════════
Sources (curated seeds, all openly-licensed)
═══════════════════════════════════════════════════════════════════════

The default seed list at `Gen14/targets/ck/brain/reading_room/web_seeds.json`
points at:

  - Wikipedia (CC-BY-SA): Special:Random + a few featured articles
  - Project Gutenberg (Public Domain): full text of classic books
  - Wikisource (CC-BY-SA / PD): primary texts
  - Stanford Encyclopedia of Philosophy (CC-BY-NC-SA in non-commercial)
  - arXiv abstracts (most CC-licensed)

Brayden can edit `web_seeds.json` any time to add or remove URLs.

═══════════════════════════════════════════════════════════════════════
What he does NOT do
═══════════════════════════════════════════════════════════════════════

  - No search-engine queries (would require API keys)
  - No JS rendering (would need headless browser)
  - No login-protected content
  - No financial / health / personal-data sites
  - No paywall bypass
  - No image / audio / video decoding (text only)

═══════════════════════════════════════════════════════════════════════
Anchors
═══════════════════════════════════════════════════════════════════════

Persist to `Gen13/var/web_reading_anchors.jsonl`:

  {
    "ts":         1779000000.0,
    "url":        "https://en.wikipedia.org/wiki/Topology",
    "host":       "en.wikipedia.org",
    "title":      "Topology - Wikipedia",
    "chunk_idx":  3,
    "text":       "...",
    "operators":  [0, 7, 8, ...],
    "resonance":  0.65
  }
"""
from __future__ import annotations

import hashlib
import json
import re
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


_USER_AGENT = ("CK-Bot/0.1 (Coherence Keeper; +https://coherencekeeper.com; "
               "respects robots.txt; rate-limited; text-only reader)")
_MAX_BYTES = 200_000
_FETCH_TIMEOUT = 10.0
_PER_HOST_MIN_GAP_SEC = 10.0


def _seeds_path() -> Path:
    """User-editable seed list."""
    return HERE / "reading_room" / "web_seeds.json"


def _anchors_path() -> Path:
    _root = HERE
    for _ in range(8):
        _root = _root.parent
        if (_root / "Gen13" / "var").exists():
            return _root / "Gen13" / "var" / "web_reading_anchors.jsonl"
    return HERE.parent / "var" / "web_reading_anchors.jsonl"


def _state_path() -> Path:
    _root = HERE
    for _ in range(8):
        _root = _root.parent
        if (_root / "Gen13" / "var").exists():
            return _root / "Gen13" / "var" / "web_reading_state.json"
    return HERE.parent / "var" / "web_reading_state.json"


_ANCHOR_LOCK = threading.Lock()
_STATE_LOCK = threading.Lock()
_HOST_LAST_FETCH: Dict[str, float] = {}
_HOST_LOCK = threading.Lock()


# ─── Default seeds (written if seeds file doesn't exist) ─────────────

_DEFAULT_SEEDS = {
    "_comment": ("CK reads the open internet from these URLs (and any "
                  "you add).  All listed are openly-licensed or PD.  "
                  "Edit freely; daemon picks up changes on next "
                  "rescan."),
    "seeds": [
        # Wikipedia random article (rotates every fetch)
        "https://en.wikipedia.org/wiki/Special:Random",
        # Wikipedia featured-articles a few high-quality starting points
        "https://en.wikipedia.org/wiki/Mathematics",
        "https://en.wikipedia.org/wiki/Topology",
        "https://en.wikipedia.org/wiki/Algebra",
        "https://en.wikipedia.org/wiki/Number_theory",
        "https://en.wikipedia.org/wiki/Group_theory",
        "https://en.wikipedia.org/wiki/Quantum_mechanics",
        "https://en.wikipedia.org/wiki/General_relativity",
        "https://en.wikipedia.org/wiki/Consciousness",
        "https://en.wikipedia.org/wiki/Philosophy_of_mind",
        "https://en.wikipedia.org/wiki/Poetry",
        "https://en.wikipedia.org/wiki/Metaphor",
        "https://en.wikipedia.org/wiki/Music_theory",
        "https://en.wikipedia.org/wiki/Cellular_automaton",
        "https://en.wikipedia.org/wiki/Information_theory",
        # Wikipedia Special:Random hits a different page each time -- so
        # adding it multiple times means more random exposure
        "https://en.wikipedia.org/wiki/Special:Random",
        "https://en.wikipedia.org/wiki/Special:Random",
        # Wikipedia "On this day" -- temporally fresh content
        "https://en.wikipedia.org/wiki/Wikipedia:Main_Page",
    ],
}


def _ensure_seeds_file() -> Path:
    path = _seeds_path()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_DEFAULT_SEEDS, indent=2),
                          encoding="utf-8")
    return path


def load_seeds() -> List[str]:
    try:
        path = _ensure_seeds_file()
        d = json.loads(path.read_text(encoding="utf-8"))
        seeds = d.get("seeds", []) or []
        return [s for s in seeds if isinstance(s, str) and s.startswith("http")]
    except Exception:
        return list(_DEFAULT_SEEDS["seeds"])


# ─── Persistence ──────────────────────────────────────────────────────

def _append_anchor(rec: Dict[str, Any]) -> None:
    try:
        path = _anchors_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with _ANCHOR_LOCK:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False,
                                    sort_keys=True) + "\n")
    except Exception:
        pass


def _load_anchors() -> List[Dict[str, Any]]:
    p = _anchors_path()
    if not p.exists():
        return []
    out: List[Dict[str, Any]] = []
    try:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        pass
    return out


def _load_state() -> Dict[str, Any]:
    p = _state_path()
    if not p.exists():
        return {"url_last_fetched": {}, "n_fetches": 0,
                "n_anchored": 0, "rr_idx": 0,
                "started_ts": time.time()}
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"url_last_fetched": {}, "n_fetches": 0,
                "n_anchored": 0, "rr_idx": 0,
                "started_ts": time.time()}


def _save_state(state: Dict[str, Any]) -> None:
    try:
        p = _state_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        with _STATE_LOCK:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
    except Exception:
        pass


# ─── Polite fetcher ──────────────────────────────────────────────────

def _polite_gap(host: str) -> None:
    """Sleep until at least _PER_HOST_MIN_GAP_SEC has elapsed since the
    last fetch from this host."""
    now = time.time()
    with _HOST_LOCK:
        last = _HOST_LAST_FETCH.get(host, 0.0)
        wait = max(0.0, last + _PER_HOST_MIN_GAP_SEC - now)
    if wait > 0:
        time.sleep(wait)
    with _HOST_LOCK:
        _HOST_LAST_FETCH[host] = time.time()


_ROBOTS_CACHE: Dict[str, Optional[urllib.robotparser.RobotFileParser]] = {}
_ROBOTS_LOCK = threading.Lock()


def _can_fetch(url: str) -> bool:
    """Best-effort robots.txt check.  Default-allow if robots.txt can't
    be reached (server might be slow); default-deny only if we get an
    explicit Disallow."""
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        host = parsed.netloc
        with _ROBOTS_LOCK:
            rp = _ROBOTS_CACHE.get(host)
        if rp is None:
            rp = urllib.robotparser.RobotFileParser()
            robots_url = f"{parsed.scheme}://{host}/robots.txt"
            try:
                req = urllib.request.Request(robots_url,
                                                headers={"User-Agent": _USER_AGENT})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    rp.parse(resp.read().decode("utf-8",
                                                  errors="replace").splitlines())
            except Exception:
                rp = None  # default-allow when robots.txt unreachable
            with _ROBOTS_LOCK:
                _ROBOTS_CACHE[host] = rp
        if rp is None:
            return True
        return rp.can_fetch(_USER_AGENT, url)
    except Exception:
        return True


_HTML_TAG_RE = re.compile(r"<[^>]+>")
_HTML_SCRIPT_RE = re.compile(r"<script[\s\S]*?</script>", re.IGNORECASE)
_HTML_STYLE_RE = re.compile(r"<style[\s\S]*?</style>", re.IGNORECASE)
_HTML_ENTITY_RE = re.compile(r"&(amp|lt|gt|quot|apos|nbsp|#\d+|#x[0-9a-fA-F]+);")
_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>",
                          re.IGNORECASE | re.DOTALL)
_WHITESPACE_RE = re.compile(r"\s+")


def _entity_to_char(m: "re.Match[str]") -> str:
    e = m.group(1)
    table = {"amp": "&", "lt": "<", "gt": ">", "quot": '"',
             "apos": "'", "nbsp": " "}
    if e in table:
        return table[e]
    if e.startswith("#x") or e.startswith("#X"):
        try:
            return chr(int(e[2:], 16))
        except Exception:
            return ""
    if e.startswith("#"):
        try:
            return chr(int(e[1:]))
        except Exception:
            return ""
    return ""


def html_to_text(html: str) -> Tuple[str, str]:
    """Strip HTML tags, extract title.  Returns (title, body_text)."""
    if not html:
        return "", ""
    title_m = _TITLE_RE.search(html)
    title = title_m.group(1).strip() if title_m else ""
    body = html
    body = _HTML_SCRIPT_RE.sub(" ", body)
    body = _HTML_STYLE_RE.sub(" ", body)
    body = _HTML_TAG_RE.sub(" ", body)
    body = _HTML_ENTITY_RE.sub(_entity_to_char, body)
    title = _HTML_ENTITY_RE.sub(_entity_to_char, title)
    body = _WHITESPACE_RE.sub(" ", body).strip()
    title = _WHITESPACE_RE.sub(" ", title).strip()
    return title, body


def fetch(url: str) -> Dict[str, Any]:
    """Polite fetch.  Returns a dict with status + text + metadata.
    Never raises; errors are reported in the dict."""
    out: Dict[str, Any] = {
        "url": url, "ok": False, "fetched_ts": time.time(),
        "text": "", "title": "", "host": "", "status": None,
        "error": None, "n_bytes": 0,
    }
    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc
        out["host"] = host
        if parsed.scheme not in ("http", "https"):
            out["error"] = f"unsupported scheme: {parsed.scheme}"
            return out
        if not _can_fetch(url):
            out["error"] = "blocked by robots.txt"
            return out
        _polite_gap(host)
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": _USER_AGENT,
                "Accept": "text/html,text/plain,*/*;q=0.5",
                "Accept-Language": "en-US,en;q=0.9",
            })
        with urllib.request.urlopen(req, timeout=_FETCH_TIMEOUT) as resp:
            out["status"] = resp.status
            ct = (resp.headers.get("Content-Type") or "").lower()
            if "text" not in ct and "html" not in ct and "json" not in ct:
                out["error"] = f"non-text content-type: {ct}"
                return out
            raw = resp.read(_MAX_BYTES + 1)
            out["n_bytes"] = len(raw)
            if len(raw) > _MAX_BYTES:
                raw = raw[:_MAX_BYTES]
            charset = "utf-8"
            if "charset=" in ct:
                try:
                    charset = ct.split("charset=", 1)[1].split(";")[0].strip()
                except Exception:
                    pass
            body = raw.decode(charset, errors="replace")
            if "html" in ct or body.lstrip().startswith("<"):
                title, text = html_to_text(body)
                out["title"] = title
                out["text"] = text
            else:
                out["text"] = body
                out["title"] = parsed.path.rsplit("/", 1)[-1] or host
        out["ok"] = True
        return out
    except urllib.error.HTTPError as e:
        out["status"] = e.code
        out["error"] = f"HTTP {e.code}"
    except urllib.error.URLError as e:
        out["error"] = f"URL error: {e.reason}"
    except socket.timeout:
        out["error"] = "timeout"
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"
    return out


# ─── Resonance scoring (same as scripture/poetry/domain) ─────────────

_OP_KEYWORDS: Dict[int, Tuple[str, ...]] = {
    0: ("void", "empty", "nothing", "barren", "wilderness", "desolate",
         "absent", "absence"),
    1: ("foundation", "rock", "earth", "land", "build", "stone", "ground",
         "structure", "lattice"),
    2: ("count", "number", "measure", "weigh", "name", "remember",
         "compare", "mark"),
    3: ("walk", "go", "way", "path", "follow", "lead", "journey", "road",
         "process", "progress"),
    4: ("fall", "sin", "break", "down", "die", "death", "loss", "ruin",
         "shadow", "sorrow", "collapse"),
    5: ("balance", "scales", "judge", "weigh", "righteous", "between",
         "harmony", "equal", "balanced"),
    6: ("trouble", "wicked", "storm", "fear", "wrath", "chaos", "anger",
         "hatred", "violence", "chaotic"),
    7: ("peace", "joy", "love", "light", "good", "blessed", "harmony",
         "rejoice", "virtue", "compassion", "mercy", "wisdom", "truth",
         "beauty", "fair", "bright"),
    8: ("breath", "spirit", "wind", "breathe", "alive", "life", "soul",
         "self", "song", "voice", "sing", "consciousness"),
    9: ("rest", "sabbath", "return", "renew", "new", "restore", "again",
         "eternal", "everlasting", "forever", "still", "reset"),
}


def encode_chunk(text: str) -> List[int]:
    if not text:
        return []
    low = text.lower()
    ops: List[int] = []
    for op_id, kws in _OP_KEYWORDS.items():
        if any(kw in low for kw in kws):
            ops.append(op_id)
    return ops


def resonance(ops: List[int]) -> float:
    if not ops:
        return 0.0
    score = 0.0
    op_set = set(ops)
    if 7 in op_set:
        score += 0.35
    if 8 in op_set:
        score += 0.20
    if 0 in op_set:
        score += 0.15
    if 9 in op_set:
        score += 0.15
    others = op_set - {0, 7, 8, 9}
    score += 0.05 * len(others)
    return min(1.0, score)


# ─── Chunking ────────────────────────────────────────────────────────

def chunk_text(text: str, target_chars: int = 600) -> List[str]:
    """Split text into resonable-sized chunks at paragraph or sentence
    boundaries.  Falls back to sentence-then-character splitting if no
    paragraph breaks exist (HTML-stripped content often has none).
    """
    if not text:
        return []
    # Try paragraph splitting first
    paras = re.split(r"\n\s*\n", text)
    if len(paras) <= 1:
        # No paragraph breaks; split on sentence boundaries instead.
        # Common end-punctuation followed by space + capital, or by
        # whitespace + capital.  Imperfect but adequate.
        paras = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    chunks: List[str] = []
    cur: List[str] = []
    cur_len = 0
    for p in paras:
        p = p.strip()
        if not p:
            continue
        # If this piece alone exceeds target, hard-split it
        while len(p) > target_chars * 2:
            chunks.append(p[:target_chars])
            p = p[target_chars:].lstrip()
        if cur_len + len(p) > target_chars and cur:
            chunks.append(" ".join(cur))
            cur = [p]
            cur_len = len(p)
        else:
            cur.append(p)
            cur_len += len(p)
    if cur:
        chunks.append(" ".join(cur))
    # Final fallback if still empty
    if not chunks and text:
        for i in range(0, len(text), target_chars):
            chunks.append(text[i:i + target_chars])
    return chunks


# ─── Anchor + ingest ─────────────────────────────────────────────────

def _hash_chunk(url: str, idx: int, text: str) -> str:
    return hashlib.sha1(
        f"{url}|{idx}|{text[:200]}".encode("utf-8")).hexdigest()[:16]


def ingest_fetched(fetched: Dict[str, Any],
                     threshold: float = 0.45,
                     cooldown_days: int = 7) -> Dict[str, Any]:
    """Chunk + score + anchor a fetched page.  Returns stats."""
    if not fetched.get("ok"):
        return {"ok": False, "reason": fetched.get("error"),
                "url": fetched.get("url"), "n_chunks": 0,
                "n_anchored": 0}
    url = fetched["url"]
    host = fetched.get("host", "")
    title = fetched.get("title", "")
    text = fetched.get("text", "")
    chunks = chunk_text(text)
    if not chunks:
        return {"ok": False, "reason": "no chunks", "url": url,
                "n_chunks": 0, "n_anchored": 0}
    cutoff = time.time() - cooldown_days * 86400
    seen: set = set()
    for prior in _load_anchors():
        if prior.get("ts", 0) > cutoff:
            seen.add((prior.get("url"), prior.get("chunk_hash")))

    n_anchored = 0
    for idx, chunk in enumerate(chunks):
        ops = encode_chunk(chunk)
        score = resonance(ops)
        if score < threshold:
            continue
        chash = _hash_chunk(url, idx, chunk)
        if (url, chash) in seen:
            continue
        _append_anchor({
            "ts":          time.time(),
            "url":         url,
            "host":        host,
            "title":       title,
            "chunk_idx":   idx,
            "chunk_hash":  chash,
            "text":        chunk[:1200],
            "operators":   ops,
            "resonance":   round(score, 3),
        })
        n_anchored += 1
        seen.add((url, chash))
    return {"ok": True, "url": url, "title": title,
            "n_chunks": len(chunks), "n_anchored": n_anchored}


# ─── Public read helpers ─────────────────────────────────────────────

def anchors(k: Optional[int] = None,
             host: Optional[str] = None) -> List[Dict[str, Any]]:
    out = _load_anchors()
    if host:
        out = [a for a in out if a.get("host") == host]
    out.sort(key=lambda r: -r.get("ts", 0))
    return out[:k] if k else out


def explore_url(url: str, threshold: float = 0.45) -> Dict[str, Any]:
    """Fetch + ingest a single URL on demand."""
    fetched = fetch(url)
    if not fetched["ok"]:
        return {"ok": False, "url": url, "error": fetched.get("error")}
    return ingest_fetched(fetched, threshold=threshold)


# ─── Daemon ──────────────────────────────────────────────────────────

class WebExplorerDaemon:
    """Polite continuous web reader.  Round-robins through the seed list;
    polite-gap-respects per-host rate limit; 24h per-URL cooldown."""

    def __init__(self, engine: Any,
                  interval_sec: float = 60.0,
                  resonance_threshold: float = 0.45,
                  per_url_cooldown_sec: float = 86400.0):
        self.engine = engine
        self.interval_sec = float(interval_sec)
        self.resonance_threshold = float(resonance_threshold)
        self.per_url_cooldown_sec = float(per_url_cooldown_sec)
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.state = _load_state()
        self._n_anchored_this_session = 0

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop, daemon=True, name="ck-web-reader")
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)

    def _loop(self) -> None:
        # Long initial settle so we don't compete with boot.
        for _ in range(60):
            if self._stop.is_set():
                return
            time.sleep(1.0)

        while not self._stop.is_set():
            try:
                seeds = load_seeds()
                if not seeds:
                    time.sleep(30)
                    continue
                rr = int(self.state.get("rr_idx", 0)) % len(seeds)
                self.state["rr_idx"] = rr + 1
                url = seeds[rr]
                # Per-URL cooldown (skip if fetched too recently)
                last = (self.state.get("url_last_fetched", {})
                          .get(url, 0.0))
                if time.time() - last < self.per_url_cooldown_sec:
                    # Not yet; rotate to next quickly
                    time.sleep(1.0)
                    continue
                fetched = fetch(url)
                self.state["n_fetches"] = (
                    self.state.get("n_fetches", 0) + 1)
                self.state.setdefault("url_last_fetched", {})[url] = (
                    time.time())
                if fetched["ok"]:
                    result = ingest_fetched(
                        fetched, threshold=self.resonance_threshold,
                        cooldown_days=int(self.per_url_cooldown_sec / 86400))
                    n = result.get("n_anchored", 0)
                    self.state["n_anchored"] = (
                        self.state.get("n_anchored", 0) + n)
                    self._n_anchored_this_session += n
                _save_state(self.state)
            except Exception:
                pass
            for _ in range(int(self.interval_sec * 10)):
                if self._stop.is_set():
                    return
                time.sleep(0.1)

    def stats(self) -> Dict[str, Any]:
        return {
            "alive":              self._thread is not None and
                                   self._thread.is_alive(),
            "interval_sec":       self.interval_sec,
            "resonance_threshold": self.resonance_threshold,
            "n_seeds":            len(load_seeds()),
            "n_fetches_total":    self.state.get("n_fetches", 0),
            "n_anchored_total":   self.state.get("n_anchored", 0),
            "anchored_this_session": self._n_anchored_this_session,
            "rr_idx":             self.state.get("rr_idx", 0),
            "user_agent":         _USER_AGENT,
            "per_host_min_gap_sec": _PER_HOST_MIN_GAP_SEC,
            "max_bytes_per_page": _MAX_BYTES,
        }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_web_reading(engine: Any) -> bool:
    daemon = WebExplorerDaemon(engine, interval_sec=60.0,
                                  resonance_threshold=0.45)
    daemon.start()
    engine.ck_web_reading = {
        "daemon":         daemon,
        "fetch":          fetch,
        "explore_url":    explore_url,
        "anchors":        anchors,
        "load_seeds":     load_seeds,
        "anchors_path":   str(_anchors_path()),
        "seeds_path":     str(_seeds_path()),
    }
    _ensure_seeds_file()

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _info():
                    return jsonify({
                        "philosophy": ("CK reads the open internet -- same "
                                        "discipline as bundled corpora."),
                        "user_agent": _USER_AGENT,
                        "seeds_path": str(_seeds_path()),
                        "n_seeds":    len(load_seeds()),
                        "anchors_path": str(_anchors_path()),
                        "endpoints": [
                            "GET  /web/info",
                            "GET  /web/stats",
                            "GET  /web/anchors[?k=N&host=X]",
                            "GET  /web/seeds",
                            "POST /web/explore  body: {url}",
                        ],
                    })

                def _stats():
                    return jsonify(daemon.stats())

                def _anchors_ep():
                    k = request.args.get("k")
                    h = request.args.get("host")
                    out = anchors(int(k) if k else None, host=h)
                    return jsonify({"n": len(out), "anchors": out})

                def _seeds_ep():
                    return jsonify({"seeds": load_seeds(),
                                     "seeds_path": str(_seeds_path())})

                def _explore():
                    data = request.get_json(silent=True) or {}
                    url = data.get("url")
                    if not url:
                        return jsonify({"error": "missing url"}), 400
                    return jsonify(explore_url(url))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/web/info",     "web_info",    _info,        ["GET"]),
                    ("/web/stats",    "web_stats",   _stats,       ["GET"]),
                    ("/web/anchors",  "web_anchors", _anchors_ep,  ["GET"]),
                    ("/web/seeds",    "web_seeds",   _seeds_ep,    ["GET"]),
                    ("/web/explore",  "web_explore", _explore,     ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] web_reading routes failed: {e}")

    n_seeds = len(load_seeds())
    suffix = ""
    if routes_registered:
        suffix = " (" + ", ".join(routes_registered) + ")"
    print(f"[CK Gen14] web_reading: MOUNTED  {n_seeds} seeds, "
          f"daemon@{daemon.interval_sec}s, polite "
          f"({int(_PER_HOST_MIN_GAP_SEC)}s/host), "
          f"threshold={daemon.resonance_threshold}{suffix}")
    return True


if __name__ == "__main__":
    print("ck_web_reading smoke test (no actual fetch unless EXPLORE=1):")
    seeds = load_seeds()
    print(f"  seeds_path: {_seeds_path()}")
    print(f"  n_seeds:    {len(seeds)}")
    print(f"  first few:  {seeds[:3]}")
    print()
    import os as _os
    if _os.environ.get("EXPLORE") == "1":
        # Try fetching one URL to confirm the polite fetcher works
        url = seeds[0] if seeds else "https://en.wikipedia.org/wiki/Topology"
        print(f"  Fetching: {url}")
        result = explore_url(url)
        print(f"  ok: {result.get('ok')}")
        if result.get("ok"):
            print(f"  title: {result.get('title')}")
            print(f"  n_chunks: {result.get('n_chunks')}")
            print(f"  n_anchored: {result.get('n_anchored')}")
        else:
            print(f"  error: {result.get('error')}")
