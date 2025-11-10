package AoC::Input;

use v5.40;
use strict;
use warnings;
use feature 'signatures';
no warnings 'experimental::signatures';

use File::Spec;
use File::Basename qw(dirname);
use Cwd qw(abs_path);

use Exporter 'import';
our @EXPORT_OK = qw(
    read_lines
    read_text
    read_grid
    read_numbers
    read_paragraphs
    parse_numbers
    get_input_path
);

=head1 NAME

AoC::Input - Input file reading and parsing utilities

=head1 SYNOPSIS

    use AoC::Input qw(read_lines read_grid parse_numbers);

    my @lines = read_lines('input.txt');
    my $grid = read_grid('input.txt');
    my @nums = parse_numbers($text);

=head1 DESCRIPTION

Provides functions for reading and parsing Advent of Code input files.

=head1 FUNCTIONS

=head2 get_input_path($filename)

Resolves the input file path. If the filename is relative, looks for it
relative to the calling script, or in the aoc-data directory structure.

=cut

sub get_input_path ($filename)
{
    # If absolute path, use as-is
    return $filename if File::Spec->file_name_is_absolute($filename);

    # Get the calling script's directory
    my ($package, $script_file) = caller;
    my $script_dir = dirname(abs_path($script_file));

    # First try relative to script
    my $local_path = File::Spec->catfile($script_dir, $filename);
    return $local_path if -e $local_path;

    # Try aoc-data structure if filename looks like "input"
    if ($filename eq 'input' && $script_dir =~ m{/(\d{4})/(\d+)/?$})
    {
        my ($year, $day) = ($1, $2);
        # Remove leading zeros from day
        $day =~ s/^0+//;
        my $aoc_data_path = File::Spec->catfile($script_dir, '../../../aoc-data', $year, $day, 'input');
        return $aoc_data_path if -e $aoc_data_path;
    }

    # Fall back to original filename
    return $filename;
}

=head2 read_lines($filename)

Reads a file and returns an array of lines (chomped).

=cut

sub read_lines ($filename)
{
    my $path = get_input_path($filename);
    open my $fh, '<', $path or die "Cannot open $path: $!";
    my @lines = <$fh>;
    close $fh;
    chomp @lines;
    return @lines;
}

=head2 read_text($filename)

Reads entire file as a single string.

=cut

sub read_text ($filename)
{
    my $path = get_input_path($filename);
    open my $fh, '<', $path or die "Cannot open $path: $!";
    local $/ = undef;
    my $text = <$fh>;
    close $fh;
    return $text;
}

=head2 read_grid($filename)

Reads a file as a 2D grid (array of arrays of characters).

=cut

sub read_grid ($filename)
{
    my @lines = read_lines($filename);
    my @grid = map { [split //] } @lines;
    return \@grid;
}

=head2 read_numbers($filename)

Reads a file and extracts all integers, one per line.

=cut

sub read_numbers ($filename)
{
    my @lines = read_lines($filename);
    return map { int($_) } @lines;
}

=head2 read_paragraphs($filename)

Reads a file and splits it into paragraphs (separated by blank lines).

=cut

sub read_paragraphs ($filename)
{
    my $text = read_text($filename);
    my @paragraphs = split /\n\n+/, $text;
    return @paragraphs;
}

=head2 parse_numbers($text)

Extracts all numbers (including negative) from a string.

=cut

sub parse_numbers ($text)
{
    my @numbers = $text =~ /-?\d+/g;
    return @numbers;
}

1;

=head1 AUTHOR

Advent of Code Solutions

=cut
