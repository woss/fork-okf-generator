/**
 * TypeScript utility library.
 */

export interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

export class DataService<T> {
  private items: T[] = [];

  /** Add an item to the collection. */
  add(item: T): void {
    this.items.push(item);
  }

  /** Get all items. */
  getAll(): T[] {
    return [...this.items];
  }

  /** Find items by predicate. */
  find(predicate: (item: T) => boolean): T | undefined {
    return this.items.find(predicate);
  }
}

export function wrapResponse<T>(data: T): ApiResponse<T> {
  return { data, status: 200, message: "success" };
}
