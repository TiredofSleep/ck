# Makefile for AO -- Advanced Ollie (C implementation)
# Builds both standalone binary and shared library
#
# Usage:
#   make        -> ao (or ao.exe on Windows)
#   make lib    -> libao.dll / libao.so / libao.dylib
#   make clean  -> remove build artifacts

CC      = gcc
CFLAGS  = -O2 -Wall -Wextra -std=c99 -pedantic
LDFLAGS = -lm

SRCS    = ao_earth.c ao_air.c ao_water.c ao_fire.c ao_ether.c
OBJS    = $(SRCS:.c=.o)

# ── Standalone binary ──
ao: $(OBJS) ao_main.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

ao_main.o: ao_main.c ao_ether.h
	$(CC) $(CFLAGS) -c $<

# ── Shared library ──
ifeq ($(OS),Windows_NT)
  LIBNAME  = libao.dll
  LIBFLAGS = -shared
else
  UNAME := $(shell uname)
  ifeq ($(UNAME),Darwin)
    LIBNAME  = libao.dylib
    LIBFLAGS = -shared -dynamiclib
  else
    LIBNAME  = libao.so
    LIBFLAGS = -shared
  endif
endif

LIB_OBJS = $(SRCS:.c=.lib.o)

%.lib.o: %.c
	$(CC) $(CFLAGS) -fPIC -DAO_BUILD_LIB -c $< -o $@

$(LIBNAME): $(LIB_OBJS)
	$(CC) $(CFLAGS) $(LIBFLAGS) -o $@ $^ $(LDFLAGS)

lib: $(LIBNAME)

# ── Pattern rules ──
%.o: %.c
	$(CC) $(CFLAGS) -c $<

# ── Dependencies ──
ao_earth.o ao_earth.lib.o: ao_earth.c ao_earth.h ao_earth_data.inc
ao_air.o ao_air.lib.o:     ao_air.c ao_air.h ao_earth.h
ao_water.o ao_water.lib.o: ao_water.c ao_water.h ao_earth.h ao_air.h
ao_fire.o ao_fire.lib.o:   ao_fire.c ao_fire.h ao_earth.h
ao_ether.o ao_ether.lib.o: ao_ether.c ao_ether.h ao_earth.h ao_air.h ao_water.h ao_fire.h

# ── Codegen (regenerate data from Python) ──
gen: gen_earth_data.py
	cd .. && python src/gen_earth_data.py > src/ao_earth_data.inc

# ── Clean ──
clean:
	rm -f *.o ao ao.exe $(LIBNAME) libao.a

.PHONY: clean lib gen
