#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 7: Some Assembly Required
# https://adventofcode.com/2015/day/7
#
# Part 1: Simulate a circuit of bitwise logic gates to find signal on wire 'a'

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub is_numeric ($val)
{
    return $val =~ /^\d+$/;
}

sub has_signal ($wires, @inputs)
{
    for my $input (@inputs)
    {
        return 0 if !is_numeric($input) && !exists $wires->{$input};
    }
    return 1;
}

sub get_value ($wires, $input)
{
    return is_numeric($input) ? int($input) : $wires->{$input};
}

sub process_instruction ($wires, $instruction)
{
    my ($source, $dest) = split / -> /, $instruction;
    my @parts = split / /, $source;

    # Direct assignment: "123 -> x" or "x -> y"
    if (@parts == 1)
    {
        return 0 unless has_signal($wires, $parts[0]);
        $wires->{$dest} = get_value($wires, $parts[0]);
        return 1;
    }
    # NOT operation: "NOT x -> h"
    elsif (@parts == 2)
    {
        my ($op, $input) = @parts;
        return 0 unless has_signal($wires, $input);
        # NOT in Perl gives negative numbers, so use 16-bit mask
        $wires->{$dest} = (~get_value($wires, $input)) & 0xFFFF;
        return 1;
    }
    # Binary operations: "x AND y -> z", "x LSHIFT 2 -> f"
    else
    {
        my ($left, $op, $right) = @parts;
        return 0 unless has_signal($wires, $left, $right);

        my $left_val = get_value($wires, $left);
        my $right_val = get_value($wires, $right);

        if ($op eq 'AND')
        {
            $wires->{$dest} = $left_val & $right_val;
        }
        elsif ($op eq 'OR')
        {
            $wires->{$dest} = $left_val | $right_val;
        }
        elsif ($op eq 'LSHIFT')
        {
            $wires->{$dest} = ($left_val << $right_val) & 0xFFFF;
        }
        elsif ($op eq 'RSHIFT')
        {
            $wires->{$dest} = $left_val >> $right_val;
        }
        return 1;
    }
}

sub solve_part1
{
    my @lines = read_lines('input');
    my %wires;
    my @pending = @lines;

    while (@pending)
    {
        my @deferred;
        for my $instruction (@pending)
        {
            push @deferred, $instruction unless process_instruction(\%wires, $instruction);
        }
        @pending = @deferred;
    }

    return $wires{a};
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
