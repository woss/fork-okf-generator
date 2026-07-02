// Package store provides data access layer for user entities.
package store

import (
	"fmt"
	"sync"
	"time"
)

// User represents a user entity in the system.
type User struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
}

// CreateUserInput holds the fields required to create a new user.
type CreateUserInput struct {
	Name  string `json:"name"`
	Email string `json:"email"`
}

// UserStore provides thread-safe CRUD operations for User entities.
type UserStore struct {
	mu    sync.RWMutex
	users map[string]User
	next  int
}

// NewUserStore creates and returns a new empty UserStore.
func NewUserStore() *UserStore {
	return &UserStore{
		users: make(map[string]User),
		next:  1,
	}
}

// List returns all users in the store.
func (s *UserStore) List() ([]User, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	result := make([]User, 0, len(s.users))
	for _, u := range s.users {
		result = append(result, u)
	}
	return result, nil
}

// Get retrieves a single user by ID.
func (s *UserStore) Get(id string) (User, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	user, ok := s.users[id]
	if !ok {
		return User{}, fmt.Errorf("user %q not found", id)
	}
	return user, nil
}

// Create inserts a new user and returns it with an auto-generated ID.
func (s *UserStore) Create(input CreateUserInput) (User, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	id := fmt.Sprintf("u_%d", s.next)
	s.next++
	user := User{
		ID:        id,
		Name:      input.Name,
		Email:     input.Email,
		CreatedAt: time.Now().UTC(),
	}
	s.users[id] = user
	return user, nil
}

// Count is a generic helper that returns the number of items in a map.
func Count[K comparable, V any](m map[K]V) int {
	return len(m)
}
