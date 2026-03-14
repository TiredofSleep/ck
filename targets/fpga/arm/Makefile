# Makefile -- CK Brain (Bare Metal ARM for Zynq-7020)
# Cross-compile with arm-none-eabi-gcc from Vitis toolchain
#
# Usage:
#   make            -- build ck_brain.elf
#   make clean      -- remove build artifacts
#   make TOOLCHAIN_PATH=C:/path/to/bin  -- specify toolchain

# Toolchain (try Vitis, then PATH)
TOOLCHAIN_PATH ?= C:/amddesigntools/2025.2/Vitis/gnu/aarch32/nt/gcc-arm-none-eabi/bin
CC      = $(TOOLCHAIN_PATH)/arm-none-eabi-gcc
OBJCOPY = $(TOOLCHAIN_PATH)/arm-none-eabi-objcopy
SIZE    = $(TOOLCHAIN_PATH)/arm-none-eabi-size

# Target
TARGET  = ck_brain

# CPU flags for Cortex-A9
CFLAGS  = -mcpu=cortex-a9 -mfpu=neon-fp16 -mfloat-abi=hard
CFLAGS += -O2 -g -Wall -Wno-unused-function
CFLAGS += -ffreestanding -nostdlib
CFLAGS += -I.

# Linker flags
LDFLAGS = -T lscript.ld -nostartfiles -nostdlib
LDFLAGS += -Wl,--gc-sections
LIBS    = -lgcc -lm

# Source files
SRCS_C  = ck_main.c ck_brain.c ck_body.c ck_led.c ck_audio.c \
          ck_ears.c ck_uart.c ck_sd.c ck_core1.c ck_dog_steer.c \
          ck_usb_host.c
SRCS_S  = boot.S

# Object files
OBJS    = $(SRCS_S:.S=.o) $(SRCS_C:.c=.o)

# Rules
all: $(TARGET).elf
	@echo ""
	@echo "  CK Brain built: $(TARGET).elf"
	@$(SIZE) $(TARGET).elf
	@echo ""

$(TARGET).elf: $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

%.o: %.S
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET).elf $(TARGET).bin

# Copy ELF to build directory for bootgen
install: $(TARGET).elf
	cp $(TARGET).elf ../build/$(TARGET).elf
	@echo "  Copied to ../build/$(TARGET).elf"

.PHONY: all clean install
