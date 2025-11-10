#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 19: Medicine for Rudolph
# https://adventofcode.com/2015/day/19
#
# Part 1: Count distinct molecules from one replacement

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part1
{
    my @lines = read_lines('input');
    my %replacements;
    my $molecule;

    # Parse replacements
    for my $line (@lines)
    {
        last if $line eq '';
        if ($line =~ /^(\w+) => (\w+)$/)
        {
            push @{$replacements{$1}}, $2;
        }
    }

    # Get molecule (last non-empty line)
    $molecule = $lines[-1];

    my %distinct;

    # Try all replacements
    for my $source (keys %replacements)
    {
        # Find all positions where source appears
        my $pos = 0;
        while (($pos = index($molecule, $source, $pos)) >= 0)
        {
            # Try each replacement for this source
            for my $replacement (@{$replacements{$source}})
            {
                my $new_molecule = substr($molecule, 0, $pos) .
                                   $replacement .
                                   substr($molecule, $pos + length($source));
                $distinct{$new_molecule} = 1;
            }
            $pos++;
        }
    }

    return scalar keys %distinct;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
