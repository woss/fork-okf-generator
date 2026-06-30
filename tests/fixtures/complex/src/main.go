package main

import (
	"fmt"
	"time"
)

// User represents a registered user.
type User struct {
	ID        int
	Email     string
	CreatedAt time.Time
}

// NewUser creates a new User with the given email.
func NewUser(id int, email string) *User {
	return &User{ID: id, Email: email, CreatedAt: time.Now()}
}

// Greet returns a greeting string for the user.
func (u *User) Greet() string {
	return fmt.Sprintf("Hello, %s!", u.Email)
}
