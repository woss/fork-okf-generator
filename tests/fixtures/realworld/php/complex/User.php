<?php

namespace App\Models;

use App\Utils\Logger;

class User {
    private int $id;
    private string $username;
    private array $roles = [];

    public function __construct(int $id, string $username) {
        $this->id = $id;
        $this->username = $username;
    }

    public function getId(): int { return $this->id; }
    public function getUsername(): string { return $this->username; }
    public function addRole(string $role): void {
        if (!in_array($role, $this->roles)) {
            $this->roles[] = $role;
        }
    }
    public function hasRole(string $role): bool { return in_array($role, $this->roles); }
}

interface LoggerInterface {
    public function log(string $message): void;
    public function error(string $message): void;
}

trait Cacheable {
    private array $cache = [];
    public function getFromCache(string $key): mixed {
        return $this->cache[$key] ?? null;
    }
}

enum AccountStatus: string {
    case ACTIVE = 'active';
    case INACTIVE = 'inactive';
    case BANNED = 'banned';
}
