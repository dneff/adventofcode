#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 24: It Hangs in the Balance
# https://adventofcode.com/2015/day/24
#
# Part 2: Find minimum quantum entanglement for 4 groups

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution product);
use Algorithm::Combinatorics qw(combinations);
use List::Util qw(sum);

sub solve_part2
{
    my @lines = read_lines('input');
    my @packages = map { int($_) } @lines;
    my $target = sum(@packages) / 4;

    # Try group sizes from smallest to largest
    for my $size (1 .. scalar @packages)
    {
        my $min_qe;

        my $iter = combinations(\@packages, $size);
        while (my $combo = $iter->next)
        {
            if (sum(@$combo) == $target)
            {
                my $qe = product(@$combo);
                $min_qe = $qe if !defined $min_qe || $qe < $min_qe;
            }
        }

        return $min_qe if defined $min_qe;
    }

    return 0;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
