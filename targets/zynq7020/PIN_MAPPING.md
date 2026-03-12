# PZ7020-StarLite Complete Pin Mapping
# Extracted from FPGA Schematics (Scribd clips), March 2026
# (c) 2026 Brayden Sanders / 7Site LLC

## Source
Schematic page "40P CON" showing JM1 (CON40) and JM2 (CON40)
FPGA: XC7Z020-2CLG400I, Banks 34 and 35

---

## JM1 -- 40-Pin Expansion Connector #1 (All Bank 35)

```
Header Pin | Row  | FPGA Ball | IO Pair        | XDC Index
-----------|------|-----------|----------------|----------
 1         | Left | VDD_5V    | (power)        | --
 2         | Right| VDD_3V3   | (power)        | --
 3         | Left | H16       | IO_13P_35      | jm1[24]
 4         | Right| E17       | IO_3P_35       | jm1[4]
 5         | Left | H17       | IO_13N_35      | jm1[25]
 6         | Right| D18       | IO_3N_35       | jm1[5]
 7         | Left | E18       | IO_5P_35       | jm1[8]
 8         | Right| F16       | IO_6P_35       | jm1[10]
 9         | Left | E19       | IO_5N_35       | jm1[9]
10         | Right| F17       | IO_6N_35       | jm1[11]
11         | Left | G17       | IO_16P_35      | jm1[30]
12         | Right| B19       | IO_2P_35       | jm1[2]
13         | Left | G18       | IO_16N_35      | jm1[31]
14         | Right| A20       | IO_2N_35       | jm1[3]
15         | Left | D19       | IO_4P_35       | jm1[6]
16         | Right| C20       | IO_1P_35       | jm1[0]
17         | Left | D20       | IO_4N_35       | jm1[7]
18         | Right| B20       | IO_1N_35       | jm1[1]
19         | Left | J18       | IO_14P_35      | jm1[26]
20         | Right| K19       | IO_10P_35      | jm1[18]
21         | Left | H18       | IO_14N_35      | jm1[27]
22         | Right| J19       | IO_10N_35      | jm1[19]
23         | Left | K17       | IO_12P_35      | jm1[22]
24         | Right| M17       | IO_8P_35       | jm1[14]
25         | Left | K18       | IO_12N_35      | jm1[23]
26         | Right| M18       | IO_8N_35       | jm1[15]
27         | Left | L16       | IO_11P_35      | jm1[20]
28         | Right| F19       | IO_15P_35      | jm1[28]
29         | Left | L17       | IO_11N_35      | jm1[21]
30         | Right| F20       | IO_15N_35      | jm1[29]
31         | Left | GND       | (ground)       | --
32         | Right| GND       | (ground)       | --
33         | Left | GND       | (ground)       | --
34         | Right| GND       | (ground)       | --
35         | Left | GND       | (ground)       | --
36         | Right| GND       | (ground)       | --
37         | Left | M19       | IO_7P_35       | jm1[12]
38         | Right| L19       | IO_9P_35       | jm1[16]
39         | Left | M20       | IO_7N_35       | jm1[13]
40         | Right| L20       | IO_9N_35       | jm1[17]
```

### JM1 Quick Lookup: Header Pin -> jm1 Index

```
Pin  3 -> jm1[24]    Pin  4 -> jm1[4]
Pin  5 -> jm1[25]    Pin  6 -> jm1[5]
Pin  7 -> jm1[8]     Pin  8 -> jm1[10]
Pin  9 -> jm1[9]     Pin 10 -> jm1[11]
Pin 11 -> jm1[30]    Pin 12 -> jm1[2]
Pin 13 -> jm1[31]    Pin 14 -> jm1[3]
Pin 15 -> jm1[6]     Pin 16 -> jm1[0]
Pin 17 -> jm1[7]     Pin 18 -> jm1[1]
Pin 19 -> jm1[26]    Pin 20 -> jm1[18]
Pin 21 -> jm1[27]    Pin 22 -> jm1[19]
Pin 23 -> jm1[22]    Pin 24 -> jm1[14]
Pin 25 -> jm1[23]    Pin 26 -> jm1[15]
Pin 27 -> jm1[20]    Pin 28 -> jm1[28]
Pin 29 -> jm1[21]    Pin 30 -> jm1[29]
Pin 37 -> jm1[12]    Pin 38 -> jm1[16]
Pin 39 -> jm1[13]    Pin 40 -> jm1[17]
```

---

## JM2 -- 40-Pin Expansion Connector #2 (Bank 35 upper + Bank 34)

```
Header Pin | Row  | FPGA Ball | IO Pair        | Bank | XDC Index
-----------|------|-----------|----------------|------|----------
 1         | Left | VDD_5V    | (power)        | --   | --
 2         | Right| VDD_3V3   | (power)        | --   | --
 3         | Left | G19       | IO_18P_35      | 35   | jm2[2]
 4         | Right| J20       | IO_17P_35      | 35   | jm2[0]
 5         | Left | G20       | IO_18N_35      | 35   | jm2[3]
 6         | Right| H20       | IO_17N_35      | 35   | jm2[1]
 7         | Left | H15       | IO_19P_35      | 35   | jm2[4]
 8         | Right| K14       | IO_20P_35      | 35   | jm2[6]
 9         | Left | G15       | IO_19N_35      | 35   | jm2[5]
10         | Right| J14       | IO_20N_35      | 35   | jm2[7]
11         | Left | K16       | IO_24P_35      | 35   | jm2[14]
12         | Right| L15       | IO_22P_35      | 35   | jm2[11]
13         | Left | J16       | IO_24N_35      | 35   | jm2[15]
14         | Right| L14       | IO_22N_35      | 35   | jm2[10]
15         | Left | N15       | IO_21P_35      | 35   | jm2[8]
16         | Right| M14       | IO_23P_35      | 35   | jm2[12]
17         | Left | N16       | IO_21N_35      | 35   | jm2[9]
18         | Right| M15       | IO_23N_35      | 35   | jm2[13]
19         | Left | T16       | IO_9P_34       | 34   | jm2[16]
20         | Right| T14       | IO_5P_34       | 34   | jm2[24]
21         | Left | U17       | IO_9N_34       | 34   | jm2[17]
22         | Right| T15       | IO_5N_34       | 34   | jm2[25]
23         | Left | P14       | IO_6P_34       | 34   | jm2[18]
24         | Right| T12       | IO_2P_34       | 34   | jm2[26]
25         | Left | R14       | IO_6N_34       | 34   | jm2[19]
26         | Right| U12       | IO_2N_34       | 34   | jm2[27]
27         | Left | T11       | IO_1P_34       | 34   | jm2[20]
28         | Right| Y16       | IO_7P_34       | 34   | jm2[28]
29         | Left | T10       | IO_1N_34       | 34   | jm2[21]
30         | Right| Y17       | IO_7N_34       | 34   | jm2[29]
31         | Left | GND       | (ground)       | --   | --
32         | Right| GND       | (ground)       | --   | --
33         | Left | GND       | (ground)       | --   | --
34         | Right| GND       | (ground)       | --   | --
35         | Left | GND       | (ground)       | --   | --
36         | Right| GND       | (ground)       | --   | --
37         | Left | V12       | IO_4P_34       | 34   | jm2[22]
38         | Right| W14       | IO_8P_34       | 34   | jm2[30]
39         | Left | W13       | IO_4N_34       | 34   | jm2[23]
40         | Right| Y14       | IO_8N_34       | 34   | jm2[31]
```

---

## XDC Index Cross-Reference

### JM1: XDC Index -> FPGA Ball -> Header Pin

```
jm1[0]  = C20 -> Pin 16      jm1[16] = L19 -> Pin 38
jm1[1]  = B20 -> Pin 18      jm1[17] = L20 -> Pin 40
jm1[2]  = B19 -> Pin 12      jm1[18] = K19 -> Pin 20
jm1[3]  = A20 -> Pin 14      jm1[19] = J19 -> Pin 22
jm1[4]  = E17 -> Pin  4      jm1[20] = L16 -> Pin 27
jm1[5]  = D18 -> Pin  6      jm1[21] = L17 -> Pin 29
jm1[6]  = D19 -> Pin 15      jm1[22] = K17 -> Pin 23
jm1[7]  = D20 -> Pin 17      jm1[23] = K18 -> Pin 25
jm1[8]  = E18 -> Pin  7      jm1[24] = H16 -> Pin  3
jm1[9]  = E19 -> Pin  9      jm1[25] = H17 -> Pin  5
jm1[10] = F16 -> Pin  8      jm1[26] = J18 -> Pin 19
jm1[11] = F17 -> Pin 10      jm1[27] = H18 -> Pin 21
jm1[12] = M19 -> Pin 37      jm1[28] = F19 -> Pin 28
jm1[13] = M20 -> Pin 39      jm1[29] = F20 -> Pin 30
jm1[14] = M17 -> Pin 24      jm1[30] = G17 -> Pin 11
jm1[15] = M18 -> Pin 26      jm1[31] = G18 -> Pin 13
```

---

## AT043TN24 FPC Pinout (from datasheet)

```
FPC Pin | Signal  | Type
--------|---------|------
  1     | VLED-   | Power (backlight cathode)
  2     | VLED+   | Power (backlight anode)
  3     | GND     | Power
  4     | VDD     | Power (3.3V)
  5-12  | R[0:7]  | Input (Red data)
 13-20  | G[0:7]  | Input (Green data)
 21-28  | B[0:7]  | Input (Blue data)
 29     | GND     | Power
 30     | PCLK    | Input (Pixel clock / DCLK)
 31     | DISP    | Input (Display on/off)
 32     | HSYNC   | Input (Horizontal sync)
 33     | VSYNC   | Input (Vertical sync)
 34     | DE      | Input (Data enable)
 35     | NC      | --
 36     | GND     | Power
 37-40  | Touch   | I/O (touch panel, if equipped)
```

---

## PZ-LCD430 Adapter: LCD Signal -> Header Pin -> jm1 Index

The PZ-LCD430 adapter board's internal FPC-to-header wiring is
**proprietary** (not published by Puzhi). Two conventions are
implemented in ck_top_full.v via the `LCD_PIN_CONV` parameter.

### Convention A (LCD_PIN_CONV = 0): Control signals first

Assumes adapter routes: control on pins 3-6, then RGB data on 7-30.

```
Header Pin | LCD Signal | FPC Pin | FPGA Ball | jm1 Index
-----------|------------|---------|-----------|----------
    3      | DCLK       |   30    |   H16     | jm1[24]
    4      | HSYNC      |   32    |   E17     | jm1[4]
    5      | VSYNC      |   33    |   H17     | jm1[25]
    6      | DE         |   34    |   D18     | jm1[5]
    7      | R[0]       |    5    |   E18     | jm1[8]
    8      | R[1]       |    6    |   F16     | jm1[10]
    9      | R[2]       |    7    |   E19     | jm1[9]
   10      | R[3]       |    8    |   F17     | jm1[11]
   11      | R[4]       |    9    |   G17     | jm1[30]
   12      | R[5]       |   10    |   B19     | jm1[2]
   13      | R[6]       |   11    |   G18     | jm1[31]
   14      | R[7]       |   12    |   A20     | jm1[3]
   15      | G[0]       |   13    |   D19     | jm1[6]
   16      | G[1]       |   14    |   C20     | jm1[0]
   17      | G[2]       |   15    |   D20     | jm1[7]
   18      | G[3]       |   16    |   B20     | jm1[1]
   19      | G[4]       |   17    |   J18     | jm1[26]
   20      | G[5]       |   18    |   K19     | jm1[18]
   21      | G[6]       |   19    |   H18     | jm1[27]
   22      | G[7]       |   20    |   J19     | jm1[19]
   23      | B[0]       |   21    |   K17     | jm1[22]
   24      | B[1]       |   22    |   M17     | jm1[14]
   25      | B[2]       |   23    |   K18     | jm1[23]
   26      | B[3]       |   24    |   M18     | jm1[15]
   27      | B[4]       |   25    |   L16     | jm1[20]
   28      | B[5]       |   26    |   F19     | jm1[28]
   29      | B[6]       |   27    |   L17     | jm1[21]
   30      | B[7]       |   28    |   F20     | jm1[29]
  31-36    | GND        |   --    |   GND     | --
   37      | BL         |   --    |   M19     | jm1[12]
   38      | (unused)   |   --    |   L19     | jm1[16]
   39      | DISP       |   --    |   M20     | jm1[13]
   40      | (unused)   |   --    |   L20     | jm1[17]
```

### Convention B (LCD_PIN_CONV = 1): FPC pass-through (data first)

Assumes adapter passes FPC signal pins sequentially to header:
FPC 5-28 (RGB data) -> Header 3-26, FPC 30-33 (control) -> Header 27-30,
FPC 34 (DE) -> Header 37. This is the simplest PCB routing.

```
Header Pin | LCD Signal | FPC Pin | FPGA Ball | jm1 Index
-----------|------------|---------|-----------|----------
    3      | R[0]       |    5    |   H16     | jm1[24]
    4      | R[1]       |    6    |   E17     | jm1[4]
    5      | R[2]       |    7    |   H17     | jm1[25]
    6      | R[3]       |    8    |   D18     | jm1[5]
    7      | R[4]       |    9    |   E18     | jm1[8]
    8      | R[5]       |   10    |   F16     | jm1[10]
    9      | R[6]       |   11    |   E19     | jm1[9]
   10      | R[7]       |   12    |   F17     | jm1[11]
   11      | G[0]       |   13    |   G17     | jm1[30]
   12      | G[1]       |   14    |   B19     | jm1[2]
   13      | G[2]       |   15    |   G18     | jm1[31]
   14      | G[3]       |   16    |   A20     | jm1[3]
   15      | G[4]       |   17    |   D19     | jm1[6]
   16      | G[5]       |   18    |   C20     | jm1[0]
   17      | G[6]       |   19    |   D20     | jm1[7]
   18      | G[7]       |   20    |   B20     | jm1[1]
   19      | B[0]       |   21    |   J18     | jm1[26]
   20      | B[1]       |   22    |   K19     | jm1[18]
   21      | B[2]       |   23    |   H18     | jm1[27]
   22      | B[3]       |   24    |   J19     | jm1[19]
   23      | B[4]       |   25    |   K17     | jm1[22]
   24      | B[5]       |   26    |   M17     | jm1[14]
   25      | B[6]       |   27    |   K18     | jm1[23]
   26      | B[7]       |   28    |   M18     | jm1[15]
   27      | DCLK       |   30    |   L16     | jm1[20]
   28      | DISP       |   31    |   F19     | jm1[28]
   29      | HSYNC      |   32    |   L17     | jm1[21]
   30      | VSYNC      |   33    |   F20     | jm1[29]
  31-36    | GND        |   --    |   GND     | --
   37      | DE         |   34    |   M19     | jm1[12]
   38      | BL         |   --    |   L19     | jm1[16]
   39      | (unused)   |   --    |   M20     | jm1[13]
   40      | (unused)   |   --    |   L20     | jm1[17]
```

---

## Other Board Connections (from schematics pages 2-7)

- **PL Clock**: 50 MHz oscillator (Y2) -> U18
- **LED1**: R19 (active-low, Bank 34)
- **LED2**: V13 (active-low, Bank 34)
- **KEY1**: G14 (active-low, Bank 35)
- **KEY2**: J15 (active-low, Bank 35)
- **Page 2**: USB 2.0 Host + SD Card (both PS-side, MIO)
- **Page 3**: PS DDR3 (512MB) + USB-to-UART (PS MIO)
- **HDMI**: Bank 34 TMDS (W18/W19 clk, R16/R17 d0, T17/R18 d1, V17/V18 d2)

---

## Notes

1. JM1 uses ALL of PL Bank 35 (16 differential IO pairs = 32 pins)
2. JM2 uses Bank 35 upper pairs (IO_17-24) + Bank 34 IOs
3. XDC indices are ordered by IO PAIR NUMBER, NOT by header pin number
4. The PZ-LCD430 adapter board plugs into JM1
5. Header pins 1/2 are power (5V/3.3V), pins 31-36 are GND
6. Pins 37-40 are IO but past the GND block (used for control signals)
7. PZ-LCD430 adapter wiring is proprietary -- two conventions supported
8. To switch: change LCD_PIN_CONV in ck_top_full.v (0=Conv A, 1=Conv B)
