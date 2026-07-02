/**
 * In-memory database abstraction layer with generic CRUD operations.
 * @module utils/db
 */

/**
 * Generic database collection interface.
 * @typeParam T - Entity type, must have an `id` field.
 */
export interface Repository<T extends { id: string }> {
  findById(id: string): T | undefined;
  findAll(): T[];
  insert(entity: T): T;
  update(id: string, partial: Partial<T>): T | undefined;
  delete(id: string): boolean;
}

/**
 * In-memory implementation of the Repository interface.
 * @typeParam T - Entity type with string `id`.
 */
export class InMemoryRepository<T extends { id: string }> implements Repository<T> {
  private items: Map<string, T> = new Map();

  findById(id: string): T | undefined {
    return this.items.get(id);
  }

  findAll(): T[] {
    return Array.from(this.items.values());
  }

  insert(entity: T): T {
    this.items.set(entity.id, entity);
    return entity;
  }

  update(id: string, partial: Partial<T>): T | undefined {
    const existing = this.items.get(id);
    if (!existing) return undefined;
    const updated = { ...existing, ...partial, id } as T;
    this.items.set(id, updated);
    return updated;
  }

  delete(id: string): boolean {
    return this.items.delete(id);
  }

  /**
   * Count the number of entities in the collection.
   * @returns Entity count.
   */
  count(): number {
    return this.items.size;
  }

  /**
   * Find entities matching a predicate.
   * @param predicate - Filter function.
   * @returns Matching entities.
   */
  findWhere(predicate: (item: T) => boolean): T[] {
    return Array.from(this.items.values()).filter(predicate);
  }
}
