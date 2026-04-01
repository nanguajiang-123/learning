package config

import (
	"os"
	"sync"

	"github.com/joho/godotenv"
)

// Settings exposes environment-driven configuration for the application.
type Settings struct {
	DBHost     string
	DBPort     string
	DBUser     string
	DBPassword string
	DBName     string
	DBSSLMode  string
	DBTimeZone string

	JWTSecret string
	JWTMethod string
	JWTExpire string

	PasswordHash string

	RedisHost     string
	RedisDB       string
	RedisPassword string
	RedisPort     string

	AppName  string
	AppEnv   string
	Debug    string
	LogLevel string
	LogDir   string

	APIHost string
	APIPort string
}

var (
	cached Settings
	once   sync.Once
)

// LoadSettings reads .env (if present) and caches all configuration values.
func LoadSettings() Settings {
	once.Do(func() {
		_ = godotenv.Load()
		cached = Settings{
			DBHost:        os.Getenv("DB_HOST"),
			DBPort:        os.Getenv("DB_PORT"),
			DBUser:        os.Getenv("DB_USER"),
			DBPassword:    os.Getenv("DB_PASSWORD"),
			DBName:        os.Getenv("DB_NAME"),
			DBSSLMode:     os.Getenv("DB_SSLMODE"),
			DBTimeZone:    os.Getenv("DB_TIMEZONE"),
			JWTSecret:     os.Getenv("JWT_SECRET"),
			JWTMethod:     os.Getenv("JWT_METHOD"),
			JWTExpire:     os.Getenv("JWT_EXPIRE"),
			PasswordHash:  os.Getenv("PASSWORD_HASH"),
			RedisPassword: os.Getenv("REDIS_PASSWORD"),
			RedisDB:       os.Getenv("REDIS_DB"),
			RedisPort:     os.Getenv("REDIS_PORT"),
			RedisHost:     os.Getenv("REDIS_HOST"),
			AppName:       os.Getenv("APP_NAME"),
			AppEnv:        os.Getenv("APP_ENV"),
			Debug:         os.Getenv("DEBUG"),
			LogLevel:      os.Getenv("LOG_LEVEL"),
			LogDir:        os.Getenv("LOG_DIR"),
			APIHost:       os.Getenv("API_HOST"),
			APIPort:       os.Getenv("API_PORT"),
		}
	})
	return cached
}
