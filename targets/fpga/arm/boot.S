/*
 * boot.S -- Minimal Bare Metal Startup for CK (Zynq-7020 ARM Cortex-A9)
 *
 * FSBL has already:
 *   - Configured DDR3
 *   - Set PLL clocks
 *   - Loaded this ELF into DDR
 *   - Jumped to _start
 *
 * We just need to:
 *   1. Set up the stack pointer
 *   2. Zero BSS
 *   3. Jump to main()
 */

.section .boot, "ax"
.global _start
.type _start, %function

_start:
    /* Disable interrupts */
    cpsid   if

    /* Set stack pointer (grows down from __stack_start) */
    ldr     sp, =__stack_start

    /* Zero BSS section */
    ldr     r0, =__bss_start
    ldr     r1, =__bss_end
    mov     r2, #0
bss_loop:
    cmp     r0, r1
    bge     bss_done
    str     r2, [r0], #4
    b       bss_loop
bss_done:

    /* Jump to C main */
    bl      main

    /* If main returns (it shouldn't), spin forever */
hang:
    wfe
    b       hang

.size _start, . - _start
