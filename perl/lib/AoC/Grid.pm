package AoC::Grid;

use v5.40;
use strict;
use warnings;
use feature 'signatures';
no warnings 'experimental::signatures';

use AoC::Point qw(point NORTH SOUTH EAST WEST);

use Exporter 'import';
our @EXPORT_OK = qw(
    make_grid
    grid_get
    grid_set
    grid_in_bounds
    grid_find
    grid_find_all
    grid_neighbors4
    grid_neighbors8
    grid_width
    grid_height
    grid_print
);

=head1 NAME

AoC::Grid - 2D grid operations

=head1 SYNOPSIS

    use AoC::Grid qw(make_grid grid_get grid_set grid_neighbors4);
    use AoC::Point qw(point);

    my $grid = make_grid(\@rows);
    my $value = grid_get($grid, point(3, 4));
    grid_set($grid, point(3, 4), 'X');
    my @neighbors = grid_neighbors4($grid, point(3, 4));

=head1 DESCRIPTION

Provides functions for working with 2D grids stored as arrays of arrays.

=head1 FUNCTIONS

=head2 make_grid(\@rows)

Creates a grid from an array of rows. Each row can be a string or arrayref.

=cut

sub make_grid ($rows)
{
    my @grid;
    for my $row (@$rows)
    {
        if (ref($row) eq 'ARRAY')
        {
            push @grid, [@$row];
        }
        else
        {
            push @grid, [split //, $row];
        }
    }
    return \@grid;
}

=head2 grid_get($grid, $point)

Gets the value at a point in the grid.

=cut

sub grid_get ($grid, $point)
{
    my ($x, $y) = ($point->x, $point->y);
    return undef unless grid_in_bounds($grid, $point);
    return $grid->[$y][$x];
}

=head2 grid_set($grid, $point, $value)

Sets the value at a point in the grid.

=cut

sub grid_set ($grid, $point, $value)
{
    my ($x, $y) = ($point->x, $point->y);
    return unless grid_in_bounds($grid, $point);
    $grid->[$y][$x] = $value;
}

=head2 grid_in_bounds($grid, $point)

Checks if a point is within the grid bounds.

=cut

sub grid_in_bounds ($grid, $point)
{
    my ($x, $y) = ($point->x, $point->y);
    return $y >= 0 && $y < scalar(@$grid) && $x >= 0 && $x < scalar(@{ $grid->[0] });
}

=head2 grid_find($grid, $value)

Finds the first occurrence of a value in the grid. Returns a Point or undef.

=cut

sub grid_find ($grid, $value)
{
    for my $y (0 .. $#$grid)
    {
        for my $x (0 .. $#{ $grid->[$y] })
        {
            return point($x, $y) if $grid->[$y][$x] eq $value;
        }
    }
    return undef;
}

=head2 grid_find_all($grid, $value)

Finds all occurrences of a value in the grid. Returns an array of Points.

=cut

sub grid_find_all ($grid, $value)
{
    my @points;
    for my $y (0 .. $#$grid)
    {
        for my $x (0 .. $#{ $grid->[$y] })
        {
            push @points, point($x, $y) if $grid->[$y][$x] eq $value;
        }
    }
    return @points;
}

=head2 grid_neighbors4($grid, $point)

Returns the 4 orthogonal neighbors that are in bounds.

=cut

sub grid_neighbors4 ($grid, $point)
{
    return grep { grid_in_bounds($grid, $_) } $point->neighbors4();
}

=head2 grid_neighbors8($grid, $point)

Returns all 8 neighbors (including diagonals) that are in bounds.

=cut

sub grid_neighbors8 ($grid, $point)
{
    return grep { grid_in_bounds($grid, $_) } $point->neighbors8();
}

=head2 grid_width($grid)

Returns the width of the grid.

=cut

sub grid_width ($grid)
{
    return scalar(@{ $grid->[0] });
}

=head2 grid_height($grid)

Returns the height of the grid.

=cut

sub grid_height ($grid)
{
    return scalar(@$grid);
}

=head2 grid_print($grid)

Prints the grid to STDOUT.

=cut

sub grid_print ($grid)
{
    for my $row (@$grid)
    {
        say join '', @$row;
    }
}

1;

=head1 AUTHOR

Advent of Code Solutions

=cut
