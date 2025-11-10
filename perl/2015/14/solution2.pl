#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 14: Reindeer Olympics
# https://adventofcode.com/2015/day/14
#
# Part 2: Award points each second to whoever is in the lead

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use List::Util qw(max);

sub solve_part2
{
    my @lines = read_lines('input');
    my $race_time = 2503;
    my @reindeer;

    # Parse reindeer stats
    for my $line (@lines)
    {
        my @numbers = $line =~ /(\d+)/g;
        my ($fly_speed, $fly_time, $rest_time) = @numbers;
        my $name = ($line =~ /^(\w+)/)[0];

        push @reindeer, {
            name => $name,
            fly_speed => $fly_speed,
            fly_time => $fly_time,
            rest_time => $rest_time,
            distance => 0,
            time => 0,
            score => 0,
        };
    }

    # Simulate each second
    for my $second (1 .. $race_time)
    {
        # Update each reindeer's position
        for my $deer (@reindeer)
        {
            my $cycle = $deer->{fly_time} + $deer->{rest_time};
            my $pos_in_cycle = $deer->{time} % $cycle;

            if ($pos_in_cycle < $deer->{fly_time})
            {
                $deer->{distance} += $deer->{fly_speed};
            }

            $deer->{time}++;
        }

        # Award points to leader(s)
        my $max_dist = max(map { $_->{distance} } @reindeer);
        for my $deer (@reindeer)
        {
            $deer->{score}++ if $deer->{distance} == $max_dist;
        }
    }

    my $max_score = max(map { $_->{score} } @reindeer);
    return $max_score;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
