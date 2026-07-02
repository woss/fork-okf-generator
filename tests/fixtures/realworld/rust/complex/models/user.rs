use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// Represents a user in the system.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    pub id: String,
    pub email: String,
    pub display_name: Option<String>,
    pub active: bool,
}

impl User {
    /// Create a new User with an auto-generated UUID.
    pub fn new(email: &str, display_name: Option<&str>) -> Self {
        User {
            id: Uuid::new_v4().to_string(),
            email: email.to_string(),
            display_name: display_name.map(|s| s.to_string()),
            active: true,
        }
    }

    /// Deactivate this user account.
    pub fn deactivate(&mut self) {
        self.active = false;
    }
}

/// Generic paginated wrapper for list responses.
#[derive(Debug, Clone, Serialize)]
pub struct Paginated<T> {
    pub items: Vec<T>,
    pub total: u64,
    pub page: u64,
    pub page_size: u64,
}

impl<T> Paginated<T> {
    /// Create a new paginated response.
    pub fn new(items: Vec<T>, total: u64, page: u64, page_size: u64) -> Self {
        Paginated {
            items,
            total,
            page,
            page_size,
        }
    }
}

/// Possible states of an entity lifecycle.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum EntityStatus {
    Active,
    Inactive,
    Archived,
}
