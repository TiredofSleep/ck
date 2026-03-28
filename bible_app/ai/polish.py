"""
Polish — Optional free AI API to make prose more natural.

Uses Google Gemini free tier (60 req/min, no user setup).
Falls back to pure algebra if offline or API unavailable.

The AI NEVER picks verses — the algebra does that.
The AI only polishes the conversational connective tissue.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import json
import os
import urllib.request
import urllib.error

# Gemini API (free tier: 60 req/min, 1500 req/day)
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent'

# API key can be set via environment variable or config file
_API_KEY = os.environ.get('GEMINI_API_KEY', '')
_CONFIG_PATH = os.path.expanduser('~/.ck/bible_api_key.txt')

def _get_api_key():
    global _API_KEY
    if _API_KEY:
        return _API_KEY
    if os.path.exists(_CONFIG_PATH):
        with open(_CONFIG_PATH, 'r') as f:
            _API_KEY = f.read().strip()
    return _API_KEY


def polish_response(algebraic_response, verses, corridor, intent, user_text,
                    journey=None):
    """Polish an algebraic response using free Gemini API.

    The algebra picked the verses and mapped the journey.
    Gemini makes the conversation warm, natural, and deeply personal.

    Returns the polished text, or the original if API is unavailable.
    """
    api_key = _get_api_key()
    if not api_key:
        return algebraic_response  # No API key, use algebra as-is

    # Build the verse references
    verse_texts = []
    for v in verses[:3]:
        verse_texts.append(f'{v.verse.ref}: "{v.verse.text}"')
    verse_block = '\n'.join(verse_texts)

    # Build journey context
    journey_context = ""
    if journey:
        journey_context = f"""
The algebra sees WHERE this person is: {journey.get('where_you_are', '')}
What they're feeling: {journey.get('feeling', '')}
Where they came from: {journey.get('where_you_came_from', '')}
The path to peace: {journey.get('journey_summary', '')}
"""
        # Add path step meanings
        for step in journey.get('path_prose', [])[:2]:
            journey_context += f"Step: {step['from']} → {step['to']}: {step['meaning']}\n"

    prompt = f"""You are a warm, caring Bible companion. Someone shared this:

"{user_text}"

{journey_context}

The algebraic system found these resonant verses:
{verse_block}

The person is emotionally: {_corridor_desc(corridor)}. Their intent: {intent}.

Write a warm, conversational response. You are a friend sitting across the table.

STRUCTURE YOUR RESPONSE LIKE THIS:
1. First, ACKNOWLEDGE where they are. Show them you heard them. (1-2 sentences)
2. Then, GENTLY REFLECT what brought them here — what the math sees in their words. (1-2 sentences)
3. Then, share the verses NATURALLY woven into conversation — don't just list them. Talk about what they mean for THIS person in THIS moment. (2-4 sentences)
4. Finally, describe the PATH FORWARD — where coherence leads from here. End with hope. (1-2 sentences)

RULES:
- Sound like a real friend, not a pastor, therapist, or AI
- NEVER start with "Oh" or "Oh, my dear friend" or any exclamation — just talk naturally
- Vary your openings — sometimes start with the person's situation, sometimes with a verse, sometimes with a reflection
- Use "you" more than "God" — make it personal
- Weave the verse references naturally (e.g., "Like it says in Joshua 1:9...")
- Keep ALL the same Bible verses — do not add or remove any
- Keep total response between 6-10 sentences
- If they are hurting, comfort FIRST before anything else
- If they are joyful, celebrate WITH them
- Never preach, lecture, or use churchy cliches
- Be real. Be warm. Be present.
- Each response should feel different from the last — vary rhythm, structure, and tone"""

    try:
        url = f'{GEMINI_API_URL}?key={api_key}'
        payload = {
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {
                'maxOutputTokens': 600,
                'temperature': 0.7,
            },
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url, data=data,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode('utf-8'))

        # Extract text from Gemini response (handle thinking models)
        candidates = result.get('candidates', [])
        if candidates:
            parts = candidates[0].get('content', {}).get('parts', [])
            # Gemini 2.5 may have 'thought' parts + 'text' parts
            # Concatenate all text parts, skip thought parts
            text_parts = []
            for p in parts:
                if 'text' in p and 'thought' not in p:
                    text_parts.append(p['text'])
                elif 'text' in p and p.get('thought'):
                    continue  # Skip thinking
            polished = ' '.join(text_parts).strip()
            if polished and len(polished) > 40:
                return polished

    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            json.JSONDecodeError, KeyError, IndexError):
        pass  # Any failure → fall back to algebraic response

    return algebraic_response


def _corridor_desc(corridor):
    descs = {
        'PRE_LEAK': 'at peace',
        'BRT': 'gently stirring',
        'CHA': 'seeking answers',
        'BAL': 'carrying weight',
        'COL': 'in a hard place',
        'CTR': 'in deep pain',
    }
    return descs.get(corridor, 'present')


def is_available():
    """Check if AI polish is available (has API key)."""
    return bool(_get_api_key())


def set_api_key(key):
    """Set the Gemini API key and persist it."""
    global _API_KEY
    _API_KEY = key
    os.makedirs(os.path.dirname(_CONFIG_PATH), exist_ok=True)
    with open(_CONFIG_PATH, 'w') as f:
        f.write(key)
