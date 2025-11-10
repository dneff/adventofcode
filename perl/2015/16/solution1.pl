#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 16: Aunt Sue
# https://adventofcode.com/2015/day/16
#
# Part 1: Find which Aunt Sue gave you the gift

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part1
{
    my @lines = read_lines('input');

    my %detected = (
        children => 3,
        cats => 7,
        samoyeds => 2,
        pomeranians => 3,
        akitas => 0,
        vizslas => 0,
        goldfish => 5,
        trees => 3,
        cars => 2,
        perfumes => 1,
    );

    my %matches;

    for my $line (@lines)
    {
        # Parse: "Sue 1: cars: 9, akitas: 3, goldfish: 0"
        $line =~ /^Sue (\d+): (.+)$/;
        my $sue_num = $1;
        my $props = $2;

        my %sue_props;
        while ($props =~ /(\w+): (\d+)/g)
        {
            $sue_props{$1} = $2;
        }

        # Count matches
        my $match_count = 0;
        for my $key (keys %sue_props)
        {
            if (exists $detected{$key} && $detected{$key} == $sue_props{$key})
            {
                $match_count++;
            }
        }

        $matches{$sue_num} = $match_count;
    }

    # Find Sue with most matches
    my $best_sue = (sort { $matches{$b} <=> $matches{$a} } keys %matches)[0];
    return $best_sue;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
