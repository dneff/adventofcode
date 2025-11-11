#!/usr/bin/env node

/**
 * Verify Advent of Code solutions against known correct answers.
 *
 * This script runs each solution file for a specified year and compares the output
 * against the answer files stored in aoc-data.
 *
 * Usage:
 *     node verify_solutions.js [YEAR] [DAY] [OPTIONS]
 *     npm run verify [-- YEAR] [DAY] [OPTIONS]
 *
 * Positional Arguments:
 *     YEAR                      The year to verify (e.g., 2015, 2016, 2017)
 *     DAY                       The day to verify (1-25)
 *
 * Options:
 *     --year YEAR, -y YEAR      The year to verify (alternative to positional)
 *     --day DAY, -d DAY         The day to verify (alternative to positional)
 *     --write-missing, -w       Write solution output to missing answer files
 *
 * Examples:
 *     npm run verify                              # Verify all years
 *     npm run verify -- 2015                      # Verify year 2015
 *     npm run verify -- 2015 20                   # Verify year 2015, day 20
 *     npm run verify -- --year 2015 --day 20 --write-missing
 *
 * If no year is specified, all years will be verified.
 * If no day is specified, all days will be verified.
 */

import { readFileSync, readdirSync, existsSync, mkdirSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Colors for terminal output
const GREEN = '\x1b[92m';
const RED = '\x1b[91m';
const YELLOW = '\x1b[93m';
const BLUE = '\x1b[94m';
const RESET = '\x1b[0m';

/**
 * Get an emoji based on the execution time.
 *
 * @param {number} elapsedTime - Execution time in seconds
 * @returns {string} Emoji string representing the speed
 */
function getTimeEmoji(elapsedTime) {
  if (elapsedTime < 1.0) return '⚡';
  if (elapsedTime < 3.0) return '🚀';
  if (elapsedTime < 10.0) return '▶️';
  if (elapsedTime < 30.0) return '🐢';
  return '🐌';
}

/**
 * Read the expected answer from aoc-data directory.
 *
 * @param {number} day - Day number (1-25)
 * @param {number} part - Part number (1 or 2)
 * @param {number} year - Year (e.g., 2015, 2016, 2017)
 * @param {string} baseDir - Base directory of the javascript solutions
 * @returns {string|null} Expected answer as string, or null if file doesn't exist or is empty
 */
function getExpectedAnswer(day, part, year, baseDir) {
  // Path from javascript/ dir to aoc-data is ../aoc-data
  const answerFile = join(baseDir, '..', 'aoc-data', String(year), String(day), `solution-${part}`);

  if (!existsSync(answerFile)) {
    return null;
  }

  try {
    const content = readFileSync(answerFile, 'utf-8').trim();
    // Return null if empty or just '0'
    if (content && content !== '0') {
      return content;
    }
    return null;
  } catch (error) {
    return null;
  }
}

/**
 * Write an answer to the aoc-data directory.
 *
 * @param {number} day - Day number (1-25)
 * @param {number} part - Part number (1 or 2)
 * @param {number} year - Year (e.g., 2015, 2016, 2017)
 * @param {string} answer - The answer to write
 * @param {string} baseDir - Base directory of the javascript solutions
 * @returns {boolean} True if successfully written, false otherwise
 */
function writeAnswer(day, part, year, answer, baseDir) {
  // Path from javascript/ dir to aoc-data is ../aoc-data
  const answerDir = join(baseDir, '..', 'aoc-data', String(year), String(day));
  const answerFile = join(answerDir, `solution-${part}`);

  try {
    // Create directory if it doesn't exist
    mkdirSync(answerDir, { recursive: true });

    // Write the answer
    writeFileSync(answerFile, answer.trim() + '\n', 'utf-8');
    return true;
  } catch (error) {
    console.error(`${RED}Error writing answer: ${error.message}${RESET}`);
    return false;
  }
}

/**
 * Run a solution file and extract the answer.
 *
 * @param {number} day - Day number (1-25)
 * @param {number} part - Part number (1 or 2)
 * @param {number} year - Year (e.g., 2015, 2016, 2017)
 * @param {string} baseDir - Base directory of the javascript solutions
 * @returns {Promise<{answer: string|null, success: boolean, elapsedTime: number, fileExists: boolean}>}
 */
async function runSolution(day, part, year, baseDir) {
  const dayPadded = String(day).padStart(2, '0');
  const solutionFile = join(baseDir, String(year), dayPadded, `solution${part}.js`);

  if (!existsSync(solutionFile)) {
    return { answer: null, success: false, elapsedTime: 0.0, fileExists: false };
  }

  return new Promise((resolve) => {
    const startTime = Date.now();
    const child = spawn('node', [solutionFile], {
      cwd: dirname(solutionFile),
      timeout: 30000,
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    child.on('close', (code) => {
      const elapsedTime = (Date.now() - startTime) / 1000;

      if (code !== 0) {
        resolve({ answer: null, success: false, elapsedTime, fileExists: true });
        return;
      }

      // Extract the answer from output (looking for lines like "Part 1: 138")
      const lines = stdout.split('\n');
      for (const line of lines) {
        if (line.includes(`Part ${part}:`)) {
          const answer = line.split(':').slice(-1)[0].trim();
          resolve({ answer, success: true, elapsedTime, fileExists: true });
          return;
        }
      }

      resolve({ answer: null, success: false, elapsedTime, fileExists: true });
    });

    child.on('error', () => {
      const elapsedTime = (Date.now() - startTime) / 1000;
      resolve({ answer: null, success: false, elapsedTime, fileExists: true });
    });
  });
}

/**
 * Get the list of years to verify.
 *
 * @param {string} baseDir - Base directory of the javascript solutions
 * @param {number|null} year - Specific year to verify, or null for all years
 * @returns {number[]} List of years to verify
 */
function getYearsToVerify(baseDir, year) {
  if (year !== null) {
    return [year];
  }

  // Find all years with javascript solutions
  if (!existsSync(baseDir)) {
    return [];
  }

  const years = [];
  const items = readdirSync(baseDir, { withFileTypes: true });
  for (const item of items) {
    if (item.isDirectory() && /^\d{4}$/.test(item.name)) {
      years.push(parseInt(item.name, 10));
    }
  }

  return years.sort((a, b) => a - b);
}

/**
 * Parse command line arguments.
 *
 * @param {string[]} args - Command line arguments
 * @returns {{year: number|null, day: number|null, writeMissing: boolean}}
 */
function parseArgs(args) {
  let year = null;
  let day = null;
  let writeMissing = false;

  // Check for positional arguments first
  const positionalArgs = args.filter((arg) => !arg.startsWith('-'));
  if (positionalArgs.length > 0) {
    const yearArg = parseInt(positionalArgs[0], 10);
    if (!isNaN(yearArg)) {
      year = yearArg;
    }
  }
  if (positionalArgs.length > 1) {
    const dayArg = parseInt(positionalArgs[1], 10);
    if (!isNaN(dayArg)) {
      day = dayArg;
    }
  }

  // Check for flag arguments (override positional)
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if ((arg === '--year' || arg === '-y') && i + 1 < args.length) {
      const yearArg = parseInt(args[i + 1], 10);
      if (!isNaN(yearArg)) {
        year = yearArg;
      }
      i++;
    } else if ((arg === '--day' || arg === '-d') && i + 1 < args.length) {
      const dayArg = parseInt(args[i + 1], 10);
      if (!isNaN(dayArg)) {
        day = dayArg;
      }
      i++;
    } else if (arg === '--write-missing' || arg === '-w') {
      writeMissing = true;
    }
  }

  return { year, day, writeMissing };
}

/**
 * Main verification function.
 */
async function main() {
  const args = process.argv.slice(2);
  const { year, day, writeMissing } = parseArgs(args);

  const baseDir = __dirname;
  const yearsToVerify = getYearsToVerify(baseDir, year);

  if (yearsToVerify.length === 0) {
    console.error(`${RED}Error: No JavaScript solutions directories found${RESET}`);
    process.exit(1);
  }

  // Determine days to verify
  let daysToVerify;
  if (day !== null) {
    if (day < 1 || day > 25) {
      console.error(`${RED}Error: Day must be between 1 and 25${RESET}`);
      process.exit(1);
    }
    daysToVerify = [day];
  } else {
    daysToVerify = Array.from({ length: 25 }, (_, i) => i + 1);
  }

  // Verify all years
  let allTotalVerified = 0;
  let allTotalCorrect = 0;
  let allTotalIncorrect = 0;
  let allTotalMissing = 0;
  let allTotalFailed = 0;

  for (const year of yearsToVerify) {
    const jsYearDir = join(baseDir, String(year));
    const aocDataDir = join(baseDir, '..', 'aoc-data', String(year));

    if (!existsSync(jsYearDir)) {
      console.error(`${RED}Error: JavaScript solutions directory not found for year ${year}${RESET}`);
      console.error(`Expected directory: ${jsYearDir}`);
      continue;
    }

    if (!existsSync(aocDataDir) && !writeMissing) {
      console.warn(`${YELLOW}Warning: aoc-data directory not found for year ${year}${RESET}`);
      console.warn(`Expected directory: ${aocDataDir}`);
      console.warn('Continuing anyway, but no answers will be verified.');
    }

    if (yearsToVerify.length > 1) {
      console.log(`\n${BLUE}Verifying ${year} Advent of Code Solutions${RESET}`);
      console.log('='.repeat(60));
    } else {
      console.log(`${BLUE}Verifying ${year} Advent of Code Solutions${RESET}`);
      console.log('='.repeat(60));
    }

    let totalVerified = 0;
    let totalCorrect = 0;
    let totalIncorrect = 0;
    let totalMissing = 0;
    let totalFailed = 0;
    let totalWritten = 0;

    for (const day of daysToVerify) {
      for (const part of [1, 2]) {
        const expected = getExpectedAnswer(day, part, year, baseDir);

        // Run the solution
        const { answer: actual, success, elapsedTime, fileExists } = await runSolution(day, part, year, baseDir);

        // Case 1: Solution file doesn't exist and answer file doesn't exist
        // -> Skip entirely, no output, no counting
        if (!fileExists && expected === null) {
          continue;
        }

        // Case 2: Solution file doesn't exist but answer file exists
        // -> Show MISSING status (solution file is missing)
        if (!fileExists && expected !== null) {
          console.log(
            `${YELLOW}○${RESET} Day ${String(day).padStart(2)} Part ${part}: ${YELLOW}MISSING${RESET} (solution file not found)`
          );
          totalMissing++;
          continue;
        }

        // Case 3: Solution file exists but failed to run
        if (fileExists && (!success || actual === null)) {
          const emoji = getTimeEmoji(elapsedTime);
          console.log(
            `${RED}✗${RESET} Day ${String(day).padStart(2)} Part ${part}: ${RED}FAILED TO RUN${RESET} (${elapsedTime.toFixed(3)}s) ${emoji}`
          );
          totalFailed++;
          continue;
        }

        // Case 4: Solution ran successfully but no expected answer
        // -> Show MISSING status (answer is missing)
        if (expected === null) {
          const emoji = getTimeEmoji(elapsedTime);
          let statusMsg = `${YELLOW}MISSING${RESET}`;

          // Write to answer file if requested
          if (writeMissing) {
            if (writeAnswer(day, part, year, actual, baseDir)) {
              statusMsg = `${YELLOW}MISSING (wrote: ${actual})${RESET}`;
              totalWritten++;
            } else {
              statusMsg = `${YELLOW}MISSING (failed to write)${RESET}`;
            }
          }

          console.log(
            `${YELLOW}○${RESET} Day ${String(day).padStart(2)} Part ${part}: ${statusMsg} (answer: ${actual}, ${elapsedTime.toFixed(3)}s) ${emoji}`
          );
          totalMissing++;
          continue;
        }

        // Case 5: Solution ran successfully and has expected answer
        // -> Compare and show CORRECT/INCORRECT
        totalVerified++;

        if (actual === expected) {
          const emoji = getTimeEmoji(elapsedTime);
          console.log(
            `${GREEN}✓${RESET} Day ${String(day).padStart(2)} Part ${part}: ${GREEN}CORRECT${RESET} (answer: ${actual}, ${elapsedTime.toFixed(3)}s) ${emoji}`
          );
          totalCorrect++;
        } else {
          const emoji = getTimeEmoji(elapsedTime);
          console.log(
            `${RED}✗${RESET} Day ${String(day).padStart(2)} Part ${part}: ${RED}INCORRECT${RESET} (expected: ${expected}, got: ${actual}, ${elapsedTime.toFixed(3)}s) ${emoji}`
          );
          totalIncorrect++;
        }
      }
    }

    // Print summary for this year
    console.log('\n' + '='.repeat(60));
    console.log(`${BLUE}Summary for ${year}:${RESET}`);
    console.log(`  ${GREEN}Correct:${RESET}      ${totalCorrect}`);
    console.log(`  ${RED}Incorrect:${RESET}    ${totalIncorrect}`);
    console.log(`  ${RED}Failed:${RESET}       ${totalFailed}`);
    console.log(`  ${YELLOW}Missing:${RESET}      ${totalMissing}`);
    if (writeMissing && totalWritten > 0) {
      console.log(`  ${YELLOW}Written:${RESET}      ${totalWritten}`);
    }
    console.log(`  ${BLUE}Total Verified:${RESET} ${totalVerified}`);

    allTotalVerified += totalVerified;
    allTotalCorrect += totalCorrect;
    allTotalIncorrect += totalIncorrect;
    allTotalMissing += totalMissing;
    allTotalFailed += totalFailed;
  }

  // Print overall summary if multiple years
  if (yearsToVerify.length > 1) {
    console.log('\n' + '='.repeat(60));
    console.log(`${BLUE}Overall Summary:${RESET}`);
    console.log(`  ${GREEN}Correct:${RESET}      ${allTotalCorrect}`);
    console.log(`  ${RED}Incorrect:${RESET}    ${allTotalIncorrect}`);
    console.log(`  ${RED}Failed:${RESET}       ${allTotalFailed}`);
    console.log(`  ${YELLOW}Missing:${RESET}      ${allTotalMissing}`);
    console.log(`  ${BLUE}Total Verified:${RESET} ${allTotalVerified}`);
  }

  if (allTotalIncorrect > 0 || allTotalFailed > 0) {
    process.exit(1);
  } else {
    if (allTotalVerified > 0) {
      console.log(`\n${GREEN}All verified solutions are correct!${RESET}`);
    } else {
      console.log(`\n${YELLOW}No solutions were verified.${RESET}`);
    }
  }
}

main().catch((error) => {
  console.error(`${RED}Fatal error: ${error.message}${RESET}`);
  process.exit(1);
});
