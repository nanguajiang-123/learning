package logger

import (
	"io"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
	"gopkg.in/natefinch/lumberjack.v2"
)

func init() {
	// 设置最低日志等级，保证所有日志都能输出
	logrus.SetLevel(logrus.DebugLevel)
	// 控制台简洁彩色日志
	logrus.SetFormatter(&logrus.TextFormatter{
		ForceColors:     true,
		DisableQuote:    true,
		TimestampFormat: "2006-01-02 15:04:05",
		FullTimestamp:   true,
	})
	logrus.SetReportCaller(false)
	// 文件日志切割，10MB自动新建下一个文件
	logDir := filepath.Join("logger", "log")
	if _, err := os.Stat(logDir); os.IsNotExist(err) {
		os.MkdirAll(logDir, 0755)
	}
	fileLogger := &lumberjack.Logger{
		Filename:   filepath.Join(logDir, "app01.log"),
		MaxSize:    10, // 单位MB
		MaxBackups: 0,  // 不限制备份数量
		MaxAge:     0,  // 不限制天数
		Compress:   false,
	}
	logrus.SetOutput(io.MultiWriter(os.Stdout, fileLogger))
}

// 文件切割由 lumberjack 处理，无需自定义 getLogFile

func RecoverMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		defer func() {
			if err := recover(); err != nil {
				// 记录错误日志
				logrus.WithField("panic", err).Error("Recovered from panic")
				// 返回标准 JSON 错误响应
				c.JSON(500, gin.H{
					"code":  500,
					"msg":   "服务器内部错误",
					"error": err,
				})
				c.Abort()
			}
		}()
		c.Next()
	}
}
