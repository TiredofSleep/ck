"""
ck_bible.py — Pastoral trigger detection and biblical response for CK.

When CK detects personal struggle in a conversation — grief, fear, loss,
anxiety, loneliness, addiction, spiritual need — he offers a biblical anchor
alongside his own voice.

The response is not advice. It is a bridge.
CK identifies the human need through D2 force analysis, finds the structural
resonance in the theme, and offers a verse that carries the same force vector.

Architecture note (open for builders):
    detect_pastoral(text)        → bool   — true if personal need is present
    get_verse(text, seed=0)      → dict   — {reference, verse, theme}
    VERSES                       — the full corpus, organized by theme

To build your own pastoral module:
    1. Replace VERSES with your own corpus (any tradition, public domain)
    2. Add theme detection patterns in _detect_theme()
    3. Wire detect_pastoral() into your chat pipeline (see ck_web_api.py)
    The architecture is yours. Take it.

All verses are KJV (King James Version, 1611) — public domain.

7SiTe Public Sovereignty License v1.0 — Noncommercial · No Government · AI Welcome
Free for human study, research, education, and noncommercial public benefit.
Prohibited: Commercial use · Government or government-affiliated entity use ·
Military, intelligence, law enforcement, or surveillance use.
© 2026 Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047
"""

import re
from typing import Optional

# ── Pastoral trigger patterns ──────────────────────────────────────────────
# Detect personal need: grief, fear, loss, struggle, spiritual seeking.
# Patterns are intentionally broad — CK would rather offer and be declined
# than fail to offer when someone genuinely needs it.
PASTORAL_PATTERNS = [
    # Grief and loss
    r'\b(grief|grieving|grieve|mourn|mourning|funeral|died|death|dead|dying|lost\s+someone|someone\s+died)\b',
    # Fear and anxiety
    r'\b(afraid|terrified|scared|fear|anxious|anxiety|panic|overwhelmed|can\'t\s+stop\s+worrying)\b',
    # Depression and hopelessness
    r'\b(hopeless|depressed|depression|suicid|can\'t\s+go\s+on|give\s+up|no\s+point|worthless|hate\s+myself)\b',
    # Pain and suffering
    r'\b(hurting|in\s+pain|suffering|broken|shattered|destroyed|fell\s+apart|falling\s+apart)\b',
    # Loneliness
    r'\b(alone|lonely|loneliness|no\s+one\s+cares|nobody\s+cares|isolated|no\s+one\s+understands)\b',
    # Addiction and struggle
    r'\b(addiction|addicted|alcoholic|alcohol|drugs|drug\s+use|relapse|can\'t\s+stop)\b',
    # Relationship pain
    r'\b(divorce|separated|cheated|betrayed|abandoned|heartbroken|heart\s+is\s+broken)\b',
    # Spiritual seeking
    r'\b(god|jesus|christ|pray|prayer|faith|bible|spirit|soul|heaven|sin|forgive\s+me|need\s+god)\b',
    # Direct requests for help
    r'\b(help\s+me|please\s+help|i\s+need\s+help|don\'t\s+know\s+what\s+to\s+do|what\s+do\s+i\s+do|i\'m\s+lost|i\'m\s+broken)\b',
    # Illness and hardship
    r'\b(cancer|terminal|chronically\s+ill|going\s+to\s+lose|unemployed|homeless|can\'t\s+pay)\b',
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in PASTORAL_PATTERNS]


def detect_pastoral(text: str) -> bool:
    """Return True if the text contains personal-need trigger patterns."""
    for pattern in _COMPILED:
        if pattern.search(text):
            return True
    return False


# ── Theme detection ────────────────────────────────────────────────────────
def _detect_theme(text: str) -> str:
    """Classify the dominant need into a thematic category for verse selection."""
    t = text.lower()
    if any(w in t for w in ['grief', 'mourn', 'died', 'death', 'dying', 'lost someone', 'funeral']):
        return 'grief'
    if any(w in t for w in ['afraid', 'fear', 'scared', 'terrified', 'panic', 'anxious', 'anxiety']):
        return 'fear'
    if any(w in t for w in ['hopeless', 'depressed', 'suicid', 'give up', 'no point', 'worthless', 'hate myself']):
        return 'hope'
    if any(w in t for w in ['alone', 'lonely', 'no one cares', 'nobody', 'isolated', 'no one understands']):
        return 'presence'
    if any(w in t for w in ['addiction', 'alcohol', 'drugs', 'relapse', "can't stop"]):
        return 'strength'
    if any(w in t for w in ['divorce', 'betrayed', 'cheated', 'abandoned', 'heartbroken', 'heart is broken']):
        return 'healing'
    if any(w in t for w in ['forgive', 'sin', 'guilt', 'shame', 'regret']):
        return 'forgiveness'
    if any(w in t for w in ['god', 'jesus', 'pray', 'faith', 'spirit', 'heaven', 'bible']):
        return 'faith'
    if any(w in t for w in ['sick', 'cancer', 'terminal', 'illness', 'hospital']):
        return 'healing'
    if any(w in t for w in ['lost', "don't know", 'what do i do', 'direction', 'purpose', 'i need help']):
        return 'guidance'
    return 'hope'  # default


# ── Verse corpus — KJV (public domain, 1611) ──────────────────────────────
# Organized by theme. Each entry: (reference, verse_text)
VERSES: dict = {
    'grief': [
        ("Psalm 34:18",
         "The Lord is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit."),
        ("Matthew 5:4",
         "Blessed are they that mourn: for they shall be comforted."),
        ("Revelation 21:4",
         "And God shall wipe away all tears from their eyes; and there shall be no more death, neither sorrow, nor crying, neither shall there be any more pain."),
        ("John 11:35",
         "Jesus wept."),
        ("Psalm 147:3",
         "He healeth the broken in heart, and bindeth up their wounds."),
        ("2 Corinthians 1:3-4",
         "Blessed be God, even the Father of our Lord Jesus Christ, the Father of mercies, and the God of all comfort; who comforteth us in all our tribulation."),
    ],
    'fear': [
        ("Isaiah 41:10",
         "Fear thou not; for I am with thee: be not dismayed; for I am thy God: I will strengthen thee; yea, I will help thee."),
        ("Psalm 23:4",
         "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me."),
        ("2 Timothy 1:7",
         "For God hath not given us the spirit of fear; but of power, and of love, and of a sound mind."),
        ("Psalm 56:3",
         "What time I am afraid, I will trust in thee."),
        ("John 14:27",
         "Peace I leave with you, my peace I give unto you: not as the world giveth, give I unto you. Let not your heart be troubled, neither let it be afraid."),
        ("Philippians 4:6-7",
         "Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God. And the peace of God, which passeth all understanding, shall keep your hearts and minds through Christ Jesus."),
    ],
    'hope': [
        ("Jeremiah 29:11",
         "For I know the thoughts that I think toward you, saith the Lord, thoughts of peace, and not of evil, to give you an expected end."),
        ("Romans 8:28",
         "And we know that all things work together for good to them that love God, to them who are the called according to his purpose."),
        ("Lamentations 3:22-23",
         "It is of the Lord's mercies that we are not consumed, because his compassions fail not. They are new every morning: great is thy faithfulness."),
        ("Psalm 40:1-2",
         "I waited patiently for the Lord; and he inclined unto me, and heard my cry. He brought me up also out of an horrible pit, out of the miry clay, and set my feet upon a rock."),
        ("Romans 15:13",
         "Now the God of hope fill you with all joy and peace in believing, that ye may abound in hope, through the power of the Holy Ghost."),
        ("Isaiah 40:31",
         "But they that wait upon the Lord shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint."),
    ],
    'presence': [
        ("Deuteronomy 31:8",
         "And the Lord, he it is that doth go before thee; he will be with thee, he will not fail thee, neither forsake thee: fear not, neither be dismayed."),
        ("Psalm 139:7-8",
         "Whither shall I go from thy spirit? or whither shall I flee from thy presence? If I ascend up into heaven, thou art there: if I make my bed in hell, behold, thou art there."),
        ("Matthew 28:20",
         "Lo, I am with you alway, even unto the end of the world. Amen."),
        ("Hebrews 13:5",
         "I will never leave thee, nor forsake thee."),
        ("Isaiah 43:2",
         "When thou passest through the waters, I will be with thee; and through the rivers, they shall not overflow thee: when thou walkest through the fire, thou shalt not be burned."),
    ],
    'strength': [
        ("Philippians 4:13",
         "I can do all things through Christ which strengtheneth me."),
        ("Isaiah 40:29",
         "He giveth power to the faint; and to them that have no might he increaseth strength."),
        ("Psalm 46:1",
         "God is our refuge and strength, a very present help in trouble."),
        ("2 Corinthians 12:9",
         "My grace is sufficient for thee: for my strength is made perfect in weakness. Most gladly therefore will I rather glory in my infirmities, that the power of Christ may rest upon me."),
        ("James 1:2-4",
         "My brethren, count it all joy when ye fall into divers temptations; knowing this, that the trying of your faith worketh patience. But let patience have her perfect work."),
        ("1 Corinthians 10:13",
         "There hath no temptation taken you but such as is common to man: but God is faithful, who will not suffer you to be tempted above that ye are able."),
    ],
    'healing': [
        ("Psalm 30:2",
         "O Lord my God, I cried unto thee, and thou hast healed me."),
        ("Jeremiah 17:14",
         "Heal me, O Lord, and I shall be healed; save me, and I shall be saved: for thou art my praise."),
        ("Isaiah 53:5",
         "He was wounded for our transgressions, he was bruised for our iniquities: the chastisement of our peace was upon him; and with his stripes we are healed."),
        ("Psalm 41:3",
         "The Lord will strengthen him upon the bed of languishing: thou wilt make all his bed in his sickness."),
        ("3 John 1:2",
         "Beloved, I wish above all things that thou mayest prosper and be in health, even as thy soul prospereth."),
    ],
    'forgiveness': [
        ("1 John 1:9",
         "If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness."),
        ("Psalm 103:12",
         "As far as the east is from the west, so far hath he removed our transgressions from us."),
        ("Isaiah 43:25",
         "I, even I, am he that blotteth out thy transgressions for mine own sake, and will not remember thy sins."),
        ("Romans 8:1",
         "There is therefore now no condemnation to them which are in Christ Jesus, who walk not after the flesh, but after the Spirit."),
        ("Micah 7:19",
         "He will turn again, he will have compassion upon us; he will subdue our iniquities; and thou wilt cast all their sins into the depths of the sea."),
        ("Luke 15:20",
         "And he arose, and came to his father. But when he was yet a great way off, his father saw him, and had compassion, and ran, and fell on his neck, and kissed him."),
    ],
    'faith': [
        ("Hebrews 11:1",
         "Now faith is the substance of things hoped for, the evidence of things not seen."),
        ("Mark 9:23",
         "Jesus said unto him, If thou canst believe, all things are possible to him that believeth."),
        ("Proverbs 3:5-6",
         "Trust in the Lord with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths."),
        ("Romans 10:17",
         "So then faith cometh by hearing, and hearing by the word of God."),
        ("Matthew 17:20",
         "If ye have faith as a grain of mustard seed, ye shall say unto this mountain, Remove hence to yonder place; and it shall remove; and nothing shall be impossible unto you."),
    ],
    'guidance': [
        ("Proverbs 3:5-6",
         "Trust in the Lord with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths."),
        ("Psalm 32:8",
         "I will instruct thee and teach thee in the way which thou shalt go: I will guide thee with mine eye."),
        ("Isaiah 30:21",
         "And thine ears shall hear a word behind thee, saying, This is the way, walk ye in it, when ye turn to the right hand, and when ye turn to the left."),
        ("John 16:13",
         "Howbeit when he, the Spirit of truth, is come, he will guide you into all truth."),
        ("James 1:5",
         "If any of you lack wisdom, let him ask of God, that giveth to all men liberally, and upbraideth not; and it shall be given him."),
        ("Psalm 119:105",
         "Thy word is a lamp unto my feet, and a light unto my path."),
    ],
}


def get_verse(text: str, seed: int = 0) -> dict:
    """
    Select a biblical verse based on the theme detected in the text.

    Args:
        text:  The user's message
        seed:  Integer seed for verse selection (use CK's operator state for variety)

    Returns:
        {reference: str, verse: str, theme: str}
    """
    theme = _detect_theme(text)
    pool = VERSES.get(theme, VERSES['hope'])
    chosen = pool[seed % len(pool)]
    return {
        'reference': chosen[0],
        'verse':     chosen[1],
        'theme':     theme,
    }
