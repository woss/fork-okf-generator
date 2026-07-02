/**
 * Generic helper functions for data transformation.
 * @module helpers
 */

import { PaginatedResponse, PaginationParams, Email } from './types';

/**
 * Paginate an array of items in memory.
 * @param items - The full array to paginate.
 * @param params - Pagination parameters.
 * @returns A paginated response wrapper.
 */
export function paginate<T>(items: T[], params: PaginationParams): PaginatedResponse<T> {
  const { page, pageSize } = params;
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  const sliced = items.slice(start, end);
  return {
    items: sliced,
    total: items.length,
    page,
    pageSize,
    hasMore: end < items.length,
  };
}

/**
 * Validate an email string format and return a branded Email type.
 * @param value - Raw email string.
 * @returns The validated email, or null if invalid.
 */
export function validateEmail(value: string): Email | null {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!re.test(value)) return null;
  return value as Email;
}

/**
 * Deeply merge two objects, with source taking priority.
 * @typeParam T - Object type.
 * @param target - Base object.
 * @param source - Override values.
 * @returns A new merged object.
 */
export function deepMerge<T extends Record<string, unknown>>(
  target: T,
  source: Partial<T>,
): T {
  const result = { ...target };
  for (const key of Object.keys(source) as (keyof T)[]) {
    const srcVal = source[key];
    const tgtVal = target[key];
    if (
      srcVal !== null &&
      typeof srcVal === 'object' &&
      !Array.isArray(srcVal) &&
      tgtVal !== null &&
      typeof tgtVal === 'object' &&
      !Array.isArray(tgtVal)
    ) {
      result[key] = deepMerge(tgtVal as Record<string, unknown>, srcVal as Record<string, unknown>) as T[keyof T];
    } else if (srcVal !== undefined) {
      result[key] = srcVal as T[keyof T];
    }
  }
  return result;
}

/**
 * Generate a random alphanumeric string of a given length.
 * @param length - Desired string length.
 * @returns Random string.
 */
export function randomString(length: number): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * Retry an async function with exponential backoff.
 * @param fn - Async function to retry.
 * @param maxRetries - Maximum number of retry attempts.
 * @returns The function's return value.
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
): Promise<T> {
  let lastError: unknown;
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      if (attempt < maxRetries - 1) {
        await new Promise((r) => setTimeout(r, Math.pow(2, attempt) * 100));
      }
    }
  }
  throw lastError;
}
