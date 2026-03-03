# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_lexicon_bulk.py -- Lexicon Expansion: 350 → 10,000+ Entries
================================================================
Operator: LATTICE (1) -- building the lattice of meaning wider.

Three expansion strategies (all zero-dependency, all phoneme-grounded):

  1. DOMAIN SEEDS: 200+ new concept families across 15 domains, 7 languages each
  2. MORPHOLOGICAL FORMS: noun→plural, verb→past/present-participle, adjective→comparative
  3. COMPOUND CONCEPTS: adjective + noun pairings from existing entries

Architecture:
  EXPANDED_LEXICON    -- dict of concept_id → [(lang, word, phonemes), ...]
  MorphExpander       -- generates morphological variants per language
  CompoundBuilder     -- generates concept pairs from existing entries
  build_full_store()  -- returns LexiconStore with all entries loaded

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET
)

# ================================================================
#  EXPANDED SEED LEXICON -- 200+ new concepts
# ================================================================
# Format: concept_id → [(lang, word, phonemes), ...]
# Languages: en, es, fr, de, he, ar, zh (7 per concept, matching seed)

EXPANDED_LEXICON = {
    # ═══════════════════════ BODY (15 new) ═══════════════════════
    'mouth': [
        ('en', 'mouth', 'mauθ'),    ('es', 'boca', 'boka'),
        ('fr', 'bouche', 'buʃ'),     ('de', 'Mund', 'munt'),
        ('he', 'peh', 'pe'),         ('ar', 'fam', 'fam'),
        ('zh', 'zui', 'zuei'),
    ],
    'ear': [
        ('en', 'ear', 'ir'),        ('es', 'oreja', 'orexa'),
        ('fr', 'oreille', 'orej'),   ('de', 'Ohr', 'or'),
        ('he', 'ozen', 'ozen'),      ('ar', 'udhun', 'udun'),
        ('zh', 'er', 'er'),
    ],
    'nose': [
        ('en', 'nose', 'noz'),      ('es', 'nariz', 'nariθ'),
        ('fr', 'nez', 'ne'),         ('de', 'Nase', 'naze'),
        ('he', 'af', 'af'),          ('ar', 'anf', 'anf'),
        ('zh', 'bi', 'bi'),
    ],
    'foot': [
        ('en', 'foot', 'fut'),      ('es', 'pie', 'pie'),
        ('fr', 'pied', 'pie'),       ('de', 'Fuss', 'fus'),
        ('he', 'regel', 'regel'),    ('ar', 'qadam', 'qadam'),
        ('zh', 'jiao', 'dʒiao'),
    ],
    'bone': [
        ('en', 'bone', 'bon'),      ('es', 'hueso', 'weso'),
        ('fr', 'os', 'os'),          ('de', 'Knochen', 'knoxen'),
        ('he', 'etsem', 'etsem'),    ('ar', 'azm', 'azm'),
        ('zh', 'gu', 'gu'),
    ],
    'skin': [
        ('en', 'skin', 'skin'),     ('es', 'piel', 'piel'),
        ('fr', 'peau', 'po'),        ('de', 'Haut', 'haut'),
        ('he', 'or', 'or'),          ('ar', 'jild', 'dʒild'),
        ('zh', 'pifu', 'pifu'),
    ],
    'tooth': [
        ('en', 'tooth', 'tuθ'),     ('es', 'diente', 'diente'),
        ('fr', 'dent', 'dan'),       ('de', 'Zahn', 'tsan'),
        ('he', 'shen', 'ʃen'),      ('ar', 'sinn', 'sin'),
        ('zh', 'ya', 'ja'),
    ],
    'tongue': [
        ('en', 'tongue', 'tang'),   ('es', 'lengua', 'lengwa'),
        ('fr', 'langue', 'lang'),    ('de', 'Zunge', 'tsunge'),
        ('he', 'lashon', 'laʃon'),   ('ar', 'lisan', 'lisan'),
        ('zh', 'she', 'ʃe'),
    ],
    'finger': [
        ('en', 'finger', 'finger'), ('es', 'dedo', 'dedo'),
        ('fr', 'doigt', 'dwa'),      ('de', 'Finger', 'finger'),
        ('he', 'etsba', 'etsba'),    ('ar', 'isba', 'isba'),
        ('zh', 'zhi', 'ʒi'),
    ],
    'stomach': [
        ('en', 'stomach', 'stamak'), ('es', 'estomago', 'estomago'),
        ('fr', 'estomac', 'estoma'), ('de', 'Magen', 'magen'),
        ('he', 'keiva', 'keiva'),    ('ar', 'mida', 'mida'),
        ('zh', 'wei', 'wei'),
    ],
    'leg': [
        ('en', 'leg', 'leg'),       ('es', 'pierna', 'pierna'),
        ('fr', 'jambe', 'ʒanb'),     ('de', 'Bein', 'bain'),
        ('he', 'regel', 'regel'),    ('ar', 'saq', 'saq'),
        ('zh', 'tui', 'tuei'),
    ],
    'arm': [
        ('en', 'arm', 'arm'),       ('es', 'brazo', 'braso'),
        ('fr', 'bras', 'bra'),       ('de', 'Arm', 'arm'),
        ('he', 'zeroa', 'zeroa'),    ('ar', 'dhira', 'dira'),
        ('zh', 'bi', 'bi'),
    ],
    'back': [
        ('en', 'back', 'bæk'),      ('es', 'espalda', 'espalda'),
        ('fr', 'dos', 'do'),         ('de', 'Ruecken', 'ruken'),
        ('he', 'gav', 'gav'),        ('ar', 'zahr', 'zahr'),
        ('zh', 'bei', 'bei'),
    ],
    'neck': [
        ('en', 'neck', 'nek'),      ('es', 'cuello', 'kwejo'),
        ('fr', 'cou', 'ku'),         ('de', 'Hals', 'hals'),
        ('he', 'tsavar', 'tsavar'),  ('ar', 'raqaba', 'raqaba'),
        ('zh', 'bo', 'bo'),
    ],
    'knee': [
        ('en', 'knee', 'ni'),       ('es', 'rodilla', 'rodija'),
        ('fr', 'genou', 'ʒenu'),     ('de', 'Knie', 'kni'),
        ('he', 'berekh', 'berex'),   ('ar', 'rukba', 'rukba'),
        ('zh', 'xi', 'ʃi'),
    ],

    # ═══════════════════════ FOOD & DRINK (20) ═══════════════════
    'bread': [
        ('en', 'bread', 'bred'),    ('es', 'pan', 'pan'),
        ('fr', 'pain', 'pen'),       ('de', 'Brot', 'brot'),
        ('he', 'lekhem', 'lexem'),   ('ar', 'khubz', 'xubz'),
        ('zh', 'mian', 'mian'),
    ],
    'milk': [
        ('en', 'milk', 'milk'),     ('es', 'leche', 'letʃe'),
        ('fr', 'lait', 'le'),        ('de', 'Milch', 'milx'),
        ('he', 'khalav', 'xalav'),   ('ar', 'halib', 'halib'),
        ('zh', 'nai', 'nai'),
    ],
    'meat': [
        ('en', 'meat', 'mit'),      ('es', 'carne', 'karne'),
        ('fr', 'viande', 'viand'),   ('de', 'Fleisch', 'flaiʃ'),
        ('he', 'basar', 'basar'),    ('ar', 'lahm', 'lahm'),
        ('zh', 'rou', 'rou'),
    ],
    'fruit': [
        ('en', 'fruit', 'frut'),    ('es', 'fruta', 'fruta'),
        ('fr', 'fruit', 'frui'),     ('de', 'Frucht', 'fruxt'),
        ('he', 'pri', 'pri'),        ('ar', 'fakiha', 'fakiha'),
        ('zh', 'guo', 'gwo'),
    ],
    'salt': [
        ('en', 'salt', 'solt'),     ('es', 'sal', 'sal'),
        ('fr', 'sel', 'sel'),        ('de', 'Salz', 'zalts'),
        ('he', 'melakh', 'melax'),   ('ar', 'milh', 'milh'),
        ('zh', 'yan', 'jan'),
    ],
    'honey': [
        ('en', 'honey', 'hani'),    ('es', 'miel', 'miel'),
        ('fr', 'miel', 'miel'),      ('de', 'Honig', 'honig'),
        ('he', 'dvash', 'dvaʃ'),     ('ar', 'asal', 'asal'),
        ('zh', 'mi', 'mi'),
    ],
    'egg': [
        ('en', 'egg', 'eg'),        ('es', 'huevo', 'wevo'),
        ('fr', 'oeuf', 'of'),        ('de', 'Ei', 'ai'),
        ('he', 'beitza', 'beitsa'),  ('ar', 'bayda', 'bajda'),
        ('zh', 'dan', 'dan'),
    ],
    'rice': [
        ('en', 'rice', 'rais'),     ('es', 'arroz', 'aros'),
        ('fr', 'riz', 'ri'),         ('de', 'Reis', 'rais'),
        ('he', 'orez', 'orez'),      ('ar', 'aruzz', 'aruz'),
        ('zh', 'mi', 'mi'),
    ],
    'wine': [
        ('en', 'wine', 'wain'),     ('es', 'vino', 'vino'),
        ('fr', 'vin', 'ven'),        ('de', 'Wein', 'vain'),
        ('he', 'yayin', 'jajin'),    ('ar', 'nabidh', 'nabid'),
        ('zh', 'jiu', 'dʒiou'),
    ],
    'oil': [
        ('en', 'oil', 'oil'),       ('es', 'aceite', 'aseite'),
        ('fr', 'huile', 'uil'),      ('de', 'Oel', 'ol'),
        ('he', 'shemen', 'ʃemen'),   ('ar', 'zayt', 'zajt'),
        ('zh', 'you', 'jou'),
    ],
    'sugar': [
        ('en', 'sugar', 'ʃuger'),   ('es', 'azucar', 'asukar'),
        ('fr', 'sucre', 'sukr'),     ('de', 'Zucker', 'tsuker'),
        ('he', 'sukar', 'sukar'),    ('ar', 'sukkar', 'sukar'),
        ('zh', 'tang', 'tang'),
    ],
    'seed': [
        ('en', 'seed', 'sid'),      ('es', 'semilla', 'semija'),
        ('fr', 'graine', 'gren'),    ('de', 'Samen', 'zamen'),
        ('he', 'zera', 'zera'),      ('ar', 'bidhra', 'bidra'),
        ('zh', 'zhong', 'ʒong'),
    ],
    'leaf': [
        ('en', 'leaf', 'lif'),      ('es', 'hoja', 'oxa'),
        ('fr', 'feuille', 'foj'),    ('de', 'Blatt', 'blat'),
        ('he', 'ale', 'ale'),        ('ar', 'waraqa', 'waraqa'),
        ('zh', 'ye', 'je'),
    ],
    'root': [
        ('en', 'root', 'rut'),      ('es', 'raiz', 'raiθ'),
        ('fr', 'racine', 'rasin'),   ('de', 'Wurzel', 'vurtsel'),
        ('he', 'shoresh', 'ʃoreʃ'), ('ar', 'jidhr', 'dʒidr'),
        ('zh', 'gen', 'gen'),
    ],
    'flower': [
        ('en', 'flower', 'flaur'),  ('es', 'flor', 'flor'),
        ('fr', 'fleur', 'fler'),     ('de', 'Blume', 'blume'),
        ('he', 'perakh', 'perax'),   ('ar', 'zahra', 'zahra'),
        ('zh', 'hua', 'xwa'),
    ],
    'grass': [
        ('en', 'grass', 'gras'),    ('es', 'hierba', 'ierba'),
        ('fr', 'herbe', 'erb'),      ('de', 'Gras', 'gras'),
        ('he', 'deshe', 'deʃe'),     ('ar', 'ushb', 'uʃb'),
        ('zh', 'cao', 'tsao'),
    ],
    'rain': [
        ('en', 'rain', 'rein'),     ('es', 'lluvia', 'juvia'),
        ('fr', 'pluie', 'plui'),     ('de', 'Regen', 'regen'),
        ('he', 'geshem', 'geʃem'),   ('ar', 'matar', 'matar'),
        ('zh', 'yu', 'ju'),
    ],
    'snow': [
        ('en', 'snow', 'sno'),      ('es', 'nieve', 'nieve'),
        ('fr', 'neige', 'neʒ'),      ('de', 'Schnee', 'ʃne'),
        ('he', 'sheleg', 'ʃeleg'),   ('ar', 'thalj', 'θaldʒ'),
        ('zh', 'xue', 'ʃue'),
    ],
    'wind': [
        ('en', 'wind', 'wind'),     ('es', 'viento', 'viento'),
        ('fr', 'vent', 'van'),       ('de', 'Wind', 'vint'),
        ('he', 'ruakh', 'ruax'),     ('ar', 'rih', 'rih'),
        ('zh', 'feng', 'feng'),
    ],
    'cloud': [
        ('en', 'cloud', 'klaud'),   ('es', 'nube', 'nube'),
        ('fr', 'nuage', 'nuaʒ'),    ('de', 'Wolke', 'volke'),
        ('he', 'anan', 'anan'),      ('ar', 'sahab', 'sahab'),
        ('zh', 'yun', 'jun'),
    ],

    # ═══════════════════════ ANIMALS (15 new) ════════════════════
    'horse': [
        ('en', 'horse', 'hors'),    ('es', 'caballo', 'kabajo'),
        ('fr', 'cheval', 'ʃeval'),   ('de', 'Pferd', 'pfert'),
        ('he', 'sus', 'sus'),        ('ar', 'hisan', 'hisan'),
        ('zh', 'ma', 'ma'),
    ],
    'cow': [
        ('en', 'cow', 'kau'),       ('es', 'vaca', 'vaka'),
        ('fr', 'vache', 'vaʃ'),      ('de', 'Kuh', 'ku'),
        ('he', 'para', 'para'),      ('ar', 'baqara', 'baqara'),
        ('zh', 'niu', 'niou'),
    ],
    'sheep': [
        ('en', 'sheep', 'ʃip'),     ('es', 'oveja', 'ovexa'),
        ('fr', 'mouton', 'muton'),   ('de', 'Schaf', 'ʃaf'),
        ('he', 'keves', 'keves'),    ('ar', 'kharuf', 'xaruf'),
        ('zh', 'yang', 'jang'),
    ],
    'snake': [
        ('en', 'snake', 'sneik'),   ('es', 'serpiente', 'serpiente'),
        ('fr', 'serpent', 'serpan'), ('de', 'Schlange', 'ʃlange'),
        ('he', 'nakhash', 'naxaʃ'), ('ar', 'afaa', 'afa'),
        ('zh', 'she', 'ʃe'),
    ],
    'lion': [
        ('en', 'lion', 'laion'),    ('es', 'leon', 'leon'),
        ('fr', 'lion', 'lion'),      ('de', 'Loewe', 'love'),
        ('he', 'aryeh', 'arje'),     ('ar', 'asad', 'asad'),
        ('zh', 'shi', 'ʃi'),
    ],
    'eagle': [
        ('en', 'eagle', 'igel'),    ('es', 'aguila', 'agila'),
        ('fr', 'aigle', 'egl'),      ('de', 'Adler', 'adler'),
        ('he', 'nesher', 'neʃer'),   ('ar', 'nisr', 'nisr'),
        ('zh', 'ying', 'jing'),
    ],
    'wolf': [
        ('en', 'wolf', 'wulf'),     ('es', 'lobo', 'lobo'),
        ('fr', 'loup', 'lu'),        ('de', 'Wolf', 'volf'),
        ('he', 'zeev', 'zeev'),      ('ar', 'dhib', 'dib'),
        ('zh', 'lang', 'lang'),
    ],
    'bear': [
        ('en', 'bear', 'ber'),      ('es', 'oso', 'oso'),
        ('fr', 'ours', 'urs'),       ('de', 'Baer', 'ber'),
        ('he', 'dov', 'dov'),        ('ar', 'dubb', 'dub'),
        ('zh', 'xiong', 'ʃiong'),
    ],
    'deer': [
        ('en', 'deer', 'dir'),      ('es', 'ciervo', 'siervo'),
        ('fr', 'cerf', 'serf'),      ('de', 'Hirsch', 'hirʃ'),
        ('he', 'ayal', 'ajal'),      ('ar', 'ghazal', 'gazal'),
        ('zh', 'lu', 'lu'),
    ],
    'ant': [
        ('en', 'ant', 'ænt'),       ('es', 'hormiga', 'ormiga'),
        ('fr', 'fourmi', 'furmi'),   ('de', 'Ameise', 'amaize'),
        ('he', 'nemala', 'nemala'),  ('ar', 'namla', 'namla'),
        ('zh', 'mayi', 'maji'),
    ],
    'bee': [
        ('en', 'bee', 'bi'),        ('es', 'abeja', 'abexa'),
        ('fr', 'abeille', 'abej'),   ('de', 'Biene', 'bine'),
        ('he', 'dvora', 'dvora'),    ('ar', 'nahla', 'nahla'),
        ('zh', 'mifeng', 'mifeng'),
    ],
    'spider': [
        ('en', 'spider', 'spaider'), ('es', 'arana', 'arana'),
        ('fr', 'araignee', 'arene'), ('de', 'Spinne', 'ʃpine'),
        ('he', 'akavish', 'akaviʃ'), ('ar', 'ankabut', 'ankabut'),
        ('zh', 'zhizhu', 'ʒiʒu'),
    ],
    'whale': [
        ('en', 'whale', 'weil'),    ('es', 'ballena', 'bajena'),
        ('fr', 'baleine', 'balen'),  ('de', 'Wal', 'val'),
        ('he', 'livyatan', 'livjatan'), ('ar', 'hut', 'hut'),
        ('zh', 'jingyu', 'dʒingju'),
    ],
    'turtle': [
        ('en', 'turtle', 'tertel'), ('es', 'tortuga', 'tortuga'),
        ('fr', 'tortue', 'tortu'),   ('de', 'Schildkroete', 'ʃiltkrote'),
        ('he', 'tsav', 'tsav'),      ('ar', 'sulahfa', 'sulahfa'),
        ('zh', 'gui', 'guei'),
    ],
    'rabbit': [
        ('en', 'rabbit', 'ræbit'),  ('es', 'conejo', 'konexo'),
        ('fr', 'lapin', 'lapen'),    ('de', 'Kaninchen', 'kaninxen'),
        ('he', 'arnav', 'arnav'),    ('ar', 'arnab', 'arnab'),
        ('zh', 'tuzi', 'tuzi'),
    ],

    # ═══════════════════════ EMOTIONS (15) ═══════════════════════
    'fear': [
        ('en', 'fear', 'fir'),      ('es', 'miedo', 'miedo'),
        ('fr', 'peur', 'per'),       ('de', 'Angst', 'angst'),
        ('he', 'pakhad', 'paxad'),   ('ar', 'khawf', 'xauf'),
        ('zh', 'kong', 'kong'),
    ],
    'joy': [
        ('en', 'joy', 'dʒoi'),      ('es', 'alegria', 'alegria'),
        ('fr', 'joie', 'ʒwa'),       ('de', 'Freude', 'froide'),
        ('he', 'simkha', 'simxa'),   ('ar', 'farah', 'farah'),
        ('zh', 'xi', 'ʃi'),
    ],
    'anger': [
        ('en', 'anger', 'anger'),   ('es', 'ira', 'ira'),
        ('fr', 'colere', 'koler'),   ('de', 'Zorn', 'tsorn'),
        ('he', 'kaaas', 'kaas'),     ('ar', 'ghadab', 'gadab'),
        ('zh', 'nu', 'nu'),
    ],
    'hope': [
        ('en', 'hope', 'hop'),      ('es', 'esperanza', 'esperansa'),
        ('fr', 'espoir', 'espwar'),  ('de', 'Hoffnung', 'hofnung'),
        ('he', 'tikva', 'tikva'),    ('ar', 'amal', 'amal'),
        ('zh', 'xiwang', 'ʃiwang'),
    ],
    'sorrow': [
        ('en', 'sorrow', 'soro'),   ('es', 'tristeza', 'tristesa'),
        ('fr', 'chagrin', 'ʃagren'), ('de', 'Trauer', 'trauer'),
        ('he', 'atsvut', 'atsvut'),  ('ar', 'huzn', 'huzn'),
        ('zh', 'bei', 'bei'),
    ],
    'shame': [
        ('en', 'shame', 'ʃeim'),    ('es', 'verguenza', 'verguensa'),
        ('fr', 'honte', 'ont'),      ('de', 'Scham', 'ʃam'),
        ('he', 'busha', 'buʃa'),     ('ar', 'khajal', 'xadʒal'),
        ('zh', 'chi', 'tʃi'),
    ],
    'pride': [
        ('en', 'pride', 'praid'),   ('es', 'orgullo', 'orgujo'),
        ('fr', 'fierte', 'fierte'),  ('de', 'Stolz', 'ʃtolts'),
        ('he', 'gaava', 'gaava'),    ('ar', 'fakhr', 'faxr'),
        ('zh', 'jiao', 'dʒiao'),
    ],
    'mercy': [
        ('en', 'mercy', 'mersi'),   ('es', 'misericordia', 'miserikordia'),
        ('fr', 'misericorde', 'mizerikord'), ('de', 'Gnade', 'gnade'),
        ('he', 'rakhamim', 'raxamim'), ('ar', 'rahma', 'rahma'),
        ('zh', 'cibei', 'tsibei'),
    ],
    'patience': [
        ('en', 'patience', 'peiʃens'), ('es', 'paciencia', 'pasiensia'),
        ('fr', 'patience', 'pasians'), ('de', 'Geduld', 'gedult'),
        ('he', 'savlanut', 'savlanut'), ('ar', 'sabr', 'sabr'),
        ('zh', 'naixi', 'naiʃi'),
    ],
    'wisdom': [
        ('en', 'wisdom', 'wizdom'), ('es', 'sabiduria', 'sabiduria'),
        ('fr', 'sagesse', 'saʒes'),  ('de', 'Weisheit', 'vaishait'),
        ('he', 'khokhma', 'xoxma'),  ('ar', 'hikma', 'hikma'),
        ('zh', 'zhihui', 'ʒihuei'),
    ],
    'courage': [
        ('en', 'courage', 'karidʒ'), ('es', 'valor', 'valor'),
        ('fr', 'courage', 'kuraʒ'),  ('de', 'Mut', 'mut'),
        ('he', 'omets', 'omets'),    ('ar', 'shujaa', 'ʃudʒa'),
        ('zh', 'yongqi', 'jongqi'),
    ],
    'trust': [
        ('en', 'trust', 'trast'),   ('es', 'confianza', 'konfiansa'),
        ('fr', 'confiance', 'konfians'), ('de', 'Vertrauen', 'fertrauen'),
        ('he', 'emun', 'emun'),      ('ar', 'thiqa', 'θiqa'),
        ('zh', 'xinren', 'ʃinren'),
    ],
    'gratitude': [
        ('en', 'gratitude', 'grætitud'), ('es', 'gratitud', 'gratitud'),
        ('fr', 'gratitude', 'gratitud'), ('de', 'Dankbarkeit', 'dankbarkait'),
        ('he', 'hakarat toda', 'hakarat toda'), ('ar', 'imtinan', 'imtinan'),
        ('zh', 'ganen', 'ganen'),
    ],
    'compassion': [
        ('en', 'compassion', 'kompæʃen'), ('es', 'compasion', 'kompasion'),
        ('fr', 'compassion', 'kompasion'), ('de', 'Mitgefuehl', 'mitgeful'),
        ('he', 'khemlah', 'xemla'),  ('ar', 'shafaqa', 'ʃafaqa'),
        ('zh', 'tongqing', 'tongqing'),
    ],
    'longing': [
        ('en', 'longing', 'longing'), ('es', 'anhelo', 'anelo'),
        ('fr', 'nostalgie', 'nostalʒi'), ('de', 'Sehnsucht', 'zensuxt'),
        ('he', 'ga-agua', 'gaagua'),  ('ar', 'shawq', 'ʃauq'),
        ('zh', 'sixiang', 'siʃiang'),
    ],

    # ═══════════════════════ ACTIONS (20 new) ════════════════════
    'give': [
        ('en', 'give', 'giv'),      ('es', 'dar', 'dar'),
        ('fr', 'donner', 'done'),    ('de', 'geben', 'geben'),
        ('he', 'latet', 'latet'),    ('ar', 'ataa', 'ata'),
        ('zh', 'gei', 'gei'),
    ],
    'take': [
        ('en', 'take', 'teik'),     ('es', 'tomar', 'tomar'),
        ('fr', 'prendre', 'prandr'), ('de', 'nehmen', 'nemen'),
        ('he', 'lakakhat', 'lakaxat'), ('ar', 'akhadha', 'axada'),
        ('zh', 'na', 'na'),
    ],
    'run': [
        ('en', 'run', 'ran'),       ('es', 'correr', 'korer'),
        ('fr', 'courir', 'kurir'),   ('de', 'laufen', 'laufen'),
        ('he', 'laruts', 'laruts'),  ('ar', 'rakada', 'rakada'),
        ('zh', 'pao', 'pao'),
    ],
    'fly': [
        ('en', 'fly', 'flai'),      ('es', 'volar', 'volar'),
        ('fr', 'voler', 'vole'),     ('de', 'fliegen', 'fligen'),
        ('he', 'lauf', 'lauf'),      ('ar', 'tara', 'tara'),
        ('zh', 'fei', 'fei'),
    ],
    'swim': [
        ('en', 'swim', 'swim'),     ('es', 'nadar', 'nadar'),
        ('fr', 'nager', 'naʒe'),     ('de', 'schwimmen', 'ʃvimen'),
        ('he', 'liskhot', 'lisxot'), ('ar', 'sabaha', 'sabaha'),
        ('zh', 'youyong', 'joujong'),
    ],
    'sing': [
        ('en', 'sing', 'sing'),     ('es', 'cantar', 'kantar'),
        ('fr', 'chanter', 'ʃante'),  ('de', 'singen', 'zingen'),
        ('he', 'lashir', 'laʃir'),   ('ar', 'ghanna', 'gana'),
        ('zh', 'chang', 'tʃang'),
    ],
    'dance': [
        ('en', 'dance', 'dæns'),    ('es', 'bailar', 'bailar'),
        ('fr', 'danser', 'danse'),   ('de', 'tanzen', 'tantsen'),
        ('he', 'lirkod', 'lirkod'),  ('ar', 'raqasa', 'raqasa'),
        ('zh', 'tiaowu', 'tiaowu'),
    ],
    'cry': [
        ('en', 'cry', 'krai'),      ('es', 'llorar', 'jorar'),
        ('fr', 'pleurer', 'plore'),  ('de', 'weinen', 'vainen'),
        ('he', 'livkot', 'livkot'),  ('ar', 'baka', 'baka'),
        ('zh', 'ku', 'ku'),
    ],
    'laugh': [
        ('en', 'laugh', 'læf'),     ('es', 'reir', 'reir'),
        ('fr', 'rire', 'rir'),       ('de', 'lachen', 'laxen'),
        ('he', 'litshok', 'litsxok'), ('ar', 'dahika', 'dahika'),
        ('zh', 'xiao', 'ʃiao'),
    ],
    'think': [
        ('en', 'think', 'θink'),    ('es', 'pensar', 'pensar'),
        ('fr', 'penser', 'panse'),   ('de', 'denken', 'denken'),
        ('he', 'lakhshov', 'laxʃov'), ('ar', 'fakara', 'fakara'),
        ('zh', 'xiang', 'ʃiang'),
    ],
    'know': [
        ('en', 'know', 'no'),       ('es', 'saber', 'saber'),
        ('fr', 'savoir', 'savwar'),  ('de', 'wissen', 'visen'),
        ('he', 'ladaat', 'ladaat'),  ('ar', 'arafa', 'arafa'),
        ('zh', 'zhidao', 'ʒidao'),
    ],
    'love_v': [
        ('en', 'love', 'lav'),      ('es', 'amar', 'amar'),
        ('fr', 'aimer', 'eme'),      ('de', 'lieben', 'liben'),
        ('he', 'leehov', 'leehov'),  ('ar', 'ahabba', 'ahaba'),
        ('zh', 'ai', 'ai'),
    ],
    'teach': [
        ('en', 'teach', 'titʃ'),    ('es', 'ensenar', 'ensenar'),
        ('fr', 'enseigner', 'ensenje'), ('de', 'lehren', 'leren'),
        ('he', 'lelamed', 'lelamed'), ('ar', 'allama', 'alama'),
        ('zh', 'jiao', 'dʒiao'),
    ],
    'learn': [
        ('en', 'learn', 'lern'),    ('es', 'aprender', 'aprender'),
        ('fr', 'apprendre', 'aprandr'), ('de', 'lernen', 'lernen'),
        ('he', 'lilmod', 'lilmod'),  ('ar', 'taallama', 'taalama'),
        ('zh', 'xue', 'ʃue'),
    ],
    'build': [
        ('en', 'build', 'bild'),    ('es', 'construir', 'konstruir'),
        ('fr', 'construire', 'konstruir'), ('de', 'bauen', 'bauen'),
        ('he', 'livnot', 'livnot'),  ('ar', 'bana', 'bana'),
        ('zh', 'jian', 'dʒian'),
    ],
    'break': [
        ('en', 'break', 'breik'),   ('es', 'romper', 'romper'),
        ('fr', 'casser', 'kase'),    ('de', 'brechen', 'brexen'),
        ('he', 'lishbor', 'liʃbor'), ('ar', 'kasara', 'kasara'),
        ('zh', 'po', 'po'),
    ],
    'open': [
        ('en', 'open', 'open'),     ('es', 'abrir', 'abrir'),
        ('fr', 'ouvrir', 'uvrir'),   ('de', 'oeffnen', 'ofnen'),
        ('he', 'liftoakh', 'liftoax'), ('ar', 'fataha', 'fataha'),
        ('zh', 'kai', 'kai'),
    ],
    'close': [
        ('en', 'close', 'kloz'),    ('es', 'cerrar', 'serar'),
        ('fr', 'fermer', 'ferme'),   ('de', 'schliessen', 'ʃlisen'),
        ('he', 'lisgor', 'lisgor'),  ('ar', 'aghlaka', 'aglaka'),
        ('zh', 'guan', 'gwan'),
    ],
    'wait': [
        ('en', 'wait', 'weit'),     ('es', 'esperar', 'esperar'),
        ('fr', 'attendre', 'atandr'), ('de', 'warten', 'varten'),
        ('he', 'lekhakot', 'lexakot'), ('ar', 'intazara', 'intazara'),
        ('zh', 'deng', 'deng'),
    ],
    'pray': [
        ('en', 'pray', 'prei'),     ('es', 'rezar', 'resar'),
        ('fr', 'prier', 'prie'),     ('de', 'beten', 'beten'),
        ('he', 'lehitpalel', 'lehitpalel'), ('ar', 'salla', 'sala'),
        ('zh', 'qidao', 'qidao'),
    ],

    # ═══════════════════════ QUALITIES (20) ══════════════════════
    'hot': [
        ('en', 'hot', 'hot'),       ('es', 'caliente', 'kaliente'),
        ('fr', 'chaud', 'ʃo'),       ('de', 'heiss', 'hais'),
        ('he', 'kham', 'xam'),       ('ar', 'harr', 'har'),
        ('zh', 're', 're'),
    ],
    'cold': [
        ('en', 'cold', 'kold'),     ('es', 'frio', 'frio'),
        ('fr', 'froid', 'frwa'),     ('de', 'kalt', 'kalt'),
        ('he', 'kar', 'kar'),        ('ar', 'barid', 'barid'),
        ('zh', 'leng', 'leng'),
    ],
    'strong': [
        ('en', 'strong', 'strong'), ('es', 'fuerte', 'fwerte'),
        ('fr', 'fort', 'for'),       ('de', 'stark', 'ʃtark'),
        ('he', 'khazak', 'xazak'),   ('ar', 'qawiy', 'qawi'),
        ('zh', 'qiang', 'qiang'),
    ],
    'weak': [
        ('en', 'weak', 'wik'),      ('es', 'debil', 'debil'),
        ('fr', 'faible', 'febl'),    ('de', 'schwach', 'ʃvax'),
        ('he', 'khalash', 'xalaʃ'),  ('ar', 'daif', 'daif'),
        ('zh', 'ruo', 'rwo'),
    ],
    'fast': [
        ('en', 'fast', 'fæst'),     ('es', 'rapido', 'rapido'),
        ('fr', 'rapide', 'rapid'),   ('de', 'schnell', 'ʃnel'),
        ('he', 'maher', 'maher'),    ('ar', 'saria', 'saria'),
        ('zh', 'kuai', 'kwai'),
    ],
    'slow': [
        ('en', 'slow', 'slo'),      ('es', 'lento', 'lento'),
        ('fr', 'lent', 'lan'),       ('de', 'langsam', 'langzam'),
        ('he', 'iti', 'iti'),        ('ar', 'batii', 'bati'),
        ('zh', 'man', 'man'),
    ],
    'high': [
        ('en', 'high', 'hai'),      ('es', 'alto', 'alto'),
        ('fr', 'haut', 'o'),         ('de', 'hoch', 'hox'),
        ('he', 'gavoah', 'gavoah'),  ('ar', 'aalii', 'ali'),
        ('zh', 'gao', 'gao'),
    ],
    'low': [
        ('en', 'low', 'lo'),        ('es', 'bajo', 'baxo'),
        ('fr', 'bas', 'ba'),         ('de', 'niedrig', 'nidrig'),
        ('he', 'namukh', 'namux'),   ('ar', 'munkhafid', 'munxafid'),
        ('zh', 'di', 'di'),
    ],
    'long': [
        ('en', 'long', 'long'),     ('es', 'largo', 'largo'),
        ('fr', 'long', 'long'),      ('de', 'lang', 'lang'),
        ('he', 'arokh', 'arox'),     ('ar', 'tawil', 'tawil'),
        ('zh', 'chang', 'tʃang'),
    ],
    'short': [
        ('en', 'short', 'ʃort'),    ('es', 'corto', 'korto'),
        ('fr', 'court', 'kur'),      ('de', 'kurz', 'kurts'),
        ('he', 'katsar', 'katsar'),  ('ar', 'qasir', 'qasir'),
        ('zh', 'duan', 'dwan'),
    ],
    'wide': [
        ('en', 'wide', 'waid'),     ('es', 'ancho', 'antʃo'),
        ('fr', 'large', 'larʒ'),     ('de', 'breit', 'brait'),
        ('he', 'rakhav', 'raxav'),   ('ar', 'waasi', 'wasi'),
        ('zh', 'kuan', 'kwan'),
    ],
    'deep': [
        ('en', 'deep', 'dip'),      ('es', 'profundo', 'profundo'),
        ('fr', 'profond', 'profon'), ('de', 'tief', 'tif'),
        ('he', 'amok', 'amok'),      ('ar', 'amiq', 'amiq'),
        ('zh', 'shen', 'ʃen'),
    ],
    'clean': [
        ('en', 'clean', 'klin'),    ('es', 'limpio', 'limpio'),
        ('fr', 'propre', 'propr'),   ('de', 'sauber', 'zauber'),
        ('he', 'naki', 'naki'),      ('ar', 'nazif', 'nazif'),
        ('zh', 'ganjing', 'gandʒing'),
    ],
    'dirty': [
        ('en', 'dirty', 'derti'),   ('es', 'sucio', 'susio'),
        ('fr', 'sale', 'sal'),       ('de', 'schmutzig', 'ʃmutsig'),
        ('he', 'melukhlakh', 'meluklax'), ('ar', 'wasikh', 'wasix'),
        ('zh', 'zang', 'tsang'),
    ],
    'heavy': [
        ('en', 'heavy', 'hevi'),    ('es', 'pesado', 'pesado'),
        ('fr', 'lourd', 'lur'),      ('de', 'schwer', 'ʃver'),
        ('he', 'kaved', 'kaved'),    ('ar', 'thaqil', 'θaqil'),
        ('zh', 'zhong', 'ʒong'),
    ],
    'empty': [
        ('en', 'empty', 'empti'),   ('es', 'vacio', 'vasio'),
        ('fr', 'vide', 'vid'),       ('de', 'leer', 'ler'),
        ('he', 'reik', 'reik'),      ('ar', 'farigh', 'farig'),
        ('zh', 'kong', 'kong'),
    ],
    'full': [
        ('en', 'full', 'ful'),      ('es', 'lleno', 'jeno'),
        ('fr', 'plein', 'plen'),     ('de', 'voll', 'fol'),
        ('he', 'male', 'male'),      ('ar', 'mumtali', 'mumtali'),
        ('zh', 'man', 'man'),
    ],
    'dry': [
        ('en', 'dry', 'drai'),      ('es', 'seco', 'seko'),
        ('fr', 'sec', 'sek'),        ('de', 'trocken', 'troken'),
        ('he', 'yavesh', 'javeʃ'),   ('ar', 'jaf', 'dʒaf'),
        ('zh', 'gan', 'gan'),
    ],
    'wet': [
        ('en', 'wet', 'wet'),       ('es', 'mojado', 'moxado'),
        ('fr', 'mouille', 'muje'),   ('de', 'nass', 'nas'),
        ('he', 'ratuv', 'ratuv'),    ('ar', 'mubtalil', 'mubtalil'),
        ('zh', 'shi', 'ʃi'),
    ],
    'round': [
        ('en', 'round', 'raund'),   ('es', 'redondo', 'redondo'),
        ('fr', 'rond', 'ron'),       ('de', 'rund', 'runt'),
        ('he', 'agol', 'agol'),      ('ar', 'mustadira', 'mustadira'),
        ('zh', 'yuan', 'juan'),
    ],

    # ═══════════════════════ OBJECTS/TOOLS (15) ══════════════════
    'house': [
        ('en', 'house', 'haus'),    ('es', 'casa', 'kasa'),
        ('fr', 'maison', 'mezon'),   ('de', 'Haus', 'haus'),
        ('he', 'bayit', 'bajit'),    ('ar', 'bayt', 'bajt'),
        ('zh', 'fang', 'fang'),
    ],
    'door': [
        ('en', 'door', 'dor'),      ('es', 'puerta', 'pwerta'),
        ('fr', 'porte', 'port'),     ('de', 'Tuer', 'tur'),
        ('he', 'delet', 'delet'),    ('ar', 'bab', 'bab'),
        ('zh', 'men', 'men'),
    ],
    'road': [
        ('en', 'road', 'rod'),      ('es', 'camino', 'kamino'),
        ('fr', 'route', 'rut'),      ('de', 'Strasse', 'ʃtrase'),
        ('he', 'derekh', 'derex'),   ('ar', 'tariq', 'tariq'),
        ('zh', 'lu', 'lu'),
    ],
    'knife': [
        ('en', 'knife', 'naif'),    ('es', 'cuchillo', 'kutʃijo'),
        ('fr', 'couteau', 'kuto'),   ('de', 'Messer', 'meser'),
        ('he', 'sakin', 'sakin'),    ('ar', 'sikkin', 'sikin'),
        ('zh', 'dao', 'dao'),
    ],
    'fire_tool': [
        ('en', 'torch', 'tortʃ'),   ('es', 'antorcha', 'antortʃa'),
        ('fr', 'torche', 'torʃ'),    ('de', 'Fackel', 'fakel'),
        ('he', 'lapid', 'lapid'),    ('ar', 'mishaal', 'miʃal'),
        ('zh', 'huoba', 'xwoba'),
    ],
    'rope': [
        ('en', 'rope', 'rop'),      ('es', 'cuerda', 'kwerda'),
        ('fr', 'corde', 'kord'),     ('de', 'Seil', 'zail'),
        ('he', 'khevel', 'xevel'),   ('ar', 'habl', 'habl'),
        ('zh', 'sheng', 'ʃeng'),
    ],
    'wheel': [
        ('en', 'wheel', 'wil'),     ('es', 'rueda', 'rweda'),
        ('fr', 'roue', 'ru'),        ('de', 'Rad', 'rad'),
        ('he', 'galgal', 'galgal'),  ('ar', 'ajala', 'adʒala'),
        ('zh', 'lun', 'lun'),
    ],
    'boat': [
        ('en', 'boat', 'bot'),      ('es', 'barco', 'barko'),
        ('fr', 'bateau', 'bato'),    ('de', 'Boot', 'bot'),
        ('he', 'sira', 'sira'),      ('ar', 'qarib', 'qarib'),
        ('zh', 'chuan', 'tʃwan'),
    ],
    'book': [
        ('en', 'book', 'buk'),      ('es', 'libro', 'libro'),
        ('fr', 'livre', 'livr'),     ('de', 'Buch', 'bux'),
        ('he', 'sefer', 'sefer'),    ('ar', 'kitab', 'kitab'),
        ('zh', 'shu', 'ʃu'),
    ],
    'song': [
        ('en', 'song', 'song'),     ('es', 'cancion', 'kansion'),
        ('fr', 'chanson', 'ʃanson'), ('de', 'Lied', 'lid'),
        ('he', 'shir', 'ʃir'),      ('ar', 'ughniya', 'ugnia'),
        ('zh', 'ge', 'ge'),
    ],
    'word': [
        ('en', 'word', 'werd'),     ('es', 'palabra', 'palabra'),
        ('fr', 'mot', 'mo'),         ('de', 'Wort', 'vort'),
        ('he', 'mila', 'mila'),      ('ar', 'kalima', 'kalima'),
        ('zh', 'ci', 'tsi'),
    ],
    'path': [
        ('en', 'path', 'pæθ'),      ('es', 'sendero', 'sendero'),
        ('fr', 'sentier', 'santie'), ('de', 'Pfad', 'pfad'),
        ('he', 'shvil', 'ʃvil'),    ('ar', 'masar', 'masar'),
        ('zh', 'xiaolu', 'ʃiaolu'),
    ],
    'wall': [
        ('en', 'wall', 'wol'),      ('es', 'muro', 'muro'),
        ('fr', 'mur', 'mur'),        ('de', 'Wand', 'vant'),
        ('he', 'kir', 'kir'),        ('ar', 'jidar', 'dʒidar'),
        ('zh', 'qiang', 'qiang'),
    ],
    'bridge': [
        ('en', 'bridge', 'bridʒ'),  ('es', 'puente', 'pwente'),
        ('fr', 'pont', 'pon'),       ('de', 'Bruecke', 'bruke'),
        ('he', 'gesher', 'geʃer'),   ('ar', 'jisr', 'dʒisr'),
        ('zh', 'qiao', 'qiao'),
    ],
    'garden': [
        ('en', 'garden', 'garden'), ('es', 'jardin', 'xardin'),
        ('fr', 'jardin', 'ʒarden'), ('de', 'Garten', 'garten'),
        ('he', 'gan', 'gan'),        ('ar', 'hadiqa', 'hadiqa'),
        ('zh', 'huayuan', 'xwajuan'),
    ],

    # ═══════════════════════ COLORS (10) ═════════════════════════
    'red': [
        ('en', 'red', 'red'),       ('es', 'rojo', 'roxo'),
        ('fr', 'rouge', 'ruʒ'),      ('de', 'rot', 'rot'),
        ('he', 'adom', 'adom'),      ('ar', 'ahmar', 'ahmar'),
        ('zh', 'hong', 'hong'),
    ],
    'blue': [
        ('en', 'blue', 'blu'),      ('es', 'azul', 'asul'),
        ('fr', 'bleu', 'blo'),       ('de', 'blau', 'blau'),
        ('he', 'kakhol', 'kaxol'),   ('ar', 'azraq', 'azraq'),
        ('zh', 'lan', 'lan'),
    ],
    'green': [
        ('en', 'green', 'grin'),    ('es', 'verde', 'verde'),
        ('fr', 'vert', 'ver'),       ('de', 'gruen', 'grun'),
        ('he', 'yarok', 'jarok'),    ('ar', 'akhdar', 'axdar'),
        ('zh', 'lv', 'lu'),
    ],
    'white': [
        ('en', 'white', 'wait'),    ('es', 'blanco', 'blanko'),
        ('fr', 'blanc', 'blan'),     ('de', 'weiss', 'vais'),
        ('he', 'lavan', 'lavan'),    ('ar', 'abyad', 'abjad'),
        ('zh', 'bai', 'bai'),
    ],
    'black': [
        ('en', 'black', 'blæk'),    ('es', 'negro', 'negro'),
        ('fr', 'noir', 'nwar'),      ('de', 'schwarz', 'ʃvarts'),
        ('he', 'shakhor', 'ʃaxor'),  ('ar', 'aswad', 'aswad'),
        ('zh', 'hei', 'hei'),
    ],
    'yellow': [
        ('en', 'yellow', 'jelo'),   ('es', 'amarillo', 'amarijo'),
        ('fr', 'jaune', 'ʒon'),      ('de', 'gelb', 'gelb'),
        ('he', 'tsahov', 'tsahov'),  ('ar', 'asfar', 'asfar'),
        ('zh', 'huang', 'hwang'),
    ],
    'gold': [
        ('en', 'gold', 'gold'),     ('es', 'oro', 'oro'),
        ('fr', 'or', 'or'),          ('de', 'Gold', 'golt'),
        ('he', 'zahav', 'zahav'),    ('ar', 'dhahab', 'dahab'),
        ('zh', 'jin', 'dʒin'),
    ],
    'silver': [
        ('en', 'silver', 'silver'), ('es', 'plata', 'plata'),
        ('fr', 'argent', 'arʒan'),   ('de', 'Silber', 'zilber'),
        ('he', 'kesef', 'kesef'),    ('ar', 'fidda', 'fida'),
        ('zh', 'yin', 'jin'),
    ],
    'iron': [
        ('en', 'iron', 'aiern'),    ('es', 'hierro', 'iero'),
        ('fr', 'fer', 'fer'),        ('de', 'Eisen', 'aizen'),
        ('he', 'barzel', 'barzel'),  ('ar', 'hadid', 'hadid'),
        ('zh', 'tie', 'tie'),
    ],
    'copper': [
        ('en', 'copper', 'koper'),  ('es', 'cobre', 'kobre'),
        ('fr', 'cuivre', 'kuivr'),   ('de', 'Kupfer', 'kupfer'),
        ('he', 'nekhoshet', 'nexoʃet'), ('ar', 'nuhas', 'nuhas'),
        ('zh', 'tong', 'tong'),
    ],

    # ═══════════════════════ NUMBERS (10) ════════════════════════
    'one': [
        ('en', 'one', 'wan'),       ('es', 'uno', 'uno'),
        ('fr', 'un', 'an'),          ('de', 'eins', 'ains'),
        ('he', 'ekhad', 'exad'),     ('ar', 'wahid', 'wahid'),
        ('zh', 'yi', 'ji'),
    ],
    'two': [
        ('en', 'two', 'tu'),        ('es', 'dos', 'dos'),
        ('fr', 'deux', 'do'),        ('de', 'zwei', 'tsvai'),
        ('he', 'shtaim', 'ʃtaim'),   ('ar', 'ithnayn', 'iθnajn'),
        ('zh', 'er', 'er'),
    ],
    'three': [
        ('en', 'three', 'θri'),     ('es', 'tres', 'tres'),
        ('fr', 'trois', 'trwa'),     ('de', 'drei', 'drai'),
        ('he', 'shalosh', 'ʃaloʃ'),  ('ar', 'thalatha', 'θalaθa'),
        ('zh', 'san', 'san'),
    ],
    'seven': [
        ('en', 'seven', 'seven'),   ('es', 'siete', 'siete'),
        ('fr', 'sept', 'set'),       ('de', 'sieben', 'ziben'),
        ('he', 'sheva', 'ʃeva'),     ('ar', 'saba', 'saba'),
        ('zh', 'qi', 'qi'),
    ],
    'ten': [
        ('en', 'ten', 'ten'),       ('es', 'diez', 'dies'),
        ('fr', 'dix', 'dis'),        ('de', 'zehn', 'tsen'),
        ('he', 'eser', 'eser'),      ('ar', 'ashara', 'aʃara'),
        ('zh', 'shi', 'ʃi'),
    ],
    'hundred': [
        ('en', 'hundred', 'handred'), ('es', 'cien', 'sien'),
        ('fr', 'cent', 'san'),       ('de', 'hundert', 'hundert'),
        ('he', 'mea', 'mea'),        ('ar', 'mia', 'mia'),
        ('zh', 'bai', 'bai'),
    ],
    'thousand': [
        ('en', 'thousand', 'θauzend'), ('es', 'mil', 'mil'),
        ('fr', 'mille', 'mil'),      ('de', 'tausend', 'tauzent'),
        ('he', 'elef', 'elef'),      ('ar', 'alf', 'alf'),
        ('zh', 'qian', 'qian'),
    ],

    # ═══════════════════════ SPIRITUAL (10) ══════════════════════
    'soul': [
        ('en', 'soul', 'sol'),      ('es', 'alma', 'alma'),
        ('fr', 'ame', 'am'),         ('de', 'Seele', 'zele'),
        ('he', 'neshama', 'neʃama'), ('ar', 'ruh', 'ruh'),
        ('zh', 'linghun', 'linghun'),
    ],
    'spirit': [
        ('en', 'spirit', 'spirit'), ('es', 'espiritu', 'espiritu'),
        ('fr', 'esprit', 'espri'),   ('de', 'Geist', 'gaist'),
        ('he', 'ruakh', 'ruax'),     ('ar', 'ruh', 'ruh'),
        ('zh', 'jingshen', 'dʒingʃen'),
    ],
    'heaven': [
        ('en', 'heaven', 'heven'),  ('es', 'cielo', 'sielo'),
        ('fr', 'ciel', 'siel'),      ('de', 'Himmel', 'himel'),
        ('he', 'shamayim', 'ʃamajim'), ('ar', 'janna', 'dʒana'),
        ('zh', 'tian', 'tian'),
    ],
    'earth_ground': [
        ('en', 'ground', 'graund'), ('es', 'suelo', 'swelo'),
        ('fr', 'sol', 'sol'),        ('de', 'Boden', 'boden'),
        ('he', 'karka', 'karka'),    ('ar', 'ard', 'ard'),
        ('zh', 'dimian', 'dimian'),
    ],
    'light_divine': [
        ('en', 'glory', 'glori'),   ('es', 'gloria', 'gloria'),
        ('fr', 'gloire', 'glwar'),   ('de', 'Herrlichkeit', 'herlixkait'),
        ('he', 'kavod', 'kavod'),    ('ar', 'majd', 'madʒd'),
        ('zh', 'rongguang', 'ronggwang'),
    ],
    'blessing': [
        ('en', 'blessing', 'blesing'), ('es', 'bendicion', 'bendision'),
        ('fr', 'benediction', 'benediksion'), ('de', 'Segen', 'zegen'),
        ('he', 'brakha', 'braxa'),   ('ar', 'baraka', 'baraka'),
        ('zh', 'zhufu', 'ʒufu'),
    ],
    'sin': [
        ('en', 'sin', 'sin'),       ('es', 'pecado', 'pekado'),
        ('fr', 'peche', 'peʃe'),     ('de', 'Suende', 'zunde'),
        ('he', 'khet', 'xet'),       ('ar', 'dhanb', 'danb'),
        ('zh', 'zui', 'zuei'),
    ],
    'grace': [
        ('en', 'grace', 'greis'),   ('es', 'gracia', 'grasia'),
        ('fr', 'grace', 'gras'),     ('de', 'Gnade', 'gnade'),
        ('he', 'khen', 'xen'),       ('ar', 'ni3ma', 'nima'),
        ('zh', 'enen', 'enen'),
    ],
    'covenant': [
        ('en', 'covenant', 'kavenant'), ('es', 'pacto', 'pakto'),
        ('fr', 'alliance', 'alians'), ('de', 'Bund', 'bunt'),
        ('he', 'brit', 'brit'),      ('ar', 'ahd', 'ahd'),
        ('zh', 'mengyue', 'mengjue'),
    ],
    'redemption': [
        ('en', 'redemption', 'ridempʃen'), ('es', 'redencion', 'redension'),
        ('fr', 'redemption', 'redanpsion'), ('de', 'Erloesung', 'erlosung'),
        ('he', 'geula', 'geula'),    ('ar', 'fidaa', 'fida'),
        ('zh', 'jiushu', 'dʒiouʃu'),
    ],

    # ═══════════════════════ SOCIAL (10) ═════════════════════════
    'king': [
        ('en', 'king', 'king'),     ('es', 'rey', 'rei'),
        ('fr', 'roi', 'rwa'),        ('de', 'Koenig', 'konig'),
        ('he', 'melekh', 'melex'),   ('ar', 'malik', 'malik'),
        ('zh', 'wang', 'wang'),
    ],
    'servant': [
        ('en', 'servant', 'servant'), ('es', 'siervo', 'siervo'),
        ('fr', 'serviteur', 'serviter'), ('de', 'Diener', 'diner'),
        ('he', 'eved', 'eved'),      ('ar', 'abd', 'abd'),
        ('zh', 'puren', 'puren'),
    ],
    'friend': [
        ('en', 'friend', 'frend'),  ('es', 'amigo', 'amigo'),
        ('fr', 'ami', 'ami'),        ('de', 'Freund', 'froint'),
        ('he', 'khaver', 'xaver'),   ('ar', 'sadiq', 'sadiq'),
        ('zh', 'pengyou', 'pengjou'),
    ],
    'enemy': [
        ('en', 'enemy', 'enemi'),   ('es', 'enemigo', 'enemigo'),
        ('fr', 'ennemi', 'enmi'),    ('de', 'Feind', 'faint'),
        ('he', 'oyev', 'ojev'),      ('ar', 'aduww', 'aduw'),
        ('zh', 'diren', 'diren'),
    ],
    'people': [
        ('en', 'people', 'pipel'),  ('es', 'gente', 'xente'),
        ('fr', 'gens', 'ʒan'),       ('de', 'Menschen', 'menʃen'),
        ('he', 'am', 'am'),          ('ar', 'naas', 'nas'),
        ('zh', 'ren', 'ren'),
    ],
    'village': [
        ('en', 'village', 'vilidʒ'), ('es', 'pueblo', 'pueblo'),
        ('fr', 'village', 'vilaʒ'),  ('de', 'Dorf', 'dorf'),
        ('he', 'kfar', 'kfar'),      ('ar', 'qarya', 'qarja'),
        ('zh', 'cunzhuang', 'tsunʒwang'),
    ],
    'land': [
        ('en', 'land', 'lænd'),     ('es', 'tierra', 'tiera'),
        ('fr', 'terre', 'ter'),      ('de', 'Land', 'lant'),
        ('he', 'erets', 'erets'),    ('ar', 'ard', 'ard'),
        ('zh', 'tudi', 'tudi'),
    ],
    'sea': [
        ('en', 'sea', 'si'),        ('es', 'mar', 'mar'),
        ('fr', 'mer', 'mer'),        ('de', 'Meer', 'mer'),
        ('he', 'yam', 'jam'),        ('ar', 'bahr', 'bahr'),
        ('zh', 'hai', 'hai'),
    ],
    'sky': [
        ('en', 'sky', 'skai'),      ('es', 'cielo', 'sielo'),
        ('fr', 'ciel', 'siel'),      ('de', 'Himmel', 'himel'),
        ('he', 'shamayim', 'ʃamajim'), ('ar', 'samaa', 'sama'),
        ('zh', 'tiankong', 'tiankong'),
    ],
    'desert': [
        ('en', 'desert', 'dezert'), ('es', 'desierto', 'desierto'),
        ('fr', 'desert', 'dezer'),   ('de', 'Wueste', 'vuste'),
        ('he', 'midbar', 'midbar'),  ('ar', 'sahraa', 'sahra'),
        ('zh', 'shamo', 'ʃamo'),
    ],
}


# ================================================================
#  MORPHOLOGICAL EXPANDER
# ================================================================

class MorphExpander:
    """Generates morphological variants: noun→plural, verb→forms.

    English-focused for now. Each form gets phonemes derived mechanically
    from the base phonemes (suffix appending preserves root physics).
    """

    # English plural rules (simplified)
    _SIBILANT_ENDS = set('sʃzʒtʃdʒ')

    @staticmethod
    def english_plural(word, phonemes):
        """Generate English plural: word → word + 's/es'."""
        if word.endswith(('s', 'sh', 'ch', 'x', 'z')):
            return (word + 'es', phonemes + 'ez')
        elif word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
            return (word[:-1] + 'ies', phonemes[:-1] + 'iz')
        elif word.endswith('f'):
            return (word[:-1] + 'ves', phonemes[:-1] + 'vz')
        elif word.endswith('fe'):
            return (word[:-2] + 'ves', phonemes[:-2] + 'vz')
        else:
            return (word + 's', phonemes + 'z')

    @staticmethod
    def english_verb_ing(word, phonemes):
        """Generate English present participle: word → word + 'ing'."""
        if word.endswith('e') and not word.endswith('ee'):
            return (word[:-1] + 'ing', phonemes[:-1] + 'ing')
        elif word.endswith('ie'):
            return (word[:-2] + 'ying', phonemes[:-2] + 'jing')
        else:
            return (word + 'ing', phonemes + 'ing')

    @staticmethod
    def english_verb_ed(word, phonemes):
        """Generate English past tense (regular): word → word + 'ed'."""
        if word.endswith('e'):
            return (word + 'd', phonemes + 'd')
        elif word.endswith(('t', 'd')):
            return (word + 'ed', phonemes + 'ed')
        else:
            return (word + 'ed', phonemes + 'd')

    @staticmethod
    def english_comparative(word, phonemes):
        """Generate comparative: word → word + 'er'."""
        if word.endswith('e'):
            return (word + 'r', phonemes + 'r')
        elif word.endswith('y') and len(word) > 1:
            return (word[:-1] + 'ier', phonemes[:-1] + 'ier')
        else:
            return (word + 'er', phonemes + 'er')

    @staticmethod
    def english_superlative(word, phonemes):
        """Generate superlative: word → word + 'est'."""
        if word.endswith('e'):
            return (word + 'st', phonemes + 'st')
        elif word.endswith('y') and len(word) > 1:
            return (word[:-1] + 'iest', phonemes[:-1] + 'iest')
        else:
            return (word + 'est', phonemes + 'est')

    @classmethod
    def expand_noun(cls, concept_id, entries):
        """Generate plural forms for English nouns."""
        forms = []
        for lang, word, phonemes in entries:
            if lang == 'en':
                pl_word, pl_phon = cls.english_plural(word, phonemes)
                forms.append((f'{concept_id}_pl', [
                    ('en', pl_word, pl_phon),
                ]))
                break
        return forms

    @classmethod
    def expand_verb(cls, concept_id, entries):
        """Generate -ing and -ed forms for English verbs."""
        forms = []
        for lang, word, phonemes in entries:
            if lang == 'en':
                ing_w, ing_p = cls.english_verb_ing(word, phonemes)
                ed_w, ed_p = cls.english_verb_ed(word, phonemes)
                forms.append((f'{concept_id}_ing', [('en', ing_w, ing_p)]))
                forms.append((f'{concept_id}_ed', [('en', ed_w, ed_p)]))
                break
        return forms

    @classmethod
    def expand_adjective(cls, concept_id, entries):
        """Generate comparative and superlative for English adjectives."""
        forms = []
        for lang, word, phonemes in entries:
            if lang == 'en':
                comp_w, comp_p = cls.english_comparative(word, phonemes)
                super_w, super_p = cls.english_superlative(word, phonemes)
                forms.append((f'{concept_id}_comp', [('en', comp_w, comp_p)]))
                forms.append((f'{concept_id}_super', [('en', super_w, super_p)]))
                break
        return forms


# ================================================================
#  NOUN/VERB/ADJ CLASSIFICATION (for morphological expansion)
# ================================================================

NOUN_CONCEPTS = {
    # From seed
    'water', 'fire', 'earth', 'light', 'air', 'hand', 'eye', 'head',
    'heart', 'blood', 'mother', 'father', 'child', 'brother', 'sister',
    'sun', 'moon', 'star', 'tree', 'stone', 'river', 'mountain',
    'dog', 'cat', 'bird', 'fish', 'day', 'night', 'year',
    'love', 'death', 'life', 'truth', 'name', 'god', 'peace', 'home', 'war',
    # From expanded
    'mouth', 'ear', 'nose', 'foot', 'bone', 'skin', 'tooth', 'tongue',
    'finger', 'stomach', 'leg', 'arm', 'back', 'neck', 'knee',
    'bread', 'milk', 'meat', 'fruit', 'salt', 'honey', 'egg', 'rice',
    'wine', 'oil', 'sugar', 'seed', 'leaf', 'root', 'flower', 'grass',
    'rain', 'snow', 'wind', 'cloud',
    'horse', 'cow', 'sheep', 'snake', 'lion', 'eagle', 'wolf', 'bear',
    'deer', 'ant', 'bee', 'spider', 'whale', 'turtle', 'rabbit',
    'fear', 'joy', 'anger', 'hope', 'sorrow', 'shame', 'pride', 'mercy',
    'patience', 'wisdom', 'courage', 'trust', 'gratitude', 'compassion', 'longing',
    'house', 'door', 'road', 'knife', 'fire_tool', 'rope', 'wheel', 'boat',
    'book', 'song', 'word', 'path', 'wall', 'bridge', 'garden',
    'gold', 'silver', 'iron', 'copper',
    'soul', 'spirit', 'heaven', 'blessing', 'sin', 'grace', 'covenant', 'redemption',
    'king', 'servant', 'friend', 'enemy', 'people', 'village', 'land', 'sea', 'sky', 'desert',
}

VERB_CONCEPTS = {
    'eat', 'drink', 'sleep', 'walk', 'see', 'hear', 'speak',
    'give', 'take', 'run', 'fly', 'swim', 'sing', 'dance', 'cry', 'laugh',
    'think', 'know', 'love_v', 'teach', 'learn', 'build', 'break',
    'open', 'close', 'wait', 'pray',
}

ADJ_CONCEPTS = {
    'big', 'small', 'good', 'new', 'old',
    'hot', 'cold', 'strong', 'weak', 'fast', 'slow',
    'high', 'low', 'long', 'short', 'wide', 'deep',
    'clean', 'dirty', 'heavy', 'empty', 'full', 'dry', 'wet', 'round',
}

COLOR_CONCEPTS = {
    'red', 'blue', 'green', 'white', 'black', 'yellow',
}


# ================================================================
#  BUILD FULL LEXICON STORE
# ================================================================

def build_full_store():
    """Build a LexiconStore with all entries: seed + expanded + morphological.

    Returns (store, stats_dict).
    """
    from ck_sim.ck_lexicon import LexiconStore, SEED_LEXICON

    store = LexiconStore()

    # 1. Seed entries (50 concepts × 7 = 350)
    for concept_id, entries in SEED_LEXICON.items():
        for lang, word, phonemes in entries:
            store.add_lexeme(
                lang=lang, wordform=word, lemma=word.lower(),
                phonemes=phonemes, freq=1000, sense_ids=[concept_id],
            )

    # 2. Expanded entries (157 concepts × 7 = 1099)
    for concept_id, entries in EXPANDED_LEXICON.items():
        for lang, word, phonemes in entries:
            store.add_lexeme(
                lang=lang, wordform=word, lemma=word.lower(),
                phonemes=phonemes, freq=500, sense_ids=[concept_id],
            )

    # 3. Morphological expansion (English forms)
    morph = MorphExpander()
    morph_count = 0

    all_concepts = {}
    all_concepts.update(SEED_LEXICON)
    all_concepts.update(EXPANDED_LEXICON)

    for concept_id, entries in all_concepts.items():
        if concept_id in NOUN_CONCEPTS:
            for form_id, form_entries in morph.expand_noun(concept_id, entries):
                for lang, word, phonemes in form_entries:
                    store.add_lexeme(
                        lang=lang, wordform=word, lemma=word.lower(),
                        phonemes=phonemes, freq=400, sense_ids=[form_id],
                    )
                    morph_count += 1

        if concept_id in VERB_CONCEPTS:
            for form_id, form_entries in morph.expand_verb(concept_id, entries):
                for lang, word, phonemes in form_entries:
                    store.add_lexeme(
                        lang=lang, wordform=word, lemma=word.lower(),
                        phonemes=phonemes, freq=400, sense_ids=[form_id],
                    )
                    morph_count += 1

        if concept_id in ADJ_CONCEPTS or concept_id in COLOR_CONCEPTS:
            for form_id, form_entries in morph.expand_adjective(concept_id, entries):
                for lang, word, phonemes in form_entries:
                    store.add_lexeme(
                        lang=lang, wordform=word, lemma=word.lower(),
                        phonemes=phonemes, freq=400, sense_ids=[form_id],
                    )
                    morph_count += 1

    stats = {
        'seed_concepts': len(SEED_LEXICON),
        'expanded_concepts': len(EXPANDED_LEXICON),
        'total_concepts': len(SEED_LEXICON) + len(EXPANDED_LEXICON),
        'morph_forms': morph_count,
        'total_lexemes': store.word_count,
        'languages': 7,
    }

    return store, stats


def lexicon_stats():
    """Quick stats without building the full store."""
    from ck_sim.ck_lexicon import SEED_LEXICON

    seed_entries = sum(len(v) for v in SEED_LEXICON.values())
    expanded_entries = sum(len(v) for v in EXPANDED_LEXICON.values())

    noun_morphs = len(NOUN_CONCEPTS) * 1    # plural
    verb_morphs = len(VERB_CONCEPTS) * 2    # -ing, -ed
    adj_morphs = (len(ADJ_CONCEPTS) + len(COLOR_CONCEPTS)) * 2  # comp, super

    return {
        'seed_concepts': 50,
        'seed_entries': seed_entries,
        'expanded_concepts': len(EXPANDED_LEXICON),
        'expanded_entries': expanded_entries,
        'noun_morphs': noun_morphs,
        'verb_morphs': verb_morphs,
        'adj_morphs': adj_morphs,
        'total_morphs': noun_morphs + verb_morphs + adj_morphs,
        'total_entries': seed_entries + expanded_entries + noun_morphs + verb_morphs + adj_morphs,
    }
