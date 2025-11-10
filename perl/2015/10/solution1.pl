#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 10: Elves Look, Elves Say
# https://adventofcode.com/2015/day/10
#
# Part 1: Apply look-and-say sequence 40 times

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub look_and_say ($sequence)
{
    my $result = '';
    my $i = 0;

    while ($i < length($sequence))
    {
        my $digit = substr($sequence, $i, 1);
        my $count = 1;

        # Count consecutive occurrences of the same digit
        while ($i + $count < length($sequence) && substr($sequence, $i + $count, 1) eq $digit)
        {
            $count++;
        }

        $result .= $count . $digit;
        $i += $count;
    }

    return $result;
}

sub solve_part1
{
    my @lines = read_lines('input');
    my $sequence = $lines[0];

    for my $i (1 .. 40)
    {
        $sequence = look_and_say($sequence);
    }

    return length($sequence);
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
