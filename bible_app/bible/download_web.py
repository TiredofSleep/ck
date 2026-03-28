"""
Download the World English Bible (WEB) from bible-api.com.

Public domain modern English translation.
Downloads chapter by chapter, writes tab-separated format.

Usage: python -m bible_app.bible.download_web
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web.txt')

# All 66 books with their chapter counts
BOOKS = [
    ('Genesis', 50), ('Exodus', 40), ('Leviticus', 27), ('Numbers', 36),
    ('Deuteronomy', 34), ('Joshua', 24), ('Judges', 21), ('Ruth', 4),
    ('1 Samuel', 31), ('2 Samuel', 24), ('1 Kings', 22), ('2 Kings', 25),
    ('1 Chronicles', 29), ('2 Chronicles', 36), ('Ezra', 10), ('Nehemiah', 13),
    ('Esther', 10), ('Job', 42), ('Psalms', 150), ('Proverbs', 31),
    ('Ecclesiastes', 12), ('Song of Solomon', 8), ('Isaiah', 66),
    ('Jeremiah', 52), ('Lamentations', 5), ('Ezekiel', 48), ('Daniel', 12),
    ('Hosea', 14), ('Joel', 3), ('Amos', 9), ('Obadiah', 1),
    ('Jonah', 4), ('Micah', 7), ('Nahum', 3), ('Habakkuk', 3),
    ('Zephaniah', 3), ('Haggai', 2), ('Zechariah', 14), ('Malachi', 4),
    ('Matthew', 28), ('Mark', 16), ('Luke', 24), ('John', 21),
    ('Acts', 28), ('Romans', 16), ('1 Corinthians', 16), ('2 Corinthians', 13),
    ('Galatians', 6), ('Ephesians', 6), ('Philippians', 4), ('Colossians', 4),
    ('1 Thessalonians', 5), ('2 Thessalonians', 3), ('1 Timothy', 6),
    ('2 Timothy', 4), ('Titus', 3), ('Philemon', 1), ('Hebrews', 13),
    ('James', 5), ('1 Peter', 5), ('2 Peter', 3), ('1 John', 5),
    ('2 John', 1), ('3 John', 1), ('Jude', 1), ('Revelation', 22),
]

TOTAL_CHAPTERS = sum(c for _, c in BOOKS)
API_BASE = 'https://bible-api.com'


def download():
    if os.path.exists(OUTPUT):
        size = os.path.getsize(OUTPUT)
        if size > 3_000_000:
            print(f'WEB already downloaded ({size:,} bytes)')
            return True

    print(f'Downloading World English Bible ({TOTAL_CHAPTERS} chapters)...')
    print(f'This will take a few minutes (rate-limited to be polite)')

    lines = []
    done = 0
    errors = 0

    for book, chapters in BOOKS:
        for ch in range(1, chapters + 1):
            # URL-encode book name
            book_url = book.replace(' ', '+')
            url = f'{API_BASE}/{book_url}+{ch}?translation=web'

            for attempt in range(3):
                try:
                    req = urllib.request.Request(url, headers={
                        'User-Agent': 'BibleCompanion/1.0 (7SiteLLC)',
                    })
                    resp = urllib.request.urlopen(req, timeout=15)
                    data = json.loads(resp.read().decode('utf-8'))

                    for v in data.get('verses', []):
                        text = v['text'].strip().replace('\n', ' ')
                        if text:
                            ref = f"{v['book_name']} {v['chapter']}:{v['verse']}"
                            lines.append(f'{ref}\t{text}')

                    done += 1
                    if done % 50 == 0:
                        pct = done / TOTAL_CHAPTERS * 100
                        print(f'  [{pct:.0f}%] {done}/{TOTAL_CHAPTERS} chapters, '
                              f'{len(lines)} verses')
                    break

                except (urllib.error.URLError, urllib.error.HTTPError,
                        TimeoutError, json.JSONDecodeError) as e:
                    errors += 1
                    if attempt < 2:
                        time.sleep(2)
                    else:
                        print(f'  SKIP: {book} {ch} ({e})')

            # Be polite to the API
            time.sleep(0.3)

    if not lines:
        print('No verses downloaded!')
        return False

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Done! {len(lines)} verses saved to {OUTPUT}')
    print(f'  Errors: {errors}')
    return True


if __name__ == '__main__':
    download()
