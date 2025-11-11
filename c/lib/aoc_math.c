#include "aoc_math.h"
#include <stdlib.h>
#include <math.h>
#include <string.h>

long long gcd(long long a, long long b) {
    a = llabs(a);
    b = llabs(b);

    while (b != 0) {
        long long temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

long long lcm(long long a, long long b) {
    if (a == 0 || b == 0) return 0;
    return llabs(a / gcd(a, b) * b);
}

long long gcd_array(const long long *numbers, size_t count) {
    if (count == 0) return 0;
    if (count == 1) return llabs(numbers[0]);

    long long result = numbers[0];
    for (size_t i = 1; i < count; i++) {
        result = gcd(result, numbers[i]);
    }
    return result;
}

long long lcm_array(const long long *numbers, size_t count) {
    if (count == 0) return 0;
    if (count == 1) return llabs(numbers[0]);

    long long result = numbers[0];
    for (size_t i = 1; i < count; i++) {
        result = lcm(result, numbers[i]);
    }
    return result;
}

bool is_prime(long long n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;

    for (long long i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
    }
    return true;
}

long long factorial(int n) {
    if (n < 0) return 0;
    if (n <= 1) return 1;

    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

long long binomial(int n, int k) {
    if (k < 0 || k > n) return 0;
    if (k == 0 || k == n) return 1;
    if (k > n - k) k = n - k;

    long long result = 1;
    for (int i = 0; i < k; i++) {
        result *= (n - i);
        result /= (i + 1);
    }
    return result;
}

long long power(long long a, int b) {
    if (b < 0) return 0;
    if (b == 0) return 1;

    long long result = 1;
    long long base = a;

    while (b > 0) {
        if (b & 1) {
            result *= base;
        }
        base *= base;
        b >>= 1;
    }

    return result;
}

long long mod_power(long long a, long long b, long long mod) {
    if (b < 0) return 0;
    if (b == 0) return 1;

    long long result = 1;
    a %= mod;

    while (b > 0) {
        if (b & 1) {
            result = (result * a) % mod;
        }
        a = (a * a) % mod;
        b >>= 1;
    }

    return result;
}

int *primes_up_to(int n, size_t *count) {
    if (n < 2) {
        *count = 0;
        return NULL;
    }

    /* Sieve of Eratosthenes */
    bool *is_prime_arr = calloc(n + 1, sizeof(bool));
    if (is_prime_arr == NULL) {
        *count = 0;
        return NULL;
    }

    /* Initialize all as prime */
    for (int i = 2; i <= n; i++) {
        is_prime_arr[i] = true;
    }

    /* Mark non-primes */
    for (int i = 2; i * i <= n; i++) {
        if (is_prime_arr[i]) {
            for (int j = i * i; j <= n; j += i) {
                is_prime_arr[j] = false;
            }
        }
    }

    /* Count primes */
    *count = 0;
    for (int i = 2; i <= n; i++) {
        if (is_prime_arr[i]) (*count)++;
    }

    /* Collect primes */
    int *primes = malloc(*count * sizeof(int));
    if (primes == NULL) {
        free(is_prime_arr);
        *count = 0;
        return NULL;
    }

    size_t idx = 0;
    for (int i = 2; i <= n; i++) {
        if (is_prime_arr[i]) {
            primes[idx++] = i;
        }
    }

    free(is_prime_arr);
    return primes;
}

long long *prime_factors(long long n, size_t *count) {
    *count = 0;
    if (n <= 1) return NULL;

    size_t capacity = 16;
    long long *factors = malloc(capacity * sizeof(long long));
    if (factors == NULL) return NULL;

    /* Factor out 2s */
    while (n % 2 == 0) {
        if (*count >= capacity) {
            capacity *= 2;
            long long *new_factors = realloc(factors, capacity * sizeof(long long));
            if (new_factors == NULL) {
                free(factors);
                *count = 0;
                return NULL;
            }
            factors = new_factors;
        }
        factors[(*count)++] = 2;
        n /= 2;
    }

    /* Factor out odd numbers */
    for (long long i = 3; i * i <= n; i += 2) {
        while (n % i == 0) {
            if (*count >= capacity) {
                capacity *= 2;
                long long *new_factors = realloc(factors, capacity * sizeof(long long));
                if (new_factors == NULL) {
                    free(factors);
                    *count = 0;
                    return NULL;
                }
                factors = new_factors;
            }
            factors[(*count)++] = i;
            n /= i;
        }
    }

    /* If n is still greater than 1, it's a prime factor */
    if (n > 1) {
        if (*count >= capacity) {
            long long *new_factors = realloc(factors, (capacity + 1) * sizeof(long long));
            if (new_factors == NULL) {
                free(factors);
                *count = 0;
                return NULL;
            }
            factors = new_factors;
        }
        factors[(*count)++] = n;
    }

    return factors;
}

long long *divisors(long long n, size_t *count) {
    *count = 0;
    if (n <= 0) return NULL;

    size_t capacity = 16;
    long long *divs = malloc(capacity * sizeof(long long));
    if (divs == NULL) return NULL;

    for (long long i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            /* Add i */
            if (*count >= capacity) {
                capacity *= 2;
                long long *new_divs = realloc(divs, capacity * sizeof(long long));
                if (new_divs == NULL) {
                    free(divs);
                    *count = 0;
                    return NULL;
                }
                divs = new_divs;
            }
            divs[(*count)++] = i;

            /* Add n/i if different from i */
            if (i != n / i) {
                if (*count >= capacity) {
                    capacity *= 2;
                    long long *new_divs = realloc(divs, capacity * sizeof(long long));
                    if (new_divs == NULL) {
                        free(divs);
                        *count = 0;
                        return NULL;
                    }
                    divs = new_divs;
                }
                divs[(*count)++] = n / i;
            }
        }
    }

    return divs;
}
