"""
Bible Digestion — The learner reads the Bible deeply, multiple passes.

Pass 1: QUALITY — Score every verse for usefulness (filter genealogies, place names)
Pass 2: INTENT — Tag every verse with what it's FOR (comfort, praise, teaching, etc.)
Pass 3: LANGUAGE — Extract warm phrases and patterns from scripture itself
Pass 4: CONNECTIONS — Build verse clusters that belong together thematically
Pass 5: FAVORITES — Identify the most beloved/well-known verses

After digestion, the system KNOWS which verses to serve and how
to talk about them using the Bible's own language.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import gzip
import json
import os
import re
import time
from collections import defaultdict

DIGEST_DIR = os.path.expanduser('~/.ck/bible_digest')
DIGEST_PATH = os.path.join(DIGEST_DIR, 'digest.json.gz')

# ── Well-known verses that should always rank high ────────────────
# These are the verses people know and love. The algebra will still
# find surprising connections, but these should never be buried.
BELOVED_VERSES = {
    # Comfort
    'Psalm 23:1', 'Psalm 23:4', 'Psalm 46:1', 'Psalm 91:1', 'Psalm 91:2',
    'Psalm 34:18', 'Psalm 147:3', 'Isaiah 41:10', 'Isaiah 43:2',
    'Matthew 11:28', 'Matthew 11:29', 'John 14:27', 'Romans 8:28',
    'Romans 8:38', 'Romans 8:39', '2 Corinthians 1:3', '2 Corinthians 1:4',
    'Revelation 21:4', 'Psalm 73:26', 'Deuteronomy 31:8',
    # Faith & Trust
    'Proverbs 3:5', 'Proverbs 3:6', 'Hebrews 11:1', 'Romans 10:17',
    'Mark 11:24', 'Matthew 17:20', 'Psalm 37:5', 'Isaiah 26:3',
    'Jeremiah 29:11', 'Philippians 4:13', 'Romans 8:31',
    # Love
    'John 3:16', '1 Corinthians 13:4', '1 Corinthians 13:7',
    '1 Corinthians 13:13', '1 John 4:8', '1 John 4:18', 'Romans 5:8',
    'Ephesians 3:17', 'Ephesians 3:18', 'Song of Solomon 8:6',
    # Peace
    'Philippians 4:6', 'Philippians 4:7', 'John 16:33', 'Isaiah 26:3',
    'Psalm 29:11', 'Colossians 3:15', 'Numbers 6:24', 'Numbers 6:25',
    'Numbers 6:26',
    # Praise & Worship
    'Psalm 100:1', 'Psalm 100:4', 'Psalm 150:6', 'Psalm 95:1',
    'Psalm 34:1', 'Psalm 103:1', 'Psalm 145:3', 'Psalm 96:1',
    'Hebrews 13:15', 'Psalm 9:1',
    # Hope
    'Romans 15:13', 'Jeremiah 29:11', 'Isaiah 40:31', 'Lamentations 3:22',
    'Lamentations 3:23', 'Psalm 42:11', 'Romans 5:3', 'Romans 5:4',
    'Hebrews 6:19', '1 Peter 1:3',
    # Strength
    'Isaiah 40:29', 'Isaiah 40:31', 'Philippians 4:13', 'Psalm 18:2',
    'Psalm 27:1', 'Psalm 28:7', 'Nehemiah 8:10', 'Ephesians 6:10',
    '2 Timothy 1:7', 'Joshua 1:9',
    # Forgiveness
    '1 John 1:9', 'Psalm 103:12', 'Isaiah 1:18', 'Micah 7:18',
    'Ephesians 1:7', 'Colossians 3:13', 'Acts 3:19', 'Psalm 32:5',
    # Wisdom
    'James 1:5', 'Proverbs 1:7', 'Proverbs 9:10', 'Psalm 119:105',
    'Colossians 3:16', '2 Timothy 3:16', 'Psalm 119:11',
    # Suffering
    'James 1:2', 'James 1:3', 'Romans 5:3', 'Romans 5:4',
    '1 Peter 5:10', '2 Corinthians 4:17', 'Psalm 34:19', 'John 16:33',
    # Salvation
    'Romans 3:23', 'Romans 6:23', 'Romans 10:9', 'Ephesians 2:8',
    'Ephesians 2:9', 'John 14:6', 'Acts 4:12', 'Titus 3:5',
    # Prayer
    'Matthew 7:7', 'Philippians 4:6', 'James 5:16', '1 John 5:14',
    'Psalm 145:18', 'Matthew 6:9', 'Jeremiah 33:3',
    # Identity in Christ
    '2 Corinthians 5:17', 'Galatians 2:20', 'Ephesians 2:10',
    'Psalm 139:14', 'Jeremiah 1:5', 'Romans 8:17', '1 Peter 2:9',
}

# ── Noise patterns (verses to score LOW) ──────────────────────────
NOISE_PATTERNS = [
    r'^And the sons of \w+[;:]',
    r'^And \w+ begat \w+',
    r'^The sons of \w+[;:]',
    r'^And these (?:are|were) the (?:sons|names|chiefs)',
    r'^\w+, \w+, \w+, \w+,',  # Lists of names
    r'^And (?:he|she|they) (?:went|came|departed)',
    r'^And it came to pass',
    r'^Now (?:these|the) (?:are|were) the',
    r'^The children of \w+,',
    r'^Of \w+[,;:] the family of',
]
_NOISE_RE = [re.compile(p, re.IGNORECASE) for p in NOISE_PATTERNS]

# ── Intent keywords for verse tagging ─────────────────────────────
INTENT_KEYWORDS = {
    'comfort': [
        'comfort', 'comforted', 'comforter', 'wipe', 'tears', 'mourn',
        'near', 'nigh', 'broken', 'brokenhearted', 'heal', 'healed',
        'rest', 'weary', 'heavy laden', 'peace', 'still', 'afraid',
        'fear not', 'do not fear', 'be not afraid', 'with thee', 'with you',
        'upholdeth', 'sustain', 'deliver', 'refuge', 'shelter', 'shadow',
        'wings', 'arms', 'carry', 'carried', 'hold', 'held',
    ],
    'praise': [
        'praise', 'praised', 'praises', 'sing', 'sang', 'song',
        'glory', 'glorify', 'glorified', 'magnify', 'exalt', 'exalted',
        'worship', 'worshipped', 'bless', 'blessed', 'thanksgiving',
        'thanks', 'thankful', 'rejoice', 'rejoiced', 'joy', 'joyful',
        'great', 'wonderful', 'marvelous', 'mighty', 'awesome', 'worthy',
        'hallelujah', 'hosanna', 'amen',
    ],
    'hope': [
        'hope', 'hoped', 'hoping', 'promise', 'promised', 'promises',
        'new', 'renew', 'renewed', 'restore', 'restored', 'future',
        'morning', 'dawn', 'light', 'arise', 'risen', 'rise',
        'wait', 'waited', 'waiting', 'patient', 'patience', 'endure',
        'overcome', 'overcame', 'victory', 'conquer',
    ],
    'love': [
        'love', 'loved', 'loveth', 'lovingkindness', 'beloved',
        'mercy', 'merciful', 'mercies', 'grace', 'gracious',
        'tender', 'compassion', 'compassionate', 'kind', 'kindness',
        'forgive', 'forgiven', 'forgiveness', 'redeem', 'redeemed',
        'salvation', 'save', 'saved', 'saviour',
    ],
    'strength': [
        'strength', 'strengthen', 'strong', 'mighty', 'power',
        'powerful', 'courage', 'courageous', 'bold', 'boldness',
        'stand', 'stood', 'firm', 'rock', 'fortress', 'shield',
        'armor', 'sword', 'fight', 'battle', 'war', 'warrior',
        'prevail', 'prevailed',
    ],
    'wisdom': [
        'wisdom', 'wise', 'understanding', 'knowledge', 'discern',
        'discernment', 'counsel', 'teach', 'taught', 'learn',
        'learned', 'instruction', 'law', 'commandment', 'statute',
        'word', 'words', 'truth', 'true', 'light', 'lamp', 'path',
    ],
    'trust': [
        'trust', 'trusted', 'trusteth', 'faith', 'faithful',
        'faithfulness', 'believe', 'believed', 'believeth',
        'rely', 'lean', 'depend', 'confidence', 'confident',
        'assurance', 'certain', 'sure',
    ],
    'suffering': [
        'suffer', 'suffered', 'suffering', 'afflict', 'affliction',
        'tribulation', 'trial', 'trouble', 'troubled', 'distress',
        'persecute', 'persecuted', 'persecution', 'pain', 'sorrow',
        'grief', 'grieve', 'grieved', 'weep', 'wept', 'cry', 'cried',
        'cross', 'crucify', 'crucified', 'death', 'die', 'died',
    ],
}


class BibleDigestion:
    """Deep multi-pass reading of the Bible.

    After digestion, every verse has:
      - quality_score: 0.0–1.0 (filters noise)
      - intent_tags: set of intents this verse serves
      - is_beloved: whether it's a well-known verse
      - phrases: warm phrases extracted from the verse
    """

    def __init__(self):
        self.verse_quality = {}      # {ref: float 0-1}
        self.verse_intents = {}      # {ref: set of intent strings}
        self.intent_index = defaultdict(list)  # {intent: [refs sorted by quality]}
        self.beloved = set()         # Well-known verse refs that exist in our Bible
        self.warm_phrases = defaultdict(list)  # {intent: [phrases from scripture]}
        self._digested = False

    @property
    def digested(self):
        return self._digested

    def digest(self, bible_index):
        """Read the Bible multiple times. Each pass learns something different."""
        if not bible_index.ready:
            bible_index.load()

        # Try loading cached digest
        if self._load():
            print(f"[Digest] Loaded cached digest ({len(self.verse_quality)} verses)")
            return

        verses = bible_index._verses
        print(f"[Digest] Reading {len(verses)} verses, 5 passes...")
        t0 = time.time()

        # ── Pass 1: QUALITY — Score every verse ───────────────────
        print("[Digest] Pass 1: Quality scoring...")
        for v in verses:
            score = self._score_quality(v.ref, v.text)
            self.verse_quality[v.ref] = score

        good = sum(1 for s in self.verse_quality.values() if s >= 0.5)
        print(f"  {good} high-quality verses (of {len(verses)})")

        # ── Pass 2: INTENT — Tag every verse ──────────────────────
        print("[Digest] Pass 2: Intent tagging...")
        for v in verses:
            tags = self._tag_intents(v.text)
            self.verse_intents[v.ref] = tags
            for tag in tags:
                self.intent_index[tag].append(v.ref)

        for intent, refs in self.intent_index.items():
            # Sort by quality within each intent
            self.intent_index[intent] = sorted(
                refs, key=lambda r: self.verse_quality.get(r, 0), reverse=True
            )
        print(f"  Intents: {dict((k, len(v)) for k, v in self.intent_index.items())}")

        # ── Pass 3: BELOVED — Mark well-known verses ─────────────
        print("[Digest] Pass 3: Beloved verse identification...")
        ref_set = set(v.ref for v in verses)
        for ref in BELOVED_VERSES:
            if ref in ref_set:
                self.beloved.add(ref)
                # Boost quality of beloved verses
                self.verse_quality[ref] = max(
                    self.verse_quality.get(ref, 0.5), 0.9
                )
        print(f"  {len(self.beloved)} beloved verses found in Bible")

        # ── Pass 4: LANGUAGE — Extract warm phrases ───────────────
        print("[Digest] Pass 4: Extracting warm language patterns...")
        for v in verses:
            if self.verse_quality.get(v.ref, 0) < 0.4:
                continue
            tags = self.verse_intents.get(v.ref, set())
            phrases = self._extract_phrases(v.text)
            for tag in tags:
                self.warm_phrases[tag].extend(phrases)

        # Deduplicate and keep best
        for intent in self.warm_phrases:
            unique = list(set(self.warm_phrases[intent]))
            # Sort by length (prefer medium-length phrases)
            unique.sort(key=lambda p: abs(len(p.split()) - 8))
            self.warm_phrases[intent] = unique[:200]

        print(f"  Phrases: {dict((k, len(v)) for k, v in self.warm_phrases.items())}")

        # ── Pass 5: CROSS-VALIDATION — Re-score with all knowledge
        print("[Digest] Pass 5: Cross-validation re-scoring...")
        for v in verses:
            ref = v.ref
            base = self.verse_quality.get(ref, 0.5)
            # Boost for having intent tags
            tag_count = len(self.verse_intents.get(ref, set()))
            if tag_count > 0:
                base = min(1.0, base + tag_count * 0.05)
            # Boost for beloved status
            if ref in self.beloved:
                base = max(base, 0.9)
            self.verse_quality[ref] = round(base, 3)

        elapsed = time.time() - t0
        self._digested = True
        print(f"[Digest] Complete in {elapsed:.1f}s")
        self._save()

    def get_verses_for_intent(self, intent, max_k=10):
        """Get the best verses for a specific intent, quality-ranked."""
        refs = self.intent_index.get(intent, [])
        # Prioritize beloved verses
        beloved_first = [r for r in refs if r in self.beloved][:max_k // 2]
        others = [r for r in refs if r not in self.beloved]
        combined = beloved_first + others
        return combined[:max_k]

    def get_warm_phrases(self, intent, max_k=5):
        """Get warm phrases from scripture for an intent."""
        return self.warm_phrases.get(intent, [])[:max_k]

    def verse_is_good(self, ref):
        """Is this verse high enough quality to show?"""
        return self.verse_quality.get(ref, 0.5) >= 0.4

    def _score_quality(self, ref, text):
        """Score a verse 0.0–1.0 for conversational usefulness."""
        score = 0.5  # Base

        # Penalty: noise patterns (genealogies, lists)
        for pattern in _NOISE_RE:
            if pattern.search(text):
                score -= 0.3
                break

        # Penalty: too short (fragments)
        words = text.split()
        if len(words) < 5:
            score -= 0.2
        elif len(words) < 8:
            score -= 0.1

        # Penalty: too long (hard to absorb)
        if len(words) > 80:
            score -= 0.1

        # Bonus: contains God/Lord/Jesus/Christ (directly about God)
        god_words = {'god', 'lord', 'jesus', 'christ', 'spirit'}
        if any(w.lower() in god_words for w in words):
            score += 0.15

        # Bonus: contains emotional/relational language
        emotional = {'love', 'heart', 'soul', 'fear', 'hope', 'peace',
                     'comfort', 'mercy', 'grace', 'faith', 'joy', 'praise',
                     'trust', 'help', 'save', 'forgive', 'heal', 'strength'}
        if any(w.lower().rstrip('.,;:!?') in emotional for w in words):
            score += 0.15

        # Bonus: well-known reference
        if ref in BELOVED_VERSES:
            score += 0.3

        return max(0.0, min(1.0, score))

    def _tag_intents(self, text):
        """Tag a verse with intents based on keywords."""
        lower = text.lower()
        tags = set()
        for intent, keywords in INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in lower:
                    tags.add(intent)
                    break
        return tags

    def _extract_phrases(self, text):
        """Extract warm, usable phrases from a verse."""
        phrases = []
        # Split on semicolons and colons (common verse structure)
        parts = re.split(r'[;:]', text)
        for part in parts:
            part = part.strip().strip('[]')
            words = part.split()
            if 4 <= len(words) <= 20:
                # Clean up
                clean = part.strip()
                if clean and clean[0].isupper():
                    phrases.append(clean)
        return phrases

    def stats(self):
        good = sum(1 for s in self.verse_quality.values() if s >= 0.5)
        return {
            'digested': self._digested,
            'total_verses': len(self.verse_quality),
            'good_verses': good,
            'beloved_found': len(self.beloved),
            'intents': {k: len(v) for k, v in self.intent_index.items()},
            'phrases': {k: len(v) for k, v in self.warm_phrases.items()},
        }

    def _save(self):
        os.makedirs(DIGEST_DIR, exist_ok=True)
        data = {
            'verse_quality': self.verse_quality,
            'verse_intents': {k: list(v) for k, v in self.verse_intents.items()},
            'intent_index': dict(self.intent_index),
            'beloved': list(self.beloved),
            'warm_phrases': dict(self.warm_phrases),
        }
        with gzip.open(DIGEST_PATH, 'wt', encoding='utf-8') as f:
            json.dump(data, f)
        print(f"[Digest] Saved to {DIGEST_PATH}")

    def _load(self):
        if not os.path.exists(DIGEST_PATH):
            return False
        try:
            with gzip.open(DIGEST_PATH, 'rt', encoding='utf-8') as f:
                data = json.load(f)
            self.verse_quality = data.get('verse_quality', {})
            self.verse_intents = {
                k: set(v) for k, v in data.get('verse_intents', {}).items()
            }
            self.intent_index = defaultdict(list, data.get('intent_index', {}))
            self.beloved = set(data.get('beloved', []))
            self.warm_phrases = defaultdict(list, data.get('warm_phrases', {}))
            self._digested = True
            return True
        except Exception:
            return False
