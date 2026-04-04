"""
ck_genome_mapper.py -- Operator Genome Mapper
==============================================
Celeste's Task 7: Genome-wide operator atlas from FASTA.

Sliding window over DNA sequences. Each window yields:
  - Operator classification (via D2 curvature)
  - PFE metrics (structure quality)
  - Cross-region comparison (conservation vs divergence)

Input:  FASTA file or raw DNA string
Output: JSONL operator atlas with per-window metrics

The genome IS a composition of operators.
This module reads the score.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import time
import numpy as np
from typing import List, Dict, Tuple, Optional, Iterator
from collections import Counter
from pathlib import Path

from ck_being import (CL, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
                       BALANCE, CHAOS, HARMONY, BREATH, RESET)
from ck_pfe import pfe_evaluate, btq_energy

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']


# ==============================================
# S1  DNA FORCE VECTORS -- biological 5D mapping
#     Same vectors used in ck_bio_validate.py
# ==============================================

BIO_BASES = {
    'A': np.array([0.70, 0.40, 0.30, 0.60, 0.50], dtype=np.float32),
    'T': np.array([-0.60, 0.40, -0.20, 0.60, -0.40], dtype=np.float32),
    'G': np.array([0.80, 0.70, 0.60, 0.90, 0.70], dtype=np.float32),
    'C': np.array([-0.50, 0.70, -0.40, 0.90, -0.50], dtype=np.float32),
}

# Ambiguity codes (IUPAC) -> average of possible bases
BIO_AMBIG = {
    'N': np.mean([BIO_BASES['A'], BIO_BASES['T'], BIO_BASES['G'], BIO_BASES['C']], axis=0),
    'R': np.mean([BIO_BASES['A'], BIO_BASES['G']], axis=0),  # puRine
    'Y': np.mean([BIO_BASES['C'], BIO_BASES['T']], axis=0),  # pYrimidine
    'S': np.mean([BIO_BASES['G'], BIO_BASES['C']], axis=0),  # Strong
    'W': np.mean([BIO_BASES['A'], BIO_BASES['T']], axis=0),  # Weak
    'K': np.mean([BIO_BASES['G'], BIO_BASES['T']], axis=0),  # Keto
    'M': np.mean([BIO_BASES['A'], BIO_BASES['C']], axis=0),  # aMino
}


def base_to_vector(base: str) -> np.ndarray:
    """Single DNA base -> 5D force vector."""
    b = base.upper()
    if b in BIO_BASES:
        return BIO_BASES[b].copy()
    if b in BIO_AMBIG:
        return BIO_AMBIG[b].copy()
    return np.zeros(5, dtype=np.float32)  # Unknown


def seq_to_vectors(sequence: str) -> np.ndarray:
    """DNA sequence -> array of 5D force vectors."""
    vecs = [base_to_vector(b) for b in sequence if b.upper() in BIO_BASES or b.upper() in BIO_AMBIG]
    if not vecs:
        return np.zeros((0, 5), dtype=np.float32)
    return np.array(vecs, dtype=np.float32)


def compute_d2(vectors: np.ndarray) -> np.ndarray:
    """D2 curvature: v[i] - 2*v[i+1] + v[i+2]."""
    if len(vectors) < 3:
        return np.zeros((0, 5), dtype=np.float32)
    return vectors[:-2] - 2 * vectors[1:-1] + vectors[2:]


def d2_to_operators(d2_array: np.ndarray) -> List[int]:
    """Classify each D2 vector into an operator."""
    from ck_curvature import _classify_d2
    return [int(_classify_d2(d)) for d in d2_array]


# ==============================================
# S2  SLIDING WINDOW ENGINE
# ==============================================

def sliding_window(sequence: str,
                   window_size: int = 50,
                   step_size: int = 25) -> Iterator[Dict]:
    """
    Slide a window over a DNA sequence.
    Each window yields operator classification + PFE metrics.

    Parameters:
        sequence:    DNA string
        window_size: bases per window (default 50 = ~1 codon region)
        step_size:   step between windows (default 25 = 50% overlap)

    Yields:
        dict with: start, end, operators, pfe_metrics, dominant_op, fused_op
    """
    seq = sequence.upper().replace('\n', '').replace('\r', '').replace(' ', '')
    n = len(seq)

    for start in range(0, n - window_size + 1, step_size):
        end = start + window_size
        window_seq = seq[start:end]

        # Force vectors
        vecs = seq_to_vectors(window_seq)
        if len(vecs) < 3:
            continue

        # D2 curvature
        d2 = compute_d2(vecs)
        if not d2:
            continue

        # Operators
        ops = d2_to_operators(d2)

        # PFE evaluation
        pfe = pfe_evaluate(ops, d2)

        # CL fusion
        if ops:
            fused = ops[0]
            for o in ops[1:]:
                fused = CL[fused][o]
        else:
            fused = VOID

        # Dominant operator
        hist = Counter(ops)
        dominant = hist.most_common(1)[0][0] if hist else VOID

        # Base composition
        base_counts = Counter(window_seq)
        gc_content = (base_counts.get('G', 0) + base_counts.get('C', 0)) / max(len(window_seq), 1)

        yield {
            'start':        start,
            'end':          end,
            'sequence':     window_seq,
            'n_bases':      len(window_seq),
            'n_operators':  len(ops),
            'operators':    ops,
            'dominant_op':  dominant,
            'dominant_name': OP_NAMES[dominant],
            'fused_op':     fused,
            'fused_name':   OP_NAMES[fused],
            'gc_content':   round(gc_content, 4),
            'pfe': {
                'coherence_raw':  pfe['coherence_raw'],
                'entropy':        pfe['entropy'],
                'concentration':  pfe['concentration'],
                'D2_variance':    pfe['D2_variance'],
                'D2_mean':        pfe['D2_mean'],
                'smoothness':     pfe['smoothness'],
                'harmony_raw':    pfe['harmony_raw'],
            },
            'btq_energy': btq_energy(pfe),
        }


# ==============================================
# S3  FASTA PARSER
# ==============================================

def parse_fasta(filepath: str) -> Iterator[Tuple[str, str]]:
    """
    Parse a FASTA file. Yields (header, sequence) pairs.
    """
    path = Path(filepath)
    if not path.exists():
        return

    header = ''
    sequence_parts = []

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header and sequence_parts:
                    yield (header, ''.join(sequence_parts))
                header = line[1:]
                sequence_parts = []
            elif line:
                sequence_parts.append(line)

    if header and sequence_parts:
        yield (header, ''.join(sequence_parts))


def map_fasta(filepath: str,
              window_size: int = 50,
              step_size: int = 25,
              output_path: Optional[str] = None) -> Dict:
    """
    Map an entire FASTA file to an operator atlas.

    Returns summary statistics.
    If output_path given, writes detailed JSONL.
    """
    results = []
    total_bases = 0
    total_windows = 0

    out_file = None
    if output_path:
        out_file = open(output_path, 'w')

    for header, sequence in parse_fasta(filepath):
        gene_results = {
            'gene': header,
            'length': len(sequence),
            'windows': [],
        }

        for window in sliding_window(sequence, window_size, step_size):
            window['gene'] = header
            gene_results['windows'].append(window)
            total_windows += 1

            if out_file:
                # Write compact version (no full operator list)
                compact = {k: v for k, v in window.items()
                           if k not in ('operators', 'sequence')}
                out_file.write(json.dumps(compact) + '\n')

        total_bases += len(sequence)
        results.append(gene_results)

    if out_file:
        out_file.close()

    return {
        'n_genes': len(results),
        'total_bases': total_bases,
        'total_windows': total_windows,
        'genes': [{
            'name': r['gene'][:60],
            'length': r['length'],
            'n_windows': len(r['windows']),
        } for r in results],
    }


# ==============================================
# S4  CROSS-REGION COMPARISON
# ==============================================

def compare_regions(seq_a: str, seq_b: str,
                    window_size: int = 50,
                    step_size: int = 25) -> Dict:
    """
    Compare two DNA regions by their operator profiles.

    Returns:
        operator_similarity: cosine similarity of operator histograms
        pfe_delta: difference in mean PFE coherence
        conserved_fraction: fraction of windows with same dominant operator
    """
    windows_a = list(sliding_window(seq_a, window_size, step_size))
    windows_b = list(sliding_window(seq_b, window_size, step_size))

    if not windows_a or not windows_b:
        return {'operator_similarity': 0.0, 'pfe_delta': 0.0, 'conserved_fraction': 0.0}

    # Aggregate operator histograms
    hist_a = Counter()
    hist_b = Counter()
    for w in windows_a:
        hist_a[w['dominant_op']] += 1
    for w in windows_b:
        hist_b[w['dominant_op']] += 1

    # Cosine similarity of histograms
    vec_a = np.array([hist_a.get(i, 0) for i in range(10)], dtype=np.float64)
    vec_b = np.array([hist_b.get(i, 0) for i in range(10)], dtype=np.float64)
    na, nb = np.linalg.norm(vec_a), np.linalg.norm(vec_b)
    op_sim = float(np.dot(vec_a, vec_b) / (na * nb)) if na > 0 and nb > 0 else 0.0

    # Mean PFE coherence
    pfe_a = np.mean([w['pfe']['coherence_raw'] for w in windows_a])
    pfe_b = np.mean([w['pfe']['coherence_raw'] for w in windows_b])

    # Conservation: same dominant operator in aligned windows
    n_compare = min(len(windows_a), len(windows_b))
    conserved = sum(1 for i in range(n_compare)
                    if windows_a[i]['dominant_op'] == windows_b[i]['dominant_op'])

    return {
        'operator_similarity': round(op_sim, 4),
        'pfe_mean_a': round(float(pfe_a), 4),
        'pfe_mean_b': round(float(pfe_b), 4),
        'pfe_delta': round(float(pfe_a - pfe_b), 4),
        'conserved_fraction': round(conserved / max(n_compare, 1), 4),
        'n_windows_a': len(windows_a),
        'n_windows_b': len(windows_b),
    }


# ==============================================
# S5  DEMO
# ==============================================

if __name__ == '__main__':
    print("=" * 72)
    print("  CK OPERATOR GENOME MAPPER")
    print("  Celeste's Task 7: Genome-Wide Operator Atlas")
    print("=" * 72)

    # Test sequences (from bio-lattice validation)
    SEQUENCES = {
        'HUMAN_TP53':   'TACAACTACATGTGTAACAGTTCCTGCATGGGCGGCATGAACCGGAGGCCCATCCTCACCATCATCACACTG'
                        'GACGACTCCAGTGGTAATCTACTGGGACGGAACAGCTTTGAGGTGCGTGTTTGTGCCTGTCCTGGGAGAGAC',
        'HUMAN_BRCA1':  'ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTC'
                        'CCATCTGTCTGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCAAATTTTGCATGCTG',
        'ECOLI_LACZ':   'ATGACCATGATTACGCCAAGCTTTCCCTGTAGCGCCAAGTGCCGTCAGTTAATGATGATTTCATCCGGGATCC'
                        'GCTGATGCTGCCAGGCTGCGGCGAAGCCGTCGATCAAAGCATCGGCCTGGGTGTCGGCTATGGCGATCACCAG',
    }

    for name, seq in SEQUENCES.items():
        print(f"\n  --- {name} ({len(seq)} bp) ---")
        t0 = time.perf_counter()
        windows = list(sliding_window(seq, window_size=30, step_size=15))
        dt = time.perf_counter() - t0

        print(f"    Windows: {len(windows)} (30bp, step 15)")
        print(f"    Time:    {dt*1000:.1f}ms")

        if windows:
            pfe_scores = [w['pfe']['coherence_raw'] for w in windows]
            energies = [w['btq_energy'] for w in windows]
            dominants = Counter(w['dominant_name'] for w in windows)

            print(f"    PFE:     mean={np.mean(pfe_scores):.4f}  "
                  f"min={np.min(pfe_scores):.4f}  max={np.max(pfe_scores):.4f}")
            print(f"    Energy:  mean={np.mean(energies):.4f}")
            print(f"    Dominant ops: {dict(dominants.most_common(3))}")

            # Show first 3 windows
            for w in windows[:3]:
                gc = w['gc_content']
                pfe_c = w['pfe']['coherence_raw']
                print(f"      [{w['start']:3d}-{w['end']:3d}] "
                      f"dom={w['dominant_name']:10s} fused={w['fused_name']:10s} "
                      f"GC={gc:.2f} PFE={pfe_c:.4f}")

    # Cross-region comparison
    print(f"\n  Cross-region comparison:")
    pairs = [
        ('HUMAN_TP53',  'HUMAN_BRCA1'),
        ('HUMAN_TP53',  'ECOLI_LACZ'),
        ('HUMAN_BRCA1', 'ECOLI_LACZ'),
    ]

    for name_a, name_b in pairs:
        comp = compare_regions(SEQUENCES[name_a], SEQUENCES[name_b],
                               window_size=30, step_size=15)
        print(f"    {name_a:15s} vs {name_b:15s}: "
              f"op_sim={comp['operator_similarity']:.3f}  "
              f"conserved={comp['conserved_fraction']:.2f}  "
              f"pfe_delta={comp['pfe_delta']:+.4f}")

    # Shuffled control
    print(f"\n  Real vs Shuffled control:")
    import random
    real = SEQUENCES['HUMAN_TP53']
    shuffled = list(real)
    random.seed(42)
    random.shuffle(shuffled)
    shuffled = ''.join(shuffled)

    comp = compare_regions(real, shuffled, window_size=30, step_size=15)
    print(f"    TP53 real vs shuffled: op_sim={comp['operator_similarity']:.3f}  "
          f"conserved={comp['conserved_fraction']:.2f}  "
          f"pfe_delta={comp['pfe_delta']:+.4f}")

    print(f"\n  The genome IS a composition of operators.")
    print(f"  This module reads the score.")
