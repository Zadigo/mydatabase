package app

type BaseErrors struct {}

func (b *BaseErrors) InternalServerError() string {
	return "Internal server error"
}

func (b *BaseErrors) NotFound() string {
	return "Resource not found"
}

func (b *BaseErrors) BadRequest() string {
	return "Bad request"
}

func (b *BaseErrors) Unauthorized() string {
	return "Unauthorized"
}

func (b *BaseErrors) Forbidden() string {
	return "Forbidden"
}
func (b *BaseErrors) Conflict() string {
	return "Conflict"
}

func (b *BaseErrors) UnprocessableEntity() string {
	return "Unprocessable entity"
}

func (b *BaseErrors) ServiceUnavailable() string {
	return "Service unavailable"
}

func (b *BaseErrors) GatewayTimeout() string {
	return "Gateway timeout"
}

func (b *BaseErrors) Send(text string) string {
	return ""
}
