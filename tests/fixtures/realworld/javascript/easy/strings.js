/**
 * String manipulation utilities.
 * @module strings
 */

/**
 * Capitalize the first letter of each word in a string.
 * @param {string} str - Input text.
 * @returns {string} Title-cased text.
 */
function toTitleCase(str) {
  if (!str) return '';
  return str.replace(/\w\S*/g, (word) => {
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  });
}

/**
 * Truncate a string to a maximum length, appending an ellipsis if truncated.
 * @param {string} str - Input text.
 * @param {number} [maxLength=80] - Maximum allowed length.
 * @param {string} [ellipsis='...'] - Suffix appended when truncated.
 * @returns {string} Truncated string.
 */
function truncate(str, maxLength = 80, ellipsis = '...') {
  if (!str || str.length <= maxLength) return str || '';
  return str.slice(0, maxLength - ellipsis.length) + ellipsis;
}

/**
 * Convert a camelCase string to snake_case.
 * @param {string} str - Input in camelCase.
 * @returns {string} snake_case version.
 */
function camelToSnake(str) {
  return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

/**
 * Test whether a string is a valid email address (simple check).
 * @param {string} str - String to test.
 * @returns {boolean} True if the string looks like an email.
 */
function isValidEmail(str) {
  if (!str) return false;
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(str);
}

/**
 * Count the number of occurrences of a substring within a string.
 * @param {string} str - The haystack.
 * @param {string} substr - The needle.
 * @returns {number} Occurrence count.
 */
function countOccurrences(str, substr) {
  if (!str || !substr) return 0;
  let count = 0;
  let pos = 0;
  while ((pos = str.indexOf(substr, pos)) !== -1) {
    count++;
    pos += substr.length;
  }
  return count;
}

/**
 * Pad a number with leading zeros to a given width.
 * @param {number} num - The number to pad.
 * @param {number} [width=3] - Total character width.
 * @returns {string} Zero-padded string.
 */
function padZero(num, width = 3) {
  return String(num).padStart(width, '0');
}

module.exports = { toTitleCase, truncate, camelToSnake, isValidEmail, countOccurrences, padZero };
