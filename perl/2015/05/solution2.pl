#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 5, Part 2
# https://adventofcode.com/2015/day/5
#
# Count how many strings are "nice" according to the new rules.

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub has_pair_twice ($s)
{
    # Check if any pair of letters appears at least twice without overlapping
    return $s =~ /(..).*\1/;
}

sub has_repeat_with_gap ($s)
{
    # Check if any letter repeats with exactly one letter between them
    return $s =~ /(.).\1/;
}

sub is_nice ($s)
{
    return has_pair_twice($s) && has_repeat_with_gap($s);
}

sub solve_part2
{
    my @lines = read_lines('input');

    my $nice_count = 0;
    for my $line (@lines)
    {
        $nice_count++ if is_nice($line);
    }

    return $nice_count;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
