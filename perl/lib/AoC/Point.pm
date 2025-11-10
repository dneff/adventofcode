package AoC::Point;

use v5.40;
use strict;
use warnings;
use feature 'signatures';
no warnings 'experimental::signatures';

use overload
    '+'      => \&add,
    '-'      => \&subtract,
    '*'      => \&multiply,
    '=='     => \&equals,
    '!='     => \&not_equals,
    '""'     => \&to_string,
    fallback => 1;

use Exporter 'import';
our @EXPORT_OK = qw(
    point
    manhattan_distance
    NORTH SOUTH EAST WEST
    UP DOWN LEFT RIGHT
);

# Direction constants
use constant NORTH => __PACKAGE__->new(0, -1);
use constant SOUTH => __PACKAGE__->new(0, 1);
use constant EAST  => __PACKAGE__->new(1, 0);
use constant WEST  => __PACKAGE__->new(-1, 0);

# Aliases
use constant UP    => NORTH;
use constant DOWN  => SOUTH;
use constant RIGHT => EAST;
use constant LEFT  => WEST;

=head1 NAME

AoC::Point - 2D point class with operator overloading

=head1 SYNOPSIS

    use AoC::Point qw(point manhattan_distance NORTH SOUTH EAST WEST);

    my $p1 = point(3, 4);
    my $p2 = point(1, 2);
    my $p3 = $p1 + $p2;        # point(4, 6)
    my $dist = manhattan_distance($p1, $p2);

    my $next = $p1 + NORTH;    # Move north

=head1 DESCRIPTION

Represents a 2D point with x and y coordinates. Supports operator overloading
for addition, subtraction, multiplication, and comparison.

=head1 METHODS

=head2 new($x, $y)

Creates a new Point object.

=cut

sub new ($class, $x, $y)
{
    return bless { x => $x, y => $y }, $class;
}

=head2 point($x, $y)

Convenience function to create a new Point.

=cut

sub point ($x, $y)
{
    return __PACKAGE__->new($x, $y);
}

=head2 x(), y()

Accessor methods for coordinates.

=cut

sub x ($self)
{
    return $self->{x};
}

sub y ($self)
{
    return $self->{y};
}

=head2 add($other)

Adds two points together (operator overload for +).

=cut

sub add ($self, $other, $swap = undef)
{
    return __PACKAGE__->new($self->{x} + $other->{x}, $self->{y} + $other->{y});
}

=head2 subtract($other)

Subtracts one point from another (operator overload for -).

=cut

sub subtract ($self, $other, $swap = undef)
{
    if ($swap)
    {
        return __PACKAGE__->new($other->{x} - $self->{x}, $other->{y} - $self->{y});
    }
    return __PACKAGE__->new($self->{x} - $other->{x}, $self->{y} - $other->{y});
}

=head2 multiply($scalar)

Multiplies a point by a scalar (operator overload for *).

=cut

sub multiply ($self, $scalar, $swap = undef)
{
    my $s = ref($scalar) ? $scalar->{x} : $scalar;
    return __PACKAGE__->new($self->{x} * $s, $self->{y} * $s);
}

=head2 equals($other)

Checks if two points are equal (operator overload for ==).

=cut

sub equals ($self, $other, $swap = undef)
{
    return $self->{x} == $other->{x} && $self->{y} == $other->{y};
}

=head2 not_equals($other)

Checks if two points are not equal (operator overload for !=).

=cut

sub not_equals ($self, $other, $swap = undef)
{
    return !$self->equals($other);
}

=head2 to_string()

Converts point to string representation (operator overload for "").

=cut

sub to_string ($self, $other = undef, $swap = undef)
{
    return "($self->{x}, $self->{y})";
}

=head2 neighbors4()

Returns the 4 orthogonal neighbors (N, S, E, W).

=cut

sub neighbors4 ($self)
{
    return (
        $self + NORTH,
        $self + SOUTH,
        $self + EAST,
        $self + WEST,
    );
}

=head2 neighbors8()

Returns all 8 neighbors (including diagonals).

=cut

sub neighbors8 ($self)
{
    my @neighbors;
    for my $dy (-1 .. 1)
    {
        for my $dx (-1 .. 1)
        {
            next if $dx == 0 && $dy == 0;
            push @neighbors, __PACKAGE__->new($self->{x} + $dx, $self->{y} + $dy);
        }
    }
    return @neighbors;
}

=head2 manhattan_distance($p1, $p2)

Calculates Manhattan distance between two points.

=cut

sub manhattan_distance ($p1, $p2)
{
    return abs($p1->{x} - $p2->{x}) + abs($p1->{y} - $p2->{y});
}

=head2 as_hash_key()

Returns a string suitable for using as a hash key.

=cut

sub as_hash_key ($self)
{
    return "$self->{x},$self->{y}";
}

1;

=head1 AUTHOR

Advent of Code Solutions

=cut
