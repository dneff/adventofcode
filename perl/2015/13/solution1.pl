#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 13: Knights of the Dinner Table
# https://adventofcode.com/2015/day/13
#
# Part 1: Find optimal seating arrangement for maximum happiness

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use Algorithm::Combinatorics qw(permutations);
use List::Util qw(max);

sub solve_part1
{
    my @lines = read_lines('input');
    my %happiness;
    my %people;

    # Parse: "Alice would gain 54 happiness units by sitting next to Bob."
    for my $line (@lines)
    {
        $line =~ s/\.$//;  # Remove trailing period
        if ($line =~ /^(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)$/)
        {
            my ($person1, $type, $amount, $person2) = ($1, $2, $3, $4);
            $amount = -$amount if $type eq 'lose';
            $happiness{$person1}{$person2} = $amount;
            $people{$person1} = 1;
            $people{$person2} = 1;
        }
    }

    my @people_list = keys %people;
    my $max_happiness = 0;

    # Try all circular seating arrangements
    my $iter = permutations(\@people_list);
    while (my $seating = $iter->next)
    {
        my $total = 0;

        # Sum happiness for adjacent pairs
        for my $i (0 .. $#$seating - 1)
        {
            my $p1 = $seating->[$i];
            my $p2 = $seating->[$i + 1];
            $total += $happiness{$p1}{$p2} + $happiness{$p2}{$p1};
        }

        # Add happiness for first and last (circular table)
        my $first = $seating->[0];
        my $last = $seating->[-1];
        $total += $happiness{$first}{$last} + $happiness{$last}{$first};

        $max_happiness = $total if $total > $max_happiness;
    }

    return $max_happiness;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
