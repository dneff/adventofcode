#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 14: Reindeer Olympics
# https://adventofcode.com/2015/day/14
#
# Part 1: Find the winning reindeer's distance after 2503 seconds

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use List::Util qw(max);

sub calculate_distance ($fly_speed, $fly_time, $rest_time, $total_time)
{
    my $cycle = $fly_time + $rest_time;
    my $full_cycles = int($total_time / $cycle);
    my $remaining = $total_time % $cycle;
    my $flying_in_remaining = $remaining < $fly_time ? $remaining : $fly_time;

    return ($full_cycles * $fly_time + $flying_in_remaining) * $fly_speed;
}

sub solve_part1
{
    my @lines = read_lines('input');
    my $race_time = 2503;
    my $max_distance = 0;

    for my $line (@lines)
    {
        # Parse: "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."
        my @numbers = $line =~ /(\d+)/g;
        my ($fly_speed, $fly_time, $rest_time) = @numbers;

        my $distance = calculate_distance($fly_speed, $fly_time, $rest_time, $race_time);
        $max_distance = $distance if $distance > $max_distance;
    }

    return $max_distance;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
