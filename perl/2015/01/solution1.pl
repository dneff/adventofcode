#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 1: Not Quite Lisp
# https://adventofcode.com/2015/day/1
#
# This script calculates the final floor Santa ends up on after following
# the instructions in the input file.
# Each '(' means go up one floor, each ')' means go down one floor.

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part1
{
    my @lines = read_lines('input');
    my $instructions = $lines[0];

    my $floor = 0;
    for my $char (split //, $instructions)
    {
        $floor++ if $char eq '(';
        $floor-- if $char eq ')';
    }

    return $floor;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
