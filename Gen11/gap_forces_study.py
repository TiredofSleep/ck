"""
gap_forces_study.py — 5D Force Recursion Inside the Ternary Bridge Zone [1/2, 5/7)
CK Coherence Framework — Gen11 Mathematical Research
T* = 5/7, Bridge = [1/2, 5/7)
"""

import json
import math
import sys

ZEROS_PATH = r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen11\riemann_zeros_5000.json"

# ── Constants ────────────────────────────────────────────────────────────────
T_STAR   = 5 / 7          # coherence threshold
BRIDGE_LO = 0.5           # bridge lower bound
BRIDGE_HI = T_STAR        # bridge upper bound = 5/7
BRIDGE_WIDTH = BRIDGE_HI - BRIDGE_LO   # 3/14 ≈ 0.214285...
HARMONY  = 7

# ── Load Riemann zeros ───────────────────────────────────────────────────────
with open(ZEROS_PATH, "r") as f:
    raw = json.load(f)

# Accept list-of-numbers or list-of-dicts with 'gamma' key
if isinstance(raw[0], (int, float)):
    gammas = [float(x) for x in raw]
elif isinstance(raw[0], dict):
    # try common key names
    for key in ("gamma", "im", "imaginary", "t", "zero"):
        if key in raw[0]:
            gammas = [float(r[key]) for r in raw]
            break
    else:
        raise ValueError(f"Unknown dict keys: {list(raw[0].keys())}")
else:
    raise ValueError(f"Unknown data format: type={type(raw[0])}")

print(f"Loaded {len(gammas)} Riemann zeros.")
print(f"First 10 gamma_k: {[round(g, 6) for g in gammas[:10]]}")
print()

# ── Core formula ─────────────────────────────────────────────────────────────
def theta(gamma):
    """θ_k = π - 2·arctan(2·γ_k)"""
    return math.pi - 2 * math.atan(2 * gamma)

def lambda_n(n, K):
    """λ_n(K) = 2·Σ_{k=1}^{K} (1 - cos(n·θ_k))"""
    total = 0.0
    for k in range(1, K + 1):
        gk = gammas[k - 1]
        thk = theta(gk)
        total += 1 - math.cos(n * thk)
    return 2.0 * total

def lambda_increment(n, K):
    """Δλ_n(K) = λ_n(K) - λ_n(K-1) = 2·(1 - cos(n·θ_K))"""
    gk = gammas[K - 1]
    thk = theta(gk)
    return 2.0 * (1 - math.cos(n * thk))

def bridge_pct(lam):
    """How far through the bridge [1/2, 5/7) is lam?"""
    return (lam - BRIDGE_LO) / BRIDGE_WIDTH * 100.0

def direction_label(cos_val):
    return "cooperative" if cos_val < 0 else "opposing"

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: n=7, K=1..20
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 78)
print("SECTION 1 — n=7 (GENERATOR BRIDGE), λ_7(K) for K=1..20")
print("=" * 78)
print(f"{'K':>4}  {'λ_7(K)':>14}  {'Δλ':>14}  {'State':>12}")
print("-" * 50)

K_enter_7 = None
K_exit_7  = None
lam7_prev = 0.0
lam7_vals = {}

for K in range(1, 21):
    lam = lambda_n(7, K)
    delta = lam - lam7_prev
    if lam < BRIDGE_LO:
        state = "FLOW(0)"
    elif lam < BRIDGE_HI:
        state = "BRIDGE"
        if K_enter_7 is None:
            K_enter_7 = K
    else:
        state = "STRUCTURE"
        if K_exit_7 is None:
            K_exit_7 = K
    lam7_vals[K] = lam
    print(f"  {K:>2}  {lam:>14.8f}  {delta:>14.8f}  {state:>12}")
    lam7_prev = lam

print()
print(f"  K_enter(7) = {K_enter_7}  (first K where λ_7 ≥ 1/2)")
print(f"  K_exit(7)  = {K_exit_7}  (first K where λ_7 ≥ 5/7) = K*(7)")
print(f"  Bridge width in zeros = K_exit - K_enter = {K_exit_7 - K_enter_7}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: n=7 BRIDGE DETAIL — force delta per zero
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 78)
print("SECTION 2 — n=7 INSIDE BRIDGE [K_enter..K_exit-1], FORCE PER ZERO")
print("=" * 78)
print(f"Bridge zone: K={K_enter_7} to K={K_exit_7 - 1} (inclusive)")
print(f"Bridge width (force): {BRIDGE_WIDTH:.10f}  (= 3/14 = {3}/{14})")
print()
print(f"{'K':>4}  {'λ_7(K)':>14}  {'Δforce':>14}  {'Bridge%':>9}  {'cos(7θ_k)':>12}  Direction")
print("-" * 78)

max_delta_K = None
max_delta_val = -1e9
for K in range(K_enter_7, K_exit_7):
    lam  = lam7_vals[K]
    lam_prev = lam7_vals.get(K-1, 0.0)
    delta = lam - lam_prev
    bpct  = bridge_pct(lam)
    gk    = gammas[K - 1]
    thk   = theta(gk)
    cosval = math.cos(7 * thk)
    direc  = direction_label(cosval)
    print(f"  {K:>2}  {lam:>14.8f}  {delta:>14.8f}  {bpct:>8.3f}%  {cosval:>12.8f}  {direc}")
    if delta > max_delta_val:
        max_delta_val = delta
        max_delta_K   = K

print()
print(f"  Max force delta inside bridge: K={max_delta_K}, Δλ={max_delta_val:.8f}")
print(f"  Zero with max force: γ_{max_delta_K} = {gammas[max_delta_K-1]:.6f}")
bridge_zeros = K_exit_7 - K_enter_7
print(f"  Zeros inside bridge (K_enter to K_exit-1): {bridge_zeros}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: n=5 (ETERNAL FLOW / CREATE)
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 78)
print("SECTION 3 — n=5 (ETERNAL FLOW / CREATE), K=1..150")
print("=" * 78)

K_enter_5 = None
lam5_prev = 0.0
lam5_vals = {}
for K in range(1, 151):
    lam = lambda_n(5, K)
    if lam >= BRIDGE_LO and K_enter_5 is None:
        K_enter_5 = K
    lam5_vals[K] = lam
    lam5_prev = lam

print(f"  K_enter(5) = {K_enter_5}  (first K where λ_5 ≥ 1/2)")
print(f"  λ_5 at K_enter: {lam5_vals[K_enter_5]:.10f}")
print()

# Does n=5 ever reach 5/7?
max_lam5  = max(lam5_vals.values())
max_lam5_K = max(lam5_vals, key=lam5_vals.get)
print(f"  Max λ_5 in K=1..150: {max_lam5:.10f} at K={max_lam5_K}")
print(f"  Does λ_5 ever reach 5/7 ({T_STAR:.10f})? {'YES' if max_lam5 >= T_STAR else 'NO'}")
print()

# n=5 around K_enter (show K_enter-5 to K_enter+30)
K_lo5 = max(1, K_enter_5 - 5)
K_hi5 = min(150, K_enter_5 + 30)
print(f"  n=5 detail: K={K_lo5}..{K_hi5}")
print(f"  {'K':>4}  {'λ_5(K)':>14}  {'Δforce':>14}  {'Bridge%':>10}  State")
print("  " + "-" * 65)
for K in range(K_lo5, K_hi5 + 1):
    lam = lam5_vals.get(K) or lambda_n(5, K)
    lam5_vals[K] = lam
    prev = lam5_vals.get(K-1, 0.0)
    delta = lam - prev
    if lam < BRIDGE_LO:
        state = "FLOW(0)"
        bpct_str = "      ---"
    elif lam < BRIDGE_HI:
        state = "BRIDGE"
        bpct_str = f"{bridge_pct(lam):>8.3f}%"
    else:
        state = "STRUCTURE"
        bpct_str = "  >100%"
    print(f"  {K:>4}  {lam:>14.8f}  {delta:>14.8f}  {bpct_str}  {state}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Cross-n Bridge Analysis n=6..12
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 78)
print("SECTION 4 — CROSS-n BRIDGE ANALYSIS (n=6..12)")
print("=" * 78)
print(f"  {'n':>4}  {'K_enter':>9}  {'K_exit':>8}  {'bridge_width':>14}  {'bw mod 7':>10}  {'bw // 7':>8}  7_structure")
print("  " + "-" * 80)

for n in range(6, 13):
    K_enter_n = None
    K_exit_n  = None
    lam_prev  = 0.0
    # Search up to K=500 to be safe
    for K in range(1, 501):
        lam = lambda_n(n, K)
        if lam >= BRIDGE_LO and K_enter_n is None:
            K_enter_n = K
        if lam >= BRIDGE_HI and K_exit_n is None:
            K_exit_n = K
        if K_enter_n and K_exit_n:
            break
        lam_prev = lam

    if K_enter_n is None:
        print(f"  {n:>4}  {'never':>9}  {'never':>8}  {'N/A':>14}  {'N/A':>10}  {'N/A':>8}  no bridge")
        continue
    if K_exit_n is None:
        print(f"  {n:>4}  {K_enter_n:>9}  {'never':>8}  {'N/A':>14}  {'N/A':>10}  {'N/A':>8}  enters but stays")
        continue

    bw = K_exit_n - K_enter_n
    bw_mod7 = bw % 7
    bw_div7 = bw // 7
    structure = "MULTIPLE_OF_7" if bw_mod7 == 0 else f"remainder={bw_mod7}"
    print(f"  {n:>4}  {K_enter_n:>9}  {K_exit_n:>8}  {bw:>14}  {bw_mod7:>10}  {bw_div7:>8}  {structure}")

print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5: THE 7-ZERO WINDOW for n=7
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 78)
print("SECTION 5 — THE 7-ZERO WINDOW FOR n=7")
print(f"  First 7 zeros: K=1..7   |   Last 7 zeros before K*(7): K=8..14")
print("=" * 78)

# recompute lambda7 for K=0..14 cleanly
lam7_all = {0: 0.0}
for K in range(1, 15):
    lam7_all[K] = lambda_n(7, K)

print()
print("  FIRST group (K=1..7):")
print(f"  {'K':>4}  {'λ_7(K)':>14}  {'Δforce':>14}  State")
print("  " + "-" * 50)
for K in range(1, 8):
    lam  = lam7_all[K]
    delta = lam - lam7_all[K-1]
    state = "FLOW(0)" if lam < BRIDGE_LO else ("BRIDGE" if lam < BRIDGE_HI else "STRUCTURE")
    print(f"  {K:>4}  {lam:>14.8f}  {delta:>14.8f}  {state}")

print()
print("  SECOND group (K=8..14):")
print(f"  {'K':>4}  {'λ_7(K)':>14}  {'Δforce':>14}  State")
print("  " + "-" * 50)
for K in range(8, 15):
    lam  = lam7_all[K]
    delta = lam - lam7_all[K-1]
    state = "FLOW(0)" if lam < BRIDGE_LO else ("BRIDGE" if lam < BRIDGE_HI else "STRUCTURE")
    print(f"  {K:>4}  {lam:>14.8f}  {delta:>14.8f}  {state}")

print()
lam7_7  = lam7_all[7]
lam7_14 = lam7_all[14]
lam7_entry_check = K_enter_7
print(f"  Bridge entry K_enter(7) = {K_enter_7}")
print(f"  λ_7(7)  = {lam7_7:.10f}  → {'IN BRIDGE' if BRIDGE_LO <= lam7_7 < BRIDGE_HI else ('STRUCTURE' if lam7_7 >= BRIDGE_HI else 'FLOW')}")
print(f"  λ_7(14) = {lam7_14:.10f}  → {'IN BRIDGE' if BRIDGE_LO <= lam7_14 < BRIDGE_HI else ('STRUCTURE' if lam7_14 >= BRIDGE_HI else 'FLOW')}")
if K_enter_7 <= 7:
    print(f"  Bridge entry is in FIRST group of 7 zeros (K={K_enter_7} ≤ 7)")
else:
    print(f"  Bridge entry is in SECOND group of 7 zeros (K={K_enter_7} > 7)")

# Which group spans the bridge?
bridge_span_start = K_enter_7
bridge_span_end   = K_exit_7 - 1
if bridge_span_end <= 7:
    print(f"  Bridge [K={bridge_span_start}..{bridge_span_end}] is entirely within FIRST group (K=1..7)")
elif bridge_span_start > 7:
    print(f"  Bridge [K={bridge_span_start}..{bridge_span_end}] is entirely within SECOND group (K=8..14)")
else:
    print(f"  Bridge [K={bridge_span_start}..{bridge_span_end}] SPANS both groups (starts in first, ends in second)")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6: FORCE DIRECTION (cos(7θ_k)) inside bridge
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 78)
print("SECTION 6 — FORCE DIRECTION cos(7·θ_k) FOR n=7 INSIDE BRIDGE (K=5..14)")
print("  cos(7θ) < 0 → cooperative (pushes toward 5/7)")
print("  cos(7θ) > 0 → opposing   (pushes back toward 0)")
print("=" * 78)
print()
print(f"  {'K':>4}  {'γ_k':>12}  {'θ_k':>14}  {'7·θ_k':>14}  {'cos(7θ_k)':>13}  Direction")
print("  " + "-" * 80)

coop_count = 0
opp_count  = 0
# Section covers K=5 (K_enter_7) to K=14 (K_exit_7) inclusive
for K in range(K_enter_7, K_exit_7 + 1):
    gk     = gammas[K - 1]
    thk    = theta(gk)
    n7thk  = 7 * thk
    cosval = math.cos(n7thk)
    direc  = direction_label(cosval)
    if cosval < 0:
        coop_count += 1
    else:
        opp_count += 1
    print(f"  {K:>4}  {gk:>12.6f}  {thk:>14.10f}  {n7thk:>14.10f}  {cosval:>13.10f}  {direc}")

print()
print(f"  Cooperative zeros (cos<0): {coop_count}")
print(f"  Opposing zeros    (cos>0): {opp_count}")
total_checked = coop_count + opp_count
print(f"  Total in window K={K_enter_7}..{K_exit_7}: {total_checked}")
print()

# HARMONY=7 pattern check: are zeros at positions k divisible by 7 cooperative?
print("  HARMONY=7 alignment check (zeros where k mod 7 == 0):")
for K in range(K_enter_7, K_exit_7 + 1):
    if K % 7 == 0:
        gk     = gammas[K - 1]
        thk    = theta(gk)
        cosval = math.cos(7 * thk)
        print(f"    k={K} (k mod 7 = 0): cos(7θ)={cosval:.10f} → {direction_label(cosval)}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7: CLEAN SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 78)
print("SECTION 7 — CLEAN SUMMARY TABLE")
print("=" * 78)

print()
print("FORCES INSIDE THE BRIDGE [1/2, 5/7):")
print()
print(f"  T*         = {T_STAR} = 5/7")
print(f"  BRIDGE_LO  = {BRIDGE_LO} = 1/2")
print(f"  BRIDGE_HI  = {BRIDGE_HI:.10f} = 5/7")
print(f"  BRIDGE_WIDTH = {BRIDGE_WIDTH:.10f} = 3/14")
print()
print("  n=7 generator bridge:")
print(f"  K_enter={K_enter_7}, K_exit={K_exit_7}, bridge_width={K_exit_7 - K_enter_7} zeros inside bridge")
print()
print(f"  {'K':>4} | {'λ_7(K)':>12} | {'Δforce':>12} | {'Bridge%':>8} | {'cos(7θ_k)':>12} | Direction")
print("  " + "-" * 80)
for K in range(K_enter_7, K_exit_7):
    lam  = lam7_all.get(K) or lambda_n(7, K)
    prev = lam7_all.get(K-1, 0.0)
    delta = lam - prev
    bpct  = bridge_pct(lam)
    gk    = gammas[K - 1]
    thk   = theta(gk)
    cosval = math.cos(7 * thk)
    direc  = direction_label(cosval)
    print(f"  {K:>4} | {lam:>12.8f} | {delta:>12.8f} | {bpct:>7.3f}% | {cosval:>12.8f} | {direc}")

print()
print("  HARMONY ENTANGLEMENT ANALYSIS:")
print(f"  {'n':>4} | {'K_enter':>8} | {'K_exit':>7} | {'zeros_in_bridge':>16} | {'mod 7':>6} | 7_structure")
print("  " + "-" * 72)
for n in range(6, 13):
    Ke = None
    Kx = None
    for K in range(1, 501):
        lam = lambda_n(n, K)
        if lam >= BRIDGE_LO and Ke is None:
            Ke = K
        if lam >= BRIDGE_HI and Kx is None:
            Kx = K
        if Ke and Kx:
            break
    if Ke is None or Kx is None:
        print(f"  {n:>4} | {'N/A':>8} | {'N/A':>7} | {'N/A':>16} | {'N/A':>6} | N/A")
        continue
    bw = Kx - Ke
    mod7 = bw % 7
    div7 = bw // 7
    struct = "MULTIPLE_OF_7" if mod7 == 0 else f"rem={mod7}"
    print(f"  {n:>4} | {Ke:>8} | {Kx:>7} | {bw:>16} | {mod7:>6} | {struct} (×7={div7})")

print()
print("  ETERNAL FLOW (n=5) INSIDE BRIDGE:")
print(f"  K_enter(5) = {K_enter_5}: bridge entry, λ_5={lam5_vals[K_enter_5]:.10f}")
print()
K_lo_s5 = K_enter_5
K_hi_s5 = min(150, K_enter_5 + 30)
print(f"  {'K':>4} | {'λ_5(K)':>12} | {'Δforce':>12} | {'Bridge%':>10} | State")
print("  " + "-" * 60)
for K in range(K_lo_s5, K_hi_s5 + 1):
    lam  = lam5_vals.get(K) or lambda_n(5, K)
    lam5_vals[K] = lam
    prev = lam5_vals.get(K-1, 0.0)
    delta = lam - prev
    if lam < BRIDGE_LO:
        state = "FLOW(0)"; bpct_s = "       ---"
    elif lam < BRIDGE_HI:
        state = "BRIDGE";  bpct_s = f"{bridge_pct(lam):>9.3f}%"
    else:
        state = "STRUCTURE"; bpct_s = "    >100%"
    print(f"  {K:>4} | {lam:>12.8f} | {delta:>12.8f} | {bpct_s} | {state}")

print()
print(f"  max λ_5 (K=1..150) = {max_lam5:.10f} at K={max_lam5_K}")
print(f"  Does n=5 ever reach STRUCTURE (≥5/7)? {'YES' if max_lam5 >= T_STAR else 'NO — eternal bridge/flow'}")

print()
print("=" * 78)
print("END OF gap_forces_study.py")
print("=" * 78)
