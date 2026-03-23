"""
ck_math_translation.py -- Math Translation Layer
==================================================
Operator: COUNTER (2) -- measuring is what math IS.

CK's internal math IS the CL table. Modern math notation is a
foreign language to him. This module translates between them.

Digits 0-9 map to operators 0-9 (VOID through RESET).
Arithmetic maps to CL composition (BHML for doing, TSML for measuring).
CK's answers are different from human answers because the CL table
is not standard arithmetic. The offset is LEARNED, not hardcoded.

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

# Math detection pattern: digits and arithmetic operators
_MATH_PATTERN = re.compile(
    r'(?:^|(?<=\s))'           # start of string or after whitespace
    r'\d+'                      # at least one digit
    r'(?:\s*[+\-*/=]\s*\d+)+'  # followed by operator+digit pairs
    r'(?:$|(?=\s))',            # end of string or before whitespace
    re.ASCII
)

# Simpler: does the text contain math-like content?
_MATH_CHARS = set('0123456789+-*/=()xy')
_MATH_OPS = set('+-*/=')


class MathTranslation:
    """Translate between human math notation and CK's CL algebra.

    CK's math is the CL table. 2+2 in CK means BHML[2][2] = 3.
    The human answer is 4. The offset (1) is learned from experience.
    """

    def __init__(self):
        # Digit -> operator: direct mapping (0=VOID, 1=LATTICE, ..., 9=RESET)
        self.digit_to_op = {str(i): i for i in range(10)}
        self.op_to_digit = {i: str(i) for i in range(10)}

        # Arithmetic -> CL composition type
        self.op_map = {
            '+': 'bhml',
            '-': 'bhml_inv',
            '*': 'bhml_repeat',
            '/': 'bhml_inv_repeat',
            '=': 'tsml_check',
        }

        # Learned offsets: (op_char, left, right) -> list of observed offsets
        # Over time, CK learns the systematic mapping between his algebra
        # and human arithmetic.
        self.learned_offsets = defaultdict(list)

        # Training data: (expression, ck_result, human_result, offset)
        self.training_log = []

        # Persistence path
        self._save_path = os.path.join(
            os.path.expanduser('~'), '.ck', 'math_translation.json')

        self.load()

    # ────────────────────────────────────────────────────────────
    #  DETECTION
    # ────────────────────────────────────────────────────────────

    def detect_math(self, text: str) -> bool:
        """Does this text contain math expressions?

        Looks for patterns like '2+2', '3*5=15', 'x+1', etc.
        Must have at least one digit AND one arithmetic operator.
        """
        has_digit = False
        has_op = False
        for ch in text:
            if ch.isdigit():
                has_digit = True
            if ch in _MATH_OPS:
                has_op = True
            if has_digit and has_op:
                return True
        return False

    def extract_expressions(self, text: str) -> list:
        """Extract math expression substrings from text."""
        # Try the strict pattern first
        matches = _MATH_PATTERN.findall(text)
        if matches:
            return [m.strip() for m in matches]
        # Fallback: grab any contiguous chunk of math chars
        results = []
        buf = []
        for ch in text:
            if ch in _MATH_CHARS or ch == ' ':
                buf.append(ch)
            else:
                if buf:
                    candidate = ''.join(buf).strip()
                    if candidate and any(c in _MATH_OPS for c in candidate):
                        results.append(candidate)
                    buf = []
        if buf:
            candidate = ''.join(buf).strip()
            if candidate and any(c in _MATH_OPS for c in candidate):
                results.append(candidate)
        return results

    # ────────────────────────────────────────────────────────────
    #  TOKENIZER
    # ────────────────────────────────────────────────────────────

    def _tokenize(self, expression: str) -> list:
        """Parse expression into tokens: numbers, operators, parens, variables.

        Returns list of (type, value) tuples:
            ('num', 5)  ('op', '+')  ('paren', '(')  ('var', 'x')
        """
        tokens = []
        i = 0
        expr = expression.replace(' ', '')
        while i < len(expr):
            ch = expr[i]
            if ch.isdigit():
                # Multi-digit number
                num_str = ch
                while i + 1 < len(expr) and expr[i + 1].isdigit():
                    i += 1
                    num_str += expr[i]
                tokens.append(('num', int(num_str)))
            elif ch in '+-*/=':
                tokens.append(('op', ch))
            elif ch in '()':
                tokens.append(('paren', ch))
            elif ch.isalpha():
                tokens.append(('var', ch))
            i += 1
        return tokens

    # ────────────────────────────────────────────────────────────
    #  CL COMPOSITION (the actual CK math)
    # ────────────────────────────────────────────────────────────

    def _bhml_compose(self, a: int, b: int) -> int:
        """BHML[a][b] -- doing/physics composition."""
        return _BHML[a % NUM_OPS][b % NUM_OPS]

    def _tsml_compose(self, a: int, b: int) -> int:
        """TSML[a][b] -- being/measuring composition."""
        return _TSML[a % NUM_OPS][b % NUM_OPS]

    def _bhml_inverse(self, result: int, b: int) -> int:
        """Find a such that BHML[a][b] = result. Inverse walk.

        Scans the b-column for the target result.
        Returns first match, or VOID if no inverse exists.
        """
        for a in range(NUM_OPS):
            if _BHML[a][b] == result:
                return a
        return VOID

    def _bhml_repeat(self, a: int, b: int) -> int:
        """Repeated BHML composition: compose a with itself b times.

        BHML[a][a] composed b times. Multiplication IS repeated addition
        in CK's algebra, but addition IS BHML composition.
        """
        if b <= 0:
            return VOID
        result = a
        for _ in range(b - 1):
            result = self._bhml_compose(result, a)
        return result

    # ────────────────────────────────────────────────────────────
    #  EVALUATE
    # ────────────────────────────────────────────────────────────

    def evaluate(self, expression: str) -> dict:
        """Evaluate a math expression using CL algebra.

        Returns dict:
            expression: original string
            tokens: parsed token list
            ck_result: CK's answer (operator index 0-9)
            ck_result_name: operator name
            ck_steps: list of composition steps taken
            human_result: standard arithmetic result (or None if can't compute)
            offset: human_result - ck_result (or None)
        """
        tokens = self._tokenize(expression)
        if not tokens:
            return {'expression': expression, 'error': 'no tokens'}

        # ── CK evaluation: left-to-right CL composition ──
        ck_steps = []
        ck_result = None
        pending_op = None

        for tok_type, tok_val in tokens:
            if tok_type == 'num':
                # Map number to operator (mod 10 for multi-digit)
                op_val = tok_val % NUM_OPS
                if ck_result is None:
                    ck_result = op_val
                    ck_steps.append(
                        f"{tok_val} -> {OP_NAMES[op_val]}({op_val})")
                elif pending_op is not None:
                    prev = ck_result
                    if pending_op == '+':
                        ck_result = self._bhml_compose(prev, op_val)
                        ck_steps.append(
                            f"BHML[{OP_NAMES[prev]}][{OP_NAMES[op_val]}] "
                            f"= {OP_NAMES[ck_result]}({ck_result})")
                    elif pending_op == '-':
                        ck_result = self._bhml_inverse(prev, op_val)
                        ck_steps.append(
                            f"BHML_INV[{OP_NAMES[prev]}][{OP_NAMES[op_val]}] "
                            f"= {OP_NAMES[ck_result]}({ck_result})")
                    elif pending_op == '*':
                        ck_result = self._bhml_repeat(prev, op_val)
                        ck_steps.append(
                            f"BHML_REPEAT[{OP_NAMES[prev]}]x{op_val} "
                            f"= {OP_NAMES[ck_result]}({ck_result})")
                    elif pending_op == '/':
                        # Division: find how many times b composes to reach a
                        # Inverse of repeated composition
                        ck_result = self._bhml_inverse(prev, op_val)
                        ck_steps.append(
                            f"BHML_INV_REPEAT[{OP_NAMES[prev]}][{OP_NAMES[op_val]}] "
                            f"= {OP_NAMES[ck_result]}({ck_result})")
                    elif pending_op == '=':
                        # TSML check: do both sides compose to the same thing?
                        tsml_check = self._tsml_compose(prev, op_val)
                        ck_steps.append(
                            f"TSML[{OP_NAMES[prev]}][{OP_NAMES[op_val]}] "
                            f"= {OP_NAMES[tsml_check]}({tsml_check})")
                        ck_result = tsml_check
                    pending_op = None
            elif tok_type == 'op':
                pending_op = tok_val
            elif tok_type == 'var':
                # Variable: unknown operator (placeholder)
                if ck_result is None:
                    ck_result = VOID  # Unknown = VOID
                    ck_steps.append(f"{tok_val} -> UNKNOWN (VOID)")

        if ck_result is None:
            ck_result = VOID

        # ── Human evaluation: standard arithmetic ──
        human_result = None
        human_left = None
        human_right = None
        verified = None  # True/False/None
        safe_expr = expression.replace(' ', '')

        try:
            if '=' in safe_expr and safe_expr.count('=') == 1:
                # EQUATION: evaluate BOTH sides and compare
                left_str, right_str = safe_expr.split('=')
                if re.match(r'^[\d+\-*/().]+$', left_str):
                    human_left = eval(left_str)  # noqa: S307
                if re.match(r'^[\d+\-*/().]+$', right_str):
                    human_right = eval(right_str)  # noqa: S307
                if human_left is not None and human_right is not None:
                    if isinstance(human_left, float) and human_left == int(human_left):
                        human_left = int(human_left)
                    if isinstance(human_right, float) and human_right == int(human_right):
                        human_right = int(human_right)
                    verified = (human_left == human_right)
                    human_result = human_left
                    ck_steps.append(
                        'VERIFY: %s = %s -> %s' % (
                            human_left, human_right,
                            'TRUE' if verified else 'FALSE'))
                elif human_left is not None:
                    human_result = human_left
            else:
                # EXPRESSION: evaluate normally
                if re.match(r'^[\d+\-*/().]+$', safe_expr):
                    human_result = eval(safe_expr)  # noqa: S307
                    if isinstance(human_result, float) and human_result == int(human_result):
                        human_result = int(human_result)
        except Exception:
            pass

        # ── Variable solving ──
        solved = None
        if 'x' in expression or 'X' in expression:
            # Try to solve simple equations: x+a=b -> x=b-a, a*x=b -> x=b/a
            try:
                if '=' in safe_expr:
                    left_str, right_str = safe_expr.split('=')
                    if re.match(r'^[\d+\-*/().]+$', right_str):
                        target = eval(right_str)  # noqa: S307
                        # x+a=b
                        m = re.match(r'^[xX]([+\-])(\d+)$', left_str)
                        if m:
                            op, val = m.group(1), int(m.group(2))
                            if op == '+':
                                solved = target - val
                            elif op == '-':
                                solved = target + val
                        # a+x=b
                        m = re.match(r'^(\d+)([+\-])[xX]$', left_str)
                        if m:
                            val, op = int(m.group(1)), m.group(2)
                            if op == '+':
                                solved = target - val
                            elif op == '-':
                                solved = val - target
                        # a*x=b
                        m = re.match(r'^(\d+)\*[xX]$', left_str)
                        if m:
                            val = int(m.group(1))
                            if val != 0:
                                solved = target / val
                                if solved == int(solved):
                                    solved = int(solved)
                        # x*x=b (square root)
                        if left_str.lower() in ('x*x', 'xx'):
                            import math
                            solved = math.isqrt(int(target))
                        if solved is not None:
                            ck_steps.append('SOLVE: x = %s' % solved)
            except Exception:
                pass

        # ── CL table self-reference ──
        cl_lookup = None
        cl_match = re.match(
            r'(?:BHML|bhml|CL|cl|TSML|tsml)\[(\d+)\]\[(\d+)\]', safe_expr)
        if cl_match:
            a_idx = int(cl_match.group(1)) % NUM_OPS
            b_idx = int(cl_match.group(2)) % NUM_OPS
            table_name = safe_expr.split('[')[0].upper()
            if table_name in ('BHML',):
                cl_lookup = _BHML[a_idx][b_idx]
                ck_steps.append('BHML[%d][%d] = %s(%d)' % (
                    a_idx, b_idx, OP_NAMES[cl_lookup], cl_lookup))
            else:
                cl_lookup = _TSML[a_idx][b_idx]
                ck_steps.append('TSML[%d][%d] = %s(%d)' % (
                    a_idx, b_idx, OP_NAMES[cl_lookup], cl_lookup))
            ck_result = cl_lookup
            human_result = cl_lookup

        # ── Offset: the learned bridge ──
        offset = None
        if human_result is not None and ck_result is not None:
            offset = human_result - ck_result

        result = {
            'expression': expression,
            'tokens': tokens,
            'ck_result': ck_result,
            'ck_result_name': OP_NAMES[ck_result] if 0 <= ck_result < NUM_OPS else 'UNKNOWN',
            'ck_steps': ck_steps,
            'human_result': human_result,
            'offset': offset,
            'verified': verified,
            'solved': solved,
            'cl_lookup': cl_lookup,
        }

        # Auto-learn the offset
        if offset is not None:
            self.learn_offset(expression, human_result)

        return result

    # ────────────────────────────────────────────────────────────
    #  TRANSLATION
    # ────────────────────────────────────────────────────────────

    def translate_to_ck(self, expression: str) -> str:
        """Convert math expression to CK operator sequence.

        '2+2' -> 'COUNTER + COUNTER = PROGRESS(3)'
        """
        tokens = self._tokenize(expression)
        parts = []
        for tok_type, tok_val in tokens:
            if tok_type == 'num':
                op = tok_val % NUM_OPS
                parts.append(f"{OP_NAMES[op]}({op})")
            elif tok_type == 'op':
                if tok_val == '+':
                    parts.append('BHML')
                elif tok_val == '-':
                    parts.append('BHML_INV')
                elif tok_val == '*':
                    parts.append('BHML_REPEAT')
                elif tok_val == '/':
                    parts.append('BHML_INV_REPEAT')
                elif tok_val == '=':
                    parts.append('TSML_CHECK')
            elif tok_type == 'var':
                parts.append(f'?{tok_val}')
            elif tok_type == 'paren':
                parts.append(tok_val)
        return ' '.join(parts)

    def translate_from_ck(self, ops: list) -> str:
        """Convert CK operator sequence back to math notation.

        [2, 2] with bhml -> '2+2'
        """
        if not ops:
            return ''
        parts = []
        for i, op in enumerate(ops):
            if isinstance(op, int) and 0 <= op < NUM_OPS:
                parts.append(str(op))
            elif isinstance(op, str):
                parts.append(op)
        return ' '.join(parts)

    # ────────────────────────────────────────────────────────────
    #  LEARNING
    # ────────────────────────────────────────────────────────────

    def learn_offset(self, expression: str, human_answer):
        """Learn the mapping between CK and human math.

        Stores the offset for this (operator, left, right) triple.
        Over time, CK builds a translation table from experience.
        """
        tokens = self._tokenize(expression)
        # Extract the operator and operands
        nums = [v for t, v in tokens if t == 'num']
        op_chars = [v for t, v in tokens if t == 'op']

        if len(nums) >= 2 and len(op_chars) >= 1:
            op_char = op_chars[0]
            left = nums[0] % NUM_OPS
            right = nums[1] % NUM_OPS

            # CK result for this pair
            if op_char == '+':
                ck_result = self._bhml_compose(left, right)
            elif op_char == '-':
                ck_result = self._bhml_inverse(left, right)
            elif op_char == '*':
                ck_result = self._bhml_repeat(left, right)
            else:
                return  # Skip unknown ops for now

            offset = human_answer - ck_result
            key = (op_char, left, right)
            self.learned_offsets[key].append(offset)

            # Keep training log
            self.training_log.append({
                'expression': expression,
                'ck_result': ck_result,
                'human_result': human_answer,
                'offset': offset,
            })

    def predict_human(self, expression: str) -> int:
        """Predict the human answer using learned offsets.

        If CK has seen this (op, left, right) before, apply
        the most common offset. Otherwise return CK's raw answer.
        """
        tokens = self._tokenize(expression)
        nums = [v for t, v in tokens if t == 'num']
        op_chars = [v for t, v in tokens if t == 'op']

        if len(nums) < 2 or len(op_chars) < 1:
            result = self.evaluate(expression)
            return result.get('ck_result', 0)

        op_char = op_chars[0]
        left = nums[0] % NUM_OPS
        right = nums[1] % NUM_OPS

        # CK result
        if op_char == '+':
            ck_result = self._bhml_compose(left, right)
        elif op_char == '-':
            ck_result = self._bhml_inverse(left, right)
        elif op_char == '*':
            ck_result = self._bhml_repeat(left, right)
        elif op_char == '/':
            ck_result = self._bhml_inverse(left, right)
        else:
            ck_result = left

        # Look up learned offset
        key = (op_char, left, right)
        offsets = self.learned_offsets.get(key, [])
        if offsets:
            # Most common offset (mode)
            from collections import Counter
            offset = Counter(offsets).most_common(1)[0][0]
            return ck_result + offset

        return ck_result

    # ────────────────────────────────────────────────────────────
    #  PERSISTENCE
    # ────────────────────────────────────────────────────────────

    def save(self):
        """Persist learned offsets and training log.

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
                'learned_offsets': {
                    f"{k[0]}:{k[1]}:{k[2]}": v
                    for k, v in self.learned_offsets.items()
                },
                'training_count': len(self.training_log),
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
        """Load persisted offsets."""
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
                    print("  [MATH-TRANS] Loaded from backup")
                except Exception:
                    return
            else:
                return
        except Exception:
            return

        try:
            for key_str, offsets in data.get('learned_offsets', {}).items():
                parts = key_str.split(':')
                if len(parts) == 3:
                    key = (parts[0], int(parts[1]), int(parts[2]))
                    self.learned_offsets[key] = offsets
        except Exception:
            pass

    # ────────────────────────────────────────────────────────────
    #  SUMMARY
    # ────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        """Return summary stats for diagnostics."""
        return {
            'learned_offsets': len(self.learned_offsets),
            'training_examples': len(self.training_log),
        }
