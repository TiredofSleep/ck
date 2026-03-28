"""
Bible Versions — Download and manage multiple translations.

Supported public domain translations:
  - KJV: King James Version (1611, classic English)
  - WEB: World English Bible (modern English, public domain)
  - BBE: Bible in Basic English (simple modern English)

The D2 algebra works on ANY English text — the Hebrew root force
mapping operates on letter shapes, not vocabulary level.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import os
import re
import json
import urllib.request
import urllib.error

BIBLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Available versions and their download sources
VERSIONS = {
    'kjv': {
        'name': 'King James Version',
        'style': 'Classic English (1611)',
        'file': 'kjv.txt',
        'url': 'https://openbible.com/textfiles/kjv.txt',
        'skip_lines': 2,  # Header lines to skip
    },
    'web': {
        'name': 'World English Bible',
        'style': 'Modern English (public domain)',
        'file': 'web.txt',
        'url': None,  # Built from embedded data
    },
    'bbe': {
        'name': 'Bible in Basic English',
        'style': 'Simple modern English',
        'file': 'bbe.txt',
        'url': None,
    },
}


def available_versions():
    """List versions with their download status."""
    result = {}
    for vid, info in VERSIONS.items():
        path = os.path.join(BIBLE_DIR, info['file'])
        result[vid] = {
            'name': info['name'],
            'style': info['style'],
            'downloaded': os.path.exists(path),
            'path': path,
        }
    return result


def get_version_path(version_id='kjv'):
    """Get the file path for a Bible version."""
    info = VERSIONS.get(version_id)
    if not info:
        return None
    return os.path.join(BIBLE_DIR, info['file'])


def download_version(version_id):
    """Download a Bible version. Returns (success, message)."""
    info = VERSIONS.get(version_id)
    if not info:
        return False, f'Unknown version: {version_id}'

    dest = os.path.join(BIBLE_DIR, info['file'])
    if os.path.exists(dest):
        return True, f'{info["name"]} already downloaded'

    if info['url']:
        try:
            print(f'[Bible] Downloading {info["name"]}...')
            urllib.request.urlretrieve(info['url'], dest)
            size = os.path.getsize(dest)
            return True, f'Downloaded {info["name"]} ({size:,} bytes)'
        except Exception as e:
            return False, f'Download failed: {e}'

    return False, f'{info["name"]} is not available for auto-download yet'


def convert_from_json_source(json_path, output_path, book_names=None):
    """Convert a JSON Bible source to tab-separated format.

    Expected JSON format: list of {"book": int, "chapter": int, "verse": int, "text": str}
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not book_names:
        book_names = _DEFAULT_BOOK_NAMES

    lines = []
    for entry in data:
        book_num = entry.get('book', entry.get('b', 0))
        chapter = entry.get('chapter', entry.get('c', 0))
        verse = entry.get('verse', entry.get('v', 0))
        text = entry.get('text', entry.get('t', ''))

        book_name = book_names.get(book_num, f'Book{book_num}')
        ref = f'{book_name} {chapter}:{verse}'
        lines.append(f'{ref}\t{text}')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return len(lines)


_DEFAULT_BOOK_NAMES = {
    1: 'Genesis', 2: 'Exodus', 3: 'Leviticus', 4: 'Numbers',
    5: 'Deuteronomy', 6: 'Joshua', 7: 'Judges', 8: 'Ruth',
    9: '1 Samuel', 10: '2 Samuel', 11: '1 Kings', 12: '2 Kings',
    13: '1 Chronicles', 14: '2 Chronicles', 15: 'Ezra', 16: 'Nehemiah',
    17: 'Esther', 18: 'Job', 19: 'Psalm', 20: 'Proverbs',
    21: 'Ecclesiastes', 22: 'Song of Solomon', 23: 'Isaiah',
    24: 'Jeremiah', 25: 'Lamentations', 26: 'Ezekiel', 27: 'Daniel',
    28: 'Hosea', 29: 'Joel', 30: 'Amos', 31: 'Obadiah',
    32: 'Jonah', 33: 'Micah', 34: 'Nahum', 35: 'Habakkuk',
    36: 'Zephaniah', 37: 'Haggai', 38: 'Zechariah', 39: 'Malachi',
    40: 'Matthew', 41: 'Mark', 42: 'Luke', 43: 'John',
    44: 'Acts', 45: 'Romans', 46: '1 Corinthians', 47: '2 Corinthians',
    48: 'Galatians', 49: 'Ephesians', 50: 'Philippians', 51: 'Colossians',
    52: '1 Thessalonians', 53: '2 Thessalonians', 54: '1 Timothy',
    55: '2 Timothy', 56: 'Titus', 57: 'Philemon', 58: 'Hebrews',
    59: 'James', 60: '1 Peter', 61: '2 Peter', 62: '1 John',
    63: '2 John', 64: '3 John', 65: 'Jude', 66: 'Revelation',
}
