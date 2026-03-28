"""
People Memory — Remembers everyone the companion meets.

Each person gets a local profile that persists across sessions:
  - What corridors they tend to live in
  - What intents they express most
  - Which verses resonated with them
  - What topics they've discussed
  - Their conversation history (summarized)

All local. Never sent anywhere. Clearable on request.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import json
import os
import time
from collections import defaultdict

MEMORY_DIR = os.path.expanduser('~/.ck/bible_companion/people')


class PersonMemory:
    """Memory for one person (identified by session_id)."""

    def __init__(self, person_id, save_dir=None):
        self.person_id = person_id
        self._dir = os.path.join(save_dir or MEMORY_DIR, person_id[:32])
        self._path = os.path.join(self._dir, 'memory.json')

        # Core memory
        self.name = None                # If they tell us their name
        self.first_seen = None
        self.last_seen = None
        self.visit_count = 0

        # Patterns over time
        self.corridor_history = []       # Recent corridors (last 100)
        self.intent_counts = defaultdict(int)  # How often each intent
        self.favorite_verses = {}        # {ref: {times_shown, engaged, score}}
        self.topics = []                 # Recent topic keywords (last 50)

        # Conversation summaries (not full text — privacy)
        self.summaries = []              # [{timestamp, corridor, intent, verse_ref, engagement}]

        # Preferences
        self.bible_version = 'kjv'

        self._load()

    def record_visit(self, corridor, intent, verse_refs, user_text_length):
        """Record a conversation turn."""
        now = time.time()
        if self.first_seen is None:
            self.first_seen = now
        self.last_seen = now
        self.visit_count += 1

        # Track corridor pattern
        self.corridor_history.append(corridor)
        if len(self.corridor_history) > 100:
            self.corridor_history = self.corridor_history[-100:]

        # Track intent pattern
        self.intent_counts[intent] += 1

        # Track verses shown
        for ref in verse_refs:
            if ref not in self.favorite_verses:
                self.favorite_verses[ref] = {
                    'times_shown': 0, 'engaged': 0, 'score': 0.5,
                }
            self.favorite_verses[ref]['times_shown'] += 1

        # Summary (no raw text stored)
        self.summaries.append({
            'timestamp': now,
            'corridor': corridor,
            'intent': intent,
            'verse_ref': verse_refs[0] if verse_refs else None,
            'text_length': user_text_length,
        })
        if len(self.summaries) > 200:
            self.summaries = self.summaries[-200:]

        self._save()

    def record_engagement(self, verse_ref):
        """Record that a person engaged with a verse (continued talking after seeing it)."""
        if verse_ref in self.favorite_verses:
            fv = self.favorite_verses[verse_ref]
            fv['engaged'] += 1
            fv['score'] = min(1.0, fv['score'] + 0.1)
            self._save()

    def set_name(self, name):
        """Person shared their name."""
        self.name = name
        self._save()

    def get_greeting(self):
        """Get a personalized greeting based on memory."""
        if self.visit_count == 0:
            return None  # First time — use default welcome

        name_part = f", {self.name}" if self.name else ""

        # What corridor do they usually live in?
        dominant_corridor = self._dominant_corridor()

        if self.visit_count == 1:
            return f"Welcome back{name_part}."
        elif self.visit_count < 5:
            return f"Good to see you again{name_part}."
        elif dominant_corridor in ('COL', 'CTR'):
            return f"I'm glad you came back{name_part}. How are you doing?"
        elif dominant_corridor in ('PRE_LEAK', 'BRT'):
            return f"Welcome back{name_part}. It's good to be here with you."
        else:
            return f"Hello again{name_part}. What's on your heart today?"

    def get_verse_preference(self, verse_ref):
        """Get this person's preference for a verse (-0.5 to +0.5)."""
        fv = self.favorite_verses.get(verse_ref)
        if fv is None or fv['times_shown'] < 2:
            return 0.0
        # Positive if they engaged, negative if they ignored
        engagement_rate = fv['engaged'] / max(1, fv['times_shown'])
        return (engagement_rate - 0.3) * 0.5  # Center around 30% engagement

    def get_dominant_intent(self):
        """What does this person usually come here for?"""
        if not self.intent_counts:
            return None
        return max(self.intent_counts, key=self.intent_counts.get)

    def _dominant_corridor(self):
        if not self.corridor_history:
            return 'BRT'
        recent = self.corridor_history[-20:]
        counts = defaultdict(int)
        for c in recent:
            counts[c] += 1
        return max(counts, key=counts.get)

    def clear(self):
        """Clear all memory for this person."""
        self.name = None
        self.first_seen = None
        self.last_seen = None
        self.visit_count = 0
        self.corridor_history = []
        self.intent_counts = defaultdict(int)
        self.favorite_verses = {}
        self.topics = []
        self.summaries = []
        self._save()

    def to_dict(self):
        """Export memory (for API response, no sensitive data)."""
        return {
            'person_id': self.person_id[:8] + '...',
            'name': self.name,
            'first_seen': self.first_seen,
            'last_seen': self.last_seen,
            'visit_count': self.visit_count,
            'dominant_corridor': self._dominant_corridor(),
            'dominant_intent': self.get_dominant_intent(),
            'top_verses': sorted(
                [(ref, d['score'], d['times_shown'])
                 for ref, d in self.favorite_verses.items()
                 if d['times_shown'] >= 2],
                key=lambda x: x[1], reverse=True
            )[:5],
            'total_summaries': len(self.summaries),
        }

    def _save(self):
        os.makedirs(self._dir, exist_ok=True)
        data = {
            'person_id': self.person_id,
            'name': self.name,
            'first_seen': self.first_seen,
            'last_seen': self.last_seen,
            'visit_count': self.visit_count,
            'corridor_history': self.corridor_history,
            'intent_counts': dict(self.intent_counts),
            'favorite_verses': self.favorite_verses,
            'topics': self.topics,
            'summaries': self.summaries,
            'bible_version': self.bible_version,
        }
        with open(self._path, 'w') as f:
            json.dump(data, f)

    def _load(self):
        if not os.path.exists(self._path):
            return
        try:
            with open(self._path, 'r') as f:
                data = json.load(f)
            self.name = data.get('name')
            self.first_seen = data.get('first_seen')
            self.last_seen = data.get('last_seen')
            self.visit_count = data.get('visit_count', 0)
            self.corridor_history = data.get('corridor_history', [])
            self.intent_counts = defaultdict(int, data.get('intent_counts', {}))
            self.favorite_verses = data.get('favorite_verses', {})
            self.topics = data.get('topics', [])
            self.summaries = data.get('summaries', [])
            self.bible_version = data.get('bible_version', 'kjv')
        except Exception:
            pass  # Corrupted, start fresh


class PeopleMemory:
    """Manages memory for all people the companion meets."""

    def __init__(self, save_dir=None):
        self._save_dir = save_dir or MEMORY_DIR
        self._cache = {}  # {person_id: PersonMemory}

    def get(self, person_id):
        """Get or create memory for a person."""
        if person_id not in self._cache:
            self._cache[person_id] = PersonMemory(person_id, self._save_dir)
        return self._cache[person_id]

    def clear_person(self, person_id):
        """Clear all memory for one person."""
        mem = self.get(person_id)
        mem.clear()

    def clear_all(self):
        """Clear ALL people memory."""
        import shutil
        if os.path.exists(self._save_dir):
            shutil.rmtree(self._save_dir)
        self._cache.clear()

    def stats(self):
        """Global stats about people memory."""
        total_files = 0
        if os.path.exists(self._save_dir):
            for d in os.listdir(self._save_dir):
                if os.path.isdir(os.path.join(self._save_dir, d)):
                    total_files += 1
        return {
            'people_remembered': total_files,
            'cached': len(self._cache),
            'save_dir': self._save_dir,
        }
