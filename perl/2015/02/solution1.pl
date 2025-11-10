#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 2: I Was Told There Would Be No Math
# https://adventofcode.com/2015/day/2
#
# Calculate the total wrapping paper needed for presents.

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution sum);
use List::Util qw(min);

sub get_wrapping ($l, $w, $h)
{
    my @sides = ($l * $w, $w * $h, $h * $l);
    my $wrapping = 2 * sum(@sides);
    my $slack = min(@sides);
    return $wrapping + $slack;
}

sub solve_part1
{
    my @lines = read_lines('input');

    my $total_wrapping = 0;
    for my $line (@lines)
    {
        my ($l, $w, $h) = split /x/, $line;
        $total_wrapping += get_wrapping($l, $w, $h);
    }

    return $total_wrapping;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
