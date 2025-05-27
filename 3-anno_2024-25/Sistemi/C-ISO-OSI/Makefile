###############################################################################
# Makefile for ISO/OSI Simulation Project (Linux + MinGW-w64 support)
#
# Supports PLATFORM=linux (default) or PLATFORM=mingw for Windows cross-compile
# Adds -I. for constants.h and includes all levelN/ directories
###############################################################################

#----------------------------------------
# 1) Platform and Compiler Selection
#----------------------------------------
# Choose platform: "linux" (default) or "mingw"
PLATFORM ?= linux

ifeq ($(PLATFORM), mingw)
    CC := x86_64-w64-mingw32-gcc
    TARGET := osi_simulation.exe
    CFLAGS := -Wall -Wextra -g
    CFLAGS += -DPLATFORM_WINDOWS
else
    CC := gcc
    TARGET := osi_simulation
    CFLAGS := -Wall -Wextra -g
    CFLAGS += -DPLATFORM_LINUX
endif

# Include root directory (for constants.h) and levelN folders
CFLAGS += -I.
LEVEL_DIRS := level1 level2 level3 level4 level5 level6 level7
CFLAGS += $(addprefix -I,$(LEVEL_DIRS))

#----------------------------------------
# 2) Source files and object files
#----------------------------------------
SRCS := main.c $(wildcard level1/*.c) $(wildcard level2/*.c) \
        $(wildcard level3/*.c) $(wildcard level4/*.c) \
        $(wildcard level5/*.c) $(wildcard level6/*.c) \
        $(wildcard level7/*.c)

OBJS := $(SRCS:.c=.o)

#----------------------------------------
# 3) Default rule: build the executable
#----------------------------------------
.PHONY: all
all: $(TARGET)

$(TARGET): $(OBJS)
	@echo "Linking all modules → $(TARGET)"
	$(CC) $(CFLAGS) $^ -o $@

#----------------------------------------
# 4) Compile rule: .c → .o
#----------------------------------------
%.o: %.c
	@echo "Compiling $< → $@"
	$(CC) $(CFLAGS) -c $< -o $@

#----------------------------------------
# 5) Clean up
#----------------------------------------
.PHONY: clean
clean:
	@echo "Removing object files and '$(TARGET)'"
	rm -f $(OBJS) $(TARGET)

#----------------------------------------
# 6) Force rebuild
#----------------------------------------
.PHONY: rebuild
rebuild: clean all

###############################################################################
# Usage:
#
#   make                    # builds 'osi_simulation' for Linux
#   make PLATFORM=mingw     # builds 'osi_simulation.exe' for Windows (cross)
#   make clean              # removes all *.o and the executable
#   make rebuild            # cleans and rebuilds
#
# Notes:
#   - Requires MinGW-w64 cross compiler for PLATFORM=mingw:
#       sudo apt install mingw-w64
#   - PLATFORM_WINDOWS and PLATFORM_LINUX macros allow conditional C code
###############################################################################
