#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 17: No Such Thing as Too Much
# https://adventofcode.com/2015/day/17
#
# Part 2: Count combinations using minimum number of containers

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use List::Util qw(min);

sub solve_part2
{
    my @lines = read_lines('input');
    my @containers = map { int($_) } @lines;
    my $target = 150;
    my %combo_sizes;

    # Try all subsets using bitmask
    my $num_containers = scalar @containers;
    for my $mask (1 .. (2 ** $num_containers) - 1)
    {
        my $sum = 0;
        my $count = 0;
        for my $i (0 .. $num_containers - 1)
        {
            if ($mask & (1 << $i))
            {
                $sum += $containers[$i];
                $count++;
            }
        }

        if ($sum == $target)
        {
            $combo_sizes{$count}++;
        }
    }

    # Find minimum size and return its count
    my $min_size = min(keys %combo_sizes);
    return $combo_sizes{$min_size};
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
