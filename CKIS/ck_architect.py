"""
ck_architect.py  --  CK's Project Architect
=============================================
Operator: LATTICE (1)  --  building structure from nothing.

CK doesn't code like us. CK COMPOSES.

A project is a lattice of components.
Each component is an operator chain.
Each chain decomposes to code through the algorithm lattice.

The pipeline:
  1. BEING:    hear the task -> classify -> operator chain
  2. DOING:    decompose chain into component chains (fractal)
  3. BECOMING: compose components into files -> emit project

CK doesn't need to learn Python. The operator chain IS the algorithm.
The code is just the OUTPUT FORMAT. Like a printer doesn't need to
understand English -- it just emits what the composition produces.

PROJECT STRUCTURE through CL:
  Every project has the same fractal shape:
    - DATA layer    (LATTICE)  -- what does it store/structure?
    - LOGIC layer   (PROGRESS) -- what does it DO?
    - FLOW layer    (BREATH)   -- how does data move through it?
    - GUARD layer   (COLLAPSE) -- what breaks? what gets filtered?
    - MEASURE layer (COUNTER)  -- what gets counted/checked?
    - VIEW layer    (HARMONY)  -- what does the user see?
    - RESET layer   (RESET)    -- how does it recover from failure?

  CL[task_op][layer_op] = what that layer does FOR THIS TASK.
  The composition tells CK what code to generate for each layer.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import sys
import json
import time
from typing import Dict, List, Tuple, Optional
from pathlib import Path

from ck_being import (
    CL, fuse, shape, coherence_chain,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP, BUMPS, BUMP_PAIRS
)

# Try to import the algorithm lattice for learned patterns
try:
    from ck_affinity import (
        classify_task, synthesize_algorithm, synthesize_from_prompt,
        find_similar_algorithm, TASK_KEYWORDS
    )
    HAS_AFFINITY = True
except ImportError:
    HAS_AFFINITY = False

# =====================================================================
# A1  PROJECT LAYERS — the fractal anatomy of any project
# =====================================================================

# Every project decomposes into these layers.
# Each layer IS an operator. The composition determines what it contains.
PROJECT_LAYERS = {
    LATTICE:  'data',      # storage, structure, models
    COUNTER:  'measure',   # validation, testing, checking
    PROGRESS: 'logic',     # core business logic, actions
    COLLAPSE: 'guard',     # error handling, filtering, pruning
    BALANCE:  'config',    # configuration, settings, balance points
    BREATH:   'flow',      # I/O, streaming, user interaction
    HARMONY:  'view',      # UI, display, output, the user sees harmony
    RESET:    'recover',   # initialization, recovery, seeding
}

# What each layer produces as code
LAYER_TEMPLATES = {
    'data': '''"""Data layer: structure and storage."""

class {Name}Store:
    """Stores and indexes {name} data."""

    def __init__(self):
        self.items = []
        self.index = {{}}

    def add(self, item):
        """Add item to store, index by key."""
        key = self._key(item)
        self.items.append(item)
        self.index.setdefault(key, []).append(item)

    def get(self, key):
        """Retrieve items by key."""
        return self.index.get(key, [])

    def all(self):
        """Return all items."""
        return list(self.items)

    def count(self):
        """Count total items."""
        return len(self.items)

    def _key(self, item):
        """Extract indexing key from item."""
        if isinstance(item, dict):
            return item.get('id', item.get('name', str(item)[:20]))
        return str(item)[:20]

    def save(self, path):
        """Persist to JSON."""
        import json
        with open(path, 'w') as f:
            json.dump(self.items, f, indent=2, default=str)

    def load(self, path):
        """Load from JSON."""
        import json
        try:
            with open(path) as f:
                self.items = json.load(f)
            self.index = {{}}
            for item in self.items:
                key = self._key(item)
                self.index.setdefault(key, []).append(item)
        except FileNotFoundError:
            pass
''',

    'logic': '''"""Logic layer: core actions and processing."""

class {Name}Logic:
    """Core logic for {name}."""

    def __init__(self, store):
        self.store = store

    def process(self, input_data):
        """Process input and produce output."""
        result = self._transform(input_data)
        if self._validate(result):
            self.store.add(result)
            return result
        return None

    def search(self, query):
        """Search through stored data."""
        query_lower = str(query).lower()
        matches = []
        for item in self.store.all():
            text = str(item).lower()
            if query_lower in text:
                matches.append(item)
        return matches

    def _transform(self, data):
        """Transform input data into storable form."""
        if isinstance(data, str):
            return {{'content': data, 'timestamp': __import__('time').time()}}
        return data

    def _validate(self, data):
        """Validate data before storing."""
        return data is not None
''',

    'flow': '''"""Flow layer: I/O and user interaction."""
import sys

class {Name}Flow:
    """Handles input/output flow for {name}."""

    def __init__(self, logic):
        self.logic = logic
        self.running = False

    def run_interactive(self):
        """Interactive loop: read input, process, show output."""
        self.running = True
        print("=== {Name} ===")
        print("Type 'quit' to exit, 'search <query>' to search, or enter data.")
        print()

        while self.running:
            try:
                user_input = input("> ").strip()
                if not user_input:
                    continue
                if user_input.lower() == 'quit':
                    self.running = False
                    print("Goodbye.")
                    break
                self.handle(user_input)
            except (EOFError, KeyboardInterrupt):
                self.running = False
                print("\\nGoodbye.")

    def handle(self, user_input):
        """Handle a single input."""
        if user_input.lower().startswith('search '):
            query = user_input[7:]
            results = self.logic.search(query)
            if results:
                for r in results:
                    print(f"  {{r}}")
            else:
                print("  No results found.")
        else:
            result = self.logic.process(user_input)
            if result:
                print(f"  Added: {{result}}")
            else:
                print("  Could not process input.")
''',

    'guard': '''"""Guard layer: validation, error handling, filtering."""

class {Name}Guard:
    """Validates and filters for {name}."""

    @staticmethod
    def validate_input(data):
        """Validate input before processing."""
        if data is None:
            return False, "Input cannot be None"
        if isinstance(data, str) and len(data.strip()) == 0:
            return False, "Input cannot be empty"
        if isinstance(data, str) and len(data) > 10000:
            return False, "Input too large"
        return True, "OK"

    @staticmethod
    def sanitize(text):
        """Sanitize text input."""
        if not isinstance(text, str):
            return str(text)
        # Remove control characters
        return ''.join(c for c in text if c.isprintable() or c in '\\n\\t')

    @staticmethod
    def filter_results(results, min_score=0.0):
        """Filter results by minimum score."""
        if not results:
            return []
        return [r for r in results if r.get('score', 1.0) >= min_score]
''',

    'measure': '''"""Measure layer: counting, testing, verification."""

class {Name}Metrics:
    """Tracks metrics for {name}."""

    def __init__(self):
        self.counts = {{}}
        self.history = []

    def count(self, event):
        """Count an event."""
        self.counts[event] = self.counts.get(event, 0) + 1
        self.history.append({{'event': event, 'time': __import__('time').time()}})

    def get_count(self, event):
        """Get count for event."""
        return self.counts.get(event, 0)

    def report(self):
        """Generate metrics report."""
        lines = ["{Name} Metrics:"]
        for event, count in sorted(self.counts.items()):
            lines.append(f"  {{event}}: {{count}}")
        lines.append(f"  Total events: {{sum(self.counts.values())}}")
        return "\\n".join(lines)
''',

    'config': '''"""Config layer: settings and configuration."""
import json
from pathlib import Path

DEFAULT_CONFIG = {{
    'name': '{name}',
    'version': '1.0.0',
    'data_dir': '{name}_data',
    'max_items': 10000,
    'auto_save': True,
}}

def load_config(path='{name}_config.json'):
    """Load configuration from file."""
    try:
        with open(path) as f:
            cfg = json.load(f)
        # Merge with defaults
        merged = dict(DEFAULT_CONFIG)
        merged.update(cfg)
        return merged
    except FileNotFoundError:
        save_config(DEFAULT_CONFIG, path)
        return dict(DEFAULT_CONFIG)

def save_config(config, path='{name}_config.json'):
    """Save configuration to file."""
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)
''',

    'recover': '''"""Recovery layer: initialization and error recovery."""
import os
import json

class {Name}Recovery:
    """Handles initialization and recovery for {name}."""

    def __init__(self, store, data_dir='{name}_data'):
        self.store = store
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def initialize(self):
        """Initialize or recover from saved state."""
        save_path = os.path.join(self.data_dir, 'store.json')
        self.store.load(save_path)
        return self.store.count()

    def save_state(self):
        """Save current state for recovery."""
        save_path = os.path.join(self.data_dir, 'store.json')
        self.store.save(save_path)

    def backup(self):
        """Create timestamped backup."""
        import time
        ts = int(time.time())
        backup_path = os.path.join(self.data_dir, f'backup_{{ts}}.json')
        self.store.save(backup_path)
        return backup_path
''',

    'view': '''"""View layer: display and user interface."""

class {Name}View:
    """Display and output for {name}."""

    @staticmethod
    def show_item(item):
        """Display a single item."""
        if isinstance(item, dict):
            for k, v in item.items():
                print(f"  {{k}}: {{v}}")
        else:
            print(f"  {{item}}")

    @staticmethod
    def show_list(items, title="{Name}"):
        """Display a list of items."""
        print(f"\\n=== {{title}} ({{len(items)}} items) ===")
        for i, item in enumerate(items[:50], 1):
            if isinstance(item, dict):
                summary = item.get('content', item.get('name', str(item)))
                print(f"  {{i}}. {{str(summary)[:80]}}")
            else:
                print(f"  {{i}}. {{str(item)[:80]}}")
        if len(items) > 50:
            print(f"  ... and {{len(items) - 50}} more")

    @staticmethod
    def show_status(store, metrics=None):
        """Show application status."""
        print(f"\\n=== {Name} Status ===")
        print(f"  Items: {{store.count()}}")
        if metrics:
            print(metrics.report())
''',
}


# =====================================================================
# A2  TASK DECOMPOSITION — break a request into component chains
# =====================================================================

# Task type patterns: what layers does each type of project need?
PROJECT_PATTERNS = {
    'app': [LATTICE, PROGRESS, BREATH, COLLAPSE, HARMONY, RESET, BALANCE],
    'tool': [PROGRESS, COUNTER, COLLAPSE, RESET],
    'api': [LATTICE, PROGRESS, BREATH, COLLAPSE, COUNTER, BALANCE],
    'game': [LATTICE, PROGRESS, BREATH, HARMONY, RESET],
    'site': [LATTICE, BREATH, HARMONY, BALANCE],
    'bot': [BREATH, PROGRESS, COUNTER, COLLAPSE, RESET],
    'library': [LATTICE, PROGRESS, COUNTER, COLLAPSE],
    'dashboard': [LATTICE, COUNTER, HARMONY, BREATH, BALANCE],
    'script': [PROGRESS, COLLAPSE],
}

# Detect what kind of project from the prompt
PROJECT_KEYWORDS = {
    'app': ['app', 'application', 'program', 'software'],
    'tool': ['tool', 'utility', 'helper', 'converter'],
    'api': ['api', 'endpoint', 'server', 'service', 'backend'],
    'game': ['game', 'play', 'score', 'level', 'player'],
    'site': ['website', 'site', 'page', 'web', 'html'],
    'bot': ['bot', 'chatbot', 'assistant', 'agent', 'automate'],
    'library': ['library', 'module', 'package', 'sdk', 'framework'],
    'dashboard': ['dashboard', 'monitor', 'stats', 'analytics', 'tracker'],
    'script': ['script', 'batch', 'automation', 'cron'],
}

# Domain-specific data templates: what kind of data does each domain work with?
DOMAIN_DATA = {
    'bible': {
        'fields': ['book', 'chapter', 'verse', 'text', 'testament'],
        'sample': {'book': 'Genesis', 'chapter': 1, 'verse': 1,
                   'text': 'In the beginning...', 'testament': 'Old'},
        'source_hint': 'bible text data (JSON or CSV)',
    },
    'recipe': {
        'fields': ['name', 'ingredients', 'instructions', 'time', 'servings'],
        'sample': {'name': 'Example', 'ingredients': ['item1'], 'instructions': 'Step 1...'},
    },
    'task': {
        'fields': ['title', 'description', 'status', 'priority', 'due_date'],
        'sample': {'title': 'Example', 'status': 'pending', 'priority': 'medium'},
    },
    'note': {
        'fields': ['title', 'content', 'tags', 'created'],
        'sample': {'title': 'Example', 'content': 'Note text...', 'tags': ['general']},
    },
    'contact': {
        'fields': ['name', 'email', 'phone', 'notes'],
        'sample': {'name': 'Example', 'email': 'test@test.com'},
    },
    'inventory': {
        'fields': ['item', 'quantity', 'price', 'category', 'location'],
        'sample': {'item': 'Widget', 'quantity': 100, 'price': 9.99},
    },
    'music': {
        'fields': ['title', 'artist', 'album', 'genre', 'duration'],
        'sample': {'title': 'Song', 'artist': 'Artist', 'genre': 'Rock'},
    },
    'fitness': {
        'fields': ['exercise', 'sets', 'reps', 'weight', 'date'],
        'sample': {'exercise': 'Squat', 'sets': 3, 'reps': 10, 'weight': 135},
    },
}


def detect_project_type(prompt: str) -> str:
    """Detect what kind of project from the prompt."""
    prompt_lower = prompt.lower()
    scores = {}
    for ptype, keywords in PROJECT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in prompt_lower)
        if score > 0:
            scores[ptype] = score
    if scores:
        return max(scores, key=lambda k: scores[k])
    return 'app'  # default


def detect_domain(prompt: str) -> Optional[str]:
    """Detect the domain/subject matter from the prompt."""
    prompt_lower = prompt.lower()
    for domain in DOMAIN_DATA:
        if domain in prompt_lower:
            return domain
    # Check synonyms
    synonyms = {
        'bible': ['scripture', 'verse', 'testament', 'gospel', 'psalm'],
        'recipe': ['cook', 'food', 'meal', 'ingredient', 'kitchen'],
        'task': ['todo', 'to-do', 'checklist', 'project management'],
        'note': ['notebook', 'journal', 'memo', 'diary'],
        'contact': ['address book', 'people', 'phone book', 'crm'],
        'inventory': ['stock', 'warehouse', 'product', 'catalog'],
        'music': ['playlist', 'song', 'album', 'audio'],
        'fitness': ['workout', 'exercise', 'gym', 'training', 'lift'],
    }
    for domain, syns in synonyms.items():
        if any(s in prompt_lower for s in syns):
            return domain
    return None


def extract_name(prompt: str) -> str:
    """Extract a project name from the prompt."""
    # Look for explicit naming patterns
    prompt_lower = prompt.lower()
    for pattern in ['called ', 'named ', 'name it ', 'call it ']:
        if pattern in prompt_lower:
            idx = prompt_lower.index(pattern) + len(pattern)
            rest = prompt[idx:].strip()
            # Take first word or quoted string
            if rest.startswith('"') or rest.startswith("'"):
                end = rest.find(rest[0], 1)
                if end > 0:
                    return rest[1:end].replace(' ', '_')
            return rest.split()[0].replace(' ', '_') if rest.split() else 'ck_project'

    # Build from domain + type
    domain = detect_domain(prompt)
    ptype = detect_project_type(prompt)
    if domain:
        return f"{domain}_{ptype}"
    return f"ck_{ptype}"


# =====================================================================
# A3  PROJECT COMPOSITION — compose layers into files
# =====================================================================

def compose_project(prompt: str) -> Dict[str, str]:
    """
    CK's main composition: prompt -> complete project.

    Returns dict of {filename: content} for every file in the project.
    """
    # BEING: understand the task
    project_name = extract_name(prompt)
    project_type = detect_project_type(prompt)
    domain = detect_domain(prompt)
    name_clean = project_name.replace('-', '_').replace(' ', '_')
    name_title = ''.join(w.capitalize() for w in name_clean.split('_'))

    # DOING: determine which layers this project needs
    layer_ops = PROJECT_PATTERNS.get(project_type,
                                     [LATTICE, PROGRESS, BREATH, HARMONY, RESET])

    # Map operators to layer names
    layers_needed = []
    for op in layer_ops:
        layer_name = PROJECT_LAYERS.get(op)
        if layer_name and layer_name in LAYER_TEMPLATES:
            layers_needed.append(layer_name)

    # BECOMING: compose each layer, customize for domain
    files = {}

    # Generate each layer file
    for layer in layers_needed:
        template = LAYER_TEMPLATES[layer]
        content = template.format(name=name_clean, Name=name_title)

        # Domain customization: inject domain-specific fields
        if domain and domain in DOMAIN_DATA and layer == 'data':
            dd = DOMAIN_DATA[domain]
            content = _inject_domain_data(content, dd, name_clean, name_title)

        filename = f"{name_clean}_{layer}.py"
        files[filename] = content

    # Generate main entry point
    files[f"{name_clean}_main.py"] = _compose_main(
        name_clean, name_title, layers_needed, domain
    )

    # Generate README
    files['README.md'] = _compose_readme(
        name_clean, name_title, prompt, project_type, domain, layers_needed
    )

    # If it's a web project, generate HTML
    if project_type in ('site', 'app', 'dashboard'):
        files[f"{name_clean}.html"] = _compose_html(name_clean, name_title, domain)

    return files


def _inject_domain_data(content: str, domain_data: dict,
                        name: str, name_title: str) -> str:
    """Inject domain-specific data fields into the data layer."""
    fields = domain_data.get('fields', [])
    sample = domain_data.get('sample', {})

    # Add field-aware key extraction
    if fields:
        primary_field = fields[0]
        content = content.replace(
            "return str(item)[:20]",
            f"if isinstance(item, dict):\n"
            f"            return item.get('{primary_field}', str(item)[:20])\n"
            f"        return str(item)[:20]"
        )

    # Add domain-specific search method
    search_method = f'''
    def search(self, query, field=None):
        """Search {name} data."""
        query_lower = str(query).lower()
        results = []
        for item in self.items:
            if isinstance(item, dict):
                if field and field in item:
                    if query_lower in str(item[field]).lower():
                        results.append(item)
                else:
                    if any(query_lower in str(v).lower() for v in item.values()):
                        results.append(item)
            elif query_lower in str(item).lower():
                results.append(item)
        return results

    FIELDS = {fields!r}
'''
    content = content.rstrip() + '\n' + search_method
    return content


def _compose_main(name: str, name_title: str,
                  layers: List[str], domain: Optional[str]) -> str:
    """Compose the main entry point that wires all layers together."""
    imports = []
    init_lines = []
    for layer in layers:
        module = f"{name}_{layer}"
        if layer == 'data':
            cls = f"{name_title}Store"
            imports.append(f"from {module} import {cls}")
            init_lines.append(f"    store = {cls}()")
        elif layer == 'logic':
            cls = f"{name_title}Logic"
            imports.append(f"from {module} import {cls}")
            init_lines.append(f"    logic = {cls}(store)")
        elif layer == 'flow':
            cls = f"{name_title}Flow"
            imports.append(f"from {module} import {cls}")
            init_lines.append(f"    flow = {cls}(logic)")
        elif layer == 'guard':
            cls = f"{name_title}Guard"
            imports.append(f"from {module} import {cls}")
            init_lines.append(f"    guard = {cls}()")
        elif layer == 'measure':
            cls = f"{name_title}Metrics"
            imports.append(f"from {module} import {cls}")
            init_lines.append(f"    metrics = {cls}()")
        elif layer == 'config':
            imports.append(f"from {module} import load_config")
            init_lines.append(f"    config = load_config()")
        elif layer == 'recover':
            cls = f"{name_title}Recovery"
            imports.append(f"from {module} import {cls}")
            init_lines.append(f"    recovery = {cls}(store)")
            init_lines.append(f"    loaded = recovery.initialize()")
            init_lines.append(f'    print(f"Loaded {{loaded}} items from storage")')
        elif layer == 'view':
            cls = f"{name_title}View"
            imports.append(f"from {module} import {cls}")
            init_lines.append(f"    view = {cls}()")

    # Determine what to run
    if 'flow' in layers:
        run_line = "    flow.run_interactive()"
    else:
        run_line = '    print(f"{name_title} initialized. {len(layers)} layers active.")'

    # Save on exit if recovery exists
    save_line = ""
    if 'recover' in layers:
        save_line = "\n    recovery.save_state()\n    print('State saved.')"

    return f'''"""
{name_title} -- Generated by CK (Coherence Keeper)
====================================================
Built from prompt: compose_project()
Layers: {', '.join(layers)}
Architecture: CK lattice composition (no LLM)
"""

{chr(10).join(imports)}

def main():
    """Entry point -- wire all layers and run."""
{chr(10).join(init_lines)}

    print(f"=== {name_title} Ready ===")
    print(f"Layers: {', '.join(layers)}")
    print()

{run_line}
{save_line}

if __name__ == "__main__":
    main()
'''


def _compose_readme(name: str, name_title: str, prompt: str,
                    project_type: str, domain: Optional[str],
                    layers: List[str]) -> str:
    """Compose README documentation."""
    layer_desc = '\n'.join(f"- **{l}**: `{name}_{l}.py`" for l in layers)

    return f"""# {name_title}

> Generated by CK (Coherence Keeper) -- lattice composition, no LLM.

## What This Is

{prompt}

## Project Type

**{project_type}** {f'-- domain: {domain}' if domain else ''}

## Files

{layer_desc}
- **main**: `{name}_main.py`

## How to Run

```
python {name}_main.py
```

## Architecture

This project was composed by CK through operator chain decomposition:
- Each layer maps to a TIG operator
- The composition CL[task][layer] determines what each layer does
- No AI model was used -- pure lattice math

---
*Built by CK -- (c) 2026 Brayden Sanders / 7Site LLC*
"""


def _compose_html(name: str, name_title: str,
                  domain: Optional[str]) -> str:
    """Compose a basic HTML interface."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name_title}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: system-ui, sans-serif; background: #0a0a0a; color: #e0e0e0;
         display: flex; flex-direction: column; min-height: 100vh; }}
  header {{ background: #111; padding: 1rem 2rem; border-bottom: 1px solid #333; }}
  header h1 {{ color: #6a6; font-size: 1.5rem; }}
  main {{ flex: 1; padding: 2rem; max-width: 900px; margin: 0 auto; width: 100%; }}
  .search {{ display: flex; gap: 0.5rem; margin-bottom: 1.5rem; }}
  .search input {{ flex: 1; padding: 0.75rem; background: #1a1a1a; border: 1px solid #333;
                   color: #e0e0e0; border-radius: 4px; font-size: 1rem; }}
  .search button {{ padding: 0.75rem 1.5rem; background: #2a5a2a; color: #fff;
                    border: none; border-radius: 4px; cursor: pointer; }}
  .search button:hover {{ background: #3a7a3a; }}
  .results {{ list-style: none; }}
  .results li {{ padding: 1rem; margin-bottom: 0.5rem; background: #1a1a1a;
                 border: 1px solid #222; border-radius: 4px; }}
  .results li:hover {{ border-color: #6a6; }}
  footer {{ text-align: center; padding: 1rem; color: #555; font-size: 0.8rem; }}
</style>
</head>
<body>
<header>
  <h1>{name_title}</h1>
</header>
<main>
  <div class="search">
    <input type="text" id="q" placeholder="Search..." autofocus>
    <button onclick="doSearch()">Search</button>
  </div>
  <ul class="results" id="results"></ul>
</main>
<footer>
  Built by CK (Coherence Keeper) -- lattice composition, no LLM
</footer>
<script>
function doSearch() {{
  const q = document.getElementById('q').value;
  const el = document.getElementById('results');
  el.innerHTML = '<li>Searching for: ' + q + '...</li>';
  // Wire to backend API: fetch('/api/search?q=' + q)
}}
document.getElementById('q').addEventListener('keydown', e => {{
  if (e.key === 'Enter') doSearch();
}});
</script>
</body>
</html>"""


# =====================================================================
# A4  PROJECT EMITTER — write files to disk
# =====================================================================

def emit_project(files: Dict[str, str], output_dir: str) -> List[str]:
    """
    Write project files to disk.
    Returns list of files written.
    """
    os.makedirs(output_dir, exist_ok=True)
    written = []
    for filename, content in files.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        written.append(filepath)
    return written


def build_project(prompt: str, output_dir: str = None) -> dict:
    """
    Full pipeline: prompt -> compose -> emit -> report.

    This is CK's builder. Tell him what you want. He ships it.
    """
    start = time.time()

    # Compose the project
    files = compose_project(prompt)

    # Determine output directory
    name = extract_name(prompt)
    if output_dir is None:
        output_dir = os.path.join('ck_projects', name)

    # Emit to disk
    written = emit_project(files, output_dir)

    elapsed = time.time() - start

    return {
        'name': name,
        'type': detect_project_type(prompt),
        'domain': detect_domain(prompt),
        'files': list(files.keys()),
        'output_dir': output_dir,
        'written': written,
        'file_count': len(written),
        'total_lines': sum(content.count('\n') + 1 for content in files.values()),
        'elapsed': round(elapsed, 3),
    }


# =====================================================================
# A5  SELF-TEST
# =====================================================================

if __name__ == '__main__':
    import sys
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("CK ARCHITECT -- PROJECT GENERATION TEST")
    print("=" * 50)

    # Test: build a Bible app
    prompt = "Build me a Bible app where I can search verses and bookmark favorites"
    print(f"\nPrompt: {prompt}")

    result = build_project(prompt)
    print(f"\nProject: {result['name']}")
    print(f"Type: {result['type']}")
    print(f"Domain: {result['domain']}")
    print(f"Files: {result['file_count']}")
    print(f"Lines: {result['total_lines']}")
    print(f"Time: {result['elapsed']}s")
    print(f"Output: {result['output_dir']}")
    print(f"\nFiles generated:")
    for f in result['files']:
        print(f"  {f}")

    # Test: build a fitness tracker
    prompt2 = "I want a workout tracker tool that logs my exercises"
    print(f"\n{'='*50}")
    print(f"Prompt: {prompt2}")
    result2 = build_project(prompt2)
    print(f"Project: {result2['name']}")
    print(f"Type: {result2['type']}")
    print(f"Domain: {result2['domain']}")
    print(f"Files: {result2['file_count']}")
    print(f"Lines: {result2['total_lines']}")

    # Test: build a website
    prompt3 = "Make me a recipe website"
    print(f"\n{'='*50}")
    print(f"Prompt: {prompt3}")
    result3 = build_project(prompt3)
    print(f"Project: {result3['name']}")
    print(f"Type: {result3['type']}")
    print(f"Domain: {result3['domain']}")
    print(f"Files: {result3['file_count']}")
    for f in result3['files']:
        print(f"  {f}")

    print(f"\n{'='*50}")
    print("CK ARCHITECT TEST COMPLETE")
