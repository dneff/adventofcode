#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 18: Like a GIF For Your Yard
# https://adventofcode.com/2015/day/18
#
# Part 1: Conway's Game of Life with lights

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub get_neighbors ($row, $col, $max)
{
    my @neighbors;
    my @offsets = ([-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]);

    for my $offset (@offsets)
    {
        my $r = $row + $offset->[0];
        my $c = $col + $offset->[1];
        push @neighbors, [$r, $c] if $r >= 0 && $r <= $max && $c >= 0 && $c <= $max;
    }

    return @neighbors;
}

sub solve_part1
{
    my @lines = read_lines('input');
    my %lights;
    my $max_coord = $#lines;

    # Initialize grid
    for my $row (0 .. $#lines)
    {
        my @chars = split //, $lines[$row];
        for my $col (0 .. $#chars)
        {
            $lights{"$row,$col"} = 1 if $chars[$col] eq '#';
        }
    }

    # Run 100 steps
    for my $step (1 .. 100)
    {
        my %neighbor_counts;
        my %new_lights;

        # Count neighbors for all positions
        for my $key (keys %lights)
        {
            my ($row, $col) = split /,/, $key;
            for my $neighbor (get_neighbors($row, $col, $max_coord))
            {
                my $n_key = join ',', @$neighbor;
                $neighbor_counts{$n_key}++;
            }
        }

        # Apply rules
        for my $row (0 .. $max_coord)
        {
            for my $col (0 .. $max_coord)
            {
                my $key = "$row,$col";
                my $count = $neighbor_counts{$key} // 0;
                my $is_on = exists $lights{$key};

                if ($is_on && ($count == 2 || $count == 3))
                {
                    $new_lights{$key} = 1;
                }
                elsif (!$is_on && $count == 3)
                {
                    $new_lights{$key} = 1;
                }
            }
        }

        %lights = %new_lights;
    }

    return scalar keys %lights;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
