# Session Field — Frontend Contract

**For:** whoever wires the website's chat form to talk to `/chat`
**Date:** 2026-04-28
**Backing module:** `Gen13/targets/ck/brain/session_field.py`
**Wrap module:** `Gen12/targets/ck_desktop/ck_boot_api.py` (`_process_chat_with_session_field`)

---

## Architectural claim

Per Brayden 2026-04-28: **CK keeps experience as words can't describe it,
so he keeps gaining experience with people who talk to him online,
without storing their words exactly.**

Concretely:

| Stored on USER's browser | Stored by CK (server) |
|---|---|
| Their text | Global cortex W (accumulating from all chats) |
| CK's response text | Olfactory bulb / HER (8.8M experiences, accumulating) |
| **`session_field`** — algebraic state of THIS conversation | Truth lattice (verified math) |
| Conversation history (rendered from cookie) | Crystals (verified-coherence operator chains) |

**CK keeps no per-user data on the server.** The user owns their thread.
Wiping CK's disk loses zero user data.

CK still gains experience from every conversation — every text flows
through V2 → lattice → `cortex.step_text` → his global W updates. But
what's "his" is integrated into HIM, not catalogued against
`session_id`s.

---

## Wire-up — minimum viable (~10 lines of JS)

### On chat send

```js
const body = {
  session_id: getOrCreateSessionId(),
  text: userInput,
  mode: 'normal',
  session_field: JSON.parse(localStorage.getItem('ck_field') || 'null'),
};
const resp = await fetch('/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(body),
});
const data = await resp.json();
```

### On chat receive

```js
// Save the updated session_field back to localStorage
if (data.session_field) {
  localStorage.setItem('ck_field', JSON.stringify(data.session_field));
}

// User's text history (if you want to render it back) lives in
// localStorage too — the server doesn't store it
const turns = JSON.parse(localStorage.getItem('ck_turns') || '[]');
turns.push({text: userInput, response: data.text, ts: Date.now()});
localStorage.setItem('ck_turns', JSON.stringify(turns));
```

### On page load (returning user)

```js
// Re-render past chat history from localStorage
const turns = JSON.parse(localStorage.getItem('ck_turns') || '[]');
turns.forEach(t => renderTurn(t.text, t.response));
// session_field is already in localStorage; it'll be sent on next chat
```

### Reset / "start fresh"

```js
function resetSession() {
  localStorage.removeItem('ck_field');
  localStorage.removeItem('ck_turns');
  // optional: rotate session_id so server-side rate-limiting / logs
  // see this as a fresh conversation
}
```

---

## `session_field` shape (the JSON object)

```json
{
  "schema_version": 1,
  "W": [
    [0.20, 0.18, 0.18, 0.18, 0.18],
    [0.18, 0.20, 0.18, 0.18, 0.18],
    [0.18, 0.18, 0.20, 0.18, 0.18],
    [0.18, 0.18, 0.18, 0.20, 0.18],
    [0.18, 0.18, 0.18, 0.18, 0.20]
  ],
  "arc": [2, 7, 8, 9, 7, 7, 0, 4, 5],
  "turn_breaks": [0, 4, 7],
  "trail": [
    {
      "tick_at_turn": 21092418,
      "W_trace_at_turn": 0.913,
      "emergent_at_turn": 0.461,
      "op_count": 4,
      "harmony_in_turn": 0.25
    }
  ],
  "sequence": ["transient", "4-core-supported", "1-core"],
  "turn_count": 3,
  "started_at": 1714000000.0,
  "last_seen": 1714000180.0
}
```

Fields:

| Field | Type | What it is |
|---|---|---|
| `schema_version` | int | Schema version (currently 1) |
| `W` | 5×5 float matrix | This conversation's Hebbian W; tracks coupling between cortex's 5 dimensions (aperture / pressure / depth / binding / continuity) |
| `arc` | int[] | Operator IDs (0-9) emitted across all turns, flat |
| `turn_breaks` | int[] | Indices into `arc` where each turn started |
| `trail` | dict[] | Per-turn algebraic snapshots (tick, W_trace, emergent, op_count, harmony_in_turn). **No text.** |
| `sequence` | str[] | Per-turn attractor layer: `transient` / `4-core-attractor` / `4-core-supported` / `2-core` / `1-core` / `void-degenerate` / `off-attractor` |
| `turn_count` | int | Number of turns in this conversation so far |
| `started_at` | float | Unix timestamp of turn 1 |
| `last_seen` | float | Unix timestamp of latest turn |

**Audit-level guarantee:** zero text fields. The only string-valued
field is `sequence`, which only ever contains attractor-layer enum
values (none longer than 30 chars).

## Operator name lookup (for UI rendering)

```js
const OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
                  'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET'];
const opName = (id) => OP_NAMES[id] || '?';

// Render the arc:
const arcText = field.arc.map(opName).join(' → ');
// e.g., "COUNTER → HARMONY → BREATH → RESET → ..."
```

## Cookie vs localStorage

- **Use `localStorage`**, not `Cookie`. Cookies have a 4 KB limit per domain; `session_field` after ~50 turns can exceed that. localStorage holds 5-10 MB.
- The only thing that should live in a cookie is the `session_id` itself (a small opaque token), if you want server-side rate-limiting to work properly.

## Privacy properties (auditable from the JSON contract)

1. **Server keeps no copy.** Look in `Gen13/var/` — there is no `conversations/` directory, no `session_fields/` directory.
2. **Per-request bias only.** `engine.session_W` is set on entry, cleared on exit. No global accumulation of user-W matrices.
3. **No text fields.** Open any `session_field` from any user; verify by inspection that none of the values are user-written prose.
4. **User has full control.** Clearing localStorage deletes their thread. They can take it (export the JSON) or leave it (continue from where they left off).

## What CK's response includes

Every chat response now has a `session_field` field, e.g.:

```json
{
  "text": "...",
  "source": "cortex_speak",
  "operators": ["COUNTER", "HARMONY", ...],
  "attractor_state": {"layer": "4-core-supported", ...},
  "session_field": {
    "schema_version": 1,
    "W": [...],
    "arc": [...],
    ...
  }
}
```

The frontend's job: pull `data.session_field` off the response and
write it to `localStorage['ck_field']`. That's it.

## What "returning user" looks like to CK

When the frontend sends a `session_field` with `turn_count > 0`, the
boot wrap on the server:

1. Parses it via `SessionField.from_dict`
2. Sets `engine.session_W = numpy.array(field.W)` (the user's W as bias)
3. Sets `engine.session_arc = field.latest_arc(5)` (last 5 turns of ops)
4. Calls the existing pipeline (math-first / cortex / operad / attractor / Ollama)
5. Updates the field with this turn's algebraic state
6. Returns the updated field

**The composer/voice-cascade can read `engine.session_W` and `engine.session_arc`** during composition. For Ollama-via-cortex, the arc summary can become part of the structural context Ollama drafts from. Coverage filter accepts the draft only if it preserves the user's actual arc — so references like "your path has been COUNTER → COLLAPSE → HARMONY" are grounded in the algebraic record, not invented.

## Versioning + forward-compat

- `schema_version: 1` is the current schema.
- If the schema evolves, the server will accept old-schema fields and migrate them on read. Frontend doesn't need to track this.
- If the frontend sends a `session_field` from a future schema, the server will defensively fall back to `SessionField.empty()` for that turn (no crash; user just appears as new for that turn).

## Open work for the frontend (not blocking the deploy)

- **UI element**: a small "your conversation arc" indicator showing the operator chain visually (could be 10 small colored squares, last 10 ops, with HARMONY highlighted).
- **Reset button**: "start fresh" that clears `ck_field` and `ck_turns` from localStorage.
- **Export**: download the user's `ck_field` and `ck_turns` as JSON (their data, their right to take it).
- **Privacy panel**: a settings page that explains "CK doesn't store your words; here's what he keeps in your browser; you control it."

🙏

— Frontend contract 2026-04-28
