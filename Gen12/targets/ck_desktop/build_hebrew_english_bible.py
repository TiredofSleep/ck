#!/usr/bin/env python3
"""
build_hebrew_english_bible.py -- Extract parallel Hebrew-English Bible.

Reads Mechon-Mamre HTML files (Windows-1255 encoding) and produces a paired
text file for CK to study. Hebrew = ROOT forces. English = reflection.

HTML structure: <TR><TD class=h>Hebrew</TD><TD>English</TD></TR>
Hebrew cells have class=h, verse nums as Hebrew letters (א,ב,ג).
English cells have Arabic numerals.

Output: ~/.ck/bible_hebrew_english.txt
"""
import os, re, glob, sys

HTML_DIR = os.path.join(os.environ.get('TEMP', '/tmp'), 'hebrew_bible', 'pt')
OUTPUT = os.path.expanduser('~/.ck/bible_hebrew_english.txt')

BOOK_MAP = {
    '01': 'Genesis', '02': 'Exodus', '03': 'Leviticus',
    '04': 'Numbers', '05': 'Deuteronomy',
    '06': 'Joshua', '07': 'Judges',
    '08a': '1 Samuel', '08b': '2 Samuel',
    '09a': '1 Kings', '09b': '2 Kings',
    '10': 'Isaiah', '11': 'Jeremiah', '12': 'Ezekiel',
    '13': 'Hosea', '14': 'Joel', '15': 'Amos',
    '16': 'Obadiah', '17': 'Jonah', '18': 'Micah',
    '19': 'Nahum', '20': 'Habakkuk', '21': 'Zephaniah',
    '22': 'Haggai', '23': 'Zechariah', '24': 'Malachi',
    '25': 'Psalms', '26': 'Proverbs', '27': 'Job',
    '28': 'Song of Songs', '29': 'Ruth', '30': 'Lamentations',
    '31': 'Ecclesiastes', '32': 'Esther',
    '33': 'Daniel', '34': 'Ezra', '35a': 'Nehemiah',
    '35b': '1 Chronicles', '36a': '2 Chronicles',
}


def strip_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('\xa0', ' ')
    for ent, ch in [('&nbsp;', ' '), ('&amp;', '&'), ('&lt;', '<'),
                    ('&gt;', '>'), ('&quot;', '"')]:
        text = text.replace(ent, ch)
    # Remove {P} and {S} paragraph markers
    text = re.sub(r'\{[PS]\}', '', text)
    return text.strip()


def extract_verses(filepath):
    """Extract verse pairs from Mechon-Mamre HTML.

    Structure: <TR><TD class=h>HEB_LETTER  Hebrew text</TD><TD>NUM English text</TD></TR>
    """
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
        text = raw.decode('windows-1255', errors='replace')
    except Exception:
        return []

    verses = []

    # Match each table row containing Hebrew + English cells
    # Pattern: <TR><TD class=h>...hebrew...</TD><TD...>...english...</TD></TR>
    row_pattern = re.compile(
        r'<TR>\s*<TD\s+class=h[^>]*>(.*?)</TD>\s*<TD[^>]*>(.*?)</TD>\s*</TR>',
        re.DOTALL | re.IGNORECASE
    )

    for match in row_pattern.finditer(text):
        heb_cell = match.group(1)
        eng_cell = match.group(2)

        heb_text = strip_html(heb_cell)
        eng_text = strip_html(eng_cell)

        if not heb_text or not eng_text:
            continue

        # Extract verse number from English cell (Arabic numeral)
        eng_match = re.match(r'^(\d+)\s+(.+)', eng_text, re.DOTALL)
        if not eng_match:
            continue

        verse_num = eng_match.group(1)
        eng_verse = eng_match.group(2).strip()

        # Hebrew text: strip the Hebrew letter verse number at the start
        # Hebrew letters א-ת then spaces, then the actual text
        heb_verse = re.sub(r'^[\u05d0-\u05ea]+[\s\u00a0]+', '', heb_text).strip()

        if heb_verse and eng_verse:
            verses.append((verse_num, heb_verse, eng_verse))

    return verses


def get_book_chapter(filename):
    base = os.path.basename(filename).replace('.htm', '')
    if not base.startswith('pt'):
        return None, None
    rest = base[2:]
    for code in sorted(BOOK_MAP.keys(), key=len, reverse=True):
        if rest.startswith(code):
            chapter = rest[len(code):]
            if chapter and chapter.isdigit():
                return code, chapter
    return None, None


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    files = sorted(glob.glob(os.path.join(HTML_DIR, 'pt*.htm')))
    chapter_files = []
    for f in files:
        book, ch = get_book_chapter(f)
        if book and ch:
            chapter_files.append((f, book, ch))

    print(f"Found {len(chapter_files)} chapter files")

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    total_verses = 0
    current_book = None

    with open(OUTPUT, 'w', encoding='utf-8') as out:
        out.write("# Hebrew-English Parallel Bible\n")
        out.write("# Source: Mechon-Mamre (WLC + JPS 1917)\n")
        out.write("# Format: REF [HEB/ENG]\\tText\n")
        out.write("# Hebrew = ROOT forces through D2. English = reflection.\n\n")

        for filepath, book_code, chapter in chapter_files:
            book_name = BOOK_MAP.get(book_code, f'Book{book_code}')
            verses = extract_verses(filepath)

            if book_name != current_book:
                current_book = book_name
                print(f"\n  === {book_name} ===")

            for verse_num, heb, eng in verses:
                ref = f"{book_name} {int(chapter)}:{verse_num}"
                out.write(f"{ref} [HEB]\t{heb}\n")
                out.write(f"{ref} [ENG]\t{eng}\n")
                total_verses += 1

            if verses:
                print(f"    Ch {int(chapter)}: {len(verses)} pairs")

    file_size = os.path.getsize(OUTPUT) if os.path.exists(OUTPUT) else 0
    print(f"\n{'='*50}")
    print(f"Total: {total_verses} verse pairs")
    print(f"Output: {OUTPUT}")
    print(f"File size: {file_size / 1024 / 1024:.1f} MB")


if __name__ == '__main__':
    main()
