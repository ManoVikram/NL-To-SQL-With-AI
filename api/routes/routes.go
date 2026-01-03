package routes

import (
	"github.com/ManoVikram/NL-To-SQL-With-AI/api/handlers"
	"github.com/ManoVikram/NL-To-SQL-With-AI/api/services"
	"github.com/gin-gonic/gin"
)

func RegisterRoutes(server *gin.Engine, services *services.Service) {
	server.POST("api/query", handlers.QueryHandler(services))
}
