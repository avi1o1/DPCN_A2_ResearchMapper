// Stand-in for chrome://resources/js/assert.js (only assert() is imported).
export function assert(value, message) {
  if (!value) {
    throw new Error('Assertion failed' + (message ? `: ${message}` : ''));
  }
}
