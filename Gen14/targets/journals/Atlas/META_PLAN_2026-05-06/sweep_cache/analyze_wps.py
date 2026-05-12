"""Analysis script: per-branch unique WPs, deltas vs local inventory, branch-specific WPs"""
import re
import os
import glob
import json

cache_dir = r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\META_PLAN_2026-05-06\sweep_cache"

with open(os.path.join(cache_dir, "wp_extract_results.json"), "r") as f:
    data = json.load(f)

# Local inventory WPs
LOCAL_WPS = set([1, 9, 10, 11, 12, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
                 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115,
                 116, 117, 118, 119, 120, 121, 122, 123, 124, 127])

print(f"Local inventory has {len(LOCAL_WPS)} unique WPs")

# Per-branch summary
per_branch_wps = {}
for label, wps in data.items():
    nums = sorted([int(k) for k in wps.keys()])
    per_branch_wps[label] = set(nums)

# Sets per branch
print("\n=== Branch WP sets ===")
for label in sorted(per_branch_wps.keys()):
    nums = per_branch_wps[label]
    print(f"  {label}: {len(nums)} (max={max(nums) if nums else 'n/a'})")

# Combined union
all_remote = set()
for label, nums in per_branch_wps.items():
    all_remote.update(nums)
print(f"\nUnion of all remote WPs (md/tex): {len(all_remote)}")

# Delta: in remote not in local
remote_minus_local = sorted(all_remote - LOCAL_WPS)
print(f"\nWPs in REMOTE but NOT in LOCAL: {len(remote_minus_local)}")
print(remote_minus_local)

# Delta: in local not in remote
local_minus_remote = sorted(LOCAL_WPS - all_remote)
print(f"\nWPs in LOCAL but NOT in REMOTE: {len(local_minus_remote)}")
print(local_minus_remote)

# Branch contribution: for each branch, what unique WPs does it contribute?
print("\n=== Branches that have WPs not present in tig-synthesis ===")
tig_set = per_branch_wps.get('ck_tig_synthesis', set())
print(f"  tig-synthesis has: {len(tig_set)} WPs, max={max(tig_set)}")
for label in sorted(per_branch_wps.keys()):
    nums = per_branch_wps[label]
    extra = nums - tig_set
    if extra:
        print(f"  {label} has {len(extra)} extra WPs not in tig-synthesis: {sorted(extra)}")

# Highest-WP per branch
print("\n=== Highest WP per branch (md/tex) ===")
for label in sorted(per_branch_wps.keys()):
    nums = per_branch_wps[label]
    if nums:
        print(f"  {label}: max WP = {max(nums)}")

# Find canonical branch for each WP
print("\n=== Per-WP canonical branch ===")
wp_branches = {}
for label, nums in per_branch_wps.items():
    for n in nums:
        wp_branches.setdefault(n, []).append(label)
for wp in sorted(wp_branches.keys()):
    branches = wp_branches[wp]
    if 'ck_tig_synthesis' in branches:
        canonical = 'tig-synthesis'
    elif 'ck_master' in branches:
        canonical = 'master'
    else:
        canonical = branches[0]

# Find WPs that appear only in branches OTHER than tig-synthesis
print("\n=== WPs that exist in some branch but NOT tig-synthesis ===")
unique_to_other = set()
for wp, brs in wp_branches.items():
    if 'ck_tig_synthesis' not in brs:
        unique_to_other.add(wp)
        print(f"  WP{wp}: only in branches: {brs}")
print(f"\nTotal: {len(unique_to_other)}")

# Save analysis
analysis = {
    'local_wps': sorted(LOCAL_WPS),
    'all_remote_wps': sorted(all_remote),
    'remote_minus_local': remote_minus_local,
    'local_minus_remote': local_minus_remote,
    'per_branch_wp_sets': {k: sorted(v) for k, v in per_branch_wps.items()},
    'wp_branch_index': {str(k): v for k, v in wp_branches.items()},
}
with open(os.path.join(cache_dir, "wp_analysis.json"), "w") as f:
    json.dump(analysis, f, indent=2)
print("\nSaved to wp_analysis.json")
