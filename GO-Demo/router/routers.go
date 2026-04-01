package router

import (
	"fmt"

	"gin-ranking/controllers"
	"gin-ranking/logger"
	"gin-ranking/middleware"
	"net/http"

	"github.com/gin-gonic/gin"
)

func Rrouters() *gin.Engine {
	r := gin.Default()
	// 注册全局 recover 中间件
	r.Use(logger.RecoverMiddleware())
	// 注入请求级 DB
	r.Use(middleware.DBMiddleware())

	r.GET("/ping", func(c *gin.Context) {

		c.String(200, fmt.Sprintf("pong"))
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	r.GET("/order/info", controllers.OrderController{}.GetOrderInfo)

	user := r.Group("/user")
	{
		user.POST("/list", func(s *gin.Context) {
			s.String(200, fmt.Sprintf("pong"))
		})

		user.POST("/login", controllers.UserController{}.Login)

		user.GET("/get", controllers.UserController{}.GetUserList)

		user.GET("/info/:id", controllers.UserController{}.GetUserInfo)

		user.POST("/add", controllers.UserController{}.Register)

		user.POST("/update/:id", controllers.UserController{}.UpdateUser)
	}
	return r

}
