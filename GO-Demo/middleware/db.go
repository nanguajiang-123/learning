package middleware

import (
    "gin-ranking/dao"

    "github.com/gin-gonic/gin"
    "gorm.io/gorm"
)

const dbContextKey = "DB"

// DBMiddleware injects a request-scoped *gorm.DB into gin.Context.
func DBMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        db := dao.GetDB().WithContext(c.Request.Context())
        c.Set(dbContextKey, db)
        c.Next()
    }
}

// GetDB returns the request-scoped *gorm.DB if middleware is installed.
func GetDB(c *gin.Context) *gorm.DB {
    if val, ok := c.Get(dbContextKey); ok {
        if db, ok2 := val.(*gorm.DB); ok2 {
            return db
        }
    }
    return nil
}

// ResolveDB returns the request-scoped *gorm.DB if middleware is enabled;
// otherwise it falls back to the global pool bound to the request context.
func ResolveDB(c *gin.Context) *gorm.DB {
    if db := GetDB(c); db != nil {
        return db
    }
    return dao.GetDB().WithContext(c.Request.Context())
}
