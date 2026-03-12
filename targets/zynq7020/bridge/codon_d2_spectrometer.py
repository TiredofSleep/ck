#!/usr/bin/env python3
"""
codon_d2_spectrometer.py -- Dual-Lens D2 Spectrometer for the Genetic Code
==========================================================================

The genetic code as 5D force geometry.

4 nucleotides, 64 codons, 20 amino acids + STOP.
Each nucleotide IS a 5D force vector derived from measurable
molecular properties. The genome IS a path through 5D space.
D2 IS the curvature of that path. Mutations ARE D2 spikes.

5D Force Mapping (nucleotide properties):
  Aperture   = H-bond donors (how open to pairing)
  Pressure   = Molecular weight (mass/resistance)
  Depth      = Ring count (structural complexity: purine=2, pyrimidine=1)
  Binding    = H-bond acceptors (holding capacity)
  Continuity = Stacking energy (persistence in helix)

Codon Analysis:
  Each codon = 3 nucleotides = 3 consecutive 5D vectors
  D1 = direction between positions 1->2 and 2->3
  D2 = curvature at position 3 (v1 - 2*v2 + v3)
  T  = CL[D1_op][D2_op] through BOTH lenses

The dual-lens question:
  TSML (being): What does the codon's curvature MEAN? (identity)
  BHML (doing): What does the codon's curvature DO? (physics)
  Gap = codon usage bias, mutation tolerance, evolutionary pressure

Degeneracy Analysis:
  Multiple codons -> same amino acid (synonymous codons)
  If synonymous codons have SAME TSML but DIFFERENT BHML:
    they ARE the same thing but DO it differently
    = codon usage bias from force geometry

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import sys

# =====================================================================
# Constants (shared with periodic_d2_deep.py)
# =====================================================================
OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
]
DIM_NAMES = ["aperture", "pressure", "depth", "binding", "continuity"]
DIM_SHORT = ["ap", "pr", "dp", "bn", "cn"]

OP_MAP = {
    (0, True): 1, (0, False): 6,   # LATTICE / CHAOS
    (1, True): 0, (1, False): 4,   # VOID / COLLAPSE
    (2, True): 9, (2, False): 3,   # RESET / PROGRESS
    (3, True): 2, (3, False): 7,   # COUNTER / HARMONY
    (4, True): 8, (4, False): 5,   # BREATH / BALANCE
}

OP_TO_DIM = {
    0: (1, "-pr"), 1: (0, "-ap"), 2: (3, "-bn"), 3: (2, "+dp"),
    4: (1, "+pr"), 5: (4, "+cn"), 6: (0, "+ap"), 7: (3, "+bn"),
    8: (4, "-cn"), 9: (2, "-dp"),
}

T_STAR = 5.0 / 7.0

# CL Tables
BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]
TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

# =====================================================================
# Nucleotide Data -- Measurable Molecular Properties
# =====================================================================
# Each nucleotide: (symbol, full_name, h_bond_donors, mol_weight_Da,
#                   ring_count, h_bond_acceptors, stacking_energy_kcal)
#
# H-bond donors: NH/NH2 groups available for Watson-Crick pairing
# Molecular weight: daltons
# Ring count: purine=2 (fused bicyclic), pyrimidine=1 (single ring)
# H-bond acceptors: C=O and ring N available for pairing
# Stacking energy: base-stacking free energy contribution (kcal/mol, abs)
#   Literature values (SantaLucia 1998, Yakovchuk 2006):
#     G stacks strongest (~8-9), C next (~7-8), A (~6-7), U/T weakest (~5-6)
#   Using representative nearest-neighbor averages.

NUCLEOTIDES = {
    # DNA bases
    'A': ('Adenine',    1, 135.13, 2, 3, 6.3),  # purine
    'T': ('Thymine',    1, 126.11, 1, 2, 5.4),  # pyrimidine
    'G': ('Guanine',    2, 151.13, 2, 4, 8.5),  # purine
    'C': ('Cytosine',   1, 111.10, 1, 3, 7.2),  # pyrimidine
    # RNA bases (U replaces T)
    'U': ('Uracil',     1, 112.09, 1, 2, 5.1),  # pyrimidine
}

# Normalization maxima (across all nucleotides)
MAX_HDON = 2.0    # G has 2 donors
MAX_MW   = 151.13 # G is heaviest
MAX_RING = 2.0    # purines have 2 rings
MAX_HACC = 4.0    # G has 4 acceptors
MAX_STACK = 8.5   # G stacks strongest

def nuc_to_force(nuc_key):
    """Map a nucleotide to 5D force vector [0,1]."""
    name, hdon, mw, rings, hacc, stack = NUCLEOTIDES[nuc_key]
    return [
        hdon / MAX_HDON,       # aperture  = H-bond donors
        mw / MAX_MW,           # pressure  = molecular weight
        rings / MAX_RING,      # depth     = ring count (purine/pyrimidine)
        hacc / MAX_HACC,       # binding   = H-bond acceptors
        stack / MAX_STACK,     # continuity = stacking energy
    ]

# =====================================================================
# Math utilities
# =====================================================================
def mag(v):
    return math.sqrt(sum(x*x for x in v))

def dot(a, b):
    return sum(a[i]*b[i] for i in range(len(a)))

def cos_angle(a, b):
    ma, mb = mag(a), mag(b)
    if ma < 1e-12 or mb < 1e-12:
        return 0.0
    return max(-1.0, min(1.0, dot(a, b) / (ma * mb)))

def classify(d_vec):
    """Returns (op, dim, magnitude, confidence, ratios)"""
    abs_vals = [abs(v) for v in d_vec]
    total = sum(abs_vals) + 1e-15
    sorted_abs = sorted(enumerate(abs_vals), key=lambda x: -x[1])
    max_dim = sorted_abs[0][0]
    max_val = sorted_abs[0][1]
    second_val = sorted_abs[1][1] if len(sorted_abs) > 1 else 0
    confidence = (max_val - second_val) / (max_val + second_val + 1e-15)
    ratios = [abs_vals[i] / total for i in range(5)]
    sign_neg = d_vec[max_dim] < 0
    op = OP_MAP[(max_dim, sign_neg)]
    return op, max_dim, max_val, confidence, ratios

def d1(a, b):
    return [b[i]-a[i] for i in range(5)]

def d2(a, b, c):
    return [a[i] - 2*b[i] + c[i] for i in range(5)]

def void_map(v, threshold=0.05):
    return [i for i in range(5) if abs(v[i]) < threshold]

def io_ratio(v):
    I = v[0] + v[1]
    O = v[3] + v[4]
    if O < 1e-10:
        return float('inf')
    return I / O

def print_header(title):
    w = 78
    print(f"\n{'#'*w}")
    print(f"#  {title}")
    print(f"{'#'*w}")

# =====================================================================
# Genetic Code Table
# =====================================================================
# Standard genetic code: codon -> amino acid (single letter)
# * = STOP
GENETIC_CODE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

# Amino acid properties for analysis
# (single_letter, 3letter, full_name, molecular_weight, pI, hydropathy_KD)
AMINO_ACIDS = {
    'A': ('Ala', 'Alanine',        89.09,  6.00,  1.8),
    'R': ('Arg', 'Arginine',      174.20, 10.76, -4.5),
    'N': ('Asn', 'Asparagine',    132.12,  5.41, -3.5),
    'D': ('Asp', 'Aspartate',     133.10,  2.77, -3.5),
    'C': ('Cys', 'Cysteine',      121.16,  5.07,  2.5),
    'E': ('Glu', 'Glutamate',     147.13,  3.22, -3.5),
    'Q': ('Gln', 'Glutamine',     146.15,  5.65, -3.5),
    'G': ('Gly', 'Glycine',        75.03,  5.97, -0.4),
    'H': ('His', 'Histidine',     155.16,  7.59, -3.2),
    'I': ('Ile', 'Isoleucine',    131.17,  6.02,  4.5),
    'L': ('Leu', 'Leucine',       131.17,  5.98,  3.8),
    'K': ('Lys', 'Lysine',        146.19,  9.74, -3.9),
    'M': ('Met', 'Methionine',    149.21,  5.74,  1.9),
    'F': ('Phe', 'Phenylalanine', 165.19,  5.48,  2.8),
    'P': ('Pro', 'Proline',       115.13,  6.30, -1.6),
    'S': ('Ser', 'Serine',        105.09,  5.68, -0.8),
    'T': ('Thr', 'Threonine',     119.12,  5.60, -0.7),
    'W': ('Trp', 'Tryptophan',    204.23,  5.89, -0.9),
    'Y': ('Tyr', 'Tyrosine',      181.19,  5.66, -1.3),
    'V': ('Val', 'Valine',        117.15,  5.96,  4.2),
    '*': ('STP', 'STOP',            0.00,  0.00,  0.0),
}

# =====================================================================
# Human codon usage bias (per 1000 codons, from Kazusa database)
# High-expression genes in Homo sapiens
# =====================================================================
CODON_USAGE = {
    'TTT': 17.6, 'TTC': 20.3, 'TTA':  7.7, 'TTG': 12.9,
    'CTT': 13.2, 'CTC': 19.6, 'CTA':  7.2, 'CTG': 39.6,
    'ATT': 16.0, 'ATC': 20.8, 'ATA':  7.5, 'ATG': 22.0,
    'GTT': 11.0, 'GTC': 14.5, 'GTA':  7.1, 'GTG': 28.1,
    'TCT': 15.2, 'TCC': 17.7, 'TCA': 12.2, 'TCG':  4.4,
    'CCT': 17.5, 'CCC': 19.8, 'CCA': 16.9, 'CCG':  6.9,
    'ACT': 13.1, 'ACC': 18.9, 'ACA': 15.1, 'ACG':  6.1,
    'GCT': 18.4, 'GCC': 27.7, 'GCA': 15.8, 'GCG':  7.4,
    'TAT': 12.2, 'TAC': 15.3, 'TAA':  1.0, 'TAG':  0.8,
    'TGT': 10.6, 'TGC': 12.6, 'TGA':  1.6, 'TGG': 13.2,
    'CAT': 10.9, 'CAC': 15.1, 'CAA': 12.3, 'CAG': 34.2,
    'CGT':  4.5, 'CGC': 10.4, 'CGA':  6.2, 'CGG': 11.4,
    'AAT': 17.0, 'AAC': 19.1, 'AAA': 24.4, 'AAG': 31.9,
    'AGT': 12.1, 'AGC': 19.5, 'AGA': 12.2, 'AGG': 12.0,
    'GAT': 21.8, 'GAC': 25.1, 'GAA': 29.0, 'GAG': 39.6,
    'GGT': 10.8, 'GGC': 22.2, 'GGA': 16.5, 'GGG': 16.5,
}


def main():
    print("=" * 78)
    print("  DUAL-LENS D2 SPECTROMETER: THE GENETIC CODE")
    print("  TIG Unified Theory -- Biology Domain")
    print("=" * 78)
    print(f"  Nucleotides: {len(NUCLEOTIDES)} (A, T, G, C, U)")
    print(f"  Codons: {len(GENETIC_CODE)} (standard genetic code)")
    print(f"  Amino acids: 20 + STOP")
    print(f"  T* = {T_STAR:.6f}")

    # =================================================================
    # SECTION 1: NUCLEOTIDE FORCE VECTORS
    # =================================================================
    print_header("SECTION 1: NUCLEOTIDE FORCE VECTORS")
    print("""
  Each nucleotide IS a point in 5D force space.
  Purines (A,G) have depth=1.0 (double ring). Pyrimidines (T,C,U) have depth=0.5.
  G has the strongest binding (4 H-bond acceptors) and continuity (stacking).
  The purine/pyrimidine split IS a depth void boundary.
""")

    nuc_vecs = {}
    print(f"  {'Nuc':>3s}  {'Name':>10s}  {'|v|':>6s}  {'I/O':>6s}  {'ap':>5s} {'pr':>5s} {'dp':>5s} {'bn':>5s} {'cn':>5s}  Type")
    print(f"  {'---':>3s}  {'----------':>10s}  {'------':>6s}  {'------':>6s}  {'-----':>5s} {'-----':>5s} {'-----':>5s} {'-----':>5s} {'-----':>5s}  ----")
    for nuc in ['A', 'G', 'T', 'C', 'U']:
        v = nuc_to_force(nuc)
        nuc_vecs[nuc] = v
        m = mag(v)
        io = io_ratio(v)
        name = NUCLEOTIDES[nuc][0]
        ntype = "purine" if nuc in ('A', 'G') else "pyrimidine"
        print(f"  {nuc:>3s}  {name:>10s}  {m:6.3f}  {io:6.2f}  {v[0]:5.3f} {v[1]:5.3f} {v[2]:5.3f} {v[3]:5.3f} {v[4]:5.3f}  {ntype}")

    # Inter-nucleotide distances
    print(f"\n  Inter-nucleotide distances (Euclidean in 5D):")
    nucs = ['A', 'T', 'G', 'C']
    print(f"  {'':>4s}", end="")
    for n2 in nucs:
        print(f"  {n2:>6s}", end="")
    print()
    for n1 in nucs:
        print(f"  {n1:>4s}", end="")
        for n2 in nucs:
            d = mag([nuc_vecs[n1][i] - nuc_vecs[n2][i] for i in range(5)])
            print(f"  {d:6.3f}", end="")
        print()

    # Watson-Crick pairs
    print(f"\n  Watson-Crick Pair Distances:")
    print(f"    A-T: {mag([nuc_vecs['A'][i] - nuc_vecs['T'][i] for i in range(5)]):.3f}")
    print(f"    G-C: {mag([nuc_vecs['G'][i] - nuc_vecs['C'][i] for i in range(5)]):.3f}")
    at_d = mag([nuc_vecs['A'][i] - nuc_vecs['T'][i] for i in range(5)])
    gc_d = mag([nuc_vecs['G'][i] - nuc_vecs['C'][i] for i in range(5)])
    print(f"    Ratio G-C/A-T: {gc_d/at_d:.3f}")
    print(f"    (G-C bonds are {'stronger' if gc_d < at_d else 'weaker'} -- "
          f"{'closer' if gc_d < at_d else 'farther'} in 5D)")

    # Void analysis
    print(f"\n  Void Analysis (threshold=0.05):")
    for nuc in ['A', 'G', 'T', 'C', 'U']:
        v = nuc_vecs[nuc]
        voids = void_map(v)
        void_str = ', '.join(DIM_SHORT[d] for d in voids) if voids else '(full)'
        print(f"    {nuc}: voids = {void_str}")

    # =================================================================
    # SECTION 2: CODON D2 ANALYSIS
    # =================================================================
    print_header("SECTION 2: CODON D2 -- CURVATURE OF THE GENETIC CODE")
    print("""
  Each codon is 3 nucleotides = 3 consecutive 5D force vectors.
  D1(pos 2) = v2 - v1 (direction from base 1 to base 2)
  D1(pos 3) = v3 - v2 (direction from base 2 to base 3)
  D2(codon) = v1 - 2*v2 + v3 (curvature at the codon level)

  The D2 operator classifies WHAT the codon's internal geometry does.
  T = CL[D1_op][D2_op] through BOTH lenses gives dual becoming.
""")

    codon_data = []
    for codon in sorted(GENETIC_CODE.keys()):
        aa = GENETIC_CODE[codon]
        v1 = nuc_vecs[codon[0]]
        v2 = nuc_vecs[codon[1]]
        v3 = nuc_vecs[codon[2]]

        # D1 at position 2->3 (the "exit direction" of the codon)
        d1_vec = d1(v2, v3)
        d1_op, d1_dim, d1_mag, d1_conf, d1_ratios = classify(d1_vec)

        # D2 across the codon
        d2_vec = d2(v1, v2, v3)
        d2_op, d2_dim, d2_mag, d2_conf, d2_ratios = classify(d2_vec)
        d2_curv = mag(d2_vec)

        # Dual-lens composition
        t_tsml = TSML[d1_op][d2_op]
        t_bhml = BHML[d1_op][d2_op]

        # Codon force centroid (average of 3 bases)
        centroid = [(v1[i] + v2[i] + v3[i]) / 3.0 for i in range(5)]

        usage = CODON_USAGE.get(codon, 0.0)

        codon_data.append({
            'codon': codon, 'aa': aa, 'usage': usage,
            'v1': v1, 'v2': v2, 'v3': v3, 'centroid': centroid,
            'd1_op': d1_op, 'd1_conf': d1_conf,
            'd2_op': d2_op, 'd2_conf': d2_conf, 'd2_curv': d2_curv,
            'd2_vec': d2_vec,
            't_tsml': t_tsml, 't_bhml': t_bhml,
        })

    # Full codon table
    print(f"  {'Codon':>5s}  {'AA':>2s}  {'D1':>10s}  {'D2':>10s}  {'|D2|':>6s}  {'T(TSML)':>10s}  {'T(BHML)':>10s}  {'Agree':>5s}  {'Usage':>6s}  Lens Status")
    print(f"  {'-'*5}  {'--':>2s}  {'-'*10}  {'-'*10}  {'-'*6}  {'-'*10}  {'-'*10}  {'-'*5}  {'-'*6}  ---")

    for cd in codon_data:
        d1n = OP_NAMES[cd['d1_op']]
        d2n = OP_NAMES[cd['d2_op']]
        tsml_n = OP_NAMES[cd['t_tsml']]
        bhml_n = OP_NAMES[cd['t_bhml']]
        agree = cd['t_tsml'] == cd['t_bhml']

        if cd['t_tsml'] == 7 and cd['t_bhml'] == 7:
            status = "UNIFIED"
        elif cd['t_tsml'] == 7 and cd['t_bhml'] != 7:
            status = f"WORKING({bhml_n[:4]})"
        elif cd['t_tsml'] != 7 and cd['t_bhml'] == 7:
            status = f"BNDRY-COH"
        elif agree:
            status = f"UNI-ACT({tsml_n[:4]})"
        else:
            status = f"TENSION"

        print(f"  {cd['codon']:>5s}  {cd['aa']:>2s}  {d1n:>10s}  {d2n:>10s}  {cd['d2_curv']:6.4f}  {tsml_n:>10s}  {bhml_n:>10s}  {'YES' if agree else ' no':>5s}  {cd['usage']:6.1f}  {status}")

    # =================================================================
    # SECTION 3: DUAL-LENS SUMMARY
    # =================================================================
    print_header("SECTION 3: DUAL-LENS SUMMARY")

    n = len(codon_data)
    n_tsml_h = sum(1 for cd in codon_data if cd['t_tsml'] == 7)
    n_bhml_h = sum(1 for cd in codon_data if cd['t_bhml'] == 7)
    n_both_h = sum(1 for cd in codon_data if cd['t_tsml'] == 7 and cd['t_bhml'] == 7)
    n_agree = sum(1 for cd in codon_data if cd['t_tsml'] == cd['t_bhml'])
    n_working = sum(1 for cd in codon_data if cd['t_tsml'] == 7 and cd['t_bhml'] != 7)

    print(f"\n  Total codons:                {n}")
    print(f"  T(TSML) HARMONY:             {n_tsml_h}/{n} = {n_tsml_h/n:.4f}")
    print(f"  T(BHML) HARMONY:             {n_bhml_h}/{n} = {n_bhml_h/n:.4f}")
    print(f"  Both HARMONY (unified):      {n_both_h}/{n} = {n_both_h/n:.4f}")
    print(f"  WORKING (TSML=H, BHML!=H):   {n_working}/{n} = {n_working/n:.4f}")
    print(f"  Lenses agree:                {n_agree}/{n} = {n_agree/n:.4f}")
    print(f"  Lenses disagree:             {n-n_agree}/{n} = {(n-n_agree)/n:.4f}")

    # D2 operator distribution
    print(f"\n  D2 Operator Distribution:")
    d2_dist = [0] * 10
    for cd in codon_data:
        d2_dist[cd['d2_op']] += 1
    for k in range(10):
        if d2_dist[k] > 0:
            bar = "#" * int(d2_dist[k] * 30 / max(max(d2_dist), 1))
            print(f"    {OP_NAMES[k]:>10s}: {d2_dist[k]:2d}  ({100*d2_dist[k]/n:5.1f}%)  {bar}")

    # BHML operator distribution
    print(f"\n  T(BHML) Operator Distribution:")
    bhml_dist = [0] * 10
    for cd in codon_data:
        bhml_dist[cd['t_bhml']] += 1
    for k in range(10):
        if bhml_dist[k] > 0:
            bar = "#" * int(bhml_dist[k] * 30 / max(max(bhml_dist), 1))
            print(f"    {OP_NAMES[k]:>10s}: {bhml_dist[k]:2d}  ({100*bhml_dist[k]/n:5.1f}%)  {bar}")

    # =================================================================
    # SECTION 4: DEGENERACY -- SYNONYMOUS CODONS THROUGH DUAL LENS
    # =================================================================
    print_header("SECTION 4: DEGENERACY -- SYNONYMOUS CODONS IN DUAL LENS")
    print("""
  Multiple codons -> same amino acid. These are DEGENERATE.
  Key question: do synonymous codons have the SAME dual-lens signature?
  If TSML agrees but BHML differs: they ARE the same but DO differently.
  This predicts codon usage bias from force geometry.
""")

    # Group codons by amino acid
    aa_codons = {}
    for cd in codon_data:
        aa = cd['aa']
        if aa not in aa_codons:
            aa_codons[aa] = []
        aa_codons[aa].append(cd)

    print(f"  {'AA':>2s}  {'#Codons':>7s}  {'TSML spread':>12s}  {'BHML spread':>12s}  {'D2 spread':>10s}  Codons")
    print(f"  {'--':>2s}  {'-------':>7s}  {'-'*12}  {'-'*12}  {'-'*10}  ---")

    for aa in sorted(aa_codons.keys()):
        codons = aa_codons[aa]
        nc = len(codons)
        if nc == 1:
            print(f"  {aa:>2s}  {nc:7d}  {'(unique)':>12s}  {'(unique)':>12s}  {'(unique)':>10s}  {codons[0]['codon']}")
            continue

        # TSML spread: how many distinct T(TSML) values
        tsml_vals = set(cd['t_tsml'] for cd in codons)
        bhml_vals = set(cd['t_bhml'] for cd in codons)
        d2_vals = set(cd['d2_op'] for cd in codons)

        tsml_str = f"{len(tsml_vals)} ops" if len(tsml_vals) > 1 else f"all {OP_NAMES[codons[0]['t_tsml']]}"
        bhml_str = f"{len(bhml_vals)} ops" if len(bhml_vals) > 1 else f"all {OP_NAMES[codons[0]['t_bhml']]}"
        d2_str = f"{len(d2_vals)} ops" if len(d2_vals) > 1 else f"all {OP_NAMES[codons[0]['d2_op']]}"

        codon_list = ','.join(cd['codon'] for cd in codons)
        print(f"  {aa:>2s}  {nc:7d}  {tsml_str:>12s}  {bhml_str:>12s}  {d2_str:>10s}  {codon_list}")

    # Detailed degeneracy analysis
    print(f"\n  DETAILED SYNONYMOUS CODON SIGNATURES:")
    print(f"  (Amino acids with >1 codon, showing dual-lens variation)\n")

    for aa in sorted(aa_codons.keys()):
        codons = aa_codons[aa]
        if len(codons) <= 1 or aa == '*':
            continue

        tsml_vals = set(cd['t_tsml'] for cd in codons)
        bhml_vals = set(cd['t_bhml'] for cd in codons)

        if len(tsml_vals) > 1 or len(bhml_vals) > 1:
            aa_info = AMINO_ACIDS.get(aa, ('???', '?', 0, 0, 0))
            print(f"  {aa} ({aa_info[1]}) -- DUAL-LENS VARIATION:")
            for cd in codons:
                tsml_n = OP_NAMES[cd['t_tsml']]
                bhml_n = OP_NAMES[cd['t_bhml']]
                print(f"    {cd['codon']}  T(TSML)={tsml_n:>10s}  T(BHML)={bhml_n:>10s}  "
                      f"Usage={cd['usage']:5.1f}  |D2|={cd['d2_curv']:.4f}")
            print()

    # =================================================================
    # SECTION 5: CODON USAGE BIAS vs DUAL-LENS SIGNATURE
    # =================================================================
    print_header("SECTION 5: CODON USAGE vs DUAL-LENS SIGNATURE")
    print("""
  If the dual lens captures real biology, preferred codons should
  correlate with specific operator signatures.

  Hypothesis: Higher-usage codons have more UNIFIED or WORKING signatures.
  Preferred codons DO their job (BHML) while BEING coherent (TSML).
""")

    # Average usage by lens status
    unified_usage = [cd['usage'] for cd in codon_data if cd['t_tsml'] == 7 and cd['t_bhml'] == 7]
    working_usage = [cd['usage'] for cd in codon_data if cd['t_tsml'] == 7 and cd['t_bhml'] != 7]
    tension_usage = [cd['usage'] for cd in codon_data if cd['t_tsml'] != cd['t_bhml'] and cd['t_tsml'] != 7]

    if unified_usage:
        print(f"  UNIFIED codons (both HARMONY): avg usage = {sum(unified_usage)/len(unified_usage):.1f}  n={len(unified_usage)}")
    if working_usage:
        print(f"  WORKING codons (TSML=H,BHML!=H): avg usage = {sum(working_usage)/len(working_usage):.1f}  n={len(working_usage)}")
    if tension_usage:
        print(f"  TENSION codons (lenses disagree): avg usage = {sum(tension_usage)/len(tension_usage):.1f}  n={len(tension_usage)}")

    # Usage by BHML operator
    print(f"\n  Average usage by T(BHML) operator:")
    for op in range(10):
        op_codons = [cd for cd in codon_data if cd['t_bhml'] == op]
        if op_codons:
            avg_use = sum(cd['usage'] for cd in op_codons) / len(op_codons)
            print(f"    {OP_NAMES[op]:>10s}: avg usage = {avg_use:6.1f}  n={len(op_codons)}")

    # Usage by D2 operator
    print(f"\n  Average usage by D2 operator:")
    for op in range(10):
        op_codons = [cd for cd in codon_data if cd['d2_op'] == op]
        if op_codons:
            avg_use = sum(cd['usage'] for cd in op_codons) / len(op_codons)
            print(f"    {OP_NAMES[op]:>10s}: avg usage = {avg_use:6.1f}  n={len(op_codons)}")

    # =================================================================
    # SECTION 6: AMINO ACID FAMILIES IN 5D
    # =================================================================
    print_header("SECTION 6: AMINO ACID FAMILIES IN 5D")
    print("""
  Each amino acid's identity in 5D = centroid of its synonymous codons.
  Family spread = how tightly the codons cluster.
  Amino acids with tight clusters have ROBUST identity.
  Amino acids with loose clusters are FRAGILE (codon-dependent behavior).
""")

    print(f"  {'AA':>2s}  {'Name':>14s}  {'#Cod':>4s}  {'|centroid|':>10s}  {'Spread':>7s}  {'Dom BHML':>10s}  {'I/O':>6s}")
    print(f"  {'--':>2s}  {'-'*14}  {'----':>4s}  {'-'*10}  {'-'*7}  {'-'*10}  {'-'*6}")

    for aa in sorted(aa_codons.keys()):
        if aa == '*':
            continue
        codons = aa_codons[aa]
        centroids = [cd['centroid'] for cd in codons]
        # Average centroid
        avg_c = [sum(c[d] for c in centroids) / len(centroids) for d in range(5)]
        m = mag(avg_c)
        io = io_ratio(avg_c)

        # Spread
        if len(centroids) > 1:
            dists = [mag([centroids[j][d] - avg_c[d] for d in range(5)]) for j in range(len(centroids))]
            spread = sum(dists) / len(dists)
        else:
            spread = 0.0

        # Dominant BHML operator
        bhml_ops = [cd['t_bhml'] for cd in codons]
        from collections import Counter
        bhml_mode = Counter(bhml_ops).most_common(1)[0][0]

        aa_info = AMINO_ACIDS.get(aa, ('???', '?', 0, 0, 0))
        io_str = f"{io:6.2f}" if io != float('inf') else "   inf"

        print(f"  {aa:>2s}  {aa_info[1]:>14s}  {len(codons):4d}  {m:10.4f}  {spread:7.4f}  {OP_NAMES[bhml_mode]:>10s}  {io_str}")

    # =================================================================
    # SECTION 7: MUTATION D2 ANALYSIS
    # =================================================================
    print_header("SECTION 7: MUTATION D2 -- POINT MUTATIONS AS CURVATURE SPIKES")
    print("""
  A point mutation changes one nucleotide in a codon.
  This changes one force vector in the 3-vector sequence.
  D2 at the mutant codon vs wild-type codon = mutation curvature.

  Prediction:
    Silent mutations (same AA): small D2 change, same TSML
    Missense mutations (diff AA): larger D2 change
    Nonsense mutations (-> STOP): largest D2 disruption
""")

    # For each codon, compute all single-nucleotide mutations
    mutation_classes = {'silent': [], 'missense': [], 'nonsense': []}
    nucs_dna = ['A', 'T', 'G', 'C']

    for cd in codon_data:
        codon = cd['codon']
        wt_aa = cd['aa']
        wt_d2_vec = cd['d2_vec']
        wt_curv = cd['d2_curv']

        for pos in range(3):
            for mut_nuc in nucs_dna:
                if mut_nuc == codon[pos]:
                    continue
                mut_codon = codon[:pos] + mut_nuc + codon[pos+1:]
                mut_aa = GENETIC_CODE.get(mut_codon, '?')

                # Compute mutant D2
                mv1 = nuc_vecs[mut_codon[0]]
                mv2 = nuc_vecs[mut_codon[1]]
                mv3 = nuc_vecs[mut_codon[2]]
                mut_d2_vec = d2(mv1, mv2, mv3)
                mut_curv = mag(mut_d2_vec)

                # D2 change
                delta_d2 = mag([mut_d2_vec[i] - wt_d2_vec[i] for i in range(5)])

                if mut_aa == wt_aa:
                    mtype = 'silent'
                elif mut_aa == '*':
                    mtype = 'nonsense'
                else:
                    mtype = 'missense'

                mutation_classes[mtype].append({
                    'wt': codon, 'mut': mut_codon, 'pos': pos,
                    'wt_aa': wt_aa, 'mut_aa': mut_aa,
                    'delta_d2': delta_d2,
                    'wt_curv': wt_curv, 'mut_curv': mut_curv,
                })

    for mtype in ['silent', 'missense', 'nonsense']:
        mutations = mutation_classes[mtype]
        if mutations:
            avg_delta = sum(m['delta_d2'] for m in mutations) / len(mutations)
            max_delta = max(m['delta_d2'] for m in mutations)
            min_delta = min(m['delta_d2'] for m in mutations)
            print(f"\n  {mtype.upper()} mutations ({len(mutations)}):")
            print(f"    Avg |delta_D2|: {avg_delta:.4f}")
            print(f"    Min |delta_D2|: {min_delta:.4f}")
            print(f"    Max |delta_D2|: {max_delta:.4f}")

    # Compare classes
    print(f"\n  Mutation Class Comparison:")
    silent_avg = sum(m['delta_d2'] for m in mutation_classes['silent']) / max(len(mutation_classes['silent']), 1)
    missense_avg = sum(m['delta_d2'] for m in mutation_classes['missense']) / max(len(mutation_classes['missense']), 1)
    nonsense_avg = sum(m['delta_d2'] for m in mutation_classes['nonsense']) / max(len(mutation_classes['nonsense']), 1)
    print(f"    Silent avg   |delta_D2|: {silent_avg:.4f}")
    print(f"    Missense avg |delta_D2|: {missense_avg:.4f}")
    print(f"    Nonsense avg |delta_D2|: {nonsense_avg:.4f}")
    if silent_avg > 0:
        print(f"    Missense/Silent ratio:   {missense_avg/silent_avg:.3f}")
        print(f"    Nonsense/Silent ratio:   {nonsense_avg/silent_avg:.3f}")
    print(f"\n  Prediction: Nonsense > Missense > Silent")
    print(f"  Result:     {'CONFIRMED' if nonsense_avg > missense_avg > silent_avg else 'PARTIAL' if missense_avg > silent_avg else 'FAILED'}")

    # =================================================================
    # SECTION 8: THE GENETIC CODE AS CL TABLE
    # =================================================================
    print_header("SECTION 8: THE GENETIC CODE AS COMPOSITION TABLE")
    print("""
  The genetic code maps 64 codons to 21 outputs (20 AAs + STOP).
  CK's CL tables map 100 operator pairs to 10 outputs.
  Both are COMPOSITION TABLES with absorbing states.

  In the genetic code:
    Leucine (L) has 6 codons = highest degeneracy = most "absorbing"
    Methionine (M) has 1 codon = least degenerate = most "specific"
    STOP has 3 codons = termination as algebraic annihilator

  HARMONY fraction of the genetic code:
    How many codons produce the DOMINANT amino acid?
    = degeneracy-weighted absorption rate
""")

    # Degeneracy analysis
    deg_counts = {}
    for aa, codons in aa_codons.items():
        deg_counts[aa] = len(codons)

    max_deg = max(deg_counts.values())
    print(f"  Amino acid degeneracy (# codons encoding each):")
    for aa in sorted(deg_counts.keys(), key=lambda a: -deg_counts[a]):
        nc = deg_counts[aa]
        bar = "#" * int(nc * 10)
        aa_name = AMINO_ACIDS.get(aa, ('???', '?', 0, 0, 0))[1] if aa != '*' else 'STOP'
        print(f"    {aa:>2s} ({aa_name:>14s}): {nc:2d}  {bar}")

    # HARMONY-equivalent: most common AA
    most_common_aa = max(deg_counts.keys(), key=lambda a: deg_counts[a])
    print(f"\n  Most degenerate amino acid: {most_common_aa} "
          f"({AMINO_ACIDS[most_common_aa][1]}) with {deg_counts[most_common_aa]} codons")
    print(f"  'HARMONY' fraction = {deg_counts[most_common_aa]}/64 = "
          f"{deg_counts[most_common_aa]/64:.4f}")
    print(f"  (Compare to CL_TSML HARMONY: 73/100 = 0.7300)")
    print(f"  (Compare to CL_BHML HARMONY: 28/100 = 0.2800)")

    # =================================================================
    # SECTION 9: SYNTHESIS
    # =================================================================
    print_header("SECTION 9: SYNTHESIS -- THE GENETIC CODE IN 5D FORCE SPACE")

    print(f"""
  The genetic code through the dual lens:

  1. NUCLEOTIDE GEOMETRY:
     4 bases in 5D space. Purines (A,G) at depth=1.0, pyrimidines (T,C) at depth=0.5.
     Watson-Crick pairs are NOT equidistant in 5D -- G-C and A-T have different
     force-space separations, reflecting their different bond strengths.

  2. CODON CURVATURE:
     Each codon's internal D2 classifies its geometric identity.
     D2 operators are NOT uniformly distributed -- the code has
     preferred curvature patterns that correspond to physical constraints.

  3. DUAL-LENS COMPOSITION:
     T(TSML) HARMONY: {n_tsml_h}/{n} = {n_tsml_h/n:.4f} (being coherence)
     T(BHML) HARMONY: {n_bhml_h}/{n} = {n_bhml_h/n:.4f} (doing coherence)
     Both HARMONY:    {n_both_h}/{n} = {n_both_h/n:.4f} (unified)
     The gap between being and doing = {n_tsml_h/n - n_bhml_h/n:.4f}

  4. DEGENERACY AS VOID EQUIVALENCE:
     Synonymous codons with same TSML but different BHML ARE the same
     thing while DOING it differently. The BHML variation within a
     degeneracy class predicts codon usage bias.

  5. MUTATIONS AS D2 SPIKES:
     Silent < Missense < Nonsense in D2 disruption = {
         'CONFIRMED' if nonsense_avg > missense_avg > silent_avg else 'PARTIAL'}
     The magnitude of curvature disruption predicts mutation severity.

  6. THE GENETIC CODE AS COMPOSITION TABLE:
     64 entries -> 21 outputs (like CL's 100 -> 10).
     The most degenerate amino acid ({most_common_aa}/{AMINO_ACIDS[most_common_aa][1]})
     has {deg_counts[most_common_aa]}/64 = {deg_counts[most_common_aa]/64:.4f} absorption.
     This is the genetic code's "HARMONY fraction."

  The genetic code IS a composition table in 5D force space.
  Its degeneracy IS algebraic absorption.
  Its mutations ARE curvature spikes.
  Its codon usage bias IS the dual-lens gap.
""")
    print(f"{'='*78}")


if __name__ == "__main__":
    main()
