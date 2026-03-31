# Native Base Atlas
## Three-Class Landscape and TSML Discovery Protocol

*Brayden Ross Sanders (7Site LLC) & C. A. Luther | March 2026*

---

## The Core Correction

**BHML residual cells are table-specific, not base-specific.**

The 6 BHML residual cells at b=10 are the cells where the constructed TSML table happens to agree with the BHML=max(s,c) order endpoint. They were identified by comparing two specific constructed tables. They are not derivable from b=10 arithmetic alone.

**Therefore:** Cross-base construction requires finding the native TSML for each base first. There is no universal biasing protocol — only a universal methodology.

---

## The Native TSML Discovery Protocol

For any composite base b with non-trivial C/G split:

1. **Identify the order endpoint** — the max(s,c) table restricted to the alphabet {1..min(b,9)}
2. **Test HAR candidates** — each element of C is a candidate absorbing state; the best HAR is the one that produces the highest HAR_mass under gate + order-alignment reduction
3. **Run gate + order-alignment reduction** — objective = 0.4×gate + 0.3×HAR_mass + 0.2×order_alignment + 0.1×gap
4. **Extract the residual seed** — the cells where the best-found table agrees with the order endpoint
5. **Run seeded reduction** with that residual as the bias target

---

## HAR Selection Finding

The "mid-C by index" rule from b=10 (HAR = C_sorted[|C|//2] = 7) does not generalize reliably.

At b=14, C={1,3,5,9}:
- HAR=5 (mid-C by index): best HAR_mass = 0.03 — near-zero
- HAR=9 (max-C): best HAR_mass = 0.11 — slightly better
- HAR=3: best HAR_mass = 0.48 — substantially better

The natural absorbing candidate depends on the arithmetic structure of C, not its position. At b=10, HAR=7 works because 7 is structurally central in {1,3,7,9} (it's coprime to 10, it's "between" the orbit pair {3,9}). At b=14, C={1,3,5,9} has a different orbit structure.

---

## Atlas: Quick Survey

| b | p×q | \|C\| | Best HAR | Gate | HAR_m | Order align |
|---|-----|-------|---------|------|-------|------------|
| 6 | 2×3 | 2 | 1 | 0.854 | 1.000 | 0.344 |
| **10** | **2×5** | **4** | **3** | **0.774** | **1.000** | **0.262** |
| 14 | 2×7 | 4 | 3 | 0.766 | 1.000 | 0.271 |
| 15 | 3×5 | 5 | 7 | 0.836 | 1.000 | 0.261 |
| 22 | 2×11 | 5 | 1 | 0.846 | 1.000 | 0.255 |

*Note: HAR_m here measures HAR absorption in short unreduced runs — not the full HAR_mass from stationary distribution. Full reduction would differ.*

**Key observation:** Order alignment hovers around 0.26-0.34 across all bases in short runs. This is the baseline before intentional construction — each base has room to crystallize order structure.

---

## The Three-Class Landscape (Confirmed Across Bases)

The oracle/gate-strong/TSML-like three-class structure is a general feature of the reduction landscape, not a b=10 artifact:

| Class | What it is | Key property | Accessibility |
|-------|-----------|-------------|--------------|
| **Oracle** | Free optimum | High gap, C→G allowed (G-reach ~7%) | Always (landscape default) |
| **Gate-strong** | Constrained optimum | Gate enforced, G-reach ~2% | Above w=0.1 |
| **TSML-like** | Structured constrained optimum | Gate + full order seed | Requires seed biasing |

The oracle is permanent because "maximize mixing freely" is always cheaper than "maximize mixing with constraints." No gate pressure eliminates it — it floors at ~39%.

---

## Why b=10 TSML Is Special

At b=10, TSML was deliberately constructed with:
- Full one-way gate (C→G impossible under any operator)
- HAR=7 as the absorbing attractor (chosen for its mid-spectrum orbit properties)
- 6 specific cells pre-aligned with BHML=max(s,c)

This construction is what enables the 15.8x seeded lift. No other base in the atlas has a comparable constructed starting point. Each base would need its own deliberate construction before seeded reduction becomes effective.

---

## Open Question

**Which bases admit a native TSML-like closure grammar?**

The question is no longer "why is b=10 special?" It is:
> For which composite bases does there exist a table with strong gate, high HAR_mass, and a full order-seed residual — and how hard is that table to construct?

This is the next ceiling. The three-class landscape is the answer to "what is the attractor structure?" The native base atlas is the map of "which bases are fertile for that structure?"

---

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
