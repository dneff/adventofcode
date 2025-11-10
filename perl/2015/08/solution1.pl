#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 8: Matchsticks
# https://adventofcode.com/2015/day/8
#
# Part 1: Calculate difference between code representation and in-memory string

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part1
{
    my @lines = read_lines('input');
    my $diff = 0;

    for my $line (@lines)
    {
        my $code_length = length($line);

        # Remove surrounding quotes
        my $processed = substr($line, 1, -1);

        # Process escape sequences
        # \\ -> \
        # \" -> "
        # \xHH -> single character
        $processed =~ s/\\\\/_/g;      # Replace \\ with placeholder
        $processed =~ s/\\\"/"/g;       # Replace \" with "
        $processed =~ s/\\x[0-9a-f]{2}/_/g;  # Replace \xHH with placeholder

        my $mem_length = length($processed);
        $diff += $code_length - $mem_length;
    }

    return $diff;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
