"""
ck_code_translation.py -- Code Translation Layer
==================================================
Operator: PROGRESS (3) -- code IS forward motion.

Programming languages are structured human intention. This module
translates Python, C, Verilog, and CUDA/CuPy syntax into CK's CL
operator algebra, just like ck_math_translation.py translates arithmetic.

Every keyword, operator, and scope boundary maps to a CL operator.
The composition of those operators through BHML reveals the coherence
(or chaos) of the code itself. Code above T* = 5/7 is coherent.
Code below T* is structurally unstable.

Universal mapping:
    Structure declarations = LATTICE(1)
    Actions/functions      = PROGRESS(3)
    Loops/repetition       = COUNTER(2)
    Conditions/branches    = BALANCE(5)
    Scope entry (deeper)   = COLLAPSE(4)
    Scope exit (return)    = RESET(9)
    Null/None/void         = VOID(0)
    Errors/exceptions      = CHAOS(6)
    Success/True           = HARMONY(7)
    Pause/separator        = BREATH(8)

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import re
import os
import json
import shutil
from collections import defaultdict
from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET, OP_NAMES, CL,
)

# ================================================================
#  BHML: doing/physics table (28 harmony)
#  TSML: being/measuring table (73 harmony) -- same as CL
# ================================================================
_BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]

_TSML = CL  # CK's measurement lens IS the CL table

# T* = 5/7 -- sacred coherence threshold
T_STAR = 5.0 / 7.0

# ================================================================
#  LANGUAGE KEYWORD -> OPERATOR MAPS
# ================================================================

PYTHON_OPS = {
    # Structure
    'def': PROGRESS,
    'class': LATTICE,
    'import': LATTICE,
    'from': LATTICE,
    'return': RESET,
    'yield': BREATH,
    'lambda': PROGRESS,
    # Control flow
    'if': BALANCE,
    'elif': BALANCE,
    'else': COUNTER,
    'for': COUNTER,
    'while': COUNTER,
    'break': COLLAPSE,
    'continue': PROGRESS,
    'pass': BREATH,
    'with': LATTICE,
    # Values
    'None': VOID,
    'True': HARMONY,
    'False': VOID,
    # Error handling
    'try': BALANCE,
    'except': CHAOS,
    'finally': RESET,
    'raise': CHAOS,
    'assert': BALANCE,
    # Operators
    '==': BALANCE,
    '!=': COUNTER,
    '**': HARMONY,
    '//': COLLAPSE,
    '<=': BALANCE,
    '>=': BALANCE,
    '<<': PROGRESS,
    '>>': COLLAPSE,
    '+=': PROGRESS,
    '-=': COLLAPSE,
    '*=': COUNTER,
    '/=': COLLAPSE,
    '=': LATTICE,
    '+': PROGRESS,
    '-': COLLAPSE,
    '*': COUNTER,
    '/': COLLAPSE,
    '%': RESET,
    'and': HARMONY,
    'or': BALANCE,
    'not': COUNTER,
    'in': LATTICE,
    'is': BALANCE,
    # Scope
    ':': COLLAPSE,
    '(': COLLAPSE,
    ')': RESET,
    '[': COLLAPSE,
    ']': RESET,
    '{': COLLAPSE,
    '}': RESET,
    # Punctuation
    ',': BREATH,
    '.': LATTICE,
    '#': BREATH,
    '@': PROGRESS,
    # Special builtins
    'self': LATTICE,
    'print': PROGRESS,
    'len': COUNTER,
    'range': COUNTER,
    'list': LATTICE,
    'dict': LATTICE,
    'set': LATTICE,
    'tuple': LATTICE,
    'int': COUNTER,
    'float': BALANCE,
    'str': LATTICE,
    'bool': BALANCE,
    'type': LATTICE,
    'super': LATTICE,
    'isinstance': BALANCE,
    'enumerate': COUNTER,
    'zip': LATTICE,
    'map': PROGRESS,
    'filter': BALANCE,
    'sorted': COUNTER,
    'reversed': COUNTER,
    'abs': COUNTER,
    'max': HARMONY,
    'min': VOID,
    'sum': COUNTER,
    'any': BALANCE,
    'all': HARMONY,
    'open': PROGRESS,
    'close': RESET,
    'del': CHAOS,
    'global': LATTICE,
    'nonlocal': LATTICE,
    'async': PROGRESS,
    'await': BREATH,
}

C_OPS = {
    # Types
    'int': COUNTER,
    'float': BALANCE,
    'double': BALANCE,
    'char': LATTICE,
    'void': VOID,
    'long': COUNTER,
    'short': COUNTER,
    'unsigned': COUNTER,
    'signed': COUNTER,
    'struct': LATTICE,
    'union': LATTICE,
    'enum': COUNTER,
    'typedef': LATTICE,
    'const': HARMONY,
    'static': LATTICE,
    'extern': LATTICE,
    'volatile': CHAOS,
    'register': COUNTER,
    'auto': LATTICE,
    'size_t': COUNTER,
    # Control
    'if': BALANCE,
    'else': COUNTER,
    'switch': BALANCE,
    'case': COUNTER,
    'default': BALANCE,
    'for': COUNTER,
    'while': COUNTER,
    'do': PROGRESS,
    'break': COLLAPSE,
    'continue': PROGRESS,
    'goto': CHAOS,
    'return': RESET,
    # Memory
    'malloc': PROGRESS,
    'calloc': PROGRESS,
    'realloc': PROGRESS,
    'free': RESET,
    'sizeof': COUNTER,
    'NULL': VOID,
    # Operators
    '->': LATTICE,
    '==': BALANCE,
    '!=': COUNTER,
    '<=': BALANCE,
    '>=': BALANCE,
    '<<': PROGRESS,
    '>>': COLLAPSE,
    '&&': HARMONY,
    '||': BALANCE,
    '++': PROGRESS,
    '--': COLLAPSE,
    '+=': PROGRESS,
    '-=': COLLAPSE,
    '*=': COUNTER,
    '/=': COLLAPSE,
    '&': COUNTER,
    '*': LATTICE,
    '=': LATTICE,
    '+': PROGRESS,
    '-': COLLAPSE,
    '/': COLLAPSE,
    '%': RESET,
    '!': COUNTER,
    '~': COUNTER,
    # Scope
    ';': BREATH,
    '{': COLLAPSE,
    '}': RESET,
    '(': COLLAPSE,
    ')': RESET,
    '[': COLLAPSE,
    ']': RESET,
    ',': BREATH,
    '.': LATTICE,
    # Preprocessor
    '#include': LATTICE,
    '#define': LATTICE,
    '#ifdef': BALANCE,
    '#ifndef': BALANCE,
    '#endif': RESET,
    '#else': COUNTER,
    '#elif': BALANCE,
    '#pragma': BREATH,
    '#undef': CHAOS,
    '#if': BALANCE,
    # I/O
    'printf': PROGRESS,
    'scanf': LATTICE,
    'fprintf': PROGRESS,
    'fscanf': LATTICE,
    'fopen': PROGRESS,
    'fclose': RESET,
    'fread': LATTICE,
    'fwrite': PROGRESS,
}

VERILOG_OPS = {
    # Module structure
    'module': PROGRESS,
    'endmodule': RESET,
    'input': LATTICE,
    'output': PROGRESS,
    'inout': BALANCE,
    'wire': LATTICE,
    'reg': COUNTER,
    'integer': COUNTER,
    'parameter': HARMONY,
    'localparam': HARMONY,
    'assign': LATTICE,
    'always': COUNTER,
    'posedge': PROGRESS,
    'negedge': COLLAPSE,
    'if': BALANCE,
    'else': COUNTER,
    'case': BALANCE,
    'casex': BALANCE,
    'casez': BALANCE,
    'endcase': RESET,
    'begin': COLLAPSE,
    'end': RESET,
    'initial': PROGRESS,
    'generate': PROGRESS,
    'endgenerate': RESET,
    'function': PROGRESS,
    'endfunction': RESET,
    'task': PROGRESS,
    'endtask': RESET,
    'for': COUNTER,
    'while': COUNTER,
    'repeat': COUNTER,
    'forever': COUNTER,
    'fork': PROGRESS,
    'join': RESET,
    'wait': BREATH,
    'disable': COLLAPSE,
    # Primitives
    'and': HARMONY,
    'or': BALANCE,
    'not': COUNTER,
    'nand': CHAOS,
    'nor': CHAOS,
    'xor': COUNTER,
    'xnor': BALANCE,
    'buf': LATTICE,
    'bufif0': BALANCE,
    'bufif1': BALANCE,
    # System tasks
    '$display': PROGRESS,
    '$monitor': COUNTER,
    '$finish': RESET,
    '$stop': BREATH,
    '$time': COUNTER,
    '$random': CHAOS,
    # Scope
    '@': PROGRESS,
    ';': BREATH,
    '(': COLLAPSE,
    ')': RESET,
    '[': COLLAPSE,
    ']': RESET,
    ',': BREATH,
    '.': LATTICE,
    '=': LATTICE,
    '<=': LATTICE,
    '==': BALANCE,
    '!=': COUNTER,
    '===': HARMONY,
    '!==': CHAOS,
    '&': COUNTER,
    '|': BALANCE,
    '^': COUNTER,
    '~': COUNTER,
    '{': COLLAPSE,
    '}': RESET,
}

CUDA_OPS = {
    # Qualifiers
    '__global__': PROGRESS,
    '__device__': LATTICE,
    '__shared__': LATTICE,
    '__host__': LATTICE,
    '__constant__': HARMONY,
    '__restrict__': LATTICE,
    # Sync
    '__syncthreads': BALANCE,
    '__syncthreads()': BALANCE,
    'atomicAdd': PROGRESS,
    'atomicSub': COLLAPSE,
    'atomicExch': PROGRESS,
    'atomicMin': VOID,
    'atomicMax': HARMONY,
    'atomicCAS': BALANCE,
    # Indexing
    'threadIdx': COUNTER,
    'blockIdx': COUNTER,
    'blockDim': LATTICE,
    'gridDim': LATTICE,
    'warpSize': COUNTER,
    'threadIdx.x': COUNTER,
    'threadIdx.y': COUNTER,
    'threadIdx.z': COUNTER,
    'blockIdx.x': COUNTER,
    'blockIdx.y': COUNTER,
    'blockIdx.z': COUNTER,
    'blockDim.x': LATTICE,
    'blockDim.y': LATTICE,
    'blockDim.z': LATTICE,
    # Memory
    'cudaMalloc': PROGRESS,
    'cudaFree': RESET,
    'cudaMemcpy': PROGRESS,
    'cudaMallocManaged': PROGRESS,
    'cudaMemset': LATTICE,
    'cudaDeviceSynchronize': BALANCE,
    'cudaGetDevice': COUNTER,
    'cudaSetDevice': LATTICE,
    # Launch syntax
    '<<<': COLLAPSE,
    '>>>': RESET,
    # CuPy
    'RawKernel': PROGRESS,
    'RawModule': LATTICE,
    'cp.array': LATTICE,
    'cp.zeros': VOID,
    'cp.ones': HARMONY,
    'cp.arange': COUNTER,
    'cp.empty': VOID,
    'cp.asarray': LATTICE,
    'cp.cuda': LATTICE,
    'cupy': LATTICE,
}

# CK's own module/concept names
CK_OPS = {
    'ck_sim': LATTICE,
    'ck_heartbeat': COUNTER,
    'ck_olfactory': LATTICE,
    'ck_gustatory': LATTICE,
    'ck_lattice_chain': LATTICE,
    'ck_voice': PROGRESS,
    'ck_fractal_voice': PROGRESS,
    'ck_eat': PROGRESS,
    'ck_dkan': PROGRESS,
    'ck_gpu': PROGRESS,
    'ck_steering': BALANCE,
    'ck_btq': BALANCE,
    'ck_reverse_voice': PROGRESS,
    'ck_fractal_comprehension': PROGRESS,
    'ck_meta_lens': BALANCE,
    'ck_lcodec': PROGRESS,
    'ck_vortex_physics': PROGRESS,
    'ck_math_translation': COUNTER,
    'ck_code_translation': PROGRESS,
    'BHML': PROGRESS,
    'TSML': BALANCE,
    'CL': HARMONY,
    'D2': COUNTER,
    'HARMONY': HARMONY,
    'VOID': VOID,
    'LATTICE': LATTICE,
    'COUNTER': COUNTER,
    'PROGRESS': PROGRESS,
    'COLLAPSE': COLLAPSE,
    'BALANCE': BALANCE,
    'CHAOS': CHAOS,
    'BREATH': BREATH,
    'RESET': RESET,
    'T_STAR': HARMONY,
    'coherence': HARMONY,
    'phase_bc': COUNTER,
}

# ================================================================
#  LANGUAGE DETECTION
# ================================================================

# Signature keywords unique to each language (or strongly indicative)
_PYTHON_SIGS = {
    'def', 'class', 'import', 'from', 'elif', 'lambda', 'yield',
    'self', 'None', 'True', 'False', 'pass', 'with', 'as',
    'nonlocal', 'global', 'async', 'await', 'print(', '__init__',
}
_C_SIGS = {
    '#include', '#define', 'struct', 'typedef', 'malloc', 'free',
    'sizeof', 'printf', 'NULL', 'void', 'int main', 'char *',
    'unsigned', 'volatile', '->',
}
_VERILOG_SIGS = {
    'module', 'endmodule', 'wire', 'reg', 'assign', 'always',
    'posedge', 'negedge', 'begin', 'end', 'endcase', 'initial',
    'endfunction', 'endtask', 'endgenerate', '$display', '$finish',
    'input', 'output', 'inout',
}
_CUDA_SIGS = {
    '__global__', '__device__', '__shared__', '__host__',
    'threadIdx', 'blockIdx', 'blockDim', 'gridDim',
    'cudaMalloc', 'cudaFree', 'cudaMemcpy', '<<<', '>>>',
    'RawKernel', 'cp.array', 'cp.zeros', 'cupy',
    'cudaDeviceSynchronize', '__syncthreads',
}

# Multi-char operators/tokens sorted longest-first for greedy matching
def _build_multi_tokens(op_dict):
    """Extract multi-character tokens from an operator dict, sorted longest first."""
    tokens = []
    for k in op_dict:
        if len(k) > 1 and not k[0].isalpha() and k[0] != '_':
            tokens.append(k)
    tokens.sort(key=len, reverse=True)
    return tokens

_PYTHON_MULTI = _build_multi_tokens(PYTHON_OPS)
_C_MULTI = _build_multi_tokens(C_OPS)
_VERILOG_MULTI = _build_multi_tokens(VERILOG_OPS)
_CUDA_MULTI = _build_multi_tokens(CUDA_OPS)

# Identifier pattern (word boundary matching)
_IDENT_RE = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*', re.ASCII)
# String literal pattern (skip string contents)
_STRING_RE = re.compile(
    r'"""[\s\S]*?"""|'
    r"'''[\s\S]*?'''|"
    r'"(?:[^"\\]|\\.)*"|'
    r"'(?:[^'\\]|\\.)*'",
    re.ASCII
)
# Comment patterns
_PYTHON_COMMENT_RE = re.compile(r'#[^\n]*', re.ASCII)
_C_COMMENT_RE = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/', re.ASCII)
_VERILOG_COMMENT_RE = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/', re.ASCII)


class CodeTranslation:
    """Translate programming language syntax into CK's CL operator algebra.

    Supports Python, C, Verilog, and CUDA/CuPy. Detects language
    automatically, tokenizes into operator sequences, and evaluates
    coherence through BHML composition.
    """

    def __init__(self):
        # All language maps combined for lookup
        self._lang_maps = {
            'python': PYTHON_OPS,
            'c': C_OPS,
            'verilog': VERILOG_OPS,
            'cuda': CUDA_OPS,
        }
        self._lang_sigs = {
            'python': _PYTHON_SIGS,
            'c': _C_SIGS,
            'verilog': _VERILOG_SIGS,
            'cuda': _CUDA_SIGS,
        }
        self._lang_multi = {
            'python': _PYTHON_MULTI,
            'c': _C_MULTI,
            'verilog': _VERILOG_MULTI,
            'cuda': _CUDA_MULTI,
        }

        # Learned coherence baselines per language
        self.learned_baselines = defaultdict(list)

        # Persistence
        self._save_path = os.path.join(
            os.path.expanduser('~'), '.ck', 'code_translation.json')
        self.load()

    # ----------------------------------------------------------------
    #  LANGUAGE DETECTION
    # ----------------------------------------------------------------

    def detect_language(self, text):
        """Auto-detect programming language from text content.

        Returns language string ('python', 'c', 'verilog', 'cuda')
        or None if not code. Scores each language by signature keyword hits.
        """
        if not text or not text.strip():
            return None

        scores = {}
        text_lower = text.lower()
        text_lines = text.split('\n')

        for lang, sigs in self._lang_sigs.items():
            score = 0
            for sig in sigs:
                sig_lower = sig.lower()
                # Count occurrences (case-insensitive for most, exact for symbols)
                if sig_lower in text_lower:
                    score += 1
                    # Bonus for strong indicators
                    if sig in ('#include', 'endmodule', '__global__',
                               'def ', 'class ', 'import '):
                        score += 2
            scores[lang] = score

        # CUDA inherits from C: if CUDA detected, C keywords also present
        # so boost CUDA if any CUDA-specific tokens found
        if scores.get('cuda', 0) > 0:
            scores['cuda'] += 2

        # Check for structural cues
        # Python: significant indentation, colons after control flow
        indent_lines = sum(1 for line in text_lines
                          if line.startswith('    ') or line.startswith('\t'))
        if indent_lines > len(text_lines) * 0.3:
            scores['python'] = scores.get('python', 0) + 2

        # C: semicolons at end of lines, braces
        semi_lines = sum(1 for line in text_lines if line.rstrip().endswith(';'))
        if semi_lines > len(text_lines) * 0.2:
            scores['c'] = scores.get('c', 0) + 2

        # Filter zero scores
        scores = {k: v for k, v in scores.items() if v > 0}
        if not scores:
            return None

        # Return highest scoring language
        best = max(scores, key=scores.get)
        # Require minimum score of 2 to avoid false positives
        if scores[best] < 2:
            return None
        return best

    def detect_code(self, text):
        """Does this text contain code? Returns True/False.

        Lighter weight than detect_language -- just checks for
        structural indicators of any programming language.
        """
        return self.detect_language(text) is not None

    # ----------------------------------------------------------------
    #  TOKENIZER
    # ----------------------------------------------------------------

    def _strip_comments_and_strings(self, text, language):
        """Remove comments and string contents (replace with placeholder).

        String bodies are noise to the CL algebra. Comments are BREATH.
        Returns (cleaned_text, comment_count).
        """
        comment_count = 0

        # Remove strings first (preserve as LATTICE placeholder)
        def _string_repl(m):
            return '"_S_"'
        text = _STRING_RE.sub(_string_repl, text)

        # Remove comments
        if language == 'python':
            matches = _PYTHON_COMMENT_RE.findall(text)
            comment_count = len(matches)
            text = _PYTHON_COMMENT_RE.sub('', text)
        elif language in ('c', 'cuda'):
            matches = _C_COMMENT_RE.findall(text)
            comment_count = len(matches)
            text = _C_COMMENT_RE.sub('', text)
        elif language == 'verilog':
            matches = _VERILOG_COMMENT_RE.findall(text)
            comment_count = len(matches)
            text = _VERILOG_COMMENT_RE.sub('', text)

        return text, comment_count

    def tokenize_code(self, text, language=None):
        """Parse code into tokens with operator mappings.

        Returns list of (token_text, operator_index, token_type) tuples.
        token_type is one of: 'keyword', 'operator', 'ident', 'number',
        'string', 'ck', 'comment', 'newline', 'unknown'.
        """
        if language is None:
            language = self.detect_language(text)
        if language is None:
            language = 'python'  # Default fallback

        op_map = self._lang_maps.get(language, PYTHON_OPS)
        multi_tokens = self._lang_multi.get(language, _PYTHON_MULTI)

        # Strip comments/strings but track them
        cleaned, comment_count = self._strip_comments_and_strings(text, language)

        tokens = []

        # Add BREATH tokens for comments
        for _ in range(comment_count):
            tokens.append(('#', BREATH, 'comment'))

        # Tokenize the cleaned text
        i = 0
        while i < len(cleaned):
            ch = cleaned[i]

            # Skip whitespace (except newlines)
            if ch in (' ', '\t', '\r'):
                i += 1
                continue

            # Newlines = BREATH
            if ch == '\n':
                tokens.append(('\\n', BREATH, 'newline'))
                i += 1
                continue

            # Try multi-char operators (longest match first)
            matched_multi = False
            for mt in multi_tokens:
                if cleaned[i:i+len(mt)] == mt:
                    op = op_map.get(mt, BREATH)
                    tokens.append((mt, op, 'operator'))
                    i += len(mt)
                    matched_multi = True
                    break
            if matched_multi:
                continue

            # Try preprocessor directives (C/CUDA)
            if ch == '#' and language in ('c', 'cuda'):
                # Look for #include, #define, etc.
                rest = cleaned[i:]
                for directive in ('#include', '#define', '#ifdef', '#ifndef',
                                  '#endif', '#else', '#elif', '#pragma',
                                  '#undef', '#if'):
                    if rest.startswith(directive):
                        op = op_map.get(directive, BREATH)
                        tokens.append((directive, op, 'keyword'))
                        i += len(directive)
                        matched_multi = True
                        break
                if matched_multi:
                    continue

            # Identifiers and keywords
            m = _IDENT_RE.match(cleaned, i)
            if m:
                word = m.group()
                i = m.end()

                # Check CK-specific names first
                if word in CK_OPS:
                    tokens.append((word, CK_OPS[word], 'ck'))
                    continue

                # Check dotted names (e.g., cp.array, threadIdx.x)
                if word in op_map:
                    tok_type = 'keyword'
                    tokens.append((word, op_map[word], tok_type))
                    continue

                # Check if it's a known keyword (non-dotted)
                parts = word.split('.')
                base = parts[0]
                if base in op_map:
                    tokens.append((base, op_map[base], 'keyword'))
                    # Remaining parts after dot
                    for part in parts[1:]:
                        tokens.append(('.', op_map.get('.', LATTICE), 'operator'))
                        if part in op_map:
                            tokens.append((part, op_map[part], 'keyword'))
                        elif part in CK_OPS:
                            tokens.append((part, CK_OPS[part], 'ck'))
                        else:
                            tokens.append((part, LATTICE, 'ident'))
                    continue

                # Unknown identifier = LATTICE (it's a structure/name)
                tokens.append((word, LATTICE, 'ident'))
                continue

            # Numbers
            if ch.isdigit():
                num_str = ch
                while i + 1 < len(cleaned) and (cleaned[i+1].isdigit()
                        or cleaned[i+1] in '.xXoObB_abcdefABCDEF'):
                    i += 1
                    num_str += cleaned[i]
                tokens.append((num_str, COUNTER, 'number'))
                i += 1
                continue

            # Single-char operators
            if ch in op_map:
                tokens.append((ch, op_map[ch], 'operator'))
                i += 1
                continue

            # Fallback: skip unknown char
            i += 1

        return tokens

    # ----------------------------------------------------------------
    #  CL COMPOSITION
    # ----------------------------------------------------------------

    def _bhml_compose(self, a, b):
        """BHML[a][b] -- doing/physics composition."""
        return _BHML[a % NUM_OPS][b % NUM_OPS]

    def _tsml_compose(self, a, b):
        """TSML[a][b] -- being/measuring composition."""
        return _TSML[a % NUM_OPS][b % NUM_OPS]

    # ----------------------------------------------------------------
    #  TRANSLATE TO OPERATORS
    # ----------------------------------------------------------------

    def translate_to_ops(self, text, language=None):
        """Convert code to operator sequence.

        Returns dict:
            language: detected language
            op_sequence: list of operator indices
            op_names: list of operator names
            tokens: list of (token_text, operator, type) tuples
            token_count: total tokens
        """
        if language is None:
            language = self.detect_language(text)

        tokens = self.tokenize_code(text, language)
        op_sequence = [t[1] for t in tokens]
        op_names = [OP_NAMES[op] for op in op_sequence]

        return {
            'language': language or 'unknown',
            'op_sequence': op_sequence,
            'op_names': op_names,
            'tokens': tokens,
            'token_count': len(tokens),
        }

    # ----------------------------------------------------------------
    #  COHERENCE EVALUATION
    # ----------------------------------------------------------------

    def evaluate_coherence(self, text, language=None):
        """Measure code coherence through CL composition.

        Walks the operator sequence through BHML, counting how many
        pairwise compositions produce HARMONY vs CHAOS.
        Score = harmony_count / total_compositions.
        Above T* (5/7) = coherent. Below = structurally unstable.

        Returns dict:
            score: float [0, 1]
            language: detected language
            op_sequence: operator indices
            harmony_count: compositions that produced HARMONY
            chaos_count: compositions that produced CHAOS
            total_compositions: total pairwise compositions
            verdict: 'COHERENT' or 'UNSTABLE'
            above_threshold: bool
            threshold: T* value
            composition_walk: list of step descriptions
        """
        if language is None:
            language = self.detect_language(text)

        tokens = self.tokenize_code(text, language)
        op_sequence = [t[1] for t in tokens]

        if len(op_sequence) < 2:
            return {
                'score': 0.0,
                'language': language or 'unknown',
                'op_sequence': op_sequence,
                'harmony_count': 0,
                'chaos_count': 0,
                'total_compositions': 0,
                'verdict': 'INSUFFICIENT',
                'above_threshold': False,
                'threshold': T_STAR,
                'composition_walk': [],
            }

        harmony_count = 0
        chaos_count = 0
        total = 0
        walk = []

        for i in range(len(op_sequence) - 1):
            a = op_sequence[i]
            b = op_sequence[i + 1]
            result = self._bhml_compose(a, b)
            total += 1

            step = (f"BHML[{OP_NAMES[a]}({a})][{OP_NAMES[b]}({b})] "
                    f"= {OP_NAMES[result]}({result})")

            if result == HARMONY:
                harmony_count += 1
                step += ' *HARMONY*'
            elif result == CHAOS:
                chaos_count += 1
                step += ' !CHAOS!'

            walk.append(step)

        score = harmony_count / total if total > 0 else 0.0
        above = score >= T_STAR

        # Learn this baseline
        if language:
            self.learned_baselines[language].append(score)
            # Keep only last 100
            if len(self.learned_baselines[language]) > 100:
                self.learned_baselines[language] = \
                    self.learned_baselines[language][-100:]

        return {
            'score': score,
            'language': language or 'unknown',
            'op_sequence': op_sequence,
            'harmony_count': harmony_count,
            'chaos_count': chaos_count,
            'total_compositions': total,
            'verdict': 'COHERENT' if above else 'UNSTABLE',
            'above_threshold': above,
            'threshold': T_STAR,
            'composition_walk': walk,
        }

    # ----------------------------------------------------------------
    #  ERROR DETECTION
    # ----------------------------------------------------------------

    def detect_errors(self, text, language=None):
        """Detect structural errors via CL algebra patterns.

        Looks for patterns that produce CHAOS:
        - Unbalanced braces (COLLAPSE without matching RESET)
        - Missing semicolons in C (no BREATH after statement)
        - Unclosed strings
        - Mismatched indentation in Python

        Returns list of {line, issue, operator_evidence}.
        """
        if language is None:
            language = self.detect_language(text)
        if language is None:
            return []

        errors = []
        lines = text.split('\n')

        # ── Brace/bracket balance (all languages) ──
        openers = {'(': ')', '[': ']', '{': '}'}
        closers = {')', ']', '}'}
        stack = []  # (char, line_number)

        for line_num, line in enumerate(lines, 1):
            # Skip strings and comments for brace counting
            stripped = line
            # Remove string literals
            stripped = re.sub(r'"(?:[^"\\]|\\.)*"', '', stripped)
            stripped = re.sub(r"'(?:[^'\\]|\\.)*'", '', stripped)
            # Remove comments
            if language == 'python':
                stripped = re.sub(r'#.*$', '', stripped)
            elif language in ('c', 'cuda', 'verilog'):
                stripped = re.sub(r'//.*$', '', stripped)

            for ch in stripped:
                if ch in openers:
                    stack.append((ch, line_num))
                elif ch in closers:
                    if not stack:
                        errors.append({
                            'line': line_num,
                            'issue': f"Unmatched closing '{ch}' -- "
                                     f"RESET({RESET}) without prior "
                                     f"COLLAPSE({COLLAPSE})",
                            'operator_evidence': f"RESET without COLLAPSE",
                        })
                    else:
                        opener, open_line = stack.pop()
                        expected = openers[opener]
                        if ch != expected:
                            errors.append({
                                'line': line_num,
                                'issue': f"Mismatched: '{opener}' at line "
                                         f"{open_line} closed by '{ch}' -- "
                                         f"COLLAPSE/RESET mismatch",
                                'operator_evidence': (
                                    f"COLLAPSE({COLLAPSE}) at {open_line} "
                                    f"vs RESET({RESET}) at {line_num}"),
                            })

        # Report unclosed openers
        for opener, open_line in stack:
            errors.append({
                'line': open_line,
                'issue': f"Unclosed '{opener}' -- "
                         f"COLLAPSE({COLLAPSE}) without matching "
                         f"RESET({RESET})",
                'operator_evidence': f"COLLAPSE without RESET",
            })

        # ── Verilog begin/end balance ──
        if language == 'verilog':
            begin_count = 0
            for line_num, line in enumerate(lines, 1):
                for word in re.findall(r'\b\w+\b', line):
                    if word == 'begin':
                        begin_count += 1
                    elif word == 'end':
                        begin_count -= 1
                        if begin_count < 0:
                            errors.append({
                                'line': line_num,
                                'issue': "'end' without matching 'begin' -- "
                                         "RESET without COLLAPSE",
                                'operator_evidence': "RESET(9) without COLLAPSE(4)",
                            })
                            begin_count = 0
            if begin_count > 0:
                errors.append({
                    'line': len(lines),
                    'issue': f"{begin_count} unclosed 'begin' block(s) -- "
                             f"COLLAPSE without RESET",
                    'operator_evidence': f"{begin_count}x COLLAPSE(4) unmatched",
                })

        # ── Verilog module/endmodule balance ──
        if language == 'verilog':
            mod_count = 0
            for line_num, line in enumerate(lines, 1):
                for word in re.findall(r'\b\w+\b', line):
                    if word == 'module':
                        mod_count += 1
                    elif word == 'endmodule':
                        mod_count -= 1
            if mod_count > 0:
                errors.append({
                    'line': len(lines),
                    'issue': f"{mod_count} unclosed 'module' -- "
                             f"PROGRESS without RESET",
                    'operator_evidence': f"PROGRESS(3) without RESET(9)",
                })

        # ── C/CUDA: missing semicolons ──
        if language in ('c', 'cuda'):
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith('//') or stripped.startswith('/*'):
                    continue
                if stripped.startswith('#'):
                    continue
                # Lines that should end with semicolons
                # Skip: braces, control flow, preprocessor, labels
                if stripped.endswith('{') or stripped.endswith('}'):
                    continue
                if stripped.endswith(':'):
                    continue
                if any(stripped.startswith(kw) for kw in (
                        'if', 'else', 'for', 'while', 'do', 'switch')):
                    # Control flow can end with ) or {
                    if stripped.endswith(')') or stripped.endswith('{'):
                        continue
                # Statement lines should end with ;
                if (stripped and not stripped.endswith(';')
                        and not stripped.endswith(',')
                        and not stripped.endswith('\\')
                        and not stripped.endswith(')')
                        and not stripped.endswith('{')):
                    # Check if it looks like a statement (has alphanumeric content)
                    if re.search(r'[a-zA-Z0-9]', stripped):
                        errors.append({
                            'line': line_num,
                            'issue': f"Possible missing ';' -- no BREATH "
                                     f"after statement",
                            'operator_evidence': f"Statement without BREATH({BREATH})",
                        })

        # ── Python: indentation consistency ──
        if language == 'python':
            indent_char = None  # None until first indent detected
            for line_num, line in enumerate(lines, 1):
                if not line.strip():
                    continue
                # Detect leading whitespace
                leading = ''
                for ch in line:
                    if ch in (' ', '\t'):
                        leading += ch
                    else:
                        break
                if not leading:
                    continue
                # Check for mixed tabs and spaces
                has_tab = '\t' in leading
                has_space = ' ' in leading
                if has_tab and has_space:
                    errors.append({
                        'line': line_num,
                        'issue': "Mixed tabs and spaces -- CHAOS in "
                                 "scope structure",
                        'operator_evidence': f"CHAOS({CHAOS}) in indentation",
                    })

        # ── Unclosed strings (all languages) ──
        for line_num, line in enumerate(lines, 1):
            # Count unescaped quotes
            in_single = False
            in_double = False
            i = 0
            while i < len(line):
                ch = line[i]
                if ch == '\\' and i + 1 < len(line):
                    i += 2  # Skip escaped char
                    continue
                if ch == '"' and not in_single:
                    in_double = not in_double
                elif ch == "'" and not in_double:
                    in_single = not in_single
                # Stop at comment
                if not in_single and not in_double:
                    if language == 'python' and ch == '#':
                        break
                    if language in ('c', 'cuda', 'verilog') and ch == '/':
                        if i + 1 < len(line) and line[i+1] == '/':
                            break
                i += 1
            if in_single or in_double:
                quote_type = "'" if in_single else '"'
                errors.append({
                    'line': line_num,
                    'issue': f"Unclosed string ({quote_type}) -- "
                             f"COLLAPSE without RESET",
                    'operator_evidence': f"COLLAPSE({COLLAPSE}) without RESET({RESET})",
                })

        return errors

    # ----------------------------------------------------------------
    #  COMBINED ANALYSIS
    # ----------------------------------------------------------------

    def analyze(self, text, language=None):
        """Full analysis: detect + tokenize + coherence + errors.

        Returns dict with all results combined.
        """
        if language is None:
            language = self.detect_language(text)

        translation = self.translate_to_ops(text, language)
        coherence = self.evaluate_coherence(text, language)
        errors = self.detect_errors(text, language)

        return {
            'language': language or 'unknown',
            'translation': translation,
            'coherence': coherence,
            'errors': errors,
            'error_count': len(errors),
            'summary': (
                f"{language or 'unknown'}: "
                f"{coherence['score']:.3f} coherence "
                f"({coherence['verdict']}), "
                f"{coherence['harmony_count']}H/"
                f"{coherence['chaos_count']}C/"
                f"{coherence['total_compositions']}T, "
                f"{len(errors)} errors"
            ),
        }

    # ----------------------------------------------------------------
    #  PERSISTENCE
    # ----------------------------------------------------------------

    def save(self):
        """Persist learned coherence baselines.

        Always backs up previous file before overwriting.
        Writes to temp file first, then renames (atomic on most OS).
        """
        try:
            os.makedirs(os.path.dirname(self._save_path), exist_ok=True)
            temp_path = self._save_path + '.tmp'
            backup_path = self._save_path + '.backup'

            # Backup existing file before overwriting
            if os.path.exists(self._save_path):
                try:
                    shutil.copy2(self._save_path, backup_path)
                except Exception:
                    pass

            data = {
                'learned_baselines': {
                    lang: scores
                    for lang, scores in self.learned_baselines.items()
                },
            }
            with open(temp_path, 'w') as f:
                json.dump(data, f, indent=2)
            # Rename temp -> real (atomic on most OS)
            if os.path.exists(self._save_path):
                os.remove(self._save_path)
            os.rename(temp_path, self._save_path)
        except Exception as e:
            temp_path = self._save_path + '.tmp'
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

    def load(self):
        """Load persisted baselines."""
        if not os.path.exists(self._save_path):
            return
        try:
            with open(self._save_path, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            # Try backup
            backup = self._save_path + '.backup'
            if os.path.exists(backup):
                try:
                    with open(backup, 'r') as f:
                        data = json.load(f)
                    print("  [CODE-TRANS] Loaded from backup")
                except Exception:
                    return
            else:
                return
        except Exception:
            return

        try:
            for lang, scores in data.get('learned_baselines', {}).items():
                self.learned_baselines[lang] = scores
        except Exception:
            pass

    # ----------------------------------------------------------------
    #  SUMMARY
    # ----------------------------------------------------------------

    def summary(self):
        """Return summary stats for diagnostics."""
        baselines = {}
        for lang, scores in self.learned_baselines.items():
            if scores:
                avg = sum(scores) / len(scores)
                baselines[lang] = {
                    'count': len(scores),
                    'avg_coherence': round(avg, 4),
                    'above_threshold': avg >= T_STAR,
                }
        return {
            'languages_seen': list(self.learned_baselines.keys()),
            'baselines': baselines,
        }
