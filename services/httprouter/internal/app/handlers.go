package app

import (
	"log"
	"net/http"

	"github.com/Zadigo/httprouter/internal/app/middlewares"
	"github.com/Zadigo/httprouter/internal/models"
	"github.com/gorilla/websocket"
)

// BaseRoutes provides default handlers that will
// be used to handle the incoming HTTP requests to the
// the Django database endpoints
type BaseRoutes struct {}

// Returns information about the database.
func (b *BaseRoutes) GetInformation(w http.ResponseWriter, r *http.Request) {
}

// Get a resource from the database.
func (b *BaseRoutes) Get(w http.ResponseWriter, r *http.Request) {
}

// Create a new resource in the database.
func (b *BaseRoutes) Post(w http.ResponseWriter, r *http.Request) {
}

// Update an existing resource in the database.
func (b *BaseRoutes) Put(w http.ResponseWriter, r *http.Request) {
}

// Partially update an existing resource in the database.
func (b *BaseRoutes) Patch(w http.ResponseWriter, r *http.Request) {
}

// Delete a resource from the database.
func (b *BaseRoutes) Delete(w http.ResponseWriter, r *http.Request) {
}

// Create a real-time connection to the database.
func (b *BaseRoutes) Connect(w http.ResponseWriter, r *http.Request) {
	upgrader := websocket.Upgrader{}
	conn, err := upgrader.Upgrade(w, r, nil)

	if err != nil {
		http.Error(w, "Failed to establish websocket connection", http.StatusInternalServerError)
		return
	}
	
	defer func() {
		conn.Close()
	}()

	middlewares.WsMiddleware(conn)

	for {
		var message models.WebsocketMessage
		err = conn.ReadJSON(&message)

		if err != nil {
			log.Println("❌ Read error:", err)
			break
		}
	}
}
