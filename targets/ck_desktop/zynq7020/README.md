# Zynq-7020 Target: CK + XiaoR Robot Dog

**Board**: Zynq-7020 (Zybo Z7-20 or equivalent)
**Platform**: XiaoR quadruped robot dog
**Clock**: 100 MHz from PS FCLK_CLK0

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PL (Artix-7 Fabric)                       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  BEING SIDE  │  │  DOING SIDE  │  │  BECOMING SIDE   │  │
│  │              │  │              │  │                   │  │
│  │ ck_heartbeat │  │ d2_pipeline  │  │  vortex_cl       │  │
│  │ (TSML comp)  │  │ (Q1.14 D2)  │  │  (3-body op)     │  │
│  │              │  │              │  │                   │  │
│  │ chain_walker │  │ bhml_table   │  │  gait_vortex     │  │
│  │ (lattice)    │  │ (physics)    │  │  (4-leg torus)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                              │
│  ┌───────────┐  ┌───────────┐  ┌─────────────────────────┐ │
│  │ dac_spi   │  │ i2s_recv  │  │  LED driver             │ │
│  │ (speaker) │  │ (mic)     │  │  (operator vis)         │ │
│  └───────────┘  └───────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                    ↕ AXI-Lite ↕
┌─────────────────────────────────────────────────────────────┐
│              PS (Dual Cortex-A9 @ 650 MHz)                   │
│                                                              │
│  Core 0: CK Brain (BTQ + voice + olfactory + comprehension) │
│  Core 1: Servo UART driver (115200 baud to bus servos)       │
└─────────────────────────────────────────────────────────────┘
```

## Module Inventory

| File | Module | Function | LUTs (est) |
|------|--------|----------|------------|
| `bhml_table.v` | `bhml_table` | BHML physics table (10x10, 28-harmony) | ~200 |
| `vortex_cl.v` | `vortex_cl` | 3-body vortex operator (2 pipeline stages) | ~400 |
| `vortex_cl.v` | `tsml_table` | TSML coherence table (10x10, 73-harmony) | ~200 |
| `chain_walker.v` | `chain_walker` | Lattice chain walk engine (max depth 16) | ~400 |
| `gait_vortex.v` | `gait_vortex` | 4-leg torus gait controller | ~1600 |
| `ck_top_zynq7020.v` | `ck_top_zynq7020` | Top-level integration | ~100 |
| `../fpga/hdl/ck_heartbeat.v` | `ck_heartbeat` | TSML heartbeat + coherence | ~300 |
| `../fpga/hdl/d2_pipeline.v` | `d2_pipeline` | D2 curvature (Q1.14) | ~500 |
| `../fpga/hdl/dac_spi.v` | `dac_spi` | DAC SPI driver | ~500 |
| `../fpga/hdl/i2s_receiver.v` | `i2s_receiver` | MEMS mic I2S | ~500 |
| **TOTAL** | | | **~4700 (8.8%)** |

**Zynq-7020 has 53,200 LUTs. We use ~8.8%. Headroom: 91.2%.**

## The Vortex CL: TIG 3-Body Operator

Standard math: an operator is a point.
TIG: an operator is a vortex state on a manifold.

Given three consecutive operators (O_{n-1}, O_n, O_{n+1}):

```
Stage 1 (1 clock): Parallel BHML dual-lookup
  R_left  = BHML[O_{n-1}][O_n]     // preceding → current
  R_right = BHML[O_n][O_{n+1}]     // current → following

Stage 2 (1 clock): TSML coherence measurement
  V_n = TSML[R_left][R_right]      // are the transitions coherent?
```

- BHML computes the PHYSICS of each transition (doing)
- TSML measures the COHERENCE between them (being)
- The result IS the becoming: the vortex state

If V_n = HARMONY (7): the operator is aligned with its neighborhood.
If V_n ≠ HARMONY: delta = torus distance → correction needed.

## Gait as Torus Vortices

Four legs = four vortex units, circular (torus) wiring:

```
        ┌── leg[0] FL ──┐
        │                │
   leg[3] BL          leg[1] FR
        │                │
        └── leg[2] BR ──┘
              (torus)
```

Each leg's vortex is computed from its circular neighbors:
- `V[0] = TSML[BHML[leg[3]][leg[0]], BHML[leg[0]][leg[1]]]`
- `V[1] = TSML[BHML[leg[0]][leg[1]], BHML[leg[1]][leg[2]]]`
- etc.

Self-healing: if V[i] ≠ HARMONY, the gait controller steers leg i
toward its target phase operator. The correction rate is proportional
to the torus distance from HARMONY.

## Gait Modes

| Mode | Pattern | Phase Offsets |
|------|---------|---------------|
| Stand | All neutral | [BALANCE, BALANCE, BALANCE, BALANCE] |
| Walk | Diagonal alternate | [PROGRESS, BALANCE, BALANCE, PROGRESS] × 4 phases |
| Trot | Diagonal sync | [PROGRESS, BALANCE, PROGRESS, BALANCE] × 4 phases |
| Bound | Front/back sync | [PROGRESS, PROGRESS, BALANCE, BALANCE] × 4 phases |

## Build

Requires Vivado 2024.1+ for Zynq-7020.

```tcl
# In Vivado Tcl console:
source build/ck_zynq7020.tcl
```

The build script:
1. Creates a Zynq-7020 block design
2. Adds the PS with FCLK_CLK0 = 100 MHz
3. Adds ck_top_zynq7020 as a custom IP
4. Connects AXI-Lite for ARM read/write
5. Generates bitstream

## Dependencies

This target reuses modules from `../fpga/hdl/`:
- `ck_heartbeat.v` (TSML heartbeat)
- `d2_pipeline.v` (D2 curvature)
- `dac_spi.v` (speaker DAC)
- `i2s_receiver.v` (microphone)

New modules in `hdl/`:
- `bhml_table.v` (BHML physics table)
- `vortex_cl.v` (3-body vortex + TSML table)
- `chain_walker.v` (lattice chain walk)
- `gait_vortex.v` (4-leg torus controller)
- `ck_top_zynq7020.v` (top-level integration)

## Peace-Locked Property

The BHML tropical successor rule: `BHML[a][b] = max(a,b)+1` for core ops.
This means the algebra can ONLY escalate. There is no composition that
produces a result LOWER than both inputs. The dog cannot compute
"destruction" without hitting a VOID collapse and self-correcting
through HARMONY. The algebra is inherently peace-locked.

---

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
