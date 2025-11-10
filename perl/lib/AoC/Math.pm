package AoC::Math;

use v5.40;
use strict;
use warnings;
use feature 'signatures';
no warnings 'experimental::signatures';

use List::Util qw(min max);

use Exporter 'import';
our @EXPORT_OK = qw(
    gcd
    lcm
    gcd_list
    lcm_list
    is_prime
    primes_up_to
    factors
    divisors
    factorial
    binomial
    sign
    clamp
);

=head1 NAME

AoC::Math - Mathematical utility functions

=head1 SYNOPSIS

    use AoC::Math qw(gcd lcm primes_up_to factorial);

    my $g = gcd(48, 18);
    my $l = lcm(12, 18);
    my @primes = primes_up_to(100);
    my $f = factorial(5);

=head1 DESCRIPTION

Provides mathematical utility functions commonly needed in Advent of Code.

=head1 FUNCTIONS

=head2 gcd($a, $b)

Calculates the greatest common divisor using Euclid's algorithm.

=cut

sub gcd ($a, $b)
{
    ($a, $b) = ($b, $a) if $b > $a;
    while ($b != 0)
    {
        ($a, $b) = ($b, $a % $b);
    }
    return $a;
}

=head2 lcm($a, $b)

Calculates the least common multiple.

=cut

sub lcm ($a, $b)
{
    return ($a * $b) / gcd($a, $b);
}

=head2 gcd_list(@numbers)

Calculates GCD of a list of numbers.

=cut

sub gcd_list (@numbers)
{
    return $numbers[0] if @numbers == 1;
    my $result = $numbers[0];
    for my $n (@numbers[1 .. $#numbers])
    {
        $result = gcd($result, $n);
    }
    return $result;
}

=head2 lcm_list(@numbers)

Calculates LCM of a list of numbers.

=cut

sub lcm_list (@numbers)
{
    return $numbers[0] if @numbers == 1;
    my $result = $numbers[0];
    for my $n (@numbers[1 .. $#numbers])
    {
        $result = lcm($result, $n);
    }
    return $result;
}

=head2 is_prime($n)

Checks if a number is prime.

=cut

sub is_prime ($n)
{
    return 0 if $n < 2;
    return 1 if $n == 2;
    return 0 if $n % 2 == 0;

    for (my $i = 3; $i * $i <= $n; $i += 2)
    {
        return 0 if $n % $i == 0;
    }
    return 1;
}

=head2 primes_up_to($n)

Returns all prime numbers up to n using Sieve of Eratosthenes.

=cut

sub primes_up_to ($n)
{
    return () if $n < 2;

    my @is_prime = (1) x ($n + 1);
    $is_prime[0] = $is_prime[1] = 0;

    for (my $i = 2; $i * $i <= $n; $i++)
    {
        if ($is_prime[$i])
        {
            for (my $j = $i * $i; $j <= $n; $j += $i)
            {
                $is_prime[$j] = 0;
            }
        }
    }

    my @primes = grep { $is_prime[$_] } 0 .. $n;
    return @primes;
}

=head2 factors($n)

Returns the prime factors of n.

=cut

sub factors ($n)
{
    my @factors;
    my $d = 2;

    while ($d * $d <= $n)
    {
        while ($n % $d == 0)
        {
            push @factors, $d;
            $n /= $d;
        }
        $d++;
    }

    push @factors, $n if $n > 1;
    return @factors;
}

=head2 divisors($n)

Returns all divisors of n.

=cut

sub divisors ($n)
{
    my @divisors;
    for (my $i = 1; $i * $i <= $n; $i++)
    {
        if ($n % $i == 0)
        {
            push @divisors, $i;
            push @divisors, $n / $i if $i != $n / $i;
        }
    }
    return sort { $a <=> $b } @divisors;
}

=head2 factorial($n)

Calculates n!

=cut

sub factorial ($n)
{
    my $result = 1;
    $result *= $_ for 2 .. $n;
    return $result;
}

=head2 binomial($n, $k)

Calculates binomial coefficient C(n, k) = n! / (k! * (n-k)!)

=cut

sub binomial ($n, $k)
{
    return 0 if $k > $n;
    return 1 if $k == 0 || $k == $n;

    # Optimize by using the smaller of k and n-k
    $k = $n - $k if $k > $n - $k;

    my $result = 1;
    for my $i (1 .. $k)
    {
        $result *= ($n - $k + $i);
        $result /= $i;
    }
    return $result;
}

=head2 sign($n)

Returns -1, 0, or 1 depending on the sign of n.

=cut

sub sign ($n)
{
    return $n <=> 0;
}

=head2 clamp($value, $min, $max)

Clamps a value between min and max.

=cut

sub clamp ($value, $min_val, $max_val)
{
    return max($min_val, min($max_val, $value));
}

1;

=head1 AUTHOR

Advent of Code Solutions

=cut
