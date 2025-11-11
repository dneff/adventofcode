# Advent of Code C Solutions - Main Makefile

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -O2 -I./lib
LDFLAGS = -lm

# Library source files
LIB_SRCS = lib/aoc_utils.c lib/aoc_input.c lib/aoc_point.c lib/aoc_grid.c lib/aoc_math.c
LIB_OBJS = $(LIB_SRCS:.c=.o)

# Verification script
VERIFY_SRC = verify_solutions.c
VERIFY_BIN = verify_solutions

.PHONY: all clean lib verify help

all: lib

# Build the helper library
lib: $(LIB_OBJS)

# Build verification script
verify: $(VERIFY_BIN)

$(VERIFY_BIN): $(VERIFY_SRC) $(LIB_OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Pattern rule for object files
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

# Clean build artifacts
clean:
	rm -f $(LIB_OBJS)
	rm -f $(VERIFY_BIN)
	find . -type f -name "solution1" -o -name "solution2" | xargs rm -f

# Clean and rebuild
rebuild: clean all

help:
	@echo "Advent of Code C Solutions - Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  all       - Build the helper library (default)"
	@echo "  lib       - Build the helper library"
	@echo "  verify    - Build the verification script"
	@echo "  clean     - Remove all build artifacts"
	@echo "  rebuild   - Clean and rebuild everything"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "To build and run a specific solution:"
	@echo "  cd YEAR/DAY"
	@echo "  make"
	@echo "  ./solution1"
	@echo "  ./solution2"

# Dependencies
lib/aoc_utils.o: lib/aoc_utils.c lib/aoc_utils.h
lib/aoc_input.o: lib/aoc_input.c lib/aoc_input.h lib/aoc_utils.h
lib/aoc_point.o: lib/aoc_point.c lib/aoc_point.h
lib/aoc_grid.o: lib/aoc_grid.c lib/aoc_grid.h lib/aoc_point.h
lib/aoc_math.o: lib/aoc_math.c lib/aoc_math.h
