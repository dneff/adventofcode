#define _POSIX_C_SOURCE 200809L

#include "aoc_input.h"
#include "aoc_utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

LineArray read_lines(const char *filename) {
    LineArray result = {NULL, 0};
    FILE *file = fopen(filename, "r");

    if (file == NULL) {
        fprintf(stderr, "Error: Cannot open file %s\n", filename);
        return result;
    }

    size_t capacity = 16;
    result.lines = malloc(capacity * sizeof(char *));
    if (result.lines == NULL) {
        fclose(file);
        return result;
    }

    char *line = NULL;
    size_t len = 0;
    ssize_t read;

    while ((read = getline(&line, &len, file)) != -1) {
        /* Remove newline */
        if (read > 0 && line[read - 1] == '\n') {
            line[read - 1] = '\0';
            read--;
        }
        if (read > 0 && line[read - 1] == '\r') {
            line[read - 1] = '\0';
        }

        /* Expand array if needed */
        if (result.count >= capacity) {
            capacity *= 2;
            char **new_lines = realloc(result.lines, capacity * sizeof(char *));
            if (new_lines == NULL) {
                free(line);
                fclose(file);
                free_line_array(&result);
                result.count = 0;
                return result;
            }
            result.lines = new_lines;
        }

        /* Copy the line */
        result.lines[result.count] = strdup(line);
        if (result.lines[result.count] == NULL) {
            free(line);
            fclose(file);
            free_line_array(&result);
            result.count = 0;
            return result;
        }
        result.count++;
    }

    free(line);
    fclose(file);
    return result;
}

char *read_file(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Error: Cannot open file %s\n", filename);
        return NULL;
    }

    /* Get file size */
    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);

    /* Allocate buffer */
    char *content = malloc(size + 1);
    if (content == NULL) {
        fclose(file);
        return NULL;
    }

    /* Read file */
    size_t read_size = fread(content, 1, size, file);
    content[read_size] = '\0';

    fclose(file);
    return content;
}

IntArray read_numbers(const char *filename) {
    IntArray result = {NULL, 0};
    LineArray lines = read_lines(filename);

    if (lines.count == 0) {
        return result;
    }

    result.numbers = malloc(lines.count * sizeof(int));
    if (result.numbers == NULL) {
        free_line_array(&lines);
        return result;
    }

    for (size_t i = 0; i < lines.count; i++) {
        result.numbers[i] = atoi(trim(lines.lines[i]));
        result.count++;
    }

    free_line_array(&lines);
    return result;
}

int *parse_numbers(const char *text, size_t *count) {
    if (text == NULL || count == NULL) return NULL;

    *count = 0;
    size_t capacity = 16;
    int *numbers = malloc(capacity * sizeof(int));
    if (numbers == NULL) return NULL;

    const char *p = text;
    while (*p) {
        /* Skip non-digit characters (except minus sign) */
        while (*p && !isdigit(*p) && *p != '-') p++;
        if (!*p) break;

        /* Parse number */
        char *end;
        int num = (int)strtol(p, &end, 10);

        /* Only add if we actually parsed something */
        if (end != p) {
            /* Expand array if needed */
            if (*count >= capacity) {
                capacity *= 2;
                int *new_numbers = realloc(numbers, capacity * sizeof(int));
                if (new_numbers == NULL) {
                    free(numbers);
                    *count = 0;
                    return NULL;
                }
                numbers = new_numbers;
            }

            numbers[(*count)++] = num;
            p = end;
        } else {
            p++;
        }
    }

    return numbers;
}

void free_line_array(LineArray *arr) {
    if (arr == NULL) return;

    for (size_t i = 0; i < arr->count; i++) {
        free(arr->lines[i]);
    }
    free(arr->lines);
    arr->lines = NULL;
    arr->count = 0;
}

void free_int_array(IntArray *arr) {
    if (arr == NULL) return;

    free(arr->numbers);
    arr->numbers = NULL;
    arr->count = 0;
}

char *get_input_path(int year, int day, char *buffer, size_t buffer_size) {
    snprintf(buffer, buffer_size, "../../../aoc-data/%d/%d/input", year, day);
    return buffer;
}
