package app

import (
	"context"
	"net/http"

	"github.com/go-chi/chi/v5"
)

// CORS middleware to handle cross-origin requests
func Cors(next http.Handler) http.Handler {
	fn := func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		origin := r.Header.Get("Origin")

		if _, ok := AllowedOrigins[origin]; !ok {
			http.Error(w, "Origin not allowed", http.StatusForbidden)
			return
		}

		next.ServeHTTP(w, r)
	}
	return http.HandlerFunc(fn)
}

// Authorization middleware to check for valid authorization header
func Authorization(next http.Handler) http.Handler {
	fn := func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")
		if authHeader == "" {
			// http.Error(w, "Unauthorized", http.StatusUnauthorized)
			// return
		}
		next.ServeHTTP(w, r)
	}
	return http.HandlerFunc(fn)
}

// DatabaseIdMiddleware is a middleware that retrieves the database ID
// from the URL parameters and adds it to the request context.
func DatabaseIdMiddleware(next http.Handler) http.Handler {
	fn := func(w http.ResponseWriter, r *http.Request) {
		databaseUuid := chi.URLParam(r, "databaseUuid")
		
		var ctx context.Context
		
		ctx = context.WithValue(r.Context(), "databaseUuid", databaseUuid)
		next.ServeHTTP(w, r.WithContext(ctx))
	}
	return http.HandlerFunc(fn)
}
