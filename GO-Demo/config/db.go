package config

import (
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func InitDB() (*gorm.DB, error) {
	setting := LoadSettings()
	dsn := fmt.Sprintf(
		"host=%s user=%s password=%s dbname=%s port=%s sslmode=%s TimeZone=%s",
		setting.DBHost,
		setting.DBUser,
		setting.DBPassword,
		setting.DBName,
		setting.DBPort,
		setting.DBSSLMode,
		setting.DBTimeZone,
	)

	db, err := gorm.Open(postgres.New(postgres.Config{
		DSN:                  dsn,
		PreferSimpleProtocol: true,
	}), &gorm.Config{})
	return db, err
}
