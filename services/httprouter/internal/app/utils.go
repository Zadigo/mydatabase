package app

import (
	"sync"

	"github.com/Zadigo/httprouter/internal/models"
)

type ConnectedClients struct {
	clients map[string]*models.WebsocketClientInterface
	mu      sync.Mutex
}

func NewConnectedClients() *ConnectedClients {
	return &ConnectedClients{
		clients: make(map[string]*models.WebsocketClientInterface),
	}
}

func (c *ConnectedClients) AddClient(client *models.WebsocketClientInterface) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.clients[(*client).GetUuid()] = client
}

func (c *ConnectedClients) RemoveClient(uuid string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	delete(c.clients, uuid)
}

func (c *ConnectedClients) GetClient(uuid string) (*models.WebsocketClientInterface, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()
	client, exists := c.clients[uuid]
	if exists {
		return client, true
	}
	return nil, false
}
