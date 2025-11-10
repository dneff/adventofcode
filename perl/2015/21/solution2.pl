#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 21: RPG Simulator 20XX
# https://adventofcode.com/2015/day/21
#
# Part 2: Find maximum cost and still lose

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use List::Util qw(max);

my %shop = (
    weapons => [
        { name => 'Dagger', cost => 8, attack => 4, armor => 0 },
        { name => 'Shortsword', cost => 10, attack => 5, armor => 0 },
        { name => 'Warhammer', cost => 25, attack => 6, armor => 0 },
        { name => 'Longsword', cost => 40, attack => 7, armor => 0 },
        { name => 'Greataxe', cost => 74, attack => 8, armor => 0 },
    ],
    armors => [
        { name => 'None', cost => 0, attack => 0, armor => 0 },
        { name => 'Leather', cost => 13, attack => 0, armor => 1 },
        { name => 'Chainmail', cost => 31, attack => 0, armor => 2 },
        { name => 'Splintmail', cost => 53, attack => 0, armor => 3 },
        { name => 'Bandedmail', cost => 75, attack => 0, armor => 4 },
        { name => 'Platemail', cost => 102, attack => 0, armor => 5 },
    ],
    rings => [
        { name => 'None1', cost => 0, attack => 0, armor => 0 },
        { name => 'None2', cost => 0, attack => 0, armor => 0 },
        { name => 'Damage +1', cost => 25, attack => 1, armor => 0 },
        { name => 'Damage +2', cost => 50, attack => 2, armor => 0 },
        { name => 'Damage +3', cost => 100, attack => 3, armor => 0 },
        { name => 'Defense +1', cost => 20, attack => 0, armor => 1 },
        { name => 'Defense +2', cost => 40, attack => 0, armor => 2 },
        { name => 'Defense +3', cost => 80, attack => 0, armor => 3 },
    ],
);

sub player_wins ($player_hp, $player_attack, $player_armor, $boss_hp, $boss_attack, $boss_armor)
{
    my $php = $player_hp;
    my $bhp = $boss_hp;

    while (1)
    {
        # Player attacks
        $bhp -= max(1, $player_attack - $boss_armor);
        return 1 if $bhp <= 0;

        # Boss attacks
        $php -= max(1, $boss_attack - $player_armor);
        return 0 if $php <= 0;
    }
}

sub solve_part2
{
    my @lines = read_lines('input');
    my ($boss_hp) = $lines[0] =~ /(\d+)/;
    my ($boss_attack) = $lines[1] =~ /(\d+)/;
    my ($boss_armor) = $lines[2] =~ /(\d+)/;

    my $player_hp = 100;
    my $max_cost = 0;

    # Try all equipment combinations
    for my $weapon (@{$shop{weapons}})
    {
        for my $armor (@{$shop{armors}})
        {
            for my $i (0 .. $#{$shop{rings}})
            {
                for my $j ($i + 1 .. $#{$shop{rings}})
                {
                    my $ring1 = $shop{rings}[$i];
                    my $ring2 = $shop{rings}[$j];

                    my $cost = $weapon->{cost} + $armor->{cost} + $ring1->{cost} + $ring2->{cost};
                    my $attack = $weapon->{attack} + $armor->{attack} + $ring1->{attack} + $ring2->{attack};
                    my $def = $weapon->{armor} + $armor->{armor} + $ring1->{armor} + $ring2->{armor};

                    # Find max cost that still loses
                    if (!player_wins($player_hp, $attack, $def, $boss_hp, $boss_attack, $boss_armor))
                    {
                        $max_cost = $cost if $cost > $max_cost;
                    }
                }
            }
        }
    }

    return $max_cost;
}

# Compute and print answer
my $answer = solve_part2();
print_solution(2, $answer);
