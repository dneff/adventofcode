# Perl Solutions for Advent of Code

This directory contains Perl implementations of Advent of Code solutions, leveraging Perl's powerful text processing capabilities, extensive CPAN ecosystem, and modern language features.

## Requirements

- Perl 5.40 or later (for modern features like subroutine signatures)
- cpanminus for installing dependencies (optional but recommended)

### Installing Perl

**macOS (with Homebrew):**
```bash
brew install perl
```

**Ubuntu/Debian:**
```bash
sudo apt-get install perl
```

**Installing cpanminus:**
```bash
curl -L https://cpanmin.us | perl - App::cpanminus
```

## Installation

Install CPAN dependencies:

```bash
cd perl
cpanm --installdeps .
```

Or manually install key modules:

```bash
cpanm Algorithm::Combinatorics Math::BigInt Memoize Digest::MD5
```

## Directory Structure

```
perl/
├── README.md              # This file
├── cpanfile               # CPAN dependencies
├── .perltidyrc            # Code formatting configuration
├── lib/AoC/               # Helper modules
│   ├── Input.pm           # File I/O and parsing utilities
│   ├── Point.pm           # 2D point class with operator overloading
│   ├── Grid.pm            # 2D grid operations
│   ├── Math.pm            # Mathematical utilities
│   └── Utils.pm           # Common utility functions
├── verify_solutions.pl    # Solution verification script
└── 2015/                  # Year 2015 solutions
    ├── 01/
    │   ├── solution1.pl
    │   └── solution2.pl
    └── ...
```

## Running Solutions

Solutions are organized by year and day. Each day has two parts:

```bash
# Run from the perl directory
perl 2015/01/solution1.pl
perl 2015/01/solution2.pl

# Or make them executable and run directly
chmod +x 2015/01/solution1.pl
./2015/01/solution1.pl
```

## Helper Library Usage

The helper library provides reusable modules for common Advent of Code tasks.

### Input Module (AoC::Input)

Reading and parsing input files:

```perl
use lib '../../lib';
use AoC::Input qw(read_lines read_text read_numbers parse_numbers);

# Read file as array of lines
my @lines = read_lines('input');

# Read entire file as string
my $text = read_text('input');

# Read file as array of integers
my @numbers = read_numbers('input');

# Extract all numbers from text
my @nums = parse_numbers($text);

# Read file split by blank lines
my @paragraphs = read_paragraphs('input');

# Read as 2D grid
my $grid = read_grid('input');
```

### Point Module (AoC::Point)

2D coordinate handling with operator overloading:

```perl
use lib '../../lib';
use AoC::Point qw(point manhattan_distance NORTH SOUTH EAST WEST);

# Create points
my $p1 = point(3, 4);
my $p2 = point(1, 2);

# Arithmetic operations
my $p3 = $p1 + $p2;           # point(4, 6)
my $p4 = $p1 - $p2;           # point(2, 2)
my $p5 = $p1 * 2;             # point(6, 8)

# Comparison
if ($p1 == $p2) { ... }

# Movement with direction constants
my $next = $p1 + NORTH;       # Move up
my $next = $p1 + EAST;        # Move right

# Neighbors
my @neighbors4 = $p1->neighbors4();   # 4 orthogonal
my @neighbors8 = $p1->neighbors8();   # 8 including diagonals

# Distance
my $dist = manhattan_distance($p1, $p2);

# Hash key
my $key = $p1->as_hash_key();  # "3,4"
```

### Grid Module (AoC::Grid)

2D grid operations:

```perl
use lib '../../lib';
use AoC::Grid qw(make_grid grid_get grid_set grid_neighbors4);
use AoC::Point qw(point);

# Create grid from array of strings
my @rows = read_lines('input');
my $grid = make_grid(\@rows);

# Access grid cells
my $value = grid_get($grid, point(3, 4));
grid_set($grid, point(3, 4), 'X');

# Find values
my $pos = grid_find($grid, 'S');        # First occurrence
my @positions = grid_find_all($grid, '#');  # All occurrences

# Get neighbors
my @neighbors = grid_neighbors4($grid, point(3, 4));
my @all = grid_neighbors8($grid, point(3, 4));

# Grid properties
my $width = grid_width($grid);
my $height = grid_height($grid);

# Check bounds
if (grid_in_bounds($grid, $pos)) { ... }

# Print grid
grid_print($grid);
```

### Math Module (AoC::Math)

Mathematical utilities:

```perl
use lib '../../lib';
use AoC::Math qw(gcd lcm primes_up_to factorial binomial);

# GCD and LCM
my $g = gcd(48, 18);                  # 6
my $l = lcm(12, 18);                  # 36
my $g2 = gcd_list(48, 18, 24);        # 6
my $l2 = lcm_list(12, 18, 24);        # 72

# Primes
my $is_p = is_prime(17);              # 1 (true)
my @primes = primes_up_to(100);       # All primes up to 100

# Factors and divisors
my @factors = factors(60);            # (2, 2, 3, 5)
my @divs = divisors(12);              # (1, 2, 3, 4, 6, 12)

# Combinatorics
my $fact = factorial(5);              # 120
my $comb = binomial(5, 2);            # 10

# Utilities
my $s = sign(-5);                     # -1
my $c = clamp(15, 0, 10);             # 10
```

### Utils Module (AoC::Utils)

Common utility functions:

```perl
use lib '../../lib';
use AoC::Utils qw(print_solution count_if frequencies sum product);

# Print solution
print_solution(1, 42);                # "Part 1: 42"

# Counting and filtering
my $count = count_if { $_ > 5 } @numbers;

# Frequencies
my %freq = frequencies(@items);
# %freq = ('a' => 3, 'b' => 2, 'c' => 1)

# Grouping
my $groups = group_by { length $_ } @words;
# { 3 => ['cat', 'dog'], 4 => ['bear'] }

# Min/max by custom criteria
my $min = min_by { abs($_ - 10) } @numbers;
my $max = max_by { $_->{score} } @items;

# Math operations
my $total = sum(@numbers);
my $prod = product(@numbers);

# Unique elements
my @unique = uniq(@list);

# String trimming
my $trimmed = trim("  hello  ");     # "hello"
```

## Solution Template

Here's a typical solution structure:

```perl
#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 1: Not Quite Lisp
# https://adventofcode.com/2015/day/1

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part1 {
    my @lines = read_lines('input');

    # Solution logic here
    my $answer = 0;

    return $answer;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
```

## Verifying Solutions

Use the verification script to check solutions against known answers:

```bash
# Verify all solutions
perl verify_solutions.pl

# Verify specific year
perl verify_solutions.pl 2015

# Verify specific day
perl verify_solutions.pl 2015 1

# Write missing answers to aoc-data
perl verify_solutions.pl --write-missing
perl verify_solutions.pl 2015 --write-missing
```

## Code Style

This project follows modern Perl best practices:

- **Perl 5.40+** features including subroutine signatures
- **perltidy** for consistent formatting (see `.perltidyrc`)
- **perlcritic** for code quality (severity level 3)
- Comprehensive POD documentation in modules
- Clear variable names and comments

Format code with:
```bash
perltidy -b script.pl
```

Check code quality with:
```bash
perlcritic --severity 3 script.pl
```

## Perl Features Showcased

These solutions demonstrate idiomatic Perl patterns:

- **Regular expressions** for powerful text parsing
- **Operator overloading** for intuitive Point arithmetic
- **List::Util** and **List::MoreUtils** for functional programming
- **Hash and array manipulation** for data structures
- **Subroutine signatures** for clear function interfaces
- **Postfix dereferencing** for readable code
- **CPAN modules** for complex algorithms (combinatorics, etc.)

## Input Files

Solutions expect input files at:
```
../../../aoc-data/YEAR/DAY/input
```

This path is relative to each solution script. The `AoC::Input` module automatically handles this path resolution.

## Common Patterns

### Reading and Processing Lines
```perl
my @lines = read_lines('input');
my $result = sum(map { process_line($_) } @lines);
```

### Grid Traversal
```perl
my $grid = read_grid('input');
my $start = grid_find($grid, 'S');

my %visited;
my @queue = ($start);

while (@queue) {
    my $pos = shift @queue;
    next if $visited{$pos->as_hash_key}++;

    for my $next (grid_neighbors4($grid, $pos)) {
        push @queue, $next if grid_get($grid, $next) ne '#';
    }
}
```

### Pattern Matching
```perl
my @lines = read_lines('input');
for my $line (@lines) {
    if ($line =~ /(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\./) {
        my ($person1, $sign, $amount, $person2) = ($1, $2, $3, $4);
        # Process...
    }
}
```

## Resources

- [Perl Documentation](https://perldoc.perl.org/)
- [Modern Perl Book](http://modernperlbooks.com/)
- [CPAN](https://metacpan.org/)
- [Advent of Code](https://adventofcode.com/)

## Author

Advent of Code Solutions Collection
