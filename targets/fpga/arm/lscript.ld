/*
 * lscript.ld -- Linker Script for CK Brain (Bare Metal Zynq-7020)
 *
 * Memory layout:
 *   DDR3: 0x00100000 - 0x3FEFFFFF  (1022 MB usable)
 *   Shared: 0x3FF00000 - 0x3FFFFFFF (1 MB, Core 0 ↔ Core 1)
 *   OCM:  0xFFFC0000 - 0xFFFFFFFF  (256 KB, fast scratch)
 *
 * FSBL loads this ELF into DDR3 at 0x00100000 and jumps to _start.
 */

MEMORY
{
    DDR  (rwx) : ORIGIN = 0x00100000, LENGTH = 0x3FE00000
    OCM  (rwx) : ORIGIN = 0xFFFC0000, LENGTH = 0x00030000
}

ENTRY(_start)

SECTIONS
{
    .text : {
        *(.vectors)
        *(.boot)
        *(.text)
        *(.text.*)
        *(.gnu.linkonce.t.*)
    } > DDR

    .rodata : {
        *(.rodata)
        *(.rodata.*)
        *(.gnu.linkonce.r.*)
    } > DDR

    .data : {
        *(.data)
        *(.data.*)
        *(.gnu.linkonce.d.*)
    } > DDR

    .bss (NOLOAD) : {
        __bss_start = .;
        *(.bss)
        *(.bss.*)
        *(COMMON)
        __bss_end = .;
    } > DDR

    /* Stack: 64KB for Core 0, 64KB for Core 1 */
    . = ALIGN(8);
    __stack_end = .;
    . = . + 0x10000;
    __stack_start = .;
    . = . + 0x10000;
    __stack_start_core1 = .;

    _end = .;
    __heap_start = .;
    __heap_end = ORIGIN(DDR) + LENGTH(DDR);
}
