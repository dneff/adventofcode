#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 4: The Ideal Stocking Stuffer
# https://adventofcode.com/2015/day/4
#
# Find the lowest positive number that produces an MD5 hash starting with
# five zeroes when combined with the secret key.

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use Digest::MD5 qw(md5_hex);

sub solve_part1
{
    my @lines = read_lines('input');
    my $secret_key = $lines[0];
    chomp $secret_key;

    my $suffix = 0;

    while (1)
    {
        my $test = $secret_key . $suffix;
        my $hash = md5_hex($test);

        if (substr($hash, 0, 5) eq '00000')
        {
            return $suffix;
        }

        $suffix++;
    }
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
