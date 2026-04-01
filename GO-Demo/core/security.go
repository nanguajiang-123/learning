package core

import (
	"strings"

	"github.com/sirupsen/logrus"
	"golang.org/x/crypto/bcrypt"

	"gin-ranking/config"
)

var passwordHasher passwordHasherImpl

type passwordHasherImpl interface {
	Hash(password string) (string, error)
	Compare(hashed, password string) error
}

type bcryptHasher struct{}

func (bcryptHasher) Hash(password string) (string, error) {
	hashed, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	return string(hashed), err
}

func (bcryptHasher) Compare(hashed, password string) error {
	return bcrypt.CompareHashAndPassword([]byte(hashed), []byte(password))
}

func init() {
	settings := config.LoadSettings()
	algo := strings.ToLower(strings.TrimSpace(settings.PasswordHash))
	if algo == "" {
		logrus.Warn("PASSWORD_HASH not provided, defaulting to bcrypt")
		return
	}
	if algo == "bcrypt" {
		passwordHasher = bcryptHasher{}
		return
	}
	logrus.Warnf("unsupported PASSWORD_HASH=%s, defaulting to bcrypt", algo)

}

func HashPassword(password string) (string, error) {
	if passwordHasher == nil {
		passwordHasher = bcryptHasher{}
	}
	return passwordHasher.Hash(password)
}

func ComparePassword(hash, password string) error {
	if passwordHasher == nil {
		passwordHasher = bcryptHasher{}
	}
	return passwordHasher.Compare(hash, password)
}
