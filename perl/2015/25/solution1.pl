#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 25: Let It Snow
# https://adventofcode.com/2015/day/25
#
# Part 1: Calculate code at specific grid position

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub next_code ($code)
{
    return 20151125 if $code == 0;
    return ($code * 252533) % 33554393;
}

sub get_iterations ($row, $col)
{
    # Calculate position in diagonal traversal
    my $max_row = $row + $col - 1;
    my $iterations = ($max_row * ($max_row - 1)) / 2;
    $iterations += $col;
    return $iterations;
}

sub solve_part1
{
    my @lines = read_lines('input');
    my $line = $lines[0];

    # Parse: "To continue, please consult the code grid in the manual.  Enter the code at row 2978, column 3083."
    my ($row, $col) = $line =~ /row (\d+), column (\d+)/;

    my $code = 0;
    for (1 .. get_iterations($row, $col))
    {
        $code = next_code($code);
    }

    return $code;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
