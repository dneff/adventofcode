#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 11: Corporate Policy
# https://adventofcode.com/2015/day/11
#
# Part 2: Find the next valid password after the first one

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub has_straight ($pwd)
{
    for my $i (0 .. length($pwd) - 3)
    {
        my $c1 = ord(substr($pwd, $i, 1));
        my $c2 = ord(substr($pwd, $i + 1, 1));
        my $c3 = ord(substr($pwd, $i + 2, 1));
        return 1 if $c2 == $c1 + 1 && $c3 == $c2 + 1;
    }
    return 0;
}

sub has_invalid_chars ($pwd)
{
    return $pwd =~ /[iol]/;
}

sub has_two_pairs ($pwd)
{
    my @pairs;
    for my $i (0 .. length($pwd) - 2)
    {
        if (substr($pwd, $i, 1) eq substr($pwd, $i + 1, 1))
        {
            push @pairs, substr($pwd, $i, 1);
            $i++;  # Skip the second character of the pair
        }
    }
    my %unique = map { $_ => 1 } @pairs;
    return keys %unique >= 2;
}

sub is_valid ($pwd)
{
    return 0 if has_invalid_chars($pwd);
    return 0 unless has_straight($pwd);
    return 0 unless has_two_pairs($pwd);
    return 1;
}

sub increment_password ($pwd)
{
    my @chars = split //, $pwd;

    # Increment from right to left
    for (my $i = $#chars; $i >= 0; $i--)
    {
        if ($chars[$i] eq 'z')
        {
            $chars[$i] = 'a';
        }
        else
        {
            $chars[$i] = chr(ord($chars[$i]) + 1);
            last;
        }
    }

    return join '', @chars;
}

sub find_next_password ($pwd)
{
    $pwd = increment_password($pwd);
    while (!is_valid($pwd))
    {
        $pwd = increment_password($pwd);
    }
    return $pwd;
}

sub solve_part2
{
    my @lines = read_lines('input');
    my $pwd = $lines[0];

    # Find first valid password
    $pwd = find_next_password($pwd);
    # Find second valid password
    $pwd = find_next_password($pwd);

    return $pwd;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
