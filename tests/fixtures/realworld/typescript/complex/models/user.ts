/**
 * User domain model for the user management service.
 * @module models/user
 */

import { Email, UserRole, Address } from '../../easy/types';

/**
 * Core user entity stored in the database.
 */
export class User {
  public readonly id: string;
  public readonly email: Email;
  public name: string;
  public role: UserRole;
  public address: Address | null;
  private _passwordHash: string;
  protected createdAt: Date;
  protected updatedAt: Date;

  constructor(
    id: string,
    email: Email,
    name: string,
    role: UserRole = UserRole.USER,
    address: Address | null = null,
  ) {
    this.id = id;
    this.email = email;
    this.name = name;
    this.role = role;
    this.address = address;
    this._passwordHash = '';
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }

  /**
   * Set the user's password by storing a bcrypt-style hash.
   * @param hash - Pre-computed password hash.
   */
  public setPasswordHash(hash: string): void {
    this._passwordHash = hash;
    this.updatedAt = new Date();
  }

  /**
   * Check whether the user has administrative privileges.
   * @returns True if the user is an admin.
   */
  public isAdmin(): boolean {
    return this.role === UserRole.ADMIN;
  }

  /**
   * Serialize the user to a plain object, excluding the password hash.
   * @returns Public user data.
   */
  public toJSON(): Record<string, unknown> {
    return {
      id: this.id,
      email: this.email,
      name: this.name,
      role: this.role,
      address: this.address,
      createdAt: this.createdAt.toISOString(),
      updatedAt: this.updatedAt.toISOString(),
    };
  }
}

/**
 * Administrative user with additional system permissions.
 */
export class AdminUser extends User {
  public readonly permissions: string[];

  constructor(
    id: string,
    email: Email,
    name: string,
    permissions: string[] = ['read', 'write', 'delete', 'manage'],
  ) {
    super(id, email, name, UserRole.ADMIN);
    this.permissions = permissions;
  }

  /**
   * Grant an additional permission to this admin user.
   * @param permission - Permission string to add.
   */
  public grantPermission(permission: string): void {
    if (!this.permissions.includes(permission)) {
      this.permissions.push(permission);
    }
  }
}
