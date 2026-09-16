package main

import (
	"context"

	"github.com/Zadigo/httprouter/internal/app"
)

func main() {
	ctx := context.Background()
	app := app.NewHttpApp(ctx)
	app.Start()
}
