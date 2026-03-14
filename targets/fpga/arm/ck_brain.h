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

/* ── AXI GPIO Register Layout ── */
/*
 * Each AXI GPIO block has:
 *   Offset 0x0000: GPIO_DATA   (Channel 1 data)
 *   Offset 0x0004: GPIO_TRI    (Channel 1 tri-state)
 *   Offset 0x0008: GPIO2_DATA  (Channel 2 data, if dual)
 *   Offset 0x000C: GPIO2_TRI   (Channel 2 tri-state)
 */
#define GPIO_CH1_DATA  0x0000
#define GPIO_CH1_TRI   0x0004
#define GPIO_CH2_DATA  0x0008
#define GPIO_CH2_TRI   0x000C

/* ── AXI GPIO Base Addresses (Vivado auto-assigned) ── */
/* From build log: assign_bd_address auto-assign, 64K each */

#define CK_GPIO_DAC_BASE       0x41200000  /* DAC SPI (speaker output) */
#define CK_GPIO_GAIT_RD_BASE   0x41210000  /* Gait vortex read */
#define CK_GPIO_GAIT_WR_BASE   0x41220000  /* Gait vortex write */
#define CK_GPIO_HB_RD_BASE     0x41230000  /* Heartbeat read (2x32 input) */
#define CK_GPIO_HB_WR_BASE     0x41240000  /* Heartbeat write (32 output) */
#define CK_GPIO_I2C_BASE       0x41250000  /* I2C master (IMU) */
#define CK_GPIO_LED_BASE       0x41260000  /* LED GPIO (4-bit output) */
#define CK_GPIO_MIC_BASE       0x41270000  /* I2S microphone */
#define CK_GPIO_SERVO_BASE     0x41280000  /* Bus servo UART */
#define CK_GPIO_SERVO_CAL_BASE 0x41290000  /* Servo calibration read */

/* ═══════════════════════════════════════════
 * HEARTBEAT WRITE (axi_gpio_hb_wr @ 0x41240000)
 * ═══════════════════════════════════════════
 * Channel 1 (32-bit output to PL):
 *   [3:0]   phase_b       -- Being operator input
 *   [7:4]   phase_d       -- Doing operator input
 *   [8]     tick_strobe   -- Pulse high to trigger tick
 *   [9]     enable        -- Heartbeat enable
 */
#define CK_REG_HB_WR        (CK_GPIO_HB_WR_BASE + GPIO_CH1_DATA)

/* Packing macros for heartbeat write register */
#define CK_HB_WR_PACK(b, d, strobe, en) \
    (((uint32_t)(b) & 0xF) | \
     (((uint32_t)(d) & 0xF) << 4) | \
     (((uint32_t)(strobe) & 1) << 8) | \
     (((uint32_t)(en) & 1) << 9))

/* Convenience register names (backward compat) */
#define CK_REG_PHASE_B      CK_REG_HB_WR  /* packed: bits [3:0] */
#define CK_REG_PHASE_D      CK_REG_HB_WR  /* packed: bits [7:4] */
#define CK_REG_TICK_STROBE  CK_REG_HB_WR  /* packed: bit [8] */
#define CK_REG_ENABLE       CK_REG_HB_WR  /* packed: bit [9] */

/* ═══════════════════════════════════════════
 * HEARTBEAT READ (axi_gpio_hb_rd @ 0x41230000)
 * ═══════════════════════════════════════════
 * Channel 1 (32-bit input from PL):
 *   [3:0]   phase_bc      -- Becoming: CL[b][d]
 *   [7:4]   fused_op      -- Running fuse result
 *   [8]     bump_detected -- Quantum bump pair
 *   [9]     tick_done     -- Tick complete flag
 *   [25:10] coh_num       -- Harmony count (16 bits)
 *   [31:26] (reserved)
 *
 * Channel 2 (32-bit input from PL):
 *   [15:0]  coh_den       -- Window size (16 bits)
 *   [19:16] phase_b_out   -- Echo Being
 *   [23:20] phase_d_out   -- Echo Doing
 *   [31:24] tick_count[7:0] (low byte for quick check)
 */
#define CK_REG_HB_RD_CH1    (CK_GPIO_HB_RD_BASE + GPIO_CH1_DATA)
#define CK_REG_HB_RD_CH2    (CK_GPIO_HB_RD_BASE + GPIO_CH2_DATA)

/* Unpacking macros for heartbeat read */
#define CK_HB_RD_PHASE_BC(v)   ((v) & 0xF)
#define CK_HB_RD_FUSE(v)       (((v) >> 4) & 0xF)
#define CK_HB_RD_BUMP(v)       (((v) >> 8) & 1)
#define CK_HB_RD_TICK_DONE(v)  (((v) >> 9) & 1)
#define CK_HB_RD_COH_NUM(v)    (((v) >> 10) & 0xFFFF)
#define CK_HB_RD2_COH_DEN(v)   ((v) & 0xFFFF)
#define CK_HB_RD2_B_OUT(v)     (((v) >> 16) & 0xF)
#define CK_HB_RD2_D_OUT(v)     (((v) >> 20) & 0xF)

/* Legacy names -- read both channels and unpack */
#define CK_REG_PHASE_BC    CK_REG_HB_RD_CH1
#define CK_REG_TICK_DONE   CK_REG_HB_RD_CH1
#define CK_REG_COH_NUM     CK_REG_HB_RD_CH1
#define CK_REG_COH_DEN     CK_REG_HB_RD_CH2
#define CK_REG_BUMP        CK_REG_HB_RD_CH1
#define CK_REG_FUSE        CK_REG_HB_RD_CH1
#define CK_REG_PHASE_B_OUT CK_REG_HB_RD_CH2
#define CK_REG_PHASE_D_OUT CK_REG_HB_RD_CH2
#define CK_REG_TICK_COUNT  CK_REG_HB_RD_CH2  /* packed in ch2 upper bits */

/* ═══════════════════════════════════════════
 * GAIT WRITE (axi_gpio_gait_wr @ 0x41220000)
 * ═══════════════════════════════════════════
 * Channel 1 (32-bit output):
 *   [1:0]   gait_mode     -- 0=stand, 1=walk, 2=trot, 3=bound
 *   [2]     gait_start    -- Pulse to start
 *   [3]     gait_enable   -- Enable gait controller
 *   [19:4]  leg_ops       -- {leg3[15:12],leg2[11:8],leg1[7:4],leg0[3:0]}
 */
#define CK_REG_GAIT_WR      (CK_GPIO_GAIT_WR_BASE + GPIO_CH1_DATA)
#define CK_REG_GAIT_MODE    CK_REG_GAIT_WR  /* bits [1:0] */
#define CK_REG_GAIT_START   CK_REG_GAIT_WR  /* bit [2] */
#define CK_REG_GAIT_ENABLE  CK_REG_GAIT_WR  /* bit [3] */
#define CK_REG_LEG_OPS      CK_REG_GAIT_WR  /* bits [19:4] */

/* ═══════════════════════════════════════════
 * GAIT READ (axi_gpio_gait_rd @ 0x41210000)
 * ═══════════════════════════════════════════
 * Channel 1 (32-bit input):
 *   [15:0]  vortex_flat   -- {v3[12:9],v2[8:6],v1[5:3],v0[2:0]}
 *   [19:16] aligned_flat  -- per-leg aligned flags
 *   [31:20] correction_flat -- {c3,c2,c1,c0} 3-bit each
 *
 * Channel 2 (32-bit input):
 *   [15:0]  gait_coh_num  -- Gait coherence numerator
 *   [19:16] gait_phase    -- Current gait phase
 *   [31:20] gait_tick     -- Gait tick count (12 bits)
 */
#define CK_REG_GAIT_RD_CH1  (CK_GPIO_GAIT_RD_BASE + GPIO_CH1_DATA)
#define CK_REG_GAIT_RD_CH2  (CK_GPIO_GAIT_RD_BASE + GPIO_CH2_DATA)
#define CK_REG_GAIT_VTX_01  CK_REG_GAIT_RD_CH1
#define CK_REG_GAIT_VTX_23  CK_REG_GAIT_RD_CH1
#define CK_REG_GAIT_ALIGN   CK_REG_GAIT_RD_CH1
#define CK_REG_GAIT_CORR    CK_REG_GAIT_RD_CH1
#define CK_REG_GAIT_COH     CK_REG_GAIT_RD_CH2
#define CK_REG_GAIT_PHASE   CK_REG_GAIT_RD_CH2
#define CK_REG_GAIT_TICK    CK_REG_GAIT_RD_CH2
#define CK_REG_GAIT_ALL_OK  CK_REG_GAIT_RD_CH1  /* bit in aligned_flat */

/* ═══════════════════════════════════════════
 * SERVO CALIBRATION (axi_gpio_servo_cal @ 0x41290000)
 * ═══════════════════════════════════════════
 * Channel 1 (32-bit input):
 *   [11:0]  hip0_pwm      -- Leg 0 hip PWM
 *   [27:16] knee0_pwm     -- Leg 0 knee PWM
 *   [31:28] valid         -- New values ready (bit 28)
 *
 * Channel 2 (32-bit input):
 *   [11:0]  hip1_pwm      -- Leg 1 hip PWM
 *   [27:16] knee1_pwm     -- Leg 1 knee PWM
 *
 * Note: Legs 2-3 read via GPIO_SERVO_BASE channel 2 for update strobe,
 *       full 4-leg readout requires reading both GPIOs.
 *       For now, packed: ch1={knee0,hip0}, ch2={knee1,hip1}
 *       Legs 2-3 share the same GPIO with update strobe.
 */
#define CK_REG_SERVO_CAL_CH1 (CK_GPIO_SERVO_CAL_BASE + GPIO_CH1_DATA)
#define CK_REG_SERVO_CAL_CH2 (CK_GPIO_SERVO_CAL_BASE + GPIO_CH2_DATA)
#define CK_REG_SERVO_UPDATE  (CK_GPIO_SERVO_BASE + GPIO_CH1_DATA)   /* W: pulse */
#define CK_REG_SERVO_VALID   CK_REG_SERVO_CAL_CH1  /* bit 28 */
#define CK_REG_SERVO_L0_HK   CK_REG_SERVO_CAL_CH1  /* {knee0[27:16],hip0[11:0]} */
#define CK_REG_SERVO_L0_A    CK_REG_SERVO_CAL_CH2  /* (unused for 2-DOF legs) */
#define CK_REG_SERVO_L1_HK   CK_REG_SERVO_CAL_CH2  /* {knee1[27:16],hip1[11:0]} */
#define CK_REG_SERVO_L1_A    CK_REG_SERVO_CAL_CH2  /* (unused) */
#define CK_REG_SERVO_L2_HK   CK_REG_SERVO_CAL_CH1  /* (overlap -- use GPIO read) */
#define CK_REG_SERVO_L2_A    CK_REG_SERVO_CAL_CH1
#define CK_REG_SERVO_L3_HK   CK_REG_SERVO_CAL_CH2
#define CK_REG_SERVO_L3_A    CK_REG_SERVO_CAL_CH2

/* ═══════════════════════════════════════════
 * BUS SERVO UART (axi_gpio_servo @ 0x41280000)
 * ═══════════════════════════════════════════
 * Channel 1 (32-bit output): {write_strobe[8], tx_data[7:0]}
 * Channel 2 (32-bit input):  {tx_full[0]}
 */
#define CK_SERVO_UART_BASE    CK_GPIO_SERVO_BASE
#define CK_SERVO_UART_TX      (CK_GPIO_SERVO_BASE + GPIO_CH1_DATA)
#define CK_SERVO_UART_SR      (CK_GPIO_SERVO_BASE + GPIO_CH2_DATA)
#define CK_SERVO_UART_TXFULL  (1 << 0)

/* ═══════════════════════════════════════════
 * DAC SPI (axi_gpio_dac @ 0x41200000)
 * ═══════════════════════════════════════════
 * Channel 1 (32-bit output): {valid[16], sample[15:0]}
 * Channel 2 (32-bit input):  {fifo_full[0]}
 */
#define CK_DAC_BASE           CK_GPIO_DAC_BASE
#define CK_DAC_SAMPLE         (CK_GPIO_DAC_BASE + GPIO_CH1_DATA)
#define CK_DAC_STATUS         (CK_GPIO_DAC_BASE + GPIO_CH2_DATA)
#define CK_DAC_FIFO_FULL      (1 << 0)

/* ═══════════════════════════════════════════
 * I2S MICROPHONE (axi_gpio_mic @ 0x41270000)
 * ═══════════════════════════════════════════
 * Channel 1 (32-bit input):  {count[31:24], valid[23], sample[22:0]}
 * Channel 2 (32-bit output): {read_ack[0]}
 */
#define CK_MIC_BASE           CK_GPIO_MIC_BASE
#define CK_MIC_SAMPLE         (CK_GPIO_MIC_BASE + GPIO_CH1_DATA)
#define CK_MIC_STATUS         (CK_GPIO_MIC_BASE + GPIO_CH1_DATA)  /* count in upper bits */
#define CK_MIC_READ           (CK_GPIO_MIC_BASE + GPIO_CH2_DATA)

/* ═══════════════════════════════════════════
 * I2C MASTER (axi_gpio_i2c @ 0x41250000)
 * ═══════════════════════════════════════════
 * Channel 1 (32-bit output): {cmd[17:16], addr[14:8], data[7:0]}
 * Channel 2 (32-bit input):  {busy[1], ack[0], data[15:8]}
 */
#define CK_I2C_BASE           CK_GPIO_I2C_BASE
#define CK_I2C_DATA           (CK_GPIO_I2C_BASE + GPIO_CH1_DATA)
#define CK_I2C_ADDR           (CK_GPIO_I2C_BASE + GPIO_CH1_DATA)  /* packed bits [14:8] */
#define CK_I2C_CMD            (CK_GPIO_I2C_BASE + GPIO_CH1_DATA)  /* packed bits [17:16] */
#define CK_I2C_STATUS         (CK_GPIO_I2C_BASE + GPIO_CH2_DATA)

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
