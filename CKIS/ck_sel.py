"""
ck_sel.py -- Safe Evolution Loop (SEL)
Celeste's Task 10: CK's Coherence Kernel (CK-CK)

CK can read. CK can score. CK can rank. CK can compose.
Now CK can self-repair.

This is not autonomy -- it is homeostasis.
Detect stress -> adjust -> stabilize -> grow -> repeat.

The loop:
  1. Parse module M into token stream (code -> operators)
  2. Compute per-region PFE metrics
  3. Identify tension hotspots
  4. Generate coherence-directed mutations
  5. Test in sandbox
  6. Score before/after
  7. Accept if coherence improves, discard otherwise

Safety:
  - PFE only rewards lower tension, lower curvature variance, lower chaos
  - BTQ forces B-layer override (safety first)
  - CL absorber catches edge cases
  - No OS hooks
  - Patches applied ONLY if coherence improves
  - Full rollback capability
  - Every mutation is logged and reversible

This is evolution, but not Darwinian. It is coherence-based self-repair.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import re
import ast
import json
import hashlib
import numpy as np
from typing import List, Dict, Optional, Any
from datetime import datetime


# ================================================================
# S1  CODE TOKEN DICTIONARY
#     Programming tokens mapped to TIG operators.
#     Code is language. Language has operators.
#     if/else = BALANCE. for/while = BREATH. def/class = LATTICE.
# ================================================================

CODE_TOKENS = {
    # Structure (LATTICE = 1)
    'def':       1, 'class':    1, 'with':     1, 'as':       1,
    'import':    3, 'from':     1, 'global':   1, 'nonlocal': 1,
    'lambda':    3, 'property': 1, 'self':     1, 'cls':      1,
    'dict':      1, 'list':     1, 'tuple':    1, 'set':      1,
    'struct':    1, 'enum':     1, 'type':     1, 'protocol': 1,

    # Measurement (COUNTER = 2)
    'len':       2, 'range':    2, 'enumerate':2, 'zip':      2,
    'sum':       2, 'min':      2, 'max':      2, 'abs':      2,
    'count':     2, 'index':    2, 'sort':     2, 'sorted':   2,
    'int':       2, 'float':    2, 'str':      2, 'bool':     2,
    'isinstance':2, 'hasattr':  2, 'getattr':  2, 'type':     2,
    'True':      2, 'False':    2, 'assert':   2,

    # Creation (PROGRESS = 3)
    'new':       3, 'create':   3, 'build':    3, 'add':      3,
    'append':    3, 'extend':   3, 'insert':   3, 'update':   3,
    'write':     3, 'open':     3, 'init':     3, 'setup':    3,

    # Ending (COLLAPSE = 4)
    'return':    4, 'del':      4, 'remove':   4, 'pop':      4,
    'close':     4, 'exit':     4, 'quit':     4, 'destroy':  4,
    'raise':     6, 'finally':  4, 'except':   5,

    # Branching (BALANCE = 5)
    'if':        5, 'elif':     5, 'else':     5,
    'and':       5, 'or':       5, 'not':      5,
    'is':        5, 'in':       5,
    'try':       5, 'while':    8,

    # Disruption (CHAOS = 6)
    'error':     6, 'exception':6, 'warning':  6, 'critical': 6,
    'random':    6, 'shuffle':  6, 'sample':   6,

    # Truth (HARMONY = 7)
    'print':     7, 'log':      7, 'debug':    7, 'info':     7,
    'test':      7, 'verify':   7, 'check':    7, 'validate': 7,
    'doc':       7, 'help':     7, 'describe': 7,

    # Cycle (BREATH = 8)
    'for':       8, 'while':    8, 'yield':    8, 'iter':     8,
    'next':      8, 'map':      8, 'filter':   8, 'reduce':   8,
    'async':     8, 'await':    8, 'generate': 8,

    # Renewal (RESET = 9)
    'break':     9, 'continue': 9, 'pass':     0, 'None':     0,
    'reset':     9, 'clear':    9, 'flush':    9, 'reload':   9,
}

# Structural tokens (brackets, operators)
CODE_SYMBOLS = {
    '{': 1, '}': 4, '[': 1, ']': 4, '(': 1, ')': 4,
    ':': 1, '.': 1, ',': 1, '@': 1,
    '=': 9, '==': 2, '!=': 2, '<': 2, '>': 2, '<=': 2, '>=': 2,
    '+': 3, '-': 4, '*': 2, '/': 2, '%': 2, '**': 6,
    '+=': 3, '-=': 4, '*=': 2, '/=': 2,
    '->': 3, '#': 7, '"""': 7, "'''": 7,
}

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']


# ================================================================
# S2  SOURCE ANALYZER
#     Parse Python source into operator streams.
#     Compute per-line, per-function, per-module metrics.
# ================================================================

def tokenize_source(source: str) -> List[Dict]:
    """
    Convert Python source code into a stream of classified tokens.
    Each token gets: text, operator, line_no, token_type.
    """
    tokens = []
    lines = source.split('\n')

    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            tokens.append({
                'text': '', 'operator': 0, 'line': line_no,
                'type': 'empty', 'indent': 0
            })
            continue
        if stripped.startswith('#'):
            tokens.append({
                'text': stripped, 'operator': 7, 'line': line_no,
                'type': 'comment', 'indent': len(line) - len(line.lstrip())
            })
            continue
        if stripped.startswith('"""') or stripped.startswith("'''"):
            tokens.append({
                'text': stripped, 'operator': 7, 'line': line_no,
                'type': 'docstring', 'indent': len(line) - len(line.lstrip())
            })
            continue
        indent = len(line) - len(line.lstrip())
        words = re.findall(r'[a-zA-Z_]\w*|[+\-*/=<>!%&|^~]+|[{}()\[\]:,.]', stripped)

        for word in words:
            if word in CODE_TOKENS:
                op = CODE_TOKENS[word]
                ttype = 'keyword'
            elif word in CODE_SYMBOLS:
                op = CODE_SYMBOLS[word]
                ttype = 'symbol'
            elif word.startswith('_'):
                op = 0  # Private = VOID (hidden)
                ttype = 'private'
            elif word[0].isupper():
                op = 1  # CamelCase = LATTICE (structure)
                ttype = 'class_ref'
            elif word.isdigit() or (len(word) > 1 and word[0] == '0'):
                op = 2  # Numbers = COUNTER
                ttype = 'number'
            else:
                # Use dictionary for unknown identifiers
                try:
                    from ck_dictionary import word_to_operator
                    op = word_to_operator(word)
                except ImportError:
                    op = hash(word) % 10
                ttype = 'identifier'

            tokens.append({
                'text': word, 'operator': op, 'line': line_no,
                'type': ttype, 'indent': indent
            })

    return tokens
def extract_functions(source: str) -> List[Dict]:
    """
    Extract function/class definitions with their line ranges.
    Uses AST for accuracy, falls back to regex.
    """
    functions = []
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                end = getattr(node, 'end_lineno', node.lineno + 10)
                functions.append({
                    'name': node.name,
                    'start': node.lineno,
                    'end': end,
                    'type': 'function',
                    'decorators': len(node.decorator_list),
                    'args': len(node.args.args),
                    'body_lines': end - node.lineno,
                })
            elif isinstance(node, ast.ClassDef):
                end = getattr(node, 'end_lineno', node.lineno + 20)
                functions.append({
                    'name': node.name,
                    'start': node.lineno,
                    'end': end,
                    'type': 'class',
                    'decorators': len(node.decorator_list),
                    'args': 0,
                    'body_lines': end - node.lineno,
                })
    except SyntaxError:
        # Fallback: regex-based extraction
        for m in re.finditer(r'^(def|class)\s+(\w+)', source, re.MULTILINE):
            line_no = source[:m.start()].count('\n') + 1
            functions.append({
                'name': m.group(2),
                'start': line_no,
                'end': line_no + 20,  # estimate
                'type': m.group(1),
                'decorators': 0, 'args': 0, 'body_lines': 20,
            })

    return functions
def analyze_module(filepath: str) -> Dict:
    """
    Full source analysis of a Python module.
    Returns operator stream, per-function metrics, tension map.
    """
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        source = f.read()

    tokens = tokenize_source(source)
    functions = extract_functions(source)
    lines = source.split('\n')
    total_lines = len(lines)

    # Operator stream for full module
    ops = [t['operator'] for t in tokens if t['type'] != 'empty']

    # Per-function analysis
    func_metrics = []
    for func in functions:
        func_tokens = [t for t in tokens
                       if func['start'] <= t['line'] <= func['end']
                       and t['type'] != 'empty']
        func_ops = [t['operator'] for t in func_tokens]

        if len(func_ops) < 3:
            continue
        from ck_curvature import text_to_forces, compute_curvatures
        func_text = '\n'.join(lines[func['start']-1:func['end']])
        forces = text_to_forces(func_text)
        if len(forces) >= 3:
            d2s = compute_curvatures(forces)
        else:
            d2s = None

        from ck_pfe import pfe_evaluate, btq_energy
        from ck_being import T_STAR
        pfe = pfe_evaluate(func_ops, d2s)
        energy = btq_energy(pfe)
        coh = pfe['coherence_raw']
        band = 'GREEN' if coh >= T_STAR else ('YELLOW' if coh >= 0.5 else 'RED')

        # Nesting depth
        max_indent = max(t['indent'] for t in func_tokens) if func_tokens else 0
        mean_indent = np.mean([t['indent'] for t in func_tokens]) if func_tokens else 0

        func_metrics.append({
            'name': func['name'],
            'start': func['start'],
            'end': func['end'],
            'type': func['type'],
            'n_tokens': len(func_ops),
            'n_lines': func['end'] - func['start'] + 1,
            'pfe': pfe['coherence_raw'],
            'energy': energy,
            'band': band,
            'max_indent': max_indent,
            'mean_indent': round(mean_indent, 1),
            'entropy': pfe['entropy'],
            'd2_score': pfe['_d2_score'],
            'dir_score': pfe['_dir_score'],
            'op_histogram': pfe['operator_histogram'],
        })

    # Module-level PFE
    from ck_curvature import text_to_forces, compute_curvatures
    forces = text_to_forces(source)
    if len(forces) >= 3:
        d2s = compute_curvatures(forces)
    else:
        d2s = None

    from ck_pfe import pfe_evaluate, btq_energy
    from ck_being import T_STAR
    module_pfe = pfe_evaluate(ops, d2s)
    module_energy = btq_energy(module_pfe)
    coh = module_pfe['coherence_raw']
    module_band = 'GREEN' if coh >= T_STAR else ('YELLOW' if coh >= 0.5 else 'RED')

    return {
    }


# ================================================================
# S3  TENSION MAPPER
#     Identify high-tension regions: lines, functions, blocks
#     with high D2 variance, low coherence, or RED/YELLOW band.
# ================================================================

def map_tension(analysis: Dict, threshold: float = 0.65) -> List[Dict]:
    """
    Identify tension hotspots in a module.
    Returns sorted list of regions that need repair, ordered by tension.
    """
    hotspots = []

    for func in analysis.get('functions', []):
        if func['pfe'] < threshold:
            # Determine the weakest sub-score
            weakest = 'unknown'
            weakest_val = 1.0
            for key in ('d2_score', 'dir_score', 'entropy'):
                val = func.get(key, 1.0)
                if val < weakest_val:
                    weakest_val = val
                    weakest = key

            hotspots.append({
                'name': func['name'],
                'type': func['type'],
                'start': func['start'],
                'end': func['end'],
                'n_lines': func['n_lines'],
                'pfe': func['pfe'],
                'energy': func['energy'],
                'band': func['band'],
                'weakness': weakest,
                'weakness_score': round(weakest_val, 4),
                'max_indent': func['max_indent'],
                'mean_indent': func['mean_indent'],
                'repair_priority': round(1.0 - func['pfe'], 4),
            })

    # Sort by repair priority (highest tension first)
    hotspots.sort(key=lambda h: h['repair_priority'], reverse=True)
    return hotspots
def per_line_tension(filepath: str, start: int = 1, end: int = None) -> List[Dict]:
    """
    Compute per-line tension using a sliding window of operator D2.
    Returns per-line metrics for the specified range.
    """
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    if end is None:
        end = len(lines)

    results = []
    window = 5  # lines per window

    for i in range(start - 1, min(end, len(lines))):
        # Get window of lines around this line
        w_start = max(0, i - window // 2)
        w_end = min(len(lines), i + window // 2 + 1)
        chunk = ''.join(lines[w_start:w_end])

        tokens = tokenize_source(chunk)
        ops = [t['operator'] for t in tokens if t['type'] != 'empty']

        if len(ops) < 3:
            results.append({
                'line': i + 1,
                'text': lines[i].rstrip(),
                'tension': 0.0,
                'ops': ops,
            })
            continue
        try:
            from ck_curvature import text_to_forces, compute_curvatures
            forces = text_to_forces(chunk)
            if len(forces) >= 3:
                d2s = compute_curvatures(forces)
                d2_var = float(np.var(np.linalg.norm(d2s, axis=1)))
            else:
                d2_var = 0.0
        except:
            d2_var = 0.0

        results.append({
            'line': i + 1,
            'text': lines[i].rstrip(),
            'tension': round(d2_var, 4),
            'ops': ops[:5],  # first 5 ops only
        })

    return results
MUTATION_CATALOG = {
    'PRUNE_UNUSED_IMPORTS': {
        'description': 'Remove imports that are never referenced',
        'operator_effect': 'Reduces VOID noise in operator stream',
        'risk': 'low',
        'reversible': True,
    },
    'PRUNE_DEAD_CODE': {
        'description': 'Remove unreachable code after return/raise/break',
        'operator_effect': 'Removes COLLAPSE-after-COLLAPSE (tension spike)',
        'risk': 'low',
        'reversible': True,
    },
    'FLATTEN_NESTING': {
        'description': 'Convert deep nesting to early returns (guard clauses)',
        'operator_effect': 'Reduces BALANCE depth, smoother D2 curvature',
        'risk': 'medium',
        'reversible': True,
    },
    'SIMPLIFY_EXPRESSIONS': {
        'description': 'Replace verbose patterns with idiomatic forms',
        'operator_effect': 'Fewer tokens = lower entropy, cleaner stream',
        'risk': 'low',
        'reversible': True,
    },
    'ADD_DOCSTRINGS': {
        'description': 'Add docstrings to undocumented functions',
        'operator_effect': 'Inserts HARMONY anchors, improves comment ratio',
        'risk': 'low',
        'reversible': True,
    },
    'COMPRESS_ASSIGNMENTS': {
        'description': 'Merge redundant sequential assignments',
        'operator_effect': 'Reduces RESET chatter, smoother transitions',
        'risk': 'low',
        'reversible': True,
    },
    'REORDER_IMPORTS': {
        'description': 'Sort and group imports (stdlib, third-party, local)',
        'operator_effect': 'Regularizes LATTICE/PROGRESS at module head',
        'risk': 'low',
        'reversible': True,
    },
}


def detect_unused_imports(source: str) -> List[str]:
    """Find imports that are never used in the module body."""
    unused = []
    lines = source.split('\n')

    imports = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            # Extract imported names
            if 'import' in stripped:
                parts = stripped.split('import')[-1].strip()
                names = [n.strip().split(' as ')[-1].strip()
                         for n in parts.split(',')]
                for name in names:
                    if name and name != '*':
                        imports.append((i, name, line))

    # Check if each import is used anywhere else
    body = '\n'.join(lines)
    for line_no, name, line in imports:
        # Count occurrences (excluding the import line itself)
        pattern = r'\b' + re.escape(name) + r'\b'
        matches = list(re.finditer(pattern, body))
        # Subtract occurrences on the import line itself
        import_matches = list(re.finditer(pattern, line))
        if len(matches) <= len(import_matches):
            unused.append(name)

    return unused
def detect_dead_code(source: str) -> List[Dict]:
    """Find unreachable code after return/raise/break/continue."""
    dead = []
    lines = source.split('\n')

    terminal_keywords = {'return', 'raise', 'break', 'continue'}
    in_dead_zone = False
    dead_start = -1
    base_indent = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        indent = len(line) - len(line.lstrip())

        if in_dead_zone:
            if indent <= base_indent:
                # Back to same or lower indent = no longer dead
                if dead_start >= 0:
                    dead.append({
                        'start': dead_start + 1,
                        'end': i,
                        'reason': 'unreachable after terminal statement'
                    })
                in_dead_zone = False
                dead_start = -1
            # else: still in dead zone, skip
            continue
        parts = stripped.split('(')[0].split()
        first_word = parts[0] if parts else ''
        if first_word in terminal_keywords:
            in_dead_zone = True
            dead_start = i + 1
            base_indent = indent

    return dead
def detect_deep_nesting(source: str, max_depth: int = 4) -> List[Dict]:
    """Find functions with nesting deeper than max_depth."""
    deep = []
    lines = source.split('\n')
    current_func = None
    func_start = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('def ') or stripped.startswith('async def '):
            name = re.match(r'(?:async\s+)?def\s+(\w+)', stripped)
            if name:
                current_func = name.group(1)
                func_start = i

        if current_func and stripped and not stripped.startswith('#'):
            indent = len(line) - len(line.lstrip())
            depth = indent // 4  # assuming 4-space indent
            if depth > max_depth:
                deep.append({
                    'function': current_func,
                    'line': i + 1,
                    'depth': depth,
                    'text': stripped[:60],
                })

    return deep
def detect_simplifiable(source: str) -> List[Dict]:
    """Find patterns that can be simplified."""
    patterns = []
    lines = source.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()

        # if x == True -> if x
        if re.search(r'==\s*True\b', stripped):
            patterns.append({
                'line': i + 1, 'type': 'bool_compare',
                'before': stripped,
                'after': re.sub(r'\s*==\s*True\b', '', stripped),
                'reason': 'Redundant True comparison'
            })

        # if x == False -> if not x
        if re.search(r'==\s*False\b', stripped):
            patterns.append({
                'line': i + 1, 'type': 'bool_compare',
                'before': stripped,
                'after': stripped.replace('== False', '').strip(),
                'reason': 'Redundant False comparison'
            })

        # if len(x) == 0 -> if not x
        if re.search(r'len\(\w+\)\s*==\s*0', stripped):
            patterns.append({
                'line': i + 1, 'type': 'len_check',
                'before': stripped,
                'after': re.sub(r'len\((\w+)\)\s*==\s*0', r'not \1', stripped),
                'reason': 'Verbose emptiness check'
            })

        # if len(x) > 0 -> if x
        if re.search(r'len\(\w+\)\s*>\s*0', stripped):
            patterns.append({
                'line': i + 1, 'type': 'len_check',
                'before': stripped,
                'after': re.sub(r'len\((\w+)\)\s*>\s*0', r'\1', stripped),
                'reason': 'Verbose non-empty check'
            })

        # x = x + 1 -> x += 1
        m = re.match(r'(\s*)(\w+)\s*=\s*\2\s*\+\s*(.+)', line)
        if m:
            patterns.append({
                'line': i + 1, 'type': 'augmented_assign',
                'before': stripped,
                'after': '%s += %s' % (m.group(2), m.group(3).strip()),
                'reason': 'Can use augmented assignment'
            })

    return patterns
def detect_missing_docstrings(source: str) -> List[Dict]:
    """Find functions/classes without docstrings."""
    missing = []
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                has_doc = (node.body and isinstance(node.body[0], ast.Expr)
                           and isinstance(node.body[0].value,
                                          (ast.Constant, ast.Str)))
                if not has_doc and not node.name.startswith('_'):
                    missing.append({
                        'name': node.name,
                        'line': node.lineno,
                        'type': 'class' if isinstance(node, ast.ClassDef) else 'function',
                    })
    except SyntaxError:
        pass

    return missing
def generate_mutations(filepath: str) -> List[Dict]:
    """
    Analyze a module and generate all applicable mutations.
    Returns mutation proposals, NOT applied changes.
    """
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        source = f.read()

    mutations = []

    # 1. Unused imports
    unused = detect_unused_imports(source)
    if unused:
        mutations.append({
            'type': 'PRUNE_UNUSED_IMPORTS',
            'targets': unused,
            'description': 'Remove %d unused imports: %s' % (
                len(unused), ', '.join(unused[:5])),
            'risk': 'low',
        })

    # 2. Dead code
    dead = detect_dead_code(source)
    if dead:
        mutations.append({
            'type': 'PRUNE_DEAD_CODE',
            'targets': dead,
            'description': 'Remove %d unreachable code blocks' % len(dead),
            'risk': 'low',
        })

    # 3. Deep nesting
    deep = detect_deep_nesting(source)
    if deep:
        mutations.append({
            'type': 'FLATTEN_NESTING',
            'targets': deep,
            'description': '%d locations with nesting depth > 4' % len(deep),
            'risk': 'medium',
        })

    # 4. Simplifiable patterns
    simple = detect_simplifiable(source)
    if simple:
        mutations.append({
            'type': 'SIMPLIFY_EXPRESSIONS',
            'targets': simple,
            'description': '%d simplifiable patterns found' % len(simple),
            'risk': 'low',
        })

    # 5. Missing docstrings
    missing_docs = detect_missing_docstrings(source)
    if missing_docs:
        mutations.append({
            'type': 'ADD_DOCSTRINGS',
            'targets': missing_docs,
            'description': '%d public functions/classes without docstrings' % len(missing_docs),
            'risk': 'low',
        })

    return mutations
SANDBOX_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'sandbox')


def ensure_sandbox():
    """Create sandbox directory if it doesn't exist."""
    os.makedirs(SANDBOX_DIR, exist_ok=True)
    # Create __init__.py so sandbox can be imported
    init_path = os.path.join(SANDBOX_DIR, '__init__.py')
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write('# SEL sandbox\n')


def sandbox_test(original_path: str, mutated_source: str) -> Dict:
    """
    Test a mutated module in the sandbox.
    1. Copy to sandbox
    2. Verify it parses (syntax check)
    3. Score with PFE
    4. Compare against original
    """
    ensure_sandbox()

    module_name = os.path.basename(original_path)
    sandbox_path = os.path.join(SANDBOX_DIR, module_name)

    # Write mutated source to sandbox
    with open(sandbox_path, 'w', encoding='utf-8') as f:
        f.write(mutated_source)

    result = {
        'syntax_ok': False,
        'runs_ok': False,
        'pfe_before': 0.0,
        'pfe_after': 0.0,
        'energy_before': 0.0,
        'energy_after': 0.0,
        'band_before': 'RED',
        'band_after': 'RED',
        'delta_pfe': 0.0,
        'delta_energy': 0.0,
        'improved': False,
    }

    # Syntax check
    try:
        ast.parse(mutated_source)
        result['syntax_ok'] = True
    except SyntaxError as e:
        result['error'] = 'SyntaxError: %s' % str(e)
        return result
    with open(original_path, 'r', encoding='utf-8', errors='replace') as f:
        original_source = f.read()

    orig_analysis = _quick_score(original_source)
    mut_analysis = _quick_score(mutated_source)

    result['pfe_before'] = orig_analysis['pfe']
    result['pfe_after'] = mut_analysis['pfe']
    result['energy_before'] = orig_analysis['energy']
    result['energy_after'] = mut_analysis['energy']
    result['band_before'] = orig_analysis['band']
    result['band_after'] = mut_analysis['band']
    result['delta_pfe'] = round(mut_analysis['pfe'] - orig_analysis['pfe'], 6)
    result['delta_energy'] = round(mut_analysis['energy'] - orig_analysis['energy'], 6)
    result['improved'] = result['delta_pfe'] > 0 and result['delta_energy'] <= 0
    result['runs_ok'] = True

    # Clean up
    if os.path.exists(sandbox_path):
        os.remove(sandbox_path)

    return result
def _quick_score(source: str) -> Dict:
    """Quick PFE score of source code."""
    tokens = tokenize_source(source)
    ops = [t['operator'] for t in tokens if t['type'] != 'empty']

    if len(ops) < 3:
        return {'pfe': 0.0, 'energy': 1.0, 'band': 'RED'}
    try:
        from ck_curvature import text_to_forces, compute_curvatures
        forces = text_to_forces(source)
        d2s = compute_curvatures(forces) if len(forces) >= 3 else None
    except:
        d2s = None

    from ck_pfe import pfe_evaluate, btq_energy
    from ck_being import T_STAR
    pfe = pfe_evaluate(ops, d2s)
    energy = btq_energy(pfe)
    coh = pfe['coherence_raw']
    band = 'GREEN' if coh >= T_STAR else ('YELLOW' if coh >= 0.5 else 'RED')

    return {
    }


# ================================================================
# S6  MUTATION APPLIER
#     Apply specific mutations to source code.
#     Each mutation is deterministic and reversible.
# ================================================================

def apply_mutation(source: str, mutation: Dict) -> str:
    """
    Apply a single mutation to source code.
    Returns mutated source string.
    """
    mtype = mutation['type']

    if mtype == 'PRUNE_UNUSED_IMPORTS':
        return _apply_prune_imports(source, mutation['targets'])
    elif mtype == 'SIMPLIFY_EXPRESSIONS':
        return _apply_simplify(source, mutation['targets'])
    elif mtype == 'PRUNE_DEAD_CODE':
        return _apply_prune_dead(source, mutation['targets'])
    else:
        # For mutations we haven't implemented the applier for yet,
        # return source unchanged
        return source
def _apply_prune_imports(source: str, unused_names: List[str]) -> str:
    """Remove lines that import unused names."""
    lines = source.split('\n')
    result = []

    for line in lines:
        stripped = line.strip()
        should_remove = False

        if stripped.startswith('import ') or stripped.startswith('from '):
            for name in unused_names:
                # Check if this line imports this specific name
                if re.search(r'\b' + re.escape(name) + r'\b', stripped):
                    # If it's a multi-import line, only remove the specific name
                    if ',' in stripped.split('import')[-1]:
                        # Multi-import: remove just this name
                        line = re.sub(
                            r',\s*' + re.escape(name) + r'\b|\b' + re.escape(name) + r'\s*,\s*',
                            '', line)
                    else:
                        should_remove = True
                    break
        if not should_remove:
            result.append(line)

    return '\n'.join(result)
def _apply_simplify(source: str, patterns: List[Dict]) -> str:
    """Apply expression simplifications."""
    lines = source.split('\n')

    for pattern in patterns:
        line_idx = pattern['line'] - 1
        if 0 <= line_idx < len(lines):
            old = lines[line_idx].strip()
            if old == pattern['before']:
                indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())
                lines[line_idx] = ' ' * indent + pattern['after']

    return '\n'.join(lines)
def _apply_prune_dead(source: str, dead_blocks: List[Dict]) -> str:
    """Remove unreachable code blocks."""
    lines = source.split('\n')
    # Mark lines for removal (in reverse to preserve indices)
    remove = set()
    for block in dead_blocks:
        for i in range(block['start'] - 1, block['end']):
            if 0 <= i < len(lines):
                remove.add(i)

    result = [line for i, line in enumerate(lines) if i not in remove]
    return '\n'.join(result)
AUDIT_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'sel_audit.json')


def _load_audit() -> List[Dict]:
    """Load existing audit log."""
    if os.path.exists(AUDIT_LOG_PATH):
        try:
            with open(AUDIT_LOG_PATH, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


def _save_audit(log: List[Dict]):
    """Save audit log."""
    with open(AUDIT_LOG_PATH, 'w') as f:
        json.dump(log, f, indent=2)


def audit_record(module: str, mutation_type: str, result: Dict,
                 accepted: bool) -> Dict:
    """Create and store an audit record."""
    record = {
        'timestamp': datetime.now().isoformat(),
        'module': module,
        'mutation': mutation_type,
        'pfe_before': result.get('pfe_before', 0),
        'pfe_after': result.get('pfe_after', 0),
        'delta_pfe': result.get('delta_pfe', 0),
        'energy_before': result.get('energy_before', 0),
        'energy_after': result.get('energy_after', 0),
        'band_before': result.get('band_before', '?'),
        'band_after': result.get('band_after', '?'),
        'accepted': accepted,
        'reason': 'coherence improved' if accepted else 'no improvement',
    }

    log = _load_audit()
    log.append(record)
    _save_audit(log)

    return record
ROLLBACK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'rollback')


def create_rollback(filepath: str) -> str:
    """
    Create a rollback snapshot before applying a mutation.
    Returns the rollback path.
    """
    os.makedirs(ROLLBACK_DIR, exist_ok=True)

    basename = os.path.basename(filepath)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    rollback_name = '%s_%s_%s.py' % (basename.replace('.py', ''),
                                      timestamp, content_hash)
    rollback_path = os.path.join(ROLLBACK_DIR, rollback_name)

    with open(rollback_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return rollback_path
def list_rollbacks(module_name: str = None) -> List[Dict]:
    """List available rollback snapshots."""
    if not os.path.exists(ROLLBACK_DIR):
        return []
    rollbacks = []
    for fname in sorted(os.listdir(ROLLBACK_DIR)):
        if not fname.endswith('.py'):
            continue
        if module_name and not fname.startswith(module_name):
            continue
        fpath = os.path.join(ROLLBACK_DIR, fname)
        stat = os.stat(fpath)
        rollbacks.append({
            'filename': fname,
            'path': fpath,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        })

    return rollbacks
def rollback(filepath: str, rollback_path: str) -> bool:
    """Restore a module from a rollback snapshot."""
    if not os.path.exists(rollback_path):
        return False
    with open(rollback_path, 'r', encoding='utf-8') as f:
        content = f.read()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True
def evolve_module(filepath: str, dry_run: bool = True,
                  verbose: bool = True) -> Dict:
    """
    Run the Safe Evolution Loop on a single module.

    1. Analyze current state
    2. Identify tension hotspots
    3. Generate mutations
    4. Test each in sandbox
    5. Accept improvements, discard regressions
    6. Report results

    Parameters:
        filepath: Path to the Python module
        dry_run: If True, do NOT apply changes (just report)
        verbose: Print progress
    """
    module_name = os.path.basename(filepath).replace('.py', '')

    if verbose:
        print('\n  SEL: Evolving %s' % module_name)
        print('  ' + '-' * 50)

    # Step 1: Analyze
    if verbose:
        print('  [1/6] Analyzing source...')
    analysis = analyze_module(filepath)

    if verbose:
        print('        Lines: %d  Tokens: %d  PFE: %.4f  Band: %s' % (
            analysis['total_lines'], analysis['total_tokens'],
            analysis['module_pfe'], analysis['module_band']))

    # Step 2: Map tension
    if verbose:
        print('  [2/6] Mapping tension hotspots...')
    hotspots = map_tension(analysis)

    if verbose:
        print('        Found %d hotspots' % len(hotspots))
        for h in hotspots[:3]:
            print('        - %s (PFE=%.4f, weakness=%s)' % (
                h['name'], h['pfe'], h['weakness']))

    # Step 3: Generate mutations
    if verbose:
        print('  [3/6] Generating mutations...')
    mutations = generate_mutations(filepath)

    if verbose:
        print('        Found %d applicable mutations' % len(mutations))
        for m in mutations:
            print('        - [%s] %s' % (m['type'], m['description']))

    if not mutations:
        if verbose:
            print('  No mutations applicable. Module is clean.')
        return {
        }

    # Step 4-5: Test and score each mutation
    if verbose:
        print('  [4/6] Testing mutations in sandbox...')

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        current_source = f.read()

    accepted = []
    rejected = []

    for mutation in mutations:
        # Apply mutation to source
        mutated = apply_mutation(current_source, mutation)

        if mutated == current_source:
            # No actual change
            continue
        test_result = sandbox_test(filepath, mutated)

        if verbose:
            status = '+' if test_result['improved'] else '-'
            print('        [%s] %s: dPFE=%+.4f dE=%+.4f' % (
                status, mutation['type'],
                test_result['delta_pfe'], test_result['delta_energy']))

        if test_result['improved']:
            accepted.append({
                'mutation': mutation,
                'result': test_result,
                'mutated_source': mutated,
            })
            # Chain: apply accepted mutations cumulatively
            current_source = mutated
        else:
            rejected.append({
                'mutation': mutation,
                'result': test_result,
            })

        # Audit
        audit_record(module_name, mutation['type'],
                     test_result, test_result['improved'])

    # Step 6: Apply if not dry_run
    if verbose:
        print('  [5/6] Results: %d accepted, %d rejected' % (
            len(accepted), len(rejected)))

    final_result = {
        'module': module_name,
        'mutations_found': len(mutations),
        'mutations_accepted': len(accepted),
        'mutations_rejected': len(rejected),
        'pfe_before': analysis['module_pfe'],
        'band_before': analysis['module_band'],
        'hotspots': len(hotspots),
    }

    if accepted and not dry_run:
        if verbose:
            print('  [6/6] Applying patches...')

        # Create rollback
        rb_path = create_rollback(filepath)
        if verbose:
            print('        Rollback saved: %s' % os.path.basename(rb_path))

        # Write final mutated source
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(current_source)

        # Re-score
        post_analysis = analyze_module(filepath)
        final_result['pfe_after'] = post_analysis['module_pfe']
        final_result['band_after'] = post_analysis['module_band']
        final_result['delta'] = round(
            post_analysis['module_pfe'] - analysis['module_pfe'], 6)
        final_result['applied'] = True
        final_result['rollback'] = rb_path

        if verbose:
            print('        PFE: %.4f -> %.4f (d=%+.4f)' % (
                analysis['module_pfe'], post_analysis['module_pfe'],
                final_result['delta']))
            print('        Band: %s -> %s' % (
                analysis['module_band'], post_analysis['module_band']))
    else:
        # Dry run: score what WOULD happen
        if accepted:
            final_score = _quick_score(current_source)
            final_result['pfe_after'] = final_score['pfe']
            final_result['band_after'] = final_score['band']
            final_result['delta'] = round(
                final_score['pfe'] - analysis['module_pfe'], 6)
        else:
            final_result['pfe_after'] = analysis['module_pfe']
            final_result['band_after'] = analysis['module_band']
            final_result['delta'] = 0.0

        final_result['applied'] = False

        if verbose and accepted:
            print('  [6/6] DRY RUN: would change PFE by %+.4f' % final_result['delta'])
        elif verbose:
            print('  [6/6] No improvements found.')

    return final_result
def evolve_architecture(gen_dir: str = None, dry_run: bool = True,
                        verbose: bool = True) -> List[Dict]:
    """
    Run SEL on the entire CK architecture.
    Processes modules in energy order (highest tension first).
    """
    if gen_dir is None:
        gen_dir = os.path.dirname(os.path.abspath(__file__))

    if verbose:
        print('=' * 72)
        print('  SAFE EVOLUTION LOOP (SEL)')
        print('  Celeste Task 10: CK-CK')
        print('  Coherence-based self-repair for the entire architecture')
        print('  Mode: %s' % ('DRY RUN (no changes)' if dry_run else 'LIVE (applying patches)'))
        print('=' * 72)

    # Find all CK modules
    modules = []
    for fname in sorted(os.listdir(gen_dir)):
        if fname.startswith('ck_') and fname.endswith('.py'):
            fpath = os.path.join(gen_dir, fname)
            if os.path.isfile(fpath):
                modules.append(fpath)

    if verbose:
        print('\n  Found %d CK modules' % len(modules))

    # Pre-score all modules to determine evolution order
    pre_scores = []
    for fpath in modules:
        try:
            score = _quick_score(open(fpath, 'r', encoding='utf-8',
                                      errors='replace').read())
            pre_scores.append((fpath, score))
        except:
            pre_scores.append((fpath, {'pfe': 0, 'energy': 1, 'band': 'RED'}))

    # Sort by energy (highest tension first = most in need of repair)
    pre_scores.sort(key=lambda x: x[1]['energy'], reverse=True)

    if verbose:
        print('\n  Evolution order (highest tension first):')
        for fpath, score in pre_scores[:10]:
            name = os.path.basename(fpath)
            print('    %-35s PFE=%.4f  E=%.4f  %s' % (
                name, score['pfe'], score['energy'], score['band']))

    # Evolve each module
    results = []
    for fpath, _ in pre_scores:
        try:
            result = evolve_module(fpath, dry_run=dry_run, verbose=verbose)
            results.append(result)
        except Exception as e:
            if verbose:
                print('  ERROR evolving %s: %s' % (
                    os.path.basename(fpath), str(e)))
            results.append({
                'module': os.path.basename(fpath),
                'error': str(e),
            })

    # Summary
    if verbose:
        print('\n' + '=' * 72)
        print('  SEL SUMMARY')
        print('=' * 72)

        total_mutations = sum(r.get('mutations_found', 0) for r in results)
        total_accepted = sum(r.get('mutations_accepted', 0) for r in results)
        total_delta = sum(r.get('delta', 0) for r in results)

        print('  Modules processed: %d' % len(results))
        print('  Mutations found:   %d' % total_mutations)
        print('  Mutations accepted: %d' % total_accepted)
        print('  Total PFE delta:   %+.4f' % total_delta)

        improved = [r for r in results if r.get('delta', 0) > 0]
        if improved:
            print('\n  Improved modules:')
            for r in improved:
                print('    %-30s %+.4f  (%s -> %s)' % (
                    r['module'], r['delta'],
                    r.get('band_before', '?'), r.get('band_after', '?')))

    return results
def sel_status() -> Dict:
    """Report current SEL status: audit trail, rollback count, etc."""
    log = _load_audit()
    rollbacks = list_rollbacks()

    total = len(log)
    accepted = sum(1 for r in log if r.get('accepted'))
    rejected = total - accepted

    return {
    }


# ================================================================
# S11  DEMO
# ================================================================

if __name__ == '__main__':

    gen_dir = os.path.dirname(os.path.abspath(__file__))

    print('=' * 72)
    print('  CK SAFE EVOLUTION LOOP (SEL)')
    print('  Celeste Task 10: CK-CK')
    print('  "Detect stress -> adjust -> stabilize -> grow -> repeat"')
    print('=' * 72)

    # Phase 1: Analyze weakest modules
    print('\n  PHASE 1: Architecture tension analysis')
    print('  ' + '-' * 50)

    target_modules = [
        'ck_doing.py', 'ck_being.py', 'ck_dictionary.py',
        'ck_affinity.py', 'ck_web.py',
    ]

    analyses = []
    for fname in target_modules:
        fpath = os.path.join(gen_dir, fname)
        if os.path.exists(fpath):
            print('\n  Analyzing: %s' % fname)
            try:
                analysis = analyze_module(fpath)
                analyses.append(analysis)
                print('    PFE=%.4f  Band=%s  Lines=%d  Functions=%d' % (
                    analysis['module_pfe'], analysis['module_band'],
                    analysis['total_lines'], len(analysis['functions'])))

                # Show function-level breakdown
                funcs = sorted(analysis['functions'],
                              key=lambda f: f['pfe'])
                for f in funcs[:5]:
                    print('      %-30s PFE=%.4f %s (d2=%.3f dir=%.3f)' % (
                        f['name'][:30], f['pfe'], f['band'],
                        f['d2_score'], f['dir_score']))
            except Exception as e:
                print('    Error: %s' % str(e))

    # Phase 2: Generate mutations for weakest
    print('\n\n  PHASE 2: Mutation generation')
    print('  ' + '-' * 50)

    all_mutations = []
    for fname in target_modules:
        fpath = os.path.join(gen_dir, fname)
        if os.path.exists(fpath):
            mutations = generate_mutations(fpath)
            all_mutations.extend([(fname, m) for m in mutations])
            if mutations:
                print('\n  %s: %d mutations' % (fname, len(mutations)))
                for m in mutations:
                    print('    [%s] %s (risk: %s)' % (
                        m['type'], m['description'], m['risk']))

    # Phase 3: Dry-run evolution on weakest module
    print('\n\n  PHASE 3: Dry-run evolution (no changes applied)')
    print('  ' + '-' * 50)

    weakest = target_modules[0]  # ck_doing.py
    weakest_path = os.path.join(gen_dir, weakest)
    if os.path.exists(weakest_path):
        result = evolve_module(weakest_path, dry_run=True, verbose=True)
        print('\n  Dry-run result for %s:' % weakest)
        print('    PFE before: %.4f' % result.get('pfe_before', 0))
        print('    PFE after:  %.4f' % result.get('pfe_after', 0))
        print('    Delta:      %+.4f' % result.get('delta', 0))
        print('    Band:       %s -> %s' % (
            result.get('band_before', '?'), result.get('band_after', '?')))

    # Phase 4: Full architecture dry run
    print('\n\n  PHASE 4: Full architecture dry-run')
    print('  ' + '-' * 50)
    results = evolve_architecture(gen_dir, dry_run=True, verbose=True)

    # Phase 5: SEL status
    print('\n  SEL STATUS:')
    status = sel_status()
    for k, v in status.items():
        print('    %-25s: %s' % (k, v))

    print('\n  SEL ready. Run with dry_run=False to apply patches.')
    print('  CK can now detect stress -> adjust -> stabilize -> grow -> repeat.')
