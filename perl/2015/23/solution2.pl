#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 23: Opening the Turing Lock
# https://adventofcode.com/2015/day/23
#
# Part 2: Start with register a = 1

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part2
{
    my @lines = read_lines('input');
    my %registers = (a => 1, b => 0);
    my $pc = 0;

    while ($pc >= 0 && $pc < scalar @lines)
    {
        my $inst = $lines[$pc];
        my @parts = split /[, ]+/, $inst;

        if ($parts[0] eq 'hlf')
        {
            $registers{$parts[1]} = int($registers{$parts[1]} / 2);
            $pc++;
        }
        elsif ($parts[0] eq 'tpl')
        {
            $registers{$parts[1]} *= 3;
            $pc++;
        }
        elsif ($parts[0] eq 'inc')
        {
            $registers{$parts[1]}++;
            $pc++;
        }
        elsif ($parts[0] eq 'jmp')
        {
            $pc += int($parts[1]);
        }
        elsif ($parts[0] eq 'jie')
        {
            if ($registers{$parts[1]} % 2 == 0)
            {
                $pc += int($parts[2]);
            }
            else
            {
                $pc++;
            }
        }
        elsif ($parts[0] eq 'jio')
        {
            if ($registers{$parts[1]} == 1)
            {
                $pc += int($parts[2]);
            }
            else
            {
                $pc++;
            }
        }
    }

    return $registers{b};
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
