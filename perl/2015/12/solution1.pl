#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 12: JSAbacusFramework.io
# https://adventofcode.com/2015/day/12
#
# Part 1: Sum all numbers in JSON document

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
        $sum += sum_numbers($_) for values %$data;
    }
    elsif (defined $data && $data =~ /^-?\d+$/)
    {
        $sum += $data;
    }

    return $sum;
}

sub solve_part1
{
    my @lines = read_lines('input');
    my $json_text = $lines[0];

    my $data = decode_json($json_text);
    return sum_numbers($data);
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
