"""V2: per-WP analysis - which branches have what versions, including paths"""
import re
import os
import json

cache_dir = r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\META_PLAN_2026-05-06\sweep_cache"

with open(os.path.join(cache_dir, "wp_extract_results.json"), "r") as f:
    data = json.load(f)

# Build per-WP -> {branch: [paths]}
wp_index = {}
for label, wps in data.items():
    if label.startswith('all_or_nothing') or label.startswith('crystal_') or \
       label == 'crystals' or label == 'dual_lattice' or label == 'tig_unified' or \
       label == 'time_for_help':
        continue
    for wp_str, paths in wps.items():
        wp_num = int(wp_str)
        wp_index.setdefault(wp_num, {})[label] = paths

# Print per-WP summary - sort by WP num and show count of branches it's in
print(f"=== WP-number distribution across branches (md/tex only) ===\n")
print(f"WP# | branches | tig-synthesis? | master? | sample-path")
print('-' * 100)
multi_version_wps = []
for wp in sorted(wp_index.keys()):
    branches = wp_index[wp]
    n_branches = len(branches)
    has_tig = 'ck_tig_synthesis' in branches
    has_master = 'ck_master' in branches
    sample_path = ""
    if has_tig:
        sample_path = branches['ck_tig_synthesis'][0]
    elif has_master:
        sample_path = branches['ck_master'][0]
    else:
        for k, v in branches.items():
            sample_path = v[0]; break
    print(f"WP{wp:<4} | {n_branches:<8} | {'YES' if has_tig else 'NO ':<14} | {'YES' if has_master else 'NO ':<7} | {sample_path[:80]}")

    # Multi-version detection
    unique_paths = set()
    for br, paths in branches.items():
        for p in paths:
            unique_paths.add(p)
    if len(unique_paths) > 1:
        multi_version_wps.append((wp, len(branches), len(unique_paths)))

print(f"\n=== WPs with multiple distinct paths across branches (potentially divergent) ===")
print(f"WP# | n-branches | n-distinct-paths")
for wp, nb, np_ in sorted(multi_version_wps, key=lambda x: -x[2])[:30]:
    print(f"WP{wp:<4} | {nb:<10} | {np_}")

# Get WP-numbers that exist ONLY in tig-synthesis (newest material)
tig_paths = data.get('ck_tig_synthesis', {})
tig_only_wps = []
for wp_str, paths in tig_paths.items():
    wp = int(wp_str)
    in_other = False
    for label, wps in data.items():
        if label == 'ck_tig_synthesis':
            continue
        if wp_str in wps:
            in_other = True
            break
    if not in_other:
        tig_only_wps.append(wp)

print(f"\n=== WPs ONLY in tig-synthesis (newest, not in any other ck branch) ===")
print(f"Count: {len(tig_only_wps)}")
print(sorted(tig_only_wps))

# Show WP116-127 details (these are the bridge dirac papers)
print("\n=== WP116-127 distribution ===")
for wp in sorted(wp_index.keys()):
    if 116 <= wp <= 127:
        branches = wp_index[wp]
        for br, paths in branches.items():
            for p in paths:
                print(f"WP{wp}: {br}: {p}")

# Count tex-only and md-only WPs
tex_wps = set()
md_wps = set()
for wp_str, paths in tig_paths.items():
    wp = int(wp_str)
    for p in paths:
        if p.lower().endswith('.tex'):
            tex_wps.add(wp)
        elif p.lower().endswith('.md'):
            md_wps.add(wp)
print(f"\n=== tig-synthesis: tex only WPs: {len(tex_wps - md_wps)}, md only: {len(md_wps - tex_wps)}, both: {len(md_wps & tex_wps)} ===")
print(f"Tex only: {sorted(tex_wps - md_wps)}")

with open(os.path.join(cache_dir, "wp_analysis_v2.json"), "w") as f:
    json.dump({
        'wp_index': {str(k): v for k, v in wp_index.items()},
        'tig_only_wps': sorted(tig_only_wps),
        'multi_version_wps': [{'wp': w, 'n_branches': nb, 'n_distinct_paths': np_} for w, nb, np_ in multi_version_wps],
    }, f, indent=2)
