package controllers

import (
	"gin-ranking/dao"
	"gin-ranking/dependence"
	"gin-ranking/middleware"
	"gin-ranking/models"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

type UserController struct{}

func (u UserController) GetUserInfo(c *gin.Context) {
	idstr := c.Param("id")

	id, _ := strconv.Atoi(idstr)

	user, _ := models.GetUserTest(id)
	logrus.Debugf("Received GetUserInfo request with id: %d ", id)
	ReturnSuccess(c, http.StatusOK, "获取用户信息成功", user)

}

func (u UserController) GetUserList(c *gin.Context) {
	// defer func() {
	// 	if err := recover(); err != nil {
	// 		fmt.Printf("发生了错误：%v\n", err)
	// 	}
	// }()
	var num3 int = 10
	logrus.Debugf("执行了 GetUserList 方法")
	ReturnSuccess(c, 10, num3, 111)
	// 其他正常逻辑

}

func (u UserController) AddUser(c *gin.Context) {
	email := c.PostForm("email")
	password := c.PostForm("password")
	id, err := models.AddUser(email, password)
	if err != nil {
		ReturnError(c, 1, "添加用户失败")
		return
	}
	logrus.Debugf("添加用户成功，ID: %d", id)
	ReturnSuccess(c, http.StatusOK, "添加用户成功", id)

}

func (u UserController) Login(c *gin.Context) {
	email := c.PostForm("email")
	password := c.PostForm("password")

	var user models.User
	if err := dao.Db.Where("email = ?", email).First(&user).Error; err != nil {
		logrus.Debugf("login failed, user not found: %s", email)
		ReturnError(c, 1, "用户不存在或密码错误")
		return
	}

	if user.Password != password {
		logrus.Debugf("login failed, invalid password for: %s", email)
		ReturnError(c, 1, "用户不存在或密码错误")
		return
	}

	token, err := dependence.CreateToken(user.ID)
	if err != nil {
		logrus.Errorf("create token failed: %v", err)
		ReturnError(c, 1, "生成 token 失败")
		return
	}

	ReturnSuccess(c, http.StatusOK, "登录成功", gin.H{"token": token})
}

func (u UserController) UpdateUser(c *gin.Context) {
	idstr := c.Param("id")
	email := c.PostForm("email")
	id, _ := strconv.Atoi(idstr)
	// 按需使用延迟事务：优先使用中间件提供的事务（写时才 Begin()），否则使用全局 DB
	db := dao.Db.WithContext(c.Request.Context())
	if getDB := middleware.GetLazyDB(c); getDB != nil {
		db = getDB()
	}

	if err := db.Model(&models.User{}).Where("id = ?", id).Update("email", email).Error; err != nil {
		logrus.Errorf("更新用户失败，ID: %d, 错误: %v", id, err)
		ReturnError(c, 1, "更新用户失败")
		return
	}
	logrus.Debugf("更新用户成功，ID: %d", id)
	ReturnSuccess(c, http.StatusOK, "更新用户成功", id)
}
