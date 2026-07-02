/**
 * Basic math utility functions.
 * @module math
 */

/**
 * Clamp a number between a minimum and maximum value.
 * @param {number} value - The value to clamp.
 * @param {number} min - Lower bound.
 * @param {number} max - Upper bound.
 * @returns {number} The clamped value.
 */
function clamp(value, min, max) {
  if (value < min) return min;
  if (value > max) return max;
  return value;
}

/**
 * Round a number to a specified number of decimal places.
 * @param {number} value - The value to round.
 * @param {number} [decimals=2] - Number of decimal places.
 * @returns {number} The rounded value.
 */
function roundTo(value, decimals = 2) {
  const factor = Math.pow(10, decimals);
  return Math.round(value * factor) / factor;
}

/**
 * Compute the arithmetic mean of an array of numbers.
 * @param {number[]} numbers - Array of numeric values.
 * @returns {number} The mean average.
 */
function average(numbers) {
  if (numbers.length === 0) return 0;
  return numbers.reduce((sum, n) => sum + n, 0) / numbers.length;
}

/**
 * Compute the standard deviation of a numeric array.
 * @param {number[]} numbers - Array of numeric values.
 * @returns {number} Population standard deviation.
 */
function standardDeviation(numbers) {
  if (numbers.length < 2) return 0;
  const avg = average(numbers);
  const variance = numbers.reduce((sum, n) => sum + Math.pow(n - avg, 2), 0) / numbers.length;
  return Math.sqrt(variance);
}

/**
 * Linear interpolation between two values.
 * @param {number} a - Start value.
 * @param {number} b - End value.
 * @param {number} t - Interpolation factor (0-1).
 * @returns {number} The interpolated value.
 */
function lerp(a, b, t) {
  return a + (b - a) * clamp(t, 0, 1);
}

/**
 * Check if a number is approximately equal to another within a tolerance.
 * @param {number} a - First number.
 * @param {number} b - Second number.
 * @param {number} [epsilon=1e-10] - Comparison tolerance.
 * @returns {boolean} True if the numbers are approximately equal.
 */
function approxEqual(a, b, epsilon = 1e-10) {
  return Math.abs(a - b) < epsilon;
}

module.exports = { clamp, roundTo, average, standardDeviation, lerp, approxEqual };
