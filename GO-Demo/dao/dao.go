package dao

import (
	"gin-ranking/config"

	"github.com/bytedance/gopkg/util/logger"
	"gorm.io/gorm"
)

var (
	Db  *gorm.DB
	err error
)

func GetDB() *gorm.DB {
	return Db
}
func init() {
	Db, err = config.InitDB()
	if err != nil {
		logger.Debug(map[string]interface{}{"mysql connet error": err.Error()})
	}
	if Db.Error != nil {
		logger.Debug(map[string]interface{}{"mysql connet error": Db.Error.Error()})
	}

}
