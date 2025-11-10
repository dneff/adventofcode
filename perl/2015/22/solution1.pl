#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code 2015 - Day 22: Wizard Simulator 20XX
# https://adventofcode.com/2015/day/22
#
# Part 1: Find minimum mana to win wizard battle

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);
use List::Util qw(min max);
use Storable qw(dclone);

my %spells = (
    missile => { name => 'missile', cost => 53, attack => 4, armor => 0, heal => 0, mana => 0, turns => 0 },
    drain => { name => 'drain', cost => 73, attack => 2, armor => 0, heal => 2, mana => 0, turns => 0 },
    shield => { name => 'shield', cost => 113, attack => 0, armor => 7, heal => 0, mana => 0, turns => 6 },
    poison => { name => 'poison', cost => 173, attack => 3, armor => 0, heal => 0, mana => 0, turns => 6 },
    recharge => { name => 'recharge', cost => 229, attack => 0, armor => 0, heal => 0, mana => 101, turns => 5 },
);

my $minimum_mana = 10**15;

sub apply_effects ($player, $boss)
{
    $player->{armor} = 0;
    my @ending;

    for my $i (0 .. $#{$player->{effects}})
    {
        my $spell = $player->{effects}[$i];
        $boss->{hp} -= $spell->{attack};
        $player->{mana} += $spell->{mana};
        $player->{armor} += $spell->{armor};
        $spell->{turns}--;
        push @ending, $i if $spell->{turns} == 0;
    }

    for my $i (reverse @ending)
    {
        splice @{$player->{effects}}, $i, 1;
    }

    return $boss->{hp} <= 0;
}

sub resolve_turn ($player, $boss, $spell)
{
    return $player->{mana_used} if $player->{mana_used} > $minimum_mana;

    # Player casts spell
    $player->{mana} -= $spell->{cost};
    $player->{mana_used} += $spell->{cost};

    if ($spell->{turns} > 0)
    {
        push @{$player->{effects}}, dclone($spell);
    }
    else
    {
        $boss->{hp} -= $spell->{attack};
        $player->{hp} += $spell->{heal};
    }

    return $player->{mana_used} if $boss->{hp} <= 0;

    # Boss turn
    return $player->{mana_used} if apply_effects($player, $boss);

    $player->{hp} -= max(1, $boss->{attack} - $player->{armor});
    return $minimum_mana if $player->{hp} <= 0;

    # Next player turn
    return $player->{mana_used} if apply_effects($player, $boss);

    # Try next spells
    my %active = map { $_->{name} => 1 } @{$player->{effects}};
    my @costs = ($minimum_mana);

    for my $spell_name (keys %spells)
    {
        my $s = $spells{$spell_name};
        next if $active{$s->{name}};
        next if $s->{cost} > $player->{mana};

        my $result = resolve_turn(dclone($player), dclone($boss), $s);
        push @costs, $result if defined $result;
    }

    $minimum_mana = min(@costs);
    return $minimum_mana;
}

sub solve_part1
{
    my $player = {
        hp => 50,
        mana => 500,
        attack => 1,
        armor => 0,
        effects => [],
        mana_used => 0,
    };

    my $boss = { hp => 55, mana => 0, attack => 8, armor => 0, effects => [] };

    for my $spell_name (keys %spells)
    {
        my $result = resolve_turn(dclone($player), dclone($boss), $spells{$spell_name});
        $minimum_mana = min($minimum_mana, $result) if defined $result;
    }

    return $minimum_mana;
}

# Compute and print answer
my $answer = solve_part1();
print_solution(1, $answer);
