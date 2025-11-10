#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 5: Doesn't He Have Intern-Elves For This?
# https://adventofcode.com/2015/day/5
#
# Count how many strings are "nice" according to the rules.

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub has_three_vowels ($s)
{
    my $vowel_count = () = $s =~ /[aeiou]/g;
    return $vowel_count >= 3;
}

sub has_double_letter ($s)
{
    return $s =~ /(.)\1/;
}

sub no_forbidden_pairs ($s)
{
    return $s !~ /ab|cd|pq|xy/;
}

sub is_nice ($s)
{
    return has_three_vowels($s) && has_double_letter($s) && no_forbidden_pairs($s);
}

sub solve_part1
{
    my @lines = read_lines('input');

    my $nice_count = 0;
    for my $line (@lines)
    {
        $nice_count++ if is_nice($line);
    }

    return $nice_count;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
