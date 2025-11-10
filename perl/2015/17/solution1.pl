#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 17: No Such Thing as Too Much
# https://adventofcode.com/2015/day/17
#
# Part 1: Count combinations of containers that hold exactly 150 liters

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part1
{
    my @lines = read_lines('input');
    my @containers = map { int($_) } @lines;
    my $target = 150;
    my $valid_combos = 0;

    # Try all subsets using bitmask
    my $num_containers = scalar @containers;
    for my $mask (1 .. (2 ** $num_containers) - 1)
    {
        my $sum = 0;
        for my $i (0 .. $num_containers - 1)
        {
            if ($mask & (1 << $i))
            {
                $sum += $containers[$i];
            }
        }

        $valid_combos++ if $sum == $target;
    }

    return $valid_combos;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
