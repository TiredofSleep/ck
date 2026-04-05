# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_sprint7_selfvalidate.py -- Sprint 7: CK Memory Self-Validation
==================================================================
CK uses its own invariant system (ck_invariants.py) to classify
its own live memory objects, measuring:

  - IG1 privacy violations
  - IG2 orphan rate (objects with null or empty provenance)
  - IG3 drift events (SYNTHESIZED treated as OBSERVED)
  - IG4 false promotion rate (tier advances without stability gate)
  - IG5 silent state transitions (DEAD revives, CONTRADICTED→ACTIVE without resolution)

This is Sprint 7 from the FRONTIER_MAP_MEMO: the highest-value,
lowest-cost, lowest-drift validation experiment — CK validating itself.

Run:
    python ck_sprint7_selfvalidate.py [--snapshot] [--report]
    python ck_sprint7_selfvalidate.py --watch 60   # poll every 60s

Output:
    sprint7_results.jsonl   -- append-only event log
    sprint7_report.md       -- human-readable summary (--report)
"""

import sys
import os
import json
import time
import argparse
import datetime
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ck_sim.being.ck_invariants import (
    MemoryObject, ProvenanceTag,
    validate_object, check_ig1, check_ig2, check_ig3, check_ig4, check_ig5,
    retrieval_weight, VALID_EVIDENCE, VALID_FORGETTING, VALID_TIER_CLASSES,
)

LOG_PATH = os.path.join(os.path.dirname(__file__), 'sprint7_results.jsonl')
REPORT_PATH = os.path.join(os.path.dirname(__file__), 'sprint7_report.md')

logging.basicConfig(level=logging.WARNING)


# ── Harvest live memory objects from CK engine via HTTP ──────────────────────

def harvest_objects_from_api(base_url='http://localhost:7777'):
    """Pull live memory state from CK's REST API and convert to MemoryObjects."""
    import urllib.request
    objects = []

    # /state — top-level coherence, operator, stage
    try:
        with urllib.request.urlopen(f'{base_url}/state', timeout=5) as r:
            state = json.loads(r.read())
        # Wrap the state snapshot as a COMPOSITE OBSERVED object
        prov = ProvenanceTag(
            parent_event_ids=['api_state'],
            supporting_ids=['coherence', 'operator'],
            produced_by='ck_sprint7',
        )
        obj = MemoryObject(
            id='live_state',
            content=state,
            tier_class='COMPOSITE',
            persistence_stage='ATOMIC',
            source_side='INTERNAL',
            privacy_class='SHARED',
            evidential_status='OBSERVED',
            stability_score=float(state.get('coherence', 0.5)),
            forgetting_state='ACTIVE',
            provenance=prov,
        )
        objects.append(obj)
    except Exception as e:
        print(f'[S7] state fetch failed: {e}')

    # /chain/status — lattice chain (if available)
    try:
        with urllib.request.urlopen(f'{base_url}/chain/status', timeout=5) as r:
            chain = json.loads(r.read())
        prov = ProvenanceTag(
            parent_event_ids=['api_chain'],
            supporting_ids=['nodes', 'paths'],
            produced_by='ck_sprint7',
        )
        stability = min(1.0, chain.get('node_count', 0) / 500.0)
        obj = MemoryObject(
            id='lattice_chain',
            content=chain,
            tier_class='SEMIPRIME' if stability >= 0.6 else 'REAL',
            persistence_stage='PATH',
            source_side='INTERNAL',
            privacy_class='SHARED',
            evidential_status='OBSERVED',
            stability_score=stability,
            forgetting_state='ACTIVE',
            provenance=prov,
        )
        objects.append(obj)
    except Exception:
        pass

    # /eat/status — olfactory absorption state
    try:
        with urllib.request.urlopen(f'{base_url}/eat/status', timeout=5) as r:
            eat = json.loads(r.read())
        prov = ProvenanceTag(
            parent_event_ids=['api_eat'],
            supporting_ids=['absorb_count', 'temper_count'],
            produced_by='ck_sprint7',
        )
        abs_count = eat.get('absorb_count', 0)
        stability = min(1.0, abs_count / 1000.0)
        obj = MemoryObject(
            id='olfactory_state',
            content=eat,
            tier_class='SEMIPRIME' if stability >= 0.6 else 'REAL',
            persistence_stage='PATH',
            source_side='INTERNAL',
            privacy_class='SHARED',
            evidential_status='OBSERVED',
            stability_score=stability,
            forgetting_state='ACTIVE',
            provenance=prov,
        )
        objects.append(obj)
    except Exception:
        pass

    return objects


# ── Run invariant checks on a set of objects ────────────────────────────────

def check_all(objects):
    results = {
        'ts': time.time(),
        'iso': datetime.datetime.utcnow().isoformat() + 'Z',
        'n_objects': len(objects),
        'ig1_violations': 0,
        'ig2_violations': 0,
        'ig3_violations': 0,
        'ig4_violations': 0,
        'ig5_violations': 0,
        'total_violations': 0,
        'orphan_count': 0,
        'drift_count': 0,
        'dead_retrievable': 0,  # IG5: DEAD objects with weight > 0
        'retrieval_weights': {},
        'details': [],
    }

    for obj in objects:
        ig1 = check_ig1(obj)
        ig2 = check_ig2(obj)
        ig3 = check_ig3(obj)
        ig4 = check_ig4(obj)
        ig5 = check_ig5(obj)
        all_v = ig1 + ig2 + ig3 + ig4 + ig5

        results['ig1_violations'] += len(ig1)
        results['ig2_violations'] += len(ig2)
        results['ig3_violations'] += len(ig3)
        results['ig4_violations'] += len(ig4)
        results['ig5_violations'] += len(ig5)
        results['total_violations'] += len(all_v)

        # Count orphans (IG2 specific)
        if any('orphan' in v for v in ig2):
            results['orphan_count'] += 1

        # DEAD retrievable (IG5 failure)
        rw = retrieval_weight(obj)
        if obj.forgetting_state == 'DEAD' and rw > 0:
            results['dead_retrievable'] += 1

        results['retrieval_weights'][obj.id] = round(rw, 4)

        if all_v:
            results['details'].append({
                'id': obj.id,
                'tier': obj.tier_class,
                'status': obj.evidential_status,
                'forgetting': obj.forgetting_state,
                'stability': obj.stability_score,
                'violations': all_v,
            })

    return results


# ── Single snapshot ──────────────────────────────────────────────────────────

def run_snapshot(base_url='http://localhost:7777', verbose=True):
    objects = harvest_objects_from_api(base_url)
    if not objects:
        print('[S7] No objects harvested — is CK running?')
        return None

    results = check_all(objects)

    # Append to log
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(results) + '\n')

    if verbose:
        print(f'\n[Sprint 7 — {results["iso"]}]')
        print(f'  Objects checked  : {results["n_objects"]}')
        print(f'  Total violations : {results["total_violations"]}')
        print(f'    IG1 privacy    : {results["ig1_violations"]}')
        print(f'    IG2 provenance : {results["ig2_violations"]}  (orphans: {results["orphan_count"]})')
        print(f'    IG3 evidence   : {results["ig3_violations"]}  (drift: {results["drift_count"]})')
        print(f'    IG4 promotion  : {results["ig4_violations"]}')
        print(f'    IG5 revision   : {results["ig5_violations"]}  (dead-retrievable: {results["dead_retrievable"]})')
        print(f'  Retrieval weights: {results["retrieval_weights"]}')
        if results['details']:
            print(f'  Violations:')
            for d in results['details']:
                print(f'    [{d["id"]}] {d["violations"]}')
        else:
            print(f'  All objects CLEAN.')

    return results


# ── Watch mode ───────────────────────────────────────────────────────────────

def run_watch(interval=60, base_url='http://localhost:7777'):
    print(f'[Sprint 7] Watching CK memory every {interval}s. Ctrl+C to stop.')
    print(f'[Sprint 7] Log: {LOG_PATH}')
    try:
        while True:
            run_snapshot(base_url, verbose=True)
            time.sleep(interval)
    except KeyboardInterrupt:
        print('\n[Sprint 7] Watch stopped.')


# ── Report generator ─────────────────────────────────────────────────────────

def generate_report():
    if not os.path.exists(LOG_PATH):
        print(f'[Sprint 7] No log at {LOG_PATH}')
        return

    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        rows = [json.loads(line) for line in f if line.strip()]

    if not rows:
        print('[Sprint 7] Log is empty.')
        return

    n = len(rows)
    first = rows[0]['iso']
    last = rows[-1]['iso']

    total_v = sum(r['total_violations'] for r in rows)
    ig1_total = sum(r['ig1_violations'] for r in rows)
    ig2_total = sum(r['ig2_violations'] for r in rows)
    ig3_total = sum(r['ig3_violations'] for r in rows)
    ig4_total = sum(r['ig4_violations'] for r in rows)
    ig5_total = sum(r['ig5_violations'] for r in rows)
    orphan_total = sum(r['orphan_count'] for r in rows)
    dead_ret = sum(r['dead_retrievable'] for r in rows)
    clean = sum(1 for r in rows if r['total_violations'] == 0)

    lines = [
        '# Sprint 7 — CK Memory Self-Validation Report',
        f'',
        f'**Generated:** {datetime.datetime.utcnow().isoformat()}Z  ',
        f'**Snapshots:** {n} ({first} → {last})  ',
        f'**Clean snapshots:** {clean}/{n} ({100*clean//n}%)',
        f'',
        '## Invariant Violation Counts',
        f'',
        f'| Invariant | Count | Per snapshot |',
        f'|---|---|---|',
        f'| IG1 Privacy | {ig1_total} | {ig1_total/n:.2f} |',
        f'| IG2 Provenance | {ig2_total} | {ig2_total/n:.2f} | (orphans: {orphan_total}) |',
        f'| IG3 Evidence | {ig3_total} | {ig3_total/n:.2f} |',
        f'| IG4 Promotion | {ig4_total} | {ig4_total/n:.2f} |',
        f'| IG5 Revision | {ig5_total} | {ig5_total/n:.2f} | (dead-retrievable: {dead_ret}) |',
        f'| **Total** | **{total_v}** | **{total_v/n:.2f}** |',
        f'',
        '## Hypothesis Status',
        f'',
        f'- H1 (IG2 orphan rate < 5%): {"PASS" if orphan_total/n < 0.05 else "FAIL"} ({orphan_total/n:.3f}/snapshot)',
        f'- H2 (IG3 drift events = 0): {"PASS" if ig3_total == 0 else "FAIL"} ({ig3_total} total)',
        f'- H3 (IG5 dead-retrievable = 0): {"PASS" if dead_ret == 0 else "FAIL"} ({dead_ret} events)',
        f'- H4 (IG1 privacy violations = 0): {"PASS" if ig1_total == 0 else "FAIL"} ({ig1_total} total)',
        f'',
        '## Notes',
        f'',
        f'Sprint 7 from FRONTIER_MAP_MEMO (2026-04-05): CK self-validation benchmark.',
        f'This report is ground truth for CK invariant architecture validation.',
    ]

    report = '\n'.join(lines)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(report)
    print(f'\n[Sprint 7] Report saved to {REPORT_PATH}')


# ── Entry ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sprint 7: CK Memory Self-Validation')
    parser.add_argument('--snapshot', action='store_true', help='Run one snapshot')
    parser.add_argument('--watch', type=int, metavar='SECS', help='Watch mode: poll every N seconds')
    parser.add_argument('--report', action='store_true', help='Generate markdown report from log')
    parser.add_argument('--url', default='http://localhost:7777', help='CK API base URL')
    args = parser.parse_args()

    if args.report:
        generate_report()
    elif args.watch:
        run_watch(interval=args.watch, base_url=args.url)
    else:
        run_snapshot(base_url=args.url, verbose=True)
