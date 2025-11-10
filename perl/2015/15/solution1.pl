#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 15: Science for Hungry People
# https://adventofcode.com/2015/day/15
#
# Part 1: Find the highest-scoring cookie recipe

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution product);
use List::Util qw(max);

sub solve_part1
{
    my @lines = read_lines('input');
    my @ingredients;

    # Parse ingredients
    for my $line (@lines)
    {
        my @numbers = $line =~ /(-?\d+)/g;
        push @ingredients, {
            capacity => $numbers[0],
            durability => $numbers[1],
            flavor => $numbers[2],
            texture => $numbers[3],
            calories => $numbers[4],
        };
    }

    my $max_score = 0;
    my $total = 100;

    # Try all combinations that sum to 100
    for my $i1 (0 .. $total)
    {
        for my $i2 (0 .. $total - $i1)
        {
            for my $i3 (0 .. $total - $i1 - $i2)
            {
                my $i4 = $total - $i1 - $i2 - $i3;
                my @amounts = ($i1, $i2, $i3, $i4);

                # Calculate property totals
                my $capacity = 0;
                my $durability = 0;
                my $flavor = 0;
                my $texture = 0;

                for my $i (0 .. $#ingredients)
                {
                    $capacity += $amounts[$i] * $ingredients[$i]{capacity};
                    $durability += $amounts[$i] * $ingredients[$i]{durability};
                    $flavor += $amounts[$i] * $ingredients[$i]{flavor};
                    $texture += $amounts[$i] * $ingredients[$i]{texture};
                }

                # Negative properties count as 0
                $capacity = 0 if $capacity < 0;
                $durability = 0 if $durability < 0;
                $flavor = 0 if $flavor < 0;
                $texture = 0 if $texture < 0;

                my $score = $capacity * $durability * $flavor * $texture;
                $max_score = $score if $score > $max_score;
            }
        }
    }

    return $max_score;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
