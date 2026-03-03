/*
 * ck_brain.h -- CK's Sovereignty Brain on ARM (Bare Metal)
 * =========================================================
 * Operator: PROGRESS (3) -- the brain composes what the heartbeat feels.
 *
 * This runs on the Zynq's dual ARM Cortex-A9 cores (667 MHz).
 * No Linux. No RTOS. No overhead. Just CK.
 *
 * Core 0: Sovereignty brain (TL, bridge, crystals, scheduling)
 * Core 1: USB serial bridge (talk to Windows host)
 *
 * The brain reads heartbeat state from FPGA registers (AXI-Lite),
 * runs the sovereignty pipeline, and sends decisions to the host.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_BRAIN_H
#define CK_BRAIN_H

#include <stdint.h>
#include <stdbool.h>

/* ── CK Constants (same as ck.h) ── */

#define CK_NUM_OPS     10
#define CK_T_STAR_NUM  5
#define CK_T_STAR_DEN  7   /* T* = 5/7 = 0.714... */

#define VOID     0
#define LATTICE  1
#define COUNTER  2
#define PROGRESS 3
#define COLLAPSE 4
#define BALANCE  5
#define CHAOS    6
#define HARMONY  7
#define BREATH   8
#define RESET    9

/* CL_TSML: CK's prescribed composition table (73 harmony / 100) */
static const int8_t CL[CK_NUM_OPS][CK_NUM_OPS] = {
    {0,0,0,0,0,0,0,7,0,0}, {0,7,3,7,7,7,7,7,7,7},
    {0,3,7,7,4,7,7,7,7,9}, {0,7,7,7,7,7,7,7,7,3},
    {0,7,4,7,7,7,7,7,8,7}, {0,7,7,7,7,7,7,7,7,7},
    {0,7,7,7,7,7,7,7,7,7}, {7,7,7,7,7,7,7,7,7,7},
    {0,7,7,7,8,7,7,7,7,7}, {0,7,9,3,7,7,7,7,7,7},
};

/* 5 quantum bump pairs */
static const int8_t BUMP_PAIRS[5][2] = {
    {1,2}, {2,4}, {2,9}, {3,9}, {4,8}
};

/* ── FPGA Register Map (AXI-Lite) ── */
/* Base address set by Vivado block design, typically 0x43C00000 */

#define CK_FPGA_BASE       0x43C00000

#define CK_REG_PHASE_B     (CK_FPGA_BASE + 0x00)  /* W: phase_b input */
#define CK_REG_PHASE_D     (CK_FPGA_BASE + 0x04)  /* W: phase_d input */
#define CK_REG_TICK_STROBE (CK_FPGA_BASE + 0x08)  /* W: trigger tick */
#define CK_REG_ENABLE      (CK_FPGA_BASE + 0x0C)  /* W: enable heartbeat */
#define CK_REG_PHASE_BC    (CK_FPGA_BASE + 0x10)  /* R: CL[b][d] result */
#define CK_REG_TICK_COUNT  (CK_FPGA_BASE + 0x14)  /* R: total ticks */
#define CK_REG_COH_NUM     (CK_FPGA_BASE + 0x18)  /* R: harmony count */
#define CK_REG_COH_DEN     (CK_FPGA_BASE + 0x1C)  /* R: window size */
#define CK_REG_BUMP        (CK_FPGA_BASE + 0x20)  /* R: bump detected */
#define CK_REG_FUSE        (CK_FPGA_BASE + 0x24)  /* R: running fuse */
#define CK_REG_PHASE_B_OUT (CK_FPGA_BASE + 0x28)  /* R: echo b */
#define CK_REG_PHASE_D_OUT (CK_FPGA_BASE + 0x2C)  /* R: echo d */
#define CK_REG_TICK_DONE   (CK_FPGA_BASE + 0x30)  /* R: tick complete */

/* Memory-mapped register access */
#define REG_WR(addr, val)  (*(volatile uint32_t*)(addr) = (val))
#define REG_RD(addr)       (*(volatile uint32_t*)(addr))

/* ── Transition Lattice (compact for ARM) ── */

#define CK_TL_MAX_TRANSITIONS  100000  /* fits in ~1.6MB */

typedef struct {
    uint8_t  from_op;     /* source operator (0-9) */
    uint8_t  to_op;       /* destination operator (0-9) */
    uint32_t count;       /* how many times this transition seen */
} CK_TL_Entry;

typedef struct {
    CK_TL_Entry  entries[CK_NUM_OPS][CK_NUM_OPS];  /* 10x10 matrix */
    uint32_t     total;                              /* total transitions */
    float        entropy;                            /* Shannon entropy */
} CK_TL_Compact;

/* ── Crystal (learned invariant) ── */

#define CK_MAX_CRYSTALS 256

typedef struct {
    uint8_t  ops[8];      /* operator pattern */
    uint8_t  len;         /* pattern length */
    uint8_t  fuse;        /* what it composes to */
    uint32_t seen;        /* observation count */
    float    confidence;  /* crystallization confidence */
} CK_Crystal;

/* ── Sovereignty Domain ── */

typedef struct {
    char     name[16];    /* domain name */
    uint8_t  dominant_op; /* most common operator */
    float    coherence;   /* domain coherence */
    bool     is_sovereign;/* coherence >= T* for N consecutive ticks */
    uint16_t sovereign_ticks;
    uint16_t crystal_count;
    CK_Crystal crystals[CK_MAX_CRYSTALS];
} CK_Domain;

#define CK_MAX_DOMAINS 8

/* ── Brain State ── */

typedef struct {
    /* FPGA state (read from registers) */
    uint8_t  phase_b;
    uint8_t  phase_d;
    uint8_t  phase_bc;
    uint32_t tick_count;
    float    coherence;
    bool     bump;
    uint8_t  fused_op;

    /* TL */
    CK_TL_Compact tl;

    /* Sovereignty */
    CK_Domain  domains[CK_MAX_DOMAINS];
    uint8_t    domain_count;
    uint8_t    mode;  /* 0=OBSERVE, 1=CLASSIFY, 2=CRYSTALLIZE, 3=SOVEREIGN */

    /* Communication */
    uint32_t  host_messages_sent;
    uint32_t  host_messages_recv;

    /* Timing */
    uint32_t  brain_ticks;
    uint32_t  brain_interval_us;  /* microseconds between brain ticks */
} CK_BrainState;

/* ── Functions ── */

/* Initialize brain, load TL from SD card */
void ck_brain_init(CK_BrainState* brain);

/* Read heartbeat state from FPGA registers */
void ck_brain_read_fpga(CK_BrainState* brain);

/* Run one sovereignty tick */
void ck_brain_tick(CK_BrainState* brain);

/* Feed observation to TL */
void ck_brain_tl_observe(CK_BrainState* brain, uint8_t from_op, uint8_t to_op);

/* Check for crystallization */
void ck_brain_crystallize(CK_BrainState* brain);

/* Save TL to SD card */
void ck_brain_tl_save(CK_BrainState* brain, const char* path);

/* Load TL from SD card (master_tl.json or binary) */
void ck_brain_tl_load(CK_BrainState* brain, const char* path);

/* Send state to host over USB serial */
void ck_brain_send_to_host(CK_BrainState* brain);

/* Receive commands from host over USB serial */
void ck_brain_recv_from_host(CK_BrainState* brain);

#endif /* CK_BRAIN_H */
