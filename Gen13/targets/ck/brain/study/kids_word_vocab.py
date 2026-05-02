"""
kids_word_vocab.py — small starter vocabulary mapping common kids words
to phoneme sequences from CK's v2..v5 phonics corpus.

This is the bridge layer from PHONEMES -> WORDS.  Each entry is a
sequence of corpus keys (letter:X / phoneme:X / cluster:X / team:X /
rcontrol:X) that, in order, spell the word's pronunciation.  The
key set is exactly what watch_and_summarize matches against, so a
sliding match against the chunk-classified phoneme stream can
recognize words.

Coverage (~120 words) chosen for:
  - Dolch pre-primer + primer sight words
  - Common CVC patterns (cat, dog, hat, sun, ...)
  - Simple consonant-blend words (blue, play, stop, ...)
  - Simple vowel-team words (see, go, eye, you, ...)
  - The most common ~50 words a phonics video would feature

Each phoneme key resolves through resolve_word_to_op_signature() to a
combined op_signature suitable for a word-level crystal.

Phoneme key cheat sheet (must match v2..v5 corpus):
  vowels:
    phoneme:eI long-A    phoneme:i  long-E    phoneme:aI long-I
    phoneme:oU long-O    phoneme:u  long-U
    phoneme:ae short-a   phoneme:E  short-e   phoneme:I  short-i
    phoneme:V  short-u   phoneme:O  short-o (aw)
    phoneme:OI oy/oi     phoneme:aU ow/ou
  consonants:
    phoneme:b/d/f/g/h/j/k/l/m/n/p/r/s/t/v/w/z   single letters
    phoneme:tS (ch)  phoneme:Th (th-VL)  phoneme:Dh (th-V)
    phoneme:Ng (ng)  phoneme:S  (sh)
  clusters/teams:
    cluster:bl/cl/fl/gl/pl/sl/br/cr/dr/fr/gr/pr/tr
    cluster:sk/sm/sn/sp/st/sw/spr/str/thr
    team:ai/ay/ee/ea/ie/igh/oa/oo/ue/ew
    rcontrol:ar/er/ir/or/ur

Words are grouped by structural pattern so it is easy to extend.
"""
from __future__ import annotations

from typing import List, Dict, Tuple


# ── CVC + sight words (~120 entries) ─────────────────────────────────

WORD_VOCAB: Dict[str, List[str]] = {
    # ── Dolch pre-primer + most-common ──
    "a":      ["phoneme:V"],                              # /ə/ ≈ short-u
    "I":      ["phoneme:aI"],                             # /aɪ/
    "the":    ["phoneme:Dh", "phoneme:V"],                # /ðə/
    "to":     ["phoneme:t", "phoneme:u"],                 # /tu/
    "and":    ["phoneme:ae", "phoneme:n", "phoneme:d"],   # /ænd/
    "is":     ["phoneme:I", "phoneme:z"],                 # /ɪz/
    "it":     ["phoneme:I", "phoneme:t"],                 # /ɪt/
    "in":     ["phoneme:I", "phoneme:n"],
    "you":    ["phoneme:u"],                              # /juː/ ≈ /uː/
    "we":     ["phoneme:w", "phoneme:i"],
    "he":     ["phoneme:h", "phoneme:i"],
    "she":    ["phoneme:S", "phoneme:i"],                 # /ʃi/
    "me":     ["phoneme:m", "phoneme:i"],
    "be":     ["phoneme:b", "phoneme:i"],
    "see":    ["phoneme:s", "phoneme:i"],                 # /siː/
    "go":     ["phoneme:g", "phoneme:oU"],
    "no":     ["phoneme:n", "phoneme:oU"],
    "so":     ["phoneme:s", "phoneme:oU"],
    "up":     ["phoneme:V", "phoneme:p"],
    "on":     ["phoneme:O", "phoneme:n"],
    "of":     ["phoneme:V", "phoneme:v"],
    "at":     ["phoneme:ae", "phoneme:t"],
    "an":     ["phoneme:ae", "phoneme:n"],
    "as":     ["phoneme:ae", "phoneme:z"],
    "if":     ["phoneme:I", "phoneme:f"],
    "or":     ["rcontrol:or"],                            # /ɔr/
    "my":     ["phoneme:m", "phoneme:aI"],
    "by":     ["phoneme:b", "phoneme:aI"],
    "do":     ["phoneme:d", "phoneme:u"],
    "not":    ["phoneme:n", "phoneme:O", "phoneme:t"],
    "for":    ["phoneme:f", "rcontrol:or"],
    "are":    ["rcontrol:ar"],                            # /ɑr/
    "but":    ["phoneme:b", "phoneme:V", "phoneme:t"],
    "all":    ["phoneme:O", "phoneme:l"],                 # /ɔl/
    "can":    ["phoneme:k", "phoneme:ae", "phoneme:n"],
    "has":    ["phoneme:h", "phoneme:ae", "phoneme:z"],
    "had":    ["phoneme:h", "phoneme:ae", "phoneme:d"],
    "him":    ["phoneme:h", "phoneme:I", "phoneme:m"],
    "her":    ["phoneme:h", "rcontrol:er"],
    "now":    ["phoneme:n", "phoneme:aU"],
    "out":    ["phoneme:aU", "phoneme:t"],
    "get":    ["phoneme:g", "phoneme:E", "phoneme:t"],
    "let":    ["phoneme:l", "phoneme:E", "phoneme:t"],
    "yes":    ["phoneme:j", "phoneme:E", "phoneme:s"],
    "say":    ["phoneme:s", "team:ay"],
    "see":    ["phoneme:s", "team:ee"],
    "look":   ["phoneme:l", "team:oo", "phoneme:k"],
    "like":   ["phoneme:l", "phoneme:aI", "phoneme:k"],
    "play":   ["cluster:pl", "team:ay"],
    "blue":   ["cluster:bl", "team:ue"],
    "red":    ["phoneme:r", "phoneme:E", "phoneme:d"],
    "big":    ["phoneme:b", "phoneme:I", "phoneme:g"],
    "two":    ["phoneme:t", "phoneme:u"],
    "one":    ["phoneme:w", "phoneme:V", "phoneme:n"],
    "find":   ["phoneme:f", "phoneme:aI", "phoneme:n", "phoneme:d"],
    "down":   ["phoneme:d", "phoneme:aU", "phoneme:n"],
    "come":   ["phoneme:k", "phoneme:V", "phoneme:m"],
    "make":   ["phoneme:m", "phoneme:eI", "phoneme:k"],
    "this":   ["phoneme:Dh", "phoneme:I", "phoneme:s"],
    "that":   ["phoneme:Dh", "phoneme:ae", "phoneme:t"],
    "what":   ["phoneme:w", "phoneme:V", "phoneme:t"],
    "with":   ["phoneme:w", "phoneme:I", "phoneme:Th"],
    "want":   ["phoneme:w", "phoneme:O", "phoneme:n", "phoneme:t"],
    "have":   ["phoneme:h", "phoneme:ae", "phoneme:v"],
    "good":   ["phoneme:g", "team:oo", "phoneme:d"],
    "they":   ["phoneme:Dh", "team:ay"],
    "from":   ["cluster:fr", "phoneme:V", "phoneme:m"],

    # ── Animals + things kids name (CVC heavy) ──
    "cat":    ["phoneme:k", "phoneme:ae", "phoneme:t"],
    "dog":    ["phoneme:d", "phoneme:O", "phoneme:g"],
    "fish":   ["phoneme:f", "phoneme:I", "phoneme:S"],
    "bird":   ["phoneme:b", "rcontrol:ir", "phoneme:d"],
    "bear":   ["phoneme:b", "phoneme:E", "phoneme:r"],
    "duck":   ["phoneme:d", "phoneme:V", "phoneme:k"],
    "frog":   ["cluster:fr", "phoneme:O", "phoneme:g"],
    "pig":    ["phoneme:p", "phoneme:I", "phoneme:g"],
    "cow":    ["phoneme:k", "phoneme:aU"],
    "horse":  ["phoneme:h", "rcontrol:or", "phoneme:s"],
    "mouse":  ["phoneme:m", "phoneme:aU", "phoneme:s"],
    "snake":  ["cluster:sn", "phoneme:eI", "phoneme:k"],
    "hen":    ["phoneme:h", "phoneme:E", "phoneme:n"],
    "ten":    ["phoneme:t", "phoneme:E", "phoneme:n"],
    "sun":    ["phoneme:s", "phoneme:V", "phoneme:n"],
    "run":    ["phoneme:r", "phoneme:V", "phoneme:n"],
    "fun":    ["phoneme:f", "phoneme:V", "phoneme:n"],
    "bug":    ["phoneme:b", "phoneme:V", "phoneme:g"],
    "ball":   ["phoneme:b", "phoneme:O", "phoneme:l"],
    "bell":   ["phoneme:b", "phoneme:E", "phoneme:l"],
    "fall":   ["phoneme:f", "phoneme:O", "phoneme:l"],
    "wall":   ["phoneme:w", "phoneme:O", "phoneme:l"],
    "bed":    ["phoneme:b", "phoneme:E", "phoneme:d"],
    "leg":    ["phoneme:l", "phoneme:E", "phoneme:g"],
    "egg":    ["phoneme:E", "phoneme:g"],
    "ant":    ["phoneme:ae", "phoneme:n", "phoneme:t"],
    "hat":    ["phoneme:h", "phoneme:ae", "phoneme:t"],
    "hot":    ["phoneme:h", "phoneme:O", "phoneme:t"],
    "pot":    ["phoneme:p", "phoneme:O", "phoneme:t"],
    "top":    ["phoneme:t", "phoneme:O", "phoneme:p"],
    "stop":   ["cluster:st", "phoneme:O", "phoneme:p"],
    "star":   ["cluster:st", "rcontrol:ar"],
    "tree":   ["cluster:tr", "team:ee"],
    "boy":    ["phoneme:b", "phoneme:OI"],
    "toy":    ["phoneme:t", "phoneme:OI"],
    "boat":   ["phoneme:b", "team:oa", "phoneme:t"],
    "rain":   ["phoneme:r", "team:ai", "phoneme:n"],
    "day":    ["phoneme:d", "team:ay"],
    "way":    ["phoneme:w", "team:ay"],
    "may":    ["phoneme:m", "team:ay"],
    "name":   ["phoneme:n", "phoneme:eI", "phoneme:m"],
    "game":   ["phoneme:g", "phoneme:eI", "phoneme:m"],
    "cake":   ["phoneme:k", "phoneme:eI", "phoneme:k"],
    "bike":   ["phoneme:b", "phoneme:aI", "phoneme:k"],
    "kite":   ["phoneme:k", "phoneme:aI", "phoneme:t"],
    "light":  ["phoneme:l", "team:igh", "phoneme:t"],
    "night":  ["phoneme:n", "team:igh", "phoneme:t"],
    "right":  ["phoneme:r", "team:igh", "phoneme:t"],
    "ride":   ["phoneme:r", "phoneme:aI", "phoneme:d"],
    "side":   ["phoneme:s", "phoneme:aI", "phoneme:d"],
    "time":   ["phoneme:t", "phoneme:aI", "phoneme:m"],
    "five":   ["phoneme:f", "phoneme:aI", "phoneme:v"],
    "nine":   ["phoneme:n", "phoneme:aI", "phoneme:n"],
    "smile":  ["cluster:sm", "phoneme:aI", "phoneme:l"],
    "snow":   ["cluster:sn", "team:oa"],   # actually /snoʊ/, oa team is /oʊ/
    "spring": ["cluster:spr", "phoneme:I", "phoneme:Ng"],
    "strong": ["cluster:str", "phoneme:O", "phoneme:Ng"],
    "three":  ["cluster:thr", "team:ee"],
    "swim":   ["cluster:sw", "phoneme:I", "phoneme:m"],
    "shark":  ["phoneme:S", "rcontrol:ar", "phoneme:k"],
    "ship":   ["phoneme:S", "phoneme:I", "phoneme:p"],
    "chip":   ["phoneme:tS", "phoneme:I", "phoneme:p"],
    "chin":   ["phoneme:tS", "phoneme:I", "phoneme:n"],
    "thing":  ["phoneme:Th", "phoneme:I", "phoneme:Ng"],
    "thumb":  ["phoneme:Th", "phoneme:V", "phoneme:m"],
    "this":   ["phoneme:Dh", "phoneme:I", "phoneme:s"],
    "song":   ["phoneme:s", "phoneme:O", "phoneme:Ng"],
    "ring":   ["phoneme:r", "phoneme:I", "phoneme:Ng"],
    "wing":   ["phoneme:w", "phoneme:I", "phoneme:Ng"],
    "king":   ["phoneme:k", "phoneme:I", "phoneme:Ng"],
    "moon":   ["phoneme:m", "team:oo", "phoneme:n"],
    "food":   ["phoneme:f", "team:oo", "phoneme:d"],
    "cool":   ["phoneme:k", "team:oo", "phoneme:l"],
    "school": ["phoneme:s", "phoneme:k", "team:oo", "phoneme:l"],
    "new":    ["phoneme:n", "team:ew"],
    "blue":   ["cluster:bl", "team:ue"],
    "true":   ["cluster:tr", "team:ue"],
    "green":  ["cluster:gr", "team:ee", "phoneme:n"],
    "brown":  ["cluster:br", "phoneme:aU", "phoneme:n"],
    "black":  ["cluster:bl", "phoneme:ae", "phoneme:k"],
    "white":  ["phoneme:w", "phoneme:aI", "phoneme:t"],
    "yellow": ["phoneme:j", "phoneme:E", "phoneme:l", "phoneme:oU"],
    "pink":   ["phoneme:p", "phoneme:I", "phoneme:Ng", "phoneme:k"],
    "happy":  ["phoneme:h", "phoneme:ae", "phoneme:p", "phoneme:i"],
    "letter": ["phoneme:l", "phoneme:E", "phoneme:t", "rcontrol:er"],
    "sound":  ["phoneme:s", "phoneme:aU", "phoneme:n", "phoneme:d"],
    "word":   ["phoneme:w", "rcontrol:ur", "phoneme:d"],
    "read":   ["phoneme:r", "team:ee", "phoneme:d"],
    "book":   ["phoneme:b", "team:oo", "phoneme:k"],
    "song":   ["phoneme:s", "phoneme:O", "phoneme:Ng"],
    "phone":  ["phoneme:f", "phoneme:oU", "phoneme:n"],   # ph spelling
    "knee":   ["phoneme:n", "team:ee"],                    # silent k
    "know":   ["phoneme:n", "team:oa"],                    # silent k
}


def words_with_pattern(pattern: List[str]) -> List[str]:
    """Return words that match an exact phoneme sequence pattern."""
    return [w for w, p in WORD_VOCAB.items() if p == pattern]


def all_phonemes_used() -> List[str]:
    """Distinct phoneme keys appearing in any word."""
    used = set()
    for seq in WORD_VOCAB.values():
        used.update(seq)
    return sorted(used)


def words_starting_with(phoneme: str) -> List[str]:
    return [w for w, p in WORD_VOCAB.items() if p and p[0] == phoneme]


if __name__ == "__main__":
    print(f"vocab size: {len(WORD_VOCAB)} words")
    print(f"distinct phoneme keys used: {len(all_phonemes_used())}")
    print(f"sample words starting with phoneme:s: "
          f"{words_starting_with('phoneme:s')[:8]}")
    print(f"sample words starting with cluster:tr: "
          f"{words_starting_with('cluster:tr')}")
