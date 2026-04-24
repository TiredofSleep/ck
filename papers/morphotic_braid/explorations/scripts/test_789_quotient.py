<!-- PACKET: evening_handoff_2026_04_23/test_789_quotient.py -->
"""
Test: is the partition {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7,8,9} a
congruence of TSML?

If yes: TSML/~ is a well-defined 7-element quotient. Compare to Fano Steiner, octonion table, Vidinli.

If no: identify WHERE it fails — maybe a looser merging works.
"""
import numpy as np

TSML = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

# Your proposed partition: {7,8,9} are one class (call it "H"), others are singletons
CLASSES = [{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7, 8, 9}]
# Class labels: 0, 1, 2, 3, 4, 5, 6, H (call H = 7 for simplicity, since HARMONY is in the merged class)
elt_to_cls = {}
for ci, c in enumerate(CLASSES):
    for e in c: elt_to_cls[e] = ci  # cls 7 corresponds to {7,8,9}

# Check congruence: for each pair of classes (Ci, Cj), do all (a,b) with a in Ci, b in Cj give outputs in the same class?
print("="*75)
print("CONGRUENCE TEST for partition {0},{1},{2},{3},{4},{5},{6},{7,8,9}")
print("="*75)
print()

violations = []
for ci, class_i in enumerate(CLASSES):
    for cj, class_j in enumerate(CLASSES):
        output_classes = set()
        output_details = []
        for a in class_i:
            for b in class_j:
                out = TSML[a][b]
                out_cls = elt_to_cls[out]
                output_classes.add(out_cls)
                output_details.append((a, b, out, out_cls))
        if len(output_classes) > 1:
            violations.append({
                'classes': (ci, cj),
                'class_labels': (sorted(class_i), sorted(class_j)),
                'output_classes': sorted(output_classes),
                'details': output_details,
            })

if not violations:
    print("✓ CONGRUENCE HOLDS! The partition is valid, quotient is well-defined.")
else:
    print(f"✗ CONGRUENCE FAILS. {len(violations)} class-pairs have inconsistent outputs.")
    print()
    print("VIOLATIONS:")
    for v in violations:
        ci_label = f"{{{','.join(str(x) for x in v['class_labels'][0])}}}"
        cj_label = f"{{{','.join(str(x) for x in v['class_labels'][1])}}}"
        print(f"\n  Classes {ci_label} × {cj_label}:")
        print(f"    Output falls in classes: {v['output_classes']}")
        for (a, b, out, out_cls) in v['details']:
            cls_name = '{7,8,9}' if out_cls == 7 else str(out_cls)
            print(f"      TSML[{a}][{b}] = {out} → class {cls_name}")

# If violations exist, identify the pairs where merging fails
# Specifically: what does TSML do on {7,8,9}?
print()
print("="*75)
print("DETAILED: how does TSML treat {7, 8, 9}?")
print("="*75)
print()
print("TSML's row 7:", TSML[7])
print("TSML's row 8:", TSML[8])
print("TSML's row 9:", TSML[9])
print()
print("TSML's column 7:", [TSML[i][7] for i in range(10)])
print("TSML's column 8:", [TSML[i][8] for i in range(10)])
print("TSML's column 9:", [TSML[i][9] for i in range(10)])

# Specifically: is TSML[a][7] ~ TSML[a][8] ~ TSML[a][9] for each a?
print()
print("For each row a, do TSML[a][7], TSML[a][8], TSML[a][9] land in same class?")
for a in range(10):
    outs = [TSML[a][7], TSML[a][8], TSML[a][9]]
    classes = [elt_to_cls[o] for o in outs]
    same = len(set(classes)) == 1
    mark = "✓" if same else "✗"
    print(f"  {mark} a={a}: TSML[{a}][7,8,9] = {outs}, classes {classes}")

# Similar for rows
print()
print("For each column b, do TSML[7][b], TSML[8][b], TSML[9][b] land in same class?")
for b in range(10):
    outs = [TSML[7][b], TSML[8][b], TSML[9][b]]
    classes = [elt_to_cls[o] for o in outs]
    same = len(set(classes)) == 1
    mark = "✓" if same else "✗"
    print(f"  {mark} b={b}: TSML[7,8,9][{b}] = {outs}, classes {classes}")

