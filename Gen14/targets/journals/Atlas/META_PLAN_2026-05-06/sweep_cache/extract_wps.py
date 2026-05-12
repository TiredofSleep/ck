import re
import os
import glob
import json

cache_dir = r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\META_PLAN_2026-05-06\sweep_cache"
WP_RE = re.compile(r'WP[_-]?(\d+)', re.IGNORECASE)

def extract_wp_numbers_from_file(path):
    """Return dict {wp_num: [list of full paths matching that WP]}"""
    results = {}
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            low = line.lower()
            if not (low.endswith('.md') or low.endswith('.tex')):
                continue
            basename = os.path.basename(line)
            m = WP_RE.search(basename)
            if m:
                num = int(m.group(1))
                results.setdefault(num, []).append(line)
    return results

all_branches = {}
for tree_file in sorted(glob.glob(os.path.join(cache_dir, "tree_*.txt"))):
    label = os.path.basename(tree_file).replace("tree_", "").replace(".txt", "")
    all_branches[label] = extract_wp_numbers_from_file(tree_file)

print("=== Per-branch WP-number sets (md/tex only) ===\n")
all_wp_nums = set()
for label, wps in all_branches.items():
    nums = sorted(wps.keys())
    all_wp_nums.update(nums)
    print(f"{label}: {len(nums)} unique WP-numbers")
    if 0 < len(nums) < 80:
        print(f"  -> {nums}")

print(f"\n=== Universe of all WP-numbers across all branches/repos: {len(all_wp_nums)} ===")
print(sorted(all_wp_nums))

with open(os.path.join(cache_dir, "wp_extract_results.json"), "w") as f:
    json.dump({label: {str(k): v for k, v in wps.items()} for label, wps in all_branches.items()}, f, indent=2)
print("\nSaved to wp_extract_results.json")
