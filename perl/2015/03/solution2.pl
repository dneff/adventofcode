#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 3, Part 2
# https://adventofcode.com/2015/day/3
#
# Count how many houses receive at least one present from Santa or Robo-Santa.

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use AoC::Point qw(point NORTH SOUTH EAST WEST);

sub solve_part2
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
    my @locations = (point(0, 0), point(0, 0));    # Santa and Robo-Santa

    # Mark starting location
    for my $loc (@locations)
    {
        $houses{ $loc->as_hash_key }++;
    }

    my @chars = split //, $path;
    for my $idx (0 .. $#chars)
    {
        my $char = $chars[$idx];
        my $turn = $idx % 2;

        $locations[$turn] = $locations[$turn] + $directions{$char};
        $houses{ $locations[$turn]->as_hash_key }++;
    }

    return scalar keys %houses;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
