#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 8: Matchsticks
# https://adventofcode.com/2015/day/8
#
# Part 2: Calculate difference when re-encoding strings

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part2
{
    my @lines = read_lines('input');
    my $diff = 0;

    for my $line (@lines)
    {
        my $original_length = length($line);

        # Encode: escape backslashes and quotes, then wrap in quotes
        my $encoded = $line;
        $encoded =~ s/\\/\\\\/g;    # \ -> \\
        $encoded =~ s/"/\\"/g;       # " -> \"
        $encoded = '"' . $encoded . '"';

        my $encoded_length = length($encoded);
        $diff += $encoded_length - $original_length;
    }

    return $diff;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
