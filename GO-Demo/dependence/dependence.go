package dependence

import (
	"errors"
	"fmt"

	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v4"

	"gin-ranking/config"
	"gin-ranking/dao"
	"gin-ranking/models"
)

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

	settings := config.LoadSettings()
	if settings.JWTSecret == "" {
		return zero, errors.New("JWT_SECRET not set")
	}
	method := settings.JWTMethod
	if method == "" {
		return zero, errors.New("JWT_METHOD not set")
	}

	token, err := jwt.ParseWithClaims(tokenString, jwt.MapClaims{}, func(token *jwt.Token) (interface{}, error) {
		// 校验 token 使用的算法与配置一致，防止 alg 攻击
		expected := jwt.GetSigningMethod(method)
		if expected == nil {
			return nil, fmt.Errorf("unsupported signing method configured: %s", method)
		}
		if token.Method.Alg() != expected.Alg() {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(settings.JWTSecret), nil
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
	if err := dao.GetDB().First(&user, uid).Error; err != nil {
		return zero, err
	}

	return user, nil
}

// createToken 根据环境配置生成带过期时间的 JWT
func CreateToken(userID uint) (string, error) {
	settings := config.LoadSettings()
	if settings.JWTSecret == "" {
		return "", errors.New("JWT_SECRET not set")
	}
	if settings.JWTMethod == "" {
		return "", errors.New("JWT_METHOD not set")
	}
	expires, _ := strconv.Atoi(settings.JWTExpire)
	method := settings.JWTMethod

	now := time.Now()
	claims := jwt.MapClaims{
		"user_id": userID,
		"iat":     now.Unix(),
		"exp":     now.Add(time.Duration(expires) * time.Second).Unix(),
	}

	signingMethod := jwt.GetSigningMethod(method)
	if signingMethod == nil {
		return "", fmt.Errorf("unsupported signing method configured: %s", method)
	}

	token := jwt.NewWithClaims(signingMethod, claims)
	return token.SignedString([]byte(settings.JWTSecret))
}
