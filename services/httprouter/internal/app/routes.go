package app

import (
	"time"

	"github.com/go-chi/chi/middleware"
	"github.com/go-chi/chi/v5"
)

func (h *HttpApp) loadRoutes() {
	router := chi.NewRouter()

	router.Use(middleware.RequestID)
	router.Use(middleware.RealIP)
	router.Use(Cors)
	router.Use(middleware.Logger)
	router.Use(middleware.Recoverer)
	router.Use(JsonHeartbeat("/health"))
	router.Use(middleware.Timeout(60 * time.Second))
	router.Use(Authorization)

	router.Route("/v1/", h.registerBaseRoutes)

	h.router = router
}

func (h *HttpApp) registerBaseRoutes(chiRouter chi.Router) {
	baseRoutes := &BaseRoutes{}
	chiRouter.Route("/{databaseUuid}", func(r chi.Router) {
		r.Use(DatabaseIdMiddleware)
		
		r.Get("/", baseRoutes.Get)
		r.Post("/", baseRoutes.Post)
		r.Put("/", baseRoutes.Put)
		r.Patch("/", baseRoutes.Patch)
		r.Delete("/", baseRoutes.Delete)
	})
}
