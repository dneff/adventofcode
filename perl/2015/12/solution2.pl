#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 12: JSAbacusFramework.io
# https://adventofcode.com/2015/day/12
#
# Part 2: Sum all numbers, ignoring objects containing "red"

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use JSON::PP;

sub sum_numbers ($data)
{
    my $sum = 0;

    if (ref($data) eq 'ARRAY')
    {
        $sum += sum_numbers($_) for @$data;
    }
    elsif (ref($data) eq 'HASH')
    {
        # Check if any value is "red"
        my $has_red = 0;
        for my $val (values %$data)
        {
            if (defined $val && !ref($val) && $val eq 'red')
            {
                $has_red = 1;
                last;
            }
        }

        # Only sum if no "red" value found
        unless ($has_red)
        {
            $sum += sum_numbers($_) for values %$data;
        }
    }
    elsif (defined $data && $data =~ /^-?\d+$/)
    {
        $sum += $data;
    }

    return $sum;
}

sub solve_part2
{
    my @lines = read_lines('input');
    my $json_text = $lines[0];

    my $data = decode_json($json_text);
    return sum_numbers($data);
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
