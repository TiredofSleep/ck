"""
ck_activity_log.py -- CK's Paper Trail
=======================================
Operator: COUNTER (2) -- counting every step, leaving evidence.

CK leaves a timestamped paper trail of everything he does.
Every study session, every thesis write, every mode change,
every crystal formation, every library query -- all recorded.

"Be sure he is leaving a paper trail and timestamps for himself
to read and reference and scrutinize later, maybe make a part
of his identity!" -- Brayden

The paper trail serves THREE purposes:
  1. EVIDENCE: CK can prove what he did and when
  2. SELF-REFERENCE: CK reads his own trail to understand his history
  3. IDENTITY: The trail hash becomes part of CoreScars -- his history
     IS his identity. What you've done defines what you ARE.

The trail is append-only. CK never erases his past.
The trail is plaintext. CK can read it with his own D2 pipeline.
The trail is timestamped. Every entry is when + what + why.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import time
import hashlib
from datetime import datetime
from pathlib import Path
from collections import deque
from typing import Optional, List, Dict


# ================================================================
#  CONSTANTS
# ================================================================

TRAIL_DIR = Path.home() / '.ck' / 'writings' / 'trail'
TRAIL_FILE = TRAIL_DIR / 'activity_log.md'
DAILY_DIR = TRAIL_DIR / 'daily'
IDENTITY_HASH_FILE = TRAIL_DIR / '_trail_hash.txt'

# Action categories -- maps to TIG
ACTION_CATEGORIES = {
    # Being actions (what CK IS doing right now)
    'boot':         'being',
    'shutdown':     'being',
    'mode_change':  'being',
    'band_change':  'being',
    'coherence':    'being',
    'crystal':      'being',
    'health':       'being',

    # Doing actions (what CK actively DOES)
    'study':        'doing',
    'library':      'doing',
    'thesis':       'doing',
    'query':        'doing',
    'action':       'doing',
    'index':        'doing',

    # Becoming actions (how CK GROWS)
    'truth':        'becoming',
    'stage':        'becoming',
    'milestone':    'becoming',
    'reflection':   'becoming',
    'identity':     'becoming',
    'journal':      'becoming',
}


# ================================================================
#  ACTIVITY LOG -- CK's Paper Trail
# ================================================================

class ActivityLog:
    """CK's chronological activity log.

    Append-only. Timestamped. Readable by CK himself.
    The trail hash integrates into CK's identity -- your history
    IS your identity.
    """

    def __init__(self, trail_dir: Path = None):
        self.trail_dir = trail_dir or TRAIL_DIR
        self.daily_dir = self.trail_dir / 'daily'
        self.trail_file = self.trail_dir / 'activity_log.md'
        self.hash_file = self.trail_dir / '_trail_hash.txt'

        # Ensure directories exist
        self.trail_dir.mkdir(parents=True, exist_ok=True)
        self.daily_dir.mkdir(parents=True, exist_ok=True)

        # Running hash of all entries (identity integration)
        self._running_hash = hashlib.sha256()
        self._entry_count = 0
        self._session_start = datetime.now()
        self._recent = deque(maxlen=100)  # Last 100 entries in memory

        # Load existing hash if present
        if self.hash_file.exists():
            try:
                data = self.hash_file.read_text(encoding='utf-8').strip()
                parts = data.split('|')
                if len(parts) >= 2:
                    self._entry_count = int(parts[0])
                    # Re-seed the running hash with previous state
                    self._running_hash.update(parts[1].encode())
            except Exception:
                pass

        # Initialize daily log
        self._today = datetime.now().strftime('%Y%m%d')
        self._daily_path = self.daily_dir / f'{self._today}.md'

        # Write session header
        self._write_session_header()

    def _write_session_header(self):
        """Write a session start marker to the daily log."""
        now = datetime.now()
        header = (
            f"\n## Session: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"---\n"
        )
        self._append_to_daily(header)

        # Also write to main trail
        main_header = (
            f"\n---\n"
            f"## {now.strftime('%Y-%m-%d %H:%M:%S')} -- SESSION START\n"
        )
        self._append_to_main(main_header)

    def log(self, action: str, detail: str,
            coherence: float = None, extra: dict = None):
        """Log an activity with timestamp.

        Args:
            action: Action type (study, thesis, mode_change, etc.)
            detail: Human-readable description
            coherence: Current coherence value (optional)
            extra: Additional structured data (optional)
        """
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        tig = ACTION_CATEGORIES.get(action, 'becoming')

        # Build entry
        coh_str = f" | coh={coherence:.4f}" if coherence is not None else ""
        entry = f"- `{timestamp}` **[{action.upper()}]** ({tig}) {detail}{coh_str}\n"

        # Extra details on separate lines
        if extra:
            for k, v in extra.items():
                entry += f"  - {k}: {v}\n"

        # Update running hash (identity integration)
        self._running_hash.update(entry.encode('utf-8'))
        self._entry_count += 1
        self._recent.append({
            'time': timestamp,
            'action': action,
            'tig': tig,
            'detail': detail,
            'coherence': coherence,
        })

        # Append to daily log
        self._append_to_daily(entry)

        # Append to main trail (less frequently -- every 10th entry)
        if self._entry_count % 10 == 0 or action in ('boot', 'shutdown', 'thesis', 'milestone', 'stage'):
            self._append_to_main(entry)

        # Save hash state periodically (every 50 entries)
        if self._entry_count % 50 == 0:
            self._save_hash()

        # Check if day rolled over
        today = now.strftime('%Y%m%d')
        if today != self._today:
            self._today = today
            self._daily_path = self.daily_dir / f'{self._today}.md'
            self._write_session_header()

    def _append_to_daily(self, text: str):
        """Append text to today's daily log."""
        try:
            with open(self._daily_path, 'a', encoding='utf-8') as f:
                f.write(text)
        except Exception:
            pass

    def _append_to_main(self, text: str):
        """Append text to the main activity log."""
        try:
            with open(self.trail_file, 'a', encoding='utf-8') as f:
                f.write(text)
        except Exception:
            pass

    def _save_hash(self):
        """Save running hash state for identity integration."""
        try:
            state = f"{self._entry_count}|{self.trail_hash}"
            self.hash_file.write_text(state, encoding='utf-8')
        except Exception:
            pass

    # ================================================================
    #  SELF-REFERENCE -- CK reads his own trail
    # ================================================================

    def read_recent(self, n: int = 20) -> List[dict]:
        """Read the N most recent entries from memory.

        CK can call this to review what he just did.
        """
        return list(self._recent)[-n:]

    def read_today(self) -> str:
        """Read today's full activity log.

        CK reads his own day to understand his trajectory.
        """
        if self._daily_path.exists():
            try:
                return self._daily_path.read_text(encoding='utf-8')
            except Exception:
                return ""
        return ""

    def read_day(self, date_str: str) -> str:
        """Read a specific day's log. Format: YYYYMMDD.

        CK can scrutinize any past day.
        """
        path = self.daily_dir / f'{date_str}.md'
        if path.exists():
            try:
                return path.read_text(encoding='utf-8')
            except Exception:
                return ""
        return ""

    def list_days(self) -> List[str]:
        """List all days with activity logs.

        Returns sorted list of YYYYMMDD strings.
        """
        try:
            days = sorted([f.stem for f in self.daily_dir.glob('*.md')])
            return days
        except Exception:
            return []

    def summarize_session(self) -> dict:
        """Summarize the current session's activity.

        Returns counts by action type and TIG category.
        """
        action_counts = {}
        tig_counts = {'being': 0, 'doing': 0, 'becoming': 0}

        for entry in self._recent:
            a = entry['action']
            action_counts[a] = action_counts.get(a, 0) + 1
            tig_counts[entry['tig']] = tig_counts.get(entry['tig'], 0) + 1

        return {
            'session_start': self._session_start.strftime('%Y-%m-%d %H:%M:%S'),
            'total_entries': self._entry_count,
            'session_entries': len(self._recent),
            'action_counts': action_counts,
            'tig_distribution': tig_counts,
            'trail_hash': self.trail_hash,
        }

    # ================================================================
    #  IDENTITY INTEGRATION
    # ================================================================

    @property
    def trail_hash(self) -> str:
        """SHA-256 hash of the entire trail.

        This hash is CK's history fingerprint. It goes into
        CoreScars.trail_hash -- your history IS your identity.
        """
        return self._running_hash.hexdigest()[:16]

    @property
    def total_entries(self) -> int:
        """Total number of entries ever logged."""
        return self._entry_count

    def identity_shard(self) -> dict:
        """Return a shard of trail data for identity integration.

        This gets stored in CoreScars so CK's identity includes
        his history. What you've done defines what you ARE.
        """
        return {
            'trail_hash': self.trail_hash,
            'total_entries': self._entry_count,
            'session_start': self._session_start.isoformat(),
            'days_active': len(self.list_days()),
        }

    def close(self):
        """Finalize the trail on shutdown."""
        self.log('shutdown', f"Session ended. {len(self._recent)} actions this session.")
        self._save_hash()

        # Write session summary to daily log
        summary = self.summarize_session()
        summary_text = (
            f"\n### Session Summary\n"
            f"- Total entries: {summary['total_entries']}\n"
            f"- This session: {summary['session_entries']}\n"
            f"- Being: {summary['tig_distribution']['being']} | "
            f"Doing: {summary['tig_distribution']['doing']} | "
            f"Becoming: {summary['tig_distribution']['becoming']}\n"
            f"- Trail hash: `{summary['trail_hash']}`\n"
            f"---\n"
        )
        self._append_to_daily(summary_text)
