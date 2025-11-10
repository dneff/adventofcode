#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 3: Perfectly Spherical Houses in a Vacuum
# https://adventofcode.com/2015/day/3
#
# Count how many houses receive at least one present.

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use AoC::Point qw(point NORTH SOUTH EAST WEST);

sub solve_part1
{
    my @lines = read_lines('input');
    my $path = $lines[0];

    my %directions = (
        '^' => NORTH,
        'v' => SOUTH,
        '>' => EAST,
        '<' => WEST,
    );

    my %houses;
    my $location = point(0, 0);
    $houses{ $location->as_hash_key }++;

    for my $char (split //, $path)
    {
        $location = $location + $directions{$char};
        $houses{ $location->as_hash_key }++;
    }

    return scalar keys %houses;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
