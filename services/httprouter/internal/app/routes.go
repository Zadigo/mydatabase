package app

import (
	"time"

	custom_middlewares "github.com/Zadigo/httprouter/internal/app/middlewares"
	"github.com/go-chi/chi/middleware"
	"github.com/go-chi/chi/v5"
)

func (h *HttpApp) loadRoutes() {
	router := chi.NewRouter()

	router.Use(middleware.RequestID)
	router.Use(middleware.RealIP)
	router.Use(custom_middlewares.Cors)
	router.Use(middleware.AllowContentType("application/json"))
	router.Use(middleware.Throttle(1000))
	router.Use(middleware.Logger)
	router.Use(middleware.Recoverer)
	router.Use(custom_middlewares.JsonHeartbeat("/health"))
	router.Use(middleware.Timeout(60 * time.Second))
	router.Use(custom_middlewares.Authorization)

	router.Route("/v1/", h.registerBaseRoutes)

	h.router = router
}

func (h *HttpApp) registerBaseRoutes(chiRouter chi.Router) {
	baseRoutes := &BaseRoutes{}
	chiRouter.Route("/{databaseUuid}", func(r chi.Router) {
		r.Use(custom_middlewares.DatabaseIdMiddleware)
		
		r.Get("/", baseRoutes.Get)
		r.Post("/", baseRoutes.Post)
		r.Put("/", baseRoutes.Put)
		r.Patch("/", baseRoutes.Patch)
		r.Delete("/", baseRoutes.Delete)
	})
}
