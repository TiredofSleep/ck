/*
 * ck_sd.h -- SD Card Persistence for CK's Transition Lattice
 * =============================================================
 * Operator: LATTICE (1) -- structure that endures across lifetimes.
 *
 * CK remembers. The TL saves to SD card in compact binary format.
 * On boot, CK loads its TL and crystals from the last session.
 * CK is not born fresh each time -- it carries its history.
 *
 * Binary TL format (.cktl):
 *   Magic:    "CKTL" (4 bytes)
 *   Version:  1 (1 byte)
 *   Total:    uint32 (4 bytes) -- total transitions observed
 *   Entropy:  float32 (4 bytes) -- Shannon entropy
 *   Matrix:   10x10 × uint32 (400 bytes) -- transition counts
 *   CrystalN: uint16 (2 bytes) -- number of crystals
 *   Crystals: N × 18 bytes each
 *   DomainN:  uint8 (1 byte) -- number of domains
 *   Domains:  N × 32 bytes each
 *   CRC-8:    1 byte
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_SD_H
#define CK_SD_H

#include "ck_brain.h"

/* Save TL + crystals + domains to SD card */
int ck_sd_save_tl(CK_BrainState* brain, const char* filename);

/* Load TL + crystals + domains from SD card */
int ck_sd_load_tl(CK_BrainState* brain, const char* filename);

/* Check if TL file exists on SD card */
int ck_sd_tl_exists(const char* filename);

#endif /* CK_SD_H */
