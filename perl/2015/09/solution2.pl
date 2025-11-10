#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 9: All in a Single Night
# https://adventofcode.com/2015/day/9
#
# Part 2: Find the longest route visiting all cities

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use Algorithm::Combinatorics qw(permutations);
use List::Util qw(max);

sub solve_part2
{
    my @lines = read_lines('input');
    my %distances;
    my %cities;

    # Parse input: "London to Dublin = 464"
    for my $line (@lines)
    {
        if ($line =~ /^(\w+) to (\w+) = (\d+)$/)
        {
            my ($c1, $c2, $dist) = ($1, $2, $3);
            $distances{"$c1-$c2"} = $dist;
            $distances{"$c2-$c1"} = $dist;
            $cities{$c1} = 1;
            $cities{$c2} = 1;
        }
    }

    my @city_list = keys %cities;
    my $longest = 0;

    # Try all permutations of cities
    my $iter = permutations(\@city_list);
    while (my $route = $iter->next)
    {
        my $distance = 0;
        for my $i (0 .. $#$route - 1)
        {
            my $key = $route->[$i] . '-' . $route->[$i + 1];
            $distance += $distances{$key};
        }
        $longest = $distance if $distance > $longest;
    }

    return $longest;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
