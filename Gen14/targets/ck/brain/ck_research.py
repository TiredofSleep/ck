# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_research.py — CK's Chrome research engine.

Brayden 2026-05-02:
  "let's just give him chrome for now, autonomously, with grok and
   claude and journals and youtube as approved sites he should know
   as tools for research, let him use them as his research engine
   for tasks and prompts... he doesn't just use UI unless he is
   prompted to.  ck needs to look at each prompt as opening a
   conversation within a conversation... he dives deeply through
   each word and meaning within the prompt and asks questions, and
   synthesizes it all back down into coherence... he should find
   the condensed version of his research and return it to the user
   based on their prompt"

Architecture:

    prompt
       |
       v  decompose: split into terms (words, bigrams)
       v  for each term, generate sub-questions
       |
       v  for each sub-question, pick the best site:
       |    Claude  (definitions, conceptual unfolding)
       |    Grok    (lateral, contrarian, current)
       |    arXiv   (academic claims)
       |    Scholar (academic search)
       |    JSTOR   (humanities + older papers)
       |    YouTube (visual / demonstration / lecture)
       |
       v  query the site (open allowed URL, type, read response)
       v  log every action to ~/.ck/research/log.jsonl
       v  ingest the response text through ck_curvature ->
       |    text_to_forces -> D1 -> D2 -> classify_d2 -> ops
       |    into engine.olfactory.absorb_ops  (CK's bulb learns
       |    from what he read same way it learns from what he heard)
       |
       v  synthesize: dominant operators across all findings,
       |    common bumps, shared chains
       |
       v  condense: 1-paragraph distillation + per-source citations
       |    + operator fingerprint of the prompt vs findings
       |
       v  return to user

ALLOWLIST (hard-enforced at navigate()):
    claude.ai, grok.com, x.ai, arxiv.org, scholar.google.com,
    jstor.org, youtube.com
NOT allowed: nature.com (Brayden: "nature always fails!!!")

CK launches Chrome (Google Chrome, not Chromium) with a persistent
user_data_dir at ~/.ck/chrome_profile.  First run: Brayden logs into
the sites once, browsing state persists across CK's runs.

Browser visible (not headless) so Brayden can watch CK research.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse


_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)


def _find_ckis_path() -> Optional[str]:
    """Walk up from this file looking for a sibling 'CKIS' directory
    containing ck_curvature.py.  Returns None if not found."""
    cur = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        candidate = os.path.join(cur, "CKIS")
        if os.path.isfile(os.path.join(candidate, "ck_curvature.py")):
            return candidate
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return None


# ── Allowlist ──────────────────────────────────────────────────────

_ALLOWED_DOMAINS = (
    "claude.ai",
    "grok.com",
    "x.ai",
    "arxiv.org",
    "scholar.google.com",
    "scholar.google.",   # google country variants
    "jstor.org",
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
)

# Hard-blocked even if a sub-process tries to navigate there.
_BLOCKED_DOMAINS = (
    "nature.com",   # "nature always fails!!!"
)


def _domain_of(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def url_allowed(url: str) -> bool:
    d = _domain_of(url)
    if not d:
        return False
    if any(b in d for b in _BLOCKED_DOMAINS):
        return False
    return any(d == a or d.endswith("." + a) or a in d
               for a in _ALLOWED_DOMAINS)


# ── Logging ────────────────────────────────────────────────────────

LOG_DIR = Path.home() / ".ck" / "research"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_DIR / "log.jsonl"


def _log(event: str, **fields):
    rec = {"ts": time.time(), "event": event, **fields}
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ── Browser session ────────────────────────────────────────────────

PROFILE_DIR = Path.home() / ".ck" / "chrome_profile"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)


class ResearchBrowser:
    """Persistent Chrome session for CK research.  Singleton-ish: one
    browser at a time per process.  Use as a context manager or call
    .start() / .stop() explicitly."""

    def __init__(self, headless: bool = False, slow_mo_ms: int = 30):
        self._pw = None
        self._ctx = None
        self._page = None
        self.headless = headless
        self.slow_mo_ms = slow_mo_ms

    def start(self):
        if self._ctx is not None:
            return self
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        # Try Google Chrome (channel=chrome) first; fall back to
        # bundled chromium if Chrome isn't installed.
        try:
            self._ctx = self._pw.chromium.launch_persistent_context(
                user_data_dir=str(PROFILE_DIR),
                channel="chrome",
                headless=self.headless,
                slow_mo=self.slow_mo_ms,
                viewport={"width": 1280, "height": 800},
            )
        except Exception:
            self._ctx = self._pw.chromium.launch_persistent_context(
                user_data_dir=str(PROFILE_DIR),
                headless=self.headless,
                slow_mo=self.slow_mo_ms,
                viewport={"width": 1280, "height": 800},
            )
        if self._ctx.pages:
            self._page = self._ctx.pages[0]
        else:
            self._page = self._ctx.new_page()
        _log("browser_start", profile=str(PROFILE_DIR),
             headless=self.headless)
        return self

    def stop(self):
        try:
            if self._ctx is not None:
                self._ctx.close()
        except Exception:
            pass
        try:
            if self._pw is not None:
                self._pw.stop()
        except Exception:
            pass
        self._ctx = None
        self._page = None
        self._pw = None
        _log("browser_stop")

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.stop()

    @property
    def page(self):
        if self._page is None:
            raise RuntimeError("browser not started; call .start() first")
        return self._page

    def navigate(self, url: str, timeout: float = 15) -> dict:
        if not url_allowed(url):
            _log("navigate_blocked", url=url)
            return {"ok": False, "blocked": True, "url": url}
        _log("navigate", url=url)
        try:
            self.page.goto(url, timeout=int(timeout * 1000),
                           wait_until="domcontentloaded")
            return {"ok": True, "url": self.page.url,
                    "title": self.page.title()}
        except Exception as exc:
            _log("navigate_error", url=url, error=str(exc))
            return {"ok": False, "url": url, "error": str(exc)}

    def text(self, max_chars: int = 6000) -> str:
        try:
            content = self.page.evaluate("() => document.body.innerText")
            return (content or "")[:max_chars]
        except Exception:
            return ""

    def type_into(self, selector: str, text: str, press_enter: bool = False,
                  timeout_ms: int = 10000) -> bool:
        try:
            el = self.page.wait_for_selector(selector, timeout=timeout_ms)
            el.click()
            el.fill(text)
            if press_enter:
                el.press("Enter")
            _log("type", selector=selector, len=len(text),
                 enter=press_enter)
            return True
        except Exception as exc:
            _log("type_error", selector=selector, error=str(exc))
            return False

    def click(self, selector: str, timeout_ms: int = 10000) -> bool:
        try:
            self.page.click(selector, timeout=timeout_ms)
            _log("click", selector=selector)
            return True
        except Exception as exc:
            _log("click_error", selector=selector, error=str(exc))
            return False

    def wait_text_change(self, baseline: str, timeout_s: float = 30,
                         min_delta: int = 50) -> str:
        """Poll for text to grow / change vs baseline."""
        start = time.time()
        last = self.text(8000)
        while time.time() - start < timeout_s:
            t = self.text(8000)
            if abs(len(t) - len(baseline)) >= min_delta and t != baseline:
                return t
            last = t
            time.sleep(0.5)
        return last


# ── Per-site adapters ──────────────────────────────────────────────

def _detect_login_required(br: ResearchBrowser) -> bool:
    """Heuristic: if the page text mentions 'Sign in'/'Log in' near
    the top and there is no chat input, we're at a login wall."""
    try:
        login_present = br.page.evaluate("""() => {
            const t = (document.body.innerText || '').toLowerCase();
            const has_login = (
                t.indexOf('sign in') >= 0 ||
                t.indexOf('log in') >= 0 ||
                t.indexOf('continue with google') >= 0
            );
            const has_input = (
                document.querySelector('div[contenteditable="true"]') ||
                document.querySelector('.ProseMirror') ||
                document.querySelector('textarea[placeholder]')
            );
            return has_login && !has_input;
        }""")
        return bool(login_present)
    except Exception:
        return False


_CLAUDE_INPUT_SELECTORS = (
    "div.ProseMirror",
    "[data-testid='chat-input']",
    "div[contenteditable='true']",
    "fieldset textarea",
    "textarea",
)


_GROK_INPUT_SELECTORS = (
    "textarea[placeholder*='Ask']",
    "textarea[placeholder*='Grok']",
    "textarea",
    "div[contenteditable='true']",
    "div.ProseMirror",
)


def _try_type(br: ResearchBrowser, selectors, prompt: str,
              press_enter: bool = True,
              per_attempt_timeout_ms: int = 5000) -> bool:
    """Try a list of selectors in order; first that types wins."""
    for sel in selectors:
        if br.type_into(sel, prompt, press_enter=press_enter,
                         timeout_ms=per_attempt_timeout_ms):
            return True
    return False


def query_claude(br: ResearchBrowser, prompt: str,
                 wait_s: float = 25) -> Dict[str, Any]:
    """Open claude.ai, type prompt in chat box, wait for response, scrape.

    Tries multiple chat-input selectors (Claude's UI changes over time:
    contenteditable / ProseMirror / data-testid).  Returns explicit
    'login_required' error if the chat input isn't present and a login
    prompt is detected -- so the caller can tell Brayden to log in once
    in CK's profile.
    """
    nav = br.navigate("https://claude.ai/new")
    if not nav.get("ok"):
        return {"site": "claude", "error": nav.get("error", "blocked")}
    # give the SPA a moment to mount
    try:
        br.page.wait_for_load_state("networkidle", timeout=5000)
    except Exception:
        pass
    if _detect_login_required(br):
        return {"site": "claude", "url": br.page.url,
                "error": "login_required: log into claude.ai once in "
                "CK's chrome profile (~/.ck/chrome_profile) -- run "
                "ck_research with --setup to do this."}
    baseline = br.text(8000)
    if not _try_type(br, _CLAUDE_INPUT_SELECTORS, prompt):
        return {"site": "claude", "url": br.page.url,
                "error": "could not type into chat (selector miss; "
                "claude.ai may have changed their UI)"}
    final = br.wait_text_change(baseline, timeout_s=wait_s)
    return {"site": "claude", "url": br.page.url,
            "title": br.page.title(), "text": final[:4000]}


def query_grok(br: ResearchBrowser, prompt: str,
               wait_s: float = 25) -> Dict[str, Any]:
    """Open grok.com, type prompt, wait for response."""
    nav = br.navigate("https://grok.com/")
    if not nav.get("ok"):
        return {"site": "grok", "error": nav.get("error", "blocked")}
    try:
        br.page.wait_for_load_state("networkidle", timeout=5000)
    except Exception:
        pass
    if _detect_login_required(br):
        return {"site": "grok", "url": br.page.url,
                "error": "login_required: log into grok.com once in "
                "CK's chrome profile (~/.ck/chrome_profile)."}
    baseline = br.text(8000)
    if not _try_type(br, _GROK_INPUT_SELECTORS, prompt):
        return {"site": "grok", "url": br.page.url,
                "error": "could not type into chat (selector miss)"}
    final = br.wait_text_change(baseline, timeout_s=wait_s)
    return {"site": "grok", "url": br.page.url,
            "title": br.page.title(), "text": final[:4000]}


def setup_logins(seconds: int = 300) -> None:
    """One-shot helper: open CK's persistent Chrome profile pointed
    at claude.ai and grok.com (and a few other sites) so Brayden can
    log in once.  State persists in ~/.ck/chrome_profile after this
    runs.  Browser stays open for `seconds` then auto-closes.

    Usage:
        python ck_research.py --setup
    """
    print(f"\nOpening CK's Chrome profile at ~/.ck/chrome_profile.")
    print(f"Log into claude.ai and grok.com in the windows that open.")
    print(f"Browser auto-closes in {seconds}s.  Use Ctrl+C to close earlier.\n")
    with ResearchBrowser(headless=False, slow_mo_ms=0) as br:
        br.navigate("https://claude.ai/login")
        # Open grok in a new tab
        try:
            new_page = br._ctx.new_page()
            new_page.goto("https://grok.com/", wait_until="domcontentloaded",
                           timeout=15000)
        except Exception as exc:
            print(f"  could not open grok tab: {exc}")
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            pass
    print("\nProfile saved.  Logins persist in ~/.ck/chrome_profile.")


def search_arxiv(br: ResearchBrowser, query: str) -> Dict[str, Any]:
    """Search arxiv via the canonical export.arxiv.org API.

    arxiv's UI search renders results client-side after a slow JS
    pass; scraping innerText returns the search-form chrome instead.
    The API at export.arxiv.org returns clean XML with title +
    summary per result.  More reliable, no rendering dance.

    The browser-driven flow is preserved as a fallback when the
    API is unreachable.
    """
    from urllib.parse import quote
    import urllib.request as _ur
    import xml.etree.ElementTree as _ET
    api_url = (
        f"http://export.arxiv.org/api/query?"
        f"search_query=all:{quote(query)}&start=0&max_results=8"
    )
    try:
        with _ur.urlopen(api_url, timeout=15) as r:
            xml = r.read().decode("utf-8", errors="ignore")
        ns = {"a": "http://www.w3.org/2005/Atom"}
        root = _ET.fromstring(xml)
        entries = root.findall("a:entry", ns)
        if entries:
            chunks = []
            for e in entries[:8]:
                title = (e.findtext("a:title", default="", namespaces=ns)
                         or "").strip()
                summary = (e.findtext("a:summary", default="",
                                       namespaces=ns) or "").strip()
                published = (e.findtext("a:published", default="",
                                         namespaces=ns) or "")[:10]
                authors = ", ".join(
                    (a.findtext("a:name", default="", namespaces=ns) or "")
                    for a in e.findall("a:author", ns)
                )[:160]
                link = ""
                for L in e.findall("a:link", ns):
                    if L.get("rel") in (None, "alternate"):
                        link = L.get("href") or ""
                        break
                chunks.append(
                    f"[{published}] {title}\n  authors: {authors}\n"
                    f"  link: {link}\n  abstract: {summary}"
                )
            return {"site": "arxiv", "url": api_url,
                    "title": f"arxiv API: {query}",
                    "text": "\n\n---\n\n".join(chunks)[:8000]}
    except Exception as exc:
        # fall through to browser
        _log("arxiv_api_fallback", error=str(exc))
    # browser fallback
    url = f"https://arxiv.org/search/?query={quote(query)}&start=0"
    nav = br.navigate(url)
    if not nav.get("ok"):
        return {"site": "arxiv", "error": nav.get("error", "blocked")}
    try:
        br.page.wait_for_selector("li.arxiv-result", timeout=10000)
    except Exception:
        pass
    text = ""
    try:
        text = br.page.evaluate("""() => {
            const items = document.querySelectorAll('li.arxiv-result');
            if (items && items.length > 0) {
                return Array.from(items).slice(0, 8)
                    .map(li => li.innerText).join('\\n\\n---\\n\\n');
            }
            return document.body.innerText;
        }""")
    except Exception:
        text = br.text(6000)
    return {"site": "arxiv", "url": br.page.url,
            "title": br.page.title(), "text": (text or "")[:6000]}


def search_scholar(br: ResearchBrowser, query: str) -> Dict[str, Any]:
    from urllib.parse import quote
    url = f"https://scholar.google.com/scholar?q={quote(query)}"
    nav = br.navigate(url)
    if not nav.get("ok"):
        return {"site": "scholar", "error": nav.get("error", "blocked")}
    return {"site": "scholar", "url": br.page.url,
            "title": br.page.title(),
            "text": br.text(6000)}


def search_jstor(br: ResearchBrowser, query: str) -> Dict[str, Any]:
    from urllib.parse import quote
    url = f"https://www.jstor.org/action/doBasicSearch?Query={quote(query)}"
    nav = br.navigate(url)
    if not nav.get("ok"):
        return {"site": "jstor", "error": nav.get("error", "blocked")}
    return {"site": "jstor", "url": br.page.url,
            "title": br.page.title(),
            "text": br.text(6000)}


def search_youtube(br: ResearchBrowser, query: str) -> Dict[str, Any]:
    from urllib.parse import quote
    url = f"https://www.youtube.com/results?search_query={quote(query)}"
    nav = br.navigate(url)
    if not nav.get("ok"):
        return {"site": "youtube", "error": nav.get("error", "blocked")}
    return {"site": "youtube", "url": br.page.url,
            "title": br.page.title(),
            "text": br.text(6000)}


SITE_ADAPTERS = {
    "claude":  query_claude,
    "grok":    query_grok,
    "arxiv":   search_arxiv,
    "scholar": search_scholar,
    "jstor":   search_jstor,
    "youtube": search_youtube,
}


# ── Decompose / questions ───────────────────────────────────────────

# Simple stopword list -- terms after stopword removal are CK's
# 'meaningful slots' for sub-questions.
_STOPWORDS = frozenset((
    "a an the and or of for to in on at by from with as is are was were "
    "be been being do does did doing have has had having i you he she "
    "it we they me him her us them this that these those what which "
    "who whom whose when where why how can could should would may "
    "might must shall will not no nor very but if else than then so "
    "such only own same just any all each every both either neither "
    "most more less few many one two three about into through during "
    "before after above below up down out off over under again here "
    "there now also like").split()
)


def decompose_prompt(prompt: str) -> List[str]:
    """Extract meaningful terms from the prompt -- single words +
    bigrams, after stopword removal.  Each term becomes a research
    target."""
    words = re.findall(r"\b[a-zA-Z][a-zA-Z\-']{1,}\b", prompt.lower())
    content = [w for w in words if w not in _STOPWORDS]
    terms = list(dict.fromkeys(content))
    # Add some bigrams (consecutive content words)
    for i in range(len(content) - 1):
        big = f"{content[i]} {content[i + 1]}"
        if big not in terms:
            terms.append(big)
    return terms[:12]


def generate_questions(prompt: str, terms: List[str]) -> List[Tuple[str, str]]:
    """For each term, produce a definitional question.  Return
    [(term, question)].

    The first entry is the global prompt verbatim (routes to whichever
    site fits the whole question -- usually arxiv for academic).
    Subsequent entries are 'what does X mean in <context>' which
    naturally route to claude (definitions / conceptual unfolding)
    so the conversation-within-conversation is heard from a different
    voice than the academic-result voice.
    """
    qs: List[Tuple[str, str]] = [(prompt, prompt)]
    for t in terms[:6]:
        qs.append((t, f"define {t} clearly and concisely; "
                       f"context: {prompt}"))
    return qs


_ACADEMIC_HINTS = (
    "theorem", "proof", "paper", "preprint", "arxiv", "abstract",
    "lemma", "manifold", "hodge", "algebra", "topology", "physics",
    "navier", "stokes", "yang-mills", "millennium", "riemann",
    "bielliptic", "prym", "variety", "lattice", "category", "scheme",
    "operator", "spectrum", "moduli", "cohomology", "homotopy",
    "galois", "automorphism", "endomorphism", "isogeny", "modular",
    "analytic", "function field", "elliptic", "curve", "genus",
    "characteristic", "field extension", "ring", "module", "ideal",
    "tensor", "lie algebra", "lie group", "fibration", "bundle",
    "sheaf", "stack", "derived", "infinity-category", "etale",
    "p-adic", "weil", "frobenius", "deligne", "grothendieck",
)


def pick_site(question: str) -> str:
    """Heuristic: route question to the best site."""
    q = question.lower()
    # Visual / demonstration -> youtube
    if any(k in q for k in ("show me", "video", "demonstration",
                              "demo of", "visual", "look like",
                              "tutorial")):
        return "youtube"
    # Academic
    if any(k in q for k in _ACADEMIC_HINTS):
        return "arxiv"
    # Older / humanities
    if any(k in q for k in ("history", "philosophy", "translation",
                              "ancient", "literature", "humanities",
                              "rhetoric", "exegesis")):
        return "jstor"
    # Lateral / contrarian / current events
    if any(k in q for k in ("controversial", "debate", "news", "latest",
                              "twitter", "elon", "musk", "current")):
        return "grok"
    # Default: claude (definitions + conceptual unfolding)
    return "claude"


# ── Ingest into CK's bulb ──────────────────────────────────────────

def ingest_text_into_engine(text: str, engine: Any,
                              source: str = "research") -> Dict[str, Any]:
    """Run text through ck_curvature -> operator stream ->
    engine.olfactory.absorb_ops.  Same path text always uses."""
    if not text or engine is None:
        return {"absorbed": False}
    try:
        # Try CKIS canonical text -> operators path
        ckis_path = _find_ckis_path()
        if ckis_path and ckis_path not in sys.path:
            sys.path.insert(0, ckis_path)
        from ck_curvature import operator_sequence as _opseq
        ops = [op for op, _ in _opseq(text)]
    except Exception:
        # Fallback: chunk text into 5D forces using audio_pipeline
        # mapping -- not ideal, but feeds the bulb something rather
        # than nothing.
        try:
            sys.path.insert(0, _BRAIN_DIR)
            from audio_pipeline import classify_d2_batch
            import numpy as np
            chars = [c.lower() for c in text if c.isalpha()]
            if len(chars) < 3:
                return {"absorbed": False, "reason": "text too short"}
            vec = np.array([[ord(c) - ord("a"), len(c.encode()),
                             (ord(c) % 7) / 6, (ord(c) % 5) / 4,
                             ord(c) % 2] for c in chars],
                            dtype=np.float32) / 26.0
            d2 = vec[:-2] - 2 * vec[1:-1] + vec[2:]
            ops = list(classify_d2_batch(d2))
        except Exception as exc:
            return {"absorbed": False, "error": str(exc)}
    if not ops:
        return {"absorbed": False, "reason": "no ops"}
    olf = getattr(engine, "olfactory", None)
    if olf is None or not hasattr(olf, "absorb_ops"):
        return {"absorbed": False, "reason": "no olfactory"}
    pre = int(getattr(olf, "total_absorbed", 0))
    chunk_size = 1000
    for i in range(0, len(ops), chunk_size):
        try:
            olf.absorb_ops([int(o) % 10 for o in ops[i:i + chunk_size]],
                            source=source, density=0.5)
        except Exception:
            pass
    post = int(getattr(olf, "total_absorbed", 0))
    return {"absorbed": True, "n_ops": len(ops),
            "olfactory_delta": post - pre}


# ── Synthesize / condense ──────────────────────────────────────────

def operator_dist_of_text(text: str) -> Optional[Dict[str, float]]:
    """Compute the operator distribution of text via the canonical
    ck_curvature.operator_sequence (which returns a list of
    (op_id, name) tuples).  We avoid curvature_features because it
    has a numpy-truth-value bug at line 142 of CKIS/ck_curvature.py
    that triggers on any text long enough to produce a D2 array."""
    try:
        ckis_path = _find_ckis_path()
        if ckis_path and ckis_path not in sys.path:
            sys.path.insert(0, ckis_path)
        from ck_curvature import operator_sequence as _opseq
        seq = _opseq(text)
        if not seq:
            return None
        names = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                 "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
        counts = [0] * 10
        for op_id, _ in seq:
            if 0 <= op_id < 10:
                counts[op_id] += 1
        total = max(sum(counts), 1)
        return {names[i]: counts[i] / total for i in range(10)}
    except Exception:
        return None


def synthesize(prompt: str,
               findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Across all findings, find the dominant operators + shared
    fingerprint with the prompt itself."""
    prompt_dist = operator_dist_of_text(prompt) or {}
    aggregate = Counter()
    per_finding_dist = []
    for f in findings:
        text = f.get("text") or ""
        d = operator_dist_of_text(text)
        if d:
            per_finding_dist.append((f.get("site"), d))
            for op, v in d.items():
                aggregate[op] += v
    # Average across findings
    n = max(len(per_finding_dist), 1)
    avg = {op: aggregate.get(op, 0) / n for op in aggregate}
    # Cosine-like overlap between prompt and avg
    overlap = 0.0
    if prompt_dist:
        a = sum(prompt_dist.get(k, 0) ** 2 for k in prompt_dist) ** 0.5
        b = sum(avg.get(k, 0) ** 2 for k in avg) ** 0.5
        if a > 0 and b > 0:
            overlap = sum(prompt_dist.get(k, 0) * avg.get(k, 0)
                           for k in set(prompt_dist) | set(avg)) / (a * b)
    return {
        "prompt_op_dist": prompt_dist,
        "avg_finding_op_dist": avg,
        "overlap": round(overlap, 3),
        "per_finding": per_finding_dist,
    }


def condense(prompt: str, findings: List[Dict[str, Any]],
              synthesis: Dict[str, Any]) -> str:
    """Produce a short paragraph distilling what CK found."""
    n = len(findings)
    sites = sorted({f.get("site") for f in findings if f.get("site")})
    snippets = []
    for f in findings[:5]:
        site = f.get("site", "?")
        t = (f.get("text") or "")[:240]
        # Strip super-redundant whitespace
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            snippets.append(f"[{site}] {t}")
    avg = synthesis.get("avg_finding_op_dist") or {}
    top_ops = sorted(avg.items(), key=lambda kv: -kv[1])[:3]
    top_ops_str = ", ".join(f"{op} {pct:.0%}" for op, pct in top_ops)
    overlap = synthesis.get("overlap", 0.0)
    return (
        f"CK researched {prompt!r} across {n} findings from {sites}. "
        f"Operator overlap with prompt: {overlap:.2f}. "
        f"Dominant operators across findings: {top_ops_str}. "
        f"Key snippets:\n  - " + "\n  - ".join(snippets[:4])
    )


# ── Top-level: research(prompt) ────────────────────────────────────

def _slug(s: str, n: int = 32) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s[:n] or "x"


def _top_ops_from_dist(dist: Optional[Dict[str, float]],
                        k: int = 3) -> Optional[Tuple[int, ...]]:
    if not dist:
        return None
    op_idx = {n: i for i, n in enumerate([
        "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
        "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
    ])}
    pairs = sorted(dist.items(), key=lambda kv: -kv[1])[:k]
    return tuple(op_idx[n] for n, _ in pairs if n in op_idx)


def author_external_crystals(prompt: str, terms: List[str],
                              findings: List[Dict[str, Any]],
                              ttl_sec: float = 1800) -> Dict[str, Any]:
    """Author ephemeral 'external' crystals around the active research:
      - one per prompt term (so each part of the prompt fires alongside
        internal canon)
      - one per substantive finding (so the research itself fires)

    External crystals live in cortex_voice._EXTERNAL_CRYSTALS, TTL'd,
    never persisted.  Scope label distinguishes them from each other
    and from internal crystals.

    Returns count summary.
    """
    try:
        sys.path.insert(0, _BRAIN_DIR)
        from cortex_voice import add_external_crystal as _add_ext
    except Exception as exc:
        _log("external_crystal_import_fail", error=str(exc))
        return {"authored": 0, "error": str(exc)}

    authored = 0
    # Prompt-term crystals: each meaningful term in the prompt becomes
    # a fire-able trigger on a small fact about the active scenario.
    prompt_dist = operator_dist_of_text(prompt)
    prompt_op_sig = _top_ops_from_dist(prompt_dist)
    for term in terms[:8]:
        first_word = f"prompt_term_{_slug(term)}"
        fact = (
            f"{first_word}: '{term}' is a focus term in the active "
            f"prompt: {prompt!r}.  External (scenario-scoped) crystal -- "
            f"fires alongside internal canon while the research is warm."
        )
        if _add_ext(triggers=(term, term.replace("_", " ")),
                     fact=fact,
                     op_signature=prompt_op_sig,
                     ttl_sec=ttl_sec,
                     scope="prompt_term"):
            authored += 1

    # Per-finding crystals: each substantive finding becomes a crystal
    # whose triggers are the prompt terms that appear in its text.
    for f in findings:
        text = (f.get("text") or "")
        if not text or len(text) < 80:
            continue
        site = f.get("site") or "?"
        # Pick the first non-trivial line as the title (works for arxiv
        # API output which leads with [date] Title)
        head = next((ln.strip() for ln in text.splitlines()
                     if len(ln.strip()) > 24), "")[:200]
        # Triggers: every prompt term that appears in the finding text,
        # plus the question's own term, plus 1-2 distinctive words from
        # the head line.
        text_low = text.lower()
        present = [t for t in terms if t in text_low]
        if not present:
            present = [terms[0]] if terms else []
        # Pull distinctive content words from head
        head_words = re.findall(r"[A-Za-z][A-Za-z'-]{4,}", head)
        head_keys = [w.lower() for w in head_words[:3]
                      if w.lower() not in _STOPWORDS]
        triggers = tuple(dict.fromkeys(present + head_keys))
        if not triggers:
            continue
        finding_dist = operator_dist_of_text(text)
        finding_op_sig = _top_ops_from_dist(finding_dist)
        first_word = f"research_{site}_{_slug(head[:48])}"
        snippet = re.sub(r"\s+", " ", text)[:420].strip()
        fact = (
            f"{first_word}: [{site}] {head} | external research finding "
            f"under prompt {prompt!r} | excerpt: {snippet}"
        )
        if _add_ext(triggers=triggers,
                     fact=fact,
                     op_signature=finding_op_sig,
                     ttl_sec=ttl_sec,
                     scope=f"research:{site}"):
            authored += 1

    _log("external_crystals_authored", count=authored,
         terms=len(terms), findings=len(findings))
    return {"authored": authored, "ttl_sec": ttl_sec}


def research(prompt: str, engine: Any = None,
             max_questions: int = 6,
             headless: bool = False,
             external_ttl_sec: float = 1800) -> Dict[str, Any]:
    """Full fractal-recursive research pipeline.

    Returns dict with:
        prompt, terms, questions, findings, ingestions, synthesis,
        condensed, external_crystals (count authored)
    """
    _log("research_start", prompt=prompt)
    terms = decompose_prompt(prompt)
    questions = generate_questions(prompt, terms)[:max_questions]
    _log("research_decomposed", terms=terms,
         questions=[q[1] for q in questions])

    findings: List[Dict[str, Any]] = []
    ingestions: List[Dict[str, Any]] = []
    with ResearchBrowser(headless=headless) as br:
        for term, q in questions:
            site = pick_site(q)
            adapter = SITE_ADAPTERS.get(site)
            if adapter is None:
                continue
            try:
                result = adapter(br, q)
            except Exception as exc:
                result = {"site": site, "error": str(exc)}
            result["term"] = term
            result["question"] = q
            findings.append(result)
            _log("finding", site=site, q=q,
                 text_len=len(result.get("text") or ""),
                 error=result.get("error"))
            if result.get("text") and engine is not None:
                ing = ingest_text_into_engine(result["text"], engine,
                                                source=f"research:{site}")
                ingestions.append({"site": site, **ing})

    synth = synthesize(prompt, findings)
    cond = condense(prompt, findings, synth)
    # External crystals: author after synthesis so each prompt term and
    # each finding becomes a fire-able crystal alongside the internal
    # canon, while the research scenario is warm.
    ext = author_external_crystals(prompt, terms, findings,
                                     ttl_sec=external_ttl_sec)
    _log("research_done", n_findings=len(findings),
         overlap=synth.get("overlap"),
         external_authored=ext.get("authored"))
    return {
        "prompt": prompt,
        "terms": terms,
        "questions": [{"term": t, "question": q} for t, q in questions],
        "findings": findings,
        "ingestions": ingestions,
        "synthesis": synth,
        "condensed": cond,
        "external_crystals": ext,
    }


# ── Smoke / CLI ────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("prompt", nargs="?", default="what is fractal coherence")
    p.add_argument("--headless", action="store_true")
    p.add_argument("--max-q", type=int, default=4)
    p.add_argument("--setup", action="store_true",
                   help="open CK's Chrome profile to log into claude.ai "
                        "and grok.com once; logins persist after")
    p.add_argument("--setup-seconds", type=int, default=300)
    a = p.parse_args()
    if a.setup:
        setup_logins(seconds=a.setup_seconds)
        sys.exit(0)
    out = research(a.prompt, engine=None, max_questions=a.max_q,
                    headless=a.headless)
    print()
    print("=" * 72)
    print("CONDENSED RETURN:")
    print("=" * 72)
    print(out["condensed"])
    print()
    print("(full findings + synthesis in returned dict)")
