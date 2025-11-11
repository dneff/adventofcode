# Advent of Code 2015 - Day 1 Makefile

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -O2 -I../../lib
LDFLAGS = -lm

# Library files
LIB_DIR = ../../lib
LIB_SRCS = $(LIB_DIR)/aoc_utils.c $(LIB_DIR)/aoc_input.c $(LIB_DIR)/aoc_point.c $(LIB_DIR)/aoc_grid.c $(LIB_DIR)/aoc_math.c
LIB_OBJS = $(LIB_SRCS:.c=.o)

# Solution binaries
SOLUTIONS = solution1 solution2

.PHONY: all clean run

all: $(SOLUTIONS)

solution1: solution1.c $(LIB_OBJS)
	$(CC) $(CFLAGS) -o $@ $< $(LIB_OBJS) $(LDFLAGS)

solution2: solution2.c $(LIB_OBJS)
	$(CC) $(CFLAGS) -o $@ $< $(LIB_OBJS) $(LDFLAGS)

# Build library objects if needed
$(LIB_DIR)/%.o: $(LIB_DIR)/%.c
	$(MAKE) -C ../.. lib

run: all
	@echo "Running Part 1:"
	@./solution1
	@echo ""
	@echo "Running Part 2:"
	@./solution2

clean:
	rm -f $(SOLUTIONS)
