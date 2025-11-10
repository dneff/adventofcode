#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 6: Probably a Fire Hazard
# https://adventofcode.com/2015/day/6
#
# Part 2: Same commands but different semantics - lights have brightness levels

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use List::Util qw(max);

sub solve_part2
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
                $grid{$key} //= 0;

                if ($action eq 'on')
                {
                    $grid{$key} += 1;
                }
                elsif ($action eq 'off')
                {
                    $grid{$key} = max(0, $grid{$key} - 1);
                }
                elsif ($action eq 'toggle')
                {
                    $grid{$key} += 2;
                }
            }
        }
    }

    my $total_brightness = 0;
    $total_brightness += $_ for values %grid;
    return $total_brightness;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
