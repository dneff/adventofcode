#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 2, Part 2
# https://adventofcode.com/2015/day/2
#
# Calculate the total ribbon needed for presents.

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use List::Util qw(min);

sub get_ribbon ($l, $w, $h)
{
    my @perimeters = ($l + $w, $w + $h, $h + $l);
    my $ribbon = 2 * min(@perimeters);
    return $ribbon;
}

sub get_bow ($l, $w, $h)
{
    return $l * $w * $h;
}

sub solve_part2
{
    my @lines = read_lines('input');

    my $total_ribbon = 0;
    for my $line (@lines)
    {
        my ($l, $w, $h) = split /x/, $line;
        $total_ribbon += get_ribbon($l, $w, $h);
        $total_ribbon += get_bow($l, $w, $h);
    }

    return $total_ribbon;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
