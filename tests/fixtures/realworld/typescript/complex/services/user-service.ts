/**
 * User management service with business logic and validation.
 * @module services/user-service
 */

import { Email, UserRole, Address, validateEmail, PaginatedResponse, paginate } from '../../easy/types';
import { User, AdminUser } from '../models/user';
import { InMemoryRepository } from '../utils/db';
import { randomString } from '../../easy/helpers';

/**
 * Decorator that logs method invocations to the console.
 */
function Logged(target: unknown, propertyKey: string, descriptor: PropertyDescriptor): void {
  const original = descriptor.value;
  descriptor.value = function (...args: unknown[]) {
    console.log(`[UserService] ${propertyKey} called with`, args);
    return original.apply(this, args);
  };
}

/**
 * Dependency injection decorator stub.
 */
function Injectable(): (target: new (...args: unknown[]) => unknown) => void {
  return (target: new (...args: unknown[]) => unknown) => {
    Reflect.defineMetadata('injectable', true, target);
  };
}

/**
 * Route decorator stub for controller methods.
 */
function Route(method: string, path: string): (target: unknown, propertyKey: string, descriptor: PropertyDescriptor) => void {
  return (target: unknown, propertyKey: string, descriptor: PropertyDescriptor): void => {
    Reflect.defineMetadata('route', { method, path }, descriptor.value);
  };
}

export interface CreateUserDto {
  email: string;
  name: string;
  role?: UserRole;
  address?: Address;
}

export interface UpdateUserDto {
  name?: string;
  role?: UserRole;
  address?: Address;
}

/**
 * Service layer encapsulating all user-related business logic.
 */
@Injectable()
export class UserService {
  private repo: InMemoryRepository<User>;

  constructor(repo?: InMemoryRepository<User>) {
    this.repo = repo ?? new InMemoryRepository<User>();
  }

  /**
   * Create a new user after validating input.
   * @param dto - User creation data.
   * @returns The newly created User entity.
   * @throws If email validation fails.
   */
  @Logged
  @Route('POST', '/api/users')
  createUser(dto: CreateUserDto): User {
    const email = validateEmail(dto.email);
    if (!email) {
      throw new Error(`Invalid email address: ${dto.email}`);
    }
    const id = `user_${randomString(12)}`;
    const role = dto.role ?? UserRole.USER;
    const user: User = role === UserRole.ADMIN
      ? new AdminUser(id, email, dto.name)
      : new User(id, email, dto.name, role, dto.address ?? null);
    this.repo.insert(user);
    return user;
  }

  /**
   * Retrieve a user by ID.
   * @param id - User identifier.
   * @returns The user, or undefined.
   */
  @Route('GET', '/api/users/:id')
  getUser(id: string): User | undefined {
    return this.repo.findById(id);
  }

  /**
   * List all users with optional pagination.
   * @param page - Page number (1-indexed).
   * @param pageSize - Items per page.
   * @returns Paginated list of users.
   */
  @Route('GET', '/api/users')
  listUsers(page: number = 1, pageSize: number = 20): PaginatedResponse<User> {
    const all = this.repo.findAll();
    return paginate(all, { page, pageSize });
  }

  /**
   * Update user fields.
   * @param id - User identifier.
   * @param dto - Fields to update.
   * @returns The updated user, or undefined if not found.
   */
  @Logged
  @Route('PATCH', '/api/users/:id')
  updateUser(id: string, dto: UpdateUserDto): User | undefined {
    return this.repo.update(id, dto as Partial<User>);
  }

  /**
   * Remove a user from the system.
   * @param id - User identifier.
   * @returns True if the user was deleted.
   */
  @Route('DELETE', '/api/users/:id')
  deleteUser(id: string): boolean {
    return this.repo.delete(id);
  }

  /**
   * Find users matching a role.
   * @param role - Target role.
   * @returns Array of users with the given role.
   */
  findUsersByRole(role: UserRole): User[] {
    return this.repo.findWhere((u) => u.role === role);
  }
}
