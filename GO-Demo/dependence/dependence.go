package dependence

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v4"
	"gorm.io/gorm"

	"gin-ranking/dao"
	"gin-ranking/models"
)

// getDB 返回全局数据库连接
func getDB() *gorm.DB {
	// dao.Db 是 *gorm.DB，直接返回即可
	return dao.Db
}

// getCurrentUser 从 Authorization: Bearer <token> 中解析 JWT，返回当前用户
func getCurrentUser(c *gin.Context) (models.User, error) {
	var zero models.User
	auth := c.GetHeader("Authorization")
	if auth == "" {
		return zero, errors.New("authorization header empty")
	}

	// 支持 "Bearer <token>" 格式
	var tokenString string
	if len(auth) > 7 && auth[:7] == "Bearer " {
		tokenString = auth[7:]
	} else {
		tokenString = auth
	}

	// 从环境读取签名密钥与签名算法，避免硬编码
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		return zero, errors.New("JWT_SECRET not set")
	}

	method := os.Getenv("JWT_METHOD")

	token, err := jwt.ParseWithClaims(tokenString, jwt.MapClaims{}, func(token *jwt.Token) (interface{}, error) {
		// 校验 token 使用的算法与配置一致，防止 alg 攻击
		expected := jwt.GetSigningMethod(method)
		if expected == nil {
			return nil, fmt.Errorf("unsupported signing method configured: %s", method)
		}
		if token.Method.Alg() != expected.Alg() {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(secret), nil
	})
	if err != nil || !token.Valid {
		return zero, errors.New("invalid token")
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		return zero, errors.New("invalid token claims")
	}

	// 期望 claims 中包含 user_id 字段
	uidVal, ok := claims["user_id"]
	if !ok {
		return zero, errors.New("user_id not found in token")
	}

	// jwt 解码后数字通常为 float64
	var uid uint
	switch v := uidVal.(type) {
	case float64:
		uid = uint(v)
	case int:
		uid = uint(v)
	case uint:
		uid = v
	default:
		return zero, errors.New("invalid user_id type in token")
	}

	var user models.User
	if err := dao.Db.First(&user, uid).Error; err != nil {
		return zero, err
	}

	return user, nil
}

// createToken 根据环境配置生成带过期时间的 JWT
func CreateToken(userID uint) (string, error) {
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		return "", errors.New("JWT_SECRET not set")
	}

	method := os.Getenv("JWT_METHOD")
	if method == "" {
		return "", errors.New("JWT_METHOD not set")
	}

	// 读取过期时间（秒），支持数字字符串，若有解析错误则使用默认 3600
	expSec := os.Getenv("JWT_EXPIRE")
	expire, _ := strconv.Atoi(expSec)

	now := time.Now()
	claims := jwt.MapClaims{
		"user_id": userID,
		"iat":     now.Unix(),
		"exp":     now.Add(time.Duration(expire) * time.Second).Unix(),
	}

	signingMethod := jwt.GetSigningMethod(method)
	if signingMethod == nil {
		return "", fmt.Errorf("unsupported signing method configured: %s", method)
	}

	token := jwt.NewWithClaims(signingMethod, claims)
	return token.SignedString([]byte(secret))
}
