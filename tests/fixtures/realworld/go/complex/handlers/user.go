// Package handlers provides HTTP handler functions for user endpoints.
package handlers

import (
	"encoding/json"
	"net/http"

	"github.com/okfgen/go-service/store"
)

// ListUsers returns an HTTP handler that lists all users from the store.
func ListUsers(s *store.UserStore) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		users, err := s.List()
		if err != nil {
			http.Error(w, `{"error":"failed to list users"}`, http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]any{"users": users, "count": len(users)})
	}
}

// GetUser returns an HTTP handler that fetches a single user by ID.
func GetUser(s *store.UserStore) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		id := r.PathValue("id")
		user, err := s.Get(id)
		if err != nil {
			http.Error(w, `{"error":"user not found"}`, http.StatusNotFound)
			return
		}
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(user)
	}
}

// CreateUser returns an HTTP handler that creates a new user.
func CreateUser(s *store.UserStore) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var input store.CreateUserInput
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
			return
		}
		user, err := s.Create(input)
		if err != nil {
			http.Error(w, `{"error":"`+err.Error()+`"}`, http.StatusBadRequest)
			return
		}
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(user)
	}
}
