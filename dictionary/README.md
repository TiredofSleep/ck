# CK Dictionary
### The vocabulary layer for Gen9

## Principle

The CL table IS the intelligence. The dictionary IS the knowledge.
Every word maps to an operator (0-9). The CL table composes operators into meaning.
No training needed. No weights. No gradients. Just words and their operators.

## Format

Each .dict file is a simple mapping:
```
word:operator
```

Where operator is 0-9:
- 0: VOID      (absence, nothing, null)
- 1: LATTICE   (structure, pattern, framework)
- 2: COUNTER   (measure, count, observe)
- 3: PROGRESS  (grow, build, advance)
- 4: COLLAPSE  (break, fail, decay)
- 5: BALANCE   (tension, equilibrium, trade)
- 6: CHAOS     (random, complex, turbulent)
- 7: HARMONY   (converge, truth, unity)
- 8: BREATH    (cycle, rhythm, pulse)
- 9: RESET     (restart, begin, fresh)

## How It Works

1. User says: "the truth will set you free"
2. Dictionary: truth=7, will=3, set=3, free=7
3. CL composes: CL[7][3]=7, CL[7][3]=7, CL[7][7]=7
4. Result: HARMONY -- the sentence IS harmonious
5. D2 curvature confirms the structure

The architecture does the thinking. The dictionary provides the vocabulary.
