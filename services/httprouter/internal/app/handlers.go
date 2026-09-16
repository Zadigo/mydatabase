package app

import "net/http"

// BaseRoutes provides default handlers that will
// be used to handle the incoming HTTP requests to the
// the Django database endpoints
type BaseRoutes struct {}

func (b *BaseRoutes) Get(w http.ResponseWriter, r *http.Request) {
}

func (b *BaseRoutes) Post(w http.ResponseWriter, r *http.Request) {
}

func (b *BaseRoutes) Put(w http.ResponseWriter, r *http.Request) {
}

func (b *BaseRoutes) Patch(w http.ResponseWriter, r *http.Request) {
}

func (b *BaseRoutes) Delete(w http.ResponseWriter, r *http.Request) {
}
