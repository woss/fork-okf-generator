/**
 * Core type definitions for the utility library.
 * @module types
 */

/** ISO 8601 date string format. */
export type ISODateString = string;

/** Email address represented as a branded type. */
export type Email = string & { __brand: 'Email' };

/** Generic pagination parameters. */
export interface PaginationParams {
  page: number;
  pageSize: number;
}

/** Generic paginated response wrapper. */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

/** Sort direction enumeration. */
export enum SortDirection {
  ASC = 'asc',
  DESC = 'desc',
}

/** A generic API response wrapper. */
export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
  timestamp: ISODateString;
}

/** User role within the system. */
export enum UserRole {
  ADMIN = 'admin',
  MODERATOR = 'moderator',
  USER = 'user',
}

/** Address value object. */
export interface Address {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}
