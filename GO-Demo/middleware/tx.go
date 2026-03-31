package middleware

import (
    "gin-ranking/dao"
    "net/http"

    "github.com/gin-gonic/gin"
    "gorm.io/gorm"
)

// LazyTxMiddleware 延迟创建事务：仅当 handler 通过 context 中提供的 getDB 函数请求时才 Begin()
func LazyTxMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        var tx *gorm.DB
        getDB := func() *gorm.DB {
            if tx == nil {
                tx = dao.Db.WithContext(c.Request.Context()).Begin()
            }
            return tx
        }

        c.Set("GetDB", getDB)

        c.Next()

        if tx == nil {
            return // 从未开启事务
        }

        if len(c.Errors) > 0 {
            _ = tx.Rollback().Error
            return
        }

        if err := tx.Commit().Error; err != nil {
            _ = tx.Rollback().Error
            c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"error": "db commit failed"})
            return
        }
    }
}

// GetLazyDB 从 context 返回延迟创建事务的函数（如果中间件未安装返回 nil）
func GetLazyDB(c *gin.Context) func() *gorm.DB {
    if val, ok := c.Get("GetDB"); ok {
        if f, ok2 := val.(func() *gorm.DB); ok2 {
            return f
        }
    }
    return nil
}
