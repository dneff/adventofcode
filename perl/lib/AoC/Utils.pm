package AoC::Utils;

use v5.40;
use strict;
use warnings;
use feature 'signatures';
no warnings 'experimental::signatures';

use Exporter 'import';
our @EXPORT_OK = qw(
    print_solution
    count_if
    frequencies
    group_by
    min_by
    max_by
    sum
    product
    uniq
    trim
);

=head1 NAME

AoC::Utils - Common utility functions for Advent of Code solutions

=head1 SYNOPSIS

    use AoC::Utils qw(print_solution count_if frequencies);

    print_solution(1, 42);
    my $count = count_if { $_ > 5 } @numbers;
    my %freq = frequencies(@items);

=head1 DESCRIPTION

Provides common utility functions used across Advent of Code solutions.

=head1 FUNCTIONS

=head2 print_solution($part, $answer)

Prints the solution in a formatted way.

=cut

sub print_solution ($part, $answer)
{
    say "Part $part: $answer";
}

=head2 count_if { block } @list

Counts the number of items in @list for which the block returns true.

=cut

sub count_if (&@)
{
    my $code = shift;
    my $count = 0;
    for (@_)
    {
        local $_ = $_;
        $count++ if $code->();
    }
    return $count;
}

=head2 frequencies(@list)

Returns a hash mapping each unique item to its frequency.

=cut

sub frequencies (@list)
{
    my %freq;
    $freq{$_}++ for @list;
    return %freq;
}

=head2 group_by { block } @list

Groups items by the result of the block. Returns a hash reference.

=cut

sub group_by (&@)
{
    my $code = shift;
    my %groups;
    for (@_)
    {
        local $_ = $_;
        my $key = $code->();
        push @{ $groups{$key} }, $_;
    }
    return \%groups;
}

=head2 min_by { block } @list

Returns the item with the minimum value according to the block.

=cut

sub min_by (&@)
{
    my $code = shift;
    return unless @_;
    my $min_item = $_[0];
    my $min_val = do { local $_ = $min_item; $code->() };

    for my $item (@_[1 .. $#_])
    {
        local $_ = $item;
        my $val = $code->();
        if ($val < $min_val)
        {
            $min_val = $val;
            $min_item = $item;
        }
    }
    return $min_item;
}

=head2 max_by { block } @list

Returns the item with the maximum value according to the block.

=cut

sub max_by (&@)
{
    my $code = shift;
    return unless @_;
    my $max_item = $_[0];
    my $max_val = do { local $_ = $max_item; $code->() };

    for my $item (@_[1 .. $#_])
    {
        local $_ = $item;
        my $val = $code->();
        if ($val > $max_val)
        {
            $max_val = $val;
            $max_item = $item;
        }
    }
    return $max_item;
}

=head2 sum(@numbers)

Returns the sum of all numbers.

=cut

sub sum (@numbers)
{
    my $total = 0;
    $total += $_ for @numbers;
    return $total;
}

=head2 product(@numbers)

Returns the product of all numbers.

=cut

sub product (@numbers)
{
    my $result = 1;
    $result *= $_ for @numbers;
    return $result;
}

=head2 uniq(@list)

Returns unique items from the list, preserving order.

=cut

sub uniq (@list)
{
    my %seen;
    return grep { !$seen{$_}++ } @list;
}

=head2 trim($string)

Removes leading and trailing whitespace.

=cut

sub trim ($str)
{
    $str =~ s/^\s+|\s+$//g;
    return $str;
}

1;

=head1 AUTHOR

Advent of Code Solutions

=cut
