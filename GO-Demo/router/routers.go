package router

import (
	"gin-ranking/controllers"
	"gin-ranking/logger"
	"gin-ranking/middleware"

	"github.com/gin-gonic/gin"
)

func Rrouters() *gin.Engine {
	r := gin.Default()
	// 注册全局 recover 中间件
	r.Use(logger.RecoverMiddleware())
	// 注入请求级 DB
	r.Use(middleware.DBMiddleware())

	user := r.Group("/user")
	{

		user.POST("/login", controllers.UserController{}.Login)

		user.GET("/get", controllers.UserController{}.GetUserList)

		user.GET("/info/:id", controllers.UserController{}.GetUserInfo)

		user.POST("/register", controllers.UserController{}.Register)

		user.POST("/update/:id", controllers.UserController{}.UpdateUser)

		user.POST("/logout/:id", controllers.UserController{}.LogoutUser)

	}
	return r

}
