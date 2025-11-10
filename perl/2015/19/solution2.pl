#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 19: Medicine for Rudolph
# https://adventofcode.com/2015/day/19
#
# Part 2: Find minimum fabrication steps using mathematical formula

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part2
{
    my @lines = read_lines('input');
    my $molecule = $lines[-1];

    # Count atoms (uppercase letters)
    my $num_atoms = () = $molecule =~ /[A-Z]/g;

    # Count special tokens
    my $num_rn = () = $molecule =~ /Rn/g;
    my $num_ar = () = $molecule =~ /Ar/g;
    my $num_y = () = $molecule =~ /Y/g;

    # Apply the formula: atoms - Rn - Ar - (2 * Y) - 1
    my $steps = $num_atoms - $num_rn - $num_ar - (2 * $num_y) - 1;

    return $steps;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
