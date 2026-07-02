use serde::Serialize;
use std::collections::HashMap;

use crate::models::user::{Paginated, User};

/// Generic repository trait for entities that can be serialized.
pub trait Repository<T: Serialize> {
    /// Insert a new entity into the repository.
    fn insert(&mut self, entity: T) -> String;
    /// Retrieve an entity by its ID.
    fn get(&self, id: &str) -> Option<&T>;
    /// Delete an entity by its ID.
    fn delete(&mut self, id: &str) -> bool;
    /// Return the number of entities stored.
    fn count(&self) -> usize;
}

/// In-memory implementation of `Repository` for `User` entities.
pub struct UserRepository {
    users: HashMap<String, User>,
}

impl UserRepository {
    /// Create a new empty UserRepository.
    pub fn new() -> Self {
        UserRepository {
            users: HashMap::new(),
        }
    }

    /// List all users with pagination.
    pub fn list_paginated(&self, page: u64, page_size: u64) -> Paginated<&User>
    where
        User: Serialize,
    {
        let all: Vec<&User> = self.users.values().collect();
        let total = all.len() as u64;
        let start = ((page.saturating_sub(1)) * page_size) as usize;
        let items: Vec<&User> = all.into_iter().skip(start).take(page_size as usize).collect();
        Paginated::new(items, total, page, page_size)
    }
}

impl Repository<User> for UserRepository {
    fn insert(&mut self, user: User) -> String {
        let id = user.id.clone();
        self.users.insert(id.clone(), user);
        id
    }

    fn get(&self, id: &str) -> Option<&User> {
        self.users.get(id)
    }

    fn delete(&mut self, id: &str) -> bool {
        self.users.remove(id).is_some()
    }

    fn count(&self) -> usize {
        self.users.len()
    }
}

impl Default for UserRepository {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insert_and_get_user() {
        let mut repo = UserRepository::new();
        let user = User::new("alice@test.com", Some("Alice"));
        let id = repo.insert(user);
        let fetched = repo.get(&id);
        assert!(fetched.is_some());
        assert_eq!(fetched.unwrap().email, "alice@test.com");
    }
}
