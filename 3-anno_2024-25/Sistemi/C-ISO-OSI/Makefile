###############################################################################
# Makefile for ISO/OSI Simulation Project (fixed include path)
#
# - Ensures "constants.h" in the repo root is found by adding -I. (dot) to CFLAGS
# - Assumes this directory structure:
#     .
#     ├── constants.h
#     ├── main.c
#     ├── level1/
#     │   ├── level1_fisic.c
#     │   └── level1_fisic.h
#     ├── level2/
#     │   ├── level2_datalink.c
#     │   └── level2_datalink.h
#     ├── level3/
#     │   ├── level3_network.c
#     │   └── level3_network.h
#     ├── level4/
#     │   ├── level4_transport.c
#     │   └── level4_transport.h
#     ├── level5/
#     │   ├── level5_session.c
#     │   └── level5_session.h
#     ├── level6/
#     │   ├── level6_presentation.c
#     │   └── level6_presentation.h
#     └── level7/
#         ├── level7_application.c
#         └── level7_application.h
#
# - Produces a single executable named "osi_simulation"
# - Uses gcc, with -Wall -Wextra -std=c11, and includes each level directory plus the root
# - Supports a "clean" target to remove object files and the binary
###############################################################################

#----------------------------------------
# 1) Compiler and flags
#----------------------------------------
CC      := gcc
CFLAGS  := -Wall -Wextra -g

# Include project root so that constants.h is found:
CFLAGS  += -I.

# Include each levelN/ folder for its own headers
LEVEL_DIRS := level1 level2 level3 level4 level5 level6 level7
CFLAGS     += $(addprefix -I,$(LEVEL_DIRS))

#----------------------------------------
# 2) Source files and object files
#----------------------------------------
# Gather all .c files under level*/ and also main.c
SRCS   := main.c $(wildcard level1/*.c) $(wildcard level2/*.c) \
           $(wildcard level3/*.c) $(wildcard level4/*.c) \
           $(wildcard level5/*.c) $(wildcard level6/*.c) \
           $(wildcard level7/*.c)

# Convert each .c to .o for object files
OBJS   := $(SRCS:.c=.o)

#----------------------------------------
# 3) Target executable
#----------------------------------------
TARGET := osi_simulation

#----------------------------------------
# 4) Default rule: build the executable
#----------------------------------------
.PHONY: all
all: $(TARGET)

# Link all object files into the final executable
$(TARGET): $(OBJS)
	@echo "Linking all modules → $(TARGET)"
	$(CC) $(CFLAGS) $^ -o $@

#----------------------------------------
# 5) Compile rule: .c → .o
#----------------------------------------
%.o: %.c
	@echo "Compiling $< → $@"
	$(CC) $(CFLAGS) -c $< -o $@

#----------------------------------------
# 6) Clean up
#----------------------------------------
.PHONY: clean
clean:
	@echo "Removing object files and '$(TARGET)'"
	rm -f $(OBJS) $(TARGET)

#----------------------------------------
# 7) Phony target for force rebuild
#----------------------------------------
.PHONY: rebuild
rebuild: clean all

###############################################################################
# Usage:
#
#   make           # builds 'osi_simulation'
#   make clean     # removes all *.o and the 'osi_simulation' binary
#   make rebuild   # same as 'make clean' then 'make'
#
# Notes:
#   - The "-I." in CFLAGS ensures that "constants.h" (in the repo root)
#     is visible to all levelN/*.c files.
#   - Each levelN folder is also in the include path, so #include "levelX_*.h"
#     works without specifying a relative path.
###############################################################################
