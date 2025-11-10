#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 6: Probably a Fire Hazard
# https://adventofcode.com/2015/day/6
#
# Part 1: Control a 1000x1000 grid of lights with on/off/toggle commands

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part1
{
    my @lines = read_lines('input');
    my %grid;

    for my $line (@lines)
    {
        # Parse: "turn on 0,0 through 999,999" or "toggle 0,0 through 500,500"
        my ($action, $x1, $y1, $x2, $y2);

        if ($line =~ /turn on (\d+),(\d+) through (\d+),(\d+)/)
        {
            ($action, $x1, $y1, $x2, $y2) = ('on', $1, $2, $3, $4);
        }
        elsif ($line =~ /turn off (\d+),(\d+) through (\d+),(\d+)/)
        {
            ($action, $x1, $y1, $x2, $y2) = ('off', $1, $2, $3, $4);
        }
        elsif ($line =~ /toggle (\d+),(\d+) through (\d+),(\d+)/)
        {
            ($action, $x1, $y1, $x2, $y2) = ('toggle', $1, $2, $3, $4);
        }

        for my $x ($x1 .. $x2)
        {
            for my $y ($y1 .. $y2)
            {
                my $key = "$x,$y";
                if ($action eq 'on')
                {
                    $grid{$key} = 1;
                }
                elsif ($action eq 'off')
                {
                    $grid{$key} = 0;
                }
                elsif ($action eq 'toggle')
                {
                    $grid{$key} = $grid{$key} ? 0 : 1;
                }
            }
        }
    }

    my $lit = 0;
    $lit += $_ for values %grid;
    return $lit;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
