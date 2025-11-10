#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 20: Infinite Elves and Infinite Houses
# https://adventofcode.com/2015/day/20
#
# Part 2: Elves deliver 11x presents but stop after 50 houses

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part2
{
    my @lines = read_lines('input');
    my $target = int($lines[0]);

    # Upper bound estimate
    my $max_house = int($target / 11);
    my @presents = (0) x ($max_house + 1);

    # Sieve: each elf delivers to their multiples (max 50 houses)
    for my $elf (1 .. $max_house)
    {
        my $presents_to_deliver = 11 * $elf;
        my $house_count = 0;

        for (my $house = $elf; $house <= $max_house && $house_count < 50; $house += $elf)
        {
            $presents[$house] += $presents_to_deliver;
            $house_count++;
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
my $answer = solve_part2();
print_solution(2, $answer);
