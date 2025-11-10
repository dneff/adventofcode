#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 20: Infinite Elves and Infinite Houses
# https://adventofcode.com/2015/day/20
#
# Part 1: Find first house to receive target presents

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part1
{
    my @lines = read_lines('input');
    my $target = int($lines[0]);

    # Upper bound estimate
    my $max_house = int($target / 30);
    my @presents = (0) x ($max_house + 1);

    # Sieve: each elf delivers to their multiples
    for my $elf (1 .. $max_house)
    {
        my $presents_to_deliver = 10 * $elf;

        for (my $house = $elf; $house <= $max_house; $house += $elf)
        {
            $presents[$house] += $presents_to_deliver;
        }
    }

    # Find first house with enough presents
    for my $house (1 .. $max_house)
    {
        return $house if $presents[$house] >= $target;
    }

    return 0;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
