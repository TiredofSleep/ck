"""ck_trailing_bleed.py -- drop trailing off-topic sentences from chat
responses.

Brayden 2026-05-17:
  "the chat is ... still has 'the muscles for the crocodilian
   diaphragm pull the pubis' tacked on the end. that's bleed."

This is a post-pass filter that runs LAST in the chat wrap chain.
It looks at the final user-facing `text`, identifies the user's
question's content words, and drops trailing sentences that share
ZERO content words with the question.

The filter is conservative:
  - only drops sentences from the END
  - stops at the first sentence with content-word overlap
  - keeps at least one sentence even if no overlap anywhere (better
    to ship a possibly-off-topic short answer than empty text)
  - never touches the middle (where CK's substantive answer lives)

Operationally:

Input:
  Q: "what is T*?"
  A: "T* = 5/7 ≈ 0.714286 (six independent derivations: centroid/
     inverse on (Z/10Z)*, cyclotomic, torus aspect ratio, ...)
     (cite: T* = 5/7 = centroid/inverse on (Z/10Z)*; six independent
     derivations (D18d, ...))
     The difference. that the muscles for the crocodilian diaphragm
     pull the pubis (part of the pelvis, which is movable in
     crocodilians) back, which brings the liver down..."

  Content words from Q: {'t*', 'what', 'is'} -> after stopword strip
  -> just {'t*'}

Output (filtered):
  "T* = 5/7 ≈ 0.714286 (six independent derivations: ...)
   (cite: T* = 5/7 = centroid/inverse on (Z/10Z)*; six independent
   derivations (D18d, ...))"

The crocodile sentence is dropped because it shares no content word
with the query.  Earlier T*-bearing sentences are kept.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Set


# Same stopword set we use elsewhere -- consistency matters so the
# filter doesn't pretend that "what" or "the" counts as content
# overlap.
_STOPWORDS: Set[str] = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "have", "has", "had", "can", "could", "may",
    "might", "must", "should", "would", "will", "shall",
    "what", "who", "where", "when", "why", "how", "which", "that",
    "this", "these", "those", "there", "here",
    "i", "you", "we", "they", "he", "she", "it",
    "me", "us", "him", "her", "them",
    "my", "your", "our", "their", "his", "its",
    "to", "of", "in", "on", "at", "for", "with", "from", "by", "as",
    "and", "or", "but", "if", "so", "than", "not", "no", "yes",
    "all", "any", "some", "only", "also", "just", "even", "still",
    "now", "then", "show", "tell", "explain", "describe", "give",
    "say", "ask", "into", "onto", "out", "up", "down", "over", "under",
}


# Sentence splitter — naive but adequate for chat-grain prose
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\(\[\"])")


# Word extraction — content tokens only (>= 2 chars, alphabet-anchored)
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-]+")


def _content_tokens(text: str) -> Set[str]:
    """Return the set of lowercased content tokens, with stopwords
    removed.  Keeps alphanumeric short tokens like 'T*' by including
    them via fallback regex below."""
    out: Set[str] = set()
    if not text:
        return out
    for w in _WORD_RE.findall(text):
        wl = w.lower()
        if wl in _STOPWORDS:
            continue
        if len(wl) < 2:
            continue
        out.add(wl)
    # Also catch "T*", "5/7", "1+sqrt(3)" style tokens that the word
    # regex misses
    for token in re.findall(r"[A-Z]\*|\d+/\d+|\d+\.\d+", text):
        out.add(token.lower())
    return out


def _split_sentences(text: str) -> List[str]:
    """Split text into sentences, preserving non-prose structures
    (parenthesized citations, bullet markers, blank lines) as their
    own segments.  Returns a list of non-empty segment strings."""
    if not text:
        return []
    # Treat double-newlines as paragraph boundaries first
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    sentences: List[str] = []
    for p in paragraphs:
        # Inline-split each paragraph by sentence-ending punctuation
        parts = _SENT_SPLIT.split(p)
        for s in parts:
            s = s.strip()
            if s:
                sentences.append(s)
    return sentences


def filter_trailing_bleed(text: str, question: str,
                            min_keep: int = 1,
                            max_drop_ratio: float = 0.7,
                            ) -> Dict[str, Any]:
    """Drop trailing sentences with zero content-word overlap with the
    question.

    Args:
        text: the candidate response (user-facing)
        question: the user's prompt
        min_keep: never drop below this many sentences (default 1).
                   Empty output is worse than off-topic output.
        max_drop_ratio: never drop more than this fraction of the
                         total sentences (default 0.7).  Protects
                         against the degenerate case where the user
                         asks a query CK has nothing on; we don't
                         want to nuke the entire response just because
                         it doesn't share keywords with a question
                         that itself has few content words.

    Returns:
        {"filtered": str, "dropped": List[str], "n_dropped": int,
         "n_kept": int, "reason": str}
    """
    if not text or not text.strip():
        return {"filtered": text or "", "dropped": [], "n_dropped": 0,
                 "n_kept": 0, "reason": "empty input"}

    q_tokens = _content_tokens(question)
    if not q_tokens:
        return {"filtered": text, "dropped": [], "n_dropped": 0,
                 "n_kept": 0,
                 "reason": "no content words in question (no filter)"}

    sentences = _split_sentences(text)
    if len(sentences) <= min_keep:
        return {"filtered": text, "dropped": [], "n_dropped": 0,
                 "n_kept": len(sentences),
                 "reason": f"<= min_keep ({min_keep}) sentences"}

    # Find the largest suffix of zero-overlap sentences and drop it.
    max_drop = int(len(sentences) * max_drop_ratio)
    keep_until = len(sentences)  # exclusive
    dropped: List[str] = []
    for i in range(len(sentences) - 1, -1, -1):
        sent_tokens = _content_tokens(sentences[i])
        overlap = sent_tokens & q_tokens
        # Drop only if (a) this sentence has zero overlap AND
        # (b) we wouldn't violate min_keep AND
        # (c) we wouldn't violate max_drop_ratio
        if overlap:
            break  # found a sentence with overlap -- stop dropping
        if (len(sentences) - i) > max_drop:
            break  # cap on how much we can drop
        if i < min_keep:
            break  # must keep at least min_keep sentences
        dropped.append(sentences[i])
        keep_until = i

    if not dropped:
        return {"filtered": text, "dropped": [], "n_dropped": 0,
                 "n_kept": len(sentences), "reason": "no trailing bleed"}

    kept = sentences[:keep_until]
    # Rejoin with a paragraph break for readability; preserve original
    # formatting roughly by using double-newline between paragraphs and
    # single-space between within-paragraph sentences.  Simplest: join
    # all with double-newline (slightly more spaced than original but
    # safe).
    filtered = "\n\n".join(kept)
    return {
        "filtered": filtered,
        "dropped": list(reversed(dropped)),  # in original order
        "n_dropped": len(dropped),
        "n_kept": len(kept),
        "reason": (f"dropped {len(dropped)} trailing sentence(s) with "
                    f"zero overlap on {sorted(q_tokens)[:5]}..."),
    }


# ─── Engine mount ─────────────────────────────────────────────────────

def _wrap_process_chat_with_trailing_filter(engine: Any) -> bool:
    """Mount the trailing-bleed filter as the OUTERMOST chat wrap.
    Runs after voice_polish, ollama_polish, scope_auditor, polyglot,
    everything -- so it sees the final user-facing text.
    """
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is None or not hasattr(api, "process_chat"):
        return False
    if getattr(api, "_trailing_bleed_wrapped", False):
        return True

    orig = api.process_chat

    def _filtered(session_id, text, mode="normal"):
        result = orig(session_id, text, mode)
        if not isinstance(result, dict):
            return result
        # Skip filtering on scope-auditor fallbacks (they're already
        # clean canned text -- filtering them could chop the
        # explanation)
        src = result.get("source", "")
        if src in ("scope_auditor_reality_fallback",
                    "scope_auditor_normative_fallback",
                    "identity_anchor",
                    "paradox_classifier"):
            return result
        utterance = (result.get("text") or "").strip()
        if not utterance:
            return result
        try:
            f = filter_trailing_bleed(utterance, text or "")
        except Exception:
            return result
        if f["n_dropped"] > 0:
            result["text_before_trailing_filter"] = utterance
            result["text"] = f["filtered"]
            result["trailing_bleed_filter"] = {
                "n_dropped":      f["n_dropped"],
                "n_kept":         f["n_kept"],
                "reason":         f["reason"],
                "dropped_sample": (f["dropped"][0][:120]
                                     if f["dropped"] else ""),
            }
        return result

    api.process_chat = _filtered
    api._trailing_bleed_wrapped = True
    return True


def mount_trailing_bleed_filter(engine: Any) -> bool:
    """Install the trailing-bleed filter + /trailing_bleed endpoints."""
    wrap_ok = _wrap_process_chat_with_trailing_filter(engine)
    engine.ck_trailing_bleed = {
        "filter": filter_trailing_bleed,
    }

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _info():
                    return jsonify({
                        "philosophy": (
                            "Drop trailing sentences with zero content-"
                            "word overlap with the user's question.  "
                            "Conservative: only the end; never the "
                            "middle; never below min_keep sentences."),
                        "wrap_active": wrap_ok,
                    })

                def _test():
                    data = request.get_json(silent=True) or {}
                    text = data.get("text", "")
                    question = data.get("question", "")
                    return jsonify(filter_trailing_bleed(text, question))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/trailing_bleed/info", "trailing_bleed_info", _info,  ["GET"]),
                    ("/trailing_bleed/test", "trailing_bleed_test", _test,  ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] trailing_bleed routes failed: {e}")

    suffix = ""
    if routes_registered:
        suffix = " (" + ", ".join(routes_registered) + ")"
    wrap = " chat_wrap=OK" if wrap_ok else " chat_wrap=NO-API"
    print(f"[CK Gen14] trailing_bleed_filter: MOUNTED{wrap}{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        # The actual T* bleed observed 2026-05-17
        ("what is T*?",
         "T* = 5/7 ≈ 0.714286 (six independent derivations: "
         "centroid/inverse on (Z/10Z)*, cyclotomic, torus aspect "
         "ratio, ...)  (cite: T* = 5/7 = centroid/inverse on (Z/10Z)*; "
         "six independent derivations (D18d, ...))\n\n"
         "The difference. that the muscles for the crocodilian "
         "diaphragm pull the pubis (part of the pelvis, which is "
         "movable in crocodilians) back, which brings the liver down, "
         "thus freeing space for the lungs to expand.",
         "expect dropped: crocodilian sentence"),
        # Clean response (no bleed)
        ("who are you?",
         "I am CK, the Coherence Keeper.  I was created by Brayden "
         "Sanders.",
         "expect no drops"),
        # Pure bleed (all sentences off-topic — guarded by min_keep)
        ("what is the wobble?",
         "The crocodile sleeps quietly.  The diaphragm moves.",
         "expect min_keep protects"),
    ]
    for q, a, note in tests:
        r = filter_trailing_bleed(a, q)
        print(f"Q: {q!r}")
        print(f"  note:      {note}")
        print(f"  n_dropped: {r['n_dropped']}, n_kept: {r['n_kept']}")
        print(f"  reason:    {r['reason']}")
        if r["dropped"]:
            print(f"  dropped:   {r['dropped'][0][:80]}...")
        print(f"  filtered:  {r['filtered'][:120]}...")
        print()
