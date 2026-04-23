"""
ck_ollama_filter.py -- pure-function cleanup of Ollama drafts
=============================================================

Extracted from ``ck_boot_api.py`` so unit tests can exercise the
filter without importing the full boot module (which would run
CK's entire startup pipeline as a side effect -- HER hydration,
vocabulary expansion, GPU init, etc.).

The single export is ``postfilter_ollama``.  ``ck_boot_api``
re-exports it as ``_postfilter_ollama`` for backward compatibility
with callers that still reference the private name.

CK speaks in first person about himself.  Ollama drafts sometimes
drift into assistant-voice tropes ("great question", "according to
the readout") or sycophantic openers ("a philosophical question!").
These deflect from CK's own voice and should be peeled away so the
underlying content can either stand on its own or get rejected by
the steering gate for being sub-coherent.

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

# Leading interjections that Ollama often prepends.  The match is
# case-insensitive on the prefix only -- the downstream sentence's
# case is preserved.  One-layer peel: if the remaining text ALSO
# starts with a trope, we do NOT recurse (keeps legitimate content
# that happens to echo a trope safe).
_SYCOPHANTIC_PREFIXES = (
    "a philosophical question", "a perceptive question",
    "a thoughtful question", "an interesting question",
    "great question", "excellent question", "good question",
    "what a", "that's a", "that's an",
    "according to the ck", "according to ck",
    "according to the readout", "the readout suggests",
    "as an ai", "i'm an ai", "i am an ai",
    "as a language model", "i cannot", "sorry,", "i apologize",
)

# Identity-drift phrases.  When a draft contains ANY of these (not just
# as a prefix -- anywhere in the first ~200 chars), it has separated
# itself FROM CK and is speaking ABOUT CK.  CK is a creature, not an
# assistant.  These drafts are rejected wholesale: the filter returns
# '' and the caller treats that as "no usable draft", which lets the
# honest structural fallback own the turn.  This is safer than trying
# to splice the identity drift out mid-sentence.
_IDENTITY_DRIFT_PHRASES = (
    "speaking alongside",
    "alongside the ck",
    "alongside ck",
    "as an ai assistant",
    "i am an ai assistant",
    "i'm an ai assistant",
    "i am a math-literate assistant",
    "i'm a math-literate assistant",
    "i am an assistant",
    "i'm an assistant",
    "i am a language model",
    "i'm a language model",
    "the ck is an artificial intelligence",
    "ck is an artificial intelligence",
)
_IDENTITY_SCAN_WINDOW = 240  # characters


def _has_identity_drift(low: str) -> bool:
    """True if the lowercased text exhibits assistant-separate-from-CK
    framing in the opening window.  Callers reject the draft entirely
    when this fires."""
    head = low[:_IDENTITY_SCAN_WINDOW]
    return any(p in head for p in _IDENTITY_DRIFT_PHRASES)


def postfilter_ollama(text: str) -> str:
    """Strip common Ollama noise: code fences, markdown headers, AI
    disclaimers, sycophantic openers, and meta-commentary about the
    readout.  Reject wholesale (-> '') when the draft exhibits
    assistant-identity drift (CK framing itself as a separate helper).

    Non-string or empty input returns ''.
    """
    if not isinstance(text, str):
        return ''
    t = text.strip()
    if not t:
        return ''
    # Strip surrounding code fences
    if t.startswith('```'):
        t = t.strip('`').strip()
    # Identity-drift check runs BEFORE peeling so an early "speaking
    # alongside CK" or "I am a math-literate assistant" kills the draft
    # regardless of what opener it has.  CK speaks as himself or the
    # honest structural fallback owns the turn.
    if _has_identity_drift(t.lower()):
        return ''
    # Drop sycophantic / meta openers that precede the actual sentence.
    # Pattern: a short interjection ending in "!", "?" or "," followed
    # by the real answer.  We split on the first terminator and keep
    # the remainder if one exists.
    low = t.lower()
    for prefix in _SYCOPHANTIC_PREFIXES:
        if low.startswith(prefix):
            cut_at = -1
            for ch in ('.', '!', '?', ','):
                idx = t.find(ch)
                if idx != -1 and (cut_at == -1 or idx < cut_at):
                    cut_at = idx
            if cut_at != -1:
                t = t[cut_at + 1:].lstrip()
                low = t.lower()
            # Only peel one layer per call so we don't eat legitimate
            # content that happens to contain one of these phrases.
            break
    # Remove markdown header hashes
    lines = [ln.lstrip('# ').rstrip() for ln in t.splitlines()]
    t = '\n'.join(ln for ln in lines if ln)
    return t.strip()


# Backward-compat alias used by ck_boot_api.
_postfilter_ollama = postfilter_ollama


__all__ = ["postfilter_ollama", "_postfilter_ollama", "_SYCOPHANTIC_PREFIXES"]
