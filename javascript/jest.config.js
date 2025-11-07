/**
 * Jest configuration for ES6 modules
 */

export default {
  testEnvironment: 'node',
  transform: {},
  testMatch: ['**/test/**/*.test.js'],
  collectCoverageFrom: ['aoc-helpers.js', '!**/node_modules/**', '!**/test/**'],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
};
