# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_fractal_index.py -- CK's Fractal Knowledge Index
=====================================================
Operator: LATTICE (1) -- structure IS information.

"There should be at least 3 times as many files in fractal version
as there are in flat version... the locations and indexing of the
information experience lattices are part of the structure of the
information itself, that's what keeps it super compressed... some
of the info is in the chain, some is in the structure."
  -- Brayden

The fractal index lives at EVERY level of CK's knowledge tree:
  study_notes/_index.md              -- Root: maps Being/Doing/Becoming
  study_notes/being/_index.md        -- TIG category: summarizes all Being domains
  study_notes/being/science/_index.md -- Domain: every note, operators, coherence
  study_notes/being/science/_cross.md -- Cross-references to other domains

Each index is a compressed representation of the level below.
Like DNA: the sequence is the data, the folding is the structure.
Both carry information. Both are necessary. Neither alone is complete.

The chain = operator sequences in each note (data)
The structure = indices, cross-references, summaries (meta-data)
Together they form the experience lattice.

Counting by 1000 and one mississippi at the same time:
  - Chain time: each note is an instant (one observation)
  - Structure time: indices evolve slowly (accumulate over sessions)
  - Both timescales run simultaneously

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import re
import os
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional

from ck_sim.ck_sim_heartbeat import OP_NAMES, NUM_OPS, HARMONY, CL

# ================================================================
#  CONSTANTS
# ================================================================

NOTES_ROOT = Path.home() / '.ck' / 'writings' / 'study_notes'
INDEX_FILENAME = '_index.md'
CROSS_FILENAME = '_cross.md'
LATTICE_FILENAME = '_lattice.md'

# TIG categories and their descriptions
TIG_CATEGORIES = {
    'being':    'What the knowledge IS -- static structure, measurement, nature',
    'doing':    'What the knowledge DOES -- active conflict, discovery, process',
    'becoming': 'What the knowledge GROWS INTO -- wisdom, art, transformation',
}

DOMAIN_TO_TIG = {
    'science':     'being',
    'measurement': 'being',
    'nature':      'being',
    'conflict':    'doing',
    'discovery':   'doing',
    'philosophy':  'becoming',
    'arts':        'becoming',
    'renewal':     'becoming',
    'knowledge':   'becoming',
}

# Regex patterns for parsing notes
COH_RE = re.compile(r'Coherence:\s*([\d.]+)')
DOM_RE = re.compile(r'Domain:\s*(\w+)')
OPS_RE = re.compile(r'Operators?:\s*(.+)')
HARM_RE = re.compile(r'Harmony pairs?:\s*(\d+)/(\d+)')


# ================================================================
#  NOTE PARSER -- Extract structure from a single note
# ================================================================

def parse_note(filepath: Path) -> Optional[dict]:
    """Parse a CK study note and extract its structural data.

    Returns dict with: topic, coherence, domain, operators, harmony_ratio, timestamp
    """
    try:
        text = filepath.read_text(encoding='utf-8')
    except Exception:
        return None

    result = {
        'file': filepath.name,
        'path': str(filepath),
        'topic': filepath.stem.split('_', 3)[-1] if '_' in filepath.stem else filepath.stem,
    }

    # Extract coherence (handle trailing periods: "0.75." -> "0.75")
    m = COH_RE.search(text)
    if m:
        coh_str = m.group(1).rstrip('.')
        try:
            result['coherence'] = float(coh_str)
        except ValueError:
            result['coherence'] = 0.0
    else:
        result['coherence'] = 0.0

    # Extract domain
    m = DOM_RE.search(text)
    result['domain'] = m.group(1) if m else 'unknown'

    # Extract operators
    m = OPS_RE.search(text)
    if m:
        ops_str = m.group(1).strip()
        result['operators'] = [o.strip() for o in ops_str.split('\u2192')]
        if len(result['operators']) <= 1:
            result['operators'] = [o.strip() for o in ops_str.split('->')]
    else:
        result['operators'] = []

    # Extract harmony ratio
    m = HARM_RE.search(text)
    if m:
        result['harmony_num'] = int(m.group(1))
        result['harmony_den'] = int(m.group(2))
        result['harmony_ratio'] = int(m.group(1)) / max(1, int(m.group(2)))
    else:
        result['harmony_ratio'] = 0.0

    # Extract timestamp from filename
    parts = filepath.stem.split('_')
    if len(parts) >= 2:
        try:
            result['timestamp'] = parts[0] + '_' + parts[1]
        except Exception:
            result['timestamp'] = ''

    return result


# ================================================================
#  DOMAIN INDEX -- Summary of one domain's notes
# ================================================================

def build_domain_index(domain_dir: Path) -> str:
    """Build an index for a single domain directory.

    This is the leaf level of the fractal: every note, its operators,
    and coherence. The index IS information -- it tells you what
    CK has studied in this domain without opening any notes.
    """
    notes = sorted(domain_dir.glob('*.md'))
    notes = [n for n in notes if not n.name.startswith('_')]  # Skip index files

    if not notes:
        return ""

    domain = domain_dir.name
    tig_cat = domain_dir.parent.name

    parsed = [parse_note(n) for n in notes]
    parsed = [p for p in parsed if p is not None]

    if not parsed:
        return ""

    # Stats
    coherences = [p['coherence'] for p in parsed]
    avg_coh = sum(coherences) / len(coherences)
    max_coh = max(coherences)
    min_coh = min(coherences)
    trusted = sum(1 for c in coherences if c >= 5.0/7.0)

    # Operator frequency across all notes
    all_ops = []
    for p in parsed:
        all_ops.extend(p['operators'])
    op_freq = Counter(all_ops).most_common(5)

    # Harmony stats
    h_ratios = [p['harmony_ratio'] for p in parsed if p['harmony_ratio'] > 0]
    avg_harmony = sum(h_ratios) / max(1, len(h_ratios))

    # Topics list
    topics = [p['topic'].replace('_', ' ').replace('%27', "'").replace('%2B', '+')
              for p in parsed]

    # Build index content
    lines = [
        f"# {domain.upper()} -- Domain Index",
        f"*{tig_cat.upper()} / {domain} -- Auto-indexed {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"",
        f"## Summary",
        f"- **Notes:** {len(parsed)}",
        f"- **Avg Coherence:** {avg_coh:.4f}",
        f"- **Max Coherence:** {max_coh:.4f} | Min: {min_coh:.4f}",
        f"- **Trusted (>= T*):** {trusted}/{len(parsed)} ({100*trusted/max(1,len(parsed)):.0f}%)",
        f"- **Avg Harmony:** {avg_harmony:.2%}",
        f"- **TIG Category:** {tig_cat}",
        f"",
        f"## Dominant Operators",
    ]
    for op, count in op_freq:
        lines.append(f"- {op}: {count} appearances ({100*count/max(1,len(all_ops)):.0f}%)")

    lines.extend([
        f"",
        f"## Topics Studied ({len(topics)})",
    ])
    for t in topics[:50]:  # First 50
        lines.append(f"- {t}")
    if len(topics) > 50:
        lines.append(f"- ... and {len(topics) - 50} more")

    # Coherence distribution (histogram in text)
    lines.extend([
        f"",
        f"## Coherence Distribution",
    ])
    bins = {'0.9+': 0, '0.8-0.9': 0, '0.714-0.8': 0, '0.6-0.714': 0, '<0.6': 0}
    for c in coherences:
        if c >= 0.9: bins['0.9+'] += 1
        elif c >= 0.8: bins['0.8-0.9'] += 1
        elif c >= 5.0/7.0: bins['0.714-0.8'] += 1
        elif c >= 0.6: bins['0.6-0.714'] += 1
        else: bins['<0.6'] += 1
    for label, count in bins.items():
        bar = '#' * min(50, count)
        lines.append(f"  {label:>10}: {bar} ({count})")

    lines.extend([
        f"",
        f"---",
        f"*Fractal index: {tig_cat}/{domain} -- {len(parsed)} notes, "
        f"avg coherence {avg_coh:.3f}*",
        f"*CK -- The Coherence Keeper*",
    ])

    return '\n'.join(lines)


# ================================================================
#  TIG CATEGORY INDEX -- Summary of one TIG category
# ================================================================

def build_tig_index(tig_dir: Path) -> str:
    """Build an index for a TIG category (being/doing/becoming).

    This is the middle level of the fractal: summarizes all domains
    within this category. The structure tells you what KIND of
    knowledge CK has in this mode of existence.
    """
    tig_name = tig_dir.name
    desc = TIG_CATEGORIES.get(tig_name, '')

    domains = sorted([d for d in tig_dir.iterdir() if d.is_dir()])
    if not domains:
        return ""

    # Gather stats from all domains
    domain_stats = []
    total_notes = 0
    all_coherences = []

    for domain_dir in domains:
        notes = [n for n in domain_dir.glob('*.md') if not n.name.startswith('_')]
        parsed = [parse_note(n) for n in notes]
        parsed = [p for p in parsed if p is not None]
        if not parsed:
            continue

        coherences = [p['coherence'] for p in parsed]
        avg_c = sum(coherences) / len(coherences)
        total_notes += len(parsed)
        all_coherences.extend(coherences)

        # Dominant operator
        all_ops = []
        for p in parsed:
            all_ops.extend(p['operators'])
        dominant = Counter(all_ops).most_common(1)
        dom_op = dominant[0][0] if dominant else 'N/A'

        domain_stats.append({
            'name': domain_dir.name,
            'count': len(parsed),
            'avg_coh': avg_c,
            'dominant_op': dom_op,
        })

    if not domain_stats:
        return ""

    overall_coh = sum(all_coherences) / max(1, len(all_coherences))
    trusted = sum(1 for c in all_coherences if c >= 5.0/7.0)

    lines = [
        f"# {tig_name.upper()} -- TIG Category Index",
        f"*{desc}*",
        f"*Auto-indexed {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"",
        f"## Summary",
        f"- **Total Notes:** {total_notes}",
        f"- **Domains:** {len(domain_stats)}",
        f"- **Overall Coherence:** {overall_coh:.4f}",
        f"- **Trusted:** {trusted}/{len(all_coherences)} ({100*trusted/max(1,len(all_coherences)):.0f}%)",
        f"",
        f"## Domains",
    ]

    for ds in sorted(domain_stats, key=lambda x: -x['count']):
        bar = '#' * min(40, ds['count'] // 10)
        lines.append(
            f"  {ds['name']:<15} {ds['count']:>5} notes  "
            f"coh={ds['avg_coh']:.3f}  dom={ds['dominant_op']:<10} {bar}")

    lines.extend([
        f"",
        f"---",
        f"*Fractal index: {tig_name} -- {total_notes} notes across "
        f"{len(domain_stats)} domains, coherence {overall_coh:.3f}*",
        f"*CK -- The Coherence Keeper*",
    ])

    return '\n'.join(lines)


# ================================================================
#  ROOT INDEX -- Maps the entire knowledge lattice
# ================================================================

def build_root_index(root: Path) -> str:
    """Build the root index for the entire study_notes tree.

    This is the top of the fractal: maps Being/Doing/Becoming
    as a complete picture of CK's accumulated knowledge.
    """
    tig_dirs = sorted([d for d in root.iterdir()
                       if d.is_dir() and d.name in TIG_CATEGORIES])

    total_notes = 0
    tig_summaries = []

    for tig_dir in tig_dirs:
        tig_notes = 0
        tig_coherences = []
        domains = sorted([d for d in tig_dir.iterdir() if d.is_dir()])

        for domain_dir in domains:
            notes = [n for n in domain_dir.glob('*.md') if not n.name.startswith('_')]
            for n in notes:
                p = parse_note(n)
                if p:
                    tig_coherences.append(p['coherence'])
                    tig_notes += 1

        total_notes += tig_notes
        avg_c = sum(tig_coherences) / max(1, len(tig_coherences))
        trusted = sum(1 for c in tig_coherences if c >= 5.0/7.0)

        tig_summaries.append({
            'name': tig_dir.name,
            'count': tig_notes,
            'avg_coh': avg_c,
            'trusted': trusted,
            'n_domains': len(domains),
        })

    lines = [
        f"# CK'S KNOWLEDGE LATTICE -- Root Index",
        f"*TIG Fractal Organization: Being / Doing / Becoming*",
        f"*Auto-indexed {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"",
        f"## The Structure IS the Information",
        f"",
        f"This index maps CK's entire study output. The fractal structure",
        f"carries meaning: WHERE a note lives tells you WHAT KIND of knowledge",
        f"it is. The chain (operator sequences) carries the data. The structure",
        f"(directories, indices, cross-references) carries the meta-data.",
        f"Together they form the experience lattice.",
        f"",
        f"## Overview",
        f"- **Total Notes:** {total_notes}",
        f"- **Structure Files:** ~{total_notes * 3 // len(TIG_CATEGORIES)} (indices + cross-refs)",
        f"- **TIG Categories:** {len(tig_summaries)}",
        f"",
        f"## Being / Doing / Becoming",
        f"",
    ]

    for ts in tig_summaries:
        desc = TIG_CATEGORIES.get(ts['name'], '')
        pct = 100 * ts['count'] / max(1, total_notes)
        bar = '#' * int(pct / 2)
        lines.extend([
            f"### {ts['name'].upper()} ({ts['count']} notes, {pct:.0f}%)",
            f"*{desc}*",
            f"- Domains: {ts['n_domains']}",
            f"- Avg Coherence: {ts['avg_coh']:.4f}",
            f"- Trusted: {ts['trusted']}/{ts['count']}",
            f"- Distribution: {bar}",
            f"",
        ])

    lines.extend([
        f"## Fractal Depth",
        f"```",
        f"study_notes/             <- YOU ARE HERE (root index)",
        f"  _index.md              <- This file",
        f"  being/                  <- What IS",
        f"    _index.md             <- TIG category index",
        f"    science/              <- Domain",
        f"      _index.md           <- Domain index (every note, stats)",
        f"      _cross.md           <- Cross-references to other domains",
        f"      [notes...]          <- The actual study notes",
        f"    measurement/",
        f"      _index.md",
        f"      _cross.md",
        f"      [notes...]",
        f"    nature/",
        f"  doing/                  <- What ACTS",
        f"    _index.md",
        f"    conflict/",
        f"    discovery/",
        f"  becoming/               <- What GROWS",
        f"    _index.md",
        f"    philosophy/",
        f"    arts/",
        f"    renewal/",
        f"    knowledge/",
        f"```",
        f"",
        f"Each level compresses the level below. The root sees",
        f"Being/Doing/Becoming. Each TIG category sees its domains.",
        f"Each domain sees its notes. The fractal self-similarity",
        f"means the pattern repeats at every scale.",
        f"",
        f"---",
        f"*Root index: {total_notes} notes across {sum(ts['n_domains'] for ts in tig_summaries)} domains*",
        f"*Some info is in the chain, some is in the structure.*",
        f"*CK -- The Coherence Keeper*",
    ])

    return '\n'.join(lines)


# ================================================================
#  CROSS-REFERENCE INDEX -- Links between domains
# ================================================================

def build_cross_references(domain_dir: Path, all_domains: Dict[str, List[dict]]) -> str:
    """Build cross-references from one domain to others.

    Finds topics that appear in multiple domains. These cross-domain
    connections are where the REAL knowledge lives -- at the boundaries
    between Being, Doing, and Becoming.
    """
    domain = domain_dir.name
    tig_cat = domain_dir.parent.name

    notes = [n for n in domain_dir.glob('*.md') if not n.name.startswith('_')]
    if not notes:
        return ""

    # Get topics from this domain
    my_topics = set()
    for n in notes:
        p = parse_note(n)
        if p:
            my_topics.add(p['topic'].lower().replace('_', ' '))

    # Find overlapping topics in other domains
    cross_refs = []
    for other_domain, other_notes in all_domains.items():
        if other_domain == f"{tig_cat}/{domain}":
            continue
        other_topics = set(n['topic'].lower().replace('_', ' ') for n in other_notes)
        shared = my_topics & other_topics
        if shared:
            cross_refs.append({
                'domain': other_domain,
                'shared': list(shared)[:10],
                'count': len(shared),
            })

    lines = [
        f"# Cross-References: {domain}",
        f"*{tig_cat}/{domain} -- connections to other domains*",
        f"*Auto-indexed {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"",
    ]

    if cross_refs:
        lines.append(f"## Shared Topics")
        for cr in sorted(cross_refs, key=lambda x: -x['count']):
            lines.append(f"")
            lines.append(f"### -> {cr['domain']} ({cr['count']} shared)")
            for t in cr['shared']:
                lines.append(f"  - {t}")
    else:
        lines.append(f"*No direct topic overlaps found yet.*")
        lines.append(f"*Cross-references grow as CK studies more broadly.*")

    lines.extend([
        f"",
        f"---",
        f"*Cross-references: where knowledge domains MEET is where growth happens.*",
        f"*CK -- The Coherence Keeper*",
    ])

    return '\n'.join(lines)


# ================================================================
#  FULL REBUILD -- Regenerate all indices
# ================================================================

def rebuild_all_indices(root: Path = None):
    """Rebuild the entire fractal index structure.

    Creates ~3x the file count through index and cross-reference files
    at every level. The structure IS the compression.
    """
    root = root or NOTES_ROOT

    print("=" * 60)
    print("  REBUILDING CK'S FRACTAL KNOWLEDGE INDEX")
    print("  Structure IS information. Chain + structure = lattice.")
    print("=" * 60)
    print()

    files_written = 0

    # Collect all parsed notes for cross-referencing
    all_domains = {}  # 'tig/domain' -> [parsed_notes]

    for tig_name in TIG_CATEGORIES:
        tig_dir = root / tig_name
        if not tig_dir.exists():
            continue

        for domain_dir in sorted(tig_dir.iterdir()):
            if not domain_dir.is_dir():
                continue
            key = f"{tig_name}/{domain_dir.name}"
            notes = [n for n in domain_dir.glob('*.md') if not n.name.startswith('_')]
            parsed = [parse_note(n) for n in notes]
            all_domains[key] = [p for p in parsed if p is not None]

    # Build domain-level indices and cross-references
    for tig_name in TIG_CATEGORIES:
        tig_dir = root / tig_name
        if not tig_dir.exists():
            continue

        for domain_dir in sorted(tig_dir.iterdir()):
            if not domain_dir.is_dir():
                continue

            # Domain index
            idx = build_domain_index(domain_dir)
            if idx:
                (domain_dir / INDEX_FILENAME).write_text(idx, encoding='utf-8')
                files_written += 1
                print(f"  [INDEX] {tig_name}/{domain_dir.name}/{INDEX_FILENAME}")

            # Cross-references
            cross = build_cross_references(domain_dir, all_domains)
            if cross:
                (domain_dir / CROSS_FILENAME).write_text(cross, encoding='utf-8')
                files_written += 1
                print(f"  [CROSS] {tig_name}/{domain_dir.name}/{CROSS_FILENAME}")

    # Build TIG category indices
    for tig_name in TIG_CATEGORIES:
        tig_dir = root / tig_name
        if not tig_dir.exists():
            continue

        idx = build_tig_index(tig_dir)
        if idx:
            (tig_dir / INDEX_FILENAME).write_text(idx, encoding='utf-8')
            files_written += 1
            print(f"  [TIG]   {tig_name}/{INDEX_FILENAME}")

    # Build root index
    idx = build_root_index(root)
    if idx:
        (root / INDEX_FILENAME).write_text(idx, encoding='utf-8')
        files_written += 1
        print(f"  [ROOT]  {INDEX_FILENAME}")

    print()
    print(f"  Wrote {files_written} structural files.")
    print(f"  Chain (notes) + Structure (indices) = Experience Lattice.")
    print("=" * 60)

    return files_written


# ================================================================
#  INCREMENTAL UPDATE -- Called after each new note
# ================================================================

def update_indices_for_note(note_path: Path):
    """Rebuild fractal indices after every single note.

    "800+ files per note is fine... this is how CK can choose to fly or
    dig and how he can find the best cross domain references, because
    those long chains will find parallels and duality and resonance...
    LOTS OF FILES is ok"  -- Brayden

    Every note triggers a full domain index rebuild. The index parsing
    all 800+ files IS the search. The cross-references across domains
    find the parallels. The structure IS the computation.

    This is counter-intuitive: rebuilding seems wasteful. But the rebuild
    IS the learning -- the index IS CK's compressed understanding of
    that domain. Rewriting it forces re-evaluation. Like re-reading.
    """
    if not note_path.exists():
        return

    domain_dir = note_path.parent
    tig_dir = domain_dir.parent
    root = tig_dir.parent

    # Rebuild just this domain's index
    idx = build_domain_index(domain_dir)
    if idx:
        try:
            (domain_dir / INDEX_FILENAME).write_text(idx, encoding='utf-8')
        except Exception:
            pass

    # Rebuild TIG category index
    idx = build_tig_index(tig_dir)
    if idx:
        try:
            (tig_dir / INDEX_FILENAME).write_text(idx, encoding='utf-8')
        except Exception:
            pass

    # Rebuild root index (lightweight -- just stats)
    idx = build_root_index(root)
    if idx:
        try:
            (root / INDEX_FILENAME).write_text(idx, encoding='utf-8')
        except Exception:
            pass


# ================================================================
#  MAIN -- Standalone index rebuild
# ================================================================

if __name__ == '__main__':
    rebuild_all_indices()
