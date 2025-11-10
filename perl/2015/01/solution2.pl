#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 1, Part 2
# https://adventofcode.com/2015/day/1
#
# This script finds the position of the first character in the input
# that causes Santa to enter the basement (floor -1).

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part2
{
    my @lines = read_lines('input');
    my $instructions = $lines[0];

    my $floor = 0;
    my @chars = split //, $instructions;

    for my $idx (0 .. $#chars)
    {
        my $char = $chars[$idx];
        $floor++ if $char eq '(';
        $floor-- if $char eq ')';

        if ($floor == -1)
        {
            return $idx + 1;    # 1-based position
        }
    }

    return undef;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
