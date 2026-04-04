"""
index_submission.py — Auto-index a collaboration GitHub issue into submissions/INDEX.md

Triggered by GitHub Actions when an issue labeled 'collaboration' is opened or edited.
Reads issue body, detects problem area and coherence class, appends to the right table.

No email. No inbox. The filesystem organizes itself.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ── Read from environment (set by GitHub Actions) ──────────────────────────
issue_number = os.environ.get('ISSUE_NUMBER', '?')
issue_title  = os.environ.get('ISSUE_TITLE', '')
issue_body   = os.environ.get('ISSUE_BODY', '')
issue_user   = os.environ.get('ISSUE_USER', 'unknown')
issue_url    = os.environ.get('ISSUE_URL', '')
issue_date_raw = os.environ.get('ISSUE_DATE', '')

# Parse date
try:
    dt = datetime.fromisoformat(issue_date_raw.replace('Z', '+00:00'))
    date_str = dt.strftime('%Y-%m-%d')
except Exception:
    date_str = datetime.utcnow().strftime('%Y-%m-%d')

# ── Detect problem area ────────────────────────────────────────────────────
PROBLEM_AREAS = {
    'Riemann Hypothesis':  ['riemann', 'rh', 'zeta', 'zeros'],
    'Navier-Stokes':       ['navier', 'stokes', 'ns', 'fluid', 'blow'],
    'BSD Conjecture':      ['bsd', 'birch', 'swinnerton', 'elliptic', 'rank', 'sha'],
    'Hodge Conjecture':    ['hodge', 'algebraic cycle', 'cohomology'],
    'Yang-Mills':          ['yang', 'mills', 'ym', 'mass gap', 'gauge'],
    'P vs NP':             ['p vs np', 'p=np', 'complexity', 'sat', 'np-hard'],
}

body_lower = issue_body.lower()
title_lower = issue_title.lower()
search_text = body_lower + ' ' + title_lower

# Detect checked checkboxes in issue body (markdown `[x]` pattern)
checked_areas = []
for area, keywords in PROBLEM_AREAS.items():
    area_pattern = re.escape(area.lower())
    if re.search(r'\[x\].*' + area_pattern, body_lower) or \
       re.search(area_pattern + r'.*\[x\]', body_lower):
        checked_areas.append(area)

if not checked_areas:
    # Fall back to keyword detection
    for area, keywords in PROBLEM_AREAS.items():
        if any(kw in search_text for kw in keywords):
            checked_areas.append(area)

if not checked_areas:
    checked_areas = ['Other / Cross-Problem']

# ── Detect coherence class ─────────────────────────────────────────────────
coherence = 'unknown'
if re.search(r'\[x\].*resolved', body_lower):
    coherence = 'RESOLVED'
elif re.search(r'\[x\].*boundary', body_lower):
    coherence = 'BOUNDARY'
elif re.search(r'\[x\].*escaped', body_lower):
    coherence = 'ESCAPED'
elif re.search(r'\[x\].*haven', body_lower):
    coherence = '—'

# ── Extract user's link ────────────────────────────────────────────────────
link_match = re.search(r'https?://\S+', issue_body)
user_link = link_match.group(0).strip('.,)>') if link_match else issue_url

# ── Detect "index it" checkbox ────────────────────────────────────────────
wants_index = bool(re.search(r'\[x\].*yes.*index', body_lower) or
                   re.search(r'\[x\].*index it', body_lower))
if not wants_index:
    # Default: index everything unless explicitly opted out
    wants_index = not bool(re.search(r'\[x\].*no.*just connecting', body_lower))

if not wants_index:
    print(f"Issue #{issue_number}: user opted out of indexing. No change to INDEX.md.")
    sys.exit(0)

# ── Extract brief description ──────────────────────────────────────────────
# Look for "What you found" section
what_match = re.search(
    r'what you found.*?what.*?working on.*?\n+(.*?)(?:\n\n|\n##|$)',
    issue_body, re.IGNORECASE | re.DOTALL
)
if what_match:
    brief = what_match.group(1).strip()[:80].replace('|', '/').replace('\n', ' ')
else:
    brief = issue_title.replace('[COLLAB]', '').strip()[:80]

# ── Build table row ────────────────────────────────────────────────────────
row = f"| {date_str} | [@{issue_user}](https://github.com/{issue_user}) | {brief} | {coherence} | [#{issue_number}]({issue_url}) |"

# ── Update INDEX.md ────────────────────────────────────────────────────────
index_path = Path('submissions/INDEX.md')
content = index_path.read_text(encoding='utf-8')

inserted = set()
for area in checked_areas:
    if area in inserted:
        continue
    inserted.add(area)

    # Find the section header
    section_pattern = re.compile(
        r'(## ' + re.escape(area) + r'\n.*?\n\|.*?\|\n\|[-| ]+\|\n)((?:\|.*\|\n)*)',
        re.DOTALL
    )
    match = section_pattern.search(content)
    if match:
        header = match.group(1)
        existing_rows = match.group(2)
        # Check if this issue is already indexed
        if f'#{issue_number}]' in existing_rows:
            print(f"Issue #{issue_number} already indexed under '{area}'. Skipping.")
            continue
        # Remove placeholder row if present
        existing_rows_clean = re.sub(r'\| — \| — \| — \| — \| — \|\n', '', existing_rows)
        new_section = header + existing_rows_clean + row + '\n'
        content = content[:match.start()] + new_section + content[match.end():]
        print(f"Indexed #{issue_number} under '{area}'")
    else:
        # Section not found — append to Other
        fallback = '## Other / Cross-Problem'
        fb_match = re.search(
            r'(' + re.escape(fallback) + r'\n.*?\n\|.*?\|\n\|[-| ]+\|\n)((?:\|.*\|\n)*)',
            content, re.DOTALL
        )
        if fb_match:
            existing_rows = fb_match.group(2)
            existing_rows_clean = re.sub(r'\| — \| — \| — \| — \| — \|\n', '', existing_rows)
            new_section = fb_match.group(1) + existing_rows_clean + row + '\n'
            content = content[:fb_match.start()] + new_section + content[fb_match.end():]
            print(f"Indexed #{issue_number} under 'Other / Cross-Problem' (section '{area}' not found)")

index_path.write_text(content, encoding='utf-8')
print(f"submissions/INDEX.md updated.")
