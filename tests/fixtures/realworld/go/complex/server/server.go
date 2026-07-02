// Package server provides an HTTP API server skeleton with route registration.
package server

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/okfgen/go-service/handlers"
	"github.com/okfgen/go-service/store"
)

// Server wraps an http.Server with route handlers and middleware.
type Server struct {
	httpServer *http.Server
	userStore  *store.UserStore
	mux        *http.ServeMux
}

// NewServer creates a new Server with the given store and default routes.
func NewServer(userStore *store.UserStore) *Server {
	s := &Server{
		userStore: userStore,
		mux:       http.NewServeMux(),
	}
	s.registerRoutes()
	return s
}

// registerRoutes attaches all API endpoints to the mux.
func (s *Server) registerRoutes() {
	s.mux.HandleFunc("GET /api/users", s.wrap(handlers.ListUsers(s.userStore)))
	s.mux.HandleFunc("GET /api/users/{id}", s.wrap(handlers.GetUser(s.userStore)))
	s.mux.HandleFunc("POST /api/users", s.wrap(handlers.CreateUser(s.userStore)))
}

// wrap applies common middleware (logging, JSON content-type) to a handler.
func (s *Server) wrap(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		w.Header().Set("Content-Type", "application/json")
		next(w, r)
		fmt.Printf("[%s] %s %s (%v)\n", r.Method, r.URL.Path, r.RemoteAddr, time.Since(start))
	}
}

// Listen starts the HTTP server on the given address.
func (s *Server) Listen(addr string) error {
	s.httpServer = &http.Server{
		Addr:         addr,
		Handler:      s.mux,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}
	return s.httpServer.ListenAndServe()
}

// jsonResponse writes a JSON-encoded response with the given status code.
func jsonResponse(w http.ResponseWriter, status int, data any) {
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}
