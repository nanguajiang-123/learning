package controllers

import (
	"errors"
	"fmt"

	"gin-ranking/core"
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

func (u UserController) Register(c *gin.Context) {
	email := c.PostForm("email")
	password := c.PostForm("password")
	id, err := models.AddUser(email, password)
	if err != nil {
		if errors.Is(err, models.ErrEmailExists) {
			ReturnError(c, 1, "邮箱已被注册")
			return
		}
		logrus.Errorf("register failed: %v", err)
		ReturnError(c, 1, "用户注册失败")
		return
	}
	logrus.Debugf("用户注册成功，ID: %d", id)
	ReturnSuccess(c, http.StatusOK, "用户注册成功", id)

}

func (u UserController) Login(c *gin.Context) {
	email := c.PostForm("email")
	password := c.PostForm("password")

	var user models.User
	db := middleware.ResolveDB(c)
	if err := db.Where("email = ?", email).First(&user).Error; err != nil {
		logrus.Debugf("login failed, user not found: %s", email)
		ReturnError(c, 1, "用户不存在或密码错误")
		return
	}

	if err := core.ComparePassword(user.Password, password); err != nil {
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
	// 使用中间件注入的请求级 DB；若未注入则回退到全局连接池
	db := middleware.ResolveDB(c)

	if err := db.Model(&models.User{}).Where("id = ?", id).Update("email", email).Error; err != nil {
		logrus.Errorf("更新用户失败，ID: %d, 错误: %v", id, err)
		ReturnError(c, 1, "更新用户失败")
		return
	}
	logrus.Debugf("更新用户成功，ID: %d", id)
	ReturnSuccess(c, http.StatusOK, "更新用户成功", id)
}

// LogoutUser validates JWT, checks the requested user id, then deletes related data.
func (u UserController) LogoutUser(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil || id <= 0 {
		logrus.Debugf("logout rejected: invalid user id, raw=%q", idStr)
		ReturnError(c, 1, "无效的用户ID")
		return
	}

	currentUser, err := dependence.GetCurrentUser(c)
	if err != nil {
		logrus.Debugf("logout rejected: jwt auth failed for id=%d, err=%v", id, err)
		ReturnError(c, 1, err.Error())
		return
	}

	if currentUser.ID != uint(id) {
		logrus.Debugf("logout rejected: token user mismatch, token_id=%d, req_id=%d", currentUser.ID, id)
		ReturnError(c, 1, "token 用户与请求用户不一致")
		return
	}

	db := middleware.ResolveDB(c)
	if db == nil {
		logrus.Debugf("logout rejected: db is nil for id=%d", id)
		ReturnError(c, 1, "数据库连接不可用")
		return
	}

	// 目前代码库中仅发现 users 与该 id 直接关联，这里先删除 users 记录。
	res := db.Where("id = ?", id).Delete(&models.User{})
	if res.Error != nil {
		logrus.Debugf("logout failed: delete user id=%d error=%v", id, res.Error)
		ReturnError(c, 1, fmt.Sprintf("注销失败: %v", res.Error))
		return
	}
	if res.RowsAffected == 0 {
		logrus.Debugf("logout failed: user id=%d not found", id)
		ReturnError(c, 1, "注销失败: user not found")
		return
	}

	logrus.Debugf("logout success: user id=%d", id)
	ReturnSuccess(c, http.StatusOK, "注销成功", gin.H{"user_id": id})
}
