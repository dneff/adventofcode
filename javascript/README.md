# Advent of Code - JavaScript Solutions

JavaScript solutions for Advent of Code puzzles (2015-2024).

## Project Structure

```
javascript/
├── 2015/           # Solutions for year 2015
├── 2016/           # Solutions for year 2016
├── 2017/           # Solutions for year 2017
├── 2018/           # Solutions for year 2018
├── 2019/           # Solutions for year 2019
├── 2020/           # Solutions for year 2020
├── 2021/           # Solutions for year 2021
├── 2022/           # Solutions for year 2022
├── 2023/           # Solutions for year 2023
├── 2024/           # Solutions for year 2024
├── package.json    # Project configuration
├── eslint.config.js # ESLint configuration
└── .gitignore      # Git ignore rules
```

## Requirements

- Node.js >= 18.0.0
- npm (comes with Node.js)

## Getting Started

### Installation

```bash
# Navigate to the javascript directory
cd javascript

# Install dependencies
npm install
```

### Running Solutions

Solutions are organized by year and day:

```bash
# Run a specific solution
node 2015/01/solution1.js
node 2015/01/solution2.js
```

## Development

### Available Scripts

```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Lint code
npm run lint

# Lint and auto-fix issues
npm run lint:fix

# Format code
npm run format

# Check code formatting
npm run format:check
```

### Code Style

This project uses:
- **ESLint** for linting with ES2024 features
- **Prettier** for code formatting
- **Jest** for testing

Code style guidelines:
- Use ES6 modules (`import`/`export`)
- 2-space indentation
- Single quotes for strings
- Semicolons required
- Maximum line length: 120 characters
- Maximum complexity: 15

### Solution Pattern

Each day's solution should follow this structure:

```javascript
// YEAR/DAY/solution1.js
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function solve() {
  const input = readFileSync(join(__dirname, 'input.txt'), 'utf-8');
  // Solution logic here
  return result;
}

const answer = solve();
console.log(`Part 1: ${answer}`);
```

## Testing

Tests should be placed alongside solution files with a `.test.js` extension:

```javascript
// YEAR/DAY/solution1.test.js
import { describe, it, expect } from '@jest/globals';
import { solve } from './solution1.js';

describe('Year YEAR Day DAY - Part 1', () => {
  it('should solve example input', () => {
    const result = solve(exampleInput);
    expect(result).toBe(expectedAnswer);
  });
});
```

## Input Files

Input files are stored in each day's directory:
```
YEAR/DAY/
├── input.txt
├── solution1.js
└── solution2.js
```

## Contributing

When adding new solutions:
1. Follow the established directory structure
2. Include input files in the appropriate day directory
3. Run linting and formatting before committing
4. Add tests for non-trivial logic

## Resources

- [Advent of Code](https://adventofcode.com/)
- [Node.js Documentation](https://nodejs.org/docs/latest/api/)
- [ESLint Documentation](https://eslint.org/docs/latest/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
