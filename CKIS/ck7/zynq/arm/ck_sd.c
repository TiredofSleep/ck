/*
 * ck_sd.c -- SD Card Persistence for CK's Transition Lattice
 * =============================================================
 * Operator: LATTICE (1) -- structure that endures across lifetimes.
 *
 * Uses Xilinx FatFs library (included in bare metal BSP) for
 * FAT32 SD card access via the Zynq PS SD controller.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_sd.h"
#include <string.h>

/*
 * NOTE: In a real Vitis bare metal project, include:
 *   #include "ff.h"        // Xilinx FatFs
 *   #include "xsdps.h"     // Zynq SD driver
 *
 * For now, we define the interface with stubs.
 * The actual implementation uses FatFs f_open/f_write/f_read/f_close.
 */

/* Magic bytes for TL file format */
static const uint8_t TL_MAGIC[4] = {'C', 'K', 'T', 'L'};
static const uint8_t TL_VERSION = 1;

/* Simple CRC-8/MAXIM (same as ck_serial.py) */
static uint8_t crc8(const uint8_t* data, uint32_t len) {
    uint8_t crc = 0x00;
    for (uint32_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (int bit = 0; bit < 8; bit++) {
            if (crc & 0x80)
                crc = (crc << 1) ^ 0x31;
            else
                crc = crc << 1;
        }
    }
    return crc;
}

/* ── Serialization helpers ── */

static void write_u8(uint8_t* buf, uint32_t* pos, uint8_t val) {
    buf[(*pos)++] = val;
}

static void write_u16(uint8_t* buf, uint32_t* pos, uint16_t val) {
    buf[(*pos)++] = val & 0xFF;
    buf[(*pos)++] = (val >> 8) & 0xFF;
}

static void write_u32(uint8_t* buf, uint32_t* pos, uint32_t val) {
    buf[(*pos)++] = val & 0xFF;
    buf[(*pos)++] = (val >> 8) & 0xFF;
    buf[(*pos)++] = (val >> 16) & 0xFF;
    buf[(*pos)++] = (val >> 24) & 0xFF;
}

static void write_f32(uint8_t* buf, uint32_t* pos, float val) {
    uint32_t* p = (uint32_t*)&val;
    write_u32(buf, pos, *p);
}

static uint8_t read_u8(const uint8_t* buf, uint32_t* pos) {
    return buf[(*pos)++];
}

static uint16_t read_u16(const uint8_t* buf, uint32_t* pos) {
    uint16_t val = buf[*pos] | ((uint16_t)buf[*pos + 1] << 8);
    *pos += 2;
    return val;
}

static uint32_t read_u32(const uint8_t* buf, uint32_t* pos) {
    uint32_t val = buf[*pos] | ((uint32_t)buf[*pos+1] << 8)
                 | ((uint32_t)buf[*pos+2] << 16) | ((uint32_t)buf[*pos+3] << 24);
    *pos += 4;
    return val;
}

static float read_f32(const uint8_t* buf, uint32_t* pos) {
    uint32_t raw = read_u32(buf, pos);
    float* p = (float*)&raw;
    return *p;
}

/* ── Save TL to SD Card ── */

int ck_sd_save_tl(CK_BrainState* brain, const char* filename) {
    /*
     * Serialize brain state to binary buffer, then write to file.
     *
     * Max buffer size:
     *   Header: 13 bytes
     *   Matrix: 400 bytes
     *   Crystals: 2 + 256*18 = 4610 bytes
     *   Domains: 1 + 8*32 = 257 bytes
     *   CRC: 1 byte
     *   Total: ~5,281 bytes max
     */
    static uint8_t buf[6000];
    uint32_t pos = 0;

    /* Header */
    memcpy(buf + pos, TL_MAGIC, 4); pos += 4;
    write_u8(buf, &pos, TL_VERSION);
    write_u32(buf, &pos, brain->tl.total);
    write_f32(buf, &pos, brain->tl.entropy);

    /* TL Matrix: 10x10 transition counts */
    for (int i = 0; i < CK_NUM_OPS; i++) {
        for (int j = 0; j < CK_NUM_OPS; j++) {
            write_u32(buf, &pos, brain->tl.entries[i][j].count);
        }
    }

    /* Crystals */
    CK_Domain* dom = (brain->domain_count > 0) ? &brain->domains[0] : NULL;
    uint16_t nc = dom ? dom->crystal_count : 0;
    write_u16(buf, &pos, nc);

    for (int c = 0; c < nc; c++) {
        CK_Crystal* cr = &dom->crystals[c];
        for (int p = 0; p < 8; p++) write_u8(buf, &pos, cr->ops[p]);
        write_u8(buf, &pos, cr->len);
        write_u8(buf, &pos, cr->fuse);
        write_u32(buf, &pos, cr->seen);
        write_f32(buf, &pos, cr->confidence);
    }

    /* Domains */
    write_u8(buf, &pos, brain->domain_count);
    for (int d = 0; d < brain->domain_count; d++) {
        CK_Domain* dm = &brain->domains[d];
        /* Name (16 bytes, zero-padded) */
        memcpy(buf + pos, dm->name, 16); pos += 16;
        write_u8(buf, &pos, dm->dominant_op);
        write_f32(buf, &pos, dm->coherence);
        write_u8(buf, &pos, dm->is_sovereign ? 1 : 0);
        write_u16(buf, &pos, dm->sovereign_ticks);
        write_u16(buf, &pos, dm->crystal_count);
        /* Pad to 32 bytes */
        uint32_t domain_used = 16 + 1 + 4 + 1 + 2 + 2; /* = 26 */
        for (uint32_t p = domain_used; p < 32; p++) write_u8(buf, &pos, 0);
    }

    /* CRC over everything */
    uint8_t crc = crc8(buf, pos);
    write_u8(buf, &pos, crc);

    /*
     * Write to SD card via FatFs.
     * In actual Vitis project:
     *
     *   FATFS fs;
     *   FIL file;
     *   UINT bw;
     *   f_mount(&fs, "0:", 1);
     *   f_open(&file, filename, FA_WRITE | FA_CREATE_ALWAYS);
     *   f_write(&file, buf, pos, &bw);
     *   f_close(&file);
     *
     * Returns 0 on success, -1 on failure.
     */
    (void)filename;
    (void)buf;
    (void)pos;

    return 0;  /* Stub: always succeeds */
}

/* ── Load TL from SD Card ── */

int ck_sd_load_tl(CK_BrainState* brain, const char* filename) {
    /*
     * Read binary file from SD card, deserialize into brain state.
     *
     * In actual Vitis project:
     *   FATFS fs;
     *   FIL file;
     *   UINT br;
     *   f_mount(&fs, "0:", 1);
     *   FRESULT res = f_open(&file, filename, FA_READ);
     *   if (res != FR_OK) return -1;
     *   f_read(&file, buf, sizeof(buf), &br);
     *   f_close(&file);
     */
    static uint8_t buf[6000];
    uint32_t file_size = 0;

    /* Stub: pretend we read the file */
    (void)filename;
    (void)buf;

    if (file_size == 0) {
        /* No file found -- start fresh */
        return -1;
    }

    uint32_t pos = 0;

    /* Verify magic */
    if (memcmp(buf + pos, TL_MAGIC, 4) != 0) return -1;
    pos += 4;

    /* Version check */
    uint8_t ver = read_u8(buf, &pos);
    if (ver != TL_VERSION) return -1;

    /* Header */
    brain->tl.total = read_u32(buf, &pos);
    brain->tl.entropy = read_f32(buf, &pos);

    /* TL Matrix */
    for (int i = 0; i < CK_NUM_OPS; i++) {
        for (int j = 0; j < CK_NUM_OPS; j++) {
            brain->tl.entries[i][j].from_op = i;
            brain->tl.entries[i][j].to_op = j;
            brain->tl.entries[i][j].count = read_u32(buf, &pos);
        }
    }

    /* Crystals */
    uint16_t nc = read_u16(buf, &pos);
    if (brain->domain_count == 0) {
        brain->domain_count = 1;
        memset(&brain->domains[0], 0, sizeof(CK_Domain));
        strncpy(brain->domains[0].name, "default", 15);
    }
    CK_Domain* dom = &brain->domains[0];
    dom->crystal_count = (nc > CK_MAX_CRYSTALS) ? CK_MAX_CRYSTALS : nc;

    for (int c = 0; c < nc && c < CK_MAX_CRYSTALS; c++) {
        CK_Crystal* cr = &dom->crystals[c];
        for (int p = 0; p < 8; p++) cr->ops[p] = read_u8(buf, &pos);
        cr->len = read_u8(buf, &pos);
        cr->fuse = read_u8(buf, &pos);
        cr->seen = read_u32(buf, &pos);
        cr->confidence = read_f32(buf, &pos);
    }

    /* Domains */
    brain->domain_count = read_u8(buf, &pos);
    if (brain->domain_count > CK_MAX_DOMAINS) brain->domain_count = CK_MAX_DOMAINS;

    for (int d = 0; d < brain->domain_count; d++) {
        CK_Domain* dm = &brain->domains[d];
        memcpy(dm->name, buf + pos, 16); pos += 16;
        dm->dominant_op = read_u8(buf, &pos);
        dm->coherence = read_f32(buf, &pos);
        dm->is_sovereign = read_u8(buf, &pos) ? true : false;
        dm->sovereign_ticks = read_u16(buf, &pos);
        dm->crystal_count = read_u16(buf, &pos);
        pos += (32 - 26); /* Skip padding */
    }

    /* CRC verify */
    uint8_t stored_crc = buf[pos];
    uint8_t computed_crc = crc8(buf, pos);
    if (stored_crc != computed_crc) return -2; /* CRC mismatch */

    return 0;
}

int ck_sd_tl_exists(const char* filename) {
    /*
     * Check if file exists on SD card.
     * FatFs: f_stat(filename, NULL) == FR_OK
     */
    (void)filename;
    return 0; /* Stub */
}
