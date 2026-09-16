package middlewares

import (
	"context"
	"net/http"

	"github.com/go-chi/chi"
)

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

