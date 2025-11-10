#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

=head1 NAME

verify_solutions.pl - Verify Advent of Code Perl solutions against known correct answers

=head1 SYNOPSIS

    perl verify_solutions.pl [YEAR] [DAY] [OPTIONS]

=head1 DESCRIPTION

This script runs each Perl solution file for a specified year and compares the output
against the answer files stored in aoc-data.

=head1 USAGE

    perl verify_solutions.pl                    # Verify all years
    perl verify_solutions.pl 2015               # Verify year 2015
    perl verify_solutions.pl 2015 20            # Verify year 2015, day 20
    perl verify_solutions.pl --year 2015 --day 20 --write-missing

=head1 OPTIONS

=over 4

=item B<YEAR>

The year to verify (e.g., 2015)

=item B<DAY>

The day to verify (1-25)

=item B<--year YEAR, -y YEAR>

The year to verify (alternative to positional argument)

=item B<--day DAY, -d DAY>

The day to verify (alternative to positional argument)

=item B<--write-missing, -w>

Write solution output to missing answer files

=back

=cut

use Getopt::Long;
use File::Spec;
use File::Basename qw(dirname);
use Cwd qw(abs_path);
use Time::HiRes qw(time);

# Colors for terminal output
use constant
{
    GREEN  => "\033[92m",
    RED    => "\033[91m",
    YELLOW => "\033[93m",
    BLUE   => "\033[94m",
    RESET  => "\033[0m",
};

sub get_time_emoji ($elapsed_time)
{
    return "⚡" if $elapsed_time < 1.0;
    return "🚀" if $elapsed_time < 3.0;
    return "▶️"  if $elapsed_time < 10.0;
    return "🐢" if $elapsed_time < 30.0;
    return "🐌";
}

sub get_expected_answer ($day, $part, $year, $base_dir)
{
    # Path from perl/ dir to aoc-data is ../../aoc-data
    my $answer_file = File::Spec->catfile($base_dir, '../..', 'aoc-data', $year, $day, "solution-$part");

    return undef unless -e $answer_file;

    open my $fh, '<', $answer_file or return undef;
    my $content = do { local $/; <$fh> };
    close $fh;

    $content =~ s/^\s+|\s+$//g;    # trim

    # Return undef if empty or just '0'
    return undef if !$content || $content eq '0';

    return $content;
}

sub write_answer ($day, $part, $year, $answer, $base_dir)
{
    my $answer_dir = File::Spec->catfile($base_dir, '../..', 'aoc-data', $year, $day);
    my $answer_file = File::Spec->catfile($answer_dir, "solution-$part");

    # Create directory if it doesn't exist
    unless (-d $answer_dir)
    {
        system('mkdir', '-p', $answer_dir) == 0 or return 0;
    }

    # Write the answer
    open my $fh, '>', $answer_file or do
    {
        say RED . "Error writing answer: $!" . RESET;
        return 0;
    };
    print $fh $answer . "\n";
    close $fh;

    return 1;
}

sub run_solution ($day, $part, $year, $base_dir)
{
    my $day_str = sprintf("%02d", $day);
    my $solution_file = File::Spec->catfile($base_dir, $year, $day_str, "solution$part.pl");

    return (undef, 0, 0.0, 0) unless -e $solution_file;

    my $start_time = time();

    # Run the solution and capture output
    my $output = `perl $solution_file 2>&1`;
    my $exit_code = $? >> 8;

    my $elapsed_time = time() - $start_time;

    return (undef, 0, $elapsed_time, 1) if $exit_code != 0;

    # Extract the answer from output (looking for lines like "Part 1: 138")
    for my $line (split /\n/, $output)
    {
        if ($line =~ /Part $part:\s*(.+)/)
        {
            my $answer = $1;
            $answer =~ s/^\s+|\s+$//g;
            return ($answer, 1, $elapsed_time, 1);
        }
    }

    return (undef, 0, $elapsed_time, 1);
}

sub get_years_to_verify ($base_dir, $year)
{
    return ($year) if defined $year;

    # Find all years with Perl solutions
    opendir my $dh, $base_dir or return ();
    my @years = grep { /^\d{4}$/ && -d File::Spec->catfile($base_dir, $_) } readdir $dh;
    closedir $dh;

    return sort { $a <=> $b } @years;
}

sub main
{
    my ($year_pos, $day_pos, $year_flag, $day_flag, $write_missing, $help);

    GetOptions(
        'year|y=i'      => \$year_flag,
        'day|d=i'       => \$day_flag,
        'write-missing|w' => \$write_missing,
        'help|h'        => \$help,
    ) or die "Error in command line arguments\n";

    if ($help)
    {
        print <<'HELP';
Usage: perl verify_solutions.pl [YEAR] [DAY] [OPTIONS]

Verify Advent of Code Perl solutions against known correct answers.

Positional Arguments:
    YEAR                      The year to verify (e.g., 2015)
    DAY                       The day to verify (1-25)

Options:
    --year YEAR, -y YEAR      The year to verify (alternative to positional)
    --day DAY, -d DAY         The day to verify (alternative to positional)
    --write-missing, -w       Write solution output to missing answer files
    --help, -h                Show this help message

Examples:
    perl verify_solutions.pl              # Verify all years
    perl verify_solutions.pl 2015         # Verify year 2015
    perl verify_solutions.pl 2015 20      # Verify year 2015, day 20
    perl verify_solutions.pl --year 2015 --day 20 --write-missing
HELP
        exit 0;
    }

    # Get positional arguments
    $year_pos = shift @ARGV if @ARGV;
    $day_pos = shift @ARGV if @ARGV;

    # Prioritize positional arguments over flags
    my $year = $year_pos // $year_flag;
    my $day = $day_pos // $day_flag;

    my $base_dir = dirname(abs_path($0));
    my @years_to_verify = get_years_to_verify($base_dir, $year);

    unless (@years_to_verify)
    {
        say RED . "Error: No Perl solutions directories found" . RESET;
        exit 1;
    }

    # Determine days to verify
    my @days_to_verify;
    if (defined $day)
    {
        unless ($day >= 1 && $day <= 25)
        {
            say RED . "Error: Day must be between 1 and 25" . RESET;
            exit 1;
        }
        @days_to_verify = ($day);
    }
    else
    {
        @days_to_verify = (1 .. 25);
    }

    # Verify all years
    my $all_total_verified = 0;
    my $all_total_correct = 0;
    my $all_total_incorrect = 0;
    my $all_total_missing = 0;
    my $all_total_failed = 0;

    for my $year (@years_to_verify)
    {
        my $perl_year_dir = File::Spec->catfile($base_dir, $year);
        my $aoc_data_dir = File::Spec->catfile($base_dir, '../..', 'aoc-data', $year);

        unless (-d $perl_year_dir)
        {
            say RED . "Error: Perl solutions directory not found for year $year" . RESET;
            say "Expected directory: $perl_year_dir";
            next;
        }

        if (!-d $aoc_data_dir && !$write_missing)
        {
            say YELLOW . "Warning: aoc-data directory not found for year $year" . RESET;
            say "Expected directory: $aoc_data_dir";
            say "Continuing anyway, but no answers will be verified.";
        }

        if (@years_to_verify > 1)
        {
            say "\n" . BLUE . "Verifying $year Advent of Code Solutions" . RESET;
            say "=" x 60;
        }
        else
        {
            say BLUE . "Verifying $year Advent of Code Solutions" . RESET;
            say "=" x 60;
        }

        my $total_verified = 0;
        my $total_correct = 0;
        my $total_incorrect = 0;
        my $total_missing = 0;
        my $total_failed = 0;
        my $total_written = 0;

        for my $day (@days_to_verify)
        {
            for my $part (1, 2)
            {
                my $expected = get_expected_answer($day, $part, $year, $base_dir);

                # Run the solution
                my ($actual, $success, $elapsed_time, $file_exists) = run_solution($day, $part, $year, $base_dir);

                # Case 1: Solution file doesn't exist and answer file doesn't exist
                next if !$file_exists && !defined $expected;

                # Case 2: Solution file doesn't exist but answer file exists
                if (!$file_exists && defined $expected)
                {
                    printf "%s Day %2d Part %d: %s (solution file not found)\n",
                        YELLOW . "○" . RESET, $day, $part, YELLOW . "MISSING" . RESET;
                    $total_missing++;
                    next;
                }

                # Case 3: Solution file exists but failed to run
                if ($file_exists && (!$success || !defined $actual))
                {
                    my $emoji = get_time_emoji($elapsed_time);
                    printf "%s Day %2d Part %d: %s (%.3fs) %s\n",
                        RED . "✗" . RESET, $day, $part, RED . "FAILED TO RUN" . RESET,
                        $elapsed_time, $emoji;
                    $total_failed++;
                    next;
                }

                # Case 4: Solution ran successfully but no expected answer
                if (!defined $expected)
                {
                    my $emoji = get_time_emoji($elapsed_time);
                    my $status_msg = YELLOW . "MISSING" . RESET;

                    # Write to answer file if requested
                    if ($write_missing)
                    {
                        if (write_answer($day, $part, $year, $actual, $base_dir))
                        {
                            $status_msg = YELLOW . "MISSING (wrote: $actual)" . RESET;
                            $total_written++;
                        }
                        else
                        {
                            $status_msg = YELLOW . "MISSING (failed to write)" . RESET;
                        }
                    }

                    printf "%s Day %2d Part %d: %s (answer: %s, %.3fs) %s\n",
                        YELLOW . "○" . RESET, $day, $part, $status_msg, $actual, $elapsed_time, $emoji;
                    $total_missing++;
                    next;
                }

                # Case 5: Solution ran successfully and has expected answer
                $total_verified++;

                if ($actual eq $expected)
                {
                    my $emoji = get_time_emoji($elapsed_time);
                    printf "%s Day %2d Part %d: %s (answer: %s, %.3fs) %s\n",
                        GREEN . "✓" . RESET, $day, $part, GREEN . "CORRECT" . RESET,
                        $actual, $elapsed_time, $emoji;
                    $total_correct++;
                }
                else
                {
                    my $emoji = get_time_emoji($elapsed_time);
                    printf "%s Day %2d Part %d: %s (expected: %s, got: %s, %.3fs) %s\n",
                        RED . "✗" . RESET, $day, $part, RED . "INCORRECT" . RESET,
                        $expected, $actual, $elapsed_time, $emoji;
                    $total_incorrect++;
                }
            }
        }

        # Print summary for this year
        say "\n" . "=" x 60;
        say BLUE . "Summary for $year:" . RESET;
        say "  " . GREEN . "Correct:" . RESET . "      $total_correct";
        say "  " . RED . "Incorrect:" . RESET . "    $total_incorrect";
        say "  " . RED . "Failed:" . RESET . "       $total_failed";
        say "  " . YELLOW . "Missing:" . RESET . "      $total_missing";
        if ($write_missing && $total_written > 0)
        {
            say "  " . YELLOW . "Written:" . RESET . "      $total_written";
        }
        say "  " . BLUE . "Total Verified:" . RESET . " $total_verified";

        $all_total_verified += $total_verified;
        $all_total_correct += $total_correct;
        $all_total_incorrect += $total_incorrect;
        $all_total_missing += $total_missing;
        $all_total_failed += $total_failed;
    }

    # Print overall summary if multiple years
    if (@years_to_verify > 1)
    {
        say "\n" . "=" x 60;
        say BLUE . "Overall Summary:" . RESET;
        say "  " . GREEN . "Correct:" . RESET . "      $all_total_correct";
        say "  " . RED . "Incorrect:" . RESET . "    $all_total_incorrect";
        say "  " . RED . "Failed:" . RESET . "       $all_total_failed";
        say "  " . YELLOW . "Missing:" . RESET . "      $all_total_missing";
        say "  " . BLUE . "Total Verified:" . RESET . " $all_total_verified";
    }

    if ($all_total_incorrect > 0 || $all_total_failed > 0)
    {
        exit 1;
    }
    else
    {
        if ($all_total_verified > 0)
        {
            say "\n" . GREEN . "All verified solutions are correct!" . RESET;
        }
        else
        {
            say "\n" . YELLOW . "No solutions were verified." . RESET;
        }
    }
}

main();

=head1 AUTHOR

Advent of Code Solutions

=cut
