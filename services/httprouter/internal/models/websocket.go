package models

import (
	"github.com/gorilla/websocket"
)

const (
	// A player requests to identify themselves
	MUST_IDENTIFY = "must_identify"
)

// WebsocketMessage represents a message sent
// over the websocket connection.
type BaseWebsocketMessage struct {
	Action  string `json:"action"`
	Message string `json:"message"`
}

type WebsocketMessage struct {
	BaseWebsocketMessage
}

type WebsocketClientInterface interface {
	GetUuid() string
	SetConn(conn *websocket.Conn)
	SendJsonMessage(message WebsocketMessage) error
	ReceiveJsonMessage() (WebsocketMessage, error)
}
