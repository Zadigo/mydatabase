package app

import (
	"context"
	"log"
	"net/http"

	"github.com/go-chi/chi/v5"
)

type HttpApp struct {
	ctx context.Context
	router *chi.Mux
	errCh chan error
}

func (h *HttpApp) Start() {
	log.Println("Starting HTTP server...")

	if h.router == nil {
		log.Fatal("Server is nil. Call NewHttpApp to initialize the server")
	}

	go func() {
		log.Println("HTTP server is running on :8000")
		h.errCh <- http.ListenAndServe(":8000", h.router)
	}()

	select {
	case err := <-h.errCh:
		if err != nil {
			panic(err)
		}
	case <-h.ctx.Done():
		close(h.errCh)
		return
	}
}

func NewHttpApp(ctx context.Context) *HttpApp {
	app := &HttpApp{
		ctx: ctx,
		router: nil,
		errCh: make(chan error),
	}
	app.loadRoutes()
	return app
}
