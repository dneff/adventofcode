/*
 * Advent of Code C Solutions - Verification Script
 *
 * This program verifies C solutions against known correct answers stored
 * in the aoc-data repository.
 *
 * Usage:
 *   ./verify_solutions [YEAR] [DAY] [OPTIONS]
 *
 * Options:
 *   --year YEAR, -y YEAR      The year to verify (e.g., 2015)
 *   --day DAY, -d DAY         The day to verify (1-25)
 *   --write-missing, -w       Write solution output to missing answer files
 *   --help, -h                Show this help message
 *
 * Examples:
 *   ./verify_solutions              # Verify all years
 *   ./verify_solutions 2015         # Verify year 2015
 *   ./verify_solutions 2015 1       # Verify year 2015, day 1
 *   ./verify_solutions --year 2015 --day 1 --write-missing
 */

#define _POSIX_C_SOURCE 200809L
#define _XOPEN_SOURCE 700

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <dirent.h>
#include <time.h>
#include <errno.h>

/* ANSI color codes */
#define COLOR_GREEN "\033[92m"
#define COLOR_RED "\033[91m"
#define COLOR_YELLOW "\033[93m"
#define COLOR_BLUE "\033[94m"
#define COLOR_RESET "\033[0m"

typedef struct {
    int year;
    int day;
    bool write_missing;
} Options;

/* Forward declarations */
void print_help(void);
bool parse_args(int argc, char *argv[], Options *opts);
bool directory_exists(const char *path);
bool file_exists(const char *path);
char *read_answer_file(int year, int day, int part);
bool write_answer_file(int year, int day, int part, const char *answer);
bool run_solution(int year, int day, int part, char **output, double *elapsed);
bool build_solution(int year, int day);
void verify_day(int year, int day, Options *opts, int *stats);
void verify_year(int year, Options *opts);
const char *get_time_emoji(double elapsed);
int compare_strings(const char *a, const char *b);

void print_help(void) {
    printf("Advent of Code C Solutions - Verification Script\n\n");
    printf("Usage: ./verify_solutions [YEAR] [DAY] [OPTIONS]\n\n");
    printf("Positional Arguments:\n");
    printf("  YEAR                      The year to verify (e.g., 2015)\n");
    printf("  DAY                       The day to verify (1-25)\n\n");
    printf("Options:\n");
    printf("  --year YEAR, -y YEAR      The year to verify\n");
    printf("  --day DAY, -d DAY         The day to verify\n");
    printf("  --write-missing, -w       Write solution output to missing answer files\n");
    printf("  --help, -h                Show this help message\n\n");
    printf("Examples:\n");
    printf("  ./verify_solutions              # Verify all years\n");
    printf("  ./verify_solutions 2015         # Verify year 2015\n");
    printf("  ./verify_solutions 2015 1       # Verify year 2015, day 1\n");
    printf("  ./verify_solutions --year 2015 --day 1 --write-missing\n");
}

bool parse_args(int argc, char *argv[], Options *opts) {
    opts->year = -1;
    opts->day = -1;
    opts->write_missing = false;

    int year_pos = -1;
    int day_pos = -1;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_help();
            exit(0);
        } else if (strcmp(argv[i], "-w") == 0 || strcmp(argv[i], "--write-missing") == 0) {
            opts->write_missing = true;
        } else if ((strcmp(argv[i], "-y") == 0 || strcmp(argv[i], "--year") == 0) && i + 1 < argc) {
            opts->year = atoi(argv[++i]);
        } else if ((strcmp(argv[i], "-d") == 0 || strcmp(argv[i], "--day") == 0) && i + 1 < argc) {
            opts->day = atoi(argv[++i]);
        } else if (argv[i][0] != '-') {
            /* Positional argument */
            if (year_pos == -1) {
                year_pos = atoi(argv[i]);
            } else if (day_pos == -1) {
                day_pos = atoi(argv[i]);
            }
        }
    }

    /* Prioritize positional arguments */
    if (year_pos != -1) opts->year = year_pos;
    if (day_pos != -1) opts->day = day_pos;

    return true;
}

bool directory_exists(const char *path) {
    struct stat st;
    return stat(path, &st) == 0 && S_ISDIR(st.st_mode);
}

bool file_exists(const char *path) {
    return access(path, F_OK) == 0;
}

char *read_answer_file(int year, int day, int part) {
    char path[512];
    snprintf(path, sizeof(path), "../../aoc-data/%d/%d/solution-%d", year, day, part);

    FILE *f = fopen(path, "r");
    if (!f) return NULL;

    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);

    if (size <= 0) {
        fclose(f);
        return NULL;
    }

    char *content = malloc(size + 1);
    if (!content) {
        fclose(f);
        return NULL;
    }

    size_t read = fread(content, 1, size, f);
    content[read] = '\0';
    fclose(f);

    /* Trim whitespace */
    char *end = content + strlen(content) - 1;
    while (end > content && (*end == ' ' || *end == '\n' || *end == '\r' || *end == '\t')) {
        *end = '\0';
        end--;
    }

    /* Return NULL if empty or just "0" */
    if (strlen(content) == 0 || strcmp(content, "0") == 0) {
        free(content);
        return NULL;
    }

    return content;
}

bool write_answer_file(int year, int day, int part, const char *answer) {
    char dir_path[512];
    char file_path[512];

    snprintf(dir_path, sizeof(dir_path), "../../aoc-data/%d/%d", year, day);
    snprintf(file_path, sizeof(file_path), "%s/solution-%d", dir_path, part);

    /* Create directory if needed */
    char cmd[1024];
    snprintf(cmd, sizeof(cmd), "mkdir -p %s", dir_path);
    if (system(cmd) != 0) {
        return false;
    }

    FILE *f = fopen(file_path, "w");
    if (!f) return false;

    fprintf(f, "%s\n", answer);
    fclose(f);
    return true;
}

bool run_solution(int year, int day, int part, char **output, double *elapsed) {
    char path[256];
    snprintf(path, sizeof(path), "%d/%02d/solution%d", year, day, part);

    if (!file_exists(path)) {
        return false;
    }

    /* Run the solution and capture output */
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "./%s 2>&1", path);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    FILE *fp = popen(cmd, "r");
    if (!fp) return false;

    char buffer[4096] = {0};
    size_t total = 0;

    while (fgets(buffer + total, sizeof(buffer) - total, fp)) {
        total = strlen(buffer);
    }

    int status = pclose(fp);

    clock_gettime(CLOCK_MONOTONIC, &end);
    *elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    if (status != 0) return false;

    /* Extract answer from output (looking for "Part X: answer") */
    char *line = strtok(buffer, "\n");
    while (line) {
        char part_str[32];
        snprintf(part_str, sizeof(part_str), "Part %d:", part);

        if (strstr(line, part_str)) {
            char *colon = strchr(line, ':');
            if (colon) {
                colon++;
                while (*colon == ' ') colon++;

                *output = strdup(colon);
                return true;
            }
        }
        line = strtok(NULL, "\n");
    }

    return false;
}

bool build_solution(int year, int day) {
    char path[256];
    snprintf(path, sizeof(path), "%d/%02d", year, day);

    if (!directory_exists(path)) return false;

    /* Build using make */
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "cd %s && make > /dev/null 2>&1", path);

    return system(cmd) == 0;
}

const char *get_time_emoji(double elapsed) {
    if (elapsed < 1.0) return "⚡";
    if (elapsed < 3.0) return "🚀";
    if (elapsed < 10.0) return "▶️";
    if (elapsed < 30.0) return "🐢";
    return "🐌";
}

int compare_strings(const char *a, const char *b) {
    if (!a || !b) return a == b ? 0 : 1;

    /* Trim and compare */
    while (*a == ' ') a++;
    while (*b == ' ') b++;

    size_t len_a = strlen(a);
    size_t len_b = strlen(b);

    while (len_a > 0 && (a[len_a - 1] == ' ' || a[len_a - 1] == '\n')) len_a--;
    while (len_b > 0 && (b[len_b - 1] == ' ' || b[len_b - 1] == '\n')) len_b--;

    if (len_a != len_b) return 1;
    return strncmp(a, b, len_a);
}

void verify_day(int year, int day, Options *opts, int *stats) {
    /* stats: [verified, correct, incorrect, missing, failed, written] */

    /* Build the solution first */
    if (!build_solution(year, day)) {
        return;  /* Skip if can't build */
    }

    for (int part = 1; part <= 2; part++) {
        char *expected = read_answer_file(year, day, part);
        char *actual = NULL;
        double elapsed = 0.0;

        char solution_path[256];
        snprintf(solution_path, sizeof(solution_path), "%d/%02d/solution%d", year, day, part);

        bool file_present = file_exists(solution_path);

        if (!file_present && !expected) {
            continue;  /* Skip entirely */
        }

        if (!file_present && expected) {
            printf("%s○%s Day %2d Part %d: %sMISSING%s (solution file not found)\n",
                   COLOR_YELLOW, COLOR_RESET, day, part, COLOR_YELLOW, COLOR_RESET);
            stats[3]++;
            free(expected);
            continue;
        }

        bool success = run_solution(year, day, part, &actual, &elapsed);

        if (!success || !actual) {
            printf("%s✗%s Day %2d Part %d: %sFAILED TO RUN%s (%.3fs) %s\n",
                   COLOR_RED, COLOR_RESET, day, part, COLOR_RED, COLOR_RESET, elapsed,
                   get_time_emoji(elapsed));
            stats[4]++;
            free(expected);
            continue;
        }

        if (!expected) {
            const char *status_msg = "MISSING";
            if (opts->write_missing) {
                if (write_answer_file(year, day, part, actual)) {
                    printf("%s○%s Day %2d Part %d: %sMISSING (wrote: %s)%s (answer: %s, %.3fs) %s\n",
                           COLOR_YELLOW, COLOR_RESET, day, part, COLOR_YELLOW, actual,
                           COLOR_RESET, actual, elapsed, get_time_emoji(elapsed));
                    stats[5]++;
                } else {
                    printf("%s○%s Day %2d Part %d: %sMISSING (failed to write)%s (answer: %s, %.3fs) %s\n",
                           COLOR_YELLOW, COLOR_RESET, day, part, COLOR_YELLOW,
                           COLOR_RESET, actual, elapsed, get_time_emoji(elapsed));
                }
            } else {
                printf("%s○%s Day %2d Part %d: %s%s%s (answer: %s, %.3fs) %s\n",
                       COLOR_YELLOW, COLOR_RESET, day, part, COLOR_YELLOW, status_msg,
                       COLOR_RESET, actual, elapsed, get_time_emoji(elapsed));
            }
            stats[3]++;
            free(actual);
            continue;
        }

        /* Compare answers */
        stats[0]++;
        if (compare_strings(actual, expected) == 0) {
            printf("%s✓%s Day %2d Part %d: %sCORRECT%s (answer: %s, %.3fs) %s\n",
                   COLOR_GREEN, COLOR_RESET, day, part, COLOR_GREEN, COLOR_RESET,
                   actual, elapsed, get_time_emoji(elapsed));
            stats[1]++;
        } else {
            printf("%s✗%s Day %2d Part %d: %sINCORRECT%s (expected: %s, got: %s, %.3fs) %s\n",
                   COLOR_RED, COLOR_RESET, day, part, COLOR_RED, COLOR_RESET,
                   expected, actual, elapsed, get_time_emoji(elapsed));
            stats[2]++;
        }

        free(expected);
        free(actual);
    }
}

void verify_year(int year, Options *opts) {
    char year_path[256];
    snprintf(year_path, sizeof(year_path), "%d", year);

    if (!directory_exists(year_path)) {
        printf("%sError: Directory not found for year %d%s\n", COLOR_RED, year, COLOR_RESET);
        return;
    }

    printf("\n%sVerifying %d Advent of Code Solutions%s\n", COLOR_BLUE, year, COLOR_RESET);
    printf("============================================================\n");

    int stats[6] = {0};  /* verified, correct, incorrect, missing, failed, written */

    if (opts->day > 0) {
        verify_day(year, opts->day, opts, stats);
    } else {
        for (int day = 1; day <= 25; day++) {
            verify_day(year, day, opts, stats);
        }
    }

    printf("\n============================================================\n");
    printf("%sSummary for %d:%s\n", COLOR_BLUE, year, COLOR_RESET);
    printf("  %sCorrect:%s      %d\n", COLOR_GREEN, COLOR_RESET, stats[1]);
    printf("  %sIncorrect:%s    %d\n", COLOR_RED, COLOR_RESET, stats[2]);
    printf("  %sFailed:%s       %d\n", COLOR_RED, COLOR_RESET, stats[4]);
    printf("  %sMissing:%s      %d\n", COLOR_YELLOW, COLOR_RESET, stats[3]);
    if (opts->write_missing && stats[5] > 0) {
        printf("  %sWritten:%s      %d\n", COLOR_YELLOW, COLOR_RESET, stats[5]);
    }
    printf("  %sTotal Verified:%s %d\n", COLOR_BLUE, COLOR_RESET, stats[0]);

    if (stats[2] > 0 || stats[4] > 0) {
        exit(1);
    } else if (stats[0] > 0) {
        printf("\n%sAll verified solutions are correct!%s\n", COLOR_GREEN, COLOR_RESET);
    } else {
        printf("\n%sNo solutions were verified.%s\n", COLOR_YELLOW, COLOR_RESET);
    }
}

int main(int argc, char *argv[]) {
    Options opts;
    if (!parse_args(argc, argv, &opts)) {
        return 1;
    }

    if (opts.year > 0) {
        verify_year(opts.year, &opts);
    } else {
        /* Verify all years */
        DIR *dir = opendir(".");
        if (!dir) {
            fprintf(stderr, "Error opening current directory\n");
            return 1;
        }

        struct dirent *entry;
        int years[100];
        int year_count = 0;

        while ((entry = readdir(dir)) != NULL) {
            /* Skip . and .. */
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
                continue;
            }

            /* Check if it's a directory */
            struct stat st;
            if (stat(entry->d_name, &st) == 0 && S_ISDIR(st.st_mode)) {
                if (entry->d_name[0] >= '2') {
                    int year = atoi(entry->d_name);
                    if (year >= 2015 && year <= 2030) {
                        years[year_count++] = year;
                    }
                }
            }
        }
        closedir(dir);

        /* Sort years */
        for (int i = 0; i < year_count - 1; i++) {
            for (int j = i + 1; j < year_count; j++) {
                if (years[i] > years[j]) {
                    int temp = years[i];
                    years[i] = years[j];
                    years[j] = temp;
                }
            }
        }

        for (int i = 0; i < year_count; i++) {
            verify_year(years[i], &opts);
        }
    }

    return 0;
}
